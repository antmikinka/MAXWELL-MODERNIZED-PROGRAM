"""
maxwell.jax.electromagnetism — JAX-compatible Maxwell electromagnetism.

JAX-pytree versions of Maxwell's electromagnetic computations,
enabling JIT compilation, automatic differentiation, and vectorized evaluation.

Implemented:
- FaradayInductionJAX: Faraday's law with safe operations and pytree support
- analyze_faraday_induction_jax: Complete multi-turn coil induction analysis
- ElectromagneticFieldJAX: Complete EM field state (E, B, H, D, J, rho)
- MaxwellEquationsJAX: Gauss's laws, Faraday's law, Ampere-Maxwell law
- verify_maxwell_equations_jax: Numerical verification suite
- LorentzForceJAX, MaxwellStressTensorJAX: EM forces and stress
- DisplacementCurrentJAX, AmpereMaxwellLawJAX: Displacement current, Ampere-Maxwell
- ElectricFieldJAX: Electric field definition, flux, Gauss's law, EMF
- ElectrostaticEnergyJAX, CapacitorEnergyJAX: Electrostatic energy (Arts. 630-631)
- MagneticEnergyJAX, InductorEnergyJAX: Magnetic energy (Arts. 632-633)
- NetworkSolverJAX, KirchhoffJAX: Network analysis, KCL/KVL (Arts. 273-280)
- WheatstoneBridgeJAX: Wheatstone bridge theory (Arts. 281-284)
- ReciprocityVerifierJAX: Reciprocity theorem (Arts. 277-278)

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from maxwell.jax.electromagnetism.ampere_maxwell import (
    AmpereMaxwellLawJAX,
    DisplacementCurrentJAX,
    capacitor_paradox_jax,
    curl_H_jax,
    displacement_current_jax,
    magnetic_field_from_current_jax,
    total_current_jax,
)
from maxwell.jax.electromagnetism.equations import (
    ElectromagneticFieldJAX,
    MaxwellEquationsJAX,
    verify_maxwell_equations_jax,
)
from maxwell.jax.electromagnetism.field import (
    ElectricFieldJAX,
    electric_flux_jax,
    electric_tension_jax,
    electromotive_force_jax,
    field_from_potential_jax,
    gauss_law_closed_surface_jax,
    superposition_field_jax,
)
from maxwell.jax.electromagnetism.energy import (
    CapacitorEnergyJAX,
    ElectrostaticEnergyJAX,
    analyze_electrostatic_energy_jax,
    calc_capacitor_energy_jax,
    calc_electrostatic_energy_density_jax,
    calc_energy_density_from_ED_dot_jax,
    calc_total_electrostatic_energy_jax,
    verify_electrostatic_energy_density_jax,
)
from maxwell.jax.electromagnetism.magnetic_energy import (
    InductorEnergyJAX,
    MagneticEnergyJAX,
    analyze_magnetic_energy_jax,
    calc_energy_density_from_BH_dot_jax,
    calc_inductor_energy_jax,
    calc_magnetic_energy_density_jax,
    calc_total_magnetic_energy_jax,
    verify_magnetic_energy_density_jax,
)
from maxwell.jax.electromagnetism.ohms_law import (
    ConductivityJAX,
    OhmsLawJAX,
    PowerDissipationJAX,
    ResistanceJAX,
    analyze_ohms_law_jax,
    calc_conductance_jax,
    calc_conductivity_jax,
    calc_current_jax,
    calc_power_from_I2R_jax,
    calc_power_from_IV_jax,
    calc_power_from_V2R_jax,
    calc_resistance_jax,
    calc_resistivity_jax,
    calc_voltage_jax,
    parallel_resistance_jax,
    series_resistance_jax,
    temperature_corrected_resistance_jax,
    verify_ohms_law_jax,
)
from maxwell.jax.electromagnetism.electrokinetic import (
    CoupledCircuitEnergyJAX,
    ElectrokineticEnergyJAX,
    analyze_electrokinetic_energy_jax,
    calc_coupled_circuits_energy_jax,
    calc_coupling_coefficient_jax,
    calc_electrokinetic_energy_jax,
    calc_mutual_inductance_energy_jax,
    calc_single_circuit_energy_jax,
    calc_two_circuit_energy_jax,
    verify_coupled_circuits_energy_jax,
)
from maxwell.jax.electromagnetism.forces import (
    LorentzForceJAX,
    MaxwellStressTensorJAX,
)
from maxwell.jax.electromagnetism.induction import (
    FaradayInductionJAX,
    analyze_faraday_induction_jax,
)
from maxwell.jax.electromagnetism.network_solver import (
    KirchhoffJAX,
    NetworkSolverJAX,
    ReciprocityVerifierJAX,
    WheatstoneBridgeJAX,
    analyze_network_jax,
    kirchhoff_junction_rule_jax,
    kirchhoff_loop_rule_jax,
    reciprocity_theorem_jax,
    solve_network_jax,
    verify_network_solution_jax,
    wheatstone_bridge_balance_jax,
    wheatstone_bridge_sensitivity_jax,
)
from maxwell.jax.electromagnetism.conduction_3d import (
    Conduction3DJAX,
    EffectiveConductivityJAX,
    SpreadingResistanceJAX,
    analyze_conduction_jax,
    circular_contact_resistance_jax,
    conduction_power_density_jax,
    effective_conductivity_parallel_jax,
    effective_conductivity_series_jax,
    electric_field_from_current_density_jax,
    hemispherical_spreading_resistance_jax,
    maxwell_garnett_conductivity_jax,
    ohms_law_3d_jax,
    spherical_spreading_resistance_jax,
    verify_conduction_3d_jax,
)
from maxwell.jax.electromagnetism.electrolysis import (
    FARADAY_CONSTANT_JAX,
    AVOGADRO_NUMBER_JAX,
    ELEMENTARY_CHARGE_EMU_JAX,
    R_GAS_CGS_JAX,
    ElectrolysisCellJAX,
    FaradayLawsJAX,
    IonTransportJAX,
    PolarizationJAX,
    battery_back_emf_jax,
    concentration_polarization_jax,
    decomposition_voltage_jax,
    electrochemical_equivalent_jax,
    electrolyte_conductivity_jax,
    faraday_first_law_jax,
    faraday_second_law_jax,
    ion_migration_velocity_jax,
    kohlrausch_law_jax,
    polarization_emf_jax,
    transference_number_jax,
    verify_electrolysis_jax,
)

from maxwell.jax.electromagnetism.joule_heating import (
    JouleHeatingJAX,
    HeatDissipationJAX,
    SubstanceResistanceJAX,
    joule_heating_power_jax,
    joule_energy_dissipated_jax,
    joule_power_density_jax,
    joule_temperature_rise_jax,
    joule_heating_from_voltage_jax,
    cooling_rate_jax,
    steady_state_temperature_jax,
    substance_resistivity_at_temp_jax,
    substance_resistance_jax,
    verify_joule_heating_jax,
    analyze_joule_heating_jax,
)

__all__ = [
    # Ohm's law / Part II Electrokinematics
    "OhmsLawJAX",
    "ResistanceJAX",
    "ConductivityJAX",
    "PowerDissipationJAX",
    "calc_voltage_jax",
    "calc_current_jax",
    "calc_resistance_jax",
    "calc_conductance_jax",
    "calc_resistivity_jax",
    "calc_conductivity_jax",
    "series_resistance_jax",
    "parallel_resistance_jax",
    "temperature_corrected_resistance_jax",
    "calc_power_from_IV_jax",
    "calc_power_from_I2R_jax",
    "calc_power_from_V2R_jax",
    "verify_ohms_law_jax",
    "analyze_ohms_law_jax",
    # Ampere-Maxwell
    "AmpereMaxwellLawJAX",
    "DisplacementCurrentJAX",
    "capacitor_paradox_jax",
    "curl_H_jax",
    "displacement_current_jax",
    "magnetic_field_from_current_jax",
    "total_current_jax",
    # Electrostatic energy
    "ElectrostaticEnergyJAX",
    "CapacitorEnergyJAX",
    "calc_electrostatic_energy_density_jax",
    "calc_energy_density_from_ED_dot_jax",
    "calc_capacitor_energy_jax",
    "calc_total_electrostatic_energy_jax",
    "verify_electrostatic_energy_density_jax",
    "analyze_electrostatic_energy_jax",
    # Magnetic energy
    "MagneticEnergyJAX",
    "InductorEnergyJAX",
    "calc_magnetic_energy_density_jax",
    "calc_energy_density_from_BH_dot_jax",
    "calc_inductor_energy_jax",
    "calc_total_magnetic_energy_jax",
    "verify_magnetic_energy_density_jax",
    "analyze_magnetic_energy_jax",
    # Maxwell equations
    "ElectromagneticFieldJAX",
    "MaxwellEquationsJAX",
    "verify_maxwell_equations_jax",
    # Electric field
    "ElectricFieldJAX",
    "electric_flux_jax",
    "electric_tension_jax",
    "electromotive_force_jax",
    "field_from_potential_jax",
    "gauss_law_closed_surface_jax",
    "superposition_field_jax",
    # Forces
    "LorentzForceJAX",
    "MaxwellStressTensorJAX",
    # Faraday
    "FaradayInductionJAX",
    "analyze_faraday_induction_jax",
    # Electrokinetic energy
    "ElectrokineticEnergyJAX",
    "CoupledCircuitEnergyJAX",
    "calc_electrokinetic_energy_jax",
    "calc_single_circuit_energy_jax",
    "calc_coupled_circuits_energy_jax",
    "calc_mutual_inductance_energy_jax",
    "calc_two_circuit_energy_jax",
    "calc_coupling_coefficient_jax",
    "verify_coupled_circuits_energy_jax",
    "analyze_electrokinetic_energy_jax",
    # Network solver / Kirchhoff / Wheatstone bridge (Arts. 273-284)
    "NetworkSolverJAX",
    "KirchhoffJAX",
    "WheatstoneBridgeJAX",
    "ReciprocityVerifierJAX",
    "kirchhoff_junction_rule_jax",
    "kirchhoff_loop_rule_jax",
    "solve_network_jax",
    "wheatstone_bridge_balance_jax",
    "wheatstone_bridge_sensitivity_jax",
    "reciprocity_theorem_jax",
    "verify_network_solution_jax",
    "analyze_network_jax",
    # 3D conduction / spreading resistance / effective conductivity (Arts. 285-296, 297-324)
    "Conduction3DJAX",
    "SpreadingResistanceJAX",
    "EffectiveConductivityJAX",
    "ohms_law_3d_jax",
    "electric_field_from_current_density_jax",
    "conduction_power_density_jax",
    "spherical_spreading_resistance_jax",
    "hemispherical_spreading_resistance_jax",
    "circular_contact_resistance_jax",
    "maxwell_garnett_conductivity_jax",
    "effective_conductivity_series_jax",
    "effective_conductivity_parallel_jax",
    "verify_conduction_3d_jax",
    "analyze_conduction_jax",
    # Electrolysis / Faraday's laws / ion transport (Arts. 249-263)
    "FaradayLawsJAX",
    "IonTransportJAX",
    "PolarizationJAX",
    "ElectrolysisCellJAX",
    "FARADAY_CONSTANT_JAX",
    "ELEMENTARY_CHARGE_EMU_JAX",
    "AVOGADRO_NUMBER_JAX",
    "R_GAS_CGS_JAX",
    "faraday_first_law_jax",
    "faraday_second_law_jax",
    "electrochemical_equivalent_jax",
    "polarization_emf_jax",
    "decomposition_voltage_jax",
    "ion_migration_velocity_jax",
    "electrolyte_conductivity_jax",
    "kohlrausch_law_jax",
    "concentration_polarization_jax",
    "battery_back_emf_jax",
    "transference_number_jax",
    "verify_electrolysis_jax",
    # Joule heating and substance resistance (Arts. 351-370)
    "JouleHeatingJAX",
    "HeatDissipationJAX",
    "SubstanceResistanceJAX",
    "joule_heating_power_jax",
    "joule_energy_dissipated_jax",
    "joule_power_density_jax",
    "joule_temperature_rise_jax",
    "joule_heating_from_voltage_jax",
    "cooling_rate_jax",
    "steady_state_temperature_jax",
    "substance_resistivity_at_temp_jax",
    "substance_resistance_jax",
    "verify_joule_heating_jax",
    "analyze_joule_heating_jax",
]
