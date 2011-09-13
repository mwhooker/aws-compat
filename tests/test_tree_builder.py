from unittest import TestCase
from awscompat import collector


class TestTreeBuilder(TestCase):

    def test_builds_tree(self):

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

        klasses = [A, B, C, D, E]

        expected = {
            A: {
                B: {
                    C: {
                    }
                },
                D: {
                }
            },
            E: {
            }
        }

        self.assertEqual(collector.build_graph(klasses), expected)

    def test_runs_in_order(self):
        assert False

    def test_failure_pruning(self):
        assert False

    def test_correct_children_received(self):
        assert False
