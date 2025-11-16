# Quick Start Guide

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/[username]/yankee-stadium-beer-price-controls.git
   cd yankee-stadium-beer-price-controls
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

### Option 1: Streamlit Web App (Recommended)

Launch the interactive web interface:

```bash
streamlit run src/app.py
```

This will open a browser window with:
- Interactive parameter controls
- Real-time simulation results
- Comparative visualizations
- Downloadable data

### Option 2: Command Line

Run the basic example script:

```bash
python src/example.py
```

This prints results to console including:
- All policy scenarios
- Summary statistics
- Key insights
- Comparative analysis

### Option 3: Python API

Use the model in your own scripts:

```python
from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator

# Initialize model
model = StadiumEconomicModel(
    capacity=46537,
    base_ticket_price=80.0,
    base_beer_price=12.5,
    ticket_elasticity=-0.625,
    beer_elasticity=-0.965
)

# Create simulator
simulator = BeerPriceControlSimulator(model)

# Run scenarios
results = simulator.run_all_scenarios(
    price_ceiling=8.0,
    price_floor=15.0
)

print(results)
```

## Understanding the Parameters

### Demand Elasticities

- **Ticket elasticity** (-0.49 to -0.76): How much attendance changes with ticket price
  - More negative = more elastic (more sensitive to price)
  - Literature shows MLB demand is **inelastic**

- **Beer elasticity** (-0.79 to -1.14): How much beer consumption changes with price
  - Values near -1.0 are "unit elastic"
  - MLB beer demand is **relatively inelastic**

### Externality Costs

- **Crime cost per beer** ($2.50): External costs from alcohol-related violence
  - Based on Carpenter & Dobkin (2015): 10% alcohol increase → 1% assault increase
  - Includes police, emergency services, property damage

- **Health cost per beer** ($1.50): External costs from health system burden
  - Based on Manning et al. (1991), inflation-adjusted
  - Includes ER visits, treatment, long-term health impacts

## Policy Scenarios Explained

1. **Baseline (Profit Max)**: Stadium chooses prices to maximize profit (no constraints)

2. **Current Observed Prices**: Actual market prices ($80 tickets, $12.50 beer)

3. **Price Ceiling**: Maximum beer price (e.g., $8)
   - Aims to increase affordability
   - May reduce stadium revenue
   - Could increase consumption and externalities

4. **Price Floor**: Minimum beer price (e.g., $15)
   - Aims to reduce consumption
   - May increase stadium revenue
   - Could reduce externalities

5. **Beer Ban**: Zero beer sales allowed
   - Eliminates beer revenue
   - May reduce attendance (complementarity)
   - Eliminates beer-related externalities
   - May shift drinking to pre-game (not modeled)

6. **Social Optimum**: Prices that maximize social welfare (CS + PS - Externalities)
   - Typically higher beer price than profit maximum
   - Internalizes external costs

## Key Metrics

- **Consumer Surplus**: Consumer benefit above what they pay
- **Producer Surplus**: Stadium profit (revenue - costs)
- **Externality Cost**: Social costs from alcohol consumption
- **Social Welfare**: CS + PS - Externalities (total societal benefit)
- **Deadweight Loss**: Efficiency loss from price distortions

## Customizing the Analysis

### Changing Parameters

Edit `data/default_parameters.json` or use the Streamlit sidebar controls to adjust:
- Stadium capacity
- Baseline prices
- Elasticities
- Cost structure
- Consumer preferences
- Externality costs

### Adding New Scenarios

In `src/simulation.py`, add custom scenarios:

```python
def run_custom_scenario(self):
    # Your custom price controls
    return self.run_scenario(
        "Custom Policy",
        beer_price_min=10.0,
        beer_price_max=20.0
    )
```

### Sensitivity Analysis

Run sensitivity analysis on any parameter:

```python
# Example: How do results change with different beer elasticities?
results = simulator.sensitivity_analysis(
    parameter_name='beer_elasticity',
    values=[-0.5, -0.7, -0.9, -1.1, -1.3]
)
```

## Interpreting Results

### Revenue Effects

- **Higher beer prices** → Lower consumption → May increase or decrease revenue (depends on elasticity)
- **Lower ticket prices** → Higher attendance → More total beer sales

### Welfare Effects

- **Price ceiling below equilibrium** → Consumer surplus up, producer surplus down, deadweight loss
- **Price floor above equilibrium** → Consumer surplus down, producer surplus may rise, deadweight loss
- **Externalities matter**: Socially optimal price > privately optimal price

### Realistic Expectations

- Elasticities suggest **small consumption responses** to moderate price changes
- Complementarity between tickets and beer means **joint optimization** is key
- Externality reduction requires **large** price increases or quantity restrictions
- Revenue loss from restrictions is **substantial** (beer is high-margin)

## Limitations

1. **Static model**: Doesn't capture long-run effects (season tickets, loyalty)
2. **Single representative consumer**: Ignores heterogeneity (casual vs. regular fans)
3. **No substitution**: Doesn't model pre-game drinking or smuggling
4. **Perfect enforcement**: Assumes price controls are perfectly enforced
5. **Partial equilibrium**: Doesn't model competition from other entertainment

## Next Steps

- **Explore the Streamlit app** to see how changing parameters affects outcomes
- **Read the academic references** in `references/REFERENCES.md`
- **Modify the model** to test your own hypotheses
- **Run sensitivity analyses** to understand parameter uncertainty

## Troubleshooting

### Import errors
```bash
# Make sure you're in the project root directory
cd yankee-stadium-beer-price-controls

# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Streamlit not loading
```bash
# Check Streamlit is installed
streamlit --version

# Try running from project root with full path
streamlit run src/app.py
```

## Getting Help

- **Documentation**: See `README.md` and `references/REFERENCES.md`
- **Issues**: Open an issue on GitHub
- **Questions**: Check the "About" section in the Streamlit app

## Citation

If you use this model in research:

```bibtex
@software{yankee_stadium_beer_controls,
  title = {Beer Price Controls at Yankee Stadium: Economic Simulator},
  author = {[Your Name]},
  year = {2025},
  url = {https://github.com/[username]/yankee-stadium-beer-price-controls}
}
```
