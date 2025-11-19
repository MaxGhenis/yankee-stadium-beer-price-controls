"""
Test that non-binding price ceilings have no effect on equilibrium.

This is critical for comparative statics analysis: when ceiling > optimal price,
the ceiling should not affect outcomes.
"""

import numpy as np
import pytest

from src.model import StadiumEconomicModel


class TestNonBindingCeilings:
    """Test that price ceilings above optimal have no effect."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_unconstrained_optimal_price(self, model):
        """Find the unconstrained optimal beer price for reference."""
        ticket_price, beer_price, result = model.optimal_pricing()

        # Optimal should be positive and reasonable
        assert beer_price > 0
        assert beer_price < 30
        assert ticket_price > 0

        # Store for other tests
        return beer_price

    def test_ceiling_above_optimal_has_no_effect(self, model):
        """Price ceiling above optimal should not change equilibrium."""
        # Get unconstrained optimum
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Try ceiling well above optimal (e.g., if optimal is ~$12, try $20)
        high_ceiling = unc_beer + 5.0

        # Should get same result
        ceil_ticket, ceil_beer, ceil_result = model.optimal_pricing(beer_price_control=high_ceiling)

        # Prices should be identical (or ceiling, whichever is lower)
        assert ceil_beer <= high_ceiling, "Beer price should not exceed ceiling"

        # If ceiling is non-binding, should match unconstrained
        if high_ceiling > unc_beer:
            # This test will FAIL with current implementation!
            # Current code forces beer price to equal ceiling even when non-binding
            assert ceil_beer == pytest.approx(
                unc_beer, rel=1e-3
            ), f"Non-binding ceiling should not affect beer price: {ceil_beer} != {unc_beer}"

            assert ceil_ticket == pytest.approx(
                unc_ticket, rel=1e-3
            ), f"Non-binding ceiling should not affect ticket price: {ceil_ticket} != {unc_ticket}"

            assert ceil_result["profit"] == pytest.approx(
                unc_result["profit"], rel=1e-3
            ), f"Non-binding ceiling should not affect profit: {ceil_result['profit']} != {unc_result['profit']}"

    def test_binding_vs_nonbinding_ceiling(self, model):
        """Compare binding vs non-binding ceilings."""
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Binding ceiling (well below optimal)
        binding_ceiling = unc_beer - 3.0
        bind_ticket, bind_beer, bind_result = model.optimal_pricing(
            beer_price_control=binding_ceiling
        )

        # Non-binding ceiling (well above optimal)
        nonbinding_ceiling = unc_beer + 3.0
        nonbind_ticket, nonbind_beer, nonbind_result = model.optimal_pricing(
            beer_price_control=nonbinding_ceiling
        )

        # Binding ceiling should force beer price down
        assert bind_beer == binding_ceiling, "Binding ceiling should set beer price"
        assert bind_ticket > unc_ticket, "Binding ceiling should raise ticket prices"

        # Non-binding ceiling should have no effect
        # THIS WILL FAIL with current implementation
        assert nonbind_beer == pytest.approx(
            unc_beer, rel=1e-3
        ), "Non-binding ceiling should not affect beer price"
        assert nonbind_ticket == pytest.approx(
            unc_ticket, rel=1e-3
        ), "Non-binding ceiling should not affect ticket price"

    def test_ceiling_at_exactly_optimal(self, model):
        """Ceiling exactly at optimal should have minimal/no effect."""
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Set ceiling at exactly the optimal price
        exact_ticket, exact_beer, exact_result = model.optimal_pricing(beer_price_control=unc_beer)

        # Should get essentially the same result
        assert exact_beer == pytest.approx(unc_beer, rel=1e-6)
        assert exact_ticket == pytest.approx(unc_ticket, rel=1e-3)
        assert exact_result["profit"] == pytest.approx(unc_result["profit"], rel=1e-3)

    def test_comparative_statics_plateaus(self, model):
        """
        Test that comparative statics flatten above optimal price.

        For price ceiling analysis, outcomes should plateau when ceiling
        becomes non-binding.
        """
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Test range of ceilings above optimal
        high_ceilings = np.linspace(unc_beer + 1, unc_beer + 10, 5)

        profits = []
        tickets = []
        beers = []

        for ceiling in high_ceilings:
            t, b, r = model.optimal_pricing(beer_price_control=ceiling)

            # With current bug: these will all be different
            # After fix: these should all be the same (plateau)
            profits.append(r["profit"])
            tickets.append(t)
            beers.append(b)

        # All should be approximately equal (flat line)
        # THIS WILL FAIL with current implementation
        profit_std = np.std(profits)
        ticket_std = np.std(tickets)

        assert profit_std < 0.01 * np.mean(
            profits
        ), f"Profits should be constant with non-binding ceilings, but std={profit_std}"
        assert (
            ticket_std < 0.01
        ), f"Ticket prices should be constant with non-binding ceilings, but std={ticket_std}"
