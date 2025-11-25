"""
Generate charts showing how outcomes vary with beer price ceilings.

Creates comparative statics plots with beer price cap on x-axis.
"""

import sys

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import StadiumEconomicModel

# Set style
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 11


def simulate_price_ceilings(
    ceiling_range: np.ndarray,
    model: StadiumEconomicModel,
    crime_cost: float = 2.50,
    health_cost: float = 1.50,
) -> pd.DataFrame:
    """
    Simulate outcomes across range of beer price ceilings.

    Args:
        ceiling_range: Array of beer price ceiling values
        model: StadiumEconomicModel instance

    Returns:
        DataFrame with results for each ceiling level
    """
    results = []

    for ceiling in ceiling_range:
        # Model now handles binding vs non-binding automatically
        # Ceiling sets upper bound; if ceiling > optimal, optimizer chooses optimal
        ticket_price, beer_price, revenue = model.optimal_pricing(
            beer_price_control=ceiling, ceiling_mode=True
        )

        # Get welfare metrics
        # Temporarily override model's external costs
        original_crime = model.external_costs.get("crime", 2.50)
        original_health = model.external_costs.get("health", 1.50)
        model.external_costs["crime"] = crime_cost
        model.external_costs["health"] = health_cost

        try:
            welfare = model.social_welfare(ticket_price, beer_price)
        finally:
            model.external_costs["crime"] = original_crime
            model.external_costs["health"] = original_health
        results.append(
            {
                "beer_ceiling": ceiling,
                "ticket_price": ticket_price,
                "beer_price": beer_price,
                "attendance": revenue["attendance"],
                "beers_per_fan": revenue["beers_per_fan"],
                "total_beers": revenue["total_beers"],
                "ticket_revenue": revenue["ticket_revenue"],
                "beer_revenue": revenue["beer_revenue"],
                "total_revenue": revenue["total_revenue"],
                "profit": revenue["profit"],
                "consumer_surplus": welfare["consumer_surplus"],
                "producer_surplus": welfare["producer_surplus"],
                "externality_cost": welfare["externality_cost"],
                "social_welfare": welfare["social_welfare"],
            }
        )

    return pd.DataFrame(results)


