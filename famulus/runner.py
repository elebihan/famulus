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
   famulus.runner
   ``````````````

   Classes and helper functions to run tests and suites


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import re
from .event import EventLogger, EventLoggerFormat, TestEvent
from .command import CommandRunner
from .result import TestResult, SuiteResult, TestStatus
from .time import Stopwatch
from .log import debug
from gettext import gettext as _


class ExpectationError(Exception):
    """Error raised when the result of a command does not meet expectation"""
    def __init__(self):
        Exception.__init__(self, _("Command result does not meet expectation"))


class BaseRunner:
    """Abstract base class for running tests or suites"""
    def __init__(self, cmd_runner, evt_handler):
        self._cmd_runner = cmd_runner
        self._event_handler = evt_handler
        self._stopwatch = Stopwatch()

    @property
    def stopwatch(self):
        """Return the stopwatch used"""
        return self._stopwatch

    @property
    def cmd_runner(self):
        """Return the command runner used"""
        return self._cmd_runner

    @property
    def event_handler(self):
        """Return the event handler used"""
        return self._event_handler

    def run(self):
        raise NotImplementedError

    def _notify_event(self, source, event, data=None):
        self.event_handler.handle(source, event, data)

    def _record_begin(self, source):
        self._stopwatch.start()
        self._notify_event(source, TestEvent.begin)

    def _record_end(self, source):
        self._stopwatch.stop()
        self._notify_event(source, TestEvent.end)


class TestRunner(BaseRunner):
    """Run a test"""
    def __init__(self, cmd_runner, evt_handler=EventLogger()):
        BaseRunner.__init__(self, cmd_runner, evt_handler)

    def run(self, test):
        """Run a test.

        @param test: the test to run
        @type test: Test

        @return: the result of the test
        @rtype: TestResult
        """
        debug(_("Running test {}").format(test.name))
        self._record_begin(test)
        self._run_setup(test)
        result = self._run_command(test)
        self._run_teardown(test)
        self._record_end(test)
        return result

    def _run_setup(self, test):
        self._notify_event(test, TestEvent.setup)
        for command in test.setup:
            self.cmd_runner.run(command)

    def _run_teardown(self, test):
        self._notify_event(test, TestEvent.teardown)
        for command in test.teardown:
            self.cmd_runner.run(command)

    def _run_command(self, test):
        self._notify_event(test, TestEvent.command)
        result = TestResult(test, TestStatus.passed)
        try:
            output = self.cmd_runner.run(test.command)
            self._check_output(test, output)
        except Exception as e:
            debug(_("Test failed ({})").format(e))
            result.status = TestStatus.failed
        event = TestEvent.success if result.is_success else TestEvent.failure
        self._notify_event(test, event)
        return result

    def _check_output(self, test, output):
        if test.expect:
            if not output or not re.match(test.expect, output):
                raise ExpectationError


class SuiteRunner(BaseRunner):
    """Run a suite"""
    def __init__(self, cmd_runner, evt_handler=EventLogger()):
        BaseRunner.__init__(self, cmd_runner, evt_handler)

    def run(self, suite):
        """Run a suite.

        Run all the tests in a suite, then all the child suites

        @param suite: suite to run
        @type suite: Suite

        @return: the result of the suite
        @rtype: SuiteResult
        """
        debug(_("Running suite {}").format(suite.name))
        self._record_begin(suite)
        result = SuiteResult(suite)
        for t in suite.tests:
            t_result = self._run_test(t)
            result.test_results.append(t_result)
        for s in suite.suites:
            s_result = self._run_suite(s)
            result.suite_results.append(s_result)
        event = TestEvent.success if result.is_success else TestEvent.failure
        self._notify_event(suite, event)
        self._record_end(suite)
        return result

    def _run_test(self, test):
        t_runner = TestRunner(self.cmd_runner, self.event_handler)
        return t_runner.run(test)

    def _run_suite(self, suite):
        s_runner = SuiteRunner(self.cmd_runner, self.event_handler)
        return s_runner.run(suite)


def create_suite_runner(uri, format):
    """Create a tailor-made suite runner.

    @param uri: URI of the target
    @type uri: str

    @param format: event logger format as string
    @type format: string

    @return: a suite runner
    @rtype: SuiteRunner
    """
    if format in [e.name for e in EventLoggerFormat]:
        format = EventLoggerFormat[format]
    else:
        ValueError(_("unsupported event logging format"))

    debug(_("URI (unused): {}").format(uri))

    runner = SuiteRunner(CommandRunner(uri), EventLogger(format))
    return runner


# vim: ts=4 sw=4 sts=4 et ai
