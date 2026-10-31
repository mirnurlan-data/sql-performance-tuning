#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results

# Connect ONLY to the explicitly named local Docker Compose demo service.
db() { docker compose exec -T postgres psql -X -v ON_ERROR_STOP=1 -U portfolio -d portfolio "$@"; }
explain() { printf 'EXPLAIN (ANALYZE, BUFFERS) %s\n' "$query" | db; }

echo "Resetting the DISPOSABLE lab schema in the local Docker demo database."
echo 'DROP SCHEMA IF EXISTS lab CASCADE;' | db > /dev/null
db < sql/01_schema.sql > /dev/null
db < sql/02_seed.sql > /dev/null
query="$(cat queries/customer_orders.sql)"

# Capture one detailed plan and repeat each configuration to reduce reliance
# on one noisy CI measurement. These are NOT independent cold-cache trials.
explain > results/before.txt
db -A -t < queries/customer_orders.sql > results/rows_before.txt
: > results/trials_before.txt
for n in 1 2 3 4 5; do
  echo "--- BASELINE TRIAL $n ---" >> results/trials_before.txt
  explain >> results/trials_before.txt
done

db < sql/03_optimization.sql > /dev/null
explain > results/after.txt
db -A -t < queries/customer_orders.sql > results/rows_after.txt
: > results/trials_after.txt
for n in 1 2 3 4 5; do
  echo "--- INDEXED TRIAL $n ---" >> results/trials_after.txt
  explain >> results/trials_after.txt
done

diff -u results/rows_before.txt results/rows_after.txt
echo "PASS: identical rows; five measured trials per configuration."
echo "Inspection: results/before.txt, results/after.txt and results/trials_*.txt."
