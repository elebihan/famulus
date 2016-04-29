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
   famulus.testmanager
   ```````````````````

   Classes and helper functions to manage test and suite files.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import yaml
import shutil
from .log import debug, warning
from .test import TestSpec, SuiteSpec
from .utils import get_data_dir
from subprocess import check_call
from gettext import gettext as _

from enum import Enum

TEST_INFO_TEMPLATE = """{1}
--
Author: {0.author}"""

SUITE_INFO_TEMPLATE = """{1}
--
Tests: {2}
Author: {0.author}"""

TestType = Enum('TestType', 'single suite')


class TestManager:
    """Manage test and suite specifications"""
    def __init__(self):
        self._search_paths = []
        self._tests = []
        self._suites = []
        self.editor = os.environ.get('EDITOR', 'vi')

    def add_search_path(self, path):
        """Adds a new path for searching test/suite specifications.

        @param path: path where to look for new tests/suites
        @type path: str
        """
        self._search_paths.append(path)

    def scan(self):
        """Scan all known search paths for tests/suites"""
        for path in reversed(self._search_paths):
            debug(_("Searching for tests in {}").format(path))
            for entry in os.listdir(path):
                fn = os.path.join(path, entry)
                if fn.endswith('.yaml'):
                    try:
                        self.load_file(fn)
                    except ValueError as e:
                        warning(_("Skipping {} ({})".format(fn, e)))

    @property
    def tests(self):
        """List of tests"""
        return [t for (t, f) in self._tests]

    @property
    def suites(self):
        """List of suites"""
        return [s for (s, f) in self._suites]

    def load_file(self, filename):
        """Load a test or a suite from a file"""
        t_names = [t.name for t in self.tests]
        s_names = [s.name for s in self.suites]
        with open(filename) as f:
            doc = yaml.load(f.read())
            if not doc:
                raise ValueError(_("Invalid YAML file"))
            if 'type' not in doc:
                raise ValueError(_("Invalid test/suite file"))
            if doc['type'] == 'test':
                if doc['name'] in t_names:
                    debug(_("Skipping test from {} (already in list)".format(filename)))
                else:
                    test = TestSpec(doc)
                    self._tests.append((test, filename))
                    debug(_("Loaded test from '{}'").format(filename))
            elif doc['type'] == 'suite':
                if doc['name'] in s_names:
                    debug(_("Skipping suite from {} (already in list)".format(filename)))
                else:
                    suite = SuiteSpec(doc)
                    self._suites.append((suite, filename))
                    debug(_("Loaded suite from '{}'").format(filename))
            else:
                raise ValueError(_("Invalid category in test/suite file"))

    def find_test(self, name):
        """Find a test by its name.

        @param name: name of the test to find.
        @type name: str

        @return: the test specification
        @rtype: TestSpec
        """
        for (test, fn) in self._tests:
            if test.name == name:
                return test

    def find_suite(self, name):
        """Find a suite by its name.

        @param name: name of the suite to find.
        @type name: str

        @return: the test suite specification
        @rtype: SuiteSpec
        """
        for (suite, fn) in self._suites:
            if suite.name == name:
                return suite

    def create_test(self, name, path, template=None):
        """Create a new test.

        @param name: name of the new test
        @type name: str
        @param path: location to store the test file
        @param path: str
        """
        if not self.find_test(name):
            filename = self._create_file_for(TestType.single,
                                             name,
                                             path,
                                             template)
            self.load_file(filename)
        else:
            raise ValueError(_("A test with this name already exists"))

    def create_suite(self, name, path, template=None):
        """Create a new suite.

        @param name: name of the new suite
        @type name: str
        @param path: location to store the suite file
        @param path: str
        """
        if not self.find_suite(name):
            filename = self._create_file_for(TestType.suite,
                                             name,
                                             path,
                                             template)
            self.load_file(filename)
        else:
            raise ValueError(_("A suite with this name already exists"))

    def _create_file_for(self, what, name, path, template):
        samples = {
            TestType.single: 'test.yaml',
            TestType.suite: 'suite.yaml',
        }
        if template:
            fn = self._find_file_for(what, template)
            if not fn:
                raise ValueError(_('Invalid template name'))
        else:
            fn = os.path.join(get_data_dir(), 'samples', samples[what])
        return self._create_file(name, path, fn)

    def _create_file(self, name, path, template):
        filename = os.path.join(path, name + '.yaml')
        debug(_("Creating {} from {}".format(filename, template)))
        shutil.copy(template, filename)
        check_call([self.editor, filename])
        return filename

    def _find_file_for(self, what, name):
        items = {
            TestType.single: self._tests,
            TestType.suite: self._suites,
        }

        for (item, fn) in items[what]:
            if item.name == name:
                return fn

    def describe_test(self, name):
        """Describe a test.

        @param name: name of the test to describe
        @type name: str

        @return: description of the test
        @rtype: str
        """

        test = self.find_test(name)
        if test:
            text = ''.join(test.description).strip()
            return TEST_INFO_TEMPLATE.format(test, text)
        else:
            raise ValueError(_("Invalid test name"))

    def describe_suite(self, name):
        """Describe a suite.

        @param name: name of the suite to describe
        @type name: str

        @return: description of the suite
        @rtype: str
        """

        suite = self.find_suite(name)
        if suite:
            text = ''.join(suite.description).strip()
            tests = ', '.join(suite.tests)
            return SUITE_INFO_TEMPLATE.format(suite, text, tests)
        else:
            raise ValueError(_("Invalid suite name"))

    def edit_test(self, name):
        """Edit a test specification.

        @param name: name of the test to edit
        @type name: str
        """
        fn = self._find_file_for(TestType.single, name)
        if fn:
            check_call([self.editor, fn])
        else:
            raise ValueError(_("Invalid test name"))

    def edit_suite(self, name):
        """Edit a suite specification.

        @param name: name of the suite to edit
        @type name: str
        """
        fn = self._find_file_for(TestType.suite, name)
        if fn:
            check_call([self.editor, fn])
        else:
            raise ValueError(_("Invalid suite name"))


# vim: ts=4 sw=4 sts=4 et ai
