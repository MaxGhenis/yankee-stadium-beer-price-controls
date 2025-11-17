"""
Heterogeneous consumer model for stadium beer pricing.

Key difference from base model: Fans have different beer preferences.
- Type 1 (60%): Non-drinkers/light drinkers (low α_beer)
- Type 2 (40%): Regular drinkers (high α_beer)

This captures the empirical fact that ~40% of fans consume alcohol.
"""

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class ConsumerType:
    """Represents a type of consumer with specific preferences."""
    name: str
    share: float  # Population share (must sum to 1 across types)
    alpha_beer: float  # Utility weight on beer
    alpha_experience: float  # Utility weight on stadium experience
    income: float  # Income/budget


class HeterogeneousStadiumModel:
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
        consumer_types: List[ConsumerType] = None,
        base_ticket_price: float = 80.0,
        base_beer_price: float = 12.5,
        ticket_cost: float = 3.5,
        beer_cost: float = 2.0,
        beer_excise_tax: float = 0.074,
        beer_sales_tax_rate: float = 0.08875,
        experience_degradation_cost: float = 250.0,
        cross_price_elasticity: float = 0.1,
        beer_demand_sensitivity: float = 0.30
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
            beer_excise_tax: Excise tax per beer
            beer_sales_tax_rate: Sales tax rate
            experience_degradation_cost: Internalized cost parameter
            cross_price_elasticity: Beer price effect on attendance
            beer_demand_sensitivity: Price sensitivity parameter
        """
        self.capacity = capacity
        self.base_ticket_price = base_ticket_price
        self.base_beer_price = base_beer_price
        self.ticket_cost = ticket_cost
        self.beer_cost = beer_cost
        self.beer_excise_tax = beer_excise_tax
        self.beer_sales_tax_rate = beer_sales_tax_rate
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

    def _create_default_types(self) -> List[ConsumerType]:
        """
        Create default 2-type model matching empirical data.

        From Lenk et al. (2010):
        - 60% don't drink (or drink very little)
        - 40% drink, averaging 2.5 beers
        """
        types = [
            ConsumerType(
                name="Non-Drinker",
                share=0.60,
                alpha_beer=1.0,  # Low enough that B = α/P - 1 < 0 at typical prices
                alpha_experience=3.0,  # High stadium experience value
                income=200.0
            ),
            ConsumerType(
                name="Drinker",
                share=0.40,
                alpha_beer=43.75,  # Calibrated so B = 2.5 at P=$12.50
                                    # FOC: α/(B+1) = P → 43.75/3.5 = 12.50 ✓
                alpha_experience=2.5,  # Moderate stadium experience value
                income=200.0
            )
        ]
        return types

    def _beers_consumed_by_type(
        self,
        beer_price: float,
        consumer_type: ConsumerType
    ) -> float:
        """
        Calculate beer consumption for a specific consumer type.

        Uses utility maximization: max α_beer·ln(B+1) subject to budget
        FOC: α_beer/(B+1) = P_beer
        Solution: B = α_beer/P_beer - 1

        But we also need to respect the semi-log aggregate demand structure.
        We'll use a hybrid: type-specific utility-based demand, but scaled to
        match aggregate semi-log behavior.
        """
        if beer_price <= 0:
            return 0

        # Utility-based demand for this type
        # B = α/(P) - 1, but enforce non-negative
        optimal_beers = max(0, consumer_type.alpha_beer / beer_price - 1)

        # Also apply price sensitivity (semi-log component)
        price_ratio = beer_price / self.base_beer_price
        sensitivity_factor = np.exp(-self.beer_demand_sensitivity * (beer_price - self.base_beer_price))

        # Combine: type-specific preference × price sensitivity
        total_beers = optimal_beers * sensitivity_factor

        return max(0, total_beers)

    def _attendance_by_type(
        self,
        ticket_price: float,
        beer_price: float,
        consumer_type: ConsumerType
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

        # Beer price cross-effect (types with high α_beer more affected)
        # Scale cross-elasticity by type's beer preference
        type_cross_elasticity = self.cross_price_elasticity * (consumer_type.alpha_beer / 2.0)
        if beer_price > 0:
            beer_ratio = beer_price / self.base_beer_price
            cross_effect = beer_ratio ** (-type_cross_elasticity)
        else:
            cross_effect = 0.95  # Small reduction for beer ban

        attendance = type_base_attendance * ticket_effect * cross_effect
        return attendance

    def total_attendance(self, ticket_price: float, beer_price: float) -> float:
        """Sum attendance across all consumer types."""
        total = sum(
            self._attendance_by_type(ticket_price, beer_price, ct)
            for ct in self.consumer_types
        )
        return min(total, self.capacity)

    def total_beer_consumption(
        self,
        ticket_price: float,
        beer_price: float
    ) -> Tuple[float, Dict[str, float]]:
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
                'attendance': attendance,
                'beers_per_fan': beers_per_fan,
                'total_beers': type_total
            }
            total += type_total

        return total, breakdown

    def stadium_revenue(self, ticket_price: float, beer_price: float) -> Dict[str, float]:
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
        internalized_costs = self.experience_degradation_cost * (beers_per_1000 ** 2)

        total_costs = ticket_costs + beer_costs + internalized_costs
        profit = total_revenue - total_costs

        # Tax revenue
        sales_tax_revenue = (beer_price - pre_tax_beer_price) * total_beers
        excise_tax_revenue = self.beer_excise_tax * total_beers

        return {
            'attendance': attendance,
            'beers_per_fan': beers_per_fan,
            'total_beers': total_beers,
            'ticket_revenue': ticket_revenue,
            'beer_revenue': beer_revenue,
            'total_revenue': total_revenue,
            'ticket_costs': ticket_costs,
            'beer_costs': beer_costs,
            'internalized_costs': internalized_costs,
            'total_costs': total_costs,
            'profit': profit,
            'sales_tax_revenue': sales_tax_revenue,
            'excise_tax_revenue': excise_tax_revenue,
            'breakdown_by_type': breakdown
        }

    def optimal_pricing(self, beer_price_control: float = None, ceiling_mode: bool = True) -> Tuple[float, float, Dict]:
        """Find profit-maximizing prices with heterogeneous consumers."""
        def objective(prices):
            ticket_p, beer_p = prices
            if beer_p < 0 or ticket_p < 0:
                return 1e10
            result = self.stadium_revenue(ticket_p, beer_p)
            return -result['profit']

        # Set bounds
        ticket_bounds = (self.ticket_cost, self.TICKET_PRICE_MAX)
        beer_min = self.beer_cost + self.BEER_PRICE_MIN_MARGIN
        beer_bounds = (beer_min, self.BEER_PRICE_MAX)

        # Apply ceiling if specified
        if beer_price_control is not None and ceiling_mode:
            if beer_price_control < beer_min:
                beer_bounds = (beer_price_control, beer_price_control)
            else:
                beer_bounds = (beer_min, beer_price_control)

        # Optimize
        result = minimize(
            objective,
            x0=[self.base_ticket_price, self.base_beer_price],
            bounds=[ticket_bounds, beer_bounds],
            method='L-BFGS-B'
        )

        optimal_ticket = result.x[0]
        optimal_beer = result.x[1]
        metrics = self.stadium_revenue(optimal_ticket, optimal_beer)

        return optimal_ticket, optimal_beer, metrics


# Quick test
if __name__ == "__main__":
    print("="*70)
    print("HETEROGENEOUS CONSUMER MODEL TEST")
    print("="*70)
    print()

    model = HeterogeneousStadiumModel()

    print("Consumer Types:")
    for ct in model.consumer_types:
        print(f"  {ct.name} ({ct.share*100:.0f}%): α_beer={ct.alpha_beer}, α_exp={ct.alpha_experience}")
    print()

    # Test at observed prices
    result_obs = model.stadium_revenue(80, 12.50)
    print(f"At observed prices ($80 tickets, $12.50 beer):")
    print(f"  Attendance: {result_obs['attendance']:,.0f}")
    print(f"  Total beers: {result_obs['total_beers']:,.0f}")
    print(f"  Beers/fan: {result_obs['beers_per_fan']:.2f}")
    print(f"  Profit: ${result_obs['profit']:,.0f}")
    print()

    # Breakdown by type
    print("Consumption by type:")
    for type_name, data in result_obs['breakdown_by_type'].items():
        print(f"  {type_name}: {data['beers_per_fan']:.2f} beers/fan")
    print()

    # Find optimal
    opt_ticket, opt_beer, opt_result = model.optimal_pricing()
    print(f"Model-predicted optimal:")
    print(f"  Beer: ${opt_beer:.2f} (observed: $12.50, gap: ${opt_beer - 12.50:+.2f})")
    print(f"  Ticket: ${opt_ticket:.2f} (observed: $80, gap: ${opt_ticket - 80:+.2f})")
    print(f"  Profit: ${opt_result['profit']:,.0f}")
    print()

    # Compare to homogeneous model
    from model import StadiumEconomicModel
    homo_model = StadiumEconomicModel()
    homo_opt_t, homo_opt_b, _ = homo_model.optimal_pricing()

    print("="*70)
    print("COMPARISON: Heterogeneous vs Homogeneous")
    print("="*70)
    print(f"Homogeneous model optimal beer: ${homo_opt_b:.2f}")
    print(f"Heterogeneous model optimal beer: ${opt_beer:.2f}")
    print(f"Observed: $12.50")
    print()

    if abs(opt_beer - 12.50) < abs(homo_opt_b - 12.50):
        improvement = abs(homo_opt_b - 12.50) - abs(opt_beer - 12.50)
        print(f"✓ Heterogeneous model is ${improvement:.2f} closer to observed price!")
    else:
        print(f"✗ Heterogeneous model didn't improve calibration")
