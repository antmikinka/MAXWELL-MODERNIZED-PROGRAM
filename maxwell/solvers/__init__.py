"""
maxwell.solvers — Numerical solvers for magnetic induction problems.

This subpackage implements numerical methods for solving magnetic
induction problems from Maxwell's Treatise:
- Induction in arbitrary bodies (induction_solvers.py, Arts. 427-429)
- Boundary value problems
- Demagnetizing field calculations

Category: A (maxwell_original) — Maxwell's numerical methods.
"""

from __future__ import annotations

from maxwell.solvers.induction_solvers import (
    InductionProblem,
    InductionSolution,
    solve_induction_iterative,
    compute_demagnetizing_field,
    demagnetizing_factors,
    solve_ellipsoid_induction,
    solve_induction_with_boundary,
    verify_induction_solver,
)

from maxwell.solvers.shape_solvers import (
    CylindricalMagnet,
    RectangularMagnet,
    compare_shape_demagnetizing_factors,
    shape_magnetostatic_energy,
    optimize_shape_for_field,
    verify_shape_solvers,
)

__all__ = [
    # Induction Solvers (Arts. 427-429)
    "InductionProblem",
    "InductionSolution",
    "solve_induction_iterative",
    "compute_demagnetizing_field",
    "demagnetizing_factors",
    "solve_ellipsoid_induction",
    "solve_induction_with_boundary",
    "verify_induction_solver",
    # Shape Solvers (Arts. 439-440)
    "CylindricalMagnet",
    "RectangularMagnet",
    "compare_shape_demagnetizing_factors",
    "shape_magnetostatic_energy",
    "optimize_shape_for_field",
    "verify_shape_solvers",
]
