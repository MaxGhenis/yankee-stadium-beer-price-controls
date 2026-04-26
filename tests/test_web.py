"""Tests for web-data export."""

from yankee_stadium_beer_controls.web import export_web_data


def test_export_web_data_writes_context_json(tmp_path):
    output = export_web_data(tmp_path, draws=10)

    assert output.exists()
    assert output.name == "context.json"
