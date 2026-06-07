# Investor Reports - Project Context

This repository is a framework for syncing, extracting, and analyzing official corporate financial reports to generate evidence-based investor briefs. It focuses on reconciling management narratives with reported figures and decoding corporate language.

## Project Overview

- **Core Purpose**: Automate the collection of financial reports (PDFs) and provide a structured environment for AI-assisted financial analysis.
- **Main Technologies**: 
    - **Python 3.12+**: Orchestrates the sync pipeline, validation, and indexing.
    - **Node.js 22+**: Handles PDF text extraction via PDF.js.
    - **Markdown**: Used for extracted source data and generated reports.
    - **HTML/CSS**: Simple landing page for the report library.
- **Architecture**:
    - `scripts/`: Python and Node.js logic for data processing.
    - `sources/`: Structured directory containing extracted Markdown files, metadata (`reports.json`), and an index (`INDEX.md`).
    - `reports/`: The final destination for analyzed briefs.
    - `.agents/skills/`: Specialized instructions for financial analysis.

## Key Commands

### Environment Setup
```bash
# Install Node.js dependencies for PDF extraction
npm ci
```

### Data Pipeline
```bash
# Discover and extract new reports (Amplifon)
python3 scripts/sync_amplifon_reports.py

# Check for new reports without downloading
python3 scripts/sync_amplifon_reports.py --check

# Discover and extract new GN reports
python3 scripts/sync_gn_reports.py

# Discover and extract new Sonova reports
python3 scripts/sync_sonova_reports.py

# Inventory all sources and update company/report dashboards
python3 scripts/inventory_reports.py

# Force refresh all extracted Markdown from original PDFs
python3 scripts/sync_amplifon_reports.py --refresh-extracts
python3 scripts/sync_gn_reports.py --refresh-extracts
python3 scripts/sync_sonova_reports.py --refresh-extracts
```
...
## Repository Structure

- `index.html`: Company-directory landing page.
- `companies/`: Company-level report-history dashboards.
- `sources/`: Data lake of extracted financial materials.
- `reports/`: Human/AI-written investor briefs.
- `ROADMAP.md`: Future development plans.
- `scripts/`:
    - `sync_amplifon_reports.py`: Amplifon source automation.
    - `sync_gn_reports.py`: GN source automation.
    - `sync_sonova_reports.py`: Sonova source automation.
    - `inventory_reports.py`: Batch analysis inventory and dashboard updater.
    - `extract_pdf_markdown.mjs`: The text extraction engine.
- `.github/workflows/`: Automation for bi-monthly syncs and PR generation.

## Scheduled Sync Behavior

- Amplifon, GN, and Sonova automatically discover supported files from their
  official investor indexes.
- Existing official URLs in company `config.json` files remain supported as
  compatibility seeds.
- Workflows run on the 1st and 15th of each month UTC and can be triggered
  manually:
    - Amplifon: `17 8 1,15 * *`, runs unit tests, then
      `python3 scripts/sync_amplifon_reports.py`, and opens
      `automation/sync-amplifon-reports` when files change.
    - GN: `47 8 1,15 * *`, runs `npm test`, then
      `python3 scripts/sync_gn_reports.py`, and opens
      `automation/sync-gn-reports` when files change.
    - Sonova: `27 9 1,15 * *`, runs `npm test`, then
      `python3 scripts/sync_sonova_reports.py`, and opens
      `automation/sync-sonova-reports` when files change.
- Scheduled syncs download new PDFs temporarily, validate PDF signature and
  size, record SHA-256 checksums, extract page-marked Markdown, update
  `reports.json`, regenerate `INDEX.md`, and skip duplicate URLs,
  duplicate period/type combinations, unrelated materials, sustainability-only
  documents, and replacement candidates.
