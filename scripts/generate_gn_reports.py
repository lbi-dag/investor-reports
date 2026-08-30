#!/usr/bin/env python3
from html import escape
from pathlib import Path


REPORTS_DIR = Path("reports")
ANALYSIS_DATE = "2026-06-06"
SKILL_VERSION = "1.1.0"
MODEL_VERSION = "OpenAI GPT-5.5"

SOURCES = {
    "annual": ("2025-fy/annual-report.md", "GN Annual Report 2025", "3deac8acec8e35cbd49fca178e9e21cff5a200801af61a5f18d87f789200e555"),
    "q1": ("2026-q1/interim-report.md", "GN Interim Report Q1 2026", "3e94e922dcec3e679621d07f7a92b194eba38969c20c4a5147bfa3d293be0a84"),
    "q1-presentation": ("2026-q1/conference-call-presentation.md", "GN Q1 2026 Conference Call Presentation", "5520895639af4f618d355c27576ff18b76e9761d1a0367f8a9d2a0bad41372b1"),
    "h1": ("2026-h1/conference-call-presentation.md", "GN Q2 2026 Conference Call Presentation", "fad18b263ebfa5fbc557eeacea0e8db51e3f635d1b57223301a75b3702435cdb"),
}

REPORTS = [
    {
        "slug": "2025",
        "period": "FY 2025",
        "ended": "December 31, 2025",
        "badge": "Debt improves, but earnings retreat",
        "verdict": "GN generated slightly more free cash flow and reduced net debt, but the operating recovery remained incomplete: reported revenue fell 7%, EBITA fell 11%, net profit fell 33%, and leverage stayed at 3.8x as Enterprise and Gaming weakness outweighed Hearing growth.",
        "consistency": "Medium-low: GN delivered its adjusted organic-growth and EBITA-margin guidance, but only after excluding the wind-down effect, while reported revenue, EBITA, profit, and share price all declined.",
        "consistency_ref": ("annual", "22-28"),
        "kpis": [("DKK 16.8B", "Revenue", "-7% YoY"), ("-4%", "Reported organic growth", "-1% excl. wind-down"), ("11.4%", "EBITA margin", "-60 bps YoY"), ("DKK 8.9B", "Net debt", "-DKK 823M YoY")],
        "working": [
            ("Hearing delivered 5% organic growth on top of 10% in 2024 and 13% in 2023, continuing to gain market share.", "annual", "25"),
            ("Gaming's divisional margin improved to 11.6% from 2.4%, helped by the product-line wind-down, pricing, supply-chain integration, and cost reductions.", "annual", "27"),
            ("Free cash flow excluding M&A increased to DKK 1,112 million and net interest-bearing debt fell by DKK 823 million to DKK 8,876 million.", "annual", "22, 24"),
        ],
        "obscured": [
            ("GN emphasized -1% organic growth excluding the Elite and Talk wind-down, while reported organic growth was -4% and total revenue fell 7%.", "annual", "23"),
            ("EBITA fell 11% to DKK 1,908 million and net profit fell 33% to DKK 710 million; higher net financial costs absorbed more of the operating result.", "annual", "22, 24"),
            ("Debt declined, but leverage remained unchanged at 3.8x because earnings also weakened. GN paused dividends and buybacks until leverage moves closer to 2.0x.", "annual", "22, 31"),
            ("Enterprise organic revenue fell 6% and divisional profit fell 13%; management's resilience framing did not prevent negative operating leverage.", "annual", "26"),
        ],
        "decoded": [
            ("“Solid financial performance in a challenging year”", "Cash flow and debt moved in the right direction, but revenue, EBITA, net profit, EPS, and market capitalization all declined.", "High", "annual", "22-24"),
            ("Organic growth was “in line with financial guidance”", "That statement uses -1% growth excluding the wind-down; reported organic growth was -4%.", "High", "annual", "23"),
            ("Enterprise “demonstrated continued resilience”", "The business protected gross margin and market share, but organic revenue fell 6% and divisional profit fell 13%.", "High", "annual", "26"),
        ],
        "bull": "Hearing momentum persists, Enterprise product launches restore growth, Gaming retains its improved margin structure, and cash generation finally reduces leverage.",
        "bear": "Enterprise and Gaming remain structurally weak, Hearing growth cannot offset them, and high financing costs keep profit and leverage under pressure.",
        "watch": "Organic growth by division; Enterprise Evolve3 sell-through; EBITA margin; net financial costs; free cash flow; leverage versus the 2.0x target.",
        "sources": ["annual"],
    },
    {
        "slug": "2026-q1",
        "period": "Q1 2026",
        "ended": "March 31, 2026",
        "badge": "Best asset surges as remaining business stalls",
        "verdict": "GN's Hearing division delivered 9% organic growth and a 17.1% adjusted EBITA margin just as GN agreed to sell it, while continuing Enterprise and Gaming operations shrank 4% organically and their adjusted EBITA margin collapsed to 0.3%; the transaction can repair the balance sheet, but leaves a much weaker operating base.",
        "consistency": "Low: the pre-transaction 2026 group guidance became obsolete, Enterprise guidance was reduced from 0%-6% to -3%-3%, and the continuing business now depends on cost actions to reach a sustainable margin.",
        "consistency_ref": ("annual", "28"),
        "kpis": [("DKK 2.10B", "Continuing revenue", "-8% YoY"), ("-4%", "Continuing organic growth", "Enterprise -5%; Gaming -1%"), ("0.3%", "Continuing adj. EBITA margin", "Down from 5.7%"), ("DKK 300M", "Hearing adj. EBITA", "+75% YoY")],
        "working": [
            ("Hearing organic revenue grew 9% and adjusted EBITA rose to DKK 300 million from DKK 171 million, producing a 17.1% adjusted margin.", "q1", "3-5"),
            ("Free cash flow excluding M&A improved to DKK -45 million from DKK -395 million, helped by working-capital management.", "q1", "2-3, 7"),
            ("Net interest-bearing debt fell to DKK 8,914 million from DKK 10,145 million and adjusted leverage improved to 3.8x from 4.4x.", "q1", "5, 7"),
            ("The DKK 17.0 billion Hearing transaction is expected to reduce short-term leverage to 1.0x-1.5x if it closes.", "q1", "4"),
        ],
        "obscured": [
            ("Continuing operations revenue fell 8%, organic revenue fell 4%, and adjusted EBITA fell 95% to DKK 6 million.", "q1", "3, 5-6"),
            ("Enterprise gross margin fell 220 basis points and divisional margin fell 420 basis points; Gaming gross margin fell 280 basis points.", "q1", "3"),
            ("GN recorded DKK 1,311 million of Q1 one-off costs across continuing and discontinued operations, driving a DKK 946 million group loss.", "q1", "3, 5"),
            ("The separation and right-sizing plan requires around DKK 750 million of cash one-off costs across 2026-2027, while planned savings initially offset roughly DKK 200 million of stranded costs.", "q1", "4, 7-8"),
        ],
        "decoded": [
            ("“Executing well on our priorities”", "Hearing and product launches showed progress, but continuing adjusted EBITA was almost eliminated and Enterprise guidance was cut.", "High", "q1", "7-8"),
            ("Enterprise margin effects are “temporary by nature”", "Tariffs, an inventory provision, and launch investments may reverse, but they contributed to a 420-basis-point divisional-margin decline in Q1.", "Medium", "q1-presentation", "6"),
            ("The transaction will “drive shareholder value”", "The sale can transform leverage, but GN is disposing of the division currently producing nearly all adjusted EBITA and intends to resume buybacks after closing.", "High", "q1", "4-5"),
        ],
        "bull": "The Hearing sale closes on time, debt falls sharply, Evolve3 converts launch interest into growth, and cost actions lift the remaining business toward a 10%-11% underlying EBITA margin.",
        "bear": "The transaction is delayed, EMEA weakness persists, Enterprise and Gaming fail to replace sold earnings, and carve-out costs or stranded costs exceed current estimates.",
        "watch": "Hearing-sale approvals and closing; Enterprise growth versus revised -3%-3% guidance; continuing adjusted EBITA margin versus 8%-9%; DKK 750 million cash-cost budget; post-close leverage and buybacks.",
        "sources": ["q1", "q1-presentation", "annual"],
    },
    {
        "slug": "2026-h1",
        "period": "H1 2026",
        "ended": "June 30, 2026",
        "badge": "Margin recovery needs a very strong second half",
        "analysis_date": "2026-08-30",
        "verdict": "GN's remaining Enterprise and Gaming operations improved gross margins in Q2, led by Gaming, but H1 organic revenue was still down 4%, Q2 adjusted EBITA margin was only 5.1%, free cash flow turned sharply negative, and the increased margin target now depends on a 4%-9% organic-growth second half while Hearing is being sold.",
        "consistency": "Low: after cutting the continuing-operations revenue outlook in Q1, GN cut it again at H1 while raising the margin target. The new target assumes a sharp H2 inflection from negative first-half organic growth, tariff refunds, seasonality, and cost actions rather than delivery already visible in the H1 result.",
        "consistency_ref": ("h1", "15-16"),
        "kpis": [("-4%", "H1 organic growth", "Continuing operations"), ("DKK 2.17B", "Q2 revenue", "-6% reported YoY"), ("5.1%", "Q2 adj. EBITA margin", "Down from 7.1%"), ("DKK -616M", "Q2 FCF ex M&A", "Working-capital and carve-out use")],
        "working": [
            ("Gaming delivered 5% organic revenue growth in Q2, with gross margin rising 520 basis points and adjusted divisional profit margin rising 280 basis points as Nova Pro Omni supported market-share gains.", "h1", "11"),
            ("Enterprise gross margin improved 110 basis points in Q2 through pricing discipline, lower tariffs, and FX despite a 7% organic revenue decline.", "h1", "8"),
            ("The Hearing carve-out remains expected to close toward year-end, with planned 2027 structural savings of around DKK 200 million intended to offset stranded costs.", "h1", "4"),
        ],
        "obscured": [
            ("Continuing operations recorded -4% organic growth in H1. Q2 revenue fell 6% reported and adjusted EBITA margin was 5.1%, after Q1's 0.3% margin.", "h1", "14, 16"),
            ("GN reduced 2026 continuing-operations organic-growth guidance to 0%-3% from 0%-6%, while increasing the adjusted EBITA-margin target to 9%-10%; the implied H2 organic-growth range is 4%-9%.", "h1", "15-16"),
            ("Q2 free cash flow excluding M&A was negative DKK 616 million because of temporary working-capital build, supply-chain insourcing, and Hearing-carve-out costs; net interest-bearing debt was still DKK 9.6 billion.", "h1", "14"),
            ("The sale plan also carries around DKK 750 million of cash costs across 2026-27, approximately 75% expected in 2026, alongside one-off transaction, carve-out, right-sizing, and impairment costs.", "h1", "4, 19"),
        ],
        "decoded": [
            ("“Steady progress”", "Q2 gross-margin trends improved, but revenue remained negative, free cash flow was sharply negative, and delivery of the revised target rests on a much stronger H2.", "High", "h1", "14-16"),
            ("Evolve3 success is “boding well for strong H2 2026”", "Premium headset sell-out is encouraging, but the full benefit depends on September launches, gradual rollout, and an improvement in pressured EMEA demand.", "Medium", "h1", "7-10"),
        ],
        "bull": "Evolve3 launches and Gaming market-share gains return the continuing business to growth in Q3, tariff refunds and operating leverage lift margins, and the Hearing sale closes on schedule with cost actions containing stranded costs.",
        "bear": "EMEA remains weak, new product launches fail to convert sell-out into revenue, working-capital and carve-out costs persist, and the required H2 growth and margin inflection does not occur before GN loses Hearing's earnings contribution.",
        "watch": "Quarterly Enterprise and Gaming organic growth; Evolve3 sell-in and EMEA demand; Q3 free-cash-flow normalization; progress against the DKK 750 million cash-cost budget; Hearing closing and post-close leverage; delivery of 0%-3% growth and 9%-10% adjusted EBITA margin.",
        "sources": ["h1", "q1"],
        "source_caveat": "The H1 interim financial report was not yet in the source lake when this brief was prepared. H1 conclusions use GN's Q2 conference-call presentation and the Q1 interim report; verify detailed financial-statement disclosures against the official H1 filing when it is available.",
    },
]

