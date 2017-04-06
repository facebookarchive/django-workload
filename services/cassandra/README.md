# Cassandra configuration

## Requirements
This directory sets up a Cassandra NoSQL server.

The server binds to *all network interfaces* so this should only be run in a
firewalled environment.

## Setup
This setup relies on the host system having Cassandra installed, we merely
provide configuration as needed.

On Ubuntu 16.4 issue the following commands as root:

    # Installing dependencies and Java 8, accepting prompts
    apt-get install software-properties-common curl
    add-apt-repository ppa:webupd8team/java
    apt-get update
    apt-get install oracle-java8-installer

    # install Cassandra, from http://cassandra.apache.org/download/
    echo "deb http://www.apache.org/dist/cassandra/debian 310x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
    curl https://www.apache.org/dist/cassandra/KEYS | apt-key add -
    apt-get update
    apt-get install cassandra

Configure cassandra to listen to a public IP address. Please do protect this
cluster with a firewall to prevent unauthorised access!

Edit `/etc/cassandra/cassandra.yml` to replace the `listen_address` configuration
with `listen_address eth0`, then restart with `systemctl restart cassandra`.

There seems to be an issue with cassandra expecting the output of `hostname` to
resolve to either an ipv4 address or to localhost; if you see an error about
`Local host name unknown: java.net.UnknownHostException` in
`/var/log/cassandra/system.log`, add `hostname` to `/etc/hosts` for the
`127.0.0.1` entry.

We'll use the default configuration.
