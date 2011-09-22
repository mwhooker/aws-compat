import imp
import glob
import os.path
import inspect
import awscompat.tests.base as base


def collect(dir, include_modules=None):
    classes = set([])

    for path in glob.glob(os.path.join(dir, '*.py')):
        module_name = inspect.getmodulename(path)
        if include_modules and module_name not in include_modules:
            continue
        module_name = 'awscompat.tests.' + module_name
        module = imp.load_source(module_name, path)
        for k, v in inspect.getmembers(module):
            if inspect.isclass(v) \
               and issubclass(v, base.TestNode) \
               and v is not base.TestNode:
                classes.add(v)

    assert len(classes)
    return classes
