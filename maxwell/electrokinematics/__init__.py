"""
Electrokinematics — Part II of Maxwell's Treatise.

This package implements Maxwell's theory of electrokinematics from Part II:
- Electric currents and conduction (Arts. 230-248)
- Electrolysis (Arts. 249-263)
- Thermoelectric effects (Arts. 264-272)
- Linear network theory (Arts. 273-284)
- 3D conduction theory (Arts. 285-296)

CGS-EMU units are used throughout, following Maxwell's conventions.
"""

from maxwell.electrokinematics.electrolysis import (
    # Constants
    FARADAY_CONSTANT,
    ELEMENTARY_CHARGE_EMU,
    AVOGADRO_NUMBER,
    # Faraday's Laws
    faraday_first_law,
    faraday_second_law,
    electrochemical_equivalent,
    # Polarization
    polarization_emf,
    decomposition_voltage,
    # Ionic Conduction
    ion_migration_velocity,
    electrolyte_conductivity,
    kohlrausch_law,
    concentration_polarization,
    battery_back_emf,
    # Ion Data
    IonData,
    ION_DATA,
    get_ion_data,
    limiting_molar_conductivity,
    transference_number,
    # Cell Model
    ElectrolysisCell,
    # Analysis
    analyze_electrolysis,
    # Verification
    verify_faradays_laws,
    verify_kohlrausch_law,
)

from maxwell.electrokinematics.network_solver import (
    # Kirchhoff's Laws (Arts. 273-275)
    kirchhoff_junction_rule,
    kirchhoff_loop_rule,
    # Conductance Matrix (Arts. 276-280)
    build_conductance_matrix,
    solve_network,
    # Wheatstone Bridge (Arts. 281-284)
    wheatstone_bridge_balance,
    wheatstone_bridge_sensitivity,
    # Reciprocity (Arts. 277-278)
    reciprocity_theorem,
    # Conjugate Functions (Art. 280)
    conjugate_functions_2d,
    # Classes
    NetworkAnalyzer,
)

from maxwell.electrokinematics.conduction_3d import (
    # Ohm's Law 3D (Arts. 285-288)
    ohms_law_3d,
    electric_field_from_current_density,
    # Anisotropic Conductivity (Arts. 288-290)
    anisotropic_conductivity,
    principal_conduction_axes,
    # Continuity Equation (Arts. 291-292)
    continuity_equation,
    verify_steady_state_continuity,
    # Point Source Solutions (Arts. 293-295)
    point_source_potential,
    dipole_potential,
    spreading_resistance,
    # Interface Boundary Conditions (Art. 296)
    interface_boundary_conditions,
    # Method of Images
    method_of_images_conductor,
    # Classes
    Conduction3DAnalyzer,
)

from maxwell.electrokinematics.dielectric_conduction import (
    # Dielectric Conductivity (Arts. 325-326)
    dielectric_conductivity,
    # Leakage Current (Arts. 327-328)
    leakage_current_density,
    # Dielectric Absorption (Arts. 329-330)
    dielectric_absorption,
    absorption_current,
    # Residual Charge (Art. 331)
    residual_charge,
    residual_charge_recovery,
    # Layered Dielectrics (Arts. 332-333)
    layered_dielectric,
    # Composite Dielectrics (Art. 334)
    composite_dielectric_conductivity,
    # Class
    DielectricConductor,
)

from maxwell.electrokinematics.resistance_measurement import (
    # Measurement Error Class
    MeasurementError,
    # Substitution Method (Arts. 335-340)
    substitution_method,
    calculate_resistance_from_voltage,
    # Differential Galvanometer (Arts. 341-345)
    differential_galvanometer_method,
    # Wheatstone Bridge (Arts. 346-350)
    wheatstone_bridge_measurement,
    # Low Resistance (Arts. 351-354)
    kelvin_double_bridge,
    four_terminal_measurement,
    # High Resistance (Arts. 355-358)
    leakage_method,
    capacitor_discharge_method,
    # Analyzer
    ResistanceMeasurementAnalyzer,
)

from maxwell.electrokinematics.emf_bodies import (
    # Constants
    R_GAS,
    FARADAY_CONSTANT,
    ELEMENTARY_CHARGE_EMU,
    BOLTZMANN_CONSTANT,
    REFERENCE_TEMPERATURE,
    # Contact EMF (Arts. 246-247)
    contact_emf_metal_electrolyte,
    concentration_cell_emf,
    # Junction Potential (Art. 248)
    junction_potential,
    junction_potential_multi_ion,
    # EMF Series (Arts. 246-248)
    emf_series_bodies,
    volta_series_table,
    # Class
    ContactEMFAnalyzer,
)

