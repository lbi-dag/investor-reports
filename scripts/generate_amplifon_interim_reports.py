#!/usr/bin/env python3
from html import escape
from pathlib import Path


REPORTS_DIR = Path("reports")
ANALYSIS_DATE = "2026-06-06"
SKILL_VERSION = "1.1.0"
MODEL_VERSION = "OpenAI GPT-5 Codex"

REPORTS = [
    {
        "slug": "2024-q1",
        "period": "Q1 2024",
        "ended": "March 31, 2024",
        "badge": "Strong start, acquisition-heavy cash use",
        "source": "2024-q1/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at March 31, 2024",
        "sha": "a84dc09427d31b862a95bde12e3f9b8baaa9ada92c5ba0b7bac7bde05aeb4425",
        "pages": "6-7, 20-29, 41",
        "verdict": "Amplifon opened 2024 with broad revenue growth and a meaningful recurring margin improvement, but free cash flow weakened and acquisition spending pushed net debt higher, making the quality of the growth less clean than the headline suggests.",
        "consistency": "Not rated: this is the earliest quarterly source in the repository, so prior management claims cannot be tested reliably.",
        "kpis": [("€573.1M", "Revenue", "+6.1% YoY"), ("23.9%", "Recurring EBITDA margin", "+100 bps YoY"), ("€35.7M", "Recurring group profit", "+2.2% YoY"), ("€37.2M", "Free cash flow", "Down 19.6% YoY")],
        "working": [
            "Revenue increased across every geography, with reported growth of 6.1% and constant-exchange-rate growth of 8.8%.",
            "Recurring EBITDA rose 10.7% and margin expanded by 100 basis points, supporting management's claim that productivity actions were helping.",
            "Americas organic growth reached 13.0% and APAC organic growth reached 8.8%, showing that growth was not limited to acquisitions.",
        ],
        "obscured": [
            "Recurring group profit rose only 2.2%, far slower than recurring EBITDA, as financing and other below-EBITDA costs absorbed much of the operating gain.",
            "Free cash flow fell to €37.2M from €46.3M while capital expenditure increased.",
            "Acquisition cash-outs rose to €71.3M from €38.8M, leaving period cash flow negative and increasing net debt to €883.3M.",
        ],
        "decoded": [
            ("“Noticeable increase in revenues across all geographies”", "Accurate, but acquisitions supplied 3.2 percentage points of group growth and the resulting cash-outs exceeded free cash flow.", "High"),
            ("“Confirming the Group's ability to generate operating cash flow”", "The business generated positive free cash flow, but less than the prior year and not enough to fund the acquisition pace.", "High"),
        ],
        "bull": "Productivity gains persist, EMEA normalization continues, and organic growth remains above the market.",
        "bear": "Acquisition spending keeps outrunning free cash flow while profit growth remains much weaker than EBITDA growth.",
        "watch": "Recurring EBITDA margin versus the >24.6% FY target; EMEA demand; acquisition cash-outs; free cash flow; net debt.",
    },
    {
        "slug": "2024-h1",
        "period": "H1 2024",
        "ended": "June 30, 2024",
        "badge": "Growth continues, cash conversion weakens",
        "source": "2024-h1/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at June 30, 2024",
        "sha": "71972d4a15a39dee382c24e376ae4017b40a7d22744d88847eef4178ce59fa9b",
        "pages": "6-7, 22-33, 47",
        "verdict": "First-half revenue and recurring EBITDA grew strongly, but EMEA weakened in Q2, recurring profit barely advanced, free cash flow fell sharply, and acquisition-led spending lifted net debt above €1.0B.",
        "consistency": "Medium: the Q1 profitability improvement remained visible at group level, but Q2 exposed weaker EMEA growth and regional margin pressure.",
        "kpis": [("€1.18B", "Revenue", "+5.7% YoY"), ("25.2%", "Recurring EBITDA margin", "+40 bps YoY"), ("€90.3M", "Recurring group profit", "+1.0% YoY"), ("€46.8M", "Free cash flow", "Down 38.5% YoY")],
        "working": [
            "Revenue grew 5.7%, supported by 4.6% organic growth and acquisitions.",
            "Recurring EBITDA increased 10.9% and recurring margin expanded 40 basis points.",
            "Americas organic growth reached 14.4% and APAC delivered 7.2%, sustaining strong growth outside Europe.",
        ],
        "obscured": [
            "Q2 EMEA organic growth turned negative at -0.6%, weakening the broad-growth narrative established in Q1.",
            "Recurring group profit increased only 1.0% despite double-digit recurring EBITDA growth.",
            "Free cash flow fell to €46.8M from €76.1M and acquisition cash-outs more than doubled to €142.7M, pushing net debt to €1.01B.",
        ],
        "decoded": [
            ("“Strong improvement in profitability”", "True for recurring EBITDA, but not for recurring group profit or cash generation.", "High"),
            ("“Above-market organic growth”", "Group organic growth was solid, but it increasingly depended on Americas while EMEA softened in Q2.", "High"),
        ],
        "bull": "Americas and APAC growth continues while EMEA demand normalizes and productivity measures support the full-year margin target.",
        "bear": "European softness persists and higher interest, working-capital, and acquisition needs prevent operating growth from converting into profit and cash.",
        "watch": "Q3 EMEA organic growth; regional margins; recurring group profit growth; free cash flow; net debt and acquisition spending.",
    },
    {
        "slug": "2024-9m",
        "period": "9M 2024",
        "ended": "September 30, 2024",
        "badge": "Revenue growth masks margin deterioration",
        "source": "2024-9m/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at September 30, 2024",
        "sha": "f606249c3264964115395e259bb13bec4e70bf5de57f00e9027d8b2d91ba537e",
        "pages": "6-7, 22-34, 47",
        "verdict": "Amplifon maintained 6.1% revenue growth through nine months, but recurring profit declined, Q3 margins weakened across EMEA and Americas, free cash flow fell, and net debt climbed as acquisition spending accelerated.",
        "consistency": "Low: Q1's strong profitability narrative weakened materially by Q3, while the full-year margin target became harder to reconcile with deteriorating quarterly margins.",
        "kpis": [("€1.74B", "Revenue", "+6.1% YoY"), ("23.6%", "Recurring EBITDA margin", "+10 bps YoY"), ("€107.4M", "Recurring group profit", "-4.8% YoY"), ("€1.07B", "Net debt ex leases", "+€216.1M YTD")],
        "working": [
            "Revenue rose 6.1%, with Americas and APAC delivering strong organic and acquisition-led growth.",
            "Americas organic growth reached 13.5% and APAC organic growth reached 6.0%.",
            "Reported EBITDA rose 9.5%, helped by lower non-recurring costs than in the comparison period.",
        ],
        "obscured": [
            "Recurring EBITDA margin improved only 10 basis points, while Q3 recurring margin fell 40 basis points.",
            "Recurring group profit declined 4.8%; Q3 recurring group profit fell 25.5%.",
            "Free cash flow fell to €50.6M and acquisition cash-outs rose to €184.1M, helping push net debt to €1.07B.",
        ],
        "decoded": [
            ("“Slight increase in profitability”", "Reported EBITDA improved, but recurring profit declined and Q3 margins deteriorated.", "High"),
            ("“Decided acceleration” of the US direct-store network", "The expansion supported revenue growth but management explicitly acknowledged that it diluted margins.", "High"),
        ],
        "bull": "US direct-store investments mature, APAC remains resilient, and EMEA demand improves enough to restore margin momentum.",
        "bear": "The expansion remains dilutive, EMEA stays weak, and debt continues rising faster than recurring earnings.",
        "watch": "FY recurring EBITDA margin; Q4 EMEA and Americas margins; recurring group profit; free cash flow; leverage.",
    },
    {
        "slug": "2025-q1",
        "period": "Q1 2025",
        "ended": "March 31, 2025",
        "badge": "Record EBITDA margin, weaker earnings quality",
        "source": "2025-q1/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at March 31, 2025",
        "sha": "4070ca9c9205067eab95304ab8c261fddb90bb7deb0fb6af533eb3b07840a69f",
        "pages": "6-7, 26-36, 50",
        "verdict": "Amplifon achieved a record first-quarter EBITDA margin, but organic growth was nearly flat, reported and adjusted profits declined, free cash flow halved, and net debt increased.",
        "consistency": "Medium-low: the margin record supports management's profitability framing, but growth, profit, and cash flow were all weaker than Q1 2024.",
        "kpis": [("€587.8M", "Revenue", "+2.6% YoY"), ("+0.1%", "Organic growth", "Near flat"), ("23.9%", "Adjusted EBITDA margin", "+20 bps YoY"), ("€18.5M", "Free cash flow", "Down 50.4% YoY")],
        "working": [
            "Revenue increased 2.6% despite a soft market and difficult comparison base.",
            "Adjusted EBITDA rose 3.4% and adjusted margin reached 23.9%, a first-quarter record.",
            "EMEA reported revenue grew 2.0% and Americas reported revenue grew 6.9%.",
        ],
        "obscured": [
            "Organic growth was only 0.1%, so acquisitions provided almost all of the reported revenue growth.",
            "Reported group profit fell 5.7% and adjusted group profit fell 5.5%, despite the EBITDA margin record.",
            "Free cash flow fell to €18.5M from €37.2M and net debt excluding leases increased to €996.6M.",
        ],
        "decoded": [
            ("“Solid performance in revenues”", "Reported revenue grew, but underlying organic growth was effectively flat.", "High"),
            ("“Profitability increased, reaching a first quarter record”", "Accurate at EBITDA margin level; both reported and adjusted net profit declined.", "High"),
        ],
        "bull": "Market demand improves and the record EBITDA margin begins translating into stronger profit and cash flow.",
        "bear": "Low organic growth persists while acquisition dependence, weaker APAC performance, and debt pressure continue.",
        "watch": "Organic growth; APAC revenue and margin; adjusted group profit; free cash flow; net debt.",
    },
    {
        "slug": "2025-h1",
        "period": "H1 2025",
        "ended": "June 30, 2025",
        "badge": "Guidance cut confirms broad deterioration",
        "source": "2025-h1/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at June 30, 2025",
        "sha": "705275a2a50d355bed32b9eab627eac68399bae8a1cf8da399590c505c060170",
        "pages": "6-7, 31-46, 61",
        "verdict": "Amplifon's first-half results showed broad deterioration: revenue was nearly flat, margins and profits fell across regions, cash conversion weakened, debt rose, and management cut both revenue-growth and margin guidance.",
        "consistency": "Low: Q1's record-margin framing gave way to an 80-basis-point adjusted margin decline and a material full-year guidance cut.",
        "kpis": [("€1.18B", "Revenue", "+0.3% YoY"), ("24.4%", "Adjusted EBITDA margin", "-80 bps YoY"), ("€90.5M", "Adjusted group profit", "-16.1% YoY"), ("€1.11B", "Net debt ex leases", "+€147.2M YTD")],
        "working": [
            "Revenue remained slightly positive despite weak global demand.",
            "Americas still produced positive organic growth, and France and Germany showed better market momentum.",
            "Free cash flow remained positive and acquisition cash-outs were substantially lower than in H1 2024.",
        ],
        "obscured": [
            "Adjusted EBITDA fell 3.2% and adjusted margin fell 80 basis points; every region's adjusted EBITDA declined.",
            "Adjusted group profit fell 16.1% and reported group profit fell 22.4%.",
            "Management cut constant-currency revenue guidance from mid-to-high single digit to around 3%, and adjusted margin guidance from at least 24% to around 23%.",
        ],
        "decoded": [
            ("“Progressive normalization” expected", "The recovery remained a forecast after a weak first half, not an observed group-wide result.", "High"),
            ("“Temporary factors” in Southern Europe", "The factors may be temporary, but they were material enough to contribute to a large guidance cut.", "Medium"),
        ],
        "bull": "US demand and Southern Europe recover, while Fit4Growth restores margins without materially damaging revenue.",
        "bear": "The guidance cut proves insufficient as weak demand, regional margin pressure, and shareholder distributions keep debt elevated.",
        "watch": "Delivery against revised 3% constant-currency growth and 23% margin guidance; regional margins; adjusted profit; net debt.",
    },
    {
        "slug": "2025-9m",
        "period": "9M 2025",
        "ended": "September 30, 2025",
        "badge": "Flat revenue, falling profit, rising debt",
        "source": "2025-9m/financial-report.md",
        "source_title": "Amplifon Interim Financial Report as at September 30, 2025",
        "sha": "a4d45cfb07d5a3adea74d9fc7b8aee2b66f502c4d86096724aaba7260a00f23d",
        "pages": "6-7, 31-46, 61",
        "verdict": "Nine-month revenue was flat while adjusted EBITDA, adjusted profit, and free cash flow fell sharply; Fit4Growth offered a credible response, but guidance was narrowed again and debt rose after heavy buybacks and dividends.",
        "consistency": "Low: management narrowed constant-currency growth guidance again after the H1 cut, while margins, profit, cash flow, and debt all moved in the wrong direction.",
        "kpis": [("€1.74B", "Revenue", "-0.1% YoY"), ("22.7%", "Adjusted EBITDA margin", "-90 bps YoY"), ("€109.6M", "Adjusted group profit", "-18.4% YoY"), ("€1.17B", "Net debt ex leases", "+€212.9M YTD")],
        "working": [
            "Constant-currency revenue grew 1.8%, and EMEA reported revenue rose 1.5%.",
            "Q3 organic trends improved in most key markets according to management.",
            "Fit4Growth established a measurable 150-200 basis-point adjusted margin improvement target by 2027.",
        ],
        "obscured": [
            "Reported revenue declined 0.1%, adjusted EBITDA fell 4.1%, and adjusted group profit fell 18.4%.",
            "Adjusted EBITDA declined in every region, with APAC down 11.2% and Americas down 7.4%.",
            "Free cash flow fell to €28.4M while €108.2M of buybacks and €65.3M of dividends helped lift net debt to €1.17B.",
        ],
        "decoded": [
            ("“Substantially aligned” revenues", "Revenue was flat, but earnings and cash generation deteriorated materially.", "High"),
            ("Fit4Growth is “progressing well”", "The program has measurable targets, but near-term actions also reduce the revenue perimeter and benefits remain largely prospective.", "Medium"),
        ],
        "bull": "Fit4Growth delivers early margin gains, private-pay demand recovers, and the revenue perimeter stabilizes.",
        "bear": "Restructuring fails to offset weak demand while buybacks, dividends, and lower cash flow keep leverage elevated.",
        "watch": "FY constant-currency growth versus 2%-2.5%; adjusted margin near 23%; Fit4Growth savings and revenue impact; free cash flow; net debt.",
    },
]

