from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection


config = None

ec2_conn = EC2Connection()
s3_conn = S3Connection()