STYLE = """
*{box-sizing:border-box}body{margin:0;background:#f4f4f6;color:#1f2937;font:13px Arial,sans-serif}a{color:#164e63}.back{display:block;max-width:960px;margin:16px auto 0;padding:0 8px;text-decoration:none}.page{max-width:960px;margin:12px auto 24px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px #0002}.header{background:linear-gradient(135deg,#253746,#0f172a);color:#fff;padding:26px 32px;display:flex;justify-content:space-between;gap:20px}.header h1{margin:0;font-size:24px}.header p{margin:5px 0}.meta{text-align:right;line-height:1.7;font-size:11px}.badge{display:inline-block;padding:3px 10px;border:1px solid #ffffff66;border-radius:20px}.verdict,.consistency{padding:13px 22px;line-height:1.6}.verdict{background:#fff8e1;border-left:5px solid #f59e0b}.consistency{background:#f8fafc;border-left:5px solid #64748b}.kpis{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #e5e7eb}.kpi{text-align:center;padding:16px 10px;border-right:1px solid #e5e7eb}.kpi:last-child{border:0}.value{font-size:20px;font-weight:700;color:#164e63}.label{font-size:10px;text-transform:uppercase;color:#6b7280}.change{margin-top:4px;font-size:11px}.content{padding:22px 26px 8px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}section{margin-bottom:22px}h2{font-size:13px;text-transform:uppercase;color:#164e63;border-bottom:2px solid #cffafe;padding-bottom:5px}.item{line-height:1.55;margin:0 0 11px}.cite{font-size:10.5px;color:#6b7280}.decode,.outlook{padding:10px 12px;margin-bottom:8px;background:#fafafa;border-left:3px solid #d1d5db}.claim{font-style:italic;color:#6b7280}.plain{margin-top:5px;line-height:1.5}.confidence{margin-top:5px;font-size:10px;color:#6b7280}.sources{padding:0 26px 22px;line-height:1.7}.footer{display:flex;justify-content:space-between;background:#1a1a2e;color:#9ca3af;padding:11px 24px;font-size:10.5px}.metadata{padding:12px 24px;background:#f9fafb;color:#6b7280;font-size:10px;line-height:1.6}@media(max-width:720px){.header,.footer{display:block}.meta{text-align:left;margin-top:12px}.kpis,.grid{grid-template-columns:1fr 1fr}.content{padding:18px 16px}.sources{padding:0 16px 18px}}@media(max-width:440px){.kpis,.grid{grid-template-columns:1fr}}
"""


