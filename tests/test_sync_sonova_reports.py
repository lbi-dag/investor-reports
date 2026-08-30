import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_gn_reports.py"
SPEC = importlib.util.spec_from_file_location("sync_sonova_engine", SCRIPT)
syncer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(syncer)


class SyncSonovaReportsTest(unittest.TestCase):
    def test_classifies_supported_sonova_documents(self):
        cases = [
            (
                "Full-Year Results 2025/26",
                "https://www.sonova.com/sites/default/files/2026-05/01_Sonova_AR_25-26_Full_Report_en.pdf",
                "financial-reports",
                ("2026-fy", "annual-report"),
            ),
            (
                "Half-Year Results 2025/26",
                "https://www.sonova.com/sites/default/files/2025-11/Sonova_Half-Year%20report%202025-26_EN.pdf",
                "financial-reports",
                ("2026-h1", "half-year-report"),
            ),
            (
                "Media Release publication FY 2025/26 results",
                "https://www.sonova.com/sites/default/files/2026-05/Sonova_FY25-26%20Results_EN.pdf",
                "financial-reports",
                ("2026-fy", "results-release"),
            ),
            (
                "Full-Year Results 2025/26",
                "https://www.sonova.com/sites/default/files/2026-05/Sonova%20FY_25-26_Presentation.pdf",
                "investor-presentations",
                ("2026-fy", "results-presentation"),
            ),
        ]
        for context, url, source_kind, expected in cases:
            with self.subTest(url=url):
                result = syncer.classify_sonova_document(context, url, source_kind)
                self.assertEqual((result["period"], result["kind"]), expected)

    def test_rejects_unrelated_sonova_documents(self):
        cases = [
            ("Strategy Update", "https://www.sonova.com/sites/default/files/2026-03/Sonova_Strategy_Presentation.pdf", "investor-presentations"),
            ("Sustainability Report", "https://www.sonova.com/sites/default/files/2026-05/Sonova_AR_25-26_Sustainability_en.pdf", "financial-reports"),
            ("Compensation Report", "https://www.sonova.com/sites/default/files/2026-05/Sonova_AR_25-26_Comp_en.pdf", "financial-reports"),
            ("Restated comparative figures FY 24/25 and FY 25/26", "https://www.sonova.com/sites/default/files/2026-05/Restated_comparative_figures.pdf", "financial-reports"),
        ]
        for context, url, source_kind in cases:
            with self.subTest(url=url):
                self.assertIsNone(syncer.classify_sonova_document(context, url, source_kind))

    def test_discovers_contextual_sonova_links(self):
        config = {
            "official_domain": "sonova.com",
            "allowed_pdf_paths": ["/wp-content/uploads/", "/sites/default/files/"],
            "index_pages": [{"kind": "financial-reports", "url": "https://www.sonova.com/financial-reports/"}],
        }
        body = b"""
        <h3>Full-Year Results 2025/26</h3>
        <a href="/wp-content/uploads/2026/05/01_Sonova_AR_25-26_Full_Report_en.pdf"></a>
        <h3>Sustainability Report</h3>
        <a href="/wp-content/uploads/2026/05/10_Sonova_AR_25-26_Sustainability_en.pdf"></a>
        """
        with patch.object(syncer, "fetch", return_value=body):
            documents = syncer.discover_sonova_documents(config)
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]["kind"], "annual-report")

    def test_rejects_non_official_pdf_url(self):
        config = {"official_domain": "sonova.com", "allowed_pdf_paths": ["/wp-content/uploads/", "/sites/default/files/"]}
        self.assertFalse(syncer.is_official_pdf("https://example.test/sites/default/files/report.pdf", config))
        self.assertFalse(syncer.is_official_pdf("https://www.sonova.com/other/report.pdf", config))
        self.assertTrue(syncer.is_official_pdf("https://www.sonova.com/wp-content/uploads/2026/05/report.pdf", config))
        self.assertTrue(syncer.is_official_pdf("https://www.sonova.com/sites/default/files/report.pdf", config))

    def test_discovery_respects_sonova_coverage_start(self):
        config = {
            "official_domain": "sonova.com",
            "allowed_pdf_paths": ["/wp-content/uploads/"],
            "discovery_since": "2026-01-01",
            "index_pages": [{"kind": "financial-reports", "url": "https://www.sonova.com/financial-reports/"}],
        }
        body = b"""
        <h3>Annual Report 2024/25</h3>
        <a href="/wp-content/uploads/2025/05/01_Sonova_AR_24-25_Full_Report_en.pdf"></a>
        <h3>Full-Year Results 2025/26</h3>
        <a href="/wp-content/uploads/2026/05/01_Sonova_AR_25-26_Full_Report_en.pdf"></a>
        """
        with patch.object(syncer, "fetch", return_value=body):
            documents = syncer.discover_sonova_documents(config)
        self.assertEqual([(item["period"], item["kind"]) for item in documents], [("2026-fy", "annual-report")])

    def test_source_config_uses_live_sonova_reports_index(self):
        config_path = Path(__file__).resolve().parents[1] / "sources" / "sonova" / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["index_pages"], [{
            "kind": "financial-reports",
            "label": "Reports and presentations",
            "url": "https://www.sonova.com/financial-reports/",
        }])
        self.assertIn("/wp-content/uploads/", config["allowed_pdf_paths"])


if __name__ == "__main__":
    unittest.main()
