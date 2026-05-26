#!/usr/bin/env bash
set -euo pipefail

# Install the Python package when pip is available. If this environment has a
# Python without pip, sitecustomize.py still makes `python -m arena_cli.cli`
# work from the repository root.
if python -m pip --version >/dev/null 2>&1; then
  python -m pip install -e arena
else
  echo "python -m pip is unavailable; using local sitecustomize.py fallback for arena_cli" >&2
fi

if command -v npm >/dev/null 2>&1; then
  (cd packages/site && npm install)
else
  echo "npm not found; install Node.js to build the site" >&2
fi

python -m arena_cli.cli build-catalog
