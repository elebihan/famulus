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


class CommandRunner:
    """Run commands on local/remote machine.

    @param uri: URI of the remote machine
    @type uri: str
    """
    def __init__(self, uri):
        factory = ClientFactory()
        self._clients = {
            'local': factory.create_client_for_uri('local://'),
            'remote': factory.create_client_for_uri(uri),
        }

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


# vim: ts=4 sw=4 sts=4 et ai
