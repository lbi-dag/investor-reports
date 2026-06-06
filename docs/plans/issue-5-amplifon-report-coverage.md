# Issue #5 Plan: Complete Amplifon Report Coverage

## Objective

Produce a consistent, sourced HTML investor report for every available Amplifon
reporting period from 2024 onward, then make coverage and report quality
verifiable by automation.

Issue: https://github.com/lbi-dag/investor-reports/issues/5

## Current Coverage

| Period | Official source extracts | HTML report | Required comparison context |
| --- | ---: | --- | --- |
| 2024 Q1 | 1 | Present | No earlier repository source; state the limitation |
| 2024 H1 | 1 | Present | 2024 Q1 |
| 2024 9M | 1 | Present | 2024 H1 and 2024 Q1 |
| 2024 FY | 1 | Present | 2024 H1 |
| 2025 Q1 | 1 | Present | 2024 Q1 and 2024 FY |
| 2025 H1 | 1 | Present | 2024 H1, 2025 Q1, and 2024 FY |
| 2025 9M | 1 | Present | 2024 9M, 2025 H1, and 2024 FY |
| 2025 FY | 2 | Present | 2024 FY |
| 2026 Q1 | 2 | Present | 2025 Q1 and 2025 FY |

All nine available Amplifon periods have a validated HTML investor report.

## Delivery Strategy

### 1. Define and validate the report contract

- Treat the existing reports as the visual baseline, but define one explicit
  required structure for new reports.
- Require a one-line verdict, historical-consistency assessment, key figures,
  genuine strengths, obscured weaknesses, track record, decoded language, bull
  and bear cases, measurable watchlist, sources, caveats, and metadata.
- Require metadata for analysis date, skill version, model identity when known,
  and every primary source SHA-256.
- Add automated validation for required sections, metadata, source citations,
  report filenames, and local links.
- Extend inventory tests so a period is `PRESENT` only when its report passes
  the report contract, rather than merely when an HTML file exists.

### 2. Produce the 2024 sequence chronologically

- Generate Q1 first and explicitly document the lack of earlier repository
  context.
- Generate H1 using Q1 to test management's sequential framing.
- Generate 9M using Q1 and H1 to identify narrative changes and recurring
  adjustments.
- Revalidate the existing FY report against the completed 2024 sequence and
  correct any unsupported historical-consistency claims.

Chronological production matters because each completed report becomes
comparison context for the next period.

### 3. Produce the 2025 sequence chronologically

- Generate Q1 with both 2024 Q1 year-over-year context and 2024 FY guidance.
- Generate H1 with 2024 H1 year-over-year context and 2025 Q1 sequential
  context.
- Generate 9M with 2024 9M year-over-year context and 2025 H1 sequential
  context.
- Revalidate the existing FY 2025 and Q1 2026 reports after the missing
  comparison periods exist.

### 4. Regenerate indexes and verify completion

- Run `python3 scripts/inventory_reports.py`.
- Confirm every manifest period is marked `PRESENT`.
- Confirm dashboard rows link to the correct report.
- Confirm each dashboard brief matches the corresponding report header badge.
- Run the complete test suite.
- Run a local-link validator across `index.html` and every report.
- Manually inspect desktop and narrow-screen layouts for at least one quarterly,
  one interim, and one annual report.

## Delivered Dashboard Experience

- The Amplifon page features the latest analysis and shows coverage and source
  counts.
- Archive briefs come from each report's concise header badge rather than the
  longer one-line verdict.
- Reporting periods use investor-friendly labels such as `Q1 2026` and
  `FY 2025`.
- The desktop archive table becomes linked report cards on narrow screens.
- The generator applies the same company-page structure to covered and planned
  companies.

## Implementation Boundaries

- Keep analytical conclusions authored from the official source extracts; do
  not attempt to generate investor conclusions from regexes or templates.
- Automate the repeatable shell around analysis: report scaffolding, metadata,
  inventory, contract validation, and link validation.
- Use only primary Amplifon materials for company-specific facts. Label any
  external context separately.
- Preserve distinctions between reported, adjusted, organic, constant-currency,
  and pro forma figures.
- Do not claim a year-over-year or sequential comparison when definitions are
  incompatible.

## Proposed Commits

1. Add report-contract and local-link validation with tests.
2. Add 2024 Q1, H1, and 9M reports; reconcile the existing 2024 FY report.
3. Add 2025 Q1, H1, and 9M reports; reconcile existing later reports.
4. Regenerate inventory/dashboard and document final verification.

## Acceptance Checklist

- [x] Six missing HTML reports are added.
- [x] Every source period in `sources/amplifon/reports.json` maps to a valid
      report or a documented exception.
- [x] Every report follows the required structure and metadata contract.
- [x] Every material factual claim has a primary-source citation.
- [x] Relevant YoY and sequential comparisons reconcile metric definitions.
- [x] All report and source links resolve locally.
- [x] Dashboard and inventory show complete Amplifon coverage.
- [x] Automated tests pass.
- [ ] Representative responsive layouts are manually verified.

## Risks

- Interim extracts may omit details needed for a confident conclusion. Reports
  must state those limitations instead of filling gaps.
- Existing reports are not fully structurally consistent, so validation may
  expose follow-up corrections outside the six missing files.
- Six manually analyzed reports create review load. Keep each report focused on
  material changes and verify periods chronologically to reduce contradictions.
