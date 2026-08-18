"""
Cyclic functions and solid angles — topology of magnetic fields.

Implements the theory of cyclic functions from Part III of Maxwell's Treatise:
- Solid angle of a closed curve (Arts. 417-418)
- Solid angle as spherical curve (Art. 419)
- Double line integral for solid angle (Art. 420)
- Determinant formulation (Art. 421)
- Cyclic functions and their properties (Art. 422)

Maxwell shows that the solid angle subtended by a closed curve
is a cyclic function — it increases by 4π each time the observation
point passes through the surface bounded by the curve.

The solid angle is fundamental to computing the potential of
magnetic shells and current loops.

Category: A (maxwell_original) — Maxwell's theory of cyclic functions.

References:
    Part III, Arts. 417-422: Solid angles and cyclic functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class CyclicFunction:
    """
    Cyclic function — function with branch cuts.

    Art. 422: A cyclic function is one that increases by a fixed
    amount (the period) each time a point traverses a certain
    closed curve or surface.

    The solid angle Ω subtended by a closed loop is cyclic:
    - Ω increases by 4π when the point passes through the loop
    - Ω is multi-valued: Ω + 4πn for any integer n

    This is analogous to the complex logarithm or argument function.

    Attributes:
        base_function: The underlying single-valued function.
        period: Amount added per cycle (4π for solid angle).
        branch_surface: Surface defining the branch cut.
    """

    base_function: Callable[[np.ndarray], float]
    period: float = 4 * np.pi
    branch_surface: np.ndarray = None  # Points defining branch cut surface

    @classmethod
    @maxwell_cite(
        422,
        part=3,
        chapter="Cyclic Functions",
        theory_class="maxwell_original",
        description="Create cyclic function from solid angle",
    )
    def from_solid_angle(
        cls,
        solid_angle_func: Callable[[np.ndarray], float],
        loop_curve: np.ndarray,
    ) -> CyclicFunction:
        """
        Create cyclic function from solid angle of a loop.

        Art. 422: The solid angle of a closed loop is the canonical
        cyclic function in magnetism.

        Args:
            solid_angle_func: Function computing solid angle Ω.
            loop_curve: Points defining the closed loop.

        Returns:
            CyclicFunction object.

        Reference:
            Part III, Art. 422: Cyclic nature of solid angle.
        """
        return cls(
            base_function=solid_angle_func,
            period=4 * np.pi,
            branch_surface=loop_curve,
        )

    def evaluate(self, point: np.ndarray, sheet: int = 0) -> float:
        """
        Evaluate cyclic function on a specific Riemann sheet.

        Args:
            point: Position where function is evaluated.
            sheet: Integer specifying which sheet (0 = principal).

        Returns:
            Function value on specified sheet.
        """
        base_value = self.base_function(point)
        return base_value + sheet * self.period


@maxwell_cite(
    417,
    part=3,
    chapter="Solid Angles",
    theory_class="maxwell_original",
    description="Calculate solid angle of closed curve",
)
def calc_solid_angle_closed_curve(
    loop_curve: np.ndarray,
    observation_point: np.ndarray,
) -> float:
    """
    Calculate solid angle subtended by a closed curve.

    Art. 417: The solid angle Ω subtended by a closed curve C
    at an observation point P is the area on the unit sphere
    centered at P that is enclosed by the projection of C.

    For a planar loop with area A and normal n:
        Ω = A * (r̂ · n) / r²  (small angle approximation)

    Exact formula via line integral:
        Ω = ∮_C (r × dl) · r̂ / r²

    Args:
        loop_curve: Array of points defining closed loop (N, 3).
        observation_point: Point where solid angle is computed (cm).

    Returns:
        Solid angle Ω (steradians). Range: -4π to +4π.

    Reference:
        Part III, Art. 417: Solid angle of closed curve.

    Note:
        The sign depends on orientation: positive when the
        loop is traversed counterclockwise as seen from P.
    """
    loop_curve = np.asarray(loop_curve, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    if len(loop_curve.shape) != 2 or loop_curve.shape[1] != 3:
        raise ValueError("loop_curve must be (N, 3) array")

    # Ensure loop is closed
    if not np.allclose(loop_curve[0], loop_curve[-1]):
        loop_curve = np.vstack([loop_curve, loop_curve[0]])

    # Compute solid angle via line integral formula
    # Ω = ∮ (r × dl) · r̂ / r² = ∮ (r × dl) / r³

    Omega = 0.0

    for i in range(len(loop_curve) - 1):
        r1 = loop_curve[i] - observation_point
        r2 = loop_curve[i + 1] - observation_point
        dl = r2 - r1

        # Use midpoint for r
        r_mid = (r1 + r2) / 2
        r_mag = np.linalg.norm(r_mid)

        if r_mag < 1e-10:
            # Point is on the curve — solid angle is undefined
            # Return limiting value from one side
            continue

        # (r × dl) · r̂ / r²
        cross = np.cross(r_mid, dl)
        Omega += float(np.dot(cross, r_mid)) / (r_mag**3)

    return Omega


@maxwell_cite(
    418,
    part=3,
    chapter="Solid Angles",
    theory_class="maxwell_original",
    description="Solid angle as spherical curve area",
)
def solid_angle_as_sphere_curve(
    loop_curve: np.ndarray,
    observation_point: np.ndarray,
    num_sample_points: int = 1000,
) -> float:
    """
    Calculate solid angle by projecting curve onto sphere.

    Art. 418: The solid angle equals the area on the unit sphere
    enclosed by the spherical curve formed by projecting the loop.

    This function computes the area by:
    1. Projecting loop points onto unit sphere centered at observation point
    2. Computing spherical polygon area using Girard's theorem

    Args:
        loop_curve: Array of points defining closed loop (N, 3).
        observation_point: Point where solid angle is computed.
        num_sample_points: Number of points for sampling.

    Returns:
        Solid angle Ω (steradians).

    Reference:
        Part III, Art. 418: Spherical curve interpretation.
    """
    loop_curve = np.asarray(loop_curve, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    # Project curve onto unit sphere
    directions = loop_curve - observation_point
    distances = np.linalg.norm(directions, axis=1, keepdims=True)

    # Handle zero distances (point on curve)
    mask = distances[:, 0] > 1e-10
    if not np.any(mask):
        return 0.0  # Degenerate case

    directions = directions[mask]
    distances = distances[mask]
    unit_directions = directions / distances

    if len(unit_directions) < 3:
        return 0.0  # Not enough points

    # Compute spherical polygon area using excess angle formula
    # For a spherical polygon: Area = Σ(interior angles) - (n-2)π

    # Compute angles between consecutive great circle arcs
    total_angle = 0.0
    n = len(unit_directions)

    for i in range(n):
        prev = unit_directions[i - 1]  # Handles wrap-around
        curr = unit_directions[i]
        next_pt = unit_directions[(i + 1) % n]

        # Great circle arc directions (tangent vectors)
        tangent_in = curr - np.dot(curr, prev) * prev
        tangent_out = next_pt - np.dot(next_pt, curr) * curr

        # Normalize
        t_in_mag = np.linalg.norm(tangent_in)
        t_out_mag = np.linalg.norm(tangent_out)

        if t_in_mag > 1e-10 and t_out_mag > 1e-10:
            tangent_in = tangent_in / t_in_mag
            tangent_out = tangent_out / t_out_mag

            # Angle between tangents
            cos_angle = np.dot(tangent_in, tangent_out)
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle = np.arccos(cos_angle)
            total_angle += angle

    # Spherical excess
    Omega = total_angle - (n - 2) * np.pi

    # Normalize to [-2π, 2π] range
    while Omega > 2 * np.pi:
        Omega -= 4 * np.pi
    while Omega < -2 * np.pi:
        Omega += 4 * np.pi

    return Omega


@maxwell_cite(
    419,
    part=3,
    chapter="Solid Angles",
    theory_class="maxwell_original",
    description="Gauss's double line integral for solid angle",
)
def solid_angle_double_line_integral(
    loop1: np.ndarray,
    loop2: np.ndarray,
) -> float:
    """
    Calculate solid angle using Gauss's double line integral.

    Art. 419: Gauss discovered that the solid angle can be expressed
    as a double line integral over two curves — the loop and an
    auxiliary curve at infinity.

    For practical computation, we use:
        Ω = ∮_C1 ∮_C2 (r1 - r2) · (dl1 × dl2) / |r1 - r2|³

    This is related to the linking number of two curves.

    Args:
        loop1: First closed loop (N, 3).
        loop2: Second closed loop (M, 3) — often taken as
               a reference curve or the observer's path.

    Returns:
        Double line integral value (related to linking number).

    Reference:
        Part III, Art. 419: Gauss's double integral.
    """
    loop1 = np.asarray(loop1, dtype=np.float64)
    loop2 = np.asarray(loop2, dtype=np.float64)

    if len(loop1.shape) != 2 or loop1.shape[1] != 3:
        raise ValueError("loop1 must be (N, 3) array")
    if len(loop2.shape) != 2 or loop2.shape[1] != 3:
        raise ValueError("loop2 must be (M, 3) array")

    # Ensure loops are closed
    if not np.allclose(loop1[0], loop1[-1]):
        loop1 = np.vstack([loop1, loop1[0]])
    if not np.allclose(loop2[0], loop2[-1]):
        loop2 = np.vstack([loop2, loop2[0]])

    integral = 0.0

    for i in range(len(loop1) - 1):
        r1a = loop1[i]
        r1b = loop1[i + 1]
        dl1 = r1b - r1a
        r1_mid = (r1a + r1b) / 2

        for j in range(len(loop2) - 1):
            r2a = loop2[j]
            r2b = loop2[j + 1]
            dl2 = r2b - r2a
            r2_mid = (r2a + r2b) / 2

            r_vec = r1_mid - r2_mid
            r_mag = np.linalg.norm(r_vec)

            if r_mag < 1e-10:
                continue

            # (dl1 × dl2) · r̂ / r²
            cross = np.cross(dl1, dl2)
            integral += float(np.dot(cross, r_vec)) / (r_mag**3)

    return integral


@maxwell_cite(
    420,
    part=3,
    chapter="Solid Angles",
    theory_class="maxwell_original",
    description="Determinant formulation of solid angle",
)
def solid_angle_determinant(
    triangle_vertices: np.ndarray,
    observation_point: np.ndarray,
) -> float:
    """
    Calculate solid angle of a triangle using determinant formula.

    Art. 420: For a triangular surface element, the solid angle
    can be computed using a determinant formulation.

    Given three vertices r1, r2, r3 and observation point P:
        Ω = 2 * arctan(det([r1-P, r2-P, r3-P]) / (r1·r2×r3 + ...))

    where the denominator involves dot and cross products.

    Args:
        triangle_vertices: Three vertices of triangle (3, 3).
        observation_point: Point where solid angle is computed.

    Returns:
        Solid angle of triangle (steradians).

    Reference:
        Part III, Art. 420: Determinant formula.
    """
    triangle_vertices = np.asarray(triangle_vertices, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    if triangle_vertices.shape != (3, 3):
        raise ValueError("triangle_vertices must be (3, 3) array")

    # Vectors from observation point to vertices
    r1 = triangle_vertices[0] - observation_point
    r2 = triangle_vertices[1] - observation_point
    r3 = triangle_vertices[2] - observation_point

    r1_mag = np.linalg.norm(r1)
    r2_mag = np.linalg.norm(r2)
    r3_mag = np.linalg.norm(r3)

    if min(r1_mag, r2_mag, r3_mag) < 1e-10:
        return 0.0  # Degenerate

    # Unit vectors
    n1 = r1 / r1_mag
    n2 = r2 / r2_mag
    n3 = r3 / r3_mag

    # Determinant (triple product)
    det = np.dot(n1, np.cross(n2, n3))

    # Denominator: 1 + n1·n2 + n2·n3 + n3·n1
    denom = 1.0 + np.dot(n1, n2) + np.dot(n2, n3) + np.dot(n3, n1)

    # Solid angle
    if abs(denom) < 1e-15:
        # Special case: triangle covers hemisphere
        return 2 * np.pi * np.sign(det)

    Omega = 2.0 * np.arctan2(det, denom)

    return Omega


@maxwell_cite(
    421,
    part=3,
    chapter="Cyclic Functions",
    theory_class="maxwell_original",
    description="Vector potential of closed curve via solid angle",
)
def vector_potential_closed_curve(
    loop_curve: np.ndarray,
    current: float,
    observation_point: np.ndarray,
) -> np.ndarray:
    """
    Calculate vector potential of current loop via solid angle.

    Art. 421: The vector potential of a closed current loop can
    be expressed in terms of the solid angle:

        A = (I/c) ∇Ω

    where Ω is the solid angle subtended by the loop.

    This is equivalent to the magnetic shell formulation where
    the loop is replaced by a magnetic shell of strength I/c.

    Args:
        loop_curve: Points defining the current loop (N, 3).
        current: Current in loop (abamperes, CGS-EMU).
        observation_point: Point where A is calculated.

    Returns:
        Vector potential A (gauss·cm).

    Reference:
        Part III, Art. 421: A from solid angle.
    """
    loop_curve = np.asarray(loop_curve, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    # Compute solid angle and its gradient
    h = 1e-6

    def solid_angle_at(point: np.ndarray) -> float:
        return calc_solid_angle_closed_curve(loop_curve, point)

    # Numerical gradient
    grad_Omega = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        Omega_plus = solid_angle_at(observation_point + delta)
        Omega_minus = solid_angle_at(observation_point - delta)
        grad_Omega[i] = (Omega_plus - Omega_minus) / (2 * h)

    # A = (I/c) ∇Ω
    A = (current / CONST.C) * grad_Omega

    return A


@maxwell_cite(
    422,
    part=3,
    chapter="Cyclic Functions",
    theory_class="maxwell_original",
    description="Cyclic function period for magnetic shell",
)
def magnetic_shell_potential_jump(
    shell_strength: float,
) -> float:
    """
    Calculate potential jump across magnetic shell.

    Art. 422: When crossing a magnetic shell (current loop),
    the scalar potential jumps by:

        ΔΩ = 4π * (shell strength)

    For a current loop, shell strength = I/c, so:
        ΔΩ = 4πI/c

    This is the cyclic period of the potential function.

    Args:
        shell_strength: Magnetic shell strength Φ (for current loop, I/c).

    Returns:
        Potential jump ΔΩ (gauss·cm).

    Reference:
        Part III, Art. 422: Potential jump across shell.
    """
    return 4 * np.pi * shell_strength


@maxwell_cite(
    417,
    418,
    419,
    420,
    421,
    422,
    part=3,
    chapter="Solid Angles and Cyclic Functions",
    theory_class="maxwell_original",
    description="Solid angle of planar loop",
)
def solid_angle_planar_loop(
    loop_vertices: np.ndarray,
    observation_point: np.ndarray,
) -> float:
    """
    Calculate solid angle of a planar polygonal loop.

    Art. 417-422: For a planar polygon, the solid angle can be
    computed exactly by summing contributions from each edge.

    Uses the formula:
        Ω = Σ_i arctan[(r_i × r_{i+1}) · n / (r_i · r_{i+1} + r_i r_{i+1})]

    where n is the plane normal and r_i are vectors to vertices.

    Args:
        loop_vertices: Vertices of planar polygon (N, 3).
        observation_point: Point where solid angle is computed.

    Returns:
        Solid angle Ω (steradians).

    Reference:
        Part III, Arts. 417-422: Planar loop solid angle.
    """
    loop_vertices = np.asarray(loop_vertices, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    if len(loop_vertices) < 3:
        return 0.0

    # Ensure closed
    if not np.allclose(loop_vertices[0], loop_vertices[-1]):
        loop_vertices = np.vstack([loop_vertices, loop_vertices[0]])

    # Compute plane normal from vertices
    v1 = loop_vertices[1] - loop_vertices[0]
    v2 = loop_vertices[2] - loop_vertices[0]
    normal = np.cross(v1, v2)
    normal_mag = np.linalg.norm(normal)

    if normal_mag < 1e-15:
        return 0.0  # Degenerate (collinear points)

    normal = normal / normal_mag

    # Compute solid angle by summing edge contributions
    Omega = 0.0
    n = len(loop_vertices)

    for i in range(n - 1):
        r1 = loop_vertices[i] - observation_point
        r2 = loop_vertices[i + 1] - observation_point

        r1_mag = np.linalg.norm(r1)
        r2_mag = np.linalg.norm(r2)

        if min(r1_mag, r2_mag) < 1e-10:
            continue

        # Cross product
        cross = np.cross(r1, r2)
        cross_dot_n = float(np.dot(cross, normal))

        # Denominator
        denom = r1_mag * r2_mag + np.dot(r1, r2)

        if abs(denom) < 1e-15:
            # Edge subtends 180 degrees
            angle = np.pi * np.sign(cross_dot_n)
        else:
            angle = np.arctan2(cross_dot_n, denom)

        Omega += angle

    return Omega
