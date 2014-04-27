import contextlib
from datetime import datetime
import functools
import inspect
import os
import sys

import unittest2 as unittest

from src import clogger


logger = clogger.setup_custom_logger(__name__)


class MultipleAssertionError(AssertionError):
    pass


def _suppress_log_assertion_errors(assertion_method):
    """
     Suppresses and logs all types of AssertionError exceptions and appends them to _suppressed_assertions list. To
     raise exception immediately add {always_raise = True} parameter in your assert method.
    """
    @functools.wraps(assertion_method)
    def wrapped(self, *args, **kwargs):
        always_raise = kwargs.pop('always_raise', False)
        try:
            assertion_method(self, *args, **kwargs)
        except AssertionError:
            exc_info = sys.exc_info()
            logger.error('Assertion error:\n %s', exc_info[1])

            filename = os.environ.get('LOG_DIR','/Users/farooque/PycharmProjects/crittercism/logs') + "/screenshots/" + \
                       self._testMethodName + \
                       datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%ss') + ".png"
            #self.browser.get_screenshot_as_file(filename)
            self.browser.save_screenshot(filename)
            logger.error("Screenshot on failure saved: %s with URL %s" % (filename, self.browser.current_url))

            if not self._suppress_assertions or always_raise:
                raise exc_info[0], exc_info[1], exc_info[2]
            else:
                self._suppressed_assertions.append(exc_info)

    return wrapped


class TestCaseWithMultipleAssertions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaseWithMultipleAssertions, self).__init__(*args, **kwargs)
        self._suppress_assertions = False
        self._suppressed_assertions = []

    @classmethod
    def _wrap_assertions(cls):

        """
        Wraps all  the methods of unittest.TestCase base class which names start from "assert" or "fail" with
        _suppress_log_assertion_errors decorator
        """
        for name in dir(cls):
            if not (name.startswith('assert') or name.startswith('fail')):
                continue
            old_value = getattr(cls, name, None)
            if not inspect.ismethod(old_value):
                continue
            setattr(cls, name, _suppress_log_assertion_errors(old_value))

    @contextlib.contextmanager
    def multiple_assertions(self):
        """
        Creates the context manager to handle multiple assertions in tests cases
        """
        self._suppress_assertions = True
        self._suppressed_assertions = []
        try:
            # all your assertions are called here:
            yield
            if len(self._suppressed_assertions) == 1:
                exc_info = self._suppressed_assertions[0]
                raise exc_info[0], exc_info[1], exc_info[2]
            elif self._suppressed_assertions:
                assertions_gen = (ei[1] for ei in self._suppressed_assertions)
                msg = 'Multiple assertions failed:\n %s' % (
                    ',\n '.join(str(a) for a in assertions_gen))
                raise MultipleAssertionError(msg)
        finally:
            self._suppress_assertions = False
            self._suppressed_assertions = []

#Apply _wrap_assertions method during the import of TestCaseWithMultipleAssertions class
TestCaseWithMultipleAssertions._wrap_assertions()
