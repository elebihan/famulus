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
   famulus.clients.ssh
   ```````````````````

   Classes and helper functions for interacting machine via SSH

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""


import paramiko
from .client import Client, CommandFailedError, MissingCredentialsError
from ..log import debug
from gettext import gettext as _


class SSHClient(Client):
    """Client which interacts with machine via SSH"""
    def __init__(self, resource):
        Client.__init__(self, resource)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self._shell = '/bin/sh -l -c'

    def connect(self):
        if not self.username:
            raise MissingCredentialsError(_("missing username"))
        if not self.password:
            raise MissingCredentialsError(_("missing password"))
        self._ssh.connect(self.resource,
                          username=self.username,
                          password=self.password,
                          look_for_keys=False,
                          allow_agent=False)
        self._connected = True

    def disconnect(self):
        self._ssh.close()
        self._connected = False

    def execute(self, command):
        status, out_buf, err_buf = self.execute_full(command)
        if status != 0:
            text = err_buf.decode('utf-8').strip()
            lines = text.splitlines()
            for line in lines:
                debug('SSHClient: stderr: ' + line)
            if len(lines):
                msg = lines[-1]
            else:
                msg = _("Command exited with code {}").format(status)
            raise CommandFailedError(msg)
        return out_buf.decode('utf-8').strip()

    def execute_full(self, command):
        """Execute a command on the machine

        @param command: command to execute
        @type command: str

        @return: command exit code and stdout/stderr buffers as a tuple
        @rtype: tuple
        """
        status = -1
        stdout_buf = bytearray()
        stderr_buf = bytearray()

        channel = self._ssh.get_transport().open_session()
        stdout = channel.makefile()
        stderr = channel.makefile_stderr()

        channel.exec_command(self._shell + ' \'' + command + '\'')

        while True:
            if channel.recv_ready():
                stdout_buf += stdout.read()
            if channel.recv_stderr_ready():
                stderr_buf += stderr.read()
            if channel.exit_status_ready():
                status = channel.recv_exit_status()
                stdout_buf += stdout.read()
                stderr_buf += stderr.read()
                break

        channel.close()

        return (status, stdout_buf, stderr_buf)

# vim: ts=4 sw=4 sts=4 et ai
