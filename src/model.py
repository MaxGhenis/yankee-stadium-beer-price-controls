"""
Economic model for beer pricing at Yankee Stadium.

This module implements the core economic model including:
- Consumer utility maximization
- Stadium revenue maximization
- Demand functions with elasticities and stadium-specific adjustments
- Externality calculations

STADIUM-SPECIFIC FEATURES:
- Captive audience (no outside alternatives during game)
- Complementarity between tickets and beer
- High willingness to pay (social/experiential value)
- Demand calibrated so observed prices are near-optimal
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from typing import Tuple, Dict


class StadiumEconomicModel:
    """
    Models consumer and producer behavior in stadium beer market.

    Key differences from general alcohol markets:
    1. CAPTIVE AUDIENCE: Fans have no alternatives during game → less elastic
    2. EXPERIENTIAL VALUE: Beer consumption is part of stadium experience
    3. COMPLEMENTARITY: Beer and tickets are consumed together
    4. PROFIT MAXIMIZATION: Stadiums are sophisticated monopolists

    Literature-based elasticities are adjusted for stadium context.
    """

    def __init__(self,
                 capacity: int = 46537,
                 base_ticket_price: float = 80.0,
                 base_beer_price: float = 12.5,
                 ticket_elasticity: float = -0.625,  # midpoint of -0.49 to -0.76
                 beer_elasticity: float = -0.965,    # midpoint of -0.79 to -1.14
                 ticket_cost: float = 20.0,
                 beer_cost: float = 5.0,  # All-in cost including labor, cups, waste
                 beer_excise_tax: float = 0.074,  # Federal + state + local excise per beer
                 beer_sales_tax_rate: float = 0.08875,  # NYC sales tax rate
                 consumer_income: float = 200.0,
                 alpha: float = 1.5,  # utility weight on beer
                 beta: float = 3.0,   # utility weight on stadium experience
                 # Stadium-specific parameters
                 captive_demand_share: float = 0.5,  # Share of demand that's price-insensitive
                 # Internalized costs (crowd management, brand, experience degradation)
                 experience_degradation_cost: float = 250.0,  # Quadratic cost parameter (calibrated)
                 capacity_constraint: float = 50000,  # Max beers that can be served
                 # Complementarity between tickets and beer
                 cross_price_elasticity: float = 0.1):  # Beer price effect on attendance
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
            beer_excise_tax: Excise tax per beer (federal + state + local)
            beer_sales_tax_rate: Sales tax rate (applied to pre-tax price)
            consumer_income: Representative consumer income ($)
            alpha: Utility weight on beer consumption
            beta: Utility weight on stadium experience
            captive_demand_share: Fraction of demand from committed fans (less elastic)
            experience_degradation_cost: Internalized cost per beer (crowd mgmt, brand, experience)
            capacity_constraint: Maximum beers that can be served per game
            cross_price_elasticity: Cross-elasticity between beer price and attendance (negative for complements)
        """
        self.capacity = capacity
        self.base_ticket_price = base_ticket_price
        self.base_beer_price = base_beer_price
        self.ticket_elasticity = ticket_elasticity
        self.beer_elasticity = beer_elasticity
        self.ticket_cost = ticket_cost
        self.beer_cost = beer_cost
        self.beer_excise_tax = beer_excise_tax
        self.beer_sales_tax_rate = beer_sales_tax_rate
        self.consumer_income = consumer_income
        self.alpha = alpha
        self.beta = beta
        self.captive_demand_share = captive_demand_share
        self.experience_degradation_cost = experience_degradation_cost
        self.capacity_constraint = capacity_constraint
        self.cross_price_elasticity = cross_price_elasticity

        # Calculate base quantities for calibration
        # Calibrate so that observed prices are near-optimal
        self.base_attendance = self.capacity * 0.85  # 85% capacity at baseline
        self.base_beers_per_fan = 1.0  # 40% drink * 2.5 beers = 1.0 average

    def _attendance_demand(self, ticket_price: float, beer_price: float) -> float:
        """
        Calculate attendance as function of ticket and beer prices.

        Uses semi-log demand (like beer) to avoid corner solutions:
        A = A₀ · exp(-λ_ticket · (P_ticket - P₀)) · cross_effect(P_beer)

        Calibrated so $80 tickets are approximately optimal.

        NOTE: Semi-log demand is LOG-CONCAVE, which is critical for theoretical
        results. Leisten (2024) proves that under log-concavity, beer price
        ceilings cause ticket prices to rise. Our functional form satisfies this
        condition: ln(A) is concave because it's linear in price plus a
        negative power term.
        """
        # Semi-log ticket demand (calibrated to make $80 near-optimal)
        # With ticket MC = $20, optimal markup (P-MC)/P = 0.75
        # This implies λ_ticket ≈ 1/(P - MC) = 1/60 ≈ 0.017
        ticket_sensitivity = 0.017
        ticket_deviation = ticket_price - self.base_ticket_price

        # Own-price effect
        price_effect = np.exp(-ticket_sensitivity * ticket_deviation)

        # Cross-price effect (beer is complement)
        # NOTE: Parameter is ASSUMED (not from empirical estimates)
        # Literature documents complementarity but not specific cross-elasticity
        # Benchmarks: cars/gas=-1.6 (strong), food=-0.1 to -0.5 (weak-moderate)
        # Our default 0.1 is conservative (weak complementarity)
        if beer_price > 0:
            beer_ratio = beer_price / self.base_beer_price
            cross_effect = beer_ratio ** (-self.cross_price_elasticity)
        else:
            # Beer ban: 5% attendance reduction due to lost complementary good
            cross_effect = 0.95

        attendance = self.base_attendance * price_effect * cross_effect
        return min(attendance, self.capacity)

    def _beers_per_fan_demand(self, beer_price: float, income: float) -> float:
        """
        Calculate beers consumed per fan as function of price.

        STADIUM-SPECIFIC MODEL:
        Uses semi-log demand calibrated so observed prices are profit-maximizing.
        This reflects:
        - Captive audience (no alternatives during game)
        - Experiential consumption (part of stadium ritual)
        - Heterogeneous fans with varying willingness to pay

        Form: Q = Q_base * exp(-sensitivity * (P - P_base))
        where sensitivity is calibrated to make P_base approximately optimal.

        At baseline ($12.50): ~40% of fans drink, averaging 2.5 beers = 1.0 per attendee

        NOTE: This functional form is LOG-CONCAVE (ln(Q) is linear in P, thus concave),
        satisfying the condition in Leisten (2024) for proving that beer price ceilings
        cause ticket prices to rise.
        """
        if beer_price <= 0:
            return 0

        # Semi-log demand: Q = Q_base * exp(-λ(P - P_base))
        # Calibrate λ so that P_base ($12.50) is near profit-maximum
        # With MC = $5 (all-in cost), optimal markup (P-MC)/P = 0.60
        # FOC: P - 1/λ = MC → 12.50 - 1/λ = 5 → λ = 0.133

        price_sensitivity = 0.133  # Calibrated for observed prices with realistic costs
        price_deviation = beer_price - self.base_beer_price

        quantity = self.base_beers_per_fan * np.exp(-price_sensitivity * price_deviation)

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

    def _internalized_costs(self, total_beers: float) -> float:
        """
        Calculate costs the stadium internalizes from alcohol consumption.

        These are negative externalities on OTHER CUSTOMERS that the monopolist
        stadium internalizes because they affect future profits:

        1. CROWD MANAGEMENT: Security, cleanup, liability insurance
           - More drunk fans → more incidents → CONVEX cost (incidents compound)

        2. EXPERIENCE DEGRADATION: Drunk fans degrade experience for others
           - Affects future attendance and willingness to pay
           - CONVEX: First few drunk fans OK, but as more get drunk it compounds

        3. BRAND/REPUTATION: Excessive intoxication damages brand
           - "Cheap beer stadium" or "rowdy crowd" reputation
           - CONVEX: Reputational damage accelerates with extreme consumption

        4. CAPACITY: Service bottlenecks and operational costs
           - Can only serve so many beers per game
           - Quadratic penalty near capacity

        Args:
            total_beers: Total beers sold

        Returns:
            Internalized cost ($) the stadium faces
        """
        # CONVEX cost for experience degradation
        # Costs accelerate as consumption increases (compounding negative effects)
        # Calibrated so observed prices ($12.50) are profit-maximizing
        beers_per_1000 = total_beers / 1000
        experience_cost = self.experience_degradation_cost * (beers_per_1000 ** 2)

        # Capacity penalty: quadratic cost as approach capacity
        if total_beers > self.capacity_constraint:
            capacity_penalty = ((total_beers - self.capacity_constraint) ** 2) * 0.001
        else:
            capacity_penalty = 0

        return experience_cost + capacity_penalty

    def stadium_revenue(self, ticket_price: float, beer_price: float) -> Dict[str, float]:
        """
        Calculate stadium revenues and costs INCLUDING internalized externalities and taxes.

        NOTE: beer_price is the CONSUMER price (including all taxes).
        Stadium receives: beer_price / (1 + sales_tax_rate) - excise_tax

        The stadium is a monopolist that internalizes negative externalities
        (crowd management, brand damage, experience degradation) because
        these affect its long-run profits.

        Returns:
            Dict with ticket_revenue, beer_revenue, total_revenue,
            ticket_cost, beer_cost, total_cost, profit
        """
        attendance = self._attendance_demand(ticket_price, beer_price)
        beers_per_fan = self._beers_per_fan_demand(beer_price, self.consumer_income)
        total_beers = attendance * beers_per_fan

        # BEER REVENUE (after taxes):
        # Consumer pays: beer_price (includes sales tax)
        # Pre-sales-tax price: beer_price / (1 + sales_tax_rate)
        # Stadium receives: pre_tax - excise_tax
        pre_tax_beer_price = beer_price / (1 + self.beer_sales_tax_rate)
        stadium_beer_price = pre_tax_beer_price - self.beer_excise_tax

        # REVENUES
        ticket_revenue = ticket_price * attendance
        beer_revenue = stadium_beer_price * total_beers  # What stadium actually receives
        total_revenue = ticket_revenue + beer_revenue

        # COSTS
        ticket_costs = self.ticket_cost * attendance
        beer_costs = self.beer_cost * total_beers

        # INTERNALIZED COSTS: Stadium internalizes externalities on other customers
        internalized_costs = self._internalized_costs(total_beers)

        total_costs = ticket_costs + beer_costs + internalized_costs

        # PROFIT
        profit = total_revenue - total_costs

        # TAX REVENUE (collected by government)
        sales_tax_revenue = (beer_price - pre_tax_beer_price) * total_beers
        excise_tax_revenue = self.beer_excise_tax * total_beers
        total_tax_revenue = sales_tax_revenue + excise_tax_revenue

        return {
            'attendance': attendance,
            'beers_per_fan': beers_per_fan,
            'total_beers': total_beers,
            'consumer_beer_price': beer_price,  # What consumer pays
            'stadium_beer_price': stadium_beer_price,  # What stadium receives
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
            'total_tax_revenue': total_tax_revenue
        }

    def optimal_pricing(self,
                       beer_price_control: float = None,
                       ticket_price_control: float = None) -> Tuple[float, float, Dict]:
        """
        Find revenue-maximizing prices (possibly with constraints).

        With stadium-specific demand, observed prices should be near-optimal.

        Args:
            beer_price_control: Max beer price if price ceiling, min if floor
            ticket_price_control: Max ticket price if ceiling, min if floor

        Returns:
            (optimal_ticket_price, optimal_beer_price, results_dict)
        """
        def objective(prices):
            ticket_p, beer_p = prices
            if beer_p < 0 or ticket_p < 0:
                return 1e10  # penalty for negative prices
            result = self.stadium_revenue(ticket_p, beer_p)
            return -result['profit']  # minimize negative profit

        # Set bounds
        ticket_bounds = (self.ticket_cost, 200)
        # Beer price must be above cost; with captive demand, optimal is higher
        beer_bounds = (self.beer_cost + 0.1, 30)

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
        With captive demand component, CS is higher than pure elastic model.
        """
        attendance = self._attendance_demand(ticket_price, beer_price)
        beers_per_fan = self._beers_per_fan_demand(beer_price, self.consumer_income)

        # Consumer surplus from tickets (using elasticity formula)
        ticket_cs = (attendance * ticket_price) / (1 + self.ticket_elasticity)

        # Consumer surplus from beer (adjusted for captive component)
        total_beers = attendance * beers_per_fan
        # Captive consumers have higher surplus (would pay more)
        captive_surplus_multiplier = 1.5  # Captive fans get 50% more surplus
        beer_cs = (total_beers * beer_price) / (1 + self.beer_elasticity * 0.7)
        beer_cs *= captive_surplus_multiplier

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

        With externalities, socially optimal price > privately optimal price.

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
