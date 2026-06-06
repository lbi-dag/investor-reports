#!/usr/bin/env python3
"""Discover, download, and index official Amplifon financial reports."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "amplifon"
CONFIG_PATH = SOURCE_DIR / "config.json"
MANIFEST_PATH = SOURCE_DIR / "reports.json"
INDEX_PATH = SOURCE_DIR / "INDEX.md"
USER_AGENT = "investor-reports-source-sync/1.0"
MIN_PDF_BYTES = 10_000


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.links.append((self._href, clean_text(" ".join(self._text))))
            self._href = None
            self._text = []


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def parse_links(body: bytes) -> list[tuple[str, str]]:
    parser = LinkParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    return parser.links


def discover_detail_pages(config: dict) -> list[tuple[str, str, str]]:
    discovered: list[tuple[str, str, str]] = []
    base_url = config["base_url"]
    for source in config["index_pages"]:
        for href, _ in parse_links(fetch(source["url"])):
            absolute = urllib.parse.urljoin(base_url, href)
            if source["kind"] == "financial-report":
                if "/en/investors/financial-reports/" not in absolute:
                    continue
            elif "/en/investors/presentations-and-webcast/" not in absolute:
                continue
            if absolute not in {item[1] for item in discovered}:
                discovered.append((source["kind"], absolute, source["url"]))
    return discovered


def discover_pdf(detail_url: str) -> str | None:
    candidates = []
    for href, _ in parse_links(fetch(detail_url)):
        absolute = urllib.parse.urljoin(detail_url, href)
        if urllib.parse.urlparse(absolute).path.lower().endswith(".pdf"):
            candidates.append(absolute)
    archive = [url for url in candidates if "/content/dam/amplifon/archive/en/investors/" in url]
    return (archive or candidates or [None])[0]


def title_from_detail_url(detail_url: str, pdf_url: str) -> str:
    slug = urllib.parse.unquote(detail_url.rstrip("/").split("/")[-1])
    pdf_name = urllib.parse.unquote(urllib.parse.urlparse(pdf_url).path.split("/")[-1])
    source = slug if slug.lower() not in {"download", "document"} else pdf_name.removesuffix(".pdf")
    return clean_text(re.sub(r"[-_]+", " ", source))


def classify(title: str, pdf_url: str, source_kind: str) -> tuple[str, str, str] | None:
    text = clean_text(f"{title} {urllib.parse.unquote(pdf_url)}")
    lower = clean_text(re.sub(r"[-_]+", " ", text.lower()))
    year_matches = re.findall(r"\b20\d{2}\b", text)
    if not year_matches:
        return None

    if "annual report" in lower:
        annual_match = re.search(r"annual report\s+(20\d{2})", lower)
        year = annual_match.group(1) if annual_match else year_matches[-1]
        return f"{year}-fy", "annual-report", f"Annual Report {year}"

    if source_kind == "results-presentation":
        if "result" not in lower or "presentation" not in lower:
            return None
        year = year_matches[-1]
        if re.search(r"\bq1\b", lower):
            label = "Q1"
            period = "q1"
        elif re.search(r"\b(h1|q2)\b", lower):
            label = "H1"
            period = "h1"
        elif re.search(r"\b(9m|q3)\b", lower):
            label = "9M"
            period = "9m"
        elif re.search(r"\b(fy|q4)\b", lower):
            label = "FY"
            period = "fy"
        else:
            return None
        return f"{year}-{period}", "results-presentation", f"{label} {year} Results Presentation"

    date_match = re.search(r"\b(31 march|30 june|30 september)\s+(20\d{2})\b", lower)
    if not date_match:
        return None
    period_by_date = {"31 march": "q1", "30 june": "h1", "30 september": "9m"}
    label_by_date = {"31 march": "31 March", "30 june": "30 June", "30 september": "30 September"}
    date_text, year = date_match.groups()
    period = period_by_date[date_text]
    canonical = f"Interim Financial Report as at {label_by_date[date_text]} {year}"
    return f"{year}-{period}", "financial-report", canonical


def local_filename(period: str, kind: str) -> str:
    filename = {
        "annual-report": "annual-report.md",
        "financial-report": "financial-report.md",
        "results-presentation": "results-presentation.md",
    }[kind]
    return f"{period}/{filename}"


def validate_pdf(data: bytes, source_url: str) -> None:
    if len(data) < MIN_PDF_BYTES:
        raise ValueError(f"PDF from {source_url} is unexpectedly small ({len(data)} bytes)")
    if not data.startswith(b"%PDF-"):
        raise ValueError(f"Download from {source_url} is not a PDF")


def extract_markdown(data: bytes, destination: Path, report: dict) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        pdf_path = Path(temporary) / "source.pdf"
        markdown_path = Path(temporary) / "extract.md"
        pdf_path.write_bytes(data)
        subprocess.run(
            ["node", str(ROOT / "scripts" / "extract_pdf_markdown.mjs"), str(pdf_path), str(markdown_path)],
            check=True,
        )
        extracted = markdown_path.read_text(encoding="utf-8")
    if "<!-- page: 1 -->" not in extracted:
        raise ValueError(f"Extractor produced no page markers for {report['source_url']}")
    frontmatter = [
        "---",
        f'title: "{report["title"].replace(chr(34), chr(39))}"',
        f'period: "{report["period"]}"',
        f'kind: "{report["kind"]}"',
        f'source_url: "{report["source_url"]}"',
        f'downloaded_at: "{report["downloaded_at"]}"',
        f'pdf_sha256: "{report["sha256"]}"',
        f'pdf_size_bytes: {report["size_bytes"]}',
        'extractor: "pdfjs-dist-6.0.227"',
        "---",
        "",
    ]
    destination.write_text("\n".join(frontmatter) + extracted, encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def period_sort_key(report: dict) -> tuple[int, int, str]:
    year, period = report["period"].split("-", 1)
    order = {"q1": 1, "h1": 2, "9m": 3, "fy": 4}
    return int(year), order[period], report["kind"]


def display_period(period: str) -> str:
    year, suffix = period.split("-", 1)
    return f"{suffix.upper()} {year}" if suffix != "fy" else f"FY {year}"


def generate_index(manifest: dict, config: dict) -> str:
    lines = [
        "# Amplifon Source Reports",
        "",
        "Official Amplifon investor materials downloaded from",
        "[corporate.amplifon.com](https://corporate.amplifon.com/en/investors).",
        "",
        "Amplifon's interim financial reporting cadence uses Q1, H1, and 9M reports",
        "rather than standalone Q2 and Q3 reports. Annual reports are stored under the",
        "financial year they cover, even when published the following year.",
        "",
        "PDFs are downloaded temporarily, checksum-verified, and converted to page-marked",
        "Markdown. The original PDF remains available through its official download URL.",
        "",
        "This file is generated by `python3 scripts/sync_amplifon_reports.py` from",
        "[reports.json](reports.json).",
        "",
        "## Reports",
        "",
        "| Period | Document | Downloaded | Local file | Official download URL |",
        "| --- | --- | --- | --- | --- |",
    ]
    for report in sorted(manifest["reports"], key=period_sort_key):
        lines.append(
            f'| {display_period(report["period"])} | {report["title"]} | '
            f'{report["downloaded_at"]} | [{Path(report["local_file"]).name}]'
            f'({report["local_file"]}) | [Download]({report["source_url"]}) |'
        )
    lines.extend(["", "## Official Indexes", ""])
    for source in config["index_pages"]:
        label = "Financial reports" if source["kind"] == "financial-report" else "Presentations and webcasts"
        lines.append(f'- [{label}]({source["url"]})')
    return "\n".join(lines) + "\n"


def verify_manifest(manifest: dict) -> None:
    for report in manifest["reports"]:
        path = SOURCE_DIR / report["local_file"]
        if not path.is_file():
            raise FileNotFoundError(f"Manifest file is missing: {path}")
        extracted = path.read_text(encoding="utf-8")
        if "<!-- page: 1 -->" not in extracted or report["source_url"] not in extracted:
            raise ValueError(f"Markdown extract metadata is invalid: {path}")


def refresh_extracts(manifest: dict) -> None:
    for report in manifest["reports"]:
        data = fetch(report["source_url"])
        validate_pdf(data, report["source_url"])
        if hashlib.sha256(data).hexdigest() != report["sha256"] or len(data) != report["size_bytes"]:
            raise ValueError(f"Official PDF changed for {report['source_url']}")
        extract_markdown(data, SOURCE_DIR / report["local_file"], report)
        print(f"Refreshed {report['local_file']}")


def sync(download_date: str, check: bool = False) -> int:
    config = load_json(CONFIG_PATH)
    manifest = load_json(MANIFEST_PATH)
    known_urls = {report["source_url"] for report in manifest["reports"]}
    known_keys = {(report["period"], report["kind"]) for report in manifest["reports"]}
    additions = []

    for source_kind, detail_url, _ in discover_detail_pages(config):
        pdf_url = discover_pdf(detail_url)
        if not pdf_url or pdf_url in known_urls:
            continue
        classification = classify(title_from_detail_url(detail_url, pdf_url), pdf_url, source_kind)
        if not classification:
            continue
        period, kind, title = classification
        if (period, kind) in known_keys:
            print(f"Skipping replacement candidate for {period} {kind}: {pdf_url}", file=sys.stderr)
            continue
        additions.append((period, kind, title, pdf_url))
        known_keys.add((period, kind))

    if check:
        if additions:
            for period, kind, _, url in additions:
                print(f"New report available: {period} {kind} {url}")
            return 1
        print("No new reports found.")
        return 0

    for period, kind, title, pdf_url in additions:
        data = fetch(pdf_url)
        validate_pdf(data, pdf_url)
        report = {
                "period": period,
                "title": title,
                "kind": kind,
                "local_file": local_filename(period, kind),
                "source_url": pdf_url,
                "downloaded_at": download_date,
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        destination = SOURCE_DIR / report["local_file"]
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite {destination}")
        extract_markdown(data, destination, report)
        manifest["reports"].append(report)
        print(f"Downloaded and extracted {title} to {report['local_file']}")

    manifest["reports"].sort(key=period_sort_key)
    verify_manifest(manifest)
    write_json(MANIFEST_PATH, manifest)
    INDEX_PATH.write_text(generate_index(manifest, config), encoding="utf-8")
    print(f"Indexed {len(manifest['reports'])} reports; added {len(additions)}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report whether new documents exist without downloading")
    parser.add_argument("--refresh-extracts", action="store_true", help="Regenerate Markdown from verified source PDFs")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Download date recorded for new files")
    args = parser.parse_args()
    if args.refresh_extracts:
        manifest = load_json(MANIFEST_PATH)
        refresh_extracts(manifest)
        verify_manifest(manifest)
        return 0
    return sync(args.date, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
