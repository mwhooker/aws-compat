import os.path
import json

from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection


CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'config.json'
)

with open(CONFIG_PATH) as f:
    config = json.load(f)

ec2_conn = EC2Connection()
s3_conn = S3Connection()
