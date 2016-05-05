# -*- coding: utf-8 -*-
#
# This file is part of famulus
#
# Copyright (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
   famulus.event
   `````````````

   Classes and helper functions for events occuring during test/suite
   execution.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc
import sys
from datetime import datetime
from enum import Enum
from gettext import gettext as _


TestEvent = Enum('TestEvent', 'begin end failure success')


class BaseEventHandler:
    """Abstract base class for test/suite event handler."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, source, event, data=None):
        """Handle an event.

        @param source: source of the event
        @type source: BaseTest

        @param event: the event which occured
        @type event: TestEvent

        @param data: additional data
        @type data: any Python type
        """
        return


class DummyEventHandler(BaseEventHandler):
    """Dummy event handler"""

    def handle(self, source, event, data=None):
        pass


class HumanEventFormatter:
    """Format an event for a human"""

    def format(self, source, event, data):
        """Format the event.

        @param source: source of the event
        @type source: BaseTest

        @param event: the event which occured
        @type event: TestEvent

        @param data: additional data
        @type data: any Python type

        @return: event formatted as text
        @rtype: str
        """
        text = ""
        if type(source).__name__ == 'Suite':
            if source.name != 'root':
                if event == TestEvent.success:
                    text = "{:<48} [PASSED]\n".format(source.brief + "...")
                elif event == TestEvent.failure:
                    text = "{:<48} [FAILED]\n".format(source.brief + "...")
        else:
            if event == TestEvent.begin:
                text = "{:<48} ".format(source.brief + "...")
            elif event == TestEvent.failure:
                text = "[FAILED]"
            elif event == TestEvent.success:
                text = "[PASSED]"
            elif event == TestEvent.end:
                text = "\n"
        return text


class MachineEventFormatter:
    """Format an event for a machine"""

    def format(self, source, event, data):
        """Format the event.

        @param source: source of the event
        @type source: BaseTest

        @param event: the event which occured
        @type event: TestEvent

        @param data: additional data
        @type data: any Python type

        @return: event formatted as text
        @rtype: str
        """
        messages = {
            TestEvent.begin: (
                _("start"),
                source.brief,
            ),
            TestEvent.end: (
                _("end"),
                None,
            ),
            TestEvent.failure: (
                _("failure"),
                None,
            ),
            TestEvent.success: (
                _("success"),
                None,
            ),
        }
        msg, extra = messages[event]
        ts = datetime.now().isoformat()
        text = "{}: {}: {}".format(ts, source.name, msg)
        if extra:
            text += ": {}".format(extra)
        return text + '\n'


EventLoggerFormat = Enum('EventLoggerFormat', 'human machine')


class EventLogger(BaseEventHandler):
    """Log events to standard output.

    @param format: format for logging events
    @type format: EventLoggerFormat
    """
    def __init__(self, format=EventLoggerFormat.human):
        self._format = format

    @property
    def format(self):
        """Return the format used for logging events"""
        return self._format

    def handle(self, source, event, data=None):
        formatters = {
            EventLoggerFormat.human: HumanEventFormatter,
            EventLoggerFormat.machine: MachineEventFormatter,
        }
        klass = formatters[self.format]
        text = klass().format(source, event, data)
        sys.stdout.write(text)

# vim: ts=4 sw=4 sts=4 et ai
