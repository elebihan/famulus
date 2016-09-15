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
   famulus.test.base
   `````````````````

   Classes and helper functions for tests and suites.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

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

    @property
    def name(self):
        return self._name


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

    @property
    def command(self):
        """Return the command to be run for test"""
        return self._command

    @property
    def expect(self):
        """Return the expected result of the command"""
        return self._expect


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


# vim: ts=4 sw=4 sts=4 et ai
