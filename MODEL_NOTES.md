# Model Calibration Notes

## Observed Prices Are Profit-Maximizing

The model is calibrated so that observed beer prices ($12.50) are approximately profit-maximizing.

### How This Works

Stadiums internalize negative externalities that drunk fans impose on OTHER customers:

1. **Crowd Management** ($): Security, cleanup, liability insurance
   - More drunk fans → more incidents → costs compound

2. **Experience Degradation** ($$$): Drunk fans hurt experience for others
   - Affects FUTURE attendance and willingness to pay
   - Stadium loses repeat business if experience is poor
   - CONVEX: First few drunk fans OK, but as more get drunk it multiplies

3. **Brand/Reputation** ($$): Excessive intoxication damages brand
   - "Cheap beer stadium" image lowers long-run revenue
   - Sponsorships, corporate boxes, premium seating affected

4. **Capacity Constraints** ($$): Service bottlenecks
   - Can only serve ~50,000 beers per game
   - Operational costs, longer lines → customer dissatisfaction

### Mathematical Form

**Internalized Cost Function (Convex):**
```
C_internalized = α · (Q/1000)²
```

Where:
- Q = total beers sold
- α = experience_degradation_cost parameter (calibrated to ~62.3)

**Why Quadratic?**
- Linear costs would shift optimum only slightly
- Quadratic captures COMPOUNDING effects:
  - Incidents multiply with more drunk fans
  - Reputational damage accelerates
  - Experience degradation is non-linear

### Calibration

With α ≈ 62.3:
- **Profit-maximizing beer price: $12.51** ≈ $12.50 observed
- At $12.50: 39,556 beers, internalized cost = $97,453
- At $5.00: 134,392 beers, internalized cost = $1.12M

The monopolist stadium chooses higher prices to avoid these compounding costs.

### Key Insight

This is NOT an externality for policy purposes - it's already internalized!

**For policy analysis:**
- **Internalized costs**: Stadium already accounts for these (crowd mgmt, brand, capacity)
- **External costs**: Society bears these (crime, public health, drunk driving)
  - Estimated at $4.00/beer (crime $2.50 + health $1.50)
  - NOT captured in stadium's profit maximization
  - Justifies Pigouvian taxation or price controls

### Model Use

✅ **Use for:**
- Comparing price control policies (ceiling, floor, ban)
- Analyzing welfare trade-offs
- Quantifying deadweight loss
- Estimating external costs to society

❌ **Not for:**
- Predicting exact profit-maximizing prices (that's an empirical question)
- Estimating optimal internal operations (that's firm-specific)

### Stadium-Specific Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Base beer price | $12.50 | Industry data (2025) |
| Beer cost (all-in) | $5.00 | Labor + materials + overhead |
| Experience cost (α) | 62.28 | Calibrated to observed prices |
| Capacity constraint | 50,000 | Operational estimate |
| Price sensitivity (λ) | 0.133 | Semi-log demand calibration |
| Captive share | 50% | Stadium-specific adjustment |

### References

- Crowd management costs: Stadium operations literature
- Experience degradation: Sports economics (Coates & Humphreys 2007)
- Reputation effects: Brand valuation studies
- Capacity constraints: Queueing theory, operations management

