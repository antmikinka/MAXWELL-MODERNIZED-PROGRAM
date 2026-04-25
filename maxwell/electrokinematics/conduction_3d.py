"""
Conduction in Three Dimensions (Arts. 285-296).

Implements Maxwell's theory of three-dimensional current conduction as
described in Part II, Chapter VII (Arts. 285-296):

- Current density and generalized Ohm's law (Arts. 285-288)
- Anisotropic conductivity and principal axes (Arts. 288-290)
- Continuity equation for steady and time-varying currents (Arts. 291-292)
- Point source solutions and spreading resistance (Arts. 293-295)
- Boundary conditions at interfaces (Art. 296)

This module extends circuit theory to continuous media, providing the
foundation for understanding current flow in bulk conductors, electrolytes,
and semiconductors.

All calculations use CGS-EMU units:
    - Current density: abamperes/cm²
    - Electric field: abvolts/cm
    - Conductivity: siemens/cm (abΩ^-1 cm^-1)
    - Resistivity: abΩ·cm

Category: A (maxwell_original) — Maxwell's theory of 3D conduction.

References:
    Part II, Chapter VII: Conduction in Three Dimensions (Arts. 285-296).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np
from functools import wraps

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, C


# =============================================================================
# CURRENT DENSITY AND OHM'S LAW 3D (Arts. 285-288)
# =============================================================================

@maxwell_cite(
    285, 286, 287,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Generalized Ohm's law in 3D: J = sigma * E"
)
def ohms_law_3d(
    electric_field: np.ndarray,
    conductivity: float | np.ndarray,
    position: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate current density from electric field using Ohm's law.

    Arts. 285-287: Maxwell generalized Ohm's law to three dimensions,
    relating the current density vector J to the electric field E:

        J = sigma * E

    where:
        - J = current density (abamperes/cm²)
        - sigma = electrical conductivity (siemens/cm)
        - E = electric field (abvolts/cm)

    For isotropic conductors, sigma is a scalar. For anisotropic materials
    (crystals, layered structures), sigma is a 3×3 tensor.

    Maxwell states: "The current is proportional to the electromotive force
    and inversely proportional to the resistance," extended to three dimensions.

    Args:
        electric_field: Electric field vector E (abvolts/cm), shape (3,) or (..., 3).
        conductivity: Electrical conductivity. Can be:
                     - Scalar (isotropic material)
                     - 3×3 array (anisotropic material, conductivity tensor)
                     - Function of position sigma(x, y, z)
        position: Optional position (x, y, z) for spatially varying conductivity.

    Returns:
        Current density vector J (abamperes/cm²), same shape as electric_field.

    Raises:
        ValueError: If conductivity tensor is not symmetric positive definite.

    References:
        Part II, Art. 285: Current density definition.
        Part II, Art. 286: Ohm's law in three dimensions.
        Part II, Art. 287: Relation between current and field.

    Example:
        >>> # Isotropic conductor: sigma = 1 S/cm, E = (1, 0, 0) abV/cm
        >>> J = ohms_law_3d(np.array([1.0, 0.0, 0.0]), conductivity=1.0)
        >>> print(f"J = {J} abA/cm²")  # J = [1. 0. 0.] abA/cm²

        >>> # Anisotropic conductor with tensor conductivity
        >>> sigma = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 0.5]])
        >>> J = ohms_law_3d(np.array([1.0, 1.0, 1.0]), sigma)
        >>> print(f"J = {J} abA/cm²")  # J = [2. 1. 0.5] abA/cm²
    """
    electric_field = np.asarray(electric_field, dtype=np.float64)

    # Handle callable conductivity (spatially varying)
    if callable(conductivity):
        if position is None:
            raise ValueError("position required for callable conductivity")
        conductivity = conductivity(position)

    sigma = conductivity if isinstance(conductivity, np.ndarray) else float(conductivity)

    # Validate electric field shape
    if electric_field.shape[-1:] != (3,):
        raise ValueError(f"electric_field must have shape (..., 3), got {electric_field.shape}")

    if isinstance(sigma, np.ndarray):
        # Tensor conductivity
        if sigma.shape != (3, 3):
            raise ValueError(f"Conductivity tensor must be 3×3, got {sigma.shape}")

        # Check symmetry (for physical conductivity tensor)
        if not np.allclose(sigma, sigma.T, rtol=1e-10):
            raise ValueError("Conductivity tensor must be symmetric (Onsager reciprocity)")

        # Check positive definiteness
        eigenvalues = np.linalg.eigvalsh(sigma)
        if np.any(eigenvalues < -1e-10):
            raise ValueError(f"Conductivity tensor must be positive semi-definite, "
                           f"got eigenvalues {eigenvalues}")

        # J = sigma @ E (tensor contraction)
        if electric_field.shape == (3,):
            return sigma @ electric_field
        else:
            # Handle batched input
            return np.einsum('ij,...j->...i', sigma, electric_field)
    else:
        # Scalar conductivity (isotropic)
        if sigma < 0:
            raise ValueError(f"Conductivity must be non-negative, got {sigma}")
        return sigma * electric_field


