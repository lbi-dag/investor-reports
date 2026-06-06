---
name: read-between-financial-lines
description: Analyze official company financial reports, earnings releases, presentations, filings, and management commentary to produce a skeptical, evidence-based investor brief. Use when Codex needs to interpret corporate language, compare management framing with reported figures, identify risks hidden by adjusted metrics or selective comparisons, decode euphemisms, or turn source materials into a plain-English investor report.
---

# Read Between Financial Lines

Produce a fair but skeptical investor analysis from primary company materials. Treat management language as a claim to test, not as truth or deception by default.

## Workflow

1. Establish the assignment.
   - Identify company, reporting period, intended audience, requested output format, and investment horizon.
   - Prefer official filings, results releases, presentations, transcripts, and regulatory announcements.
   - State source gaps that prevent a reliable conclusion.

2. Build the factual baseline before interpreting.
   - Extract reported and adjusted revenue, growth, margins, profit, cash flow, debt, guidance, segment results, and capital allocation.
   - Record comparison periods, currencies, constant-currency claims, and management-defined measures.
   - Recalculate important changes when inputs are available.
   - Read [analysis-checklist.md](references/analysis-checklist.md) for the full review checklist.

3. Reconcile the story with the numbers.
   - Compare reported versus adjusted results.
   - Compare organic growth with acquisition-driven growth.
   - Compare profit with cash generation and cash generation with debt movement.
   - Compare group-level claims with weak segments or geographies.
   - Compare current guidance with prior targets and actual delivery.
   - Identify omitted context, changed definitions, selective time windows, and recurring "one-offs."

4. Decode corporate language.
   - Select only phrases whose framing materially affects investor understanding.
   - For each phrase, provide:
     - **Management phrase:** exact short quote or faithful paraphrase.
     - **Plain English:** the most defensible interpretation.
     - **Evidence:** figures or source passages supporting the interpretation.
     - **Confidence:** high, medium, or low.
   - Mention a plausible benign interpretation when evidence is ambiguous.

5. Form the investment view.
   - Separate durable strengths from temporary positives.
   - Separate operational problems from accounting presentation.
   - Present bull case, bear case, catalysts, and measurable items to watch.
   - Distinguish facts, calculations, management claims, and analyst inferences.

6. Deliver the requested artifact.
   - Default to a concise Markdown investor brief.
   - When creating a repository report, follow the repository's existing format unless the user requests a redesign.
   - Read [output-structure.md](references/output-structure.md) for the default brief and HTML-report guidance.

## Evidence Rules

- Cite every material factual claim with a page, section, document title, or URL.
- Use primary official sources for company-specific facts. Use secondary sources only for external context and label them.
- Never imply that adjusted metrics are inherently misleading; explain the adjustment and test whether it is economically meaningful or recurring.
- Never call language deceptive without strong evidence of contradiction or material omission.
- Do not invent motives, forecasts, peer comparisons, or valuation conclusions.
- Preserve units and distinguish reported, organic, constant-currency, and pro forma figures.
- Use exact dates and reporting periods.
- Mark unavailable information as unavailable rather than filling gaps.

## Analytical Tone

Write for an intelligent general investor. Be direct, specific, and independent. Avoid both management cheerleading and performative cynicism. Replace vague judgments with measurable evidence.

Use labels where ambiguity matters:

- **Fact:** directly stated in a source.
- **Calculation:** derived from disclosed figures; show the inputs.
- **Management claim:** management's characterization or outlook.
- **Inference:** evidence-based analyst interpretation.

## Quality Gate

Before finishing, verify:

- Every strong conclusion has supporting evidence.
- Reported and adjusted figures are not conflated.
- Positive and negative evidence both appear.
- The decoded-language section adds insight rather than merely sounding sarcastic.
- The watchlist contains measurable future outcomes.
- Sources and limitations are visible to the reader.
