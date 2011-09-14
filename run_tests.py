#!/usr/bin/env python
import os.path

from awscompat.tests.s3 import TestS3Bucket, TestS3Object
from awscompat import collector
from awscompat import runner


test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')

classes = collector.collect(test_dir)
runner = runner.Runner(classes)
runner.run()