@maxwell_cite(
    287,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Calculate electric field from current density (inverse Ohm's law)"
)
def electric_field_from_current_density(
    current_density: np.ndarray,
    conductivity: float | np.ndarray,
) -> np.ndarray:
    """
    Calculate electric field from current density (inverse of Ohm's law).

    Art. 287: Given the current density J and conductivity sigma, the
    electric field is:

        E = rho * J = J / sigma

    where rho = 1/sigma is the resistivity.

    For anisotropic materials with tensor conductivity, this becomes:

        E = rho @ J

    where rho = sigma^(-1) is the resistivity tensor.

    Args:
        current_density: Current density vector J (abamperes/cm²).
        conductivity: Conductivity (scalar or 3×3 tensor).

    Returns:
        Electric field vector E (abvolts/cm).

    References:
        Part II, Art. 287: Inverse Ohm's law.

    Example:
        >>> # Given J = (1, 0, 0) abA/cm² and sigma = 0.5 S/cm
        >>> E = electric_field_from_current_density(np.array([1.0, 0.0, 0.0]), 0.5)
        >>> print(f"E = {E} abV/cm")  # E = [2. 0. 0.] abV/cm
    """
    current_density = np.asarray(current_density, dtype=np.float64)

    if isinstance(conductivity, np.ndarray):
        # Tensor conductivity: E = sigma^(-1) @ J
        if conductivity.shape != (3, 3):
            raise ValueError(f"Conductivity tensor must be 3×3, got {conductivity.shape}")

        try:
            resistivity = np.linalg.inv(conductivity)
        except np.linalg.LinAlgError:
            raise ValueError("Conductivity tensor is singular, cannot invert")

        return resistivity @ current_density
    else:
        # Scalar conductivity
        if conductivity <= 0:
            raise ValueError(f"Conductivity must be positive, got {conductivity}")

        return current_density / conductivity


# =============================================================================
# ANISOTROPIC CONDUCTIVITY (Arts. 288-290)
# =============================================================================

@maxwell_cite(
    288, 289, 290,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Create anisotropic conductivity tensor from principal axes"
)
def anisotropic_conductivity(
    principal_conductivities: np.ndarray,
    rotation_matrix: np.ndarray = None,
) -> np.ndarray:
    """
    Construct the conductivity tensor for an anisotropic material.

    Arts. 288-290: Maxwell showed that in crystalline or structured materials,
    conductivity depends on direction. The conductivity is described by a
    symmetric second-rank tensor that can be diagonalized in a principal
    axis system:

        sigma_principal = diag(sigma_1, sigma_2, sigma_3)

    In an arbitrary coordinate system related by rotation R:

        sigma = R @ sigma_principal @ R^T

    Maxwell's analysis: The principal conductivities correspond to the
    crystal axes, and current does not necessarily flow parallel to the
    applied electric field except along principal directions.

    Args:
        principal_conductivities: Array [sigma_1, sigma_2, sigma_3] of
                                 conductivities along principal axes (siemens/cm).
        rotation_matrix: Optional 3×3 rotation matrix from principal axes
                        to laboratory frame. If None, returns diagonal tensor.

    Returns:
        3×3 conductivity tensor in laboratory frame.

    Raises:
        ValueError: If conductivities are negative or rotation matrix invalid.

    References:
        Part II, Art. 288: Anisotropic conduction theory.
        Part II, Art. 289: Principal axes of conduction.
        Part II, Art. 290: Transformation of conductivity tensor.

    Example:
        >>> # Uniaxial crystal (sigma_parallel != sigma_perpendicular)
        >>> sigma_principal = np.array([1.0, 0.5, 0.5])
        >>> sigma = anisotropic_conductivity(sigma_principal)
        >>> print(f"sigma = \n{sigma}")  # Diagonal tensor

        >>> # Rotate by 45° around z-axis
        >>> import numpy as np
        >>> theta = np.pi / 4
        >>> R = np.array([[np.cos(theta), -np.sin(theta), 0],
        ...               [np.sin(theta), np.cos(theta), 0],
        ...               [0, 0, 1]])
        >>> sigma_rotated = anisotropic_conductivity(sigma_principal, R)
    """
    principal_conductivities = np.asarray(principal_conductivities, dtype=np.float64)

    if principal_conductivities.shape != (3,):
        raise ValueError(f"principal_conductivities must have shape (3,), "
                        f"got {principal_conductivities.shape}")

    if np.any(principal_conductivities < 0):
        raise ValueError("Principal conductivities must be non-negative")

    # Diagonal tensor in principal axes
    sigma_principal = np.diag(principal_conductivities)

    if rotation_matrix is None:
        return sigma_principal

    # Validate rotation matrix
    rotation_matrix = np.asarray(rotation_matrix, dtype=np.float64)
    if rotation_matrix.shape != (3, 3):
        raise ValueError(f"rotation_matrix must be 3×3, got {rotation_matrix.shape}")

    # Check orthogonality: R @ R.T = I
    identity_check = rotation_matrix @ rotation_matrix.T
    if not np.allclose(identity_check, np.eye(3), rtol=1e-10, atol=1e-10):
        raise ValueError("rotation_matrix must be orthogonal (R @ R.T = I)")

    # Check determinant = +1 (proper rotation, not reflection)
    det = np.linalg.det(rotation_matrix)
    if not np.isclose(abs(det), 1.0, rtol=1e-10):
        raise ValueError(f"rotation_matrix must have |det| = 1, got {det}")

    # Transform to laboratory frame: sigma = R @ sigma_p @ R^T
    return rotation_matrix @ sigma_principal @ rotation_matrix.T


@maxwell_cite(
    288, 289,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Find principal conduction axes from conductivity tensor"
)
def principal_conduction_axes(
    conductivity_tensor: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Find the principal axes and principal conductivities of an anisotropic material.

    Arts. 288-289: Given a conductivity tensor sigma, Maxwell showed that
    there exist three orthogonal principal directions in which current flows
    parallel to the applied field. These are the eigenvectors of sigma, and
    the corresponding principal conductivities are the eigenvalues.

    The principal axes are found by diagonalizing the symmetric tensor:

        sigma @ v_i = lambda_i * v_i

    where:
        - lambda_i = principal conductivity along axis i
        - v_i = unit vector along principal axis i

    Args:
        conductivity_tensor: 3×3 symmetric conductivity tensor.

    Returns:
        Dictionary with:
        - principal_conductivities: Array [sigma_1, sigma_2, sigma_3] (eigenvalues)
        - principal_axes: 3×3 matrix whose columns are the principal direction vectors
        - anisotropy_ratio: sigma_max / sigma_min (measure of anisotropy)
        - is_isotropic: True if all principal conductivities are equal
        - isotropy_tolerance: Threshold used for isotropy check

    Raises:
        ValueError: If tensor is not symmetric or not positive semi-definite.

    References:
        Part II, Art. 288: Principal axes theory.
        Part II, Art. 289: Eigenvalue problem for conductivity.

    Example:
        >>> # Anisotropic tensor
        >>> sigma = np.array([[2, 0.5, 0], [0.5, 1, 0], [0, 0, 0.5]])
        >>> result = principal_conduction_axes(sigma)
        >>> print(f"Principal conductivities: {result['principal_conductivities']}")
        >>> print(f"Principal axes:\n{result['principal_axes']}")
    """
    conductivity_tensor = np.asarray(conductivity_tensor, dtype=np.float64)

    if conductivity_tensor.shape != (3, 3):
        raise ValueError(f"conductivity_tensor must be 3×3, got {conductivity_tensor.shape}")

    # Check symmetry
    if not np.allclose(conductivity_tensor, conductivity_tensor.T, rtol=1e-10):
        raise ValueError("Conductivity tensor must be symmetric")

    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(conductivity_tensor)

    # Sort by eigenvalue (descending)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Check positive semi-definiteness
    if np.any(eigenvalues < -1e-10):
        raise ValueError(f"Tensor must be positive semi-definite, "
                        f"got eigenvalues {eigenvalues}")

    # Anisotropy ratio
    sigma_max = np.max(eigenvalues)
    sigma_min = np.min(eigenvalues)
    anisotropy_ratio = sigma_max / sigma_min if sigma_min > 1e-15 else float('inf')

    # Isotropy check
    isotropy_tolerance = 1e-6 * sigma_max
    is_isotropic = np.all(np.abs(eigenvalues - eigenvalues[0]) < isotropy_tolerance)

    return {
        "principal_conductivities": eigenvalues,
        "principal_axes": eigenvectors,  # Columns are eigenvectors
        "anisotropy_ratio": anisotropy_ratio,
        "is_isotropic": is_isotropic,
        "isotropy_tolerance": isotropy_tolerance,
    }


# =============================================================================
# CONTINUITY EQUATION (Arts. 291-292)
# =============================================================================

@maxwell_cite(
    291, 292,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Continuity equation for charge conservation"
)
def continuity_equation(
    current_density_func: Callable[[np.ndarray], np.ndarray],
    charge_density_func: Callable[[np.ndarray, float], float] = None,
    position: np.ndarray = None,
    time: float = None,
) -> dict[str, float]:
    """
    Verify the continuity equation for charge conservation.

    Arts. 291-292: Maxwell's continuity equation expresses conservation of
    electric charge:

        div(J) + d(rho)/dt = 0

    where:
        - J = current density (abamperes/cm²)
        - rho = charge density (abcoulombs/cm³)
        - div(J) = divergence of current density

    For steady currents (DC), d(rho)/dt = 0, so:

        div(J) = 0

    This means that in steady state, current flows in closed loops with no
    sources or sinks of charge.

    Maxwell states: "The total current flowing out of any closed surface
    equals the rate of decrease of charge within that surface."

    The function computes:
        residual = div(J) + d(rho)/dt

    which should be zero for a physically valid solution.

    Args:
        current_density_func: Function J(r) returning current density at position.
        charge_density_func: Optional function rho(r, t) for time-varying charge.
                            If None, assumes steady state (d(rho)/dt = 0).
        position: Position r = (x, y, z) at which to evaluate.
        time: Time t for time-varying problems.

    Returns:
        Dictionary with:
        - divergence_J: div(J) at the given position
        - d_rho_dt: d(rho)/dt (0 if steady state)
        - continuity_residual: div(J) + d(rho)/dt (should be ~0)
        - is_satisfied: True if continuity equation holds

    Raises:
        ValueError: If position not provided or functions are invalid.

    References:
        Part II, Art. 291: Continuity equation for steady currents.
        Part II, Art. 292: Time-varying charge and current.

    Example:
        >>> # Steady current: J = (x, y, z) has div(J) = 3
        >>> J_func = lambda r: r  # Radial current
        >>> result = continuity_equation(J_func, position=np.array([1, 1, 1]))
        >>> print(f"div(J) = {result['divergence_J']}")  # Should be 3
        >>> # Not satisfied for steady state!
        >>> print(f"Satisfied: {result['is_satisfied']}")  # False
    """
    if position is None:
        raise ValueError("position must be provided")

    position = np.asarray(position, dtype=np.float64)
    if position.shape != (3,):
        raise ValueError(f"position must have shape (3,), got {position.shape}")

    # Compute divergence of J using finite differences
    eps = 1e-6  # Small displacement for numerical differentiation
    J_at_pos = current_density_func(position)

    # div(J) = dJx/dx + dJy/dy + dJz/dz
    div_J = 0.0
    for i in range(3):
        pos_plus = position.copy()
        pos_minus = position.copy()
        pos_plus[i] += eps
        pos_minus[i] -= eps

        J_plus = current_density_func(pos_plus)
        J_minus = current_density_func(pos_minus)

        div_J += (J_plus[i] - J_minus[i]) / (2 * eps)

    # Time derivative of charge density
    if charge_density_func is not None and time is not None:
        dt = 1e-6
        rho_plus = charge_density_func(position, time + dt)
        rho_minus = charge_density_func(position, time - dt)
        d_rho_dt = (rho_plus - rho_minus) / (2 * dt)
    else:
        d_rho_dt = 0.0  # Steady state

    # Continuity residual
    residual = div_J + d_rho_dt
    is_satisfied = abs(residual) < 1e-6 * max(1.0, abs(div_J), abs(d_rho_dt))

    return {
        "divergence_J": div_J,
        "d_rho_dt": d_rho_dt,
        "continuity_residual": residual,
        "is_satisfied": is_satisfied,
        "position": position,
        "time": time,
    }


@maxwell_cite(
    291,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Verify steady-state continuity (div(J) = 0)"
)
def verify_steady_state_continuity(
    current_density_func: Callable[[np.ndarray], np.ndarray],
    test_points: list[np.ndarray],
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify that a current distribution satisfies steady-state continuity.

    Art. 291: For steady (DC) currents, the continuity equation reduces to:

        div(J) = 0

    This function tests whether a given current density field satisfies
    this condition at multiple test points.

    Args:
        current_density_func: Function J(r) returning current density.
        test_points: List of positions to test.
        tolerance: Numerical tolerance for divergence check.

    Returns:
        Dictionary with:
        - n_points_tested: Number of test points
        - max_divergence: Maximum |div(J)| found
        - mean_divergence: Mean |div(J)| over test points
        - all_satisfied: True if div(J) ≈ 0 at all points
        - failed_points: List of positions where |div(J)| > tolerance
        - divergences: List of div(J) values at each point

    References:
        Part II, Art. 291: Steady-state continuity.

    Example:
        >>> # Solenoidal field: J = (0, x, 0) has div(J) = 0
        >>> J_func = lambda r: np.array([0, r[0], 0])
        >>> points = [np.array([x, y, z]) for x in [0, 1] for y in [0, 1] for z in [0, 1]]
        >>> result = verify_steady_state_continuity(J_func, points)
        >>> assert result["all_satisfied"]
    """
    divergences = []
    failed_points = []

    for point in test_points:
        result = continuity_equation(current_density_func, position=point)
        div_J = result["divergence_J"]
        divergences.append(div_J)

        if abs(div_J) > tolerance:
            failed_points.append(point)

    divergences = np.array(divergences)

    return {
        "n_points_tested": len(test_points),
        "max_divergence": float(np.max(np.abs(divergences))),
        "mean_divergence": float(np.mean(np.abs(divergences))),
        "all_satisfied": len(failed_points) == 0,
        "failed_points": failed_points,
        "divergences": divergences.tolist(),
    }


# =============================================================================
# INTERFACE BOUNDARY CONDITIONS (Art. 296)
# =============================================================================

@maxwell_cite(
    296,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Boundary conditions at interface between conductors"
)
def interface_boundary_conditions(
    J1: np.ndarray,
    sigma1: float | np.ndarray,
    J2: np.ndarray,
    sigma2: float | np.ndarray,
    interface_normal: np.ndarray,
) -> dict[str, float | bool]:
    """
    Verify boundary conditions at the interface between two conductors.

    Art. 296: Maxwell derived the boundary conditions for current flow
    across an interface between two materials with different conductivities.

    At the interface, the following must be continuous:

    1. Normal component of current density (no charge accumulation):
        J1_n = J2_n
        n · J1 = n · J2

    2. Tangential component of electric field (no surface curl):
        E1_t = E2_t
        n × E1 = n × E2

    From Ohm's law J = sigma * E, these imply:
        - Normal: sigma1 * E1_n = sigma2 * E2_n (E normal is discontinuous)
        - Tangential: J1_t / sigma1 = J2_t / sigma2 (J tangential is discontinuous)

    The current "refracts" at the interface according to:

        tan(theta1) / tan(theta2) = sigma1 / sigma2

    where theta is the angle from the normal.

    Args:
        J1: Current density in material 1 (abamperes/cm²).
        sigma1: Conductivity of material 1 (scalar or tensor).
        J2: Current density in material 2 (abamperes/cm²).
        sigma2: Conductivity of material 2.
        interface_normal: Unit normal vector pointing from 1 to 2.

    Returns:
        Dictionary with:
        - J1_normal: Normal component of J1
        - J2_normal: Normal component of J2
        - normal_continuity_error: |J1_n - J2_n|
        - E1_tangential: Tangential component of E1
        - E2_tangential: Tangential component of E2
        - tangential_continuity_error: |E1_t - E2_t|
        - normal_bc_satisfied: True if J1_n = J2_n
        - tangential_bc_satisfied: True if E1_t = E2_t
        - refraction_angle1: Angle of J1 from normal (degrees)
        - refraction_angle2: Angle of J2 from normal (degrees)

    Raises:
        ValueError: If interface_normal is not a unit vector.

    References:
        Part II, Art. 296: Interface boundary conditions.

    Example:
        >>> # Current crossing from sigma=1 to sigma=2
        >>> J1 = np.array([1, 0, 1])  # At 45° to normal
        >>> J2 = np.array([1, 0, 2])  # Refracted
        >>> n = np.array([0, 0, 1])
        >>> result = interface_boundary_conditions(J1, 1.0, J2, 2.0, n)
        >>> print(f"Normal continuity error: {result['normal_continuity_error']}")
    """
    # Validate inputs
    J1 = np.asarray(J1, dtype=np.float64)
    J2 = np.asarray(J2, dtype=np.float64)
    interface_normal = np.asarray(interface_normal, dtype=np.float64)

    if J1.shape != (3,) or J2.shape != (3,) or interface_normal.shape != (3,):
        raise ValueError("J1, J2, and interface_normal must have shape (3,)")

    normal_mag = np.linalg.norm(interface_normal)
    if not np.isclose(normal_mag, 1.0, rtol=1e-10):
        raise ValueError(f"interface_normal must be a unit vector, got |n| = {normal_mag}")

    # Normal components: J_n = n · J
    J1_normal = np.dot(interface_normal, J1)
    J2_normal = np.dot(interface_normal, J2)
    normal_error = abs(J1_normal - J2_normal)

    # Electric fields from Ohm's law
    if isinstance(sigma1, np.ndarray):
        E1 = electric_field_from_current_density(J1, sigma1)
    else:
        E1 = J1 / sigma1 if sigma1 > 0 else np.zeros(3)

    if isinstance(sigma2, np.ndarray):
        E2 = electric_field_from_current_density(J2, sigma2)
    else:
        E2 = J2 / sigma2 if sigma2 > 0 else np.zeros(3)

    # Tangential components: E_t = E - n*(n·E)
    E1_normal_comp = np.dot(interface_normal, E1) * interface_normal
    E2_normal_comp = np.dot(interface_normal, E2) * interface_normal

    E1_tangential = E1 - E1_normal_comp
    E2_tangential = E2 - E2_normal_comp

    tangential_error = np.linalg.norm(E1_tangential - E2_tangential)

    # Refraction angles
    J1_mag = np.linalg.norm(J1)
    J2_mag = np.linalg.norm(J2)

    cos_theta1 = J1_normal / J1_mag if J1_mag > 0 else 1.0
    cos_theta2 = J2_normal / J2_mag if J2_mag > 0 else 1.0

    theta1 = np.degrees(np.arccos(np.clip(cos_theta1, -1, 1)))
    theta2 = np.degrees(np.arccos(np.clip(cos_theta2, -1, 1)))

    # Verification
    normal_satisfied = normal_error < 1e-6 * max(1.0, abs(J1_normal), abs(J2_normal))
    tangential_satisfied = tangential_error < 1e-6 * max(1.0, np.linalg.norm(E1_tangential), np.linalg.norm(E2_tangential))

    return {
        "J1_normal": J1_normal,
        "J2_normal": J2_normal,
        "normal_continuity_error": normal_error,
        "E1_tangential": E1_tangential,
        "E2_tangential": E2_tangential,
        "tangential_continuity_error": tangential_error,
        "normal_bc_satisfied": normal_satisfied,
        "tangential_bc_satisfied": tangential_satisfied,
        "refraction_angle1": theta1,
        "refraction_angle2": theta2,
        "E1_normal_component": E1_normal_comp,
        "E2_normal_component": E2_normal_comp,
    }


# =============================================================================
# POINT SOURCE SOLUTIONS (Arts. 293-295)
# =============================================================================

@maxwell_cite(
    293, 294,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Potential from point current source in infinite medium"
)
def point_source_potential(
    source_position: np.ndarray,
    current: float,
    conductivity: float,
    observation_point: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate potential and field from a point current source in infinite medium.

    Arts. 293-294: Maxwell solved for the potential due to a point source
    of current in an infinite homogeneous conducting medium.

    For a source injecting current I at position r_0 in a medium with
    conductivity sigma, the potential at position r is:

        V(r) = I / (4 * pi * sigma * |r - r_0|)

    The current density is radial:

        J(r) = I / (4 * pi * r^2) * r_hat

    and the electric field is:

        E(r) = J(r) / sigma = I / (4 * pi * sigma * r^2) * r_hat

    This is analogous to the electrostatic potential of a point charge,
    with I/sigma replacing q/epsilon.

    Args:
        source_position: Position r_0 of the point source (cm).
        current: Current I injected (abamperes). Positive = source, negative = sink.
        conductivity: Conductivity sigma of the medium (siemens/cm).
        observation_point: Position r where potential is evaluated.
                          If None, returns the potential function.

    Returns:
        If observation_point provided:
        Dictionary with:
        - potential: V at observation point (abvolts)
        - electric_field: E vector at observation point (abvolts/cm)
        - current_density: J vector at observation point (abamperes/cm²)
        - distance: |r - r_0| (cm)
        Otherwise:
        Dictionary with callable functions for V, E, J.

    Raises:
        ValueError: If conductivity is not positive or observation at source.

    References:
        Part II, Art. 293: Point source potential.
        Part II, Art. 294: Current distribution from point source.

    Example:
        >>> # Point source at origin, I = 1 abA, sigma = 1 S/cm
        >>> result = point_source_potential(
        ...     source_position=np.array([0, 0, 0]),
        ...     current=1.0,
        ...     conductivity=1.0,
        ...     observation_point=np.array([1, 0, 0])
        ... )
        >>> print(f"V = {result['potential']:.6f} abV")
        >>> print(f"|E| = {np.linalg.norm(result['electric_field']):.6f} abV/cm")
    """
    source_position = np.asarray(source_position, dtype=np.float64)
    if source_position.shape != (3,):
        raise ValueError(f"source_position must have shape (3,), got {source_position.shape}")

    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")

    if observation_point is None:
        # Return potential field functions
        def potential_func(r):
            r = np.asarray(r, dtype=np.float64)
            dist = np.linalg.norm(r - source_position)
            if dist < 1e-15:
                raise ValueError("Cannot evaluate potential at source position")
            return current / (4 * np.pi * conductivity * dist)

        def field_func(r):
            r = np.asarray(r, dtype=np.float64)
            r_vec = r - source_position
            dist = np.linalg.norm(r_vec)
            if dist < 1e-15:
                raise ValueError("Cannot evaluate field at source position")
            r_hat = r_vec / dist
            E_mag = current / (4 * np.pi * conductivity * dist ** 2)
            return E_mag * r_hat

        def current_density_func(r):
            r = np.asarray(r, dtype=np.float64)
            return conductivity * field_func(r)

        return {
            "potential_func": potential_func,
            "electric_field_func": field_func,
            "current_density_func": current_density_func,
            "source_position": source_position,
            "current": current,
            "conductivity": conductivity,
        }

    # Evaluate at observation point
    observation_point = np.asarray(observation_point, dtype=np.float64)
    if observation_point.shape != (3,):
        raise ValueError(f"observation_point must have shape (3,), got {observation_point.shape}")

    r_vec = observation_point - source_position
    dist = np.linalg.norm(r_vec)

    if dist < 1e-15:
        raise ValueError("Cannot evaluate at source position (singularity)")

    r_hat = r_vec / dist

    # Potential: V = I / (4*pi*sigma*r)
    potential = current / (4 * np.pi * conductivity * dist)

    # Electric field: E = I / (4*pi*sigma*r^2) * r_hat
    E_mag = current / (4 * np.pi * conductivity * dist ** 2)
    electric_field = E_mag * r_hat

    # Current density: J = sigma * E = I / (4*pi*r^2) * r_hat
    J_mag = current / (4 * np.pi * dist ** 2)
    current_density = J_mag * r_hat

    return {
        "potential": potential,
        "electric_field": electric_field,
        "current_density": current_density,
        "distance": dist,
        "direction": r_hat,
        "source_position": source_position,
        "observation_point": observation_point,
        "current": current,
        "conductivity": conductivity,
    }


@maxwell_cite(
    294,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Potential from source-sink pair (dipole)"
)
def dipole_potential(
    source_position: np.ndarray,
    sink_position: np.ndarray,
    current: float,
    conductivity: float,
    observation_point: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate potential from a source-sink pair (current dipole).

    Art. 294: A source and sink of equal and opposite current form a
    dipole. By superposition:

        V(r) = I / (4*pi*sigma) * (1/|r - r_source| - 1/|r - r_sink|)

    In the far-field limit (|r| >> |r_source - r_sink|), this becomes:

        V(r) ≈ (p · r_hat) / (4*pi*sigma*r^2)

    where p = I * d is the dipole moment (d = r_sink - r_source).

    This is the current-flow analogue of an electric dipole.

    Args:
        source_position: Position of current source (+I).
        sink_position: Position of current sink (-I).
        current: Current magnitude I (abamperes).
        conductivity: Conductivity of medium (siemens/cm).
        observation_point: Position to evaluate (or None for functions).

    Returns:
        If observation_point provided:
        Dictionary with potential, field, current density at that point.
        Otherwise: Dictionary with callable functions.

    References:
        Part II, Art. 294: Source-sink superposition and dipole limit.

    Example:
        >>> # Dipole along z-axis
        >>> result = dipole_potential(
        ...     source_position=np.array([0, 0, -0.5]),
        ...     sink_position=np.array([0, 0, 0.5]),
        ...     current=1.0,
        ...     conductivity=1.0,
        ...     observation_point=np.array([1, 0, 0])
        ... )
        >>> print(f"V = {result['potential']:.6f} abV")
    """
    if observation_point is None:
        # Return functions
        def potential_func(r):
            r = np.asarray(r, dtype=np.float64)
            r_source = np.linalg.norm(r - source_position)
            r_sink = np.linalg.norm(r - sink_position)
            if r_source < 1e-15 or r_sink < 1e-15:
                raise ValueError("Cannot evaluate at source or sink position")
            return current / (4 * np.pi * conductivity) * (1/r_source - 1/r_sink)

        def field_func(r):
            r = np.asarray(r, dtype=np.float64)
            r_s_vec = r - source_position
            r_k_vec = r - sink_position
            r_s = np.linalg.norm(r_s_vec)
            r_k = np.linalg.norm(r_k_vec)
            if r_s < 1e-15 or r_k < 1e-15:
                raise ValueError("Cannot evaluate at source or sink position")

            # E = I/(4*pi*sigma) * (r_s/r_s^3 - r_k/r_k^3)
            factor = current / (4 * np.pi * conductivity)
            E = factor * (r_s_vec / r_s ** 3 - r_k_vec / r_k ** 3)
            return E

        def current_density_func(r):
            return conductivity * field_func(r)

        # Dipole moment
        d_vec = sink_position - source_position
        dipole_moment = current * d_vec

        return {
            "potential_func": potential_func,
            "electric_field_func": field_func,
            "current_density_func": current_density_func,
            "dipole_moment": dipole_moment,
            "source_position": source_position,
            "sink_position": sink_position,
            "current": current,
            "conductivity": conductivity,
        }

    observation_point = np.asarray(observation_point, dtype=np.float64)

    r_s_vec = observation_point - source_position
    r_k_vec = observation_point - sink_position
    r_s = np.linalg.norm(r_s_vec)
    r_k = np.linalg.norm(r_k_vec)

    if r_s < 1e-15 or r_k < 1e-15:
        raise ValueError("Cannot evaluate at source or sink position")

    # Potential by superposition
    potential = current / (4 * np.pi * conductivity) * (1/r_s - 1/r_k)

    # Electric field
    factor = current / (4 * np.pi * conductivity)
    electric_field = factor * (r_s_vec / r_s ** 3 - r_k_vec / r_k ** 3)

    # Current density
    current_density = conductivity * electric_field

    # Dipole moment
    d_vec = sink_position - source_position
    dipole_moment = current * d_vec

    return {
        "potential": potential,
        "electric_field": electric_field,
        "current_density": current_density,
        "dipole_moment": dipole_moment,
        "source_position": source_position,
        "sink_position": sink_position,
        "observation_point": observation_point,
        "distance_to_source": r_s,
        "distance_to_sink": r_k,
    }


@maxwell_cite(
    295,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Calculate spreading resistance of point contact"
)
def spreading_resistance(
    contact_radius: float,
    conductivity: float,
    geometry: str = "hemisphere",
) -> float:
    """
    Calculate the spreading resistance of a point contact.

    Art. 295: When current enters a conductor through a small contact,
    the resistance is dominated by the "spreading" of current from the
    contact into the bulk. Maxwell calculated this spreading resistance.

    For a circular contact of radius a on a semi-infinite conductor:

        R_spread = 1 / (4 * sigma * a)

    For a spherical electrode of radius a in an infinite medium:

        R_spread = 1 / (4 * pi * sigma * a)

    This resistance is independent of the bulk dimensions (as long as
    they are much larger than the contact).

    Args:
        contact_radius: Radius a of the contact (cm).
        conductivity: Conductivity sigma of the medium (siemens/cm).
        geometry: Contact geometry. Options:
                 - "hemisphere": Semi-infinite medium, contact on surface
                 - "sphere": Infinite medium, spherical electrode
                 - "disk": Circular disk contact on surface

    Returns:
        Spreading resistance R_spread (abohms).

    Raises:
        ValueError: If contact_radius or conductivity not positive.

    References:
        Part II, Art. 295: Spreading resistance calculation.

    Example:
        >>> # Circular contact, radius 0.1 cm, sigma = 1 S/cm
        >>> R = spreading_resistance(0.1, 1.0, geometry="hemisphere")
        >>> print(f"R_spread = {R:.6f} abohm")

        >>> # Spherical electrode
        >>> R = spreading_resistance(0.1, 1.0, geometry="sphere")
        >>> print(f"R_spread = {R:.6f} abohm")
    """
    if contact_radius <= 0:
        raise ValueError(f"contact_radius must be positive, got {contact_radius}")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")

    if geometry == "hemisphere":
        # Current spreads into hemisphere: R = 1/(4*sigma*a)
        return 1.0 / (4.0 * conductivity * contact_radius)

    elif geometry == "sphere":
        # Current spreads spherically: R = 1/(4*pi*sigma*a)
        return 1.0 / (4.0 * np.pi * conductivity * contact_radius)

    elif geometry == "disk":
        # Circular disk on surface: R = 1/(4*sigma*a) (same as hemisphere)
        return 1.0 / (4.0 * conductivity * contact_radius)

    else:
        raise ValueError(f"Unknown geometry: {geometry}. Options: hemisphere, sphere, disk")


# =============================================================================
# METHOD OF IMAGES FOR CONDUCTORS
# =============================================================================

@maxwell_cite(
    293, 294, 296,
    part=2, chapter="Conduction in Three Dimensions",
    theory_class="maxwell_original",
    description="Method of images for point source near conducting boundary"
)
def method_of_images_conductor(
    source_position: np.ndarray,
    current: float,
    conductivity: float,
    boundary_position: float,
    boundary_type: str = "insulating",
    observation_point: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Solve for point source near a planar boundary using method of images.

    Arts. 293-294, 296: Maxwell extended the method of images to conduction
    problems. For a point source near a planar boundary:

    1. Insulating boundary (J_n = 0):
       Place an image source of SAME strength at the mirror position.
       The normal currents cancel at the boundary.

    2. Conducting boundary (V = 0, perfect conductor):
       Place an image sink of OPPOSITE strength at the mirror position.
       The potential is zero at the boundary.

    The total potential is the superposition of the real source and image.

    Args:
        source_position: Position of the real source (cm).
        current: Current of the source (abamperes).
        conductivity: Conductivity of the medium (siemens/cm).
        boundary_position: z-coordinate of the planar boundary (assumed z = const).
        boundary_type: "insulating" (J_n = 0) or "conducting" (V = 0).
        observation_point: Position to evaluate potential.

    Returns:
        Dictionary with potential, field, and image source parameters.

    Raises:
        ValueError: If boundary_type is invalid.

    References:
        Part II, Arts. 293-294: Method of images.
        Part II, Art. 296: Boundary conditions.

    Example:
        >>> # Source above insulating boundary
        >>> result = method_of_images_conductor(
        ...     source_position=np.array([0, 0, 1]),
        ...     current=1.0,
        ...     conductivity=1.0,
        ...     boundary_position=0.0,
        ...     boundary_type="insulating",
        ...     observation_point=np.array([1, 0, 0.5])
        ... )
        >>> print(f"V = {result['potential']:.6f} abV")
    """
    source_position = np.asarray(source_position, dtype=np.float64)

    # Image position: mirror across boundary plane z = boundary_position
    image_position = source_position.copy()
    image_position[2] = 2 * boundary_position - source_position[2]

    # Image current strength
    if boundary_type == "insulating":
        image_current = current  # Same sign
    elif boundary_type == "conducting":
        image_current = -current  # Opposite sign
    else:
        raise ValueError(f"boundary_type must be 'insulating' or 'conducting', got {boundary_type}")

    if observation_point is None:
        # Return functions
        def potential_func(r):
            r = np.asarray(r, dtype=np.float64)
            r_real = np.linalg.norm(r - source_position)
            r_image = np.linalg.norm(r - image_position)
            if r_real < 1e-15 or r_image < 1e-15:
                raise ValueError("Cannot evaluate at source or image position")
            return current / (4 * np.pi * conductivity * r_real) + \
                   image_current / (4 * np.pi * conductivity * r_image)

        def field_func(r):
            r = np.asarray(r, dtype=np.float64)
            r_r_vec = r - source_position
            r_i_vec = r - image_position
            r_r = np.linalg.norm(r_r_vec)
            r_i = np.linalg.norm(r_i_vec)

            factor = 1 / (4 * np.pi * conductivity)
            E = factor * (current * r_r_vec / r_r ** 3 + image_current * r_i_vec / r_i ** 3)
            return E

        return {
            "potential_func": potential_func,
            "electric_field_func": field_func,
            "source_position": source_position,
            "image_position": image_position,
            "image_current": image_current,
            "boundary_type": boundary_type,
            "boundary_position": boundary_position,
            "conductivity": conductivity,
        }

    # Evaluate at observation point
    observation_point = np.asarray(observation_point, dtype=np.float64)

    r_r_vec = observation_point - source_position
    r_i_vec = observation_point - image_position
    r_r = np.linalg.norm(r_r_vec)
    r_i = np.linalg.norm(r_i_vec)

    if r_r < 1e-15 or r_i < 1e-15:
        raise ValueError("Cannot evaluate at source or image position")

    # Superposition
    potential = current / (4 * np.pi * conductivity * r_r) + \
                image_current / (4 * np.pi * conductivity * r_i)

    factor = 1 / (4 * np.pi * conductivity)
    electric_field = factor * (current * r_r_vec / r_r ** 3 + image_current * r_i_vec / r_i ** 3)

    current_density = conductivity * electric_field

    return {
        "potential": potential,
        "electric_field": electric_field,
        "current_density": current_density,
        "source_position": source_position,
        "image_position": image_position,
        "image_current": image_current,
        "boundary_type": boundary_type,
        "boundary_position": boundary_position,
        "observation_point": observation_point,
    }


# =============================================================================
# 3D CONDUCTION ANALYZER CLASS
# =============================================================================

@dataclass
class Conduction3DAnalyzer:
    """
    Comprehensive analyzer for 3D conduction problems.

    This class provides methods for analyzing:
    - Current flow in anisotropic media
    - Boundary value problems
    - Point source configurations
    - Continuity verification

    Attributes:
        conductivity: Conductivity (scalar or 3×3 tensor).
        domain_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
    """

    conductivity: float | np.ndarray
    domain_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = None

    @maxwell_cite(
        285, 286, 287,
        part=2, chapter="Conduction in Three Dimensions",
        theory_class="maxwell_original",
        description="Analyze current flow for given electric field"
    )
    def analyze_current_flow(
        self,
        electric_field: np.ndarray,
        position: np.ndarray = None,
    ) -> dict[str, float | np.ndarray]:
        """
        Analyze current flow for a given electric field.

        Args:
            electric_field: Electric field vector (abvolts/cm).
            position: Optional position for spatially varying conductivity.

        Returns:
            Dictionary with J, |J|, direction, and power density.
        """
        J = ohms_law_3d(electric_field, self.conductivity, position)
        J_mag = np.linalg.norm(J)

        # Power density: P = J · E = sigma * E^2
        power_density = np.dot(J, electric_field)

        return {
            "current_density": J,
            "current_magnitude": J_mag,
            "current_direction": J / J_mag if J_mag > 0 else np.zeros(3),
            "power_density": power_density,
            "electric_field": electric_field,
        }

    @maxwell_cite(
        288, 289,
        part=2, chapter="Conduction in Three Dimensions",
        theory_class="maxwell_original",
        description="Analyze anisotropy of conductivity tensor"
    )
    def analyze_anisotropy(self) -> dict[str, float | np.ndarray]:
        """
        Analyze the anisotropy of the conductivity tensor.

        Returns:
            Dictionary with principal conductivities, axes, and anisotropy measures.
        """
        if isinstance(self.conductivity, (int, float)):
            return {
                "is_isotropic": True,
                "conductivity": self.conductivity,
                "anisotropy_ratio": 1.0,
            }

        result = principal_conduction_axes(self.conductivity)
        return result

    @maxwell_cite(
        291, 292,
        part=2, chapter="Conduction in Three Dimensions",
        theory_class="maxwell_original",
        description="Verify continuity for given current distribution"
    )
    def verify_continuity(
        self,
        current_density_func: Callable[[np.ndarray], np.ndarray],
        test_points: list[np.ndarray],
    ) -> dict:
        """
        Verify continuity equation for a current distribution.

        Args:
            current_density_func: J(r) function.
            test_points: List of positions to test.

        Returns:
            Result from verify_steady_state_continuity().
        """
        return verify_steady_state_continuity(current_density_func, test_points)


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CONDUCTION IN THREE DIMENSIONS")
    print("Maxwell's Treatise, Part II, Chapter VII (Arts. 285-296)")
    print("=" * 70)

    # Test Ohm's law 3D
    print("\n--- Ohm's Law 3D (Arts. 285-287) ---")
    E = np.array([1.0, 0.0, 0.0])
    J = ohms_law_3d(E, conductivity=0.5)
    print(f"  E = {E} abV/cm, sigma = 0.5 S/cm")
    print(f"  J = {J} abA/cm²")

    # Test anisotropic conductivity
    print("\n--- Anisotropic Conductivity (Arts. 288-290) ---")
    sigma_principal = np.array([2.0, 1.0, 0.5])
    sigma = anisotropic_conductivity(sigma_principal)
    print(f"  Principal conductivities: {sigma_principal}")
    print(f"  Conductivity tensor:\n{sigma}")

    # Test principal axes
    result = principal_conduction_axes(sigma)
    print(f"  Recovered principal conductivities: {result['principal_conductivities']}")
    print(f"  Anisotropy ratio: {result['anisotropy_ratio']:.2f}")

    # Test continuity equation
    print("\n--- Continuity Equation (Arts. 291-292) ---")
    # Solenoidal field: div(J) = 0
    J_solenoidal = lambda r: np.array([0, r[0], 0])
    test_points = [np.array([x, y, z]) for x in [0, 1] for y in [0, 1] for z in [0, 1]]
    continuity = verify_steady_state_continuity(J_solenoidal, test_points)
    print(f"  Solenoidal field J = (0, x, 0):")
    print(f"    Max divergence: {continuity['max_divergence']:.2e}")
    print(f"    All satisfied: {continuity['all_satisfied']}")

    # Test point source
    print("\n--- Point Source Potential (Arts. 293-294) ---")
    ps = point_source_potential(
        source_position=np.array([0, 0, 0]),
        current=1.0,
        conductivity=1.0,
        observation_point=np.array([1, 0, 0])
    )
    print(f"  Point source at origin, I = 1 abA, sigma = 1 S/cm")
    print(f"  At r = (1, 0, 0):")
    print(f"    V = {ps['potential']:.6f} abV")
    print(f"    |E| = {np.linalg.norm(ps['electric_field']):.6f} abV/cm")

    # Test dipole
    print("\n--- Dipole Potential ---")
    dipole = dipole_potential(
        source_position=np.array([0, 0, -0.5]),
        sink_position=np.array([0, 0, 0.5]),
        current=1.0,
        conductivity=1.0,
        observation_point=np.array([1, 0, 0])
    )
    print(f"  Dipole along z-axis")
    print(f"  At r = (1, 0, 0): V = {dipole['potential']:.6f} abV")

    # Test spreading resistance
    print("\n--- Spreading Resistance (Art. 295) ---")
    R_hemi = spreading_resistance(0.1, 1.0, geometry="hemisphere")
    R_sphere = spreading_resistance(0.1, 1.0, geometry="sphere")
    print(f"  Contact radius = 0.1 cm, sigma = 1 S/cm")
    print(f"    Hemisphere: R = {R_hemi:.6f} abohm")
    print(f"    Sphere: R = {R_sphere:.6f} abohm")

    # Test boundary conditions
    print("\n--- Interface Boundary Conditions (Art. 296) ---")
    J1 = np.array([1, 0, 1])
    J2 = np.array([1, 0, 2])
    bc = interface_boundary_conditions(J1, 1.0, J2, 2.0, np.array([0, 0, 1]))
    print(f"  Current crossing interface (sigma1=1, sigma2=2):")
    print(f"    J1_normal = {bc['J1_normal']:.3f}, J2_normal = {bc['J2_normal']:.3f}")
    print(f"    Normal BC satisfied: {bc['normal_bc_satisfied']}")
    print(f"    Refraction angles: theta1 = {bc['refraction_angle1']:.1f} deg, theta2 = {bc['refraction_angle2']:.1f} deg")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)