from maxwell.electrokinematics.resistance_distribution import (
    # Spherical Geometry (Arts. 297-299)
    resistance_of_sphere,
    resistance_of_isolated_sphere,
    # Cylindrical Geometry (Arts. 300-303)
    resistance_of_cylinder,
    resistance_tube,
    current_distribution_cylinder,
    # Spherical Shell (Arts. 304-306)
    resistance_of_shell,
    current_distribution_sphere,
    # Spreading Resistance (Arts. 307-309)
    spreading_resistance_plane,
    current_distribution_plane,
    potential_distribution_plane,
    # Flow Tube Method
    resistance_by_flow_tubes,
    # Class
    ResistanceDistributionAnalyzer,
)

from maxwell.electrokinematics.heterogeneous_media import (
    # Series Combinations (Arts. 310-314)
    effective_conductivity_series,
    stratified_conductor_effective,
    # Parallel Combinations (Arts. 315-318)
    effective_conductivity_parallel,
    maxwell_garnett_conductivity,
    # Interface Effects (Arts. 319-321)
    interface_resistance,
    boundary_layer_conduction,
    # Stratified Media (Arts. 322-324)
    stratified_conductor,
    # Mixed Conductor (Arts. 319-322)
    mixed_conductor,
    # Class
    HeterogeneousMediaAnalyzer,
)

from maxwell.electrokinematics.resistance_substances import (
    # Material Database
    MaterialResistance,
    MATERIAL_DATABASE,
    get_material_data,
    # Metal Resistance (Arts. 359-362)
    metal_resistance,
    temperature_coefficient,
    # Alloy Resistance (Arts. 363-364)
    alloy_resistance,
    matthiessen_rule,
    # Electrolyte Resistance (Arts. 365-366)
    electrolyte_resistance,
    electrolyte_conductivity_vs_concentration,
    # Dielectric Resistance (Arts. 367-368)
    dielectric_resistance,
    surface_resistivity,
    # Semiconductor Resistance (Arts. 369-370)
    semiconductor_resistance,
    photoconductivity,
    # Class
    ResistanceSubstancesAnalyzer,
)

from maxwell.electrokinematics.emf import (
    # Constants
    FARADAY_CONSTANT,
    R_GAS,
    ELEMENTARY_CHARGE_EMU,
    ABSOLUTE_ZERO,
    REFERENCE_TEMPERATURE,
    # Contact EMF (Arts. 264-266)
    contact_potential,
    contact_potential_from_ev,
    volta_series_emf,
    # Chemical EMF (Arts. 267-269)
    chemical_emf,
    nernst_equation,
    # Thermoelectric Effects (Arts. 270-272)
    seebeck_effect,
    seebeck_effect_temperature_dependent,
    peltier_effect,
    peltier_coefficient_from_seebeck,
    thomson_effect,
    thomson_coefficient_from_seebeck,
    kelvin_relations,
    # EMF Source Class
    EMFSource,
    # Analysis Functions
    analyze_voltaic_cell,
    analyze_thermoelectric_generator,
    # Verification
    verify_emf_theory,
)

