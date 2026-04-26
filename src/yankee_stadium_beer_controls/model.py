"""
Heterogeneous consumer model for stadium beer pricing.

Key features:
- 2 consumer types: Non-drinkers (60%, alpha_beer=0.0) and Drinkers (40%, alpha_beer=43.75)
- Quasilinear utility: U = alpha * ln(B+1) + Y
- Beer demand from FOC: B = alpha/P - 1
- Beer consumer surplus: exact integral from utility function
- Endogenous cross-price effects: cheaper beer raises drinker CS, lowering
  their net cost of attendance, so more drinkers attend
- Attendance: semi-log in net cost (P_T - CS_beer)
- Total consumer surplus: A/lambda from semi-log demand in generalized price
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.optimize import minimize

from yankee_stadium_beer_controls.config_loader import get_parameter, load_full_config


@dataclass
class ConsumerType:
    """Represents a type of consumer with specific preferences."""

    name: str
    share: float  # Population share (must sum to 1 across types)
    alpha_beer: float  # Utility weight on beer


class StadiumEconomicModel:
    """
    Stadium model with heterogeneous consumer preferences and
    utility-consistent consumer surplus and attendance.
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
        experience_degradation_cost: float = None,
        ticket_price_sensitivity: float = None,
        beer_max_per_person: float = 6.5,
    ):
        self.capacity = capacity
        self.base_ticket_price = base_ticket_price
        self.base_beer_price = base_beer_price
        self.ticket_cost = ticket_cost
        self.beer_cost = beer_cost
        self.beer_max_per_person = beer_max_per_person

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

        if experience_degradation_cost is None:
            experience_degradation_cost = get_parameter("experience_degradation_cost", 62.28)
        self.experience_degradation_cost = experience_degradation_cost

        if ticket_price_sensitivity is None:
            ticket_price_sensitivity = get_parameter("ticket_price_sensitivity", 0.0078125)
        self.ticket_price_sensitivity = ticket_price_sensitivity

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

        # Precompute baseline CS_beer and net_cost per type
        self._baseline_cs_beer = {}
        self._baseline_net_cost = {}
        for ct in self.consumer_types:
            cs = self._beer_consumer_surplus(self.base_beer_price, ct)
            self._baseline_cs_beer[ct.name] = cs
            self._baseline_net_cost[ct.name] = self.base_ticket_price - cs

    def _create_default_types(self) -> list[ConsumerType]:
        """Create default 2-type model with calibrated parameters from the loaded config."""
        return [
            ConsumerType(
                name="Non-Drinker",
                share=0.60,
                alpha_beer=get_parameter("alpha_beer_nondrinker", 0.0),
            ),
            ConsumerType(
                name="Drinker",
                share=0.40,
                alpha_beer=get_parameter("alpha_beer_drinker", 43.75),
            ),
        ]

    def _beers_consumed_by_type(self, beer_price: float, consumer_type: ConsumerType) -> float:
        """
        Beer consumption for a specific consumer type.

        FOC: alpha/(B+1) = P --> B = alpha/P - 1, capped at [0, beer_max_per_person].
        """
        P = max(float(beer_price), 0.01)
        optimal_beers = consumer_type.alpha_beer / P - 1
        return max(0.0, min(optimal_beers, self.beer_max_per_person))

    def _beer_consumer_surplus(self, beer_price: float, consumer_type: ConsumerType) -> float:
        """
        Exact beer consumer surplus from quasilinear utility U = α·ln(B+1) + Y.

        Three cases:
        - Non-buyer (α ≤ P): CS = 0
        - Unconstrained (B < B_max): CS = α·ln(α/P) - (α - P)
        - Constrained at B_max: CS = α·ln(B_max+1) - P·B_max
        """
        alpha = consumer_type.alpha_beer
        P = max(float(beer_price), 0.01)

        # Non-buyer: α ≤ P means B = α/P - 1 ≤ 0
        if alpha <= P:
            return 0.0

        # Unconstrained optimal: B = α/P - 1
        optimal_beers = alpha / P - 1

        if optimal_beers <= self.beer_max_per_person:
            # Unconstrained: CS = alpha * ln(alpha/P) - (alpha - P)
            return float(alpha * np.log(alpha / P) - (alpha - P))

        # Constrained at B_max: CS = alpha * ln(B_max+1) - P * B_max
        return float(alpha * np.log(self.beer_max_per_person + 1) - P * self.beer_max_per_person)

    def _raw_attendance_by_type(
        self, ticket_price: float, beer_price: float, consumer_type: ConsumerType
    ) -> float:
        """
        Raw (pre-capacity-scaling) attendance for a consumer type.

        Uses net cost: net_cost = P_T - CS_beer(P_B)
        A_i = A_base_i · exp(-λ · (net_cost - baseline_net_cost))

        Cross-price effects emerge endogenously: cheaper beer → higher CS_beer
        → lower net cost → more attendance (for drinkers).
        """
        type_base_attendance = self.base_attendance * consumer_type.share
        # Convert numpy arrays from scipy optimizer to Python floats
        tp = np.asarray(ticket_price).item()
        bp = np.asarray(beer_price).item()
        cs_beer = self._beer_consumer_surplus(bp, consumer_type)
        net_cost = tp - cs_beer
        baseline_net_cost = self._baseline_net_cost[consumer_type.name]

        exponent = -self.ticket_price_sensitivity * (net_cost - baseline_net_cost)
        attendance = type_base_attendance * np.exp(exponent)
        return attendance

    def total_attendance(self, ticket_price: float, beer_price: float) -> float:
        """Sum attendance across all types, with proportional capacity scaling."""
        raw_total = sum(
            self._raw_attendance_by_type(ticket_price, beer_price, ct) for ct in self.consumer_types
        )
        return min(raw_total, self.capacity)

    def total_beer_consumption(
        self, ticket_price: float, beer_price: float
    ) -> tuple[float, dict[str, dict[str, float]]]:
        """Calculate total beer consumption across all types."""
        raw_attendances = {
            ct.name: self._raw_attendance_by_type(ticket_price, beer_price, ct)
            for ct in self.consumer_types
        }
        raw_total = sum(raw_attendances.values())
        scale = min(1.0, self.capacity / raw_total) if raw_total > 0 else 1.0

        breakdown = {}
        total = 0.0
        for ct in self.consumer_types:
            attendance = raw_attendances[ct.name] * scale
            beers_per_fan = self._beers_consumed_by_type(beer_price, ct)
            type_total = attendance * beers_per_fan
            breakdown[ct.name] = {
                "attendance": attendance,
                "beers_per_fan": beers_per_fan,
                "total_beers": type_total,
            }
            total += type_total

        return total, breakdown

    def stadium_revenue(self, ticket_price: float, beer_price: float) -> dict[str, Any]:
        """Calculate stadium revenues with heterogeneous consumers."""
        attendance = self.total_attendance(ticket_price, beer_price)
        total_beers, breakdown = self.total_beer_consumption(ticket_price, beer_price)

        beers_per_fan = total_beers / attendance if attendance > 0 else 0

        # Tax calculations
        pre_tax_beer_price = beer_price / (1 + self.beer_sales_tax_rate)
        stadium_beer_price = pre_tax_beer_price - self.beer_excise_tax

        # Revenues
        ticket_revenue = ticket_price * attendance
        beer_revenue = stadium_beer_price * total_beers
        total_revenue = ticket_revenue + beer_revenue

        # Costs
        ticket_costs = self.ticket_cost * attendance
        beer_costs = self.beer_cost * total_beers

        # Internalized costs: C = k · (Q/1000)²
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
    ) -> tuple[float, float, dict[str, Any]]:
        """Find profit-maximizing prices with heterogeneous consumers."""
        beer_min = self.beer_cost + self.BEER_PRICE_MIN_MARGIN
        ticket_bounds = (self.ticket_cost, self.TICKET_PRICE_MAX)

        def negative_profit_both(prices):
            ticket_p, beer_p = prices
            if beer_p < 0 or ticket_p < 0:
                return 1e10
            return -self.stadium_revenue(ticket_p, beer_p)["profit"]

        if beer_price_control is None:
            # Unconstrained optimization over both prices
            result = minimize(
                negative_profit_both,
                x0=[self.base_ticket_price, self.base_beer_price],
                bounds=[ticket_bounds, (beer_min, self.BEER_PRICE_MAX)],
                method="L-BFGS-B",
            )
            optimal_ticket, optimal_beer = result.x
            return optimal_ticket, optimal_beer, self.stadium_revenue(optimal_ticket, optimal_beer)

        # Determine effective beer price under control
        if ceiling_mode:
            if not hasattr(self, "_unconstrained_beer_optimum"):
                unconstrained = minimize(
                    negative_profit_both,
                    x0=[self.base_ticket_price, self.base_beer_price],
                    bounds=[ticket_bounds, (beer_min, self.BEER_PRICE_MAX)],
                    method="L-BFGS-B",
                )
                self._unconstrained_beer_optimum = unconstrained.x[1]
            optimal_beer = min(beer_price_control, self._unconstrained_beer_optimum)
        else:
            optimal_beer = beer_price_control

        # Optimize ticket price given fixed beer price
        def negative_profit_ticket(ticket_p):
            if ticket_p < 0:
                return 1e10
            return -self.stadium_revenue(ticket_p, optimal_beer)["profit"]

        result = minimize(
            negative_profit_ticket,
            x0=self.base_ticket_price,
            bounds=[ticket_bounds],
            method="L-BFGS-B",
        )
        optimal_ticket = result.x[0]

        return optimal_ticket, optimal_beer, self.stadium_revenue(optimal_ticket, optimal_beer)

    def consumer_surplus(self, ticket_price: float, beer_price: float) -> float:
        """
        Aggregate consumer surplus from semi-log demand in generalized price.

        Attendance depends on net cost P_T - CS_beer(P_B). The integral under
        that semi-log demand curve, A/λ, is therefore surplus for the full
        ticket-plus-beer option. Adding beer surplus separately would double
        count the same option value.
        """
        attendance = self.total_attendance(ticket_price, beer_price)
        return attendance / self.ticket_price_sensitivity

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
        tax_revenue = result["sales_tax_revenue"] + result["excise_tax_revenue"]

        sw = cs + ps + tax_revenue - ext_cost

        return {
            "consumer_surplus": cs,
            "producer_surplus": ps,
            "tax_revenue": tax_revenue,
            "externality_cost": ext_cost,
            "social_welfare": sw,
            "total_beers": result["total_beers"],
            "attendance": result["attendance"],
        }
