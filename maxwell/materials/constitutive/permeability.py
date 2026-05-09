"""maxwell.materials.constitutive.permeability — Permeability relation (Art. 614).

Implements Maxwell's treatment of magnetic permeability, including
the relation between B, H, and the permeability coefficient.

Maxwell's CGS formulation (Art. 614):
    Permeability equation (Eq. L):

        B = μH

    where:
    - μ = permeability coefficient
    - For vacuum, μ = 1 in CGS
    - For paramagnetic materials, μ > 1
    - For diamagnetic materials, μ < 1

    Maxwell also defined the coefficient of magnetization k:
        μ = 1 + 4πk

where:
    B = magnetic induction (gauss)
    H = magnetic field intensity (oersted)
    μ = permeability (dimensionless in CGS)
    k = coefficient of magnetization (dimensionless)

Category: A (maxwell_original) — Maxwell's permeability theory.

References:
    Part IV, Art. 614: Permeability equation (Eq. L).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

# Alias for test compatibility
VACUUM_PERMEABILITY = 1.0  # In CGS-EMU, mu_0 = 1 by definition


@dataclass
class Permeability:
    """
    Permeability calculator for magnetic materials.

    Art. 614: Maxwell's permeability relation:

        B = μH

    where μ is the permeability coefficient.

    Attributes:
        permeability: Permeability coefficient μ (dimensionless).
    """

    permeability: float = 1.0

    def __post_init__(self):
        """Validate permeability."""
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")

    @maxwell_cite(
        614,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate magnetic induction B from H",
    )
    def B_from_H(self, H_field: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic induction from magnetic field.

        Art. 614: B = μH

        Args:
            H_field: Magnetic field intensity (oersted).

        Returns:
            Magnetic induction B (gauss).
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        return self.permeability * H_field

    @maxwell_cite(
        614,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate magnetic field H from B",
    )
    def H_from_B(self, B_field: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field from magnetic induction.

        Art. 614: H = B / μ

        Args:
            B_field: Magnetic induction (gauss).

        Returns:
            Magnetic field intensity H (oersted).
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        return B_field / self.permeability

    # Aliases for backward compatibility
    magnetic_induction = B_from_H
    magnetic_field = H_from_B

    @maxwell_cite(
        614,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate coefficient of magnetization k",
    )
    def magnetization_coefficient(self) -> float:
        """
        Calculate Maxwell's coefficient of magnetization k.

        Art. 614: From μ = 1 + 4πk:

            k = (μ - 1) / (4π)

        Returns:
            Coefficient of magnetization k.
        """
        return (self.permeability - 1.0) / (4.0 * np.pi)

    @property
    def relative_permeability(self) -> float:
        """
        Relative permeability (same as μ in CGS).

        Returns:
            Relative permeability μ_r = μ.
        """
        return self.permeability


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic induction: B = μH",
)
def calc_magnetic_induction_permeability(
    H_field: np.ndarray,
    permeability: float,
) -> np.ndarray:
    """
    Calculate magnetic induction using permeability.

    Art. 614: The constitutive relation:

        B = μH

    Args:
        H_field: Magnetic field intensity (oersted).
        permeability: Permeability coefficient μ.

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part IV, Art. 614: Permeability equation (Eq. L).
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    return permeability * H_field


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate permeability from coefficient k",
)
def calc_permeability_from_k(k: float) -> float:
    """
    Calculate permeability from Maxwell's coefficient k.

    Art. 614: From μ = 1 + 4πk:

        μ = 1 + 4πk

    Args:
        k: Coefficient of magnetization.

    Returns:
        Permeability μ.

    Reference:
        Part IV, Art. 614: Permeability from k.
    """
    return 1.0 + 4.0 * np.pi * k


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate coefficient k from permeability",
)
def calc_k_from_permeability(permeability: float) -> float:
    """
    Calculate Maxwell's coefficient k from permeability.

    Art. 614: From μ = 1 + 4πk:

        k = (μ - 1) / (4π)

    Args:
        permeability: Permeability μ.

    Returns:
        Coefficient of magnetization k.

    Reference:
        Part IV, Art. 614: k from permeability.
    """
    return (permeability - 1.0) / (4.0 * np.pi)


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic energy density",
)
def calc_magnetic_energy_density(
    B_field: np.ndarray | float,
    permeability: float = None,
    H_field: np.ndarray = None,
) -> float:
    """
    Calculate magnetic energy density.

    Art. 614: The magnetic energy density is:

        u = (1/8π) * B · H = (1/8π) * μH² = B² / (8πμ)

    This function supports two calling conventions:
    1. calc_magnetic_energy_density(B, mu) — scalar B and permeability
    2. calc_magnetic_energy_density(B, H=H) — vector B and H field

    Args:
        B_field: Magnetic induction (gauss) — scalar or vector.
        permeability: Permeability coefficient μ (when using scalar B).
        H_field: Magnetic field intensity (oersted) — optional.

    Returns:
        Energy density (ergs/cm³).

    Reference:
        Part IV, Art. 614: Magnetic energy.
    """
    # If B_field is scalar and permeability is provided, use u = B²/(8πμ)
    if isinstance(B_field, (int, float)) or np.isscalar(B_field):
        B = float(B_field)
        if permeability is None:
            raise ValueError("permeability must be provided when B is scalar")
        return B**2 / (8.0 * np.pi * permeability)

    # Otherwise use u = (1/8π) * B · H
    if H_field is None:
        if permeability is not None:
            # Compute H from B and mu
            H_field = np.asarray(B_field, dtype=np.float64) / permeability
        else:
            raise ValueError("Either H_field or permeability must be provided")
    else:
        H_field = np.asarray(H_field, dtype=np.float64)

    B_field = np.asarray(B_field, dtype=np.float64)
    return (1.0 / (8.0 * np.pi)) * np.dot(B_field, H_field)


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Classify material by permeability",
)
def classify_material_by_permeability(permeability: float) -> str:
    """
    Classify magnetic material by permeability.

    Art. 614: Materials are classified as:
    - Diamagnetic: μ < 1 (k < 0)
    - Paramagnetic: μ > 1 (k > 0, small)
    - Ferromagnetic: μ >> 1 (k >> 0)

    Args:
        permeability: Permeability μ.

    Returns:
        Material classification string.

    Reference:
        Part IV, Art. 614: Material classification.
    """
    k = calc_k_from_permeability(permeability)

    if permeability < 1.0:
        return "diamagnetic"
    elif permeability < 1.1:
        return "paramagnetic"
    else:
        return "ferromagnetic"


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic flux through surface",
)
def calc_magnetic_flux(
    B_field: np.ndarray,
    area: float,
    normal: np.ndarray = None,
) -> float:
    """
    Calculate magnetic flux through a surface.

    Art. 614: The magnetic flux is:

        Φ = B · A = B · n * A

    Args:
        B_field: Magnetic induction (gauss).
        area: Surface area (cm²).
        normal: Unit normal to surface (default: z-axis).

    Returns:
        Magnetic flux Φ (maxwells).

    Reference:
        Part IV, Art. 614: Magnetic flux.
    """
    B_field = np.asarray(B_field, dtype=np.float64)

    if normal is None:
        normal = np.array([0.0, 0.0, 1.0])
    else:
        normal = np.asarray(normal, dtype=np.float64)
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm

    return np.dot(B_field, normal) * area


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Verify permeability relations",
)
def verify_permeability_relations(
    H_field: np.ndarray = None,
    permeability: float = 100.0,
    tolerance: float = 1e-10,
) -> dict[str, float | np.ndarray | bool]:
    """
    Verify permeability relations.

    Art. 614: This function verifies:
    1. B = μH
    2. H = B/μ
    3. μ = 1 + 4πk

    Args:
        H_field: Test magnetic field (oersted).
        permeability: Test permeability.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if H_field is None:
        H_field = np.array([100.0, 0.0, 0.0])

    H_field = np.asarray(H_field, dtype=np.float64)

    # Calculate B
    B = calc_magnetic_induction_permeability(H_field, permeability)

    # Calculate H from B
    H_from_B = B / permeability

    # Verify H = B/μ
    H_error = (
        np.linalg.norm(H_field - H_from_B) / np.linalg.norm(H_field)
        if np.linalg.norm(H_field) > 0
        else 0
    )

    # Verify μ = 1 + 4πk
    k = calc_k_from_permeability(permeability)
    mu_from_k = calc_permeability_from_k(k)
    mu_error = abs(mu_from_k - permeability) / permeability

    return {
        "H_field": H_field,
        "permeability": permeability,
        "coefficient_k": k,
        "magnetic_induction_B": B,
        "H_from_B": H_from_B,
        "H_error": H_error,
        "permeability_error": mu_error,
        "material_type": classify_material_by_permeability(permeability),
        "verified": H_error < tolerance and mu_error < tolerance,
    }


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Complete permeability analysis",
)
def analyze_permeability(
    H_field: np.ndarray,
    permeability: float,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of permeability.

    Art. 614: Comprehensive analysis including:
    1. Magnetic induction
    2. Coefficient of magnetization
    3. Energy density
    4. Material classification

    Args:
        H_field: Applied magnetic field (oersted).
        permeability: Permeability μ.

    Returns:
        Dictionary with complete analysis results.
    """
    H_field = np.asarray(H_field, dtype=np.float64)

    B = calc_magnetic_induction_permeability(H_field, permeability)
    k = calc_k_from_permeability(permeability)
    energy_density = calc_magnetic_energy_density(B, H_field)

    return {
        "H_field": H_field,
        "H_magnitude": np.linalg.norm(H_field),
        "permeability": permeability,
        "coefficient_k": k,
        "magnetic_induction_B": B,
        "B_magnitude": np.linalg.norm(B),
        "energy_density": energy_density,
        "material_type": classify_material_by_permeability(permeability),
        "B_enhancement_factor": permeability,
    }


# Alias for test compatibility
calc_B_from_H = calc_magnetic_induction_permeability


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic field H from B: H = B/μ",
)
def calc_H_from_B(
    B_field: np.ndarray,
    permeability: float,
) -> np.ndarray:
    """
    Calculate magnetic field from magnetic induction.

    Art. 614: The inverse relation:

        H = B / μ

    Args:
        B_field: Magnetic induction (gauss).
        permeability: Permeability coefficient μ.

    Returns:
        Magnetic field intensity H (oersted).

    Reference:
        Part IV, Art. 614: Permeability equation (Eq. L).
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    return B_field / permeability


@maxwell_cite(
    614,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate relative permeability",
)
def calc_relative_permeability(permeability: float) -> float:
    """
    Calculate relative permeability.

    Art. 614: In CGS, the relative permeability is:

        μ_r = μ / μ_0 = μ  (since μ_0 = 1 in CGS)

    Args:
        permeability: Permeability μ.

    Returns:
        Relative permeability μ_r.

    Reference:
        Part IV, Art. 614: Relative permeability.
    """
    return permeability
