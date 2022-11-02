set -a
. ./.env
set +a

psql -h "${POSTGRES_SERVER}" -p "${POSTGRES_PORT}"  -U postgres -f scripts/setup_pod_users.sql;
