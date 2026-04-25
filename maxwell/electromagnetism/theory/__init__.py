"""maxwell.electromagnetism.theory — General equations and theory of the electromagnetic field.

Maxwell's general equations (Arts. 594-603) and related theory including
energy conservation, dynamical models, and force law comparisons.
"""

from maxwell.electromagnetism.theory.general_equations import (
    ElectromagneticField,
    MaxwellEquations,
    GeneralEquationsCalculator,
    calc_faradays_law,
    calc_general_emf,
    calc_ponderomotive_force,
    calc_magnetic_induction,
    calc_ampere_maxwell,
    calc_electric_displacement,
    calc_conduction_current,
    calc_gauss_law_electric,
    calc_gauss_law_magnetic,
    numerical_divergence,
    numerical_curl,
    verify_maxwell_equations,
    analyze_complete_field,
)

from maxwell.electromagnetism.theory.comparisons import (
    compare_force_laws,
    verify_action_reaction,
)

from maxwell.electromagnetism.theory.conservation import (
    verify_energy_conservation_rl,
    analyze_energy_conservation,
)

from maxwell.electromagnetism.theory.dynamical_model import (
    calc_energy_density,
    calc_poynting_vector,
    calc_field_momentum,
)

__all__ = [
    # General equations (Arts. 594-603)
    "ElectromagneticField",
    "MaxwellEquations",
    "GeneralEquationsCalculator",
    "calc_faradays_law",
    "calc_general_emf",
    "calc_ponderomotive_force",
    "calc_magnetic_induction",
    "calc_ampere_maxwell",
    "calc_electric_displacement",
    "calc_conduction_current",
    "calc_gauss_law_electric",
    "calc_gauss_law_magnetic",
    "numerical_divergence",
    "numerical_curl",
    "verify_maxwell_equations",
    "analyze_complete_field",
    # Force comparisons (Arts. 526-527)
    "compare_force_laws",
    "verify_action_reaction",
    # Energy conservation (Arts. 543-544)
    "verify_energy_conservation_rl",
    "analyze_energy_conservation",
    # Dynamical model (Arts. 568-577)
    "calc_energy_density",
    "calc_poynting_vector",
    "calc_field_momentum",
]
