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
   famulus.test.results
   ````````````````````

   Classes and helper functions for test and suite results

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from enum import Enum


TestStatus = Enum('TestStatus', 'passed failed')


class TestResult:
    """Represent the result of the execution of a test.

    @param test: the test which generated this result
    @type test: Test
    """
    def __init__(self, test, status=TestStatus.failed):
        self._test = test
        self.status = status

    @property
    def test(self):
        """Return the associated test"""
        return self._test

    @property
    def is_failure(self):
        """Tell whether the test failed or not"""
        return self.status == TestStatus.failed

    @property
    def is_success(self):
        """Tell whether the test succeeded or not"""
        return self.status == TestStatus.passed


class SuiteResult:
    """Represent the result of the execution of a suite.

    @param suite: the suite which generated this result
    @type suite: Suite
    """
    def __init__(self, suite):
        self._suite = suite
        self.test_results = []
        self.suite_results = []

    @property
    def suite(self):
        """Return the associated suite"""
        return self._suite

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
        return self.status == TestStatus.failed

    @property
    def is_success(self):
        """Tell whether the suite succeeded or not"""
        return self.status == TestStatus.passed

# vim: ts=4 sw=4 sts=4 et ai
