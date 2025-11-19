"""
Heterogeneous consumer model for stadium beer pricing.

Key difference from base model: Fans have different beer preferences.
- Type 1 (60%): Non-drinkers/light drinkers (low α_beer)
- Type 2 (40%): Regular drinkers (high α_beer)

This captures the empirical fact that ~40% of fans consume alcohol.
"""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from src.config_loader import load_full_config  # Import load_full_config to be available here


@dataclass
class ConsumerType:
    """Represents a type of consumer with specific preferences."""

    name: str
    share: float  # Population share (must sum to 1 across types)
    alpha_beer: float  # Utility weight on beer
    alpha_experience: float  # Utility weight on stadium experience
    income: float  # Income/budget


class StadiumEconomicModel:
    """
    Stadium model with heterogeneous consumer preferences.

    Extends base model by allowing different consumer types with varying
    beer preferences. This can help calibrate to observed prices by capturing
    the extensive margin (who drinks) vs intensive margin (how much).
    """

    # Optimization bounds
    TICKET_PRICE_MAX = 200.0
    BEER_PRICE_MAX = 30.0
    BEER_PRICE_MIN_MARGIN = 0.1

    def __init__(
        self,
        capacity: int = 46537,
        consumer_types: list[ConsumerType] = None,
        base_ticket_price: float = 80.0,
        base_beer_price: float = 12.5,
        ticket_cost: float = 3.5,
        beer_cost: float = 2.0,
        experience_degradation_cost: float = None,  # Auto-load from config.yaml if None
        cross_price_elasticity: float = 0.1,
        beer_demand_sensitivity: float = 0.30,
        # Compatibility parameters (ignored in heterogeneous model)
        ticket_elasticity: float = -0.625,
        beer_elasticity: float = -0.965,
        alpha: float = 1.5,
        beta: float = 3.0,
        consumer_income: float = 200.0,
        captive_demand_share: float = 0.5,
        capacity_constraint: float = 50000,
    ):
        """
        Initialize heterogeneous consumer model.

        Args:
            capacity: Stadium seating capacity
            consumer_types: List of ConsumerType objects (if None, creates default 2 types)
            base_ticket_price: Baseline ticket price
            base_beer_price: Baseline beer price
            ticket_cost: Marginal cost per ticket
            beer_cost: Marginal cost per beer
            experience_degradation_cost: Internalized cost parameter
            cross_price_elasticity: Beer price effect on attendance
            beer_demand_sensitivity: Price sensitivity parameter
        """
        self.capacity = capacity
        self.base_ticket_price = base_ticket_price
        self.base_beer_price = base_beer_price
        self.ticket_cost = ticket_cost
        self.beer_cost = beer_cost

        # Load full config to get taxes and external costs
        full_config = load_full_config()
        self.taxes = full_config.get("taxes", {})
        self.external_costs = full_config.get("external_costs", {})

        self.beer_excise_tax = (
            self.taxes.get("excise_federal", 0.0)
            + self.taxes.get("excise_state", 0.0)
            + self.taxes.get("excise_local", 0.0)
        )
        self.beer_sales_tax_rate = self.taxes.get("sales_tax_rate", 0.0) / 100

        # Load experience_degradation_cost from config if not specified
        if experience_degradation_cost is None:
            experience_degradation_cost = self._load_calibrated_internalized_cost()
        self.experience_degradation_cost = experience_degradation_cost

        self.cross_price_elasticity = cross_price_elasticity
        self.beer_demand_sensitivity = beer_demand_sensitivity

        # Default to 2-type model if not specified
        if consumer_types is None:
            self.consumer_types = self._create_default_types()
        else:
            self.consumer_types = consumer_types

        # Verify shares sum to 1
        total_share = sum(t.share for t in self.consumer_types)
        assert abs(total_share - 1.0) < 1e-6, f"Consumer shares must sum to 1, got {total_share}"

        # Baseline attendance (85% capacity)
        self.base_attendance = self.capacity * 0.85

        # Compatibility attributes for old tests
        self.ticket_elasticity = -0.625  # Average elasticity (for compatibility)
        self.beer_elasticity = -0.965  # Average elasticity (for compatibility)
        self.consumer_income = 200.0  # Average income (for compatibility)

    def _create_default_types(self) -> list[ConsumerType]:
        """
        Create default 2-type model with calibrated parameters from config.yaml.

        From Lenk et al. (2010):
        - 60% don't drink (or drink very little)
        - 40% drink, averaging 2.5 beers
        """
        try:
            from .config_loader import get_parameter
        except ImportError:
            from config_loader import get_parameter

        types = [
            ConsumerType(
                name="Non-Drinker",
                share=0.60,
                alpha_beer=get_parameter("alpha_beer_nondrinker", 1.0),
                alpha_experience=3.0,
                income=200.0,
            ),
            ConsumerType(
                name="Drinker",
                share=0.40,
                alpha_beer=get_parameter("alpha_beer_drinker", 43.75),
                alpha_experience=2.5,
                income=200.0,
            ),
        ]
        return types

    def _beers_consumed_by_type(self, beer_price: float, consumer_type: ConsumerType) -> float:
        """
        Calculate beer consumption for a specific consumer type.

        Uses utility-based demand with satiation:
        FOC: α_beer/(B+1) = P_beer → B = α_beer/P_beer - 1

        But capped at reasonable maximum (no one drinks 50+ beers).
        """
        # Special case: Free beer (P ≈ 0)
        if beer_price <= 0.01:
            # At P=0, utility-based formula gives infinity
            # Use empirical open-bar consumption instead
            # Data: Open bars average 5-6 drinks (wedding/tailgate data)
            # For heavy drinkers at baseball game: 6-7 beers reasonable
            FREE_BEER_CONSUMPTION = 6.5  # Based on open bar empirical data
            # Only drinkers (high alpha) consume at free price
            if consumer_type.alpha_beer > 10:
                return FREE_BEER_CONSUMPTION
            else:
                return 0

        # Normal case: Utility-based demand
        # FOC: α/(B+1) = P → B = α/P - 1
        optimal_beers = consumer_type.alpha_beer / beer_price - 1

        # Cap at physiological maximum
        MAX_BEERS_PHYSIOLOGICAL = 10.0

        # Return max of 0 and min of optimal/physiological limit
        return max(0, min(optimal_beers, MAX_BEERS_PHYSIOLOGICAL))

    def _attendance_by_type(
        self, ticket_price: float, beer_price: float, consumer_type: ConsumerType
    ) -> float:
        """
        Attendance for a specific consumer type.

        Each type decides whether to attend based on utility comparison.
        Types with higher beer preference affected more by beer prices.
        """
        # Baseline attendance for this type
        type_base_attendance = self.base_attendance * consumer_type.share

        # Ticket price effect (semi-log)
        ticket_sensitivity = 0.017  # Standard sensitivity
        ticket_effect = np.exp(-ticket_sensitivity * (ticket_price - self.base_ticket_price))

        # Beer price cross-effect (drinkers more affected than non-drinkers)
        # Use SAME cross-elasticity for all, but drinkers feel it more through utility
        # Don't scale by alpha (causes explosion at low prices!)
        if beer_price > 0:
            beer_ratio = beer_price / self.base_beer_price
            cross_effect = beer_ratio ** (-self.cross_price_elasticity)
        else:
            cross_effect = 0.95  # Small reduction for beer ban

        attendance = type_base_attendance * ticket_effect * cross_effect
        return min(
            attendance, self.capacity * consumer_type.share
        )  # Cap at type's share of capacity

    def total_attendance(self, ticket_price: float, beer_price: float) -> float:
        """Sum attendance across all consumer types."""
        total = sum(
            self._attendance_by_type(ticket_price, beer_price, ct) for ct in self.consumer_types
        )
        return min(total, self.capacity)

    def total_beer_consumption(
        self, ticket_price: float, beer_price: float
    ) -> tuple[float, dict[str, float]]:
        """
        Calculate total beer consumption across all types.

        Returns:
            (total_beers, breakdown_by_type)
        """
        breakdown = {}
        total = 0

        for ct in self.consumer_types:
            attendance = self._attendance_by_type(ticket_price, beer_price, ct)
            beers_per_fan = self._beers_consumed_by_type(beer_price, ct)
            type_total = attendance * beers_per_fan

            breakdown[ct.name] = {
                "attendance": attendance,
                "beers_per_fan": beers_per_fan,
                "total_beers": type_total,
            }
            total += type_total

        return total, breakdown

    def stadium_revenue(self, ticket_price: float, beer_price: float) -> dict[str, float]:
        """Calculate stadium revenues with heterogeneous consumers."""
        attendance = self.total_attendance(ticket_price, beer_price)
        total_beers, breakdown = self.total_beer_consumption(ticket_price, beer_price)

        # Calculate beers per fan (aggregate)
        beers_per_fan = total_beers / attendance if attendance > 0 else 0

        # Tax calculations (same as base model)
        pre_tax_beer_price = beer_price / (1 + self.beer_sales_tax_rate)
        stadium_beer_price = pre_tax_beer_price - self.beer_excise_tax

        # Revenues
        ticket_revenue = ticket_price * attendance
        beer_revenue = stadium_beer_price * total_beers
        total_revenue = ticket_revenue + beer_revenue

        # Costs
        ticket_costs = self.ticket_cost * attendance
        beer_costs = self.beer_cost * total_beers

        # Internalized costs
        beers_per_1000 = total_beers / 1000
        internalized_costs = self.experience_degradation_cost * (beers_per_1000**2)

        total_costs = ticket_costs + beer_costs + internalized_costs
        profit = total_revenue - total_costs

        # Tax revenue
        sales_tax_revenue = (beer_price - pre_tax_beer_price) * total_beers
        excise_tax_revenue = self.beer_excise_tax * total_beers

        return {
            "attendance": attendance,
            "beers_per_fan": beers_per_fan,
            "total_beers": total_beers,
            "ticket_revenue": ticket_revenue,
            "beer_revenue": beer_revenue,
            "total_revenue": total_revenue,
            "ticket_costs": ticket_costs,
            "beer_costs": beer_costs,
            "internalized_costs": internalized_costs,
            "total_costs": total_costs,
            "profit": profit,
            "sales_tax_revenue": sales_tax_revenue,
            "excise_tax_revenue": excise_tax_revenue,
            "breakdown_by_type": breakdown,
        }

    def optimal_pricing(
        self, beer_price_control: float = None, ceiling_mode: bool = True
    ) -> tuple[float, float, dict]:
        """Find profit-maximizing prices with heterogeneous consumers."""
        beer_min = self.beer_cost + self.BEER_PRICE_MIN_MARGIN
        ticket_bounds = (self.ticket_cost, self.TICKET_PRICE_MAX)

        # Step 1: Determine beer price (before optimization)
        if beer_price_control is not None:
            if ceiling_mode:
                # Get unconstrained beer optimum (cache to avoid recomputing)
                if not hasattr(self, "_unconstrained_beer_optimum"):

                    def objective_both(prices):
                        ticket_p, beer_p = prices
                        if beer_p < 0 or ticket_p < 0:
                            return 1e10
                        result = self.stadium_revenue(ticket_p, beer_p)
                        return -result["profit"]

                    unconstrained = minimize(
                        objective_both,
                        x0=[self.base_ticket_price, self.base_beer_price],
                        bounds=[ticket_bounds, (beer_min, self.BEER_PRICE_MAX)],
                        method="L-BFGS-B",
                    )
                    self._unconstrained_beer_optimum = unconstrained.x[1]

                # Beer price = min(ceiling, unconstrained_optimum)
                optimal_beer = min(beer_price_control, self._unconstrained_beer_optimum)
            else:
                # Fixed price mode
                optimal_beer = beer_price_control
        else:
            # No constraints - optimize both prices together
            def objective_both(prices):
                ticket_p, beer_p = prices
                if beer_p < 0 or ticket_p < 0:
                    return 1e10
                result = self.stadium_revenue(ticket_p, beer_p)
                return -result["profit"]

            result = minimize(
                objective_both,
                x0=[self.base_ticket_price, self.base_beer_price],
                bounds=[ticket_bounds, (beer_min, self.BEER_PRICE_MAX)],
                method="L-BFGS-B",
            )
            optimal_ticket = result.x[0]
            optimal_beer = result.x[1]
            metrics = self.stadium_revenue(optimal_ticket, optimal_beer)
            return optimal_ticket, optimal_beer, metrics

        # Step 2: Optimize ticket price given fixed beer price
        def objective_ticket(ticket_p):
            if ticket_p < 0:
                return 1e10
            result = self.stadium_revenue(ticket_p, optimal_beer)
            return -result["profit"]

        result = minimize(
            objective_ticket, x0=self.base_ticket_price, bounds=[ticket_bounds], method="L-BFGS-B"
        )

        optimal_ticket = result.x[0]
        metrics = self.stadium_revenue(optimal_ticket, optimal_beer)

        return optimal_ticket, optimal_beer, metrics

    def consumer_surplus(self, ticket_price: float, beer_price: float) -> float:
        """
        Calculate aggregate consumer surplus across heterogeneous types.

        CS = sum over types of (share × type_CS)
        Simplified approximation using elasticity formula.
        """
        attendance = self.total_attendance(ticket_price, beer_price)
        total_beers, _ = self.total_beer_consumption(ticket_price, beer_price)

        # Ticket CS (using average elasticity approximation)
        ticket_cs = (attendance * ticket_price) / (1 + (-0.625))

        # Beer CS (adjusted for heterogeneity - drinkers get more surplus)
        beer_cs = (total_beers * beer_price) / (1 + (-0.965) * 0.7) * 1.5

        return ticket_cs + beer_cs

    def producer_surplus(self, ticket_price: float, beer_price: float) -> float:
        """Calculate producer surplus (profit)."""
        result = self.stadium_revenue(ticket_price, beer_price)
        return result["profit"]

    def externality_cost(self, total_beers: float) -> float:
        """Calculate external costs from alcohol consumption."""
        crime_cost_per_beer = self.external_costs.get("crime", 2.50)
        health_cost_per_beer = self.external_costs.get("health", 1.50)
        return total_beers * (crime_cost_per_beer + health_cost_per_beer)

    def social_welfare(self, ticket_price: float, beer_price: float) -> dict[str, float]:
        """Calculate total social welfare including externalities."""
        cs = self.consumer_surplus(ticket_price, beer_price)
        ps = self.producer_surplus(ticket_price, beer_price)

        result = self.stadium_revenue(ticket_price, beer_price)
        ext_cost = self.externality_cost(result["total_beers"])

        sw = cs + ps - ext_cost

        return {
            "consumer_surplus": cs,
            "producer_surplus": ps,
            "externality_cost": ext_cost,
            "social_welfare": sw,
            "total_beers": result["total_beers"],
            "attendance": result["attendance"],
        }

    # Compatibility methods for old tests/code
    def _attendance_demand(self, ticket_price: float, beer_price: float) -> float:
        """Compatibility wrapper - use total_attendance()."""
        return self.total_attendance(ticket_price, beer_price)

    def _beers_per_fan_demand(self, beer_price: float, income: float) -> float:
        """
        Compatibility wrapper - returns average beers per fan across all types.
        """
        total_beers, _ = self.total_beer_consumption(self.base_ticket_price, beer_price)
        attendance = self.total_attendance(self.base_ticket_price, beer_price)
        return total_beers / attendance if attendance > 0 else 0

    def _load_calibrated_internalized_cost(self) -> float:
        """Load experience_degradation_cost from config.yaml."""
        try:
            from .config_loader import load_full_config
        except ImportError:
            from config_loader import load_full_config
        full_config = load_full_config()
        return full_config.get("calibration", {}).get("experience_degradation_cost", 62.28)


