from functools import wraps
from inspect import getdoc

from statsd.defaults import django as statsd_django_defaults
from statsd.client import StatsClient


_patches = []


def register_patch(f):
    _patches.append((f, getdoc(f) or ''))


# TODO: send a pull request upstream
@register_patch
def patch_django_statsd_ipv6():
    """Make django_statsd work with IPv6"""
    def insert_ipv6(**kwargs):
        if 'ipv6' not in kwargs:
            kwargs['ipv6'] = statsd_django_defaults.ipv6
        return StatsClient(**kwargs)

    # Only needs to be applied if STATSD_IPV6 is set to True and the connection
    # fails when trying to import the client.
    try:
        from django_statsd.clients import normal
    except OSError as e:
        if e.errno == -2:  # Name or service not known
            # patch the client to make sure we can support IPv6
            # Use sys.modules to avoid triggering the exception again
            import sys
            normal = sys.modules['django_statsd.clients.normal']
            normal.StatsClient = insert_ipv6
        else:
            raise


@register_patch
def patch_cassandra_execute():
    """Record timings for Cassandra operations"""
    from django_statsd.clients import statsd
    from django_cassandra_engine.connection import CassandraConnection

    def decorator(orig):
        @wraps(orig)
        def timed_execute(self, *args, **kwargs):
            with statsd.timer('cassandra.execute'):
                return orig(self, *args, **kwargs)

    CassandraConnection.execute = decorator(CassandraConnection.execute)


def apply():
    for patch, descr in _patches:
        print(descr)
        patch()
