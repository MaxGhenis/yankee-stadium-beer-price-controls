#!/bin/bash
# Clean rebuild of documentation (no caching issues)

set -e

echo "🧹 Cleaning old build artifacts..."
rm -rf docs/_build

echo "📊 Updating documentation values from model..."
python3 scripts/update_docs_values.py

echo "📈 Regenerating charts..."
python3 src/price_ceiling_analysis.py

echo "📚 Building documentation..."
cd docs && myst build --html

echo ""
echo "✓ Clean rebuild complete!"
echo ""
echo "View at: http://localhost:3003"
echo "Tip: Hard refresh browser (Cmd+Shift+R) to avoid cache"
