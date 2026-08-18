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

from maxwell.electromagnetism.forces.elemental import (
    CurrentElement,
    analyze_elemental_forces,
    calc_ampere_force,
    calc_element_mutual_energy,
    calc_grassmann_force,
    calc_parallel_element_force,
    verify_force_equivalence,
)
from maxwell.electromagnetism.forces.generalized import (
    GeneralizedForce,
    analyze_generalized_forces,
    calc_force_coaxial_coils,
    calc_force_from_energy,
    calc_force_movable_coil,
    calc_force_on_dipole,
    calc_torque_on_loop,
    verify_generalized_forces,
)
from maxwell.electromagnetism.forces.lorentz import (
    LorentzForce,
    LorentzForceCalculator,
    analyze_lorentz_force,
    calc_force_between_parallel_currents,
    calc_force_density,
    calc_force_on_distribution,
    calc_force_on_moving_charge,
    calc_force_on_wire,
    calc_torque_on_current_loop,
    verify_parallel_current_attraction,
)
from maxwell.electromagnetism.forces.medium_force import (
    MediumForceCalculator,
    analyze_medium_forces,
    calc_dipole_force_near_wire,
    calc_magnetized_body_force,
    calc_medium_force,
    calc_permeable_medium_force,
    verify_magnetic_response,
    verify_medium_force,
)
from maxwell.electromagnetism.forces.ponderomotive import (
    PonderomotiveForce,
    analyze_ponderomotive_forces,
    calc_electric_force_density,
    calc_force_from_stress_tensor,
    calc_force_on_point_charge,
    calc_force_on_wire_ponderomotive,
    calc_magnetic_force_density,
    calc_ponderomotive_force,
    verify_ponderomotive_forces,
)
from maxwell.electromagnetism.forces.sliding import (
    SlidingConductor,
    analyze_sliding_conductor,
    calc_magnetic_braking_force,
    calc_motional_emf_arbitrary,
    calc_motional_emf_sliding,
    calc_power_dissipation,
    verify_motional_emf,
)
from maxwell.electromagnetism.forces.stress_tensor import (
    MaxwellStressTensor,
    analyze_stress_tensor,
    calc_electric_stress_tensor,
    calc_electromagnetic_pressure,
    calc_field_line_pressure,
    calc_field_line_tension,
    calc_force_density_from_stress,
    calc_force_on_conductor,
    calc_force_on_surface,
    calc_magnetic_stress_tensor,
    calc_maxwell_stress_tensor,
    calc_surface_force,
    verify_stress_tensor_properties,
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
    # Elemental forces (Arts. 510-515)
    "CurrentElement",
    "calc_ampere_force",
    "calc_grassmann_force",
    "calc_element_mutual_energy",
    "verify_force_equivalence",
    "calc_parallel_element_force",
    "analyze_elemental_forces",
    # Generalized forces (Arts. 573-578)
    "GeneralizedForce",
    "calc_force_from_energy",
    "calc_force_movable_coil",
    "calc_torque_on_loop",
    "calc_force_on_dipole",
    "calc_force_coaxial_coils",
    "verify_generalized_forces",
    "analyze_generalized_forces",
    # Ponderomotive forces (Arts. 494-499)
    "PonderomotiveForce",
    "calc_electric_force_density",
    "calc_magnetic_force_density",
    "calc_ponderomotive_force",
    "calc_force_on_point_charge",
    "calc_force_on_wire_ponderomotive",
    "calc_force_from_stress_tensor",
    "verify_ponderomotive_forces",
    "analyze_ponderomotive_forces",
    # Sliding conductor (Arts. 536-539)
    "SlidingConductor",
    "calc_motional_emf_sliding",
    "calc_magnetic_braking_force",
    "calc_power_dissipation",
    "calc_motional_emf_arbitrary",
    "verify_motional_emf",
    "analyze_sliding_conductor",
    # Medium forces (Arts. 639-640)
    "MediumForceCalculator",
    "calc_medium_force",
    "calc_magnetized_body_force",
    "calc_permeable_medium_force",
    "calc_dipole_force_near_wire",
    "verify_medium_force",
    "verify_magnetic_response",
    "analyze_medium_forces",
]
