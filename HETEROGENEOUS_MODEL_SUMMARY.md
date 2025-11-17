# Heterogeneous Consumer Model - Major Breakthrough

## Key Finding: 76% Improvement in Calibration

The heterogeneous preference model (`model_heterogeneous.py`) significantly improves our ability to match observed prices:

**Calibration Results:**
- **Homogeneous model**: Predicts optimal beer = $14.59 (error: $2.09)
- **Heterogeneous model**: Predicts optimal beer = $13.00 (error: $0.50)
- **Improvement**: 76% reduction in calibration error!

## Model Structure

**Two Consumer Types** (matching Lenk et al. 2010 data):

1. **Non-Drinkers (60%)**
   - α_beer = 1.0 (low beer preference → consume 0 beers)
   - α_experience = 3.0 (high stadium value)
   - Attend for the game, not the beer

2. **Drinkers (40%)**
   - α_beer = 43.75 (calibrated to consume 2.5 beers at $12.50)
   - α_experience = 2.5 (moderate stadium value)
   - Beer is important part of experience

## Critical New Insight: Selection Effects

**Attendance Composition Shifts with Price Controls:**

At $7 beer ceiling:
- Baseline: 60% non-drinkers, 40% drinkers
- With ceiling: 30% non-drinkers, 70% drinkers (+30 percentage points!)
- Mechanism: $200 tickets drive out non-drinkers; drinkers stay for cheap beer

**Policy Implication**: Price ceilings don't just change aggregate attendance - they change WHO attends. Crowd becomes concentrated with drinkers, potentially amplifying externalities.

## Why Heterogeneity Matters Economically

Not just curve-fitting - captures genuine economic mechanism:

1. **Extensive margin**: Who drinks? (missing from representative consumer)
2. **Intensive margin**: How much do drinkers drink?
3. **Selection effects**: Policies change crowd composition
4. **Lower optimal price**: Stadium prices to capture marginal drinkers

## Usage

```python
from src.model_heterogeneous import HeterogeneousStadiumModel

# Default: 2-type model (60% non-drinkers, 40% drinkers)
model = HeterogeneousStadiumModel()

# Homogeneous version (for comparison)
homo_model = HeterogeneousStadiumModel.create_homogeneous(alpha_beer=1.5)

# Custom types
from src.model_heterogeneous import ConsumerType
custom_types = [
    ConsumerType("Light", share=0.7, alpha_beer=5.0, alpha_experience=3.0, income=150),
    ConsumerType("Heavy", share=0.3, alpha_beer=80.0, alpha_experience=2.0, income=250)
]
custom_model = HeterogeneousStadiumModel(consumer_types=custom_types)
```

## Next Steps

1. Make heterogeneous the default model (replace model.py)
2. Add composition reporting to all policy scenarios
3. Create distributional welfare analysis
4. Update documentation throughout

The heterogeneous model should become the primary specification given its superior calibration and richer insights.
