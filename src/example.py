"""
Example script demonstrating basic usage of the beer price control model.

Run this to see a simple simulation without the Streamlit interface.
"""


from .model import StadiumEconomicModel
from .simulation import BeerPriceControlSimulator


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
        ticket_elasticity=-0.625,  # midpoint of -0.49 to -0.76
        beer_elasticity=-0.965,  # midpoint of -0.79 to -1.14
        ticket_cost=20.0,
        beer_cost=2.0,
        consumer_income=200.0,
        alpha=1.5,
        beta=3.0,
    )
    print("✓ Model initialized")
    print()

    # Create simulator
    simulator = BeerPriceControlSimulator(model)

    # Run all scenarios
    print("Running policy scenarios...")
    print("  - Baseline (Profit Max)")
    print("  - Current Observed Prices")
    print("  - Price Ceiling ($8)")
    print("  - Price Floor ($15)")
    print("  - Beer Ban")
    print("  - Social Optimum")
    print()

    results = simulator.run_all_scenarios(
        price_ceiling=8.0, price_floor=15.0, crime_cost_per_beer=2.5, health_cost_per_beer=1.5
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
    social_opt_row = results[results["scenario"] == "Social Optimum"].iloc[0]
    beer_ban_row = results[results["scenario"] == "Beer Ban"].iloc[0]

    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print()

    print("1. PROFIT MAXIMIZATION vs. SOCIAL OPTIMUM")
    print(f"   Profit Max Beer Price:  ${baseline_row['beer_price']:.2f}")
    print(f"   Social Opt Beer Price:  ${social_opt_row['beer_price']:.2f}")
    print(
        f"   Difference:             ${social_opt_row['beer_price'] - baseline_row['beer_price']:.2f}"
    )
    print()
    print(
        f"   Stadium profit loss at social optimum: ${baseline_row['profit'] - social_opt_row['profit']:,.0f}"
    )
    print(
        f"   Social welfare gain:                   ${social_opt_row['social_welfare'] - baseline_row['social_welfare']:,.0f}"
    )
    print()

    print("2. BEER BAN IMPACTS")
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

    print("3. ELASTICITY IMPLICATIONS")
    print(f"   Ticket demand elasticity: {model.ticket_elasticity:.2f} (inelastic)")
    print(f"   Beer demand elasticity:   {model.beer_elasticity:.2f} (inelastic)")
    print("   → Teams can raise prices without large quantity reductions")
    print("   → Price controls will have limited impact on consumption")
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
    print("For interactive exploration, run: streamlit run src/app.py")
    print()


if __name__ == "__main__":
    main()
