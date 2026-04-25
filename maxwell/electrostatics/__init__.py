"""
Electrostatics — Maxwell's Part I.

This package implements Maxwell's electrostatic theory from Part I
of the Treatise:

- Chapter I: Description of Phenomena (Arts. 12–19)
- Chapter I–VI: Fundamental concepts, electric field, potential
- Chapter VI: Points & Lines of Equilibrium (Arts. 112–116)
- Chapter VII: Equipotential Surfaces (Arts. 117–123)
- Chapter VIII: Simple Cases of Electrostatics (Arts. 124–127)
- Chapter X: Confocal Surfaces (Arts. 147–156)
- Chapter VII: Theory of Dielectrics (Arts. 157–164)
- Chapter VIII: Electrification (Arts. 165–170)
- Chapter XI: Electric Images (Arts. 171–181)
- Chapter XIII: Electrostatic Instruments (Arts. 207–229)

Modules:
    phenomena: Electrification phenomena, scintillation, sparks (Arts. 12–19).
    equilibrium_surfaces: Equilibrium points, equipotential surfaces, simple cases (Arts. 112–127).
    dielectrics: Dielectric theory and electrification (Arts. 157–170).
    confocal_surfaces: Confocal ellipsoids and hyperboloids (Arts. 147–156).
    electric_images: Method of images (Arts. 171–181).
    instruments: Electrostatic instruments (Arts. 207–229).
    general_theorems: Green's theorem, reciprocity, uniqueness, energy (Arts. 86-102).
    force_theory: Force theory and elementary electricity (Arts. 27-28, 31-37, 41-42, 50-63, 65).
"""

from __future__ import annotations

from maxwell.electrostatics.phenomena import (
    # Electrification by Friction (Arts. 12–14)
    electrification_by_friction,
    vitreous_electrification_glass_silk,
    resinous_electrification_resin_fur,
    verify_friction_conservation,
    # Electrification by Induction (Arts. 15–16)
    electrification_by_induction,
    induced_surface_distribution,
    # Electrification by Contact (Art. 17)
    electrification_by_contact,
    charge_sharing_equal_spheres,
    # Electric Scintillation (Art. 18)
    electric_scintillation,
    corona_discharge_at_point,
    # Electric Sparks (Art. 19)
    electric_spark_properties,
    spark_gap_breakdown,
    # Classification (Arts. 12–19)
    phenomena_classifier,
    complete_phenomenology,
    # Enumerations and Data Classes
    ElectrificationType,
    PhenomenonClass,
    FrictionPair,
    DischargePhenomenon,
    SparkProperties,
)

from maxwell.electrostatics.equilibrium_surfaces import (
    # Points & Lines of Equilibrium (Arts. 112–116)
    equilibrium_points,
    equilibrium_lines,
    saddle_point_analysis,
    # Equipotential Surfaces (Arts. 117–123)
    equipotential_surface,
    surface_curvature,
    field_line_tracing,
    surface_charge_density,
    # Simple Cases of Electrostatics (Arts. 124–127)
    isolated_sphere,
    parallel_plate_capacitor,
    concentric_spheres,
    coaxial_cylinders,
)

from maxwell.electrostatics.dielectrics import (
    # Specific Inductive Capacity (Arts. 157–159)
    specific_inductive_capacity,
    table_specific_inductive_capacities,
    # Dielectric Polarization (Arts. 160–161)
    dielectric_polarization,
    electric_susceptibility,
    # Bound Charge (Arts. 162–163)
    bound_charge_density,
    bound_charge_density_linear,
    surface_bound_charge,
    # Dielectric Displacement (Art. 164)
    dielectric_displacement,
    gauss_law_dielectric,
    # Electrification by Friction (Arts. 165–166) - alias to avoid conflict
    electrification_by_friction as dielectric_electrification_by_friction,
    # Electrification by Contact (Arts. 167–168) - alias to avoid conflict
    electrification_by_contact as dielectric_electrification_by_contact,
    charge_distribution_conductor,
    # Electrification by Induction (Arts. 169–170) - alias to avoid conflict
    electrification_by_induction as dielectric_electrification_by_induction,
    image_charge_induction,
    # Dielectric Material Class
    DielectricMaterial,
)

