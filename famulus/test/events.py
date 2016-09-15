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
   famulus.test.events
   ```````````````````

   Classes and helper functions for events occuring during test/suite
   execution.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc
import sys
from colorama import Fore, Style
from datetime import datetime
from enum import Enum
from gettext import gettext as _


TestEvent = Enum('TestEvent',
                 'begin end failure success setup command teardown')


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


class EventFormatter:
    """Abstract base class for formatting an event"""
    def __init__(self, colored):
        self._colored = colored

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
        raise NotImplementedError

    def _colorize(self, text, color):
        if self._colored:
            return color + text + Style.RESET_ALL
        else:
            return text


class HumanEventFormatter(EventFormatter):
    """Format an event for a human"""

    def format(self, source, event, data):
        text = ""
        if type(source).__name__ == 'Suite':
            if source.name != 'root':
                if event == TestEvent.success:
                    text = "{:<48} [{}]\n".format(source.brief + "...",
                                                  self._colorize('PASSED',
                                                                 Fore.GREEN))
                elif event == TestEvent.failure:
                    text = "{:<48} [{}]\n".format(source.brief + "...",
                                                  self._colorize('FAILED',
                                                                 Fore.RED))
        else:
            if event == TestEvent.begin:
                text = "{:<48} ".format(source.brief + "...")
            elif event == TestEvent.failure:
                text = "[{}]".format(self._colorize('FAILED', Fore.RED))
            elif event == TestEvent.success:
                text = "[{}]".format(self._colorize('PASSED', Fore.GREEN))
            elif event == TestEvent.end:
                text = "\n"
        return text


class MachineEventFormatter(EventFormatter):
    """Format an event for a machine"""

    def format(self, source, event, data):
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
                self._colorize(_("failure"), Fore.RED),
                None,
            ),
            TestEvent.success: (
                self._colorize(_("success"), Fore.GREEN),
                None,
            ),
            TestEvent.command: (
                _("command"),
                None,
            ),
            TestEvent.setup: (
                _("setup"),
                None,
            ),
            TestEvent.teardown: (
                _("teardown"),
                None,
            ),
        }
        msg, extra = messages[event]
        ts = datetime.now().isoformat()
        text = "{}: {}: {}".format(ts, source.name, msg)
        if extra:
            text += ": {}".format(extra)
        return text + '\n'


class EventLoggerFormat(Enum):
    human, machine = (0, 1)

    @classmethod
    def parse(klass, string):
        if string in [e.name for e in klass]:
            return klass[string]
        raise ValueError(_("unsupported event logging format"))


class EventLogger(BaseEventHandler):
    """Log events to standard output"""
    def __init__(self, format=EventLoggerFormat.human):
        self._format = format

    @property
    def format(self):
        """Return the format used for logging events.

        @return: the format used for logging events
        @rtype: EventLoggerFormat
        """
        return self._format

    def handle(self, source, event, data=None):
        formatter = self._create_formatter()
        text = formatter.format(source, event, data)
        sys.stdout.write(text)

    def _create_formatter(self):
        formatters = {
            EventLoggerFormat.human: HumanEventFormatter,
            EventLoggerFormat.machine: MachineEventFormatter,
        }
        klass = formatters[self.format]
        return klass(sys.stdout.isatty())

# vim: ts=4 sw=4 sts=4 et ai
