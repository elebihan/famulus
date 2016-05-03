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
   famulus.spec
   ````````````

   Classes and helper functions for test and suite specifications

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from enum import Enum


SpecType = Enum('SpecType', 'test suite')


class BaseSpec:
    """Base class for a specification.

    @param params: dictionary of params for creating specification.
    @type params: dict
    """
    def __init__(self, params):
        self.name = params['name']
        self.brief = params['brief']
        self.category = params.get('catgeory', 'Unknown')
        self.author = params.get('author', 'Unknown')
        self.description = params.get('description', 'No description given')


class TestSpec(BaseSpec):
    """Specification of a test to run.

    @param params: dictionary of params for creating test.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params)
        self.command = params['command']
        self.expect = params['expect']
        self.setup = params.get('setup', [])
        self.teardown = params.get('teardown', [])


class SuiteSpec(BaseSpec):
    """Specification of a suite to run.

    @param params: dictionary of params for creating suite.
    @type params: dict
    """
    def __init__(self, params):
        BaseSpec.__init__(self, params)
        self.tests = params.get('tests', [])
        self.suites = params.get('suites', [])


# vim: ts=4 sw=4 sts=4 et ai
