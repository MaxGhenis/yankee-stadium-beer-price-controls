"""
Comprehensive sanity check tests for economic model.

These tests verify fundamental economic laws, accounting identities,
and data quality constraints that should ALWAYS hold.
"""

import numpy as np
import pytest

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestMonotonicity:
    """Test that outcomes obey economic monotonicity laws."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_profit_decreases_with_tighter_ceiling(self, model):
        """Binding ceilings should monotonically reduce profit."""
        _, optimal_beer, _ = model.optimal_pricing()

        ceilings = np.linspace(optimal_beer - 5, optimal_beer - 1, 5)
        profits = []

        for ceiling in sorted(ceilings):
            _, _, result = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)
            profits.append(result["profit"])

        for i in range(len(profits) - 1):
            assert profits[i] <= profits[i + 1]

    def test_consumption_increases_with_lower_prices(self, model):
        """Lower beer prices should increase per-fan consumption."""
        prices = [8, 10, 12, 14, 16]
        consumptions = [model.stadium_revenue(80, p)["beers_per_fan"] for p in prices]

        for i in range(len(consumptions) - 1):
            assert consumptions[i] >= consumptions[i + 1]

    def test_attendance_decreases_with_ticket_price(self, model):
        """Higher ticket prices should reduce attendance."""
        ticket_prices = [60, 80, 100, 120]
        attendance = [model.total_attendance(p, 12.5) for p in ticket_prices]

        for i in range(len(attendance) - 1):
            assert attendance[i] >= attendance[i + 1]

    def test_externalities_proportional_to_consumption(self, model):
        """External costs should scale linearly with beer quantity."""
        ext_1 = model.externality_cost(1000)
        ext_2 = model.externality_cost(2000)
        assert ext_2 == pytest.approx(ext_1 * 2)


class TestAccountingIdentities:
    """Test that accounting identities always hold."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_revenue_equals_components(self, model):
        """Total revenue must equal ticket + beer revenue."""
        result = model.stadium_revenue(80, 12.5)
        total = result["ticket_revenue"] + result["beer_revenue"]
        assert result["total_revenue"] == pytest.approx(total, rel=1e-6)

    def test_costs_equal_components(self, model):
        """Total costs must equal all cost components."""
        result = model.stadium_revenue(80, 12.5)
        total = result["ticket_costs"] + result["beer_costs"] + result["internalized_costs"]
        assert result["total_costs"] == pytest.approx(total, rel=1e-6)

    def test_profit_equals_revenue_minus_cost(self, model):
        """Profit must equal revenue minus costs."""
        result = model.stadium_revenue(80, 12.5)
        expected_profit = result["total_revenue"] - result["total_costs"]
        assert result["profit"] == pytest.approx(expected_profit, rel=1e-6)

    def test_welfare_accounting_identity(self, model):
        """SW must equal CS + PS - externalities."""
        welfare = model.social_welfare(80, 12.5)
        expected_sw = (
            welfare["consumer_surplus"] + welfare["producer_surplus"] - welfare["externality_cost"]
        )
        assert welfare["social_welfare"] == pytest.approx(expected_sw, rel=1e-6)

    def test_tax_revenue_calculation(self, model):
        """Verify tax calculations match statutory rates."""
        result = model.stadium_revenue(80, 12.5)
        consumer_price = 12.5
        pre_tax = consumer_price / (1 + model.beer_sales_tax_rate)
        total_beers = result["total_beers"]
        expected_sales_tax_rev = (consumer_price - pre_tax) * total_beers
        expected_excise_tax_rev = model.beer_excise_tax * total_beers
        assert result["sales_tax_revenue"] == pytest.approx(expected_sales_tax_rev, rel=1e-6)
        assert result["excise_tax_revenue"] == pytest.approx(expected_excise_tax_rev, rel=1e-6)


