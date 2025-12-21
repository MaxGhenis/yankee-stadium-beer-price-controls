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

A **\$7 price ceiling** would be a binding constraint (below optimal \$13.87).

**Effects:**

| Metric | Current (\$13.87) | With \$7 Ceiling | Change |
|--------|------------------|-----------------|--------|
| Consumer beer price | \$13.87 | \$7.00 | -\$6.87 (-50%) |
| Stadium receives | \$11.41 | \$6.35 | -\$5.06 (-44%) |
| Total beers sold | 39,700 | 91,604 | +51,903 (+130.7%) |
| Stadium profit | \$3.43M | \$3.00M | \$-0.43M (-12.4%) |
| Consumer surplus | \$11.3M | \$11.7M | +\$0.4M (+3.9%) |
| Externality cost | \$0.2M | \$0.4M | +\$0.2M (+130.7%) |
| Social welfare | \$14.5M | \$14.3M | +\$-0.2M (+-1.3%) |

**Annual impacts (81 games):**
- Stadium revenue loss: **-\$34M/season**
- Consumer surplus gain: **+\$35.8M/season**
- External cost increase: **+\$16.8M/season**
- Net social welfare gain: **+\$-15.5M/season**

**Winners:**
- Consumers (+\$35.8M surplus) - Cheaper beer outweighs higher tickets on average
- Government (+ tax revenue from higher volume)

**Losers:**
- Stadium (-\$34M profit)
- Society (+\$16.8M externality costs)

### Price Ceiling: \$8

Less restrictive than \$7 ceiling:

**Effects relative to \$7 ceiling:**
- Slightly lower consumption
- Higher stadium profit
- Lower externality costs
- Similar consumer surplus gain

### Price Floor: \$15

**Non-binding** (above optimal \$13.87), minimal effects.

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
- Consumer surplus gain: +\$35.8M
- Producer surplus loss: -\$34M
- Externality increase: -\$16.8M (Note: this is a cost, so it's a negative impact)
- **Net gain: +\$-15.5M** (positive despite DWL)

The positive net reflects that current equilibrium has underpriced externalities.

## Pigouvian Taxation

Alternative to price controls: **tax** to internalize externalities.

### Optimal Additional Tax

$$t_{Pigovian} = MEC = \$4.00 - \$1.30 = \$2.70/beer$$

**Effects:**
- Consumer price: \$13.87 + \$2.70 = \${{ pigouvian_consumer_price }}
- Reduces consumption ~28% (elasticity -0.29)
- Total beers: ~28,500 (from 39,556)
- **Revenue: ~\$8.7M/season**

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
  - \$13.87
  - 39,700
  - \$3.43M
  - \${{ baseline_tax_revenue_k }}k
  - Baseline
* - **$7 Ceiling**
  - $7.00
  - 91,604
  - \$3.00M
  - \${{ ceiling7_tax_revenue_k }}k
  - DWL from binding constraint
* - **Pigouvian Tax**
  - \${{ pigouvian_consumer_price }}
  - 28,500
  - $2.1M
  - \${{ pigouvian_tax_revenue_k }}k
  - **Most efficient**
```

**Pigouvian tax is more efficient:**
- No deadweight loss (price = social marginal cost)
- Raises revenue for affected communities
- Reduces externalities
- Preserves stadium autonomy

## Policy Recommendations

1. **First-best**: Add \$2.70/beer Pigouvian tax
   - Internalizes external costs
   - Raises \$8.7M/season for NYC
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