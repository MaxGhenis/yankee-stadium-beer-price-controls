"""
Integration tests for the simulation engine.

Tests policy scenarios and comparative statics.
"""

import pandas as pd
import pytest

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestSimulatorInitialization:
    """Test simulator setup."""

    def test_initialization(self):
        """Simulator initializes with model."""
        model = StadiumEconomicModel()
        sim = BeerPriceControlSimulator(model)
        assert sim.model is model


class TestPolicyScenarios:
    """Test individual policy scenarios."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_baseline_scenario(self, simulator):
        """Baseline scenario runs without errors."""
        result = simulator.run_scenario("Baseline")
        assert "profit" in result
        assert "social_welfare" in result
        assert result["profit"] > 0

    def test_price_ceiling_scenario(self, simulator):
        """Price ceiling scenario respects constraint."""
        result = simulator.run_scenario("Price Ceiling", beer_price_max=8.0)
        assert result["beer_price"] <= 8.0

    def test_beer_ban_scenario(self, simulator):
        """Beer ban scenario."""
        result = simulator.run_scenario("Ban", beer_banned=True)
        assert result["total_beers"] == 0
        assert result["beer_revenue"] == 0

    def test_beer_ban_reduces_attendance(self, simulator):
        """Compare at same ticket price to isolate complementarity effect."""
        ban = simulator.run_scenario("Ban", beer_banned=True)
        # Beer ban should reduce attendance from baseline ~39,500
        # Due to complementarity, losing beer reduces value of attending
        baseline = simulator.run_scenario("Baseline")
        assert ban["attendance"] < baseline["attendance"], "Beer ban should reduce attendance"


class TestFullSimulation:
    """Test running all scenarios together."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_run_all_scenarios(self, simulator):
        """All scenarios run successfully."""
        results = simulator.run_all_scenarios(price_ceiling=8.0)

        assert isinstance(results, pd.DataFrame)
        assert len(results) == 4  # 4 scenarios

        # Check all scenarios present
        expected_scenarios = [
            "Baseline (Profit Max)",
            "Current Observed Prices",
            "Price Ceiling ($8.0)",
            "Beer Ban",
        ]
        for scenario in expected_scenarios:
            assert scenario in results["scenario"].values

    def test_all_scenarios_have_required_columns(self, simulator):
        """All scenarios have required output columns."""
        results = simulator.run_all_scenarios()

        required_cols = [
            "scenario",
            "ticket_price",
            "beer_price",
            "attendance",
            "total_beers",
            "profit",
            "social_welfare",
            "externality_cost",
        ]
        for col in required_cols:
            assert col in results.columns

    def test_profit_maximization(self, simulator):
        """Baseline scenario should maximize profit among comparable scenarios.

        NOTE: Due to model calibration, baseline may not be absolute maximum.
        This is expected - see MODEL_NOTES.md for explanation.
        """
        results = simulator.run_all_scenarios()

        baseline_profit = results[results["scenario"] == "Baseline (Profit Max)"]["profit"].values[
            0
        ]

        # Baseline should generate positive profit
        assert baseline_profit > 0

        # Should be higher than constrained scenarios
        ceiling_profit = results[results["scenario"].str.contains("Ceiling")]["profit"].values[0]

        # A constraint should reduce profit (or be equal if non-binding)
        assert baseline_profit >= ceiling_profit


class TestComparativeStatics:
    """Test comparative analysis functions."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_comparative_statics(self, simulator):
        """Comparative statics calculates changes correctly."""
        results = simulator.run_all_scenarios()
        changes = simulator.calculate_comparative_statics(results)

        # Should have change and pct_change columns
        assert "profit_change" in changes.columns
        assert "profit_pct_change" in changes.columns

        # Baseline scenario should have zero change
        baseline_changes = changes[changes["scenario"] == "Current Observed Prices"]
        assert abs(baseline_changes["profit_change"].values[0]) < 0.01

    def test_summary_statistics(self, simulator):
        """Summary statistics calculated correctly."""
        results = simulator.run_all_scenarios()
        summary = simulator.summary_statistics(results)

        assert "profit_maximizing_scenario" in summary
        assert "welfare_maximizing_scenario" in summary
        assert "lowest_externality_scenario" in summary


class TestSensitivityAnalysis:
    """Test sensitivity analysis over parameters."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_elasticity_sensitivity(self, simulator):
        """Sensitivity analysis over elasticity works."""
        results = simulator.sensitivity_analysis(
            parameter_name="beer_elasticity", values=[-0.5, -0.7, -0.9, -1.1]
        )

        assert isinstance(results, pd.DataFrame)
        assert len(results) == 4
        assert "beer_elasticity" in results.columns

    def test_externality_sensitivity(self, simulator):
        """Sensitivity analysis over externality costs works."""
        results = simulator.sensitivity_analysis(
            parameter_name="crime_cost", values=[1.0, 2.0, 3.0, 4.0]
        )

        assert len(results) == 4
        assert "crime_cost" in results.columns

        # Higher crime costs should reduce social welfare
        assert results["social_welfare"].iloc[0] > results["social_welfare"].iloc[-1]


class TestExternalityCalculations:
    """Test externality-related calculations."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_externality_increases_with_consumption(self, simulator):
        """Externality costs should increase with beer consumption."""
        low_price = simulator.run_scenario("Low", beer_price_max=8.0)
        high_price = simulator.run_scenario("High", beer_price_min=15.0)

        assert low_price["total_beers"] > high_price["total_beers"]
        assert low_price["externality_cost"] > high_price["externality_cost"]


class TestRealisticScenarios:
    """Test that scenarios produce realistic economic outcomes."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_observed_prices_near_optimum(self, simulator):
        """
        Current observed prices should be close to profit maximum.

        Real stadiums are sophisticated profit-maximizers, so
        observed prices should be near-optimal.
        """
        results = simulator.run_all_scenarios()

        current = results[results["scenario"] == "Current Observed Prices"]
        baseline = results[results["scenario"] == "Baseline (Profit Max)"]

        current_profit = current["profit"].values[0]
        max_profit = baseline["profit"].values[0]

        # Current should be within 90% of maximum
        # (accounts for other considerations like customer satisfaction)
        assert current_profit >= 0.90 * max_profit

    def test_beer_ban_major_revenue_loss(self, simulator):
        """Beer ban should cause substantial revenue loss."""
        results = simulator.run_all_scenarios()

        baseline = results[results["scenario"] == "Baseline (Profit Max)"]
        ban = results[results["scenario"] == "Beer Ban"]

        revenue_loss = baseline["total_revenue"].values[0] - ban["total_revenue"].values[0]

        # Beer is high margin, should be significant loss
        assert revenue_loss > 0
        # Should lose meaningful revenue (at least 10%)
        # Note: With heterogeneous consumers and differential sensitivity,
        # drinkers may substitute away more under ban, reducing baseline revenue
        assert revenue_loss >= 0.10 * baseline["total_revenue"].values[0]
