# Investor Reports

Static investor briefs generated from official company financial materials.

The project focuses on reading beyond management's headline narrative:
reconciling reported and adjusted figures, identifying selective comparisons,
and translating material corporate language into evidence-based plain English.

## Company Directory And Report Dashboards

The root [company directory](index.html) lists covered and planned companies.
Each covered company has a report-history dashboard, such as
[Amplifon](companies/amplifon.html), with:

- Company identity, ticker, coverage start, and official-source count
- A featured link to the latest analysis
- Human-readable reporting periods and analysis status
- Short report briefs extracted from each report header badge
- A desktop report archive and responsive mobile report cards

The header badge is the report's concise archive summary. Keep it short,
specific, and distinct from the longer one-line verdict inside the report.

## Repository Structure

- `index.html`: Company-directory landing page.
- `companies/`: Company-level report-history dashboards.
- `reports/`: Published investor briefs and reporting inventory.
- `sources/amplifon/`, `sources/gn/`, `sources/sonova/`: Company source manifests, generated indexes, and page-marked Markdown extracts.
- `scripts/sync_amplifon_reports.py`: Amplifon source discovery, validation, extraction, and indexing pipeline.
- `scripts/sync_gn_reports.py`: Configured GN source validation, extraction, and indexing pipeline.
- `scripts/sync_sonova_reports.py`: Configured Sonova source validation, extraction, and indexing pipeline.
- `scripts/inventory_reports.py`: Batch analysis inventory and dashboard generator.
- `scripts/extract_pdf_markdown.mjs`: PDF.js-based page-aware text extractor.
- `.agents/skills/read-between-financial-lines/`: Reusable financial-analysis skill.
- `.agents/skills/add-new-company/`: Command workflow for discovering and adding company coverage.
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

See [sources/amplifon/INDEX.md](sources/amplifon/INDEX.md) and
[sources/gn/INDEX.md](sources/gn/INDEX.md) for the current source collections
and official download links.

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

Download and extract configured official GN materials:

```bash
python3 scripts/sync_gn_reports.py
python3 scripts/sync_sonova_reports.py
```

Add newly published GN documents to `sources/gn/config.json`, then use
`python3 scripts/sync_gn_reports.py --check` to confirm they are not yet in the
manifest.

## Batch Analysis & Dashboard

Inventory the entire data lake and update the company directory and report dashboards:

```bash
python3 scripts/inventory_reports.py
```

The inventory command:

1. Includes only reports that pass the report-structure validator.
2. Matches source periods to published investor reports.
3. Extracts each report's header badge for its dashboard brief.
4. Regenerates `index.html`, every page in `companies/`, and
   `reports/inventory.json`.

Regenerate the standardized interim-period Amplifon reports:

```bash
python3 scripts/generate_amplifon_interim_reports.py
```

Regenerate the GN FY 2025 and Q1 2026 investor reports:

```bash
python3 scripts/generate_gn_reports.py
python3 scripts/generate_sonova_reports.py
```

Regenerate every Markdown extract after improving or upgrading the extractor:

```bash
python3 scripts/sync_amplifon_reports.py --refresh-extracts
python3 scripts/sync_gn_reports.py --refresh-extracts
```

The refresh command re-downloads each official PDF temporarily and refuses to
continue if its size or SHA-256 differs from the recorded source metadata.

## Scheduled Sync

GitHub Actions runs the Amplifon and GN syncs twice monthly. They can also be
started manually with the **Sync Amplifon reports** and **Sync GN reports**
workflows.

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

## Add A New Company

Invoke `$add-new-company` with the company name. The command searches for and
qualifies the official investor-relations source, creates repeatable source and
report automation, and analyzes the latest two available reporting periods.

Private companies without public financial reports receive a documented source
discovery result instead of fabricated reports.

## Test

```bash
npm test
```

The test command validates report structure and all local dashboard, report,
and source links.

## Run The Static Site

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000`.
