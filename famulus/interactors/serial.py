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
   famulus.interactors.serial
   ``````````````````````````

   Classes and helper functions for interacting with machines

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import io
import serial
import pexpect
import pexpect_serial
from ..log import debug
from ..errors import TimeoutError
from gettext import gettext as _


class SerialInteractor:
    """Interact with a machine connected via a serial port.

    :param port: name of the serial port to use
    :type port: str

    :param baudrate: baudrate of the serial port
    :type baudrate: int

    :param timeout: maximum duration to wait for a read operation, in seconds.
    :type timeout: int
    """
    def __init__(self, port, baudrate=115200, timeout=30):
        self._port = serial.Serial(None, baudrate=baudrate, timeout=timeout)
        self._port.port = port
        self.line_term = '\n'

    def get_timeout(self):
        return self._port.timeout

    def set_timeout(self, value):
        self._port.timeout = value

    timeout = property(get_timeout, set_timeout, None, 'timeout')

    def get_baudrate(self):
        return self._port.baudrate

    def set_baudrate(self, value):
        self._port.baudrate = value

    baudrate = property(get_baudrate, set_baudrate, None, 'baudrate')

    def open(self):
        """Open the associated serial port and initialize interactor"""
        self._port.open()
        self._output = io.StringIO()
        self._child = pexpect_serial.SerialSpawn(self._port,
                                                 maxread=1,
                                                 timeout=self.timeout,
                                                 encoding='utf-8')
        self._child.logfile_read = self._output

    def close(self):
        """Close the associated serial port and release interactor"""
        self._port.close()

    def send(self, string):
        """Send a string over the serial port, including line terminator.

        :param string: character string to send
        :type string: str
        """
        debug(_("Sending '{}'".format(string)))
        self._child.send(string + self.line_term)

    def expect(self, pattern):
        """Wait for a pattern to be read from serial port.

        :param pattern: regular expression of pattern to wait for
        :type pattern: str

        :return: data read from serial until pattern was found
        :rtype: list of str

        Read data from the serial port and look for a given pattern. When
        found, all the data read is returned as a list of character strings.
        """
        try:
            debug(_("Expecting '{}'".format(pattern)))
            self._child.expect(pattern)
            lines = self._output.getvalue().split('\n')
            self._output.truncate(0)
            return lines[1:-1]
        except pexpect.exceptions.TIMEOUT:
            raise TimeoutError(_("timeout when waiting for pattern"))

    def reset_buffers(self):
        """Reset internal input/output buffers"""
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()

    def interrupt(self, sequence):
        """Send a sequence of characters to interrupt operation.

        :param sequence: list of characters to send
        :type sequence: str
        """
        self._port.write(sequence)

# vim: ts=4 sw=4 sts=4 et ai
