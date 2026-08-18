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

from maxwell.electrokinematics.conduction_3d import (  # Ohm's Law 3D (Arts. 285-288); Anisotropic Conductivity (Arts. 288-290); Continuity Equation (Arts. 291-292); Point Source Solutions (Arts. 293-295); Interface Boundary Conditions (Art. 296); Method of Images; Classes
    Conduction3DAnalyzer,
    anisotropic_conductivity,
    continuity_equation,
    dipole_potential,
    electric_field_from_current_density,
    interface_boundary_conditions,
    method_of_images_conductor,
    ohms_law_3d,
    point_source_potential,
    principal_conduction_axes,
    spreading_resistance,
    verify_steady_state_continuity,
)
from maxwell.electrokinematics.dielectric_conduction import (  # Dielectric Conductivity (Arts. 325-326); Leakage Current (Arts. 327-328); Dielectric Absorption (Arts. 329-330); Residual Charge (Art. 331); Layered Dielectrics (Arts. 332-333); Composite Dielectrics (Art. 334); Class
    DielectricConductor,
    absorption_current,
    composite_dielectric_conductivity,
    dielectric_absorption,
    dielectric_conductivity,
    layered_dielectric,
    leakage_current_density,
    residual_charge,
    residual_charge_recovery,
)
from maxwell.electrokinematics.electrolysis import (  # Constants; Faraday's Laws; Polarization; Ionic Conduction; Ion Data; Cell Model; Analysis; Verification
    AVOGADRO_NUMBER,
    ELEMENTARY_CHARGE_EMU,
    FARADAY_CONSTANT,
    ION_DATA,
    ElectrolysisCell,
    IonData,
    analyze_electrolysis,
    battery_back_emf,
    concentration_polarization,
    decomposition_voltage,
    electrochemical_equivalent,
    electrolyte_conductivity,
    faraday_first_law,
    faraday_second_law,
    get_ion_data,
    ion_migration_velocity,
    kohlrausch_law,
    limiting_molar_conductivity,
    polarization_emf,
    transference_number,
    verify_faradays_laws,
    verify_kohlrausch_law,
)
from maxwell.electrokinematics.emf import (  # Constants; Contact EMF (Arts. 264-266); Chemical EMF (Arts. 267-269); Thermoelectric Effects (Arts. 270-272); EMF Source Class; Analysis Functions; Verification
    ABSOLUTE_ZERO,
    ELEMENTARY_CHARGE_EMU,
    FARADAY_CONSTANT,
    R_GAS,
    REFERENCE_TEMPERATURE,
    EMFSource,
    analyze_thermoelectric_generator,
    analyze_voltaic_cell,
    chemical_emf,
    contact_potential,
    contact_potential_from_ev,
    kelvin_relations,
    nernst_equation,
    peltier_coefficient_from_seebeck,
    peltier_effect,
    seebeck_effect,
    seebeck_effect_temperature_dependent,
    thomson_coefficient_from_seebeck,
    thomson_effect,
    verify_emf_theory,
    volta_series_emf,
)
from maxwell.electrokinematics.emf_bodies import (  # Constants; Contact EMF (Arts. 246-247); Junction Potential (Art. 248); EMF Series (Arts. 246-248); Class
    BOLTZMANN_CONSTANT,
    ELEMENTARY_CHARGE_EMU,
    FARADAY_CONSTANT,
    R_GAS,
    REFERENCE_TEMPERATURE,
    ContactEMFAnalyzer,
    concentration_cell_emf,
    contact_emf_metal_electrolyte,
    emf_series_bodies,
    junction_potential,
    junction_potential_multi_ion,
    volta_series_table,
)
from maxwell.electrokinematics.heterogeneous_media import (  # Series Combinations (Arts. 310-314); Parallel Combinations (Arts. 315-318); Interface Effects (Arts. 319-321); Stratified Media (Arts. 322-324); Mixed Conductor (Arts. 319-322); Class
    HeterogeneousMediaAnalyzer,
    boundary_layer_conduction,
    effective_conductivity_parallel,
    effective_conductivity_series,
    interface_resistance,
    maxwell_garnett_conductivity,
    mixed_conductor,
    stratified_conductor,
    stratified_conductor_effective,
)
from maxwell.electrokinematics.network_solver import (  # Kirchhoff's Laws (Arts. 273-275); Conductance Matrix (Arts. 276-280); Wheatstone Bridge (Arts. 281-284); Reciprocity (Arts. 277-278); Conjugate Functions (Art. 280); Classes
    NetworkAnalyzer,
    build_conductance_matrix,
    conjugate_functions_2d,
    kirchhoff_junction_rule,
    kirchhoff_loop_rule,
    reciprocity_theorem,
    solve_network,
    wheatstone_bridge_balance,
    wheatstone_bridge_sensitivity,
)
from maxwell.electrokinematics.resistance_distribution import (  # Spherical Geometry (Arts. 297-299); Cylindrical Geometry (Arts. 300-303); Spherical Shell (Arts. 304-306); Spreading Resistance (Arts. 307-309); Flow Tube Method; Class
    ResistanceDistributionAnalyzer,
    current_distribution_cylinder,
    current_distribution_plane,
    current_distribution_sphere,
    potential_distribution_plane,
    resistance_by_flow_tubes,
    resistance_of_cylinder,
    resistance_of_isolated_sphere,
    resistance_of_shell,
    resistance_of_sphere,
    resistance_tube,
    spreading_resistance_plane,
)
from maxwell.electrokinematics.resistance_measurement import (  # Measurement Error Class; Substitution Method (Arts. 335-340); Differential Galvanometer (Arts. 341-345); Wheatstone Bridge (Arts. 346-350); Low Resistance (Arts. 351-354); High Resistance (Arts. 355-358); Analyzer
    MeasurementError,
    ResistanceMeasurementAnalyzer,
    calculate_resistance_from_voltage,
    capacitor_discharge_method,
    differential_galvanometer_method,
    four_terminal_measurement,
    kelvin_double_bridge,
    leakage_method,
    substitution_method,
    wheatstone_bridge_measurement,
)
from maxwell.electrokinematics.resistance_substances import (  # Material Database; Metal Resistance (Arts. 359-362); Alloy Resistance (Arts. 363-364); Electrolyte Resistance (Arts. 365-366); Dielectric Resistance (Arts. 367-368); Semiconductor Resistance (Arts. 369-370); Class
    MATERIAL_DATABASE,
    MaterialResistance,
    ResistanceSubstancesAnalyzer,
    alloy_resistance,
    dielectric_resistance,
    electrolyte_conductivity_vs_concentration,
    electrolyte_resistance,
    get_material_data,
    matthiessen_rule,
    metal_resistance,
    photoconductivity,
    semiconductor_resistance,
    surface_resistivity,
    temperature_coefficient,
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
