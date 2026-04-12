"""
Fields module — Maxwell's field theory of electromagnetism.

This module contains the implementation of Maxwell's field equations,
including the Ampere-Maxwell law with displacement current.

References:
    Part IV, Arts. 606-607: Ampere-Maxwell law and displacement current.
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

__all__ = [
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
]
