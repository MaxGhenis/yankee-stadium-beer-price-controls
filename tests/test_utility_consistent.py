"""
TDD tests for utility-consistent model rewrite.

These tests define the EXPECTED behavior of the new model.
Write tests FIRST, then implement the model to pass them.

Key changes tested:
1. Beer consumer surplus uses exact formula from utility function
2. Attendance uses endogenous cross-price effects via net cost
3. Total consumer surplus = A / λ
4. Dead parameters removed from API
5. Compatibility wrappers deleted
"""

import math

import numpy as np
import pytest

from src.model import ConsumerType, StadiumEconomicModel


# ============================================================================
# Phase 1: ConsumerType dataclass simplification
# ============================================================================


class TestConsumerTypeSimplified:
    """ConsumerType should only have name, share, alpha_beer."""

    def test_consumer_type_has_required_fields(self):
        """ConsumerType should have name, share, alpha_beer."""
        ct = ConsumerType(name="Drinker", share=0.4, alpha_beer=43.75)
        assert ct.name == "Drinker"
        assert ct.share == 0.4
        assert ct.alpha_beer == 43.75

    def test_consumer_type_no_alpha_experience(self):
        """ConsumerType should NOT have alpha_experience field."""
        ct = ConsumerType(name="Drinker", share=0.4, alpha_beer=43.75)
        assert not hasattr(ct, "alpha_experience")

    def test_consumer_type_no_income(self):
        """ConsumerType should NOT have income field."""
        ct = ConsumerType(name="Drinker", share=0.4, alpha_beer=43.75)
        assert not hasattr(ct, "income")


# ============================================================================
# Phase 2: Constructor cleanup
# ============================================================================


class TestConstructorCleanup:
    """Constructor should not accept dead parameters."""

    def test_default_initialization(self):
        """Model initializes with defaults."""
        model = StadiumEconomicModel()
        assert model.capacity == 46537
        assert model.base_ticket_price == 80.0
        assert model.base_beer_price == 12.5

    def test_has_ticket_price_sensitivity(self):
        """Model should have ticket_price_sensitivity parameter."""
        model = StadiumEconomicModel()
        assert hasattr(model, "ticket_price_sensitivity")
        # λ is calibrated jointly with k; should be in reasonable range
        # Implied elasticity at P=$80: -λ*80 should be between -0.5 and -2.0
        assert 0.005 < model.ticket_price_sensitivity < 0.03

    def test_has_beer_max_per_person(self):
        """Model should have beer_max_per_person."""
        model = StadiumEconomicModel()
        assert hasattr(model, "beer_max_per_person")
        assert model.beer_max_per_person == 10.0

    def test_no_cross_price_elasticity_param(self):
        """Constructor should NOT accept cross_price_elasticity."""
        # Should raise TypeError for unexpected keyword
        with pytest.raises(TypeError):
            StadiumEconomicModel(cross_price_elasticity=0.1)

    def test_no_beer_demand_sensitivity_param(self):
        """Constructor should NOT accept beer_demand_sensitivity."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(beer_demand_sensitivity=0.3)

    def test_no_ticket_elasticity_param(self):
        """Constructor should NOT accept ticket_elasticity."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(ticket_elasticity=-0.625)

    def test_no_beer_elasticity_param(self):
        """Constructor should NOT accept beer_elasticity."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(beer_elasticity=-0.965)

    def test_no_consumer_income_param(self):
        """Constructor should NOT accept consumer_income."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(consumer_income=200)

    def test_no_captive_demand_share_param(self):
        """Constructor should NOT accept captive_demand_share."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(captive_demand_share=0.5)

    def test_no_alpha_param(self):
        """Constructor should NOT accept alpha."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(alpha=1.5)

    def test_no_beta_param(self):
        """Constructor should NOT accept beta."""
        with pytest.raises(TypeError):
            StadiumEconomicModel(beta=3.0)


# ============================================================================
# Phase 3: Beer consumer surplus (exact from utility)
# ============================================================================


