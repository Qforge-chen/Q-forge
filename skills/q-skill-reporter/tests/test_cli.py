from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReporterCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package_root = Path(__file__).resolve().parent.parent
        self.fixtures = self.package_root / "fixtures"
        self.src_root = self.package_root / "src"

    def test_cli_smoke_render_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "cli-output.html"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.src_root) + os.pathsep + env.get("PYTHONPATH", "")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "q_skill_reporter",
                    "render-markdown",
                    "--input",
                    str(self.fixtures / "sample-report.md"),
                    "--output",
                    str(output_path),
                    "--title",
                    "CLI Smoke"
                ],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertIn("cli-output.html", result.stdout)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
