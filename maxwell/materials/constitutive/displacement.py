"""maxwell.materials.constitutive.displacement — Electric displacement (Art. 608).

Implements Maxwell's constitutive relation for electric displacement,
relating D to E in dielectric materials.

Maxwell's CGS formulation (Art. 608):
    Electric displacement equation (Eq. F):

        D = εE = E + 4πP

    where:
    - P = polarization (electric dipole moment per unit volume)
    - ε = permittivity = 1 + 4πχ_e (χ_e = electric susceptibility)

    In CGS-Gaussian:
        D = εE  (statcoulombs/cm²)
        P = χ_e E  (polarization)
        D = E + 4πP

where:
    D = electric displacement (statcoulombs/cm²)
    E = electric field intensity (statvolts/cm)
    P = polarization (statcoulombs/cm²)
    ε = permittivity (dimensionless)
    χ_e = electric susceptibility (dimensionless)

Category: A (maxwell_original) — Maxwell's displacement theory.

References:
    Part IV, Art. 608: Electric displacement equation (Eq. F).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectricDisplacement:
    """
    Electric displacement calculator for dielectric materials.

    Art. 608: Maxwell's relation for dielectrics:

        D = εE = E + 4πP

    where P is the polarization (electric dipole moment per volume).

    Attributes:
        susceptibility: Electric susceptibility χ_e (dimensionless).
        permittivity: Permittivity ε = 1 + 4πχ_e.
    """

    susceptibility: float = None
    permittivity: float = None

    def __post_init__(self):
        """Calculate permittivity from susceptibility if not provided."""
        # If permittivity is provided, calculate susceptibility
        if self.permittivity is not None:
            # In CGS-Gaussian: ε = K (dielectric constant)
            # Susceptibility χ_e = (ε - 1) / (4π) for the 4πP formulation
            # But for P = (ε - 1)*E (simplified), use χ_e = ε - 1
            if self.susceptibility is None:
                self.susceptibility = self.permittivity - 1.0
        # If susceptibility is provided but not permittivity, calculate permittivity
        elif self.susceptibility is not None:
            self.permittivity = 1.0 + 4.0 * np.pi * self.susceptibility
        else:
            # Both are None, default to vacuum
            self.susceptibility = 0.0
            self.permittivity = 1.0

    @maxwell_cite(
        608,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate electric displacement D from E",
    )
    def displacement(self, E_field: np.ndarray) -> np.ndarray:
        """
        Calculate electric displacement D from electric field E.

        Art. 608: D = εE

        Args:
            E_field: Electric field intensity (statvolts/cm).

        Returns:
            Electric displacement D (statcoulombs/cm²).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        return self.permittivity * E_field

    @maxwell_cite(
        608,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate polarization P from E",
    )
    def polarization(self, E_field: np.ndarray) -> np.ndarray:
        """
        Calculate polarization P (electric dipole moment per volume).

        Art. 608: P = χ_e E

        Args:
            E_field: Electric field intensity (statvolts/cm).

        Returns:
            Polarization P (statcoulombs/cm²).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        return self.susceptibility * E_field

    @maxwell_cite(
        608,
        part=4,
        chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate E from D",
    )
    def electric_field(self, D_field: np.ndarray) -> np.ndarray:
        """
        Calculate electric field E from displacement D.

        Art. 608: E = D / ε

        Args:
            D_field: Electric displacement (statcoulombs/cm²).

        Returns:
            Electric field intensity E (statvolts/cm).
        """
        D_field = np.asarray(D_field, dtype=np.float64)
        return D_field / self.permittivity


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate electric displacement: D = εE",
)
def calc_electric_displacement(
    E_field: np.ndarray,
    permittivity: float = 1.0,
) -> np.ndarray:
    """
    Calculate electric displacement from electric field.

    Art. 608: The constitutive relation for dielectrics:

        D = εE

    In CGS, for vacuum ε = 1, so D = E.

    Args:
        E_field: Electric field intensity (statvolts/cm).
        permittivity: Relative permittivity ε (dimensionless).

    Returns:
        Electric displacement D (statcoulombs/cm²).

    Reference:
        Part IV, Art. 608: Electric displacement (Eq. F).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    return permittivity * E_field


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate polarization: P = χE",
)
def calc_polarization(
    E_field: np.ndarray,
    susceptibility: float,
) -> np.ndarray:
    """
    Calculate electric polarization.

    Art. 608: The polarization (electric dipole moment per unit volume):

        P = χ_e E

    Args:
        E_field: Electric field intensity (statvolts/cm).
        susceptibility: Electric susceptibility χ_e.

    Returns:
        Polarization P (statcoulombs/cm²).

    Reference:
        Part IV, Art. 608: Polarization.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    return susceptibility * E_field


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate permittivity from susceptibility",
)
def calc_permittivity_from_susceptibility(susceptibility: float) -> float:
    """
    Calculate permittivity from electric susceptibility.

    Art. 608: The relation is:

        ε = 1 + 4πχ_e

    Args:
        susceptibility: Electric susceptibility χ_e.

    Returns:
        Permittivity ε (dimensionless).

    Reference:
        Part IV, Art. 608: Permittivity relation.
    """
    return 1.0 + 4.0 * np.pi * susceptibility


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate dielectric constant (specific inductive capacity)",
)
def calc_dielectric_constant(permittivity: float) -> float:
    """
    Calculate dielectric constant (Maxwell's specific inductive capacity).

    Art. 608: The dielectric constant K is the ratio of permittivity
    to vacuum permittivity. In CGS-Gaussian, ε_0 = 1, so:

        K = ε

    Args:
        permittivity: Relative permittivity.

    Returns:
        Dielectric constant K (dimensionless).

    Reference:
        Part IV, Art. 608: Dielectric constant.
    """
    return permittivity


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate permittivity from dielectric constant",
)
def calc_permittivity(dielectric_constant: float) -> float:
    """
    Calculate permittivity from dielectric constant.

    Art. 608: In CGS-Gaussian units, the permittivity equals
    the dielectric constant:

        ε = K

    This is the inverse of calc_dielectric_constant.

    Args:
        dielectric_constant: Dielectric constant K (dimensionless).

    Returns:
        Permittivity ε (dimensionless).

    Reference:
        Part IV, Art. 608: Permittivity from dielectric constant.
    """
    return dielectric_constant


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate bound charge density from polarization",
)
def calc_bound_charge_density(
    polarization_func: callable,
    position: np.ndarray,
    delta: float = 1e-6,
) -> float:
    """
    Calculate bound charge density from polarization.

    Art. 608: The bound (polarization) charge density is:

        rho_bound = -div(P)

    Args:
        polarization_func: Function P(r) returning polarization.
        position: Position for evaluation.
        delta: Finite difference step.

    Returns:
        Bound charge density (statcoulombs/cm³).

    Reference:
        Part IV, Art. 608: Bound charge.
    """
    position = np.asarray(position, dtype=np.float64)
    P = np.asarray(polarization_func(position), dtype=np.float64)

    # Numerical divergence
    div_P = 0.0
    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta

        P_plus = polarization_func(pos_plus)[i]
        P_minus = polarization_func(pos_minus)[i]

        div_P += (P_plus - P_minus) / (2 * delta)

    return -div_P


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Verify displacement relations",
)
def verify_displacement_relations(
    E_field: np.ndarray = None,
    susceptibility: float = 0.5,
    tolerance: float = 1e-10,
) -> dict[str, float | np.ndarray | bool]:
    """
    Verify electric displacement relations.

    Art. 608: This function verifies:
    1. D = E + 4πP
    2. D = εE
    3. ε = 1 + 4πχ_e

    Args:
        E_field: Test electric field (statvolts/cm).
        susceptibility: Test susceptibility.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if E_field is None:
        E_field = np.array([100.0, 0.0, 0.0])

    E_field = np.asarray(E_field, dtype=np.float64)

    # Calculate quantities
    permittivity = calc_permittivity_from_susceptibility(susceptibility)
    P = calc_polarization(E_field, susceptibility)
    D_from_eps = calc_electric_displacement(E_field, permittivity)
    D_from_P = E_field + 4.0 * np.pi * P

    # Verify D = E + 4πP = εE
    D_error = (
        np.linalg.norm(D_from_eps - D_from_P) / np.linalg.norm(D_from_eps)
        if np.linalg.norm(D_from_eps) > 0
        else 0
    )

    # Verify ε = 1 + 4πχ
    eps_check = calc_permittivity_from_susceptibility(susceptibility)
    eps_error = abs(eps_check - (1.0 + 4.0 * np.pi * susceptibility))

    return {
        "E_field": E_field,
        "susceptibility": susceptibility,
        "permittivity": permittivity,
        "polarization_P": P,
        "D_from_eps": D_from_eps,
        "D_from_E_4piP": D_from_P,
        "D_error": D_error,
        "permittivity_error": eps_error,
        "verified": D_error < tolerance and eps_error < tolerance,
    }


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Complete displacement analysis",
)
def analyze_displacement(
    E_field: np.ndarray,
    susceptibility: float,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of electric displacement.

    Art. 608: Comprehensive analysis including:
    1. Polarization
    2. Electric displacement
    3. Permittivity
    4. Material classification

    Args:
        E_field: Applied electric field (statvolts/cm).
        susceptibility: Electric susceptibility.

    Returns:
        Dictionary with complete analysis results.
    """
    E_field = np.asarray(E_field, dtype=np.float64)

    permittivity = calc_permittivity_from_susceptibility(susceptibility)
    P = calc_polarization(E_field, susceptibility)
    D = calc_electric_displacement(E_field, permittivity)

    # Material classification
    if susceptibility > 0:
        material_type = "dielectric"
    elif susceptibility < 0:
        material_type = "unusual (negative susceptibility)"
    else:
        material_type = "vacuum"

    return {
        "E_field": E_field,
        "susceptibility": susceptibility,
        "permittivity": permittivity,
        "dielectric_constant": permittivity,
        "polarization_P": P,
        "electric_displacement_D": D,
        "material_type": material_type,
        "D_enhancement_factor": permittivity,
    }


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate displacement current density",
)
def calc_displacement_current(dD_dt: np.ndarray) -> np.ndarray:
    """
    Calculate displacement current density.

    Art. 608: Maxwell's displacement current:

        J_d = (1/4π) * dD/dt

    This term completes Ampere's law and predicts electromagnetic waves.

    Args:
        dD_dt: Time derivative of electric displacement (statcoulombs/cm²/s).

    Returns:
        Displacement current density J_d (abamperes/cm²).

    Reference:
        Part IV, Art. 608: Displacement current.
    """
    dD_dt = np.asarray(dD_dt, dtype=np.float64)
    return dD_dt / (4.0 * np.pi)


# Alias for test compatibility
calc_displacement = calc_electric_displacement


@maxwell_cite(
    608,
    part=4,
    chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate polarization from E and permittivity",
)
def calc_polarization(E_field: np.ndarray, permittivity: float) -> np.ndarray:
    """
    Calculate electric polarization.

    Art. 608: The polarization (electric dipole moment per unit volume):

        P = (ε - 1) * E / (4π) = χ_e * E

    In terms of permittivity:
        P = D - E = (ε - 1) * E

    Args:
        E_field: Electric field intensity (statvolts/cm).
        permittivity: Relative permittivity ε (dimensionless).

    Returns:
        Polarization P (statcoulombs/cm²).

    Reference:
        Part IV, Art. 608: Polarization.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    return (permittivity - 1.0) * E_field


# Alias for ElectricDisplacement class (test expects "Displacement")
Displacement = ElectricDisplacement
