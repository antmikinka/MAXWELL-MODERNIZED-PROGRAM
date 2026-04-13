"""
Electrostatic equilibrium points, equipotential surfaces, and simple cases.

This module implements Maxwell's theory from Part I:

1. **Points & Lines of Equilibrium** (Arts. 112-116):
   - Points where the electric field vanishes (E = 0)
   - Lines of equilibrium and their properties
   - Saddle point analysis and stability

2. **Equipotential Surfaces** (Arts. 117-123):
   - Surfaces of constant potential V(x,y,z) = constant
   - Curvature of equipotential surfaces
   - Field line tracing as orthogonal trajectories
   - Surface charge density from potential gradient

3. **Simple Cases of Electrostatics** (Arts. 124-127):
   - Parallel plate capacitor (uniform field)
   - Concentric spheres (spherical symmetry)
   - Coaxial cylinders (cylindrical symmetry)
   - Isolated charged sphere

Category: A (maxwell_original) — Maxwell's theory of electrostatic equilibrium.

References:
    Part I, Chapter VI: Points & Lines of Equilibrium (Arts. 112-116).
    Part I, Chapter VII: Equipotential Surfaces (Arts. 117-123).
    Part I, Chapter VIII: Simple Cases of Electrostatics (Arts. 124-127).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple
import numpy as np
from scipy import optimize, ndimage

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


# =============================================================================
# POINTS & LINES OF EQUILIBRIUM (Arts. 112-116)
# =============================================================================

@maxwell_cite(
    112, 113, 114,
    part=1, chapter="Points & Lines of Equilibrium",
    theory_class="maxwell_original",
    description="Find points where electric field vanishes (E = 0)"
)
def equilibrium_points(
    potential_func: Callable[[np.ndarray], float],
    bounds: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
    grid_resolution: int = 20,
    tolerance: float = 1e-6,
) -> dict[str, np.ndarray | list[np.ndarray]]:
    """
    Find equilibrium points where the electric field vanishes.

    Arts. 112-114: Maxwell showed that at equilibrium points, the electric
    field E = -grad(V) = 0. These are critical points of the potential.

    Equilibrium points are classified as:
        - Stable: local minimum of V (for positive test charge)
        - Unstable: local maximum of V
        - Saddle: neither max nor min (most common in electrostatics)

    Maxwell proved (Art. 114) that stable equilibrium is impossible in
    a charge-free region (Earnshaw's theorem).

    Args:
        potential_func: Function V(r) returning potential at position r.
        bounds: Search bounds ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        grid_resolution: Number of grid points per dimension for initial search.
        tolerance: Convergence tolerance for root finding.

    Returns:
        Dictionary with:
        - equilibrium_points: List of positions where E = 0
        - point_types: Classification ('stable', 'unstable', 'saddle')
        - field_magnitudes: |E| at each point (should be ~0)

    Raises:
        ValueError: If no equilibrium points found in search region.

    References:
        Part I, Art. 112: Definition of equilibrium points.
        Part I, Art. 113: Conditions for equilibrium.
        Part I, Art. 114: Impossibility of stable equilibrium.

    Example:
        >>> # Two equal charges: equilibrium at midpoint
        >>> def V_two_charges(r):
        ...     r1 = np.linalg.norm(r - np.array([-1, 0, 0]))
        ...     r2 = np.linalg.norm(r - np.array([1, 0, 0]))
        ...     return 1/r1 + 1/r2
        >>> result = equilibrium_points(V_two_charges,
        ...     bounds=((-3, 3), (-3, 3), (-3, 3)))
        >>> print(f"Found {len(result['equilibrium_points'])} points")
    """
    bounds = tuple(tuple(b) for b in bounds)

    # Create search grid
    x_range = np.linspace(bounds[0][0], bounds[0][1], grid_resolution)
    y_range = np.linspace(bounds[1][0], bounds[1][1], grid_resolution)
    z_range = np.linspace(bounds[2][0], bounds[2][1], grid_resolution)

    # Find candidate regions where |E| might be small
    candidates = []

    def electric_field_magnitude(r):
        """Compute |E| = |grad(V)| using numerical differentiation."""
        h = 1e-7
        grad = np.zeros(3)
        for i in range(3):
            r_plus = r.copy()
            r_minus = r.copy()
            r_plus[i] += h
            r_minus[i] -= h
            grad[i] = (potential_func(r_plus) - potential_func(r_minus)) / (2 * h)
        return np.linalg.norm(grad)

    # Grid search for local minima of |E|
    local_minima = []
    for i, x in enumerate(x_range[1:-1], 1):
        for j, y in enumerate(y_range[1:-1], 1):
            for k, z in enumerate(z_range[1:-1], 1):
                r = np.array([x, y, z])
                E_mag = electric_field_magnitude(r)

                # Check if this is a local minimum
                is_minimum = True
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        for dk in [-1, 0, 1]:
                            if di == dj == dk == 0:
                                continue
                            ni, nj, nk = i + di, j + dj, k + dk
                            if 0 <= ni < grid_resolution and 0 <= nj < grid_resolution and 0 <= nk < grid_resolution:
                                r_neighbor = np.array([x_range[ni], y_range[nj], z_range[nk]])
                                if electric_field_magnitude(r_neighbor) < E_mag:
                                    is_minimum = False
                                    break
                        if not is_minimum:
                            break
                    if not is_minimum:
                        break

                if is_minimum and E_mag < 1.0:  # Threshold to exclude far-field
                    candidates.append(r)

    # Refine candidates using optimization
    equilibrium_points_list = []
    for candidate in candidates:
        result = optimize.minimize(
            electric_field_magnitude,
            candidate,
            method='Nelder-Mead',
            options={'xatol': tolerance, 'fatol': tolerance}
        )

        if result.success and result.fun < tolerance:
            # Check if this point is unique (not duplicate)
            is_duplicate = False
            for existing in equilibrium_points_list:
                if np.linalg.norm(result.x - existing) < tolerance * 10:
                    is_duplicate = True
                    break

            if not is_duplicate:
                equilibrium_points_list.append(result.x)

    if not equilibrium_points_list:
        # Return empty result if no points found
        return {
            "equilibrium_points": [],
            "point_types": [],
            "field_magnitudes": [],
            "search_bounds": bounds,
            "grid_resolution": grid_resolution,
        }

    # Classify each equilibrium point
    point_types = []
    field_magnitudes = []

    for point in equilibrium_points_list:
        # Compute Hessian of potential at this point
        hessian = _compute_hessian(potential_func, point)
        eigenvalues = np.linalg.eigvalsh(hessian)

        # Classify based on eigenvalues
        pos_eig = np.sum(eigenvalues > tolerance)
        neg_eig = np.sum(eigenvalues < -tolerance)

        if pos_eig == 3:
            point_type = 'stable'  # Local minimum
        elif neg_eig == 3:
            point_type = 'unstable'  # Local maximum
        else:
            point_type = 'saddle'  # Mixed (most common)

        point_types.append(point_type)
        field_magnitudes.append(electric_field_magnitude(point))

    return {
        "equilibrium_points": equilibrium_points_list,
        "point_types": point_types,
        "field_magnitudes": field_magnitudes,
        "search_bounds": bounds,
        "grid_resolution": grid_resolution,
    }


def _compute_hessian(func: Callable[[np.ndarray], float], x: np.ndarray, h: float = 1e-5) -> np.ndarray:
    """Compute numerical Hessian matrix of a scalar function."""
    n = len(x)
    hessian = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            x_pp = x.copy()
            x_pm = x.copy()
            x_mp = x.copy()
            x_mm = x.copy()

            x_pp[i] += h
            x_pp[j] += h
            x_pm[i] += h
            x_pm[j] -= h
            x_mp[i] -= h
            x_mp[j] += h
            x_mm[i] -= h
            x_mm[j] -= h

            hessian[i, j] = (func(x_pp) - func(x_pm) - func(x_mp) + func(x_mm)) / (4 * h * h)
            hessian[j, i] = hessian[i, j]

    return hessian


@maxwell_cite(
    115, 116,
    part=1, chapter="Points & Lines of Equilibrium",
    theory_class="maxwell_original",
    description="Find lines of equilibrium (continuous curves where E = 0)"
)
def equilibrium_lines(
    potential_func: Callable[[np.ndarray], float],
    seed_point: np.ndarray,
    direction: np.ndarray,
    step_size: float = 0.01,
    max_steps: int = 1000,
    tolerance: float = 1e-6,
) -> dict[str, np.ndarray | list[np.ndarray]]:
    """
    Trace lines of equilibrium where the electric field vanishes continuously.

    Arts. 115-116: Maxwell showed that in symmetric configurations,
    equilibrium points can form continuous lines or curves. Along such
    lines, E = 0 at every point.

    Examples:
        - Axis between two equal like charges: equilibrium circle in plane
        - Axis of rotational symmetry: equilibrium line along axis

    The algorithm traces the line by following the direction where |E|
    remains minimized.

    Args:
        potential_func: Function V(r) returning potential.
        seed_point: Starting point on the equilibrium line.
        direction: Initial direction to trace.
        step_size: Step size for tracing.
        max_steps: Maximum number of steps.
        tolerance: Tolerance for |E| = 0 condition.

    Returns:
        Dictionary with:
        - line_points: Array of positions along the equilibrium line
        - field_magnitudes: |E| at each point (should be ~0)
        - line_length: Total length of traced line
        - direction_vectors: Tangent direction at each point

    References:
        Part I, Art. 115: Lines of equilibrium.
        Part I, Art. 116: Properties of equilibrium lines.

    Example:
        >>> # Axis of symmetry for ring of charge
        >>> def V_ring(r):
        ...     rho = np.sqrt(r[0]**2 + r[1]**2)
        ...     z = r[2]
        ...     R = 1.0  # Ring radius
        ...     return 1/np.sqrt((rho-R)**2 + z**2)
        >>> result = equilibrium_lines(V_ring,
        ...     seed_point=np.array([0, 0, 0]),
        ...     direction=np.array([0, 0, 1]))
    """
    seed_point = np.asarray(seed_point, dtype=np.float64)
    direction = np.asarray(direction, dtype=np.float64)
    direction = direction / np.linalg.norm(direction)

    def electric_field(r):
        """Compute E = -grad(V)."""
        h = 1e-7
        grad = np.zeros(3)
        for i in range(3):
            r_plus = r.copy()
            r_minus = r.copy()
            r_plus[i] += h
            r_minus[i] -= h
            grad[i] = -(potential_func(r_plus) - potential_func(r_minus)) / (2 * h)
        return grad

    # Trace in positive direction
    points_forward = [seed_point.copy()]
    directions_forward = [direction.copy()]

    current_point = seed_point.copy()
    current_direction = direction.copy()

    for step in range(max_steps):
        # Move along current direction
        next_point = current_point + step_size * current_direction

        # Project to find equilibrium (minimize |E| perpendicular to line)
        E = electric_field(next_point)
        E_mag = np.linalg.norm(E)

        if E_mag > tolerance * 10:
            # Try to correct back to equilibrium line
            # Move in direction of -E (steepest descent)
            correction = -0.1 * E
            next_point += correction

        # Update direction (tangent to line)
        # Use the direction perpendicular to E
        if np.linalg.norm(E) > 1e-10:
            # Gram-Schmidt: remove component parallel to E
            current_direction = current_direction - np.dot(current_direction, E) * E / np.dot(E, E)
            if np.linalg.norm(current_direction) > 1e-10:
                current_direction = current_direction / np.linalg.norm(current_direction)

        points_forward.append(next_point.copy())
        directions_forward.append(current_direction.copy())
        current_point = next_point

        # Check if we've left the equilibrium region
        if E_mag > tolerance * 100:
            break

    # Trace in negative direction
    points_backward = [seed_point.copy()]
    current_point = seed_point.copy()
    current_direction = -direction.copy()

    for step in range(max_steps):
        next_point = current_point + step_size * current_direction
        E = electric_field(next_point)
        E_mag = np.linalg.norm(E)

        if E_mag > tolerance * 10:
            correction = -0.1 * E
            next_point += correction

        if np.linalg.norm(E) > 1e-10:
            current_direction = current_direction - np.dot(current_direction, E) * E / np.dot(E, E)
            if np.linalg.norm(current_direction) > 1e-10:
                current_direction = current_direction / np.linalg.norm(current_direction)

        points_backward.append(next_point.copy())
        current_point = next_point

        if E_mag > tolerance * 100:
            break

    # Combine (reverse backward to start from seed)
    points_backward.reverse()
    line_points = points_backward[:-1] + points_forward
    line_points = np.array(line_points)

    # Compute field magnitudes
    field_magnitudes = [np.linalg.norm(electric_field(p)) for p in line_points]

    # Compute line length
    line_length = sum(np.linalg.norm(line_points[i+1] - line_points[i])
                      for i in range(len(line_points)-1))

    return {
        "line_points": line_points,
        "field_magnitudes": field_magnitudes,
        "line_length": line_length,
        "seed_point": seed_point,
        "num_points": len(line_points),
    }


@maxwell_cite(
    113, 114, 115,
    part=1, chapter="Points & Lines of Equilibrium",
    theory_class="maxwell_original",
    description="Analyze stability and type of equilibrium points"
)
def saddle_point_analysis(
    potential_func: Callable[[np.ndarray], float],
    equilibrium_point: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Analyze the nature of an equilibrium point using the Hessian.

    Arts. 113-115: Maxwell analyzed equilibrium points by examining the
    second derivatives of the potential. The Hessian matrix determines
    the type of equilibrium:

    In charge-free regions, Laplace's equation requires:
        d²V/dx² + d²V/dy² + d²V/dz² = 0

    This means the sum of eigenvalues is zero, so:
        - Cannot have all positive (no stable equilibrium)
        - Cannot have all negative (no unstable equilibrium in vacuum)
        - Must have mixed signs (saddle point)

    This is Earnshaw's theorem: no stable electrostatic equilibrium.

    Args:
        potential_func: Function V(r) returning potential.
        equilibrium_point: Position of equilibrium point.

    Returns:
        Dictionary with:
        - equilibrium_point: Input position
        - hessian: 3x3 Hessian matrix at the point
        - eigenvalues: Eigenvalues of Hessian
        - eigenvectors: Principal directions
        - point_type: Classification ('saddle', 'stable', 'unstable')
        - laplacian: Trace of Hessian (should be 0 in vacuum)
        - principal_curvatures: Curvature along principal axes

    References:
        Part I, Art. 113: Conditions at equilibrium points.
        Part I, Art. 114: Impossibility of stable equilibrium.
        Part I, Art. 115: Saddle point properties.

    Example:
        >>> # Midpoint between two equal charges
        >>> def V(r):
        ...     return 1/np.linalg.norm(r - np.array([-1,0,0])) + 1/np.linalg.norm(r - np.array([1,0,0]))
        >>> result = saddle_point_analysis(V, np.array([0, 0, 0]))
        >>> print(f"Type: {result['point_type']}")
        >>> print(f"Eigenvalues: {result['eigenvalues']}")
    """
    equilibrium_point = np.asarray(equilibrium_point, dtype=np.float64)

    # Compute Hessian
    hessian = _compute_hessian(potential_func, equilibrium_point)

    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(hessian)

    # Laplacian (trace of Hessian)
    laplacian = np.trace(hessian)

    # Classify point
    tol = 1e-6
    pos_eig = np.sum(eigenvalues > tol)
    neg_eig = np.sum(eigenvalues < -tol)

    if pos_eig == 3:
        point_type = 'stable'
    elif neg_eig == 3:
        point_type = 'unstable'
    elif pos_eig == 2 and neg_eig == 1:
        point_type = 'saddle_2up_1down'
    elif pos_eig == 1 and neg_eig == 2:
        point_type = 'saddle_1up_2down'
    else:
        point_type = 'saddle'

    # Principal curvatures (eigenvalues of Hessian)
    principal_curvatures = eigenvalues

    return {
        "equilibrium_point": equilibrium_point,
        "hessian": hessian,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "point_type": point_type,
        "laplacian": laplacian,
        "principal_curvatures": principal_curvatures,
        "positive_curvature_directions": pos_eig,
        "negative_curvature_directions": neg_eig,
    }


# =============================================================================
# EQUIPOTENTIAL SURFACES (Arts. 117-123)
# =============================================================================

@maxwell_cite(
    117, 118, 119,
    part=1, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Generate equipotential surface V(x,y,z) = constant"
)
def equipotential_surface(
    potential_func: Callable[[np.ndarray], float],
    potential_value: float,
    bounds: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
    resolution: int = 50,
    marching_cubes: bool = True,
) -> dict[str, np.ndarray | float]:
    """
    Generate an equipotential surface for a given potential value.

    Arts. 117-119: Maxwell introduced equipotential surfaces as surfaces
    where the potential is constant: V(x,y,z) = V₀.

    Key properties:
        - Electric field is everywhere perpendicular to equipotentials
        - No work is done moving a charge along an equipotential
        - Conductors in equilibrium are equipotential volumes

    Args:
        potential_func: Function V(r) returning potential.
        potential_value: The constant potential value V₀.
        bounds: Grid bounds ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        resolution: Number of grid points per dimension.
        marching_cubes: If True, use marching cubes for surface extraction.

    Returns:
        Dictionary with:
        - surface_vertices: Vertices of the equipotential surface
        - surface_faces: Triangular faces connecting vertices
        - potential_value: The V₀ value
        - volume_enclosed: Volume enclosed by surface (if closed)
        - surface_area: Area of the equipotential surface

    References:
        Part I, Art. 117: Definition of equipotential surfaces.
        Part I, Art. 118: Properties of equipotentials.
        Part I, Art. 119: Relation to conductors.

    Example:
        >>> # Equipotential around point charge
        >>> def V(r):
        ...     return 1/np.linalg.norm(r)
        >>> result = equipotential_surface(V, potential_value=1.0,
        ...     bounds=((-2, 2), (-2, 2), (-2, 2)))
        >>> print(f"Surface area: {result['surface_area']:.2f}")
    """
    bounds = tuple(tuple(b) for b in bounds)

    # Create 3D grid
    x = np.linspace(bounds[0][0], bounds[0][1], resolution)
    y = np.linspace(bounds[1][0], bounds[1][1], resolution)
    z = np.linspace(bounds[2][0], bounds[2][1], resolution)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Evaluate potential on grid
    V_grid = np.zeros((resolution, resolution, resolution))
    for i in range(resolution):
        for j in range(resolution):
            for k in range(resolution):
                V_grid[i, j, k] = potential_func(np.array([X[i,j,k], Y[i,j,k], Z[i,j,k]]))

    # Extract isosurface using marching cubes
    if marching_cubes:
        try:
            from skimage import measure
            verts, faces, normals, values = measure.marching_cubes(
                V_grid, level=potential_value,
                spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
            )
            # Offset vertices to correct bounds
            verts[:, 0] += bounds[0][0]
            verts[:, 1] += bounds[1][0]
            verts[:, 2] += bounds[2][0]
        except ImportError:
            # Fallback: return grid data
            return {
                "potential_grid": V_grid,
                "grid_x": x,
                "grid_y": y,
                "grid_z": z,
                "potential_value": potential_value,
                "isosurface_level": potential_value,
                "note": "scikit-image not available; grid data returned",
            }
    else:
        # Return grid data for manual extraction
        return {
            "potential_grid": V_grid,
            "grid_x": x,
            "grid_y": y,
            "grid_z": z,
            "potential_value": potential_value,
        }

    # Compute surface area
    total_area = 0.0
    for face in faces:
        v0, v1, v2 = verts[face]
        # Area of triangle = 0.5 * |cross(v1-v0, v2-v0)|
        cross = np.cross(v1 - v0, v2 - v0)
        total_area += 0.5 * np.linalg.norm(cross)

    # Compute enclosed volume (using divergence theorem approximation)
    # For a closed surface: V = (1/3) * integral(r . n dA)
    volume = 0.0
    for face in faces:
        v0, v1, v2 = verts[face]
        centroid = (v0 + v1 + v2) / 3
        cross = np.cross(v1 - v0, v2 - v0)
        volume += np.dot(centroid, cross) / 6

    return {
        "surface_vertices": verts,
        "surface_faces": faces,
        "potential_value": potential_value,
        "surface_area": total_area,
        "volume_enclosed": abs(volume),
        "bounds": bounds,
        "resolution": resolution,
    }


@maxwell_cite(
    120, 121,
    part=1, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Compute curvature of equipotential surfaces"
)
def surface_curvature(
    potential_func: Callable[[np.ndarray], float],
    point: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Compute the curvature of an equipotential surface at a point.

    Arts. 120-121: Maxwell analyzed the curvature of equipotential
    surfaces. The principal curvatures are related to the field gradient.

    For an equipotential surface V = constant:
        - Principal curvatures κ₁, κ₂ describe the surface bending
        - Mean curvature H = (κ₁ + κ₂) / 2
        - Gaussian curvature K = κ₁ * κ₂

    Maxwell showed that in charge-free regions:
        κ₁ + κ₂ = -(1/|E|) * d|E|/dn

    where n is the normal direction to the surface.

    Args:
        potential_func: Function V(r) returning potential.
        point: Point on the equipotential surface.

    Returns:
        Dictionary with:
        - point: Input position
        - normal: Unit normal to surface (direction of E)
        - principal_curvatures: [κ₁, κ₂]
        - mean_curvature: H = (κ₁ + κ₂) / 2
        - gaussian_curvature: K = κ₁ * κ₂
        - field_magnitude: |E| at the point
        - field_gradient_normal: d|E|/dn

    References:
        Part I, Art. 120: Curvature of equipotential surfaces.
        Part I, Art. 121: Relation to field variation.

    Example:
        >>> # Curvature of spherical equipotential around point charge
        >>> def V(r):
        ...     return 1/np.linalg.norm(r)
        >>> result = surface_curvature(V, np.array([1, 0, 0]))
        >>> print(f"Mean curvature: {result['mean_curvature']}")
    """
    point = np.asarray(point, dtype=np.float64)
    h = 1e-6

    # Compute electric field E = -grad(V)
    grad_V = np.zeros(3)
    for i in range(3):
        r_plus = point.copy()
        r_minus = point.copy()
        r_plus[i] += h
        r_minus[i] -= h
        grad_V[i] = (potential_func(r_plus) - potential_func(r_minus)) / (2 * h)

    E = -grad_V
    E_mag = np.linalg.norm(E)

    if E_mag < 1e-10:
        # At equilibrium point, curvature is undefined
        return {
            "point": point,
            "normal": np.array([np.nan, np.nan, np.nan]),
            "principal_curvatures": np.array([np.nan, np.nan]),
            "mean_curvature": np.nan,
            "gaussian_curvature": np.nan,
            "field_magnitude": 0.0,
            "note": "Equilibrium point; curvature undefined",
        }

    # Unit normal (in direction of E)
    normal = E / E_mag

    # Compute Hessian of potential
    hessian = _compute_hessian(potential_func, point)

    # The shape operator (Weingarten map) for equipotential surface
    # S = -(I - nn^T) * H / |grad V|, where H is Hessian
    # Projected Hessian onto tangent plane

    # Projection matrix onto tangent plane
    P = np.eye(3) - np.outer(normal, normal)

    # Projected Hessian (restricted to tangent plane)
    H_tangent = P @ hessian @ P

    # Find eigenvalues in tangent plane
    # We need eigenvalues of H_tangent restricted to 2D tangent space

    # Find two orthonormal tangent vectors
    if abs(normal[0]) < 0.9:
        t1 = np.cross(normal, [1, 0, 0])
    else:
        t1 = np.cross(normal, [0, 1, 0])
    t1 = t1 / np.linalg.norm(t1)
    t2 = np.cross(normal, t1)
    t2 = t2 / np.linalg.norm(t2)

    # 2x2 matrix of H_tangent in tangent basis
    H_2d = np.array([
        [t1 @ H_tangent @ t1, t1 @ H_tangent @ t2],
        [t2 @ H_tangent @ t1, t2 @ H_tangent @ t2]
    ])

    # Eigenvalues give curvatures (with sign convention)
    eigvals = np.linalg.eigvalsh(H_2d)

    # Principal curvatures (with proper sign)
    # κ = -eigenvalue / |grad V| (negative because surface bends opposite to field)
    principal_curvatures = -eigvals / E_mag

    mean_curvature = np.mean(principal_curvatures)
    gaussian_curvature = np.prod(principal_curvatures)

    # Field gradient along normal
    E_plus = np.zeros(3)
    E_minus = np.zeros(3)
    for i in range(3):
        r_plus = point + h * normal
        r_minus = point - h * normal
        grad_V_plus = np.zeros(3)
        grad_V_minus = np.zeros(3)
        for j in range(3):
            rp = r_plus.copy()
            rm = r_minus.copy()
            rp[j] += h
            rm[j] -= h
            grad_V_plus[j] = (potential_func(rp) - potential_func(r_plus)) / h
            grad_V_minus[j] = (potential_func(rm) - potential_func(r_minus)) / h
        E_plus[i] = -np.dot(grad_V_plus, normal)
        E_minus[i] = -np.dot(grad_V_minus, normal)

    dE_dn = (np.linalg.norm(E + h * np.array([0, 0, 0])) - np.linalg.norm(E - h * np.array([0, 0, 0]))) / (2 * h)
    # Simplified: directional derivative of |E| along normal
    r_plus = point + h * normal
    r_minus = point - h * normal
    grad_plus = np.zeros(3)
    grad_minus = np.zeros(3)
    for i in range(3):
        rp = r_plus.copy()
        rm = r_minus.copy()
        rp[i] += h
        rm[i] -= h
        grad_plus[i] = (potential_func(rp) - potential_func(r_plus)) / (2 * h)
        grad_minus[i] = (potential_func(rm) - potential_func(r_minus)) / (2 * h)

    E_plus_mag = np.linalg.norm(grad_plus)
    E_minus_mag = np.linalg.norm(grad_minus)
    field_gradient_normal = (E_plus_mag - E_minus_mag) / (2 * h)

    return {
        "point": point,
        "normal": normal,
        "principal_curvatures": principal_curvatures,
        "mean_curvature": mean_curvature,
        "gaussian_curvature": gaussian_curvature,
        "field_magnitude": E_mag,
        "field_gradient_normal": field_gradient_normal,
        "potential_at_point": potential_func(point),
    }


@maxwell_cite(
    122, 123,
    part=1, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Trace field lines orthogonal to equipotentials"
)
def field_line_tracing(
    potential_func: Callable[[np.ndarray], float],
    seed_point: np.ndarray,
    max_length: float = 100.0,
    step_size: float = 0.01,
    direction: int = 1,
) -> dict[str, np.ndarray | float]:
    """
    Trace electric field lines as orthogonal trajectories to equipotentials.

    Arts. 122-123: Maxwell showed that field lines (lines of force) are
    everywhere orthogonal to equipotential surfaces. Field lines follow:

        dr/ds = E / |E| = -grad(V) / |grad(V)|

    where s is arc length along the field line.

    Field lines:
        - Start on positive charges and end on negative charges
        - Never cross (uniqueness of E direction)
        - Are perpendicular to conductor surfaces

    Args:
        potential_func: Function V(r) returning potential.
        seed_point: Starting point for field line.
        max_length: Maximum length to trace.
        step_size: Step size for integration.
        direction: +1 to follow E, -1 to go opposite.

    Returns:
        Dictionary with:
        - field_line: Array of positions along field line
        - potentials: Potential values at each point
        - field_magnitudes: |E| at each point
        - total_length: Arc length of traced line
        - start_point: Initial seed point
        - end_point: Final point

    References:
        Part I, Art. 122: Field lines as orthogonal trajectories.
        Part I, Art. 123: Properties of field lines.

    Example:
        >>> # Field line from point charge
        >>> def V(r):
        ...     return 1/np.linalg.norm(r)
        >>> result = field_line_tracing(V, seed_point=np.array([2, 0, 0]))
        >>> print(f"Line has {len(result['field_line'])} points")
    """
    seed_point = np.asarray(seed_point, dtype=np.float64)

    def electric_field(r):
        """Compute E = -grad(V)."""
        h = 1e-7
        grad = np.zeros(3)
        for i in range(3):
            r_plus = r.copy()
            r_minus = r.copy()
            r_plus[i] += h
            r_minus[i] -= h
            grad[i] = -(potential_func(r_plus) - potential_func(r_minus)) / (2 * h)
        return grad

    # Integrate field line using Runge-Kutta 4
    points = [seed_point.copy()]
    potentials = [potential_func(seed_point)]
    field_mags = [np.linalg.norm(electric_field(seed_point))]

    current_point = seed_point.copy()
    total_length = 0.0

    for step in range(int(max_length / step_size)):
        E = electric_field(current_point)
        E_mag = np.linalg.norm(E)

        if E_mag < 1e-10:
            # Reached equilibrium point or charge
            break

        # Normalize to get direction
        direction_vec = direction * E / E_mag

        # RK4 integration
        k1 = direction_vec

        E2 = electric_field(current_point + 0.5 * step_size * k1)
        k2 = direction * E2 / np.linalg.norm(E2) if np.linalg.norm(E2) > 1e-10 else k1

        E3 = electric_field(current_point + 0.5 * step_size * k2)
        k3 = direction * E3 / np.linalg.norm(E3) if np.linalg.norm(E3) > 1e-10 else k2

        E4 = electric_field(current_point + step_size * k3)
        k4 = direction * E4 / np.linalg.norm(E4) if np.linalg.norm(E4) > 1e-10 else k3

        next_point = current_point + (step_size / 6) * (k1 + 2*k2 + 2*k3 + k4)

        # Check if we've gone too far
        segment_length = np.linalg.norm(next_point - current_point)
        if total_length + segment_length > max_length:
            break

        points.append(next_point.copy())
        potentials.append(potential_func(next_point))
        field_mags.append(np.linalg.norm(electric_field(next_point)))

        current_point = next_point
        total_length += segment_length

    return {
        "field_line": np.array(points),
        "potentials": potentials,
        "field_magnitudes": field_mags,
        "total_length": total_length,
        "start_point": seed_point,
        "end_point": current_point,
        "num_points": len(points),
    }


@maxwell_cite(
    119, 120, 121,
    part=1, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Surface charge density σ = -ε₀ * ∂V/∂n"
)
def surface_charge_density(
    potential_func: Callable[[np.ndarray], float],
    surface_points: np.ndarray,
    surface_normals: np.ndarray,
    epsilon_0: float = 1.0,
) -> dict[str, np.ndarray | float]:
    """
    Calculate surface charge density from potential gradient.

    Arts. 119-121: Maxwell showed that the surface charge density on
    a conductor is related to the normal derivative of potential:

        σ = -ε₀ * (∂V/∂n) = ε₀ * E_n

    where ∂V/∂n is the derivative along the outward normal.

    For a conductor, the field inside is zero, so:
        E_n = |E| just outside the surface

    Args:
        potential_func: Function V(r) returning potential.
        surface_points: Points on the surface (N, 3).
        surface_normals: Outward unit normals at each point (N, 3).
        epsilon_0: Permittivity constant (default 1.0 in CGS-ESU).

    Returns:
        Dictionary with:
        - surface_charge_density: σ at each point
        - normal_field: E_n (normal component of E)
        - surface_points: Input points
        - total_charge: Total charge on surface (integral of σ)

    References:
        Part I, Art. 119: Surface charge on conductors.
        Part I, Arts. 120-121: Relation to field gradient.

    Example:
        >>> # Charged sphere
        >>> def V(r):
        ...     return 100/np.linalg.norm(r) if np.linalg.norm(r) > 1 else 100
        >>> points = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> normals = points  # For sphere, normal = position (unit)
        >>> result = surface_charge_density(V, points, normals)
        >>> print(f"σ = {result['surface_charge_density']}")
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    surface_normals = np.asarray(surface_normals, dtype=np.float64)

    h = 1e-6

    def electric_field(r):
        """Compute E = -grad(V)."""
        grad = np.zeros(3)
        for i in range(3):
            r_plus = r.copy()
            r_minus = r.copy()
            r_plus[i] += h
            r_minus[i] -= h
            grad[i] = -(potential_func(r_plus) - potential_func(r_minus)) / (2 * h)
        return grad

    # Compute surface charge density at each point
    sigma = np.zeros(len(surface_points))
    normal_field = np.zeros(len(surface_points))

    for i, (point, normal) in enumerate(zip(surface_points, surface_normals)):
        E = electric_field(point)
        E_n = np.dot(E, normal)  # Normal component
        normal_field[i] = E_n

        # σ = ε₀ * E_n (outward normal, E points in direction of force on + charge)
        sigma[i] = epsilon_0 * E_n

    # Estimate total charge using simple area weighting
    # ( assumes points are roughly uniformly distributed)
    if len(surface_points) > 0:
        # Approximate area per point (crude estimate)
        avg_spacing = np.mean([
            np.linalg.norm(surface_points[i] - surface_points[j])
            for i in range(min(10, len(surface_points)))
            for j in range(i+1, min(10, len(surface_points)))
        ])
        area_per_point = avg_spacing ** 2
        total_charge = np.sum(sigma) * area_per_point
    else:
        total_charge = 0.0

    return {
        "surface_charge_density": sigma,
        "normal_field": normal_field,
        "surface_points": surface_points,
        "total_charge": total_charge,
        "epsilon_0": epsilon_0,
    }


# =============================================================================
# SIMPLE CASES OF ELECTROSTATICS (Arts. 124-127)
# =============================================================================

@maxwell_cite(
    124,
    part=1, chapter="Simple Cases of Electrostatics",
    theory_class="maxwell_original",
    description="Potential and field of isolated charged sphere"
)
def isolated_sphere(
    total_charge: float,
    radius: float,
    evaluation_points: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Calculate potential and field of an isolated charged conducting sphere.

    Art. 124: Maxwell analyzed the simplest case: a single isolated
    conducting sphere with total charge Q.

    For r >= R (outside sphere):
        V(r) = Q / r
        E(r) = Q / r² * r_hat

    For r < R (inside sphere):
        V(r) = Q / R (constant)
        E(r) = 0

    The sphere is an equipotential volume with V = Q/R on its surface.

    Args:
        total_charge: Total charge Q (statcoulombs).
        radius: Sphere radius R (cm).
        evaluation_points: Points where V and E are computed.

    Returns:
        Dictionary with:
        - potentials: V at each evaluation point
        - electric_fields: E vector at each point
        - field_magnitudes: |E| at each point
        - surface_potential: V at r = R
        - capacitance: Self-capacitance (R in CGS-ESU)

    References:
        Part I, Art. 124: Charged sphere solution.

    Example:
        >>> result = isolated_sphere(
        ...     total_charge=100, radius=5.0,
        ...     evaluation_points=np.array([[10, 0, 0], [0, 10, 0]])
        ... )
        >>> print(f"V at r=10: {result['potentials'][0]}")
    """
    evaluation_points = np.asarray(evaluation_points, dtype=np.float64)
    if evaluation_points.ndim == 1:
        evaluation_points = evaluation_points.reshape(1, -1)

    n_points = len(evaluation_points)
    potentials = np.zeros(n_points)
    electric_fields = np.zeros((n_points, 3))
    field_magnitudes = np.zeros(n_points)

    for i, point in enumerate(evaluation_points):
        r = np.linalg.norm(point)

        if r < radius:
            # Inside: constant potential, zero field
            potentials[i] = total_charge / radius
            electric_fields[i] = np.zeros(3)
            field_magnitudes[i] = 0.0
        else:
            # Outside: point charge formula
            potentials[i] = total_charge / r
            if r > 1e-10:
                r_hat = point / r
                electric_fields[i] = (total_charge / r ** 2) * r_hat
                field_magnitudes[i] = abs(total_charge) / r ** 2

    surface_potential = total_charge / radius
    capacitance = radius  # Self-capacitance of isolated sphere in CGS-ESU

    return {
        "potentials": potentials,
        "electric_fields": electric_fields,
        "field_magnitudes": field_magnitudes,
        "surface_potential": surface_potential,
        "capacitance": capacitance,
        "total_charge": total_charge,
        "radius": radius,
    }


@maxwell_cite(
    124, 125,
    part=1, chapter="Simple Cases of Electrostatics",
    theory_class="maxwell_original",
    description="Uniform field between parallel plate capacitor"
)
def parallel_plate_capacitor(
    plate_potential: float,
    plate_separation: float,
    plate_area: float = None,
    evaluation_points: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate field and capacitance of parallel plate capacitor.

    Arts. 124-125: Maxwell analyzed the parallel plate capacitor as a
    fundamental case with uniform electric field.

    For infinite plates (or plates large compared to separation):
        E = V / d (uniform, directed from + to - plate)
        σ = E / (4π) = V / (4πd) (surface charge density)

    Capacitance:
        C = A / (4πd) (CGS-ESU)
        C = ε₀A / d (SI)

    Maxwell noted edge effects cause field fringing near plate boundaries.

    Args:
        plate_potential: Potential difference V between plates (statvolts).
        plate_separation: Distance d between plates (cm).
        plate_area: Plate area A (cm²). Optional for capacitance.
        evaluation_points: Points for field evaluation. Optional.

    Returns:
        Dictionary with:
        - electric_field: Uniform E = V/d (statvolts/cm)
        - surface_charge_density: σ on plates
        - capacitance: C (statfarads) if area provided
        - energy_density: u = E²/(8π) (erg/cm³)
        - total_energy: U = CV²/2 if area provided

    References:
        Part I, Art. 124: Uniform field case.
        Part I, Art. 125: Capacitance and energy.

    Example:
        >>> result = parallel_plate_capacitor(
        ...     plate_potential=100, plate_separation=1.0,
        ...     plate_area=100.0
        ... )
        >>> print(f"E = {result['electric_field']} statV/cm")
        >>> print(f"C = {result['capacitance']:.2f} statF")
    """
    # Uniform electric field (directed from + to - plate)
    electric_field_magnitude = plate_potential / plate_separation

    # Surface charge density (CGS-ESU: σ = E / (4π))
    surface_charge_density = electric_field_magnitude / (4 * np.pi)

    # Energy density
    energy_density = electric_field_magnitude ** 2 / (8 * np.pi)

    result = {
        "electric_field": electric_field_magnitude,
        "electric_field_vector": np.array([electric_field_magnitude, 0, 0]),
        "surface_charge_density": surface_charge_density,
        "plate_potential": plate_potential,
        "plate_separation": plate_separation,
        "energy_density": energy_density,
    }

    if plate_area is not None:
        # Capacitance C = A / (4πd) in CGS-ESU
        capacitance = plate_area / (4 * np.pi * plate_separation)
        result["capacitance"] = capacitance
        result["total_energy"] = 0.5 * capacitance * plate_potential ** 2
        result["plate_area"] = plate_area

    if evaluation_points is not None:
        evaluation_points = np.asarray(evaluation_points, dtype=np.float64)
        if evaluation_points.ndim == 1:
            evaluation_points = evaluation_points.reshape(1, -1)

        # Compute potential at each point (assuming plates at x=0 and x=d)
        potentials = np.zeros(len(evaluation_points))
        fields = np.zeros((len(evaluation_points), 3))

        for i, point in enumerate(evaluation_points):
            x = point[0] if len(point) > 0 else 0
            # Linear potential: V(x) = V * (1 - x/d) for 0 <= x <= d
            if 0 <= x <= plate_separation:
                potentials[i] = plate_potential * (1 - x / plate_separation)
                fields[i, 0] = electric_field_magnitude

        result["evaluation_potentials"] = potentials
        result["evaluation_fields"] = fields

    return result


@maxwell_cite(
    126,
    part=1, chapter="Simple Cases of Electrostatics",
    theory_class="maxwell_original",
    description="Potential between concentric spheres"
)
def concentric_spheres(
    inner_potential: float,
    outer_potential: float,
    inner_radius: float,
    outer_radius: float,
    evaluation_points: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate potential and field between concentric spherical conductors.

    Art. 126: Maxwell solved the case of two concentric spherical
    conductors with different potentials.

    With spherical symmetry, Laplace's equation gives:
        V(r) = A + B/r

    Boundary conditions V(R₁) = V₁, V(R₂) = V₂ determine A and B:
        V(r) = V₁ + (V₂ - V₁) * (R₁/r - R₁/R₂) / (R₁/R₂ - 1)

    Or equivalently:
        V(r) = (V₁*R₁*(R₂-r) + V₂*R₂*(r-R₁)) / (r*(R₂-R₁))

    Electric field:
        E(r) = -dV/dr = (V₁ - V₂) * R₁*R₂ / ((R₂ - R₁) * r²)

    Capacitance of spherical capacitor:
        C = R₁*R₂ / (R₂ - R₁) (CGS-ESU)

    Args:
        inner_potential: V₁ on inner sphere (statvolts).
        outer_potential: V₂ on outer sphere (statvolts).
        inner_radius: R₁ radius of inner sphere (cm).
        outer_radius: R₂ radius of outer sphere (cm).
        evaluation_points: Points for evaluation. Optional.

    Returns:
        Dictionary with:
        - potential_function: A, B coefficients for V(r) = A + B/r
        - capacitance: C of the spherical capacitor
        - field_at_inner: E at r = R₁
        - field_at_outer: E at r = R₂
        - evaluation_results: V and E at specified points

    References:
        Part I, Art. 126: Concentric spheres solution.

    Example:
        >>> result = concentric_spheres(
        ...     inner_potential=100, outer_potential=0,
        ...     inner_radius=1.0, outer_radius=5.0
        ... )
        >>> print(f"C = {result['capacitance']:.2f} statF")
    """
    R1, R2 = inner_radius, outer_radius
    V1, V2 = inner_potential, outer_potential

    if R1 >= R2:
        raise ValueError("Inner radius must be less than outer radius")

    # Coefficients for V(r) = A + B/r
    # V1 = A + B/R1
    # V2 = A + B/R2
    # Solving: B = (V1 - V2) / (1/R1 - 1/R2) = (V1 - V2) * R1 * R2 / (R2 - R1)
    #        A = V1 - B/R1

    B = (V1 - V2) * R1 * R2 / (R2 - R1)
    A = V1 - B / R1

    # Capacitance C = R1*R2 / (R2 - R1) in CGS-ESU
    capacitance = R1 * R2 / (R2 - R1)

    # Electric field at boundaries
    # E(r) = B / r² (radially outward if B > 0)
    E_inner = B / R1 ** 2
    E_outer = B / R2 ** 2

    result = {
        "coefficient_A": A,
        "coefficient_B": B,
        "potential_formula": "V(r) = A + B/r",
        "capacitance": capacitance,
        "field_at_inner": E_inner,
        "field_at_outer": E_outer,
        "inner_potential": V1,
        "outer_potential": V2,
        "inner_radius": R1,
        "outer_radius": R2,
    }

    if evaluation_points is not None:
        evaluation_points = np.asarray(evaluation_points, dtype=np.float64)
        if evaluation_points.ndim == 1:
            evaluation_points = evaluation_points.reshape(1, -1)

        potentials = np.zeros(len(evaluation_points))
        fields = np.zeros((len(evaluation_points), 3))
        field_magnitudes = np.zeros(len(evaluation_points))

        for i, point in enumerate(evaluation_points):
            r = np.linalg.norm(point)

            if r < R1:
                # Inside inner sphere: constant potential
                potentials[i] = V1
                fields[i] = np.zeros(3)
            elif r > R2:
                # Outside outer sphere: constant potential
                potentials[i] = V2
                fields[i] = np.zeros(3)
            else:
                # Between spheres
                potentials[i] = A + B / r
                r_hat = point / r if r > 1e-10 else np.zeros(3)
                fields[i] = (B / r ** 2) * r_hat
                field_magnitudes[i] = abs(B) / r ** 2

        result["evaluation_potentials"] = potentials
        result["evaluation_fields"] = fields
        result["evaluation_field_magnitudes"] = field_magnitudes

    return result


@maxwell_cite(
    127,
    part=1, chapter="Simple Cases of Electrostatics",
    theory_class="maxwell_original",
    description="Potential between coaxial cylinders"
)
def coaxial_cylinders(
    inner_potential: float,
    outer_potential: float,
    inner_radius: float,
    outer_radius: float,
    evaluation_points: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate potential and field between coaxial cylindrical conductors.

    Art. 127: Maxwell solved the case of two coaxial cylindrical
    conductors (coaxial cable geometry).

    With cylindrical symmetry, Laplace's equation gives:
        V(r) = A * ln(r) + B

    Boundary conditions V(R₁) = V₁, V(R₂) = V₂ determine A and B:
        A = (V1 - V2) / ln(R1/R2)
        B = V1 - A * ln(R1)

    Electric field (radial):
        E(r) = -dV/dr = -A / r = (V1 - V2) / (r * ln(R2/R1))

    Capacitance per unit length:
        C' = 1 / (2 * ln(R2/R1)) (CGS-ESU, per cm)
        C' = 2πε₀ / ln(R2/R1) (SI)

    Args:
        inner_potential: V₁ on inner cylinder (statvolts).
        outer_potential: V₂ on outer cylinder (statvolts).
        inner_radius: R₁ radius of inner cylinder (cm).
        outer_radius: R₂ radius of outer cylinder (cm).
        evaluation_points: Points for evaluation. Optional.

    Returns:
        Dictionary with:
        - potential_function: A, B coefficients for V(r) = A*ln(r) + B
        - capacitance_per_length: C' per unit length
        - field_at_inner: E at r = R₁
        - field_at_outer: E at r = R₂
        - evaluation_results: V and E at specified points

    References:
        Part I, Art. 127: Coaxial cylinders solution.

    Example:
        >>> result = coaxial_cylinders(
        ...     inner_potential=100, outer_potential=0,
        ...     inner_radius=0.1, outer_radius=1.0
        ... )
        >>> print(f"C' = {result['capacitance_per_length']:.2f} statF/cm")
    """
    R1, R2 = inner_radius, outer_radius
    V1, V2 = inner_potential, outer_potential

    if R1 >= R2:
        raise ValueError("Inner radius must be less than outer radius")

    # Coefficients for V(r) = A * ln(r) + B
    # V1 = A * ln(R1) + B
    # V2 = A * ln(R2) + B
    # Solving: A = (V1 - V2) / ln(R1/R2)
    #          B = V1 - A * ln(R1)

    ln_ratio = np.log(R1 / R2)
    A = (V1 - V2) / ln_ratio
    B = V1 - A * np.log(R1)

    # Capacitance per unit length (CGS-ESU)
    # C' = 1 / (2 * ln(R2/R1))
    capacitance_per_length = 1.0 / (2 * np.log(R2 / R1))

    # Electric field at boundaries
    # E(r) = -A / r
    E_inner = -A / R1
    E_outer = -A / R2

    result = {
        "coefficient_A": A,
        "coefficient_B": B,
        "potential_formula": "V(r) = A * ln(r) + B",
        "capacitance_per_length": capacitance_per_length,
        "field_at_inner": E_inner,
        "field_at_outer": E_outer,
        "inner_potential": V1,
        "outer_potential": V2,
        "inner_radius": R1,
        "outer_radius": R2,
    }

    if evaluation_points is not None:
        evaluation_points = np.asarray(evaluation_points, dtype=np.float64)
        if evaluation_points.ndim == 1:
            evaluation_points = evaluation_points.reshape(1, -1)

        potentials = np.zeros(len(evaluation_points))
        fields = np.zeros((len(evaluation_points), 3))
        field_magnitudes = np.zeros(len(evaluation_points))

        for i, point in enumerate(evaluation_points):
            # Cylindrical radius (distance from z-axis)
            r = np.sqrt(point[0] ** 2 + point[1] ** 2)
            z = point[2] if len(point) > 2 else 0

            if r < R1:
                # Inside inner cylinder
                potentials[i] = V1
                fields[i] = np.zeros(3)
            elif r > R2:
                # Outside outer cylinder
                potentials[i] = V2
                fields[i] = np.zeros(3)
            else:
                # Between cylinders
                potentials[i] = A * np.log(r) + B
                # Field is radial in cylindrical coordinates
                if r > 1e-10:
                    r_hat = np.array([point[0]/r, point[1]/r, 0])
                    fields[i] = (-A / r) * r_hat
                    field_magnitudes[i] = abs(A) / r

        result["evaluation_potentials"] = potentials
        result["evaluation_fields"] = fields
        result["evaluation_field_magnitudes"] = field_magnitudes

    return result


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EQUILIBRIUM SURFACES AND SIMPLE ELECTROSTATICS")
    print("Maxwell's Treatise, Part I (Arts. 112-127)")
    print("=" * 70)

    # Test equilibrium points
    print("\n--- Equilibrium Points (Arts. 112-114) ---")
    def V_two_charges(r):
        r1 = np.linalg.norm(r - np.array([-1, 0, 0]))
        r2 = np.linalg.norm(r - np.array([1, 0, 0]))
        return 1/r1 + 1/r2

    result = equilibrium_points(V_two_charges, bounds=((-3, 3), (-3, 3), (-3, 3)), grid_resolution=15)
    print(f"  Found {len(result['equilibrium_points'])} equilibrium points")
    if result['equilibrium_points']:
        for i, (pt, ptype) in enumerate(zip(result['equilibrium_points'], result['point_types'])):
            print(f"    Point {i}: {pt} - Type: {ptype}")

    # Test saddle point analysis
    print("\n--- Saddle Point Analysis (Arts. 113-115) ---")
    result = saddle_point_analysis(V_two_charges, np.array([0, 0, 0]))
    print(f"  At origin: type = {result['point_type']}")
    print(f"  Eigenvalues: {result['eigenvalues']}")
    print(f"  Laplacian: {result['laplacian']:.2e} (should be ~0)")

    # Test equipotential surface
    print("\n--- Equipotential Surfaces (Arts. 117-119) ---")
    def V_point_charge(r):
        return 1 / max(np.linalg.norm(r), 0.1)

    result = equipotential_surface(V_point_charge, potential_value=1.0,
                                    bounds=((-3, 3), (-3, 3), (-3, 3)), resolution=30)
    if 'surface_area' in result:
        print(f"  V = 1.0 equipotential: area = {result['surface_area']:.2f}")
        print(f"  Volume enclosed: {result['volume_enclosed']:.2f}")

    # Test surface curvature
    print("\n--- Surface Curvature (Arts. 120-121) ---")
    result = surface_curvature(V_point_charge, np.array([1, 0, 0]))
    print(f"  At r=(1,0,0): mean curvature = {result['mean_curvature']:.2f}")
    print(f"  Gaussian curvature: {result['gaussian_curvature']:.2f}")

    # Test field line tracing
    print("\n--- Field Line Tracing (Arts. 122-123) ---")
    result = field_line_tracing(V_point_charge, seed_point=np.array([2, 0, 0]),
                                 max_length=10.0, step_size=0.1)
    print(f"  Field line: {result['num_points']} points traced")
    print(f"  Total length: {result['total_length']:.2f}")

    # Test surface charge density
    print("\n--- Surface Charge Density (Arts. 119-121) ---")
    sphere_points = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])
    sphere_normals = sphere_points.copy()
    result = surface_charge_density(V_point_charge, sphere_points, sphere_normals)
    print(f"  Surface charge density: {result['surface_charge_density']}")
    print(f"  (sigma values shown above)")

    # Test isolated sphere
    print("\n--- Isolated Sphere (Art. 124) ---")
    result = isolated_sphere(total_charge=100, radius=5.0,
                              evaluation_points=np.array([[10, 0, 0], [5, 0, 0]]))
    print(f"  V at r=10: {result['potentials'][0]:.2f}")
    print(f"  V at surface: {result['potentials'][1]:.2f}")
    print(f"  Capacitance: {result['capacitance']}")

    # Test parallel plate capacitor
    print("\n--- Parallel Plate Capacitor (Arts. 124-125) ---")
    result = parallel_plate_capacitor(plate_potential=100, plate_separation=1.0,
                                       plate_area=100.0)
    print(f"  E = {result['electric_field']:.2f} statV/cm")
    print(f"  Surface charge density: {result['surface_charge_density']:.4f} statC/cm^2")
    print(f"  C = {result['capacitance']:.2f} statF")

    # Test concentric spheres
    print("\n--- Concentric Spheres (Art. 126) ---")
    result = concentric_spheres(inner_potential=100, outer_potential=0,
                                 inner_radius=1.0, outer_radius=5.0)
    print(f"  Capacitance: {result['capacitance']:.2f} statF")
    print(f"  E at inner: {result['field_at_inner']:.2f}")
    print(f"  E at outer: {result['field_at_outer']:.2f}")

    # Test coaxial cylinders
    print("\n--- Coaxial Cylinders (Art. 127) ---")
    result = coaxial_cylinders(inner_potential=100, outer_potential=0,
                                inner_radius=0.1, outer_radius=1.0)
    print(f"  C' = {result['capacitance_per_length']:.4f} statF/cm")
    print(f"  E at inner: {result['field_at_inner']:.2f}")
    print(f"  E at outer: {result['field_at_outer']:.2f}")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)
