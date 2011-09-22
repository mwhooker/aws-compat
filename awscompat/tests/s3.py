import httplib2
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from awscompat import util


S3_CONN = S3Connection()

def test_bucket():
    bucket_name = util.make_key('test_bucket')

    bucket = S3_CONN.create_bucket(bucket_name)
    all_buckets = S3_CONN.get_all_buckets()
    assert bucket_name in [bucket.name for bucket in all_buckets]

    S3_CONN.delete_bucket(bucket_name)
    all_buckets = S3_CONN.get_all_buckets()
    assert bucket_name not in [bucket.name for bucket in all_buckets]


def test_object():

    bucket_name = util.make_key('test_bucket')
    bucket = S3_CONN.create_bucket(bucket_name)

    key = util.make_key('test_object')
    value = util.make_key()

    def get_key():
        k = Key(bucket)
        k.key = key
        return k

    k = get_key()
    k.set_metadata('meta', 'data')
    k.set_contents_from_string(value)

    k = get_key()
    assert k.get_contents_as_string() == value
    assert k.get_metadata('meta') == 'data'

    get_key().delete()
    assert not get_key().exists()


def test_acl():
    bucket_name = util.make_key('test_bucket')
    bucket = S3_CONN.create_bucket(bucket_name)
    key = Key(bucket)
    key.key = util.make_key('test_object')
    key.set_contents_from_string(util.make_key())

    h = httplib2.Http()

    key.make_public()

    url = key.generate_url(60 * 60 * 24, query_auth=False)
    resp, content = h.request(url, "GET")
    assert resp['status'] == '200'
    assert content == key.get_contents_as_string()

    key.set_canned_acl('private')

    url = key.generate_url(60 * 60 * 24, query_auth=False)
    resp, content = h.request(url, "GET")
    assert resp['status'] == '403'
