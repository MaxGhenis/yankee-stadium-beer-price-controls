"""
Calibration script for stadium economic model.

Numerically finds parameter values that make observed prices ($80 tickets, $12.50 beer)
approximately profit-maximizing. Saves results to config.yaml for reproducibility.
"""

import sys
from pathlib import Path

import yaml
from scipy.optimize import minimize_scalar


# Temporarily set sensitivity to test different values
class TemporaryModel:
    """Temporary model class for calibration (avoids circular dependency)."""

    def __init__(self, sensitivity):
        # Import here to avoid issues during calibration
        sys.path.insert(0, str(Path(__file__).parent))
        from model import StadiumEconomicModel

        # Create model with manually specified sensitivity
        self.model = StadiumEconomicModel(beer_demand_sensitivity=sensitivity)

    def optimal_beer_price(self):
        _, beer_price, _ = self.model.optimal_pricing()
        return beer_price


def calibrate_multi_parameter(
    target_beer_price: float = 12.50, target_ticket_price: float = 80.0, tolerance: float = 0.50
) -> dict:
    """
    Calibrate BOTH beer sensitivity AND internalized cost to match observed prices.

    This is more flexible than calibrating sensitivity alone.

    Args:
        target_beer_price: Observed beer price to match
        target_ticket_price: Observed ticket price to match
        tolerance: Acceptable deviation from target (dollars)

    Returns:
        Dict with calibrated parameters and diagnostics
    """
    from scipy.optimize import minimize

    sys.path.insert(0, str(Path(__file__).parent))
    from model import StadiumEconomicModel

    print("Multi-parameter calibration to match:")
    print(f"  Target beer price: ${target_beer_price:.2f}")
    print(f"  Target ticket price: ${target_ticket_price:.2f}")
    print(f"  Tolerance: ±${tolerance:.2f}")
    print()

    def objective(params):
        """Minimize combined error in beer and ticket prices."""
        sensitivity, internalized_cost, beer_cost = params

        if sensitivity <= 0 or internalized_cost <= 0 or beer_cost <= 0:
            return 1e10

        try:
            model = StadiumEconomicModel(
                beer_demand_sensitivity=sensitivity,
                experience_degradation_cost=internalized_cost,
                beer_cost=beer_cost,
            )
            opt_ticket, opt_beer, _ = model.optimal_pricing()

            # Equal weighting on both prices
            beer_error = (opt_beer - target_beer_price) ** 2
            ticket_error = (opt_ticket - target_ticket_price) ** 2
            total_error = beer_error + ticket_error

            return total_error
        except Exception:
            return 1e10

    print("Optimizing 3 parameters: beer sensitivity, internalized cost, beer marginal cost...")
    result = minimize(
        objective,
        x0=[0.35, 800.0, 5.0],  # Initial guess
        bounds=[(0.20, 0.60), (200.0, 3000.0), (1.0, 10.0)],  # Reasonable ranges
        method="L-BFGS-B",
        options={"maxiter": 100},
    )

    best_sensitivity, best_internalized, best_beer_cost = result.x

    # Verify
    model = StadiumEconomicModel(
        beer_demand_sensitivity=best_sensitivity,
        experience_degradation_cost=best_internalized,
        beer_cost=best_beer_cost,
    )
    opt_ticket, opt_beer, opt_result = model.optimal_pricing()

    print("\n✓ Calibration complete!")
    print(f"  Beer demand sensitivity: {best_sensitivity:.6f}")
    print(f"  Internalized cost parameter: ${best_internalized:.2f}")
    print(f"  Beer marginal cost: ${best_beer_cost:.2f}")
    print(
        f"\n  Predicted optimal beer: ${opt_beer:.2f} (target: ${target_beer_price:.2f}, error: ${abs(opt_beer - target_beer_price):.2f})"
    )
    print(
        f"  Predicted optimal ticket: ${opt_ticket:.2f} (target: ${target_ticket_price:.2f}, error: ${abs(opt_ticket - target_ticket_price):.2f})"
    )

    if (
        abs(opt_beer - target_beer_price) <= tolerance
        and abs(opt_ticket - target_ticket_price) <= tolerance * 2
    ):
        print("\n✓ Success! Both prices within tolerance")
    else:
        print("\n⚠️  Best achievable - structural model limitations remain")

    return {
        "beer_demand_sensitivity": float(best_sensitivity),
        "experience_degradation_cost": float(best_internalized),
        "beer_cost": float(best_beer_cost),
        "target_beer_price": float(target_beer_price),
        "target_ticket_price": float(target_ticket_price),
        "achieved_optimal_beer": float(opt_beer),
        "achieved_optimal_ticket": float(opt_ticket),
        "beer_error": float(abs(opt_beer - target_beer_price)),
        "ticket_error": float(abs(opt_ticket - target_ticket_price)),
        "notes": "Multi-parameter calibration (sensitivity + internalized costs + beer marginal cost)",
    }


