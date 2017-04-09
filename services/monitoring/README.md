# Monitoring configuration

## Requirements
This directory sets up a graphite server to track performance metrics.

Make sure you are running this in a firewalled environment.

We'll use docker to manage the installation, so follow the docker
installation instructions:

    https://docs.docker.com/engine/installation/linux/ubuntu/

Follow the instructions for the CE setup (Community Edition).

Next, install the hopsoft/graphite-statsd docker container, follow instructions
at:

    https://github.com/hopsoft/docker-graphite-statsd

Timeseries data can then be directed to UDP port 8125.
