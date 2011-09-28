from uuid import uuid4
import time



class TimeoutException(Exception): pass

def wait(condition, wait=0.1, timeout=30):
    """
    Loop until condition() is True or timeout.

    Params:
        condition: callable. Boolean return type
        wait: how long to wait in between calls to condition
        timout: if set, how long to wait, in seconds, before aborting.
    """

    assert callable(condition)
    start = time.time()
    while not condition():
        time.sleep(0.1)
        if time.time() >= start + timeout:
            raise TimeoutException()


"""
class Retry(object):
    def __init__(self, 

"""
def retry(f=None, max_tries=5):
    """ Retry function f

    can be used as a decorator or invoked directly.

    args:
        max_tries number of times to try before giving up
    """
    def wrapper(f):
        def inner(*args, **kwargs):
            for i in xrange(max_tries):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    if i + 1 == max_tries:
                        raise
                    continue
        return inner

    if f:
        assert callable(f)
        return wrapper(f)()
    return wrapper
