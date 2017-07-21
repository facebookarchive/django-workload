# Cassandra configuration

## Requirements
This directory sets up a Cassandra NoSQL server.

## Setup
This setup relies on the host system having Cassandra installed, we merely
provide configuration as needed.

On Ubuntu 16.04 issue the following commands as root:

    # Installing dependencies and Java 8, accepting prompts
    apt-get install software-properties-common curl
    add-apt-repository ppa:webupd8team/java
    apt-get update
    apt-get install oracle-java8-installer

    # install Cassandra 3.0.14, from http://cassandra.apache.org/download/
    echo "deb http://www.apache.org/dist/cassandra/debian 30x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
    curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -
    apt-get update
    apt-get install cassandra

If you configure cassandra to listen to a public IP address, please do protect this
cluster with a firewall to prevent unauthorised access!

To change the default listen address for Cassandra (localhost), edit
`/etc/cassandra/cassandra.yaml` to replace the `listen_address` configuration
with `listen_address <desired_ip_address>`. If planning to deploy Cassandra
on the same machine as uWSGI, this parameter does not need changing.

There seems to be an issue with cassandra expecting the output of `hostname` to
resolve to either an ipv4 address or to localhost; if you see an error about
`Local host name unknown: java.net.UnknownHostException` in
`/var/log/cassandra/system.log`, add `hostname` to `/etc/hosts` for the
`127.0.0.1` entry.

We'll use the default configuration.
