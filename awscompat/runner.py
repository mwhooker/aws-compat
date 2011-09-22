from collections import defaultdict


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
        self.branches = defaultdict(list)

        for klass in classes:
            self.branches[klass.depends].append(klass)

    def run(self, parent_klass=None, parent_obj=None):

        if parent_klass not in self.branches:
            return

        for klass in self.branches[parent_klass]:
            obj = klass(parent_obj)
            obj.setUp()

            try:
                obj.pre()
                obj.pre_condition()
            except (Exception, AssertionError) as e:
                self.pre_failure(obj, e)
                """
                try:
                    obj.post()
                except Exception:
                    pass
                continue
                """

            self.run(klass, obj)

            """
            try:
                obj.post()
            except Exception, e:
                self.post_error(obj, e)
                continue

            try:
                obj.post_condition()
            except (Exception, AssertionError) as e:
                self.post_failure(obj, e)
            """

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
