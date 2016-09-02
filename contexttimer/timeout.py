# -*- coding: utf-8 -*-

"""
Definition of timeout decorators.

If the clock time of a function/method call, decorated with @timeout,
exceeds a given limit, a handler will be called and the call will be
terminated.
The timeout decorator currently only works in Unix systems.

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

import signal


class Timeout(Exception):
    pass


def timeout_handler(signum, frame):
    raise Timeout


def timeout(limit, handler):
    """A decorator ensuring that the decorated function tun time does not
    exceeds the argument limit.

    :args limit: the time limit
    :type limit: int

    :args handler: the handler function called when the decorated
    function times out.
    :type handler: callable

    Example:
    >>>def timeout_handler(limit, f, *args, **kwargs):
    ...     print "{func} call timed out after {lim}s.".format(
    ...         func=f.__name__, lim=limit)
    ...
    >>>@timeout(limit=5, handler=timeout_handler)
    ... def work(foo, bar, baz="spam")
    ...     time.sleep(10)
    >>>work("foo", "bar", "baz")
    # time passes...
    work call timed out after 5s.
    >>>


    """
    def wrapper(f):
        def wrapped_f(*args, **kwargs):
            old_handler = signal.getsignal(signal.SIGALRM)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(limit)
            try:
                res = f(*args, **kwargs)
            except Timeout:
                handler(limit, f, args, kwargs)
            else:
                return res
            finally:
                signal.signal(signal.SIGALRM, old_handler)
                signal.alarm(0)
        return wrapped_f
    return wrapper
