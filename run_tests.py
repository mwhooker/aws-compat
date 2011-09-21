#!/usr/bin/env python
import os.path

from awscompat import collector
from awscompat import runner


test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')

classes = collector.collect(test_dir)
runner = runner.Runner(classes)
runner.run()
runner.print_messages()
