import tempfile
import unittest
from pathlib import Path

from scripts.validate_reports import REQUIRED_MARKERS, validate_report
from scripts.generate_amplifon_interim_reports import REPORTS


class ValidateReportsTest(unittest.TestCase):
    def test_generated_report_definitions_are_unique_and_have_sources(self):
        slugs = [report["slug"] for report in REPORTS]
        self.assertEqual(len(slugs), len(set(slugs)))
        for report in REPORTS:
            self.assertTrue((Path("sources/amplifon") / report["source"]).exists())

    def test_accepts_complete_report_with_resolving_source_link(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            source.write_text("source", encoding="utf-8")
            report = root / "report.html"
            markers = "\n".join(REQUIRED_MARKERS)
            report.write_text(f'{markers}<a href="source.md">source</a>../sources/', encoding="utf-8")

            self.assertEqual(validate_report(report), [])

    def test_rejects_missing_markers_and_broken_links(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "report.html"
            report.write_text('<a href="missing.md">source</a>', encoding="utf-8")

            errors = validate_report(report)

            self.assertIn("missing required marker: One-line verdict:", errors)
            self.assertIn("broken local link: missing.md", errors)
