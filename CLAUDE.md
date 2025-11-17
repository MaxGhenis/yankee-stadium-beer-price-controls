# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic economics research project analyzing beer price controls at Yankee Stadium. It models consumer welfare, stadium revenue, attendance effects, and negative externalities (crime, health costs) from alcohol consumption. The project includes:

- A Python economic model with demand functions, revenue optimization, and welfare calculations
- A Streamlit web application for interactive policy exploration
- JupyterBook documentation with academic paper format
- Comprehensive test suite with 98% coverage

**Key insight**: The model distinguishes between *internalized* costs (crowd management, brand damage, experience degradation that the stadium already accounts for) and *external* costs (crime, public health) that justify policy intervention.

## Development Commands

### Environment Setup
```bash
# Create virtual environment with uv (recommended)
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (development mode)
uv pip install -e ".[dev]"

# Install with docs dependencies
uv pip install -e ".[dev,docs]"
```

### Testing
```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_model.py -v

# Run specific test function
pytest tests/test_model.py::TestDemandFunctions::test_beer_demand_at_baseline -v

# Run tests with output (disable capture)
pytest tests/ -v -s
```

### Code Quality
```bash
# Lint with ruff
ruff check src tests

# Format with black
black src tests

# Check formatting without modifying
black --check src tests

# Type check with mypy
mypy src
```

### Running the Application
```bash
# Launch interactive Streamlit app
streamlit run src/app.py

# Run example simulation
python src/example.py
```

### Building Documentation
```bash
# Build JupyterBook documentation
cd docs
jupyter-book build .

# View built docs (output in docs/_build/html)
open _build/html/index.html  # macOS
```

## Architecture

### Core Model (`src/model.py`)

The `StadiumEconomicModel` class is the heart of the economic analysis:

**Demand Functions**:
- Uses **semi-log demand** (not constant elasticity) calibrated so observed prices are near profit-maximizing
- `_attendance_demand()`: Ticket demand with cross-price effects from beer (complementarity)
- `_beers_per_fan_demand()`: Beer consumption per attendee
- Key calibration: baseline is 1.0 beers/fan (~40% of fans drink, averaging 2.5 beers)

**Revenue Calculations** (`stadium_revenue()`):
- Handles NYC tax structure: 8.875% sales tax + $0.074/beer excise tax
- Stadium receives: `beer_price / (1 + sales_tax_rate) - excise_tax`
- Includes internalized costs via `_internalized_costs()` with convex cost function
- Returns dict with attendance, consumption, revenue, costs, profit, and tax revenue

**Optimization** (`optimal_pricing()`):
- Uses scipy L-BFGS-B to find profit-maximizing ticket and beer prices
- Supports price controls via `beer_price_control` parameter
- Returns tuple: `(optimal_ticket_price, optimal_beer_price, results_dict)`

**Welfare Analysis**:
- `consumer_surplus()`: Using elasticity formula adjusted for captive audience
- `producer_surplus()`: Stadium profit
- `externality_cost()`: External costs from crime ($2.50/beer) and health ($1.50/beer)
- `social_welfare()`: CS + PS - externalities

**Critical Parameters**:
- `cross_price_elasticity` (default 0.1): Beer price effect on attendance. This is ASSUMED, not empirically estimated. Default is conservative (weak complementarity).
- `experience_degradation_cost` (default 250.0): Calibrated convex cost for internalized externalities
- Tax structure: Excise $0.074/beer, sales tax 8.875%

### Simulation Engine (`src/simulation.py`)

The `BeerPriceControlSimulator` class runs policy scenarios:

**Scenarios**:
1. Baseline (current profit-maximizing prices)
2. Current observed prices (for comparison)
3. Price ceiling (e.g., $7-8 max beer price)
4. Price floor (e.g., $15 min beer price)
5. Beer ban (zero sales)
6. Social optimum (maximize social welfare, not just profit)

