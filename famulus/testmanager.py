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
from .log import debug
from .test import Test, Suite
from gettext import gettext as _


class TestManager:
    """Manage test and test suite files"""
    def __init__(self):
        self._search_paths = []
        self._tests = []
        self._suites = []

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

# vim: ts=4 sw=4 sts=4 et ai