STYLE = """
*{box-sizing:border-box}body{margin:0;background:#f4f4f6;color:#1f2937;font:13px Arial,sans-serif}a{color:#8b0013}.back{display:block;max-width:960px;margin:16px auto 0;padding:0 8px;text-decoration:none}.page{max-width:960px;margin:12px auto 24px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px #0002}.header{background:linear-gradient(135deg,#c0001a,#69000e);color:#fff;padding:26px 32px;display:flex;justify-content:space-between;gap:20px}.header h1{margin:0;font-size:24px}.header p{margin:5px 0}.meta{text-align:right;line-height:1.7;font-size:11px}.badge{display:inline-block;padding:3px 10px;border:1px solid #ffffff66;border-radius:20px}.verdict,.consistency{padding:13px 22px;line-height:1.6}.verdict{background:#fff8e1;border-left:5px solid #f59e0b}.consistency{background:#f8fafc;border-left:5px solid #64748b}.kpis{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #e5e7eb}.kpi{text-align:center;padding:16px 10px;border-right:1px solid #e5e7eb}.kpi:last-child{border:0}.value{font-size:20px;font-weight:700;color:#b00018}.label{font-size:10px;text-transform:uppercase;color:#6b7280}.change{margin-top:4px;font-size:11px}.content{padding:22px 26px 8px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}section{margin-bottom:22px}h2{font-size:13px;text-transform:uppercase;color:#b00018;border-bottom:2px solid #f8d7dc;padding-bottom:5px}.item{line-height:1.55;margin:0 0 11px}.cite{font-size:10.5px;color:#6b7280}.decode,.outlook{padding:10px 12px;margin-bottom:8px;background:#fafafa;border-left:3px solid #d1d5db}.claim{font-style:italic;color:#6b7280}.plain{margin-top:5px;line-height:1.5}.confidence{margin-top:5px;font-size:10px;color:#6b7280}.sources{padding:0 26px 22px;line-height:1.7}.footer{display:flex;justify-content:space-between;background:#1a1a2e;color:#9ca3af;padding:11px 24px;font-size:10.5px}.metadata{padding:12px 24px;background:#f9fafb;color:#6b7280;font-size:10px;line-height:1.6}@media(max-width:720px){.header,.footer{display:block}.meta{text-align:left;margin-top:12px}.kpis,.grid{grid-template-columns:1fr 1fr}.content{padding:18px 16px}.sources{padding:0 16px 18px}}@media(max-width:440px){.kpis,.grid{grid-template-columns:1fr}}
"""


