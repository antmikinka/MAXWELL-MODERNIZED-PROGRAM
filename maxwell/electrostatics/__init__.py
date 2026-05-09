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

from maxwell.electrostatics.confocal_surfaces import (  # Confocal Ellipsoid Potential (Arts. 147–150); Confocal Hyperboloid (Arts. 151–153); Ellipsoidal Coordinates (Arts. 154–156)
    EllipsoidalHarmonic,
    confocal_ellipsoid_potential,
    confocal_field_lines,
    confocal_hyperboloid,
    ellipsoid_capacitance,
    ellipsoidal_coordinates,
    ellipsoidal_harmonic_expansion,
    laplacian_ellipsoidal,
)
from maxwell.electrostatics.dielectrics import (
    DielectricMaterial,
    bound_charge_density,
    bound_charge_density_linear,
    charge_distribution_conductor,
    dielectric_displacement,
    dielectric_polarization,
    electric_susceptibility,
)
from maxwell.electrostatics.dielectrics import (
    electrification_by_contact as dielectric_electrification_by_contact,
)
from maxwell.electrostatics.dielectrics import (
    electrification_by_friction as dielectric_electrification_by_friction,  # Specific Inductive Capacity (Arts. 157–159); Dielectric Polarization (Arts. 160–161); Bound Charge (Arts. 162–163); Dielectric Displacement (Art. 164); Electrification by Friction (Arts. 165–166) - alias to avoid conflict; Electrification by Contact (Arts. 167–168) - alias to avoid conflict; Electrification by Induction (Arts. 169–170) - alias to avoid conflict; Dielectric Material Class
)
from maxwell.electrostatics.dielectrics import (
    electrification_by_induction as dielectric_electrification_by_induction,
)
from maxwell.electrostatics.dielectrics import (
    gauss_law_dielectric,
    image_charge_induction,
    specific_inductive_capacity,
    surface_bound_charge,
    table_specific_inductive_capacities,
)
from maxwell.electrostatics.electric_images import (  # Point Charge Above Plane (Arts. 171–173); Point Charge Near Sphere (Arts. 174–176); Line Charge Near Cylinder (Arts. 177–178); Electrical Inversion (Arts. 179–180); Image System Analysis (Art. 181); Force Calculations (Arts. 173, 175, 178)
    force_charge_conductor,
    image_line_charge_cylinder,
    image_point_charge_plane,
    image_point_charge_sphere,
    image_system_analysis,
    inversion_method,
    invert_sphere_to_plane,
)
from maxwell.electrostatics.equilibrium_surfaces import (  # Points & Lines of Equilibrium (Arts. 112–116); Equipotential Surfaces (Arts. 117–123); Simple Cases of Electrostatics (Arts. 124–127)
    coaxial_cylinders,
    concentric_spheres,
    equilibrium_lines,
    equilibrium_points,
    equipotential_surface,
    field_line_tracing,
    isolated_sphere,
    parallel_plate_capacitor,
    saddle_point_analysis,
    surface_charge_density,
    surface_curvature,
)
from maxwell.electrostatics.force_theory import (  # Force Theory (Arts. 27-28, 31-37, 41-42); Elementary Theory of Electricity (Arts. 50-63, 65); Utility functions
    ElectricityType,
    InductionSystem,
    charge_conservation,
    charge_induction,
    check_charge_conservation,
    coulomb_force,
    electric_tension,
    electrification_types,
    electrostatic_attraction,
    field_concept,
    field_from_charges,
    field_reality_statement,
    force_between_types,
    force_medium,
    force_superposition,
    induced_charge_distribution,
    one_fluid_theory,
    repulsion_law,
    two_fluid_theory,
    verify_isolated_system_conservation,
)
from maxwell.electrostatics.general_theorems import (  # Green's Theorem (Arts. 95–97); Green's Reciprocity Theorem (Arts. 98–99); Potential from Charge Distribution (Arts. 100–101); Uniqueness Theorem (Art. 102); Electrostatic Energy (Arts. 86–88); Energy Density in Field (Arts. 89–90); Energy of System (Arts. 91–92); Virtual Work Principle (Arts. 93–94)
    electrostatic_energy,
    energy_density_field,
    energy_density_uniform_field,
    energy_of_conductor_system,
    energy_of_system,
    force_between_conductors_constant_charge,
    force_between_conductors_constant_potential,
    greens_reciprocity,
    greens_theorem,
    potential_from_charge_distribution,
    potential_from_point_charges,
    uniqueness_theorem,
    virtual_work_principle,
    work_to_assemble_charges,
)
from maxwell.electrostatics.instruments import (  # Quadrant Electrometer (Arts. 207–215); Absolute Electrometer (Arts. 216–220); Attracted Disk Electrometer (Arts. 221–225); Torsion Electrometer (Arts. 226–228); Henley Electrometer (Art. 229); Sensitivity Analysis (Arts. 210–215)
    QuadrantElectrometer,
    absolute_electrometer,
    attracted_disk_electrometer,
    attracted_disk_force,
    calibration_electrometer,
    electrometer_sensitivity,
    henley_electrometer,
    measure_charge_torsion,
    quadrant_electrometer,
    torsion_electrometer,
)
from maxwell.electrostatics.phenomena import (  # Electrification by Friction (Arts. 12–14); Electrification by Induction (Arts. 15–16); Electrification by Contact (Art. 17); Electric Scintillation (Art. 18); Electric Sparks (Art. 19); Classification (Arts. 12–19); Enumerations and Data Classes
    DischargePhenomenon,
    ElectrificationType,
    FrictionPair,
    PhenomenonClass,
    SparkProperties,
    charge_sharing_equal_spheres,
    complete_phenomenology,
    corona_discharge_at_point,
    electric_scintillation,
    electric_spark_properties,
    electrification_by_contact,
    electrification_by_friction,
    electrification_by_induction,
    induced_surface_distribution,
    phenomena_classifier,
    resinous_electrification_resin_fur,
    spark_gap_breakdown,
    verify_friction_conservation,
    vitreous_electrification_glass_silk,
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
