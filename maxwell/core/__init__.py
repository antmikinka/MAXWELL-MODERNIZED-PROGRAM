"""
maxwell.core — Core electrostatic and magnetic primitives and field theory.

This subpackage implements the fundamental objects of electrostatics and magnetism:
- Charge and electrification (charge.py)
- Units and dimensional analysis (units.py)
- Electric fields and lines of force (field.py)
- Electric potential and Laplace/Poisson solvers (potential.py)
- Magnetic poles, magnets, and forces (magnet.py)
- Magnetic matter and molecular theory (matter.py)
- Magnetic moment and magnetization (moment.py)

Category: A (maxwell_original) — Maxwell's electrostatic and magnetic theory.
"""

from __future__ import annotations

from maxwell.core.charge import (
    PointCharge,
    faraday_isolation_proof,
    verify_charge_conservation,
)

from maxwell.core.units import (
    CGSUnitConverter,
    MagneticDimensions,
    CONVERTER,
)

from maxwell.core.field import (
    ElectricField,
    EquipotentialSurface,
    LineOfForce,
    electric_tension,
    electric_flux,
    gauss_law_closed_surface,
    field_from_potential,
    line_integral,
)

from maxwell.core.potential import (
    ElectricPotential,
    laplace_equation,
    poisson_equation,
    solve_poisson,
    solve_laplace,
    boundary_condition_potential,
    boundary_condition_normal_derivative,
    boundary_condition_tangential,
    system_energy,
    potential_difference,
    electromotive_force_potential,
)

from maxwell.core.magnet import (
    MagneticPole,
    Magnet,
    MagneticAxis,
    MagneticQuantity,
    earth_response,
    mutual_action,
    center_and_axes,
    verify_force_law_evidence,
)

from maxwell.core.matter import (
    MolecularMagnet,
    MagneticMatterTheory,
    verify_equal_opposite,
    break_magnet,
    verify_fragments_complete,
    molecular_magnetization_model,
)

from maxwell.core.moment import (
    MagnetizationVector,
    MagneticPolarization,
    MagneticParticle,
    MagneticMoment,
    MagnetizationIntensity,
    MagnetizationComponents,
    resultant_moment_and_axis,
)

__all__ = [
    # Charge
    "PointCharge",
    "faraday_isolation_proof",
    "verify_charge_conservation",
    # Units
    "CGSUnitConverter",
    "MagneticDimensions",
    "CONVERTER",
    # Field
    "ElectricField",
    "EquipotentialSurface",
    "LineOfForce",
    "electric_tension",
    "electric_flux",
    "gauss_law_closed_surface",
    "field_from_potential",
    "line_integral",
    # Potential
    "ElectricPotential",
    "laplace_equation",
    "poisson_equation",
    "solve_poisson",
    "solve_laplace",
    "boundary_condition_potential",
    "boundary_condition_normal_derivative",
    "boundary_condition_tangential",
    "system_energy",
    "potential_difference",
    "electromotive_force_potential",
    # Magnet (Part III)
    "MagneticPole",
    "Magnet",
    "MagneticAxis",
    "MagneticQuantity",
    "earth_response",
    "mutual_action",
    "center_and_axes",
    "verify_force_law_evidence",
    # Magnetic Matter (Part III)
    "MolecularMagnet",
    "MagneticMatterTheory",
    "verify_equal_opposite",
    "break_magnet",
    "verify_fragments_complete",
    "molecular_magnetization_model",
    # Magnetic Moment (Part III)
    "MagnetizationVector",
    "MagneticPolarization",
    "MagneticParticle",
    "MagneticMoment",
    "MagnetizationIntensity",
    "MagnetizationComponents",
    "resultant_moment_and_axis",
]
