#!/usr/bin/env python3
import json
import re
from html import escape
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
COMPANIES = ["amplifon"]
COMPANY_DIRECTORY = [
    {"slug": "amplifon", "name": "Amplifon", "ticker": "AMP:IM", "description": "Global hearing-care retailer with coverage from 2024 onward."},
    {"slug": "starkey", "name": "Starkey", "ticker": "Private", "description": "Hearing-aid manufacturer. Source collection and analysis are planned."},
]
SKILL_VERSION = "1.1.0"  # Increment when SKILL.md or references change

PAGE_STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #1a1a2e; padding: 40px 20px; }
.container { max-width: 1100px; margin: 0 auto; }
.header { background: linear-gradient(135deg, #1f3a8a 0%, #1e1b4b 100%); color: #fff; padding: 40px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 10px 32px rgba(15, 23, 42, .15); }
.header h1 { font-size: 32px; margin-bottom: 10px; }.header p { font-size: 16px; opacity: .9; max-width: 700px; margin-bottom: 20px; }
.header-link { display: inline-block; color: #fff; text-decoration: none; font-size: 13px; padding: 8px 16px; margin-right: 8px; background: #ffffff1a; border: 1px solid #ffffff33; border-radius: 6px; }
.stats-bar,.company-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
.stat-card,.company-card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px #0000000d; border-left: 4px solid #1f3a8a; }
.stat-value { font-size: 24px; font-weight: 700; color: #111827; }.stat-label { font-size: 12px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }
.company-card h2 { margin-bottom: 6px; }.company-card p { color: #4b5563; line-height: 1.5; margin-bottom: 14px; }.company-meta { color: #6b7280; font-size: 12px; margin-bottom: 14px; }
.dashboard-table { width: 100%; background: #fff; border-radius: 12px; box-shadow: 0 4px 20px #00000014; border-collapse: collapse; overflow: hidden; }
.dashboard-table th { background: #f9fafb; padding: 16px; text-align: left; font-size: 12px; text-transform: uppercase; color: #4b5563; border-bottom: 1px solid #e5e7eb; }
.dashboard-table td { padding: 16px; border-bottom: 1px solid #f3f4f6; font-size: 14px; }.verdict-cell { max-width: 480px; color: #374151; font-style: italic; }
.status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }.status-analyzed { background: #dcfce7; color: #166534; }.status-missing { background: #f3f4f6; color: #6b7280; }
.view-btn { display: inline-block; padding: 7px 14px; background: #1f3a8a; color: #fff; text-decoration: none; border-radius: 6px; font-size: 12px; }.view-btn.disabled { background: #e5e7eb; color: #6b7280; pointer-events: none; }
@media (max-width: 720px) { body { padding: 20px 10px; }.header { padding: 26px 22px; }.table-wrap { overflow-x: auto; }.dashboard-table { min-width: 760px; } }
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

def extract_verdict(html_path):
    try:
        if not html_path.exists():
            return "Analysis pending..."
        with open(html_path, "r") as f:
            content = f.read()
            # Look for <div class="verdict"><strong>One-line verdict:</strong> ...</div>
            match = re.search(r'<div class="verdict">\s*<strong>One-line verdict:</strong>\s*(.*?)\s*</div>', content, re.DOTALL)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return "Analysis pending..."

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
          <h2>{escape(company["name"])}</h2>
          <div class="company-meta">{escape(company["ticker"])} · {status}</div>
          <p>{escape(company["description"])}</p>
          {action}
        </article>""")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Investor Reports Company Directory</title><style>{PAGE_STYLE}</style></head><body><main class="container">
<header class="header"><h1>Investor Reports</h1><p>Select a company to review its reporting history and evidence-based investor briefs.</p>
<a class="header-link" href="https://github.com/lbi-dag/investor-reports">View on GitHub</a></header>
<div class="stats-bar"><div class="stat-card"><div class="stat-value">{len(COMPANY_DIRECTORY)}</div><div class="stat-label">Companies listed</div></div>
<div class="stat-card"><div class="stat-value">{analyzed_count}</div><div class="stat-label">Analyzed reports</div></div>
<div class="stat-card"><div class="stat-value">{len(COMPANIES)}</div><div class="stat-label">Companies with source coverage</div></div></div>
<section class="company-grid">{''.join(cards)}</section></main></body></html>
"""


def render_company_page(company, inventory):
    rows = []
    for item in sorted(inventory, key=lambda value: period_sort_key(value["period"]), reverse=True):
        period = item["period"]
        status = item["status"]
        filename = f'{company["slug"]}-{period.replace("-fy", "")}.html'
        report_path = REPORTS_DIR / filename
        verdict = extract_verdict(report_path) if status == "PRESENT" else "Analysis pending..."
        status_class = "status-analyzed" if status == "PRESENT" else "status-missing"
        button_class = "view-btn" if status == "PRESENT" else "view-btn disabled"
        link = f"../reports/{filename}" if status == "PRESENT" else "#"
        rows.append(f"""
        <tr>
          <td>{period.upper()}</td>
          <td><span class="status-badge {status_class}">{status.capitalize()}</span></td>
          <td class="verdict-cell">{verdict}</td>
          <td><a href="{link}" class="{button_class}">{"View report" if status == "PRESENT" else "Pending"}</a></td>
        </tr>""")
    analyzed_count = sum(item["status"] == "PRESENT" for item in inventory)
    missing_count = len(inventory) - analyzed_count
    source_index = SOURCES_DIR / company["slug"] / "INDEX.md"
    source_link = (
        f'<a class="header-link" href="../sources/{company["slug"]}/INDEX.md">Official source index</a>'
        if source_index.exists()
        else ""
    )
    rows_html = ''.join(rows) or '<tr><td colspan="4">No reports available yet. Coverage is planned.</td></tr>'
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(company["name"])} Investor Reports</title><style>{PAGE_STYLE}</style></head><body><main class="container">
<header class="header"><h1>{escape(company["name"])} Report History</h1><p>Period-level investor briefs reconciling management narratives with official reported figures.</p>
<a class="header-link" href="../index.html">All companies</a>{source_link}</header>
<div class="stats-bar"><div class="stat-card"><div class="stat-value">{analyzed_count}</div><div class="stat-label">Analyzed reports</div></div>
<div class="stat-card"><div class="stat-value">{missing_count}</div><div class="stat-label">Pending analysis</div></div>
<div class="stat-card"><div class="stat-value">{escape(company["ticker"])}</div><div class="stat-label">Ticker</div></div></div>
<div class="table-wrap"><table class="dashboard-table"><thead><tr><th>Period</th><th>Status</th><th>One-line verdict</th><th>Action</th></tr></thead>
<tbody>{rows_html}</tbody></table></div></main></body></html>
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
