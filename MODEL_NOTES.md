# Model Calibration Notes

## Beer Price Discrepancy

The model finds profit-maximizing beer prices of $5-7, while observed prices are $12.50.

### Why This Happens

With semi-log demand Q = Q₀·e^(-λP), profit maximization leads to prices close to marginal cost when:
- Demand is relatively elastic at low prices
- Volume effects dominate margin effects
- No capacity or quality constraints

### Why Real Stadiums Charge $12.50

Real prices reflect factors beyond pure profit maximization:

1. **Experience/Brand Value**: Don't want "cheap beer" image
2. **Crowd Management**: Limit intoxication and rowdy behavior  
3. **Social Responsibility**: Minimize alcohol-related incidents
4. **Capacity Constraints**: Limited beer service capacity
5. **Quality Signaling**: Higher prices signal premium experience

### Model Use

The model is best used for:
- **Comparative analysis**: How do price changes affect outcomes?
- **Policy evaluation**: Impact of price ceilings/floors relative to baseline
- **Welfare analysis**: Trade-offs between profit, consumer surplus, and externalities

NOT for:
- Predicting absolute optimal prices
- Matching observed prices exactly

### Stadium-Specific Adjustments

The model includes:
- Captive audience effects (50% price-insensitive demand)
- Complementarity between tickets and beer
- Semi-log demand calibrated to stadium context
- Realistic all-in costs ($5 including labor)

Even with these adjustments, pure profit maximization suggests lower prices than observed.
This is expected and reflects non-modeled considerations.
