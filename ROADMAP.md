# Product Roadmap - Investor Reports

This roadmap outlines the strategic direction for the Investor Reports ecosystem, focusing on enhancing analytical depth, scaling report coverage, and improving investor engagement.

## Q3 2026: Foundation & Scaling

### 1. Multi-Period Contextual Intelligence
- **Goal**: Enable the analysis engine to compare current results against prior periods and historical management claims.
- **Key Actions**:
    - Update `read-between-financial-lines` skill to require prior-period reports as context.
    - Implement logic to detect "dropped" KPIs or restated baselines.
    - Add "Historical Consistency" score to reports.
- **Related Issues**: #8

### 2. Batch Analysis Pipeline & Metadata Tracking
- **Goal**: Automate report generation for all historical data in the `sources/` directory.
- **Key Actions**:
    - Create `scripts/inventory_reports.py` to process the entire data lake.
    - Add metadata fields to reports: analysis date, LLM model version, and extraction engine version.
    - Implement a "Stale Report" detection system to trigger re-analysis when skills or models are upgraded.
- **Related Issues**: #5, #4

### 3. "Market-Reality" Dashboard
- **Goal**: Transform the landing page into a high-signal investor dashboard.
- **Key Actions**:
    - Redesign `index.html` to show a summary table of latest verdicts.
    - Integrate a basic stock price lookup (via API or static sync) to show price reaction since report release.
    - Add visual indicators (e.g., "Narrative/Price Divergence" badges).
- **Related Issues**: #10, #7

## Future Directions
- **Peer Comparison Engine**: Automated reconciliation against competitor filings (e.g., Amplifon vs. Sonova).
- **Audio Transcript Analysis**: Extending the pipeline to earnings call transcripts to detect vocal sentiment shifts.
- **Interactive Citations**: Hover-over citations that reveal the exact source Markdown snippet.
