from unittest import TestCase
from awscompat import util

class TestRetry(TestCase):

    def setUp(self):
        self.mock_called = 0

    def _mock(self, succeed_on_try=None):
        self.mock_called += 1
        if self.mock_called == succeed_on_try:
            return 42
        print self.mock_called
        raise Exception

    def test_decorator(self):

        @util.retry(max_tries=5)
        def mock():
            return self._mock(succeed_on_try=2)

        self.assertEqual(mock(), 42)
        self.assertEqual(self.mock_called, 2)


    def test_invoke(self):
        mock = lambda: self._mock(succeed_on_try=2)

        ret = util.retry(mock, max_tries=5)
        self.assertEqual(ret, 42)
        self.assertEqual(self.mock_called, 2)

    def test_raises(self):
        mock = lambda: self._mock()

        self.assertRaises(Exception, util.retry, (mock,))
