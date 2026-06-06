import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_amplifon_reports.py"
SPEC = importlib.util.spec_from_file_location("sync_amplifon_reports", SCRIPT)
syncer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(syncer)


class SyncAmplifonReportsTest(unittest.TestCase):
    def test_classifies_supported_documents(self):
        cases = [
            (
                "Financial-report-31-03-2026",
                "https://example.test/Interim%20Financial%20Report%20as%20at%2031%20March%202026.pdf",
                "financial-report",
                ("2026-q1", "financial-report", "Interim Financial Report as at 31 March 2026"),
            ),
            (
                "Annual-Report-2025",
                "https://example.test/Annual-Report-eng-25-03-2026.pdf",
                "financial-report",
                ("2025-fy", "annual-report", "Annual Report 2025"),
            ),
            (
                "presentation-q1-2026",
                "https://example.test/Q1-2026-Results-Presentation.pdf",
                "results-presentation",
                ("2026-q1", "results-presentation", "Q1 2026 Results Presentation"),
            ),
        ]
        for title, url, source_kind, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(syncer.classify(title, url, source_kind), expected)

    def test_rejects_non_results_presentation(self):
        result = syncer.classify(
            "extraordinary-presentation",
            "https://example.test/Amplifon-to-acquire-GN-Hearing.pdf",
            "results-presentation",
        )
        self.assertIsNone(result)

    def test_sync_downloads_new_report_and_generates_index(self):
        with tempfile.TemporaryDirectory() as temporary:
            source_dir = Path(temporary)
            config_path = source_dir / "config.json"
            manifest_path = source_dir / "reports.json"
            index_path = source_dir / "INDEX.md"
            config = {
                "company": "Amplifon",
                "base_url": "https://example.test",
                "index_pages": [
                    {"kind": "financial-report", "url": "https://example.test/reports"},
                    {"kind": "results-presentation", "url": "https://example.test/presentations"},
                ],
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            manifest_path.write_text(json.dumps({"company": "Amplifon", "reports": []}), encoding="utf-8")
            pages = {
                "https://example.test/reports": b'<a href="/en/investors/financial-reports/Financial-report-31-03-2026">READ</a>',
                "https://example.test/presentations": b'<a href="/en/investors/presentations-and-webcast/extraordinary-presentation">READ</a>',
                "https://example.test/en/investors/financial-reports/Financial-report-31-03-2026": (
                    b'<a href="/content/dam/amplifon/archive/en/investors/financial-reports/2026/'
                    b'Interim%20Financial%20Report%20as%20at%2031%20March%202026.pdf">Download</a>'
                ),
                "https://example.test/en/investors/presentations-and-webcast/extraordinary-presentation": (
                    b'<a href="/content/dam/amplifon/archive/en/investors/presentations-webcast/2026/'
                    b'Amplifon-to-acquire-GN-Hearing.pdf">Download</a>'
                ),
                "https://example.test/content/dam/amplifon/archive/en/investors/financial-reports/2026/"
                "Interim%20Financial%20Report%20as%20at%2031%20March%202026.pdf": b"%PDF-1.7\n" + b"x" * 10_000,
            }

            with (
                patch.object(syncer, "SOURCE_DIR", source_dir),
                patch.object(syncer, "CONFIG_PATH", config_path),
                patch.object(syncer, "MANIFEST_PATH", manifest_path),
                patch.object(syncer, "INDEX_PATH", index_path),
                patch.object(syncer, "fetch", side_effect=lambda url: pages[url]),
                patch.object(
                    syncer,
                    "extract_markdown",
                    side_effect=lambda _, destination, report: (
                        destination.parent.mkdir(parents=True, exist_ok=True),
                        destination.write_text(
                            f'---\nsource_url: "{report["source_url"]}"\n---\n\n<!-- page: 1 -->\n\nExtracted text\n',
                            encoding="utf-8",
                        ),
                    ),
                ),
            ):
                self.assertEqual(syncer.sync("2026-06-06"), 0)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["reports"]), 1)
            self.assertEqual(manifest["reports"][0]["period"], "2026-q1")
            self.assertTrue((source_dir / "2026-q1" / "financial-report.md").is_file())
            self.assertIn("2026-06-06", index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
