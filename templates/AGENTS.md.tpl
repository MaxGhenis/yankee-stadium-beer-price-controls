<!--AGENT: ALL-->
# Project Context for AI Agents

<!-- This file is the template for generating CLAUDE.md and GEMINI.md. -->
<!-- Edit this file, then run `python scripts/generate_agent_files.py` to update the agent-specific files with live model values. -->

## Project Overview

**Name:** Yankee Stadium Beer Price Controls
**Purpose:** An economic research project and simulation engine analyzing the impact of beer price controls (ceilings, floors) at Yankee Stadium. It uses a rigorous economic model to simulate consumer behavior, stadium revenue maximization, and social welfare outcomes (including externalities like crime and health costs).

**Key Findings:**
*   **General Equilibrium Response:** A $6 beer ceiling (half price) causes ticket prices to rise ~21% as the stadium shifts revenue capture to tickets. Attendance falls ~20%.
*   **Selection Effects:** Higher tickets disproportionately deter non-drinkers, shifting crowd composition toward drinkers. Per-fan consumption triples (+207%).
*   **Consumption Paradox:** Despite lower attendance, total beer consumption increases 146% because per-fan consumption more than offsets attendance decline.
*   **Internalized Costs:** The model distinguishes between costs the stadium pays (security, brand damage) and costs society pays (crime, public health).

## Technical Stack

*   **Language:** Python 3.13
*   **Package Manager:** `uv` (recommended)
*   **Web Framework:** Streamlit (for the interactive app)
*   **Documentation:** JupyterBook (MyST Markdown)
*   **Testing:** `pytest` (98% coverage)
*   **Linting/Formatting:** `ruff`, `black`

## Project Structure

### Source Code (`src/`)
*   **`model.py`**: The core `StadiumEconomicModel` class.
    *   **Features:** Heterogeneous consumers (Drinkers vs. Non-drinkers), semi-log demand, revenue optimization (L-BFGS-B), welfare calculation.
    *   **Key Methods:** `total_attendance()`, `stadium_revenue()`, `optimal_pricing()`, `social_welfare()`.
*   **`simulation.py`**: The `BeerPriceControlSimulator` class.
    *   **Function:** Runs policy scenarios (Baseline, Ceiling, Floor, Ban, Social Optimum) and sensitivity analyses.
*   **`app.py`**: The Streamlit dashboard.
    *   **Function:** Visualizes model results, allows real-time parameter adjustment, and compares scenarios.
*   **`calibrate.py`**: Tools for calibrating model parameters to observed market data.

### Documentation (`docs/`)
*   **Format:** JupyterBook (MyST).
*   **Content:** Academic paper structure including `intro.md`, `model.md`, and interactive notebooks (`simulation.ipynb`).
*   **Build System:** Uses `myst`. **CRITICAL:** Always perform a clean build (`scripts/rebuild_docs.sh`) to avoid stale cache issues.

### Tests (`tests/`)
*   Comprehensive suite covering model logic, simulation scenarios, and calibration.
*   **Convention:** Uses `pytest` fixtures. Run with `pytest tests/`.

## Development Workflow

### 1. Environment Setup
```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev,docs]"
```

### 2. Running the Application
```bash
streamlit run src/app.py
```

### 3. Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

### 4. Code Quality
```bash
# Formatting
black src tests

# Linting
ruff check src tests

# Type Checking
mypy src
```

### 5. Documentation
**Always use the rebuild script to ensure fresh content:**
```bash
./scripts/rebuild_docs.sh
```
*   The output is generated in `docs/_build/site/`.
*   Never rely on `myst build` alone without cleaning first.

<!--AGENT: CLAUDE-->
## Architecture Details (Claude Specific)

### Core Model (`src/model.py`)

The `StadiumEconomicModel` class features **heterogeneous consumers**:

**Consumer Types**:
- **Non-Drinkers (60%)**: α_beer=1.0 → 0 beers at typical prices
- **Drinkers (40%)**: α_beer=43.75 → 2.5 beers at \$12.50
- Matches empirical data: 40% drink, 1.0 beers/fan average

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

### Simulation Engine (`src/simulation.py`)

The `BeerPriceControlSimulator` class runs policy scenarios:

**Scenarios**:
1. Baseline (current profit-maximizing prices)
2. Current observed prices (for comparison)
3. Price ceiling (e.g., $6 = half price)
4. Price floor (e.g., $15 min beer price)
5. Beer ban (zero sales)
6. Social optimum (maximize social welfare, not just profit)

## Calibration Philosophy

The model uses **semi-log demand calibrated to observed prices** rather than constant elasticity:
- Literature elasticities inform calibration but aren't directly used
- Baseline prices ($80 tickets, $12.50 beer) should be approximately profit-maximizing
- This reflects that stadiums are sophisticated monopolists
- Stadium-specific adjustments: captive audience, experiential value, complementarity

**Why tickets may differ from pure profit max**: Real stadiums consider brand value, crowd management, and social responsibility not fully captured in the model. The model is for *comparative analysis* of policies, not exact price prediction.

## Critical Parameters
- `cross_price_elasticity` (default 0.1): Beer price effect on attendance. This is ASSUMED, not empirically estimated. Default is conservative (weak complementarity).
- `experience_degradation_cost` (default {{ experience_degradation_cost }}): Calibrated convex cost for internalized externalities
- Tax structure: Excise $0.074/beer, sales tax 8.875%

<!--AGENT: GEMINI-->
## Key Economic Concepts

*   **Heterogeneous Consumers:** The model separates fans into "Drinkers" (40%) and "Non-Drinkers" (60%) to accurately model demand response.
*   **Complementarity:** Assumes a cross-price elasticity (default 0.1) where beer price affects ticket demand (and vice versa).
*   **Selection Effects:** Price policies change the composition of the crowd (e.g., cheap beer attracts more drinkers).
*   **Social Welfare:** Calculated as Consumer Surplus + Producer Surplus - External Costs.

## Conventions

*   **Line Length:** 100 characters.
*   **Type Hints:** Encouraged but strictly enforced only where `mypy` passes.
*   **Docstrings:** Google style.
*   **Reverting:** Do not revert changes unless explicitly asked.
*   **Tests:** All new features must include tests.