class TestBeerConsumerSurplus:
    """Beer CS should use exact formula from quasilinear utility."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_method_exists(self, model):
        """_beer_consumer_surplus method should exist."""
        assert hasattr(model, "_beer_consumer_surplus")

    def test_drinker_cs_at_baseline(self, model):
        """Drinker CS at $12.50 should be α·ln(α/P) - (α - P)."""
        alpha = 43.75
        P = 12.50
        # Unconstrained formula: α·ln(α/P) - (α - P)
        expected = alpha * math.log(alpha / P) - (alpha - P)
        # expected = 43.75 * ln(3.5) - 31.25 ≈ 43.75 * 1.2528 - 31.25 ≈ 54.81 - 31.25 ≈ 23.56

        drinker_type = model.consumer_types[1]  # Drinker
        actual = model._beer_consumer_surplus(P, drinker_type)
        assert actual == pytest.approx(expected, rel=1e-4)

    def test_nondrinker_cs_zero(self, model):
        """Non-drinker CS at $12.50 should be 0 (α ≤ P)."""
        nondrinker = model.consumer_types[0]
        cs = model._beer_consumer_surplus(12.50, nondrinker)
        assert cs == 0.0

    def test_cs_nonnegative(self, model):
        """CS should never be negative."""
        for ct in model.consumer_types:
            for price in [1, 5, 10, 15, 20, 50]:
                cs = model._beer_consumer_surplus(price, ct)
                assert cs >= 0, f"CS negative for {ct.name} at ${price}"

    def test_cs_decreases_with_price(self, model):
        """Higher prices should reduce CS."""
        drinker = model.consumer_types[1]
        cs_low = model._beer_consumer_surplus(8.0, drinker)
        cs_high = model._beer_consumer_surplus(15.0, drinker)
        assert cs_low > cs_high

    def test_cs_at_bmax_constraint(self, model):
        """When constrained at B_max, CS = α·ln(B_max+1) - P·B_max."""
        drinker = model.consumer_types[1]
        # At very low price, B = α/P - 1 might exceed B_max
        # E.g., at P=$1, B = 43.75/1 - 1 = 42.75, capped at B_max=10
        # CS should be α·ln(B_max+1) - P·B_max = 43.75*ln(11) - 1*10
        alpha = 43.75
        B_max = model.beer_max_per_person
        P = 1.0
        expected = alpha * math.log(B_max + 1) - P * B_max
        actual = model._beer_consumer_surplus(P, drinker)
        assert actual == pytest.approx(expected, rel=1e-4)

    def test_cs_zero_when_alpha_leq_price(self, model):
        """CS should be 0 when α ≤ P (non-buyer)."""
        nondrinker = model.consumer_types[0]  # alpha=1.0
        # At any price >= 1.0, non-drinker buys nothing
        for price in [1.0, 5.0, 12.50, 20.0]:
            cs = model._beer_consumer_surplus(price, nondrinker)
            assert cs == 0.0, f"Non-drinker CS should be 0 at ${price}"


# ============================================================================
# Phase 4: Endogenous attendance via net cost
# ============================================================================


class TestEndogenousAttendance:
    """Attendance should use net_cost = P_T - CS_beer (endogenous cross-price)."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_baseline_attendance_reasonable(self, model):
        """Attendance at baseline should be ~85% capacity."""
        attendance = model.total_attendance(80.0, 12.50)
        assert 0.80 * model.capacity <= attendance <= 0.90 * model.capacity

    def test_attendance_decreases_with_ticket_price(self, model):
        """Higher tickets → lower attendance."""
        a_low = model.total_attendance(60, 12.50)
        a_high = model.total_attendance(120, 12.50)
        assert a_high < a_low

    def test_cheaper_beer_increases_drinker_attendance(self, model):
        """Cheaper beer → higher CS_beer → lower net cost → more drinkers attend."""
        a_expensive = model.total_attendance(80, 20.0)
        a_cheap = model.total_attendance(80, 5.0)
        assert a_cheap > a_expensive

    def test_beer_price_doesnt_affect_nondrinker_attendance(self, model):
        """Non-drinkers have CS_beer=0, so beer price shouldn't affect them."""
        # Get non-drinker attendance at two beer prices
        # Need to look at type-level attendance
        nondrinker = model.consumer_types[0]
        a1 = model._raw_attendance_by_type(80, 10.0, nondrinker)
        a2 = model._raw_attendance_by_type(80, 20.0, nondrinker)
        # Non-drinker alpha=1.0, CS_beer=0 at both prices, so attendance identical
        assert a1 == pytest.approx(a2, rel=1e-6)

    def test_endogenous_cross_price_effect_magnitude(self, model):
        """Cross-price effect should be meaningful for drinkers."""
        # Drinker CS at $12.50 ≈ $23.56
        # Drinker CS at $7.00: α·ln(α/P) - (α-P) = 43.75*ln(6.25) - 36.75 ≈ 43.57
        # Net cost change: (80 - 43.57) - (80 - 23.56) = -20.01
        # Attendance increase: exp(-λ * (-20.01)) where λ = 0.0078125
        # = exp(0.156) ≈ 1.169 → ~17% more drinker attendance
        a_baseline = model.total_attendance(80, 12.50)
        a_cheap = model.total_attendance(80, 7.0)
        pct_increase = (a_cheap - a_baseline) / a_baseline
        # Should be meaningful positive effect (5-15%)
        assert pct_increase > 0.02, "Cheap beer should increase attendance"
        assert pct_increase < 0.30, "Effect shouldn't be unreasonably large"

    def test_raw_attendance_method_exists(self, model):
        """_raw_attendance_by_type should exist (pre-capacity-scaling)."""
        assert hasattr(model, "_raw_attendance_by_type")

    def test_capacity_constraint_honored(self, model):
        """Total attendance should never exceed capacity."""
        # Very low prices should still respect capacity
        attendance = model.total_attendance(10, 1.0)
        assert attendance <= model.capacity

    def test_no_attendance_demand_method(self, model):
        """_attendance_demand compat wrapper should be deleted."""
        assert not hasattr(model, "_attendance_demand")

    def test_no_beers_per_fan_demand_method(self, model):
        """_beers_per_fan_demand compat wrapper should be deleted."""
        assert not hasattr(model, "_beers_per_fan_demand")

    def test_precomputed_baseline_values(self, model):
        """Model should precompute baseline CS and net cost per type."""
        assert hasattr(model, "_baseline_cs_beer")
        assert hasattr(model, "_baseline_net_cost")
        assert len(model._baseline_cs_beer) == len(model.consumer_types)
        assert len(model._baseline_net_cost) == len(model.consumer_types)


