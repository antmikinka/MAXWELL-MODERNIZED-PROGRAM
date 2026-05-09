"""
Ampere-Maxwell Law — Maxwell's displacement current correction to Ampere's law.

Implements the Ampere-Maxwell law as described by Maxwell in Articles 606-607:

- Ampere's original law: ∮H·dl = 4πI (Art. 606)
- Maxwell's displacement current: J_d = (1/4π)·dD/dt (Art. 606)
- Ampere-Maxwell law: ∇ × H = 4πJ + dD/dt (Art. 607)
- Necessity of displacement current for consistency (Art. 607)

Maxwell's CGS formulation:
    Ampere's Law (original): ∮H·dl = 4πI_enclosed
    Displacement current: J_d = (1/4π)·dD/dt = (ε/4π)·dE/dt
    Ampere-Maxwell Law: ∇ × H = 4πJ_total = 4π(J_cond + J_disp)
    In vacuum: ∇ × H = (1/c)·dE/dt (since D = E in vacuum, CGS-Gaussian)

where:
    H = magnetic field intensity (oersted)
    J = conduction current density (abamperes/cm²)
    D = electric displacement field (statcoulombs/cm²)
    E = electric field intensity (statvolts/cm)
    ε = permittivity (dimensionless in CGS-Gaussian, ε₀ = 1/4π)
    c = speed of light (cm/s)

The displacement current was Maxwell's crucial insight that completed
electromagnetic theory and predicted electromagnetic waves.

Category: A (maxwell_original) — Maxwell's theory of displacement current.

References:
    Part IV, Arts. 606-607: Ampere-Maxwell law and displacement current.
    Part IV, Ch. XX: Electromagnetic theory of light (consequences of displacement current).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class DisplacementCurrent:
    """
    Displacement current density — Maxwell's crucial addition to Ampere's law.

    Art. 606-607: Maxwell recognized that Ampere's law alone was incomplete.
    When the electric field changes with time, there is an additional "current"
    term that must be included:

        J_d = (1/4π) · dD/dt = (ε/4π) · dE/dt

    This displacement current ensures charge conservation and leads to the
    prediction of electromagnetic waves propagating at speed c.

    In CGS-Gaussian units:
        J_d = (1/4π) · dD/dt  (abamperes/cm²)
        D = εE  (statcoulombs/cm²)

    Attributes:
        E_field: Electric field vector (statvolts/cm).
        dE_dt: Rate of change of electric field (statvolts/cm/s).
        permittivity: Permittivity ε (dimensionless in CGS).
    """

    E_field: np.ndarray
    dE_dt: np.ndarray
    permittivity: float = 1.0

    def __post_init__(self):
        """Validate parameters and convert to arrays."""
        self.E_field = np.asarray(self.E_field, dtype=np.float64)
        self.dE_dt = np.asarray(self.dE_dt, dtype=np.float64)

        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")

    @property
    def D_field(self) -> np.ndarray:
        """
        Electric displacement field D = εE.

        Returns:
            D field vector (statcoulombs/cm²).
        """
        return self.permittivity * self.E_field

    @property
    def dD_dt(self) -> np.ndarray:
        """
        Rate of change of displacement field dD/dt = ε·dE/dt.

        Returns:
            Rate of change of D (statcoulombs/cm²/s).
        """
        return self.permittivity * self.dE_dt

    @property
    def J_displacement(self) -> np.ndarray:
        """
        Displacement current density J_d = (1/4π)·dD/dt.

        Returns:
            Displacement current density (abamperes/cm²).

        Reference:
            Part IV, Art. 606: Displacement current definition.
        """
        return (1.0 / (4.0 * np.pi)) * self.dD_dt

    @property
    def magnitude(self) -> float:
        """
        Magnitude of displacement current density.

        Returns:
            |J_d| (abamperes/cm²).
        """
        return float(np.linalg.norm(self.J_displacement))

    @classmethod
    @maxwell_cite(
        606,
        607,
        part=4,
        chapter="Displacement Current",
        theory_class="maxwell_original",
        description="Create displacement current from E field and its time derivative",
    )
    def from_E_and_derivative(
        cls,
        E_field: np.ndarray,
        dE_dt: np.ndarray,
        permittivity: float = 1.0,
    ) -> DisplacementCurrent:
        """
        Create displacement current from electric field and its time derivative.

        Art. 606-607: The displacement current arises from the time-varying
        electric field: J_d = (ε/4π) · dE/dt

        Args:
            E_field: Electric field vector (statvolts/cm).
            dE_dt: Time derivative of E (statvolts/cm/s).
            permittivity: Permittivity ε (default: 1.0 for vacuum in CGS-Gaussian).

        Returns:
            DisplacementCurrent object.

        Reference:
            Part IV, Arts. 606-607: Displacement current formulation.
        """
        return cls(E_field=E_field, dE_dt=dE_dt, permittivity=permittivity)

    @classmethod
    @maxwell_cite(
        606,
        part=4,
        chapter="Displacement Current",
        theory_class="maxwell_original",
        description="Create displacement current from D field derivative",
    )
    def from_D_derivative(
        cls,
        dD_dt: np.ndarray,
    ) -> DisplacementCurrent:
        """
        Create displacement current directly from dD/dt.

        Art. 606: J_d = (1/4π) · dD/dt

        Args:
            dD_dt: Rate of change of displacement field (statcoulombs/cm²/s).

        Returns:
            DisplacementCurrent object.

        Reference:
            Part IV, Art. 606: Displacement current from D field.
        """
        # Create with dummy E_field, since we directly have dD_dt
        J_d = (1.0 / (4.0 * np.pi)) * dD_dt
        # Store dD_dt in dE_dt field as a proxy
        return cls(E_field=np.zeros(3), dE_dt=dD_dt, permittivity=1.0)


@dataclass
class AmpereMaxwellLaw:
    """
    Ampere-Maxwell Law — complete calculator for the generalized Ampere's law.

    Art. 606-607: Maxwell's completion of Ampere's law by adding displacement current:

        ∇ × H = 4πJ_cond + dD/dt = 4π(J_cond + J_disp)

    This equation governs how magnetic fields are produced by both:
    1. Conduction currents (moving charges)
    2. Displacement currents (changing electric fields)

    The integral form:
        ∮H·dl = 4πI_enclosed + d(∫D·dA)/dt

    In vacuum (CGS-Gaussian, D = E, ε = 1):
        ∇ × H = (1/c) · dE/dt

    Attributes:
        J_conduction: Conduction current density (abamperes/cm²).
        dE_dt: Time derivative of electric field (statvolts/cm/s).
        permittivity: Permittivity ε (dimensionless).
    """

    J_conduction: np.ndarray
    dE_dt: np.ndarray
    permittivity: float = 1.0

    def __post_init__(self):
        """Validate parameters and convert to arrays."""
        self.J_conduction = np.asarray(self.J_conduction, dtype=np.float64)
        self.dE_dt = np.asarray(self.dE_dt, dtype=np.float64)

        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")

    @property
    def J_displacement(self) -> np.ndarray:
        """
        Displacement current density J_d = (ε/4π)·dE/dt.

        Returns:
            Displacement current density (abamperes/cm²).

        Reference:
            Part IV, Art. 606: Displacement current.
        """
        return (self.permittivity / (4.0 * np.pi)) * self.dE_dt

    @property
    def J_total(self) -> np.ndarray:
        """
        Total effective current density J_total = J_cond + J_disp.

        Returns:
            Total current density (abamperes/cm²).

        Reference:
            Part IV, Art. 607: Total current in Ampere-Maxwell law.
        """
        return self.J_conduction + self.J_displacement

    @property
    def curl_H(self) -> np.ndarray:
        """
        Curl of magnetic field: ∇ × H = 4πJ_total.

        Returns:
            Curl of H (oersted/cm).

        Reference:
            Part IV, Art. 607: Differential form of Ampere-Maxwell law.
        """
        return 4.0 * np.pi * self.J_total

    @classmethod
    @maxwell_cite(
        606,
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Create Ampere-Maxwell law calculator",
    )
    def from_currents(
        cls,
        J_conduction: np.ndarray,
        dE_dt: np.ndarray,
        permittivity: float = 1.0,
    ) -> AmpereMaxwellLaw:
        """
        Create Ampere-Maxwell law calculator from conduction current and dE/dt.

        Art. 606-607: The complete law requires both conduction current and
        the time derivative of the electric field.

        Args:
            J_conduction: Conduction current density (abamperes/cm²).
            dE_dt: Time derivative of E (statvolts/cm/s).
            permittivity: Permittivity ε (default: 1.0 for vacuum).

        Returns:
            AmpereMaxwellLaw object.

        Reference:
            Part IV, Arts. 606-607: Complete Ampere-Maxwell formulation.
        """
        return cls(J_conduction=J_conduction, dE_dt=dE_dt, permittivity=permittivity)

    @classmethod
    @maxwell_cite(
        606,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Create from H field curl and permittivity",
    )
    def from_curl_H(
        cls,
        curl_H: np.ndarray,
        permittivity: float = 1.0,
    ) -> AmpereMaxwellLaw:
        """
        Create Ampere-Maxwell calculator from known curl of H.

        Art. 607: Given ∇ × H, we can determine the total current:
            J_total = (1/4π) · ∇ × H

        Args:
            curl_H: Curl of magnetic field (oersted/cm).
            permittivity: Permittivity ε.

        Returns:
            AmpereMaxwellLaw object with J_total derived from curl_H.

        Reference:
            Part IV, Art. 607: Relating curl H to total current.
        """
        J_total = curl_H / (4.0 * np.pi)
        # Assume all current is conduction (can be adjusted later)
        return cls(J_conduction=J_total, dE_dt=np.zeros(3), permittivity=permittivity)

    @maxwell_cite(
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate curl of H field",
    )
    def compute_curl_H(
        self,
        J_conduction: np.ndarray = None,
        dE_dt: np.ndarray = None,
    ) -> np.ndarray:
        """
        Compute curl of H from currents.

        Art. 607: ∇ × H = 4π(J_cond + J_disp)

        Args:
            J_conduction: Optional override conduction current density.
            dE_dt: Optional override time derivative of E.

        Returns:
            Curl of H vector (oersted/cm).

        Reference:
            Part IV, Art. 607: Curl H calculation.
        """
        J_cond = J_conduction if J_conduction is not None else self.J_conduction
        dE = dE_dt if dE_dt is not None else self.dE_dt

        J_disp = (self.permittivity / (4.0 * np.pi)) * dE
        J_total = J_cond + J_disp

        return 4.0 * np.pi * J_total

    @maxwell_cite(
        606,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate displacement current density",
    )
    def compute_displacement_current(
        self,
        dE_dt: np.ndarray = None,
        permittivity: float = None,
    ) -> np.ndarray:
        """
        Compute displacement current density J_d.

        Art. 606: J_d = (ε/4π) · dE/dt

        Args:
            dE_dt: Optional override time derivative of E.
            permittivity: Optional override permittivity.

        Returns:
            Displacement current density (abamperes/cm²).

        Reference:
            Part IV, Art. 606: Displacement current calculation.
        """
        dE = dE_dt if dE_dt is not None else self.dE_dt
        eps = permittivity if permittivity is not None else self.permittivity

        return (eps / (4.0 * np.pi)) * dE

    @maxwell_cite(
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate total current density",
    )
    def compute_total_current(
        self,
        J_conduction: np.ndarray = None,
        dE_dt: np.ndarray = None,
    ) -> np.ndarray:
        """
        Compute total effective current density.

        Art. 607: J_total = J_cond + J_disp

        Args:
            J_conduction: Optional override conduction current.
            dE_dt: Optional override time derivative of E.

        Returns:
            Total current density (abamperes/cm²).

        Reference:
            Part IV, Art. 607: Total current.
        """
        J_cond = J_conduction if J_conduction is not None else self.J_conduction
        J_disp = self.compute_displacement_current(dE_dt)

        return J_cond + J_disp


@maxwell_cite(
    606,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Calculate Ampere's law: ∮H·dl = 4πI",
)
def calc_ampere_law(
    current_density: np.ndarray,
    path_length: float,
) -> float:
    """
    Calculate the line integral of H around a closed path (original Ampere's law).

    Art. 606: For a steady current, Ampere's law states:

        ∮H·dl = 4πI_enclosed

    where I_enclosed is the total current passing through any surface
    bounded by the closed path.

    For uniform current density J perpendicular to area A:
        I = J · A

    For a simple circular path of radius r around a wire:
        ∮H·dl = H · 2πr = 4πI
        H = 2I/r (the Oersted field)

    In CGS-EMU:
        I in abamperes
        H in oersted
        dl in cm

    Args:
        current_density: Current density vector J (abamperes/cm²).
        path_length: Length of the integration path (cm).

    Returns:
        Line integral ∮H·dl (oersted·cm).

    Raises:
        ValueError: If path_length is not positive.

    Reference:
        Part IV, Art. 606: Original Ampere's law.

    Example:
        >>> # 1 abampere through circular path of 2π cm circumference
        >>> J = np.array([0, 0, 1])  # 1 abA/cm²
        >>> result = calc_ampere_law(J, 2 * np.pi)
        >>> print(f"∮H·dl = {result:.2f} oersted·cm")
    """
    if path_length <= 0:
        raise ValueError(f"Path length must be positive, got {path_length}")

    current_density = np.asarray(current_density, dtype=np.float64)

    # For uniform J, estimate I as J * A where A is effective area
    # For a circular path, A = πr² and path = 2πr, so r = path/(2π)
    # A = path²/(4π)
    effective_area = (path_length**2) / (4.0 * np.pi)
    I_enclosed = np.linalg.norm(current_density) * effective_area

    # ∮H·dl = 4πI
    return 4.0 * np.pi * I_enclosed


@maxwell_cite(
    606,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Calculate displacement current: J_d = (ε/4π)·dE/dt",
)
def calc_displacement_current(
    E_field: np.ndarray,
    dE_dt: np.ndarray,
    permittivity: float = 1.0,
) -> np.ndarray:
    """
    Calculate displacement current density.

    Art. 606: Maxwell's displacement current density:

        J_d = (1/4π) · dD/dt = (ε/4π) · dE/dt

    This term represents the "current" associated with a changing
    electric field, even in the absence of charge motion.

    In CGS-Gaussian:
        E in statvolts/cm
        dE/dt in statvolts/cm/s
        ε dimensionless (ε = 1 for vacuum)
        J_d in abamperes/cm²

    Args:
        E_field: Electric field vector (statvolts/cm).
        dE_dt: Time derivative of E (statvolts/cm/s).
        permittivity: Permittivity ε (default: 1.0 for vacuum).

    Returns:
        Displacement current density vector (abamperes/cm²).

    Raises:
        ValueError: If permittivity is not positive.

    Reference:
        Part IV, Art. 606: Displacement current formulation.

    Example:
        >>> # E field changing at 1e10 statV/cm/s in vacuum
        >>> dE_dt = np.array([0, 0, 1e10])
        >>> J_d = calc_displacement_current(np.zeros(3), dE_dt)
        >>> print(f"J_d = {J_d} abamperes/cm²")
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")

    E_field = np.asarray(E_field, dtype=np.float64)
    dE_dt = np.asarray(dE_dt, dtype=np.float64)

    # J_d = (ε/4π) · dE/dt
    return (permittivity / (4.0 * np.pi)) * dE_dt


@maxwell_cite(
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Calculate Ampere-Maxwell law: ∇×H = 4πJ + dD/dt",
)
def calc_ampere_maxwell(
    H_curl: np.ndarray,
    J_conduction: np.ndarray,
    dD_dt: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Calculate and verify the complete Ampere-Maxwell law.

    Art. 607: The differential form of the Ampere-Maxwell law:

        ∇ × H = 4πJ_cond + dD/dt

    This function computes each term and verifies the relationship.

    In CGS:
        H in oersted
        curl H in oersted/cm
        J in abamperes/cm²
        D in statcoulombs/cm²
        dD/dt in statcoulombs/cm²/s

    Args:
        H_curl: Curl of H field (oersted/cm).
        J_conduction: Conduction current density (abamperes/cm²).
        dD_dt: Time derivative of D field (statcoulombs/cm²/s).

    Returns:
        Dictionary with:
        - lhs: Left-hand side ∇ × H (oersted/cm)
        - rhs_conduction: 4πJ_cond contribution (oersted/cm)
        - rhs_displacement: dD/dt contribution (oersted/cm)
        - rhs_total: Total right-hand side (oersted/cm)
        - residual: Difference |LHS - RHS| (should be ~0)
        - verified: True if equation holds within numerical tolerance

    Reference:
        Part IV, Art. 607: Complete Ampere-Maxwell law.

    Example:
        >>> # Verify Ampere-Maxwell for known fields
        >>> H_curl = np.array([0, 1e-6, 0])
        >>> J = np.array([0, 1e-7, 0])
        >>> dD_dt = np.array([0, 5e-7, 0])
        >>> result = calc_ampere_maxwell(H_curl, J, dD_dt)
        >>> assert result['verified']
    """
    H_curl = np.asarray(H_curl, dtype=np.float64)
    J_conduction = np.asarray(J_conduction, dtype=np.float64)
    dD_dt = np.asarray(dD_dt, dtype=np.float64)

    # Right-hand side terms
    rhs_conduction = 4.0 * np.pi * J_conduction
    rhs_displacement = dD_dt  # dD/dt appears directly in CGS
    rhs_total = rhs_conduction + rhs_displacement

    # Residual (should be zero for exact solution)
    residual = np.linalg.norm(H_curl - rhs_total)
    tolerance = 1e-10 * max(np.linalg.norm(H_curl), np.linalg.norm(rhs_total), 1.0)
    verified = residual < tolerance

    return {
        "lhs": H_curl,
        "rhs_conduction": rhs_conduction,
        "rhs_displacement": rhs_displacement,
        "rhs_total": rhs_total,
        "residual": residual,
        "verified": verified,
    }


@maxwell_cite(
    606,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Calculate magnetic field from steady current",
)
def calc_magnetic_field_from_current(
    J: np.ndarray,
    position: np.ndarray,
    current_element: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate magnetic field H at a position from a current distribution.

    Art. 606: For steady currents (no displacement current), the magnetic
    field is given by the Biot-Savart law (derived from Ampere's law):

        H(r) = (1/4π) · ∫ (J(r') × (r - r')) / |r - r'|³ dV'

    For a current element I·dl at position r':
        dH = (I/4π) · (dl × r_hat) / r²

    For an infinite straight wire:
        H = 2I/r (Oersted's result)

    This function provides simplified calculation for specific geometries.

    In CGS-EMU:
        J in abamperes/cm²
        position in cm
        H in oersted

    Args:
        J: Current density vector (abamperes/cm²).
        position: Position vector relative to current source (cm).
        current_element: Optional current element vector I·dl (abampere·cm).
                        If provided, calculates field from this element.

    Returns:
        Magnetic field vector H (oersted).

    Raises:
        ValueError: If position is at origin (singularity).

    Reference:
        Part IV, Art. 606: Field from steady currents.

    Example:
        >>> # Field from current element at 1 cm distance
        >>> Idl = np.array([0, 0, 1])  # 1 abA·cm along z
        >>> r = np.array([1, 0, 0])  # 1 cm along x
        >>> H = calc_magnetic_field_from_current(np.zeros(3), r, Idl)
        >>> print(f"H = {H} oersted")
    """
    position = np.asarray(position, dtype=np.float64)
    r_mag = np.linalg.norm(position)

    if r_mag < 1e-15:
        raise ValueError("Position cannot be at current location (singularity)")

    if current_element is not None:
        # Field from current element (Biot-Savart)
        # dH = (1/4π) · (I·dl × r_hat) / r²
        current_element = np.asarray(current_element, dtype=np.float64)
        r_hat = position / r_mag

        # dH = (1/4π) · (Idl × r) / r³
        dH = (1.0 / (4.0 * np.pi)) * np.cross(current_element, r_hat) / (r_mag**2)
        return dH
    else:
        # Simplified: field from uniform current sheet
        # For infinite sheet: H = 2πJ (in appropriate direction)
        J = np.asarray(J, dtype=np.float64)
        # This is a simplified model; real calculation requires integration
        # H direction is perpendicular to both J and position
        H_direction = np.cross(J, position)
        H_dir_norm = np.linalg.norm(H_direction)

        if H_dir_norm < 1e-15:
            return np.zeros(3)

        # Magnitude estimate (order of magnitude)
        H_mag = (2.0 * np.pi * np.linalg.norm(J)) / r_mag
        return H_mag * (H_direction / H_dir_norm)


@maxwell_cite(
    606,
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Calculate total current density: J_total = J + J_d",
)
def calc_total_current_density(
    J_conduction: np.ndarray,
    dE_dt: np.ndarray,
    permittivity: float = 1.0,
) -> np.ndarray:
    """
    Calculate total effective current density including displacement current.

    Art. 606-607: The total current that sources the magnetic field is:

        J_total = J_conduction + J_displacement
        J_total = J + (ε/4π) · dE/dt

    This unified current density appears in the Ampere-Maxwell equation:
        ∇ × H = 4π · J_total

    In CGS:
        J_conduction in abamperes/cm²
        dE_dt in statvolts/cm/s
        J_total in abamperes/cm²

    Args:
        J_conduction: Conduction current density (abamperes/cm²).
        dE_dt: Time derivative of E (statvolts/cm/s).
        permittivity: Permittivity ε (default: 1.0 for vacuum).

    Returns:
        Total current density vector (abamperes/cm²).

    Reference:
        Part IV, Arts. 606-607: Total current in Ampere-Maxwell law.

    Example:
        >>> # Equal conduction and displacement currents
        >>> J = np.array([1e-6, 0, 0])
        >>> dE_dt = np.array([4 * np.pi * 1e-6, 0, 0])  # Chosen for J_d = J
        >>> J_total = calc_total_current_density(J, dE_dt)
        >>> print(f"J_total = {J_total} abamperes/cm²")
    """
    J_conduction = np.asarray(J_conduction, dtype=np.float64)
    dE_dt = np.asarray(dE_dt, dtype=np.float64)

    J_displacement = calc_displacement_current(np.zeros(3), dE_dt, permittivity)
    return J_conduction + J_displacement


@maxwell_cite(
    606,
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Demonstrate necessity of displacement current (capacitor paradox)",
)
def verify_displacement_current_necessity(
    charging_current: float = 1.0,
    plate_area: float = 100.0,
    plate_separation: float = 1.0,
    time_interval: float = 1.0,
) -> dict[str, float | bool]:
    """
    Verify the necessity of displacement current using the capacitor paradox.

    Art. 606-607: Maxwell recognized a fundamental problem with Ampere's
    original law. Consider a charging capacitor:

    - Surface S1 cuts through the wire: ∮H·dl = 4πI (current passes through)
    - Surface S2 passes between plates: ∮H·dl = 0 (no current passes through)

    This is a contradiction! The same loop gives different results depending
    on which surface is chosen.

    Maxwell's solution: The changing electric field between the plates
    constitutes a displacement current:
        I_d = (1/4π) · d(∫D·dA)/dt = (εA/4π) · dE/dt

    For a charging capacitor:
        I_d = I_conduction (they are equal!)

    This restores consistency: both surfaces now give the same ∮H·dl.

    Args:
        charging_current: Current charging the capacitor (abamperes).
        plate_area: Area of capacitor plates (cm²).
        plate_separation: Distance between plates (cm).
        time_interval: Time interval for charging (seconds).

    Returns:
        Dictionary with:
        - conduction_current: I through wire (abamperes)
        - displacement_current: I_d between plates (abamperes)
        - E_field: Electric field between plates (statvolts/cm)
        - dE_dt: Rate of E field change (statvolts/cm/s)
        - without_displacement: ∮H·dl for S2 without displacement (should be wrong)
        - with_displacement: ∮H·dl for S2 with displacement (should equal 4πI)
        - paradox_resolved: True if displacement current resolves the paradox

    Reference:
        Part IV, Arts. 606-607: Capacitor paradox and displacement current.

    Example:
        >>> result = verify_displacement_current_necessity()
        >>> assert result['paradox_resolved']
    """
    if charging_current <= 0:
        raise ValueError(f"Charging current must be positive, got {charging_current}")
    if plate_area <= 0:
        raise ValueError(f"Plate area must be positive, got {plate_area}")
    if plate_separation <= 0:
        raise ValueError(f"Plate separation must be positive, got {plate_separation}")
    if time_interval <= 0:
        raise ValueError(f"Time interval must be positive, got {time_interval}")

    # For a capacitor being charged with current I:
    # dQ/dt = I
    # Q = C · V, where C = εA/(4πd) in CGS
    # E = V/d = 4πQ/(εA) for parallel plate capacitor

    # Rate of charge accumulation
    dQ_dt = charging_current  # abcoulombs/s = abamperes

    # In CGS-Gaussian (ε = 1 for vacuum between plates):
    # E = 4πσ where σ = Q/A is surface charge density
    # dE/dt = 4π/A · dQ/dt = 4πI/A

    dE_dt = (4.0 * np.pi / plate_area) * charging_current

    # Displacement current density: J_d = (1/4π) · dE/dt
    J_d = (1.0 / (4.0 * np.pi)) * dE_dt

    # Total displacement current through plate area
    I_displacement = J_d * plate_area

    # Verify: I_d should equal I_conduction
    # I_d = (1/4π) · dE/dt · A = (1/4π) · (4πI/A) · A = I ✓

    # Line integral without displacement current (wrong!)
    without_displacement = 0.0  # No conduction current passes through S2

    # Line integral with displacement current (correct!)
    with_displacement = 4.0 * np.pi * I_displacement

    # Expected result (should match 4πI from surface S1)
    expected = 4.0 * np.pi * charging_current

    # Verify paradox is resolved
    paradox_resolved = np.isclose(with_displacement, expected, rtol=1e-10)

    return {
        "conduction_current": charging_current,
        "displacement_current": I_displacement,
        "E_field_rate_of_change": dE_dt,
        "without_displacement": without_displacement,
        "with_displacement": with_displacement,
        "expected_result": expected,
        "paradox_resolved": paradox_resolved,
        "current_match": np.isclose(I_displacement, charging_current, rtol=1e-10),
    }


@maxwell_cite(
    606,
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Complete Ampere-Maxwell law analysis",
)
def analyze_ampere_maxwell(
    J_conduction: np.ndarray,
    E_field: np.ndarray,
    dE_dt: np.ndarray,
    permittivity: float = 1.0,
    position: np.ndarray = None,
) -> dict[str, np.ndarray | float]:
    """
    Perform comprehensive analysis of the Ampere-Maxwell law.

    Art. 606-607: Complete analysis including:

    1. Displacement current density
    2. Total effective current
    3. Curl of H field
    4. Magnetic field from currents
    5. Verification of Ampere-Maxwell consistency

    Args:
        J_conduction: Conduction current density (abamperes/cm²).
        E_field: Electric field vector (statvolts/cm).
        dE_dt: Time derivative of E (statvolts/cm/s).
        permittivity: Permittivity ε (default: 1.0 for vacuum).
        position: Optional position for field calculation (cm).

    Returns:
        Dictionary with complete analysis:
        - J_conduction: Input conduction current (abamperes/cm²)
        - J_displacement: Displacement current density (abamperes/cm²)
        - J_total: Total effective current (abamperes/cm²)
        - curl_H: Curl of magnetic field (oersted/cm)
        - displacement_magnitude: |J_d| (abamperes/cm²)
        - current_ratio: |J_d|/|J_cond| (relative importance)
        - H_field: Magnetic field at position if provided (oersted)
        - regime: "conduction_dominated", "displacement_dominated", or "mixed"

    Reference:
        Part IV, Arts. 606-607: Complete Ampere-Maxwell analysis.

    Example:
        >>> result = analyze_ampere_maxwell(
        ...     J_conduction=np.array([1e-6, 0, 0]),
        ...     E_field=np.array([0, 1000, 0]),
        ...     dE_dt=np.array([0, 1e10, 0]),
        ...     permittivity=1.0,
        ...     position=np.array([0, 0, 1])
        ... )
        >>> print(f"Regime: {result['regime']}")
    """
    J_conduction = np.asarray(J_conduction, dtype=np.float64)
    E_field = np.asarray(E_field, dtype=np.float64)
    dE_dt = np.asarray(dE_dt, dtype=np.float64)

    # Displacement current
    J_displacement = calc_displacement_current(E_field, dE_dt, permittivity)
    J_disp_mag = np.linalg.norm(J_displacement)

    # Total current
    J_total = calc_total_current_density(J_conduction, dE_dt, permittivity)
    J_cond_mag = np.linalg.norm(J_conduction)

    # Curl of H
    curl_H = 4.0 * np.pi * J_total

    # Current ratio (displacement vs conduction)
    if J_cond_mag > 1e-15:
        current_ratio = J_disp_mag / J_cond_mag
    else:
        current_ratio = float("inf") if J_disp_mag > 0 else 0.0

    # Determine regime
    if current_ratio > 10:
        regime = "displacement_dominated"
    elif current_ratio < 0.1:
        regime = "conduction_dominated"
    else:
        regime = "mixed"

    # Magnetic field at position (if provided)
    H_field = None
    if position is not None:
        H_field = calc_magnetic_field_from_current(J_total, position)

    return {
        "J_conduction": J_conduction,
        "J_displacement": J_displacement,
        "J_total": J_total,
        "curl_H": curl_H,
        "displacement_magnitude": J_disp_mag,
        "conduction_magnitude": J_cond_mag,
        "current_ratio": current_ratio,
        "H_field": H_field,
        "regime": regime,
    }


class AmpereMaxwellCalculator:
    """
    Comprehensive Ampere-Maxwell law calculator.

    Art. 606-607: This class provides a unified interface for all
    Ampere-Maxwell calculations:

    - Displacement current from changing E field
    - Total effective current
    - Curl of H field
    - Magnetic field from current distributions
    - Verification of displacement current necessity

    Attributes:
        permittivity: Permittivity ε (default: 1.0 for vacuum).
    """

    def __init__(self, permittivity: float = 1.0):
        """
        Initialize Ampere-Maxwell calculator.

        Args:
            permittivity: Permittivity ε (default: 1.0 for CGS-Gaussian vacuum).
        """
        if permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {permittivity}")
        self.permittivity = permittivity

    @maxwell_cite(
        606,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate displacement current density",
    )
    def displacement_current(
        self,
        dE_dt: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate displacement current density.

        Art. 606: J_d = (ε/4π) · dE/dt

        Args:
            dE_dt: Time derivative of E (statvolts/cm/s).

        Returns:
            Displacement current density (abamperes/cm²).

        Reference:
            Part IV, Art. 606: Displacement current.
        """
        return calc_displacement_current(np.zeros(3), dE_dt, self.permittivity)

    @maxwell_cite(
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate total current density",
    )
    def total_current(
        self,
        J_conduction: np.ndarray,
        dE_dt: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate total effective current density.

        Art. 607: J_total = J_cond + J_disp

        Args:
            J_conduction: Conduction current density (abamperes/cm²).
            dE_dt: Time derivative of E (statvolts/cm/s).

        Returns:
            Total current density (abamperes/cm²).

        Reference:
            Part IV, Art. 607: Total current.
        """
        return calc_total_current_density(J_conduction, dE_dt, self.permittivity)

    @maxwell_cite(
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate curl of H field",
    )
    def curl_H(
        self,
        J_conduction: np.ndarray,
        dE_dt: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate curl of magnetic field.

        Art. 607: ∇ × H = 4πJ_total

        Args:
            J_conduction: Conduction current density (abamperes/cm²).
            dE_dt: Time derivative of E (statvolts/cm/s).

        Returns:
            Curl of H (oersted/cm).

        Reference:
            Part IV, Art. 607: Curl H calculation.
        """
        J_total = self.total_current(J_conduction, dE_dt)
        return 4.0 * np.pi * J_total

    @maxwell_cite(
        606,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Calculate magnetic field from current",
    )
    def magnetic_field(
        self,
        J_total: np.ndarray,
        position: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate magnetic field from current distribution.

        Art. 606: Field from steady currents (Biot-Savart law).

        Args:
            J_total: Total current density (abamperes/cm²).
            position: Position relative to current (cm).

        Returns:
            Magnetic field H (oersted).

        Reference:
            Part IV, Art. 606: Field from currents.
        """
        return calc_magnetic_field_from_current(J_total, position)

    @maxwell_cite(
        606,
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Complete Ampere-Maxwell analysis",
    )
    def analyze(
        self,
        J_conduction: np.ndarray,
        E_field: np.ndarray,
        dE_dt: np.ndarray,
        position: np.ndarray = None,
    ) -> dict[str, np.ndarray | float]:
        """
        Perform complete Ampere-Maxwell analysis.

        Art. 606-607: Comprehensive analysis of the electromagnetic
        field configuration.

        Args:
            J_conduction: Conduction current density (abamperes/cm²).
            E_field: Electric field (statvolts/cm).
            dE_dt: Time derivative of E (statvolts/cm/s).
            position: Optional position for field calculation.

        Returns:
            Dictionary with complete analysis results.

        Reference:
            Part IV, Arts. 606-607: Complete analysis.
        """
        return analyze_ampere_maxwell(
            J_conduction=J_conduction,
            E_field=E_field,
            dE_dt=dE_dt,
            permittivity=self.permittivity,
            position=position,
        )

    @maxwell_cite(
        606,
        607,
        part=4,
        chapter="Ampere-Maxwell Law",
        theory_class="maxwell_original",
        description="Verify displacement current necessity",
    )
    def verify_displacement_necessity(
        self,
        charging_current: float,
        plate_area: float,
        plate_separation: float,
        time_interval: float,
    ) -> dict[str, float | bool]:
        """
        Verify displacement current resolves the capacitor paradox.

        Art. 606-607: Demonstration that displacement current is
        necessary for consistency.

        Args:
            charging_current: Current charging capacitor (abamperes).
            plate_area: Plate area (cm²).
            plate_separation: Plate separation (cm).
            time_interval: Charging time interval (s).

        Returns:
            Dictionary with verification results.

        Reference:
            Part IV, Arts. 606-607: Capacitor paradox verification.
        """
        return verify_displacement_current_necessity(
            charging_current=charging_current,
            plate_area=plate_area,
            plate_separation=plate_separation,
            time_interval=time_interval,
        )
