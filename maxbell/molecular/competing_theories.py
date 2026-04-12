"""maxbell.molecular.competing_theories — Compatibility shim.

Re-exports from maxwell.molecular.competing_theories.
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
    maxwells_theory_advantages,
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
    "maxwells_theory_advantages",
    "diamagnetic_response",
]
