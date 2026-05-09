"""
Magnetic constitutive relation — the B = H + 4πI law.

Implements the constitutive relation from Part III of Maxwell's Treatise:
- Constitutive relation B = H + 4πI (Art. 400)
- Magnetic permeability μ and susceptibility κ
- Linear and nonlinear magnetic materials

In CGS units, the constitutive relation is:
    B = H + 4πI

For linear materials where I = κH:
    B = H + 4πκH = (1 + 4πκ)H = μH

where:
- κ is magnetic susceptibility (dimensionless in CGS)
- μ = 1 + 4πκ is permeability (dimensionless in CGS)

Category: A (maxwell_original) — Maxwell's constitutive relation.

References:
    Part III, Art. 400: Magnetic constitutive relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


class MaterialType(Enum):
    """
    Classification of magnetic materials by susceptibility.

    Art. 400: Materials are classified by their magnetic response:

    - Diamagnetic: κ < 0 (weakly repelled by magnetic field)
    - Paramagnetic: κ > 0 (weakly attracted to magnetic field)
    - Ferromagnetic: κ >> 0, nonlinear (strongly attracted)

    In CGS, typical values:
    - Diamagnetic: κ ≈ -10⁻⁵ to -10⁻⁶
    - Paramagnetic: κ ≈ +10⁻⁵ to +10⁻³
    - Ferromagnetic: κ ≈ 10² to 10⁶ (variable)
    """

    DIAMAGNETIC = "diamagnetic"
    PARAMAGNETIC = "paramagnetic"
    FERROMAGNETIC = "ferromagnetic"
    ANTIMAGNETIC = "antimagnetic"  # κ = -1/4π, perfect diamagnet

    @classmethod
    @maxwell_cite(
        400,
        part=3,
        chapter="Magnetic Constitutive Relation",
        theory_class="maxwell_original",
        description="Classify material by susceptibility",
    )
    def from_susceptibility(cls, kappa: float) -> MaterialType:
        """
        Classify material by its magnetic susceptibility.

        Args:
            kappa: Magnetic susceptibility κ (CGS, dimensionless).

        Returns:
            MaterialType classification.

        Reference:
            Part III, Art. 400: Material classification.
        """
        if kappa < -0.1:
            return cls.ANTIMAGNETIC  # Perfect diamagnet (superconductor)
        elif kappa < 0:
            return cls.DIAMAGNETIC
        elif kappa < 10:
            return cls.PARAMAGNETIC
        else:
            return cls.FERROMAGNETIC


@dataclass
class MagneticConstitutiveRelation:
    """
    Magnetic constitutive relation — relates B, H, and I.

    Art. 400: The constitutive relation specifies how the magnetic
    induction B relates to the magnetic force H and magnetization I.

    General form (CGS):
        B = H + 4πI

    For linear materials (I = κH):
        B = μH  where μ = 1 + 4πκ

    Attributes:
        susceptibility: Magnetic susceptibility κ (dimensionless).
        permeability: Magnetic permeability μ (dimensionless).
        is_linear: True if material is linear (constant κ).
    """

    susceptibility: float = 0.0  # κ, dimensionless in CGS
    permeability: float = 1.0  # μ, dimensionless in CGS
    is_linear: bool = True

    def __post_init__(self):
        # For linear materials, μ = 1 + 4πκ
        if self.is_linear:
            self.permeability = 1.0 + 4 * np.pi * self.susceptibility

    @property
    def material_type(self) -> MaterialType:
        """Classify material by susceptibility."""
        return MaterialType.from_susceptibility(self.susceptibility)

    @classmethod
    @maxwell_cite(
        400,
        part=3,
        chapter="Magnetic Constitutive Relation",
        theory_class="maxwell_original",
        description="Create constitutive relation from susceptibility",
    )
    def from_susceptibility(
        cls,
        kappa: float,
    ) -> MagneticConstitutiveRelation:
        """
        Create constitutive relation from susceptibility.

        Art. 400: For linear materials, the susceptibility κ defines
        the material's magnetic response:

            I = κH
            B = (1 + 4πκ)H = μH

        Args:
            kappa: Magnetic susceptibility (dimensionless).

        Returns:
            MagneticConstitutiveRelation object.

        Reference:
            Part III, Art. 400: Linear constitutive relation.
        """
        mu = 1.0 + 4 * np.pi * kappa
        return cls(susceptibility=kappa, permeability=mu, is_linear=True)

    @classmethod
    @maxwell_cite(
        400,
        part=3,
        chapter="Magnetic Constitutive Relation",
        theory_class="maxwell_original",
        description="Create constitutive relation from permeability",
    )
    def from_permeability(
        cls,
        mu: float,
    ) -> MagneticConstitutiveRelation:
        """
        Create constitutive relation from permeability.

        Args:
            mu: Magnetic permeability μ (dimensionless).

        Returns:
            MagneticConstitutiveRelation object.

        Reference:
            Part III, Art. 400: Permeability definition.
        """
        kappa = (mu - 1.0) / (4 * np.pi)
        return cls(susceptibility=kappa, permeability=mu, is_linear=True)

    @classmethod
    @maxwell_cite(
        400,
        part=3,
        chapter="Magnetic Constitutive Relation",
        theory_class="maxwell_original",
        description="Create constitutive relation for vacuum",
    )
    def vacuum(cls) -> MagneticConstitutiveRelation:
        """
        Create constitutive relation for vacuum.

        In vacuum: κ = 0, μ = 1, so B = H.

        Returns:
            MagneticConstitutiveRelation for vacuum.

        Reference:
            Part III, Art. 400: Vacuum case.
        """
        return cls(susceptibility=0.0, permeability=1.0, is_linear=True)


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Calculate B from H and I",
)
def calc_constitutive_relation(
    H_field: np.ndarray,
    magnetization: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic induction B using the constitutive relation.

    Art. 400: The fundamental constitutive relation in CGS is:

        B = H + 4πI

    This relates:
    - H: Magnetic force (gauss) — field from free currents/poles
    - I: Magnetization (emu/cm³) — magnetic moment per unit volume
    - B: Magnetic induction (gauss) — total magnetic field

    Args:
        H_field: Magnetic force H (gauss).
        magnetization: Magnetization I (emu/cm³).

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part III, Art. 400: B = H + 4πI.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    return H_field + 4 * np.pi * magnetization


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Calculate B from H for linear material",
)
def calc_B_linear(
    H_field: np.ndarray,
    susceptibility: float,
) -> np.ndarray:
    """
    Calculate B from H for linear magnetic material.

    Art. 400: For linear materials where I = κH:

        B = μH = (1 + 4πκ)H

    Args:
        H_field: Magnetic force H (gauss).
        susceptibility: Magnetic susceptibility κ (dimensionless).

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part III, Art. 400: Linear material relation.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    mu = 1.0 + 4 * np.pi * susceptibility

    return mu * H_field


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Calculate magnetization from H",
)
def calc_magnetization(
    H_field: np.ndarray,
    susceptibility: float,
) -> np.ndarray:
    """
    Calculate magnetization I from H field.

    Art. 400: For linear materials:

        I = κH

    Args:
        H_field: Magnetic force H (gauss).
        susceptibility: Magnetic susceptibility κ.

    Returns:
        Magnetization I (emu/cm³).

    Reference:
        Part III, Art. 400: I = κH.
    """
    H_field = np.asarray(H_field, dtype=np.float64)

    return susceptibility * H_field


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Extract I from B and H",
)
def extract_magnetization(
    B_field: np.ndarray,
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Extract magnetization I from measured B and H.

    Art. 400: Rearranging the constitutive relation:

        I = (B - H) / 4π

    This allows determination of magnetization from field measurements.

    Args:
        B_field: Magnetic induction B (gauss).
        H_field: Magnetic force H (gauss).

    Returns:
        Magnetization I (emu/cm³).

    Reference:
        Part III, Art. 400: Extracting I.
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    return (B_field - H_field) / (4 * np.pi)


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Calculate susceptibility from measurements",
)
def calc_susceptibility(
    B_field: np.ndarray,
    H_field: np.ndarray,
) -> float:
    """
    Calculate magnetic susceptibility from field measurements.

    Art. 400: For linear materials, the susceptibility can be
    determined from B and H measurements:

        κ = (B - H) / (4πH) = (μ - 1) / 4π

    Args:
        B_field: Magnetic induction B (gauss).
        H_field: Magnetic force H (gauss).

    Returns:
        Magnetic susceptibility κ (dimensionless).

    Reference:
        Part III, Art. 400: Measuring susceptibility.
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    H_mag = np.linalg.norm(H_field)
    if H_mag == 0:
        return 0.0

    # For linear materials, B and H are parallel
    # κ = (|B| - |H|) / (4π|H|)
    B_mag = np.linalg.norm(B_field)

    return (B_mag - H_mag) / (4 * np.pi * H_mag)


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Permeability conversion between CGS and SI",
)
def permeability_cgs_to_si(mu_cgs: float) -> float:
    """
    Convert permeability from CGS to SI units.

    Art. 400: In CGS, permeability is dimensionless. In SI, it has
    units of H/m. The conversion is:

        μ_SI = μ_CGS × μ₀

    where μ₀ = 4π × 10⁻⁷ H/m.

    Args:
        mu_cgs: Permeability in CGS (dimensionless).

    Returns:
        Permeability in SI (H/m).

    Reference:
        Part III, Art. 400: Unit conversion.
    """
    mu_0_si = 4 * np.pi * 1e-7  # H/m
    return mu_cgs * mu_0_si


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Permeability conversion between SI and CGS",
)
def permeability_si_to_cgs(mu_si: float) -> float:
    """
    Convert permeability from SI to CGS units.

    Args:
        mu_si: Permeability in SI (H/m).

    Returns:
        Permeability in CGS (dimensionless).

    Reference:
        Part III, Art. 400: Unit conversion.
    """
    mu_0_si = 4 * np.pi * 1e-7  # H/m
    return mu_si / mu_0_si


@maxwell_cite(
    400,
    part=3,
    chapter="Magnetic Constitutive Relation",
    theory_class="maxwell_original",
    description="Common material susceptibilities",
)
def typical_susceptibilities() -> dict[str, float]:
    """
    Return typical susceptibility values for common materials.

    Art. 400: Maxwell catalogs the magnetic properties of various
    substances. Modern measurements give:

    Returns:
        Dictionary mapping material names to κ values (CGS, 20°C).

    Reference:
        Part III, Art. 400: Material properties.
    """
    return {
        # Diamagnetic (κ < 0)
        "vacuum": 0.0,
        "air": 3.6e-7,  # Very weakly paramagnetic
        "water": -9.0e-6,
        "copper": -9.8e-6,
        "gold": -3.4e-5,
        "silver": -2.6e-5,
        "bismuth": -1.66e-4,  # Strongest diamagnetic element
        "pyrolytic_carbon": -4.5e-4,  # Can levitate in strong field
        # Paramagnetic (κ > 0, small)
        "aluminum": 2.2e-5,
        "platinum": 2.9e-4,
        "tungsten": 6.8e-5,
        "oxygen_gas": 1.9e-6,
        "manganese": 3.7e-4,
        # Ferromagnetic (κ >> 0, nonlinear)
        "iron_pure": 5000,  # Approximate, varies with H
        "iron_electrical": 4000,
        "steel": 1000,
        "nickel": 600,
        "cobalt": 250,
        "mu_metal": 100000,  # High-permeability alloy
        "permalloy": 100000,
    }
