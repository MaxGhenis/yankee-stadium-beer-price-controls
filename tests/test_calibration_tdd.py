"""
TDD tests for model calibration.

These tests define EXPECTED behavior. Write tests FIRST, then fix model to pass.
"""

import pytest

from src.model import StadiumEconomicModel


class TestCalibrationRequirements:
    """Model MUST match observed prices as approximately optimal."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_optimal_beer_close_to_observed(self, model):
        """
        CRITICAL: Optimal beer should be $12-14, not $19!

        Observed: $12.50
        Acceptable range: $12-14 (within $1.50)
        Current bug: Predicting $19.33
        """
        _, optimal_beer, _ = model.optimal_pricing()

        assert (
            11.5 <= optimal_beer <= 14.5
        ), f"Optimal beer ${optimal_beer:.2f} too far from observed $12.50 (should be $12-14)"

    def test_free_beer_matches_open_bar_data(self, model):
        """Free beer should give ~2.6 beers/fan average (open bar data)."""
        result = model.stadium_revenue(80, 0.01)

        # 60% non-drinkers (0) + 40% drinkers (6.5) = 2.6 average
        assert (
            2.0 <= result["beers_per_fan"] <= 3.5
        ), f"Free beer: {result['beers_per_fan']:.1f} beers/fan (expected 2.6)"

    def test_baseline_consumption_matches_data(self, model):
        """At $12.50, should match 1.0 beers/fan."""
        result = model.stadium_revenue(80, 12.50)

        assert (
            0.8 <= result["beers_per_fan"] <= 1.2
        ), f"Baseline: {result['beers_per_fan']:.2f} beers/fan (should be ~1.0)"

    def test_drinkers_consume_2point5_at_baseline(self, model):
        """Drinkers should consume 2.5 beers at $12.50 (empirical data)."""
        result = model.stadium_revenue(80, 12.50)
        breakdown = result["breakdown_by_type"]

        drinker_consumption = breakdown["Drinker"]["beers_per_fan"]

        assert (
            2.0 <= drinker_consumption <= 3.0
        ), f"Drinkers: {drinker_consumption:.2f} beers (should be ~2.5)"


class TestPriceCeilingBehavior:
    """Price ceilings should work correctly."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_ceiling_always_binds(self, model):
        """Beer price should NEVER exceed ceiling."""
        for ceiling in [5, 7, 10, 13, 15, 18, 20]:
            _, beer_price, _ = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)

            assert (
                beer_price <= ceiling + 0.01
            ), f"Beer ${beer_price:.2f} exceeds ceiling ${ceiling:.2f}!"

    def test_nonbinding_ceiling_no_effect(self, model):
        """Ceiling above optimal should have no effect."""
        _, optimal_beer, _ = model.optimal_pricing()

        # Ceiling well above optimal
        _, ceiling_beer, _ = model.optimal_pricing(
            beer_price_control=optimal_beer + 5, ceiling_mode=True
        )

        assert ceiling_beer == pytest.approx(
            optimal_beer, rel=1e-2
        ), f"Non-binding ceiling changed price: ${ceiling_beer:.2f} != ${optimal_beer:.2f}"


class TestDemandConsistency:
    """Demand should be internally consistent."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_calibration_triangle_consistent(self, model):
        """
        Three calibration points should be mutually consistent:
        1. Free beer → 2.6 beers/fan (open bar data)
        2. $12.50 → 1.0 beers/fan (observed)
        3. $20 → ~0.5 beers/fan (low consumption)

        These define the demand curve.
        """
        r_free = model.stadium_revenue(80, 0.01)
        r_base = model.stadium_revenue(80, 12.50)
        r_high = model.stadium_revenue(80, 20.00)

        # Check all three points
        assert 2.0 <= r_free["beers_per_fan"] <= 3.5, "Free beer calibration"
        assert 0.8 <= r_base["beers_per_fan"] <= 1.2, "Baseline calibration"
        assert 0.3 <= r_high["beers_per_fan"] <= 0.8, "High price calibration"

        # Should be monotone
        assert (
            r_free["beers_per_fan"] > r_base["beers_per_fan"] > r_high["beers_per_fan"]
        ), "Demand should decrease with price"
