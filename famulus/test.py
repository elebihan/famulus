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

   Classes and helper functions for tests and test suites.


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from gettext import gettext as _

COMMON_KEYS = ['name', 'type', 'category', 'author', 'brief', 'description']
TEST_KEYS = COMMON_KEYS + ['setup', 'teardown', 'command', 'expect']
SUITE_KEYS = COMMON_KEYS + ['tests']


class Test:
    """Represent a test to be run.

    @param params: dictionary of params for creating test.
    @type params: dict
    """
    def __init__(self, params):
        if not params.keys() & set(TEST_KEYS):
            raise ValueError(_("Invalid keys in dictionary"))
        self.name = params['name']
        self.brief = params['brief']


class Suite:
    """Represent a test suite to be run.

    @param params: dictionary of params for creating test.
    @type params: dict
    """
    def __init__(self, params):
        if not params.keys() & set(SUITE_KEYS):
            raise ValueError(_("Invalid keys in dictionary"))
        self.name = params['name']
        self.brief = params['brief']

# vim: ts=4 sw=4 sts=4 et ai
