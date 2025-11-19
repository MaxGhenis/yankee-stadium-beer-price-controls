# Data Sources & Limitations

## What We Have vs What We Don't

### ✅ ACTUAL DATA (Published)

**1. Beer Prices (2025)**
- Range: \$10-15 at Yankee Stadium (industry reports, fan reports)
- **Model baseline: \$12.50**
- Source: Team Marketing Report (TMR), StubHub, TripAdvisor reviews, fan reports
- **Interpretation:** Most likely this represents the **menu/sticker price (pre-sales-tax)**
  - When fans report "I paid \$12 for beer," they typically mean the posted menu price
  - With 8.875% NYC sales tax: **Consumer actually pays \$13.59**
  - Stadium receives: **\$12.37** after taxes (\$1.02 sales tax + \$0.07 excise)
  - **For our model:** We treat \$12.50 as the consumer-facing decision price
  - Demand responds to \$12.50 (the price consumers see and compare)
  - Revenue calculations properly account for tax wedge

**Tax Structure per Beer:**
| Item | Amount |
|------|--------|
| Menu price (what consumer sees) | \$12.50 |
| NYC sales tax (8.875%) | +\$1.11 |
| **Total consumer pays** | **\$13.61** |
| Less: Sales tax to government | -\$1.11 |
| Less: Federal excise tax (\$18/barrel) | -\$0.058 |
| Less: NY State excise (\$0.14/gal) | -\$0.012 |
| Less: NYC excise (\$0.12/gal) | -\$0.004 |
| **Stadium receives** | **\$12.43** |

- **Limitation:** Industry price reports rarely clarify whether prices are pre-tax or post-tax, leading to ambiguity across sources

**2. Ticket Prices**
- Average: ~\$80 (likely secondary market all-in price)
- Source: Secondary market data (StubHub, SeatGeek)
- **Note:** Secondary market prices typically include all fees and taxes

**3. Stadium Capacity**
- 46,537 seats
- Source: Official MLB data

**4. General Stadium Alcohol Consumption**
- ~40% of attendees drink
- Mean BAC: 0.057% among drinkers
- Source: Lenk et al. (2010) - survey of 100+ professional stadiums

**5. Demand Elasticities (OTHER contexts)**
- Ticket: -0.49 to -0.76 (MLB general, 1970s-1980s)
- Source: Noll (1974), Scully (1989)
- Beer: -0.79 to -1.14 (general alcohol market)
- Source: Various alcohol demand studies

**6. Externality Estimates**
- Crime: 10% alcohol ↑ → 1% assault ↑
- Source: Carpenter & Dobkin (2015) - regression discontinuity
- External costs: \$0.48-\$1.19/drink (1986 dollars)
- Source: Manning et al. (1991)

**7. Tax Rates**
- Federal excise: \$18/barrel
- NY State: \$0.14/gallon
- NYC: \$0.12/gallon
- Sales tax: 8.875%
- Source: TTB, NY Dept of Taxation

---

### ❌ WHAT WE DON'T HAVE (Proprietary/Unavailable)

**1. Actual Yankee Stadium Beer Sales**
- ❌ Total beers sold per game
- ❌ Sales by brand/type
- ❌ Revenue from beer vs tickets
- ❌ Profit margins

**Why:** Stadium concession data is PROPRIETARY (Legends Hospitality runs Yankees concessions)

**2. Yankee Stadium-Specific Elasticities**
- ❌ How Yankees fans specifically respond to price changes
- ❌ Attendance sensitivity to ticket prices
- ❌ Beer demand curve at Yankee Stadium

**Why:** Would require natural experiments or proprietary transaction data

**3. Internalized Cost Function**
- ❌ Actual cost of crowd management per beer
- ❌ Brand value impact from alcohol incidents
- ❌ Experience degradation quantification

**Why:** Internal operational data, not disclosed

---

## What's Calibrated vs Estimated

### CALIBRATED (To Match Observed Prices)

