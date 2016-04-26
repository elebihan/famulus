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
   famulus.log
   ```````````

   Helper functions for logging

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import sys
import logging
from colorama import init, Fore

__LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

try:
    __level = __LOG_LEVELS[os.environ.get('FAMULUS_LOG', 'info').lower()]
except:
    __level = logging.INFO

__logger = logging.getLogger('famulus')
__logger.setLevel(__level)


class ColoredFormatter(logging.Formatter):
    """Add color to messages.

    @param fmt: format string
    @type: str
    """
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        colors = {
            'WARNING': Fore.YELLOW,
            'INFO': '',
            'DEBUG': Fore.BLUE,
            'CRITICAL': Fore.MAGENTA,
            'ERROR': Fore.RED,
        }
        message = logging.Formatter.format(self, record)
        return colors[record.levelname] + message


class LevelFilter(logging.Filter):
    def __init__(self, allowed, reject):
        self._allowed = allowed
        self._reject = reject

    def filter(self, record):
        if self._reject:
            return record.levelno != self._allowed
        else:
            return record.levelno == self._allowed


def _create_handler(stream, allowed, reject):
    fmt = "%(levelname)s: %(message)s"
    handler = logging.StreamHandler(stream)
    filter = LevelFilter(allowed, reject)
    handler.addFilter(filter)
    if stream.isatty():
        formatter = ColoredFormatter(fmt)
        init(autoreset=True)
    else:
        formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    return handler


def setup_logging():
    """Set up logging system"""
    h1 = _create_handler(sys.stdout, logging.INFO, False)
    h2 = _create_handler(sys.stderr, logging.INFO, True)
    for h in __logger.handlers:
        __logger.removeHandler(h)
    __logger.addHandler(h1)
    __logger.addHandler(h2)


def debug(message):
    """Log a debug message.

    The message will only be printed to standard output if the environment
    variable 'FAMULUS_LOG' is set to 'DEBUG'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.debug(message)


def warning(message):
    """Log a warning message.

    The message will only be printed to standard output if the environment
    variable 'FAMULUS_LOG' is set to 'WARNING'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.warning(message)


def info(message):
    """Log an informative message.

    The message will only be printed to standard output if the environment
    variable 'FAMULUS_LOG' is set to 'INFO'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.info(message)


def error(message):
    """Log an error message.

    The message will only be printed to standard error if the environment
    variable 'FAMULUS_LOG' is set to 'ERROR'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.error(message)


def set_level(level):
    """Set current logging level.

    @param level: the new logging level
    @type level: str
    """
    __logger.setLevel(level)

# vim: ts=4 sw=4 sts=4 et ai
