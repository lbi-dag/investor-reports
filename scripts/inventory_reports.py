#!/usr/bin/env python3
import json
import re
from html import escape, unescape
from pathlib import Path
from datetime import datetime
try:
    from scripts.validate_reports import report_structure_errors
except ModuleNotFoundError:
    from validate_reports import report_structure_errors

# Configuration
REPORTS_DIR = Path("reports")
SOURCES_DIR = Path("sources")
COMPANY_PAGES_DIR = Path("companies")
COMPANIES = ["amplifon", "gn", "sonova"]
COMPANY_DIRECTORY = [
    {"slug": "amplifon", "name": "Amplifon", "ticker": "AMP:IM", "logo": "amplifon.svg", "logo_class": "", "description": "Global hearing-care retailer with coverage from 2024 onward."},
    {"slug": "sonova", "name": "Sonova", "ticker": "SOON:SW", "logo": "sonova.png", "logo_class": "", "description": "Global hearing-care technology and audiological-care group with coverage from H1 2025/26 onward."},
    {"slug": "gn", "name": "GN Group", "ticker": "GN.CO", "logo": "gn.svg", "logo_class": "logo-stage-dark", "description": "Hearing, enterprise-audio, and gaming technology group with coverage from FY 2025 onward."},
]
SKILL_VERSION = "1.1.0"  # Increment when SKILL.md or references change

