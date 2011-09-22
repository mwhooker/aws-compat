#!/usr/bin/env python
"""
import os.path

from awscompat import collector
from awscompat import runner


test_dir = os.path.join(os.path.dirname(__file__), 'awscompat', 'tests')

classes = collector.collect(test_dir)
runner = runner.Runner(classes)
runner.run()
runner.print_messages()
"""

"""
threw = False
x.next()
print "middle"
try:
    x.next()
except StopIteration:
    threw = True
    pass
assert threw
"""

from awscompat.tests.s3 import test_bucket, test_object, test_acl


def run(tests, val=None):
    if not len(tests):
        return

    f = tests.pop(0)
    try:
        test_gen = f(val)
    except Exception, e:
        # let parents do cleanup
        return

    threw = False

    run(tests, test_gen.next())

    try:
        test_gen.next()
    except StopIteration:
        threw = True
        pass
    except Exception, e:
        return

    assert threw

run([test_bucket, test_object, test_acl])
