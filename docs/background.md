# Background & Literature

## Current Pricing at Yankee Stadium (2025)

### Observed Prices
- **Beer**: \$10-15, average **\$12.50**
- **Tickets**: Average **\$80**
- **Stadium capacity**: 46,537

### Consumer Behavior
- **~40% of attendees** consume alcohol at games {cite}`wolfe1998baseball`
- Wolfe et al. (1998) found 41% of male spectators tested positive for alcohol at MLB games
- Average consumption: **2.5 beers** among drinkers
- Overall average: **1.0 beers per attendee**

### Institutional Context: Legends Hospitality

Yankee Stadium concessions are operated by **Legends Hospitality**, a joint venture originally founded by the New York Yankees and Dallas Cowboys in 2008. Legends manages food and beverage operations for over 200 venues globally, including major sports facilities, convention centers, and entertainment venues.

**Key implications for modeling:**

1. **Sophisticated pricing**: Legends employs advanced analytics and dynamic pricing strategies, consistent with our assumption that observed prices reflect profit-maximization.

2. **Revenue sharing**: The relationship between venue ownership and concession operations means the stadium already captures most of the joint surplus from tickets and beer. Price controls would directly affect this integrated profit stream.

3. **Operational capacity**: Large-scale operators like Legends can adjust staffing, inventory, and vendor deployment in response to policy changes, supporting our assumption that supply-side adjustments are feasible.

4. **Brand considerations**: Premium hospitality operators internalize brand reputation costs from alcohol-related incidents, which we model as internalized externalities distinct from true social costs.

This institutional structure supports our theoretical assumption that the stadium operator maximizes joint profits across tickets and concessions, rather than treating them as independent revenue streams.

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

**Stadium-specific evidence:**

{cite}`klick2021seventh` provides the most directly relevant evidence using MLB data from Philadelphia (2006-2015). They exploit the natural experiment that baseball games vary in length while alcohol sales stop after the 7th inning. Key finding: **extra innings significantly reduce stadium-area crime**, especially assaults, by giving fans more time to sober up before departure.

{cite}`montolio2019hooligans` studied FC Barcelona home games and found elevated thefts within a **700-meter radius** of the stadium on game days. Away matches showed no effect, confirming the stadium as the crime generator.

{cite}`glassman2018alcohol` documented a natural experiment at a college football stadium: **330 crime incidents/year** without alcohol sales (2009-2011) vs **475 with alcohol** (2012-2013)—a 44% increase.

Stadium alcohol cutoff policies (e.g., stopping sales after 7th inning) reduce post-game crime by allowing fans to sober up before leaving.

### Public Health Costs

{cite}`manning1991costs` estimated external costs of alcohol at **\$0.48-\$1.19 per drink** (1986 dollars), including:
- Traffic accidents
- Emergency room visits
- Long-term health impacts
- Fetal alcohol syndrome

Inflation-adjusted to 2025: **~\$1.50-\$3.00 per drink**.

{cite}`rehm2009global` provide global estimates of alcohol-related disease burden and economic costs.

### Deriving External Cost Estimates

**Crime externality (\$2.50/beer):**

The crime cost estimate combines three components:
1. **Base crime risk**: From {cite}`carpenter2015mlda`, a 10% consumption increase → 1% assault increase. With stadium consumption averaging ~40,000 beers/game and approximately 2-3 stadium-related assaults per game, this implies ~\$1,000-2,000 in crime costs per marginal beer cluster.
2. **Police/security costs**: NYC allocates significant police presence for games; marginal policing costs attributable to alcohol-fueled incidents add ~\$0.50-1.00/beer.
3. **Property crime**: {cite}`montolio2019hooligans` found elevated thefts within 700m of stadiums; applying their estimates to NYC suggests ~\$0.50/beer.

Combining these yields our \$2.50/beer point estimate, with a plausible range of \$1.50-\$3.50.

**Health externality (\$1.50/beer):**

{cite}`manning1991costs` estimated external health costs at \$0.48-\$1.19/drink in 1986 dollars. Applying the CPI-Medical Care index (approximately 3× since 1986) yields \$1.44-\$3.57/drink in 2024 dollars. We use the midpoint (\$2.50) adjusted downward to \$1.50 because:
- Stadium consumption is episodic, not chronic (lower liver disease risk)
- Most fans use public transit (lower DUI externality)
- Stadium environment provides some harm reduction (security, cutoffs)

**Total: \$4.00/beer** (with Monte Carlo range \$2.50-\$5.50)

These are costs borne by **society**, not the stadium.

#### Stadium-Specific Adjustments

Our \$4.00/beer estimate may be conservative or generous depending on stadium-specific factors:

**Factors suggesting HIGHER externalities:**
- **Concentrated timing**: 40,000+ fans leaving at once creates peak-load problems for police, transit
- **Geographic concentration**: Bronx neighborhood bears costs of 81 home games
- **Driving risk**: Some fans drive home (vs. bar patrons who may cab/walk)
- **Group dynamics**: Stadium crowds may amplify aggressive behavior

**Factors suggesting LOWER externalities:**
- **Controlled environment**: Security, sales cutoffs, ID checks reduce worst outcomes
- **Public transit access**: Most fans use subway (4 train), reducing DUI
- **7th inning cutoff**: Allows sobering before departure
- **Premium pricing**: \$12.50/beer naturally limits consumption

**Uncertainty range:**
- **Conservative**: \$2.50/beer (stadium safety measures effective)
- **Baseline**: \$4.00/beer (used in model)
- **High**: \$6.00/beer (neighborhood bears concentrated costs)

This uncertainty is incorporated in our Monte Carlo analysis, which samples crime costs from \$1.50-\$3.50 and health costs from \$1.00-\$2.00.

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
