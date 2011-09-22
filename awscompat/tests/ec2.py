from boto.ec2.connection import EC2Connection

from base import TestNode

class TestSecurityGroups(TestNode):

    def setUp(self):
        self.conn = EC2Connection()
        self.group_name = self.make_key('group_name')
        self.group_desc = self.make_key('group_desc')

    def pre(self):
        self.group = self.conn.create_security_group(
            self.group_name,
            self.group_desc
        )

    def pre_condition(self):
        assert repr(self.group) in [repr(g) for g in self.conn.get_all_security_groups()]

    def post(self):
        self.group.delete()

    def post_condition(self):
        assert repr(self.group) not in [repr(g) for g in self.conn.get_all_security_groups()]
