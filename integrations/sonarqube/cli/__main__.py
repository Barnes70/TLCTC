"""Entrypoint for `python -m cli` (or `python -m tlctc_sonar` if symlinked)."""

import sys

from .tlctc_sonar import main

if __name__ == "__main__":
    sys.exit(main())
