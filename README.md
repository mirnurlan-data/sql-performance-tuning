# PostgreSQL Query Performance Lab

[![PostgreSQL Lab CI](https://github.com/mirnurlan-data/sql-performance-tuning/actions/workflows/ci.yml/badge.svg)](https://github.com/mirnurlan-data/sql-performance-tuning/actions/workflows/ci.yml)

A reproducible PostgreSQL 16 query tuning lab over **25,000 synthetic customers** and **400,000 synthetic orders**.

## Engineering evidence

The CI workflow runs a disposable PostgreSQL database, executes the same query with and without a composite index, compares **identical output rows**, and captures real `EXPLAIN (ANALYZE, BUFFERS)` evidence. It additionally collects **five timed trials per configuration** and produces a JSON summary with median, min, max and nearest-rank p95.

[Latest CI workflow and artifacts](https://github.com/mirnurlan-data/sql-performance-tuning/actions/workflows/ci.yml) · [Methodology and limitations](docs/methodology.md) · [Architecture](docs/architecture.md)

## Run

Requires Docker Compose and Python 3.10+:

```bash
docker compose up -d --wait
bash scripts/benchmark.sh
python scripts/summarize_plans.py
python -m unittest discover -s tests -v
```

After the run, inspect `results/before.txt`, `results/after.txt`, `results/trials_before.txt`, `results/trials_after.txt` and `results/summary.json`. All are generated from actual executions and uploaded by CI, not hard-coded.

## Query and targeted index

```sql
SELECT order_id, ordered_at, total_amount
FROM lab.orders
WHERE customer_id = 4242 AND ordered_at >= TIMESTAMP '2025-06-01'
ORDER BY ordered_at DESC, order_id DESC
LIMIT 20;

CREATE INDEX idx_orders_customer_recent
ON lab.orders (customer_id, ordered_at DESC, order_id DESC)
INCLUDE (total_amount);
```

The composite B-tree index may support the equality filter, date range, and sort, but a specific execution plan or speedup is **not** promised.

## Query-plan evidence

The machine-readable CI summary also reports whether the captured baseline and indexed plans actually reference `idx_orders_customer_recent`. This is observed planner behavior, **not** a guaranteed index scan or speedup. Review the full EXPLAIN artifacts when interpreting results.

## Design boundaries

This is a single synthetic lookup measured in consecutive phases, **not** a production-concurrency benchmark. The new index consumes disk and adds write cost. See [methodology](docs/methodology.md) for confounders and better experimental design.

**Safety:** the runner drops and recreates the `lab` schema in the disposable Docker demo database. Never use it against production or client data.
