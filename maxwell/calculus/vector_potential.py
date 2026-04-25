"""
Magnetic vector potential — A field where B = ∇×A.

Implements the theory of vector potential from Part III of Maxwell's Treatise:
- Vector potential definition B = ∇×A (Arts. 405-406)
- Relation between scalar potential Ω and vector potential A
- Gauge freedom in vector potential

Maxwell introduces the vector potential A such that:
    B = ∇ × A

This automatically satisfies ∇·B = 0 since ∇·(∇×A) = 0.

In CGS, for a current distribution J:
    A(r) = (1/c) ∫ J(r') / |r - r'| dV'

Category: A (maxwell_original) — Maxwell's vector potential theory.

References:
    Part III, Arts. 405-406: Magnetic vector potential.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class VectorPotential:
    """
    Magnetic vector potential — A field at a point.

    Art. 405-406: The magnetic vector potential A is defined such that:

        B = ∇ × A

    This definition automatically ensures ∇·B = 0.

    The vector potential is not unique — adding ∇χ to A leaves B
    unchanged (gauge freedom). The Coulomb gauge ∇·A = 0 is commonly
    used in magnetostatics.

    Attributes:
        value: Vector potential A (gauss·cm).
        position: Position where A is evaluated (cm).
    """

    value: np.ndarray  # shape (3,), gauss·cm
    position: np.ndarray  # shape (3,), cm

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.value.shape != (3,):
            raise ValueError(f"A must be 3D")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D")

    @property
    def magnitude(self) -> float:
        """Magnitude of vector potential |A|."""
        return float(np.linalg.norm(self.value))

    @classmethod
    @maxwell_cite(
        405,
        part=3, chapter="Vector Potential",
        theory_class="maxwell_original",
        description="Create A from current distribution",
    )
    def from_current_distribution(
        cls,
        current_density_func: Callable[[np.ndarray], np.ndarray],
        position: np.ndarray,
        integration_volume: np.ndarray,
    ) -> VectorPotential:
        """
        Create vector potential from current distribution.

        Art. 405: For a steady current distribution J, the vector
        potential is:

            A(r) = (1/c) ∫ J(r') / |r - r'| dV'  (CGS)

        Args:
            current_density_func: Function returning J at a position.
            position: Position where A is calculated (cm).
            integration_volume: Array of sample points (N, 3).

        Returns:
            VectorPotential object.

        Reference:
            Part III, Art. 405: A from current distribution.
        """
        position = np.asarray(position, dtype=np.float64)
        integration_volume = np.asarray(integration_volume, dtype=np.float64)

        A = np.zeros(3)

        # Estimate volume element
        if len(integration_volume) > 1:
            bounds = np.max(integration_volume, axis=0) - np.min(integration_volume, axis=0)
            dV = np.prod(bounds) / len(integration_volume)
        else:
            dV = 1.0

        for r_prime in integration_volume:
            r_vec = position - r_prime
            r_mag = np.linalg.norm(r_vec)

            if r_mag < 1e-10:
                continue  # Skip singularity

            J = current_density_func(r_prime)
            A += (dV / CONST.C) * J / r_mag

        return cls(value=A, position=position)

    @classmethod
    @maxwell_cite(
        406,
        part=3, chapter="Vector Potential",
        theory_class="maxwell_original",
        description="Create A from magnetic dipole",
    )
    def from_dipole(
        cls,
        magnetic_moment: np.ndarray,
        dipole_position: np.ndarray,
        field_point: np.ndarray,
    ) -> VectorPotential:
        """
        Create vector potential from a magnetic dipole.

        Art. 406: For a magnetic dipole m at position r₀, the
        vector potential at r is:

            A(r) = (m × (r - r₀)) / |r - r₀|³

        Args:
            magnetic_moment: Dipole moment m (emu).
            dipole_position: Position of dipole (cm).
            field_point: Position where A is calculated (cm).

        Returns:
            VectorPotential object.

        Reference:
            Part III, Art. 406: A from dipole.
        """
        magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
        dipole_position = np.asarray(dipole_position, dtype=np.float64)
        field_point = np.asarray(field_point, dtype=np.float64)

        r_vec = field_point - dipole_position
        r_mag = np.linalg.norm(r_vec)

        if r_mag < 1e-10:
            return cls(value=np.zeros(3), position=field_point)

        # A = (m × r) / r³
        A = np.cross(magnetic_moment, r_vec) / (r_mag ** 3)

        return cls(value=A, position=field_point)


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Calculate B from A via curl",
)
def calc_B_from_vector_potential(
    A_field_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate magnetic induction B from vector potential A.

    Art. 405: The magnetic field is the curl of the vector potential:

        B = ∇ × A

    In components:
        B_x = ∂A_z/∂y - ∂A_y/∂z
        B_y = ∂A_x/∂z - ∂A_z/∂x
        B_z = ∂A_y/∂x - ∂A_x/∂y

    Args:
        A_field_func: Function returning A at a position.
        position: Position where B is calculated (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part III, Art. 405: B = ∇×A.
    """
    position = np.asarray(position, dtype=np.float64)

    # Compute curl numerically
    B = np.zeros(3)

    # B_x = ∂A_z/∂y - ∂A_y/∂z
    # B_y = ∂A_x/∂z - ∂A_z/∂x
    # B_z = ∂A_y/∂x - ∂A_x/∂y

    A_center = A_field_func(position)

    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3

        delta = np.zeros(3)
        delta[j] = h
        A_plus = A_field_func(position + delta)
        A_minus = A_field_func(position - delta)

        B[i] = (A_plus[k] - A_minus[k]) / (2 * h)

        delta[j] = 0
        delta[k] = h
        A_plus = A_field_func(position + delta)
        A_minus = A_field_func(position - delta)

        B[i] -= (A_plus[j] - A_minus[j]) / (2 * h)

    return B


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Calculate vector potential from magnetization",
)
def calc_vector_potential_from_magnetization(
    magnetization_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    integration_volume: np.ndarray,
) -> np.ndarray:
    """
    Calculate vector potential from magnetization distribution.

    Art. 405: For a magnetized body with magnetization M(r'),
    the vector potential is:

        A(r) = ∫ (M(r') × (r - r')) / |r - r'|³ dV'

    This is equivalent to the bound current formulation:
        J_bound = c ∇ × M
        A(r) = (1/c) ∫ J_bound(r') / |r - r'| dV'

    Args:
        magnetization_func: Function returning M at a position.
        position: Position where A is calculated (cm).
        integration_volume: Array of sample points (N, 3).

    Returns:
        Vector potential A (gauss·cm).

    Reference:
        Part III, Art. 405: A from magnetization.
    """
    position = np.asarray(position, dtype=np.float64)
    integration_volume = np.asarray(integration_volume, dtype=np.float64)

    A = np.zeros(3)

    # Estimate volume element
    if len(integration_volume) > 1:
        bounds = np.max(integration_volume, axis=0) - np.min(integration_volume, axis=0)
        dV = np.prod(bounds) / len(integration_volume)
    else:
        dV = 1.0

    for r_prime in integration_volume:
        r_vec = position - r_prime
        r_mag = np.linalg.norm(r_vec)

        if r_mag < 1e-10:
            continue

        M = magnetization_func(r_prime)

        # dA = (M × r̂) / r² dV = (M × r) / r³ dV
        dA = dV * np.cross(M, r_vec) / (r_mag ** 3)
        A += dA

    return A


