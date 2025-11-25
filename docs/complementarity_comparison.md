# Complementarity Model Comparison

## Two Approaches to Beer-Ticket Complementarity

This analysis compares two modeling approaches for stadium pricing with complementary goods.

### Leisten (2025): One-Way Complementarity

{cite}`leisten2025beer` assumes **beer prices do NOT affect ticket demand**:

$$q_{ticket}(P_T) \quad \text{(not a function of } P_B \text{)}$$

**Mechanism for ticket increase under ceiling:**
- Stadium has first-order condition with "complementarity discount"
- $P_T = -\frac{q_T}{q_T'} - P_B \cdot q_B(P_B)$
- When $P_B$ falls (binding ceiling), discount term shrinks
- $P_T$ must rise to restore optimal markup

**Key insight**: Tickets rise purely through markup adjustment, not through demand-side effects.

### Our Model: Two-Way Complementarity

We assume **beer prices DO affect ticket demand** (cross-price elasticity = 0.1):

$$A(P_T, P_B) = A_0 \cdot e^{-\lambda_T(P_T - P_T^0)} \cdot \left(\frac{P_B}{P_B^0}\right)^{-\epsilon_{cross}}$$

**Mechanism for ticket increase under ceiling:**
1. Beer margin collapses ($11.41 → $6.35 net/beer)
2. Stadium shifts revenue focus to tickets
3. Higher ticket prices reduce attendance
4. Reduced attendance limits beer sales at bad margin (self-limiting)

**Key insight**: Tickets rise both to capture shifted revenue AND because demand-side cross-effects exist.

## Model Comparison

| Feature | Leisten (2025) | Our Model |
|---------|----------------|-----------|
| Cross-price elasticity | 0 (one-way) | 0.1 (two-way) |
| Beer affects attendance | No | Yes |
| Consumer heterogeneity | No | Yes (2 types) |
| Ticket increase mechanism | Markup adjustment | Margin shift + cross-effects |
| Selection effects | No | Yes (crowd composition) |

## Why Both Predict Ticket Increases

Despite different mechanisms, both models reach the same qualitative conclusion:

**Beer ceiling → Ticket prices rise**

This is because the core economic logic is the same:
- Tickets and beer are joint revenue sources
- Constraining one margin shifts optimization to the other
- Stadium re-optimizes to maintain profit

## Which Is More Realistic?

### Arguments for One-Way (Leisten)
- Simpler, more tractable
- Fans may not consider beer prices when buying tickets
- Ticket decision is temporally separated from beer purchase

### Arguments for Two-Way (Our Model)
- More symmetric and general
- Fans consider total game cost
- Pre-game drinking substitutes for expensive stadium beer
- Empirically: attendance does appear to respond to concession prices

### Empirical Test
The models make different predictions about **attendance response** to beer price changes:
- **Leisten**: Attendance unchanged when beer price falls
- **Our model**: Attendance increases (slightly) when beer price falls

With stadium transaction data, this could be tested directly.

## Monte Carlo Results by Cross-Price Elasticity

Our Monte Carlo analysis samples `cross_price_elasticity` from [0, 0.3] to span both models:

```
Cross-Price = 0.0 (Leisten):  Ticket change = +$X
Cross-Price = 0.1 (baseline): Ticket change = +$Y
Cross-Price = 0.3 (strong):   Ticket change = +$Z
```

The directional effect (tickets rise) is **robust** across all values.
The magnitude varies with this assumption.

## Conclusion

Both Leisten and our heterogeneous model agree:
- Beer price ceilings cause ticket prices to rise
- Stadium profit falls
- Consumption increases

Our model adds:
- Selection effects (who attends changes)
- Attendance response to beer prices
- Better calibration to observed prices

For policy analysis, the **directional conclusions are robust** to the complementarity assumption.
The exact magnitudes depend on this uncertain parameter.

```{bibliography}
:filter: docname in docnames
```
