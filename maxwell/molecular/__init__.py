"""maxwell.molecular — Molecular currents and competing theories (Arts. 832-866).

Package for Maxwell's treatment of molecular currents and alternative
electromagnetic theories including Weber's, Neumann's, and other formulations.
"""

from maxwell.molecular.amperes_theory import (
    AmperesTheory,
    MolecularCurrent,
    analyze_amperes_theory,
    calc_molecular_field,
    calc_molecular_moment,
    verify_amperes_theory,
)
from maxwell.molecular.competing_theories import (
    CompetingTheory,
    TheoryComparison,
    analyze_amperes_theory,
    analyze_neumanns_theory,
    analyze_theory_differences,
    analyze_webers_theory,
    compare_electromagnetic_theories,
    compare_theories,
    diamagnetic_response,
    maxwell_advantages,
    maxwells_theory_advantages,
    synthesize_theory_comparison,
    verify_theory_consistency,
)
from maxwell.molecular.neumanns_theory import (
    NeumannPotential,
    NeumannTheory,
    analyze_neumanns_theory,
    calc_mutual_inductance_neumann,
    calc_neumann_potential,
    circular_loop_inductance,
    mutual_potential_energy,
    neumann_mutual_inductance,
    verify_neumanns_theory,
)
from maxwell.molecular.webers_theory import (
    WeberForce,
    WebersTheory,
    analyze_webers_theory,
    calc_weber_force,
    calc_weber_potential,
    verify_webers_theory,
    weber_force,
    weber_potential,
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
    "weber_force",
    "weber_potential",
    "verify_webers_theory",
    "analyze_webers_theory",
    # Neumann's theory (Arts. 851-858)
    "NeumannTheory",
    "NeumannPotential",
    "calc_neumann_potential",
    "calc_mutual_inductance_neumann",
    "neumann_mutual_inductance",
    "circular_loop_inductance",
    "mutual_potential_energy",
    "verify_neumanns_theory",
    "analyze_neumanns_theory",
    # Competing theories comparison (Arts. 859-866)
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
