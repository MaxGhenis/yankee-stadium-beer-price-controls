"""
Configuration loader for calibrated model parameters.

Local `config.yaml` overlays the packaged or checked-in defaults.
"""

from importlib import resources
from pathlib import Path
from typing import Any

import yaml

PACKAGED_CONFIG_NAME = "default_config.yaml"

# Default calibrated values (fallback if config.yaml not found)
DEFAULTS = {
    "experience_degradation_cost": 126.726307,
    "alpha_beer_drinker": 43.75,
    "alpha_beer_nondrinker": 0.0,
    "ticket_price_sensitivity": 0.01317848,
    "beer_cost": 2.0,
    "ticket_cost": 3.5,
}


def _source_checkout_root() -> Path | None:
    module_path = Path(__file__).resolve()
    candidate_root = module_path.parents[2]
    if (candidate_root / "pyproject.toml").exists():
        return candidate_root
    return None


def _candidate_config_paths() -> list[Path]:
    cwd_config = Path.cwd() / "config.yaml"
    repo_root = _source_checkout_root()
    repo_root_config = repo_root / "config.yaml" if repo_root is not None else None

    # Prefer the caller's working directory over the repository checkout so
    # local experiments can override the packaged or checked-in calibration.
    paths = [cwd_config]
    if repo_root_config is not None and cwd_config != repo_root_config:
        paths.append(repo_root_config)
    return paths


def _load_yaml_path(config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as config_file:
        loaded = yaml.safe_load(config_file) or {}
    return loaded if isinstance(loaded, dict) else {}


def _load_packaged_config() -> dict[str, Any]:
    try:
        packaged_resource = resources.files("yankee_stadium_beer_controls").joinpath(
            PACKAGED_CONFIG_NAME
        )
        with packaged_resource.open("r", encoding="utf-8") as config_file:
            loaded = yaml.safe_load(config_file) or {}
    except (FileNotFoundError, ModuleNotFoundError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config() -> dict[str, Any]:
    """
    Load calibration config from local overrides or the packaged default.

    Returns:
        Dict with calibrated parameters, or defaults if file not found
    """
    calibration = load_full_config().get("calibration", {})
    return calibration if calibration else dict(DEFAULTS)


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


def load_full_config() -> dict[str, Any]:
    """Load the full merged config with local overrides layered on top."""
    full_config: dict[str, Any] = {"calibration": dict(DEFAULTS)}

    packaged_config = _load_packaged_config()
    if packaged_config:
        full_config = _merge_dicts(full_config, packaged_config)

    for config_path in reversed(_candidate_config_paths()):
        if not config_path.exists():
            continue
        full_config = _merge_dicts(full_config, _load_yaml_path(config_path))

    return full_config
