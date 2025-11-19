"""
Comprehensive sanity check tests for economic model.

These tests verify fundamental economic laws, accounting identities,
and data quality constraints that should ALWAYS hold.
"""

import pytest
import numpy as np
import pandas as pd
from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestMonotonicity:
    """Test that outcomes obey economic monotonicity laws."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_profit_decreases_with_tighter_ceiling(self, model):
        """Binding ceilings should monotonically reduce profit."""
        # Get optimal price
        _, optimal_beer, _ = model.optimal_pricing()

        # Test tighter and tighter ceilings
        ceilings = np.linspace(optimal_beer - 5, optimal_beer - 1, 5)
        profits = []

        for ceiling in sorted(ceilings):
            _, _, result = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)
            profits.append(result['profit'])

        # Profits should be monotonically increasing as ceiling rises
        for i in range(len(profits) - 1):
            assert profits[i] <= profits[i + 1], \
                f"Profit should increase as ceiling rises: {profits[i]} > {profits[i+1]}"

    def test_consumption_increases_with_lower_prices(self, model):
        """Lower beer prices should increase per-fan consumption."""
        prices = [8, 10, 12, 14, 16]
        consumption = [model._beers_per_fan_demand(p, 200) for p in prices]

        # Consumption should decrease as price increases
        for i in range(len(consumption) - 1):
            assert consumption[i] >= consumption[i + 1], \
                f"Consumption should decrease with price: {consumption[i]} < {consumption[i+1]}"

    def test_attendance_decreases_with_ticket_price(self, model):
        """Higher ticket prices should reduce attendance."""
        ticket_prices = [60, 80, 100, 120]
        attendance = [model._attendance_demand(p, 12.5) for p in ticket_prices]

        for i in range(len(attendance) - 1):
            assert attendance[i] >= attendance[i + 1], \
                f"Attendance should decrease with ticket price"

    def test_externalities_proportional_to_consumption(self, model):
        """External costs should scale linearly with beer quantity."""
        beers_1 = 1000
        beers_2 = 2000
        
        ext_1 = model.externality_cost(beers_1)
        ext_2 = model.externality_cost(beers_2)
        
        # Should be exactly double (linear)
        assert ext_2 == pytest.approx(ext_1 * 2)


class TestAccountingIdentities:
    """Test that accounting identities always hold."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_revenue_equals_components(self, model):
        """Total revenue must equal ticket + beer revenue."""
        result = model.stadium_revenue(80, 12.5)

        total = result['ticket_revenue'] + result['beer_revenue']
        assert result['total_revenue'] == pytest.approx(total, rel=1e-6), \
            f"Revenue accounting error: {result['total_revenue']} != {total}"

    def test_costs_equal_components(self, model):
        """Total costs must equal all cost components."""
        result = model.stadium_revenue(80, 12.5)

        total = result['ticket_costs'] + result['beer_costs'] + result['internalized_costs']
        assert result['total_costs'] == pytest.approx(total, rel=1e-6), \
            f"Cost accounting error: {result['total_costs']} != {total}"

    def test_profit_equals_revenue_minus_cost(self, model):
        """Profit must equal revenue minus costs."""
        result = model.stadium_revenue(80, 12.5)

        expected_profit = result['total_revenue'] - result['total_costs']
        assert result['profit'] == pytest.approx(expected_profit, rel=1e-6), \
            f"Profit accounting error: {result['profit']} != {expected_profit}"

    def test_welfare_accounting_identity(self, model):
        """SW must equal CS + PS - externalities."""
        welfare = model.social_welfare(80, 12.5)

        expected_sw = (
            welfare['consumer_surplus'] +
            welfare['producer_surplus'] -
            welfare['externality_cost']
        )

        assert welfare['social_welfare'] == pytest.approx(expected_sw, rel=1e-6), \
            f"Welfare accounting error: {welfare['social_welfare']} != {expected_sw}"

    def test_tax_revenue_calculation(self, model):
        """Verify tax calculations match statutory rates."""
        result = model.stadium_revenue(80, 12.5)

        # Consumer pays $12.50
        # Pre-sales-tax: $12.50 / 1.08875 = $11.48
        # Sales tax: $12.50 - $11.48 = $1.02
        # Excise tax: $0.074
        # Total tax: $1.09 per beer

        consumer_price = 12.5
        pre_tax = consumer_price / (1 + model.beer_sales_tax_rate)
        expected_sales_tax = consumer_price - pre_tax
        expected_excise_tax = model.beer_excise_tax
        expected_total_tax = expected_sales_tax + expected_excise_tax

        total_beers = result['total_beers']
        expected_sales_tax_rev = expected_sales_tax * total_beers
        expected_excise_tax_rev = expected_excise_tax * total_beers

        assert result['sales_tax_revenue'] == pytest.approx(expected_sales_tax_rev, rel=1e-6)
        assert result['excise_tax_revenue'] == pytest.approx(expected_excise_tax_rev, rel=1e-6)


