from __future__ import annotations

import json
import unittest
from pathlib import Path


class EightDContractSmokeTests(unittest.TestCase):
    def test_public_fixture_matches_expected_keys(self) -> None:
        fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "sample-review-result.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(data["alignment_status"], "ALIGNMENT_NEEDED")
        self.assertIn("blocked_sections", data)
        self.assertTrue(data["blocked_sections"])


if __name__ == "__main__":
    unittest.main()
