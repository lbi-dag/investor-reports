---
name: add-new-company
description: Add a company to the investor-reports repository by finding its official investor-relations site, qualifying and downloading official financial materials, creating repeatable source-sync and report-generation automation, and analyzing the latest two reporting periods. Use when asked to add, onboard, cover, or start reports for a new company.
---

# Add New Company

Add company coverage end to end. Use `$read-between-financial-lines` for the
analysis stage.

## Workflow

1. **Establish company identity**
   - Confirm legal name, public/private status, ticker, exchange, official
     corporate site, and investor-relations site.
   - Search the web, then verify every selected source on an official company
     domain.

2. **Qualify official financial sources**
   - Prefer annual reports, interim/quarterly reports, results releases, and
     results presentations.
   - Select the latest two reporting periods with enough primary evidence for
     a defensible investor brief.
   - Do not substitute a foundation, subsidiary, similarly named company,
     third-party estimate, or press coverage for company financial reports.
   - Record the discovery outcome using
     [discovery-template.md](references/discovery-template.md).

3. **Handle companies without public reports**
   - If no official investor-relations page or financial reports exist, stop
     the source/report implementation.
   - Add `sources/<slug>/DISCOVERY.md` documenting searches, official evidence,
     source gaps, and why analysis is blocked.
   - Update the company-directory description to state that the company is
     private or that public financial reports are unavailable.
   - Never fabricate reports, metrics, sync scripts, or analysis.

4. **Create source automation**
   - Follow the established company sync patterns in `scripts/sync_*_reports.py`.
   - Store configuration, manifest, generated index, and page-marked extracts
     under `sources/<slug>/`.
   - Downloads must be temporary, PDF-signature checked, checksum recorded,
     extracted with `scripts/extract_pdf_markdown.mjs`, and validated.
   - Add focused tests and a twice-monthly GitHub Actions workflow.

5. **Analyze the latest two periods**
   - Read `$read-between-financial-lines`.
   - Create a reproducible `scripts/generate_<slug>_reports.py`.
   - Cite page-marked official extracts for every material claim.
   - Include report badge, verdict, historical consistency, KPIs, genuine
     strengths, obscured weaknesses, decoded language, bull/bear cases,
     measurable watchlist, sources, caveats, and metadata.

6. **Integrate and verify**
   - Add the company to source coverage only after a valid source manifest
     exists.
   - Run report generation, `python3 scripts/inventory_reports.py`,
     `npm test`, the company sync with `--check`, and `git diff --check`.
   - Report clearly when the workflow stops because public reports do not
     exist.

## Completion Standard

- Official source identity is proven.
- The latest two available periods are analyzed, or the absence of public
  financial reports is documented.
- Automation is repeatable and tested.
- Generated dashboards and all local links validate.
