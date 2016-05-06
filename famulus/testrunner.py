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
   famulus.testrunner
   ``````````````````

   Classes and helper functions to run suites


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .event import EventLogger, EventLoggerFormat
from gettext import gettext as _


class TestRunner:
    """Run suites"""
    def __init__(self):
        self.event_handler = EventLogger()

    def run(self, suite):
        """Run a suite.

        @param suite: suite to run
        @type suite: Suite
        """
        propagate_event_handler(suite, self.event_handler)
        return suite.run()


def propagate_event_handler(suite, event_handler):
    """Set the event handler for a suite and its inner tests/suites"""
    suite.event_handler = event_handler
    for t in suite.tests:
        t.event_handler = event_handler
    for s in suite.suites:
        propagate_event_handler(s, event_handler)


def create_test_runner(format):
    """Create a tailor-made test runner.

    @param format: event logger format as string
    @type format: string

    @return: a test runner
    @rtype: TestRunner
    """
    if format in [e.name for e in EventLoggerFormat]:
        format = EventLoggerFormat[format]
    else:
        ValueError(_("unsupported event logging format"))

    runner = TestRunner()
    runner.event_handler.format = format
    return runner


# vim: ts=4 sw=4 sts=4 et ai