from maxwell.electrostatics.confocal_surfaces import (
    # Confocal Ellipsoid Potential (Arts. 147–150)
    confocal_ellipsoid_potential,
    ellipsoid_capacitance,
    # Confocal Hyperboloid (Arts. 151–153)
    confocal_hyperboloid,
    confocal_field_lines,
    # Ellipsoidal Coordinates (Arts. 154–156)
    ellipsoidal_coordinates,
    laplacian_ellipsoidal,
    ellipsoidal_harmonic_expansion,
    EllipsoidalHarmonic,
)

from maxwell.electrostatics.electric_images import (
    # Point Charge Above Plane (Arts. 171–173)
    image_point_charge_plane,
    # Point Charge Near Sphere (Arts. 174–176)
    image_point_charge_sphere,
    # Line Charge Near Cylinder (Arts. 177–178)
    image_line_charge_cylinder,
    # Electrical Inversion (Arts. 179–180)
    inversion_method,
    invert_sphere_to_plane,
    # Image System Analysis (Art. 181)
    image_system_analysis,
    # Force Calculations (Arts. 173, 175, 178)
    force_charge_conductor,
)

from maxwell.electrostatics.instruments import (
    # Quadrant Electrometer (Arts. 207–215)
    quadrant_electrometer,
    QuadrantElectrometer,
    # Absolute Electrometer (Arts. 216–220)
    absolute_electrometer,
    calibration_electrometer,
    # Attracted Disk Electrometer (Arts. 221–225)
    attracted_disk_electrometer,
    attracted_disk_force,
    # Torsion Electrometer (Arts. 226–228)
    torsion_electrometer,
    measure_charge_torsion,
    # Henley Electrometer (Art. 229)
    henley_electrometer,
    # Sensitivity Analysis (Arts. 210–215)
    electrometer_sensitivity,
)

from maxwell.electrostatics.general_theorems import (
    # Green's Theorem (Arts. 95–97)
    greens_theorem,
    # Green's Reciprocity Theorem (Arts. 98–99)
    greens_reciprocity,
    # Potential from Charge Distribution (Arts. 100–101)
    potential_from_charge_distribution,
    potential_from_point_charges,
    # Uniqueness Theorem (Art. 102)
    uniqueness_theorem,
    # Electrostatic Energy (Arts. 86–88)
    electrostatic_energy,
    work_to_assemble_charges,
    # Energy Density in Field (Arts. 89–90)
    energy_density_field,
    energy_density_uniform_field,
    # Energy of System (Arts. 91–92)
    energy_of_system,
    energy_of_conductor_system,
    # Virtual Work Principle (Arts. 93–94)
    virtual_work_principle,
    force_between_conductors_constant_charge,
    force_between_conductors_constant_potential,
)

from maxwell.electrostatics.force_theory import (
    # Force Theory (Arts. 27-28, 31-37, 41-42)
    electric_tension,
    electrostatic_attraction,
    repulsion_law,
    force_medium,
    force_superposition,
    # Elementary Theory of Electricity (Arts. 50-63, 65)
    two_fluid_theory,
    one_fluid_theory,
    charge_conservation,
    verify_isolated_system_conservation,
    electrification_types,
    ElectricityType,
    force_between_types,
    charge_induction,
    induced_charge_distribution,
    InductionSystem,
    field_concept,
    field_reality_statement,
    # Utility functions
    coulomb_force,
    field_from_charges,
    check_charge_conservation,
)

