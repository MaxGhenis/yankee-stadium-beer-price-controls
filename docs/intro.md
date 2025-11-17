# Introduction

## Motivation

Professional sports stadiums face a fundamental economic trade-off in alcohol pricing. Higher beer prices reduce consumption and associated negative externalities, including violence, public health costs, and drunk driving. However, beer sales represent a significant revenue stream for stadiums, with high profit margins that complement ticket revenue. This trade-off has motivated policy discussions about imposing price controls on stadium alcohol sales to address public health and safety concerns.

This paper analyzes the economic impacts of beer price controls at Yankee Stadium, one of the nation's most prominent sports venues. We examine:

effects on consumer welfare, stadium profit maximization across both ticket and beer revenue, attendance responses to price changes, and social externalities from alcohol consumption. We also evaluate current alcohol taxation relative to optimal Pigouvian benchmarks.

## Contribution

Our primary contribution is distinguishing between externalities that stadiums internalize through their profit maximization and those borne by society more broadly. We show that stadiums, as monopolists facing repeated interactions with customers, internalize negative effects that drunk fans impose on other attendees. These include increased security costs, reputational damage, and degradation of the stadium experience for other customers. We model these internalized costs as a convex function of total alcohol consumption, calibrated such that observed prices emerge as approximately profit-maximizing.

This distinction is economically important because only true social externalities that remain uninternalized by the stadium justify policy intervention beyond market outcomes. We estimate these remaining external costs at $4.00 per beer (comprising $2.50 for crime and violence and $1.50 for public health impacts), while current taxes total only $1.09 per beer, suggesting substantial under-taxation relative to the Pigouvian optimum.

## Main Findings

Our calibrated model yields several key results. First, we find that current pricing (average $80 tickets, $12.50 beer) is approximately profit-maximizing when accounting for taxes and internalized costs. The model predicts an optimal consumer beer price of $12.85, validating our calibration approach against observed market behavior.

Second, we identify a substantial Pigouvian tax gap. While external costs from alcohol consumption total approximately $4.00 per beer, current combined taxes amount to only $1.09 per beer, implying under-taxation of 73% relative to the social optimum. An additional tax of $2.91 per beer would fully internalize external costs while generating approximately $6.7 million in annual revenue for New York City.

Third, we analyze the general equilibrium effects of a binding beer price ceiling. A $7 ceiling (representing a 44% reduction from current prices) induces substantial adjustments in ticket pricing due to complementarity between the two goods. Specifically, the stadium's profit-maximizing response is to raise ticket prices by approximately $32 (36% increase). This occurs because the beer price ceiling compresses beer profit margins from $6.41 to $1.35 per unit (after accounting for taxes and marginal costs). The stadium optimally shifts toward ticket revenue, despite this causing a 38% decline in attendance. Importantly, per-capita beer consumption increases by 108%, leading to a 97% increase in external costs contrary to the presumed policy objective.

Fourth, we find that alternative policies dominate price ceilings on efficiency grounds. A Pigouvian tax of $2.91 per beer would internalize external costs, reduce consumption by 29%, and generate $6.7 million annually in tax revenue without creating deadweight loss from binding quantity constraints. This represents the first-best policy response to the externality problem.

### Model Innovation

This analysis treats **crowd management, brand damage, and experience degradation as internalized costs** that stadiums face from excessive alcohol consumption. These are externalities that drunk fans impose on OTHER customers, which the monopolist stadium internalizes because they affect future profits.

**Internalized (by stadium):**
- Crowd management & security
- Brand/reputation damage
- Experience degradation for other fans
- Capacity constraints

**External (borne by society):**
- Crime & violence in surrounding area
- Public health costs
- Drunk driving
- Non-attendee impacts

This distinction is crucial for policy analysis.

### Data & Methods

- **Literature-based elasticities**: Ticket demand -0.625, beer demand -0.965 (Noll 1974, Scully 1989, Krautmann & Berri 2007)
- **Current prices**: Industry data (2025)
- **Externality estimates**: Academic literature (Manning et al. 1991, Carpenter & Dobkin 2015)
- **Tax data**: Federal, NY State, NYC tax authorities
- **Stadium-specific demand**: Semi-log form with captive audience effects

### Structure of Report

1. **Background**: Literature review and empirical context
2. **Model**: Economic framework and assumptions
3. **Calibration**: Parameter estimation and validation
4. **Simulation**: Policy scenarios including $7 price ceiling
5. **Policy Analysis**: Welfare implications and recommendations
6. **Tax Analysis**: Current taxes vs optimal Pigouvian tax
7. **Conclusion**: Summary and policy recommendations

---

**Interactive exploration:** [Streamlit Web App](http://localhost:8501)

**Code repository:** [GitHub](https://github.com/maxghenis/yankee-stadium-beer-price-controls)
