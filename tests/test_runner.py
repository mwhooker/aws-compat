import functools
from awscompat import runner
from unittest import TestCase



class MockNode(object):

    def pre(self, **parents):
        pass

    def post(self):
        self.record.append(self.__class__.__name__)


def build_node(name, depends=None, record=None):
    attrs = {}
    if depends:
        attrs['depends'] = {depends.__class__.__name__: depends}
    else:
        attrs['depends'] = {}
    attrs['record'] = record
    return type(name, (MockNode,), attrs)


class CallRecord(list):

    def testOrder(self, lhs, rhs):
        """Test that class lhs appears before class rhs in self."""
        return self.index(lhs.__name__) < self.index(rhs.__name__)

class TestRunner(TestCase):


    def setUp(self):
        self.call_record = CallRecord()
        self.build = functools.partial(build_node, record=self.call_record)

    def test_order(self):

        a = self.build('a')
        b = self.build('b', a)
        c = self.build('c', b)
        d = self.build('d', a)

        classes = [a, b, c, d]

        fixture = runner.Runner(classes)
        fixture.run()

        self.assertTrue(self.call_record.testOrder(b, a))
        self.assertTrue(self.call_record.testOrder(c, b))
        self.assertTrue(self.call_record.testOrder(d, a))
