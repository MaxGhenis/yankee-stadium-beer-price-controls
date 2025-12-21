# Model Assumptions & Parameter Sources

## Empirically Estimated vs Assumed

### ✅ FROM LITERATURE (Empirical Estimates)

**Own-Price Elasticities:**
- Ticket demand: -0.49 to -0.76 {cite}`noll1974attendance,scully1989business`
- General alcohol: -0.79 to -1.14 (not stadium-specific)

**Consumption Rates:**
- 41% of male fans tested positive for alcohol {cite}`wolfe1998baseball`
- We use 40% as a round estimate for both genders

**Externalities:**
- Crime: 10% alcohol ↑ → 1% assault ↑, 2.9% rape ↑ {cite}`carpenter2015mlda`
- External costs: \$0.48-\$1.19/drink (1986\$) {cite}`manning1991costs`

### ⚠️  ASSUMED (Not From Empirical Estimates)

**Cross-Price Elasticity (Complementarity): 0.1**

**Source**: ASSUMPTION, not empirical estimate

**Rationale**:
- {cite}`coates2007ticket` and {cite}`krautmann2007concessions` document that tickets and concessions are complements
- Both papers show teams price tickets in inelastic region to drive concession sales
- BUT: Neither provides specific cross-price elasticity estimate

**What we know:**
- Tickets and beer are complements (qualitative)
- Teams jointly optimize (strong evidence)
- Complementarity is "significant" (exact magnitude unknown)

**Key Modeling Choice: Two-Way Complementarity**

Recent theoretical work by {cite}`leisten2025beer` explicitly analyzes this assumption:
- **Leisten assumes**: Beer prices do NOT affect ticket demand (one-way complementarity: tickets → beer)
- **We assume**: Beer prices DO affect ticket demand (two-way complementarity: tickets ↔ beer)

Both models predict beer ceilings cause ticket prices to rise, but through different mechanisms:
- **Leisten**: Complementarity discount term in FOC shrinks → tickets rise to restore markup
- **Our model**: Beer margin collapses → stadium shifts to tickets → higher tickets reduce attendance (limiting beer sales at bad margin)

**Why we model two-way complementarity:**
1. More realistic: fans likely consider total game cost including beer
2. Allows for substitution to pre-game drinking if stadium beer too expensive
3. Consistent with observed fan behavior (attendance drops when concession prices rise significantly)
4. Makes model symmetric and general

**Calibration approach:**
- Assume 10% beer price change → 1% attendance change
- Consistent with "weak to moderate" complementarity
- Conservative estimate (could be 0.2-0.3 if beer very important)

**Sensitivity range:**
- Leisten: 0.00 (one-way only)
- Low: 0.05 (beer minor part of experience)
- Base: 0.10 (current model)
- High: 0.30 (beer central to fan experience)

**Monte Carlo analysis**: Our uncertainty quantification samples cross_price_elasticity uniformly from [0.0, 0.3], spanning the full range from Leisten's pure one-way model to strong two-way complementarity. This ensures our qualitative conclusions (tickets rise, consumption increases) are robust to this critical but unmeasured parameter.

**Why 0.1 is reasonable for point estimates:**
- {cite}`coates2007ticket` show teams sacrifice ticket revenue for concession profits, implying cross-effects matter
- If cross-elasticity were very high (>0.3), we'd expect stadiums to heavily subsidize beer to drive attendance—they don't
- If cross-elasticity were very low (<0.05), teams wouldn't care about beer prices' effect on attendance—but they do (7th inning cutoffs, etc.)
- 0.1 represents a middle ground: beer matters, but isn't the primary attendance driver

### ⚙️  CALIBRATED (To Match Observed Prices)

**Demand Sensitivities (λ):**
- Beer: 0.133 (calibrated so \$12.50 is optimal)
- Tickets: 0.017 (calibrated so \$80 is optimal)

These are NOT elasticities - they're parameters in semi-log demand that produce realistic price levels.

**Internalized Cost (α = 250):**
- Calibrated to make observed prices profit-maximizing
- Reflects convex costs from crowd management, brand, experience
- Order of magnitude plausible but not directly measured

### 💭 EDUCATED GUESSES

**Marginal Costs:**
- Beer: \$5.00 (materials + labor + overhead)
- Tickets: \$3.50 (variable labor + cleaning)

**Basis**: Industry knowledge, reasonable cost accounting
**Not from**: Yankees financial data (proprietary)

---

## Impact on Results

**Robust findings** (insensitive to assumptions):
- Beer ceiling → tickets rise ✓
- Beer ceiling → stadium profit falls ✓
- Beer ceiling → consumption increases ✓

**Uncertain magnitudes** (sensitive to assumptions):
- Exact ticket price increase (3-6x multiplier)
- Exact welfare distribution
- Exact consumption levels

**Critical assumption**: Cross-elasticity 0.1
- If actually 0.2-0.3: Ticket response smaller, welfare effects different
- If actually 0.05: Current model reasonably accurate

---

## Literature Gap

**What we need but don't have:**

1. **Empirical cross-price elasticity estimates** between stadium tickets and beer
   - Could be estimated with panel data across stadiums
   - Or natural experiments (price changes)

2. **Stadium-specific demand estimates**
   - Yankees fans may differ from MLB average
   - NYC market effects

3. **Quantified internalized costs**
   - Actual crowd management costs per intoxication level
   - Brand value impact from incidents

**Until then**: Treat model as illustrative framework showing mechanisms, not precise predictions.

```{bibliography}
:filter: docname in docnames
```
