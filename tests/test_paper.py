"""Tests for package-native paper artifact generation."""

from datetime import date
from pathlib import Path

import pytest

from yankee_stadium_beer_controls.paper import (
    _format_letter_date,
    build_paper_artifacts,
    build_submission_bundle,
    compute_report_context,
    render_quarto_project,
)


def test_report_context_has_core_sections():
    context = compute_report_context(draws=10)

    assert "baseline" in context
    assert "ceiling_6" in context
    assert "monte_carlo" in context
    assert context["ceiling_6"]["ticket_price"] > context["baseline"]["ticket_price"]
    assert context["ceiling_6"]["total_beers"] > context["baseline"]["total_beers"]


def test_build_paper_artifacts_writes_expected_files(tmp_path: Path):
    build_paper_artifacts(tmp_path, draws=10)

    assert (tmp_path / "abstract.md").exists()
    assert (tmp_path / "baseline_vs_6.md").exists()
    assert (tmp_path / "mechanism.md").exists()
    assert (tmp_path / "robustness.md").exists()
    assert (tmp_path / "credibility.md").exists()
    assert (tmp_path / "calibration_sources.md").exists()
    assert (tmp_path / "limitations.md").exists()
    assert (tmp_path / "calibration_table.md").exists()
    assert (tmp_path / "policy_cases_table.md").exists()
    assert (tmp_path / "context.json").exists()
    assert (tmp_path / "charts" / "prices.png").exists()


def test_generated_abstract_is_journal_length(tmp_path: Path):
    build_paper_artifacts(tmp_path, draws=10)

    abstract_words = (tmp_path / "abstract.md").read_text().split()

    assert len(abstract_words) <= 150


def test_build_submission_bundle_writes_expected_files(tmp_path: Path):
    build_submission_bundle(tmp_path, draws=10)

    assert (tmp_path / "ssrn_metadata.md").exists()
    assert (tmp_path / "cover_letter_journal_of_sports_economics.md").exists()
    assert (tmp_path / "cover_letter_international_journal_of_sport_finance.md").exists()
    assert (tmp_path / "README.md").exists()


def test_format_letter_date_is_windows_safe():
    assert _format_letter_date(date(2026, 4, 6)) == "April 6, 2026"


def test_render_quarto_project_scaffolds_packaged_project(monkeypatch, tmp_path: Path):
    recorded = {}

    monkeypatch.setattr(
        "yankee_stadium_beer_controls.paper.shutil.which", lambda _: "/usr/bin/quarto"
    )

    def fake_run(cmd, check):
        recorded["cmd"] = cmd
        recorded["check"] = check

    monkeypatch.setattr("yankee_stadium_beer_controls.paper.subprocess.run", fake_run)

    project_dir = tmp_path / "paper"
    render_quarto_project(project_dir=project_dir, draws=10)

    assert (project_dir / "_quarto.yml").exists()
    assert (project_dir / "index.qmd").exists()
    assert (project_dir / "references.bib").exists()
    assert recorded["cmd"] == ["/usr/bin/quarto", "render", str(project_dir)]
    assert recorded["check"] is True


def test_render_quarto_project_requires_quarto(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("yankee_stadium_beer_controls.paper.shutil.which", lambda _: None)

    with pytest.raises(RuntimeError, match="Install Quarto CLI"):
        render_quarto_project(project_dir=tmp_path, draws=10)
