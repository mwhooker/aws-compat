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


def retry(f=None, max_tries=5, wait_exp=None):
    """
    Retry function f

    can be used as a decorator or invoked directly.

    args:
        max_tries   number of times to try before giving up
        wait_exp    wait n^wait_exp seconds between retries
                    where n is the iteration
                    no wait if None
    """
    def wrapper(f):
        def inner(*args, **kwargs):
            for i in xrange(max_tries):
                if wait_exp:
                    time.sleep(i ** wait_exp)
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
