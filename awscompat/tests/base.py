import httplib2
import telnetlib
import paramiko
from cStringIO import StringIO
from uuid import uuid4
from awscompat import util
from socket import timeout

class TestNode(object):

    depends = {}

    def __init__(self):
        self.http = httplib2.Http()

    def pre(self, **kwargs):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def make_uuid(self, prefix=None):
        return "awscompat_%s%s" % (
            "%s_" % prefix if prefix else '',
            uuid4().hex
        )

    def testSSH(self, key, username, host):
        key_file = StringIO(key)
        rsa_key = paramiko.RSAKey(file_obj=key_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        try:
            client.connect(host, username=username, pkey=rsa_key,
                           timeout=5, look_for_keys=False)
#            client.exec_command('uname')
        except paramiko.SSHException as e:
            # TODO: log e
            print "sshexception: ", e
            return False
        return True

        #output = channel.makefile('rb', -1).readlines()
        #return bool(len(output))

    def testTelnet(self, host, port, timeout=5):
        client = telnetlib.Telnet()

        try:
            client.open(host, port, timeout)
        except timeout:
            return False
        finally:
            client.close()
        return True

    @staticmethod
    def assert_raises(exc):
        """
        Decorator for functions which should raise exceptions.

        Will invoke the method upon definition.
        method should take no arguments.
        exc is the type of exception expected.
        """
        def wraps(f):
            threw = False
            try:
                f()
            except Exception, e:
                if isinstance(e, exc):
                    threw = True
                else:
                    raise e
            assert threw
        return wraps
