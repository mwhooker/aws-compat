#!/usr/bin/env python
import argparse
import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party'))

import awscompat
from awscompat import collector
from awscompat import runner


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

test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')


classes = collector.collect(test_dir, include_modules=args.m)
runner = runner.Runner(classes)
runner.run()
runner.print_messages()
