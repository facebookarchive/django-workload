# Django workload by Instagram and Intel

This project aims to provide a Django workload based on a real-world
large-scale production workload that serves mobile clients.

## Setup

The project can be set up on a single machine, or on a cluster of machines
to spread the load and to make it easier to gauge the impact of the Django
workload on both Python and the hardware it runs on.

Documentation to set up each component of the cluster is provided for in
each subdirectory. You'll need to follow the [README.md](/README.md) file in each of the
following locations:

* 3 services
  * Cassandra - services/cassandra
  * Memcached - services/memcached
  * Monitoring - services/monitoring

* Django and uWSGI - django-workload
* A load generator - client

Once set up, access http://[uwsgi_host:uwsgi_port]/ to see an overview of
the offered endpoints, or use the load generator to produce a high request
load on the server.

## Benchmarking configuration

The default benchmarking parameters used for Siege, Memcached and uWSGI are
suitable for driving high CPU utilization (>80%) in server environments:
```
uWSGI concurrent workers – 88
Memcached threads – 16
Siege Concurrency – 185
```

## Contributing

See the [CONTRIBUTING](/CONTRIBUTING.md) file for how to help out.

## License

Django Workload is [BSD-licensed](/LICENSE). We also provide an additional patent grant.
