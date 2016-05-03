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
   famulus.test
   ````````````

   Classes and helper functions for tests and suites.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .log import debug
from .event import TestEvent, DummyEventHandler
from enum import Enum
from gettext import gettext as _


class BaseTest:
    """Base class for test/suite.

    @param name: name of the object
    @type name: str
    """
    def __init__(self, name):
        self._name = name
        self.author = _('Unknown')
        self.brief = _('No brief description available')
        self.description = _('No description available')
        self.event_handler = DummyEventHandler()

    @property
    def name(self):
        return self._name

    def run(self):
        raise NotImplementedError

    def _notify_event(self, event):
        self.event_handler.handle(event, self.name)


class Test(BaseTest):
    """Represent a test to run.

    @param name: name of test
    @type name: str

    @param command: command to execute
    @type command: str

    @param expect: expected text
    @type expect: str
    """
    def __init__(self, name, command, expect):
        BaseTest.__init__(self, name)
        self._command = command
        self._expect = expect
        self.setup = []
        self.teardown = []

    def run(self):
        """Run the test"""
        debug(_("Running test {}").format(self.name))
        self._notify_event(TestEvent.begin)
        result = TestResult()
        self._notify_event(TestEvent.end)
        return result


class Suite(BaseTest):
    """Represent a suite to run.

    @param name: name of suite
    @type name: str
    """
    def __init__(self, name):
        BaseTest.__init__(self, name)
        self._tests = []
        self._suites = []

    @property
    def tests(self):
        return self._tests

    @property
    def suites(self):
        return self._suites

    def add_test(self, test):
        """Add a test to the suite.

        @param test: a test to add to the suite
        @type test: Test
        """
        self._tests.append(test)

    def add_suite(self, suite):
        """Add a suite to the suite.

        @param suite: a suite to add to the suite
        @type suite: Suite
        """
        self._suites.append(suite)

    def run(self):
        """Run all the tests, then all the suites"""
        debug(_("Running suite {}").format(self.name))
        self._notify_event(TestEvent.begin)
        res = SuiteResult()
        for test in self._tests:
            t_res = test.run()
            res.test_results.append(t_res)
        for suite in self._suites:
            s_res = suite.run()
            res.suite_results.append(s_res)
        self._notify_event(TestEvent.end)
        return res


TestStatus = Enum('TestStatus', 'passed failed')


class TestResult:
    """Represent the result of the execution of a test"""
    def __init__(self, status=TestStatus.failed):
        self.status = status


class SuiteResult:
    """Represent the result of the execution of a suite"""
    def __init__(self):
        self.test_results = []
        self.suite_results = []

    @property
    def status(self):
        status = TestStatus.passed
        for res in self.test_results:
            if res.status != TestStatus.passed:
                status = TestStatus.failed
                break
        for res in self.suite_results:
            if res.status != TestStatus.passed:
                status = TestStatus.failed
                break
        return status

    @property
    def is_failure(self):
        """Tell whether the suite failed or not"""
        if self.status == TestStatus.passed:
            return False
        return True

    @property
    def is_success(self):
        """Tell whether the suite succeeded or not"""
        if self.status == TestStatus.failed:
            return False
        return True

# vim: ts=4 sw=4 sts=4 et ai
