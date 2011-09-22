from base import TestNode
from awscompat import s3_conn, ec2_conn, config, util


class TestSecurityGroups(TestNode):

    def setUp(self):
        self.group_name = self.make_uuid('group_name')
        self.group_desc = self.make_uuid('group_desc')

    def pre(self):
        self.group = ec2_conn.create_security_group(
            self.group_name,
            self.group_desc
        )

    def pre_condition(self):
        assert len(ec2_conn.get_all_security_groups(
            groupnames=[self.group_name]))

    def post(self):
        self.group.delete()

    def post_condition(self):
        assert not len(ec2_conn.get_all_security_groups(
            groupnames=[self.group_name]))

class TestKeyPairs(TestNode):

    depends = TestSecurityGroups

    def setUp(self):
        self.key_name = self.make_uuid('key_name')

    def pre(self):
        self.keypair = ec2_conn.create_key_pair(self.key_name)

    def pre_condition(self):
        assert len(ec2_conn.get_all_key_pairs(keynames=[self.key_name]))

    def post(self):
        ec2_conn.delete_key_pair(self.key_name)

    def post_condition(self):
        assert not len(ec2_conn.get_all_key_pairs(keynames=[self.key_name]))

class TestInstance(TestNode):

    depends = TestKeyPairs

    def _instance_state(self, expected):
        self.reservation.instances[0].update()
        return lambda: self.reservation.instances[0].state == expected

    def setUp(self):
        image_id = config['ec2']['test_image_id']
        self.image = ec2_conn.get_all_images(image_ids=[image_id])[0]
        # hoist down grandparent. see TODO for fix.
        self.security_group = self.parent.parent

    def pre(self):
        self.security_group.group.authorize('tcp', 22, 22, '0.0.0.0/0')
        self.reservation = self.image.run(
            instance_type='t1.micro',
            security_groups=[self.security_group.group_name],
            key_name=self.parent.key_name
        )

        util.wait(self._instance_state('running'))

    def pre_condition(self):
        print self.reservation

    def post(self):
        self.reservation.stop_all()
        util.wait(self._instance_state('terminated'), timeout=120)

    def post_condition(self):
        pass



"""
class TestImageCreation(TestNode):

    depends = TestSecurityGroups

    def setUp(self):
        self.image_path = self.make_uuid('image_path')
        self.image_bucket = self.make_uuid('image_bucket')

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
