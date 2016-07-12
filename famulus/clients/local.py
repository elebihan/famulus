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
   famulus.clients.local
   `````````````````````

   Classes and helper functions for interacting with local machine.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .client import Client, CommandFailedError
from subprocess import check_output, CalledProcessError


class LocalClient(Client):
    """Client which interacts with the local machine"""

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def execute(self, command):
        try:
            return check_output(command.split(), universal_newlines=True)
        except CalledProcessError as e:
            raise CommandFailedError(str(e))


# vim: ts=4 sw=4 sts=4 et ai
