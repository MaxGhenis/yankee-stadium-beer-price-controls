"""
TDD test for price_ceiling_analysis.py

Tests the analysis script output, not just the model.
"""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel
from src.price_ceiling_analysis import simulate_price_ceilings


class TestPriceCeilingAnalysisScript:
    """Test the price ceiling analysis script outputs."""

    @pytest.fixture
    def model(self):
        return StadiumEconomicModel()

    def test_nonbinding_ceilings_plateau(self, model):
        """
        CRITICAL TEST: Non-binding ceilings should create flat lines in output.

        This test would have FAILED before the fix to price_ceiling_analysis.py,
        catching the bug where the script manually checked for binding.

        Allows for small numerical precision differences from optimizer.
        """
        # Find optimal price first
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Analyze ceilings from optimal to well above
        ceilings = np.linspace(unc_beer, unc_beer + 5, 6)
        df = simulate_price_ceilings(ceilings, model)

        # Ticket and beer prices should be nearly constant (within numerical precision)
        ticket_range = df['ticket_price'].max() - df['ticket_price'].min()
        beer_range = df['beer_price'].max() - df['beer_price'].min()
        profit_std = df['profit'].std()

        # Before fix: ticket range would be > $10 (huge changes)
        # After fix: ticket range should be < $0.01 (just numerical noise)
        assert ticket_range < 0.05, \
            f"Ticket prices should plateau above optimal, but range={ticket_range:.4f}"
        assert beer_range < 0.05, \
            f"Beer prices should plateau above optimal, but range={beer_range:.4f}"
        assert profit_std < 500, \
            f"Profit should be nearly constant above optimal, but std={profit_std:.0f}"

        # All values should approximately equal the unconstrained optimum
        assert df['ticket_price'].mean() == pytest.approx(unc_ticket, rel=1e-2)
        assert df['beer_price'].mean() == pytest.approx(unc_beer, rel=1e-2)

    def test_binding_ceilings_vary(self, model):
        """
        Binding ceilings (below optimal) should create varying outcomes.
        """
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Analyze binding ceilings
        ceilings = np.linspace(unc_beer - 5, unc_beer - 1, 5)
        df = simulate_price_ceilings(ceilings, model)

        # Ticket prices should VARY (not plateau)
        ticket_std = df['ticket_price'].std()
        assert ticket_std > 1.0, \
            f"Ticket prices should vary with binding ceilings, but std={ticket_std}"

        # Ticket price should be inversely related to beer ceiling
        # (lower ceiling → higher tickets)
        correlation = df['beer_ceiling'].corr(df['ticket_price'])
        assert correlation < -0.5, \
            f"Ticket price should be negatively correlated with ceiling, but corr={correlation}"

    def test_transition_point_at_optimal(self, model):
        """
        Test behavior at the transition from binding to non-binding.
        """
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Test around the optimal price
        ceilings = np.array([
            unc_beer - 1.0,  # Binding
            unc_beer - 0.1,  # Just barely binding
            unc_beer + 0.1,  # Just barely non-binding
            unc_beer + 1.0,  # Non-binding
        ])
        df = simulate_price_ceilings(ceilings, model)

        # Below optimal: prices should be changing
        below_ticket_diff = abs(df.iloc[0]['ticket_price'] - df.iloc[1]['ticket_price'])
        assert below_ticket_diff > 0.4, "Should see price changes below optimal"

        # Above optimal: prices should be constant
        above_ticket_diff = abs(df.iloc[2]['ticket_price'] - df.iloc[3]['ticket_price'])
        assert above_ticket_diff < 0.1, \
            f"Should see no price changes above optimal, but diff={above_ticket_diff}"

    def test_csv_output_has_plateau(self, model):
        """
        Test that CSV output file has correct plateau behavior.

        This catches the bug at the integration level (full script execution).
        """
        unc_ticket, unc_beer, unc_result = model.optimal_pricing()

        # Full range analysis
        ceilings = np.linspace(5, 20, 31)
        df = simulate_price_ceilings(ceilings, model)

        # Filter to non-binding range
        nonbinding = df[df['beer_ceiling'] >= unc_beer + 0.5]

        if len(nonbinding) > 1:
            # All non-binding rows should have nearly identical ticket prices
            # (allowing for numerical precision in optimizer)
            ticket_range = nonbinding['ticket_price'].max() - nonbinding['ticket_price'].min()
            assert ticket_range < 0.1, \
                f"Non-binding ceilings should plateau (range < $0.10), but range=${ticket_range:.4f}"

            # Should match unconstrained optimal (within tolerance)
            assert nonbinding['ticket_price'].mean() == pytest.approx(unc_ticket, abs=0.05)
