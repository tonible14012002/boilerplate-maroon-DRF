#!/usr/bin/env bash

set -o errexit

set -o pipefail

set -o nounset

# Wait cassandra server
until printf "" 2>>/dev/null >>/dev/tcp/${CASSANDRA_HOST}/9042; do 
    sleep 5;
    echo "Waiting for cassandra...";
done

echo Cassandra is ready, initializing schema...

cqlsh cassandra -f /schema.cql

echo "Initialized cassandra, turning off..."

exec "$@"