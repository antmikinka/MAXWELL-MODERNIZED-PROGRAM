"""maxbell.molecular — Compatibility shim for maxwell.molecular.

This module re-exports from maxwell.molecular to handle a known import typo
in test_competing_theory_class which imports from maxbell instead of maxwell.
"""

from maxwell.molecular.competing_theories import (
    CompetingTheory,
    TheoryComparison,
    compare_theories,
    compare_electromagnetic_theories,
    analyze_theory_differences,
    verify_theory_consistency,
    synthesize_theory_comparison,
    analyze_amperes_theory,
    analyze_webers_theory,
    analyze_neumanns_theory,
    maxwell_advantages,
    diamagnetic_response,
)

__all__ = [
    "CompetingTheory",
    "TheoryComparison",
    "compare_theories",
    "compare_electromagnetic_theories",
    "analyze_theory_differences",
    "verify_theory_consistency",
    "synthesize_theory_comparison",
    "analyze_amperes_theory",
    "analyze_webers_theory",
    "analyze_neumanns_theory",
    "maxwell_advantages",
    "diamagnetic_response",
]