def create_charts(df: pd.DataFrame, output_dir: Path = None):
    """
    Create comparative statics charts.

    Args:
        df: DataFrame with simulation results
        output_dir: Directory to save charts (if None, displays instead)
    """
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

    # Find equilibrium (model-predicted optimal, not observed)
    # This is where ceiling stops binding
    from model import StadiumEconomicModel

    temp_model = StadiumEconomicModel()
    _, equilibrium_beer, _ = temp_model.optimal_pricing()

    baseline_idx = np.argmin(np.abs(df["beer_ceiling"] - equilibrium_beer))
    baseline = df.iloc[baseline_idx]

    # Chart 1: Prices
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(df["beer_ceiling"], df["ticket_price"], "o-", color="#003087", linewidth=2)
    ax1.axhline(baseline["ticket_price"], color="gray", linestyle="--", alpha=0.5, label="Baseline")
    ax1.axvline(
        equilibrium_beer,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label=rf"Equilibrium ($\${equilibrium_beer:.2f})",
    )
    ax1.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Optimal Ticket Price ($)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "Stadium Response: Ticket Prices Rise as Beer Ceiling Tightens",
        fontsize=13,
        fontweight="bold",
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.plot(df["beer_ceiling"], df["beer_price"], "o-", color="#E4002B", linewidth=2)
    ax2.plot(df["beer_ceiling"], df["beer_ceiling"], "--", color="gray", alpha=0.5, label="Ceiling")
    ax2.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax2.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Actual Beer Price ($)", fontsize=12, fontweight="bold")
    ax2.set_title("Beer Price Tracks Ceiling (When Binding)", fontsize=13, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "prices.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'prices.png'}")
    else:
        plt.show()
    plt.close()

    # Chart 2: Quantities
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(df["beer_ceiling"], df["attendance"] / 1000, "o-", color="#003087", linewidth=2)
    ax1.axhline(
        baseline["attendance"] / 1000, color="gray", linestyle="--", alpha=0.5, label="Baseline"
    )
    ax1.axvline(
        equilibrium_beer,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label=rf"Equilibrium ($\${equilibrium_beer:.2f})",
    )
    ax1.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Attendance (thousands)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "Lower Beer Ceilings Reduce Attendance\n(Higher Tickets + Complementarity)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.plot(df["beer_ceiling"], df["total_beers"] / 1000, "o-", color="#E4002B", linewidth=2)
    ax2.axhline(
        baseline["total_beers"] / 1000, color="gray", linestyle="--", alpha=0.5, label="Baseline"
    )
    ax2.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax2.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Total Beer Consumption (thousands)", fontsize=12, fontweight="bold")
    ax2.set_title(
        "Lower Ceilings Increase Beer Consumption\n(Despite Lower Attendance)",
        fontsize=13,
        fontweight="bold",
    )
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "quantities.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'quantities.png'}")
    else:
        plt.show()
    plt.close()

    # Chart 3: Revenue (Stacked Area)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create stacked area chart
    ax.fill_between(
        df["beer_ceiling"],
        0,
        df["ticket_revenue"] / 1e6,
        color="#003087",
        alpha=0.7,
        label="Ticket Revenue",
    )
    ax.fill_between(
        df["beer_ceiling"],
        df["ticket_revenue"] / 1e6,
        (df["ticket_revenue"] + df["beer_revenue"]) / 1e6,
        color="#E4002B",
        alpha=0.7,
        label="Beer Revenue",
    )

    # Add total revenue line on top
    ax.plot(
        df["beer_ceiling"],
        df["total_revenue"] / 1e6,
        "k-",
        linewidth=2.5,
        label="Total Revenue",
        alpha=0.8,
    )

    ax.axvline(
        equilibrium_beer,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label=rf"Equilibrium (\${equilibrium_beer:.2f})",
    )

    ax.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue per Game ($ millions)", fontsize=12, fontweight="bold")
    ax.set_title(
        "Revenue Decomposition: Ticket vs Beer Revenue\n(Stacked Area Shows Components)",
        fontsize=13,
        fontweight="bold",
    )
    ax.legend(loc="best", fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "revenue.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'revenue.png'}")
    else:
        plt.show()
    plt.close()

    # Chart 4: Welfare Components
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Producer surplus (profit)
    ax1.plot(df["beer_ceiling"], df["profit"] / 1e6, "o-", color="#2ca02c", linewidth=2)
    ax1.axhline(baseline["profit"] / 1e6, color="gray", linestyle="--", alpha=0.5, label="Baseline")
    ax1.axvline(
        equilibrium_beer,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label=rf"Equilibrium ($\${equilibrium_beer:.2f})",
    )
    ax1.set_xlabel("Beer Price Ceiling ($)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Producer Surplus ($ millions)", fontsize=11, fontweight="bold")
    ax1.set_title("Stadium Profit Falls with Ceilings", fontsize=12, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Consumer surplus
    ax2.plot(df["beer_ceiling"], df["consumer_surplus"] / 1e6, "o-", color="#1f77b4", linewidth=2)
    ax2.axhline(
        baseline["consumer_surplus"] / 1e6,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label="Baseline",
    )
    ax2.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax2.set_xlabel("Beer Price Ceiling ($)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Consumer Surplus ($ millions)", fontsize=11, fontweight="bold")
    ax2.set_title(
        "Consumer Surplus Ambiguous\n(Cheaper Beer vs Higher Tickets)",
        fontsize=12,
        fontweight="bold",
    )
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # Externality cost
    ax3.plot(df["beer_ceiling"], df["externality_cost"] / 1e6, "o-", color="#d62728", linewidth=2)
    ax3.axhline(
        baseline["externality_cost"] / 1e6,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label="Baseline",
    )
    ax3.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax3.set_xlabel("Beer Price Ceiling ($)", fontsize=11, fontweight="bold")
    ax3.set_ylabel("Externality Cost ($ millions)", fontsize=11, fontweight="bold")
    ax3.set_title(
        "Externalities Rise with Lower Ceilings\n(More Consumption)", fontsize=12, fontweight="bold"
    )
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    # Social welfare
    ax4.plot(df["beer_ceiling"], df["social_welfare"] / 1e6, "o-", color="#9467bd", linewidth=2)
    ax4.axhline(
        baseline["social_welfare"] / 1e6, color="gray", linestyle="--", alpha=0.5, label="Baseline"
    )
    ax4.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax4.set_xlabel("Beer Price Ceiling ($)", fontsize=11, fontweight="bold")
    ax4.set_ylabel("Social Welfare ($ millions)", fontsize=11, fontweight="bold")
    ax4.set_title("Social Welfare: CS + PS - Externalities", fontsize=12, fontweight="bold")
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "welfare.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'welfare.png'}")
    else:
        plt.show()
    plt.close()

    # Chart 5: All welfare on one chart (stacked)
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        df["beer_ceiling"],
        df["consumer_surplus"] / 1e6,
        "o-",
        color="#1f77b4",
        linewidth=2,
        label="Consumer Surplus",
        markersize=6,
    )
    ax.plot(
        df["beer_ceiling"],
        df["producer_surplus"] / 1e6,
        "s-",
        color="#2ca02c",
        linewidth=2,
        label="Producer Surplus (Profit)",
        markersize=6,
    )
    ax.plot(
        df["beer_ceiling"],
        -df["externality_cost"] / 1e6,
        "^-",
        color="#d62728",
        linewidth=2,
        label="Externality Cost (negative)",
        markersize=6,
    )
    ax.plot(
        df["beer_ceiling"],
        df["social_welfare"] / 1e6,
        "D-",
        color="#9467bd",
        linewidth=3,
        label="Social Welfare (sum)",
        markersize=7,
    )

    ax.axhline(0, color="black", linestyle="-", alpha=0.3, linewidth=0.5)
    ax.axvline(12.5, color="gray", linestyle="--", alpha=0.5, label="Baseline ($12.50)")

    ax.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Welfare ($ millions per game)", fontsize=12, fontweight="bold")
    ax.set_title(
        "Welfare Decomposition: Lower Ceilings Hurt Stadium More Than They Help Consumers",
        fontsize=13,
        fontweight="bold",
    )
    ax.legend(loc="best", fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "welfare_combined.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'welfare_combined.png'}")
    else:
        plt.show()
    plt.close()

    # Chart 6: Beers per fan
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df["beer_ceiling"], df["beers_per_fan"], "o-", color="#ff7f0e", linewidth=2)
    ax.axhline(baseline["beers_per_fan"], color="gray", linestyle="--", alpha=0.5, label="Baseline")
    ax.axvline(12.5, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Beer Price Ceiling ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Beers per Fan", fontsize=12, fontweight="bold")
    ax.set_title(
        "Lower Ceilings Dramatically Increase Per-Fan Consumption", fontsize=13, fontweight="bold"
    )
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    if output_dir:
        plt.savefig(output_dir / "beers_per_fan.png", dpi=300, bbox_inches="tight")
        print(f"Saved: {output_dir / 'beers_per_fan.png'}")
    else:
        plt.show()
    plt.close()


def print_key_results(df: pd.DataFrame):
    """Print key results for specific ceiling levels."""
    baseline_idx = np.argmin(np.abs(df["beer_ceiling"] - 12.5))
    ceiling_7_idx = np.argmin(np.abs(df["beer_ceiling"] - 7.0))

    baseline = df.iloc[baseline_idx]
    ceiling_7 = df.iloc[ceiling_7_idx]

    print("\n" + "=" * 70)
    print("KEY RESULTS: $7 BEER CEILING vs BASELINE")
    print("=" * 70)

    print(f"\n{'Metric':<30} {'Baseline':<15} {'$7 Ceiling':<15} {'Change':<15}")
    print("-" * 70)

    metrics = [
        ("Beer Price", "beer_price", "$"),
        ("Ticket Price", "ticket_price", "$"),
        ("Attendance", "attendance", ""),
        ("Beers per Fan", "beers_per_fan", ""),
        ("Total Beers", "total_beers", ""),
        ("Total Revenue", "total_revenue", "$"),
        ("Profit", "profit", "$"),
        ("Consumer Surplus", "consumer_surplus", "$"),
        ("Externality Cost", "externality_cost", "$"),
        ("Social Welfare", "social_welfare", "$"),
    ]

    for name, col, prefix in metrics:
        base_val = baseline[col]
        ceil_val = ceiling_7[col]
        change = ceil_val - base_val
        pct_change = (change / base_val) * 100 if base_val != 0 else 0

        if prefix == "$" and abs(base_val) > 1000:
            # Format as millions for large dollar amounts
            print(
                f"{name:<30} ${base_val/1e6:>8.2f}M      ${ceil_val/1e6:>8.2f}M      {change/1e6:>+8.2f}M ({pct_change:>+5.1f}%)"
            )
        elif prefix == "$":
            print(
                f"{name:<30} ${base_val:>8.2f}       ${ceil_val:>8.2f}       ${change:>+8.2f} ({pct_change:>+5.1f}%)"
            )
        else:
            print(
                f"{name:<30} {base_val:>10,.0f}     {ceil_val:>10,.0f}     {change:>+10,.0f} ({pct_change:>+5.1f}%)"
            )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Initialize model with default parameters
    model = StadiumEconomicModel()

    # Range of beer price ceilings to analyze
    # From $0 (ban) to equilibrium (~$13) where ceiling stops binding
    model_temp = StadiumEconomicModel()
    _, equilibrium_price, _ = model_temp.optimal_pricing()
    ceilings = np.linspace(0.5, equilibrium_price, 26)  # $0.50 to equilibrium

    print("Simulating beer price ceilings from $5 to $20...")
    df = simulate_price_ceilings(ceilings, model, crime_cost=2.50, health_cost=1.50)

    print("\nGenerating charts...")
    output_dir = Path("charts")
    create_charts(df, output_dir)

    print_key_results(df)

    # Save data
    df.to_csv("charts/price_ceiling_analysis.csv", index=False)
    print("\nData saved to: charts/price_ceiling_analysis.csv")
    print("\nDone!")
