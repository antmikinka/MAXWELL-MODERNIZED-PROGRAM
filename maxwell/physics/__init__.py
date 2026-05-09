"""
maxwell.physics — Fundamental physics laws and relations.

This subpackage implements the basic physical laws of electrostatics and
electrokinematics from Maxwell's Treatise:

- Coulomb's law and force calculations (coulomb.py)
- Gauss's theorem and surface integrals (gauss.py)
- Ohm's law (ohm.py)
- Electric current and current density (current.py)
- Conduction in 3D and Ohm's law differential form (conduction.py)

Category: A (maxwell_original) — Maxwell's physics formulations.
"""

from __future__ import annotations

from maxwell.physics.conduction import (
    ConductivityTensor,
    calc_conduction_current,
    calc_resistance_3d,
    drift_velocity,
    effective_conductivity_layered,
    heterogeneous_conduction,
    isotropic_conductivity_tensor,
    joule_heating,
    ohm_law_microscopic,
    orthotropic_conductivity_tensor,
    specific_resistance_from_measurement,
)
from maxwell.physics.coulomb import (
    ElectrostaticForce,
    coulomb_law,
    electric_field_from_force,
    field_intensity,
    force_charge_relation,
    force_distance_law,
    measure_force,
    resultant_force,
    resultant_force_multiple,
    superposition_force,
    verify_charge_conservation_force,
    verify_inverse_square_law,
)
from maxwell.physics.coupling import (
    DipoleInteraction,
    angular_dependence,
    calc_dipole_interaction,
    dipole_equilibrium_orientations,
    dipole_force_from_gradient,
    dipole_potential_energy,
    dipole_torque,
    magnet_to_magnet_force,
    special_dipole_cases,
)
from maxwell.physics.current import (
    ElectricCurrent,
    calc_current_density,
    calc_total_current,
    continuity_equation,
    current_density_parallel,
    current_through_tilted_surface,
    current_vector,
    verify_current_conservation,
    verify_steady_current,
)
from maxwell.physics.gauss import (
    SurfaceIntegral,
    derive_inverse_square_from_gauss,
    divergence_theorem,
    gauss_cylinder,
    gauss_external_charge,
    gauss_law,
    gauss_plane,
    gauss_sphere,
    surface_integral_induction,
    surface_integral_sphere,
    trace_induction_lines,
    verify_gauss_law_numerical,
)
from maxwell.physics.magnetostriction import (
    MagnetostrictionTensor,
    MagnetostrictiveMaterial,
    explain_magnetostriction_phenomena,
    joule_magnetostriction,
    magnetoelastic_energy,
    typical_magnetostriction_constants,
    volume_magnetostriction,
)
from maxwell.physics.molecular_theory import (
    MagneticMolecule,
    MolecularEnsemble,
    curie_temperature,
    molecular_field,
    thermal_randomization,
    verify_molecular_theory,
)
from maxwell.physics.ohm import (
    calc_emf,
    calc_resistance,
    solve_ohm_law,
    specific_resistance_emu,
    uniform_wire_resistance,
)
from maxwell.physics.potentials import (
    MagneticPotential,
    calc_element_field,
    calc_element_potential,
    calc_finite_field,
    calc_finite_potential,
    compare_potential_formulations,
    finite_potential_by_integration,
)

__all__ = [
    # Ohm's Law
    "solve_ohm_law",
    "calc_emf",
    "calc_resistance",
    "uniform_wire_resistance",
    "specific_resistance_emu",
    # Coulomb's Law
    "ElectrostaticForce",
    "coulomb_law",
    "resultant_force",
    "resultant_force_multiple",
    "field_intensity",
    "measure_force",
    "force_charge_relation",
    "force_distance_law",
    "verify_inverse_square_law",
    "verify_charge_conservation_force",
    "superposition_force",
    "electric_field_from_force",
    # Gauss's Law
    "SurfaceIntegral",
    "surface_integral_induction",
    "gauss_law",
    "gauss_sphere",
    "gauss_external_charge",
    "gauss_cylinder",
    "gauss_plane",
    "trace_induction_lines",
    "divergence_theorem",
    "surface_integral_sphere",
    "verify_gauss_law_numerical",
    "derive_inverse_square_from_gauss",
    # Electric Current (Part II, Arts. 150-177)
    "ElectricCurrent",
    "calc_current_density",
    "continuity_equation",
    "calc_total_current",
    "current_vector",
    "current_through_tilted_surface",
    "verify_steady_current",
    "current_density_parallel",
    "verify_current_conservation",
    # Conduction (Part II, Arts. 230-279)
    "ConductivityTensor",
    "calc_conduction_current",
    "calc_resistance_3d",
    "heterogeneous_conduction",
    "specific_resistance_from_measurement",
    "ohm_law_microscopic",
    "joule_heating",
    "isotropic_conductivity_tensor",
    "orthotropic_conductivity_tensor",
    "drift_velocity",
    "effective_conductivity_layered",
    # Magnetic Potential (Part III, Arts. 385-386)
    "MagneticPotential",
    "calc_element_potential",
    "calc_element_field",
    "calc_finite_potential",
    "calc_finite_field",
    "finite_potential_by_integration",
    "compare_potential_formulations",
    # Dipole Coupling (Part III, Arts. 387-388)
    "DipoleInteraction",
    "calc_dipole_interaction",
    "dipole_force_from_gradient",
    "dipole_potential_energy",
    "dipole_torque",
    "special_dipole_cases",
    "dipole_equilibrium_orientations",
    "angular_dependence",
    "magnet_to_magnet_force",
    # Molecular Theory (Part III, Art. 430)
    "MagneticMolecule",
    "MolecularEnsemble",
    "molecular_field",
    "curie_temperature",
    "thermal_randomization",
    "verify_molecular_theory",
    # Magnetostriction (Part III, Arts. 447-448)
    "MagnetostrictionTensor",
    "MagnetostrictiveMaterial",
    "joule_magnetostriction",
    "volume_magnetostriction",
    "typical_magnetostriction_constants",
    "magnetoelastic_energy",
    "explain_magnetostriction_phenomena",
]
