import imp
import os.path
import inspect
import awscompat.tests.base as base
from glob import glob


def list_modules(dirname):
    modules = []
    for path in glob(os.path.join(dirname, '*.py')):
        module = inspect.getmodulename(path)
        if module not in ('__init__', 'base'):
            modules.append(module)
    return modules


def collect(dirname, include_modules=None):
    classes = set([])

    for path in glob(os.path.join(dirname, '*.py')):
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

    assert len(classes), "No test cases found."
    return classes
