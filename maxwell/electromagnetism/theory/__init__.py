"""maxwell.electromagnetism.theory — General equations and theory of the electromagnetic field.

Maxwell's general equations in two representations:

- ``general_equations.py`` — Arts. 594-603, Heaviside/Gibbs split form
- ``quaternion_expressions.py`` — Arts. 618-619, unsplit ∇A = S∇A + V∇A

Related theory includes energy conservation, dynamical models, and
force law comparisons.
"""

from maxwell.electromagnetism.theory.comparisons import (
    compare_force_laws,
    verify_action_reaction,
)
from maxwell.electromagnetism.theory.conservation import (
    analyze_energy_conservation,
    verify_energy_conservation_rl,
)
from maxwell.electromagnetism.theory.dynamical_model import (
    calc_energy_density,
    calc_field_momentum,
    calc_poynting_vector,
)
from maxwell.electromagnetism.theory.quaternion_expressions import (
    Quaternion,
    impose_s_nabla_A_zero,
    magnetic_induction_from_potential,
    nabla_of_vector,
    scalar_part_of_potential,
    verify_nabla_quaternion_parts,
)
from maxwell.electromagnetism.theory.general_equations import (
    ElectromagneticField,
    GeneralEquationsCalculator,
    MaxwellEquations,
    analyze_complete_field,
    calc_ampere_maxwell,
    calc_conduction_current,
    calc_electric_displacement,
    calc_faradays_law,
    calc_gauss_law_electric,
    calc_gauss_law_magnetic,
    calc_general_emf,
    calc_magnetic_induction,
    calc_ponderomotive_force,
    numerical_curl,
    numerical_divergence,
    verify_maxwell_equations,
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
    # Quaternion nabla (Arts. 618-619) — unsplit object; S not assumed zero
    "Quaternion",
    "nabla_of_vector",
    "magnetic_induction_from_potential",
    "scalar_part_of_potential",
    "impose_s_nabla_A_zero",
    "verify_nabla_quaternion_parts",
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
