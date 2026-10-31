# Performance measurement methodology

This is a controlled **synthetic teaching exercise**, not a production benchmark.

1. PostgreSQL 16 Docker instance starts with 25,000 synthetic customers and 400,000 orders, seeded deterministically.
2. The runner explicitly resets only the `lab` schema of the **disposable** container database.
3. `ANALYZE` gathers table statistics; run the filter/sort query and save the full baseline EXPLAIN plan.
4. Execute the same baseline query **five additional times** (the first detailed plan is excluded from the median).
5. Add a composite index matching equality filter, descending date and sort; `ANALYZE` again; save the indexed plan.
6. Run the indexed query five additional times.
7. Compare the **actual result rows** and fail if results differ. Parse `Execution Time` from all plans; reject missing, zero or non-finite timings.
8. Report observed median, min, max, and nearest-rank p95 for **each group** in the CI artifact `results/summary.json`. A negative signed median change indicates a faster observed indexed run.

## Interpretation

These measurements are sequential, not randomized or paired on identical cold-cache states. The later group may benefit from buffer warming. Because sample count is only five, p95 here is simply the largest sample. The runner, filesystem cache, concurrent load, planner choice, stats and insert pattern can affect results. Do not generalize the numeric result to other datasets or claim production improvements. Actual execution plans and buffer measurements are included for inspection.

## Engineering follow-up

For a real production decision, benchmark multiple high-frequency query shapes on anonymized realistic datasets, restore data between trials, randomize comparison order, track write overhead and disk cost of indexes, report latency distributions, use representative concurrency, and plan migrations with rollback and query-plan monitoring.
