#!/usr/bin/env python3
"""Discover, download, extract, and index official Sonova financial reports."""

from pathlib import Path

try:
    from scripts import sync_gn_reports as syncer
except ImportError:
    import sync_gn_reports as syncer

ROOT = Path(__file__).resolve().parents[1]
syncer.SOURCE_DIR = ROOT / "sources" / "sonova"
syncer.CONFIG_PATH = syncer.SOURCE_DIR / "config.json"
syncer.MANIFEST_PATH = syncer.SOURCE_DIR / "reports.json"
syncer.INDEX_PATH = syncer.SOURCE_DIR / "INDEX.md"

if __name__ == "__main__":
    raise SystemExit(syncer.main())
