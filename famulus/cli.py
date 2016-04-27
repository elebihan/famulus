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
from famulus.log import error, warning
from famulus.config import Configuration, DEFAULT_TESTS_PATH
from famulus.testmanager import TestManager
from gettext import gettext as _

DEFAULT_CONF_FILE = '~/.config/famulus.conf'

setup_i18n()

setup_logging()


class Application:
    """Command line Application"""
    def __init__(self):
        self._test_mgr = TestManager()
        self._config = Configuration()

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-V', '--version',
                                  action='version',
                                  version=__version__)
        self._parser.add_argument('-D', '--debug',
                                  action='store_true',
                                  default=False,
                                  help=_("show debug messages"))
        self._parser.add_argument('-C', '--config',
                                  metavar=_('FILE'),
                                  default=os.path.expanduser(DEFAULT_CONF_FILE),
                                  help=_('set path to configuration file'))

        subparsers = self._parser.add_subparsers(dest='command')
        p = subparsers.add_parser('list',
                                  help=_('list available tests or test suites'))
        p.add_argument('-d', '--details',
                       action='store_true',
                       dest='with_details',
                       default=False,
                       help=_("show some details"))
        p.add_argument('object',
                       choices=('tests', 'suites'),
                       help=_('objects to list'))
        p.set_defaults(func=self._parse_cmd_list)

        p = subparsers.add_parser('new',
                                  help=_('create a new test or test suite'))
        p.add_argument('-O', '--output',
                       metavar=_('DIR'),
                       default=DEFAULT_TESTS_PATH,
                       help=_('set output directory'))
        p.add_argument('-f', '--from',
                       dest='template',
                       metavar=_('FILE'),
                       help=_('use FILE as template'))
        p.add_argument('object',
                       choices=('test', 'suite'),
                       help=_('object to create'))
        p.add_argument('name',
                       help=_('name of the new object'))
        p.set_defaults(func=self._parse_cmd_new)

    def _parse_cmd_list(self, args):
        if args.object == 'tests':
            items = self._test_mgr.tests
        elif args.object == 'suites':
            items = self._test_mgr.suites
        else:
            self._parser.error(_('Invalid object'))

        for item in items:
            if args.with_details:
                text = "{0.name:<32} -- {0.brief:<48}"
            else:
                text = "{0.name}"
            print(text.format(item))

    def _parse_cmd_new(self, args):
        if args.object == 'test':
            self._test_mgr.create_test(args.name, args.output, args.template)
        elif args.object == 'suite':
            self._test_mgr.create_suite(args.name, args.output, args.template)
        else:
            self._parser.error(_('Invalid object'))

    def run(self):
        """Run the application"""
        args = self._parser.parse_args()

        if not hasattr(args, 'func'):
            self._parser.error(_('Missing command'))

        if args.debug:
            set_level('DEBUG')

        if os.path.exists(args.config):
            self._config.load_from_file(args.config)
        else:
            warning(_("Can not find configuration file. Using defaults."))

        for path in self._config.tests_paths:
            self._test_mgr.add_search_path(path)

        self._test_mgr.editor = self._config.editor

        try:
            self._test_mgr.scan()
            args.func(args)
            rc = 0
        except Exception as e:
            rc = 1
            if 'FAMULUS_SHOW_STACK_TRACES' in os.environ:
                traceback.print_exc()
            else:
                error(_("Command failed ({})").format(e))
        self._parser.exit(rc)


def main():
    app = Application()
    app.run()

# vim: ts=4 sw=4 sts=4 et ai
