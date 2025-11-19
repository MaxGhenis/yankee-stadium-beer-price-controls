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

A **\$7 price ceiling** would be a binding constraint (below optimal \${{ baseline_beer }}).

**Effects:**

| Metric | Current (\${{ baseline_beer }}) | With \$7 Ceiling | Change |
|--------|------------------|-----------------|--------|
| Consumer beer price | \${{ baseline_beer }} | \$7.00 | -\${{ baseline_beer_minus_ceiling7 }} (-{{ beer_price_pct_change_from_baseline }}%) |
| Stadium receives | \$11.41 | \$6.35 | -\$5.06 (-44%) |
| Total beers sold | {{ baseline_total_beers }} | {{ ceiling7_total_beers }} | +{{ ceiling7_total_beers_change }} (+{{ ceiling7_total_beers_pct }}%) |
| Stadium profit | \${{ baseline_profit_per_game_M }}M | \${{ ceiling7_profit_per_game_M }}M | \${{ ceiling7_profit_change_M }}M ({{ ceiling7_producer_surplus_pct }}%) |
| Consumer surplus | \${{ baseline_consumer_surplus }}M | \${{ ceiling7_consumer_surplus }}M | +\${{ ceiling7_consumer_surplus_change }}M (+{{ ceiling7_consumer_surplus_pct }}%) |
| Externality cost | \${{ baseline_externality_cost }}M | \${{ ceiling7_externality_cost }}M | +\${{ ceiling7_externality_cost_change }}M (+{{ ceiling7_externality_cost_pct }}%) |
| Social welfare | \${{ baseline_social_welfare }}M | \${{ ceiling7_social_welfare }}M | +\${{ ceiling7_social_welfare_change }}M (+{{ ceiling7_social_welfare_pct }}%) |

**Annual impacts (81 games):**
- Stadium revenue loss: **-\${{ ceiling7_profit_loss_annual_M }}M/season**
- Consumer surplus gain: **+\${{ ceiling7_consumer_surplus_change_annual }}M/season**
- External cost increase: **+\${{ ceiling7_externality_cost_change_annual }}M/season**
- Net social welfare gain: **+\${{ ceiling7_social_welfare_change_annual }}M/season**

**Winners:**
- Consumers (+\${{ ceiling7_consumer_surplus_change_annual }}M surplus) - Cheaper beer outweighs higher tickets on average
- Government (+ tax revenue from higher volume)

**Losers:**
- Stadium (-\${{ ceiling7_profit_loss_annual_M }}M profit)
- Society (+\${{ ceiling7_externality_cost_change_annual }}M externality costs)

### Price Ceiling: \$8

Less restrictive than \$7 ceiling:

**Effects relative to \$7 ceiling:**
- Slightly lower consumption
- Higher stadium profit
- Lower externality costs
- Similar consumer surplus gain

### Price Floor: \$15

**Non-binding** (above optimal \${{ baseline_beer }}), minimal effects.

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
- Consumer surplus gain: +\${{ ceiling7_consumer_surplus_change_annual }}M
- Producer surplus loss: -\${{ ceiling7_profit_loss_annual_M }}M
- Externality increase: -\${{ ceiling7_externality_cost_change_annual }}M (Note: this is a cost, so it's a negative impact)
- **Net gain: +\${{ ceiling7_social_welfare_change_annual }}M** (positive despite DWL)

The positive net reflects that current equilibrium has underpriced externalities.

## Pigouvian Taxation

Alternative to price controls: **tax** to internalize externalities.

### Optimal Additional Tax

$$t_{Pigovian} = MEC = \${{ external_cost_sum_raw }} - \${{ current_taxes_per_beer_raw }} = \${{ pigouvian_gap }}/beer$$

**Effects:**
- Consumer price: \${{ baseline_beer }} + \${{ pigouvian_gap }} = \${{ pigouvian_consumer_price }}
- Reduces consumption ~28% (elasticity -0.29)
- Total beers: ~28,500 (from 39,556)
- **Revenue: ~\${{ pigouvian_revenue_annual }}M/season**

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
  - \${{ baseline_beer }}
  - {{ baseline_total_beers }}
  - \${{ baseline_profit_per_game_M }}M
  - \${{ baseline_tax_revenue_k }}k
  - Baseline
* - **$7 Ceiling**
  - $7.00
  - {{ ceiling7_total_beers }}
  - \${{ ceiling7_profit_per_game_M }}M
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

1. **First-best**: Add \${{ pigouvian_gap }}/beer Pigouvian tax
   - Internalizes external costs
   - Raises \${{ pigouvian_revenue_annual }}M/season for NYC
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