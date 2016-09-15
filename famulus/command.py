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
   famulus.command
   ```````````````

   Classes and helper functions for running commands on local/remote machine.


   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import re
from .log import debug
from .clients.factory import ClientFactory
from gettext import gettext as _


class CommandRunnerFactory:
    """Create command runners"""
    def __init__(self):
        self._client_factory = ClientFactory()

    def create_command_runner_for_uri(self, uri):
        """Create a command runner suitable for a given URI scheme

        @param uri: URI of the remote machine
        @type uri: str
        """
        local_client = self._client_factory.create_client_for_uri('local://localhost')
        remote_client = self._client_factory.create_client_for_uri(uri)
        return CommandRunner(local_client, remote_client)


class CommandRunner:
    """Run commands on local/remote machine.

    @param local_client: client to use for local commands
    @type local_client: Client

    @param remote_client: client to use for remote commands
    @type remote_client: Client
    """
    def __init__(self, local_client, remote_client):
        self._clients = {
            'local': local_client,
            'remote': remote_client,
        }

    def setup(self):
        """Set up the command runner"""
        for name, client in self._clients.items():
            debug(_("Connecting client '{}'").format(name))
            client.connect()

    def teardown(self):
        """Tear down the command runner"""
        for name, client in self._clients.items():
            debug(_("Disconnecting client '{}'").format(name))
            client.disconnect()

    def run(self, command):
        """Execute a command.

        @param command: the command to run
        @type command: str

        @return: the output of the command
        @rtype: str
        """
        match = re.match(r'([\w]+)\((.+)\)', command)
        if match:
            name = match.group(1)
            command = match.group(2)
        else:
            name = 'remote'
        msg = _("Executing via client '{}': {}").format(name, command)
        debug(msg)
        client = self._clients[name]
        return client.execute(command)


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
