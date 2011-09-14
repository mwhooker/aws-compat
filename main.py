from awscompat.tests.s3 import TestS3Bucket, TestS3Object
from awscompat import runner

tree = runner.Runner([TestS3Bucket, TestS3Object])
tree.run()
