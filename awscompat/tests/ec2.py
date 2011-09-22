import base64
import paramiko
import boto.exception
from cStringIO import StringIO
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
        threw = False
        try:
            ec2_conn.get_all_key_pairs(keynames=[self.key_name])
        except boto.exception.EC2ResponseError:
            # this should be a 400
            threw = True
        assert threw

class TestInstance(TestNode):

    depends = TestKeyPairs


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

        util.wait(
            lambda: self.reservation.instances[0].update() == 'running',
            timeout=70
        )

    def pre_condition(self):
        key_file = StringIO(self.parent.keypair.material.encode('ascii'))
        rsa_key = paramiko.RSAKey(file_obj=key_file)
        host = self.reservation.instances[0].public_dns_name

        transport = paramiko.Transport((host, 22))
        transport.connect(username='ec2-user', pkey=rsa_key)
        channel = transport.open_session()
        channel.exec_command('uname')
        output = channel.makefile('rb', -1).readlines()
        print "output: ", output

        """
        client = paramiko.SSHClient()
        client.get_host_keys().add(host, 'ssh-rsa', key)
        client.connect(host, username='ec2-user')
        stdin, stdout, stderr = client.exec_command('uname')
        for line in stdout:
            print '... ' + line.strip('\n')
        client.close()
        """

    def post(self):
        self.reservation.instances[0].terminate()
        util.wait(
            lambda: self.reservation.instances[0].update() == 'terminated',
            timeout=120
        )

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