__all__ = [
    # Electrolysis Constants
    "FARADAY_CONSTANT",
    "ELEMENTARY_CHARGE_EMU",
    "AVOGADRO_NUMBER",
    # Faraday's Laws
    "faraday_first_law",
    "faraday_second_law",
    "electrochemical_equivalent",
    # Polarization
    "polarization_emf",
    "decomposition_voltage",
    # Ionic Conduction
    "ion_migration_velocity",
    "electrolyte_conductivity",
    "kohlrausch_law",
    "concentration_polarization",
    "battery_back_emf",
    # Ion Data
    "IonData",
    "ION_DATA",
    "get_ion_data",
    "limiting_molar_conductivity",
    "transference_number",
    # Cell Model
    "ElectrolysisCell",
    # Analysis
    "analyze_electrolysis",
    # Verification
    "verify_faradays_laws",
    "verify_kohlrausch_law",
    # Kirchhoff's Laws (Arts. 273-275)
    "kirchhoff_junction_rule",
    "kirchhoff_loop_rule",
    # Network Analysis (Arts. 276-280)
    "build_conductance_matrix",
    "solve_network",
    # Wheatstone Bridge (Arts. 281-284)
    "wheatstone_bridge_balance",
    "wheatstone_bridge_sensitivity",
    # Reciprocity (Arts. 277-278)
    "reciprocity_theorem",
    # Conjugate Functions (Art. 280)
    "conjugate_functions_2d",
    # Network Analyzer
    "NetworkAnalyzer",
    # Ohm's Law 3D (Arts. 285-288)
    "ohms_law_3d",
    "electric_field_from_current_density",
    # Anisotropic Conductivity (Arts. 288-290)
    "anisotropic_conductivity",
    "principal_conduction_axes",
    # Continuity Equation (Arts. 291-292)
    "continuity_equation",
    "verify_steady_state_continuity",
    # Point Source Solutions (Arts. 293-295)
    "point_source_potential",
    "dipole_potential",
    "spreading_resistance",
    # Interface Boundary Conditions (Art. 296)
    "interface_boundary_conditions",
    "method_of_images_conductor",
    # Conduction 3D Analyzer
    "Conduction3DAnalyzer",
    # Dielectric Conduction (Arts. 325-334)
    "dielectric_conductivity",
    "leakage_current_density",
    "dielectric_absorption",
    "absorption_current",
    "residual_charge",
    "residual_charge_recovery",
    "layered_dielectric",
    "composite_dielectric_conductivity",
    "DielectricConductor",
    # Resistance Measurement (Arts. 335-358)
    "MeasurementError",
    # Substitution Method (Arts. 335-340)
    "substitution_method",
    "calculate_resistance_from_voltage",
    # Differential Galvanometer (Arts. 341-345)
    "differential_galvanometer_method",
    # Wheatstone Bridge Methods (Arts. 346-350)
    "wheatstone_bridge_measurement",
    # Low Resistance Measurement (Arts. 351-354)
    "kelvin_double_bridge",
    "four_terminal_measurement",
    # High Resistance Measurement (Arts. 355-358)
    "leakage_method",
    "capacitor_discharge_method",
    # Analyzer
    "ResistanceMeasurementAnalyzer",
    # EMF - Electromotive Force (Arts. 264-272)
    # Constants
    "FARADAY_CONSTANT",
    "R_GAS",
    "ELEMENTARY_CHARGE_EMU",
    "ABSOLUTE_ZERO",
    "REFERENCE_TEMPERATURE",
    # Contact EMF (Arts. 264-266)
    "contact_potential",
    "contact_potential_from_ev",
    "volta_series_emf",
    # Chemical EMF (Arts. 267-269)
    "chemical_emf",
    "nernst_equation",
    # Thermoelectric Effects (Arts. 270-272)
    "seebeck_effect",
    "seebeck_effect_temperature_dependent",
    "peltier_effect",
    "peltier_coefficient_from_seebeck",
    "thomson_effect",
    "thomson_coefficient_from_seebeck",
    "kelvin_relations",
    # EMF Source Class
    "EMFSource",
    # Analysis Functions
    "analyze_voltaic_cell",
    "analyze_thermoelectric_generator",
    # Verification
    "verify_emf_theory",
    # EMF Between Bodies (Arts. 246-248) - New module
    "BOLTZMANN_CONSTANT",
    "contact_emf_metal_electrolyte",
    "concentration_cell_emf",
    "junction_potential",
    "junction_potential_multi_ion",
    "emf_series_bodies",
    "volta_series_table",
    "ContactEMFAnalyzer",
    # Resistance Distribution (Arts. 297-309) - New module
    "resistance_of_sphere",
    "resistance_of_isolated_sphere",
    "resistance_of_cylinder",
    "resistance_tube",
    "current_distribution_cylinder",
    "resistance_of_shell",
    "current_distribution_sphere",
    "spreading_resistance_plane",
    "current_distribution_plane",
    "potential_distribution_plane",
    "resistance_by_flow_tubes",
    "ResistanceDistributionAnalyzer",
    # Heterogeneous Media (Arts. 310-324) - New module
    "effective_conductivity_series",
    "stratified_conductor_effective",
    "effective_conductivity_parallel",
    "maxwell_garnett_conductivity",
    "interface_resistance",
    "boundary_layer_conduction",
    "stratified_conductor",
    "mixed_conductor",
    "HeterogeneousMediaAnalyzer",
    # Resistance of Substances (Arts. 359-370) - New module
    "MaterialResistance",
    "MATERIAL_DATABASE",
    "get_material_data",
    "metal_resistance",
    "temperature_coefficient",
    "alloy_resistance",
    "matthiessen_rule",
    "electrolyte_resistance",
    "electrolyte_conductivity_vs_concentration",
    "dielectric_resistance",
    "surface_resistivity",
    "semiconductor_resistance",
    "photoconductivity",
    "ResistanceSubstancesAnalyzer",
]
