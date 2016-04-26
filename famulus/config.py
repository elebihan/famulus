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
   famulus.config
   ``````````````

   Provides configuration files management

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from configparser import ConfigParser

DEFAULT_TESTS_PATH = '~/.local/share/famulus/tests'


class Configuration:
    """Stores the configuration of the application"""
    def __init__(self):
        self.tests_paths = [os.path.expanduser(DEFAULT_TESTS_PATH)]

    def load_from_file(self, filename):
        """Loads the configuration from a file

        @param filename: path to the configuration file to read
        @type filename: str
        """
        parser = ConfigParser()
        with open(filename) as f:
            parser.read_file(f)
        value = parser.get('General', 'TestsPaths', fallback='')
        self.tests_paths += map(lambda p: os.path.expanduser(p.strip()),
                                value.split(','))

    def save_to_file(self, filename):
        """Saves the configuration to a file

        @param filename: path to the configuration file to create
        @type filename: str
        """
        parser = ConfigParser()
        parser.set('General', 'TestsPaths', ','.join(self.tests_paths))
        with open(filename, 'w+') as f:
            parser.write(f)

# vim: ts=4 sw=4 sts=4 et ai
