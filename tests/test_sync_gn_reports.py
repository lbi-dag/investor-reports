import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_gn_reports.py"
SPEC = importlib.util.spec_from_file_location("sync_gn_reports", SCRIPT)
syncer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(syncer)


class SyncGnReportsTest(unittest.TestCase):
    def test_classifies_supported_gn_documents(self):
        cases = [
            (
                "Annual report 2025",
                "Annual Report 2025",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q1/GN-Annual-Report-2025.pdf",
                ("2025-fy", "annual-report"),
            ),
            (
                "Interim Report Q2 2026",
                "Interim report Q2 2026",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q3/GN-Interim-Report-Q2-2026.pdf",
                ("2026-h1", "interim-report"),
            ),
            (
                "Interim Report Q3 2026",
                "Presentation",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q4/GN-Q3-2026-conference-call-presentation.pdf",
                ("2026-9m", "conference-call-presentation"),
            ),
        ]
        for event, title, url, expected in cases:
            with self.subTest(url=url):
                result = syncer.classify_gn_document(event, title, url)
                self.assertEqual((result["period"], result["kind"]), expected)

    def test_rejects_unrelated_gn_documents(self):
        cases = [
            (
                "Annual report 2025",
                "Annual report 2025 cover note",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q1/GN-Annual-Report-2025-cover-note.pdf",
            ),
            (
                "GN enters agreement to sell its Hearing business to Amplifon",
                "Presentation",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q1/transaction-presentation.pdf",
            ),
            (
                "SEB Nordic Seminar",
                "Presentation",
                "https://www.gn.com/-/media/Files/Financial-Download-Center/2026/Q1/SEB-Nordic-Seminar.pdf",
            ),
        ]
        for event, title, url in cases:
            with self.subTest(url=url):
                self.assertIsNone(syncer.classify_gn_document(event, title, url))

    def test_discovers_supported_gn_event_documents(self):
        config = {
            "official_domain": "gn.com",
            "index_url": "https://www.gn.com/investor/financial-reports",
            "discovery_url": "https://www.gn.com/api/downloadcenter/events",
            "discovery_since": "2026-01-01",
            "allowed_pdf_paths": ["/-/media/Files/Financial-Download-Center/"],
        }
        events = [
            {
                "day": "07",
                "month": "May",
                "year": 2026,
                "title": "Interim report Q1 2026",
                "documents": [
                    {"title": "Interim report Q1 2026", "url": "/-/media/Files/Financial-Download-Center/2026/Q2/GN-Interim-Report-Q1-2026.pdf"},
                    {"title": "Presentation", "url": "/-/media/Files/Financial-Download-Center/2026/Q2/GN-Q1-2026-conference-call.pdf"},
                    {"title": "Teleconference", "url": "https://example.test/watch"},
                ],
            }
        ]
        with patch.object(syncer, "fetch", return_value=json.dumps(events).encode()):
            documents = syncer.discover_gn_documents(config)
        self.assertEqual([item["kind"] for item in documents], ["interim-report", "conference-call-presentation"])

    def test_configured_documents_assign_local_files(self):
        config = {
            "documents": [
                {"period": "2025-fy", "kind": "annual-report", "title": "Annual", "source_url": "https://example.test/a.pdf"},
                {"period": "2026-q1", "kind": "interim-report", "title": "Interim", "source_url": "https://example.test/b.pdf"},
            ]
        }
        documents = syncer.configured_documents(config)
        self.assertEqual(documents[0]["local_file"], "2025-fy/annual-report.md")
        self.assertEqual(documents[1]["local_file"], "2026-q1/interim-report.md")

    def test_sync_downloads_configured_documents(self):
        with tempfile.TemporaryDirectory() as temporary:
            source_dir = Path(temporary)
            config_path = source_dir / "config.json"
            manifest_path = source_dir / "reports.json"
            index_path = source_dir / "INDEX.md"
            url = "https://example.test/gn-q1.pdf"
            config = {
                "company": "GN Store Nord",
                "index_url": "https://example.test/reports",
                "documents": [{"period": "2026-q1", "title": "GN Q1", "kind": "interim-report", "source_url": url}],
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            manifest_path.write_text(json.dumps({"company": "GN Store Nord", "reports": []}), encoding="utf-8")

            with (
                patch.object(syncer, "SOURCE_DIR", source_dir),
                patch.object(syncer, "CONFIG_PATH", config_path),
                patch.object(syncer, "MANIFEST_PATH", manifest_path),
                patch.object(syncer, "INDEX_PATH", index_path),
                patch.object(syncer, "discovered_documents", return_value=[config["documents"][0]]),
                patch.object(syncer, "fetch", return_value=b"%PDF-1.7\n" + b"x" * 10_000),
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
            self.assertEqual(manifest["reports"][0]["period"], "2026-q1")
            self.assertTrue((source_dir / "2026-q1" / "interim-report.md").is_file())
            self.assertIn("GN Store Nord Source Reports", index_path.read_text(encoding="utf-8"))

    def test_sync_skips_discovered_replacement_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            source_dir = Path(temporary)
            config_path = source_dir / "config.json"
            manifest_path = source_dir / "reports.json"
            index_path = source_dir / "INDEX.md"
            existing = {
                "period": "2026-q1",
                "title": "Existing",
                "kind": "interim-report",
                "source_url": "https://www.gn.com/existing.pdf",
                "local_file": "2026-q1/interim-report.md",
                "downloaded_at": "2026-06-01",
            }
            config = {"company": "GN Store Nord", "index_url": "https://www.gn.com/reports", "documents": []}
            config_path.write_text(json.dumps(config), encoding="utf-8")
            manifest_path.write_text(json.dumps({"company": "GN Store Nord", "reports": [existing]}), encoding="utf-8")
            destination = source_dir / existing["local_file"]
            destination.parent.mkdir(parents=True)
            destination.write_text(f'{existing["source_url"]}\n<!-- page: 1 -->', encoding="utf-8")
            replacement = {**existing, "source_url": "https://www.gn.com/replacement.pdf"}

            with (
                patch.object(syncer, "SOURCE_DIR", source_dir),
                patch.object(syncer, "CONFIG_PATH", config_path),
                patch.object(syncer, "MANIFEST_PATH", manifest_path),
                patch.object(syncer, "INDEX_PATH", index_path),
                patch.object(syncer, "discovered_documents", return_value=[replacement]),
            ):
                self.assertEqual(syncer.sync("2026-06-06", check=True), 0)


if __name__ == "__main__":
    unittest.main()
