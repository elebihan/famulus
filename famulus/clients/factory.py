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
   famulus.clients.factory
   ```````````````````````

   Classes and helper functions for creating clients.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import urllib.parse
from .local import LocalClient
from .ssh import SSHClient
from .stty import STTYClient
from .uboot import UBootClient
from ..log import debug
from gettext import gettext as _


class UnsupportedSchemeError(Exception):
    """Error raised when an unsupported scheme is used"""
    def __init__(self):
        Exception.__init__(self, _("Unsupported client URI scheme"))


class ClientFactory:
    """Create local/remote clients"""
    def __init__(self):
        self._klasses = {
            "local": LocalClient,
            "ssh": SSHClient,
            "stty": STTYClient,
            "uboot": UBootClient,
        }

    def create_client_for_uri(self, uri):
        """Create a client according to the machine URI.

        @param uri: URI of the machine
        @type uri: str

        @return: a pre-configured client
        @rtype: Client
        """
        try:
            fields = urllib.parse.urlsplit(uri)
            klass = self._klasses[fields.scheme]
        except:
            raise UnsupportedSchemeError

        if fields.hostname:
            resource = fields.hostname
        elif fields.path:
            resource = fields.path
        else:
            raise UnsupportedSchemeError
        msg = _("Created client with scheme '{}' for {}")
        debug(msg.format(fields.scheme, resource))
        client = klass(resource)
        client.username = fields.username
        client.password = fields.password
        return client

# vim: ts=4 sw=4 sts=4 et ai
