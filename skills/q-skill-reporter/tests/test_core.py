from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from q_skill_reporter.core import render_findings, render_findings_file, render_markdown, render_markdown_file


class ReporterCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package_root = Path(__file__).resolve().parent.parent
        self.fixtures = self.package_root / "fixtures"

    def test_render_markdown_contains_heading(self) -> None:
        markdown_text = (self.fixtures / "sample-report.md").read_text(encoding="utf-8")
        html = render_markdown(markdown_text, title="Core Test")
        self.assertIn("Core Test", html)
        self.assertIn("Supplier Review Summary", html)

    def test_render_findings_contains_critical_badge(self) -> None:
        report = json.loads((self.fixtures / "sample-findings.json").read_text(encoding="utf-8"))
        html = render_findings(report)
        self.assertIn("critical", html)
        self.assertIn("Gamma Components", html)

    def test_render_files_write_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            markdown_output = temp_root / "markdown.html"
            findings_output = temp_root / "findings.html"
            render_markdown_file(self.fixtures / "sample-report.md", markdown_output, title="Markdown Output")
            render_findings_file(self.fixtures / "sample-findings.json", findings_output, title="Findings Output")
            self.assertTrue(markdown_output.exists())
            self.assertTrue(findings_output.exists())


if __name__ == "__main__":
    unittest.main()
