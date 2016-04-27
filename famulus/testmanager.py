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

   Classes and helper functions to manage test and test suite files.


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import yaml
import shutil
from .log import debug
from .test import Test, Suite
from .utils import get_data_dir
from subprocess import check_call
from gettext import gettext as _

from enum import Enum

TestType = Enum('TestType', 'simple suite')


class TestManager:
    """Manage test and test suite files"""
    def __init__(self):
        self._search_paths = []
        self._tests = []
        self._suites = []
        self.editor = os.environ.get('EDITOR', 'vi')

    def add_search_path(self, path):
        """Adds a new path for searching test definitions.

        @param path: path where to look for new tests
        @type path: str
        """
        self._search_paths.append(path)

    def scan(self):
        """Scan all known search paths for tests"""
        self._presets = []
        for path in self._search_paths:
            debug(_("Searching for tests in {}").format(path))
            for entry in os.listdir(path):
                fn = os.path.join(path, entry)
                if fn.endswith('.yaml'):
                    debug(_("Found test '{}'").format(fn))
                    self.load_file(fn)

    @property
    def tests(self):
        """List of tests"""
        return self._tests

    @property
    def suites(self):
        """List of test suites"""
        return self._suites

    def load_file(self, filename):
        """Load test or test suite from file"""
        with open(filename) as f:
            doc = yaml.load(f.read())
            if 'type' not in doc:
                raise ValueError(_("Invalid test file"))
            if doc['type'] == 'test':
                test = Test(doc)
                self._tests.append(test)
            elif doc['type'] == 'suite':
                suite = Suite(doc)
                self._suites.append(suite)
            else:
                raise ValueError(_("Invalid category in test file"))

    def find_test(self, name):
        """Find a test by its name.

        @param name: name of the test to find.
        @type name: str

        @return: the test
        @rtype: Test
        """
        for test in self._tests:
            if test.name == name:
                return test
        return None

    def find_suite(self, name):
        """Find a test suite by its name.

        @param name: name of the test suite to find.
        @type name: str

        @return: the test suite
        @rtype: Suite
        """
        for suite in self._suites:
            if suite.name == name:
                return suite
        return None

    def create_test(self, name, path, template=None):
        """Create a new test.

        @param name: name of the new test
        @type name: str
        @param path: location to store the test file
        @param path: str
        """
        if not self.find_test(name):
            filename = self._create_file_for(TestType.simple,
                                             name,
                                             path,
                                             template)
            self.load_file(filename)
        else:
            raise ValueError(_("A test with this name already exists"))

    def create_suite(self, name, path, template=None):
        """Create a new test suite.

        @param name: name of the new test suite
        @type name: str
        @param path: location to store the test suite file
        @param path: str
        """
        if not self.find_suite(name):
            filename = self._create_file_for(TestType.suite,
                                             name,
                                             path,
                                             template)
            self.load_file(filename)
        else:
            raise ValueError(_("A test suite with this name already exists"))

    def _create_file_for(self, what, name, path, template):
        samples = {
            TestType.simple: 'test.yaml',
            TestType.suite: 'suite.yaml',
        }
        if not template:
            template = os.path.join(get_data_dir(), 'samples', samples[what])
        return self._create_file(name, path, template)

    def _create_file(self, name, path, template):
        filename = os.path.join(path, name + '.yaml')
        debug(_("Creating {} from {}".format(filename, template)))
        shutil.copy(template, filename)
        check_call([self.editor, filename])
        return filename


# vim: ts=4 sw=4 sts=4 et ai
