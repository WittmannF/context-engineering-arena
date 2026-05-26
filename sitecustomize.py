"""Local development helper.

When commands are run from the repository root, this makes `python -m arena_cli.cli`
work even before the package is installed editable.
"""
from pathlib import Path
import sys
arena = Path(__file__).resolve().parent / "arena"
if arena.exists() and str(arena) not in sys.path:
    sys.path.insert(0, str(arena))
