# Policy Analysis

## Price Control Implementation Details

**Important Clarification:** Throughout this analysis, price controls apply to the **menu/sticker price (pre-sales-tax)**, consistent with:
- **Real-world precedent:** Scotland's Minimum Unit Pricing applies pre-VAT; US historical price controls were pre-tax
- **Enforcement practicality:** Regulators monitor posted menu prices, not checkout totals
- **Legal structure:** Sales tax is applied at point of sale, after base price is determined

**Example: \$7 Beer Price Ceiling**

| Component | Amount |
|-----------|--------|
| Maximum menu price | **\$7.00** ← *Price control applies here* |
| + NYC sales tax (8.875%) | +\$0.61 |
| = **Consumer pays** | **\$7.61** |
| - Sales tax to government | -\$0.61 |
| - Excise taxes | -\$0.074 |
| = **Stadium receives** | **\$6.85** |

**Implication:** When we analyze a "\$7 ceiling," the stadium receives only **\$6.85** after taxes, creating an even tighter constraint than the headline \$7 suggests.

This convention matches international minimum alcohol pricing (Scotland, Wales) and US retail price regulation precedent.

## Price Controls

### Price Ceiling: \$7

A **\$7 price ceiling** would be a binding constraint (below optimal \$12.85).

**Effects:**

| Metric | Current (\$12.50) | With \$7 Ceiling | Change |
|--------|------------------|-----------------|--------|
| Consumer beer price | \$12.50 | \$7.00 | -\$5.50 (-44%) |
| Stadium receives | \$11.41 | \$6.35 | -\$5.06 (-44%) |
| Total beers sold | 39,556 | 77,841 | +38,285 (+97%) |
| Stadium profit | \$2.24M | \$0.37M | -\$1.87M (-84%) |
| Consumer surplus | \$21.8M | \$28.5M | +\$11.0M (+31%) |
| Externality cost | \$158k | \$311k | +\$153k (+97%) |
| Social welfare | \$24.0M | \$28.6M | +\$4.6M (+19%) |

**Annual impacts (81 games):**
- Stadium revenue loss: **\$151M/season**
- Consumer surplus gain: **\$543M/season**
- External cost increase: **\$12.4M/season**
- Net social welfare gain: **\$373M/season**

**Winners:**
- Consumers (+\$543M surplus)
- Government (+ tax revenue from higher volume)

**Losers:**
- Stadium (-\$151M profit)
- Society (+\$12.4M externality costs)

### Price Ceiling: \$8

Less restrictive than \$7 ceiling:

**Effects relative to \$7 ceiling:**
- Slightly lower consumption
- Higher stadium profit
- Lower externality costs
- Similar consumer surplus gain

### Price Floor: \$15

**Non-binding** (above optimal \$12.85), minimal effects.

### Beer Ban

Complete prohibition of alcohol sales:

| Metric | Impact |
|--------|--------|
| Stadium revenue | -\$2.0M/game |
| Attendance | May decrease 5% (complementarity) |
| Externality costs | -\$158k (eliminated) |
| Consumer surplus | Decreases (no beer option) |

## Deadweight Loss

Price controls create **deadweight loss** (economic inefficiency):

$$DWL = SW_{optimal} - SW_{controlled}$$

For $7 ceiling:
- Consumer surplus gain: +$11.0M
- Producer surplus loss: -$1.87M
- Externality increase: -$153k
- **Net gain: +$4.6M** (positive despite DWL)

The positive net reflects that current equilibrium has underpriced externalities.

## Pigouvian Taxation

Alternative to price controls: **tax** to internalize externalities.

### Optimal Additional Tax

$$t_{Pigovian} = MEC = \$4.00 - \$1.09 = \$2.91/beer$$

**Effects:**
- Consumer price: \$12.50 + \$2.91 = **\$15.41**
- Reduces consumption ~28% (elasticity -0.29)
- Total beers: ~28,500 (from 39,556)
- **Revenue: \$116k/game = \$9.4M/season**

### Pigouvian Tax vs Price Ceiling

```{list-table}
:header-rows: 1

* - Policy
  - Consumer Price
  - Consumption
  - Stadium Profit
  - Gov Revenue
  - Efficiency
* - **Current**
  - $12.50
  - 39,556
  - $2.24M
  - $43k
  - Baseline
* - **$7 Ceiling**
  - $7.00
  - 77,841
  - $0.37M
  - $54k
  - DWL from binding constraint
* - **Pigouvian Tax**
  - $15.41
  - 28,500
  - $2.1M
  - $160k
  - **Most efficient**
```

**Pigouvian tax is more efficient:**
- No deadweight loss (price = social marginal cost)
- Raises revenue for affected communities
- Reduces externalities
- Preserves stadium autonomy

## Policy Recommendations

1. **First-best**: Add \$2.91/beer Pigouvian tax
   - Internalizes external costs
   - Raises \$9.4M/season for NYC
   - Economically efficient

2. **Second-best**: Price floor at \$15
   - Reduces consumption and externalities
   - No revenue for government
   - Stadium keeps higher margin

3. **Avoid**: Price ceiling below \$10
   - Large stadium revenue loss
   - Increases externalities
   - Consumer surplus gain offset by external costs

4. **Consider**: Hybrid approach
   - Moderate tax (+\$1.50) + earlier cutoff (6th inning)
   - Balances efficiency and feasibility
