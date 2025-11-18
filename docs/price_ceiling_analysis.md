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
**Left**: Ticket prices rise by up to \\$44 (+57%) as beer ceilings tighten from \\$13 to \\$5. Above \\$13, the ceiling is non-binding and prices plateau at baseline. **Right**: Beer price tracks the ceiling when binding (below ~\\$13).
```

**Economic mechanism:** When beer revenue margin collapses, the stadium shifts toward ticket revenue. This "revenue substitution" effect is amplified by two-way complementarity: higher tickets reduce attendance, limiting beer sales at the constrained (bad) margin.

### Attendance and Consumption Trade-offs

```{figure} ../charts/quantities.png
---
name: quantity-effects
alt: Attendance and beer consumption effects
---
**Left**: Attendance falls 38% at \\$7 ceiling due to higher ticket prices and complementarity. **Right**: Total beer consumption rises 28% despite lower attendance—per-fan consumption increases 108% at \\$7 ceiling.
```

**Key insight:** Price ceilings increase *aggregate* consumption even as they reduce attendance. The intensive margin (beers per fan) dominates the extensive margin (number of fans).

### Revenue Decomposition

```{figure} ../charts/revenue.png
---
name: revenue-decomp
alt: Revenue decomposition
---
Ticket revenue partially compensates for lost beer revenue, but total revenue falls. At \\$7 ceiling, revenue drops \\$600,000 per game (\\$49M annually for 81 home games).
```

**Implication for policy:** Price ceilings reduce stadium revenue by 18% at \$7 ceiling (\$600,000 per game). This creates incentive for stadiums to oppose such regulations or seek compensatory policies (e.g., subsidized tickets, reduced taxes).

### Welfare Analysis

```{figure} ../charts/welfare.png
---
name: welfare-quad
alt: Welfare components
---
**Top left**: Producer surplus (stadium profit) falls monotonically with tighter ceilings—most below \\$12 are binding.
**Top right**: Consumer surplus is ambiguous—cheaper beer helps, but higher tickets hurt. Net effect is negative below \\$8.
**Bottom left**: Externality costs rise with cheaper beer due to increased consumption.
**Bottom right**: Social welfare (CS + PS - externalities) declines with binding ceilings, reaching minimum around \\$7.
```

### Combined Welfare View

```{figure} ../charts/welfare_combined.png
---
name: welfare-combined
alt: Welfare decomposition on single chart
---
Lower beer ceilings reduce stadium profit by 25% at \\$7 ceiling (green line falls) while consumer surplus falls 19% (blue line). Externalities increase 28% (red line declines). Net social welfare falls 20% (purple line).
```

**Policy implication:** Price ceilings reduce welfare for both consumers (-19%) and producers (-25%), while externalities increase (+28%). Total social welfare falls 20%. This motivates alternative instruments like Pigouvian taxation.

### Per-Fan Consumption

```{figure} ../charts/beers_per_fan.png
---
name: beers-per-fan
alt: Beers per fan
---
Per-capita consumption explodes with lower price ceilings. At \\$7, average fan consumes 2.1 beers vs 1.0 at baseline—a 108% increase. This drives the externality cost increases.
```

## Quantitative Summary: \$7 Ceiling vs Baseline

| Metric | Baseline (\$12.50) | \$7 Ceiling | Change |
|--------|-------------------|-------------|---------|
| **Prices** |
| Beer price | \$12.50 | \$7.00 | -44% |
| Ticket price | \$89 | \$121 | +36% |
| **Quantities** |
| Attendance | 33,771 | 20,860 | -38% |
| Beers/fan | 1.0 | 2.1 | +108% |
| Total beers | 33,771 | 43,351 | +28% |
| **Revenue** |
| Total | \$3.40M | \$2.80M | -18% |
| Profit | \$2.27M | \$1.70M | -25% |
| **Welfare** |
| Consumer surplus | \$9.99M | \$8.14M | -19% |
| Externality cost | \$0.14M | \$0.17M | +28% |
| Social welfare | \$12.13M | \$9.66M | -20% |

## Comparison with Leisten (2025)

Our quantitative results confirm {cite}`leisten2025beer` theoretical prediction: **beer price ceilings cause ticket prices to rise**. We extend his analysis by:

1. **Magnitude**: \$7 ceiling → \$32 ticket increase (4.4x multiplier on price change)
2. **Two-way complementarity**: Beer prices affect attendance in our model
3. **Welfare decomposition**: Show who wins/loses and by how much
4. **Externalities**: Demonstrate that ceilings worsen public health outcomes

Both approaches reach the same qualitative conclusion through different mechanisms:
- **Leisten**: Complementarity discount term in FOC shrinks → ticket markup rises
- **Our model**: Beer margin collapses → stadium shifts to tickets → attendance falls (limiting beer sales at bad margin)

## Robustness

These results are robust to:
- **Cross-price elasticity**: Varying from 0.05 to 0.30 changes magnitudes but not directions
- **Demand sensitivities**: Monte Carlo over calibration parameters (see next section)
- **Externality costs**: Social welfare ranking persists across plausible cost ranges

The key insight—binding price ceilings reduce social welfare—holds throughout parameter space.

## Policy Implications

1. **Price ceilings are inefficient**: Create deadweight loss without clear beneficiaries
2. **Pigouvian taxation dominates**: Achieves same consumption reduction with revenue generation and no distortion of relative prices
3. **Stadium responses matter**: Complementarity amplifies unintended consequences
4. **Externalities worsen**: Lower prices increase consumption despite lower attendance

```{bibliography}
:filter: docname in docnames
```
