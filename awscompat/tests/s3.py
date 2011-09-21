import httplib2
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from base import TestNode


class TestBucket(TestNode):

    def setUp(self):
        self.conn = S3Connection()
        self.bucket_name = self.make_key('test_aws_conformance')

    def pre(self):
        self.bucket = self.conn.create_bucket(self.bucket_name)

    def pre_condition(self):

        all_buckets = self.conn.get_all_buckets()
        assert self.bucket_name in [bucket.name for bucket in all_buckets]

    def post(self):
        self.conn.delete_bucket(self.bucket_name)

    def post_condition(self):

        all_buckets = self.conn.get_all_buckets()
        assert self.bucket_name not in [bucket.name for bucket in all_buckets]


class TestObject(TestNode):

    depends = TestBucket

    def setUp(self):
        self.key = self.make_key('test_aws_conformance')
        self.value = self.make_key()

    def _getKey(self):
        k = Key(self.parent.bucket)
        k.key = self.key
        return k

    def pre(self):
        k = self._getKey()
        k.set_metadata('meta', 'data')
        k.set_contents_from_string(self.value)

    def pre_condition(self):
        k = self._getKey()
        assert k.get_contents_as_string() == self.value
        assert k.get_metadata('meta') == 'data'

    def post(self):
        self._getKey().delete()

    def post_condition(self):
        assert not self._getKey().exists()


class TestAcl(TestNode):

    depends = TestObject

    def setUp(self):
        self.h = httplib2.Http()
        self.k = self.parent._getKey()

    def pre(self):
        self.k.make_public()
        #self.parent.parent.bucket.set_acl('public-read', self.parent.key)

    def pre_condition(self):
        url = self.k.generate_url(60 * 60 * 24, query_auth=False)
        resp, content = self.h.request(url, "GET")
        assert resp['status'] == '200'
        assert content == self.parent.value

    def post(self):
        self.k.set_canned_acl('private')

    def post_condition(self):
        url = self.k.generate_url(60 * 60 * 24, query_auth=False)
        resp, content = self.h.request(url, "GET")
        assert resp['status'] == '403'
