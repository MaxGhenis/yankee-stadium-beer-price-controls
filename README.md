# Beer Price Ceilings at Yankee Stadium

This repository contains a small Python package and Quarto paper for a calibrated
mechanism exercise: how a profit-maximizing stadium might re-optimize tickets and
beer sales under a beer price ceiling.

The project is intentionally paper-first:

- model code lives in `src/yankee_stadium_beer_controls`
- `pyproject.toml` and `uv.lock` are the Python dependency source of truth
- Quarto reads generated fragments from package code
- git ignores generated paper, submission, coverage, and dashboard outputs
- there are no notebooks, legacy Python dashboard, or ad hoc analysis scripts in the active workflow
- the optional web UI is a Next/Tailwind view over generated package JSON
- Vercel builds the public paper site directly from the package and Quarto sources

## Quick Start

Install the Python environment:

```bash
uv sync --locked --extra dev
```

Run tests and checks:

```bash
uv run pytest
uv run ruff check src tests
uv run black --check src tests
```

Render the paper:

```bash
uv run yankee-beer-paper render --project-dir paper
```

Generate SSRN/journal submission materials:

```bash
uv run yankee-beer-paper submission --output-dir submissions
```

Build the Python package:

```bash
uv run python -m build
```

Install Quarto separately for `yankee-beer-paper render`; the package can
generate markdown fragments and submission files without the Quarto CLI.

## Deployment

Vercel builds the public paper site. The build installs `uv`, regenerates the
paper fragments from package code, renders the Quarto HTML site, and serves
`paper/_build` as a static site.

```bash
vercel deploy
```

## Optional Web App

The web app does not contain model logic. It reads a generated JSON payload:

```bash
uv run yankee-beer-web-data --output-dir web/public/data
cd web
npm ci
npm run dev
```

## Repository Layout

- `src/yankee_stadium_beer_controls/model.py`: core heterogeneous-consumer model
- `src/yankee_stadium_beer_controls/simulation.py`: scenario engine
- `src/yankee_stadium_beer_controls/price_ceiling_analysis.py`: comparative statics and figures
- `src/yankee_stadium_beer_controls/calibrate.py`: calibration command
- `src/yankee_stadium_beer_controls/paper.py`: Quarto fragments, figures, and submission outputs
- `src/yankee_stadium_beer_controls/web.py`: JSON export for the optional web app
- `paper/index.qmd`: manuscript source
- `tests/`: package, paper-build, calibration, and regression tests
- `web/`: optional Next/Tailwind dashboard

## Paper Outputs

The paper command regenerates all manuscript artifacts from package code:

- calibration table
- baseline and policy scenario tables
- ceiling stringency comparisons
- robustness diagnostics
- figures the Quarto manuscript uses
- SSRN metadata and journal cover-letter drafts

The model does not estimate causal effects. The repository makes that limited
claim reproducible and hard to accidentally desynchronize.
