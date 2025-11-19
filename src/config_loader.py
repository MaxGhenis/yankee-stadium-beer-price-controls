"""
Configuration loader for calibrated model parameters.

Single source of truth: config.yaml contains all calibrated values.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


# Default calibrated values (fallback if config.yaml not found)
DEFAULTS = {
    'experience_degradation_cost': 62.28,
    'alpha_beer_drinker': 43.75,
    'alpha_beer_nondrinker': 1.0,
    'beer_cost': 2.0,
    'ticket_cost': 3.5,
    'rowdiness_sensitivity': 0.005,
}


def load_config() -> Dict[str, Any]:
    """
    Load calibration config from config.yaml.

    Returns:
        Dict with calibrated parameters, or defaults if file not found
    """
    try:
        config_path = Path(__file__).parent.parent / 'config.yaml'
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                if config and 'calibration' in config:
                    return config['calibration']
    except Exception:
        pass

    return DEFAULTS


def get_parameter(param_name: str, default=None) -> Any:
    """
    Get a single calibrated parameter.

    Args:
        param_name: Parameter name (e.g., 'experience_degradation_cost')
        default: Default value if not in config

    Returns:
        Parameter value from config or default
    """
    config = load_config()

    if default is None and param_name in DEFAULTS:
        default = DEFAULTS[param_name]

    return config.get(param_name, default)

def load_full_config() -> Dict[str, Any]:
    """Load the entire config.yaml file."""
    config_path = Path(__file__).parent.parent / 'config.yaml'
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {} # Return empty dict if not found
