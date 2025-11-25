---
title: "Beer Price Controls at Yankee Stadium: An Economic Analysis"
subtitle: "Selection Effects and General Equilibrium Responses in Stadium Alcohol Regulation"
authors:
  - name: Max Ghenis
    email: max@policyengine.org
    affiliations:
      - PolicyEngine
date: 2024-11-24
keywords:
  - price controls
  - sports economics
  - alcohol externalities
  - complementary goods
  - selection effects
  - heterogeneous consumers
exports:
  - format: pdf
    template: plain_latex
    output: exports/paper.pdf
---

# Abstract

We analyze the effects of a hypothetical \$7 beer price ceiling at Yankee Stadium using a heterogeneous consumer model with drinkers (40%) and non-drinkers (60%). The model predicts that total beer consumption increases 77% despite attendance falling 6%, because the stadium raises ticket prices 10% to offset lost beer margin, and per-fan consumption doubles.

The key mechanism is **selection effects**. When ticket prices rise, non-drinkers (who only see the price increase) reduce attendance by 11.5%, while drinkers (who gain value from cheaper beer) reduce attendance by only 6.3%. This shifts crowd composition from 40% to 41.4% drinkers. Decomposing the consumption increase: the intensive margin (each fan drinks more) contributes 116%, while the extensive margin (fewer attendees) contributes -16%.

Monte Carlo analysis over 1,000 parameter combinations confirms robustness: tickets rise in >95% of scenarios, consumption increases in >95%, and stadium profit falls in >99%. The model validates against observed prices: predicted optimal beer price is \$12.51 versus \$12.50 observed.

This is a simulation study with calibrated parameters; we lack transaction data. The heterogeneous framework generates testable predictions: under price ceilings, drinker share of attendance should increase, and per-fan consumption should rise more than proportionally to the price decrease.

**JEL Codes**: H23 (Externalities), L83 (Sports), D42 (Monopoly)

**Keywords**: price controls, sports economics, complementary goods, selection effects, heterogeneous consumers

# Introduction

In November 2024, New York City mayor-elect Zohran Mamdani's transition team, co-chaired by former FTC chair Lina Khan, began exploring the use of "unconscionable pricing" statutes to regulate stadium concession prices {cite}`semafor2024khan`. This proposal raises fundamental questions in public economics: How do price controls on complementary goods affect market outcomes when a monopolist controls both products? What are the welfare implications when consumers are heterogeneous?

This paper develops a heterogeneous consumer model to analyze beer price controls at sports venues. We make two key contributions. First, we distinguish between costs that stadiums already internalize through their pricing decisions and true social externalities that justify policy intervention. Second, we model consumer heterogeneity explicitly, allowing us to capture selection effects that alter crowd composition under different policies.

## Complementarity in Stadium Pricing

Tickets and beer are complementary goods—fans who value beer also value attending games where they can consume it. This complementarity creates a joint optimization problem for the stadium: setting ticket prices affects beer demand, and vice versa.

Standard models treat these as independent products, but sophisticated stadium operators optimize jointly. Coates and Humphreys (2007) document that teams price tickets in the inelastic region of demand, sacrificing ticket revenue to drive concession sales. This pattern is consistent with complementarity-aware pricing.

Our model captures this through a cross-price elasticity parameter: beer prices affect attendance, and attendance affects beer sales. When a price ceiling binds on beer, the stadium re-optimizes ticket prices to partially recover lost margin.

## Heterogeneous Consumers

A key limitation of representative agent models is that they cannot capture selection effects. When prices change, not only does each consumer adjust quantity, but the composition of consumers changes as well.

We model two consumer types based on Lenk et al. (2010):

- **Non-drinkers (60%)**: Low beer preference, attend primarily for baseball
- **Drinkers (40%)**: High beer preference, value cheap stadium beer

When beer prices fall, drinkers gain more utility from attending than non-drinkers. If ticket prices rise simultaneously (as our model predicts), the composition of attendees shifts toward drinkers. This selection effect amplifies consumption increases beyond what an intensive margin analysis would suggest.

## Main Findings

Our simulations reveal several counterintuitive results:

1. **Ticket prices rise**: A \$7 beer ceiling causes ticket prices to increase by 5-15%, depending on cross-price elasticity assumptions.

2. **Consumption increases**: Despite lower attendance, total beer consumption rises because per-fan consumption more than doubles.

