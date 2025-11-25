# Comparative Statics: Varying Beer Price Ceilings

This section presents a systematic analysis of how key outcomes vary with beer price ceilings, holding all other parameters constant at their baseline values.

## Methodology

We simulate stadium optimization across beer price ceilings ranging from \$5 to \$10, computing optimal ticket prices and all downstream effects. This comparative statics exercise reveals:

1. **Stadium response**: How ticket prices adjust to compensate for constrained beer revenue
2. **Quantity effects**: Changes in attendance and consumption
3. **Revenue implications**: Decomposition into ticket vs beer revenue
4. **Welfare impacts**: Distribution across consumers, producers, and society

## Key Results

### Stadium Pricing Response

As beer ceilings tighten, the stadium raises ticket prices substantially:

| Ceiling | Ticket Increase | Attendance Change | Total Beers |
|---------|-----------------|-------------------|-------------|
| \$5 | +36% | -32% | +158% |
| \$6 | +21% | -20% | +146% |
| \$7 | +10% | -9% | +131% |
| \$8 | +4% | -2% | +110% |

**Economic mechanism:** When beer revenue margin collapses, the stadium shifts toward ticket revenue. This "revenue substitution" effect is amplified by selection effects among heterogeneous consumers.

### Attendance and Consumption Trade-offs

**Key insight:** The intensive margin (beers per fan) dominates the extensive margin (number of fans). At a \$6 ceiling (half price):
- Per-fan consumption triples (+207%): 0.86 → 2.63 beers
- Attendance falls 20%
- Net effect: Total beers increase 146%

### Selection Effects

The heterogeneous consumer model reveals that price ceilings don't just change *how much* people consume—they change *who attends*:

- **Non-drinkers**: Only see ticket increase → attendance falls more
- **Drinkers**: Beer savings offset ticket increase → attendance falls less
- **Result**: Crowd composition shifts toward drinkers

This selection effect is absent from representative agent models.

## Robustness Check: Is this just complementarity?

A common critique is that the "ticket price rise" result depends on the complementarity assumption. We tested this by varying the cross-price elasticity.

**Result:** Ticket prices rise even with zero complementarity. The internalized cost function couples the markets: cheaper beer leads to more consumption, which increases security/crowd management costs, which gets passed through to tickets.

## Quantitative Summary: \$6 Ceiling vs Baseline

| Metric | Baseline | \$6 Ceiling | Change |
|--------|----------|-------------|---------|
| **Prices** |
| Beer price | \$12.50 | \$6.00 | -52% |
| Ticket price | \$70.44 | \$85.33 | +21% |
| **Quantities** |
| Attendance | 46,345 | 37,232 | -20% |
| Beers/fan | 0.86 | 2.63 | +207% |
| Total beers | 39,700 | 97,856 | +146% |

## Comparison with Leisten (2025)

Our quantitative results confirm {cite}`leisten2025beer` theoretical prediction: **beer price ceilings cause ticket prices to rise**. We extend his analysis by:

1. **Heterogeneous consumers**: Selection effects shift crowd composition
2. **Quantitative magnitude**: \$6 ceiling → 21% ticket increase
3. **Two-way complementarity**: Beer prices affect attendance in our model

## Policy Implications

1. **Trade-offs are complex**: Ceilings increase total beer consumption and externalities while benefiting drinkers at the expense of non-drinkers and stadiums
2. **Selection effects matter**: Crowd composition shifts toward drinkers under price ceilings
3. **Stadium incentives**: The stadium loses profit, giving them incentive to resist such policies
4. **General equilibrium response**: Ticket prices rising 21% (at \$6 ceiling) is a significant adjustment that policymakers must anticipate

```{bibliography}
:filter: docname in docnames
```