def citation(source_key, pages):
    path, title, _ = SOURCES[source_key]
    return f'<a class="cite" href="../sources/gn/{path}">{escape(title)} pp. {escape(pages)}</a>'


def cited_items(items):
    return "\n".join(
        f'<p class="item"><strong>{escape(text)}</strong> {citation(source, pages)}</p>'
        for text, source, pages in items
    )


def render(report):
    kpis = "".join(
        f'<div class="kpi"><div class="value">{escape(value)}</div><div class="label">{escape(label)}</div><div class="change">{escape(change)}</div></div>'
        for value, label, change in report["kpis"]
    )
    decoded = "".join(
        f'<div class="decode"><div class="claim">{escape(claim)}</div><div class="plain">{escape(plain)}</div>'
        f'<div class="confidence">Confidence: {escape(confidence)} · {citation(source, pages)}</div></div>'
        for claim, plain, confidence, source, pages in report["decoded"]
    )
    source_items = "".join(
        f'<li><a href="../sources/gn/{SOURCES[key][0]}">{escape(SOURCES[key][1])}</a></li>'
        for key in report["sources"]
    )
    source_hashes = "; ".join(SOURCES[key][2] for key in report["sources"])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GN Group {escape(report["period"])} Investor Report</title><style>{STYLE}</style></head><body>
