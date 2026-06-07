# Developer Workflow

This document keeps local setup and operational commands out of the product
README.

## Requirements

- Python 3.12+
- Node.js 22+

Install the pinned PDF extraction dependency:

```bash
npm ci
```

## Sync Sources

Discover and extract newly published Amplifon materials:

```bash
python3 scripts/sync_amplifon_reports.py
```

Check whether new Amplifon reports exist without downloading them:

```bash
python3 scripts/sync_amplifon_reports.py --check
```

Discover and extract newly published official GN and Sonova materials:

```bash
python3 scripts/sync_gn_reports.py
python3 scripts/sync_sonova_reports.py
```

Use `--check` to scan the official indexes without downloading newly discovered
documents:

```bash
python3 scripts/sync_gn_reports.py --check
python3 scripts/sync_sonova_reports.py --check
```

Existing official URLs in each `sources/<company>/config.json` remain supported
as compatibility seeds.

## Refresh Extracts

Regenerate every Markdown extract after improving or upgrading the extractor:

```bash
python3 scripts/sync_amplifon_reports.py --refresh-extracts
python3 scripts/sync_gn_reports.py --refresh-extracts
python3 scripts/sync_sonova_reports.py --refresh-extracts
```

The refresh command re-downloads each official PDF temporarily and refuses to
continue if its size or SHA-256 differs from the recorded source metadata.

## Inventory And Dashboards

Inventory the source lake and update the company directory and report
dashboards:

```bash
python3 scripts/inventory_reports.py
```

The inventory command:

1. Includes only reports that pass the report-structure validator.
2. Matches source periods to published investor reports.
3. Extracts each report's header badge for its dashboard brief.
4. Regenerates `index.html`, every page in `companies/`, and
   `reports/inventory.json`.

## Generate Reports

Regenerate the standardized interim-period Amplifon reports:

```bash
python3 scripts/generate_amplifon_interim_reports.py
```

Regenerate the GN and Sonova investor reports:

```bash
python3 scripts/generate_gn_reports.py
python3 scripts/generate_sonova_reports.py
```

## Test

```bash
npm test
```

The test command runs Python unit tests, validates report structure, and checks
local dashboard, report, and source links.

For documentation-only link checks:

```bash
python3 scripts/validate_reports.py --links-only README.md AGENTS.md docs/*.md
```

## Run The Static Site

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000`.
