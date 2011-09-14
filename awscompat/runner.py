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
            except Exception, e:
                print "pre exception: %s" % e
                continue

            self.run(klass, obj)

            try:
                obj.post()
                obj.post_condition()
            except Exception, e:
                print "post exception: %s" % e
