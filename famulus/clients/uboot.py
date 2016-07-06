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
   famulus.clients.uboot
   `````````````````````

   Classes and helper functions for interacting with U-Boot via serial port.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .serial import SerialClient


class UBootClient(SerialClient):
    """Client which interacts with U-Boot via serial port"""
    def __init__(self, resource):
        SerialClient.__init__(self, resource)
        self.shell_prompt = r'[\w]+ > '

# vim: ts=4 sw=4 sts=4 et ai
