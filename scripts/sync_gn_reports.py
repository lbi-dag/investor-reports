#!/usr/bin/env python3
"""Discover, download, extract, and index official GN and Sonova reports."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

try:
    from scripts.sync_amplifon_reports import clean_text, extract_markdown, fetch, validate_pdf
except ModuleNotFoundError:
    from sync_amplifon_reports import clean_text, extract_markdown, fetch, validate_pdf


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "gn"
CONFIG_PATH = SOURCE_DIR / "config.json"
MANIFEST_PATH = SOURCE_DIR / "reports.json"
INDEX_PATH = SOURCE_DIR / "INDEX.md"


class ContextLinkParser(HTMLParser):
    """Capture PDF links with the closest preceding heading in their container."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._heading: list[str] | None = None
        self._latest_heading = ""
        self._href: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h2", "h3", "h4"}:
            self._heading = []
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._link_text = []

    def handle_data(self, data: str) -> None:
        if self._heading is not None:
            self._heading.append(data)
        if self._href is not None:
            self._link_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h2", "h3", "h4"} and self._heading is not None:
            self._latest_heading = clean_text(" ".join(self._heading))
            self._heading = None
        if tag == "a" and self._href is not None:
            link_text = clean_text(" ".join(self._link_text))
            self.links.append((self._href, link_text or self._latest_heading))
            self._href = None
            self._link_text = []


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def local_filename(period: str, kind: str) -> str:
    filename = {
        "annual-report": "annual-report.md",
        "interim-report": "interim-report.md",
        "half-year-report": "half-year-report.md",
        "results-release": "results-release.md",
        "results-presentation": "results-presentation.md",
        "conference-call-presentation": "conference-call-presentation.md",
    }[kind]
    return f"{period}/{filename}"


def period_sort_key(report: dict) -> tuple[int, int, str]:
    year, period = report["period"].split("-", 1)
    order = {"q1": 1, "h1": 2, "9m": 3, "fy": 4}
    return int(year), order[period], report["kind"]


def display_period(period: str) -> str:
    year, suffix = period.split("-", 1)
    return f"{suffix.upper()} {year}" if suffix != "fy" else f"FY {year}"


def configured_documents(config: dict) -> list[dict]:
    documents = []
    for document in config["documents"]:
        normalized = dict(document)
        normalized["local_file"] = local_filename(document["period"], document["kind"])
        documents.append(normalized)
    return documents


def is_official_pdf(url: str, config: dict) -> bool:
    parsed = urllib.parse.urlparse(url)
    official_domain = config["official_domain"].lower()
    allowed_paths = config.get("allowed_pdf_paths", [])
    return (
        parsed.scheme == "https"
        and (parsed.hostname or "").lower() in {official_domain, f"www.{official_domain}"}
        and parsed.path.lower().endswith(".pdf")
        and (not allowed_paths or any(parsed.path.startswith(path) for path in allowed_paths))
    )


def gn_period(event_title: str) -> tuple[str, str] | None:
    interim = re.fullmatch(r"interim report q([123]) (20\d{2})", clean_text(event_title).lower())
    if interim:
        quarter, year = interim.groups()
        suffix = {"1": "q1", "2": "h1", "3": "9m"}[quarter]
        return f"{year}-{suffix}", f"Q{quarter} {year}"
    annual = re.fullmatch(r"annual report (20\d{2})", clean_text(event_title).lower())
    if annual:
        year = annual.group(1)
        return f"{year}-fy", f"FY {year}"
    return None


def classify_gn_document(event_title: str, document_title: str, url: str) -> dict | None:
    period_info = gn_period(event_title)
    if not period_info:
        return None
    period, label = period_info
    combined = clean_text(f"{document_title} {urllib.parse.unquote(url)}").lower()
    if any(term in combined for term in ("cover note", "governance", "remuneration", "xhtml")):
        return None

    if period.endswith("-fy") and re.search(r"\bgn[- ]annual[- ]report[- ]20\d{2}\b", combined):
        kind = "annual-report"
        title = f"GN Annual Report {period[:4]}"
    elif not period.endswith("-fy") and "interim report" in combined:
        kind = "interim-report"
        title = f"GN Interim Report {label}"
    elif "conference-call" in combined:
        kind = "conference-call-presentation"
        title = f"GN {label} Conference Call Presentation"
    else:
        return None
    return {"period": period, "kind": kind, "title": title, "source_url": url}


