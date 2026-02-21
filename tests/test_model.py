"""
Unit tests for the stadium economic model.

Tests cover:
- Demand function calibration
- Revenue calculations
- Welfare metrics
- Edge cases
"""

import numpy as np
import pytest

from src.model import StadiumEconomicModel


class TestModelInitialization:
    """Test model initialization and parameter validation."""

    def test_default_initialization(self):
        """Model initializes with default parameters."""
        model = StadiumEconomicModel()
        assert model.capacity == 46537
        assert model.base_ticket_price == 80.0
        assert model.base_beer_price == 12.5

    def test_custom_parameters(self):
        """Model accepts custom parameters."""
        model = StadiumEconomicModel(capacity=50000, base_ticket_price=100.0, base_beer_price=15.0)
        assert model.capacity == 50000
        assert model.base_ticket_price == 100.0
        assert model.base_beer_price == 15.0


class TestDemandFunctions:
    """Test demand function behavior and calibration."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_attendance_at_baseline(self, model):
        """Attendance at baseline prices should be reasonable."""
        attendance = model.total_attendance(model.base_ticket_price, model.base_beer_price)
        assert 0.7 * model.capacity <= attendance <= 0.95 * model.capacity

    def test_attendance_decreases_with_ticket_price(self, model):
        """Higher ticket prices should reduce attendance."""
        base_attendance = model.total_attendance(80, 12.5)
        high_price_attendance = model.total_attendance(120, 12.5)
        assert high_price_attendance < base_attendance

    def test_attendance_decreases_with_beer_price(self, model):
        """Higher beer prices should reduce attendance (endogenous complementarity)."""
        base_attendance = model.total_attendance(80, 12.5)
        high_beer_attendance = model.total_attendance(80, 20.0)
        assert high_beer_attendance < base_attendance

    def test_beer_demand_at_baseline(self, model):
        """Beer consumption at baseline should match literature (~40% drink)."""
        result = model.stadium_revenue(model.base_beer_price, model.base_beer_price)
        # Use stadium_revenue to get aggregate beers_per_fan
        result = model.stadium_revenue(80, 12.5)
        assert 0.8 <= result["beers_per_fan"] <= 1.5

    def test_beer_demand_decreases_with_price(self, model):
        """Higher beer prices should reduce consumption."""
        r1 = model.stadium_revenue(80, 12.5)
        r2 = model.stadium_revenue(80, 20.0)
        assert r2["beers_per_fan"] < r1["beers_per_fan"]

    def test_free_beer_returns_high_quantity(self, model):
        """Free beer should return high quantity.

        With endogenous cross-price: free beer → huge drinker CS → more
        drinkers attend → higher beers_per_fan than simple 0.4*6.5=2.6.
        """
        r = model.stadium_revenue(80, 0.01)
        assert 2.0 <= r["beers_per_fan"] <= 5.0

    def test_beer_ban_reduces_attendance(self, model):
        """Beer ban (very high price) should reduce attendance via endogenous effect."""
        normal_attendance = model.total_attendance(80, 12.5)
        # Use very high price to simulate ban for drinkers
        ban_attendance = model.total_attendance(80, 1e6)
        assert ban_attendance < normal_attendance
        assert ban_attendance >= 0.80 * normal_attendance


class TestRevenueCalculations:
    """Test revenue and cost calculations."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_revenue_structure(self, model):
        """Revenue calculation returns correct structure."""
        result = model.stadium_revenue(80, 12.5)
        required_keys = [
            "attendance", "beers_per_fan", "total_beers",
            "ticket_revenue", "beer_revenue", "total_revenue",
            "ticket_costs", "beer_costs", "total_costs", "profit",
        ]
        for key in required_keys:
            assert key in result

    def test_revenue_positive(self, model):
        """Revenue should be positive at reasonable prices."""
        result = model.stadium_revenue(80, 12.5)
        assert result["total_revenue"] > 0
        assert result["ticket_revenue"] > 0
        assert result["beer_revenue"] >= 0

    def test_profit_calculation(self, model):
        """Profit should equal revenue minus costs."""
        result = model.stadium_revenue(80, 12.5)
        expected_profit = result["total_revenue"] - result["total_costs"]
        assert abs(result["profit"] - expected_profit) < 0.01


