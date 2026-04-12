"""maxwell.electromagnetism — Electromagnetic field theory (Part IV, Arts. 475-680).

Oersted's discovery, electromagnetic induction, Lorentz force,
Ampere-Maxwell law, electromagnetic energy, Maxwell stress tensor,
and the general field equations.
"""

from __future__ import annotations

from maxwell.electromagnetism.sources.oersted import (
    OerstedField,
    calc_oersted_field,
    calc_field_from_element,
    calc_force_on_pole,
    calc_circular_field_direction,
    verify_inverse_distance_law,
)

from maxwell.electromagnetism.induction.faraday import (
    MagneticFlux,
    InducedEMF,
    FaradayInduction,
    calc_magnetic_flux,
    calc_induced_emf,
    calc_motional_emf,
    calc_self_induction,
    verify_lenz_law,
)

from maxwell.electromagnetism.forces.lorentz import (
    LorentzForce,
    LorentzForceCalculator,
    calc_force_on_wire,
    calc_force_on_moving_charge,
    calc_force_between_parallel_currents,
    calc_torque_on_current_loop,
    calc_force_density,
    verify_parallel_current_attraction,
)

from maxwell.electromagnetism.forces.stress_tensor import (
    MaxwellStressTensor,
    calc_maxwell_stress_tensor,
    calc_electric_stress_tensor,
    calc_magnetic_stress_tensor,
    calc_electromagnetic_pressure,
    calc_surface_force,
    calc_force_on_surface,
    verify_stress_tensor_properties,
    analyze_stress_tensor,
)

from maxwell.electromagnetism.fields.ampere_maxwell import (
    DisplacementCurrent,
    AmpereMaxwellLaw,
    AmpereMaxwellCalculator,
    calc_ampere_law,
    calc_displacement_current,
    calc_ampere_maxwell,
    calc_total_current_density,
    verify_displacement_current_necessity,
)

from maxwell.electromagnetism.theory.general_equations import (
    # Data classes
    ElectromagneticField,
    MaxwellEquations,
    GeneralEquationsCalculator,
    # Core equation functions
    calc_faradays_law,
    calc_general_emf,
    calc_ponderomotive_force,
    calc_magnetic_induction,
    calc_ampere_maxwell as calc_ampere_maxwell_general,
    calc_electric_displacement,
    calc_conduction_current,
    calc_gauss_law_electric,
    calc_gauss_law_magnetic,
    # Vector calculus utilities
    numerical_divergence,
    numerical_curl,
    # Verification and analysis
    verify_maxwell_equations,
    analyze_complete_field,
)

from maxwell.electromagnetism.energy.electrostatic import (
    ElectrostaticEnergy,
    calc_electrostatic_energy_density,
    calc_total_electrostatic_energy,
    calc_capacitor_energy,
    calc_energy_in_dielectric,
    verify_electrostatic_energy_density,
    analyze_electrostatic_energy,
)

from maxwell.electromagnetism.energy.magnetic import (
    MagneticEnergy,
    calc_magnetic_energy_density,
    calc_magnetic_energy_density_from_B,
    calc_total_magnetic_energy,
    calc_inductor_energy,
    verify_magnetic_energy_density,
    analyze_magnetic_energy,
)

from maxwell.electromagnetism.energy.electrokinetic import (
    ElectrokineticEnergy,
    calc_electrokinetic_energy,
    calc_single_circuit_energy,
    calc_coupled_circuits_energy,
    calc_mutual_inductance_energy,
    calc_two_circuit_energy,
    calc_coupling_coefficient,
    verify_coupled_circuits_energy,
)

__all__ = [
    # Oersted (Arts. 475-479)
    "OerstedField",
    "calc_oersted_field",
    "calc_field_from_element",
    "calc_force_on_pole",
    "calc_circular_field_direction",
    "verify_inverse_distance_law",
    # Faraday (Arts. 528-531, 542)
    "MagneticFlux",
    "InducedEMF",
    "FaradayInduction",
    "calc_magnetic_flux",
    "calc_induced_emf",
    "calc_motional_emf",
    "calc_self_induction",
    "verify_lenz_law",
    # Lorentz (Arts. 490-492)
    "LorentzForce",
    "LorentzForceCalculator",
    "calc_force_on_wire",
    "calc_force_on_moving_charge",
    "calc_force_between_parallel_currents",
    "calc_torque_on_current_loop",
    "calc_force_density",
    "verify_parallel_current_attraction",
    # Maxwell Stress Tensor (Arts. 641-646)
    "MaxwellStressTensor",
    "calc_maxwell_stress_tensor",
    "calc_electric_stress_tensor",
    "calc_magnetic_stress_tensor",
    "calc_electromagnetic_pressure",
    "calc_surface_force",
    "calc_force_on_surface",
    "verify_stress_tensor_properties",
    "analyze_stress_tensor",
    # Ampere-Maxwell (Arts. 606-607)
    "DisplacementCurrent",
    "AmpereMaxwellLaw",
    "AmpereMaxwellCalculator",
    "calc_ampere_law",
    "calc_displacement_current",
    "calc_ampere_maxwell",
    "calc_total_current_density",
    "verify_displacement_current_necessity",
    # General Equations (Arts. 594-603)
    "ElectromagneticField",
    "MaxwellEquations",
    "GeneralEquationsCalculator",
    "calc_faradays_law",
    "calc_general_emf",
    "calc_ponderomotive_force",
    "calc_magnetic_induction",
    "calc_ampere_maxwell_general",
    "calc_electric_displacement",
    "calc_conduction_current",
    "calc_gauss_law_electric",
    "calc_gauss_law_magnetic",
    "numerical_divergence",
    "numerical_curl",
    "verify_maxwell_equations",
    "analyze_complete_field",
    # Electrostatic Energy (Arts. 630-631)
    "ElectrostaticEnergy",
    "calc_electrostatic_energy_density",
    "calc_total_electrostatic_energy",
    "calc_capacitor_energy",
    "calc_energy_in_dielectric",
    "verify_electrostatic_energy_density",
    "analyze_electrostatic_energy",
    # Magnetic Energy (Arts. 632-633)
    "MagneticEnergy",
    "calc_magnetic_energy_density",
    "calc_magnetic_energy_density_from_B",
    "calc_total_magnetic_energy",
    "calc_inductor_energy",
    "verify_magnetic_energy_density",
    "analyze_magnetic_energy",
    # Electrokinetic Energy (Arts. 634-638)
    "ElectrokineticEnergy",
    "calc_electrokinetic_energy",
    "calc_single_circuit_energy",
    "calc_coupled_circuits_energy",
    "calc_mutual_inductance_energy",
    "calc_two_circuit_energy",
    "calc_coupling_coefficient",
    "verify_coupled_circuits_energy",
]
