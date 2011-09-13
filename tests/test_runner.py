from unittest import TestCase
from awscompat.runner import Runner



class A(object):
    depends = None
class B(object):
    depends = A
class C(object):
    depends = B
class D(object):
    depends = A
class E(object):
    depends = None

class TestRunner(TestCase):

    def setUp(self):
        self.classes = [A, B, C, D, E]
        self.runner = Runner(self.classes)

    def test_builds_branches(self):
        expected = {
            None: [A, E],
            A: [B, D],
            B: [C]
        }

        self.assertEquals(self.runner.branches, expected)