def discover_gn_documents(config: dict) -> list[dict]:
    endpoint = config["discovery_url"]
    events = json.loads(fetch(endpoint).decode("utf-8"))
    cutoff = dt.date.fromisoformat(config["discovery_since"])
    documents = []
    for event in events:
        event_date = dt.date.fromisoformat(
            f'{event["year"]:04d}-{dt.datetime.strptime(event["month"], "%b").month:02d}-{int(event["day"]):02d}'
        )
        if event_date < cutoff:
            continue
        for document in event.get("documents", []):
            url = urllib.parse.urljoin(config["index_url"], document.get("url", "").strip())
            if not is_official_pdf(url, config):
                continue
            classified = classify_gn_document(event.get("title", ""), document.get("title", ""), url)
            if classified:
                documents.append(classified)
    return documents


def sonova_period(text: str) -> tuple[str, str, str] | None:
    normalized = clean_text(re.sub(r"[_-]+", " ", urllib.parse.unquote(text))).lower()
    fiscal = re.search(r"\b(20)?(\d{2})\s*/?\s*(\d{2})\b", normalized)
    if not fiscal:
        return None
    end_year = int(fiscal.group(3))
    year = 2000 + end_year
    if re.search(r"\b(half year|half-year|hy|h1)\b", normalized):
        return f"{year}-h1", "H1", f"{fiscal.group(2)}/{fiscal.group(3)}"
    if re.search(r"\b(full year|full-year|fy|annual|ar)\b", normalized):
        return f"{year}-fy", "FY", f"{fiscal.group(2)}/{fiscal.group(3)}"
    return None


def classify_sonova_document(context: str, url: str, source_kind: str) -> dict | None:
    combined = clean_text(f"{context} {urllib.parse.unquote(url)}")
    lower = clean_text(re.sub(r"[_-]+", " ", combined.lower()))
    if any(
        term in lower
        for term in (
            "strategy",
            "sustainability",
            "corporate governance",
            "corpgov",
            "compensation",
            "business report",
            "finance en",
            "financial report",
            "restated comparative",
        )
    ):
        return None
    period_info = sonova_period(combined)
    if not period_info:
        return None
    period, label, fiscal_year = period_info

    if period.endswith("-h1") and ("half year report" in lower or "half-year report" in lower):
        kind = "half-year-report"
        title = f"Sonova Half-Year Report 20{fiscal_year}"
    elif period.endswith("-fy") and ("full report" in lower or "annual report" in lower):
        kind = "annual-report"
        title = f"Sonova Annual Report 20{fiscal_year}"
    elif "presentation" in lower and source_kind in {"financial-reports", "investor-presentations"}:
        kind = "results-presentation"
        title = f"Sonova {label} 20{fiscal_year} Results Presentation"
    elif source_kind == "financial-reports" and ("results" in lower or "media release" in lower):
        kind = "results-release"
        title = f"Sonova {label} 20{fiscal_year} Results Release"
    else:
        return None
    return {"period": period, "kind": kind, "title": title, "source_url": url}


def discover_sonova_documents(config: dict) -> list[dict]:
    documents = []
    for source in config["index_pages"]:
        parser = ContextLinkParser()
        parser.feed(fetch(source["url"]).decode("utf-8", errors="replace"))
        for href, context in parser.links:
            url = urllib.parse.urljoin(source["url"], html.unescape(href))
            if not is_official_pdf(url, config):
                continue
            classified = classify_sonova_document(context, url, source["kind"])
            if classified:
                documents.append(classified)
    return documents


def discovered_documents(config: dict) -> list[dict]:
    if "discovery_url" not in config and "index_pages" not in config:
        return []
    if config["company"] == "GN Store Nord":
        return discover_gn_documents(config)
    if config["company"] == "Sonova":
        return discover_sonova_documents(config)
    raise ValueError(f'No discovery adapter for {config["company"]}')


