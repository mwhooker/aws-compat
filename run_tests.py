#!/usr/bin/env python
from awscompat.tests.s3 import test_bucket, test_object, test_acl


for f in (test_bucket, test_object, test_acl):
    f()
