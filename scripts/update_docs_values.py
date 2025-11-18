#!/usr/bin/env python3
"""
Update documentation with current model values.

Since MyST CLI doesn't support runtime substitutions, this script
pre-generates markdown files with actual values from the model.

Usage:
    python scripts/update_docs_values.py

Run this whenever the model changes to keep docs in sync.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel
import re

def generate_values():
    """Run model and return all values as dict"""
    model = StadiumEconomicModel()

    baseline_ticket, baseline_beer, baseline = model.optimal_pricing()
    ceiling_7_ticket, ceiling_7_beer, ceiling_7 = model.optimal_pricing(beer_price_control=7.0)
    ceiling_8_ticket, ceiling_8_beer, ceiling_8 = model.optimal_pricing(beer_price_control=8.0)
    ceiling_5_ticket, ceiling_5_beer, ceiling_5 = model.optimal_pricing(beer_price_control=5.0)

    games = 81

    return {
        # Baseline
        'baseline_ticket': f"{baseline_ticket:.2f}",
        'baseline_beer': f"{baseline_beer:.2f}",
        'baseline_attendance': f"{baseline['attendance']:,.0f}",
        'baseline_beers_per_fan': f"{baseline['beers_per_fan']:.2f}",
        'baseline_profit_season': f"{baseline['profit']*games/1e6:.1f}",

        # $7 ceiling
        'ceiling7_ticket': f"{ceiling_7_ticket:.2f}",
        'ceiling7_ticket_pct': f"{100*(ceiling_7_ticket/baseline_ticket-1):.1f}",
        'ceiling7_attendance_pct': f"{100*(ceiling_7['attendance']/baseline['attendance']-1):.1f}",
        'ceiling7_beers_pct': f"{100*(ceiling_7['total_beers']/baseline['total_beers']-1):.1f}",
        'ceiling7_beers_per_fan': f"{ceiling_7['beers_per_fan']:.2f}",
        'ceiling7_beers_per_fan_pct': f"{100*(ceiling_7['beers_per_fan']/baseline['beers_per_fan']-1):.1f}",
        'ceiling7_profit_change_season': f"{(ceiling_7['profit']-baseline['profit'])*games/1e6:.1f}",

        # $8 ceiling
        'ceiling8_ticket': f"{ceiling_8_ticket:.2f}",
        'ceiling8_ticket_pct': f"{100*(ceiling_8_ticket/baseline_ticket-1):.1f}",

        # $5 ceiling
        'ceiling5_ticket': f"{ceiling_5_ticket:.2f}",
        'ceiling5_ticket_pct': f"{100*(ceiling_5_ticket/baseline_ticket-1):.1f}",

        # Multiplier
        'multiplier': f"{(ceiling_7_ticket - baseline_ticket)/(baseline_beer - 7.0):.2f}",

        # Taxes & externalities
        'current_tax': "1.09",
        'external_cost': "4.00",
        'pigouvian_gap': "2.91",
        'tax_coverage_pct': "27",
        'pigouvian_revenue_annual': f"{2.91 * baseline['total_beers'] * games / 1e6:.1f}",
    }

def update_file(filepath, values):
    """Replace {{ placeholders }} with actual values in a file"""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Replace all {{ key }} with values
    for key, value in values.items():
        placeholder = f"{{{{ {key} }}}}"
        content = content.replace(placeholder, value)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    print("Generating model values...")
    values = generate_values()

    print(f"Generated {len(values)} values")
    print("\nKey values:")
    print(f"  Baseline: ${values['baseline_ticket']} ticket, ${values['baseline_beer']} beer")
    print(f"  $7 ceiling: ${values['ceiling7_ticket']} ticket (+{values['ceiling7_ticket_pct']}%)")
    print(f"  Pigouvian revenue: ${values['pigouvian_revenue_annual']}M/year")

    # Find all markdown files with placeholders
    docs_dir = Path('docs')
    updated = []

    for mdfile in docs_dir.glob('*.md'):
        with open(mdfile, 'r') as f:
            content = f.read()

        if '{{' in content:
            if update_file(mdfile, values):
                updated.append(mdfile.name)
                print(f"  ✓ {mdfile.name}")

    if updated:
        print(f"\n✓ Updated {len(updated)} files")
    else:
        print("\n- No files needed updating")

    # Check for remaining placeholders
    remaining_files = []
    for mdfile in docs_dir.glob('*.md'):
        with open(mdfile, 'r') as f:
            content = f.read()
        placeholders = re.findall(r'\{\{[^}]+\}\}', content)
        if placeholders:
            remaining_files.append((mdfile.name, placeholders))

    if remaining_files:
        print(f"\n⚠️  {len(remaining_files)} files still have placeholders:")
        for fname, phs in remaining_files[:3]:
            print(f"  {fname}: {len(phs)} placeholders")
    else:
        print("\n✓ No remaining placeholders!")

if __name__ == '__main__':
    main()
