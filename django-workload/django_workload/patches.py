from statsd.defaults import django as statsd_django_defaults
from statsd.client import StatsClient


# Patch up the django_statsd client handling (pass in ipv6 flag)
# TODO: send a pull request upstream
def patch_django_statsd_ipv6():
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


def apply():
    patch_django_statsd_ipv6()
