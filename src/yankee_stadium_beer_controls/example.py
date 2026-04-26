"""
Example script demonstrating basic usage of the beer price control model.

Run this to see a simple package-native simulation.
"""

from yankee_stadium_beer_controls.model import StadiumEconomicModel
from yankee_stadium_beer_controls.simulation import BeerPriceControlSimulator


def main():
    """Run basic simulation and print results."""

    print("=" * 80)
    print("YANKEE STADIUM BEER PRICE CONTROLS SIMULATION")
    print("=" * 80)
    print()

    # Initialize model with default parameters
    print("Initializing model with literature-based parameters...")
    model = StadiumEconomicModel(
        capacity=46537,
        base_ticket_price=80.0,
        base_beer_price=12.5,
        ticket_cost=3.5,
        beer_cost=2.0,
    )
    print("Model initialized")
    print()

    # Create simulator
    simulator = BeerPriceControlSimulator(model)

    # Run all scenarios
    print("Running policy scenarios...")
    print("  - Baseline (Profit Max)")
    print("  - Current Observed Prices")
    print("  - Price Ceiling ($8)")
    print("  - Beer Ban")
    print()

    results = simulator.run_all_scenarios(
        price_ceiling=8.0, crime_cost_per_beer=2.5, health_cost_per_beer=1.5
    )

    # Display results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    # Format and display key columns
    display_cols = [
        "scenario",
        "ticket_price",
        "beer_price",
        "attendance",
        "total_beers",
        "profit",
        "social_welfare",
    ]

    display_df = results[display_cols].copy()

    # Round numeric columns
    display_df["ticket_price"] = display_df["ticket_price"].round(2)
    display_df["beer_price"] = display_df["beer_price"].round(2)
    display_df["attendance"] = display_df["attendance"].round(0).astype(int)
    display_df["total_beers"] = display_df["total_beers"].round(0).astype(int)
    display_df["profit"] = display_df["profit"].round(0).astype(int)
    display_df["social_welfare"] = display_df["social_welfare"].round(0).astype(int)

    # Print table
    print(display_df.to_string(index=False))
    print()

    # Summary statistics
    summary = simulator.summary_statistics(results)

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Profit-Maximizing Scenario:    {summary['profit_maximizing_scenario']}")
    print(f"Welfare-Maximizing Scenario:   {summary['welfare_maximizing_scenario']}")
    print(f"Lowest Externality Scenario:   {summary['lowest_externality_scenario']}")
    print()

    # Key insights
    baseline_row = results[results["scenario"] == "Baseline (Profit Max)"].iloc[0]
    beer_ban_row = results[results["scenario"] == "Beer Ban"].iloc[0]

    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print()

    print("1. BEER BAN IMPACTS")
    print(
        f"   Revenue loss:          ${baseline_row['total_revenue'] - beer_ban_row['total_revenue']:,.0f}"
    )
    print(
        f"   Externality reduction: ${baseline_row['externality_cost'] - beer_ban_row['externality_cost']:,.0f}"
    )
    print(
        f"   Net social welfare:    ${beer_ban_row['social_welfare'] - baseline_row['social_welfare']:+,.0f}"
    )
    print()

    print("2. ENDOGENOUS CROSS-PRICE EFFECTS")
    print("   Beer price affects attendance through consumer surplus:")
    print("   - Cheaper beer -> higher drinker CS -> lower net cost -> more drinkers attend")
    print("   - Beer ceiling -> stadium raises tickets to compensate lost beer revenue")
    print()

    # Comparative statics
    print("=" * 80)
    print("CHANGES RELATIVE TO CURRENT PRICES")
    print("=" * 80)
    print()

    current_row = results[results["scenario"] == "Current Observed Prices"].iloc[0]

    for _, row in results.iterrows():
        if row["scenario"] == "Current Observed Prices":
            continue

        profit_change = row["profit"] - current_row["profit"]
        welfare_change = row["social_welfare"] - current_row["social_welfare"]
        beers_change = row["total_beers"] - current_row["total_beers"]

        print(f"{row['scenario']}:")
        print(f"  Profit change:         ${profit_change:+,.0f}")
        print(f"  Social welfare change: ${welfare_change:+,.0f}")
        print(f"  Beer consumption:      {beers_change:+,.0f} beers")
        print()

    print("=" * 80)
    print()
    print("For the web dashboard, run:")
    print("  uv run yankee-beer-web-data --output-dir web/public/data")
    print("  (cd web && npm run dev)")
    print()


if __name__ == "__main__":
    main()