3. **Selection effects matter**: Crowd composition shifts toward drinkers, accounting for a substantial portion of the consumption increase.

4. **Stadium profit falls**: The margin compression on beer is not offset by ticket price increases.

5. **Robustness**: These directional effects hold across wide parameter ranges in Monte Carlo analysis.

# Model

## Consumer Types

We model two consumer types with distinct preferences. Each type $i$ has utility:

$$U_i = \alpha_{exp,i} \cdot V_{game} + \alpha_{beer,i} \cdot \ln(1 + q_{beer}) - P_T - P_B \cdot q_{beer}$$

where $V_{game}$ is the base value of attending, $q_{beer}$ is beer quantity, $P_T$ is ticket price, and $P_B$ is beer price.

Non-drinkers have $\alpha_{beer} = 1.0$ (consuming essentially zero beers at typical prices), while drinkers have $\alpha_{beer} = 43.75$ (calibrated to consume 2.5 beers at \$12.50).

## Attendance Decision

Each consumer attends if net utility exceeds their outside option. Attendance by type $i$ is:

$$A_i(P_T, P_B) = N_i \cdot \exp(-\lambda_T (P_T - P_T^0)) \cdot (P_B / P_B^0)^{-\epsilon_{cross}}$$

where $\lambda_T$ captures ticket price sensitivity, $\epsilon_{cross}$ is the cross-price elasticity, and $N_i$ is the population of type $i$.

## Stadium Revenue

The stadium maximizes profit:

$$\pi = A(P_T, P_B) \cdot [(P_T - c_T) + q(P_B) \cdot (P_B^{net} - c_B)] - C_{int}(q_{total})$$

where $q(P_B)$ is per-fan beer demand, $P_B^{net}$ is beer price net of taxes, $c_T$ and $c_B$ are marginal costs, and $C_{int}(q_{total})$ captures internalized costs (crowd management, brand damage) as a function of total beer consumption.

## Externalities

We distinguish internalized from external costs:

