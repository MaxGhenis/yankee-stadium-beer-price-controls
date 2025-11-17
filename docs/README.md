# Beer Price Controls at Yankee Stadium - Documentation

## JupyterBook Report

This directory contains the complete JupyterBook analysis.

### Building the Book

**Requirements:**
```bash
pip install jupyter-book sphinxcontrib-bibtex
# OR
npm install -g mystmd
```

**Build (JupyterBook 2 / MyST):**
```bash
cd docs
myst build
myst start  # Local server
```

**Build (Legacy JupyterBook):**
```bash
jupyter-book build docs
```

**Output**: `docs/_build/site/` (MyST) or `docs/_build/html/` (legacy)

### Structure

- `intro.md` - Introduction and overview
- `executive_summary.md` - Key findings and recommendations
- `background.md` - Literature review
- `model.md` - Economic framework
- `calibration.md` - Parameter estimation
- `simulation.ipynb` - Interactive analysis with $7 ceiling
- `sensitivity.ipynb` - Robustness checks
- `monte_carlo.ipynb` - Uncertainty quantification
- `assumptions.md` - Data sources and limitations
- `complementarity_specs.md` - Alternative modeling approaches
- `policy.md` - Policy recommendations
- `taxes.md` - Pigouvian tax analysis
- `conclusion.md` - Summary
- `references.bib` - Bibliography (20+ papers)

### Deployment

**GitHub Pages** (automatic):
1. Push to `master` branch
2. GitHub Actions builds and deploys
3. Site: https://maxghenis.github.io/yankee-stadium-beer-price-controls

**Manual deployment:**
```bash
jupyter-book build docs
gh-pages -d docs/_build/html
```

### Key Results

**$7 Beer Price Ceiling Effects:**
- Ticket prices: +$32 (+36%)
- Attendance: -38%
- Stadium profit: -$47M/season
- Externality costs: +97%

**Pigouvian Tax ($2.91/beer):**
- Consumer price: $15.41
- Revenue: $6.7M/season
- Consumption: -29%
- Most efficient policy

**Model Features:**
- Tax-aware (stadium receives $11.41, not $12.50)
- Internalized costs (convex function)
- Complementarity (adjustable parameter)
- Literature-based elasticities
- Monte Carlo uncertainty

### Citations

Uses MyST markdown citation format:
- Inline: `{cite}`key``
- Multiple: `{cite}`key1,key2``
- Bibliography: `{bibliography}`

See `references.bib` for full citations.
