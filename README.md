## A timer as a context manager

When you want to measure the wall clock time of a code snippet, I usually do:

    start = time.time()
    # ...
    # Some code we want to time
    # ...
    end = time.time()
    elapsed = start - end # in secs
    elapsed_ms = elapsed * 1000 # in ms

I find this quite heavy to read and un-pythonic. `timer` allows you to do 
the exact same thing with a context manager:

    with Timer() as t:
        # Some code we want to time
    print t.elapsed_s
    print t.elapsed_ms

## The timer.Timer class
`timer.Timer` is a [context manager](http://docs.python.org/reference/datamodel.html#context-managers) with 5 attributes:
* `default_timer`: a platform specific timer function (`time.time` for Unix platforms and `time.clock` for Windows platforms)
* `start`: the time of the beginning of the execution of the code block, measured with  `default_timer`
* `end`: the time of the end of the execution of the code block, measured with  `default_timer`
* `elapsed_s`: the wall clock timing of the execution of the code block, in seconds
* `elapsed_ms`: the wall clock timing of the execution of the code block, in miliseconds

## Example

    >>> with Timer() as t:
    ...     for i in xrange(10000000):
    ...             pass
    ... 
    >>> print(t.start)
    1341568310.06
    >>> print(t.end)
    1341568310.14
    >>> print(t.elapsed_ms) 
    73.6618041992 # in miliseconds
    >>> print(t.elapsed_s)
    0.0736618041992 # in seconds