@maxwell_cite(
    406,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Relate scalar and vector potentials",
)
def relate_scalar_vector_potential(
    scalar_potential_func: Callable[[np.ndarray], float],
    vector_potential_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    h: float = 1e-8,
) -> dict[str, np.ndarray]:
    """
    Relate scalar potential Ω and vector potential A.

    Art. 406: The magnetic field can be expressed using either:
    - Scalar potential: H = -∇Ω (for current-free regions)
    - Vector potential: B = ∇×A (always valid)

    In a linear, isotropic medium with no free currents:
        H = -∇Ω
        B = μH = -μ∇Ω
        B = ∇×A

    Therefore: ∇×A = -μ∇Ω

    This function computes both H and B from their respective
    potentials for comparison.

    Args:
        scalar_potential_func: Function returning Ω at a position.
        vector_potential_func: Function returning A at a position.
        position: Position where fields are computed.
        h: Step size for numerical differentiation.

    Returns:
        Dictionary with:
        - H_from_scalar: -∇Ω
        - B_from_vector: ∇×A
        - note: Explanation of relationship

    Reference:
        Part III, Art. 406: Potential relations.
    """
    position = np.asarray(position, dtype=np.float64)

    # Compute H = -∇Ω
    grad_Omega = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        Omega_plus = scalar_potential_func(position + delta)
        Omega_minus = scalar_potential_func(position - delta)
        grad_Omega[i] = (Omega_plus - Omega_minus) / (2 * h)

    H_from_scalar = -grad_Omega

    # Compute B = ∇×A
    B_from_vector = calc_B_from_vector_potential(vector_potential_func, position, h)

    return {
        "H_from_scalar": H_from_scalar,
        "B_from_vector": B_from_vector,
        "scalar_gradient": grad_Omega,
        "note": "H = -∇Ω, B = ∇×A. In linear media: B = μH.",
    }


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Gauge transformation of vector potential",
)
def gauge_transform(
    A_field: np.ndarray,
    gauge_function_gradient: np.ndarray,
) -> np.ndarray:
    """
    Apply gauge transformation to vector potential.

    Art. 405-406: The vector potential has gauge freedom:

        A' = A + ∇χ

    leaves B = ∇×A unchanged since ∇×(∇χ) = 0.

    Common gauges:
    - Coulomb gauge: ∇·A = 0
    - Lorenz gauge: ∇·A + (1/c)∂φ/∂t = 0

    Args:
        A_field: Original vector potential.
        gauge_function_gradient: ∇χ to add.

    Returns:
        Transformed vector potential A'.

    Reference:
        Part III, Arts. 405-406: Gauge freedom.
    """
    A_field = np.asarray(A_field, dtype=np.float64)
    gauge_function_gradient = np.asarray(gauge_function_gradient, dtype=np.float64)

    return A_field + gauge_function_gradient


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Coulomb gauge condition ∇·A = 0",
)
def verify_coulomb_gauge(
    A_field_func: Callable[[np.ndarray], np.ndarray],
    test_points: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, float]:
    """
    Verify Coulomb gauge condition ∇·A = 0.

    Art. 405: The Coulomb gauge requires:

        ∇ · A = 0

    This is always possible for magnetostatic fields.

    Args:
        A_field_func: Function returning A at a position.
        test_points: Points where divergence is evaluated.
        tolerance: Maximum acceptable divergence.

    Returns:
        Dictionary with:
        - max_divergence: Maximum |∇·A| found
        - mean_divergence: Mean |∇·A|
        - is_coulomb_gauge: True if divergence < tolerance

    Reference:
        Part III, Art. 405: Coulomb gauge.
    """
    test_points = np.asarray(test_points, dtype=np.float64)
    h = 1e-6

    divergences = []

    for point in test_points:
        div = 0.0
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            A_plus = A_field_func(point + delta)
            A_minus = A_field_func(point - delta)
            div += (A_plus[i] - A_minus[i]) / (2 * h)
        divergences.append(abs(div))

    return {
        "max_divergence": max(divergences) if divergences else 0.0,
        "mean_divergence": float(np.mean(divergences)) if divergences else 0.0,
        "is_coulomb_gauge": max(divergences) <= tolerance if divergences else True,
    }


@maxwell_cite(
    406,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Vector potential for uniform B field",
)
def vector_potential_uniform_field(B_uniform: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    """
    Return vector potential for uniform magnetic field.

    Art. 406: For a uniform field B₀, one valid vector potential is:

        A(r) = (1/2) B₀ × r

    This satisfies ∇×A = B₀ and ∇·A = 0 (Coulomb gauge).

    Args:
        B_uniform: Uniform magnetic field (gauss).

    Returns:
        Function computing A(r) for the uniform field.

    Reference:
        Part III, Art. 406: Uniform field vector potential.
    """
    B_uniform = np.asarray(B_uniform, dtype=np.float64)

    def A_func(position: np.ndarray) -> np.ndarray:
        position = np.asarray(position, dtype=np.float64)
        return 0.5 * np.cross(B_uniform, position)

    return A_func