<a class="back" href="../companies/gn.html">Back to GN reports</a><main class="page">
<header class="header"><div><h1>GN Store Nord A/S - {escape(report["period"])} Results</h1><p>Independent, evidence-based investor summary</p></div>
<div class="meta">Ticker: GN.CO · Nasdaq Copenhagen<br>Period ended {escape(report["ended"])}<br><span class="badge">{escape(report["badge"])}</span></div></header>
<div class="verdict"><strong>One-line verdict:</strong> {escape(report["verdict"])}</div>
<div class="consistency"><strong>Historical Consistency Assessment:</strong> {escape(report["consistency"])}</div>
<div class="kpis">{kpis}</div><div class="content"><div class="grid"><div>
<section><h2>What Is Genuinely Working</h2>{cited_items(report["working"])}</section>
<section><h2>Track Record And Consistency</h2><p class="item">{escape(report["consistency"])} {citation(*report["consistency_ref"])} {citation("q1", "8") if report["slug"] == "2026-q1" else ""}</p></section>
</div><div><section><h2>What The Headline Obscures</h2>{cited_items(report["obscured"])}</section>
<section><h2>Corporate Language, Decoded</h2>{decoded}</section></div></div>
<section><h2>What To Watch Next</h2><div class="outlook"><p><strong>Bull case:</strong> {escape(report["bull"])}</p>
<p><strong>Bear case:</strong> {escape(report["bear"])}</p><p><strong>Measurable watchlist:</strong> {escape(report["watch"])}</p></div></section></div>
<section class="sources"><h2>Sources And Caveats</h2><ul>{source_items}
<li><a href="../sources/gn/INDEX.md">GN official source index</a></li>
<li>{escape(report.get("source_caveat", "Source Markdown is extracted from the official PDF; complex tables and visual layouts should be checked against the official PDF."))}</li>
<li>Comparisons use management-defined measures where stated and do not constitute investment advice.</li></ul></section>
<footer class="footer"><span>GN Store Nord A/S · {escape(report["period"])} · Independent analysis</span><span>Not investment advice · Verify primary sources</span></footer>
<div class="metadata"><div>Analysis Date: {report.get("analysis_date", ANALYSIS_DATE)}</div><div>Skill Version: {SKILL_VERSION}</div><div>Model Version: {MODEL_VERSION}</div><div>Source SHA-256: {source_hashes}</div></div>
</main></body></html>
"""


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    for report in REPORTS:
        path = REPORTS_DIR / f'gn-{report["slug"]}.html'
        path.write_text(render(report), encoding="utf-8")
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
