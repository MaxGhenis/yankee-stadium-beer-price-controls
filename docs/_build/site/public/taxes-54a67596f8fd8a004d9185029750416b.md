# Tax Analysis & Pigouvian Gap

## Current Tax Structure

### Beer Taxes in NYC (per 12 oz)

**Excise Taxes:**
- Federal: $0.05
- NY State: $0.013
- NYC: $0.011
- **Total excise: $0.074**

**Sales Tax:**
- NYC rate: 8.875%
- On $12.50 beer: $1.02

**Total tax: $1.09/beer (8.7% of consumer price)**

## Revenue Flow

```
Consumer pays:              $12.50
├─ Sales tax (→ government): $1.02
├─ Excise tax (→ government): $0.074
└─ Net to stadium:           $11.41
   ├─ Production cost:       -$5.00
   ├─ Internalized costs:    -$0.04
   └─ Profit:                 $6.37/beer
```

### Annual Tax Revenue (Current)

Per game (40,000 beers):
- Sales tax: $40,800
- Excise: $2,960
- **Total: $43,760/game**

Per season (81 games):
- **$3.5M/season** to government

## External Costs Not Covered by Current Taxes

### Crime Externalities: $2.50/beer

Based on {cite}`carpenter2015mlda`:
- 10% alcohol ↑ → 1% assault ↑, 2.9% rape ↑
- Police, courts, incarceration costs
- Property damage, emergency services
- Concentrated around stadium on game days

### Health Externalities: $1.50/beer

Based on {cite}`manning1991costs` (inflation-adjusted):
- Emergency room visits
- Trauma care (fights, accidents)
- Long-run health system burden
- Drunk driving crashes
- Lost productivity

### Total External Cost: $4.00/beer

## Pigouvian Tax Gap

```
External cost per beer:      $4.00
Current tax per beer:        $1.09
────────────────────────────────
Pigouvian gap:               $2.91

Coverage ratio:              27.3%
Undertaxed amount:           72.7%
```

### Comparison to Other Goods

| Good | External Cost | Current Tax | Coverage |
|------|---------------|-------------|----------|
| **Stadium beer** | $4.00 | $1.09 | **27%** |
| Cigarettes | $10/pack | $5-8/pack | 50-80% |
| Gasoline | $2/gallon | $0.50/gal | 25% |
| Carbon | $100/ton | $0-30/ton | 0-30% |

Stadium beer is **significantly undertaxed** relative to externalities.

## Optimal Pigouvian Tax

### Recommendation: +$2.91/beer

This would:
1. **Internalize external costs** (consumers face full social cost)
2. **Reduce consumption** to socially optimal level
3. **Raise revenue** for affected communities
4. **Improve efficiency** (no deadweight loss)

### Revenue Projections

**Per game:**
- Current consumption: 40,000 beers
- After tax: ~28,500 beers (29% reduction)
- Revenue: 28,500 × $2.91 = **$82,935/game**

**Per season:**
- 81 home games
- **Revenue: $6.7M/season**

(Lower than naïve $9.4M due to demand reduction)

### Where Should Revenue Go?

**Affected parties:**
1. **Bronx community**: Bears crime externalities
2. **NYC public health**: Emergency services, hospitals
3. **NYPD**: Policing costs on game days
4. **MTA**: Drunk passenger incidents

**Allocation recommendation:**
- 40% → Bronx community programs
- 30% → NYC public health
- 20% → NYPD overtime/resources
- 10% → MTA safety programs

## Tax Incidence

Who actually bears the tax burden?

With beer demand elasticity ε = -0.29 (semi-log at $12.50):

**Pass-through rate:**

$$\theta = \frac{1}{1 - \epsilon} = \frac{1}{1.29} = 0.78$$

**Effect of $2.91 tax:**
- Consumer price increase: $2.91 × 0.78 = **$2.27**
- Stadium price decrease: $2.91 × 0.22 = **$0.64**

**Result:**
- Consumer pays: $12.50 + $2.27 = $14.77
- Stadium receives: $11.41 - $0.64 = $10.77
- Government receives: $2.91

**Burden split:** 78% consumers, 22% stadium

This is standard tax incidence: more inelastic side bears more burden.

## Alternative Revenue Uses

### Option 1: Reduce Other Taxes
Use $6.7M to reduce property taxes in the Bronx

### Option 2: Public Safety
Increase police presence, security on game days

### Option 3: Public Health
Alcohol treatment programs, ER capacity

### Option 4: Return to Fans
Subsidize ticket prices or public transportation

**Most efficient:** Target spending toward externality reduction (safety, health).
