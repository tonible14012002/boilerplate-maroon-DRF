#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

if [ -z "${POSTGRES_USER}" ]; then
  base_postgres_image_default_user='postgres'
  export POSTGRES_USER="${base_postgres_image_default_user}"
fi

export DATABASE_URL=${DATABASE_URL}
echo "${POSTGRES_HOST} ${POSTGRES_PORT} ${POSTGRES_DB} ${POSTGRES_USER} ${POSTGRES_PASSWORD} ${POSTGRES_DB}"

/wait-for-it.sh "${POSTGRES_HOST}:${POSTGRES_PORT}" --timeout=100

>&2 echo "PostgreSQL is available"

/wait-for-it.sh "${CASSANDRA_HOST}:${CASSANDRA_PORT}" --timeout=100

>&2 echo "Cassandra is available"


exec "$@"