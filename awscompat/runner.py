import gevent
import logging
from topsort import topsort_levels

log = logging.getLogger('awscompat')
ch = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(ch)


class TestGraphError(Exception):
    pass


"""
TODO:
    if two nodes depend on the same parent,
    setup/tear down for each branch to provide a 
    clean slate for the children.
    OR
    start from the root for each path
        Z
        |
        A
       / \
      B   C
    Z -> A -> B
    Z -> A -> C
"""
class Runner(object):

    def __init__(self, classes):
        self.failures = []
        self.errors = []
        dependency_pairs = []

        for klass in classes:
            if not len(klass.depends):
                dependency_pairs.append((None, klass))
                continue
            for key in klass.depends:
                dependency_pairs.append((klass.depends[key], klass))

        self.run_levels = filter(all, topsort_levels(dependency_pairs))


    def run(self):

        # stores a class:object mapping
        state = {}

        def run_pre(klass):
            """Initialize the test node and run its pre method.
            
            Report any errors."""
            obj = klass()

            # Find already initialized parent objects.
            parents = {}
            if hasattr(klass, 'depends'):
                for key in klass.depends:
                    parents[key] = state[klass.depends[key]]

            try:
                obj.pre(**parents)
            except AssertionError as e:
                log.exception(e)
                self.pre_failure(obj)
            except Exception as e:
                log.exception(e)
                self.pre_error(obj)
            else:
                return obj

        def run_post(obj):
            """Run the test node's post method.
            
            Report any errors."""

            try:
                obj.post()
            except AssertionError as e:
                log.exception(e)
                self.post_failure(obj)
            except Exception as e:
                log.exception(e)
                self.post_error(obj)

        def check_pass(klass):
            """True if `klass` has a greenlet in `state`."""

            return bool(state[klass])

        def all_passed(iterable):
            """True if all members of `iterable` have a greenlet in `state`."""

            return all([check_pass(klass) for klass in iterable])

        for level in self.run_levels:
            jobs = {}
            # spawn objects in current run level
            for klass in level:
                # only classes whose parents succeeded may be run
                if all_passed(klass.depends.values()):
                    log.debug("Running %s" % klass.__name__)
                    jobs[klass] = gevent.spawn(run_pre, klass)
            gevent.joinall(jobs.values())

            # collect finished jobs in state.
            for klass in level:
                if klass in jobs:
                    state[klass] = jobs[klass].value
                else:
                    # These classes failed for some reason.
                    state[klass] = None

            # state[klass] should never raise a KeyError
            assert all([klass in state for klass in level])

        for level in reversed(self.run_levels):
            # spawn cleanup jobs for classes which ran pre successfully.
            for klass in level:
                log.debug("Shutting down %s" % klass.__name__)
            eligible = [klass for klass in level if check_pass(klass)]
            jobs = [gevent.spawn(run_post, state[klass]) for klass in eligible]
            gevent.joinall(jobs)


    def pre_failure(self, obj):
        self.failures.append((obj, 'pre'))

    def pre_error(self, obj):
        self.errors.append((obj, 'pre'))

    def post_failure(self, obj):
        self.failures.append((obj, 'post'))

    def post_error(self, obj):
        self.errors.append((obj, 'post'))

    def flush_messages(self):
        """log errors & failures. flush messages."""

        if not len(self.failures) and not len(self.errors):
            log.info('OK')

        if len(self.errors):
            for err in self.errors:
                print err
            log.error("errors: %d" % len(self.errors))
            self.errors = []

        if len(self.failures):
            log.info("failures: %d" % len(self.failures))
            self.failures = []
