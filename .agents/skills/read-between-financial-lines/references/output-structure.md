# Output Structure

## Default Investor Brief

Use this structure unless the user requests another format:

1. **Scope and sources**
   - Company, period, documents reviewed, and limitations.

2. **One-line verdict**
   - Balanced summary of operating direction, financial condition, and main uncertainty.

3. **Historical consistency score**
   - **High/Medium/Low**: Based on metric stability, restatement frequency, and guidance delivery.

4. **Key numbers**
   - Compact table with reported value, comparison, and why it matters.

5. **What is genuinely working**
   - Durable strengths supported by evidence.

6. **What the headline obscures**
   - Weaknesses, adjustment gaps, cash/debt tensions, segment problems, or changed framing.

7. **Track record and consistency**
   - Reconciliation of current performance against prior-period guidance.
   - Identification of restated figures or dropped KPIs.

8. **Corporate language, decoded**
   - Management phrase, plain English, evidence, confidence, and benign alternative when relevant.

9. **Bull case and bear case**
   - Conditions rather than unsupported predictions.

10. **What to watch**
   - Measurable outcomes for the next reporting periods.

11. **Sources and caveats**
   - Primary-source citations and unresolved questions.

## Writing Decoded Language

Prefer:

> **Management phrase:** "Significant improvement in H2 organic growth."
> **Plain English:** H2 improved relative to a weak H1, but full-year organic growth remained 0.0%.
> **Evidence:** FY results release, p. 3; H1 results release, p. 2.
> **Confidence:** High.

Avoid unsupported snark:

> Results were bad and management wants to hide it.

## HTML Reports

When producing an HTML report:

- **Metadata Header (Mandatory)**: Include a hidden or footer section with:
    - `Analysis Date`: ISO 8601 date of report generation.
    - `Skill Version`: The version of the `read-between-financial-lines` skill used.
    - `Model Version`: The LLM model name used (e.g., Gemini 1.5 Pro).
    - `Source SHA-256`: The checksums of the primary documents analyzed.
- Preserve the repository's visual conventions where practical.
- Include visible source citations or source links.
- Use semantic headings, tables, and navigation.
- Add mobile breakpoints for multi-column layouts and wide tables.
- Keep conclusions readable without relying only on color or icons.
- Include an informational-purpose disclaimer without using it as a substitute for careful sourcing.
