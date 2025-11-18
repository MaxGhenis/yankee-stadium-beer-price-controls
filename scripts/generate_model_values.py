#!/usr/bin/env python3
"""
Generate model values for MyST substitutions in documentation.

This script runs the economic model and exports key values to _config.yml
as MyST substitutions, ensuring documentation stays consistent with model predictions.

Usage:
    python scripts/generate_model_values.py

Then in markdown files, use: {{ baseline_ticket }} or {{ ceiling7_ticket_pct }}
"""

import sys
sys.path.insert(0, '.')

from src.model import StadiumEconomicModel
import yaml
from pathlib import Path

def generate_model_values():
    """Run model and generate all key values"""
    model = StadiumEconomicModel()

    # Get key scenarios
    baseline_ticket, baseline_beer, baseline = model.optimal_pricing()
    ceiling_7_ticket, ceiling_7_beer, ceiling_7 = model.optimal_pricing(beer_price_control=7.0)
    ceiling_8_ticket, ceiling_8_beer, ceiling_8 = model.optimal_pricing(beer_price_control=8.0)
    ceiling_5_ticket, ceiling_5_beer, ceiling_5 = model.optimal_pricing(beer_price_control=5.0)

    games_per_season = 81

    # Build comprehensive substitutions
    subs = {
        # Baseline
        'baseline_ticket': f"{baseline_ticket:.2f}",
        'baseline_beer': f"{baseline_beer:.2f}",
        'baseline_attendance': f"{baseline['attendance']:,.0f}",
        'baseline_beers_total': f"{baseline['total_beers']:,.0f}",
        'baseline_beers_per_fan': f"{baseline['beers_per_fan']:.2f}",
        'baseline_profit_game': f"{baseline['profit']/1e6:.2f}",
        'baseline_profit_season': f"{baseline['profit']*games_per_season/1e6:.1f}",

        # $7 ceiling
        'ceiling7_ticket': f"{ceiling_7_ticket:.2f}",
        'ceiling7_ticket_increase': f"{ceiling_7_ticket - baseline_ticket:.2f}",
        'ceiling7_ticket_pct': f"{100*(ceiling_7_ticket/baseline_ticket-1):.1f}",
        'ceiling7_attendance': f"{ceiling_7['attendance']:,.0f}",
        'ceiling7_attendance_pct': f"{100*(ceiling_7['attendance']/baseline['attendance']-1):.1f}",
        'ceiling7_beers_total': f"{ceiling_7['total_beers']:,.0f}",
        'ceiling7_beers_pct': f"{100*(ceiling_7['total_beers']/baseline['total_beers']-1):.1f}",
        'ceiling7_beers_per_fan': f"{ceiling_7['beers_per_fan']:.2f}",
        'ceiling7_beers_per_fan_pct': f"{100*(ceiling_7['beers_per_fan']/baseline['beers_per_fan']-1):.1f}",
        'ceiling7_profit_game': f"{ceiling_7['profit']/1e6:.2f}",
        'ceiling7_profit_season': f"{ceiling_7['profit']*games_per_season/1e6:.1f}",
        'ceiling7_profit_change': f"{(ceiling_7['profit']-baseline['profit'])/1e6:.2f}",
        'ceiling7_profit_change_season': f"{(ceiling_7['profit']-baseline['profit'])*games_per_season/1e6:.1f}",

        # $8 ceiling
        'ceiling8_ticket': f"{ceiling_8_ticket:.2f}",
        'ceiling8_ticket_pct': f"{100*(ceiling_8_ticket/baseline_ticket-1):.1f}",
        'ceiling8_beers_pct': f"{100*(ceiling_8['total_beers']/baseline['total_beers']-1):.1f}",

        # $5 ceiling
        'ceiling5_ticket': f"{ceiling_5_ticket:.2f}",
        'ceiling5_ticket_increase': f"{ceiling_5_ticket - baseline_ticket:.2f}",
        'ceiling5_ticket_pct': f"{100*(ceiling_5_ticket/baseline_ticket-1):.1f}",
        'ceiling5_attendance_pct': f"{100*(ceiling_5['attendance']/baseline['attendance']-1):.1f}",
        'ceiling5_beers_pct': f"{100*(ceiling_5['total_beers']/baseline['total_beers']-1):.1f}",

        # Multiplier
        'multiplier': f"{(ceiling_7_ticket - baseline_ticket)/(baseline_beer - 7.0):.2f}",

        # Externalities & taxes
        'external_cost': "4.00",
        'current_tax': "1.09",
        'pigouvian_gap': "2.91",
        'tax_coverage_pct': "27",
        'pigouvian_revenue_annual': f"{2.91 * baseline['total_beers'] * games_per_season / 1e6:.1f}",
        'external_costs_annual': f"{4.00 * baseline['total_beers'] * games_per_season / 1e6:.1f}",
        'current_tax_revenue_annual': f"{1.09 * baseline['total_beers'] * games_per_season / 1e6:.1f}",
    }

    return subs

def update_config(subs):
    """Update _config.yml with substitutions"""
    config_path = Path('docs/_config.yml')

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}

    # Update substitutions
    config['myst_substitutions'] = subs

    # Ensure substitution extension is enabled
    if 'parse' not in config:
        config['parse'] = {}
    if 'myst_enable_extensions' not in config['parse']:
        config['parse']['myst_enable_extensions'] = []
    if 'substitution' not in config['parse']['myst_enable_extensions']:
        config['parse']['myst_enable_extensions'].append('substitution')

    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Updated {config_path}")

def main():
    print("Generating model values...")
    subs = generate_model_values()

    print(f"Generated {len(subs)} substitutions")
    print("\nKey values:")
    print(f"  Baseline: ${subs['baseline_ticket']} ticket, ${subs['baseline_beer']} beer")
    print(f"  $7 ceiling: ${subs['ceiling7_ticket']} ticket (+{subs['ceiling7_ticket_pct']}%), {subs['ceiling7_attendance_pct']}% attendance")
    print(f"  Multiplier: {subs['multiplier']}x")
    print(f"  Pigouvian revenue: ${subs['pigouvian_revenue_annual']}M/year")

    update_config(subs)

    print("\n✓ Done! Use in markdown with {{ variable_name }}")
    print("\nExamples:")
    print("  The baseline ticket price is ${{ baseline_ticket }}")
    print("  A $7 ceiling increases tickets by {{ ceiling7_ticket_pct }}%")
    print("  Annual Pigouvian revenue: ${{ pigouvian_revenue_annual }}M")

if __name__ == '__main__':
    main()