def calibrate_beer_sensitivity(
    target_beer_price: float = 12.50, target_ticket_price: float = 80.0, tolerance: float = 0.10
) -> dict:
    """
    Find beer demand sensitivity that makes target prices approximately optimal.

    Args:
        target_beer_price: Observed beer price to match
        target_ticket_price: Observed ticket price to match
        tolerance: Acceptable deviation from target (dollars)

    Returns:
        Dict with calibrated parameters and diagnostics
    """
    print("Calibrating to match observed prices:")
    print(f"  Target beer price: ${target_beer_price:.2f}")
    print(f"  Target ticket price: ${target_ticket_price:.2f}")
    print(f"  Tolerance: ±${tolerance:.2f}")
    print()

    def objective(sensitivity):
        """Objective: minimize distance between optimal and target beer price."""
        try:
            temp = TemporaryModel(sensitivity)
            optimal_beer = temp.optimal_beer_price()
            error = (optimal_beer - target_beer_price) ** 2
            return error
        except Exception as e:
            print(f"  Error at sensitivity={sensitivity:.4f}: {e}")
            return 1e10

    # Search for optimal sensitivity
    print("Searching for optimal beer demand sensitivity...")
    result = minimize_scalar(objective, bounds=(0.10, 0.50), method="bounded")

    best_sensitivity = result.x

    # Verify calibration
    temp = TemporaryModel(best_sensitivity)
    optimal_beer = temp.optimal_beer_price()

    print("\n✓ Calibration complete!")
    print(f"  Beer demand sensitivity: {best_sensitivity:.6f}")
    print(f"  Predicted optimal beer: ${optimal_beer:.2f}")
    print(f"  Target beer: ${target_beer_price:.2f}")
    print(f"  Error: ${abs(optimal_beer - target_beer_price):.2f}")

    if abs(optimal_beer - target_beer_price) > tolerance:
        print("\n⚠️  WARNING: Calibration error exceeds tolerance!")
        print("  Model may not be able to match observed prices with current structure")

    return {
        "beer_demand_sensitivity": float(best_sensitivity),
        "target_beer_price": float(target_beer_price),
        "achieved_optimal_beer": float(optimal_beer),
        "calibration_error": float(abs(optimal_beer - target_beer_price)),
        "notes": "Auto-calibrated to make observed prices approximately profit-maximizing",
    }


def save_calibration(params: dict, config_path: str = "config.yaml"):
    """
    Save calibrated parameters to YAML config file.

    Args:
        params: Dict of calibrated parameters
        config_path: Path to config file (relative to project root)
    """
    config_file = Path(__file__).parent.parent / config_path

    # Use config_loader to load existing config including default structure
    # This prevents overwriting 'taxes' and 'external_costs'
    from src.config_loader import DEFAULTS, load_full_config

    full_config = load_full_config()

    # Update calibration section within the full config
    # Ensure all calibration params from DEFAULTS are included if not calibrated
    calibration_section = full_config.get("calibration", {})
    for k, v in DEFAULTS.items():
        if k not in calibration_section:
            calibration_section[k] = v

    # Add newly calibrated parameters
    calibration_section.update(params)
    calibration_section["timestamp"] = str(pd.Timestamp.now())
    calibration_section["notes"] = (
        "Heterogeneous model calibration (α_beer + experience_degradation_cost + rowdiness_sensitivity)"
    )

    full_config["calibration"] = calibration_section

    # Save
    with open(config_file, "w") as f:
        yaml.dump(full_config, f, default_flow_style=False, sort_keys=False)

    print(f"\n✓ Saved calibration to: {config_file}")
    return config_file


