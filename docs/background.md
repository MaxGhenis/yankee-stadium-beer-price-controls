# Background & Literature

## Current Pricing at Yankee Stadium (2025)

### Observed Prices
- **Beer**: \$10-15, average **\$12.50**
- **Tickets**: Average **\$80**
- **Stadium capacity**: 46,537

### Consumer Behavior
- **~40% of attendees** consume alcohol at games {cite}`lenk2010alcohol`
- Mean BAC among drinkers: **0.057%**
- Average consumption: **2.5 beers** among drinkers
- Overall average: **1.0 beers per attendee**

## Literature Review

### Demand Elasticities

**Ticket Demand (Inelastic)**

{cite}`noll1974attendance` found ticket demand elasticity of **-0.49** for MLB (1970-71 seasons), while {cite}`scully1989business` estimated **-0.63 to -0.76** for the 1984 season.

Teams consistently price in the **inelastic region** of ticket demand {cite}`fort2004inelastic`.

**Beer/Concessions Demand**

{cite}`krautmann2007concessions` found that:
- Beer demand is **relatively inelastic** in MLB
- Teams price tickets **below** revenue-maximizing level to drive concession sales
- Concessions are high-margin complements to tickets

General alcohol demand elasticities range from **-0.79 to -1.14**, but stadium demand is more inelastic due to:
- Captive audience (no alternatives during game)
- Experiential consumption (part of stadium ritual)
- Social pressure and peer effects

### Complementarity

{cite}`coates2007ticket` explain that tickets and concessions are **complementary goods**:
- Higher beer prices reduce attendance
- Lower ticket prices increase beer sales
- Teams jointly optimize across both revenue streams

This explains why teams price in the inelastic region of ticket demand - they're maximizing total profit, not just ticket revenue.

## Externalities from Stadium Alcohol Consumption

### Crime & Violence

{cite}`carpenter2015mlda` found:
- **10% increase in alcohol consumption → 1% increase in assault**
- **10% increase in alcohol consumption → 2.9% increase in rape**

{cite}`rees2009football` documented that college football games increase assault, vandalism, and disorderly conduct, with effects concentrated on game days and in the immediate vicinity.

Stadium alcohol cutoff policies (e.g., stopping sales after 7th inning) reduce post-game crime by allowing fans to sober up before leaving.

### Public Health Costs

{cite}`manning1991costs` estimated external costs of alcohol at **\$0.48-\$1.19 per drink** (1986 dollars), including:
- Traffic accidents
- Emergency room visits
- Long-term health impacts
- Fetal alcohol syndrome

Inflation-adjusted to 2025: **~\$1.50-\$3.00 per drink**.

{cite}`rehm2009global` provide global estimates of alcohol-related disease burden and economic costs.

### Total External Costs

Combining crime and health externalities:
- Crime: **\$2.50 per beer**
- Health: **\$1.50 per beer**
- **Total: \$4.00 per beer**

These are costs borne by **society**, not the stadium.

## Theoretical Foundation: Price Controls and Complementary Goods

### Leisten (2025): Rigorous Analysis of Beer Price Ceilings

{cite}`leisten2025beer` provides the theoretical foundation for analyzing beer price controls at stadiums through a rigorous monopoly model with complementary goods.

**His Model Setup:**
- Ticket demand: $q_x(p_x)$
- Beer demand: $q_y = q_x(p_x) \cdot q_y(p_y)$ (multiplicative form)
- **Key assumption**: Beer prices do NOT directly affect ticket demand (one-way complementarity: tickets → beer)
- Zero marginal costs (simplification)
- Log-concave demand functions

**First-Order Conditions (Unconstrained):**

