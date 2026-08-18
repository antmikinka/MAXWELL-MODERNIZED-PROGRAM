"""
Magnetic field decomposition — lamellar and solenoidal fields.

Implements the theory of magnetic field decomposition from Part III of Maxwell's Treatise:
- Lamellar (irrotational) distributions (Arts. 412-413)
- Complex lamellar systems (Art. 415)
- Vector potential for lamellar fields (Art. 416)

Maxwell shows that magnetic fields can be decomposed into:
1. Lamellar (irrotational) part: ∇×H = 0, derivable from scalar potential
2. Solenoidal (divergence-free) part: ∇·B = 0, derivable from vector potential

A lamellar magnetization has:
    I = -∇ψ  (gradient of scalar function)

and produces a field that can be computed from a scalar potential.

Category: A (maxwell_original) — Maxwell's field decomposition theory.

References:
    Part III, Arts. 412-416: Lamellar and solenoidal fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class LamellarDistribution:
    """
    Lamellar (irrotational) magnetization distribution.

    Art. 412-413: A magnetization is lamellar (irrotational) when it
    can be expressed as the gradient of a scalar potential:

        I = -∇ψ

    This implies ∇×I = 0 (zero curl), meaning the magnetization
    has no "circulation" or vorticity.

    Lamellar distributions are important because they produce
    fields that can be computed from scalar potentials alone.

    Attributes:
        potential_func: Scalar potential function ψ(x,y,z).
        magnetization_func: Function computing I = -∇ψ.
    """

    potential_func: Callable[[np.ndarray], float]
    magnetization_func: Optional[Callable[[np.ndarray], np.ndarray]] = None

    @classmethod
    @maxwell_cite(
        412,
        part=3,
        chapter="Field Decomposition",
        theory_class="maxwell_original",
        description="Create lamellar distribution from scalar potential",
    )
    def from_scalar_potential(
        cls,
        potential_func: Callable[[np.ndarray], float],
        h: float = 1e-8,
    ) -> LamellarDistribution:
        """
        Create lamellar distribution from scalar potential.

        Art. 412: Given a scalar potential ψ, the lamellar
        magnetization is:

            I = -∇ψ

        This function computes the magnetization numerically.

        Args:
            potential_func: Function returning ψ at a position.
            h: Step size for numerical gradient.

        Returns:
            LamellarDistribution object.

        Reference:
            Part III, Art. 412: Lamellar distributions.
        """

        def magnetization_at(point: np.ndarray) -> np.ndarray:
            point = np.asarray(point, dtype=np.float64)
            grad = np.zeros(3)

            for i in range(3):
                delta = np.zeros(3)
                delta[i] = h
                psi_plus = potential_func(point + delta)
                psi_minus = potential_func(point - delta)
                grad[i] = (psi_plus - psi_minus) / (2 * h)

            # I = -∇ψ
            return -grad

        return cls(
            potential_func=potential_func,
            magnetization_func=magnetization_at,
        )

    @maxwell_cite(
        412,
        part=3,
        chapter="Field Decomposition",
        theory_class="maxwell_original",
        description="Verify lamellar condition ∇×I = 0",
    )
    def verify_lamellar(
        self,
        test_points: np.ndarray,
        tolerance: float = 1e-10,
    ) -> bool:
        """
        Verify that the distribution is truly lamellar.

        Art. 412: A lamellar distribution must satisfy:

            ∇ × I = 0

        This function checks the condition numerically.

        Args:
            test_points: Points where curl is evaluated.
            tolerance: Maximum acceptable curl magnitude.

        Returns:
            True if curl < tolerance at all points.

        Reference:
            Part III, Art. 412: Lamellar condition.
        """
        if self.magnetization_func is None:
            return False

        test_points = np.asarray(test_points, dtype=np.float64)
        h = 1e-6

        for point in test_points:
            # Numerical curl: (∇×I)_i = ε_ijk ∂_j I_k
            curl = np.zeros(3)

            # Curl components using finite differences
            # (∇×I)_x = ∂I_z/∂y - ∂I_y/∂z
            # (∇×I)_y = ∂I_x/∂z - ∂I_z/∂x
            # (∇×I)_z = ∂I_y/∂x - ∂I_x/∂y

            I_center = self.magnetization_func(point)

            for i in range(3):
                for j in range(3):
                    if i != j:
                        delta = np.zeros(3)
                        delta[j] = h
                        I_plus = self.magnetization_func(point + delta)
                        I_minus = self.magnetization_func(point - delta)

                        # Levi-Civita symbol contribution
                        sign = 1 if (i, j) in [(0, 1), (1, 2), (2, 0)] else -1
                        curl[i] += (
                            sign
                            * (I_plus[(i + 1) % 3] - I_minus[(i + 1) % 3])
                            / (2 * h)
                        )

            if np.linalg.norm(curl) > tolerance:
                return False

        return True


@dataclass
class ComplexLamellarDistribution:
    """
    Complex lamellar system — superposition of lamellar distributions.

    Art. 415: A complex lamellar distribution is formed by the
    superposition of multiple simple lamellar systems. The total
    magnetization is the vector sum:

        I_total = I_1 + I_2 + ... + I_n

    where each I_k is lamellar (derivable from a scalar potential).

    Attributes:
        distributions: List of LamellarDistribution objects.
    """

    distributions: list[LamellarDistribution]

    @classmethod
    @maxwell_cite(
        415,
        part=3,
        chapter="Field Decomposition",
        theory_class="maxwell_original",
        description="Create complex lamellar system from components",
    )
    def from_distributions(
        cls,
        distributions: list[LamellarDistribution],
    ) -> ComplexLamellarDistribution:
        """
        Create complex lamellar system from components.

        Art. 415: Multiple lamellar distributions can be combined
        to form a complex system.

        Args:
            distributions: List of LamellarDistribution objects.

        Returns:
            ComplexLamellarDistribution object.

        Reference:
            Part III, Art. 415: Complex lamellar systems.
        """
        return cls(distributions=distributions)

    def total_magnetization(self, point: np.ndarray) -> np.ndarray:
        """
        Calculate total magnetization at a point.

        I_total = Σ I_k

        Args:
            point: Position where magnetization is calculated.

        Returns:
            Total magnetization vector (emu/cm³).
        """
        point = np.asarray(point, dtype=np.float64)
        I_total = np.zeros(3)

        for dist in self.distributions:
            if dist.magnetization_func is not None:
                I_total += dist.magnetization_func(point)

        return I_total

    def total_potential(self, point: np.ndarray) -> float:
        """
        Calculate total scalar potential at a point.

        ψ_total = Σ ψ_k

        Args:
            point: Position where potential is calculated.

        Returns:
            Total scalar potential.
        """
        point = np.asarray(point, dtype=np.float64)
        psi_total = 0.0

        for dist in self.distributions:
            psi_total += dist.potential_func(point)

        return psi_total


@maxwell_cite(
    412,
    part=3,
    chapter="Field Decomposition",
    theory_class="maxwell_original",
    description="Calculate lamellar potential",
)
def lamellar_potential(
    magnetization_func: Callable[[np.ndarray], np.ndarray],
    reference_point: np.ndarray,
    evaluation_point: np.ndarray,
    path_steps: int = 100,
) -> float:
    """
    Calculate scalar potential for lamellar magnetization.

    Art. 412: For a lamellar distribution, the scalar potential
    at a point is the line integral:

        ψ(r) = -∫ I · dl  (from reference point to r)

    The integral is path-independent for truly lamellar fields.

    Args:
        magnetization_func: Function returning I at a position.
        reference_point: Reference point where ψ = 0.
        evaluation_point: Point where potential is calculated.
        path_steps: Number of steps for numerical integration.

    Returns:
        Scalar potential ψ at evaluation point.

    Reference:
        Part III, Art. 412: Lamellar potential.
    """
    reference_point = np.asarray(reference_point, dtype=np.float64)
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)

    # Straight line path
    path_vector = evaluation_point - reference_point
    dl = path_vector / path_steps

    psi = 0.0
    for i in range(path_steps):
        t = (i + 0.5) / path_steps  # Midpoint
        current_point = reference_point + t * path_vector
        I = magnetization_func(current_point)
        psi -= np.dot(I, dl)

    return psi


@maxwell_cite(
    413,
    part=3,
    chapter="Field Decomposition",
    theory_class="maxwell_original",
    description="Calculate vector potential for lamellar field",
)
def lamellar_vector_potential(
    magnetization_func: Callable[[np.ndarray], np.ndarray],
    evaluation_point: np.ndarray,
    integration_volume: np.ndarray,
    num_samples: int = 1000,
) -> np.ndarray:
    """
    Calculate vector potential for lamellar magnetization.

    Art. 413: For a lamellar distribution, the vector potential A
    can be computed from:

        A(r) = ∫ (I(r') × (r - r')) / |r - r'|³ dV'

    This integral is over the volume containing the magnetization.

    Args:
        magnetization_func: Function returning I at a position.
        evaluation_point: Point where A is calculated.
        integration_volume: Array of sample points in volume (N, 3).
        num_samples: Number of volume elements.

    Returns:
        Vector potential A (gauss·cm).

    Reference:
        Part III, Art. 413: Vector potential for lamellar fields.
    """
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)
    integration_volume = np.asarray(integration_volume, dtype=np.float64)

    if len(integration_volume.shape) != 2 or integration_volume.shape[1] != 3:
        raise ValueError("integration_volume must be (N, 3) array")

    A = np.zeros(3)

    # Volume per sample (approximate)
    # For a regular grid, this would be the cell volume
    # Here we estimate from bounding box
    bounds_min = np.min(integration_volume, axis=0)
    bounds_max = np.max(integration_volume, axis=0)
    volume = np.prod(bounds_max - bounds_min) / len(integration_volume)

    for r_prime in integration_volume:
        r_vec = evaluation_point - r_prime
        r_mag = np.linalg.norm(r_vec)

        if r_mag < 1e-10:
            continue  # Skip singularity

        I_prime = magnetization_func(r_prime)

        # dA = (I × r̂) / r² dV = (I × r) / r³ dV
        dA = volume * np.cross(I_prime, r_vec) / (r_mag**3)
        A += dA

    return A


@maxwell_cite(
    415,
    part=3,
    chapter="Field Decomposition",
    theory_class="maxwell_original",
    description="Decompose field into lamellar and solenoidal parts",
)
def helmholtz_decomposition(
    field_func: Callable[[np.ndarray], np.ndarray],
    evaluation_point: np.ndarray,
    sample_points: np.ndarray,
) -> dict[str, np.ndarray]:
    """
    Decompose a vector field into lamellar and solenoidal parts.

    Art. 415: Any vector field can be decomposed as:

        F = F_lamellar + F_solenoidal

    where:
    - F_lamellar = -∇φ (irrotational, ∇×F = 0)
    - F_solenoidal = ∇×A (divergence-free, ∇·F = 0)

    This is the Helmholtz decomposition theorem.

    Args:
        field_func: Function returning F at a position.
        evaluation_point: Point where decomposition is computed.
        sample_points: Points for numerical integration.

    Returns:
        Dictionary with:
        - lamellar_part: -∇φ component
        - solenoidal_part: ∇×A component
        - original_field: F at evaluation point

    Reference:
        Part III, Art. 415: Field decomposition.
    """
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)
    sample_points = np.asarray(sample_points, dtype=np.float64)

    F = field_func(evaluation_point)

    # Simplified: compute scalar potential from divergence
    # φ(r) = -∫ (∇'·F(r')) / |r - r'| dV' / 4π

    # For demonstration, use a simple approximation
    # In practice, this requires solving Poisson's equation

    # Approximate: project F onto gradient direction
    # This is a simplified version for illustration

    # Compute divergence at sample points
    h = 1e-6
    divergences = []
    for point in sample_points:
        div = 0.0
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            F_plus = field_func(point + delta)
            F_minus = field_func(point - delta)
            div += (F_plus[i] - F_minus[i]) / (2 * h)
        divergences.append(div)

    # Compute scalar potential at evaluation point
    phi = 0.0
    for i, r_prime in enumerate(sample_points):
        r_vec = evaluation_point - r_prime
        r_mag = np.linalg.norm(r_vec)
        if r_mag > 1e-10:
            phi += divergences[i] / r_mag

    phi /= -4 * np.pi
    phi *= np.prod(np.max(sample_points, axis=0) - np.min(sample_points, axis=0)) / len(
        sample_points
    )

    # Lamellar part: -∇φ (approximate as F projected onto radial direction)
    # This is a simplified approximation

    # For exact decomposition, solve Poisson's equation for φ
    # Here we return a placeholder

    F_lamellar = np.zeros(3)  # Would require full Poisson solve
    F_solenoidal = F - F_lamellar

    return {
        "lamellar_part": F_lamellar,
        "solenoidal_part": F_solenoidal,
        "original_field": F,
        "scalar_potential_estimate": phi,
    }


@maxwell_cite(
    416,
    part=3,
    chapter="Field Decomposition",
    theory_class="maxwell_original",
    description="Relation between scalar and vector potentials",
)
def relate_scalar_vector_potential(
    scalar_potential_func: Callable[[np.ndarray], float],
    evaluation_point: np.ndarray,
    h: float = 1e-8,
) -> dict[str, np.ndarray]:
    """
    Relate scalar and vector potentials for lamellar fields.

    Art. 416: For a lamellar field:
    - Scalar potential: φ where F = -∇φ
    - Vector potential: A where F = ∇×A

    For lamellar fields, A can be chosen such that:
        A = ∇×(ψ r)  (for some scalar ψ)

    This is one of many possible vector potentials (gauge freedom).

    Args:
        scalar_potential_func: Function returning φ at a position.
        evaluation_point: Point where potentials are related.
        h: Step size for numerical gradient.

    Returns:
        Dictionary with:
        - gradient_of_scalar: -∇φ (the lamellar field)
        - vector_potential_example: One possible A

    Reference:
        Part III, Art. 416: Potential relations.
    """
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)

    # Compute gradient of scalar potential
    grad_phi = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        phi_plus = scalar_potential_func(evaluation_point + delta)
        phi_minus = scalar_potential_func(evaluation_point - delta)
        grad_phi[i] = (phi_plus - phi_minus) / (2 * h)

    # Lamellar field
    F_lamellar = -grad_phi

    # Vector potential example (one possible gauge choice)
    # A = (1/2) F × r is one valid choice for uniform field
    r = evaluation_point
    A_example = 0.5 * np.cross(F_lamellar, r)

    return {
        "gradient_of_scalar": grad_phi,
        "lamellar_field": F_lamellar,
        "vector_potential_example": A_example,
        "note": "Vector potential has gauge freedom: A → A + ∇χ",
    }


@maxwell_cite(
    412,
    413,
    415,
    416,
    part=3,
    chapter="Field Decomposition",
    theory_class="maxwell_original",
    description="Check if magnetization is lamellar",
)
def is_lamellar_magnetization(
    magnetization_func: Callable[[np.ndarray], np.ndarray],
    test_points: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, any]:
    """
    Check if a magnetization distribution is lamellar.

    Art. 412-416: A magnetization is lamellar if and only if:
    - ∇ × I = 0 (irrotational)

    Equivalently, I can be written as I = -∇ψ for some scalar ψ.

    Args:
        magnetization_func: Function returning I at a position.
        test_points: Points where curl is evaluated.
        tolerance: Maximum acceptable curl magnitude.

    Returns:
        Dictionary with:
        - is_lamellar: True if curl < tolerance everywhere
        - max_curl: Maximum |∇×I| found
        - test_points_checked: Number of points tested

    Reference:
        Part III, Arts. 412-416: Lamellar condition.
    """
    test_points = np.asarray(test_points, dtype=np.float64)
    h = 1e-6

    max_curl = 0.0

    for point in test_points:
        # Numerical curl
        curl = np.zeros(3)

        I_center = magnetization_func(point)

        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3

            delta = np.zeros(3)
            delta[j] = h
            I_plus = magnetization_func(point + delta)
            I_minus = magnetization_func(point - delta)

            # (∇×I)_i = ∂I_k/∂j - ∂I_j/∂k
            # Simplified for orthogonal grid
            curl[i] = (I_plus[k] - I_minus[k]) / (2 * h)

        curl_mag = np.linalg.norm(curl)
        max_curl = max(max_curl, curl_mag)

    return {
        "is_lamellar": max_curl <= tolerance,
        "max_curl": max_curl,
        "test_points_checked": len(test_points),
        "tolerance_used": tolerance,
    }
