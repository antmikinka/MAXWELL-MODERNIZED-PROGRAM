"""
Induced magnetization — para-, dia-, and ferromagnetism.

Implements the theory of induced magnetization from Part III of Maxwell's Treatise:
- Induced magnetization by external field (Arts. 424-425)
- Magnetic susceptibility I = κH (Art. 426)
- Classification: paramagnetic, diamagnetic, ferromagnetic

When a material is placed in a magnetic field H, it acquires
magnetization I proportional to the field (for linear materials):

    I = κH

where κ is the magnetic susceptibility:
- κ > 0: Paramagnetic (attracted to field)
- κ < 0: Diamagnetic (repelled by field)
- κ >> 0: Ferromagnetic (strongly attracted, nonlinear)

Category: A (maxwell_original) — Maxwell's theory of induced magnetization.

References:
    Part III, Arts. 424-426: Induced magnetization.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


class SubstanceInduction(Enum):
    """
    Classification of magnetic materials by induction type.

    Art. 424-426: Materials are classified by their response to
    an applied magnetic field:

    - Paramagnetic: κ > 0, weakly attracted (Al, Pt, O₂)
    - Diamagnetic: κ < 0, weakly repelled (Cu, Au, H₂O, Bi)
    - Ferromagnetic: κ >> 0, strongly attracted (Fe, Ni, Co)

    In CGS units, typical values:
    - Paramagnetic: κ ~ 10⁻⁵ to 10⁻³
    - Diamagnetic: κ ~ -10⁻⁶ to -10⁻⁴
    - Ferromagnetic: κ ~ 10² to 10⁶ (nonlinear)
    """

    PARAMAGNETIC = "paramagnetic"
    DIAMAGNETIC = "diamagnetic"
    FERROMAGNETIC = "ferromagnetic"
    SUPERPARAMAGNETIC = "superparamagnetic"

    @classmethod
    @maxwell_cite(
        426,
        part=3,
        chapter="Induced Magnetization",
        theory_class="maxwell_original",
        description="Classify by susceptibility",
    )
    def from_susceptibility(cls, kappa: float) -> SubstanceInduction:
        """
        Classify material by its magnetic susceptibility.

        Args:
            kappa: Magnetic susceptibility κ (CGS, dimensionless).

        Returns:
            SubstanceInduction classification.

        Reference:
            Part III, Art. 426: Material classification.
        """
        if kappa > 10:
            return cls.FERROMAGNETIC
        elif kappa > 0:
            return cls.PARAMAGNETIC
        elif kappa < -1e-3:
            return cls.DIAMAGNETIC
        else:
            return cls.DIAMAGNETIC


@dataclass
class MagneticSusceptibility:
    """
    Magnetic susceptibility — ratio of magnetization to field.

    Art. 426: The magnetic susceptibility κ is defined by:

        I = κH

    where:
    - I is magnetization (emu/cm³)
    - H is magnetic field (gauss)
    - κ is dimensionless in CGS

    For linear materials, κ is constant. For ferromagnetic
    materials, κ depends on H (nonlinear).

    Attributes:
        value: Susceptibility κ (dimensionless).
        is_constant: True if κ is independent of H.
    """

    value: float  # dimensionless in CGS
    is_constant: bool = True

    @property
    def material_type(self) -> SubstanceInduction:
        """Classify material by susceptibility."""
        return SubstanceInduction.from_susceptibility(self.value)

    @classmethod
    @maxwell_cite(
        426,
        part=3,
        chapter="Induced Magnetization",
        theory_class="maxwell_original",
        description="Create susceptibility from I and H",
    )
    def from_magnetization_and_field(
        cls,
        magnetization: np.ndarray,
        H_field: np.ndarray,
    ) -> MagneticSusceptibility:
        """
        Determine susceptibility from measured I and H.

        Art. 426: For linear materials:

            κ = |I| / |H|

        Args:
            magnetization: Measured magnetization I (emu/cm³).
            H_field: Applied field H (gauss).

        Returns:
            MagneticSusceptibility object.

        Reference:
            Part III, Art. 426: κ = I/H.
        """
        I_mag = np.linalg.norm(magnetization)
        H_mag = np.linalg.norm(H_field)

        if H_mag == 0:
            return cls(value=0.0, is_constant=True)

        kappa = I_mag / H_mag
        return cls(value=kappa, is_constant=True)


@dataclass
class InducedMagnetization:
    """
    Induced magnetization — magnetization caused by external field.

    Art. 424-425: When a material is placed in a magnetic field,
    it acquires induced magnetization proportional to the field
    (for linear materials):

        I = κH

    The induced magnetization creates its own field, modifying
    the total field inside the material:

        B = H + 4πI = (1 + 4πκ)H = μH

    Attributes:
        susceptibility: Magnetic susceptibility κ.
        applied_field: External applied field H (gauss).
        magnetization: Induced magnetization I (emu/cm³).
    """

    susceptibility: MagneticSusceptibility
    applied_field: np.ndarray  # shape (3,), gauss

    def __post_init__(self):
        self.applied_field = np.asarray(self.applied_field, dtype=np.float64)

        if self.applied_field.shape != (3,):
            raise ValueError("applied_field must be 3D")

    @property
    def magnetization(self) -> np.ndarray:
        """Calculate induced magnetization I = κH."""
        return self.susceptibility.value * self.applied_field

    @property
    def magnetic_induction(self) -> np.ndarray:
        """Calculate resulting B field: B = H + 4πI."""
        return self.applied_field + 4 * np.pi * self.magnetization

    @property
    def permeability(self) -> float:
        """Calculate permeability μ = 1 + 4πκ."""
        return 1.0 + 4 * np.pi * self.susceptibility.value

    @classmethod
    @maxwell_cite(
        424,
        part=3,
        chapter="Induced Magnetization",
        theory_class="maxwell_original",
        description="Create induced magnetization from κ and H",
    )
    def from_susceptibility_and_field(
        cls,
        susceptibility: float,
        applied_field: np.ndarray,
    ) -> InducedMagnetization:
        """
        Create induced magnetization from susceptibility and field.

        Args:
            susceptibility: Magnetic susceptibility κ.
            applied_field: Applied H field (gauss).

        Returns:
            InducedMagnetization object.

        Reference:
            Part III, Art. 424: I = κH.
        """
        return cls(
            susceptibility=MagneticSusceptibility(value=susceptibility),
            applied_field=applied_field,
        )


@maxwell_cite(
    424,
    part=3,
    chapter="Induced Magnetization",
    theory_class="maxwell_original",
    description="Calculate induced magnetization I = κH",
)
def calc_induced_magnetization(
    susceptibility: float,
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate induced magnetization in material.

    Art. 424: When a material with susceptibility κ is placed
    in a magnetic field H, it acquires magnetization:

        I = κH

    Args:
        susceptibility: Magnetic susceptibility κ (dimensionless).
        H_field: Applied magnetic field H (gauss).

    Returns:
        Induced magnetization I (emu/cm³).

    Reference:
        Part III, Art. 424: Induced magnetization formula.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    return susceptibility * H_field


@maxwell_cite(
    425,
    part=3,
    chapter="Induced Magnetization",
    theory_class="maxwell_original",
    description="Calculate B field in magnetic material",
)
def calc_B_in_material(
    H_field: np.ndarray,
    susceptibility: float,
) -> np.ndarray:
    """
    Calculate magnetic induction B inside magnetic material.

    Art. 425: Inside a material with susceptibility κ:

        B = H + 4πI = H + 4πκH = (1 + 4πκ)H = μH

    Args:
        H_field: Applied magnetic field H (gauss).
        susceptibility: Magnetic susceptibility κ.

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part III, Art. 425: B in material.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    mu = 1.0 + 4 * np.pi * susceptibility
    return mu * H_field


