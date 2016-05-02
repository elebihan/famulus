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
   famulus.suitebuilder
   ````````````````````

   Classes and helper functions to build suites

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .log import debug
from .test import Test, Suite
from .utils import topological_sort, CyclicGraphError
from gettext import gettext as _


class CyclicDependencyError(Exception):
    """Error raised when a cyclic dependency error between suites is found"""
    def __init__(self):
        Exception.__init__(self, _("Cyclic dependency between suites detected"))


class SuiteBuilder:
    """Build suite from test and suite specifications"""
    def __init__(self, manager):
        self._mgr = manager

    def build_suite_for_names(self, names):
        """Build a suite from a list of test/suite names.

        @param names: list of test/suite names
        @type names: list of str

        @return: a suite
        @rtype: Suite
        """
        s_names = [s.name for s in self._mgr.suites]
        t_names = [t.name for t in self._mgr.tests]

        self._check_circular_deps(names, s_names)

        root = Suite("root")
        root.brief = 'root suite'

        for name in names:
            if name in t_names:
                self._add_test_to_suite(root, name)
            elif name in s_names:
                self._add_suite_to_suite(root, name)

        return root

    def _check_circular_deps(self, names, suite_names):
        debug(_("Checking for circular dependencies between suites"))
        selection = [n for n in names if n in suite_names]
        graph_unsorted = {'root': selection}
        try:
            self._build_suite_deps(graph_unsorted, selection, suite_names)
        except CyclicGraphError:
            raise CyclicDependencyError

    def _build_suite_deps(self, graph_unsorted, names, suite_names):
        selection = [n for n in names if n in suite_names]
        for name in selection:
            spec = self._mgr.find_suite_spec(name)
            if spec:
                graph_unsorted[name] = spec.suites
                if spec.suites:
                    deps = ', '.join(spec.suites)
                    msg = _("Suite {} depends on {}").format(name, deps)
                else:
                    msg = _("Suite {} has no dependencies").format(name)
                debug(msg)
                topological_sort(dict(graph_unsorted))
                self._build_suite_deps(graph_unsorted,
                                       spec.suites,
                                       suite_names)

    def _add_test_to_suite(self, suite, name):
        spec = self._mgr.find_test_spec(name)
        if spec:
            t = self._create_test_from_spec(spec)
            suite.add_test(t)
            debug(_("Added test {}".format(t.name)))
        else:
            raise ValueError(_("Invalid test name"))

    def _add_suite_to_suite(self, suite, name):
        spec = self._mgr.find_suite_spec(name)
        if spec:
            s = self._create_suite_from_spec(spec)
            suite.add_suite(s)
            debug(_("Added suite {}".format(s.name)))
        else:
            raise ValueError(_("Invalid suite name"))

    def _create_test_from_spec(self, spec):
        debug(_("Creating test {}".format(spec.name)))
        test = Test(spec.name, spec.command, spec.expect)
        test.author = spec.author
        test.brief = spec.brief
        test.description = spec.description
        return test

    def _create_suite_from_spec(self, spec):
        debug(_("Creating suite {}".format(spec.name)))
        suite = Suite(spec.name)
        suite.author = spec.author
        suite.brief = spec.brief
        suite.description = spec.description
        for n in spec.tests:
            self._add_test_to_suite(suite, n)
        for n in spec.suites:
            self._add_suite_to_suite(suite, n)
        return suite

# vim: ts=4 sw=4 sts=4 et ai
