# Investor Reports

Investor Reports is an evidence-first research system for turning official
company financial materials into skeptical, sourced investor briefs.

The project is built around a simple idea: management narratives should be
tested against reported figures, historical context, and source documents before
they become investor conclusions.

## What It Delivers

- **Company dashboards:** a reader-facing directory of covered companies,
  reporting periods, source coverage, and published analyses.
- **Evidence-backed investor briefs:** concise reports that separate facts,
  calculations, management claims, and analyst inferences.
- **Corporate-language decoding:** plain-English explanations of selective
  framing, adjusted metrics, omitted context, and recurring "one-off" items.
- **Primary-source traceability:** every analysis is grounded in official PDFs
  converted into page-marked Markdown for citation and review.
- **Automated source coverage:** scheduled workflows monitor official investor
  sources for newly published reports and propose updates through pull requests.

Explore the generated experience from the root [company directory](index.html)
or individual company dashboards such as [Amplifon](companies/amplifon.html),
[GN](companies/gn.html), and [Sonova](companies/sonova.html).

## AI Architecture

The repository is designed as a source-grounded AI analysis pipeline rather than
a free-form report generator.

1. **Official-source ingestion:** company sync scripts discover supported
   reports, validate PDFs, record checksums, and extract page-marked Markdown.
2. **Structured source lake:** `sources/` stores manifests, provenance metadata,
   generated indexes, and extracted text while keeping PDF binaries out of Git.
3. **Analysis skill layer:** `.agents/skills/read-between-financial-lines/`
   defines the reasoning workflow, evidence rules, quality gates, and output
   expectations for AI-assisted analysis.
4. **Historical context:** reports are expected to compare current results with
   prior periods, detect changed baselines, and test whether management's
   framing matches the disclosed numbers.
5. **Publishing layer:** generated HTML reports and company dashboards expose
   the analysis to readers without requiring them to inspect the source lake.

The result is a workflow where AI helps interpret financial communication, but
the repository keeps the system anchored to source provenance, reproducible
extracts, and explicit analytical constraints.

## Product Surface

The public-facing site is intentionally lightweight:

- `index.html` summarizes covered companies and their latest analysis.
- `companies/` provides company-level report histories and source coverage.
- `reports/` contains published investor briefs.
- `sources/` exposes the underlying extracted source materials for audit.

The reports are written for investors who want a second read on the official
story: what is genuinely improving, what the headline obscures, what language
needs decoding, and what measurable items should be watched next.

## Automation

GitHub Actions scans official Amplifon, GN, and Sonova investor sources on the
10th and 25th of each month. Supported new documents are validated, extracted,
indexed, and proposed through company-specific automation pull requests.

See [Scheduled Source Syncs](docs/scheduled-source-syncs.md) for the technical
workflow schedules, tasks, discovery rules, and safety behavior.

## Repository Map

- `.agents/skills/`: AI workflow instructions for source discovery and
  skeptical financial analysis.
- `.github/workflows/`: scheduled source-sync automation.
- `assets/`: company logos and static site assets.
- `companies/`: generated company dashboards.
- `docs/`: technical notes, workflow details, and implementation plans.
- `reports/`: published investor briefs and inventory metadata.
- `scripts/`: source sync, extraction, validation, inventory, and report
  generation tooling.
- `sources/`: official-source manifests, indexes, and extracted Markdown.

## Learn More

- [Developer Workflow](docs/developer-workflow.md): setup, local commands,
  validation, and static-site serving.
- [Scheduled Source Syncs](docs/scheduled-source-syncs.md): GitHub Actions
  cadence, discovery rules, and PR behavior.
- [Architecture](ARCHITECTURE.md): data flow from official-source discovery
  through extraction, analysis, validation, and publishing.
- [Roadmap](ROADMAP.md): planned improvements for analysis depth, dashboards,
  and investor engagement.
- [Agent Instructions](AGENTS.md): concise operating context for AI coding
  agents working in this repository.
