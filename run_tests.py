#!/usr/bin/env python
import argparse
import boto
import functools
import json
import os.path
import sys
from urlparse import urlparse

from boto.ec2.regioninfo import RegionInfo

sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party'))

import awscompat
import awscompat.connections
from awscompat import collector
from awscompat import runner

def split_clc_url(clc_url):
    """
    Splits a cloud controller endpoint url.
    """
    parts = urlparse(clc_url)
    is_secure = parts.scheme == 'https'
    ip, port = parts.netloc.split(':')
    return {
        'ip': ip,
        'port': int(port),
        'is_secure': is_secure,
        'path': parts.path
    }


parser = argparse.ArgumentParser()
parser.add_argument('-m', metavar='MODULE', nargs='+',
                    help='Only run these test modules.')
parser.add_argument('-c', default='config.json', metavar='CONFIG_FILE',
                    help='Use alternate config file. Relative path. '
                   'Defaults to config.json')
args = parser.parse_args()


config_path = os.path.join(os.path.dirname(__file__), args.c)
try:
    with open(config_path) as f:
        awscompat.config = json.load(f)
except IOError:
    print "Please make sure a config file exists at %s" % config_path
    sys.exit(-1)


def build_connection(config, connect):
    kwargs = {}

    if config['url']:
        parts = split_clc_url(config['url'])

        kwargs = {
            'port': parts['port'],
            'is_secure': parts['is_secure'],
        }

        if len(parts['path']):
            kwargs['path'] = parts['path']

        if config.get('region_name'):
            kwargs['region'] = RegionInfo(None,
                                          config['region_name'],
                                          parts['ip'])

    return connect(**kwargs)

connect_ec2 = functools.partial(
    boto.connect_ec2,
    aws_access_key_id=awscompat.config['access_key'],
    aws_secret_access_key=awscompat.config['secret']
)

connect_s3 = functools.partial(
    boto.connect_s3,
    aws_access_key_id=awscompat.config['access_key'],
    aws_secret_access_key=awscompat.config['secret']
)

awscompat.connections.ec2_conn = build_connection(awscompat.config['ec2'], connect_ec2)
awscompat.connections.s3_conn = build_connection(awscompat.config['s3'], connect_s3)

test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')

classes = collector.collect(test_dir, include_modules=args.m)
runner = runner.Runner(classes)
runner.run()
runner.flush_messages()
