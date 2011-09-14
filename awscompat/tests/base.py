class TestNode(object):

    depends = None

    def __init__(self, parent_obj=None):
        self.parent = parent_obj

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
