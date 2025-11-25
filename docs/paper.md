---
title: "Beer Price Controls at Yankee Stadium: An Economic Analysis"
subtitle: "Selection Effects and Unintended Consequences in Stadium Alcohol Regulation"
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

This paper analyzes the economic impacts of imposing price controls on beer sales at Yankee Stadium using a **heterogeneous consumer model** with two distinct fan types: non-drinkers (60%) and drinkers (40%). Our approach, calibrated to match empirical consumption patterns, achieves superior predictive accuracy compared to representative consumer specifications, reducing calibration error by 76%.

We simulate the effects of a \$7 beer price ceiling and document significant unintended consequences operating through complementarity and **selection effects**. Monte Carlo analysis across 1,000 parameter combinations confirms these findings are robust: tickets rise in >95% of scenarios, stadium profit falls in >99%, and beer consumption increases in >95%. Point estimates suggest the ceiling induces the stadium to raise ticket prices by 5-15% (depending on cross-price elasticity assumptions), causing attendance to fall 3-8%. Total beer consumption increases substantially as per-fan consumption rises (from 1.00 to approximately 2.0 beers/fan), offsetting the attendance decline. Stadium profit falls \$15-30M per season. The heterogeneous model reveals that drinkers respond less elastically to ticket price increases than non-drinkers, leading to selection effects that alter crowd composition.

Our analysis introduces two methodological innovations. First, we distinguish between costs that stadiums internalize (crowd management, brand damage, experience degradation affecting other customers) and true social externalities (neighborhood crime, public health costs). Second, we model heterogeneous consumer preferences, which not only improves calibration but reveals that price policies induce selection effects altering crowd composition. The heterogeneous model predicts an optimal beer price of \$12.51 compared to the observed \$12.50, validating that stadiums approximately profit-maximize while accounting for fan heterogeneity.

The consumption increase operates through two channels: an **intensive margin** (each drinker consumes more at lower prices) and an **extensive margin** (crowd composition shifts toward drinkers as ticket prices rise). We decompose these effects and show that selection effects account for a substantial portion of the total consumption change—a mechanism absent from representative agent models.

This is a simulation study using calibrated parameters rather than estimated ones; we lack Yankees-specific transaction data. However, the heterogeneous consumer framework provides more realistic predictions than representative consumer models and generates novel, testable insights about selection effects in stadium alcohol regulation. We provide extensive Monte Carlo robustness checks demonstrating that qualitative conclusions hold across wide parameter ranges.

**JEL Codes**: H23 (Externalities), L83 (Sports), D62 (Externalities)

**Keywords**: price controls, sports economics, alcohol externalities, complementary goods, stadium pricing, selection effects, heterogeneous consumers

# Introduction

In November 2024, Alexandria Ocasio-Cortez proposed capping beer prices at Yankee Stadium at \$7-\$8, citing fan affordability concerns. This proposal raises fundamental questions in public economics: How do price controls on complementary goods affect market outcomes when a monopolist controls both products? What are the welfare implications when consumers are heterogeneous?

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

$$\pi = A(P_T, P_B) \cdot [(P_T - c_T) + Q(P_B) \cdot (P_B^{net} - c_B)] - C_{int}(Q_{total})$$

where $P_B^{net}$ is beer price net of taxes, $c_T$ and $c_B$ are marginal costs, and $C_{int}$ captures internalized costs (crowd management, brand damage).

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

| Outcome | Baseline | \$7 Ceiling | Change |
|---------|----------|-------------|--------|
| Ticket price | \$70.44 | \$77.29 | +9.7% |
| Beer price | \$12.50 | \$7.00 | -44.0% |
| Attendance | 39,559 | 37,296 | -5.7% |
| Beers/fan | 1.00 | 2.10 | +110% |
| Total beers | 39,559 | 78,322 | +98% |
| Stadium profit | \$1.82M | \$1.51M | -17.0% |

## Decomposition: Intensive vs. Extensive Margin

The consumption increase decomposes into:

- **Intensive margin**: Each attendee drinks more at lower prices
- **Extensive margin**: Crowd composition shifts toward drinkers

Both margins contribute positively to consumption growth, but the intensive margin dominates.

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

# Conclusion

This paper analyzes beer price controls at Yankee Stadium using a heterogeneous consumer model. Our main findings are:

1. **Price ceilings backfire**: A \$7 beer ceiling causes ticket prices to rise and total consumption to nearly double.

2. **Selection effects matter**: Crowd composition shifts toward drinkers, amplifying consumption increases.

3. **Results are robust**: Directional effects hold across wide parameter ranges.

4. **Stadiums internalize costs**: Much of the alcohol-related costs (crowd management, brand damage) are already reflected in stadium pricing.

The heterogeneous consumer framework represents an advance over representative agent models for analyzing policies with distributional consequences. Future work could extend this approach to other complementary goods settings.

# References

- Coates, D., & Humphreys, B. R. (2007). Ticket prices, concessions and attendance at professional sporting events. *International Journal of Sport Finance*, 2(3), 161-170.
- Krautmann, A. C., & Berri, D. J. (2007). Can we find it at the concessions? Understanding price elasticity in professional sports. *Journal of Sports Economics*, 8(2), 183-191.
- Leisten, M. (2025). Economic analysis of beer price controls at Yankee Stadium. Twitter/X thread.
- Lenk, K. M., Toomey, T. L., & Erickson, D. J. (2010). Alcohol control policies and practices at professional sports stadiums. *Public Health Reports*, 125(5), 665-673.
- Luca, M., & Sood, N. (2018). Sobering up after the seventh inning: Alcohol and crime around the ballpark. *Journal of Policy Analysis and Management*.
