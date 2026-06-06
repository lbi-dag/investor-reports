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

# Inventory all sources and update the Market Reality Dashboard
python3 scripts/inventory_reports.py

# Force refresh all extracted Markdown from original PDFs
python3 scripts/sync_amplifon_reports.py --refresh-extracts
```
...
## Repository Structure

- `index.html`: Market Reality Dashboard and report landing page.
- `sources/`: Data lake of extracted financial materials.
- `reports/`: Human/AI-written investor briefs.
- `ROADMAP.md`: Future development plans.
- `scripts/`:
    - `sync_amplifon_reports.py`: The primary automation script.
    - `inventory_reports.py`: Batch analysis inventory and dashboard updater.
    - `extract_pdf_markdown.mjs`: The text extraction engine.
- `.github/workflows/`: Automation for bi-monthly syncs and PR generation.