# ============================================================================
# Phase 5: Consumer surplus = A / λ
# ============================================================================


class TestConsumerSurplusFormula:
    """CS should use the integral under semi-log demand: A / λ."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_cs_positive_at_baseline(self, model):
        """CS should be positive at baseline prices."""
        cs = model.consumer_surplus(80, 12.50)
        assert cs > 0

    def test_cs_formula_is_attendance_over_lambda(self, model):
        """CS = total_attendance / ticket_price_sensitivity."""
        attendance = model.total_attendance(80, 12.50)
        expected_cs = attendance / model.ticket_price_sensitivity
        actual_cs = model.consumer_surplus(80, 12.50)
        assert actual_cs == pytest.approx(expected_cs, rel=1e-6)

    def test_cs_decreases_with_higher_ticket_price(self, model):
        """Higher ticket prices → less attendance → less CS."""
        cs_low = model.consumer_surplus(60, 12.50)
        cs_high = model.consumer_surplus(120, 12.50)
        assert cs_low > cs_high

    def test_cs_increases_with_cheaper_beer(self, model):
        """Cheaper beer → more drinker attendance → more CS."""
        cs_expensive = model.consumer_surplus(80, 20.0)
        cs_cheap = model.consumer_surplus(80, 8.0)
        assert cs_cheap > cs_expensive

    def test_social_welfare_accounting(self, model):
        """SW = CS + PS - externalities should still hold."""
        sw = model.social_welfare(80, 12.50)
        expected = sw["consumer_surplus"] + sw["producer_surplus"] - sw["externality_cost"]
        assert sw["social_welfare"] == pytest.approx(expected, rel=1e-6)


# ============================================================================
# Phase 6: Beer demand unchanged
# ============================================================================


class TestBeerDemandUnchanged:
    """Beer demand formula should be unchanged: B = max(0, min(α/P - 1, B_max))."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_drinker_consumption_at_baseline(self, model):
        """Drinkers should consume 2.5 beers at $12.50."""
        drinker = model.consumer_types[1]
        beers = model._beers_consumed_by_type(12.50, drinker)
        # α/P - 1 = 43.75/12.50 - 1 = 2.5
        assert beers == pytest.approx(2.5, rel=1e-4)

    def test_nondrinker_zero_at_baseline(self, model):
        """Non-drinkers should consume 0 at $12.50."""
        nondrinker = model.consumer_types[0]
        beers = model._beers_consumed_by_type(12.50, nondrinker)
        assert beers == 0

    def test_aggregate_consumption_one_beer(self, model):
        """Aggregate at $12.50 should be ~1.0 beers/fan."""
        result = model.stadium_revenue(80, 12.50)
        assert 0.85 <= result["beers_per_fan"] <= 1.15

    def test_consumption_capped_at_bmax(self, model):
        """Consumption should be capped at beer_max_per_person."""
        drinker = model.consumer_types[1]
        # At $1, B = 43.75/1 - 1 = 42.75, should be capped at 10
        beers = model._beers_consumed_by_type(1.0, drinker)
        assert beers == model.beer_max_per_person

    def test_consumption_monotone_decreasing(self, model):
        """Consumption should decrease with price."""
        drinker = model.consumer_types[1]
        prices = [5, 8, 10, 12.5, 15, 20]
        consumptions = [model._beers_consumed_by_type(p, drinker) for p in prices]
        for i in range(len(consumptions) - 1):
            assert consumptions[i] >= consumptions[i + 1]