For beer (standard monopoly markup):
$$p_y = -\frac{q_y(p_y)}{q_y'(p_y)}$$

For tickets (markup with complementarity discount):
$$p_x = -\frac{q_x(p_x)}{q_x'(p_x)} - p_y q_y(p_y)$$

The second term represents a "complementarity discount" - stadium lowers ticket prices because each attendee brings complementary beer revenue.

**With Beer Price Ceiling $Z$:**

When ceiling binds, the FOC for tickets becomes:
$$p_x = -\frac{q_x(p_x)}{q_x'(p_x)} - Z q_y(Z)$$

The complementarity discount shrinks as $Z$ falls, so $p_x$ must rise to restore the FOC.

**Key Result:**

Taking total derivatives with respect to ceiling $Z$:
$$\frac{dp_x}{dZ} = \frac{Zq_y'(Z) - q_y(Z)}{\frac{q_x(p_x)q_x''(p_x)}{q_x'(p_x)} - 2}$$

The sign depends on whether $2q_x'(p_x)^2 > q_x(p_x)q_x''(p_x)$.

**Under log-concavity** (his key assumption), this inequality holds, proving:

$$\frac{dp_x}{dZ} < 0$$

**Meaning: Lower beer ceilings cause ticket prices to rise.**

**Our Extension:**

We extend Leisten's framework by:
1. **Two-way complementarity**: Beer prices affect ticket demand in our model ($A(P_T, P_B)$)
2. **Realistic costs**: Marginal costs, taxes, internalized externalities
3. **Quantitative calibration**: Predicts magnitude (not just sign) of effects
4. **Welfare analysis**: Decompose impacts across consumers, producers, society

Both approaches reach the same qualitative conclusion but through different mechanisms:
- **Leisten**: Complementarity discount shrinks → tickets rise to restore markup
- **Our model**: Beer margin collapses → stadium shifts to tickets → attendance falls (limiting beer sales at bad margin)

## Why Stadiums Charge \$12.50

### Internalized Costs (Already in Stadium's Optimization)

Stadiums face costs from excessive alcohol consumption that affect their own profits:

1. **Crowd Management**: Security, cleanup, liability insurance
2. **Experience Degradation**: Drunk fans hurt experience for other customers → reduces repeat attendance
3. **Brand/Reputation**: "Cheap beer stadium" image → lowers long-run revenue
4. **Capacity Constraints**: Service bottlenecks, operational costs

These are **negative externalities on other customers** that the monopolist stadium internalizes.

Our model shows these internalized costs are **convex** (accelerating):
$$C_{internalized} = 250 \cdot \left(\frac{Q}{1000}\right)^2$$

At \$5 beer: Would sell 117k beers → internalized cost = **\$13.8M**
At \$12.50: Sells 40k beers → internalized cost = **\$1.6k**

Stadium chooses \$12.50 to maximize profit accounting for these costs.

### Distinction: Internalized vs External

```{list-table}
:header-rows: 1
:name: internalized-vs-external

* - Cost Type
  - Who Bears It
  - Internalized?
* - Crowd management
  - Stadium
  - ✅ Yes
* - Brand damage
  - Stadium (future revenue)
  - ✅ Yes
* - Experience degradation
  - Other customers → Stadium
  - ✅ Yes
* - Crime in neighborhood
  - Society
  - ❌ No
* - Public health
  - Society
  - ❌ No
* - Drunk driving
  - Society
  - ❌ No
```

Only the **external costs** (\$4.00/beer) justify policy intervention beyond what the stadium already does.

## Policy Context

### Current Alcohol Policies at Stadiums

{cite}`lenk2010policies` surveyed 100+ professional stadiums and found:
- Most stop alcohol sales after 7th inning
- Varying ID checking enforcement
- Few quantity limits per transaction
- No stadium-specific price controls

### Proposed Policies

Various jurisdictions have considered:
- Price floors (minimum prices)
- Price ceilings (maximum prices)
- Purchase limits (beers per transaction)
- Earlier sale cutoffs
- Complete alcohol bans

Our analysis evaluates these policies using welfare economics framework.

```{bibliography}
:filter: docname in docnames
```