@maxwell_cite(
    426,
    part=3,
    chapter="Induced Magnetization",
    theory_class="maxwell_original",
    description="Determine susceptibility from measurements",
)
def determine_susceptibility(
    H_applied: np.ndarray,
    B_measured: np.ndarray,
) -> float:
    """
    Determine susceptibility from field measurements.

    Art. 426: Given applied field H and measured induction B:

        κ = (|B| - |H|) / (4π|H|)

    This assumes linear, isotropic material.

    Args:
        H_applied: Applied field H (gauss).
        B_measured: Measured induction B (gauss).

    Returns:
        Magnetic susceptibility κ.

    Reference:
        Part III, Art. 426: Measuring κ.
    """
    H_applied = np.asarray(H_applied, dtype=np.float64)
    B_measured = np.asarray(B_measured, dtype=np.float64)

    H_mag = np.linalg.norm(H_applied)
    B_mag = np.linalg.norm(B_measured)

    if H_mag == 0:
        return 0.0

    return (B_mag - H_mag) / (4 * np.pi * H_mag)


@maxwell_cite(
    424,
    425,
    426,
    part=3,
    chapter="Induced Magnetization",
    theory_class="maxwell_original",
    description="Force on paramagnetic/diamagnetic body in field gradient",
)
def force_on_induced_magnet(
    susceptibility: float,
    volume: float,
    H_field_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate force on paramagnetic/diamagnetic body in field gradient.

    Art. 424-426: A material with susceptibility κ in a non-uniform
    field experiences a force:

        F = (κ/μ₀) V ∇(H²/2)  (SI)
        F = κ V (H · ∇)H  (CGS)

    For paramagnetic (κ > 0): attracted to strong field
    For diamagnetic (κ < 0): repelled from strong field

    Args:
        susceptibility: Magnetic susceptibility κ.
        volume: Volume of material (cm³).
        H_field_func: Function returning H at a position.
        position: Position of body (cm).
        h: Step size for gradient.

    Returns:
        Force vector F (dyne).

    Reference:
        Part III, Arts. 424-426: Force on induced magnet.
    """
    from typing import Callable

    H_field = np.asarray(H_field_func(position), dtype=np.float64)

    # Compute gradient of H²
    def H_squared(pt: np.ndarray) -> float:
        H = H_field_func(pt)
        return float(np.dot(H, H))

    grad_H2 = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        grad_H2[i] = (H_squared(position + delta) - H_squared(position - delta)) / (
            2 * h
        )

    # F = (κ/2) V ∇(H²) in CGS approximation
    F = 0.5 * susceptibility * volume * grad_H2

    return F


@maxwell_cite(
    426,
    part=3,
    chapter="Induced Magnetization",
    theory_class="maxwell_original",
    description="Typical susceptibility values for common materials",
)
def typical_susceptibility_values() -> dict[str, dict[str, float]]:
    """
    Return typical susceptibility values for common materials.

    Art. 426: Maxwell catalogs the magnetic properties of various
    substances. Modern measurements give these CGS values at 20°C:

    Returns:
        Dictionary mapping material names to properties.

    Reference:
        Part III, Art. 426: Material properties table.
    """
    return {
        # Diamagnetic (κ < 0)
        "vacuum": {"kappa": 0.0, "type": "reference"},
        "air": {"kappa": 3.6e-7, "type": "paramagnetic"},
        "water": {"kappa": -9.0e-6, "type": "diamagnetic"},
        "copper": {"kappa": -9.8e-6, "type": "diamagnetic"},
        "gold": {"kappa": -3.4e-5, "type": "diamagnetic"},
        "silver": {"kappa": -2.6e-5, "type": "diamagnetic"},
        "bismuth": {"kappa": -1.66e-4, "type": "diamagnetic"},
        "pyrolytic_carbon": {"kappa": -4.5e-4, "type": "diamagnetic"},
        "graphite": {"kappa": -8.0e-5, "type": "diamagnetic"},
        # Paramagnetic (κ > 0, small)
        "aluminum": {"kappa": 2.2e-5, "type": "paramagnetic"},
        "platinum": {"kappa": 2.9e-4, "type": "paramagnetic"},
        "tungsten": {"kappa": 6.8e-5, "type": "paramagnetic"},
        "oxygen_gas": {"kappa": 1.9e-6, "type": "paramagnetic"},
        "manganese": {"kappa": 3.7e-4, "type": "paramagnetic"},
        "titanium": {"kappa": 1.8e-4, "type": "paramagnetic"},
        # Ferromagnetic (κ >> 0, nonlinear)
        "iron_pure": {
            "kappa": 5000,
            "type": "ferromagnetic",
            "note": "approximate, varies with H",
        },
        "iron_electrical": {"kappa": 4000, "type": "ferromagnetic"},
        "steel": {"kappa": 1000, "type": "ferromagnetic"},
        "nickel": {"kappa": 600, "type": "ferromagnetic"},
        "cobalt": {"kappa": 250, "type": "ferromagnetic"},
        "mu_metal": {"kappa": 100000, "type": "ferromagnetic"},
        "permalloy": {"kappa": 100000, "type": "ferromagnetic"},
    }
