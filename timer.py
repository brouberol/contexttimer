"""

Ctimer - A timer context manager measuring the
wall time of the code block it contains.

Copyright (C) 2013 Balthazar Rouberol - <brouberol@imap.cc>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from timeit import default_timer


class Timer(object):
    """ A timer as a context manager. """

    def __init__(self, timer=default_timer):
        self.timer = timer
        # default_timer measures wall clock time, not CPU time!
        # On Unix systems, it corresponds to time.time
        # On Windows systems, it corresponds to time.clock

    def __enter__(self):
        """ Store the start time """
        self.start = self.timer()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Store the start time and calculate the elapsed time (in s and ms)

        """
        self.end = self.timer()  # measure end time

        # elapsed time, in seconds
        self.elapsed_seconds = self.end - self.start

        # elapsed time, in ms
        self.elapsed_milliseconds = self.elapsed_seconds * 1000

    def __call__(self):
        """ Return the current time """
        return self.timer()
