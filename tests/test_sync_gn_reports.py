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
            self.assertIn("GN Source Reports", index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