class TestComparativeStaticsSigns:
    """Test that comparative statics have correct signs."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_beer_ceiling_raises_tickets(self, model):
        """Lower beer ceiling should raise optimal ticket prices."""
        _, optimal_beer, _ = model.optimal_pricing()
        ticket_low, _, _ = model.optimal_pricing(
            beer_price_control=optimal_beer - 3, ceiling_mode=True
        )
        ticket_high, _, _ = model.optimal_pricing(
            beer_price_control=optimal_beer - 1, ceiling_mode=True
        )
        assert ticket_low > ticket_high

    def test_higher_costs_raise_prices(self, model):
        """Higher marginal costs should raise optimal prices."""
        model_low = StadiumEconomicModel(beer_cost=2.0)
        _, beer_low, _ = model_low.optimal_pricing()
        model_high = StadiumEconomicModel(beer_cost=4.0)
        _, beer_high, _ = model_high.optimal_pricing()
        assert beer_high > beer_low


class TestDataQuality:
    """Test that outputs meet data quality constraints."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_all_quantities_nonnegative(self, model):
        """No negative quantities."""
        result = model.stadium_revenue(80, 12.5)
        nonnegative_fields = [
            "attendance", "beers_per_fan", "total_beers",
            "ticket_revenue", "beer_revenue", "total_revenue",
            "ticket_costs", "beer_costs", "total_costs",
        ]
        for field in nonnegative_fields:
            assert result[field] >= 0

    def test_prices_in_reasonable_range(self, model):
        """Optimal prices should be in reasonable range."""
        ticket, beer, result = model.optimal_pricing()
        assert 20 <= ticket <= 300
        assert 5 <= beer <= 50

    def test_no_nans_or_infs(self, model):
        """Verify no NaN/Inf in outputs."""
        result = model.stadium_revenue(80, 12.5)
        for key, value in result.items():
            if isinstance(value, int | float):
                assert not np.isnan(value)
                assert not np.isinf(value)

    def test_attendance_not_exceeds_capacity(self, model):
        """Attendance should never exceed stadium capacity."""
        result = model.stadium_revenue(10, 5)
        assert result["attendance"] <= model.capacity

    def test_beer_consumption_reasonable(self, model):
        """Beers per fan should be in reasonable range."""
        result = model.stadium_revenue(80, 12.5)
        assert 0 <= result["beers_per_fan"] <= 5


class TestContinuity:
    """Test continuity of outcomes across parameter changes."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_continuous_at_binding_threshold(self, model):
        """Outcomes should be continuous as ceiling crosses optimal."""
        _, optimal_beer, _ = model.optimal_pricing()
        epsilon = 0.1

        t_below, b_below, r_below = model.optimal_pricing(
            beer_price_control=optimal_beer - epsilon, ceiling_mode=True
        )
        t_above, b_above, r_above = model.optimal_pricing(
            beer_price_control=optimal_beer + epsilon, ceiling_mode=True
        )
        t_unc, b_unc, r_unc = model.optimal_pricing()

        assert b_above == pytest.approx(b_unc, rel=1e-2)
        assert t_above == pytest.approx(t_unc, rel=1e-2)
        assert b_below == pytest.approx(optimal_beer - epsilon, rel=1e-6)


class TestEconomicIntuition:
    """Test that model follows basic economic intuition."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_complements_cross_price_negative(self, model):
        """Beer price increases should reduce attendance (endogenous complementarity)."""
        attendance_cheap = model.total_attendance(80, 8)
        attendance_expensive = model.total_attendance(80, 16)
        assert attendance_cheap > attendance_expensive

    def test_demand_slopes_down(self, model):
        """Demand should be downward sloping."""
        r1 = model.stadium_revenue(80, 8)
        r2 = model.stadium_revenue(80, 16)
        assert r1["beers_per_fan"] > r2["beers_per_fan"]

    def test_higher_prices_reduce_welfare(self, model):
        """Higher prices should reduce consumer surplus."""
        cs_low = model.consumer_surplus(80, 10)
        cs_high = model.consumer_surplus(80, 15)
        assert cs_low > cs_high

    def test_optimal_price_above_marginal_cost(self, model):
        """Monopolist should price above marginal cost."""
        _, beer_price, _ = model.optimal_pricing()
        assert beer_price > model.beer_cost

    def test_profit_maximization_works(self, model):
        """Optimal pricing should yield higher profit than arbitrary pricing."""
        _, _, optimal_result = model.optimal_pricing()
        arbitrary_result = model.stadium_revenue(60, 10)
        assert optimal_result["profit"] >= arbitrary_result["profit"] * 0.95


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
            "scenario", "ticket_price", "beer_price", "attendance",
            "total_beers", "profit", "consumer_surplus",
            "externality_cost", "social_welfare",
        ]
        for col in required_cols:
            assert col in results.columns
            assert not results[col].isna().any()

    def test_no_negative_prices(self, simulator):
        """All prices should be positive."""
        results = simulator.run_all_scenarios()
        assert (results["ticket_price"] > 0).all()
        assert (results["beer_price"] >= 0).all()

    def test_no_negative_quantities(self, simulator):
        """All quantities should be non-negative."""
        results = simulator.run_all_scenarios()
        assert (results["attendance"] >= 0).all()
        assert (results["total_beers"] >= 0).all()

    def test_welfare_components_sensible(self, simulator):
        """Welfare components should have reasonable magnitudes."""
        results = simulator.run_all_scenarios()
        assert (results["consumer_surplus"] > 0).all()
        assert results["social_welfare"].mean() > 0


