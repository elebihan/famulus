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
   famulus.clients.serial
   ``````````````````````

   Classes and helper functions for interacting with machine via serial port.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import time
from .client import Client, CommandFailedError, MissingCredentialsError
from ..interactors.serial import SerialInteractor
from gettext import gettext as _


class SerialClient(Client):
    """Client which interacts with the machine via serial port"""
    def __init__(self, resource):
        self._serial = SerialInteractor(resource)
        self.shell_prompt = '# '
        self.login_prompt = None
        self.passw_prompt = None
        self.cmd_delay = 0.1

    def _login(self):
        self._serial.send('')
        if self.login_prompt:
            if not self.username:
                raise MissingCredentialsError(_("missing username"))
            self._serial.expect(self.login_prompt)
            self._serial.send(self.username)
            if self.password:
                self._serial.expect(self.passw_prompt)
                self._serial.send(self.password)
            self._serial.expect(self.shell_prompt)

    def _logout(self):
        if self.login_prompt:
            self._serial.interrupt(b'\04')

    def execute(self, command):
        time.sleep(self.cmd_delay)
        self._serial.reset_buffers()
        try:
            self._serial.send(command)
            lines = self._serial.expect(self.shell_prompt)
            return '\n'.join(lines)
        except Exception as e:
            raise CommandFailedError(str(e))

    def connect(self):
        self._serial.open()
        self._login()
        self._connected = True

    def disconnect(self):
        self._logout()
        self._serial.close()
        self._connected = False

# vim: ts=4 sw=4 sts=4 et ai
