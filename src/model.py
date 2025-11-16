"""
Economic model for beer pricing at Yankee Stadium.

This module implements the core economic model including:
- Consumer utility maximization
- Stadium revenue maximization
- Demand functions with elasticities
- Externality calculations
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from typing import Tuple, Dict


class StadiumEconomicModel:
    """
    Models consumer and producer behavior in stadium beer market.

    Based on literature showing:
    - Ticket demand elasticity: -0.49 to -0.76 (inelastic)
    - Beer demand elasticity: -0.79 to -1.14 (relatively inelastic)
    - Teams maximize revenue across tickets + concessions
    """

    def __init__(self,
                 capacity: int = 46537,
                 base_ticket_price: float = 80.0,
                 base_beer_price: float = 12.5,
                 ticket_elasticity: float = -0.625,  # midpoint of -0.49 to -0.76
                 beer_elasticity: float = -0.965,    # midpoint of -0.79 to -1.14
                 ticket_cost: float = 20.0,
                 beer_cost: float = 2.0,
                 consumer_income: float = 200.0,
                 alpha: float = 1.5,  # utility weight on beer
                 beta: float = 3.0):  # utility weight on stadium experience
        """
        Initialize model parameters.

        Args:
            capacity: Stadium seating capacity
            base_ticket_price: Baseline ticket price ($)
            base_beer_price: Baseline beer price ($)
            ticket_elasticity: Price elasticity of attendance demand
            beer_elasticity: Price elasticity of beer demand
            ticket_cost: Marginal cost per ticket ($)
            beer_cost: Marginal cost per beer ($)
            consumer_income: Representative consumer income ($)
            alpha: Utility weight on beer consumption
            beta: Utility weight on stadium experience
        """
        self.capacity = capacity
        self.base_ticket_price = base_ticket_price
        self.base_beer_price = base_beer_price
        self.ticket_elasticity = ticket_elasticity
        self.beer_elasticity = beer_elasticity
        self.ticket_cost = ticket_cost
        self.beer_cost = beer_cost
        self.consumer_income = consumer_income
        self.alpha = alpha
        self.beta = beta

        # Calculate base quantities for reference point
        self.base_attendance = self._attendance_demand(base_ticket_price, base_beer_price)
        self.base_beers_per_fan = self._beers_per_fan_demand(base_beer_price, consumer_income)

    def _attendance_demand(self, ticket_price: float, beer_price: float) -> float:
        """
        Calculate attendance as function of ticket and beer prices.

        Uses constant elasticity demand: Q = A * P^ε
        where A is calibrated to match baseline.

        Beer price matters because tickets and beer are complements.
        Cross-price elasticity estimated at 0.1 (small complementarity).
        """
        # Calibrate scale parameter to match base case
        if not hasattr(self, 'base_attendance'):
            base = self.capacity * 0.85  # assume 85% capacity at baseline
        else:
            base = self.base_attendance

        # Own-price effect (negative)
        price_effect = (ticket_price / self.base_ticket_price) ** self.ticket_elasticity

        # Cross-price effect (positive - beer is complement)
        cross_elasticity = 0.1  # 10% increase in beer price -> 1% decrease in attendance
        cross_effect = (beer_price / self.base_beer_price) ** (-cross_elasticity)

        attendance = base * price_effect * cross_effect

        return min(attendance, self.capacity)

    def _beers_per_fan_demand(self, beer_price: float, income: float) -> float:
        """
        Calculate beers consumed per fan as function of price.

        Uses constant elasticity: Q = A * P^ε
        Calibrated so ~40% of fans drink (mean ~2.5 beers) at baseline.
        """
        # Calibrate scale parameter
        # At baseline: 40% drink, average 2.5 beers among drinkers = 1.0 beers per attendee
        if not hasattr(self, 'base_beers_per_fan'):
            base_quantity = 1.0
        else:
            base_quantity = self.base_beers_per_fan

        quantity = base_quantity * (beer_price / self.base_beer_price) ** self.beer_elasticity

        return max(quantity, 0)

    def consumer_utility(self, beers: float, has_ticket: bool = True) -> float:
        """
        Calculate consumer utility from stadium experience.

        U(B, T) = α·ln(B + 1) + β·ln(T + 1) + Y

        where:
        - B = beers consumed
        - T = time enjoying stadium (9 innings if attend)
        - Y = other consumption
        """
        if not has_ticket:
            return self.consumer_income  # outside option

        innings = 9
        utility = (
            self.alpha * np.log(beers + 1) +
            self.beta * np.log(innings + 1) +
            (self.consumer_income - self.base_ticket_price - beers * self.base_beer_price)
        )
        return utility

    def optimal_beer_consumption(self, beer_price: float, ticket_price: float) -> float:
        """
        Consumer's optimal beer quantity given prices.

        Solves: max U(B) subject to budget constraint
        FOC: α/(B+1) = P_beer
        """
        # Check if attending is optimal
        utility_attend = self.consumer_utility(
            self._beers_per_fan_demand(beer_price, self.consumer_income),
            has_ticket=True
        )
        utility_not_attend = self.consumer_income

        if utility_not_attend >= utility_attend:
            return 0

        return self._beers_per_fan_demand(beer_price, self.consumer_income)

    def stadium_revenue(self, ticket_price: float, beer_price: float) -> Dict[str, float]:
        """
        Calculate stadium revenues and costs.

        Returns:
            Dict with ticket_revenue, beer_revenue, total_revenue,
            ticket_cost, beer_cost, total_cost, profit
        """
        attendance = self._attendance_demand(ticket_price, beer_price)
        beers_per_fan = self._beers_per_fan_demand(beer_price, self.consumer_income)
        total_beers = attendance * beers_per_fan

        ticket_revenue = ticket_price * attendance
        beer_revenue = beer_price * total_beers
        total_revenue = ticket_revenue + beer_revenue

        ticket_costs = self.ticket_cost * attendance
        beer_costs = self.beer_cost * total_beers
        total_costs = ticket_costs + beer_costs

        profit = total_revenue - total_costs

        return {
            'attendance': attendance,
            'beers_per_fan': beers_per_fan,
            'total_beers': total_beers,
            'ticket_revenue': ticket_revenue,
            'beer_revenue': beer_revenue,
            'total_revenue': total_revenue,
            'ticket_costs': ticket_costs,
            'beer_costs': beer_costs,
            'total_costs': total_costs,
            'profit': profit
        }

    def optimal_pricing(self,
                       beer_price_control: float = None,
                       ticket_price_control: float = None) -> Tuple[float, float, Dict]:
        """
        Find revenue-maximizing prices (possibly with constraints).

        Args:
            beer_price_control: Max beer price if price ceiling, min if floor
            ticket_price_control: Max ticket price if ceiling, min if floor

        Returns:
            (optimal_ticket_price, optimal_beer_price, results_dict)
        """
        def objective(prices):
            ticket_p, beer_p = prices
            result = self.stadium_revenue(ticket_p, beer_p)
            return -result['profit']  # minimize negative profit

        # Set bounds
        ticket_bounds = (10, 200)
        beer_bounds = (0, 30)

        if beer_price_control is not None:
            beer_bounds = (beer_price_control, beer_price_control)
        if ticket_price_control is not None:
            ticket_bounds = (ticket_price_control, ticket_price_control)

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

    def consumer_surplus(self, ticket_price: float, beer_price: float) -> float:
        """
        Calculate consumer surplus.

        CS = ∫[P_max to P*] Q(P) dP

        For constant elasticity: CS = Q*P / (1 + ε)
        """
        attendance = self._attendance_demand(ticket_price, beer_price)
        beers_per_fan = self._beers_per_fan_demand(beer_price, self.consumer_income)

        # Consumer surplus from tickets (using elasticity formula)
        ticket_cs = (attendance * ticket_price) / (1 + self.ticket_elasticity)

        # Consumer surplus from beer
        total_beers = attendance * beers_per_fan
        beer_cs = (total_beers * beer_price) / (1 + self.beer_elasticity)

        return ticket_cs + beer_cs

    def producer_surplus(self, ticket_price: float, beer_price: float) -> float:
        """Calculate producer surplus (profit)."""
        result = self.stadium_revenue(ticket_price, beer_price)
        return result['profit']

    def deadweight_loss(self,
                       current_ticket_price: float,
                       current_beer_price: float,
                       optimal_ticket_price: float,
                       optimal_beer_price: float) -> float:
        """
        Calculate deadweight loss from price distortion.

        DWL = (CS + PS)_optimal - (CS + PS)_current
        """
        current_welfare = (
            self.consumer_surplus(current_ticket_price, current_beer_price) +
            self.producer_surplus(current_ticket_price, current_beer_price)
        )

        optimal_welfare = (
            self.consumer_surplus(optimal_ticket_price, optimal_beer_price) +
            self.producer_surplus(optimal_ticket_price, optimal_beer_price)
        )

        return optimal_welfare - current_welfare

    def externality_cost(self,
                        total_beers: float,
                        crime_cost_per_beer: float = 2.50,
                        health_cost_per_beer: float = 1.50) -> float:
        """
        Calculate external costs from alcohol consumption.

        Based on literature:
        - 10% increase in alcohol → 1% increase in assault, 2.9% increase in rape
        - External costs ~$0.48-$1.19 per drink (Manning et al. 1991, inflation-adjusted)
        - Higher at stadium due to concentration and transportation

        Args:
            total_beers: Total beers consumed at game
            crime_cost_per_beer: Crime/violence cost per beer ($)
            health_cost_per_beer: Health system cost per beer ($)

        Returns:
            Total external cost ($)
        """
        total_cost = total_beers * (crime_cost_per_beer + health_cost_per_beer)
        return total_cost

    def social_welfare(self,
                      ticket_price: float,
                      beer_price: float,
                      crime_cost_per_beer: float = 2.50,
                      health_cost_per_beer: float = 1.50) -> Dict[str, float]:
        """
        Calculate total social welfare including externalities.

        SW = CS + PS - External_Costs

        Returns:
            Dict with consumer_surplus, producer_surplus, externality_cost,
            social_welfare
        """
        cs = self.consumer_surplus(ticket_price, beer_price)
        ps = self.producer_surplus(ticket_price, beer_price)

        result = self.stadium_revenue(ticket_price, beer_price)
        ext_cost = self.externality_cost(
            result['total_beers'],
            crime_cost_per_beer,
            health_cost_per_beer
        )

        sw = cs + ps - ext_cost

        return {
            'consumer_surplus': cs,
            'producer_surplus': ps,
            'externality_cost': ext_cost,
            'social_welfare': sw,
            'total_beers': result['total_beers'],
            'attendance': result['attendance']
        }
