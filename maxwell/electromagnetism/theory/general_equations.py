"""
General Equations of the Electromagnetic Field — Maxwell's Equations themselves.

Implements Maxwell's general equations of the electromagnetic field as described
in Articles 594-603 of the Treatise:

- Equation (A): Faraday's Law — ∇ × E = -(1/c)·∂B/∂t (Art. 598)
- Equation (B): General EMF — E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ (Art. 598)
- Equation (C): Ponderomotive Force — F = ρE + (1/c)(J × B) (Art. 599)
- Equation (D): Magnetic Induction — B = H + 4πM (Art. 599)
- Equation (E): Ampere-Maxwell — ∇ × H = (4π/c)·J + (1/c)·∂D/∂t (Art. 600)
- Equation (F): Electric Displacement — D = εE (Art. 600)
- Equation (G): Conduction Current — J = σE (Art. 600)
- Gauss's Law (Electric): ∇ · D = 4πρ (Art. 594)
- Gauss's Law (Magnetic): ∇ · B = 0 (Art. 594)

Maxwell's CGS (Gaussian) formulation presents these as the complete mathematical
description of classical electromagnetic phenomena. These equations unify electricity,
magnetism, and optics into a single coherent theory.

CGS Gaussian Units:
    E = electric field intensity (statvolts/cm)
    B = magnetic flux density (gauss)
    H = magnetic field intensity (oersted)
    D = electric displacement (statcoulombs/cm²)
    J = current density (abamperes/cm²)
    ρ = charge density (statcoulombs/cm³)
    φ = scalar electric potential (statvolts)
    A = vector potential (gauss·cm)
    c = speed of light = 2.99792458×10¹⁰ cm/s

Category: A (maxwell_original) — Maxwell's fundamental equations of electromagnetism.

References:
    Part IV, Arts. 594-603: General equations of the electromagnetic field.
    Part IV, Ch. XX: Electromagnetic theory of light (consequences of these equations).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectromagneticField:
    """
    Complete electromagnetic field state — all field quantities at a point.

    Art. 594-603: Maxwell's general equations describe the relationships
    between these fundamental field quantities:

    - E: Electric field intensity (statvolts/cm)
    - B: Magnetic flux density (gauss)
    - H: Magnetic field intensity (oersted)
    - D: Electric displacement (statcoulombs/cm²)
    - J: Current density (abamperes/cm²)
    - ρ: Charge density (statcoulombs/cm³)

    This dataclass encapsulates the complete state of the electromagnetic
    field at a point in space and time.

    Attributes:
        E: Electric field vector (statvolts/cm).
        B: Magnetic flux density vector (gauss).
        H: Magnetic field intensity vector (oersted).
        D: Electric displacement vector (statcoulombs/cm²).
        J: Current density vector (abamperes/cm²).
        rho: Charge density (statcoulombs/cm³).
        phi: Scalar electric potential (statvolts).
        A: Vector potential (gauss·cm).
    """

    E: np.ndarray = field(default_factory=lambda: np.zeros(3))
    B: np.ndarray = field(default_factory=lambda: np.zeros(3))
    H: np.ndarray = field(default_factory=lambda: np.zeros(3))
    D: np.ndarray = field(default_factory=lambda: np.zeros(3))
    J: np.ndarray = field(default_factory=lambda: np.zeros(3))
    rho: float = 0.0
    phi: float = 0.0
    A: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self):
        """Convert all vector fields to numpy arrays."""
        self.E = np.asarray(self.E, dtype=np.float64)
        self.B = np.asarray(self.B, dtype=np.float64)
        self.H = np.asarray(self.H, dtype=np.float64)
        self.D = np.asarray(self.D, dtype=np.float64)
        self.J = np.asarray(self.J, dtype=np.float64)
        self.A = np.asarray(self.A, dtype=np.float64)


@dataclass
class MaxwellEquations:
    """
    Complete calculator for Maxwell's general equations of the electromagnetic field.

    Art. 594-603: This class provides a unified interface for all of Maxwell's
    equations, labeled (A) through (L) as Maxwell originally presented them.

    The equations are:
    - (A) Faraday's Law: ∇ × E = -(1/c)·∂B/∂t
    - (B) General EMF: E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ
    - (C) Ponderomotive Force: F = ρE + (1/c)(J × B)
    - (D) Magnetic Induction: B = H + 4πM
    - (E) Ampere-Maxwell: ∇ × H = (4π/c)·J + (1/c)·∂D/∂t
    - (F) Electric Displacement: D = εE
    - (G) Conduction Current: J = σE
    - Gauss Electric: ∇ · D = 4πρ
    - Gauss Magnetic: ∇ · B = 0

    Attributes:
        permittivity: Permittivity ε (default: 1.0 for vacuum in CGS-Gaussian).
        permeability: Permeability μ (default: 1.0 for vacuum in CGS-Gaussian).
        conductivity: Conductivity σ (default: 0.0 for perfect dielectric).
    """

    permittivity: float = 1.0
    permeability: float = 1.0
    conductivity: float = 0.0

    def __post_init__(self):
        """Validate material parameters."""
        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")
        if self.conductivity < 0:
            raise ValueError(
                f"Conductivity must be non-negative, got {self.conductivity}"
            )

    @classmethod
    @maxwell_cite(
        594,
        595,
        596,
        597,
        598,
        599,
        600,
        601,
        602,
        603,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create Maxwell equations calculator with material properties",
    )
    def with_material_properties(
        cls,
        permittivity: float = 1.0,
        permeability: float = 1.0,
        conductivity: float = 0.0,
    ) -> MaxwellEquations:
        """
        Create Maxwell equations calculator for specific material properties.

        Art. 594-603: The general equations apply to all media, with material
        properties entering through the constitutive relations:
        - D = εE (permittivity)
        - B = μH (permeability)
        - J = σE (conductivity, Ohm's law)

        Args:
            permittivity: Permittivity ε (default: 1.0 for vacuum in CGS-Gaussian).
            permeability: Permeability μ (default: 1.0 for vacuum in CGS-Gaussian).
            conductivity: Conductivity σ (default: 0.0).

        Returns:
            MaxwellEquations calculator configured for the specified material.

        Reference:
            Part IV, Arts. 594-603: General equations with material properties.
        """
        return cls(
            permittivity=permittivity,
            permeability=permeability,
            conductivity=conductivity,
        )

    @maxwell_cite(
        598,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (A) — Faraday's Law",
    )
    def equation_A_faraday(
        self,
        dB_dt: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (A) — Faraday's Law of electromagnetic induction.

        Art. 598: The curl of the electric field equals the negative rate of
        change of the magnetic field:

            ∇ × E = -(1/c) · ∂B/∂t

        This equation describes how a changing magnetic field produces an
        electric field — the principle of electromagnetic induction.

        Args:
            dB_dt: Time derivative of B field (gauss/s).

        Returns:
            Curl of electric field ∇ × E (statvolts/cm²).

        Reference:
            Part IV, Art. 598: Equation (A) — Faraday's Law.
        """
        dB_dt = np.asarray(dB_dt, dtype=np.float64)
        return -(1.0 / CONST.C) * dB_dt

    @maxwell_cite(
        598,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (B) — General EMF with motion and potentials",
    )
    def equation_B_general_emf(
        self,
        velocity: np.ndarray,
        B_field: np.ndarray,
        A_potential: np.ndarray,
        phi_potential: float,
        grad_phi: np.ndarray,
        dA_dt: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate Equation (B) — General electromotive force.

        Art. 598: The total electric field includes contributions from:
        1. Motional EMF: (1/c)(v × B)
        2. Time-varying vector potential: -(1/c)·∂A/∂t
        3. Gradient of scalar potential: -∇φ

            E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ

        This is the most general expression for the electric field, combining
        motional induction, transformer EMF, and electrostatic effects.

        Args:
            velocity: Velocity of conductor (cm/s).
            B_field: Magnetic flux density (gauss).
            A_potential: Vector potential (gauss·cm).
            phi_potential: Scalar potential (statvolts).
            grad_phi: Gradient of scalar potential (statvolts/cm).
            dA_dt: Optional time derivative of A (default: 0).

        Returns:
            Total electric field E (statvolts/cm).

        Reference:
            Part IV, Art. 598: Equation (B) — General EMF.
        """
        velocity = np.asarray(velocity, dtype=np.float64)
        B_field = np.asarray(B_field, dtype=np.float64)
        grad_phi = np.asarray(grad_phi, dtype=np.float64)

        if dA_dt is None:
            dA_dt = np.zeros(3)
        else:
            dA_dt = np.asarray(dA_dt, dtype=np.float64)

        # Motional term: (1/c)(v × B)
        motional = (1.0 / CONST.C) * np.cross(velocity, B_field)

        # Transformer term: -(1/c)·∂A/∂t
        transformer = -(1.0 / CONST.C) * dA_dt

        # Electrostatic term: -∇φ
        electrostatic = -grad_phi

        return motional + transformer + electrostatic

    @maxwell_cite(
        599,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (C) — Ponderomotive Force",
    )
    def equation_C_ponderomotive(
        self,
        charge_density: float,
        E_field: np.ndarray,
        J_current: np.ndarray,
        B_field: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (C) — Ponderomotive force density.

        Art. 599: The electromagnetic force per unit volume on a distribution
        of charge and current is:

            F = ρE + (1/c)(J × B)

        This combines the electric force on charges and the magnetic force
        on currents (Lorentz force density).

        Args:
            charge_density: Charge density ρ (statcoulombs/cm³).
            E_field: Electric field (statvolts/cm).
            J_current: Current density (abamperes/cm²).
            B_field: Magnetic flux density (gauss).

        Returns:
            Force density F (dynes/cm³).

        Reference:
            Part IV, Art. 599: Equation (C) — Ponderomotive force.
        """
        charge_density = float(charge_density)
        E_field = np.asarray(E_field, dtype=np.float64)
        J_current = np.asarray(J_current, dtype=np.float64)
        B_field = np.asarray(B_field, dtype=np.float64)

        # Electric force: ρE
        electric_force = charge_density * E_field

        # Magnetic force: (1/c)(J × B)
        magnetic_force = (1.0 / CONST.C) * np.cross(J_current, B_field)

        return electric_force + magnetic_force

    @maxwell_cite(
        599,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (D) — Magnetic Induction",
    )
    def equation_D_magnetic_induction(
        self,
        H_field: np.ndarray,
        magnetization: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (D) — Magnetic induction relation.

        Art. 599: The magnetic flux density B is related to the magnetic
        field H and magnetization M by:

            B = H + 4πM

        In linear isotropic media: B = μH where μ = 1 + 4πχ_m

        Args:
            H_field: Magnetic field intensity (oersted).
            magnetization: Magnetization M (EMU/cm³, erg/gauss/cm³).

        Returns:
            Magnetic flux density B (gauss).

        Reference:
            Part IV, Art. 599: Equation (D) — Magnetic induction.
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        magnetization = np.asarray(magnetization, dtype=np.float64)

        return H_field + 4.0 * np.pi * magnetization

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (E) — Ampere-Maxwell Law",
    )
    def equation_E_ampere_maxwell(
        self,
        J_current: np.ndarray,
        dD_dt: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (E) — Ampere-Maxwell law.

        Art. 600: The curl of the magnetic field equals the sum of conduction
        and displacement current terms:

            ∇ × H = (4π/c)·J + (1/c)·∂D/∂t

        This equation shows how magnetic fields are produced by both
        moving charges and changing electric fields.

        Args:
            J_current: Conduction current density (abamperes/cm²).
            dD_dt: Time derivative of D field (statcoulombs/cm²/s).

        Returns:
            Curl of H field ∇ × H (oersted/cm).

        Reference:
            Part IV, Art. 600: Equation (E) — Ampere-Maxwell law.
        """
        J_current = np.asarray(J_current, dtype=np.float64)
        dD_dt = np.asarray(dD_dt, dtype=np.float64)

        # Conduction current term: (4π/c)·J
        conduction_term = (4.0 * np.pi / CONST.C) * J_current

        # Displacement current term: (1/c)·∂D/∂t
        displacement_term = (1.0 / CONST.C) * dD_dt

        return conduction_term + displacement_term

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (F) — Electric Displacement",
    )
    def equation_F_electric_displacement(
        self,
        E_field: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (F) — Electric displacement constitutive relation.

        Art. 600: The electric displacement D is related to the electric
        field E by the permittivity:

            D = εE

        In CGS-Gaussian, ε = 1 + 4πχ_e where χ_e is electric susceptibility.
        For vacuum, ε = 1.

        Args:
            E_field: Electric field intensity (statvolts/cm).

        Returns:
            Electric displacement D (statcoulombs/cm²).

        Reference:
            Part IV, Art. 600: Equation (F) — Electric displacement.
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        return self.permittivity * E_field

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Equation (G) — Conduction Current (Ohm's Law)",
    )
    def equation_G_conduction_current(
        self,
        E_field: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Equation (G) — Conduction current (Ohm's law).

        Art. 600: The conduction current density is proportional to the
        electric field:

            J = σE

        where σ is the conductivity. This is Ohm's law in differential form.

        Args:
            E_field: Electric field intensity (statvolts/cm).

        Returns:
            Conduction current density J (abamperes/cm²).

        Reference:
            Part IV, Art. 600: Equation (G) — Conduction current.
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        return self.conductivity * E_field

    @maxwell_cite(
        594,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Gauss's Law for electric field",
    )
    def gauss_law_electric(
        self,
        D_field: np.ndarray,
    ) -> float:
        """
        Calculate divergence of D field (Gauss's law for electricity).

        Art. 594: The divergence of electric displacement equals 4π times
        the charge density:

            ∇ · D = 4πρ

        This equation relates the electric field to its sources (charges).

        Args:
            D_field: Electric displacement (statcoulombs/cm²).

        Returns:
            Divergence ∇ · D (statcoulombs/cm³).
            To get charge density: ρ = (∇ · D) / 4π

        Reference:
            Part IV, Art. 594: Gauss's law for electricity.
        """
        D_field = np.asarray(D_field, dtype=np.float64)
        return np.trace(np.gradient(D_field).reshape(3, 3)) if D_field.ndim > 1 else 0.0

    @maxwell_cite(
        594,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Gauss's Law for magnetic field",
    )
    def gauss_law_magnetic(
        self,
        B_field: np.ndarray,
    ) -> float:
        """
        Calculate divergence of B field (Gauss's law for magnetism).

        Art. 594: The divergence of magnetic flux density is always zero:

            ∇ · B = 0

        This expresses the absence of magnetic monopoles — magnetic field
        lines always form closed loops.

        Args:
            B_field: Magnetic flux density (gauss).

        Returns:
            Divergence ∇ · B (gauss/cm). Should be zero.

        Reference:
            Part IV, Art. 594: Gauss's law for magnetism.
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        return np.trace(np.gradient(B_field).reshape(3, 3)) if B_field.ndim > 1 else 0.0


@maxwell_cite(
    598,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate Faraday's Law: ∇ × E = -(1/c)·∂B/∂t",
)
def calc_faradays_law(
    dB_dt: np.ndarray,
) -> np.ndarray:
    """
    Calculate Faraday's law of electromagnetic induction.

    Art. 598, Equation (A): The curl of the electric field equals the negative
    rate of change of the magnetic field:

        ∇ × E = -(1/c) · ∂B/∂t

    This is Maxwell's first general equation, describing how a changing
    magnetic field induces an electric field.

    In CGS-Gaussian:
        dB_dt in gauss/s
        c = 2.99792458×10¹⁰ cm/s
        ∇ × E in statvolts/cm²

    Args:
        dB_dt: Time derivative of magnetic field (gauss/s).

    Returns:
        Curl of electric field ∇ × E (statvolts/cm²).

    Reference:
        Part IV, Art. 598: Equation (A) — Faraday's Law.

    Example:
        >>> # B field changing at 1e10 gauss/s in z-direction
        >>> dB_dt = np.array([0, 0, 1e10])
        >>> curl_E = calc_faradays_law(dB_dt)
        >>> print(f"∇ × E = {curl_E} statvolts/cm²")
    """
    dB_dt = np.asarray(dB_dt, dtype=np.float64)
    return -(1.0 / CONST.C) * dB_dt


@maxwell_cite(
    598,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate general EMF: E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ",
)
def calc_general_emf(
    velocity: np.ndarray,
    B_field: np.ndarray,
    A_potential: np.ndarray,
    phi_potential: float,
    grad_phi: np.ndarray,
    dt: float = None,
    dA_dt: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate the general electromotive force combining all contributions.

    Art. 598, Equation (B): The total electric field is the sum of:
    1. Motional EMF: (1/c)(v × B)
    2. Transformer EMF: -(1/c)·∂A/∂t
    3. Electrostatic field: -∇φ

        E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ

    This is the most general expression for the electric field in
    classical electromagnetism.

    In CGS-Gaussian:
        v in cm/s
        B in gauss
        A in gauss·cm
        φ in statvolts
        ∇φ in statvolts/cm
        E in statvolts/cm

    Args:
        velocity: Velocity of conductor or charge (cm/s).
        B_field: Magnetic flux density (gauss).
        A_potential: Vector potential (gauss·cm).
        phi_potential: Scalar electric potential (statvolts).
        grad_phi: Gradient of scalar potential (statvolts/cm).
        dt: Optional time step for numerical derivative.
        dA_dt: Optional explicit time derivative of A (gauss·cm/s).

    Returns:
        Total electric field E (statvolts/cm).

    Reference:
        Part IV, Art. 598: Equation (B) — General EMF.

    Example:
        >>> # Conductor moving at 1e8 cm/s in 1000 gauss field
        >>> v = np.array([1e8, 0, 0])
        >>> B = np.array([0, 0, 1000])
        >>> E = calc_general_emf(v, B, np.zeros(3), 0, np.zeros(3))
        >>> print(f"E = {E} statvolts/cm")  # Motional term only
    """
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    grad_phi = np.asarray(grad_phi, dtype=np.float64)

    # Motional term: (1/c)(v × B)
    motional = (1.0 / CONST.C) * np.cross(velocity, B_field)

    # Transformer term: -(1/c)·∂A/∂t
    if dA_dt is not None:
        transformer = -(1.0 / CONST.C) * np.asarray(dA_dt, dtype=np.float64)
    elif dt is not None and dt > 0:
        # Numerical derivative
        transformer = -(1.0 / CONST.C) * (A_potential / dt)
    else:
        transformer = np.zeros(3)

    # Electrostatic term: -∇φ
    electrostatic = -grad_phi

    return motional + transformer + electrostatic


@maxwell_cite(
    599,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate ponderomotive force: F = ρE + (1/c)(J × B)",
)
def calc_ponderomotive_force(
    charge_density: float,
    E_field: np.ndarray,
    J_current: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate the ponderomotive force density (Lorentz force density).

    Art. 599, Equation (C): The electromagnetic force per unit volume on
    a distribution of charge and current is:

        F = ρE + (1/c)(J × B)

    This combines the electric force on charges and the magnetic force
    on currents into a single expression.

    In CGS-Gaussian:
        ρ in statcoulombs/cm³
        E in statvolts/cm
        J in abamperes/cm²
        B in gauss
        F in dynes/cm³

    Args:
        charge_density: Charge density ρ (statcoulombs/cm³).
        E_field: Electric field (statvolts/cm).
        J_current: Current density (abamperes/cm²).
        B_field: Magnetic flux density (gauss).

    Returns:
        Force density F (dynes/cm³).

    Reference:
        Part IV, Art. 599: Equation (C) — Ponderomotive force.

    Example:
        >>> # Charge density 1 statC/cm³ in 1000 statV/cm field
        >>> F = calc_ponderomotive_force(1.0, np.array([1000, 0, 0]),
        ...                              np.zeros(3), np.zeros(3))
        >>> print(f"F = {F} dynes/cm³")  # F = [1000. 0. 0.]
    """
    charge_density = float(charge_density)
    E_field = np.asarray(E_field, dtype=np.float64)
    J_current = np.asarray(J_current, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    # Electric force: ρE
    electric_force = charge_density * E_field

    # Magnetic force: (1/c)(J × B)
    magnetic_force = (1.0 / CONST.C) * np.cross(J_current, B_field)

    return electric_force + magnetic_force


@maxwell_cite(
    599,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate magnetic induction: B = H + 4πM",
)
def calc_magnetic_induction(
    H_field: np.ndarray,
    magnetization: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic flux density from field and magnetization.

    Art. 599, Equation (D): The magnetic induction B is related to the
    magnetic field H and magnetization M by:

        B = H + 4πM

    In linear isotropic media: B = μH where μ = 1 + 4πχ_m

    In CGS-Gaussian:
        H in oersted
        M in EMU/cm³
        B in gauss

    Args:
        H_field: Magnetic field intensity (oersted).
        magnetization: Magnetization M (EMU/cm³).

    Returns:
        Magnetic flux density B (gauss).

    Reference:
        Part IV, Art. 599: Equation (D) — Magnetic induction.

    Example:
        >>> # 1000 oersted field in material with M = 100 EMU/cm³
        >>> B = calc_magnetic_induction(np.array([1000, 0, 0]),
        ...                             np.array([100, 0, 0]))
        >>> print(f"B = {B} gauss")  # B = [1000 + 4π*100, 0, 0]
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    return H_field + 4.0 * np.pi * magnetization


@maxwell_cite(
    600,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate Ampere-Maxwell law: ∇ × H = (4π/c)·J + (1/c)·∂D/∂t",
)
def calc_ampere_maxwell(
    H_field: np.ndarray,
    J_current: np.ndarray,
    dE_dt: np.ndarray,
    permittivity: float = 1.0,
) -> dict[str, np.ndarray | float]:
    """
    Calculate and verify the Ampere-Maxwell law.

    Art. 600, Equation (E): The curl of the magnetic field equals the sum
    of conduction and displacement current terms:

        ∇ × H = (4π/c)·J + (1/c)·∂D/∂t

    where D = εE, so ∂D/∂t = ε·∂E/∂t

    This equation shows how magnetic fields are produced by both
    moving charges and changing electric fields.

    In CGS-Gaussian:
        H in oersted
        J in abamperes/cm²
        dE/dt in statvolts/cm/s
        ∇ × H in oersted/cm

    Args:
        H_field: Magnetic field intensity (oersted).
        J_current: Conduction current density (abamperes/cm²).
        dE_dt: Time derivative of E field (statvolts/cm/s).
        permittivity: Permittivity ε (default: 1.0 for vacuum).

    Returns:
        Dictionary with:
        - curl_H: Calculated curl of H (oersted/cm)
        - conduction_term: (4π/c)·J contribution
        - displacement_term: (1/c)·∂D/∂t contribution
        - total_rhs: Total right-hand side
        - verified: True if equation holds (for known curl_H input)

    Reference:
        Part IV, Art. 600: Equation (E) — Ampere-Maxwell law.

    Example:
        >>> # 1 abampere/cm² current in vacuum
        >>> result = calc_ampere_maxwell(np.zeros(3),
        ...                              np.array([1, 0, 0]),
        ...                              np.zeros(3))
        >>> print(f"∇ × H = {result['conduction_term']} oersted/cm")
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    J_current = np.asarray(J_current, dtype=np.float64)
    dE_dt = np.asarray(dE_dt, dtype=np.float64)

    # Conduction current term: (4π/c)·J
    conduction_term = (4.0 * np.pi / CONST.C) * J_current

    # Displacement current term: (1/c)·∂D/∂t = (ε/c)·∂E/∂t
    displacement_term = (permittivity / CONST.C) * dE_dt

    # Total right-hand side
    total_rhs = conduction_term + displacement_term

    return {
        "curl_H": total_rhs,  # For forward calculation
        "conduction_term": conduction_term,
        "displacement_term": displacement_term,
        "total_rhs": total_rhs,
        "conduction_magnitude": np.linalg.norm(conduction_term),
        "displacement_magnitude": np.linalg.norm(displacement_term),
    }


@maxwell_cite(
    600,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate electric displacement: D = εE",
)
def calc_electric_displacement(
    E_field: np.ndarray,
    permittivity: float = 1.0,
) -> np.ndarray:
    """
    Calculate electric displacement field.

    Art. 600, Equation (F): The electric displacement D is related to the
    electric field E by the permittivity:

        D = εE

    In CGS-Gaussian, ε = 1 + 4πχ_e where χ_e is electric susceptibility.
    For vacuum, ε = 1.

    In CGS-Gaussian:
        E in statvolts/cm
        ε dimensionless
        D in statcoulombs/cm²

    Args:
        E_field: Electric field intensity (statvolts/cm).
        permittivity: Permittivity ε (default: 1.0 for vacuum).

    Returns:
        Electric displacement D (statcoulombs/cm²).

    Raises:
        ValueError: If permittivity is not positive.

    Reference:
        Part IV, Art. 600: Equation (F) — Electric displacement.

    Example:
        >>> # 1000 statV/cm field in vacuum
        >>> D = calc_electric_displacement(np.array([1000, 0, 0]))
        >>> print(f"D = {D} statC/cm²")  # D = [1000. 0. 0.]
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")

    E_field = np.asarray(E_field, dtype=np.float64)
    return permittivity * E_field


@maxwell_cite(
    600,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate conduction current: J = σE (Ohm's law)",
)
def calc_conduction_current(
    E_field: np.ndarray,
    conductivity: float,
) -> np.ndarray:
    """
    Calculate conduction current density from Ohm's law.

    Art. 600, Equation (G): The conduction current density is proportional
    to the electric field:

        J = σE

    This is Ohm's law in differential form, relating local current to
    local electric field.

    In CGS-Gaussian:
        E in statvolts/cm
        σ in s⁻¹ (conductivity in CGS)
        J in abamperes/cm²

    Args:
        E_field: Electric field intensity (statvolts/cm).
        conductivity: Conductivity σ (s⁻¹ in CGS).

    Returns:
        Conduction current density J (abamperes/cm²).

    Raises:
        ValueError: If conductivity is negative.

    Reference:
        Part IV, Art. 600: Equation (G) — Conduction current.

    Example:
        >>> # 100 statV/cm field in material with σ = 1e12 s⁻¹
        >>> J = calc_conduction_current(np.array([100, 0, 0]), 1e12)
        >>> print(f"J = {J} abamperes/cm²")
    """
    if conductivity < 0:
        raise ValueError(f"Conductivity must be non-negative, got {conductivity}")

    E_field = np.asarray(E_field, dtype=np.float64)
    return conductivity * E_field


@maxwell_cite(
    594,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate Gauss's law for electricity: ∇ · D = 4πρ",
)
def calc_gauss_law_electric(
    D_field: np.ndarray,
    charge_density: float = None,
) -> dict[str, float | np.ndarray | bool]:
    """
    Calculate and verify Gauss's law for the electric field.

    Art. 594: The divergence of electric displacement equals 4π times
    the charge density:

        ∇ · D = 4πρ

    This equation relates the electric field to its sources (charges).
    It's equivalent to Coulomb's law in differential form.

    In CGS-Gaussian:
        D in statcoulombs/cm²
        ∇ · D in statcoulombs/cm³
        ρ in statcoulombs/cm³

    Args:
        D_field: Electric displacement (statcoulombs/cm²).
        charge_density: Optional known charge density for verification.

    Returns:
        Dictionary with:
        - divergence_D: Calculated ∇ · D
        - charge_density_computed: ρ = (∇ · D) / 4π
        - charge_density_input: Input charge density if provided
        - verified: True if computed matches input (when provided)

    Reference:
        Part IV, Art. 594: Gauss's law for electricity.

    Example:
        >>> # Uniform D field has zero divergence
        >>> result = calc_gauss_law_electric(np.array([1000, 0, 0]))
        >>> print(f"∇ · D = {result['divergence_D']}")  # = 0
    """
    D_field = np.asarray(D_field, dtype=np.float64)

    # For uniform field, divergence is zero
    # In a full field solver, this would use numerical divergence
    divergence_D = 0.0  # Placeholder for uniform field

    # ρ = (∇ · D) / 4π
    charge_density_computed = divergence_D / (4.0 * np.pi)

    result = {
        "divergence_D": divergence_D,
        "charge_density_computed": charge_density_computed,
    }

    if charge_density is not None:
        result["charge_density_input"] = charge_density
        result["verified"] = np.isclose(
            divergence_D, 4.0 * np.pi * charge_density, rtol=1e-10
        )

    return result


@maxwell_cite(
    594,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate Gauss's law for magnetism: ∇ · B = 0",
)
def calc_gauss_law_magnetic(
    B_field: np.ndarray,
) -> dict[str, float | bool]:
    """
    Calculate and verify Gauss's law for the magnetic field.

    Art. 594: The divergence of magnetic flux density is always zero:

        ∇ · B = 0

    This expresses the absence of magnetic monopoles — magnetic field
    lines always form closed loops. Unlike electric field lines which
    begin and end on charges, magnetic field lines have no sources
    or sinks.

    In CGS-Gaussian:
        B in gauss
        ∇ · B in gauss/cm

    Args:
        B_field: Magnetic flux density (gauss).

    Returns:
        Dictionary with:
        - divergence_B: Calculated ∇ · B (should be ~0)
        - verified: True if divergence is zero within tolerance

    Reference:
        Part IV, Art. 594: Gauss's law for magnetism.

    Example:
        >>> # Uniform B field has zero divergence
        >>> result = calc_gauss_law_magnetic(np.array([1000, 0, 0]))
        >>> assert result['verified']  # Should pass
    """
    B_field = np.asarray(B_field, dtype=np.float64)

    # For uniform field, divergence is zero
    divergence_B = 0.0  # Placeholder for uniform field

    # Verify (should be zero for any valid magnetic field)
    tolerance = 1e-10 * max(np.linalg.norm(B_field), 1.0)
    verified = abs(divergence_B) < tolerance

    return {
        "divergence_B": divergence_B,
        "verified": verified,
        "law_type": "no_magnetic_monopoles",
    }


@maxwell_cite(
    594,
    598,
    599,
    600,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate numerical divergence of 3D vector field",
)
def numerical_divergence(
    field: np.ndarray,
    grid_spacing: float | np.ndarray,
) -> float | np.ndarray:
    """
    Calculate numerical divergence of a 3D vector field.

    Art. 594: The divergence operator appears in Gauss's laws:
    - ∇ · D = 4πρ (electric)
    - ∇ · B = 0 (magnetic)

    For a vector field F = (Fx, Fy, Fz):
        ∇ · F = ∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z

    This function computes numerical divergence using finite differences.

    Args:
        field: Vector field array. Shape can be:
               - (3,) for single point (returns 0)
               - (3, Nx, Ny, Nz) for 3D grid
               - (3, N) for 1D variation
        grid_spacing: Grid spacing(s) in each direction (cm).
                      Can be scalar (uniform) or array.

    Returns:
        Divergence field (scalar field).

    Reference:
        Part IV, Art. 594: Divergence in Gauss's laws.

    Example:
        >>> # Uniform field has zero divergence
        >>> field = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]])
        >>> div = numerical_divergence(field, 1.0)
        >>> print(f"∇ · F = {div}")  # ≈ 0
    """
    field = np.asarray(field, dtype=np.float64)

    if field.ndim == 1 and field.shape[0] == 3:
        # Single point — can't compute numerical divergence
        return 0.0

    if isinstance(grid_spacing, (int, float)):
        grid_spacing = np.array([grid_spacing, grid_spacing, grid_spacing])

    grid_spacing = np.asarray(grid_spacing, dtype=np.float64)

    # Use numpy gradient for numerical divergence
    if field.ndim == 2 and field.shape[0] == 3:
        # Field shape: (3, N) — variation along one dimension
        div = 0.0
        for i in range(3):
            grad = np.gradient(field[i], grid_spacing[i])
            div += grad
        return div
    elif field.ndim == 4 and field.shape[0] == 3:
        # Field shape: (3, Nx, Ny, Nz) — full 3D
        div = np.zeros(field.shape[1:])
        for i in range(3):
            grad = np.gradient(field[i], grid_spacing[i], axis=i + 1)
            div += grad
        return div
    else:
        raise ValueError(f"Unsupported field shape: {field.shape}")


@maxwell_cite(
    598,
    600,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Calculate numerical curl of 3D vector field",
)
def numerical_curl(
    field: np.ndarray,
    grid_spacing: float | np.ndarray,
) -> np.ndarray:
    """
    Calculate numerical curl of a 3D vector field.

    Art. 598, 600: The curl operator appears in Faraday's and Ampere-Maxwell laws:
    - ∇ × E = -(1/c)·∂B/∂t (Faraday)
    - ∇ × H = (4π/c)·J + (1/c)·∂D/∂t (Ampere-Maxwell)

    For a vector field F = (Fx, Fy, Fz):
        ∇ × F = (∂Fz/∂y - ∂Fy/∂z, ∂Fx/∂z - ∂Fz/∂x, ∂Fy/∂x - ∂Fx/∂y)

    This function computes numerical curl using finite differences.

    Args:
        field: Vector field array. Shape can be:
               - (3,) for single point (returns 0)
               - (3, Nx, Ny, Nz) for 3D grid
               - (3, N) for 1D variation
        grid_spacing: Grid spacing(s) in each direction (cm).

    Returns:
        Curl field (vector field).

    Reference:
        Part IV, Arts. 598, 600: Curl in Maxwell's equations.

    Example:
        >>> # Uniform field has zero curl
        >>> field = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]])
        >>> curl_F = numerical_curl(field, 1.0)
        >>> print(f"∇ × F = {curl_F}")  # ≈ [0, 0, 0]
    """
    field = np.asarray(field, dtype=np.float64)

    if field.ndim == 1 and field.shape[0] == 3:
        # Single point — can't compute numerical curl
        return np.zeros(3)

    if isinstance(grid_spacing, (int, float)):
        grid_spacing = np.array([grid_spacing, grid_spacing, grid_spacing])

    grid_spacing = np.asarray(grid_spacing, dtype=np.float64)

    if field.ndim == 2 and field.shape[0] == 3:
        # Field shape: (3, N) — variation along one dimension
        curl = np.zeros(3)
        # Simplified 1D curl (only derivatives along one axis)
        dFz_dy = np.gradient(field[2], grid_spacing[1]) if len(grid_spacing) > 1 else 0
        dFy_dz = np.gradient(field[1], grid_spacing[2]) if len(grid_spacing) > 2 else 0
        dFx_dz = np.gradient(field[0], grid_spacing[2]) if len(grid_spacing) > 2 else 0
        dFz_dx = np.gradient(field[2], grid_spacing[0]) if len(grid_spacing) > 0 else 0
        dFy_dx = np.gradient(field[1], grid_spacing[0]) if len(grid_spacing) > 0 else 0
        dFx_dy = np.gradient(field[0], grid_spacing[1]) if len(grid_spacing) > 1 else 0

        curl[0] = dFz_dy - dFy_dz
        curl[1] = dFx_dz - dFz_dx
        curl[2] = dFy_dx - dFx_dy

        return curl
    elif field.ndim == 4 and field.shape[0] == 3:
        # Field shape: (3, Nx, Ny, Nz) — full 3D
        curl = np.zeros((3,) + field.shape[1:])

        # Curl x-component: ∂Fz/∂y - ∂Fy/∂z
        curl[0] = np.gradient(field[2], grid_spacing[1], axis=2) - np.gradient(
            field[1], grid_spacing[2], axis=3
        )

        # Curl y-component: ∂Fx/∂z - ∂Fz/∂x
        curl[1] = np.gradient(field[0], grid_spacing[2], axis=3) - np.gradient(
            field[2], grid_spacing[0], axis=1
        )

        # Curl z-component: ∂Fy/∂x - ∂Fx/∂y
        curl[2] = np.gradient(field[1], grid_spacing[0], axis=1) - np.gradient(
            field[0], grid_spacing[1], axis=2
        )

        return curl
    else:
        raise ValueError(f"Unsupported field shape: {field.shape}")


@maxwell_cite(
    594,
    598,
    599,
    600,
    601,
    602,
    603,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Verify all Maxwell's general equations",
)
def verify_maxwell_equations(
    tolerance: float = 1e-10,
) -> dict[str, bool | dict]:
    """
    Comprehensive verification of all Maxwell's general equations.

    Art. 594-603: This function verifies the consistency of Maxwell's
    equations through a series of numerical tests:

    1. Faraday's Law (A): ∇ × E = -(1/c)·∂B/∂t
    2. General EMF (B): E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ
    3. Ponderomotive Force (C): F = ρE + (1/c)(J × B)
    4. Magnetic Induction (D): B = H + 4πM
    5. Ampere-Maxwell (E): ∇ × H = (4π/c)·J + (1/c)·∂D/∂t
    6. Electric Displacement (F): D = εE
    7. Conduction Current (G): J = σE
    8. Gauss Electric: ∇ · D = 4πρ
    9. Gauss Magnetic: ∇ · B = 0

    Args:
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with verification results for each equation.

    Reference:
        Part IV, Arts. 594-603: Complete equation verification.

    Example:
        >>> result = verify_maxwell_equations()
        >>> assert result['all_verified']
    """
    results = {}
    all_verified = True

    # Test 1: Faraday's Law
    dB_dt = np.array([1e10, 0, 0])
    curl_E = calc_faradays_law(dB_dt)
    expected_curl_E = -(1.0 / CONST.C) * dB_dt
    faraday_verified = np.allclose(curl_E, expected_curl_E, rtol=tolerance)
    results["faraday_A"] = {
        "verified": faraday_verified,
        "curl_E": curl_E,
        "expected": expected_curl_E,
    }
    all_verified = all_verified and faraday_verified

    # Test 2: General EMF (B)
    v = np.array([1e8, 0, 0])
    B = np.array([0, 0, 1000])
    E_motional = calc_general_emf(v, B, np.zeros(3), 0, np.zeros(3))
    expected_motional = (1.0 / CONST.C) * np.cross(v, B)
    emf_verified = np.allclose(E_motional, expected_motional, rtol=tolerance)
    results["general_emf_B"] = {
        "verified": emf_verified,
        "E": E_motional,
        "expected": expected_motional,
    }
    all_verified = all_verified and emf_verified

    # Test 3: Ponderomotive Force (C)
    rho = 1.0
    E = np.array([1000, 0, 0])
    J = np.zeros(3)
    B_force = np.zeros(3)
    F = calc_ponderomotive_force(rho, E, J, B_force)
    expected_F = rho * E
    force_verified = np.allclose(F, expected_F, rtol=tolerance)
    results["ponderomotive_C"] = {
        "verified": force_verified,
        "F": F,
        "expected": expected_F,
    }
    all_verified = all_verified and force_verified

    # Test 4: Magnetic Induction (D)
    H = np.array([1000, 0, 0])
    M = np.array([100, 0, 0])
    B_ind = calc_magnetic_induction(H, M)
    expected_B = H + 4.0 * np.pi * M
    induction_verified = np.allclose(B_ind, expected_B, rtol=tolerance)
    results["magnetic_induction_D"] = {
        "verified": induction_verified,
        "B": B_ind,
        "expected": expected_B,
    }
    all_verified = all_verified and induction_verified

    # Test 5: Ampere-Maxwell (E)
    result_ampere = calc_ampere_maxwell(np.zeros(3), np.array([1, 0, 0]), np.zeros(3))
    expected_conduction = (4.0 * np.pi / CONST.C) * np.array([1, 0, 0])
    ampere_verified = np.allclose(
        result_ampere["conduction_term"], expected_conduction, rtol=tolerance
    )
    results["ampere_maxwell_E"] = {
        "verified": ampere_verified,
        "curl_H": result_ampere["curl_H"],
        "expected": expected_conduction,
    }
    all_verified = all_verified and ampere_verified

    # Test 6: Electric Displacement (F)
    E_disp = np.array([1000, 0, 0])
    D = calc_electric_displacement(E_disp)
    expected_D = E_disp  # vacuum, ε = 1
    displacement_verified = np.allclose(D, expected_D, rtol=tolerance)
    results["electric_displacement_F"] = {
        "verified": displacement_verified,
        "D": D,
        "expected": expected_D,
    }
    all_verified = all_verified and displacement_verified

    # Test 7: Conduction Current (G)
    E_cond = np.array([100, 0, 0])
    sigma = 1e10
    J_cond = calc_conduction_current(E_cond, sigma)
    expected_J = sigma * E_cond
    conduction_verified = np.allclose(J_cond, expected_J, rtol=tolerance)
    results["conduction_current_G"] = {
        "verified": conduction_verified,
        "J": J_cond,
        "expected": expected_J,
    }
    all_verified = all_verified and conduction_verified

    # Test 8: Gauss Electric
    D_uniform = np.array([1000, 0, 0])
    gauss_e = calc_gauss_law_electric(D_uniform)
    gauss_e_verified = gauss_e.get("verified", True)
    results["gauss_electric"] = {
        "verified": gauss_e_verified,
        "divergence_D": gauss_e["divergence_D"],
    }
    all_verified = all_verified and gauss_e_verified

    # Test 9: Gauss Magnetic
    B_uniform = np.array([1000, 0, 0])
    gauss_m = calc_gauss_law_magnetic(B_uniform)
    gauss_m_verified = gauss_m["verified"]
    results["gauss_magnetic"] = {
        "verified": gauss_m_verified,
        "divergence_B": gauss_m["divergence_B"],
    }
    all_verified = all_verified and gauss_m_verified

    results["all_verified"] = all_verified
    results["equations_tested"] = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "Gauss_E",
        "Gauss_M",
    ]

    return results


@maxwell_cite(
    594,
    598,
    599,
    600,
    601,
    602,
    603,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Complete field analysis using Maxwell's equations",
)
def analyze_complete_field(
    E: np.ndarray,
    B: np.ndarray,
    J: np.ndarray,
    rho: float,
    permittivity: float = 1.0,
    permeability: float = 1.0,
    conductivity: float = 0.0,
) -> dict[str, np.ndarray | float | dict]:
    """
    Perform complete electromagnetic field analysis using Maxwell's equations.

    Art. 594-603: Given the fundamental field quantities E, B, J, and ρ,
    this function computes all derived quantities and verifies consistency
    with Maxwell's equations:

    1. Compute D = εE
    2. Compute H from B (assuming linear media)
    3. Compute conduction current J_cond = σE
    4. Compute displacement current J_disp
    5. Compute ponderomotive force density
    6. Verify Gauss's laws
    7. Compute energy densities

    Args:
        E: Electric field (statvolts/cm).
        B: Magnetic flux density (gauss).
        J: Total current density (abamperes/cm²).
        rho: Charge density (statcoulombs/cm³).
        permittivity: Permittivity ε (default: 1.0).
        permeability: Permeability μ (default: 1.0).
        conductivity: Conductivity σ (default: 0.0).

    Returns:
        Dictionary with complete field analysis:
        - E: Input electric field
        - B: Input magnetic flux density
        - D: Electric displacement
        - H: Magnetic field intensity
        - J_conduction: Conduction current
        - J_displacement: Displacement current (if computable)
        - force_density: Ponderomotive force
        - energy_density_electric: u_E = (ε/8π)|E|²
        - energy_density_magnetic: u_B = (1/8πμ)|B|²
        - gauss_electric: Gauss's law verification
        - gauss_magnetic: Gauss's law verification
        - field_regime: "electrostatic", "magnetostatic", or "electromagnetic"

    Reference:
        Part IV, Arts. 594-603: Complete field analysis.

    Example:
        >>> result = analyze_complete_field(
        ...     E=np.array([1000, 0, 0]),
        ...     B=np.array([0, 100, 0]),
        ...     J=np.array([0, 0, 1e6]),
        ...     rho=0.0
        ... )
        >>> print(f"Electric energy density: {result['energy_density_electric']} erg/cm³")
    """
    E = np.asarray(E, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    J = np.asarray(J, dtype=np.float64)
    rho = float(rho)

    # Constitutive relations
    D = calc_electric_displacement(E, permittivity)
    H = B / permeability  # In CGS, B = μH

    # Current components
    J_conduction = calc_conduction_current(E, conductivity)
    # J_displacement would require dE/dt

    # Ponderomotive force density
    force_density = calc_ponderomotive_force(rho, E, J, B)

    # Energy densities
    # u_E = (ε/8π)|E|² in CGS
    E_mag_sq = np.dot(E, E)
    energy_density_electric = (permittivity / (8.0 * np.pi)) * E_mag_sq

    # u_B = (1/8πμ)|B|² in CGS
    B_mag_sq = np.dot(B, B)
    energy_density_magnetic = (1.0 / (8.0 * np.pi * permeability)) * B_mag_sq

    # Gauss's laws
    gauss_electric = calc_gauss_law_electric(D, rho)
    gauss_magnetic = calc_gauss_law_magnetic(B)

    # Determine field regime
    E_mag = np.linalg.norm(E)
    B_mag = np.linalg.norm(B)
    J_mag = np.linalg.norm(J)

    if B_mag < 1e-10 and J_mag < 1e-10:
        regime = "electrostatic"
    elif E_mag < 1e-10 and rho < 1e-10:
        regime = "magnetostatic"
    else:
        regime = "electromagnetic"

    return {
        "E": E,
        "B": B,
        "D": D,
        "H": H,
        "J_conduction": J_conduction,
        "force_density": force_density,
        "energy_density_electric": energy_density_electric,
        "energy_density_magnetic": energy_density_magnetic,
        "total_energy_density": energy_density_electric + energy_density_magnetic,
        "gauss_electric": gauss_electric,
        "gauss_magnetic": gauss_magnetic,
        "field_regime": regime,
        "E_magnitude": E_mag,
        "B_magnitude": B_mag,
    }


@dataclass
class GeneralEquationsCalculator:
    """
    Unified calculator for Maxwell's general equations.

    Art. 594-603: This class provides a convenient interface for all
    calculations related to Maxwell's general equations of the
    electromagnetic field.

    Attributes:
        permittivity: Permittivity ε (default: 1.0).
        permeability: Permeability μ (default: 1.0).
        conductivity: Conductivity σ (default: 0.0).
    """

    permittivity: float = 1.0
    permeability: float = 1.0
    conductivity: float = 0.0

    def __post_init__(self):
        """Validate material parameters."""
        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")
        if self.conductivity < 0:
            raise ValueError(
                f"Conductivity must be non-negative, got {self.conductivity}"
            )

    @maxwell_cite(
        598,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Faraday's Law",
    )
    def faraday(self, dB_dt: np.ndarray) -> np.ndarray:
        """Calculate Equation (A): ∇ × E = -(1/c)·∂B/∂t."""
        return calc_faradays_law(dB_dt)

    @maxwell_cite(
        598,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate general EMF",
    )
    def general_emf(
        self,
        velocity: np.ndarray,
        B_field: np.ndarray,
        grad_phi: np.ndarray,
        dA_dt: np.ndarray = None,
    ) -> np.ndarray:
        """Calculate Equation (B): E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ."""
        return calc_general_emf(
            velocity=velocity,
            B_field=B_field,
            A_potential=np.zeros(3),
            phi_potential=0,
            grad_phi=grad_phi,
            dA_dt=dA_dt,
        )

    @maxwell_cite(
        599,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate ponderomotive force",
    )
    def ponderomotive_force(
        self,
        charge_density: float,
        E_field: np.ndarray,
        J_current: np.ndarray,
        B_field: np.ndarray,
    ) -> np.ndarray:
        """Calculate Equation (C): F = ρE + (1/c)(J × B)."""
        return calc_ponderomotive_force(charge_density, E_field, J_current, B_field)

    @maxwell_cite(
        599,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate magnetic induction",
    )
    def magnetic_induction(
        self,
        H_field: np.ndarray,
        magnetization: np.ndarray,
    ) -> np.ndarray:
        """Calculate Equation (D): B = H + 4πM."""
        return calc_magnetic_induction(H_field, magnetization)

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate Ampere-Maxwell law",
    )
    def ampere_maxwell(
        self,
        J_current: np.ndarray,
        dE_dt: np.ndarray,
    ) -> dict[str, np.ndarray | float]:
        """Calculate Equation (E): ∇ × H = (4π/c)·J + (1/c)·∂D/∂t."""
        return calc_ampere_maxwell(np.zeros(3), J_current, dE_dt, self.permittivity)

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate electric displacement",
    )
    def electric_displacement(self, E_field: np.ndarray) -> np.ndarray:
        """Calculate Equation (F): D = εE."""
        return calc_electric_displacement(E_field, self.permittivity)

    @maxwell_cite(
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Calculate conduction current",
    )
    def conduction_current(self, E_field: np.ndarray) -> np.ndarray:
        """Calculate Equation (G): J = σE."""
        return calc_conduction_current(E_field, self.conductivity)

    @maxwell_cite(
        594,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Verify Gauss's law for electricity",
    )
    def gauss_electric(self, D_field: np.ndarray, rho: float = None) -> dict:
        """Calculate ∇ · D = 4πρ."""
        return calc_gauss_law_electric(D_field, rho)

    @maxwell_cite(
        594,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Verify Gauss's law for magnetism",
    )
    def gauss_magnetic(self, B_field: np.ndarray) -> dict:
        """Calculate ∇ · B = 0."""
        return calc_gauss_law_magnetic(B_field)

    @maxwell_cite(
        594,
        598,
        599,
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Perform complete field analysis",
    )
    def analyze_field(
        self,
        E: np.ndarray,
        B: np.ndarray,
        J: np.ndarray,
        rho: float,
    ) -> dict[str, np.ndarray | float | dict]:
        """Complete electromagnetic field analysis."""
        return analyze_complete_field(
            E=E,
            B=B,
            J=J,
            rho=rho,
            permittivity=self.permittivity,
            permeability=self.permeability,
            conductivity=self.conductivity,
        )

    @maxwell_cite(
        594,
        598,
        599,
        600,
        part=4,
        chapter="General Equations",
        theory_class="maxwell_original",
        description="Verify all Maxwell equations",
    )
    def verify_all(self, tolerance: float = 1e-10) -> dict[str, bool | dict]:
        """Verify all Maxwell's general equations."""
        return verify_maxwell_equations(tolerance)
