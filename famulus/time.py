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
   famulus.time
   ````````````

   Time management classes and helper functions

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""


from datetime import datetime, timedelta
from gettext import gettext as _


class StopwatchStateError(Exception):
    """Error raised when improperly accessing the stopwatch data"""
    def __init__(self):
        Exception.__init__(self, _("Illegal stopwatch state"))


class Stopwatch:
    """Measure the amount of time elapsed."""
    def __init__(self):
        self._start_time = None
        self._stop_time = None

    def start(self):
        """Start measurement"""
        self._start_time = datetime.now()

    def stop(self):
        """Stop measurement"""
        self._stop_time = datetime.now()

    def reset(self):
        """Reset the stopwatch"""
        self._start_time = None
        self._stop_time = None

    @property
    def start_time(self):
        """Return the time when the stopwatch was started.

        @return: the start time
        @rtype: datetime

        @raise: StopwatchStateError
        """
        if self._start_time:
            return self._start_time
        raise StopwatchStateError

    @property
    def stop_time(self):
        """Return the time when the stopwatch was stopped.

        @return: the stop time
        @rtype: datetime

        @raise: StopwatchStateError
        """
        if self._start_time:
            return self._start_time
        raise StopwatchStateError

    @property
    def elapsed_time(self):
        """Return the amount of time elapsed.

        @return: time elapsed
        @rtype: timedelta
        """
        if self._start_time:
            if self._stop_time:
                return self._stop_time - self._start_time
            else:
                return datetime.now() - self._start_time
        else:
            return timedelta()

    @property
    def is_running(self):
        """Tell whether the stopwatch is running or not"""
        return ((self._start_time is not None) and (self._stop_time is None))

    @property
    def has_run(self):
        """Tell whether the stopwatch has run or not"""
        return (self._start_time and self._stop_time)


# vim: ts=4 sw=4 sts=4 et ai
