from uuid import uuid4

class TestNode(object):

    depends = {}

    def pre(self, **kwargs):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def make_uuid(self, prefix=None):
        return "awscompat_%s%s" % (
            "%s_" % prefix if prefix else '',
            uuid4().hex
        )

    def canSSH(self, key, username, host):
        key_file = StringIO(key)
        rsa_key = paramiko.RSAKey(file_obj=key_file)

        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, pkey=rsa_key)
        channel = transport.open_session()
        channel.exec_command('uname')
        output = channel.makefile('rb', -1).readlines()
        print "output: ", output
        return False
        """
        client = paramiko.SSHClient()
        client.get_host_keys().add(host, 'ssh-rsa', key)
        client.connect(host, username='ec2-user')
        stdin, stdout, stderr = client.exec_command('uname')
        for line in stdout:
            print '... ' + line.strip('\n')
        client.close()
        """
