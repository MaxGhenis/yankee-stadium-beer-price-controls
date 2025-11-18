# Maintaining Documentation Values

## Overview

Documentation values are **automatically generated from the model** to ensure consistency.

## The System

### How It Works

1. **Template**: Docs use `{{ placeholders }}` like `{{ ceiling7_ticket }}`
2. **Generate**: Script runs model and replaces placeholders with actual values
3. **Build**: MyST builds docs with real numbers

### Automation

**Pre-commit Hook** (`.git/hooks/pre-commit`):
- Automatically runs when you commit model changes
- Updates docs before committing
- Ensures docs always match code

**CI/CD** (`.github/workflows/ci.yml`):
- New `docs` job validates documentation
- Fails if values are outdated
- Builds docs on every push

**Pre-commit Framework** (`.pre-commit-config.yaml`):
- Optional: `pre-commit install` for more hooks
- Includes ruff, black, and doc updates

## Manual Usage

```bash
# Update docs after model changes
python scripts/update_docs_values.py

# Build docs
myst build --html

# Or both at once
python scripts/update_docs_values.py && cd docs && myst build --html
```

## What Gets Updated

All these values are auto-generated:
- `{{ baseline_ticket }}` = $70.44
- `{{ baseline_beer }}` = $12.51
- `{{ ceiling7_ticket }}` = $77.29
- `{{ ceiling7_ticket_pct }}` = 9.7
- `{{ ceiling7_attendance_pct }}` = -5.7
- `{{ pigouvian_revenue_annual }}` = 11.0
- And 16 more...

## Why This Approach

**Jupyter Book 2 beta doesn't support `myst_substitutions` yet**, so we:
- Pre-generate markdown before building
- Keep system simple and transparent
- Can switch to native substitutions when JB2 adds support

## Workflow Example

```bash
# 1. Modify model
vim src/model.py

# 2. Run tests
pytest tests/

# 3. Update docs (automatic on commit, or manual)
python scripts/update_docs_values.py

# 4. Build docs to preview
cd docs && myst build --html

# 5. Commit (hook runs update_docs_values.py automatically)
git add src/model.py docs/*.md
git commit -m "Update model parameters"

# 6. CI validates docs are up-to-date
git push  # Docs job checks for uncommitted changes
```

## Troubleshooting

**Docs out of sync?**
```bash
python scripts/update_docs_values.py
git add docs/*.md
```

**Want to see what would change?**
```bash
python scripts/update_docs_values.py --dry-run  # TODO: Add this flag
```

**CI failing on docs?**
```
⚠️  Documentation values were updated but not committed!
```
Solution: Run `python scripts/update_docs_values.py` and commit the changes.

## Benefits

✓ **Impossible to have wrong numbers** - all come from model code
✓ **Automatic updates** - pre-commit hook handles it
✓ **CI validation** - fails if docs out of sync
✓ **Git history** - see when numbers change
✓ **Transparent** - clear what values come from where
