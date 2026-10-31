# Reviewer checklist

## Reproducibility
- PostgreSQL 16 runs in a disposable Docker Compose container
- Synthetic records and SQL queries are stored in the repository
- GitHub Actions captures raw plans, query row outputs and summary statistics
- Query results are compared before and after indexing

## Benchmark validity
- Five sequential samples per phase; no invented statistics
- Detailed `EXPLAIN (ANALYZE, BUFFERS)` output retained in CI artifacts
- Median and nearest-rank p95 are reported, with clear small-sample caveats
- Cache warming, fixed phase order and runner noise may bias observed changes
- No generalization to production throughput or p99 latency

## Operational concerns
- Index write amplification and storage overhead are not measured
- No concurrent load, crash recovery or isolation benchmark is included
- Do not run the schema-reset script against shared or client systems
- Production decisions need representative datasets and rollout/rollback planning
