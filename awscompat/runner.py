from collections import defaultdict
from topsort import topsort


class TestGraphError(Exception):
    pass


"""
TODO:
    if two nodes depend on the same parent,
    setup/tear down for each branch to provide a 
    clean slate for the children.
    OR
    start from the root for each path
        Z
        |
        A
       / \
      B   C
    Z -> A -> B
    Z -> A -> C
"""
class Runner(object):

    def __init__(self, classes):
        self.failures = []
        self.errors = []
        dependency_pairs = []

        for klass in classes:
            if not len(klass.depends):
                dependency_pairs.append((None, klass))
                continue
            for key in klass.depends:
                dependency_pairs.append((klass.depends[key], klass))

        self.run_order = [klass for klass in topsort(dependency_pairs)
                          if klass]

    def run(self):

        seen = {}

        def next(classes):
            if not len(classes):
                return

            klass = classes.pop(0)
            obj = klass()
            seen[klass] = obj
            parents = {}

            for key in klass.depends:
                try:
                    parents[key] = seen[klass.depends[key]]
                except KeyError:
                    raise TestGraphError(
                        "Dependency %s of class %s "
                        "hasn't been initialized yet." % (
                            klass.depends[key], klass.__name__
                        )
                    )

            try:
                obj.pre(**parents)
            except AssertionError as e:
                self.pre_failure(obj, e)
            except Exception as e:
                self.pre_error(obj, e)
            finally:
                obj.post()
                return

            next(classes)

            try:
                obj.post()
            except AssertionError as e:
                self.post_failure(obj, e)
            except Exception as e:
                self.post_error(obj, e)

        next(list(self.run_order))


    def pre_failure(self, obj, e):
        self.failures.append((obj, e, 'pre'))

    def pre_error(self, obj, e):
        self.errors.append((obj, e, 'pre'))

    def post_failure(self, obj, e):
        self.failures.append((obj, e, 'post'))

    def post_error(self, obj, e):
        self.errors.append((obj, e, 'post'))

    def print_messages(self):
        if len(self.errors):
            print "errors: ", len(self.errors)
            print self.errors

        if len(self.failures):
            print "failures: ", len(self.failures)
            print self.failures

        if not len(self.failures) and not len(self.errors):
            print "OK"
