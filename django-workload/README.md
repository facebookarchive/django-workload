# The Django server itself

This provides the views to be tested for the workload. This server
runs under uWSGI (see `services/uwsgi`), and connects to the other services
set up in a cluster. See the various subdirectories of the `services/` top-level
directory in this project.

## setup

On Ubuntu 16.04, you can run:

    apt-get install python3-virtualenv
    python3 -m virtualenv -p python3 venv
    source venv/bin/activate
    pip install .