def generate_index(manifest: dict, config: dict) -> str:
    lines = [
        f'# {config["company"]} Source Reports',
        "",
        f'Official {config["company"]} investor materials downloaded from',
        f'[{config.get("official_domain", config["company"])}]({config["index_url"]}).',
        "",
        "PDFs are downloaded temporarily, checksum-verified, and converted to page-marked",
        "Markdown. The original PDF remains available through its official download URL.",
        "",
        f'This file is generated by `{config.get("sync_command", "python3 scripts/sync_gn_reports.py")}` from',
        "[config.json](config.json) and [reports.json](reports.json).",
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
    for source in config.get("index_pages", [{"url": config["index_url"], "label": "Financial reports"}]):
        lines.append(f'- [{source.get("label") or source.get("kind", "Financial reports")}]({source["url"]})')
    return "\n".join(lines) + "\n"


def verify_manifest(manifest: dict) -> None:
    for report in manifest["reports"]:
        path = SOURCE_DIR / report["local_file"]
        if not path.is_file():
            raise FileNotFoundError(f"Manifest file is missing: {path}")
        extracted = path.read_text(encoding="utf-8")
        if "<!-- page: 1 -->" not in extracted or report["source_url"] not in extracted:
            raise ValueError(f"Markdown extract metadata is invalid: {path}")


def sync(download_date: str, check: bool = False) -> int:
    config = load_json(CONFIG_PATH)
    manifest = load_json(MANIFEST_PATH)
    known_urls = {report["source_url"] for report in manifest["reports"]}
    known_keys = {(report["period"], report["kind"]) for report in manifest["reports"]}
    additions = []

    candidates = configured_documents(config) + discovered_documents(config)
    candidate_urls = set()
    for document in candidates:
        document = {**document, "local_file": local_filename(document["period"], document["kind"])}
        key = (document["period"], document["kind"])
        if document["source_url"] in known_urls or document["source_url"] in candidate_urls:
            continue
        if key in known_keys:
            print(f"Skipping replacement candidate for {document['period']} {document['kind']}: {document['source_url']}", file=sys.stderr)
            continue
        additions.append(document)
        candidate_urls.add(document["source_url"])
        known_keys.add(key)

    if check:
        if additions:
            for document in additions:
                print(f'New report available: {document["period"]} {document["kind"]} {document["source_url"]}')
            return 1
        print("No new reports found.")
        return 0

    for document in additions:
        data = fetch(document["source_url"])
        validate_pdf(data, document["source_url"])
        report = {
            **document,
            "downloaded_at": download_date,
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        destination = SOURCE_DIR / report["local_file"]
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite {destination}")
        extract_markdown(data, destination, report)
        manifest["reports"].append(report)
        print(f'Downloaded and extracted {report["title"]} to {report["local_file"]}')

    manifest["reports"].sort(key=period_sort_key)
    verify_manifest(manifest)
    write_json(MANIFEST_PATH, manifest)
    INDEX_PATH.write_text(generate_index(manifest, config), encoding="utf-8")
    print(f"Indexed {len(manifest['reports'])} reports; added {len(additions)}.")
    return 0


def refresh_extracts() -> None:
    manifest = load_json(MANIFEST_PATH)
    for report in manifest["reports"]:
        data = fetch(report["source_url"])
        validate_pdf(data, report["source_url"])
        if hashlib.sha256(data).hexdigest() != report["sha256"] or len(data) != report["size_bytes"]:
            raise ValueError(f"Official PDF changed for {report['source_url']}")
        extract_markdown(data, SOURCE_DIR / report["local_file"], report)
        print(f'Refreshed {report["local_file"]}')
    verify_manifest(manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report whether newly discovered documents are not yet downloaded")
    parser.add_argument("--refresh-extracts", action="store_true", help="Regenerate Markdown from verified source PDFs")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Download date recorded for new files")
    args = parser.parse_args()
    if args.refresh_extracts:
        refresh_extracts()
        return 0
    return sync(args.date, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