**1. Beer demand sensitivity: λ = 0.133**
- Chose semi-log functional form
- Calibrated so \$12.50 is profit-maximizing
- Based on: observed price + assumed costs

**2. Ticket demand sensitivity: λ = 0.017**
- Calibrated so \$80 is approximately optimal
- Assumption: Similar approach to beer

**3. Internalized cost parameter: α = 250**
- Calibrated to make observed prices optimal
- Reflects: crowd mgmt + brand + experience degradation
- NOT from direct cost data

**4. Baseline consumption: 1.0 beers/attendee**
- Based on Lenk et al. (2010) general stadium data
- Applied to Yankees: 40% × 2.5 = 1.0 average
- NO Yankees-specific validation

### ASSUMED (Reasonable Guesses)

**1. Beer cost: \$5**
- Assumption: Materials (\$2) + labor (\$2) + overhead (\$1)
- Not from Yankees financial data

**2. Ticket cost: \$20**
- Assumption: Operational costs per attendee
- Not from actual cost accounting

**3. Complementarity (cross-elasticity): 0.1**
- Assumption: 10% beer price ↑ → 1% attendance ↓
- Not empirically estimated for Yankees

**4. Captive demand share: 50%**
- Assumption: Half of fans drink regardless of price
- Not from survey data

---

## Validation Checks

What we CAN validate:

✅ **Observed prices near optimal** (\$12.50 vs \$12.85 model)
✅ **Consumption rates match literature** (1.0 beers/attendee)
✅ **Elasticities in reasonable range** (inelastic, as literature shows)
✅ **Tax calculations exact** (public tax code)
✅ **Externality estimates from peer-reviewed research**

What we CANNOT validate:

❌ Actual Yankees beer sales volumes
❌ Actual Yankees profit margins
❌ Actual response to hypothetical price controls
❌ Actual internalized costs

---

## Model Limitations

**1. No Yankee Stadium-Specific Data**
- Model uses general MLB/stadium parameters
- Yankees may differ (higher income fans, NYC context)

**2. Calibration Not Estimation**
- Parameters chosen to match observed prices
- Not econometrically estimated from data
- Circular: assume observed prices are optimal, calibrate to match

**3. Functional Form Assumptions**
- Semi-log demand is a choice, not empirically derived
- Quadratic internalized costs are assumption
- Could use linear, log-log, CES, etc.

**4. Cross-Sectional, Not Time-Series**
- No variation in Yankees prices to estimate elasticities
- Can't validate with Yankees-specific natural experiments

**5. Partial Equilibrium**
- Doesn't model competition from other entertainment
- Doesn't model substitution to pre-game drinking
- Single representative consumer

---

## What This Model IS Good For

✅ **Directional effects**: Sign and rough magnitude of policy impacts
✅ **Comparative analysis**: Relative effects across policies
✅ **Theoretical insights**: Internalized vs external costs distinction
✅ **Illustrative**: Shows economic tradeoffs clearly

## What This Model Is NOT

❌ **Empirical prediction**: Can't predict exact Yankees response
❌ **Causal estimate**: Not based on natural experiment
❌ **Structural econometrics**: Not estimated from micro data
❌ **Forecasting tool**: Too many assumptions for precise forecasts

---

## Ideal Data (If Available)

**Would dramatically improve model:**

1. **Transaction data**: Actual sales by game, price, brand
2. **Natural experiments**: Price changes, policy variations
3. **Panel data**: Multiple stadiums, multiple seasons
4. **Survey data**: Yankees fan preferences, willingness to pay
5. **Cost data**: Actual P&L for concessions

**None of this is publicly available.**

---

## Recommendation

Treat this as **illustrative economic analysis** showing:
- Theoretical framework for thinking about stadium pricing
- Rough orders of magnitude for policy effects
- Key economic mechanisms (complementarity, internalized costs, externalities)

For actual policy: Would need Yankees to share proprietary data or conduct empirical study with variation in prices/policies.