**Key Methods**:
- `run_scenario()`: Single policy simulation with externality costs
- `run_all_scenarios()`: Batch run all standard scenarios
- `_find_social_optimum()`: Optimization to maximize social welfare
- `sensitivity_analysis()`: Vary a parameter across values
- `calculate_comparative_statics()`: Changes relative to baseline

### Streamlit App (`src/app.py`)

Interactive web application with:
- Sidebar parameter controls (elasticities, costs, preferences, complementarity)
- Policy scenario comparison (ceiling, floor, ban, social optimum)
- **Ticket price response analysis**: Shows how ticket prices adjust when beer prices are constrained (key finding: $7 beer ceiling causes $32 ticket increase)
- Four visualization tabs: Revenue & Welfare, Attendance & Consumption, Price Comparison, Externalities
- Comparative analysis table showing changes relative to baseline

**Caching**: Uses `@st.cache_data` on `create_model()` for performance.

### Test Structure (`tests/`)

Comprehensive test suite organized by functionality:
- `test_model.py`: Core economic model tests (demand, revenue, optimization, welfare)
- `test_simulation.py`: Scenario simulation tests
- `test_coverage.py`: Meta-test ensuring 98% coverage

**Test organization**:
- Classes group related tests (e.g., `TestDemandFunctions`, `TestRevenueCalculations`)
- Uses pytest fixtures for model initialization
- Tests document expected behavior (see docstrings in `test_optimal_beer_price_reasonable()`)

## Documentation (JupyterBook)

Located in `docs/` directory:
- Academic paper format with MyST markdown and Jupyter notebooks
- Configuration: `_config.yml` (legacy Jupyter Book 1) and `myst.yml` (new MyST)
- Table of contents: `_toc.yml`
- Build output: `docs/_build/site/` (published to GitHub Pages)

**Key documents**:
- `intro.md`: Introduction with academic prose
- `background.md`: Literature review
- `model.md`: Model specification
- `simulation.ipynb`: Interactive simulation results
- `monte_carlo.ipynb`: Uncertainty quantification
- `sensitivity.ipynb`: Parameter sensitivity analysis
- `references.bib`: BibTeX citations (30+ academic papers)

## Data Sources and Calibration

**Current Pricing** (2025):
- Beer: $12.50 average (range $10-15)
- Tickets: $80 average
- Capacity: 46,537

**Literature-Based Elasticities**:
- Ticket demand: -0.625 (midpoint of -0.49 to -0.76, from Noll 1974, Scully 1989)
- Beer demand: -0.965 (midpoint of -0.79 to -1.14, relatively inelastic in MLB)

**Externality Costs**:
- Crime: $2.50/beer (based on Carpenter & Dobkin 2015: 10% alcohol increase → 1% assault increase, 2.9% rape increase)
- Health: $1.50/beer (based on Manning et al. 1991, inflation-adjusted)

**Tax Structure**:
- Federal excise: $0.058/beer (12 oz, $18/barrel)
- State excise: $0.014/beer (NY)
- Local excise: $0.002/beer (NYC)
- Sales tax: 8.875% (NYC)
- Total: Consumer pays $12.50, stadium receives $11.41

## Model Calibration Philosophy

The model uses **semi-log demand calibrated to observed prices** rather than constant elasticity:
- Literature elasticities inform calibration but aren't directly used
- Baseline prices ($80 tickets, $12.50 beer) should be approximately profit-maximizing
- This reflects that stadiums are sophisticated monopolists
- Stadium-specific adjustments: captive audience, experiential value, complementarity

**Why tickets may differ from pure profit max**: Real stadiums consider brand value, crowd management, and social responsibility not fully captured in the model. The model is for *comparative analysis* of policies, not exact price prediction.

## Key Findings (for context)

**$7 Beer Ceiling Effects**:
- Beer consumption: 1.0 → 2.1 beers/fan (+108%)
- Ticket price: $89 → $121 (+$32, +36%) - stadium shifts to ticket revenue
- Attendance: Falls 38% (higher tickets + complementarity effect)
- Stadium profit: -$47M/season

