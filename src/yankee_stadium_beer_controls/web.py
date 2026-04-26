"""Generate static JSON payloads for the Next/Tailwind dashboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from yankee_stadium_beer_controls.paper import compute_report_context


def export_web_data(output_dir: str | Path = "web/public/data", draws: int = 1000) -> Path:
    """Write dashboard-ready JSON files derived from the packaged model."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    context = compute_report_context(draws=draws)
    target = output_path / "context.json"
    target.write_text(json.dumps(context, indent=2) + "\n")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write dashboard data for the Next app.")
    parser.add_argument("--output-dir", default="web/public/data")
    parser.add_argument("--draws", type=int, default=1000)
    args = parser.parse_args(argv)

    export_web_data(args.output_dir, draws=args.draws)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
