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

# TODO: in certain cases (ie TestInstance.post), we don't want to retry until
# this function succeeds, because the expected behavior is that it fails.
    def canSSH(self, key, username, host):
        key_file = StringIO(key)
        rsa_key = paramiko.RSAKey(file_obj=key_file)

        def connect():
            transport = paramiko.Transport((host, 22))
            transport.connect(username=username, pkey=rsa_key)
            channel = transport.open_session()
            channel.exec_command('uname')
            output = channel.makefile('rb', -1).readlines()
            return bool(len(output))

        try:
            return util.retry(connect, max_tries=7, wait_exp=2)
        except Exception as e:
            # todo: log e
            return False

    def canTelnet(self, host, port):
        client = telnetlib.Telnet()

        try:
            client.open(host, port, timeout=5)
        except timeout:
            return False
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
