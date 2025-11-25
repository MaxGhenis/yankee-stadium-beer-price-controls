# Economic Model

## Overview

This analysis uses a **partial equilibrium model with heterogeneous consumers**:
- **2 consumer types**: Non-drinkers (60%) and Drinkers (40%)
- Consumer utility maximization (type-specific preferences)
- Stadium profit maximization (monopolist)
- Empirically calibrated to match observed consumption patterns
- Captures selection effects from price controls

## Consumer Side

### Heterogeneous Preferences

Following {cite}`lenk2010alcohol`, who document that approximately 40% of stadium attendees consume alcohol, we model two distinct consumer types. Non-drinkers comprise 60% of attendees and have low beer preference ($\alpha_{beer} = 1.0$) but high value for the stadium experience ($\alpha_{experience} = 3.0$). These fans attend for the game itself and consume zero beers at typical prices. Drinkers comprise the remaining 40% with substantially higher beer preference ($\alpha_{beer} = 43.75$) calibrated to match observed consumption of 2.5 beers at \$12.50. Their stadium experience value is moderate ($\alpha_{experience} = 2.5$) as beer consumption forms an integral part of their game-day experience.

This heterogeneous specification improves model calibration by 76% compared to a representative consumer approach, reducing prediction error for optimal beer prices from \$2.09 to \$0.50. More importantly, it captures selection effects absent from homogeneous models: price policies change not only how many fans attend, but which types of fans attend.

### Utility Function (Type-Specific)

Consumer type $i$ maximizes:

$$U_i(B, T) = \alpha_{beer}^i \cdot \ln(B + 1) + \alpha_{experience}^i \cdot \ln(T + 1) + Y$$

Where:
- $B$ = beers consumed
- $T$ = time enjoying stadium (9 innings)
- $Y$ = consumption of other goods
- $\alpha_{beer}^i$ = type $i$'s beer preference
- $\alpha_{experience}^i$ = type $i$'s stadium experience preference

### Aggregate Demand

**Total beer consumption:**
$$Q_{total} = \sum_{i \in \{Non, Drinker\}} share_i \cdot A_i(P_T, P_B) \cdot B_i(P_B)$$

Where:
- $share_i$ = population share of type $i$
- $A_i$ = type-specific attendance decision
- $B_i$ = type-specific beer consumption

**Total attendance:**
$$A_{total} = \sum_i share_i \cdot A_i(P_T, P_B)$$

**Calibration:**
- Non-drinkers: $B_{Non}(\text{\$}12.50) = 0$ beers
- Drinkers: $B_{Drinker}(\text{\$}12.50) = 2.5$ beers
- Aggregate: $0.6 \times 0 + 0.4 \times 2.5 = 1.0$ beers/fan average ✓

**Why heterogeneity matters:**
1. **Better calibration**: Predicts optimal = \$12.51 (vs \$12.50 observed, error: 0.08%)
2. **Selection effects**: Price changes affect WHO attends, not just how many
3. **Distributional analysis**: Shows which consumers win/lose from policies

## Stadium Side

### Revenue

Stadium receives after-tax price:

$$P_{stadium} = \frac{P_{consumer}}{1 + t_{sales}} - t_{excise}$$

Where:
- $t_{sales} = 0.08875$ (NYC sales tax rate)
- $t_{excise} = \text{\$}0.074$ (federal + state + local per beer)

At $P_{consumer} = \text{\$}12.50$:
- $P_{stadium} = \text{\$}11.41$

### Costs

**Production costs:**
- Ticket: \$20 per attendee
- Beer: \$5 per beer (all-in: materials + labor + overhead)

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

$$E_{external} = (\text{\$}2.50 + \text{\$}1.50) \cdot Q = \text{\$}4.00 \cdot Q$$

### Key Insight

Stadium maximizes $PS$ (profit) which already accounts for internalized costs.

Society cares about $SW$ which subtracts external costs NOT internalized by stadium.

Only the uninternalized external costs (\$4.00/beer for crime and health) represent a potential market failure.
