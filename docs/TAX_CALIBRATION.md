# Tax-Adjusted Calibration

## Model Now Accounts for Existing Taxes

The \$12.50 beer price is what **consumers pay** (tax-inclusive).

### Revenue Flow (per beer)

```
Consumer pays:              $12.50
Less sales tax (8.875%):    -$1.02
= Pre-tax price:            $11.48
Less excise taxes:          -$0.074
= Stadium receives:         $11.41
Less production cost:       -$5.00
Less internalized costs:    ~$0.04 (varies with volume)
= Stadium profit margin:    ~$6.37/beer
```

### Tax Breakdown

**Excise Taxes (per 12 oz):**
- Federal: \$0.05
- NY State: \$0.013
- NYC: \$0.011
- **Total: \$0.074**

**Sales Tax:**
- NYC rate: 8.875%
- On \$12.50: **\$1.02**

**Total tax: \$1.09/beer (8.7% of consumer price)**

## Profit Maximization with Taxes

Stadium chooses consumer price to maximize:
```
π = (P_consumer/(1 + t_sales) - t_excise - MC - C_internalized(Q)) · Q(P_consumer)
```

Where:
- P_consumer = price to consumer
- t_sales = sales tax rate (8.875%)
- t_excise = excise tax per unit (\$0.074)
- MC = marginal production cost (\$5.00)
- C_internalized = convex internalized cost function

**Optimal consumer price: \$12.85 ≈ \$12.50 observed ✓**

## Pigouvian Tax Gap

**External costs not captured by current taxes:**

```
External cost per beer:     $4.00
  - Crime/violence:         $2.50
  - Public health:          $1.50

Current tax per beer:       $1.09
  - Excise:                 $0.074
  - Sales:                  $1.02

Pigouvian tax gap:          $2.91/beer
Coverage ratio:             27.3%
```

### Optimal Additional Tax

To fully internalize external costs:

**Additional Pigouvian tax: \$2.91/beer**

This would bring total tax to \$4.00, fully covering external costs.

### Revenue Implications

**Per game (40,000 beers):**
- Current tax revenue: \$43,600
- Optimal tax revenue: \$160,000
- **Additional: \$116,400/game**

**Per season (81 home games):**
- Current: \$3.5M
- Optimal: \$13.0M
- **Additional: \$9.4M/season**

(Assuming no demand reduction; actual would be lower due to price elasticity)

## Policy Simulation

The Streamlit app now shows:

1. **Baseline**: Stadium optimizes at \$12.85 consumer price (accounting for current taxes)
2. **Additional Pigouvian tax**: What happens if we add \$2.91/beer tax
3. **Tax incidence**: How tax burden splits between stadium and consumers

Stadium can't avoid taxes by lowering posted price - taxes are per-unit, so they reduce profit regardless.

