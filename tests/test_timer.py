import contexttimer
import unittest
import mock

import sys
if sys.version_info.major > 2:
    from io import StringIO
else:
    from cStringIO import StringIO


class ContextTimerTest(unittest.TestCase):
    def test_timer_print(self):
        def print_reversed(string):
            print(" ".join(reversed(string.split())))

        tests = [
            # (kwargs, expected_regex)
            ({'output': True}, r"took [0-9.]+ seconds"),
            ({'output': print_reversed}, r"seconds [0-9.]+ took"),

            ({'prefix': 'foo'}, r"foo took [0-9.]+ seconds"),
            ({'output': True, 'prefix': 'foo'}, r"foo took [0-9.]+ seconds"),
            ({'output': True, 'fmt': '{} seconds later...'}, r"[0-9.]+ seconds later..."),
        ]

        for kwargs, expected in tests:
            output = StringIO()
            with mock.patch('sys.stdout', new=output):
                with contexttimer.Timer(**kwargs):
                    pass

            self.assertIsNotNone(output)
            self.assertRegexpMatches(output.getvalue(), expected)

    def test_decorator_print(self):
        # Test direct call.
        expected = r"function foo execution time: [0-9.]+"
        output = StringIO()
        with mock.patch('sys.stdout', new=output):
            @contexttimer.timer
            def foo():
                pass
            foo()
        self.assertIsNotNone(output)
        self.assertRegexpMatches(output.getvalue(), expected)

        # Test calls with 0 or more args.
        tests = [
            ({}, r"function foo execution time: [0-9.]+"),
            ({'fmt': '%(execution_time)s seconds later...'}, r"[0-9.]+ seconds later..."),
        ]

        for kwargs, expected in tests:
            output = StringIO()
            with mock.patch('sys.stdout', new=output):
                @contexttimer.timer(**kwargs)
                def foo():
                    pass
                foo()

            self.assertIsNotNone(output)
            self.assertRegexpMatches(output.getvalue(), expected)
