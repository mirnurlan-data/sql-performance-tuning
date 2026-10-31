# Benchmark methodology and limitations

1. A PostgreSQL 16 Docker Compose service stores 25,000 customers and 400,000 orders in a **dedicated** `portfolio` demo database.
2. The script drops only the `lab` schema. It is destructive **inside that local demo database**.
3. `ANALYZE` computes statistics before the baseline measurement.
4. Run the same order lookup using `EXPLAIN (ANALYZE, BUFFERS)` without an index and save the real plan.
5. Create the composite index that matches the customer filter and descending sort; rerun the query and save the new plan.
6. Compare the actual query result rows. Different results cause the runner to fail.
7. Review execution times, shared buffer hits/reads, sorts and scan type from the two recorded plans.

**Limitations:** This is one sequential before/after run, not a statistically controlled performance study. Cache warming, background load, hardware, planner choices, data distribution, and index construction can affect numbers. Do not generalize one run's speedup to production. For stronger evidence, run multiple independent trials on restored snapshots, report distributions, and vary customer IDs / row counts. Never point the runner at a shared database. The scripts use only synthetic records.
