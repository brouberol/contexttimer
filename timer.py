#!/usr/bin/env python
""" 
Define a Timer context manager, allowing to measure the 
wall time of the code block it contains.

Example:
>>> with Timer() as timer:
...     for i in xrange(10000000):
...             pass
... 
>>> print(timer.start)
1341568310.06
>>> print(timer.end)
1341568310.14
>>> print(timer.elapsed_ms) 
73.6618041992
>>> print(timer.elapsed_secs)
0.0736618041992

Written by Balthazar Rouberol - <brouberol@imap.cc>
"""

from timeit import default_timer


class Timer(object):
    """ A timer as a context manager. """
    
    def __init__(self):
        self.timer = default_timer 
        # measures wall clock time, not CPU time!
        # On Unix systems, it corresponds to time.time
        # On Windows systems, it corresponds to time.clock

    def __enter__(self):
        self.start = self.timer() # measure start time
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end = self.timer() # measure end time
        self.elapsed_s = self.end - self.start # elapsed time, in seconds
        self.elapsed_ms = self.elapsed_s * 1000  # elapsed time, in milliseconds

