#!/usr/bin/env python
import argparse
import os
import sys
try:
    import json
except ImportError:
    import simplejson as json
from itertools import ifilter

base = {
    'access_key': None,
    'secret': None,
    'ec2': {
        'url': None,
        "test_image_id": "ami-8e1fece7",
        'test_instance': {
            'instance_type': 't1.micro',
            'ramdisk_id': None,
            'kernel_id': None
        },
        'test_username': 'ec2-user'
    },
    's3': {
        'url': None
    }
}

env_map = {
    'os': {
        'access_key': 'EC2_ACCESS_KEY',
        'secret': 'EC2_SECRET_KEY'
    },
    'aws': {
        'access_key': 'AWS_ACCESS_KEY_ID',
        'secret': 'AWS_SECRET_ACCESS_KEY'
    }
}

def update_env(env_mapping):
    for key in env_mapping:
        base[key] = os.getenv(env_mapping[key])

    base['ec2']['url'] = os.getenv('EC2_URL')
    base['s3']['url'] = os.getenv('S3_URL')

if not any([os.environ.has_key(key) for key in env_map['os'].values() + env_map['aws'].values()]):
    sys.stderr.write("No access keys from the environment found. ")
    sys.stderr.write("Try sourcing your credentials file.\n")
    sys.exit(-1)

parser = argparse.ArgumentParser("Generate config file for awscompat. "
                                 "By default, provide proper config for AWS.")
parser.add_argument('provider', choices=['aws', 'os'],
                    help='generate config for amazon or openstack.')
args = parser.parse_args()

update_env(env_map[args.provider])

print json.dumps(base)
