"""
Energy in the Electromagnetic Field — Maxwell's energy formulation.

This module implements Maxwell's theory of energy storage and distribution
in electromagnetic fields, as described in Part IV, Chapter XXI (Arts. 630-640):

- Electrostatic energy: u = (1/8π) E·D (Art. 630-631)
- Magnetic energy: u = (1/8π) B·H (Art. 632-633)
- Electrokinetic energy: T = (1/2) ∫ A·J dV (Art. 634-638)

References:
    Part IV, Arts. 630-640: Energy in electromagnetic fields.
"""

from maxwell.electromagnetism.energy.electrostatic import (
    # Data class
    ElectrostaticEnergy,
    # Core functions
    calc_electrostatic_energy_density,
    calc_total_electrostatic_energy,
    calc_capacitor_energy,
    calc_energy_in_dielectric,
    calc_energy_density_from_ED_dot,
    # Analysis and verification
    verify_electrostatic_energy_density,
    analyze_electrostatic_energy,
    integrate_energy_density,
)

from maxwell.electromagnetism.energy.magnetic import (
    # Data classes
    MagneticEnergy,
    # Core functions
    calc_magnetic_energy_density,
    calc_magnetic_energy_density_from_B,
    calc_total_magnetic_energy,
    calc_inductor_energy,
    calc_energy_in_magnetic_material,
    calc_energy_density_from_BH_dot,
    # Analysis and verification
    verify_magnetic_energy_density,
    analyze_magnetic_energy,
    integrate_magnetic_energy_density,
)

from maxwell.electromagnetism.energy.electrokinetic import (
    # Data class
    ElectrokineticEnergy,
    # Core functions
    calc_electrokinetic_energy,
    calc_single_circuit_energy,
    calc_coupled_circuits_energy,
    calc_mutual_inductance_energy,
    calc_two_circuit_energy,
    calc_coupling_coefficient,
    # Analysis and verification
    analyze_electrokinetic_energy,
    verify_coupled_circuits_energy,
    integrate_electrokinetic_energy,
)

__all__ = [
    # Electrostatic energy (Arts. 630-631)
    "ElectrostaticEnergy",
    "calc_electrostatic_energy_density",
    "calc_total_electrostatic_energy",
    "calc_capacitor_energy",
    "calc_energy_in_dielectric",
    "calc_energy_density_from_ED_dot",
    "verify_electrostatic_energy_density",
    "analyze_electrostatic_energy",
    "integrate_energy_density",
    # Magnetic energy (Arts. 632-633)
    "MagneticEnergy",
    "calc_magnetic_energy_density",
    "calc_magnetic_energy_density_from_B",
    "calc_total_magnetic_energy",
    "calc_inductor_energy",
    "calc_energy_in_magnetic_material",
    "calc_energy_density_from_BH_dot",
    "verify_magnetic_energy_density",
    "analyze_magnetic_energy",
    "integrate_magnetic_energy_density",
    # Electrokinetic energy (Arts. 634-638)
    "ElectrokineticEnergy",
    "calc_electrokinetic_energy",
    "calc_single_circuit_energy",
    "calc_coupled_circuits_energy",
    "calc_mutual_inductance_energy",
    "calc_two_circuit_energy",
    "calc_coupling_coefficient",
    "analyze_electrokinetic_energy",
    "verify_coupled_circuits_energy",
    "integrate_electrokinetic_energy",
]
