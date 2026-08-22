"""Default paths for the Maxwell page verifier.

PRODUCT = MAXWELL-MODERNIZED-PROGRAM/maxwell/ (Python package).
OCR / photos are separate trees (see README).

Paths are overridable via environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path

# Product root (this repo)
PRODUCT_ROOT = Path(
    os.environ.get(
        "MAXWELL_PRODUCT_ROOT",
        Path(__file__).resolve().parent.parent,
    )
)

# Mathpix / OCR volume JSON (primary: maxwell_em_processor)
OCR_ROOT = Path(
    os.environ.get(
        "MAXWELL_OCR_ROOT",
        r"C:\Users\antmi\Downloads\maxwell_em_processor",
    )
)

VOLUME_JSON = {
    1: OCR_ROOT / "MAXWELL_VOLUME_1_MASTER_OUTPUT" / "volume_1_direct_result.json",
    2: OCR_ROOT / "MAXWELL_VOLUME_2_MASTER_OUTPUT" / "volume_2_direct_result.json",
}

# Page photos (primary: maxwell-latex-books Third Edition)
BOOKS_ROOT = Path(
    os.environ.get(
        "MAXWELL_BOOKS_ROOT",
        r"C:\Users\antmi\maxwell-latex-books",
    )
)

IMAGE_SEARCH_ROOTS = [
    BOOKS_ROOT / "Third Edition",
    BOOKS_ROOT / "Third Edition" / "15773-A Treatise On Electricity And Magnetism Vol-i_images",
    BOOKS_ROOT / "Third Edition" / "15774-A Treatise On Electricity And Magnetism Vol-ii_images",
    OCR_ROOT / "MAXWELL_VOLUME_1_MASTER_OUTPUT",
    OCR_ROOT / "MAXWELL_VOLUME_2_MASTER_OUTPUT",
    OCR_ROOT / "input",
]

# Verdict persistence (inside product so it ships with the tool)
VERDICTS_DIR = Path(
    os.environ.get(
        "MAXWELL_VERDICTS_DIR",
        Path(__file__).resolve().parent / "data",
    )
)
VERDICTS_PATH = VERDICTS_DIR / "verdicts.json"
EXPORT_DIR = VERDICTS_DIR / "exports"

# Product source for math/code view
PRODUCT_SRC = PRODUCT_ROOT / "maxwell"

# Native TeX render cache (Mathpix OCR is already LaTeX)
LATEX_CACHE_DIR = Path(
    os.environ.get(
        "MAXWELL_LATEX_CACHE",
        Path(__file__).resolve().parent / "data" / "latex_cache",
    )
)
