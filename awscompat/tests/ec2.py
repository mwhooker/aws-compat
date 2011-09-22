from base import TestNode
from awscompat import s3_conn, ec2_conn, config


class TestSecurityGroups(TestNode):

    def setUp(self):
        self.group_name = self.make_key('group_name')
        self.group_desc = self.make_key('group_desc')

    def pre(self):
        self.group = ec2_conn.create_security_group(
            self.group_name,
            self.group_desc
        )

    def pre_condition(self):
        assert repr(self.group) in [repr(g) for g in
                                    ec2_conn.get_all_security_groups()]

    def post(self):
        self.group.delete()

    def post_condition(self):
        assert repr(self.group) not in [repr(g) for g in
                                        ec2_conn.get_all_security_groups()]


def TestInstance(TestNode):

    def setUp(self):
        print ec2_conn.get_all_images()

    def pre(self):
        pass

    def pre_condition(self):
        pass

    def post(self):
        pass

    def post_condition(self):
        pass



"""
class TestImageCration(TestNode):

    depends = TestSecurityGroups

    def setUp(self):
        self.image_path = self.make_key('image_path')
        self.image_bucket = self.make_key('image_bucket')

    def pre(self):
        bucket = s3_conn.get_bucket(self.image_buckewt)
        k = Key(bucket)
        k.key = self.image_path
        k.set_contents_from_filename(path_to_image)

    def pre_condition(self):
        pass

    def post(self):
        pass

    def post_condition(self):
        pass
"""