def calibrate_heterogeneous_model(
    target_optimal_beer: float = 12.50,
    alpha_beer_drinker: float = 43.75,
    target_consumption_at_baseline: float = 2.5,
):
    """
    Calibrate heterogeneous model to match all empirical targets.

    Finds experience_degradation_cost that makes α_beer=43.75 give:
    - Optimal beer price ≈ $12.50
    - Drinkers consume 2.5 beers at $12.50
    - Aggregate 1.0 beers/fan

    Returns calibrated parameters for config.yaml
    """
    from scipy.optimize import minimize_scalar

    sys.path.insert(0, str(Path(__file__).parent))
    from model import ConsumerType, StadiumEconomicModel

    print("Calibrating heterogeneous model:")
    print(f"  Target optimal beer: ${target_optimal_beer:.2f}")
    print(f"  Drinker α_beer: {alpha_beer_drinker:.2f}")
    print(f"  Target drinker consumption at $12.50: {target_consumption_at_baseline:.1f} beers")
    print()

    def objective(intern_cost):
        if intern_cost <= 0:
            return 1e10
        try:
            types = [
                ConsumerType("Non-Drinker", 0.6, 1.0, 3.0, 200.0),
                ConsumerType("Drinker", 0.4, alpha_beer_drinker, 2.5, 200.0)
            ]
            model = StadiumEconomicModel(
                consumer_types=types,
                experience_degradation_cost=intern_cost
            )
            _, opt_beer, _ = model.optimal_pricing()
            return (opt_beer - target_optimal_beer) ** 2
        except Exception:
            return 1e10

    print("Optimizing internalized cost parameter...")
    result = minimize_scalar(objective, bounds=(10, 1000), method="bounded")
    best_intern = result.x

    # Verify
    types = [
        ConsumerType("Non-Drinker", 0.6, 1.0, 3.0, 200.0),
        ConsumerType("Drinker", 0.4, alpha_beer_drinker, 2.5, 200.0),
    ]
    model = StadiumEconomicModel(consumer_types=types, experience_degradation_cost=best_intern)
    _, opt_beer, _ = model.optimal_pricing()
    r = model.stadium_revenue(80, 12.50)

    print("\n✓ Calibration complete!")
    print(f"  experience_degradation_cost: {best_intern:.2f}")
    print(f"  alpha_beer_drinker: {alpha_beer_drinker:.2f}")
    print(f"\n  Achieved optimal beer: ${opt_beer:.2f} (target: ${target_optimal_beer:.2f})")
    print(
        f"  Drinkers consume: {r['breakdown_by_type']['Drinker']['beers_per_fan']:.2f} beers at $12.50"
    )
    print(f"  Aggregate: {r['beers_per_fan']:.2f} beers/fan")

    return {
        "experience_degradation_cost": float(best_intern),
        "alpha_beer_drinker": float(alpha_beer_drinker),
        "alpha_beer_nondrinker": 1.0,
        "target_optimal_beer": float(target_optimal_beer),
        "achieved_optimal_beer": float(opt_beer),
        "optimal_error": float(abs(opt_beer - target_optimal_beer)),
        "drinker_consumption_at_baseline": float(
            r["breakdown_by_type"]["Drinker"]["beers_per_fan"]
        ),
        "aggregate_consumption_at_baseline": float(r["beers_per_fan"]),
        "notes": "Heterogeneous model calibration (α_beer + experience_degradation_cost)",
        "method": "Numerical optimization to match optimal price and consumption data",
    }


if __name__ == "__main__":
    import pandas as pd

    print("=" * 70)
    print("HETEROGENEOUS MODEL CALIBRATION")
    print("=" * 70)
    print()

    # Calibrate heterogeneous model
    params = calibrate_heterogeneous_model(target_optimal_beer=12.50, alpha_beer_drinker=43.75)

    # Save to config
    config_file = save_calibration(params)

    print()
    print("=" * 70)
    print("✓ Calibration complete and saved to config.yaml")
    print("  Run any script - it will auto-load calibrated parameters!")
    print("=" * 70)
