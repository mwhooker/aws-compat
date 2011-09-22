from uuid import uuid4


def make_key(prefix=None):
    return "%s%s" % (
        "%s_" % prefix if prefix else '',
        uuid4().hex
    )
