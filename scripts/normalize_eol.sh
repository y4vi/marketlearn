#!/usr/bin/env bash
set -euo pipefail

echo "Normalizing line endings to LF for .py, .sh, .md, .env* files..."

find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name ".env*" \) -not -path "./.git/*" -print0 \
  | xargs -0 -n1 perl -pi -e 's/\r\n/\n/g'

echo "Done."
