"""
Forces in electromagnetic fields — Lorentz force and Maxwell stress tensor.

This module implements the force laws for currents and charges in
electromagnetic fields, as described by Maxwell in Part IV:

- Lorentz force on currents and charges (Arts. 490-492)
- Maxwell stress tensor and electromagnetic stress (Arts. 641-646)

References:
    Part IV, Arts. 490-492: Lorentz force on currents and charges.
    Part IV, Arts. 641-646: Maxwell stress tensor and force transmission.
"""

from maxwell.electromagnetism.forces.lorentz import (
    LorentzForce,
    LorentzForceCalculator,
    calc_force_on_wire,
    calc_force_on_moving_charge,
    calc_force_between_parallel_currents,
    calc_torque_on_current_loop,
    calc_force_density,
    calc_force_on_distribution,
    analyze_lorentz_force,
    verify_parallel_current_attraction,
)

from maxwell.electromagnetism.forces.stress_tensor import (
    MaxwellStressTensor,
    calc_maxwell_stress_tensor,
    calc_electric_stress_tensor,
    calc_magnetic_stress_tensor,
    calc_electromagnetic_pressure,
    calc_force_density_from_stress,
    calc_surface_force,
    calc_force_on_surface,
    calc_field_line_tension,
    calc_field_line_pressure,
    verify_stress_tensor_properties,
    analyze_stress_tensor,
    calc_force_on_conductor,
)

__all__ = [
    # Lorentz force (Arts. 490-492)
    "LorentzForce",
    "LorentzForceCalculator",
    "calc_force_on_wire",
    "calc_force_on_moving_charge",
    "calc_force_between_parallel_currents",
    "calc_torque_on_current_loop",
    "calc_force_density",
    "calc_force_on_distribution",
    "analyze_lorentz_force",
    "verify_parallel_current_attraction",
    # Maxwell stress tensor (Arts. 641-646)
    "MaxwellStressTensor",
    "calc_maxwell_stress_tensor",
    "calc_electric_stress_tensor",
    "calc_magnetic_stress_tensor",
    "calc_electromagnetic_pressure",
    "calc_force_density_from_stress",
    "calc_surface_force",
    "calc_force_on_surface",
    "calc_field_line_tension",
    "calc_field_line_pressure",
    "verify_stress_tensor_properties",
    "analyze_stress_tensor",
    "calc_force_on_conductor",
]
