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

# Force refresh all extracted Markdown from original PDFs
python3 scripts/sync_amplifon_reports.py --refresh-extracts
```

### Testing
```bash
# Run Python unit tests
npm test
# Or directly:
python3 -m unittest discover -s tests -v
```

### Local Preview
```bash
# Serve the static landing page and reports
python3 -m http.server 8000
```

## Development Conventions

### Source Management
- **PDFs are ephemeral**: The sync script downloads PDFs, validates them (SHA-256), extracts text, and deletes the PDF. DO NOT commit PDFs to the repository.
- **Extraction Format**: Extracted Markdown files include metadata headers and `<!-- page: N -->` markers. These must be preserved as they are used for citations.
- **Directory Structure**: Sources are organized by company and period, e.g., `sources/amplifon/2026-q1/financial-report.md`.

### Analysis Workflow
- Use the `read-between-financial-lines` skill for generating briefs.
- **Evidence-First**: Every factual claim must be cited with page numbers or document titles.
- **Fact vs. Claim**: Explicitly distinguish between reported facts, calculations, management claims, and analyst inferences.
- **Reconciliation**: Always compare "Adjusted" metrics against their "Reported" GAAP/IFRS counterparts.

## Specialized Skills

- **`read-between-financial-lines`**: Activated via `activate_skill`. It provides a rigorous framework for financial analysis, focusing on skepticism, evidence-based interpretation, and decoding corporate euphemisms.

## Repository Structure

- `index.html`: Landing page for the reports.
- `sources/`: Data lake of extracted financial materials.
- `reports/`: Human/AI-written investor briefs.
- `scripts/`:
    - `sync_amplifon_reports.py`: The primary automation script.
    - `extract_pdf_markdown.mjs`: The text extraction engine.
- `.github/workflows/`: Automation for bi-monthly syncs and PR generation.
