"""
Fields module — Maxwell's field theory of electromagnetism.

This module contains the implementation of Maxwell's field equations,
including the Ampere-Maxwell law with displacement current and electrotonic state.

References:
    Part IV, Arts. 606-607: Ampere-Maxwell law and displacement current.
    Part IV, Arts. 540-541: Electrotonic state (vector potential).
"""

from maxwell.electromagnetism.fields.ampere_maxwell import (
    AmpereMaxwellLaw,
    DisplacementCurrent,
    AmpereMaxwellCalculator,
    calc_ampere_law,
    calc_displacement_current,
    calc_ampere_maxwell,
    calc_magnetic_field_from_current,
    calc_total_current_density,
    verify_displacement_current_necessity,
    analyze_ampere_maxwell,
)

from maxwell.electromagnetism.fields.electrotonic import (
    ElectrotonicState,
    calc_electrotonic_uniform_field,
    calc_electrotonic_loop,
    calc_flux_from_electrotonic,
    verify_electrotonic_relations,
    analyze_electrotonic_state,
)

from maxwell.electromagnetism.fields.vector_momentum import (
    VectorPotential,
    calc_vector_potential_from_current,
    calc_vector_potential_wire,
    calc_vector_potential_dipole,
    calc_momentum_density,
    calc_total_momentum,
    verify_momentum_relations,
    verify_momentum_conservation,
    analyze_vector_potential,
)

from maxwell.electromagnetism.fields.curl_relation import (
    CurlRelations,
    verify_curl_relation,
    verify_curl_gradient_identity,
    verify_divergence_free_B,
    calc_curl,
    calc_divergence,
    verify_gauge_invariance,
    analyze_curl_relations,
)

__all__ = [
    # Ampere-Maxwell (Arts. 606-607)
    "AmpereMaxwellLaw",
    "DisplacementCurrent",
    "AmpereMaxwellCalculator",
    "calc_ampere_law",
    "calc_displacement_current",
    "calc_ampere_maxwell",
    "calc_magnetic_field_from_current",
    "calc_total_current_density",
    "verify_displacement_current_necessity",
    "analyze_ampere_maxwell",
    # Electrotonic State (Arts. 540-541)
    "ElectrotonicState",
    "calc_electrotonic_uniform_field",
    "calc_electrotonic_loop",
    "calc_flux_from_electrotonic",
    "verify_electrotonic_relations",
    "analyze_electrotonic_state",
    # Vector Momentum (Arts. 585-592)
    "VectorPotential",
    "calc_vector_potential_from_current",
    "calc_vector_potential_wire",
    "calc_vector_potential_dipole",
    "calc_momentum_density",
    "calc_total_momentum",
    "verify_momentum_relations",
    "verify_momentum_conservation",
    "analyze_vector_potential",
    # Curl Relations (Arts. 590-592)
    "CurlRelations",
    "verify_curl_relation",
    "verify_curl_gradient_identity",
    "verify_divergence_free_B",
    "calc_curl",
    "calc_divergence",
    "verify_gauge_invariance",
    "analyze_curl_relations",
]
