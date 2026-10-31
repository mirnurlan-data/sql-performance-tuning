import importlib.util
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "summarize_plans.py"
spec = importlib.util.spec_from_file_location("summarize_plans", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PlanParserTests(unittest.TestCase):
    def test_extracts_actual_execution_time(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.txt"
            p.write_text("Planning Time: 0.123 ms\nExecution Time: 15.670 ms\n")
            self.assertEqual(module.timing(p), 15.67)

    def test_fails_without_measurement(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.txt"
            p.write_text("Seq Scan\n")
            with self.assertRaises(ValueError):
                module.timing(p)


if __name__ == "__main__":
    unittest.main()
