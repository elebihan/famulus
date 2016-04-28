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

BASE_KEYS = ['name', 'type', 'category', 'author', 'brief', 'description']
TEST_KEYS = ['setup', 'teardown', 'command', 'expect']
SUITE_KEYS =['tests']


class BaseSpec:
    """Base class for a specification.

    @param params: dictionary of params for creating test.
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
    """Specification of a test case to run.

    @param params: dictionary of params for creating test.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params, TEST_KEYS)


class SuiteSpec(BaseSpec):
    """Specification a test suite to run.

    @param params: dictionary of params for creating test suite.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params, SUITE_KEYS)

# vim: ts=4 sw=4 sts=4 et ai