# Quick test
if __name__ == "__main__":
    print("=" * 70)
    print("HETEROGENEOUS CONSUMER MODEL TEST")
    print("=" * 70)
    print()

    model = StadiumEconomicModel()

    print("Consumer Types:")
    for ct in model.consumer_types:
        print(
            f"  {ct.name} ({ct.share*100:.0f}%): α_beer={ct.alpha_beer}, α_exp={ct.alpha_experience}"
        )
    print()

    # Test at observed prices
    result_obs = model.stadium_revenue(80, 12.50)
    print("At observed prices ($80 tickets, $12.50 beer):")
    print(f"  Attendance: {result_obs['attendance']:,.0f}")
    print(f"  Total beers: {result_obs['total_beers']:,.0f}")
    print(f"  Beers/fan: {result_obs['beers_per_fan']:.2f}")
    print(f"  Profit: ${result_obs['profit']:,.0f}")
    print()

    # Breakdown by type
    print("Consumption by type:")
    for type_name, data in result_obs["breakdown_by_type"].items():
        print(f"  {type_name}: {data['beers_per_fan']:.2f} beers/fan")
    print()

    # Find optimal
    opt_ticket, opt_beer, opt_result = model.optimal_pricing()
    print("Model-predicted optimal:")
    print(f"  Beer: ${opt_beer:.2f} (observed: $12.50, gap: ${opt_beer - 12.50:+.2f})")
    print(f"  Ticket: ${opt_ticket:.2f} (observed: $80, gap: ${opt_ticket - 80:+.2f})")
    print(f"  Profit: ${opt_result['profit']:,.0f}")
    print()

    # Compare to homogeneous model
    from model import StadiumEconomicModel

    homo_model = StadiumEconomicModel()
    homo_opt_t, homo_opt_b, _ = homo_model.optimal_pricing()

    print("=" * 70)
    print("COMPARISON: Heterogeneous vs Homogeneous")
    print("=" * 70)
    print(f"Homogeneous model optimal beer: ${homo_opt_b:.2f}")
    print(f"Heterogeneous model optimal beer: ${opt_beer:.2f}")
    print("Observed: $12.50")
    print()

    if abs(opt_beer - 12.50) < abs(homo_opt_b - 12.50):
        improvement = abs(homo_opt_b - 12.50) - abs(opt_beer - 12.50)
        print(f"✓ Heterogeneous model is ${improvement:.2f} closer to observed price!")
    else:
        print("✗ Heterogeneous model didn't improve calibration")
