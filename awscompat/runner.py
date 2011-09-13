from collections import defaultdict


class Runner(object):

    def __init__(self, classes):
        self.branches = defaultdict(list)

        for klass in classes:
            self.branches[klass.depends].append(klass)

    def run(self, parent_klass=None, parent_obj=None):

        if parent_klass not in self.branches:
            return

        for klass in self.branches[parent_klass]:
            print "running ", klass
            obj = klass(parent_obj)
            obj.setUp()
            obj.pre()
            obj.pre_condition()

            self.run(klass, obj)

            obj.post()
            obj.post_condition()
