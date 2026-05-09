"""maxwell.magneto_optics — Magneto-optics (Arts. 806-821).

Faraday rotation, circular polarization in magnetic media,
and energy analysis of the luminiferous medium.
"""

from __future__ import annotations

from maxwell.magneto_optics.circular_polarization import (
    CircularlyPolarizedRay,
    calc_circular_velocity_split,
    calc_magnetic_velocity_split,
    calc_natural_velocity_split,
    define_light_vector,
    derive_circular_kinematics,
    perform_kinematic_analysis,
)
from maxwell.magneto_optics.energy_analysis import (
    MagnetoOpticMedium,
    prove_real_rotation_required,
    summarize_magneto_optic_results,
)
from maxwell.magneto_optics.rotation import (
    FaradayRotator,
    VerdetTable,
    apply_verdet_negative_rotation,
    establish_rotation_laws,
    model_natural_rotation,
)

__all__ = [
    # Rotation (Arts. 806-810)
    "FaradayRotator",
    "VerdetTable",
    "establish_rotation_laws",
    "apply_verdet_negative_rotation",
    "model_natural_rotation",
    # Circular polarization (Arts. 811-817)
    "CircularlyPolarizedRay",
    "perform_kinematic_analysis",
    "calc_circular_velocity_split",
    "calc_natural_velocity_split",
    "calc_magnetic_velocity_split",
    "define_light_vector",
    "derive_circular_kinematics",
    # Energy analysis (Arts. 818-821)
    "MagnetoOpticMedium",
    "prove_real_rotation_required",
    "summarize_magneto_optic_results",
]