**Pigouvian Tax Gap**:
- External costs: $4.00/beer
- Current taxes: $1.09/beer
- Optimal additional tax: $2.91/beer
- Revenue potential: $6.7M/season for NYC

## Common Workflows

### Adding a New Policy Scenario
1. Add scenario logic to `BeerPriceControlSimulator.run_scenario()`
2. Add to `run_all_scenarios()` if it's a standard scenario
3. Update Streamlit app to display the new scenario
4. Add tests in `tests/test_simulation.py`

### Modifying the Economic Model
1. Update `StadiumEconomicModel` in `src/model.py`
2. Update tests in `tests/test_model.py`
3. Run `pytest` to ensure all tests pass
4. If changing key parameters, update documentation in `docs/`
5. Recalibrate if needed to maintain observed prices as approximately optimal

### Adding Model Parameters
1. Add parameter to `__init__()` in `StadiumEconomicModel`
2. Add parameter to Streamlit sidebar in `src/app.py`
3. Update `create_model()` function call to include new parameter
4. Update tests to use/test new parameter
5. Document parameter in this CLAUDE.md file

### Updating Documentation
1. Edit markdown/notebook files in `docs/`
2. Rebuild: `cd docs && jupyter-book build .`
3. Check output in `docs/_build/html/`
4. Commit both source and built files (GitHub Pages serves from `docs/_build/site/`)

## Code Style and Standards

- Python 3.13 required
- Line length: 100 characters (black and ruff configured)
- Type hints: Encouraged but not enforced (mypy set to continue-on-error)
- Docstrings: Google style, especially for public methods
- Test coverage: Maintain >95% coverage (currently 98%)

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
- Runs on: Ubuntu, macOS, Windows
- Python 3.13 only
- Steps: ruff lint, black format check, mypy (continue-on-error), pytest with coverage
- Uses `uv` for fast dependency installation

## Important Notes

1. **Cross-price elasticity** (tickets-beer): The default 0.1 is ASSUMED, not empirically estimated. Literature documents complementarity exists but not the specific magnitude. Sensitivity analysis is recommended.

2. **Tax-aware pricing**: Always remember the stadium receives less than the consumer pays. Use `stadium_beer_price` not `consumer_beer_price` for revenue calculations.

3. **Calibration vs prediction**: The model is calibrated so observed prices are near-optimal. It's designed for *comparative statics* (how policies change outcomes) not *price prediction*.

4. **Internalized vs external costs**: The model carefully distinguishes costs the stadium already accounts for (internalized) vs costs society bears (external). Only external costs justify policy intervention.

5. **Semi-log demand**: The model does NOT use constant elasticity demand. It uses exponential (semi-log) demand calibrated to make observed prices approximately optimal.

## References

See `docs/references.bib` for full academic references (30+ papers). Key sources:
- Stadium pricing: Noll 1974, Scully 1989, Krautmann & Berri 2007
- Alcohol externalities: Carpenter & Dobkin 2015, Manning et al. 1991
- Crime impacts: Rees & Schnepel 2009
- Theoretical analysis: Leisten 2024 Twitter thread (https://x.com/LeistenEcon/status/1990150035615494239)

## Comparison to Leisten (2025) Theoretical Analysis

Matthew Leisten's rigorous Twitter thread proves that under log-concavity, beer price ceilings cause ticket prices to rise. Key differences from our model:

**Leisten's approach:**
- One-way complementarity (tickets → beer, but beer prices don't affect ticket demand)
- Zero marginal costs (acknowledged as unrealistic)
- General functional forms with log-concavity assumption
- Proves sign of effect analytically

**Our approach:**
- Two-way complementarity (tickets ↔ beer) with assumed cross-elasticity of 0.1
- Realistic marginal costs ($3.50 tickets, $2.00 beer)
- Semi-log demand calibrated to observed prices (satisfies log-concavity)
- Quantitative predictions with welfare analysis

**Both models predict**: Beer ceilings → ticket prices rise. Our model quantifies the magnitude and adds externality analysis. Leisten proves the theoretical conditions under which this occurs.