def cited_items(items, source, pages):
    link = f'../sources/amplifon/{source}'
    return "\n".join(
        f'<p class="item"><strong>{escape(item)}</strong> '
        f'<a class="cite" href="{link}">Interim Report pp. {escape(pages)}</a></p>'
        for item in items
    )


def render(report):
    source_link = f'../sources/amplifon/{report["source"]}'
    kpis = "".join(
        f'<div class="kpi"><div class="value">{escape(value)}</div><div class="label">{escape(label)}</div><div class="change">{escape(change)}</div></div>'
        for value, label, change in report["kpis"]
    )
    decoded = "".join(
        f'<div class="decode"><div class="claim">{escape(claim)}</div><div class="plain">{escape(plain)}</div>'
        f'<div class="confidence">Confidence: {escape(confidence)} · <a href="{source_link}">Interim Report pp. {escape(report["pages"])}</a></div></div>'
        for claim, plain, confidence in report["decoded"]
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Amplifon {escape(report["period"])} Investor Report</title><style>{STYLE}</style></head><body>
<a class="back" href="../index.html">Back to Market Reality Dashboard</a><main class="page">
<header class="header"><div><h1>Amplifon S.p.A. - {escape(report["period"])} Results</h1><p>Independent, evidence-based investor summary</p></div>
<div class="meta">Ticker: AMP:IM · Euronext Milan<br>Period ended {escape(report["ended"])}<br><span class="badge">{escape(report["badge"])}</span></div></header>
<div class="verdict"><strong>One-line verdict:</strong> {escape(report["verdict"])}</div>
<div class="consistency"><strong>Historical Consistency Assessment:</strong> {escape(report["consistency"])}</div>
<div class="kpis">{kpis}</div><div class="content"><div class="grid"><div>
<section><h2>What Is Genuinely Working</h2>{cited_items(report["working"], report["source"], report["pages"])}</section>
<section><h2>Track Record And Consistency</h2><p class="item">{escape(report["consistency"])} <a class="cite" href="{source_link}">Interim Report pp. {escape(report["pages"])}</a></p></section>
</div><div><section><h2>What The Headline Obscures</h2>{cited_items(report["obscured"], report["source"], report["pages"])}</section>
<section><h2>Corporate Language, Decoded</h2>{decoded}</section></div></div>
<section><h2>What To Watch Next</h2><div class="outlook"><p><strong>Bull case:</strong> {escape(report["bull"])}</p>
<p><strong>Bear case:</strong> {escape(report["bear"])}</p><p><strong>Measurable watchlist:</strong> {escape(report["watch"])}</p></div></section></div>
<section class="sources"><h2>Sources And Caveats</h2><ul>
<li><a href="{source_link}">{escape(report["source_title"])}</a></li>
<li><a href="../sources/amplifon/INDEX.md">Amplifon official source index</a></li>
<li>Source Markdown is extracted from the official PDF; complex tables and visual layouts should be checked against the official PDF.</li>
<li>Comparisons use management-defined measures where stated and do not constitute investment advice.</li></ul></section>
<footer class="footer"><span>Amplifon S.p.A. · {escape(report["period"])} · Independent analysis</span><span>Not investment advice · Verify primary sources</span></footer>
<div class="metadata"><div>Analysis Date: {ANALYSIS_DATE}</div><div>Skill Version: {SKILL_VERSION}</div><div>Model Version: {MODEL_VERSION}</div><div>Source SHA-256: {report["sha"]}</div></div>
</main></body></html>
"""


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    for report in REPORTS:
        path = REPORTS_DIR / f'amplifon-{report["slug"]}.html'
        path.write_text(render(report), encoding="utf-8")
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