__all__ = [
    # Phenomena (Arts. 12–19)
    "electrification_by_friction",
    "vitreous_electrification_glass_silk",
    "resinous_electrification_resin_fur",
    "verify_friction_conservation",
    "electrification_by_induction",
    "induced_surface_distribution",
    "electrification_by_contact",
    "charge_sharing_equal_spheres",
    "electric_scintillation",
    "corona_discharge_at_point",
    "electric_spark_properties",
    "spark_gap_breakdown",
    "phenomena_classifier",
    "complete_phenomenology",
    "ElectrificationType",
    "PhenomenonClass",
    "FrictionPair",
    "DischargePhenomenon",
    "SparkProperties",
    # Equilibrium Points & Lines (Arts. 112–116)
    "equilibrium_points",
    "equilibrium_lines",
    "saddle_point_analysis",
    # Equipotential Surfaces (Arts. 117–123)
    "equipotential_surface",
    "surface_curvature",
    "field_line_tracing",
    "surface_charge_density",
    # Simple Cases (Arts. 124–127)
    "isolated_sphere",
    "parallel_plate_capacitor",
    "concentric_spheres",
    "coaxial_cylinders",
    # Confocal Ellipsoid (Arts. 147–150)
    "confocal_ellipsoid_potential",
    "ellipsoid_capacitance",
    # Confocal Hyperboloid (Arts. 151–153)
    "confocal_hyperboloid",
    "confocal_field_lines",
    # Ellipsoidal Coordinates (Arts. 154–156)
    "ellipsoidal_coordinates",
    "laplacian_ellipsoidal",
    "ellipsoidal_harmonic_expansion",
    "EllipsoidalHarmonic",
    # Specific Inductive Capacity (Arts. 157–159)
    "specific_inductive_capacity",
    "table_specific_inductive_capacities",
    # Dielectric Polarization (Arts. 160–161)
    "dielectric_polarization",
    "electric_susceptibility",
    # Bound Charge (Arts. 162–163)
    "bound_charge_density",
    "bound_charge_density_linear",
    "surface_bound_charge",
    # Dielectric Displacement (Art. 164)
    "dielectric_displacement",
    "gauss_law_dielectric",
    # Electrification (Arts. 165–170) - dielectric-specific (aliased)
    "dielectric_electrification_by_friction",
    "dielectric_electrification_by_contact",
    "charge_distribution_conductor",
    "dielectric_electrification_by_induction",
    "image_charge_induction",
    # Material Class
    "DielectricMaterial",
    # Electric Images (Arts. 171–181)
    "image_point_charge_plane",
    "image_point_charge_sphere",
    "image_line_charge_cylinder",
    "inversion_method",
    "invert_sphere_to_plane",
    "image_system_analysis",
    "force_charge_conductor",
    # Quadrant Electrometer (Arts. 207–215)
    "quadrant_electrometer",
    "QuadrantElectrometer",
    # Absolute Electrometer (Arts. 216–220)
    "absolute_electrometer",
    "calibration_electrometer",
    # Attracted Disk Electrometer (Arts. 221–225)
    "attracted_disk_electrometer",
    "attracted_disk_force",
    # Torsion Electrometer (Arts. 226–228)
    "torsion_electrometer",
    "measure_charge_torsion",
    # Henley Electrometer (Art. 229)
    "henley_electrometer",
    # Sensitivity Analysis (Arts. 210–215)
    "electrometer_sensitivity",
    # Green's Theorem (Arts. 95–97)
    "greens_theorem",
    # Green's Reciprocity Theorem (Arts. 98–99)
    "greens_reciprocity",
    # Potential from Charge Distribution (Arts. 100–101)
    "potential_from_charge_distribution",
    "potential_from_point_charges",
    # Uniqueness Theorem (Art. 102)
    "uniqueness_theorem",
    # Electrostatic Energy (Arts. 86–88)
    "electrostatic_energy",
    "work_to_assemble_charges",
    # Energy Density in Field (Arts. 89–90)
    "energy_density_field",
    "energy_density_uniform_field",
    # Energy of System (Arts. 91–92)
    "energy_of_system",
    "energy_of_conductor_system",
    # Virtual Work Principle (Arts. 93–94)
    "virtual_work_principle",
    "force_between_conductors_constant_charge",
    "force_between_conductors_constant_potential",
    # Force Theory (Arts. 27-28, 31-37, 41-42)
    "electric_tension",
    "electrostatic_attraction",
    "repulsion_law",
    "force_medium",
    "force_superposition",
    # Elementary Theory of Electricity (Arts. 50-63, 65)
    "two_fluid_theory",
    "one_fluid_theory",
    "charge_conservation",
    "verify_isolated_system_conservation",
    "electrification_types",
    "ElectricityType",
    "force_between_types",
    "charge_induction",
    "induced_charge_distribution",
    "InductionSystem",
    "field_concept",
    "field_reality_statement",
    # Utility functions
    "coulomb_force",
    "field_from_charges",
    "check_charge_conservation",
]
