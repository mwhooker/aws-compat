import base64
import paramiko
import boto.exception
from cStringIO import StringIO
from base import TestNode
from awscompat import s3_conn, ec2_conn, config, util


class TestSecurityGroups(TestNode):
    """Test security group generation."""

    def pre(self):
        self.group_name = self.make_uuid('group_name')
        self.group_desc = self.make_uuid('group_desc')

        self.group = ec2_conn.create_security_group(
            self.group_name,
            self.group_desc
        )

        assert len(ec2_conn.get_all_security_groups(
            groupnames=[self.group_name]))

    def post(self):
        self.group.delete()
        assert not len(ec2_conn.get_all_security_groups(
            groupnames=[self.group_name]))

class TestKeyPairs(TestNode):
    """Test keypair generation."""

    def pre(self, security_group):
        self.key_name = self.make_uuid('key_name')
        self.keypair = ec2_conn.create_key_pair(self.key_name)

        assert len(ec2_conn.get_all_key_pairs(keynames=[self.key_name]))

    def post(self):
        ec2_conn.delete_key_pair(self.key_name)

        @self.assert_raises(boto.exception.EC2ResponseError)
        def test_boto_throw():
            ec2_conn.get_all_key_pairs(keynames=[self.key_name])


class TestInstance(TestNode):
    """Test EC2 image launch and termination."""

    depends = {
        'key_pairs': TestKeyPairs,
        'security_group': TestSecurityGroups
    }


    def pre(self, key_pairs=None, security_group=None):
        image_id = config['ec2']['test_image_id']
        self.image = ec2_conn.get_all_images(image_ids=[image_id])[0]
        self.security_group = security_group
        self.key_pairs = key_pairs

        self.security_group.group.authorize('tcp', 22, 22, '0.0.0.0/0')
        self.reservation = self.image.run(
            instance_type='t1.micro',
            security_groups=[self.security_group.group_name],
            key_name=self.parent.key_name
        )

        util.wait(
            lambda: self.reservation.instances[0].update() == 'running',
            timeout=70
        )

        assert self.canSSH(
            self.parent.keypair.material.encode('ascii'),
            'ec2-user',
            self.reservation.instances[0].public_dns_name
        )


    def post(self):
        self.reservation.instances[0].terminate()
        util.wait(
            lambda: self.reservation.instances[0].update() == 'terminated',
            timeout=120
        )

        assert not self.canSSH(
            self.parent.keypair.material.encode('ascii'),
            'ec2-user',
            self.reservation.instances[0].public_dns_name
        )


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
