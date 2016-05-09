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
import argparse
import traceback
import urllib.parse
from famulus import __version__
from famulus.utils import setup_i18n, read_from_stdin
from famulus.log import setup_logging, set_level
from famulus.log import error, warning
from famulus.config import Configuration, DEFAULT_TESTS_PATH
from famulus.spec import SpecType
from famulus.testmanager import TestManager
from famulus.runner import create_suite_runner
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
        self._parser.add_argument('-T', '--tests-path',
                                  metavar=_('DIR'),
                                  dest='tests_paths',
                                  action='append',
                                  default=[],
                                  help=_('add path to tests/suites'))

        subparsers = self._parser.add_subparsers(dest='command')
        p = subparsers.add_parser('list',
                                  help=_('list available tests or suites'))
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
                                  help=_('create a new test or suite'))
        p.add_argument('-O', '--output',
                       metavar=_('DIR'),
                       default=DEFAULT_TESTS_PATH,
                       help=_('set output directory'))
        p.add_argument('-f', '--from',
                       dest='template',
                       metavar=_('NAME'),
                       help=_('use NAME as template'))
        p.add_argument('object',
                       choices=('test', 'suite'),
                       help=_('object to create'))
        p.add_argument('name',
                       help=_('name of the new object'))
        p.set_defaults(func=self._parse_cmd_new)

        p = subparsers.add_parser('show',
                                  help=_('show information about a test or suite'))
        p.add_argument('object',
                       choices=('test', 'suite'),
                       help=_('object to show'))
        p.add_argument('name',
                       help=_('name of the object'))
        p.set_defaults(func=self._parse_cmd_show)

        p = subparsers.add_parser('edit',
                                  help=_('edit a test or suite'))
        p.add_argument('object',
                       choices=('test', 'suite'),
                       help=_('object to edit'))
        p.add_argument('name',
                       help=_('name of the object'))
        p.set_defaults(func=self._parse_cmd_edit)

        p = subparsers.add_parser('run',
                                  help=_('run one or more test/suite'))
        p.add_argument('-F', '--event-format',
                       choices=('human', 'machine'),
                       default='human',
                       help=_('set event logging format'))
        p.add_argument('URI',
                       help=_(('URI of the target')))
        p.add_argument('names',
                       nargs='+',
                       metavar=_('NAME'),
                       help=_('name of the object'))
        p.set_defaults(func=self._parse_cmd_run)

    def _parse_cmd_list(self, args):
        if args.object == 'tests':
            items = self._test_mgr.tests
        elif args.object == 'suites':
            items = self._test_mgr.suites
        else:
            self._parser.error(_('Invalid object'))

        for item in items:
            if args.with_details:
                text = "{0.name:<24} -- {0.brief:<48}"
            else:
                text = "{0.name}"
            print(text.format(item))

    def _parse_cmd_new(self, args):
        try:
            self._test_mgr.create_spec(SpecType[args.object],
                                       args.name,
                                       args.output,
                                       args.template)
        except KeyError:
            self._parser.error(_('Invalid object'))

    def _parse_cmd_show(self, args):
        try:
            text = self._test_mgr.describe(SpecType[args.object], args.name)
            print(text)
        except KeyError:
            self._parser.error(_('Invalid object'))

    def _parse_cmd_edit(self, args):
        try:
            self._test_mgr.edit_spec(SpecType[args.object], args.name)
        except KeyError:
            self._parser.error(_('Invalid object'))

    def _parse_cmd_run(self, args):
        uri = self._build_full_uri(args.URI)
        names = read_from_stdin() if args.names[0] == '-' else args.names
        suite = self._test_mgr.create_suite_for_names(names)
        runner = create_suite_runner(uri, args.event_format)
        result = runner.run(suite)
        if result.is_failure:
            rc = 6
            error(_("Some tests/suites failed"))
        else:
            rc = 0
        self._parser.exit(rc)

    def _build_full_uri(self, uri):
        crumbs = urllib.parse.urlsplit(uri)
        username = crumbs.username or self._config.username
        password = crumbs.password or self._config.password
        if username:
            netloc = username
            if password:
                netloc += ':' + password
            netloc += '@' + crumbs.hostname
        else:
            netloc = crumbs.hostname
        fields = list(crumbs)
        fields[1] = netloc
        return urllib.parse.urlunsplit(fields)

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

        for path in args.tests_paths:
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