PAGE_STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #1a1a2e; padding: 40px 20px; }
a:focus-visible { outline: 3px solid #f59e0b; outline-offset: 3px; }
.container { max-width: 1100px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #1f3a8a 0%, #1e1b4b 100%); color: #fff; padding: 40px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 32px rgba(15, 23, 42, .15); }
.header-company { display: flex; align-items: center; gap: 24px; margin-bottom: 22px; }.header-logo-stage { display: flex; align-items: center; justify-content: center; width: 150px; height: 76px; flex: 0 0 auto; padding: 14px; border-radius: 12px; background: #fff; }.header-logo { display: block; max-width: 118px; max-height: 48px; }
.header h1 { font-size: 32px; margin-bottom: 8px; }.header p { font-size: 16px; line-height: 1.55; opacity: .9; max-width: 720px; }.header-meta { margin-top: 8px; color: #dbeafe; font-size: 13px; }
.header-actions { display: flex; flex-wrap: wrap; gap: 8px; }.header-link { display: inline-flex; align-items: center; gap: 8px; color: #fff; text-decoration: none; font-size: 13px; padding: 9px 16px; background: #ffffff1a; border: 1px solid #ffffff33; border-radius: 7px; transition: background .15s ease, border-color .15s ease; }.header-link:hover { background: #ffffff29; border-color: #ffffff66; }
.stats-bar,.company-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
.stat-card,.company-card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px #0000000d; border-left: 4px solid #1f3a8a; }
.stat-value { font-size: 24px; font-weight: 700; color: #111827; }.stat-label { font-size: 12px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }
.company-card h2 { margin-bottom: 6px; }.company-card p { color: #4b5563; line-height: 1.5; margin-bottom: 14px; }.company-meta { color: #6b7280; font-size: 12px; margin-bottom: 14px; }
.logo-stage { height: 92px; display: flex; align-items: center; justify-content: center; margin: -4px -4px 18px; padding: 18px; border-radius: 9px; background: #f8fafc; border: 1px solid #eef0f3; }
.logo-stage-dark { background: #253746; border-color: #253746; }.company-logo { display: block; max-width: 210px; max-height: 56px; width: auto; height: auto; }
.section-heading { margin: 0 0 14px; color: #111827; font-size: 19px; }.latest-report { display: grid; grid-template-columns: 150px 1fr auto; align-items: center; gap: 24px; margin-bottom: 30px; padding: 26px 28px; border: 1px solid #dbe4f0; border-radius: 14px; background: linear-gradient(135deg, #fff 20%, #f5f8ff 100%); box-shadow: 0 8px 24px #0f172a12; }.latest-label { margin-bottom: 7px; color: #1f3a8a; font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }.latest-period { color: #111827; font-size: 25px; font-weight: 750; }.latest-brief { color: #273449; font-size: 18px; font-weight: 650; line-height: 1.4; }
.dashboard-table { width: 100%; background: #fff; border-radius: 12px; box-shadow: 0 4px 20px #00000014; border-collapse: collapse; overflow: hidden; }
.dashboard-table th { background: #f9fafb; padding: 16px; text-align: left; font-size: 12px; text-transform: uppercase; color: #4b5563; border-bottom: 1px solid #e5e7eb; }
.dashboard-table tbody tr { transition: background .15s ease; }.dashboard-table tbody tr:hover { background: #f8faff; }.dashboard-table td { padding: 17px 16px; border-bottom: 1px solid #f3f4f6; font-size: 14px; }.period-cell { color: #111827; font-weight: 700; white-space: nowrap; }.brief-cell { max-width: 520px; color: #374151; font-weight: 550; line-height: 1.45; }
.status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }.status-analyzed { background: #dcfce7; color: #166534; }.status-missing { background: #f3f4f6; color: #6b7280; }
.view-btn { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; padding: 8px 15px; background: #1f3a8a; color: #fff; text-decoration: none; border-radius: 7px; font-size: 12px; font-weight: 650; transition: background .15s ease, transform .15s ease; }.view-btn:hover { background: #172e70; transform: translateY(-1px); }.view-btn.disabled { background: #e5e7eb; color: #6b7280; pointer-events: none; }
.mobile-report-list { display: none; }.report-card { display: block; padding: 18px; border: 1px solid #e5e7eb; border-radius: 12px; background: #fff; color: inherit; text-decoration: none; box-shadow: 0 3px 12px #0f172a0d; }.report-card-top { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }.report-card-brief { color: #273449; font-weight: 600; line-height: 1.5; }.report-card-action { display: block; margin-top: 14px; color: #1f3a8a; font-size: 12px; font-weight: 700; }.page-footer { display: flex; justify-content: space-between; gap: 20px; margin-top: 30px; padding: 18px 2px 0; border-top: 1px solid #dce2ea; color: #6b7280; font-size: 11px; line-height: 1.5; }
@media (max-width: 720px) { body { padding: 20px 12px; }.header { padding: 26px 22px; }.header-company { display: block; }.header-logo-stage { width: 128px; height: 66px; margin-bottom: 18px; }.header h1 { font-size: 27px; }.latest-report { display: block; padding: 22px; }.latest-report .view-btn { margin-top: 18px; }.table-wrap { display: none; }.mobile-report-list { display: grid; gap: 12px; }.page-footer { display: block; }.page-footer span { display: block; margin-bottom: 6px; } }
"""

def get_existing_reports():
    reports = {}
    for company in COMPANIES:
        reports[company] = []
        for file in REPORTS_DIR.glob(f"{company}-*.html"):
            if report_structure_errors(file):
                continue
            # Extract period from filename, e.g., amplifon-2025.html -> 2025
            period = file.stem.replace(f"{company}-", "")
            reports[company].append(period)
    return reports

def get_available_sources():
    sources = {}
    for company in COMPANIES:
        manifest_path = SOURCES_DIR / company / "reports.json"
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                data = json.load(f)
                # Group by period
                periods = {}
                for report in data.get("reports", []):
                    p = report["period"]
                    if p not in periods:
                        periods[p] = []
                    periods[p].append(report)
                sources[company] = periods
    return sources

def extract_brief(html_path):
    try:
        if not html_path.exists():
            return "Analysis pending"
        content = html_path.read_text(encoding="utf-8")
        match = re.search(r'<span class="badge">\s*(.*?)\s*</span>', content, re.DOTALL)
        if match:
            return unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
    except Exception:
        pass
    return "Analysis pending"


def format_period(period):
    parts = period.upper().split("-")
    if len(parts) == 1:
        return f"FY {parts[0]}"
    year, suffix = parts
    return f"{suffix} {year}"

def period_sort_key(period):
    # Standardize period sorting: Year (2024) and Period (Q1 < H1 < 9M < FY)
    parts = period.split('-')
    year = int(parts[0])
    suffix = parts[1].lower() if len(parts) > 1 else 'fy'
    
    # Define chronological weights for different reporting types
    weights = {
        'q1': 1,
        'h1': 2,
        'q2': 2,
        '9m': 3,
        'q3': 3,
        'fy': 4,
        'q4': 4
    }
    return (year, weights.get(suffix, 0))

def render_company_directory(inventory):
    analyzed_count = sum(item["status"] == "PRESENT" for item in inventory)
    cards = []
    for company in COMPANY_DIRECTORY:
        company_items = [item for item in inventory if item["company"] == company["slug"]]
        report_count = sum(item["status"] == "PRESENT" for item in company_items)
        if report_count:
            status = f"{report_count} analyzed reports"
        else:
            status = "Coverage planned"
        action = f'<a href="companies/{company["slug"]}.html" class="view-btn">View company</a>'
        cards.append(f"""<article class="company-card">
          <div class="logo-stage {company["logo_class"]}"><img class="company-logo" src="assets/company-logos/{company["logo"]}" alt="{escape(company["name"])} logo"></div>
          <h2>{escape(company["name"])}</h2>
          <div class="company-meta">{escape(company["ticker"])} · {status}</div>
          <p>{escape(company["description"])}</p>
          {action}
        </article>""")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Investor Reports Company Directory</title><style>{PAGE_STYLE}</style></head><body><main class="container">
<header class="header"><h1>Investor Reports</h1><p>Tracking the gap between corporate narratives and financial reality.</p>
<a class="header-link" href="https://github.com/lbi-dag/investor-reports"><svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>View on GitHub</a></header>
<div class="stats-bar"><div class="stat-card"><div class="stat-value">{len(COMPANY_DIRECTORY)}</div><div class="stat-label">Companies listed</div></div>
<div class="stat-card"><div class="stat-value">{analyzed_count}</div><div class="stat-label">Analyzed reports</div></div>
<div class="stat-card"><div class="stat-value">{len(COMPANIES)}</div><div class="stat-label">Companies with source coverage</div></div></div>
<section class="company-grid">{''.join(cards)}</section></main></body></html>
"""


def render_company_page(company, inventory):
    rows = []
    mobile_cards = []
    sorted_inventory = sorted(inventory, key=lambda value: period_sort_key(value["period"]), reverse=True)
    latest_report = None
    for item in sorted_inventory:
        period = item["period"]
        status = item["status"]
        filename = f'{company["slug"]}-{period.replace("-fy", "")}.html'
        report_path = REPORTS_DIR / filename
        brief = extract_brief(report_path) if status == "PRESENT" else "Analysis pending"
        display_period = format_period(period)
        status_class = "status-analyzed" if status == "PRESENT" else "status-missing"
        button_class = "view-btn" if status == "PRESENT" else "view-btn disabled"
        link = f"../reports/{filename}" if status == "PRESENT" else "#"
        status_label = "Analyzed" if status == "PRESENT" else "Pending"
        if latest_report is None and status == "PRESENT":
            latest_report = {"period": display_period, "brief": brief, "link": link}
        rows.append(f"""
        <tr>
          <td class="period-cell">{display_period}</td>
          <td><span class="status-badge {status_class}">{status_label}</span></td>
          <td class="brief-cell">{escape(brief)}</td>
          <td><a href="{link}" class="{button_class}">{"View report" if status == "PRESENT" else "Pending"}</a></td>
        </tr>""")
        if status == "PRESENT":
            mobile_cards.append(f"""<a class="report-card" href="{link}">
          <div class="report-card-top"><span class="period-cell">{display_period}</span><span class="status-badge {status_class}">{status_label}</span></div>
          <div class="report-card-brief">{escape(brief)}</div>
          <span class="report-card-action">View report →</span>
        </a>""")
        else:
            mobile_cards.append(f"""<article class="report-card">
          <div class="report-card-top"><span class="period-cell">{display_period}</span><span class="status-badge {status_class}">{status_label}</span></div>
          <div class="report-card-brief">{escape(brief)}</div>
        </article>""")
    analyzed_count = sum(item["status"] == "PRESENT" for item in inventory)
    document_count = sum(item.get("document_count", 0) for item in inventory)
    covered_periods = [item["period"] for item in inventory if item["status"] == "PRESENT"]
    coverage_since = min((period_sort_key(period), period) for period in covered_periods)[1] if covered_periods else None
    source_index = SOURCES_DIR / company["slug"] / "INDEX.md"
    source_discovery = SOURCES_DIR / company["slug"] / "DISCOVERY.md"
    if source_index.exists():
        source_link = f'<a class="header-link" href="../sources/{company["slug"]}/INDEX.md">Official source index</a>'
    elif source_discovery.exists():
        source_link = f'<a class="header-link" href="../sources/{company["slug"]}/DISCOVERY.md">Source discovery</a>'
    else:
        source_link = ""
    rows_html = ''.join(rows) or '<tr><td colspan="4">No reports available yet. Coverage is planned.</td></tr>'
    mobile_html = ''.join(mobile_cards) or '<article class="report-card">No reports available yet. Coverage is planned.</article>'
    logo = company.get("logo")
    logo_html = (
        f'<div class="header-logo-stage"><img class="header-logo" src="../assets/company-logos/{logo}" alt="{escape(company["name"])} logo"></div>'
        if logo
        else ""
    )
    description = escape(company.get("description", "Independent investor analysis based on official company materials."))
    latest_html = (
        f"""<section aria-labelledby="latest-heading"><h2 class="section-heading" id="latest-heading">Latest analysis</h2>
<article class="latest-report"><div><div class="latest-label">Latest report</div><div class="latest-period">{latest_report["period"]}</div></div>
<div class="latest-brief">{escape(latest_report["brief"])}</div><a class="view-btn" href="{latest_report["link"]}">Read latest report</a></article></section>"""
        if latest_report
        else ""
    )
    coverage_value = format_period(coverage_since) if coverage_since else "Planned"
    archive_heading = "Report archive" if inventory else "Coverage status"
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(company["name"])} Investor Reports</title><style>{PAGE_STYLE}</style></head><body><main class="container">
<header class="header"><div class="header-company">{logo_html}<div><h1>{escape(company["name"])} Investor Reports</h1><p>{description}</p><div class="header-meta">{escape(company["ticker"])} · Independent, evidence-based analysis</div></div></div>
<nav class="header-actions" aria-label="Company links"><a class="header-link" href="../index.html">All companies</a>{source_link}</nav></header>
<div class="stats-bar"><div class="stat-card"><div class="stat-value">{analyzed_count}</div><div class="stat-label">Analyzed reports</div></div>
<div class="stat-card"><div class="stat-value">{coverage_value}</div><div class="stat-label">Coverage since</div></div>
<div class="stat-card"><div class="stat-value">{document_count}</div><div class="stat-label">Official source documents</div></div></div>
{latest_html}<section aria-labelledby="archive-heading"><h2 class="section-heading" id="archive-heading">{archive_heading}</h2>
<div class="table-wrap"><table class="dashboard-table"><thead><tr><th>Period</th><th>Status</th><th>Brief</th><th>Action</th></tr></thead>
<tbody>{rows_html}</tbody></table></div><div class="mobile-report-list">{mobile_html}</div></section>
<footer class="page-footer"><span>Independent analysis for informational purposes.</span><span>Not investment advice · Verify primary sources</span></footer></main></body></html>
"""


def update_index_html(inventory):
    Path("index.html").write_text(render_company_directory(inventory), encoding="utf-8")
    COMPANY_PAGES_DIR.mkdir(exist_ok=True)
    for company in COMPANY_DIRECTORY:
        company_items = [item for item in inventory if item["company"] == company["slug"]]
        (COMPANY_PAGES_DIR / f'{company["slug"]}.html').write_text(
            render_company_page(company, company_items), encoding="utf-8"
        )

def main():
    existing = get_existing_reports()
    available = get_available_sources()
    
    inventory = []
    
    print(f"--- Batch Analysis Pipeline Inventory ---")
    print(f"Scan Date: {datetime.now().isoformat()}")
    print(f"Skill Version: {SKILL_VERSION}")
    print("-" * 40)
    
    for company, periods in available.items():
        for period, docs in periods.items():
            report_exists = period in existing.get(company, [])
            if not report_exists and period.endswith("-fy"):
                report_exists = period.replace("-fy", "") in existing.get(company, [])
            
            status = "PRESENT" if report_exists else "MISSING"
            
            item = {
                "company": company,
                "period": period,
                "status": status,
                "document_count": len(docs),
                "documents": [d["title"] for d in docs]
            }
            inventory.append(item)
            
            print(f"[{status}] {company.capitalize()} {period} ({len(docs)} documents)")

    # Update index.html
    update_index_html(inventory)

    # Write inventory for tracking
    with open("reports/inventory.json", "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "skill_version": SKILL_VERSION,
            "inventory": inventory
        }, f, indent=2)
    
    print("-" * 40)
    print(f"Inventory saved; company directory and company report pages updated.")

if __name__ == "__main__":
    main()
