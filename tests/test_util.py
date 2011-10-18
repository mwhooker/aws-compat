import functools
from unittest import TestCase
from awscompat import util


class Mock(object):

    def __init__(self):
        self.mock_called = 0

    def __call__(self, succeed_on_try=None):
        self.mock_called += 1
        if self.mock_called == succeed_on_try:
            return 42
        raise Exception

    def testCalled(self, n):
        return self.mock_called == n

    def testValue(self, val):
        return val == 42


class TestWait(TestCase):

    def setUp(self):
        self.mock = Mock()

    def test_loop(self):
        mock = functools.partial(self.mock, succeed_on_try=2)
        util.wait(mock, interval=None)
        self.assertTrue(self.mock.testCalled(2))


class TestRetry(TestCase):

    def setUp(self):
        self.mock = Mock()

    def test_decorator(self):

        @util.retry(max_tries=5)
        def mock():
            return self.mock(succeed_on_try=2)

        self.assertEqual(mock(), 42)
        self.assertTrue(self.mock.testCalled(2))

    def test_invoke(self):
        mock = functools.partial(self.mock, succeed_on_try=2)

        ret = util.retry(mock, max_tries=5)
        self.assertTrue(self.mock.testValue(ret))
        self.assertTrue(self.mock.testCalled(2))

    def test_raises(self):
        self.assertRaises(Exception, util.retry, (self.mock,))
