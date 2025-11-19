<!-- This file is auto-generated from templates/AGENTS.md.tpl. Do not edit directly. -->

# Project Context for AI Agents

<!-- This file is the template for generating CLAUDE.md and GEMINI.md. -->
<!-- Edit this file, then run `python scripts/generate_agent_files.py` to update the agent-specific files with live model values. -->

## Project Overview

**Name:** Yankee Stadium Beer Price Controls
**Purpose:** An economic research project and simulation engine analyzing the impact of beer price controls (ceilings, floors) at Yankee Stadium. It uses a rigorous economic model to simulate consumer behavior, stadium revenue maximization, and social welfare outcomes (including externalities like crime and health costs).

**Key Findings:**
*   **Unintended Consequences:** A $7 beer ceiling causes ticket prices to rise by ~$6.85 (+9.7%) as the stadium shifts revenue capture to tickets. Attendance falls ~5.7%.
*   **Pigouvian Tax Gap:** Current taxes ($1.09) are significantly lower than external costs ($4.00), suggesting an optimal additional tax of ~$2.91.
*   **Internalized Costs:** The model distinguishes between costs the stadium pays (security, brand damage) and costs society pays (crime, public health).
*   **Welfare Paradox:** A $7 ceiling actually *increases* net social welfare slightly (+0.8%) because consumer surplus gains outweigh stadium profit losses and externality increases ("Second Best" theory), but it drastically increases negative externalities (+98%).

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
