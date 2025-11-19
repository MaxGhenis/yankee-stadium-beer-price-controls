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
from src.config_loader import load_full_config # Import load_full_config from config_loader
import re

def generate_values():
    """Run model and return all values as dict"""
    model = StadiumEconomicModel()
    full_config = load_full_config() # Load full config explicitly

    baseline_ticket, baseline_beer, baseline = model.optimal_pricing()
    ceiling_7_ticket, ceiling_7_beer, ceiling_7 = model.optimal_pricing(beer_price_control=7.0)
    ceiling_8_ticket, ceiling_8_beer, ceiling_8 = model.optimal_pricing(beer_price_control=8.0)
    ceiling_5_ticket, ceiling_5_beer, ceiling_5 = model.optimal_pricing(beer_price_control=5.0)

    games = 81
    
    # Calculate additional values needed for policy.md.tpl
    # These calculations need raw numbers before formatting
    baseline_total_beers_raw = baseline['total_beers']
    ceiling7_total_beers_raw = ceiling_7['total_beers']
    
    baseline_profit_raw = baseline['profit']
    ceiling7_profit_raw = ceiling_7['profit']
    
    current_taxes_per_beer_raw = full_config['taxes']['excise_federal'] + \
                                 full_config['taxes']['excise_state'] + \
                                 full_config['taxes']['excise_local'] + \
                                 (full_config['taxes']['sales_tax_rate'] / 100 * baseline_beer) # Approx sales tax portion
    
    external_cost_sum_raw = full_config['external_costs']['crime'] + full_config['external_costs']['health']
    pigouvian_gap_raw = external_cost_sum_raw - current_taxes_per_beer_raw

    # Calculate welfare metrics for baseline and ceiling_7
    welfare_base = model.social_welfare(baseline_ticket, baseline_beer)
    welfare_7 = model.social_welfare(ceiling_7_ticket, ceiling_7_beer)

    # Pigouvian tax effects for table
    pigouvian_total_beers_raw = 28500 # from original template value
    pigouvian_gov_revenue = (pigouvian_gap_raw + current_taxes_per_beer_raw) * pigouvian_total_beers_raw

    return {
        # Baseline
        'baseline_ticket': f"{baseline_ticket:.2f}",
        'baseline_beer': f"{baseline_beer:.2f}",
        'baseline_attendance': f"{baseline['attendance']:,.0f}",
        'baseline_beers_per_fan': f"{baseline['beers_per_fan']:.2f}",
        'baseline_profit_season': f"{baseline_profit_raw*games/1e6:.1f}",
        'baseline_total_beers': f"{baseline_total_beers_raw:,.0f}",
        'baseline_profit_season_raw': f"{baseline_profit_raw}", # Raw for calculations in template
        'baseline_profit_per_game_M': f"{baseline_profit_raw/1e6:.2f}",

        # $7 ceiling
        'ceiling7_ticket': f"{ceiling_7_ticket:.2f}",
        'ceiling7_ticket_increase': f"{(ceiling_7_ticket - baseline_ticket):.2f}", # Absolute increase
        'ceiling7_ticket_pct': f"{100*(ceiling_7_ticket/baseline_ticket-1):.1f}",
        'ceiling7_attendance': f"{ceiling_7['attendance']:,.0f}",
        'ceiling7_attendance_change': f"{(ceiling_7['attendance'] - baseline['attendance']):,.0f}",
        'ceiling7_attendance_pct': f"{100*(ceiling_7['attendance']/baseline['attendance']-1):.1f}",
        'ceiling7_beers_per_fan': f"{ceiling_7['beers_per_fan']:.2f}",
        'ceiling7_beers_per_fan_pct': f"{100*(ceiling_7['beers_per_fan']/baseline['beers_per_fan']-1):.1f}",
        'ceiling7_total_beers': f"{ceiling7_total_beers_raw:,.0f}",
        'ceiling7_total_beers_change': f"{(ceiling7_total_beers_raw - baseline_total_beers_raw):,.0f}",
        'ceiling7_total_beers_pct': f"{100*(ceiling7_total_beers_raw/baseline_total_beers_raw-1):.1f}",
        'ceiling7_profit': f"{ceiling7_profit_raw:,.0f}",
        'ceiling7_profit_change': f"{(ceiling7_profit_raw-baseline_profit_raw):,.0f}",
        'ceiling7_total_revenue': f"{ceiling_7['total_revenue']/1e6:.2f}",
        'ceiling7_total_revenue_pct': f"{100*(ceiling_7['total_revenue']/baseline['total_revenue']-1):.1f}",
        'ceiling7_profit_change_M': f"{(ceiling7_profit_raw-baseline_profit_raw)/1e6:.2f}",
        'ceiling7_profit_change_season': f"{(ceiling7_profit_raw-baseline_profit_raw)*games/1e6:.1f}",
        'ceiling7_profit_season_raw': f"{ceiling7_profit_raw}", # Raw for calculations in template
        'ceiling7_profit_per_game_M': f"{ceiling7_profit_raw/1e6:.2f}",
        
        # Welfare
        'baseline_consumer_surplus': f"{welfare_base['consumer_surplus']/1e6:.1f}",
        'baseline_producer_surplus': f"{welfare_base['producer_surplus']/1e6:.1f}",
        'baseline_externality_cost': f"{welfare_base['externality_cost']/1e6:.1f}",
        'baseline_social_welfare': f"{welfare_base['social_welfare']/1e6:.1f}",

        'ceiling7_consumer_surplus': f"{welfare_7['consumer_surplus']/1e6:.1f}",
        'ceiling7_consumer_surplus_change': f"{(welfare_7['consumer_surplus']-welfare_base['consumer_surplus'])/1e6:.1f}",
        'ceiling7_consumer_surplus_pct': f"{100*(welfare_7['consumer_surplus']/welfare_base['consumer_surplus']-1):.1f}",
        'ceiling7_producer_surplus': f"{welfare_7['producer_surplus']/1e6:.1f}",
        'ceiling7_producer_surplus_change': f"{(welfare_7['producer_surplus']-welfare_base['producer_surplus'])/1e6:.1f}",
        'ceiling7_producer_surplus_pct': f"{100*(welfare_7['producer_surplus']/welfare_base['producer_surplus']-1):.1f}",
        'ceiling7_externality_cost': f"{welfare_7['externality_cost']/1e6:.1f}",
        'ceiling7_externality_cost_change': f"{(welfare_7['externality_cost']-welfare_base['externality_cost'])/1e6:.1f}",
        'ceiling7_externality_cost_pct': f"{100*(welfare_7['externality_cost']/welfare_base['externality_cost']-1):.1f}",
        'ceiling7_social_welfare': f"{welfare_7['social_welfare']/1e6:.1f}",
        'ceiling7_social_welfare_change': f"{(welfare_7['social_welfare']-welfare_base['social_welfare'])/1e6:.1f}",
        'ceiling7_social_welfare_pct': f"{100*(welfare_7['social_welfare']/welfare_base['social_welfare']-1):.1f}",
        
        # Annual changes
        'ceiling7_consumer_surplus_change_annual': f"{(welfare_7['consumer_surplus']-welfare_base['consumer_surplus'])*games/1e6:.1f}",
        'ceiling7_externality_cost_change_annual': f"{(welfare_7['externality_cost']-welfare_base['externality_cost'])*games/1e6:.1f}",
        'ceiling7_social_welfare_change_annual': f"{(welfare_7['social_welfare']-welfare_base['social_welfare'])*games/1e6:.1f}",

        # Model Parameters (from config_loader)
        'experience_degradation_cost': f"{model.experience_degradation_cost:.1f}",
        'external_cost_per_beer': f"{external_cost_sum_raw:.2f}",
            'current_taxes_per_beer': f"{current_taxes_per_beer_raw:.2f}",
            'tax_coverage_pct': f"{current_taxes_per_beer_raw / external_cost_sum_raw * 100:.0f}",
            'pigouvian_gap': f"{pigouvian_gap_raw:.2f}",
            'pigouvian_revenue_annual': f"{pigouvian_gap_raw * baseline_total_beers_raw * games / 1e6:.1f}",
            'beer_cost_raw': f"{model.beer_cost:.2f}",        
            # Additional calculated values for policy.md.tpl
        
            'baseline_beer_minus_ceiling7': f"{baseline_beer - 7.0:.2f}",
        
            'beer_price_pct_change_from_baseline': f"{100*(1-7.0/baseline_beer):.0f}",
        
            'external_cost_sum_raw': f"{external_cost_sum_raw:.2f}",
        
            'current_taxes_per_beer_raw': f"{current_taxes_per_beer_raw:.2f}",
        
            'pigouvian_consumer_price': f"{baseline_beer + pigouvian_gap_raw:.2f}",
        
            'pigouvian_total_beers_raw': f"{pigouvian_total_beers_raw:,.0f}",
        
            'pigouvian_tax_revenue_k': f"{pigouvian_gov_revenue / 1e3:.0f}",
        
            'baseline_tax_revenue_k': f"{current_taxes_per_beer_raw * baseline_total_beers_raw / 1e3:.0f}",
        
            'ceiling7_tax_revenue_k': f"{current_taxes_per_beer_raw * ceiling7_total_beers_raw / 1e3:.0f}", # Assuming sales tax rate applies to the $7, not just the pre-tax part
        
            'baseline_profit_per_game_M': f"{baseline_profit_raw/1e6:.2f}",
        
            'ceiling7_profit_per_game_M': f"{ceiling7_profit_raw/1e6:.2f}",
        
            'ceiling7_profit_change_M': f"{(ceiling7_profit_raw - baseline_profit_raw)/1e6:.2f}",
        
            'ceiling7_consumer_surplus_change_annual': f"{(welfare_7['consumer_surplus']-welfare_base['consumer_surplus'])*games/1e6:.1f}",
        
            'ceiling7_externality_cost_change_annual': f"{(welfare_7['externality_cost']-welfare_base['externality_cost'])*games/1e6:.1f}",
        
            'ceiling7_social_welfare_change_annual': f"{(welfare_7['social_welfare']-welfare_base['social_welfare'])*games/1e6:.1f}",
        
            'ceiling7_profit_loss_annual_M': f"{(ceiling7_profit_raw-baseline_profit_raw)*games/1e6 * -1:.0f}", # Absolute positive value for loss
        
        
    }

    return {
        # Baseline
        'baseline_ticket': f"{baseline_ticket:.2f}",
        'baseline_beer': f"{baseline_beer:.2f}",
        'baseline_attendance': f"{baseline['attendance']:,.0f}",
        'baseline_beers_per_fan': f"{baseline['beers_per_fan']:.2f}",
        'baseline_profit_season': f"{baseline_profit_raw*games/1e6:.1f}",
        'baseline_total_beers': f"{baseline_total_beers_raw:,.0f}",
        'baseline_profit_season_raw': f"{baseline_profit_raw}", # Raw for calculations in template

        # $7 ceiling
        'ceiling7_ticket': f"{ceiling_7_ticket:.2f}",
        'ceiling7_ticket_increase': f"{(ceiling_7_ticket - baseline_ticket):.2f}", # Absolute increase
        'ceiling7_ticket_pct': f"{100*(ceiling_7_ticket/baseline_ticket-1):.1f}",
        'ceiling7_attendance': f"{ceiling_7['attendance']:,.0f}",
        'ceiling7_attendance_change': f"{(ceiling_7['attendance'] - baseline['attendance']):,.0f}",
        'ceiling7_attendance_pct': f"{100*(ceiling_7['attendance']/baseline['attendance']-1):.1f}",
        'ceiling7_beers_per_fan': f"{ceiling_7['beers_per_fan']:.2f}",
        'ceiling7_beers_per_fan_pct': f"{100*(ceiling_7['beers_per_fan']/baseline['beers_per_fan']-1):.1f}",
        'ceiling7_total_beers': f"{ceiling7_total_beers_raw:,.0f}",
        'ceiling7_total_beers_change': f"{(ceiling7_total_beers_raw - baseline_total_beers_raw):,.0f}",
        'ceiling7_total_beers_pct': f"{100*(ceiling7_total_beers_raw/baseline_total_beers_raw-1):.1f}",
        'ceiling7_profit': f"{ceiling7_profit_raw:,.0f}",
        'ceiling7_profit_change': f"{(ceiling7_profit_raw-baseline_profit_raw):,.0f}",
        'ceiling7_profit_change_season': f"{(ceiling7_profit_raw-baseline_profit_raw)*games/1e6:.1f}",
        'ceiling7_profit_season_raw': f"{ceiling7_profit_raw}", # Raw for calculations in template
        
        # Welfare
        'baseline_consumer_surplus': f"{welfare_base['consumer_surplus']/1e6:.1f}",
        'baseline_producer_surplus': f"{welfare_base['producer_surplus']/1e6:.1f}",
        'baseline_externality_cost': f"{welfare_base['externality_cost']/1e6:.1f}",
        'baseline_social_welfare': f"{welfare_base['social_welfare']/1e6:.1f}",

        'ceiling7_consumer_surplus': f"{welfare_7['consumer_surplus']/1e6:.1f}",
        'ceiling7_consumer_surplus_change': f"{(welfare_7['consumer_surplus']-welfare_base['consumer_surplus'])/1e6:.1f}",
        'ceiling7_consumer_surplus_pct': f"{100*(welfare_7['consumer_surplus']/welfare_base['consumer_surplus']-1):.1f}",
        'ceiling7_producer_surplus': f"{welfare_7['producer_surplus']/1e6:.1f}",
        'ceiling7_producer_surplus_change': f"{(welfare_7['producer_surplus']-welfare_base['producer_surplus'])/1e6:.1f}",
        'ceiling7_producer_surplus_pct': f"{100*(welfare_7['producer_surplus']/welfare_base['producer_surplus']-1):.1f}",
        'ceiling7_externality_cost': f"{welfare_7['externality_cost']/1e6:.1f}",
        'ceiling7_externality_cost_change': f"{(welfare_7['externality_cost']-welfare_base['externality_cost'])/1e6:.1f}",
        'ceiling7_externality_cost_pct': f"{100*(welfare_7['externality_cost']/welfare_base['externality_cost']-1):.1f}",
        'ceiling7_social_welfare': f"{welfare_7['social_welfare']/1e6:.1f}",
        'ceiling7_social_welfare_change': f"{(welfare_7['social_welfare']-welfare_base['social_welfare'])/1e6:.1f}",
        'ceiling7_social_welfare_pct': f"{100*(welfare_7['social_welfare']/welfare_base['social_welfare']-1):.1f}",

        # Model Parameters (from config_loader)
        'experience_degradation_cost': f"{model.experience_degradation_cost:.1f}",
        'external_cost_per_beer': f"{full_config['external_costs']['crime'] + full_config['external_costs']['health']:.2f}",
        'current_taxes_per_beer': f"{current_taxes_per_beer_raw:.2f}",
        'tax_coverage_pct': f"{current_taxes_per_beer_raw / (full_config['external_costs']['crime'] + full_config['external_costs']['health']) * 100:.0f}",
        'pigouvian_gap': f"{pigouvian_gap_raw:.2f}",
        'pigouvian_revenue_annual': f"{pigouvian_gap_raw * baseline_total_beers_raw * games / 1e6:.1f}",
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

    templates_dir = Path('docs/templates')
    docs_dir = Path('docs')
    updated = []

    if not templates_dir.exists():
        print(f"Error: templates directory not found at {templates_dir}")
        return

    for tpl_file in templates_dir.glob('*.md.tpl'):
        output_filepath = docs_dir / tpl_file.name.replace('.tpl', '')
        
        with open(tpl_file, 'r') as f:
            content = f.read()

        original_content_of_tpl = content # Keep original to detect changes

        # Replace all {{ key }} with values
        for key, value in values.items():
            placeholder = f"{{{{ {key} }}}}"
            content = content.replace(placeholder, value)

        # Only write if content has changed (e.g., values injected)
        # Or if the target file doesn't exist yet
        write_needed = True
        if output_filepath.exists():
            with open(output_filepath, 'r') as f:
                existing_content = f.read()
            if existing_content == content:
                write_needed = False

        if write_needed:
            with open(output_filepath, 'w') as f:
                f.write(content)
            updated.append(output_filepath.name)
            print(f"  ✓ {output_filepath.name}")

    if updated:
        print(f"\n✓ Updated {len(updated)} files")
    else:
        print("\n- No files needed updating")

    # Check for remaining placeholders in generated files (should be none)
    remaining_files = []
    for mdfile in docs_dir.glob('*.md'):
        if mdfile.name == 'README.md': # Exclude docs/README.md from placeholder check
            continue
        with open(mdfile, 'r') as f:
            content = f.read()
        placeholders = re.findall(r'\{\{\s*\w+\s*\}\}', content)
        if placeholders:
            remaining_files.append((mdfile.name, placeholders))

    if remaining_files:
        print(f"\n⚠️  {len(remaining_files)} files still have placeholders (should not happen for generated files):")
        for fname, phs in remaining_files[:3]:
            print(f"  {fname}: {len(phs)} placeholders")
    else:
        print("\n✓ No remaining placeholders in generated docs!")

if __name__ == '__main__':
    main()
