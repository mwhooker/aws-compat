#!/usr/bin/env python

import sys

from boto.ec2.connection import EC2Connection
import boto.exception


conn = EC2Connection()


def delete_security_groups():
    groups = conn.get_all_security_groups(filters={
        'group-name': 'awscompat_*'
    })

    for group in groups:
        group.delete()


def delete_keypairs():
    keypairs = conn.get_all_key_pairs(filters={
        'key-name': 'awscompat_*'
    })

    for keypair in keypairs:
        keypair.delete()


def terminate_instances():
    reservations = conn.get_all_instances(filters={
        'group-name': 'awscompat_*',
        'key-name': 'awscompat_*',
    })

    for reservation in reservations:
        for instance in reservation.instances:
            instance.terminate()


if __name__ == '__main__':
    try:
#        delete_security_groups()
#        delete_keypairs()
        terminate_instances()
    except Exception, e:
        sys.stderr.write(str(e))
        sys.exit(-1)
    sys.exit(0)
