from uuid import uuid4
import time


def make_uuid(prefix=None):
    return "awscompat_%s%s" % (
        "%s_" % prefix if prefix else '',
        uuid4().hex
    )


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