# ============================================================================
# Phase 7: Calibration targets still met
# ============================================================================


class TestCalibrationTargets:
    """Model should still match empirical calibration targets."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_optimal_beer_near_observed(self, model):
        """Optimal beer should be $12-14."""
        _, opt_beer, _ = model.optimal_pricing()
        assert 11.5 <= opt_beer <= 14.5

    def test_drinkers_consume_2point5(self, model):
        """Drinkers consume 2.5 beers at baseline."""
        r = model.stadium_revenue(80, 12.50)
        drinker_beers = r["breakdown_by_type"]["Drinker"]["beers_per_fan"]
        assert 2.2 <= drinker_beers <= 2.8

    def test_aggregate_consumption_one(self, model):
        """Aggregate consumption ~1.0 beers/fan."""
        r = model.stadium_revenue(80, 12.50)
        assert 0.85 <= r["beers_per_fan"] <= 1.15

    def test_baseline_attendance_85pct(self, model):
        """Attendance should be ~85% of capacity at baseline."""
        attendance = model.total_attendance(80, 12.50)
        pct = attendance / model.capacity
        assert 0.80 <= pct <= 0.90


# ============================================================================
# Phase 8: Qualitative results preserved
# ============================================================================


class TestQualitativeResults:
    """Key qualitative results should still hold with new model."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_beer_ceiling_raises_tickets(self, model):
        """Lower beer ceiling → higher optimal ticket prices."""
        _, opt_beer, _ = model.optimal_pricing()
        t_tight, _, _ = model.optimal_pricing(beer_price_control=opt_beer - 3, ceiling_mode=True)
        t_loose, _, _ = model.optimal_pricing(beer_price_control=opt_beer - 1, ceiling_mode=True)
        assert t_tight > t_loose

    def test_ceiling_increases_per_fan_consumption(self, model):
        """Cheap beer → more consumption per fan."""
        _, opt_beer, _ = model.optimal_pricing()
        _, _, r_base = model.optimal_pricing()
        t_ceil, b_ceil, r_ceil = model.optimal_pricing(
            beer_price_control=opt_beer / 2, ceiling_mode=True
        )
        assert r_ceil["beers_per_fan"] > r_base["beers_per_fan"]

    def test_selection_effect_toward_drinkers(self, model):
        """Cheap beer → crowd shifts toward drinkers."""
        _, opt_beer, _ = model.optimal_pricing()
        _, _, r_base = model.optimal_pricing()
        t_ceil, _, r_ceil = model.optimal_pricing(
            beer_price_control=opt_beer / 2, ceiling_mode=True
        )
        # Drinker share should increase
        drinker_share_base = r_base["breakdown_by_type"]["Drinker"]["attendance"] / r_base[
            "attendance"
        ]
        drinker_share_ceil = r_ceil["breakdown_by_type"]["Drinker"]["attendance"] / r_ceil[
            "attendance"
        ]
        assert drinker_share_ceil > drinker_share_base

    def test_profit_decreases_with_tighter_ceiling(self, model):
        """Tighter ceilings should reduce profit."""
        _, opt_beer, _ = model.optimal_pricing()
        profits = []
        for ceiling in [opt_beer - 4, opt_beer - 2, opt_beer]:
            _, _, r = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)
            profits.append(r["profit"])
        # Should be monotonically increasing
        for i in range(len(profits) - 1):
            assert profits[i] <= profits[i + 1]

    def test_externalities_increase_with_cheaper_beer(self, model):
        """Cheaper beer → more consumption → more externalities."""
        _, opt_beer, _ = model.optimal_pricing()
        sw_base = model.social_welfare(80, opt_beer)
        t_ceil, b_ceil, _ = model.optimal_pricing(
            beer_price_control=opt_beer / 2, ceiling_mode=True
        )
        sw_ceil = model.social_welfare(t_ceil, b_ceil)
        assert sw_ceil["externality_cost"] > sw_base["externality_cost"]


