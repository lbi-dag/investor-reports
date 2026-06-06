# Investor Reports

Static investor briefs generated from official company financial materials.

The project focuses on reading beyond management's headline narrative:
reconciling reported and adjusted figures, identifying selective comparisons,
and translating material corporate language into evidence-based plain English.

## Market Reality Dashboard

The repository features a [Market Reality Dashboard](index.html) that tracks the gap between corporate narratives and financial reality. It provides real-time statistics on report coverage and surface-extracts key AI verdicts.

## Repository Structure

- `index.html`: Market Reality Dashboard and report-library landing page.
- `reports/`: Published investor briefs and reporting inventory.
- `sources/amplifon/`: Amplifon source manifest, generated index, and page-marked Markdown extracts.
- `scripts/sync_amplifon_reports.py`: Source discovery, validation, extraction, and indexing pipeline.
- `scripts/inventory_reports.py`: Batch analysis inventory and dashboard generator.
- `scripts/extract_pdf_markdown.mjs`: PDF.js-based page-aware text extractor.
- `.agents/skills/read-between-financial-lines/`: Reusable financial-analysis skill.
- `.github/workflows/sync-amplifon-reports.yml`: Twice-monthly source sync.
- `ROADMAP.md`: Strategic direction and upcoming features.
- `AGENTS.md`: Canonical instructions for AI agents (Gemini, Claude, Copilot).

## Source Storage

Official PDFs are not committed to Git. The sync pipeline:

1. Discovers official financial reports and results presentations.
2. Skips URLs and report-period/type combinations already in `reports.json`.
3. Downloads new PDFs temporarily.
4. Validates the PDF signature, file size, and SHA-256 checksum.
5. Extracts page-marked Markdown with source provenance.
6. Discards the temporary PDF.
7. Updates `reports.json` and regenerates `INDEX.md`.

Each Markdown extract includes:

- Official PDF URL
- Reporting period and document type
- Download date
- Original PDF size and SHA-256
- Extractor version
- `<!-- page: N -->` markers for citations

See [sources/amplifon/INDEX.md](sources/amplifon/INDEX.md) for the current source
collection and official download links.

Text extraction does not perfectly preserve complex tables, charts, or visual
layout. Use the official PDF URL when those details materially affect analysis.

## Setup

Requirements:

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

Check whether new reports exist without downloading them:

```bash
python3 scripts/sync_amplifon_reports.py --check
```

## Batch Analysis & Dashboard

Inventory the entire data lake and update the Market Reality Dashboard:

```bash
python3 scripts/inventory_reports.py
```

Regenerate every Markdown extract after improving or upgrading the extractor:

```bash
python3 scripts/sync_amplifon_reports.py --refresh-extracts
```

The refresh command re-downloads each official PDF temporarily and refuses to
continue if its size or SHA-256 differs from the recorded source metadata.

## Scheduled Sync

GitHub Actions runs the sync at **08:17 UTC on the 1st and 15th of each month**.
It can also be started manually with the **Sync Amplifon reports** workflow.

When new materials are found, the workflow opens or updates the
`automation/sync-amplifon-reports` pull request. The repository's Actions
settings must allow GitHub Actions to create and approve pull requests.

## Create An Investor Brief

Invoke `$read-between-financial-lines` and provide the relevant official
materials, extracted source files, or URLs.

The skill requires:

- A factual baseline before interpretation
- Reconciliation of management framing with disclosed figures
- Clear separation of facts, calculations, management claims, and inferences
- Visible source citations and confidence levels
- Balanced bull and bear cases with measurable items to watch

## Test

```bash
npm test
```

## Run The Static Site

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000`.
