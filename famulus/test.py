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

from enum import Enum
from .log import debug
from gettext import gettext as _

BASE_KEYS = ['name', 'type', 'category', 'author', 'brief', 'description']
TEST_KEYS = ['setup', 'teardown', 'command', 'expect']
SUITE_KEYS =['tests']

TestType = Enum('TestType', 'single suite')


class BaseSpec:
    """Base class for a specification.

    @param params: dictionary of params for creating specification.
    @type params: dict

    @param extra_keys: list of extra parameter keys
    @type extra_keys: list of str
    """
    def __init__(self, params, extra_keys=[]):
        if not params.keys() & set(BASE_KEYS + extra_keys):
            raise ValueError(_("Invalid keys in dictionary"))
        for key in params.keys():
            if key != 'type':
                setattr(self, key, params[key])


class TestSpec(BaseSpec):
    """Specification of a test to run.

    @param params: dictionary of params for creating test.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params, TEST_KEYS)


class SuiteSpec(BaseSpec):
    """Specification of a suite to run.

    @param params: dictionary of params for creating suite.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params, SUITE_KEYS)


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

    @property
    def name(self):
        return self._name

    def run(self):
        raise NotImplementedError


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
        for test in self._tests:
            test.run()
        for suite in self._suites:
            suite.run()


# vim: ts=4 sw=4 sts=4 et ai
