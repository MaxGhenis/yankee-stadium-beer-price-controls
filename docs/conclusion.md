# Conclusions

## Key Findings

### 1. Price Ceilings Increase Consumption

A $7 beer ceiling at Yankee Stadium increases total beer consumption by approximately 77%, despite reducing attendance by 6%. This occurs because:

- The stadium raises ticket prices ~10% to offset lost beer margin
- Per-fan beer consumption more than doubles (from 1.0 to 2.1 beers)
- The intensive margin effect dominates the attendance decline

### 2. Selection Effects Alter Crowd Composition

The heterogeneous consumer model reveals differential attendance responses:

| Consumer Type | Attendance Change | Mechanism |
|---------------|-------------------|-----------|
| Non-drinkers | -11.5% | Only see ticket price increase |
| Drinkers | -6.3% | Ticket increase offset by cheaper beer value |

This shifts crowd composition from 40% to 41.4% drinkers (+1.4 percentage points).

### 3. Decomposition: Intensive vs Extensive Margin

Using Shapley decomposition:
- **Intensive margin: +116%** (each fan drinks more)
- **Extensive margin: -16%** (attendance falls)

The intensive margin accounts for more than 100% of the consumption increase because the extensive margin partially offsets it—attendance falls, which would reduce consumption if per-fan consumption stayed constant.

### 4. Results Are Robust

Monte Carlo analysis over 1,000 parameter combinations:
- Tickets rise in >95% of scenarios
- Consumption increases in >95% of scenarios
- Stadium profit falls in >99% of scenarios

The qualitative conclusions hold across wide parameter ranges for cross-price elasticity (0.0-0.3) and drinker share (30%-50%).

### 5. Model Validates Against Observed Prices

The heterogeneous model predicts an optimal beer price of $12.51, compared to $12.50 observed. This 0.08% calibration error (vs 20-30% for homogeneous models) suggests:
- Stadiums approximately profit-maximize
- The two-type consumer structure captures key demand features
- Observed prices reflect equilibrium behavior

## Limitations

1. **Simulation study**: Parameters are calibrated, not estimated from transaction data
2. **Static model**: Doesn't capture dynamic adjustments (season tickets, reputation effects)
3. **No substitution**: Doesn't model pre-game drinking or smuggling responses
4. **Partial equilibrium**: No competition from other entertainment venues
5. **Perfect enforcement**: Assumes price controls are fully enforced

## Testable Predictions

The model generates predictions that could be tested with stadium transaction data:

1. Under price ceilings, **drinker share of attendance should increase**
2. **Per-fan consumption should rise more than proportionally** to the price decrease
3. **Ticket prices should partially offset** beer margin compression

These predictions distinguish the heterogeneous model from representative agent approaches.

## Broader Implications

### For Stadium Pricing

The heterogeneous consumer framework reveals that:
- Price policies change *who* attends, not just *how many*
- Selection effects can amplify or dampen policy impacts
- Simple demand elasticity estimates miss composition effects

### For Complementary Goods

When a monopolist controls two complements:
- Constraining one price shifts optimization to the other
- Consumer heterogeneity creates differential responses
- General equilibrium effects can dominate partial equilibrium intuitions

### For Policy Analysis

Representative agent models may underestimate policy effects when:
- Consumers have heterogeneous preferences for the regulated good
- Price changes induce selection on consumer composition
- Multiple margins of adjustment exist

## Future Research

- **Empirical validation**: Natural experiments from stadium policy changes
- **Dynamic model**: Repeated games, season ticket holder behavior
- **Substitution patterns**: Pre-game drinking, tailgating responses
- **Spatial analysis**: Crime externalities by distance from stadium
- **Welfare analysis**: Distributional effects across consumer types

```{bibliography}
:filter: docname in docnames
```
