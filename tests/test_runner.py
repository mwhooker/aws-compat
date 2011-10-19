import functools
import topsort
from awscompat import runner
from unittest import TestCase



class MockNode(object):

    def pre(self, **parents):
        self.record.append(self.__class__.__name__ + '_pre')

    def post(self):
        self.record.append(self.__class__.__name__ + '_post')


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

        lhs = lhs.__name__ + '_pre'
        rhs = rhs.__name__ + '_pre'
        return self.index(lhs) < self.index(rhs)

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
        print self.call_record

        self.assertTrue(self.call_record.testOrder(a, b))
        self.assertTrue(self.call_record.testOrder(b, c))
        self.assertTrue(self.call_record.testOrder(a, d))

    def test_cycles(self):
        a = self.build('a')
        b = self.build('b', a)
        a.depends = {'b': b}

        self.assertRaises(topsort.CycleError, runner.Runner, [a, b])
