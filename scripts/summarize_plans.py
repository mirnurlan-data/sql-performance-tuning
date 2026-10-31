"""Summarize real PostgreSQL EXPLAIN ANALYZE measurements.

Separate baseline/indexed trial groups remain order-confounded. These numbers
describe one CI machine and one synthetic workload, not production speedups.
"""
import json
import math
from pathlib import Path
import re
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"Execution Time:\s*([0-9.]+)\s*ms")


def timings(path: Path, expected_count: int) -> list[float]:
    samples = [float(x) for x in PATTERN.findall(path.read_text(encoding="utf-8"))]
    if len(samples) != expected_count or any(v <= 0 or not math.isfinite(v) for v in samples):
        raise ValueError(f"Expected {expected_count} positive finite timing samples in {path}; got {samples}")
    return samples


def timing(path: Path) -> float:
    return timings(path, 1)[0]


def stats(samples: list[float]) -> dict:
    ordered = sorted(samples)
    return {
        "trials_ms": samples,
        "median_ms": round(median(samples), 3),
        "min_ms": min(samples),
        "max_ms": max(samples),
        "p95_nearest_rank_ms": ordered[math.ceil(0.95 * len(ordered)) - 1],
    }


def summarize() -> dict:
    baseline = timings(ROOT / "results/trials_before.txt", 5)
    indexed = timings(ROOT / "results/trials_after.txt", 5)
    before = median(baseline)
    after = median(indexed)
    result = {
        "environment": "One GitHub Actions runner / local PostgreSQL 16 Docker demo",
        "workload": "Synthetic 25k customers, 400k orders, one customer-orders query",
        "baseline_plan_execution_ms": timing(ROOT / "results/before.txt"),
        "indexed_plan_execution_ms": timing(ROOT / "results/after.txt"),
        "baseline": stats(baseline),
        "indexed": stats(indexed),
        "median_change_percent": round((after - before) / before * 100, 2),
        "interpretation": "negative median_change_percent indicates lower measured execution time",
        "methodological_limit": "Five sequential trials per phase on one runner; no randomized order, no cold-cache equivalence or production guarantees.",
    }
    (ROOT / "results/summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
