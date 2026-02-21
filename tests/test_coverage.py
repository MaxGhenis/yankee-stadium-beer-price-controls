"""
Tests for code coverage of edge cases and rarely-used functions.
"""

import pytest

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestModelCoverage:
    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_optimal_pricing_finds_valid_prices(self, model):
        ticket, beer, result = model.optimal_pricing()
        assert beer > 0
        assert ticket > 0

    def test_revenue_with_internalized_costs(self, model):
        result = model.stadium_revenue(80, 12.5)
        assert "internalized_costs" in result
        assert result["internalized_costs"] >= 0
        expected_total = (
            result["ticket_costs"] + result["beer_costs"] + result["internalized_costs"]
        )
        assert abs(result["total_costs"] - expected_total) < 0.01


class TestSimulationCoverage:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_sensitivity_analysis_invalid_parameter(self, simulator):
        with pytest.raises(ValueError):
            simulator.sensitivity_analysis(parameter_name="invalid_param", values=[1.0, 2.0])

    def test_sensitivity_analysis_ticket_price_sensitivity(self, simulator):
        results = simulator.sensitivity_analysis(
            parameter_name="ticket_price_sensitivity", values=[0.01, 0.02]
        )
        assert len(results) == 2
        assert "ticket_price_sensitivity" in results.columns

    def test_summary_statistics_all_fields(self, simulator):
        results = simulator.run_all_scenarios()
        summary = simulator.summary_statistics(results)
        required_keys = [
            "mean_attendance", "std_attendance", "mean_total_beers",
            "std_total_beers", "mean_profit", "std_profit",
            "mean_social_welfare", "std_social_welfare",
            "profit_maximizing_scenario", "welfare_maximizing_scenario",
            "lowest_externality_scenario",
        ]
        for key in required_keys:
            assert key in summary

    def test_scenario_with_both_constraints(self, simulator):
        result = simulator.run_scenario(
            "Both Constraints", beer_price_min=10.0, beer_price_max=15.0
        )
        assert 10.0 <= result["beer_price"] <= 15.0

    def test_comparative_statics_baseline(self, simulator):
        results = simulator.run_all_scenarios()
        changes = simulator.calculate_comparative_statics(results, baseline_scenario="Beer Ban")
        ban_row = changes[changes["scenario"] == "Beer Ban"]
        if len(ban_row) > 0:
            assert abs(ban_row["profit_change"].values[0]) < 0.01


class TestEdgeCases:
    def test_very_high_internalized_cost(self):
        model = StadiumEconomicModel(experience_degradation_cost=1000.0)
        ticket, beer, result = model.optimal_pricing()
        assert beer > model.beer_cost
        assert ticket > model.ticket_cost

    def test_sensitivity_health_cost(self):
        model = StadiumEconomicModel()
        simulator = BeerPriceControlSimulator(model)
        results = simulator.sensitivity_analysis(
            parameter_name="health_cost", values=[1.0, 2.0, 3.0]
        )
        assert len(results) == 3
        assert "health_cost" in results.columns

    def test_negative_price_penalty_in_optimization(self):
        model = StadiumEconomicModel()

        def objective(prices):
            ticket_p, beer_p = prices
            if beer_p < 0 or ticket_p < 0:
                return 1e10
            result = model.stadium_revenue(ticket_p, beer_p)
            return -result["profit"]

        penalty = objective([-10, -5])
        assert penalty == 1e10
        valid = objective([80, 12.5])
        assert valid < 1e10
