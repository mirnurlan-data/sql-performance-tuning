"""Extract actual PostgreSQL EXPLAIN ANALYZE timings; fail on missing evidence."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"Execution Time:\s*([0-9.]+)\s*ms")


def timing(path: Path) -> float:
    matches = PATTERN.findall(path.read_text(encoding="utf-8"))
    if len(matches) != 1:
        raise ValueError(f"Expected one Execution Time measurement in {path}, got {len(matches)}")
    return float(matches[0])


def summarize() -> dict:
    before = timing(ROOT / "results" / "before.txt")
    after = timing(ROOT / "results" / "after.txt")
    if before <= 0:
        raise ValueError("Invalid baseline time")
    result = {
        "environment": "GitHub Actions runner or local Docker; single consecutive trial",
        "query": "customer_orders",
        "before_ms": before,
        "after_ms": after,
        "delta_ms": round(after - before, 3),
        "change_percent": round((after - before) / before * 100, 2),
        "interpretation": "negative change_percent means a faster indexed execution",
        "limitations": "not a statistically controlled or production-representative benchmark"
    }
    (ROOT / "results" / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
