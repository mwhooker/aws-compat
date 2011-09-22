from uuid import uuid4

class TestNode(object):

    depends = None

    def __init__(self, parent_obj=None):
        self.parent = parent_obj

    def make_key(self, prefix=None):
        return "awscompat_%s%s" % (
            "%s_" % prefix if prefix else '',
            uuid4().hex

    def setUp(self):
        pass

    def pre(self):
        raise NotImplementedError

    def pre_condition(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def post_condition(self):
        raise NotImplementedError
