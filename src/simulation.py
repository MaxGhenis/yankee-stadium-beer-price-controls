"""
Simulation engine for beer price control scenarios at Yankee Stadium.

Compares different policy interventions:
- Baseline (current market prices)
- Price ceiling (maximum beer price)
- Price floor (minimum beer price)
- Beer ban (zero sales)
"""


import pandas as pd

from .model import StadiumEconomicModel


class BeerPriceControlSimulator:
    """Simulates impacts of different beer pricing policies."""

    def __init__(self, model: StadiumEconomicModel):
        self.model = model

    def run_scenario(
        self,
        scenario_name: str,
        beer_price_min: float = None,
        beer_price_max: float = None,
        beer_banned: bool = False,
        crime_cost_per_beer: float = 2.50,
        health_cost_per_beer: float = 1.50,
    ) -> dict:
        """Run a single policy scenario."""
        if beer_banned:
            ticket_price = self.model.base_ticket_price
            beer_price = self.model.base_beer_price  # For welfare calculation reference
            # Use a very high beer price to model beer being unavailable
            attendance = self.model.total_attendance(ticket_price, 1e6)

            result = {
                "attendance": attendance,
                "beers_per_fan": 0,
                "total_beers": 0,
                "ticket_revenue": ticket_price * attendance,
                "beer_revenue": 0,
                "total_revenue": ticket_price * attendance,
                "ticket_costs": self.model.ticket_cost * attendance,
                "beer_costs": 0,
                "internalized_costs": 0,
                "total_costs": self.model.ticket_cost * attendance,
                "profit": ticket_price * attendance - self.model.ticket_cost * attendance,
                "breakdown_by_type": {},
            }

        elif beer_price_min is not None and beer_price_max is not None:
            beer_price = (beer_price_min + beer_price_max) / 2
            ticket_price, beer_price, result = self.model.optimal_pricing(
                beer_price_control=beer_price
            )
        elif beer_price_min is not None:
            ticket_price, beer_price, result = self.model.optimal_pricing()
            if beer_price < beer_price_min:
                ticket_price, beer_price, result = self.model.optimal_pricing(
                    beer_price_control=beer_price_min, ceiling_mode=False
                )
        elif beer_price_max is not None:
            ticket_price, beer_price, result = self.model.optimal_pricing()
            if beer_price > beer_price_max:
                ticket_price, beer_price, result = self.model.optimal_pricing(
                    beer_price_control=beer_price_max
                )
        else:
            ticket_price, beer_price, result = self.model.optimal_pricing()

        # Calculate welfare metrics
        original_crime_cost = self.model.external_costs.get("crime", 2.50)
        original_health_cost = self.model.external_costs.get("health", 1.50)

        self.model.external_costs["crime"] = crime_cost_per_beer
        self.model.external_costs["health"] = health_cost_per_beer

        try:
            welfare = self.model.social_welfare(ticket_price, beer_price)
        finally:
            self.model.external_costs["crime"] = original_crime_cost
            self.model.external_costs["health"] = original_health_cost

        output = {
            "scenario": scenario_name,
            "ticket_price": ticket_price,
            "beer_price": beer_price,
            "attendance": result["attendance"],
            "beers_per_fan": result["beers_per_fan"],
            "total_beers": result["total_beers"],
            "ticket_revenue": result["ticket_revenue"],
            "beer_revenue": result["beer_revenue"],
            "total_revenue": result["total_revenue"],
            "profit": result["profit"],
            "consumer_surplus": welfare["consumer_surplus"],
            "producer_surplus": welfare["producer_surplus"],
            "externality_cost": welfare["externality_cost"],
            "social_welfare": welfare["social_welfare"],
            "crime_cost_per_beer": crime_cost_per_beer,
            "health_cost_per_beer": health_cost_per_beer,
        }

        if "breakdown_by_type" in result:
            breakdown = result["breakdown_by_type"]
            total_attendance = result["attendance"]
            if total_attendance > 0:
                drinker_attendance = breakdown.get("Drinker", {}).get("attendance", 0)
                nondrinker_attendance = breakdown.get("Non-Drinker", {}).get("attendance", 0)
                output["drinker_share"] = drinker_attendance / total_attendance
                output["nondrinker_share"] = nondrinker_attendance / total_attendance
                output["drinker_attendance"] = drinker_attendance
                output["nondrinker_attendance"] = nondrinker_attendance
                output["drinker_beers_per_fan"] = breakdown.get("Drinker", {}).get(
                    "beers_per_fan", 0
                )
                output["nondrinker_beers_per_fan"] = breakdown.get("Non-Drinker", {}).get(
                    "beers_per_fan", 0
                )

        return output

    def run_all_scenarios(
        self,
        price_ceiling: float = 8.0,
        crime_cost_per_beer: float = 2.50,
        health_cost_per_beer: float = 1.50,
    ) -> pd.DataFrame:
        """Run all standard scenarios."""
        scenarios = []

        baseline = self.run_scenario(
            "Baseline (Profit Max)",
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer,
        )
        scenarios.append(baseline)

        current = self.run_scenario(
            "Current Observed Prices",
            beer_price_min=self.model.base_beer_price,
            beer_price_max=self.model.base_beer_price,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer,
        )
        scenarios.append(current)

        ceiling = self.run_scenario(
            f"Price Ceiling (${price_ceiling})",
            beer_price_max=price_ceiling,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer,
        )
        scenarios.append(ceiling)

        ban = self.run_scenario(
            "Beer Ban",
            beer_banned=True,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer,
        )
        scenarios.append(ban)

        return pd.DataFrame(scenarios)

    def sensitivity_analysis(
        self,
        parameter_name: str,
        values: list[float],
        crime_cost_per_beer: float = 2.50,
        health_cost_per_beer: float = 1.50,
    ) -> pd.DataFrame:
        """Run sensitivity analysis over a parameter."""
        results = []

        for value in values:
            if parameter_name == "ticket_price_sensitivity":
                original = self.model.ticket_price_sensitivity
                self.model.ticket_price_sensitivity = value
            elif parameter_name == "crime_cost":
                crime_cost_per_beer = value
            elif parameter_name == "health_cost":
                health_cost_per_beer = value
            else:
                raise ValueError(f"Unknown parameter: {parameter_name}")

            scenario = self.run_scenario(
                f"{parameter_name}={value}",
                crime_cost_per_beer=crime_cost_per_beer,
                health_cost_per_beer=health_cost_per_beer,
            )
            scenario[parameter_name] = value
            results.append(scenario)

            if parameter_name == "ticket_price_sensitivity":
                self.model.ticket_price_sensitivity = original

        return pd.DataFrame(results)

    def calculate_comparative_statics(
        self, df: pd.DataFrame, baseline_scenario: str = "Current Observed Prices"
    ) -> pd.DataFrame:
        """Calculate changes relative to baseline scenario."""
        baseline = df[df["scenario"] == baseline_scenario].iloc[0]

        changes = df.copy()
        for col in df.columns:
            if col in ["scenario"]:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                changes[f"{col}_change"] = df[col] - baseline[col]
                changes[f"{col}_pct_change"] = (df[col] - baseline[col]) / baseline[col] * 100

        return changes

    def summary_statistics(self, df: pd.DataFrame) -> dict:
        """Calculate summary statistics across scenarios."""
        return {
            "mean_attendance": df["attendance"].mean(),
            "std_attendance": df["attendance"].std(),
            "mean_total_beers": df["total_beers"].mean(),
            "std_total_beers": df["total_beers"].std(),
            "mean_profit": df["profit"].mean(),
            "std_profit": df["profit"].std(),
            "mean_social_welfare": df["social_welfare"].mean(),
            "std_social_welfare": df["social_welfare"].std(),
            "profit_maximizing_scenario": df.loc[df["profit"].idxmax(), "scenario"],
            "welfare_maximizing_scenario": df.loc[df["social_welfare"].idxmax(), "scenario"],
            "lowest_externality_scenario": df.loc[df["externality_cost"].idxmin(), "scenario"],
        }
