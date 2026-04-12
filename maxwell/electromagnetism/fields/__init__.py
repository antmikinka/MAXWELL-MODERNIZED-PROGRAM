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
]
