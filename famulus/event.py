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
   famulus.event
   `````````````

   Classes and helper functions for events occuring during test/suite
   execution.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc
from enum import Enum


TestEvent = Enum('TestEvent', 'begin end')


class BaseEventHandler:
    """Abstract base class for test/suite event handler."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, event, name):
        return


class DummyEventHandler(BaseEventHandler):
    """Dummy event handler"""

    def handle(self, event, name):
        pass

# vim: ts=4 sw=4 sts=4 et ai
