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

    apt-get install python3-virtualenv python3-dev build-essential
    python3 -m virtualenv -p python3 venv
    source venv/bin/activate
    pip install .

## running

Start the service with

    uwsgi uwsgi.ini

and you can connect to port 8000 to access the server.
