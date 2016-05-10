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
   famulus.utils
   `````````````

   Useful classes and helper functions

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import re
import sys
from gettext import bindtextdomain, textdomain
from gettext import gettext as _


def get_data_dir():
    """Returns the data directory.

    rtype: str
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(root_dir, '..')

    if os.path.exists(os.path.join(root_dir, '.git')):
        data_dir = os.path.join(root_dir, 'data')
    else:
        upper, lower = root_dir.split('lib')
        data_dir = os.path.join(upper, 'share', 'famulus')

    return os.path.normpath(data_dir)


def setup_i18n():
    """Set up internationalization."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if 'lib' not in root_dir:
        return
    root_dir, mod_dir = root_dir.split('lib', 1)
    locale_dir = os.path.join(root_dir, 'share', 'locale')

    bindtextdomain('famulus', locale_dir)
    textdomain('famulus')


class CyclicGraphError(Exception):
    """Error raised when graph is not acyclic"""


def topological_sort(graph_unsorted):
    """Perform a topological sort.

    Perform a topological sort on a mapping between an item and its
    dependencies.

    @param graph_unsorted: a mapping between strings and list of strings
    @type graph_unsorted: dict

    @return: the sorted graph
    @rtype: list of tuples

    @raise: CyclicGraphError
    """
    graph_sorted = []

    while graph_unsorted:
        acyclic = False
        for node, edges in list(graph_unsorted.items()):
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))
        if not acyclic:
            raise CyclicGraphError

    return graph_sorted


def read_from_stdin():
    """Read lines from standard input and strip them.

    @return: list of stripped lines
    @rtype: list of str
    """
    return [l.strip() for l in sys.stdin.readlines()]


class InvalidURIError(Exception):
    """Error raised when an invalid URI is used"""
    def __init__(self):
        Exception.__init__(self, _("Invalid URI"))


def validate_uri(uri):
    """Validate an URI.

    @param uri: URI to validate
    @type uri: strip

    @raise: InvalidURIError
    """
    if not re.match(r'^(?:[\w]+)://'
                    r'(?:.+(?::.+)?@)?'
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                    r'localhost|'
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                    r'(?:/?|[/?]\S+)$',
                    uri,
                    re.IGNORECASE):
        raise InvalidURIError

# vim: ts=4 sw=4 sts=4 et ai
