"""Tests for calibration file output behavior."""

from pathlib import Path

import pytest
import yaml

from yankee_stadium_beer_controls.calibrate import calibrate_heterogeneous_model, save_calibration


def test_save_calibration_writes_to_cwd_by_default(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)

    config_path = save_calibration({"ticket_price_sensitivity": 0.5})

    assert config_path == tmp_path / "config.yaml"
    assert config_path.exists()

    loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert loaded["calibration"]["ticket_price_sensitivity"] == 0.5
    assert "taxes" in loaded
    assert "external_costs" in loaded


def test_save_calibration_honors_explicit_absolute_path(tmp_path: Path):
    config_path = tmp_path / "nested" / "override.yaml"

    saved_path = save_calibration({"ticket_price_sensitivity": 0.5}, config_path=str(config_path))

    assert saved_path == config_path
    assert config_path.exists()


def test_calibration_uses_nondefault_consumption_target():
    params = calibrate_heterogeneous_model(
        target_optimal_beer=12.50,
        target_consumption_at_baseline=3.0,
    )

    assert params["alpha_beer_drinker"] == pytest.approx(50.0)
    assert params["drinker_consumption_at_baseline"] == pytest.approx(3.0)
