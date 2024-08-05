"""

Ctimer - A timer context manager measuring the
clock wall time of the code block it contains.

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

__version__ = '0.3.3'


import functools
import collections
import logging

from timeit import default_timer


class Timer(object):

    """ A timer as a context manager

    Wraps around a timer. A custom timer can be passed
    to the constructor. The default timer is timeit.default_timer.

    Note that the latter measures wall clock time, not CPU time!
    On Unix systems, it corresponds to time.time.
    On Windows systems, it corresponds to time.clock.

    Keyword arguments:
        output -- if True, print output after exiting context.
                  if callable, pass output to callable.
        format -- str.format string to be used for output; default "took {} seconds"
        prefix -- string to prepend (plus a space) to output
                  For convenience, if you only specify this, output defaults to True.
    """

    def __init__(self, timer=default_timer, factor=1,
                 output=None, fmt="took {:.3f} seconds", prefix=""):
        self.timer = timer
        self.factor = factor
        self.output = output
        self.fmt = fmt
        self.prefix = prefix
        self.end = None

    def __call__(self):
        """ Return the current time """
        return self.timer()

    def __enter__(self):
        """ Set the start time """
        self.start = self()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Set the end time """
        self.end = self()

        if self.prefix and self.output is None:
            self.output = True

        if self.output:
            output = " ".join([self.prefix, self.fmt.format(self.elapsed)])
            if callable(self.output):
                self.output(output)
            else:
                print(output)

    def __str__(self):
        return '%.3f' % (self.elapsed)

    @property
    def elapsed(self):
        """ Return the current elapsed time since start

        If the `elapsed` property is called in the context manager scope,
        the elapsed time bewteen start and property access is returned.
        However, if it is accessed outside of the context manager scope,
        it returns the elapsed time bewteen entering and exiting the scope.

        The `elapsed` property can thus be accessed at different points within
        the context manager scope, to time different parts of the block.

        """
        if self.end is None:
            # if elapsed is called in the context manager scope
            return (self() - self.start) * self.factor
        else:
            # if elapsed is called out of the context manager scope
            return (self.end - self.start) * self.factor


def timer(f=None, logger=None, level=logging.INFO,
          fmt="function %(function_name)s execution time: %(execution_time).3f",
          **timer_kwargs):
    """ Function decorator displaying the function execution time

    All kwargs are the arguments taken by the Timer class constructor.

    """
    # store Timer kwargs in local variable so the namespace isn't polluted
    # by different level args and kwargs
    if f is None:
        return functools.partial(timer, logger=logger, level=level, fmt=fmt, **timer_kwargs)

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        with Timer(**timer_kwargs) as t:
            out = f(*args, **kwargs)
        context = {
            'function_name': f.__name__,
            'execution_time': t.elapsed,
        }
        if logger:
            logger.log(
                level,
                fmt % context,
                extra=context)
        else:
            print(fmt % context)
        return out
    return wrapped


if __name__ == "__main__":
    import logging
    import time
    logging.basicConfig(level=logging.DEBUG)

    @timer(logger=logging.getLogger())
    def blah():
        time.sleep(2)

    blah()
