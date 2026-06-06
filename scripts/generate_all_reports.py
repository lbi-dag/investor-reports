#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
REPORTS_DIR = Path("reports")
SOURCES_DIR = Path("sources")
COMPANIES = ["amplifon"]
SKILL_VERSION = "1.1.0"  # Increment when SKILL.md or references change

def get_existing_reports():
    reports = {}
    for company in COMPANIES:
        reports[company] = []
        for file in REPORTS_DIR.glob(f"{company}-*.html"):
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

def update_index_html(inventory):
    analyzed_count = sum(1 for item in inventory if item["status"] == "PRESENT")
    missing_count = sum(1 for item in inventory if item["status"] == "MISSING")
    
    rows_html = ""
    # Sort inventory by period descending
    for item in sorted(inventory, key=lambda x: x["period"], reverse=True):
        company = item["company"]
        period = item["period"]
        status = item["status"]
        
        # Determine filename
        period_slug = period.replace("-fy", "")
        filename = f"{company}-{period_slug}.html"
        report_path = REPORTS_DIR / filename
        
        verdict = extract_verdict(report_path) if status == "PRESENT" else "Analysis pending..."
        status_class = "status-analyzed" if status == "PRESENT" else "status-missing"
        btn_class = "view-btn" if status == "PRESENT" else "view-btn disabled"
        link = f"reports/{filename}" if status == "PRESENT" else "#"
        
        rows_html += f"""
        <tr>
          <td><span class="ticker">{company.upper()}</span></td>
          <td>{period.upper()}</td>
          <td><span class="status-badge {status_class}">{status.capitalize()}</span></td>
          <td class="verdict-cell">{verdict}</td>
          <td>—</td>
          <td><a href="{link}" class="{btn_class}">{"View Report" if status == "PRESENT" else "Generate"}</a></td>
        </tr>"""

    # Update template stats
    if not os.path.exists("index.html"):
        return

    with open("index.html", "r") as f:
        template = f.read()
    
    # Simple string replacements for the dashboard
    template = re.sub(r'<div class="stat-value">\d+</div>\s*<div class="stat-label">Analyzed Reports</div>', 
                     f'<div class="stat-value">{analyzed_count}</div><div class="stat-label">Analyzed Reports</div>', template)
    template = re.sub(r'<div class="stat-value">\d+</div>\s*<div class="stat-label">Pending Analysis</div>', 
                     f'<div class="stat-value">{missing_count}</div><div class="stat-label">Pending Analysis</div>', template)
    
    # Replace table body
    template = re.sub(r'<tbody>.*?</tbody>', f'<tbody>{rows_html}\n      </tbody>', template, flags=re.DOTALL)
    
    with open("index.html", "w") as f:
        f.write(template)

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
    print(f"Inventory saved to reports/inventory.json and index.html updated.")

if __name__ == "__main__":
    main()
