# Executive Summary

## Beer Price Controls at Yankee Stadium: Economic Analysis

### Research Question

What are the economic impacts of imposing price controls on beer at Yankee Stadium?

This analysis examines effects on:
- Stadium revenue and profit
- Consumer welfare
- Attendance
- Alcohol consumption
- Social externalities (crime, health costs)
- Optimal tax policy

---

## Key Findings

### 1. Current Prices Are Profit-Maximizing (With Internalized Costs)

**Observed**: \$80 tickets, \$12.50 beer
**Model optimal**: \$89 tickets, \$12.85 beer

Stadiums internalize negative externalities drunk fans impose on OTHER customers:
- Crowd management costs
- Brand/reputation damage
- Experience degradation
- Capacity constraints

**Internalized cost function** (convex): $C = 250 \\cdot (Q/1000)^2\$

At \$5 beer: \$13.8M internalized costs (!)
At \$12.50 beer: \$1,563 internalized costs

This explains why stadiums don't sell cheap beer despite apparent profit potential.

### 2. Significant Pigouvian Tax Gap

**External costs** (crime + health): **\$4.00/beer**
**Current taxes**: **\$1.09/beer**
**Gap**: **\$2.91/beer** (73% undertaxed)

**Revenue opportunity**: **+\$9.4M/season** from optimal Pigouvian tax

### 3. \$7 Beer Ceiling: Mixed Effects

| Impact | Change |
|--------|--------|
| **Ticket prices** | **+\$32 (+36%)** |
| **Attendance** | -38% |
| **Beer consumption** | +108% (per fan) |
| **Stadium profit/game** | -\$575k (-25%) |
| **Stadium profit/season** | **-\$46.6M** |
| **Consumer surplus** | Complex (cheaper beer, expensive tickets) |
| **External costs** | +97% (more alcohol) |

**Ticket price rise** is optimal response:
- Beer margin collapses (stadium receives \$11.41 → \$6.35)
- Shift toward ticket revenue (unconstrained)
- Reduces attendance and limits beer sales at bad margin

### 4. Welfare Redistribution

**Current equilibrium** (\$12.50 beer):
- Consumer surplus: ~\$22M/game
- Producer surplus: ~\$2.3M/game
- External costs: ~\$160k/game
- **Social welfare**: ~\$24M/game

**With \$7 ceiling**:
- Consumer surplus: Rises (cheaper beer) but offset by higher tickets
- Producer surplus: **Falls** \$575k/game
- External costs: **Rise** +\$153k (more consumption)
- Net social welfare: Depends on weights

**Distributional concern**: Benefits may not accrue to those bearing external costs

### 5. Policy Recommendations

**Ranked by economic efficiency:**

1. **Pigouvian Tax** (+\$2.91/beer) - MOST EFFICIENT ✓
   - Internalizes external costs
   - Raises \$11.0M/season for affected communities
   - Reduces consumption optimally
   - No deadweight loss

2. **Price Floor** (\$15-16) - SECOND BEST
   - Reduces consumption and externalities
   - No government revenue
   - Stadium keeps higher margin

3. **Hybrid Policy** - POLITICALLY FEASIBLE
   - Moderate tax (+\$1.50/beer)
   - Earlier cutoff (6th inning)
   - 2-beer purchase limit

4. **Price Ceiling** (\$7) - NOT RECOMMENDED ❌
   - Large stadium revenue loss (-\$47M/season)
   - Increases externalities (+97%)
   - Tickets rise 36% (unintended consequence)
   - Constitutional concerns

5. **Beer Ban** - EXTREME
   - Eliminates externalities
   - Revenue loss: -\$2M/game
   - May shift to pre-game drinking (not modeled)

---

## Methodological Innovations

### 1. Internalized vs External Costs

**Key insight**: Monopolist stadiums internalize negative effects on their own customers.

**Internalized** (already in \$12.50 price):
- Experience degradation
- Crowd management
- Brand damage

**External** (borne by society):
- Crime in neighborhood
- Public health costs
- Drunk driving

Only **external costs** justify policy intervention.

### 2. Tax-Aware Model

Consumer pays: \$12.50
Less taxes: -\$1.09
Stadium receives: **\$11.41**

Model accounts for:
- Sales tax (8.875%)
- Excise tax (\$0.074)
- Stadium optimization over after-tax revenue

### 3. Complementarity Framework

Tickets and beer consumed together:
- Cross-elasticity: 0.1 (calibrated from theory)
- 10% beer price ↑ → 1% attendance ↓
- Drives ticket price response to beer controls

---

## Model Limitations

**Strengths:**
- ✅ Literature-based elasticities
- ✅ Tax-aware revenue calculations
- ✅ Internalized vs external cost distinction
- ✅ Theoretically grounded complementarity

**Limitations:**
- ❌ No Yankees-specific sales data (proprietary)
- ❌ Cross-elasticity assumed (not estimated)
- ❌ Static (no dynamic/long-run effects)
- ❌ Representative consumer (no heterogeneity)
- ❌ Partial equilibrium (no competition)

**Use for**: Directional effects, mechanisms, order of magnitude
**Not for**: Precise point predictions

**Uncertainty quantified**: Monte Carlo over 1,000 parameter combinations

---

## Bottom Line

### For Policymakers

**If goal is reduce alcohol consumption:**
→ Pigouvian tax (+\$2.91/beer) is most efficient

**If goal is protect consumers:**
→ Beware unintended consequences (tickets rise 36%)

**If goal is raise revenue:**
→ Tax generates \$11.0M/season for NYC

### For Stadium

**Price ceiling** causes:
- Massive profit loss (-\$47M/season)
- Optimal response: Raise tickets 36%
- Both revenue sources still fall

### For Society

**Trade-off**:
- Consumer surplus: Ambiguous (cheaper beer vs pricier tickets)
- Producer surplus: Large loss
- External costs: Increase 97%

**Net**: Depends on how you weight stadium profit vs consumer surplus vs externalities

---

## Data & Methods

**Literature**:
- 30+ academic papers
- Noll (1974), Scully (1989): Ticket elasticities
- Lenk et al. (2010): Consumption data
- Carpenter & Dobkin (2015): Crime externalities
- Deaton & Muellbauer (1980): Demand system framework

**Model**:
- Semi-log demand (calibrated)
- Convex internalized costs
- Tax-aware optimization
- Complementarity (cross-elasticity 0.1)

**Validation**:
- Observed prices ≈ optimal (\$80/\$12.50 vs \$89/\$12.85)
- Yankees attendance: 40,803/game (model: 39,556)
- Consumption: 1.0 beers/attendee (matches literature)

**Code**:
- Python package (uv)
- 63 tests, 98% coverage
- Monte Carlo uncertainty quantification
- Interactive Streamlit app
- JupyterBook report

---

**Full analysis**: [JupyterBook Report](https://maxghenis.github.io/yankee-stadium-beer-price-controls)
**Interactive tool**: [Streamlit App](http://localhost:8501)
**Code**: [GitHub Repository](https://github.com/maxghenis/yankee-stadium-beer-price-controls)
