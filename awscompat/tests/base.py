from uuid import uuid4

class TestNode(object):

    depends = None

    def __init__(self, parent_obj=None):
        self.parent = parent_obj

    def pre(self, **kwargs):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def make_uuid(self, prefix=None):
        return "awscompat_%s%s" % (
            "%s_" % prefix if prefix else '',
            uuid4().hex
        )
