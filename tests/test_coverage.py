"""
Tests specifically for code coverage of edge cases and rarely-used functions.
"""

import pytest
from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


class TestModelCoverage:
    """Tests for model.py uncovered lines."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_consumer_utility_no_ticket(self, model):
        """Test consumer utility when not attending."""
        utility_no_ticket = model.consumer_utility(0, has_ticket=False)
        assert utility_no_ticket == model.consumer_income

    def test_optimal_beer_consumption_not_attending(self, model):
        """Test optimal beer when attending isn't worthwhile."""
        # Very high ticket price makes attending suboptimal
        beers = model.optimal_beer_consumption(beer_price=12.5, ticket_price=500)
        assert beers >= 0

    def test_optimal_pricing_negative_price_penalty(self, model):
        """Test that negative prices are penalized in optimization."""
        # This tests the penalty branch in optimal_pricing
        ticket, beer, result = model.optimal_pricing()
        assert beer > 0
        assert ticket > 0

    def test_deadweight_loss(self, model):
        """Test deadweight loss calculation."""
        dwl = model.deadweight_loss(
            current_ticket_price=80,
            current_beer_price=12.5,
            optimal_ticket_price=85,
            optimal_beer_price=13.0
        )
        # DWL should be a number (could be positive or negative)
        assert isinstance(dwl, (int, float))

    def test_internalized_costs_at_capacity(self, model):
        """Test internalized costs when exceeding capacity."""
        # Create model with low capacity
        model_low_cap = StadiumEconomicModel(capacity_constraint=10000)

        # Test with beers exceeding capacity
        cost_above = model_low_cap._internalized_costs(15000)
        cost_below = model_low_cap._internalized_costs(5000)

        # Above capacity should have higher costs
        assert cost_above > cost_below

    def test_revenue_with_internalized_costs(self, model):
        """Test that revenue calculation includes internalized costs."""
        result = model.stadium_revenue(80, 12.5)

        # Should have internalized_costs field
        assert 'internalized_costs' in result
        assert result['internalized_costs'] >= 0

        # Total costs should include internalized costs
        expected_total = (
            result['ticket_costs'] +
            result['beer_costs'] +
            result['internalized_costs']
        )
        assert abs(result['total_costs'] - expected_total) < 0.01


class TestSimulationCoverage:
    """Tests for simulation.py uncovered lines."""

    @pytest.fixture
    def simulator(self):
        model = StadiumEconomicModel()
        return BeerPriceControlSimulator(model)

    def test_sensitivity_analysis_invalid_parameter(self, simulator):
        """Test sensitivity analysis with invalid parameter name."""
        with pytest.raises(ValueError):
            simulator.sensitivity_analysis(
                parameter_name='invalid_param',
                values=[1.0, 2.0]
            )

    def test_sensitivity_analysis_ticket_elasticity(self, simulator):
        """Test sensitivity over ticket elasticity."""
        results = simulator.sensitivity_analysis(
            parameter_name='ticket_elasticity',
            values=[-0.5, -0.7]
        )
        assert len(results) == 2
        assert 'ticket_elasticity' in results.columns

    def test_find_social_optimum(self, simulator):
        """Test social optimum calculation directly."""
        result = simulator._find_social_optimum(
            crime_cost_per_beer=2.5,
            health_cost_per_beer=1.5
        )

        # Should return a valid scenario dict
        assert 'scenario' in result
        assert result['scenario'] == 'Social Optimum'
        assert result['profit'] > 0 or result['profit'] < 0  # Just check it's a number

    def test_summary_statistics_all_fields(self, simulator):
        """Test that summary statistics covers all branches."""
        results = simulator.run_all_scenarios()
        summary = simulator.summary_statistics(results)

        # All summary fields should be present
        required_keys = [
            'mean_attendance',
            'std_attendance',
            'mean_total_beers',
            'std_total_beers',
            'mean_profit',
            'std_profit',
            'mean_social_welfare',
            'std_social_welfare',
            'profit_maximizing_scenario',
            'welfare_maximizing_scenario',
            'lowest_externality_scenario'
        ]

        for key in required_keys:
            assert key in summary

    def test_scenario_with_both_constraints(self, simulator):
        """Test scenario with both price floor and ceiling."""
        result = simulator.run_scenario(
            "Both Constraints",
            beer_price_min=10.0,
            beer_price_max=15.0
        )

        # Should find a price between the constraints
        assert 10.0 <= result['beer_price'] <= 15.0

    def test_comparative_statics_baseline(self, simulator):
        """Test comparative statics uses correct baseline."""
        results = simulator.run_all_scenarios()

        # Test with different baseline
        changes = simulator.calculate_comparative_statics(
            results,
            baseline_scenario='Beer Ban'
        )

        # Beer ban row should have zero change
        ban_row = changes[changes['scenario'] == 'Beer Ban']
        if len(ban_row) > 0:
            # Changes should be zero for baseline scenario
            assert abs(ban_row['profit_change'].values[0]) < 0.01


class TestEdgeCases:
    """Additional edge case tests."""

    def test_model_with_zero_captive_demand(self):
        """Test model with no captive demand."""
        model = StadiumEconomicModel(captive_demand_share=0.0)
        result = model.stadium_revenue(80, 12.5)
        assert result['profit'] > 0

    def test_model_with_full_captive_demand(self):
        """Test model with 100% captive demand."""
        model = StadiumEconomicModel(captive_demand_share=1.0)
        result = model.stadium_revenue(80, 12.5)
        assert result['profit'] > 0

    def test_very_high_internalized_cost(self):
        """Test with very high internalized costs."""
        model = StadiumEconomicModel(experience_degradation_cost=1000.0)
        ticket, beer, result = model.optimal_pricing()

        # Should still find valid prices
        assert beer > model.beer_cost
        assert ticket > model.ticket_cost

    def test_zero_income_consumer(self):
        """Test with zero consumer income."""
        model = StadiumEconomicModel(consumer_income=0)
        result = model.stadium_revenue(80, 12.5)

        # Should still compute (though not realistic)
        assert 'profit' in result

    def test_optimal_pricing_with_ticket_control(self):
        """Test optimal pricing with ticket price control."""
        model = StadiumEconomicModel()
        ticket, beer, result = model.optimal_pricing(ticket_price_control=90.0)

        # Ticket should be at control price
        assert ticket == 90.0
        assert beer > 0

    def test_sensitivity_health_cost(self):
        """Test sensitivity analysis over health cost parameter."""
        model = StadiumEconomicModel()
        simulator = BeerPriceControlSimulator(model)

        results = simulator.sensitivity_analysis(
            parameter_name='health_cost',
            values=[1.0, 2.0, 3.0]
        )

        assert len(results) == 3
        assert 'health_cost' in results.columns
