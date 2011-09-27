import httplib2
from boto.s3.key import Key
from base import TestNode
from awscompat import s3_conn, config


class TestBucket(TestNode):


    def pre(self):
        self.bucket_name = self.make_uuid('bucket')
        self.bucket = s3_conn.create_bucket(self.bucket_name)

        all_buckets = s3_conn.get_all_buckets()
        assert self.bucket_name in [bucket.name for bucket in all_buckets]

    def post(self):
        s3_conn.delete_bucket(self.bucket_name)

        all_buckets = s3_conn.get_all_buckets()
        assert self.bucket_name not in [bucket.name for bucket in all_buckets]


class TestObject(TestNode):

    depends = {'bucket': TestBucket}

    def _getKey(self):
        k = Key(self.test_bucket.bucket)
        k.key = self.key
        return k

    def pre(self, bucket):
        self.test_bucket = bucket
        self.key = self.make_uuid('object')
        self.value = self.make_uuid()

        k = self._getKey()
        k.set_metadata('meta', 'data')
        k.set_contents_from_string(self.value)

        k = self._getKey()
        assert k.get_contents_as_string() == self.value
        assert k.get_metadata('meta') == 'data'

    def post(self):
        self._getKey().delete()
        assert not self._getKey().exists()


class TestAcl(TestNode):

    depends = {'object': TestObject}

    def pre(self, object):
        self.test_object = object

        self.h = httplib2.Http()
        self.k = self.test_object._getKey()
        self.k.make_public()

        url = self.k.generate_url(60 * 60 * 24, query_auth=False, force_http=True)
        resp, content = self.h.request(url, "GET")
        assert resp['status'] == '200'
        assert content == self.test_object.value

    def post(self):
        self.k.set_canned_acl('private')

        url = self.k.generate_url(60 * 60 * 24, query_auth=False, force_http=True)
        resp, content = self.h.request(url, "GET")
        assert resp['status'] == '403'
