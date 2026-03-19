from __future__ import annotations

import json
import unittest
from pathlib import Path


class SupplierContractSmokeTests(unittest.TestCase):
    def test_public_fixture_has_warning_supplier(self) -> None:
        fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "sample-analysis-summary.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertAlmostEqual(data["overall"]["pass_rate"], 91.7)
        self.assertIn("Gamma Components", data["warning_suppliers"])


if __name__ == "__main__":
    unittest.main()
