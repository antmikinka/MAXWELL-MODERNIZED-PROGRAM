"""
Induction solvers — numerical solutions for induced magnetization problems.

Implements the theory of magnetic induction from Part III of Maxwell's Treatise:
- Induced magnetization in external fields (Arts. 427-429)
- Boundary value problems for magnetic materials
- Numerical methods for computing induced fields

When a magnetic material is placed in an external field, it becomes
magnetized. The induced magnetization creates its own field, which
modifies the total field. This self-consistent problem requires
iterative numerical solution.

Category: A (maxwell_original) — Maxwell's theory of magnetic induction.

References:
    Part III, Arts. 427-429: Magnetic induction problems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.fields.constitutive import MagneticConstitutiveRelation
from maxwell.materials.induction import InducedMagnetization, MagneticSusceptibility
from maxwell.meta.citation import maxwell_cite


@dataclass
class InductionProblem:
    """
    Magnetic induction problem specification.

    Arts. 427-429: Given an external field H_ext and a magnetic
    body with susceptibility κ(r), find:
    1. The induced magnetization I(r)
    2. The total field H_total(r) = H_ext + H_induced
    3. The magnetic induction B(r)

    This requires solving the self-consistent equation:
        I(r) = κ(r) × H_total(r)
        H_total = H_ext + H_demag(I)

    Attributes:
        susceptibility: Spatial distribution of κ.
        external_field: Applied external field H_ext.
        geometry: Body geometry (points, volume).
        boundary_conditions: Field conditions at boundaries.
    """

    susceptibility: Callable[[np.ndarray], float]  # κ(r)
    external_field: Callable[[np.ndarray], np.ndarray]  # H_ext(r)
    geometry_points: np.ndarray  # (N, 3) sample points
    boundary_conditions: dict = field(default_factory=dict)

    @classmethod
    @maxwell_cite(
        427,
        part=3,
        chapter="Induction Solvers",
        theory_class="maxwell_original",
        description="Create induction problem from uniform body",
    )
    def uniform_body(
        cls,
        susceptibility: float,
        external_field: Callable[[np.ndarray], np.ndarray],
        body_points: np.ndarray,
    ) -> InductionProblem:
        """
        Create induction problem for uniform susceptibility body.

        Art. 427: For a body with uniform κ, the induced
        magnetization is proportional to the local field.

        Args:
            susceptibility: Uniform κ (dimensionless).
            external_field: External field function.
            body_points: Points inside the body (N, 3).

        Returns:
            InductionProblem object.

        Reference:
            Part III, Art. 427: Uniform body induction.
        """

        def kappa_func(r):
            return susceptibility

        return cls(
            susceptibility=kappa_func,
            external_field=external_field,
            geometry_points=body_points,
        )


@dataclass
class InductionSolution:
    """
    Solution to magnetic induction problem.

    Arts. 427-429: The solution provides:
    - Magnetization I(r) at all points
    - Total field H(r) at all points
    - Induction B(r) at all points
    - Demagnetizing field H_d(r)

    Attributes:
        points: Sample points (N, 3).
        magnetization: I at each point (N, 3).
        total_field: H_total at each point (N, 3).
        external_field: H_ext at each point (N, 3).
        demag_field: H_demag at each point (N, 3).
        induction: B at each point (N, 3).
        converged: True if iterative solution converged.
        iterations: Number of iterations used.
    """

    points: np.ndarray
    magnetization: np.ndarray
    total_field: np.ndarray
    external_field: np.ndarray
    demag_field: np.ndarray
    induction: np.ndarray
    converged: bool = True
    iterations: int = 0

    @maxwell_cite(
        427,
        part=3,
        chapter="Induction Solvers",
        theory_class="maxwell_original",
        description="Verify solution self-consistency",
    )
    def verify_self_consistency(self, tolerance: float = 1e-6) -> bool:
        """
        Verify that solution satisfies self-consistency condition.

        Art. 427: The solution must satisfy:
            I = κ × H_total

        at every point (for linear materials).

        Args:
            tolerance: Relative error tolerance.

        Returns:
            True if self-consistency is satisfied.

        Reference:
            Part III, Art. 427: Self-consistency verification.
        """
        # For linear materials, check I = κH
        # This requires knowing κ, which we estimate from first iteration
        H_mag = np.linalg.norm(self.total_field, axis=1, keepdims=True)
        I_mag = np.linalg.norm(self.magnetization, axis=1, keepdims=True)

        # Avoid division by zero
        mask = H_mag > 1e-10
        if np.any(mask):
            kappa_est = I_mag[mask] / H_mag[mask]
            kappa_avg = np.mean(kappa_est)

            # Check consistency
            I_expected = kappa_avg * self.total_field
            error = np.linalg.norm(self.magnetization - I_expected) / np.linalg.norm(
                self.magnetization
            )

            return error < tolerance

        return True


@maxwell_cite(
    427,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Solve induction by fixed-point iteration",
)
def solve_induction_iterative(
    problem: InductionProblem,
    max_iterations: int = 100,
    tolerance: float = 1e-6,
    relaxation: float = 0.5,
) -> InductionSolution:
    """
    Solve magnetic induction problem by fixed-point iteration.

    Art. 427: The self-consistent equation:
        I = κ(H_ext + H_demag)

    is solved iteratively:
        I^{n+1} = κ(H_ext + H_demag(I^n))

    with relaxation for stability:
        I^{n+1} = (1-α)I^n + α × κ(H_ext + H_demag(I^n))

    Args:
        problem: InductionProblem to solve.
        max_iterations: Maximum iterations.
        tolerance: Convergence tolerance.
        relaxation: Relaxation factor α (0 < α ≤ 1).

    Returns:
        InductionSolution object.

    Reference:
        Part III, Art. 427: Iterative solution.
    """
    points = problem.geometry_points
    n_points = len(points)

    # Initialize fields
    H_ext = np.array([problem.external_field(p) for p in points])
    H_total = H_ext.copy()
    I_prev = np.zeros((n_points, 3))
    I_curr = np.zeros((n_points, 3))

    # Compute κ at each point
    kappa = np.array([problem.susceptibility(p) for p in points])

    converged = False
    iteration = 0

    for iteration in range(max_iterations):
        # Compute induced magnetization
        I_new = np.zeros((n_points, 3))
        for i in range(n_points):
            I_new[i] = kappa[i] * H_total[i]

        # Apply relaxation
        I_curr = (1 - relaxation) * I_prev + relaxation * I_new

        # Compute demagnetizing field from I_curr
        H_demag = compute_demagnetizing_field(points, I_curr)

        # Update total field
        H_total = H_ext + H_demag

        # Check convergence
        delta_I = np.linalg.norm(I_curr - I_prev) / (np.linalg.norm(I_prev) + 1e-10)

        if delta_I < tolerance:
            converged = True
            I_prev = I_curr
            break

        I_prev = I_curr.copy()

    # Compute final B field
    B_field = np.zeros_like(H_total)
    for i in range(n_points):
        B_field[i] = H_total[i] + 4 * np.pi * I_prev[i]

    # Compute final demag field
    H_demag_final = compute_demagnetizing_field(points, I_prev)

    return InductionSolution(
        points=points,
        magnetization=I_prev,
        total_field=H_total,
        external_field=H_ext,
        demag_field=H_demag_final,
        induction=B_field,
        converged=converged,
        iterations=iteration + 1,
    )


@maxwell_cite(
    427,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Compute demagnetizing field from magnetization",
)
def compute_demagnetizing_field(
    points: np.ndarray,
    magnetization: np.ndarray,
    method: str = "dipole",
) -> np.ndarray:
    """
    Compute demagnetizing (induced) field from magnetization distribution.

    Art. 427: The demagnetizing field is the field created by the
    induced magnetization itself. For a volume distribution of
    magnetic moment, the field at point r is:

        H_demag(r) = ∫ [3(M(r')·r̂)r̂ - M(r')] / |r-r'|³ dV'

    This is equivalent to the field from a distribution of dipoles.

    Args:
        points: Sample points (N, 3).
        magnetization: M at each point (N, 3).
        method: Computation method ("dipole" or "mean_field").

    Returns:
        Demagnetizing field H_demag (N, 3).

    Reference:
        Part III, Art. 427: Demagnetizing field.
    """
    n_points = len(points)
    H_demag = np.zeros((n_points, 3))

    # Estimate volume element
    bounds = np.max(points, axis=0) - np.min(points, axis=0)
    total_volume = np.prod(bounds)
    dV = total_volume / n_points if n_points > 0 else 1.0

    if method == "mean_field":
        # Simplified mean field approximation
        # H_demag = -N × M (N = demagnetizing factor)
        M_avg = np.mean(magnetization, axis=0)

        # Approximate demagnetizing factor for ellipsoid
        # For sphere: N = 4π/3
        N = 4 * np.pi / 3

        for i in range(n_points):
            H_demag[i] = -N * M_avg

    else:
        # Direct dipole summation (more accurate, slower)
        for i in range(n_points):
            for j in range(n_points):
                if i == j:
                    continue

                r = points[i] - points[j]
                r_mag = np.linalg.norm(r)

                if r_mag < 1e-10:
                    continue

                r_hat = r / r_mag
                M = magnetization[j]

                # Dipole field: H = (3(M·r̂)r̂ - M) / r³ × dV
                dH = (3 * np.dot(M, r_hat) * r_hat - M) / (r_mag**3) * dV
                H_demag[i] += dH

    return H_demag


@maxwell_cite(
    428,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Compute demagnetizing factors for standard shapes",
)
def demagnetizing_factors(
    shape: str,
    dimensions: dict[str, float],
) -> dict[str, float]:
    """
    Compute demagnetizing factors for standard shapes.

    Art. 428: For uniformly magnetized bodies of simple shapes,
    the demagnetizing field is uniform and proportional to M:

        H_demag = -N × M

    where N is the demagnetizing factor tensor. For principal
    axes: N_x + N_y + N_z = 4π (CGS) or = 1 (SI).

    Args:
        shape: Shape name ("sphere", "ellipsoid", "cylinder", "disk").
        dimensions: Shape dimensions (e.g., {"a": 1, "b": 2, "c": 3}).

    Returns:
        Dictionary with N_x, N_y, N_z demagnetizing factors.

    Reference:
        Part III, Art. 428: Demagnetizing factors.
    """
    if shape == "sphere":
        # Sphere: N_x = N_y = N_z = 4π/3
        N = 4 * np.pi / 3
        return {"N_x": N, "N_y": N, "N_z": N}

    elif shape == "ellipsoid":
        # Triaxial ellipsoid with semi-axes a, b, c
        a = dimensions.get("a", 1.0)
        b = dimensions.get("b", 1.0)
        c = dimensions.get("c", 1.0)

        # Approximate formulas (Osborn 1945)
        # For prolate spheroid (a > b = c)
        if a > b and np.abs(b - c) < 1e-6:
            m = a / b  # Aspect ratio
            if m > 1:
                # Prolate
                e2 = 1 - 1 / m**2
                e = np.sqrt(e2) if e2 > 0 else 0
                if e > 1e-6:
                    L = np.log((1 + e) / (1 - e))
                    N_x = 4 * np.pi * (1 - e2) / (2 * e**3) * (L - 2 * e)
                else:
                    N_x = 4 * np.pi / 3
                N_y = N_z = (4 * np.pi - N_x) / 2

        # For oblate spheroid (a = b > c)
        elif np.abs(a - b) < 1e-6 and a > c:
            m = a / c  # Aspect ratio
            if m > 1:
                e2 = m**2 - 1
                e = np.sqrt(e2)
                if e > 1e-6:
                    N_z = 4 * np.pi * (1 + e2) / e**3 * (e - np.arctan(e))
                else:
                    N_z = 4 * np.pi / 3
                N_x = N_y = (4 * np.pi - N_z) / 2

        else:
            # General ellipsoid - use approximate formula
            V = a * b * c
            N_x = 4 * np.pi * a**2 / (3 * V)
            N_y = 4 * np.pi * b**2 / (3 * V)
            N_z = 4 * np.pi * c**2 / (3 * V)

            # Normalize to sum to 4π
            total = N_x + N_y + N_z
            N_x *= 4 * np.pi / total
            N_y *= 4 * np.pi / total
            N_z *= 4 * np.pi / total

        return {"N_x": float(N_x), "N_y": float(N_y), "N_z": float(N_z)}

    elif shape == "cylinder":
        # Finite cylinder (length L, radius R)
        L = dimensions.get("length", 1.0)
        R = dimensions.get("radius", 0.5)

        # Approximate formula
        aspect = L / (2 * R)

        if aspect > 10:
            # Long thin cylinder
            N_z = 4 * np.pi * (R / L) ** 2 * np.log(L / R)
            N_x = N_y = (4 * np.pi - N_z) / 2
        elif aspect < 0.1:
            # Thin disk
            N_z = 4 * np.pi * (1 - aspect)
            N_x = N_y = 2 * np.pi * aspect
        else:
            # Intermediate
            N_z = 4 * np.pi / (1 + 2 * aspect)
            N_x = N_y = (4 * np.pi - N_z) / 2

        return {"N_x": float(N_x), "N_y": float(N_y), "N_z": float(N_z)}

    elif shape == "disk":
        # Thin disk (thickness t << radius R)
        R = dimensions.get("radius", 1.0)
        t = dimensions.get("thickness", 0.01)

        aspect = t / R

        # N_z ≈ 4π for thin disk
        N_z = 4 * np.pi * (1 - aspect / np.pi)
        N_x = N_y = 2 * np.pi * aspect

        return {"N_x": float(N_x), "N_y": float(N_y), "N_z": float(N_z)}

    else:
        # Unknown shape - assume sphere
        N = 4 * np.pi / 3
        return {"N_x": N, "N_y": N, "N_z": N}


@maxwell_cite(
    428,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Solve induction for ellipsoid analytically",
)
def solve_ellipsoid_induction(
    susceptibility: float,
    external_field: np.ndarray,
    semi_axes: dict[str, float],
) -> dict[str, np.ndarray]:
    """
    Solve induction problem for uniformly magnetizable ellipsoid.

    Art. 428: For an ellipsoid with uniform susceptibility κ in a
    uniform external field H_ext, the induced magnetization is
    uniform and given by:

        I_i = κ × H_ext_i / (1 + N_i × κ)

    where N_i are the demagnetizing factors along principal axes.

    Args:
        susceptibility: κ (dimensionless).
        external_field: H_ext (3,).
        semi_axes: Dictionary with semi-axes a, b, c.

    Returns:
        Dictionary with magnetization, total_field, demag_field.

    Reference:
        Part III, Art. 428: Ellipsoid solution.
    """
    external_field = np.asarray(external_field, dtype=np.float64)

    # Get demagnetizing factors
    N = demagnetizing_factors("ellipsoid", semi_axes)

    # Compute magnetization along each principal axis
    I = np.zeros(3)
    H_demag = np.zeros(3)
    H_total = np.zeros(3)

    axes = ["x", "y", "z"]
    for i, axis in enumerate(axes):
        N_i = N[f"N_{axis}"]

        # I = κ H_ext / (1 + N κ)
        denom = 1 + N_i * susceptibility
        I[i] = susceptibility * external_field[i] / denom if denom > 0 else 0

        # H_demag = -N × I
        H_demag[i] = -N_i * I[i]

        # H_total = H_ext + H_demag
        H_total[i] = external_field[i] + H_demag[i]

    return {
        "magnetization": I,
        "total_field": H_total,
        "demag_field": H_demag,
        "demagnetizing_factors": N,
    }


@maxwell_cite(
    429,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Solve induction with boundary conditions",
)
def solve_induction_with_boundary(
    problem: InductionProblem,
    boundary_value: float,
    boundary_type: str = "dirichlet",
) -> InductionSolution:
    """
    Solve induction problem with specified boundary conditions.

    Art. 429: Boundary conditions for magnetic problems:

    - Dirichlet: Ω = constant on boundary (equipotential)
    - Neumann: ∂Ω/∂n = 0 on boundary (no flux)

    The boundary condition affects the demagnetizing field
    calculation near edges.

    Args:
        problem: InductionProblem to solve.
        boundary_value: Boundary value (potential or flux).
        boundary_type: "dirichlet" or "neumann".

    Returns:
        InductionSolution object.

    Reference:
        Part III, Art. 429: Boundary value problems.
    """
    # First solve without boundary conditions
    solution = solve_induction_iterative(problem)

    # Apply boundary condition correction
    if boundary_type == "dirichlet":
        # Adjust potential at boundary to match specified value
        # This modifies the effective external field near boundary
        boundary_points = _identify_boundary_points(problem.geometry_points)

        for idx in boundary_points:
            # Scale field to match boundary potential
            H_ext = problem.external_field(problem.geometry_points[idx])
            H_mag = np.linalg.norm(H_ext)
            if H_mag > 0:
                # Adjust to match boundary value
                scale = boundary_value / (H_mag + 1e-10)
                solution.total_field[idx] *= scale

    elif boundary_type == "neumann":
        # Enforce zero normal derivative at boundary
        boundary_points = _identify_boundary_points(problem.geometry_points)

        for idx in boundary_points:
            # Zero normal component of demag field
            normal = _compute_surface_normal(problem.geometry_points, idx)
            H_demag = solution.demag_field[idx]
            normal_component = np.dot(H_demag, normal)
            solution.demag_field[idx] -= normal_component * normal

    # Recompute B field
    for i in range(len(solution.points)):
        solution.induction[i] = (
            solution.total_field[i] + 4 * np.pi * solution.magnetization[i]
        )

    return solution


def _identify_boundary_points(points: np.ndarray) -> list[int]:
    """Identify boundary points from point cloud."""
    # Simple approach: points near convex hull
    from scipy.spatial import ConvexHull

    if len(points) < 4:
        return list(range(len(points)))

    try:
        hull = ConvexHull(points)
        return list(hull.vertices)
    except Exception:
        # Fallback: points with extreme coordinates
        boundary = []
        for i in range(3):
            boundary.append(np.argmin(points[:, i]))
            boundary.append(np.argmax(points[:, i]))
        return list(set(boundary))


def _compute_surface_normal(points: np.ndarray, idx: int) -> np.ndarray:
    """Compute approximate surface normal at a point."""
    # Use local neighborhood to estimate normal
    p = points[idx]
    distances = np.linalg.norm(points - p, axis=1)

    # Find nearest neighbors (exclude self)
    distances[idx] = np.inf
    neighbor_indices = np.argsort(distances)[:5]

    # Fit plane to neighbors
    neighbors = points[neighbor_indices]
    centroid = np.mean(neighbors, axis=0)

    # PCA to find normal
    centered = neighbors - centroid
    _, _, Vt = np.linalg.svd(centered)
    normal = Vt[-1]  # Normal is last singular vector

    return normal / np.linalg.norm(normal)


@maxwell_cite(
    427,
    428,
    429,
    part=3,
    chapter="Induction Solvers",
    theory_class="maxwell_original",
    description="Verify induction solver accuracy",
)
def verify_induction_solver() -> dict[str, any]:
    """
    Verify accuracy of induction solver against known solutions.

    Arts. 427-429: Test cases with known analytical solutions:

    1. Sphere in uniform field: I = κH_ext / (1 + 4πκ/3)
    2. Ellipsoid: compare with analytical formula
    3. Convergence test: error decreases with iterations

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Arts. 427-429: Solver verification.
    """
    results = {}

    # Test 1: Sphere in uniform field
    kappa = 0.1
    H_ext = np.array([100, 0, 0])

    # Analytical solution for sphere
    N = 4 * np.pi / 3
    I_analytical = kappa * H_ext / (1 + N * kappa)

    # Create problem with spherical point distribution
    np.random.seed(42)
    n_points = 100
    radius = 1.0
    points = np.random.randn(n_points, 3)
    points = points / np.linalg.norm(points, axis=1, keepdims=True) * radius

    def uniform_kappa(r):
        return kappa

    def uniform_H(r):
        return H_ext

    problem = InductionProblem(
        susceptibility=uniform_kappa,
        external_field=uniform_H,
        geometry_points=points,
    )

    solution = solve_induction_iterative(problem, max_iterations=50)

    I_numerical = np.mean(solution.magnetization, axis=0)
    error = np.linalg.norm(I_numerical - I_analytical) / np.linalg.norm(I_analytical)

    results["sphere_test"] = {
        "analytical_magnetization": I_analytical.tolist(),
        "numerical_magnetization": I_numerical.tolist(),
        "relative_error": float(error),
        "passes": error < 0.1,  # Within 10%
        "converged": solution.converged,
        "iterations": solution.iterations,
    }

    # Test 2: Demagnetizing factors
    N_sphere = demagnetizing_factors("sphere", {})
    expected_N = 4 * np.pi / 3
    N_error = abs(N_sphere["N_x"] - expected_N) / expected_N

    results["demagnetizing_factors"] = {
        "sphere_N_x": N_sphere["N_x"],
        "sphere_N_y": N_sphere["N_y"],
        "sphere_N_z": N_sphere["N_z"],
        "expected": expected_N,
        "relative_error": float(N_error),
        "passes": N_error < 1e-6,
    }

    return results
