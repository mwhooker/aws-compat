from uuid import uuid4
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from awscompat import runner


class TestNode(object):

    depends = None

    def __init__(self, parent_obj=None):
        self.parent = parent_obj

    def setUp(self):
        raise NotImplementedError

    def pre(self):
        raise NotImplementedError

    def pre_condition(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def post_condition(self):
        raise NotImplementedError



class TestS3Bucket(TestNode):

    def setUp(self):
        self.conn = S3Connection()
        self.bucket_name = 'test_aws_conformance_' + uuid4().hex

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

class TestS3Object(TestNode):

    depends = TestS3Bucket

    def setUp(self):
        self.key = 'test_aws_conformance_' + uuid4().hex
        self.value = uuid4().hex
        self.k = Key(self.parent.bucket)
        self.k.key = self.key

    def pre(self):
        self.k.set_contents_from_string(self.value)

    def pre_condition(self):
        assert self.k.get_contents_as_string() == self.value

    def post(self):
        self.k.delete()

    def post_condition(self):
        assert not self.k.get_contents_as_string()


tree = runner.Runner([TestS3Bucket, TestS3Object])
tree.run()
"""


a = TestS3Bucket()
b = TestS3Object(a)
a.setUp()
a.pre()
a.pre_condition()


b.setUp()
b.pre()
b.pre_condition()
b.post()
b.post_condition

a.post()
a.post_condition()
"""
