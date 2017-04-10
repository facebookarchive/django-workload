# Template file to configure the cluster.
# Copy this file to cluster_settings.py before starting the WSGI server
# and adjust as needed.
from django_workload.settings import *

# Security settings
SECRET_KEY = '()2uyyko+p=dv*nmu$b5my9px!e0=6r5unm19or$02$-c62%gb'
DEBUG = False

# Monitoring server
STATSD_HOST = 'localhost'
STATSD_PORT = 8125

# Memcached connection
CACHES['default']['LOCATION'] = '127.0.0.1:11811'
