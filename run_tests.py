#!/usr/bin/env python
import argparse
import os.path
import json

import awscompat
from awscompat import collector
from awscompat import runner

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(config_path) as f:
    awscompat.config = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument('-m', nargs='+', help='Only run these test modules.')
args = parser.parse_args()

test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')

classes = collector.collect(test_dir, include_modules=args.m)
runner = runner.Runner(classes)
runner.run()
runner.print_messages()
