#!/bin/bash
# Build PDF export from MyST documentation

set -e

cd "$(dirname "$0")/../docs"

echo "Building PDF from MyST documentation..."

# Build PDF (requires LaTeX/TexLive installed)
uv run myst build --pdf

echo ""
echo "PDF exports created in docs/_build/exports/"
ls -la _build/exports/*.pdf 2>/dev/null || echo "No PDFs found"
