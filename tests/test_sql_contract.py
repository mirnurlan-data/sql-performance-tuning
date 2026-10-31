"""Fast structural checks; actual query execution is covered by Docker CI."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SqlContractTests(unittest.TestCase):
    def test_query_orders_by_stable_tie_breaker(self):
        query = (ROOT / "queries/customer_orders.sql").read_text(encoding="utf-8").lower()
        self.assertIn("order by ordered_at desc, order_id desc", query)
        self.assertIn("customer_id = 4242", query)
        self.assertIn("limit 20", query)

    def test_optimization_covers_lookup_and_sort(self):
        index_sql = (ROOT / "sql/03_optimization.sql").read_text(encoding="utf-8").lower()
        self.assertIn("(customer_id, ordered_at desc, order_id desc)", index_sql)
        self.assertIn("include (total_amount)", index_sql)

    def test_no_published_benchmark_fabrication(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("results/*.txt", gitignore)


if __name__ == "__main__":
    unittest.main()
