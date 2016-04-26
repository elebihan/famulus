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
   famulus.cli
   ```````````

   Provides command line interpeter helpers

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import sys
import argparse
import traceback
from famulus import __version__
from famulus.utils import setup_i18n
from famulus.log import setup_logging, set_level
from famulus.log import error
from gettext import gettext as _

setup_i18n()

setup_logging()


class Application:
    """Command line Application"""
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version',
                                  action='version',
                                  version=__version__)
        self._parser.add_argument('-D', '--debug',
                                  action='store_true',
                                  default=False,
                                  help=_("show debug messages"))

    # Insert the program options here

    def run(self):
        """Run the application"""
        args = self._parser.parse_args()

        if args.debug:
            set_level('DEBUG')
        try:
            rc = 0
            # Insert code here
        except Exception as e:
            if 'FAMULUS_SHOW_STACK_TRACES' in os.environ:
                traceback.print_exc()
            else:
                error(_("Command failed ({})").format(e))
            rc = 1
        return rc


def main():
    app = Application()
    rc = app.run()
    sys.exit(rc)

# vim: ts=4 sw=4 sts=4 et ai
