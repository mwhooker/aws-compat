import logging
from collections import defaultdict
from topsort import topsort

log = logging.getLogger('awscompat')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)


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
                self.pre_failure(obj)
            except Exception as e:
                log.exception(e)
                self.pre_error(obj)
            else:
                next(classes)

            try:
                obj.post()
            except AssertionError as e:
                self.post_failure(obj)
            except Exception as e:
                log.exception(e)
                self.post_error(obj)


        next(list(self.run_order))


    def pre_failure(self, obj):
        self.failures.append((obj, 'pre'))

    def pre_error(self, obj):
        self.errors.append((obj, 'pre'))

    def post_failure(self, obj):
        self.failures.append((obj, 'post'))

    def post_error(self, obj):
        self.errors.append((obj, 'post'))

    def print_messages(self):
        if len(self.errors):
            log.error("errors: %d" % len(self.errors))

        if len(self.failures):
            log.info("failures: %d" % len(self.failures))

        if not len(self.failures) and not len(self.errors):
            log.info('OK')
