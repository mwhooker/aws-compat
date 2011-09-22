from boto.ec2.connection import EC2Connection
from awscompat import util


EC2_CONN = EC2Connection()

def security_groups():

    group_name = util.make_key('group_name')
    group_desc = util.make_key('group_desc')

    group = EC2_CONN.create_security_group(
        group_name,
        group_desc
    )

    assert repr(group) in [repr(g) for g in
                           EC2_CONN.get_all_security_groups()]

    yield group

    group.delete()
    assert repr(group) not in [repr(g) for g in
                               EC2_CONN.get_all_security_groups()]
