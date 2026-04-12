"""
maxwell.fields — Magnetic field theory: H, B, and field decomposition.

This subpackage implements the magnetic field concepts from Part III:
- Magnetic force H and cavity measurements (force.py, Arts. 395-398)
- Magnetic induction B and flux (induction.py, Art. 399)
- Constitutive relation B = H + 4πI (constitutive.py, Art. 400)
- Solenoidal nature of B, ∇·B = 0 (solenoidal.py, Arts. 403-404)
- Lamellar and solenoidal decomposition (decomposition.py, Arts. 412-416)

Category: A (maxwell_original) — Maxwell's magnetic field theory.
"""

from __future__ import annotations

from maxwell.fields.force import (
    MagneticForce,
    magnetic_force_from_potential,
    cylindric_cavity_force,
    general_magnet_force,
    elongated_cylinder_force,
    compare_cavity_fields,
    force_on_magnetic_pole,
)

from maxwell.fields.induction import (
    MagneticInduction,
    calc_magnetic_induction,
    thin_disk_induction,
    compare_H_and_B_measurements,
    magnetic_flux,
)

from maxwell.fields.constitutive import (
    MaterialType,
    MagneticConstitutiveRelation,
    calc_constitutive_relation,
    calc_B_linear,
    calc_magnetization,
    extract_magnetization,
    calc_susceptibility,
    permeability_cgs_to_si,
    permeability_si_to_cgs,
    typical_susceptibilities,
)

from maxwell.fields.solenoidal import (
    MagneticInductionTube,
    verify_solenoidal,
    verify_zero_net_flux,
    trace_flux_tube,
    magnetic_flux_through_surface,
    prove_no_magnetic_monopoles,
)

from maxwell.fields.decomposition import (
    LamellarDistribution,
    ComplexLamellarDistribution,
    lamellar_potential,
    lamellar_vector_potential,
    helmholtz_decomposition,
    relate_scalar_vector_potential,
    is_lamellar_magnetization,
)

__all__ = [
    # Magnetic Force (Arts. 395-398)
    "MagneticForce",
    "magnetic_force_from_potential",
    "cylindric_cavity_force",
    "general_magnet_force",
    "elongated_cylinder_force",
    "compare_cavity_fields",
    "force_on_magnetic_pole",
    # Magnetic Induction (Art. 399)
    "MagneticInduction",
    "calc_magnetic_induction",
    "thin_disk_induction",
    "compare_H_and_B_measurements",
    "magnetic_flux",
    # Constitutive Relation (Art. 400)
    "MaterialType",
    "MagneticConstitutiveRelation",
    "calc_constitutive_relation",
    "calc_B_linear",
    "calc_magnetization",
    "extract_magnetization",
    "calc_susceptibility",
    "permeability_cgs_to_si",
    "permeability_si_to_cgs",
    "typical_susceptibilities",
    # Solenoidal Nature (Arts. 403-404)
    "MagneticInductionTube",
    "verify_solenoidal",
    "verify_zero_net_flux",
    "trace_flux_tube",
    "magnetic_flux_through_surface",
    "prove_no_magnetic_monopoles",
    # Field Decomposition (Arts. 412-416)
    "LamellarDistribution",
    "ComplexLamellarDistribution",
    "lamellar_potential",
    "lamellar_vector_potential",
    "helmholtz_decomposition",
    "relate_scalar_vector_potential",
    "is_lamellar_magnetization",
]