# ============================================================================
# Phase 9: Revenue and accounting unchanged
# ============================================================================


class TestRevenueAccountingUnchanged:
    """Revenue accounting, tax structure, costs should be unchanged."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_revenue_structure_keys(self, model):
        """Revenue dict should have all expected keys."""
        result = model.stadium_revenue(80, 12.5)
        for key in [
            "attendance",
            "beers_per_fan",
            "total_beers",
            "ticket_revenue",
            "beer_revenue",
            "total_revenue",
            "ticket_costs",
            "beer_costs",
            "internalized_costs",
            "total_costs",
            "profit",
            "sales_tax_revenue",
            "excise_tax_revenue",
            "breakdown_by_type",
        ]:
            assert key in result

    def test_profit_equals_revenue_minus_costs(self, model):
        """Accounting identity: profit = revenue - costs."""
        result = model.stadium_revenue(80, 12.5)
        expected = result["total_revenue"] - result["total_costs"]
        assert result["profit"] == pytest.approx(expected, rel=1e-6)

    def test_internalized_cost_formula(self, model):
        """C = k * (Q/1000)^2."""
        result = model.stadium_revenue(80, 12.5)
        Q = result["total_beers"]
        expected = model.experience_degradation_cost * (Q / 1000) ** 2
        assert result["internalized_costs"] == pytest.approx(expected, rel=1e-6)

    def test_tax_calculations(self, model):
        """Tax calculations should be correct."""
        result = model.stadium_revenue(80, 12.5)
        pre_tax = 12.5 / (1 + model.beer_sales_tax_rate)
        expected_sales_tax = (12.5 - pre_tax) * result["total_beers"]
        expected_excise = model.beer_excise_tax * result["total_beers"]
        assert result["sales_tax_revenue"] == pytest.approx(expected_sales_tax, rel=1e-6)
        assert result["excise_tax_revenue"] == pytest.approx(expected_excise, rel=1e-6)