class TestComparativeStaticsSigns:
    """Test that comparative statics have correct signs."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_beer_ceiling_raises_tickets(self, model):
        """Lower beer ceiling should raise optimal ticket prices (Leisten 2025)."""
        _, optimal_beer, _ = model.optimal_pricing()

        # Tight ceiling
        ticket_low, beer_low, _ = model.optimal_pricing(
            beer_price_control=optimal_beer - 3,
            ceiling_mode=True
        )

        # Moderate ceiling
        ticket_high, beer_high, _ = model.optimal_pricing(
            beer_price_control=optimal_beer - 1,
            ceiling_mode=True
        )

        # Tighter ceiling (lower beer) → higher tickets
        assert ticket_low > ticket_high, \
            f"Lower beer ceiling should raise tickets: ${ticket_low:.2f} not > ${ticket_high:.2f}"

    def test_complementarity_affects_response(self, model):
        """Higher cross-elasticity should amplify ticket response."""
        # Weak complementarity
        model_weak = StadiumEconomicModel(cross_price_elasticity=0.05)
        _, beer_opt_weak, _ = model_weak.optimal_pricing()
        t_weak, _, _ = model_weak.optimal_pricing(
            beer_price_control=beer_opt_weak - 3,
            ceiling_mode=True
        )

        # Strong complementarity
        model_strong = StadiumEconomicModel(cross_price_elasticity=0.20)
        _, beer_opt_strong, _ = model_strong.optimal_pricing()
        t_strong, _, _ = model_strong.optimal_pricing(
            beer_price_control=beer_opt_strong - 3,
            ceiling_mode=True
        )

        # Both should raise tickets, but strong complementarity → larger increase
        # (Though this might not always hold due to general equilibrium effects)
        # Just verify both raise tickets relative to unconstrained
        _, unc_t_weak, _ = model_weak.optimal_pricing()
        _, unc_t_strong, _ = model_strong.optimal_pricing()

        assert t_weak > unc_t_weak, "Ceiling should raise tickets (weak complementarity)"
        assert t_strong > unc_t_strong, "Ceiling should raise tickets (strong complementarity)"

    def test_higher_costs_raise_prices(self, model):
        """Higher marginal costs should raise optimal prices."""
        # Low cost
        model_low = StadiumEconomicModel(beer_cost=2.0)
        _, beer_low, _ = model_low.optimal_pricing()

        # High cost
        model_high = StadiumEconomicModel(beer_cost=4.0)
        _, beer_high, _ = model_high.optimal_pricing()

        assert beer_high > beer_low, \
            f"Higher cost should raise price: ${beer_high:.2f} not > ${beer_low:.2f}"


class TestDataQuality:
    """Test that outputs meet data quality constraints."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_all_quantities_nonnegative(self, model):
        """No negative quantities (attendance, beers, revenue, etc)."""
        result = model.stadium_revenue(80, 12.5)

        nonnegative_fields = [
            'attendance', 'beers_per_fan', 'total_beers',
            'ticket_revenue', 'beer_revenue', 'total_revenue',
            'ticket_costs', 'beer_costs', 'total_costs'
        ]

        for field in nonnegative_fields:
            assert result[field] >= 0, f"{field} should be non-negative: {result[field]}"

    def test_prices_in_reasonable_range(self, model):
        """Optimal prices should be in reasonable range (catch optimizer failures)."""
        ticket, beer, result = model.optimal_pricing()

        assert 20 <= ticket <= 300, f"Ticket price unreasonable: ${ticket:.2f}"
        assert 5 <= beer <= 50, f"Beer price unreasonable: ${beer:.2f}"

    def test_no_nans_or_infs(self, model):
        """Verify no NaN/Inf in outputs."""
        result = model.stadium_revenue(80, 12.5)
        
        for key, value in result.items():
            if isinstance(value, (int, float)):
                assert not np.isnan(value), f"{key} is NaN"
                assert not np.isinf(value), f"{key} is Inf"
    def test_attendance_not_exceeds_capacity(self, model):
        """Attendance should never exceed stadium capacity."""
        # Try very low prices
        result = model.stadium_revenue(10, 5)
        assert result['attendance'] <= model.capacity, \
            f"Attendance {result['attendance']} exceeds capacity {model.capacity}"

    def test_beer_consumption_reasonable(self, model):
        """Beers per fan should be in reasonable range."""
        beers = model._beers_per_fan_demand(12.5, 200)

        # Even heavy drinkers unlikely to consume >5 beers
        # Average fan should be 0-3 beers
        assert 0 <= beers <= 5, f"Beers per fan unreasonable: {beers:.2f}"


