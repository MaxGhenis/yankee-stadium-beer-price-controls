"""
Calibration script for stadium economic model.

Finds experience_degradation_cost (k) that makes observed prices ($80 tickets,
$12.50 beer) approximately profit-maximizing. alpha and lambda are set analytically.

Saves results to a local config.yaml override for reproducibility.
"""

from datetime import datetime
from pathlib import Path

import yaml
from scipy.optimize import minimize as scipy_minimize

from yankee_stadium_beer_controls.model import ConsumerType, StadiumEconomicModel


def calibrate_heterogeneous_model(
    target_optimal_beer: float = 12.50,
    target_optimal_ticket: float = 80.0,
    alpha_beer_drinker: float | None = None,
    target_consumption_at_baseline: float = 2.5,
):
    """
    Calibrate heterogeneous model to match all empirical targets.

    Two-parameter calibration: find (k, lambda) that minimize
    (P_B* - 12.50)^2 + (P_T* - 80)^2.

    alpha is set analytically:
    - alpha_drinker = P_B * (B + 1), unless explicitly overridden

    lambda (ticket_price_sensitivity) is calibrated jointly with k because
    the multiproduct monopolist's optimal ticket price depends on both
    demand elasticity and internalized costs.
    """

    if alpha_beer_drinker is None:
        alpha_beer_drinker = target_optimal_beer * (target_consumption_at_baseline + 1)

    print("Calibrating heterogeneous model (2 parameters: k, lambda):")
    print(f"  Target optimal beer: ${target_optimal_beer:.2f}")
    print(f"  Target optimal ticket: ${target_optimal_ticket:.2f}")
    print(f"  Drinker alpha_beer: {alpha_beer_drinker:.2f}")
    print(
        f"  Target drinker consumption at ${target_optimal_beer:.2f}: "
        f"{target_consumption_at_baseline:.1f} beers"
    )
    print()

    consumer_types = [
        ConsumerType("Non-Drinker", 0.6, 0.0),
        ConsumerType("Drinker", 0.4, alpha_beer_drinker),
    ]

    def make_model(intern_cost, lam):
        return StadiumEconomicModel(
            consumer_types=list(consumer_types),
            experience_degradation_cost=intern_cost,
            ticket_price_sensitivity=lam,
        )

    def objective(params):
        intern_cost, lam = params
        if intern_cost <= 0 or lam <= 0:
            return 1e10
        try:
            model = make_model(intern_cost, lam)
            opt_ticket, opt_beer, _ = model.optimal_pricing()
            return (opt_beer - target_optimal_beer) ** 2 + (opt_ticket - target_optimal_ticket) ** 2
        except Exception:
            return 1e10

    print("Optimizing (k, lambda)...")
    result = scipy_minimize(
        objective,
        x0=[126.0, 0.0132],
        bounds=[(1, 5000), (0.001, 0.1)],
        method="Nelder-Mead",
    )
    best_intern, best_lambda = result.x

    # Verify calibration
    model = make_model(best_intern, best_lambda)
    opt_ticket, opt_beer, _ = model.optimal_pricing()
    r = model.stadium_revenue(80, 12.50)

    # Compute implied elasticity at baseline
    implied_elasticity = -best_lambda * target_optimal_ticket

    print(f"\n  experience_degradation_cost (k): {best_intern:.6f}")
    print(f"  ticket_price_sensitivity (λ): {best_lambda:.8f}")
    print(f"  implied ticket elasticity at $80: {implied_elasticity:.4f}")
    print(f"\n  Achieved optimal beer: ${opt_beer:.2f} (target: ${target_optimal_beer:.2f})")
    print(f"  Achieved optimal ticket: ${opt_ticket:.2f} (target: ${target_optimal_ticket:.2f})")
    print(
        f"  Drinkers consume: {r['breakdown_by_type']['Drinker']['beers_per_fan']:.2f} beers at $12.50"
    )
    print(f"  Aggregate: {r['beers_per_fan']:.2f} beers/fan")

    return {
        "experience_degradation_cost": float(best_intern),
        "alpha_beer_drinker": float(alpha_beer_drinker),
        "alpha_beer_nondrinker": 0.0,
        "ticket_price_sensitivity": float(best_lambda),
        "target_optimal_beer": float(target_optimal_beer),
        "achieved_optimal_beer": float(opt_beer),
        "optimal_error": float(abs(opt_beer - target_optimal_beer)),
        "drinker_consumption_at_baseline": float(
            r["breakdown_by_type"]["Drinker"]["beers_per_fan"]
        ),
        "aggregate_consumption_at_baseline": float(r["beers_per_fan"]),
        "notes": "Utility-consistent model (endogenous cross-price effects)",
        "method": "Joint calibration of k and λ to match optimal prices",
    }


def save_calibration(params: dict, config_path: str = "config.yaml"):
    """Save calibrated parameters to a local YAML override file."""
    from yankee_stadium_beer_controls.config_loader import DEFAULTS, load_full_config

    config_file = Path(config_path)
    if not config_file.is_absolute():
        config_file = Path.cwd() / config_file
    config_file.parent.mkdir(parents=True, exist_ok=True)

    full_config = load_full_config()

    # Update calibration section
    calibration_section = full_config.get("calibration", {})
    for k, v in DEFAULTS.items():
        if k not in calibration_section:
            calibration_section[k] = v

    calibration_section.update(params)
    calibration_section["timestamp"] = str(datetime.now())

    full_config["calibration"] = calibration_section

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(full_config, f, default_flow_style=False, sort_keys=False)

    print(f"\nSaved calibration to: {config_file}")
    return config_file


def main() -> int:
    print("=" * 70)
    print("UTILITY-CONSISTENT MODEL CALIBRATION")
    print("=" * 70)
    print()

    params = calibrate_heterogeneous_model(target_optimal_beer=12.50)
    save_calibration(params)

    print()
    print("=" * 70)
    print("Calibration complete and saved to config.yaml")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