class TestOptimalPricing:
    """Test profit-maximizing price calculations."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_optimal_pricing_finds_solution(self, model):
        """Optimization should find valid prices."""
        ticket_price, beer_price, result = model.optimal_pricing()
        assert ticket_price > 0
        assert beer_price > model.beer_cost
        assert result["profit"] > 0

    def test_optimal_beer_price_reasonable(self, model):
        """Optimal beer price should be near observed."""
        ticket_price, beer_price, result = model.optimal_pricing()
        assert beer_price > model.beer_cost
        assert result["profit"] > 0
        assert beer_price < 30.0

    def test_price_ceiling_binds(self, model):
        """Price ceiling should constrain optimal price."""
        _, unconstrained_price, _ = model.optimal_pricing()
        if unconstrained_price > 10:
            _, constrained_price, _ = model.optimal_pricing(beer_price_control=8.0)
            assert constrained_price == 8.0


class TestWelfareCalculations:
    """Test consumer surplus, producer surplus, and social welfare."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_consumer_surplus_positive(self, model):
        """Consumer surplus should be positive at normal prices."""
        cs = model.consumer_surplus(80, 12.5)
        assert cs > 0

    def test_producer_surplus_equals_profit(self, model):
        """Producer surplus should equal profit."""
        ps = model.producer_surplus(80, 12.5)
        result = model.stadium_revenue(80, 12.5)
        assert abs(ps - result["profit"]) < 0.01

    def test_externality_cost_calculation(self, model):
        """Externality costs should increase with beer consumption."""
        result = model.stadium_revenue(80, 12.5)
        ext_cost = model.externality_cost(result["total_beers"])
        assert ext_cost > 0
        assert ext_cost == result["total_beers"] * (2.5 + 1.5)

    def test_social_welfare_structure(self, model):
        """Social welfare should include all components."""
        sw = model.social_welfare(80, 12.5)
        for key in ["consumer_surplus", "producer_surplus", "externality_cost", "social_welfare"]:
            assert key in sw

    def test_social_welfare_calculation(self, model):
        """Social welfare should equal CS + PS - externalities."""
        sw = model.social_welfare(80, 12.5)
        expected_sw = sw["consumer_surplus"] + sw["producer_surplus"] - sw["externality_cost"]
        assert abs(sw["social_welfare"] - expected_sw) < 0.01


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_very_high_prices(self, model):
        """Model should handle very high prices gracefully."""
        result = model.stadium_revenue(500, 50)
        assert result["attendance"] >= 0
        assert result["total_beers"] >= 0

    def test_prices_at_cost(self, model):
        """Model should handle prices at marginal cost."""
        result = model.stadium_revenue(model.ticket_cost, model.beer_cost)
        assert result["profit"] <= 0.01

    def test_capacity_constraint(self, model):
        """Attendance should never exceed capacity."""
        attendance = model.total_attendance(10, 5)
        assert attendance <= model.capacity


class TestStadiumSpecificFeatures:
    """Test stadium-specific economic features."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_complementarity_ticket_beer(self, model):
        """Tickets and beer should be complements (endogenous)."""
        attendance_cheap_beer = model.total_attendance(80, 10)
        attendance_expensive_beer = model.total_attendance(80, 20)
        assert attendance_expensive_beer < attendance_cheap_beer

    def test_log_concavity_of_ticket_demand(self, model):
        """Ticket demand should be log-concave (semi-log structure)."""
        alpha = 0.5
        A1 = model.total_attendance(60, 12.5)
        A2 = model.total_attendance(100, 12.5)
        A_mid = model.total_attendance(alpha * 60 + (1 - alpha) * 100, 12.5)

        expected_log_a = alpha * np.log(A1) + (1 - alpha) * np.log(A2)
        actual_log_a = np.log(A_mid)
        assert (
            actual_log_a == pytest.approx(expected_log_a, rel=1e-4)
            or actual_log_a >= expected_log_a
        ), f"Ticket demand should be log-concave: {actual_log_a} < {expected_log_a}"