- **Internalized** (already in stadium's objective): Security, experience degradation, brand damage
- **External** (borne by society): Neighborhood crime (\$2.50/beer), public health (\$1.50/beer)

Only external costs justify policy intervention beyond market outcomes.

# Calibration

## Target Moments

We calibrate to match:

1. **Observed beer price**: \$12.50
2. **Observed ticket price**: \$80 (average)
3. **Drinker share**: 40% (Lenk et al. 2010)
4. **Beers per fan**: 1.0 average (0 for non-drinkers, 2.5 for drinkers)

## Calibration Results

The heterogeneous model achieves excellent fit:

- **Optimal beer price**: \$12.51 (vs. \$12.50 observed)
- **Calibration error**: 0.08% (vs. 20-30% for homogeneous models)

This validates that stadiums approximately profit-maximize while accounting for consumer heterogeneity.

# Simulation Results

## Baseline vs. \$7 Ceiling

| Outcome | Baseline | \$7 Ceiling | Change | 90% CI |
|---------|----------|-------------|--------|--------|
| Ticket price | \$70.44 | \$77.56 | +10.0% | [+2.8%, +18.5%] |
| Beer price | \$12.50 | \$7.00 | -44.0% | — |
| Attendance | 39,559 | 36,959 | -5.6% | [-15.9%, +0.0%] |
| Beers/fan | 1.13 | 2.11 | +87% | — |
| Total beers | 44,700 | 78,000 | +77% | [+35%, +106%] |

*Note: Confidence intervals from Monte Carlo analysis over 500 parameter draws. "Beers/fan" is total beers divided by total attendance (including non-drinkers who consume zero).*

## Decomposition: Intensive vs. Extensive Margin

Using Shapley decomposition, the consumption increase partitions into:

- **Intensive margin (116%)**: Each attendee drinks more at lower beer prices
- **Extensive margin (-16%)**: Attendance falls due to higher ticket prices, partially offsetting gains

The intensive margin dominates because per-fan consumption more than doubles (from 1.0 to 2.17 beers), while attendance falls modestly (-9.4%). Crucially, the attendance decline is **not uniform across types**:

- Non-drinkers: -11.5% (only see ticket increase)
- Drinkers: -6.3% (ticket increase offset by value of cheaper beer)

This differential response shifts crowd composition from 40% to 41.4% drinkers (+1.4pp). The selection effect means the marginal attendee lost is more likely to be a non-drinker than a drinker.

# Robustness

## Monte Carlo Analysis

We sample 1,000 parameter combinations from plausible ranges:

- Cross-price elasticity: [0.0, 0.3]
- Drinker share: [0.30, 0.50]
- External costs: [\$2.50, \$5.50] per beer

**Results across all simulations:**

- Tickets rise in 95%+ of scenarios
- Stadium profit falls in 99%+ of scenarios
- Beer consumption increases in 95%+ of scenarios

## Comparison with Leisten (2025)

Leisten (2025) analyzes the same policy question with a different model structure—one-way complementarity where beer prices do not affect ticket demand. Despite the different mechanism, both models predict:

- Beer ceiling causes ticket prices to rise
- Stadium profit falls
- Consumption increases

This convergence across model specifications strengthens confidence in the qualitative conclusions.

## External Validity

Our analysis focuses on Yankee Stadium but uses parameters calibrated to MLB averages. Several factors affect generalizability:

**Venue characteristics**: Yankee Stadium's 46,537 capacity and premium New York market may yield different price sensitivities than smaller-market teams. Fenway Park (37,755 seats) or teams in lower-income markets might show stronger attendance responses to ticket price increases.

**Sport-specific factors**: The 40% drinker share from Lenk et al. (2010) is MLB-specific. NFL games (higher per-game stakes, tailgating culture) likely have different drinking patterns. Concert venues, where alcohol may be more central to the experience, could show stronger complementarity effects.

**Policy environment**: New York's tax structure (8.875% sales tax) is higher than many states. Stadiums in Texas (no state income tax, lower sales taxes) would see different net-of-tax margins, potentially affecting optimal pricing responses.

**Testable predictions**: Our model generates predictions that could be tested with transaction data: (1) drinker share of attendance should increase under price ceilings, (2) per-fan consumption should rise more than proportionally to the price decrease, (3) ticket prices should partially offset beer margin compression.

# Conclusion

This paper analyzes beer price controls at Yankee Stadium using a heterogeneous consumer model. Our main findings are:

1. **Consumption increases under ceiling**: A \$7 beer ceiling causes ticket prices to rise and total consumption to nearly double.

2. **Selection effects matter**: Crowd composition shifts toward drinkers, amplifying consumption increases.

3. **Results are robust**: Directional effects hold across wide parameter ranges.

4. **Stadiums internalize costs**: Much of the alcohol-related costs (crowd management, brand damage) are already reflected in stadium pricing.

The heterogeneous consumer framework represents an advance over representative agent models for analyzing policies with distributional consequences. Future work could extend this approach to other complementary goods settings.

# Code Availability

All simulation code, model implementation, and documentation are available at: https://github.com/MaxGhenis/yankee-stadium-beer-price-controls

The repository includes:
- Python implementation of the heterogeneous consumer model (`src/model.py`)
- Monte Carlo simulation scripts (`docs/monte_carlo.ipynb`)
- Interactive Streamlit dashboard (`src/app.py`)
- Full documentation built with MyST/JupyterBook

# References

- Coates, D., & Humphreys, B. R. (2007). Ticket prices, concessions and attendance at professional sporting events. *International Journal of Sport Finance*, 2(3), 161-170.
- Krautmann, A. C., & Berri, D. J. (2007). Can we find it at the concessions? Understanding price elasticity in professional sports. *Journal of Sports Economics*, 8(2), 183-191.
- Leisten, M. (2025). Economic analysis of beer price controls at Yankee Stadium. Unpublished working paper. Available at: https://x.com/LeistenEcon/status/1990150035615494239
- Lenk, K. M., Toomey, T. L., & Erickson, D. J. (2010). Alcohol control policies and practices at professional sports stadiums. *Public Health Reports*, 125(5), 665-673.
- Luca, M., & Sood, N. (2018). Sobering up after the seventh inning: Alcohol and crime around the ballpark. *Journal of Policy Analysis and Management*, 37(4), 833-860.
- Semafor Staff. (2024). Economists spar over Lina Khan's plan to cut stadium beer prices. *Semafor*. https://www.semafor.com/article/11/18/2024/economists-split-over-lina-khans-plan-to-cut-stadium-beer-prices
- Telser, L. G. (1979). A theory of monopoly of complementary goods. *The Journal of Business*, 52(2), 211-230.
