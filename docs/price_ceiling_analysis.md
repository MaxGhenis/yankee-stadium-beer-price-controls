# Comparative Statics: Varying Beer Price Ceilings

This section presents a systematic analysis of how key outcomes vary with beer price ceilings, holding all other parameters constant at their baseline values.

## Methodology

We simulate stadium optimization across beer price ceilings ranging from \$5 to \$20, computing optimal ticket prices and all downstream effects. This comparative statics exercise reveals:

1. **Stadium response**: How ticket prices adjust to compensate for constrained beer revenue
2. **Quantity effects**: Changes in attendance and consumption
3. **Revenue implications**: Decomposition into ticket vs beer revenue
4. **Welfare impacts**: Distribution across consumers, producers, and society

## Key Results

### Stadium Pricing Response

```{figure} ../charts/prices.png
---
name: price-response
alt: Price response to beer ceilings
---
**Left**: Ticket prices rise by ~\$6.85 (+9.7%) as beer ceilings tighten to \$7. The rise is less dramatic than in previous calibrations but still significant. **Right**: Beer price tracks the ceiling when binding.
```

**Economic mechanism:** When beer revenue margin collapses, the stadium shifts toward ticket revenue. This "revenue substitution" effect is amplified by two-way complementarity.

### Attendance and Consumption Trade-offs

```{figure} ../charts/quantities.png
---
name: quantity-effects
alt: Attendance and beer consumption effects
---
**Left**: Attendance falls only -5.7% at \$7 ceiling (stadium remains near capacity). **Right**: Total beer consumption doubles (+98.3%) due to lower prices, despite the slight attendance drop.
```

**Key insight:** The intensive margin (beers per fan) dominates the extensive margin (number of fans). Fans consume significantly more beer when it is cheap.

### Revenue Decomposition

```{figure} ../charts/revenue.png
---
name: revenue-decomp
alt: Revenue decomposition
---
Ticket revenue rises to compensate for lost beer margins. Total revenue actually *increases* slightly (+4.5%) because demand for cheap beer is high and ticket prices rise, but **profit** falls due to the cost of serving more beer.
```

### Welfare Analysis

```{figure} ../charts/welfare.png
---
name: welfare-quad
alt: Welfare components
---
**Top left**: Producer surplus (stadium profit) falls by ~-9.0% at \$7 ceiling.
**Top right**: Consumer surplus **rises** by ~5.3%. The benefit of cheap beer outweighs the cost of slightly more expensive tickets for the average fan.
**Bottom left**: Externality costs **explode** (+98.3%) as consumption doubles.
**Bottom right**: Social welfare increases slightly (+0.8%), as the gain in Consumer Surplus outweighs the loss in Profit and the increase in Externalities.
```

### Combined Welfare View

```{figure} ../charts/welfare_combined.png
---
name: welfare-combined
alt: Welfare decomposition on single chart
---
The welfare effects are mixed: Consumers win (+5.3%), the Stadium loses (-9.0%), and Society bears more external costs (+98.3%). The net effect is a small positive, illustrating the "Second Best" theory where regulating a monopolist can improve welfare even with externalities.
```

**Policy implication:** While the ceiling improves total social welfare slightly, it does so by shifting costs to society (crime, health) and the stadium, while consumers benefit. A Pigouvian tax would address the externality directly without these distortions.

### Per-Fan Consumption

```{figure} ../charts/beers_per_fan.png
---
name: beers-per-fan
alt: Beers per fan
---
Per-capita consumption more than doubles. At \$7, average fan consumes 2.10 beers vs 1.00 at baseline. This drives the externality cost increase.
```

## Robustness Check: Is this just complementarity?

A common critique is that the "ticket price rise" result depends entirely on the assumption that beer and tickets are complements ($\epsilon_{cross} = 0.1$). We tested this by varying the cross-price elasticity from 0.0 (independent) to 0.3 (strong complements).

```{figure} ../charts/robustness_cross_elasticity.png
---
name: robustness-cross
alt: Robustness of ticket price increase
---
Ticket prices rise by over \$5 even if beer and tickets are completely independent goods ($\epsilon_{cross}=0$). The result is robust to the complementarity assumption.
```

**Surprising Result:** Even with **zero complementarity**, ticket prices rise by \$5.87.
**Why?** The internalized cost function couples the markets. Cheaper beer leads to more consumption, which increases the "rowdiness/security" cost per fan. To the stadium, this looks like an increase in the marginal cost of serving a fan, so they raise ticket prices to cover it.

## Quantitative Summary: \$7 Ceiling vs Baseline

| Metric | Baseline (\$12.51) | \$7 Ceiling | Change |
|--------|-------------------|-------------|---------|
| **Prices** |
| Beer price | \$12.51 | \$7.00 | -44% |
| Ticket price | \$70.44 | \$77.29 | +9.7% |
| **Quantities** |
| Attendance | 46,537 | 43,894 | -5.7% |
| Beers/fan | 1.00 | 2.10 | +110.2% |
| Total beers | 46,488 | 92,178 | +98.3% |
| **Revenue** |
| Profit | \$3.42M | \$3.11M | -9.0% |
| **Welfare** |
| Consumer surplus | \$11.4M | \$12.0M | +5.3% |
| Externality cost | \$0.2M | \$0.4M | +98.3% |
| Social welfare | \$14.7M | \$14.8M | +0.8% |

## Comparison with Leisten (2025)

Our quantitative results confirm {cite}`leisten2025beer` theoretical prediction: **beer price ceilings cause ticket prices to rise**. We extend his analysis by:

1. **Magnitude**: \$7 ceiling → \$6.85 ticket increase.
2. **Two-way complementarity**: Beer prices affect attendance in our model.
3. **Welfare decomposition**: We find that consumers *can* benefit (CS rises) even if tickets rise, if the beer price drop is large enough.

## Policy Implications

1. **Trade-offs are complex**: Ceilings help consumers and slightly improve total welfare, BUT they drastically increase negative externalities (crime/health).
2. **Pigouvian taxation is likely superior**: It targets the externality directly.
3. **Stadium incentives**: The stadium loses profit (-9.0%), giving them incentive to fight this policy.
4. **Unintended consequences**: Ticket prices rising 9.7% is a significant side effect that policymakers must anticipate.

```{bibliography}
:filter: docname in docnames
```