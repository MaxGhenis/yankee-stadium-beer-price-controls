# Economic Model

## Overview

This analysis uses a **partial equilibrium model** of the stadium beer market with:
- Consumer utility maximization
- Stadium profit maximization (monopolist)
- Demand elasticities from literature
- Internalized and external costs

## Consumer Side

### Utility Function

Consumers derive utility from beer consumption and stadium experience:

$$U(B, T) = \alpha \cdot \ln(B + 1) + \beta \cdot \ln(T + 1) + Y$$

Where:
- $B$ = beers consumed
- $T$ = time enjoying stadium (9 innings)
- $Y$ = consumption of other goods
- $\alpha = 1.5$ (beer preference weight)
- $\beta = 3.0$ (stadium experience weight)

### Demand

**Semi-log demand function:**

$$Q = Q_0 \cdot e^{-\lambda(P - P_0)}$$

Where:
- $Q_0 = 1.0$ beers per fan (baseline)
- $P_0 = \$12.50$ (baseline consumer price)
- $\lambda = 0.133$ (price sensitivity)

**Properties:**
- At baseline price: 40% drink × 2.5 beers = 1.0 average
- Elasticity varies with price level
- More inelastic than general alcohol market (captive audience)

## Stadium Side

### Revenue

Stadium receives after-tax price:

$$P_{stadium} = \frac{P_{consumer}}{1 + t_{sales}} - t_{excise}$$

Where:
- $t_{sales} = 0.08875$ (NYC sales tax rate)
- $t_{excise} = \$0.074$ (federal + state + local)

At $P_{consumer} = \$12.50$:
- $P_{stadium} = \$11.41$

### Costs

**Production costs:**
- Ticket: $\$20$ per attendee
- Beer: $\$5$ per beer (all-in: materials + labor + overhead)

**Internalized costs (convex):**

$$C_{intern}(Q) = 250 \cdot \left(\frac{Q}{1000}\right)^2$$

This captures:
- Crowd management (security, cleanup, liability)
- Brand/reputation damage
- Experience degradation for other customers
- Capacity constraints

### Profit Maximization

$$\max_{P_T, P_B} \pi = P_T \cdot A(P_T, P_B) + P_{stadium}(P_B) \cdot B(P_B) \cdot A(P_T, P_B) - C$$

Subject to:
- $A \leq$ capacity
- $P_B \geq MC$

## Social Welfare

$$SW = CS + PS - E_{external}$$

Where:
- $CS$ = consumer surplus
- $PS$ = producer surplus (stadium profit)
- $E_{external}$ = external costs (crime + health)

External costs:

$$E_{external} = (\$2.50 + \$1.50) \cdot Q = \$4.00 \cdot Q$$

### Key Insight

Stadium maximizes $PS$ (profit) which already accounts for internalized costs.

Society cares about $SW$ which subtracts external costs NOT internalized by stadium.

**Gap:** $E_{external} - t_{current} = \$4.00 - \$1.09 = \$2.91/beer$

This is the Pigouvian tax gap.