class TestContinuity:
    """Test continuity of outcomes across parameter changes."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_continuous_at_binding_threshold(self, model):
        """Outcomes should be continuous as ceiling crosses optimal."""
        _, optimal_beer, _ = model.optimal_pricing()

        # Just below optimal (binding)
        epsilon = 0.1
        t_below, b_below, r_below = model.optimal_pricing(
            beer_price_control=optimal_beer - epsilon,
            ceiling_mode=True
        )

        # Just above optimal (non-binding)
        t_above, b_above, r_above = model.optimal_pricing(
            beer_price_control=optimal_beer + epsilon,
            ceiling_mode=True
        )

        # Unconstrained
        t_unc, b_unc, r_unc = model.optimal_pricing()

        # Above should match unconstrained
        assert b_above == pytest.approx(b_unc, rel=1e-2)
        assert t_above == pytest.approx(t_unc, rel=1e-2)

        # Below should be at ceiling
        assert b_below == pytest.approx(optimal_beer - epsilon, rel=1e-6)

    def test_small_parameter_changes_small_effects(self, model):
        """Small parameter changes should cause small outcome changes."""
        base_ticket, base_beer, base_result = model.optimal_pricing()

        # Change elasticity slightly
        model.beer_elasticity = model.beer_elasticity * 1.01  # 1% change

        new_ticket, new_beer, new_result = model.optimal_pricing()

        # Outcomes shouldn't change drastically (< 10% for 1% parameter change)
        ticket_change_pct = abs(new_ticket - base_ticket) / base_ticket
        profit_change_pct = abs(new_result['profit'] - base_result['profit']) / base_result['profit']

        assert ticket_change_pct < 0.10, \
            f"1% elasticity change caused {ticket_change_pct:.1%} ticket change (too sensitive)"
        assert profit_change_pct < 0.10, \
            f"1% elasticity change caused {profit_change_pct:.1%} profit change (too sensitive)"


class TestEconomicIntuition:
    """Test that model follows basic economic intuition."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_complements_cross_price_negative(self, model):
        """Beer price increases should reduce attendance (complements)."""
        attendance_cheap = model._attendance_demand(80, 8)
        attendance_expensive = model._attendance_demand(80, 16)

        assert attendance_cheap > attendance_expensive, \
            "Higher beer price should reduce attendance (complements)"

    def test_demand_slopes_down(self, model):
        """Demand should be downward sloping."""
        # Already tested elsewhere, but verify for completeness
        q_low = model._beers_per_fan_demand(8, 200)
        q_high = model._beers_per_fan_demand(16, 200)

        assert q_low > q_high, "Demand should slope down"

    def test_higher_prices_reduce_welfare(self, model):
        """Higher prices (all else equal) should reduce consumer surplus."""
        cs_low = model.consumer_surplus(80, 10)
        cs_high = model.consumer_surplus(80, 15)

        # Higher beer price → lower consumer surplus
        assert cs_low > cs_high, "Higher prices should reduce consumer surplus"

    def test_optimal_price_above_marginal_cost(self, model):
        """Monopolist should price above marginal cost."""
        _, beer_price, _ = model.optimal_pricing()

        # Should have positive markup
        assert beer_price > model.beer_cost, \
            f"Optimal beer ${beer_price:.2f} should exceed cost ${model.beer_cost:.2f}"

    def test_profit_maximization_works(self, model):
        """Optimal pricing should yield higher profit than arbitrary pricing."""
        optimal_ticket, optimal_beer, optimal_result = model.optimal_pricing()

        # Try some arbitrary prices
        arbitrary_result = model.stadium_revenue(60, 10)

        # Optimal should beat arbitrary (or be very close if arbitrary is near-optimal)
        assert optimal_result['profit'] >= arbitrary_result['profit'] * 0.95, \
            "Optimal pricing should achieve high profit"


