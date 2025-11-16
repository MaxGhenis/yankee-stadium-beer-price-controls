# Beer Price Controls at Yankee Stadium

## An Economic Analysis of Consumer Welfare, Revenue, and Externalities

This report analyzes the economic impacts of beer price controls at Yankee Stadium, examining:

- **Consumer welfare** from beer consumption and stadium experience
- **Stadium revenue** from tickets and concessions
- **Attendance effects** from price changes
- **Negative externalities** from alcohol consumption
- **Tax policy** and the Pigouvian gap

## Executive Summary

### Key Findings

1. **Current Pricing is Profit-Maximizing**
   - Observed consumer beer price: **$12.50**
   - Model-predicted optimal: **$12.85**
   - Stadiums internalize crowd management, brand, and experience costs

2. **Significant Tax Gap**
   - External costs: **$4.00/beer**
   - Current taxes: **$1.09/beer**
   - **Pigouvian tax gap: $2.91/beer** (73% undertaxed)

3. **Price Control Impacts**
   - **$7 price ceiling**: Would reduce stadium profit by $1.8M/season but increase consumer surplus
   - **$15 price floor**: Minimal impact (above optimal)
   - **Beer ban**: Reduces revenue by $2.0M/season, eliminates externalities

4. **Revenue Opportunity**
   - Optimal Pigouvian tax: +$2.91/beer
   - Potential revenue: **+$9.4M/season** (81 games × 40k beers × $2.91)

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
