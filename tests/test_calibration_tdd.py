"""
TDD tests for model calibration.
"""

import pytest

from src.model import StadiumEconomicModel


class TestCalibrationRequirements:
    """Model MUST match observed prices as approximately optimal."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_optimal_beer_close_to_observed(self, model):
        """Optimal beer should be $12-14."""
        _, optimal_beer, _ = model.optimal_pricing()
        assert 11.5 <= optimal_beer <= 14.5

    def test_free_beer_matches_open_bar_data(self, model):
        """Free beer should give reasonable beers/fan.

        With endogenous attendance, free beer attracts more drinkers,
        so beers_per_fan is higher than simple 0.4*6.5=2.6.
        """
        result = model.stadium_revenue(80, 0.01)
        assert 2.0 <= result["beers_per_fan"] <= 5.0

    def test_baseline_consumption_matches_data(self, model):
        """At $12.50, should match 1.0 beers/fan."""
        result = model.stadium_revenue(80, 12.50)
        assert 0.8 <= result["beers_per_fan"] <= 1.2

    def test_drinkers_consume_2point5_at_baseline(self, model):
        """Drinkers should consume 2.5 beers at $12.50."""
        result = model.stadium_revenue(80, 12.50)
        drinker_consumption = result["breakdown_by_type"]["Drinker"]["beers_per_fan"]
        assert 2.0 <= drinker_consumption <= 3.0


class TestPriceCeilingBehavior:
    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_ceiling_always_binds(self, model):
        for ceiling in [5, 7, 10, 13, 15, 18, 20]:
            _, beer_price, _ = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)
            assert beer_price <= ceiling + 0.01

    def test_nonbinding_ceiling_no_effect(self, model):
        _, optimal_beer, _ = model.optimal_pricing()
        _, ceiling_beer, _ = model.optimal_pricing(
            beer_price_control=optimal_beer + 5, ceiling_mode=True
        )
        assert ceiling_beer == pytest.approx(optimal_beer, rel=1e-2)


class TestDemandConsistency:
    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_calibration_triangle_consistent(self, model):
        """Three calibration points should be mutually consistent."""
        r_free = model.stadium_revenue(80, 0.01)
        r_base = model.stadium_revenue(80, 12.50)
        r_high = model.stadium_revenue(80, 20.00)

        assert 2.0 <= r_free["beers_per_fan"] <= 5.0, "Free beer calibration"
        assert 0.8 <= r_base["beers_per_fan"] <= 1.2, "Baseline calibration"
        assert 0.3 <= r_high["beers_per_fan"] <= 0.8, "High price calibration"

        assert (
            r_free["beers_per_fan"] > r_base["beers_per_fan"] > r_high["beers_per_fan"]
        ), "Demand should decrease with price"
