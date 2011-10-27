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
        'test_image_id': '',
        'test_instance': {
            'instance_type': "",
            'ramdisk_id': '',
            'kernel_id': ''
        },
        'test_username': ''
    }
}

def parse_novarc(fd):
    data = {}
    for line in ifilter(lambda x: x[:6] == 'export', fd):
        lhs, rhs = line.split('=')
        key = lhs[7:]
        value = rhs.strip('"\n')
        data[key] = value
    print data

    return {}

parser = argparse.ArgumentParser()
parser.add_argument('novarc', metavar='NOVARC',
                    help='novarc file to populate config file with.')
args = parser.parse_args()

novarc_path = os.path.join(os.getcwd(), args.novarc)
try:
    with open(novarc_path) as f:
        base.update(parse_novarc(f))
except IOError:
    print "Please make sure a config file exists at %s" % novarc_path
    sys.exit(-1)


print json.dumps(base)
