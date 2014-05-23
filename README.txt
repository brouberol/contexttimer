----------------------------
A timer as a context manager
----------------------------

``contexttimer`` provides you with a couple of utilities to quickly measure the execution time of a code block or a function.

Timer as a context manager
--------------------------
``contexttimer.Timer`` is a context manager measuring the execution time of the code block it contains.
The elapsed time is accessible through the ``elapsed`` property.

>>> with Timer() as t:
...     # some code here
>>> print t.elapsed
# a value in seconds


The ``contexttimer.Timer`` context manager
------------------------------------------
``contexttimer.Timer`` is a `context manager <http://docs.python.org/reference/datamodel.html#context-managers>`_ with 2 parameters and a public property:

* ``default_timer``: a platform specific timer function (``time.time`` for Unix platforms and ``time.clock`` for Windows platforms). You can instanciate a ``Timer`` object with your own timer, by passing it to the constructor.
* ``factor``: a multiplying factor applied to the ``elapsed`` property. For example, a factor or 1000 will lead to ``elapsed`` being expressed in milliseconds instead of seconds. Default value of 1.
* ``elapsed``: (read only property) the wall clock timing of the execution of the code block, in seconds. By default, expressed in seconds.

Example
"""""""

>>> from contexttimer import Timer
>>> with Timer() as t:
...     for i in xrange(10000000):
...         pass
...
>>> print(t.elapsed)
73.6618041992 # in miliseconds

Note that ``elapsed`` is calculated on demand, so it is possible to time sub-parts of your code block:

>>> with Timer() as t:
...     # do some things
...     print t.elapsed
...     # do other tings
...     print t.elapsed
...
10.122  # in ms
20.567


The ``contexttimer.timer`` function decorator
---------------------------------------------

You can use the ``@timer`` function decorator to measure the time execution of an entire function.
When the function returns its value, its execution time will be printed to the stdout (default), or to the argument logger.


Examples
""""""""
>>> @timer
... def sleep_for_2s():
...     time.sleep(2)

>>> sleep_for_2s()
function sleep_for_2s execution time: 2.002

>>> logging.basicConfig()
>>> @timer(logger=logging.getLogger())
... def sleep_for_2s():
...     time.sleep(2)

>>> sleep_for_2s()
DEBUG:root:function blah execution time: 2.002

As it makes use of the ``Timer`` context manager inside, all arguments passed to the ``@timer`` decorator will be used a ``Timer`` init arguments.

Example:
""""""""

>>> @timer(factor=1000)
... def sleepawhile(n):
...     time.sleep(n)
...
>>> sleepawhile(2)
function sleepawhile execution time: 2000.089

The ``contexttimer.timeout.timeout`` decorator
----------------------------------------------

You can use the ``@timeout`` function decorator to stop a function/method call and call a handler if the call exceeds a fixed amount of time.


Example:
""""""""

>>> def timeout_handler(limit, f, *args, **kwargs):
...     print "{func} call timed out after {lim}s.".format(
...         func=f.__name__, lim=limit)
...
>>> @timeout(limit=5, handler=timeout_handler)
... def work(foo, bar, baz="spam")
...     time.sleep(10)
>>> work("foo", "bar", "baz")
# time passes...
work call timed out after 5s.
>>>


Thanks
------
Thanks to halloi, wolanko and Jon Blackburn for their helpful insights and contributions.

License
-------
``contexttimer`` is released under the GPLv3 license.
