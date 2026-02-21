"""
Comprehensive TDD calibration tests.
"""

from src.model import StadiumEconomicModel


def test_triple_calibration_success():
    """Model MUST satisfy all three empirical targets."""
    model = StadiumEconomicModel()

    _, opt_beer, _ = model.optimal_pricing()
    assert 11.5 <= opt_beer <= 14.5

    r = model.stadium_revenue(80, 12.50)
    drinker_beers = r["breakdown_by_type"]["Drinker"]["beers_per_fan"]
    assert 2.2 <= drinker_beers <= 2.8
    assert 0.85 <= r["beers_per_fan"] <= 1.15


def test_free_beer_reasonable():
    """Free beer should give reasonable consumption."""
    model = StadiumEconomicModel()
    r = model.stadium_revenue(80, 0.01)
    # Endogenous attendance: free beer attracts more drinkers
    assert 2.0 <= r["beers_per_fan"] <= 5.0
