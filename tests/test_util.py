from unittest import TestCase
from awscompat import util

class TestRetry(TestCase):

    def setUp(self):
        self.mock_called = 0

    def _mock(self, succeed_on_try=None):
        self.mock_called += 1
        if self.mock_called == succeed_on_try:
            return True
        print self.mock_called
        raise Exception

    def test_decorator(self):

        @util.retry(max_tries=5)
        def mock():
            self._mock(succeed_on_try=2)

        print 'mock: ', mock
        mock()
        self.assertTrue(self.mock_called, 2)


    def test_invoke(self):
        def mock():
            self._mock(succeed_on_try=2)

        util.retry(mock, max_tries=5)
        self.assertTrue(self.mock_called, 2)
