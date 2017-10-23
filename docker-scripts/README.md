# Docker containers setup files

This directory contains all docker files and all necessary dependencies to
build and deploy all the docker images necessary to run the Django
Workload. Each entity (Cassandra, uWSGI, Memcached, Siege, Graphite) is set up
in a separate container.

For instructions on how to install docker, please refer to:

    https://docs.docker.com/engine/installation/linux/ubuntu/

## Build the docker images

To build all the necessary images for the workload, run

    [UWSGI_ONLY=1] ./build_containers.sh [/absolute/path/to/installed/python]

Running the above script with no parameters will deploy the system Python 3.5.2
on the uWSGI container. In order to deploy a custom Python build, please
provide the script above with the absolute path to the install folder of your
build

    # CPython tree
    ./configure --prefix=/some/folder
    make
    make install
    # Docker scripts
    ./build_containers.sh /some/folder

If the UWSGI_ONLY environment variable is not set to 1, the above script will
build all the containers. Since all other containers except uWSGI do not change
between runs, UWSGI_ONLY=1 can be specified before the build_containers.sh
script to only rebuild the Docker image for uWSGI:

    # remember to remove the old container & image
    ./cleanup_containers.sh
    docker image rm uwsgi-webtier
    UWSGI_ONLY=1 ./build_containers.sh /some/folder

By default, docker commands will require root access. If using "sudo", remember
to specify the "UWSGI_ONLY=1" variable __after__ the "sudo" word, otherwise it
will not be taken into consideration.

To run docker without "sudo", please follow the instructions here:

    https://docs.docker.com/engine/installation/linux/linux-postinstall/

# Run the workload

Simply run:

    # default number of Siege workers is 185. This can be
    # changed using the WORKERS environment variable
    [WORKERS=185] ./run_containers.sh

# Cleanup containers

In order to do another run, the previous containers need to be removed:

    ./cleanup_containers.sh
