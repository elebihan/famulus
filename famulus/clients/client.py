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
   famulus.clients.client
   ``````````````````````

   Basic brick for interacting with local/remote machine.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc


class CommandFailedError(Exception):
    """Error raised when a command executed on the machine faile"""
    def __init__(self, message):
        Exception.__init__(self, message)


class Client:
    """Abstract base class for interacting with local/remote machine"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, hostname):
        self._connected = False
        self._hostname = hostname

    @property
    def hostname(self):
        """FQDN or IP address of the machine"""
        return self._hostname

    @abc.abstractmethod
    def connect(self):
        """Connect to the machine"""
        pass


    @abc.abstractmethod
    def disconnect(self):
        """Disconnect from the machine"""
        pass

    @abc.abstractproperty
    def connected(self):
        """Tell whether the client is connected to the machine or not"""
        return self._connected

    @abc.abstractmethod
    def execute(self, command):
        """Execute a command on on the machine.

        @param command: command to be executed
        @type command: str

        @return: output of the command
        @rtype: str

        @raise: CommandFailedError
        """
        pass


# vim: ts=4 sw=4 sts=4 et ai
