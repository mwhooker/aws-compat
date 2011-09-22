from base import TestNode
from awscompat.connections import S3_CONN, EC2_CONN


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

class TestImageCration(TestNode):

    depends = TestSecurityGroups

    def setUp(self):
        self.image_path = self.make_key('image_path')
        self.image_bucket = self.make_key('image_bucket')

    def pre(self):
        bucket = S3_CONN.get_bucket(self.image_buckewt)
        k = Key(bucket)
        k.key = self.image_path
        k.set_contents_from_filename(path_to_image)

    def pre_condition(self):
        pass

    def post(self):
        pass

    def post_condition(self):
        pass
