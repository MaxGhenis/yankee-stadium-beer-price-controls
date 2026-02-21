"""
Integration tests for the simulation engine.

Tests policy scenarios and comparative statics.
"""

import pandas as pd
import pytest

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestSimulatorInitialization:
    def test_initialization(self):
        model = StadiumEconomicModel()
        sim = BeerPriceControlSimulator(model)
        assert sim.model is model


class TestPolicyScenarios:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_baseline_scenario(self, simulator):
        result = simulator.run_scenario("Baseline")
        assert "profit" in result
        assert "social_welfare" in result
        assert result["profit"] > 0

    def test_price_ceiling_scenario(self, simulator):
        result = simulator.run_scenario("Price Ceiling", beer_price_max=8.0)
        assert result["beer_price"] <= 8.0

    def test_beer_ban_scenario(self, simulator):
        result = simulator.run_scenario("Ban", beer_banned=True)
        assert result["total_beers"] == 0
        assert result["beer_revenue"] == 0

    def test_beer_ban_reduces_attendance(self, simulator):
        ban = simulator.run_scenario("Ban", beer_banned=True)
        baseline = simulator.run_scenario("Baseline")
        assert ban["attendance"] < baseline["attendance"]


class TestFullSimulation:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_run_all_scenarios(self, simulator):
        results = simulator.run_all_scenarios(price_ceiling=8.0)
        assert isinstance(results, pd.DataFrame)
        assert len(results) == 4
        expected_scenarios = [
            "Baseline (Profit Max)",
            "Current Observed Prices",
            "Price Ceiling ($8.0)",
            "Beer Ban",
        ]
        for scenario in expected_scenarios:
            assert scenario in results["scenario"].values

    def test_all_scenarios_have_required_columns(self, simulator):
        results = simulator.run_all_scenarios()
        required_cols = [
            "scenario", "ticket_price", "beer_price", "attendance",
            "total_beers", "profit", "social_welfare", "externality_cost",
        ]
        for col in required_cols:
            assert col in results.columns

    def test_profit_maximization(self, simulator):
        results = simulator.run_all_scenarios()
        baseline_profit = results[results["scenario"] == "Baseline (Profit Max)"]["profit"].values[0]
        assert baseline_profit > 0
        ceiling_profit = results[results["scenario"].str.contains("Ceiling")]["profit"].values[0]
        assert baseline_profit >= ceiling_profit


class TestComparativeStatics:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_comparative_statics(self, simulator):
        results = simulator.run_all_scenarios()
        changes = simulator.calculate_comparative_statics(results)
        assert "profit_change" in changes.columns
        baseline_changes = changes[changes["scenario"] == "Current Observed Prices"]
        assert abs(baseline_changes["profit_change"].values[0]) < 0.01

    def test_summary_statistics(self, simulator):
        results = simulator.run_all_scenarios()
        summary = simulator.summary_statistics(results)
        assert "profit_maximizing_scenario" in summary
        assert "welfare_maximizing_scenario" in summary


class TestSensitivityAnalysis:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_sensitivity_analysis_crime_cost(self, simulator):
        results = simulator.sensitivity_analysis(
            parameter_name="crime_cost", values=[1.0, 2.0, 3.0, 4.0]
        )
        assert len(results) == 4
        assert "crime_cost" in results.columns
        assert results["social_welfare"].iloc[0] > results["social_welfare"].iloc[-1]

    def test_sensitivity_analysis_invalid_param(self, simulator):
        with pytest.raises(ValueError):
            simulator.sensitivity_analysis(parameter_name="invalid_param", values=[1.0])


class TestExternalityCalculations:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_externality_increases_with_consumption(self, simulator):
        low_price = simulator.run_scenario("Low", beer_price_max=8.0)
        high_price = simulator.run_scenario("High", beer_price_min=15.0)
        assert low_price["total_beers"] > high_price["total_beers"]
        assert low_price["externality_cost"] > high_price["externality_cost"]


class TestRealisticScenarios:
    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_observed_prices_near_optimum(self, simulator):
        results = simulator.run_all_scenarios()
        current = results[results["scenario"] == "Current Observed Prices"]
        baseline = results[results["scenario"] == "Baseline (Profit Max)"]
        assert current["profit"].values[0] >= 0.90 * baseline["profit"].values[0]

    def test_beer_ban_major_revenue_loss(self, simulator):
        results = simulator.run_all_scenarios()
        baseline = results[results["scenario"] == "Baseline (Profit Max)"]
        ban = results[results["scenario"] == "Beer Ban"]
        revenue_loss = baseline["total_revenue"].values[0] - ban["total_revenue"].values[0]
        assert revenue_loss > 0
        assert revenue_loss >= 0.10 * baseline["total_revenue"].values[0]
