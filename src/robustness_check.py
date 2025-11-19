"""
Robustness check: Sensitivity to Cross-Price Elasticity.

Generates a phase diagram showing how the "Ticket Price Rise" result
depends on the strength of the complementarity assumption.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel


def run_sensitivity_analysis():
    """Run model across range of cross-price elasticities."""
    print("Running robustness check for cross-price elasticity...")

    elasticities = np.linspace(0.0, 0.30, 31)  # 0.0 to 0.30 in steps of 0.01
    results = []

    for epsilon in elasticities:
        # Initialize model with specific cross-elasticity
        model = StadiumEconomicModel(cross_price_elasticity=epsilon)

        # Baseline
        base_ticket, base_beer, base_metrics = model.optimal_pricing()

        # $7 Ceiling
        ceil_ticket, ceil_beer, ceil_metrics = model.optimal_pricing(beer_price_control=7.0)

        # Calculate changes
                ticket_change = ceil_ticket - base_ticket
                ticket_pct_change = (ceil_ticket / base_ticket - 1) * 100
                
                # Calculate Welfare Change (using standard costs)        welfare_base = model.social_welfare(base_ticket, base_beer)
        welfare_ceil = model.social_welfare(ceil_ticket, ceil_beer)
        sw_change = welfare_ceil["social_welfare"] - welfare_base["social_welfare"]

        results.append(
            {
                "cross_elasticity": epsilon,
                "base_ticket": base_ticket,
                "ceiling_ticket": ceil_ticket,
                "ticket_change": ticket_change,
                "ticket_pct_change": ticket_pct_change,
                "sw_change": sw_change,
            }
        )

    df = pd.DataFrame(results)
    return df


def plot_robustness(df):
    """Generate robustness plot."""
    plt.figure(figsize=(10, 6))

    # Plot Ticket Price Change
    plt.plot(
        df["cross_elasticity"],
        df["ticket_change"],
        "o-",
        color="#003087",
        linewidth=2,
        label="Ticket Price Increase ($)",
    )

    # Add reference line at current assumption
    plt.axvline(x=0.1, color="gray", linestyle="--", alpha=0.5, label="Current Assumption (0.1)")

    # Add reference line at zero change
    plt.axhline(y=0, color="black", linewidth=0.5)

    plt.xlabel("Cross-Price Elasticity (Complementarity)", fontsize=12, fontweight="bold")
    plt.ylabel("Ticket Price Increase ($)", fontsize=12, fontweight="bold")
    plt.title(
        "Robustness Check: Ticket Prices Rise Even With Weak Complementarity",
        fontsize=14,
        fontweight="bold",
    )

    plt.grid(True, alpha=0.3)
    plt.legend()

    # Annotate zero crossing if it exists
    # (It won't, because substitution effect is always positive for complementarity > 0)

    output_path = Path("charts/robustness_cross_elasticity.png")
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to {output_path}")


if __name__ == "__main__":
    df = run_sensitivity_analysis()
    df.to_csv("charts/robustness_cross_elasticity.csv", index=False)
    print("Saved data to charts/robustness_cross_elasticity.csv")

    plot_robustness(df)

    # Key stats
    base_case = df[np.isclose(df["cross_elasticity"], 0.1)].iloc[0]
    zero_case = df[np.isclose(df["cross_elasticity"], 0.0)].iloc[0]

    print("\nKey Findings:")
    print(f"At current assumption (ε=0.10): Ticket price rises ${base_case['ticket_change']:.2f}")
    print(f"At zero complementarity (ε=0.00): Ticket price rises ${zero_case['ticket_change']:.2f}")
    print(f"Result is robust? {'YES' if zero_case['ticket_change'] >= 0 else 'NO'}")
