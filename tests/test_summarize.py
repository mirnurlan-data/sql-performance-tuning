import importlib.util
from pathlib import Path
import tempfile
import unittest

file = Path(__file__).resolve().parents[1] / "scripts" / "summarize_plans.py"
spec = importlib.util.spec_from_file_location("summarize_plans", file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PlanParserTests(unittest.TestCase):
    def test_extracts_one_execution_time(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.txt"
            p.write_text("Planning Time: 0.123 ms\nExecution Time: 15.670 ms\n")
            self.assertEqual(module.timing(p), 15.67)

    def test_extracts_five_samples(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "trials.txt"
            p.write_text("".join(f"Execution Time: {n}.0 ms\n" for n in range(1, 6)))
            self.assertEqual(module.timings(p, 5), [1., 2., 3., 4., 5.])
            self.assertEqual(module.stats([5., 1., 3., 2., 4.])["median_ms"], 3.)

    def test_rejects_missing_or_nonpositive_samples(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.txt"
            p.write_text("Seq Scan\n")
            with self.assertRaises(ValueError):
                module.timings(p, 5)
            p.write_text("Execution Time: 0 ms\n")
            with self.assertRaises(ValueError):
                module.timing(p)


if __name__ == "__main__":
    unittest.main()
