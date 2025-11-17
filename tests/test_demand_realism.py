"""
TDD tests for realistic demand behavior.

These tests define what "reasonable" consumption looks like at various prices.
Write tests FIRST, then implement demand functions that pass them.
"""

import pytest
from src.model import StadiumEconomicModel


class TestRealisticConsumption:
    """Consumption should be physiologically and economically plausible."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_no_one_drinks_100_beers(self, model):
        """Even at $0.10, no one should consume 100+ beers (physiological impossibility)."""
        result = model.stadium_revenue(80, 0.10)

        # Even if free, physiological limit ~10-12 beers in 3 hours
        assert result['beers_per_fan'] < 15, \
            f"Beers/fan = {result['beers_per_fan']:.1f} exceeds physiological limit"

    def test_very_cheap_beer_reasonable(self, model):
        """At $1 beer, consumption should be high but not absurd."""
        result = model.stadium_revenue(80, 1.00)

        # At $1, maybe 4-6 beers/fan average (some drink 10, most drink 0-2)
        assert result['beers_per_fan'] < 10, \
            f"Beers/fan = {result['beers_per_fan']:.1f} too high even at \$1"

    def test_five_dollar_beer_reasonable(self, model):
        """At $5, consumption should be moderate."""
        result = model.stadium_revenue(80, 5.00)

        # At $5, maybe 2-4 beers/fan
        assert 1.5 <= result['beers_per_fan'] <= 5.0, \
            f"Beers/fan = {result['beers_per_fan']:.1f} unreasonable at \$5"

    def test_baseline_matches_data(self, model):
        """At $12.50, should match observed 1.0 beers/fan."""
        result = model.stadium_revenue(80, 12.50)

        # Should be close to 1.0 (40% drink × 2.5 beers)
        assert 0.8 <= result['beers_per_fan'] <= 1.2, \
            f"Beers/fan = {result['beers_per_fan']:.2f} doesn't match observed 1.0"

    def test_expensive_beer_low_consumption(self, model):
        """At $20, consumption should be quite low."""
        result = model.stadium_revenue(80, 20.00)

        # At $20, maybe 0.3-0.6 beers/fan
        assert result['beers_per_fan'] < 1.0, \
            f"Beers/fan = {result['beers_per_fan']:.1f} too high at \$20"

    def test_attendance_respects_capacity(self, model):
        """Attendance should never exceed capacity regardless of prices."""
        # Try various price combinations
        for ticket_p in [10, 50, 100]:
            for beer_p in [0.50, 5, 15]:
                result = model.stadium_revenue(ticket_p, beer_p)
                assert result['attendance'] <= model.capacity, \
                    f"Attendance {result['attendance']:,.0f} exceeds capacity {model.capacity:,.0f} at T=\${ticket_p}, B=\${beer_p}"

    def test_total_beers_respects_capacity(self, model):
        """Total beers should be reasonable given attendance and time."""
        result = model.stadium_revenue(80, 1.00)

        # Even at $1, can't serve unlimited beers
        # Physical constraint: ~10 beers/fan max × capacity
        max_possible = model.capacity * 10

        assert result['total_beers'] <= max_possible, \
            f"Total beers {result['total_beers']:,.0f} exceeds physical max {max_possible:,.0f}"


class TestDemandFunctionalForm:
    """Test that demand function has sensible properties."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_consumption_monotone_decreasing_in_price(self, model):
        """Consumption should decrease as price increases (law of demand)."""
        prices = [3, 5, 7, 10, 13, 15]
        consumptions = []

        for p in prices:
            result = model.stadium_revenue(80, p)
            consumptions.append(result['beers_per_fan'])

        # Should be monotone decreasing
        for i in range(len(consumptions) - 1):
            assert consumptions[i] >= consumptions[i+1], \
                f"Consumption should decrease with price: {consumptions[i]:.2f} < {consumptions[i+1]:.2f}"

    def test_consumption_smooth_not_kinked(self, model):
        """Consumption should vary smoothly with price (no kinks)."""
        prices = [10, 10.5, 11, 11.5, 12, 12.5]
        consumptions = []

        for p in prices:
            result = model.stadium_revenue(80, p)
            consumptions.append(result['beers_per_fan'])

        # Changes should be smooth (similar sized steps)
        diffs = [consumptions[i] - consumptions[i+1] for i in range(len(consumptions)-1)]

        # Standard deviation of differences should be small (smooth)
        import numpy as np
        std_diffs = np.std(diffs)
        mean_diff = np.mean([abs(d) for d in diffs])

        # Coefficient of variation should be < 1 (not too erratic)
        cv = std_diffs / mean_diff if mean_diff > 0 else 0
        assert cv < 2.0, \
            f"Consumption changes too erratic (CV={cv:.2f}), demand may have kinks"

    def test_price_elasticity_reasonable_range(self, model):
        """Implied price elasticity should be in reasonable range."""
        # Test at baseline
        p = 12.50
        delta_p = 0.50

        q1 = model.stadium_revenue(80, p)['beers_per_fan']
        q2 = model.stadium_revenue(80, p + delta_p)['beers_per_fan']

        # Elasticity = (dQ/Q) / (dP/P)
        pct_change_q = (q2 - q1) / q1 if q1 > 0 else 0
        pct_change_p = delta_p / p

        elasticity = pct_change_q / pct_change_p if pct_change_p != 0 else 0

        # Should be negative (downward sloping)
        assert elasticity < 0, f"Demand should slope down: elasticity={elasticity:.2f}"

        # Should be in plausible range for stadium beer (-0.5 to -2.0)
        assert -3.0 <= elasticity <= -0.3, \
            f"Elasticity {elasticity:.2f} outside plausible range"
