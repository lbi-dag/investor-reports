# Scheduled Source Syncs

GitHub Actions runs separate source-sync workflows for Amplifon, GN, and
Sonova. Each workflow runs on the 10th and 25th of every month, uses UTC cron
times, and supports manual execution through `workflow_dispatch`.

## Workflow Schedule

| Company | Schedule | Validation step | Sync command | Automation branch |
| --- | --- | --- | --- | --- |
| Amplifon | `17 8 10,25 * *` | `python3 -m unittest discover -s tests -v` | `python3 scripts/sync_amplifon_reports.py` | `automation/sync-amplifon-reports` |
| GN | `47 8 10,25 * *` | `npm test` | `python3 scripts/sync_gn_reports.py` | `automation/sync-gn-reports` |
| Sonova | `27 9 10,25 * *` | `npm test` | `python3 scripts/sync_sonova_reports.py` | `automation/sync-sonova-reports` |

The workflow definitions are:

- [sync-amplifon-reports.yml](../.github/workflows/sync-amplifon-reports.yml)
- [sync-gn-reports.yml](../.github/workflows/sync-gn-reports.yml)
- [sync-sonova-reports.yml](../.github/workflows/sync-sonova-reports.yml)

## Tasks Performed

Each scheduled job:

1. Checks out the repository and sets up Python 3.12.
2. Runs `npm ci` so the pinned PDF extraction dependency is available.
3. Runs the workflow's validation step.
4. Scans official company sources and classifies supported documents.
5. Skips already-recorded URLs, duplicate period/type combinations, unrelated
   materials, sustainability-only documents, and replacement candidates.
6. Downloads new PDFs temporarily and validates their PDF signature and size.
7. Records PDF size and SHA-256 checksum metadata.
8. Extracts page-marked Markdown and discards the temporary PDF.
9. Updates the company `reports.json` manifest and generated `INDEX.md`.
10. Opens or updates the company-specific automation pull request when files
    changed.

If no tracked files change, `peter-evans/create-pull-request` does not open a
new pull request.

## Company Discovery Rules

### Amplifon

Amplifon scans its official financial-report and presentation indexes. It
accepts annual and interim financial reports plus supported results
presentations.

### GN

GN scans its official download-center endpoint. It accepts annual reports,
interim Q1/Q2/Q3 reports, and their associated conference-call results
presentations.

GN maps its reporting cadence as follows:

- Q1 to `q1`
- Q2 to `h1`
- Q3 to `9m`
- Annual report to `fy`

### Sonova

Sonova scans its official financial-report and investor-presentation indexes.
It accepts annual reports, half-year reports, results releases, and results
presentations.

Sonova fiscal years use the ending year for local periods. For example,
fiscal year `2025/26` maps to `2026-fy`.

## Safety And Compatibility

- Only official company domains and configured PDF paths are accepted.
- Existing official URLs in company `config.json` files remain supported as
  compatibility seeds.
- Existing source URLs and period/type combinations are not downloaded again.
- A newly discovered URL for an existing period/type combination is treated as
  a replacement candidate and skipped without overwriting the existing source.
- PDF binaries are temporary and are not committed to Git.

The repository's Actions settings must allow GitHub Actions to create pull
requests.