class TestEndogenousCrossPriceEffects:
    """Test that cross-price effects emerge endogenously from utility."""

    def test_cheaper_beer_increases_drinker_attendance(self):
        """Cheaper beer → more drinker CS → lower net cost → more drinkers."""
        model = StadiumEconomicModel()
        a_expensive = model.total_attendance(80, 20)
        a_cheap = model.total_attendance(80, 5)
        assert a_cheap > a_expensive

    def test_nondrinker_attendance_independent_of_beer_price(self):
        """Non-drinkers have CS_beer=0, so beer price doesn't affect them."""
        model = StadiumEconomicModel()
        nondrinker = model.consumer_types[0]
        a1 = model._raw_attendance_by_type(80, 10, nondrinker)
        a2 = model._raw_attendance_by_type(80, 20, nondrinker)
        assert a1 == pytest.approx(a2, rel=1e-6)

    def test_drinker_attendance_depends_on_beer_price(self):
        """Drinkers' attendance should vary with beer price."""
        model = StadiumEconomicModel()
        drinker = model.consumer_types[1]
        a_cheap = model._raw_attendance_by_type(80, 5, drinker)
        a_expensive = model._raw_attendance_by_type(80, 20, drinker)
        assert a_cheap > a_expensive


class TestEdgeCasesRobustness:
    """Test robustness to edge cases."""

    def test_zero_externality_costs(self):
        """Model should work with zero externality costs."""
        model = StadiumEconomicModel()
        model.external_costs["crime"] = 0
        model.external_costs["health"] = 0
        welfare = model.social_welfare(80, 12.5)
        assert welfare["social_welfare"] == pytest.approx(
            welfare["consumer_surplus"] + welfare["producer_surplus"]
        )
        assert welfare["externality_cost"] == 0

    def test_very_high_externality_costs(self):
        """Model should handle very high externality estimates."""
        model = StadiumEconomicModel()
        model.external_costs["crime"] = 30
        model.external_costs["health"] = 20
        welfare = model.social_welfare(80, 12.5)
        assert welfare["externality_cost"] > 1000000

    def test_very_high_internalized_cost(self):
        """Test with very high internalized costs."""
        model = StadiumEconomicModel(experience_degradation_cost=1000.0)
        ticket, beer, result = model.optimal_pricing()
        assert beer > model.beer_cost
        assert ticket > model.ticket_cost
