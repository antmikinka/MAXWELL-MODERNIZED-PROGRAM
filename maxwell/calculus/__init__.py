"""
maxwell.calculus — Magnetic vector and scalar potentials, solid angles.

This subpackage implements the magnetic calculus from Part III:
- Line and surface integrals (integrals.py, Arts. 401-402)
- Vector potential A where B = ∇×A (vector_potential.py, Arts. 405-406)
- Solid angles and cyclic functions (cyclic.py, Arts. 417-422)

Category: A (maxwell_original) — Maxwell's magnetic calculus.
"""

from __future__ import annotations

from maxwell.calculus.cyclic import (
    CyclicFunction,
    calc_solid_angle_closed_curve,
    magnetic_shell_potential_jump,
    solid_angle_as_sphere_curve,
    solid_angle_determinant,
    solid_angle_double_line_integral,
    solid_angle_planar_loop,
    vector_potential_closed_curve,
)
from maxwell.calculus.integrals import (
    MagneticLineIntegral,
    MagneticSurfaceIntegral,
    amperes_law_integral,
    calc_line_integral_force,
    calc_surface_induction,
    stokes_theorem_magnetic,
    verify_closed_surface_zero_flux,
)
from maxwell.calculus.vector_potential import (
    VectorPotential,
    calc_B_from_vector_potential,
    calc_vector_potential_from_magnetization,
    gauge_transform,
    relate_scalar_vector_potential,
    vector_potential_uniform_field,
    verify_coulomb_gauge,
)

__all__ = [
    # Line and Surface Integrals (Arts. 401-402)
    "MagneticLineIntegral",
    "MagneticSurfaceIntegral",
    "calc_line_integral_force",
    "calc_surface_induction",
    "amperes_law_integral",
    "verify_closed_surface_zero_flux",
    "stokes_theorem_magnetic",
    # Vector Potential (Arts. 405-406)
    "VectorPotential",
    "calc_B_from_vector_potential",
    "calc_vector_potential_from_magnetization",
    "relate_scalar_vector_potential",
    "gauge_transform",
    "verify_coulomb_gauge",
    "vector_potential_uniform_field",
    # Solid Angles and Cyclic Functions (Arts. 417-422)
    "CyclicFunction",
    "calc_solid_angle_closed_curve",
    "solid_angle_as_sphere_curve",
    "solid_angle_double_line_integral",
    "solid_angle_determinant",
    "vector_potential_closed_curve",
    "magnetic_shell_potential_jump",
    "solid_angle_planar_loop",
]
