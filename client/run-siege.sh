#!/bin/sh
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# Concurrent worker count
WORKERS="${WORKERS:-144}"

# Test duration (units are H, M or S, for hours, minutes or seconds)
DURATION="${DURATION:-2M}"

# Log file (outputs CSV rows)
LOG="${LOG:-./siege.log}"

# Source file
SOURCE="${SOURCE:-urls.txt}"

# Warmup parameters
WARMUP_WORKERS="${WARMUP_WORKERS:-1}"
WARMUP_REPEAT="${WARMUP_REPEAT:-300}"
WARMUP_DURATION="${WARMUP_DURATION:-1M}"

echo "--------------------------------------------------------"
echo "----------------- First warmup run ---------------------"
echo "--------------------------------------------------------"
# run siege benchmark
# -c specifies the number of workers
# -b tells siege to enter benchmarking mode
# -t 120S specifies the run time of the benchmark, in this case 120 seconds
# -f urls.txt tells siege which urls to benchmark
# --log=./siege.log specifies the output file
siege -c ${WARMUP_WORKERS} -b -r ${WARMUP_REPEAT} -f ${SOURCE} --log=${LOG}

echo "\n--------------------------------------------------------"
echo "----------------- Second warmup run --------------------"
echo "--------------------------------------------------------"
siege -c ${WORKERS} -b -t ${WARMUP_DURATION} -f ${SOURCE} --log=${LOG}

echo "\n--------------------------------------------------------"
echo "----------------- Measurement run ----------------------"
echo "--------------------------------------------------------"
siege -c ${WORKERS} -b -t ${DURATION} -f ${SOURCE} --log=${LOG}
