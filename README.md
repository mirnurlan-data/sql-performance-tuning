# PostgreSQL Query Performance Lab

[![PostgreSQL Lab CI](https://github.com/mirnurlan-data/sql-performance-tuning/actions/workflows/ci.yml/badge.svg)](https://github.com/mirnurlan-data/sql-performance-tuning/actions/workflows/ci.yml)

A reproducible educational demonstration of PostgreSQL 16 query tuning over **25,000 synthetic customers** and **400,000 synthetic orders**.

## Architecture and measured evidence

[Architecture and engineering trade-offs](docs/architecture.md) · [Benchmark methodology](docs/methodology.md)

```text
Generate synthetic sales → run baseline query and EXPLAIN
                         → add targeted covering index
                         → re-run same query and EXPLAIN
                         → compare output rows and record actual timing
```

## Run it locally

Requirements: Docker Compose and Python 3.10+.

```bash
docker compose up -d --wait
bash scripts/benchmark.sh
python scripts/summarize_plans.py
python -m unittest discover -s tests -v
```

This creates `results/before.txt`, `results/after.txt`, `results/rows_before.txt`, `results/rows_after.txt`, and `results/summary.json`. GitHub Actions saves the measured evidence as an artifact for each run.

## SQL strategy

```sql
SELECT order_id, ordered_at, total_amount
FROM lab.orders
WHERE customer_id = 4242
  AND ordered_at >= TIMESTAMP '2025-06-01'
ORDER BY ordered_at DESC, order_id DESC
LIMIT 20;
```

Targeted index:

```sql
CREATE INDEX idx_orders_customer_recent
ON lab.orders (customer_id, ordered_at DESC, order_id DESC)
INCLUDE (total_amount);
```

The project validates that the before/after result rows are identical. **No specific speedup is promised:** query planner behavior and measured time depend on data and environment. The JSON summary is the actual result from the current run, not a fabricated success claim.

## Code map

- `sql/`: schema, synthetic seed, index migration
- `queries/`: analyzed customer-order lookup
- `scripts/benchmark.sh`: live query correctness and plan capture
- `scripts/summarize_plans.py`: extract plan timings and produce JSON
- `tests/`: parser validation tests
- `docs/`: architecture, methodology and production trade-offs

**Safety:** the benchmark resets the `lab` schema of its *disposable Docker demo database*. It should never be pointed at client or production data.
