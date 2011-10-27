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
    'ec2': {
        'url': None,
        "test_image_id": "ami-8e1fece7",
        'test_instance': {
            'instance_type': None,
            'ramdisk_id': None,
            'kernel_id': None
        },
        'test_username': 'ec2-user'
    },
    's3': {
        'url': None
    }
}

novarc_keys = [
    "EC2_ACCESS_KEY",
    "EC2_SECRET_KEY",
    "EC2_URL",
    "S3_URL",
    "EC2_USER_ID",
    "EC2_PRIVATE_KEY",
    "EC2_CERT",
    "NOVA_CERT",
    "EUCALYPTUS_CERT",
    "NOVA_API_KEY",
    "NOVA_USERNAME",
    "NOVA_PROJECT_ID",
    "NOVA_URL",
    "NOVA_VERSION",
]


parser = argparse.ArgumentParser()
parser.add_argument('--env', action='store_true',
                    help='Generate config from environment.')
args = parser.parse_args()


if args.env:
    base.update(load_env())

print json.dumps(base)
