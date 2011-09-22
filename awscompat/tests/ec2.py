from boto.ec2.connection import EC2Connection

from base import TestNode


EC2_CONN = EC2Connection()

class TestSecurityGroups(TestNode):

    def setUp(self):
        self.group_name = self.make_key('group_name')
        self.group_desc = self.make_key('group_desc')

    def pre(self):
        self.group = EC2_CONN.create_security_group(
            self.group_name,
            self.group_desc
        )

    def pre_condition(self):
        assert repr(self.group) in [repr(g) for g in
                                    EC2_CONN.get_all_security_groups()]

    def post(self):
        self.group.delete()

    def post_condition(self):
        assert repr(self.group) not in [repr(g) for g in
                                        EC2_CONN.get_all_security_groups()]
