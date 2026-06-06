#!/usr/bin/env python3
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


REQUIRED_MARKERS = (
    "One-line verdict:",
    "What Is Genuinely Working",
    "What The Headline Obscures",
    "Corporate Language, Decoded",
    "What To Watch Next",
    "Sources And Caveats",
    "Analysis Date:",
    "Skill Version:",
    "Model Version:",
    "Source SHA-256:",
)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def local_link_errors(html_path):
    parser = LinkParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    errors = []
    for href in parser.links:
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:")):
            continue
        target = (html_path.parent / unquote(parsed.path)).resolve()
        if not target.exists():
            errors.append(f"broken local link: {href}")
    return errors


def report_structure_errors(html_path):
    content = html_path.read_text(encoding="utf-8")
    errors = [f"missing required marker: {marker}" for marker in REQUIRED_MARKERS if marker not in content]
    if "../sources/" not in content:
        errors.append("missing local primary-source citation")
    return errors


def report_contract_errors(html_path):
    errors = report_structure_errors(html_path)
    errors.extend(local_link_errors(html_path))
    return errors


def validate_report(html_path):
    return report_contract_errors(Path(html_path))


def main():
    parser = argparse.ArgumentParser(description="Validate investor report structure and local links.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--links-only", action="store_true")
    args = parser.parse_args()
    paths = args.paths or sorted(Path("reports").glob("*.html"))

    failures = 0
    for path in paths:
        errors = local_link_errors(path) if args.links_only else validate_report(path)
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
