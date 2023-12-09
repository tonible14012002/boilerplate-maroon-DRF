
# \wait-for-it.sh "${MSSQL_HOST}:${MSSQL_PORT}" --timeout=90

echo "MSSQL Loaded, initializing Database"

/opt/mssql-tools/bin/sqlcmd -s "${MSSQL_HOST},${MSSQL_PORT}" -U sa -P "${SA_PASSWORD}" -d master -i /create-database.sql
