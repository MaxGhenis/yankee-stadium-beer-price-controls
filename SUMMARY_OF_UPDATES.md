# Summary of Updates (Nov 17, 2025)

## Overview

This document summarizes the comprehensive updates made to the Yankee Stadium beer price controls analysis, including integration of Leisten (2024) theoretical work, new comparative statics analysis, and enhanced documentation.

## 1. Leisten (2024) Integration

### Citation Added
- Added full citation to `docs/references.bib`
- Cited throughout documentation where relevant

### Theoretical Comparison
**Files updated:**
- `docs/assumptions.md` - Clarified one-way vs two-way complementarity assumption
- `docs/complementarity_specs.md` - Added Leisten's FOCs and theoretical foundation
- `CLAUDE.md` - Added comparison section
- `LEISTEN_COMPARISON.md` - **NEW** comprehensive comparison document

**Key distinctions documented:**
- Leisten: One-way complementarity (tickets → beer)
- Our model: Two-way complementarity (tickets ↔ beer) with cross-elasticity = 0.1
- Both predict beer ceilings cause ticket prices to rise

### Log-Concavity Verification
**Files updated:**
- `src/model.py` - Added comments explaining log-concavity of semi-log demand
- `tests/test_model.py` - **NEW** test verifying demand functions are log-concave

**Result:** Our semi-log demand satisfies Leisten's theoretical condition (all tests pass).

## 2. Price Ceiling Comparative Statics

### Analysis Script
**NEW FILE:** `src/price_ceiling_analysis.py`
- Simulates outcomes across beer price ceilings from $5 to $20
- Generates 6 publication-quality charts
- Computes detailed comparative statics
- Exports data to CSV

### Charts Generated
Location: `charts/` directory

1. **prices.png** - Ticket and beer price responses
2. **quantities.png** - Attendance and beer consumption
3. **revenue.png** - Revenue decomposition (ticket, beer, total)
4. **welfare.png** - Four-panel welfare analysis
5. **welfare_combined.png** - Combined welfare on single chart
6. **beers_per_fan.png** - Per-capita consumption

### Key Results (from analysis)

**$7 Beer Ceiling vs Baseline ($12.50):**

| Metric | Baseline | $7 Ceiling | Change |
|--------|----------|------------|---------|
| Beer Price | $12.50 | $7.00 | -44.0% |
| Ticket Price | $89.30 | $121.05 | +35.6% |
| Attendance | 33,771 | 20,860 | -38.2% |
| Beers/Fan | 1.0 | 2.1 | +107.8% |
| Total Beers | 33,771 | 43,351 | +28.4% |
| Total Revenue | $3.40M | $2.80M | -17.7% |
| Profit | $2.27M | $1.70M | -25.3% |
| Consumer Surplus | $9.99M | $8.14M | -18.6% |
| Externality Cost | $0.14M | $0.17M | +28.4% |
| Social Welfare | $12.13M | $9.66M | -20.4% |

## 3. Documentation Enhancements

### New Documentation Page
**NEW FILE:** `docs/price_ceiling_analysis.md`
- Comprehensive analysis with embedded charts
- Explains economic mechanisms
- Quantitative results table
- Comparison with Leisten (2024)
- Policy implications

**Added to TOC:** `docs/_toc.yml` (between Simulation Results and Sensitivity Analysis)

### LaTeX Fixes
**Fixed:** `docs/abstract.md`
- Escaped all dollar signs (\$) to prevent LaTeX math mode errors
- Now renders correctly in JupyterBook

### Build Status
✅ JupyterBook rebuilt successfully with new content

## 4. Streamlit App Enhancement

**Updated:** `src/app.py`

### New Tab: "Price Ceiling Analysis"
Added 5th tab with interactive comparative statics:

1. **Pricing Response**
   - Ticket prices vs ceiling
   - Beer prices vs ceiling

