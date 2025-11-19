# MyST Substitutions Guide

This project uses MyST substitutions to keep documentation values consistent with the model.

## How It Works

1. **Generate values**: Run `python scripts/generate_model_values.py`
2. **Use in docs**: Reference like `70.44` in any markdown file
3. **Build**: MyST automatically replaces with current model values

## Available Substitutions

### Baseline (Profit-Maximizing)
- `70.44` - Optimal ticket price
- `12.51` - Optimal beer price
- `46,537` - Total attendance
- `1.00` - Average beers per fan
- `276.9` - Profit per season

### $7 Beer Ceiling
- `77.29` - Ticket price under $7 ceiling
- `9.7` - Ticket price % increase
- `-5.7` - Attendance % change
- `98.3` - Total beer consumption % change
- `2.10` - Beers per fan
- `110.2` - Beers per fan % change
- `-24.9` - Profit change per season

### Externalities & Taxes
- `4.00` - External cost per beer
- `1.09` - Current tax per beer
- `2.91` - Pigouvian tax gap
- `11.0` - Annual Pigouvian revenue potential

### Other Values
- `1.24` - Ticket/beer price multiplier
- `94.84` - Ticket price under $5 ceiling
- Full list in `docs/_config.yml` under `myst_substitutions`

## Example Usage

```markdown
The baseline ticket price is $70.44 with beer at $12.51.

A $7 beer ceiling increases ticket prices by 9.7%,
causing attendance to fall -5.7%.

The Pigouvian tax could raise $11.0M annually.
```

## Benefits

1. **Consistency**: All docs use same model values
2. **Automatic updates**: Re-run script when model changes
3. **No manual errors**: No need to find/replace numbers across files
4. **Transparency**: Values come directly from model code

## Updating Values

Whenever you modify the model:
```bash
python scripts/generate_model_values.py
myst build --html
```
