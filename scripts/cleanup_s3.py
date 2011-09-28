#!/usr/bin/env python

import sys

from boto.s3.connection import S3Connection


conn = S3Connection()


def delete_keys(bucket):
    for key in bucket.list():
        key.delete()


def delete_buckets(buckets):
    for bucket in buckets:
        if bucket.name[:10] == 'awscompat_':
            delete_keys(bucket)
            bucket.delete()


if __name__ == '__main__':
    try:
        delete_buckets(conn.get_all_buckets())
    except Exception, e:
        sys.stderr.write(e)
        sys.exit(-1)
    sys.exit(0)
