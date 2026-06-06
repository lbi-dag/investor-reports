import unittest
import unittest.mock
import json
import os
import shutil
from pathlib import Path
from scripts.inventory_reports import get_existing_reports, get_available_sources, period_sort_key

class TestInventoryReports(unittest.TestCase):
    def test_period_sort_key(self):
        # Q1 < H1 < 9M < FY
        self.assertLess(period_sort_key("2024-q1"), period_sort_key("2024-h1"))
        self.assertLess(period_sort_key("2024-h1"), period_sort_key("2024-9m"))
        self.assertLess(period_sort_key("2024-9m"), period_sort_key("2024-fy"))
        # 2024 < 2025
        self.assertLess(period_sort_key("2024-fy"), period_sort_key("2025-q1"))

    def test_get_existing_reports_empty(self):
        # Test with non-existent dir
        with unittest.mock.patch('scripts.inventory_reports.REPORTS_DIR', Path('non_existent_dir')):
            reports = get_existing_reports()
            self.assertEqual(reports, {"amplifon": []})

    def test_get_available_sources_missing_manifest(self):
        # Test with missing reports.json
        with unittest.mock.patch('scripts.inventory_reports.SOURCES_DIR', Path('non_existent_dir')):
            sources = get_available_sources()
            self.assertEqual(sources, {})

if __name__ == "__main__":
    unittest.main()
