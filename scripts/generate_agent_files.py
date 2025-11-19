#!/usr/bin/env python3
"""
Generate CLAUDE.md and GEMINI.md from templates/AGENTS.md.tpl,
injecting live model values.

Usage:
    python scripts/generate_agent_files.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel

def generate_values():
    """Run model and return values dict for template substitution"""
    model = StadiumEconomicModel()
    
    # Run simulations
    baseline_ticket, baseline_beer, baseline = model.optimal_pricing()
    ceiling_7_ticket, ceiling_7_beer, ceiling_7 = model.optimal_pricing(beer_price_control=7.0)
    
    # Calculate welfare stats for ceiling 7
    welfare_base = model.social_welfare(baseline_ticket, baseline_beer)
    welfare_7 = model.social_welfare(ceiling_7_ticket, ceiling_7_beer)

    return {
        'ceiling7_ticket_increase': f"{(ceiling_7_ticket - baseline_ticket):.2f}",
        'ceiling7_ticket_pct': f"{100*(ceiling_7_ticket/baseline_ticket-1):.1f}",
        'ceiling7_attendance_pct': f"{100*(1 - ceiling_7['attendance']/baseline['attendance']):.1f}", # "falls X%"
        'ceiling7_welfare_pct': f"{100*(welfare_7['social_welfare']/welfare_base['social_welfare']-1):.1f}",
        'ceiling7_externality_pct': f"{100*(welfare_7['externality_cost']/welfare_base['externality_cost']-1):.0f}",
        'experience_degradation_cost': f"{model.experience_degradation_cost:.1f}"
    }

def main():
    template_path = Path("templates/AGENTS.md.tpl")
    if not template_path.exists():
        print("Error: templates/AGENTS.md.tpl not found.")
        return

    # 1. Generate dynamic values
    print("Generating model values...")
    values = generate_values()
    
    # 2. Read template
    with open(template_path, "r") as f:
        content = f.read()
    
    # 3. Inject values
    for key, val in values.items():
        content = content.replace(f"{{{{ {key} }}}}", val)
    
    lines = content.splitlines(keepends=True)

    # 4. Split content by agent
    claude_content = []
    gemini_content = []
    
    mode = "NONE" 
    header = "<!-- This file is auto-generated from templates/AGENTS.md.tpl. Do not edit directly. -->\n\n"
    claude_content.append(header)
    gemini_content.append(header)

    for line in lines:
        stripped = line.strip()
        
        if stripped == "<!--AGENT: ALL-->":
            mode = "ALL"
            continue
        elif stripped == "<!--AGENT: CLAUDE-->":
            mode = "CLAUDE"
            continue
        elif stripped == "<!--AGENT: GEMINI-->":
            mode = "GEMINI"
            continue
            
        if mode == "ALL":
            claude_content.append(line)
            gemini_content.append(line)
        elif mode == "CLAUDE":
            claude_content.append(line)
        elif mode == "GEMINI":
            gemini_content.append(line)

    # 5. Write output files
    with open("CLAUDE.md", "w") as f:
        f.writelines(claude_content)
    print("✓ Generated CLAUDE.md")

    with open("GEMINI.md", "w") as f:
        f.writelines(gemini_content)
    print("✓ Generated GEMINI.md")

if __name__ == "__main__":
    main()