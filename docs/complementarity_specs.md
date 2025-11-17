# Alternative Complementarity Specifications

## Theoretical Foundation: Leisten (2025)

{cite}`leisten2025beer` provides rigorous theoretical analysis of beer price controls at stadiums:

**Key result**: Under log-concavity of demand, beer price ceilings cause ticket prices to rise.

**His model:**
- Ticket demand: $q_x(p_x)$
- Concession demand: $q_y = q_x(p_x) \cdot q_y(p_y)$ (multiplicative)
- **Assumption**: Beer prices do NOT directly affect ticket demand (one-way complementarity)

**First-order conditions:**
$$p_y = -\frac{q_y(p_y)}{q_y'(p_y)}$$
$$p_x = -\frac{q_x(p_x)}{q_x'(p_x)} - p_y q_y(p_y)$$

When beer price ceiling $Z$ binds:
$$\frac{dp_x}{dZ} = \frac{Zq_y'(Z) - q_y(Z)}{\frac{q_x(p_x)q_x''(p_x)}{q_x'(p_x)} - 2}$$

Sign depends on: $2q_x'(p_x)^2$ vs $q_x(p_x)q_x''(p_x)$

**Under log-concavity:** $q_x q_x'' < q_x'^2$, so Leisten proves $\frac{dp_x}{dZ} < 0$ (tickets rise when ceiling tightens).

**Our extension:** We allow two-way complementarity ($A(P_T, P_B)$), which is more general but requires assuming the cross-elasticity magnitude.

---

## Current Specification (Two-Way Multiplicative)

**Functional form:**
$$A(P_T, P_B) = A_0 \cdot e^{-\lambda_T(P_T - P_0^T)} \cdot \left(\frac{P_B}{P_0^B}\right)^{-\epsilon_{cross}}$$

Where $\epsilon_{cross} = 0.1$

**Properties:**
- Cross-price elasticity: $\frac{\partial \ln A}{\partial \ln P_B} = -0.1$
- 10% beer price increase → 1% attendance decrease
- Symmetric: effect scales with price level
- **Log-concave**: Semi-log form satisfies Leisten's condition

**Citation**: Standard in single-equation demand {cite}`varian1992microeconomic`; two-way extension beyond {cite}`leisten2025beer`

---

## Alternative Specifications

### 1. Almost Ideal Demand System (AIDS)

**Reference**: {cite}`deaton1980almost`

**Form**: Derived from utility maximization
$$w_i = \alpha_i + \sum_j \gamma_{ij} \ln p_j + \beta_i \ln(x/P)$$

Where:
- $w_i$ = budget share of good $i$
- $\gamma_{ij}$ = cross-price effects (estimated)
- Symmetry: $\gamma_{ij} = \gamma_{ji}$

**Cross-price elasticity:**
$$\epsilon_{ij} = \frac{\gamma_{ij}}{w_i} - \delta_{ij}$$

**Advantages:**
- ✅ Theory-consistent (utility-derived)
- ✅ Flexible (Engel curves, substitution patterns)
- ✅ Testable restrictions (symmetry, homogeneity)

**Disadvantages:**
- ❌ Requires panel data (multiple markets/times)
- ❌ Need variation in both ticket AND beer prices
- ❌ Computationally intensive

**Typical estimates**: Cross-elasticities range -0.5 to +0.5 for food items {cite}`deaton1980almost`

### 2. CES Utility Function

**Reference**: {cite}`arrow1961capital`

**Form**:
$$U = \\left[\\alpha B^\\rho + (1-\\alpha) T^\\rho\\right]^{1/\\rho}$$

Where:
- $\\rho$ relates to elasticity of substitution: $\\sigma = 1/(1-\\rho)$
- $\\sigma < 1$: Complements
- $\\sigma > 1$: Substitutes
- $\\sigma = 1$: Cobb-Douglas (independent)

**Implied cross-elasticity:**
$$\\epsilon_{TB} = (\\sigma - 1) \\cdot \\frac{P_B B}{E}$$

**Advantages:**
- ✅ Micro-founded (utility maximization)
- ✅ Single parameter ($\\sigma$) controls substitution
- ✅ Nests Cobb-Douglas, Leontief (perfect complements)

**Disadvantages:**
- ❌ Restrictive (constant $\\sigma$ across price levels)
- ❌ Requires calibration or estimation

**Typical range**: $\\sigma = 0.2$ to $0.8$ for complements

### 3. Translog Demand

**Reference**: {cite}`christensen1975transcendental`

**Form**: Second-order flexible functional form
$$\\ln q_i = \\alpha_i + \\sum_j \\beta_{ij} \\ln p_j + \\gamma_i \\ln y$$

Where $\\beta_{ij}$ are cross-price terms.

**Advantages:**
- ✅ Very flexible (no restrictive functional form)
- ✅ Can nest AIDS, Cobb-Douglas
- ✅ Captures non-linearities

**Disadvantages:**
- ❌ Many parameters to estimate
- ❌ May violate regularity conditions

### 4. Linear Interaction

**Form**:
$$A = A_0 - \\alpha P_T - \\beta P_B - \\gamma P_T \\cdot P_B$$

Where $\\gamma > 0$ for complements.

**Cross-price elasticity:**
$$\\epsilon_{TB} = -\\frac{\\beta + \\gamma P_T}{A} \\cdot P_B$$

**Advantages:**
- ✅ Simple, interpretable
- ✅ Easy to estimate (linear regression)

**Disadvantages:**
- ❌ Can produce negative quantities
- ❌ Elasticity changes with price level
- ❌ No utility foundation

### 5. Nested Logit (Discrete Choice)

**Reference**: {cite}`mcfadden1978modeling`

**Form**: For attendance decision
$$P(attend) = \\frac{e^{V_{attend}}}{e^{V_{attend}} + e^{V_{not\\_attend}}}$$

Where $V_{attend}$ depends on both ticket and beer prices.

**Advantages:**
- ✅ Microfounded (random utility)
- ✅ Handles discrete choices naturally
- ✅ Rich substitution patterns

**Disadvantages:**
- ❌ Complex estimation (maximum likelihood)
- ❌ Requires individual-level data

---

## How Economists Evaluate Specifications

### 1. Theoretical Consistency

**Question**: Does specification come from utility maximization?

**Evaluation criteria:**
- Slutsky symmetry: $\\frac{\\partial q_i}{\\partial p_j} = \\frac{\\partial q_j}{\\partial p_i}$ (compensated)
- Homogeneity: Doubling all prices and income → no change
- Adding up: Budget shares sum to 1

**Rankings:**
- ✅ AIDS, CES: Fully consistent
- ⚠️  Current (multiplicative): Partial (not derived from single utility)
- ❌ Linear: Not theory-consistent

### 2. Empirical Fit

**Metrics:**
- R² or pseudo-R²
- AIC/BIC (information criteria)
- Out-of-sample prediction
- Residual diagnostics

**Data requirements:**
- Panel data (multiple markets, times)
- Price variation
- Exogenous price changes (instruments)

### 3. Flexibility vs Parsimony

**Trade-off:**
- AIDS: Very flexible (many parameters)
- CES: Parsimonious (single $\\sigma$)
- Current: Very simple (single $\\epsilon_{cross}$)

**Evaluation**:
- Use information criteria (AIC/BIC)
- Test nested models (likelihood ratio)
- Check if additional parameters improve fit

### 4. Plausibility of Estimates

**Bounds checking:**
- For complements: $\\epsilon_{cross} < 0$
- Typical range: -0.1 to -2.0
- Strong complements (cars/gas): -1.6
- Weak complements: -0.1 to -0.3

**Our choice (0.1):**
- At low end of plausible range
- Implies weak complementarity
- Conservative assumption

### 5. Policy Robustness

**Question**: Do policy conclusions change with specification?

**Evaluation:**
- Simulate under different specifications
- Check if directional effects robust
- Quantify sensitivity of key outcomes

---

## Comparison to Empirical Literature

### Food Complements
- Meat & vegetables: Cross-elasticity varies by study
- Typically -0.1 to -0.5

### Transportation
- Cars & gasoline: **-1.6** (strong complements)
- Public transit & auto: +0.5 to +0.8 (substitutes)

### Entertainment
- Movie tickets & popcorn: No published estimates found
- Theme park admission & food: No estimates found

**Stadium tickets & beer**: NO PUBLISHED ESTIMATES

---

## Recommendation for This Analysis

### Current Approach (Multiplicative with ε=0.1)

**Pros:**
- ✅ Simple, transparent
- ✅ Directionally correct (negative)
- ✅ Conservative (weak complementarity)
- ✅ Easy to adjust in sensitivity analysis

**Cons:**
- ❌ Not derived from utility
- ❌ No empirical validation
- ❌ Arbitrary functional form

### Better Approaches (If Data Available)

1. **Estimate AIDS model** with Yankees panel data
   - Vary prices across games/seasons
   - Estimate full demand system
   - Get cross-elasticity from data

2. **Use car/gasoline analogy**
   - Both are "required + optional" like tickets/beer
   - Cross-elasticity -1.6 as benchmark
   - Test sensitivity to -0.5, -1.0, -1.6

3. **Survey-based calibration**
   - Ask fans willingness to attend with/without beer
   - Discrete choice experiment
   - Estimate cross-effect structurally

### For This Project

**Keep current approach but:**
1. ✅ Document it's ASSUMED (done)
2. ✅ Run Monte Carlo over plausible range 0.05-0.30 (done)
3. ✅ Cite analogous contexts (car/gas: -1.6)
4. ✅ Show sensitivity of conclusions

**Add to references:**
- Deaton & Muellbauer (1980) for AIDS framework
- Varian (1992) for demand theory
- McFadden (1978) for discrete choice
- Empirical examples (cars/gas)

```{bibliography}
:filter: docname in docnames
```
