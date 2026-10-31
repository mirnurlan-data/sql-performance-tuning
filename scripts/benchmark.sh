#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results

# Connect only to the Docker Compose demo service, never to an arbitrary DSN.
db() { docker compose exec -T postgres psql -X -v ON_ERROR_STOP=1 -U portfolio -d portfolio "$@"; }

echo "Resetting the disposable lab schema in the local Docker demo database."
echo 'DROP SCHEMA IF EXISTS lab CASCADE;' | db > /dev/null
db < sql/01_schema.sql > /dev/null
db < sql/02_seed.sql > /dev/null

query="$(cat queries/customer_orders.sql)"
printf 'EXPLAIN (ANALYZE, BUFFERS) %s\n' "$query" | db > results/before.txt
db -A -t < queries/customer_orders.sql > results/rows_before.txt

db < sql/03_optimization.sql > /dev/null
printf 'EXPLAIN (ANALYZE, BUFFERS) %s\n' "$query" | db > results/after.txt
db -A -t < queries/customer_orders.sql > results/rows_after.txt

diff -u results/rows_before.txt results/rows_after.txt
echo "SUCCESS: Query outputs are identical. Inspect results/before.txt and results/after.txt."
echo "Only real PostgreSQL measurements should be quoted as performance results."
