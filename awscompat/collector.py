class Runner(object):

    def __init__(self, classes):
        self.branches = {}

        for klass in classes:
            parent = klass.depends
            if parent not in self.branches:
                self.branches[parent] = {}
            self.branches[parent][klass] = {}

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

"""
for klass in x:
    parent = None
    obj = klass(parent)


def populate(classes):

    _map = {}

    for klass in classes:
        obj = klass()
        _map[klass] = obj
"""

"""
classes = []

for i in TestS3Bucket, TestS3Object:
    classes.append((i, i.parent))

print classes


tree = {}

for klass, parent in classes:
    if not parent:
        tree[klass] = {}
    else:

"""
