import imp
import glob
import os.path
import inspect
import awscompat.tests.base as base


def collect(dir):
    classes = set([])

    for path in glob.glob(os.path.join(dir, '*.py')):
        module_name = 'awscompat.tests.' + inspect.getmodulename(path)
        module = imp.load_source(module_name, path)
        for k, v in inspect.getmembers(module):
            if inspect.isclass(v) \
               and issubclass(v, base.TestNode) \
               and v is not base.TestNode:
                classes.add(v)

    assert len(classes)
    return classes
