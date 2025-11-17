"""
Calibration script for stadium economic model.

Numerically finds parameter values that make observed prices ($80 tickets, $12.50 beer)
approximately profit-maximizing. Saves results to config.yaml for reproducibility.
"""

import yaml
from pathlib import Path
from scipy.optimize import minimize_scalar
import sys

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
    target_beer_price: float = 12.50,
    target_ticket_price: float = 80.0,
    tolerance: float = 0.50
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

    print(f"Multi-parameter calibration to match:")
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
                beer_cost=beer_cost
            )
            opt_ticket, opt_beer, _ = model.optimal_pricing()

            # Equal weighting on both prices
            beer_error = (opt_beer - target_beer_price) ** 2
            ticket_error = (opt_ticket - target_ticket_price) ** 2
            total_error = beer_error + ticket_error

            return total_error
        except Exception as e:
            return 1e10

    print("Optimizing 3 parameters: beer sensitivity, internalized cost, beer marginal cost...")
    result = minimize(
        objective,
        x0=[0.35, 800.0, 5.0],  # Initial guess
        bounds=[(0.20, 0.60), (200.0, 3000.0), (1.0, 10.0)],  # Reasonable ranges
        method='L-BFGS-B',
        options={'maxiter': 100}
    )

    best_sensitivity, best_internalized, best_beer_cost = result.x

    # Verify
    model = StadiumEconomicModel(
        beer_demand_sensitivity=best_sensitivity,
        experience_degradation_cost=best_internalized,
        beer_cost=best_beer_cost
    )
    opt_ticket, opt_beer, opt_result = model.optimal_pricing()

    print(f"\n✓ Calibration complete!")
    print(f"  Beer demand sensitivity: {best_sensitivity:.6f}")
    print(f"  Internalized cost parameter: ${best_internalized:.2f}")
    print(f"  Beer marginal cost: ${best_beer_cost:.2f}")
    print(f"\n  Predicted optimal beer: ${opt_beer:.2f} (target: ${target_beer_price:.2f}, error: ${abs(opt_beer - target_beer_price):.2f})")
    print(f"  Predicted optimal ticket: ${opt_ticket:.2f} (target: ${target_ticket_price:.2f}, error: ${abs(opt_ticket - target_ticket_price):.2f})")

    if abs(opt_beer - target_beer_price) <= tolerance and abs(opt_ticket - target_ticket_price) <= tolerance * 2:
        print(f"\n✓ Success! Both prices within tolerance")
    else:
        print(f"\n⚠️  Best achievable - structural model limitations remain")

    return {
        'beer_demand_sensitivity': float(best_sensitivity),
        'experience_degradation_cost': float(best_internalized),
        'beer_cost': float(best_beer_cost),
        'target_beer_price': float(target_beer_price),
        'target_ticket_price': float(target_ticket_price),
        'achieved_optimal_beer': float(opt_beer),
        'achieved_optimal_ticket': float(opt_ticket),
        'beer_error': float(abs(opt_beer - target_beer_price)),
        'ticket_error': float(abs(opt_ticket - target_ticket_price)),
        'notes': 'Multi-parameter calibration (sensitivity + internalized costs + beer marginal cost)'
    }


def calibrate_beer_sensitivity(
    target_beer_price: float = 12.50,
    target_ticket_price: float = 80.0,
    tolerance: float = 0.10
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
    print(f"Calibrating to match observed prices:")
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
    result = minimize_scalar(
        objective,
        bounds=(0.10, 0.50),
        method='bounded'
    )

    best_sensitivity = result.x

    # Verify calibration
    temp = TemporaryModel(best_sensitivity)
    optimal_beer = temp.optimal_beer_price()

    print(f"\n✓ Calibration complete!")
    print(f"  Beer demand sensitivity: {best_sensitivity:.6f}")
    print(f"  Predicted optimal beer: ${optimal_beer:.2f}")
    print(f"  Target beer: ${target_beer_price:.2f}")
    print(f"  Error: ${abs(optimal_beer - target_beer_price):.2f}")

    if abs(optimal_beer - target_beer_price) > tolerance:
        print(f"\n⚠️  WARNING: Calibration error exceeds tolerance!")
        print(f"  Model may not be able to match observed prices with current structure")

    return {
        'beer_demand_sensitivity': float(best_sensitivity),
        'target_beer_price': float(target_beer_price),
        'achieved_optimal_beer': float(optimal_beer),
        'calibration_error': float(abs(optimal_beer - target_beer_price)),
        'notes': 'Auto-calibrated to make observed prices approximately profit-maximizing'
    }


def save_calibration(params: dict, config_path: str = 'config.yaml'):
    """
    Save calibrated parameters to YAML config file.

    Args:
        params: Dict of calibrated parameters
        config_path: Path to config file (relative to project root)
    """
    config_file = Path(__file__).parent.parent / config_path

    # Load existing config if it exists
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}

    # Update calibration section
    config['calibration'] = params
    config['calibration']['timestamp'] = str(pd.Timestamp.now())

    # Save
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"\n✓ Saved calibration to: {config_file}")
    return config_file


if __name__ == "__main__":
    import pandas as pd

    print("="*70)
    print("BEER PRICE CONTROLS MODEL - MULTI-PARAMETER CALIBRATION")
    print("="*70)
    print()

    # Calibrate multiple parameters
    params = calibrate_multi_parameter(
        target_beer_price=12.50,
        target_ticket_price=80.0
    )

    # Save to config
    config_file = save_calibration(params)

    print()
    print("="*70)
    print(f"Calibration saved! Model will auto-load from config.yaml")
    print(f"  Beer sensitivity: {params['beer_demand_sensitivity']:.6f}")
    print(f"  Internalized cost: ${params['experience_degradation_cost']:.2f}")
    print("="*70)
