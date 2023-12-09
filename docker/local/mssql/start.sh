set -o errexit

set -o pipefail

set -o nounset

echo "Initializing MS SQL server"

# Start server and initialization at the same time
/run-initialization.sh & /opt/mssql/bin/sqlservr
