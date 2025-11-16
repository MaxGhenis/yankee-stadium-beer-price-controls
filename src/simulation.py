"""
Simulation engine for beer price control scenarios at Yankee Stadium.

Compares different policy interventions:
- Baseline (current market prices)
- Price ceiling (maximum beer price)
- Price floor (minimum beer price)
- Beer ban (zero sales)
- Alternative pricing strategies
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from model import StadiumEconomicModel


class BeerPriceControlSimulator:
    """
    Simulates impacts of different beer pricing policies.
    """

    def __init__(self, model: StadiumEconomicModel):
        """
        Initialize simulator with economic model.

        Args:
            model: StadiumEconomicModel instance
        """
        self.model = model

    def run_scenario(self,
                    scenario_name: str,
                    beer_price_min: float = None,
                    beer_price_max: float = None,
                    beer_banned: bool = False,
                    crime_cost_per_beer: float = 2.50,
                    health_cost_per_beer: float = 1.50) -> Dict:
        """
        Run a single policy scenario.

        Args:
            scenario_name: Name of scenario
            beer_price_min: Minimum beer price (floor)
            beer_price_max: Maximum beer price (ceiling)
            beer_banned: Whether beer sales are banned
            crime_cost_per_beer: External crime cost per beer
            health_cost_per_beer: External health cost per beer

        Returns:
            Dict with all key metrics
        """
        if beer_banned:
            # No beer allowed
            ticket_price = self.model.base_ticket_price
            # For welfare calculations, use a high price but not infinity
            beer_price = self.model.base_beer_price  # Will be 0 quantity anyway

            # Calculate attendance with beer unavailable (cross-effect applies)
            attendance = self.model._attendance_demand(ticket_price, 0)

            result = {
                'attendance': attendance,
                'beers_per_fan': 0,
                'total_beers': 0,
                'ticket_revenue': ticket_price * attendance,
                'beer_revenue': 0,
                'total_revenue': ticket_price * attendance,
                'ticket_costs': self.model.ticket_cost * attendance,
                'beer_costs': 0,
                'total_costs': self.model.ticket_cost * attendance,
                'profit': ticket_price * attendance - self.model.ticket_cost * attendance
            }

        elif beer_price_min is not None and beer_price_max is not None:
            # Both constraints - use the one that binds
            beer_price = (beer_price_min + beer_price_max) / 2
            ticket_price, beer_price, result = self.model.optimal_pricing(
                beer_price_control=beer_price
            )
        elif beer_price_min is not None:
            # Price floor
            ticket_price, beer_price, result = self.model.optimal_pricing()
            if beer_price < beer_price_min:
                # Floor binds, re-optimize
                ticket_price, beer_price, result = self.model.optimal_pricing(
                    beer_price_control=beer_price_min
                )
        elif beer_price_max is not None:
            # Price ceiling
            ticket_price, beer_price, result = self.model.optimal_pricing()
            if beer_price > beer_price_max:
                # Ceiling binds, re-optimize
                ticket_price, beer_price, result = self.model.optimal_pricing(
                    beer_price_control=beer_price_max
                )
        else:
            # No constraints - optimal pricing
            ticket_price, beer_price, result = self.model.optimal_pricing()

        # Calculate welfare metrics
        welfare = self.model.social_welfare(
            ticket_price,
            beer_price,
            crime_cost_per_beer,
            health_cost_per_beer
        )

        # Combine results
        output = {
            'scenario': scenario_name,
            'ticket_price': ticket_price,
            'beer_price': beer_price,
            'attendance': result['attendance'],
            'beers_per_fan': result['beers_per_fan'],
            'total_beers': result['total_beers'],
            'ticket_revenue': result['ticket_revenue'],
            'beer_revenue': result['beer_revenue'],
            'total_revenue': result['total_revenue'],
            'profit': result['profit'],
            'consumer_surplus': welfare['consumer_surplus'],
            'producer_surplus': welfare['producer_surplus'],
            'externality_cost': welfare['externality_cost'],
            'social_welfare': welfare['social_welfare'],
            'crime_cost_per_beer': crime_cost_per_beer,
            'health_cost_per_beer': health_cost_per_beer
        }

        return output

    def run_all_scenarios(self,
                         price_ceiling: float = 8.0,
                         price_floor: float = 15.0,
                         crime_cost_per_beer: float = 2.50,
                         health_cost_per_beer: float = 1.50) -> pd.DataFrame:
        """
        Run all standard scenarios.

        Args:
            price_ceiling: Maximum beer price for ceiling scenario
            price_floor: Minimum beer price for floor scenario
            crime_cost_per_beer: External crime cost per beer
            health_cost_per_beer: External health cost per beer

        Returns:
            DataFrame with results from all scenarios
        """
        scenarios = []

        # 1. Baseline (unrestricted profit maximization)
        baseline = self.run_scenario(
            "Baseline (Profit Max)",
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )
        scenarios.append(baseline)

        # 2. Current observed prices (for comparison)
        current = self.run_scenario(
            "Current Observed Prices",
            beer_price_min=self.model.base_beer_price,
            beer_price_max=self.model.base_beer_price,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )
        scenarios.append(current)

        # 3. Price ceiling
        ceiling = self.run_scenario(
            f"Price Ceiling (${price_ceiling})",
            beer_price_max=price_ceiling,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )
        scenarios.append(ceiling)

        # 4. Price floor
        floor = self.run_scenario(
            f"Price Floor (${price_floor})",
            beer_price_min=price_floor,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )
        scenarios.append(floor)

        # 5. Beer ban
        ban = self.run_scenario(
            "Beer Ban",
            beer_banned=True,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )
        scenarios.append(ban)

        # 6. Social optimum (maximize social welfare)
        social_opt = self._find_social_optimum(crime_cost_per_beer, health_cost_per_beer)
        scenarios.append(social_opt)

        return pd.DataFrame(scenarios)

    def _find_social_optimum(self,
                            crime_cost_per_beer: float,
                            health_cost_per_beer: float) -> Dict:
        """
        Find prices that maximize social welfare (not just profit).

        SW = CS + PS - Externalities
        """
        from scipy.optimize import minimize

        def objective(prices):
            ticket_p, beer_p = prices
            if beer_p < 0:
                return 1e10  # penalty
            welfare = self.model.social_welfare(
                ticket_p,
                beer_p,
                crime_cost_per_beer,
                health_cost_per_beer
            )
            return -welfare['social_welfare']  # minimize negative SW

        result = minimize(
            objective,
            x0=[self.model.base_ticket_price, self.model.base_beer_price],
            bounds=[(10, 200), (0, 50)],
            method='L-BFGS-B'
        )

        optimal_ticket = result.x[0]
        optimal_beer = result.x[1]

        return self.run_scenario(
            "Social Optimum",
            beer_price_min=optimal_beer,
            beer_price_max=optimal_beer,
            crime_cost_per_beer=crime_cost_per_beer,
            health_cost_per_beer=health_cost_per_beer
        )

    def sensitivity_analysis(self,
                           parameter_name: str,
                           values: List[float],
                           crime_cost_per_beer: float = 2.50,
                           health_cost_per_beer: float = 1.50) -> pd.DataFrame:
        """
        Run sensitivity analysis over a parameter.

        Args:
            parameter_name: Name of parameter to vary
                ('ticket_elasticity', 'beer_elasticity', 'crime_cost', 'health_cost')
            values: List of values to try
            crime_cost_per_beer: External crime cost per beer
            health_cost_per_beer: External health cost per beer

        Returns:
            DataFrame with results across parameter values
        """
        results = []

        for value in values:
            # Update model parameter
            if parameter_name == 'ticket_elasticity':
                original = self.model.ticket_elasticity
                self.model.ticket_elasticity = value
            elif parameter_name == 'beer_elasticity':
                original = self.model.beer_elasticity
                self.model.beer_elasticity = value
            elif parameter_name == 'crime_cost':
                crime_cost_per_beer = value
            elif parameter_name == 'health_cost':
                health_cost_per_beer = value
            else:
                raise ValueError(f"Unknown parameter: {parameter_name}")

            # Run baseline scenario
            scenario = self.run_scenario(
                f"{parameter_name}={value}",
                crime_cost_per_beer=crime_cost_per_beer,
                health_cost_per_beer=health_cost_per_beer
            )
            scenario[parameter_name] = value
            results.append(scenario)

            # Restore original value
            if parameter_name == 'ticket_elasticity':
                self.model.ticket_elasticity = original
            elif parameter_name == 'beer_elasticity':
                self.model.beer_elasticity = original

        return pd.DataFrame(results)

    def calculate_comparative_statics(self,
                                     df: pd.DataFrame,
                                     baseline_scenario: str = "Current Observed Prices") -> pd.DataFrame:
        """
        Calculate changes relative to baseline scenario.

        Args:
            df: DataFrame with scenario results
            baseline_scenario: Name of baseline scenario

        Returns:
            DataFrame with absolute and percentage changes
        """
        baseline = df[df['scenario'] == baseline_scenario].iloc[0]

        changes = df.copy()
        for col in df.columns:
            if col in ['scenario']:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                changes[f'{col}_change'] = df[col] - baseline[col]
                changes[f'{col}_pct_change'] = (
                    (df[col] - baseline[col]) / baseline[col] * 100
                )

        return changes

    def summary_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics across scenarios.

        Args:
            df: DataFrame with scenario results

        Returns:
            Dict with key summary stats
        """
        return {
            'mean_attendance': df['attendance'].mean(),
            'std_attendance': df['attendance'].std(),
            'mean_total_beers': df['total_beers'].mean(),
            'std_total_beers': df['total_beers'].std(),
            'mean_profit': df['profit'].mean(),
            'std_profit': df['profit'].std(),
            'mean_social_welfare': df['social_welfare'].mean(),
            'std_social_welfare': df['social_welfare'].std(),
            'profit_maximizing_scenario': df.loc[df['profit'].idxmax(), 'scenario'],
            'welfare_maximizing_scenario': df.loc[df['social_welfare'].idxmax(), 'scenario'],
            'lowest_externality_scenario': df.loc[df['externality_cost'].idxmin(), 'scenario']
        }
