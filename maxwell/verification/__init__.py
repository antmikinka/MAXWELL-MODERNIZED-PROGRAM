"""maxwell.verification — Equation extraction and verification against JSON sources."""

from __future__ import annotations

from maxwell.verification.equation_extractor import EquationExtractor
from maxwell.verification.equation_registry import EquationRegistry
from maxwell.verification.verifier import EquationVerifier

__all__ = [
    "EquationExtractor",
    "EquationRegistry",
    "EquationVerifier",
]
