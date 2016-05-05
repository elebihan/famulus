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
from datetime import datetime
from enum import Enum
from gettext import gettext as _


TestEvent = Enum('TestEvent', 'begin end')


class BaseEventHandler:
    """Abstract base class for test/suite event handler."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, source, event):
        """Handle an event.

        @param source: source of the event
        @type source: BaseTest

        @param event: the event which occured
        @type event: TestEvent
        """
        return


class DummyEventHandler(BaseEventHandler):
    """Dummy event handler"""

    def handle(self, source, event):
        pass


class EventLogger(BaseEventHandler):
    """Log events to standard output"""
    def __init__(self):
        pass

    def handle(self, source, event):
        messages = {
            TestEvent.begin: _("start"),
            TestEvent.end: _("end"),
        }
        ts = datetime.now().isoformat()
        text = "{}: {}: {}".format(ts, source.name, messages[event])
        print(text)

# vim: ts=4 sw=4 sts=4 et ai
