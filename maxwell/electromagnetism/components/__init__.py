"""Electromagnetic components — Coil models and field calculators.

References:
    Part IV, Arts. 670-690: Circular coils.
    Part IV, Arts. 675-685: Solenoids.
    Part IV, Arts. 680-688: Cylindrical conductors.
"""

from maxwell.electromagnetism.components.circular_coils import (
    CircularCoil,
    calc_coil_on_axis,
    calc_coil_off_axis,
    calc_double_coil_field,
    calc_coaxial_coil_pair,
    verify_coil_field,
    verify_helmholtz_uniformity,
    analyze_circular_coil,
)

from maxwell.electromagnetism.components.solenoids import (
    Solenoid,
    calc_solenoid_field,
    calc_infinite_solenoid_field,
    calc_helmholtz_center,
    calc_helmholtz_uniformity,
    verify_solenoid_field,
    analyze_solenoid,
)

from maxwell.electromagnetism.components.cylinders import (
    CylindricalConductor,
    calc_cylindrical_field,
    calc_hollow_cylinder_field,
    calc_wire_self_inductance,
    calc_cylinder_vector_potential,
    verify_cylindrical_field,
    analyze_cylindrical_conductor,
)

__all__ = [
    # Circular coils (Arts. 670-690)
    "CircularCoil",
    "calc_coil_on_axis",
    "calc_coil_off_axis",
    "calc_double_coil_field",
    "calc_coaxial_coil_pair",
    "verify_coil_field",
    "verify_helmholtz_uniformity",
    "analyze_circular_coil",
    # Solenoids (Arts. 675-685)
    "Solenoid",
    "calc_solenoid_field",
    "calc_infinite_solenoid_field",
    "calc_helmholtz_center",
    "calc_helmholtz_uniformity",
    "verify_solenoid_field",
    "analyze_solenoid",
    # Cylindrical conductors (Arts. 680-688)
    "CylindricalConductor",
    "calc_cylindrical_field",
    "calc_hollow_cylinder_field",
    "calc_wire_self_inductance",
    "calc_cylinder_vector_potential",
    "verify_cylindrical_field",
    "analyze_cylindrical_conductor",
]
