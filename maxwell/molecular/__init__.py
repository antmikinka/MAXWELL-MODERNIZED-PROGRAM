"""maxwell.molecular — Molecular currents and competing theories (Arts. 832-866).

Package for Maxwell's treatment of molecular currents and alternative
electromagnetic theories including Weber's, Neumann's, and other formulations.
"""

from maxwell.molecular.amperes_theory import (
    AmperesTheory,
    MolecularCurrent,
    calc_molecular_moment,
    calc_molecular_field,
    verify_amperes_theory,
    analyze_amperes_theory,
)

from maxwell.molecular.webers_theory import (
    WebersTheory,
    WeberForce,
    calc_weber_force,
    calc_weber_potential,
    verify_webers_theory,
    analyze_webers_theory,
)

from maxwell.molecular.neumanns_theory import (
    NeumannsTheory,
    NeumannPotential,
    calc_neumann_potential,
    calc_mutual_inductance_neumann,
    verify_neumanns_theory,
    analyze_neumanns_theory,
)

from maxwell.molecular.competing_theories import (
    CompetingTheory,
    TheoryComparison,
    compare_electromagnetic_theories,
    analyze_theory_differences,
    verify_theory_consistency,
    synthesize_theory_comparison,
)

__all__ = [
    # Ampere's theory (Arts. 832-840)
    "AmperesTheory",
    "MolecularCurrent",
    "calc_molecular_moment",
    "calc_molecular_field",
    "verify_amperes_theory",
    "analyze_amperes_theory",

    # Weber's theory (Arts. 841-850)
    "WebersTheory",
    "WeberForce",
    "calc_weber_force",
    "calc_weber_potential",
    "verify_webers_theory",
    "analyze_webers_theory",

    # Neumann's theory (Arts. 851-858)
    "NeumannsTheory",
    "NeumannPotential",
    "calc_neumann_potential",
    "calc_mutual_inductance_neumann",
    "verify_neumanns_theory",
    "analyze_neumanns_theory",

    # Competing theories comparison (Arts. 859-866)
    "CompetingTheory",
    "TheoryComparison",
    "compare_electromagnetic_theories",
    "analyze_theory_differences",
    "verify_theory_consistency",
    "synthesize_theory_comparison",
]
