# Introduction

## Motivation

In November 2024, Alexandria Ocasio-Cortez proposed capping beer prices at Yankee Stadium at $7-$8, citing fan affordability concerns. This proposal raises fundamental questions in public economics: How do price controls on complementary goods affect market outcomes when a monopolist controls both products? What are the welfare implications when consumers are heterogeneous?

This paper develops a heterogeneous consumer model to analyze beer price controls at sports venues. We make two key contributions:

1. **Heterogeneous consumers**: We model two distinct fan types—drinkers (40%) and non-drinkers (60%)—which allows us to capture selection effects that alter crowd composition under different policies.

2. **Internalized vs external costs**: We distinguish between costs that stadiums already internalize through their pricing decisions (crowd management, brand damage) and true social externalities (neighborhood crime, public health costs).

## Main Findings

Our calibrated model yields several key results:

**1. Consumption increases under price ceilings.** A $7 beer ceiling increases total consumption by 77% despite reducing attendance by 6%. This occurs because the stadium raises ticket prices ~10% to offset lost beer margin, and per-fan consumption more than doubles.

**2. Selection effects matter.** When ticket prices rise, non-drinkers reduce attendance by 11.5% while drinkers reduce attendance by only 6.3%. Drinkers gain value from cheaper beer, partially offsetting the ticket increase. This shifts crowd composition from 40% to 41.4% drinkers.

**3. The intensive margin dominates.** Decomposing the consumption increase: the intensive margin (each fan drinks more) contributes 116%, while the extensive margin (fewer attendees) contributes -16%.

**4. Results are robust.** Monte Carlo analysis over 1,000 parameter combinations confirms that tickets rise in >95% of scenarios, consumption increases in >95%, and stadium profit falls in >99%.

**5. The model validates against observed prices.** The heterogeneous model predicts an optimal beer price of $12.51, compared to $12.50 observed—a calibration error of 0.08%.

## Theoretical Framework

Our model builds on the sports economics literature examining joint ticket-concession pricing {cite}`krautmann2007concessions,coates2007ticket`. Standard models treat tickets and beer as independent products, but sophisticated stadium operators optimize jointly. Coates and Humphreys (2007) document that teams price tickets in the inelastic region of demand, sacrificing ticket revenue to drive concession sales.

We extend this framework in two ways:

**Heterogeneous consumers.** Following {cite}`lenk2010alcohol`, who document that approximately 40% of stadium attendees consume alcohol, we model two consumer types. This allows the model to capture selection effects: price policies change not only how many fans attend, but which types of fans attend.

**Internalized costs.** We model costs that stadiums internalize (security, experience degradation, brand damage) as a convex function of consumption. This explains why stadiums charge $12.50 for beer despite apparent profit potential at lower prices—drunk fans impose costs on other attendees that the stadium accounts for.

## Data and Calibration

In the absence of proprietary transaction data from Yankee Stadium, we calibrate our model using publicly available information and parameters from the academic literature:

- **Ticket demand elasticity**: -0.625 (midpoint of estimates from {cite}`noll1974attendance,scully1989business`)
- **Beer demand elasticity**: -0.965
- **Drinker share**: 40% (from {cite}`lenk2010alcohol`)
- **Current prices**: $80 tickets, $12.50 beer

Our semi-log demand specification provides flexibility while avoiding corner solutions. We calibrate price sensitivity parameters such that observed prices emerge as approximately profit-maximizing, which serves as external validation.

## Structure

The remainder of this paper proceeds as follows. The Background section reviews the literature on stadium pricing, alcohol demand, and externalities. The Model section presents our theoretical framework including heterogeneous consumers, the stadium's profit maximization problem, and the social welfare function. The Calibration section describes our strategy and validates against observed behavior. The Simulation Results section presents findings for the $7 ceiling and other policy scenarios. The Monte Carlo section quantifies parameter uncertainty. The Conclusion discusses implications and future research.

Interactive versions of our analysis, including a Streamlit application and Monte Carlo simulations, are available in the online appendix.
