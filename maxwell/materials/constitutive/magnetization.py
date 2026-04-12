"""maxwell.materials.constitutive.magnetization — Magnetization relation (Art. 605).

Implements Maxwell's constitutive relation for magnetic materials,
relating magnetic induction B to magnetic field H.

Maxwell's CGS formulation (Art. 605):
    Magnetic induction equation (Eq. D):

        B = H + 4πI = μH

    where:
    - I = intensity of magnetization (magnetic moment per unit volume)
    - μ = permeability = 1 + 4πk (k = magnetic susceptibility)

    In CGS-Gaussian:
        B = μH  (gauss)
        M = χH  (magnetization)
        B = H + 4πM

where:
    B = magnetic induction (gauss)
    H = magnetic field intensity (oersted)
    I, M = magnetization (emu/cm³)
    μ = permeability (dimensionless)
    χ = magnetic susceptibility (dimensionless)

Category: A (maxwell_original) — Maxwell's magnetization theory.

References:
    Part IV, Art. 605: Magnetic induction equation (Eq. D).
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class Magnetization:
    """
    Magnetization calculator for magnetic materials.

    Art. 605: Maxwell's relation for magnetic materials:

        B = H + 4πI = μH

    where I is the intensity of magnetization (magnetic moment
    per unit volume).

    Attributes:
        susceptibility: Magnetic susceptibility χ (dimensionless).
        permeability: Permeability μ = 1 + 4πχ.
    """

    susceptibility: float = 0.0
    permeability: float = None

    def __post_init__(self):
        """Calculate permeability from susceptibility if not provided."""
        if self.permeability is None:
            self.permeability = 1.0 + 4.0 * np.pi * self.susceptibility

    @maxwell_cite(
        605,
        part=4, chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate magnetic induction B from H",
    )
    def magnetic_induction(self, H_field: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic induction B from magnetic field H.

        Art. 605: B = μH

        Args:
            H_field: Magnetic field intensity (oersted).

        Returns:
            Magnetic induction B (gauss).
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        return self.permeability * H_field

    @maxwell_cite(
        605,
        part=4, chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate magnetization intensity I from H",
    )
    def magnetization_intensity(self, H_field: np.ndarray) -> np.ndarray:
        """
        Calculate magnetization intensity I (magnetic moment per volume).

        Art. 605: I = χH

        In Maxwell's notation, I is the intensity of magnetization.

        Args:
            H_field: Magnetic field intensity (oersted).

        Returns:
            Magnetization intensity I (emu/cm³).
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        return self.susceptibility * H_field

    @maxwell_cite(
        605,
        part=4, chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate H from B",
    )
    def magnetic_field(self, B_field: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field H from magnetic induction B.

        Art. 605: H = B / μ

        Args:
            B_field: Magnetic induction (gauss).

        Returns:
            Magnetic field intensity H (oersted).
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        return B_field / self.permeability


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic induction: B = μH",
)
def calc_magnetic_induction(
    H_field: np.ndarray,
    permeability: float = 1.0,
) -> np.ndarray:
    """
    Calculate magnetic induction from magnetic field.

    Art. 605: The constitutive relation for magnetic materials:

        B = μH

    In CGS, for vacuum μ = 1, so B = H.
    For paramagnetic materials μ > 1.
    For diamagnetic materials μ < 1.

    Args:
        H_field: Magnetic field intensity (oersted).
        permeability: Relative permeability μ (dimensionless).

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part IV, Art. 605: Magnetic induction (Eq. D).
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    return permeability * H_field


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetization: I = χH",
)
def calc_magnetization_intensity(
    H_field: np.ndarray,
    susceptibility: float,
) -> np.ndarray:
    """
    Calculate magnetization intensity.

    Art. 605: The magnetization (magnetic moment per unit volume) is:

        I = χH

    where χ is the magnetic susceptibility.

    Args:
        H_field: Magnetic field intensity (oersted).
        susceptibility: Magnetic susceptibility χ (dimensionless).

    Returns:
        Magnetization intensity I (emu/cm³).

    Reference:
        Part IV, Art. 605: Magnetization intensity.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    return susceptibility * H_field


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate permeability from susceptibility",
)
def calc_permeability(susceptibility: float) -> float:
    """
    Calculate permeability from magnetic susceptibility.

    Art. 605: The relation is:

        μ = 1 + 4πχ

    Args:
        susceptibility: Magnetic susceptibility χ.

    Returns:
        Permeability μ (dimensionless).

    Reference:
        Part IV, Art. 605: Permeability relation.
    """
    return 1.0 + 4.0 * np.pi * susceptibility


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate susceptibility from permeability",
)
def calc_susceptibility(permeability: float) -> float:
    """
    Calculate susceptibility from permeability.

    Art. 605: Inverting μ = 1 + 4πχ:

        χ = (μ - 1) / (4π)

    Args:
        permeability: Permeability μ.

    Returns:
        Susceptibility χ.

    Reference:
        Part IV, Art. 605: Susceptibility from permeability.
    """
    return (permeability - 1.0) / (4.0 * np.pi)


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate magnetic moment of magnetized body",
)
def calc_magnetic_moment(
    magnetization: np.ndarray,
    volume: float,
) -> np.ndarray:
    """
    Calculate total magnetic moment of a magnetized body.

    Art. 605: For uniform magnetization I:

        m = I * V

    Args:
        magnetization: Magnetization intensity I (emu/cm³).
        volume: Volume of body (cm³).

    Returns:
        Magnetic moment m (emu).

    Reference:
        Part IV, Art. 605: Magnetic moment.
    """
    magnetization = np.asarray(magnetization, dtype=np.float64)
    return magnetization * volume


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Verify magnetization relations",
)
def verify_magnetization(
    H_field: np.ndarray = None,
    susceptibility: float = 0.01,
    tolerance: float = 1e-10,
) -> dict[str, float | np.ndarray | bool]:
    """
    Verify magnetization relations.

    Art. 605: This function verifies:
    1. B = H + 4πI
    2. B = μH
    3. μ = 1 + 4πχ

    Args:
        H_field: Test magnetic field (oersted).
        susceptibility: Test susceptibility.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if H_field is None:
        H_field = np.array([100.0, 0.0, 0.0])

    H_field = np.asarray(H_field, dtype=np.float64)

    # Calculate quantities
    permeability = calc_permeability(susceptibility)
    I = calc_magnetization_intensity(H_field, susceptibility)
    B_from_mu = calc_magnetic_induction(H_field, permeability)
    B_from_I = H_field + 4.0 * np.pi * I

    # Verify B = H + 4πI = μH
    B_error = np.linalg.norm(B_from_mu - B_from_I) / np.linalg.norm(B_from_mu) if np.linalg.norm(B_from_mu) > 0 else 0

    # Verify μ = 1 + 4πχ
    mu_check = calc_permeability(susceptibility)
    mu_error = abs(mu_check - (1.0 + 4.0 * np.pi * susceptibility))

    return {
        "H_field": H_field,
        "susceptibility": susceptibility,
        "permeability": permeability,
        "magnetization_I": I,
        "B_from_mu": B_from_mu,
        "B_from_H_4piI": B_from_I,
        "B_error": B_error,
        "mu_error": mu_error,
        "verified": B_error < tolerance and mu_error < tolerance,
    }


@maxwell_cite(
    605,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Complete magnetization analysis",
)
def analyze_magnetization(
    H_field: np.ndarray,
    susceptibility: float,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of magnetization.

    Art. 605: Comprehensive analysis including:
    1. Magnetization intensity
    2. Magnetic induction
    3. Permeability
    4. Material classification

    Args:
        H_field: Applied magnetic field (oersted).
        susceptibility: Magnetic susceptibility.

    Returns:
        Dictionary with complete analysis results.
    """
    H_field = np.asarray(H_field, dtype=np.float64)

    permeability = calc_permeability(susceptibility)
    I = calc_magnetization_intensity(H_field, susceptibility)
    B = calc_magnetic_induction(H_field, permeability)

    # Material classification
    if susceptibility > 0:
        material_type = "paramagnetic" if susceptibility < 1 else "ferromagnetic"
    elif susceptibility < 0:
        material_type = "diamagnetic"
    else:
        material_type = "non-magnetic"

    return {
        "H_field": H_field,
        "susceptibility": susceptibility,
        "permeability": permeability,
        "magnetization_intensity": I,
        "magnetic_induction": B,
        "material_type": material_type,
        "relative_B enhancement": permeability,
    }
