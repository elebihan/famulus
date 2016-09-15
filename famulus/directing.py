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
   famulus.directing
   `````````````````
   Classes and helper functions for directing tests and commands


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .command import CommandRunnerFactory
from .test.runners import SuiteRunner
from .test.events import EventLogger


def run_suite(suite, uri, format):
    """Run suite for remote machine.

    @param suite: suite to run
    @type suite: Suite

    @param uri: URI of the remote machine
    @type uri: str

    @param format: event logger format
    @type format: EventLoggerFormat

    @return: result of the execution of the suite
    @rtype: SuiteResult
    """
    factory = CommandRunnerFactory()
    runner = SuiteRunner(factory.create_command_runner_for_uri(uri),
                         EventLogger(format))
    runner.cmd_runner.setup()
    try:
        result = runner.run(suite)
    finally:
        runner.cmd_runner.teardown()
    return result


def run_commands(uri, commands, delimited=False):
    """Run a batch of commands on local/remote machine.

    @param uri: URI of the remote machine
    @type uti: str

    @param commands: commands to execute
    @type commands: list of str

    @param delimited: if True, print a text delimeter between commands.
    @type delimted: bool
    """
    factory = CommandRunnerFactory()
    runner = factory.create_command_runner_for_uri(uri)
    runner.setup()
    for command in commands:
        output = runner.run(command)
        if delimited:
            output = "--8<--\n{}\n-->8--".format(output)
        print(output)
    runner.teardown()

# vim: ts=4 sw=4 sts=4 et ai
