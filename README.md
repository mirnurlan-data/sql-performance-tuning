# PostgreSQL Query Performance Lab

A **reproducible SQL tuning exercise** using 25,000 synthetic customers and 400,000 synthetic orders. Diagnose a customer-order lookup with `EXPLAIN (ANALYZE, BUFFERS)`, add a targeted composite index, and compare real PostgreSQL execution plans.

**Important:** Results are not fabricated. The benchmark creates local `results/before.txt` and `results/after.txt` only when you run it; no unmeasured speedup is claimed.

## Quick start

Requirements: Docker Engine and Docker Compose.

```bash
docker compose up -d --wait
bash scripts/benchmark.sh
```

Open `results/before.txt` and `results/after.txt` to compare execution time, scan strategy, sort behavior, and buffers. Query results are saved as `results/rows_before.txt` and `results/rows_after.txt`; the runner compares both and fails if they differ.

## Workload

The query filters for one customer and a date range, then orders the latest events:

```sql
SELECT order_id, ordered_at, total_amount
FROM lab.orders
WHERE customer_id = 4242
  AND ordered_at >= TIMESTAMP '2025-06-01'
ORDER BY ordered_at DESC, order_id DESC
LIMIT 20;
```

It is intentionally measured before and after this index:

```sql
CREATE INDEX idx_orders_customer_recent
ON lab.orders (customer_id, ordered_at DESC, order_id DESC)
INCLUDE (total_amount);
```

The actual optimizer plan depends on workload, PostgreSQL version, cache state and statistics; an index-only scan or a particular speedup is **not** guaranteed.

## Files

- [sql/01_schema.sql](sql/01_schema.sql): relational schema and constraints
- [sql/02_seed.sql](sql/02_seed.sql): deterministic synthetic data
- [queries/customer_orders.sql](queries/customer_orders.sql): lookup query
- [sql/03_optimization.sql](sql/03_optimization.sql): composite index
- [scripts/benchmark.sh](scripts/benchmark.sh): repeatable before/after run with correctness check
- [docs/methodology.md](docs/methodology.md): validity, limitations and safe use
- [.github/workflows/ci.yml](.github/workflows/ci.yml): Docker-based integration run

## Safety and scope

**This script resets the `lab` schema in a dedicated Docker demo database.** Do not use this script against production or client databases. The local credentials are for demonstration only. All records are synthetic, and this portfolio project is not proof of a production deployment. Use `docker compose down -v` only if you deliberately want to erase the demo volume.
