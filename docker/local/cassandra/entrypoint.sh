#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

# Wait cassandra server
/wait-for-it.sh "${CASSANDRA_HOST}:${CASSANDRA_PORT}" --timeout=100

echo Cassandra is ready, initializing schema...

exec "$@"