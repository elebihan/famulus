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
from gettext import bindtextdomain, textdomain


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

# vim: ts=4 sw=4 sts=4 et ai
