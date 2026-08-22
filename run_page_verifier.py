#!/usr/bin/env python3
"""Launch the Maxwell page Yes/No verifier (fast HTML/CSS server).

Usage (from product root):
    python run_page_verifier.py
    python -m page_verifier.server

Opens http://127.0.0.1:8765/
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    from page_verifier.server import main as server_main

    server_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