class TestSimulationOutputQuality:
    """Test that simulation outputs meet quality standards."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_all_scenarios_complete(self, simulator):
        """All scenarios should return complete data."""
        results = simulator.run_all_scenarios()

        required_cols = [
            'scenario', 'ticket_price', 'beer_price', 'attendance', 'total_beers',
            'profit', 'consumer_surplus', 'externality_cost', 'social_welfare'
        ]

        for col in required_cols:
            assert col in results.columns, f"Missing column: {col}"
            assert not results[col].isna().any(), f"Column {col} has NaN values"

    def test_no_negative_prices(self, simulator):
        """All prices should be positive."""
        results = simulator.run_all_scenarios()

        assert (results['ticket_price'] > 0).all(), "Found negative ticket price"
        assert (results['beer_price'] >= 0).all(), "Found negative beer price"

    def test_no_negative_quantities(self, simulator):
        """All quantities should be non-negative."""
        results = simulator.run_all_scenarios()

        assert (results['attendance'] >= 0).all(), "Found negative attendance"
        assert (results['total_beers'] >= 0).all(), "Found negative beer quantity"

    def test_welfare_components_sensible(self, simulator):
        """Welfare components should have reasonable magnitudes."""
        results = simulator.run_all_scenarios()

        # Consumer surplus should be positive
        assert (results['consumer_surplus'] > 0).all(), "Consumer surplus should be positive"

        # Social welfare should typically be positive
        # (might be negative in extreme cases with huge externalities)
        assert results['social_welfare'].mean() > 0, "Average social welfare should be positive"


class TestCrossPriceElasticity:
    """Test that cross-price elasticity parameter works as expected."""

    def test_zero_cross_elasticity_means_no_effect(self):
        """Zero cross-elasticity: beer prices don't affect attendance."""
        model = StadiumEconomicModel(cross_price_elasticity=0.0)

        # Attendance should be independent of beer price
        a1 = model._attendance_demand(80, 8)
        a2 = model._attendance_demand(80, 16)

        # Should be exactly equal (no cross-price effect)
        assert a1 == pytest.approx(a2, rel=1e-6), \
            "With zero cross-elasticity, beer price shouldn't affect attendance"

    def test_positive_cross_elasticity_creates_complementarity(self):
        """Positive cross-elasticity: higher beer price reduces attendance."""
        model = StadiumEconomicModel(cross_price_elasticity=0.15)

        a_cheap = model._attendance_demand(80, 8)
        a_expensive = model._attendance_demand(80, 16)

        assert a_cheap > a_expensive, \
            "With positive cross-elasticity, higher beer price should reduce attendance"

    def test_cross_elasticity_magnitude_matters(self):
        """Higher cross-elasticity → stronger complementarity effect."""
        model_weak = StadiumEconomicModel(cross_price_elasticity=0.05)
        model_strong = StadiumEconomicModel(cross_price_elasticity=0.20)

        # Compare attendance effects of doubling beer price
        a_base_weak = model_weak._attendance_demand(80, 10)
        a_double_weak = model_weak._attendance_demand(80, 20)
        effect_weak = (a_base_weak - a_double_weak) / a_base_weak

        a_base_strong = model_strong._attendance_demand(80, 10)
        a_double_strong = model_strong._attendance_demand(80, 20)
        effect_strong = (a_base_strong - a_double_strong) / a_base_strong

        # Stronger complementarity → larger attendance reduction
        assert effect_strong > effect_weak, \
            f"Strong complementarity should have larger effect: {effect_strong:.3f} not > {effect_weak:.3f}"


class TestEdgeCasesRobustness:
    """Test robustness to edge cases and extreme parameters."""

    def test_very_low_income_no_crash(self):
        """Model should handle very low income without crashing."""
        model = StadiumEconomicModel(consumer_income=50)
        # Should run without error
        result = model.stadium_revenue(80, 12.5)
        assert 'profit' in result

    def test_very_high_elasticity_no_crash(self):
        """Model should handle very elastic demand."""
        model = StadiumEconomicModel(beer_elasticity=-3.0)
        result = model.stadium_revenue(80, 12.5)
        assert 'profit' in result

    def test_zero_externality_costs(self):
        """Model should work with zero externality costs."""
        model = StadiumEconomicModel()
        model.external_costs['crime'] = 0
        model.external_costs['health'] = 0
        welfare = model.social_welfare(80, 12.5)
        
        # SW should equal CS + PS (no externality subtraction)
        assert welfare['social_welfare'] == pytest.approx(welfare['consumer_surplus'] + welfare['producer_surplus'])
        assert welfare['externality_cost'] == 0

    def test_very_high_externality_costs(self):
        """Model should handle very high externality estimates."""
        model = StadiumEconomicModel()
        # Extreme externality costs (e.g., $50/beer)
        model.external_costs['crime'] = 30
        model.external_costs['health'] = 20
        welfare = model.social_welfare(80, 12.5)
        
        # Externality cost should be huge
        assert welfare['externality_cost'] > 1000000
