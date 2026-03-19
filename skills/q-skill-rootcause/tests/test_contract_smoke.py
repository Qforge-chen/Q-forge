from __future__ import annotations

import json
import unittest
from pathlib import Path


class RootcauseContractSmokeTests(unittest.TestCase):
    def test_public_fixture_remains_unverified(self) -> None:
        fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "sample-evidence-chain.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(data["verdict"], "UNVERIFIED")
        self.assertTrue(data["evidence_gaps"])


if __name__ == "__main__":
    unittest.main()
