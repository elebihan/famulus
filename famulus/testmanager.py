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
from .spec import SpecType, TestSpec, SuiteSpec
from .suitebuilder import SuiteBuilder
from .utils import get_data_dir
from subprocess import check_call
from gettext import gettext as _

TEST_INFO_TEMPLATE = """{1}
--
Author: {0.author}"""

SUITE_INFO_TEMPLATE = """{1}
--
Tests: {2}
Author: {0.author}"""


class TestManager:
    """Manage test and suite specifications"""
    def __init__(self):
        self._search_paths = []
        self._tests = {}
        self._suites = {}
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
            debug(_("Searching for tests/suites in {}").format(path))
            for entry in os.listdir(path):
                fn = os.path.join(path, entry)
                if fn.endswith('.yaml'):
                    try:
                        self.load_spec_file(fn)
                    except ValueError as e:
                        warning(_("Skipping {} ({})".format(fn, e)))

    @property
    def tests(self):
        """List of test specifications"""
        return self._tests.values()

    @property
    def suites(self):
        """List of suite specifications"""
        return self._suites.values()

    def load_spec_file(self, filename):
        """Load a test/suite specification from a file"""
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
                    self._tests[filename] = test
                    debug(_("Loaded test from '{}'").format(filename))
            elif doc['type'] == 'suite':
                if doc['name'] in s_names:
                    debug(_("Skipping suite from {} (already in list)".format(filename)))
                else:
                    suite = SuiteSpec(doc)
                    self._suites[filename] = suite
                    debug(_("Loaded suite from '{}'").format(filename))
            else:
                raise ValueError(_("Invalid category in test/suite file"))

    def find_test_spec(self, name):
        """Find a test specification by its name.

        @param name: name of the test to find.
        @type name: str

        @return: the test specification
        @rtype: TestSpec
        """
        for test in self.tests:
            if test.name == name:
                return test

    def find_suite_spec(self, name):
        """Find a suite specification by its name.

        @param name: name of the suite to find.
        @type name: str

        @return: the test suite specification
        @rtype: SuiteSpec
        """
        for suite in self.suites:
            if suite.name == name:
                return suite

    def create_spec(self, kind, name, path, template=None):
        """Create a new test specification.

        @param kind: object kind to create a specification for
        @type kind: SpecType

        @param name: name of the new test
        @type name: str

        @param path: location to store the test file
        @param path: str
        """
        if kind == SpecType.test:
            spec = self.find_test_spec(name)
            msg =  _('Test already exists')
        elif kind == SpecType.suite:
            spec = self.find_suite_spec(name)
            msg =  _('Suite already exists')
        else:
            raise ValueError(_("Invalid object"))

        if not spec:
            filename = self._create_spec_file(kind, name, path, template)
            self.load_spec_file(filename)
        else:
            raise ValueError(msg)

    def _create_spec_file(self, kind, name, path, template):
        samples = {
            SpecType.test: 'test.yaml',
            SpecType.suite: 'suite.yaml',
        }
        if template:
            fn = self._find_spec_file(kind, template)
            if not fn:
                raise ValueError(_('Invalid template name'))
        else:
            fn = os.path.join(get_data_dir(), 'samples', samples[kind])
        return self._create_file(name, path, fn)

    def _create_file(self, name, path, template):
        filename = os.path.join(path, name + '.yaml')
        debug(_("Creating {} from {}".format(filename, template)))
        shutil.copy(template, filename)
        check_call([self.editor, filename])
        return filename

    def _find_spec_file(self, kind, name):
        collections = {
            SpecType.test: self._tests,
            SpecType.suite: self._suites,
        }

        for (fn, element) in collections[kind].items():
            if element.name == name:
                return fn

    def describe(self, kind, name):
        """Describe a test or suite.

        @param kind: object kind to describe
        @type kind: SpecType

        @param name: name of the object to describe
        @type name: str

        @return: description of the object
        @rtype: str
        """
        if kind == SpecType.test:
            spec = self.find_test_spec(name)
            msg = _('Invalid test name')
        elif kind == SpecType.suite:
            spec = self.find_suite_spec(name)
            msg = _('Invalid suite name')
        else:
            raise ValueError(_("Invalid object"))

        if spec:
            text = ''.join(spec.description).strip()
            if kind == SpecType.test:
                return TEST_INFO_TEMPLATE.format(spec, text)
            else:
                tests = ', '.join(spec.tests)
                return SUITE_INFO_TEMPLATE.format(spec, text, tests)
        else:
            raise ValueError(msg)

    def edit_spec(self, kind, name):
        """Edit a test/suite specification.

        @param kind: object kind to describe
        @type kind: SpecType

        @param name: name of the test/suite to edit
        @type name: str
        """
        fn = self._find_spec_file(kind, name)
        if fn:
            check_call([self.editor, fn])
        else:
            raise ValueError(_("Invalid test/suite name"))

    def create_suite_for_names(self, names):
        """Create a suite from a list of test/suite names.

        @param names: list of test/suite names
        @type names: list of str

        @return: a suite
        @rtype: Suite
        """
        builder = SuiteBuilder(self)
        return builder.build_suite_for_names(names)

# vim: ts=4 sw=4 sts=4 et ai
