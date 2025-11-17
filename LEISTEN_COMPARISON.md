# Comparison with Leisten (2025) Theoretical Analysis

## Summary

Matthew Leisten's rigorous Twitter thread ([link](https://x.com/LeistenEcon/status/1990150035615494239)) provides theoretical foundation for our quantitative model. We've updated our codebase to cite his work and clarify our extensions.

## Key Revisions Made

### 1. Added Citation
- Added Leisten (2025) to `docs/references.bib`
- Cited throughout documentation where relevant

### 2. Clarified Complementarity Assumption
**Files updated:**
- `docs/assumptions.md`: Added section comparing one-way (Leisten) vs two-way (our model) complementarity
- `docs/complementarity_specs.md`: Added theoretical foundation section with Leisten's FOCs and result

**Key distinction:**
- **Leisten**: Beer prices DON'T affect ticket demand (one-way: tickets → beer)
- **Our model**: Beer prices DO affect ticket demand (two-way: tickets ↔ beer)
- Both predict beer ceilings cause ticket prices to rise

### 3. Verified Log-Concavity
**Files updated:**
- `src/model.py`: Added comments explaining log-concavity of semi-log demand
- `tests/test_model.py`: Added `test_log_concavity_of_demand()` to verify our functional forms satisfy Leisten's condition

**Result:** Our semi-log demand is log-concave (ln(Q) is linear in P, thus concave), satisfying Leisten's theoretical requirement.

### 4. Updated Documentation
**Files updated:**
- `CLAUDE.md`: Added "Comparison to Leisten (2025)" section
- Explains how our quantitative calibration extends his theoretical result

## What We Agree On

Both models predict:
1. ✅ Beer price ceilings cause ticket prices to rise
2. ✅ Complementarity between tickets and beer is key mechanism
3. ✅ Log-concavity is critical for the result

## What We Add

Our model extends Leisten's work by:
1. **Quantitative calibration**: Predicts magnitude, not just sign ($7 ceiling → $32 ticket increase)
2. **Two-way complementarity**: Beer prices affect ticket demand (more realistic)
3. **Realistic costs**: Marginal costs, taxes, internalized externalities
4. **Welfare analysis**: Consumer surplus, externalities, optimal policy
5. **Empirical grounding**: Literature-based elasticities, real stadium data

## What Leisten Adds

Leisten's contribution:
1. **Rigorous proof**: Under log-concavity, dp_x/dZ < 0 (tickets rise when ceiling tightens)
2. **Explicit assumptions**: All assumptions stated upfront
3. **Mathematical clarity**: Shows log-concavity (seemingly innocuous) is critical
4. **Robustness**: Result holds for general functional forms, not specific calibration

## Complementary Approaches

- **Leisten**: "Can this happen theoretically?" → Yes, under standard assumptions
- **Our model**: "How big is the effect and what should policy do?" → Quantitative answers

Both approaches are valuable. Leisten proves theoretical possibility; we provide policy-relevant magnitudes.

## Testing

All tests pass, including new `test_log_concavity_of_demand()` which verifies our semi-log demand satisfies Leisten's theoretical condition:

```bash
pytest tests/test_model.py::TestStadiumSpecificFeatures::test_log_concavity_of_demand -v
# PASSED
```

## Files Modified

1. `docs/references.bib` - Added Leisten citation
2. `docs/assumptions.md` - Clarified complementarity assumption with Leisten comparison
3. `docs/complementarity_specs.md` - Added theoretical foundation section
4. `src/model.py` - Added log-concavity comments
5. `tests/test_model.py` - Added log-concavity test
6. `CLAUDE.md` - Added Leisten comparison section

## Acknowledgment

We're grateful to Matthew Leisten for rigorous theoretical analysis that validates our modeling approach and highlights the importance of log-concavity assumption.
