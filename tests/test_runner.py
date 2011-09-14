from unittest import TestCase
from awscompat.runner import Runner


CALLS = []

class MockBase(object):

    def __init__(self, parent):
        pass

    def __getattr__(self, name):

        if name not in ['setUp', 'pre', 'pre_condition', 'post',
                        'post_condition']:
            return super(MockBase, self).__getattr__(name)

        CALLS.append("%s.%s" % (self.__class__.__name__, name))

        def do():
            pass

        return do

class A(MockBase):
    depends = None
class B(MockBase):
    depends = A
class C(MockBase):
    depends = B
class D(MockBase):
    depends = A
class E(MockBase):
    depends = None

class TestRunner(TestCase):

    def setUp(self):
        global CALLS
        CALLS = []
        self.classes = [A, B, C, D, E]
        self.runner = Runner(self.classes)

    def test_builds_branches(self):
        expected = {
            None: [A, E],
            A: [B, D],
            B: [C]
        }

        self.assertEquals(self.runner.branches, expected)

    def test_calls_in_order(self):
        expected_calls = [
            'A.setUp', 'A.pre', 'A.pre_condition',
                'B.setUp', 'B.pre', 'B.pre_condition',
                    'C.setUp', 'C.pre', 'C.pre_condition',
                    'C.post', 'C.post_condition',
                'B.post', 'B.post_condition',
                'D.setUp', 'D.pre', 'D.pre_condition',
                'D.post', 'D.post_condition',
            'A.post', 'A.post_condition',
            'E.setUp', 'E.pre', 'E.pre_condition',
            'E.post', 'E.post_condition']

        self.runner.run()
        self.assertEqual(CALLS, expected_calls)
