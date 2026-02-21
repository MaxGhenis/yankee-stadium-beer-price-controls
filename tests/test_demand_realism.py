"""
TDD tests for realistic demand behavior.
"""

import numpy as np
import pytest

from src.model import StadiumEconomicModel


class TestRealisticConsumption:
    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_free_beer_realistic(self, model):
        result = model.stadium_revenue(80, 0.01)
        # With endogenous attendance: free beer attracts more drinkers
        assert 2.0 <= result["beers_per_fan"] <= 5.0

    def test_no_one_drinks_100_beers(self, model):
        result = model.stadium_revenue(80, 0.10)
        assert result["beers_per_fan"] < 15

    def test_very_cheap_beer_reasonable(self, model):
        result = model.stadium_revenue(80, 1.00)
        assert result["beers_per_fan"] < 10

    def test_five_dollar_beer_reasonable(self, model):
        result = model.stadium_revenue(80, 5.00)
        assert 1.5 <= result["beers_per_fan"] <= 5.0

    def test_baseline_matches_data(self, model):
        result = model.stadium_revenue(80, 12.50)
        assert 0.8 <= result["beers_per_fan"] <= 1.2

    def test_expensive_beer_low_consumption(self, model):
        result = model.stadium_revenue(80, 20.00)
        assert result["beers_per_fan"] < 1.0

    def test_attendance_respects_capacity(self, model):
        for ticket_p in [10, 50, 100]:
            for beer_p in [0.50, 5, 15]:
                result = model.stadium_revenue(ticket_p, beer_p)
                assert result["attendance"] <= model.capacity

    def test_total_beers_respects_capacity(self, model):
        result = model.stadium_revenue(80, 1.00)
        max_possible = model.capacity * 10
        assert result["total_beers"] <= max_possible


class TestDemandFunctionalForm:
    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_consumption_monotone_decreasing_in_price(self, model):
        prices = [3, 5, 7, 10, 13, 15]
        consumptions = [model.stadium_revenue(80, p)["beers_per_fan"] for p in prices]
        for i in range(len(consumptions) - 1):
            assert consumptions[i] >= consumptions[i + 1]

    def test_consumption_smooth_not_kinked(self, model):
        prices = [10, 10.5, 11, 11.5, 12, 12.5]
        consumptions = [model.stadium_revenue(80, p)["beers_per_fan"] for p in prices]
        diffs = [consumptions[i] - consumptions[i + 1] for i in range(len(consumptions) - 1)]
        std_diffs = np.std(diffs)
        mean_diff = np.mean([abs(d) for d in diffs])
        cv = std_diffs / mean_diff if mean_diff > 0 else 0
        assert cv < 2.0

    def test_price_elasticity_reasonable_range(self, model):
        p = 12.50
        delta_p = 0.50
        q1 = model.stadium_revenue(80, p)["beers_per_fan"]
        q2 = model.stadium_revenue(80, p + delta_p)["beers_per_fan"]
        pct_change_q = (q2 - q1) / q1 if q1 > 0 else 0
        pct_change_p = delta_p / p
        elasticity = pct_change_q / pct_change_p if pct_change_p != 0 else 0
        assert elasticity < 0
        assert -3.0 <= elasticity <= -0.3