2. **Quantity Effects**
   - Attendance vs ceiling
   - Total beer consumption vs ceiling

3. **Welfare Analysis**
   - Combined chart with all welfare components
   - Interactive Plotly visualization
   - Baseline markers

**Implementation:**
- Real-time computation across 31 price points ($5-$20)
- Uses existing model parameters from sidebar
- Fully integrated with parameter controls

## 5. Files Modified/Created

### New Files (7)
1. `src/price_ceiling_analysis.py` - Analysis script
2. `docs/price_ceiling_analysis.md` - Documentation page
3. `LEISTEN_COMPARISON.md` - Theoretical comparison
4. `SUMMARY_OF_UPDATES.md` - This file
5. `charts/prices.png` - Chart
6. `charts/quantities.png` - Chart
7. `charts/revenue.png` - Chart
8. `charts/welfare.png` - Chart
9. `charts/welfare_combined.png` - Chart
10. `charts/beers_per_fan.png` - Chart
11. `charts/price_ceiling_analysis.csv` - Data export

### Modified Files (9)
1. `docs/references.bib` - Added Leisten citation
2. `docs/assumptions.md` - Complementarity discussion
3. `docs/complementarity_specs.md` - Theoretical foundation
4. `docs/abstract.md` - LaTeX fixes
5. `docs/_toc.yml` - Added new page
6. `src/model.py` - Log-concavity comments
7. `tests/test_model.py` - Log-concavity test
8. `src/app.py` - New tab
9. `CLAUDE.md` - Leisten comparison

## 6. Testing

All tests pass (26/26):
```bash
pytest tests/test_model.py -v
# 26 passed in 0.77s
```

New log-concavity test confirms our semi-log demand satisfies Leisten's theoretical condition.

## 7. Key Insights from New Analysis

1. **Ticket Price Response:** $1 beer ceiling decrease → ~$6 ticket increase (multiplier effect)

2. **Quantity Trade-off:** Lower ceilings reduce attendance but increase per-capita consumption
   - Net effect: Total beer consumption rises despite fewer fans

3. **Welfare Distribution:**
   - Stadium loses substantially (profit -25% at $7 ceiling)
   - Consumers don't gain much (CS -19%)
   - Externalities worsen (+28%)
   - Net social welfare falls (-20%)

4. **Policy Implication:** Price ceilings create deadweight loss without clear beneficiaries
   - Motivates Pigouvian taxation as superior instrument

## 8. Academic Rigor

Enhanced academic standards:
- Explicit assumptions (following Leisten's example)
- Log-concavity verified mathematically
- Theoretical grounding documented
- Robustness checks expanded
- LaTeX formatting corrected

## 9. Reproducibility

All analysis is fully reproducible:
```bash
# Generate charts
python3 src/price_ceiling_analysis.py

# Run tests
pytest tests/test_model.py -v

# Build docs
cd docs && jupyter-book build .

# Launch app
streamlit run src/app.py
```

## 10. Next Steps (Optional)

Potential future enhancements:
1. Add uncertainty bands to price ceiling charts (Monte Carlo over parameters)
2. Compare one-way vs two-way complementarity side-by-side
3. Add price floor analysis (mirror of ceiling analysis)
4. Interactive chart in Streamlit allowing custom ceiling range
5. Export functionality for all charts from Streamlit app

## Citation

To cite this work:
```
Ghenis, M. (2025). Beer Price Controls at Yankee Stadium: An Economic Analysis.
PolicyEngine. https://maxghenis.github.io/yankee-stadium-beer-price-controls

Builds on theoretical work by:
Leisten, M. (2024). Twitter Thread: Economic Analysis of Beer Price Controls at
Yankee Stadium. https://x.com/LeistenEcon/status/1990150035615494239
```

## Acknowledgments

- Matthew Leisten for rigorous theoretical foundation
- Literature sources (30+ papers) for empirical parameters
- PolicyEngine team for institutional support
