import unittest
import unittest.mock
import json
import os
import shutil
from pathlib import Path
from scripts.inventory_reports import extract_brief, format_period, get_existing_reports, get_available_sources, period_sort_key, render_company_directory, render_company_page

class TestInventoryReports(unittest.TestCase):
    def test_period_sort_key(self):
        # Q1 < H1 < 9M < FY
        self.assertLess(period_sort_key("2024-q1"), period_sort_key("2024-h1"))
        self.assertLess(period_sort_key("2024-h1"), period_sort_key("2024-9m"))
        self.assertLess(period_sort_key("2024-9m"), period_sort_key("2024-fy"))
        # 2024 < 2025
        self.assertLess(period_sort_key("2024-fy"), period_sort_key("2025-q1"))

    def test_format_period(self):
        self.assertEqual(format_period("2026-q1"), "Q1 2026")
        self.assertEqual(format_period("2025-fy"), "FY 2025")

    def test_extract_brief_reads_header_badge(self):
        self.assertEqual(
            extract_brief(Path("reports/amplifon-2026-q1.html")),
            "Recovery signs, major deal risk",
        )

    def test_get_existing_reports_empty(self):
        # Test with non-existent dir
        with unittest.mock.patch('scripts.inventory_reports.REPORTS_DIR', Path('non_existent_dir')):
            reports = get_existing_reports()
            self.assertEqual(reports, {"amplifon": []})

    def test_get_existing_reports_ignores_invalid_report(self):
        with unittest.mock.patch('scripts.inventory_reports.REPORTS_DIR', Path('reports')):
            with unittest.mock.patch('scripts.inventory_reports.report_structure_errors', return_value=["invalid"]):
                reports = get_existing_reports()
                self.assertEqual(reports, {"amplifon": []})

    def test_get_available_sources_missing_manifest(self):
        # Test with missing reports.json
        with unittest.mock.patch('scripts.inventory_reports.SOURCES_DIR', Path('non_existent_dir')):
            sources = get_available_sources()
            self.assertEqual(sources, {})

    def test_company_directory_links_covered_company_and_lists_planned_company(self):
        html = render_company_directory([{"company": "amplifon", "status": "PRESENT"}])
        self.assertIn('href="companies/amplifon.html"', html)
        self.assertIn('href="companies/starkey.html"', html)
        self.assertIn('href="companies/gn.html"', html)
        self.assertIn("Coverage planned", html)
        self.assertIn("Tracking the gap between corporate narratives and financial reality.", html)
        self.assertIn("<svg", html)
        self.assertIn('src="assets/company-logos/amplifon.svg"', html)
        self.assertIn('src="assets/company-logos/starkey.svg"', html)
        self.assertIn('src="assets/company-logos/gn.svg"', html)

    def test_company_page_links_reports_from_company_directory(self):
        inventory = [{"company": "amplifon", "period": "2025-fy", "status": "PRESENT", "document_count": 2}]
        company = {"slug": "amplifon", "name": "Amplifon", "ticker": "AMP:IM", "logo": "amplifon.svg"}
        html = render_company_page(company, inventory)
        self.assertIn('href="../reports/amplifon-2025.html"', html)
        self.assertIn('href="../index.html"', html)
        self.assertIn("Stalled growth, recovery plan unproven", html)
        self.assertNotIn("One-line verdict", html)
        self.assertIn("Latest analysis", html)
        self.assertIn("FY 2025", html)
        self.assertIn("Official source documents", html)
        self.assertIn('src="../assets/company-logos/amplifon.svg"', html)

    def test_planned_company_page_has_no_broken_source_link(self):
        company = {"slug": "starkey", "name": "Starkey", "ticker": "Private"}
        html = render_company_page(company, [])
        self.assertIn("No reports available yet", html)
        self.assertNotIn("../sources/starkey/INDEX.md", html)

if __name__ == "__main__":
    unittest.main()
