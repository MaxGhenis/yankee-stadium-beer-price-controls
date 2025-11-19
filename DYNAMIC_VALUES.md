# Dynamic Model Values in Documentation

## Problem Solved

Documentation was inconsistent with model predictions:
- **Abstract claimed**: $200 tickets, 73% attendance drop
- **Model actually predicts**: $77 tickets, 6% attendance drop
- **Multiplier was 20x off!**

## Solution: MyST Substitutions

All model values are now **programmatically generated** and automatically inserted into docs.

## Usage

### 1. Generate Current Values
```bash
python scripts/generate_model_values.py
```

This runs the model and updates `docs/_config.yml` with all current predictions.

### 2. Use in Markdown

Instead of hardcoding:
```markdown
A $7 ceiling increases tickets to $77 (+10%)
```

Use substitutions:
```markdown
A $7 ceiling increases tickets to ${{ ceiling7_ticket }} (+{{ ceiling7_ticket_pct }}%)
```

### 3. Build Documentation
```bash
cd docs && myst build --html
```

MyST automatically replaces `{{ variable }}` with current model values.

## Available Values

See `docs/SUBSTITUTIONS.md` for full list. Key ones:

**Baseline:**
- `{{ baseline_ticket }}` = $70.44
- `{{ baseline_beer }}` = $12.51
- `{{ baseline_profit_season }}` = $276.9M

**$7 Ceiling:**
- `{{ ceiling7_ticket }}` = $77.29
- `{{ ceiling7_ticket_pct }}` = 9.7%
- `{{ ceiling7_attendance_pct }}` = -5.7%
- `{{ ceiling7_beers_pct }}` = 98.3%
- `{{ ceiling7_profit_change_season }}` = -$24.9M

**Taxes:**
- `{{ pigouvian_revenue_annual }}` = $11.0M (not $6.7M!)
- `{{ external_cost }}` = $4.00
- `{{ pigouvian_gap }}` = $2.91

## Benefits

1. **Consistency**: Impossible to have mismatched numbers
2. **Automatic**: Model changes propagate to all docs
3. **Transparency**: Values come directly from code
4. **Reviewable**: Git diffs show when numbers change

## Example: Abstract Fixed

**Before (hardcoded, wrong):**
```markdown
The ceiling induces the stadium to raise ticket prices to $200 (+150%),
causing attendance to fall 73%.
```

**After (dynamic, correct):**
```markdown
The ceiling induces the stadium to raise ticket prices to ${{ ceiling7_ticket }}
(+{{ ceiling7_ticket_pct }}%), causing attendance to fall {{ ceiling7_attendance_pct }}%.
```

**Renders as:**
```
The ceiling induces the stadium to raise ticket prices to $77.29
(+9.7%), causing attendance to fall -5.7%.
```

## Workflow

When you modify the model:
```bash
# 1. Update model code
vim src/model.py

# 2. Regenerate values
python scripts/generate_model_values.py

# 3. Rebuild docs
cd docs && myst build --html

# 4. Commit both code and config
git add src/model.py docs/_config.yml
git commit -m "Update model parameters"
```

## Implementation Details

- Values stored in: `docs/_config.yml` under `myst_substitutions`
- Generator script: `scripts/generate_model_values.py`
- MyST extension: `substitution` (enabled in config)
- Syntax: Jinja2-style `{{ variable }}`

## Next Steps

1. Convert remaining hardcoded values to substitutions
2. Add more scenarios (social optimum, etc.)
3. Consider adding confidence intervals from Monte Carlo
4. Automate in pre-commit hook or CI

## References

- [MyST Substitutions Docs](https://mystmd.org/guide/substitutions)
- [Jinja2 Template Syntax](https://jinja.palletsprojects.com/en/3.0.x/templates/)
