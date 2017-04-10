# The Django server and uWSGI

This provides the views to be tested for the workload. This server
runs under uWSGI and connects to the other services
set up in a cluster. See the various subdirectories of the `services/` top-level
directory in this project.

## Requirements

The uWSGI server binds to *all network interfaces* so this should only be run in
a firewalled environment.

## setup

On Ubuntu 16.04, you can run:

    apt-get install \
      build-essential \
      git \
      libmemcached-dev \
      python3-virtualenv \
      python3-dev \
      zlib1g-dev
    python3 -m virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

Next, copy the `cluster_settings_template.py` template to `cluster_settings.py`
and edit this to point to the various services running in the cluster:

    cp cluster_settings_template.py cluster_settings.py
    $EDITOR cluster_settings.py

## running

Start the service with

    uwsgi uwsgi.ini

and you can connect to port 8000 to access the server.
