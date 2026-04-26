"""Tests for configuration loading behavior."""

from pathlib import Path

import pytest
import yaml

from yankee_stadium_beer_controls import config_loader


def test_load_full_config_falls_back_to_packaged_default(monkeypatch):
    packaged_config = {
        "calibration": {"ticket_price_sensitivity": 0.123},
        "taxes": {"sales_tax_rate": 8.875},
        "external_costs": {"crime": 2.5, "health": 1.5},
    }

    monkeypatch.setattr(config_loader, "_candidate_config_paths", lambda: [])
    monkeypatch.setattr(config_loader, "_load_packaged_config", lambda: packaged_config)

    loaded = config_loader.load_full_config()

    assert loaded["taxes"] == packaged_config["taxes"]
    assert loaded["external_costs"] == packaged_config["external_costs"]
    assert loaded["calibration"]["ticket_price_sensitivity"] == 0.123
    assert (
        loaded["calibration"]["experience_degradation_cost"]
        == config_loader.DEFAULTS["experience_degradation_cost"]
    )
    assert config_loader.load_config()["ticket_price_sensitivity"] == 0.123


def test_candidate_config_paths_prioritize_cwd(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)

    paths = config_loader._candidate_config_paths()

    assert paths[0] == tmp_path / "config.yaml"


def test_load_full_config_prefers_cwd_override(monkeypatch, tmp_path: Path):
    cwd_config = tmp_path / "cwd-config.yaml"
    repo_config = tmp_path / "repo-config.yaml"

    cwd_config.write_text("calibration:\n  ticket_price_sensitivity: 0.099\n", encoding="utf-8")
    repo_config.write_text("calibration:\n  ticket_price_sensitivity: 0.013\n", encoding="utf-8")

    monkeypatch.setattr(config_loader, "_candidate_config_paths", lambda: [cwd_config, repo_config])

    loaded = config_loader.load_full_config()

    assert loaded["calibration"]["ticket_price_sensitivity"] == 0.099


def test_load_full_config_merges_local_override_with_packaged_defaults(monkeypatch, tmp_path: Path):
    override_path = tmp_path / "config.yaml"
    override_path.write_text("calibration:\n  ticket_price_sensitivity: 0.099\n", encoding="utf-8")

    packaged_config = {
        "calibration": {
            "ticket_price_sensitivity": 0.013,
            "experience_degradation_cost": 126.7,
        },
        "taxes": {"sales_tax_rate": 8.875, "excise_federal": 0.01},
        "external_costs": {"crime": 2.5, "health": 1.5},
    }

    monkeypatch.setattr(config_loader, "_candidate_config_paths", lambda: [override_path])
    monkeypatch.setattr(config_loader, "_load_packaged_config", lambda: packaged_config)

    loaded = config_loader.load_full_config()

    assert loaded["calibration"]["ticket_price_sensitivity"] == 0.099
    assert loaded["calibration"]["experience_degradation_cost"] == 126.7
    assert loaded["taxes"] == packaged_config["taxes"]
    assert loaded["external_costs"] == packaged_config["external_costs"]
    assert config_loader.load_config()["experience_degradation_cost"] == 126.7


def test_load_full_config_raises_on_malformed_local_yaml(monkeypatch, tmp_path: Path):
    bad_config = tmp_path / "config.yaml"
    bad_config.write_text(
        "calibration:\n  ticket_price_sensitivity: [unterminated\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(config_loader, "_candidate_config_paths", lambda: [bad_config])

    with pytest.raises(yaml.YAMLError):
        config_loader.load_full_config()
