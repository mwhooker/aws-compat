import boto.exception
from awscompat import config, util
from awscompat.connections import ec2_conn
from awscompat.tests.base import TestNode

class TestDescribeImages(TestNode):
    """Failing test for https://bugs.launchpad.net/nova/+bug/755829"""

    def pre(self):
        assert ec2_conn.get_all_images(
            [config['ec2']['test_image_id']]
        )[0].name


class TestSecurityGroups(TestNode):
    """Test security group generation."""

    def pre(self):
        self.group_name = self.make_uuid('group_name')
        self.group_desc = self.make_uuid('group_desc')

        self.group = ec2_conn.create_security_group(
            self.group_name,
            self.group_desc
        )

        groups = util.retry(
            lambda: ec2_conn.get_all_security_groups(
                groupnames=[self.group_name])
        )

        assert len(groups)

    def post(self):
        self.group.delete()

        # TODO: this might not raise because of delay.
        # so I can't use the retry controller
        # I should write a general purpose request wrapper
        # which polls until it gets a different response.
        @self.assert_raises(boto.exception.EC2ResponseError)
        def test_throw():
            ec2_conn.get_all_security_groups(groupnames=[self.group_name])


class TestKeyPairs(TestNode):
    """Test keypair generation."""

    def pre(self):
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
        instance_config = config['ec2']['test_instance']

        self.image = ec2_conn.get_all_images(image_ids=[image_id])[0]
        self.security_group = security_group
        self.key_pairs = key_pairs

        self.security_group.group.authorize('tcp', 22, 22, '0.0.0.0/0')
        self.reservation = self.image.run(
            security_groups=[self.security_group.group_name],
            key_name=self.key_pairs.key_name,
            **instance_config
        )

        util.wait(
            lambda: self.reservation.instances[0].update() == 'running',
            timeout=60 * 3
        )

        util.wait(
            lambda: self.testTelnet(
                self.reservation.instances[0].public_dns_name,
                22
            ),
            timeout = 60 * 5
        )

        assert util.retry(
            lambda: self.testSSH(
                self.key_pairs.keypair.material.encode('ascii'),
                config['ec2']['test_username'],
                self.reservation.instances[0].public_dns_name
            ),
            wait_exp=2
        )


    def post(self):

        self.reservation.instances[0].terminate()
        #ec2_conn.terminate_instances([self.reservation.instances[0].id])
        util.wait(
            lambda: self.reservation.instances[0].update() == 'terminated',
            timeout=60 * 2
        )

        assert util.retry(
            lambda: not self.testSSH(
                self.key_pairs.keypair.material.encode('ascii'),
                config['ec2']['test_username'],
                self.reservation.instances[0].public_dns_name
            ),
            wait_exp=2
        )
