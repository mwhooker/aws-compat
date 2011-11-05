#!/usr/bin/env python
import argparse
import os
import sys
try:
    import json
except ImportError:
    import simplejson as json
from itertools import ifilter


def update_env(env_mapping):
    for key in env_mapping:
        base[key] = os.getenv(env_mapping[key])

def update_os():
    base['ec2']['url'] = os.getenv('EC2_URL')
    base['ec2']['region_name'] = 'nova'
    base['s3']['url'] = os.getenv('S3_URL')

    base['ec2']['test_username'] = os.getenv('NOVA_USERNAME')

def update_aws():
    base['ec2']['test_username'] = 'ec2-user'
    base['ec2']['test_image_id'] = 'ami-8e1fece7'
    base['ec2']['test_instance']['instance_type'] = 't1.micro'

base = {
    'access_key': None,
    'secret': None,
    'ec2': {
        'region_name': None,
        'url': None,
        "test_image_id": None,
        'test_instance': {
            'instance_type': None,
            'ramdisk_id': None,
            'kernel_id': None
        },
        'test_username': None
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

provider_map = {
    'os': update_os,
    'aws': update_aws
}


if not any([all([os.environ.has_key(key) for key in env])
            for env in (env_map['os'].values(), env_map['aws'].values())]):
    sys.stderr.write("No access keys from the environment found. ")
    sys.stderr.write("Try sourcing your credentials file.\n")
    sys.exit(-1)

parser = argparse.ArgumentParser("Generate config file for awscompat.")
parser.add_argument('provider', choices=['aws', 'os'],
                    help='generate config for amazon or openstack.')
args = parser.parse_args()

update_env(env_map[args.provider])
provider_map[args.provider]()


print json.dumps(base)
