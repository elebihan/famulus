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
   famulus.clients.telnet
   ``````````````````````

   Classes and helper functions for interacting with machine via telnet.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import re
import telnetlib
from .client import Client, CommandFailedError, MissingCredentialsError
from gettext import gettext as _


class TelnetClient(Client):
    """Client which interacts with the machine via telnet"""
    def __init__(self, resource):
        Client.__init__(self, resource)
        self._telnet = telnetlib.Telnet()
        self.shell_prompt = r'[\w]+@\([\w]+\):~# '
        self.login_prompt = r'\([\w]+\) login: '
        self.passw_prompt = 'Password: '
        self.timeout = 30

    def _send(self, string):
        self._telnet.write(string.encode('ascii') + b'\n')

    def _expect(self, pattern):
        patterns = [re.compile(pattern.encode('ascii'))]
        (index, match, data) = self._telnet.expect(patterns, self.timeout)
        lines = data.decode('ascii').splitlines()
        return lines[1:-1]

    def _login(self):
        if not self.username:
            raise MissingCredentialsError(_("missing username"))
        self._expect(self.login_prompt)
        self._send(self.username)
        if self.password:
            self._expect(self.passw_prompt)
            self._send(self.password)
            self._expect(self.shell_prompt)

    def _logout(self):
        self._telnet.write(b'\04')

    def execute(self, command):
        try:
            self._send(command)
            lines = self._expect(self.shell_prompt)
            return '\n'.join(lines)
        except Exception as e:
            raise CommandFailedError(str(e))

    def connect(self):
        self._telnet.open(self.resource)
        self._login()
        self._connected = True

    def disconnect(self):
        self._logout()
        self._telnet.close()
        self._connected = False

# vim: ts=4 sw=4 sts=4 et ai
