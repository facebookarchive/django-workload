#!/bin/sh
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# run siege benchmark
# -c specifies the number of workers
# -b tells siege to enter benchmarking mode
# -t 120S specifies the run time of the benchmark, in this case 120 seconds
# -f urls.txt tells siege which urls to benchmark
# --log=./siege.log specifies the output file
siege -c 144 -b -t 120S -f urls.txt --log=./siege.log
