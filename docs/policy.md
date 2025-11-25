# Policy Analysis

## Price Control Implementation Details

**Important Clarification:** Throughout this analysis, price controls apply to the **menu/sticker price (pre-sales-tax)**, consistent with:
- **Real-world precedent:** Scotland's Minimum Unit Pricing applies pre-VAT; US historical price controls were pre-tax
- **Enforcement practicality:** Regulators monitor posted menu prices, not checkout totals
- **Legal structure:** Sales tax is applied at point of sale, after base price is determined

**Example: \$6 Beer Price Ceiling (Half Price)**

| Component | Amount |
|-----------|--------|
| Maximum menu price | **\$6.00** ← *Price control applies here* |
| + NYC sales tax (8.875%) | +\$0.53 |
| = **Consumer pays** | **\$6.53** |
| - Sales tax to government | -\$0.53 |
| - Excise taxes | -\$0.074 |
| = **Stadium receives** | **\$5.46** |

**Implication:** When we analyze a "\$6 ceiling," the stadium receives only **\$5.46** after taxes, creating an even tighter constraint than the headline \$6 suggests.

## Price Controls

### Price Ceiling: \$6 (Half Price)

A **\$6 price ceiling** (half of current \$12.50) would be a binding constraint.

**Effects:**

| Metric | Current (\$12.50) | With \$6 Ceiling | Change |
|--------|------------------|-----------------|--------|
| Beer price | \$12.50 | \$6.00 | -52% |
| Ticket price | \$70.44 | \$85.33 | +21% |
| Attendance | 46,345 | 37,232 | -20% |
| Beers per fan | 0.86 | 2.63 | +207% |
| Total beers sold | 39,700 | 97,856 | +146% |

**Key mechanism:** Stadium raises ticket prices to offset beer margin loss. Selection effects cause attendance decline to disproportionately affect non-drinkers.

### Price Ceiling: \$8

Less restrictive than \$6 ceiling:

| Metric | \$6 Ceiling | \$8 Ceiling |
|--------|-------------|-------------|
| Ticket increase | +21% | +4% |
| Attendance change | -20% | -2% |
| Total beers | +146% | +110% |

Higher ceilings produce smaller effects but same directional pattern.

### Price Floor: \$15

**Non-binding** (above optimal price), minimal effects.

### Beer Ban

Complete prohibition of alcohol sales:
- Eliminates beer revenue
- Attendance may decrease (complementarity)
- Eliminates externality costs
- Reduces consumer surplus for drinkers

## Pigouvian Taxation

Alternative to price controls: **tax** to internalize externalities.

### Optimal Additional Tax

$$t_{Pigouvian} = MEC = \$4.00 - \$1.09 = \$2.91/beer$$

**Effects:**
- Raises beer price (reduces consumption)
- Revenue goes to government (not stadium)
- More economically efficient than price controls

### Pigouvian Tax vs Price Ceiling

| Policy | Consumer Price | Consumption | Stadium Profit | Efficiency |
|--------|---------------|-------------|----------------|------------|
| **Current** | \$12.50 | Baseline | Baseline | Baseline |
| **\$6 Ceiling** | \$6.00 | +146% | Reduced | Creates distortions |
| **Pigouvian Tax** | \$15+ | Reduced | Similar | **Most efficient** |

**Pigouvian tax is more efficient:**
- No deadweight loss (price = social marginal cost)
- Raises revenue for affected communities
- Reduces externalities
- Preserves stadium pricing autonomy

## Policy Recommendations

1. **First-best**: Add Pigouvian tax
   - Internalizes external costs
   - Raises revenue for NYC
   - Economically efficient

2. **Avoid**: Price ceilings
   - Stadium responds by raising tickets
   - Increases total consumption and externalities
   - Creates selection effects shifting crowd toward drinkers

3. **Consider**: Hybrid approaches
   - Moderate tax + earlier cutoff (e.g., 6th inning)
   - Balances efficiency and feasibility
