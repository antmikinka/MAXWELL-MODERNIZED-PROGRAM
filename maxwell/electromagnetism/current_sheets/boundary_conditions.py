"""
Electromagnetic Boundary Conditions — field discontinuities at interfaces.

Implements Maxwell's theory of boundary conditions from Articles 663-674:

- Tangential E continuity (Art. 663-665)
- Normal B continuity (Art. 666-667)
- Normal D discontinuity (Art. 668-669)
- Tangential H discontinuity (Art. 670-671)
- Moving media boundaries (Art. 672-673)
- Energy flux at boundaries (Art. 674)

At the interface between two media, Maxwell's equations impose specific
conditions on how the fields can change. These follow from the integral
form of Maxwell's equations applied to infinitesimal pillboxes and loops
at the boundary.

CGS Units:
    E = electric field (statvolts/cm)
    B = magnetic flux density (gauss)
    D = electric displacement (statcoulombs/cm²)
    H = magnetic field intensity (oersted)

Category: A (maxwell_original) — Maxwell's electromagnetic boundary conditions.

References:
    Part IV, Ch XII: Current-Sheets (Arts. 647-674).
    Part IV, Arts. 663-674: Boundary conditions at interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectromagneticBoundary:
    """
    Electromagnetic boundary between two media.

    Art. 663-674: This class encapsulates the boundary conditions
    that electromagnetic fields must satisfy at an interface between
    two different media.

    The boundary conditions are:
    1. Tangential E is continuous: E₁t = E₂t
    2. Normal B is continuous: B₁n = B₂n
    3. Normal D has jump: D₂n - D₁n = 4πσ (surface charge)
    4. Tangential H has jump: H₂t - H₁t = (4π/c)i (surface current)

    Attributes:
        normal: Unit normal vector from medium 1 to medium 2.
        epsilon1: Permittivity of medium 1.
        epsilon2: Permittivity of medium 2.
        mu1: Permeability of medium 1.
        mu2: Permeability of medium 2.
        sigma_s: Surface charge density (statcoulombs/cm²).
        current_s: Surface current density (abamperes/cm).
    """

    normal: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 1.0]))
    epsilon1: float = 1.0
    epsilon2: float = 1.0
    mu1: float = 1.0
    mu2: float = 1.0
    sigma_s: float = 0.0
    current_s: np.ndarray = field(default_factory=lambda: np.zeros(2))

    def __post_init__(self):
        """Validate and normalize."""
        self.normal = np.asarray(self.normal, dtype=np.float64)
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm
        else:
            raise ValueError("Normal vector cannot be zero")

        if self.epsilon1 <= 0 or self.epsilon2 <= 0:
            raise ValueError("Permittivity must be positive")
        if self.mu1 <= 0 or self.mu2 <= 0:
            raise ValueError("Permeability must be positive")

        self.current_s = np.asarray(self.current_s, dtype=np.float64)

    @classmethod
    @maxwell_cite(
        663,
        664,
        665,
        666,
        667,
        668,
        669,
        670,
        671,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create boundary with dielectric interface",
    )
    def dielectric_interface(
        cls,
        epsilon1: float,
        epsilon2: float,
        normal: np.ndarray = None,
    ) -> ElectromagneticBoundary:
        """
        Create boundary for dielectric-dielectric interface.

        Art. 663-669: For a dielectric interface with no free charges
        or currents, the boundary conditions simplify to:
        - E₁t = E₂t (tangential E continuous)
        - B₁n = B₂n (normal B continuous)
        - ε₁E₁n = ε₂E₂n (normal D continuous if σ = 0)
        - H₁t = H₂t (tangential H continuous if i = 0)

        Args:
            epsilon1: Permittivity of medium 1.
            epsilon2: Permittivity of medium 2.
            normal: Unit normal (default: z-axis).

        Returns:
            ElectromagneticBoundary object.

        Reference:
            Part IV, Arts. 663-669: Dielectric boundary conditions.
        """
        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])

        return cls(
            normal=normal,
            epsilon1=epsilon1,
            epsilon2=epsilon2,
            mu1=1.0,
            mu2=1.0,
            sigma_s=0.0,
            current_s=np.zeros(2),
        )

    @classmethod
    @maxwell_cite(
        670,
        671,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create boundary with conducting surface",
    )
    def conducting_surface(
        cls,
        epsilon: float,
        surface_current: np.ndarray,
        normal: np.ndarray = None,
    ) -> ElectromagneticBoundary:
        """
        Create boundary for perfect conductor surface.

        Art. 670-671: At a perfect conductor surface:
        - E_tangential = 0 (inside conductor)
        - B_normal = 0 (inside conductor)
        - H_tangential = (4π/c) · i (surface current)
        - D_normal = 4πσ (surface charge)

        Args:
            epsilon: Permittivity of exterior medium.
            surface_current: Surface current density (abamperes/cm).
            normal: Unit normal pointing into conductor.

        Returns:
            ElectromagneticBoundary object.

        Reference:
            Part IV, Arts. 670-671: Conductor boundary conditions.
        """
        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])

        return cls(
            normal=normal,
            epsilon1=epsilon,
            epsilon2=1.0,  # Inside conductor (reference)
            mu1=1.0,
            mu2=1.0,
            sigma_s=0.0,
            current_s=np.asarray(surface_current, dtype=np.float64),
        )


@maxwell_cite(
    663,
    664,
    665,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate tangential E field continuity at boundary",
)
def calc_tangential_E_discontinuity(
    E1: np.ndarray,
    E2: np.ndarray,
    normal: np.ndarray,
    changing_B: np.ndarray = None,
    dt: float = None,
) -> dict[str, np.ndarray | float | bool]:
    """
    Calculate tangential electric field discontinuity at boundary.

    Art. 663-665: In the absence of time-varying magnetic flux through
    an infinitesimal loop at the boundary, tangential E is continuous:

        E₁t = E₂t  or  n̂ × (E₂ - E₁) = 0

    However, if there is a time-varying magnetic field localized at
    the boundary (e.g., a magnetic shell), Faraday's law gives:

        n̂ × (E₂ - E₁) = -(1/c) · ∂B/∂t · δ

    Args:
        E1: Electric field in medium 1 (statvolts/cm).
        E2: Electric field in medium 2 (statvolts/cm).
        normal: Unit normal from medium 1 to 2.
        changing_B: Optional time-varying B at boundary (gauss/s).
        dt: Time step for B change (s).

    Returns:
        Dictionary with:
        - E1_tangential: Tangential component in medium 1
        - E2_tangential: Tangential component in medium 2
        - discontinuity: n̂ × (E₂ - E₁)
        - continuous: True if tangential E is continuous
        - faraday_term: -(1/c)·∂B/∂t if provided

    Reference:
        Part IV, Arts. 663-665: Tangential E boundary condition.

    Example:
        >>> E1 = np.array([100, 0, 50])
        >>> E2 = np.array([100, 0, -50])
        >>> n = np.array([0, 0, 1])
        >>> result = calc_tangential_E_discontinuity(E1, E2, n)
        >>> print(f"Tangential E continuous: {result['continuous']}")
    """
    normal = np.asarray(normal, dtype=np.float64)
    E1 = np.asarray(E1, dtype=np.float64)
    E2 = np.asarray(E2, dtype=np.float64)

    # Tangential components: E_t = E - (E·n̂)n̂
    E1_normal = np.dot(E1, normal) * normal
    E2_normal = np.dot(E2, normal) * normal

    E1_tangential = E1 - E1_normal
    E2_tangential = E2 - E2_normal

    # Discontinuity: n̂ × (E₂ - E₁)
    delta_E = E2 - E1
    discontinuity = np.cross(normal, delta_E)

    # Check continuity
    disc_mag = np.linalg.norm(discontinuity)
    E_tan_mag = max(np.linalg.norm(E1_tangential), np.linalg.norm(E2_tangential), 1.0)
    continuous = disc_mag < 1e-10 * E_tan_mag

    # Faraday's law term if changing B is present
    faraday_term = np.zeros(3)
    if changing_B is not None and dt is not None and dt > 0:
        dB_dt = np.asarray(changing_B, dtype=np.float64) / dt
        faraday_term = -(1.0 / CONST.C) * dB_dt

    return {
        "E1_tangential": E1_tangential,
        "E2_tangential": E2_tangential,
        "E1_normal_magnitude": np.dot(E1, normal),
        "E2_normal_magnitude": np.dot(E2, normal),
        "discontinuity": discontinuity,
        "discontinuity_magnitude": disc_mag,
        "continuous": continuous,
        "faraday_term": faraday_term,
    }


@maxwell_cite(
    666,
    667,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate normal B field continuity at boundary",
)
def calc_normal_B_continuity(
    B1: np.ndarray,
    B2: np.ndarray,
    normal: np.ndarray,
) -> dict[str, float | np.ndarray | bool]:
    """
    Calculate normal magnetic flux density continuity at boundary.

    Art. 666-667: The normal component of magnetic flux density B
    is always continuous across any boundary:

        B₁n = B₂n  or  n̂ · (B₂ - B₁) = 0

    This follows from ∇ · B = 0 applied to a pillbox at the boundary.
    There are no magnetic monopoles, so magnetic field lines must
    form closed loops and cannot begin or end at a surface.

    Args:
        B1: Magnetic flux density in medium 1 (gauss).
        B2: Magnetic flux density in medium 2 (gauss).
        normal: Unit normal from medium 1 to 2.

    Returns:
        Dictionary with:
        - B1_normal: Normal component in medium 1
        - B2_normal: Normal component in medium 2
        - difference: B₂n - B₁n
        - continuous: True if normal B is continuous
        - tangential_B1: Tangential B in medium 1
        - tangential_B2: Tangential B in medium 2

    Reference:
        Part IV, Arts. 666-667: Normal B boundary condition.

    Example:
        >>> B1 = np.array([100, 0, 500])
        >>> B2 = np.array([-100, 0, 500])
        >>> n = np.array([0, 0, 1])
        >>> result = calc_normal_B_continuity(B1, B2, n)
        >>> assert result['continuous']  # Normal B is continuous
    """
    normal = np.asarray(normal, dtype=np.float64)
    B1 = np.asarray(B1, dtype=np.float64)
    B2 = np.asarray(B2, dtype=np.float64)

    # Normal components: B_n = (B·n̂)n̂
    B1_normal_mag = np.dot(B1, normal)
    B2_normal_mag = np.dot(B2, normal)

    B1_normal = B1_normal_mag * normal
    B2_normal = B2_normal_mag * normal

    # Tangential components
    B1_tangential = B1 - B1_normal
    B2_tangential = B2 - B2_normal

    # Check continuity
    difference = B2_normal_mag - B1_normal_mag
    B_normal_mag = max(abs(B1_normal_mag), abs(B2_normal_mag), 1.0)
    continuous = abs(difference) < 1e-10 * B_normal_mag

    return {
        "B1_normal": B1_normal,
        "B2_normal": B2_normal,
        "B1_normal_magnitude": B1_normal_mag,
        "B2_normal_magnitude": B2_normal_mag,
        "difference": difference,
        "continuous": continuous,
        "B1_tangential": B1_tangential,
        "B2_tangential": B2_tangential,
    }


@maxwell_cite(
    668,
    669,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate normal D field discontinuity at boundary",
)
def calc_normal_D_discontinuity(
    D1: np.ndarray,
    D2: np.ndarray,
    normal: np.ndarray,
    surface_charge: float = None,
) -> dict[str, float | np.ndarray | bool]:
    """
    Calculate normal electric displacement discontinuity at boundary.

    Art. 668-669: The normal component of electric displacement D
    has a discontinuity proportional to the free surface charge density:

        D₂n - D₁n = 4πσ  or  n̂ · (D₂ - D₁) = 4πσ

    This follows from Gauss's law ∇ · D = 4πρ applied to a pillbox
    at the charged surface.

    In terms of E field:
        ε₂E₂n - ε₁E₁n = 4πσ

    Args:
        D1: Electric displacement in medium 1 (statcoulombs/cm²).
        D2: Electric displacement in medium 2 (statcoulombs/cm²).
        normal: Unit normal from medium 1 to 2.
        surface_charge: Free surface charge σ (statcoulombs/cm²).

    Returns:
        Dictionary with:
        - D1_normal: Normal component in medium 1
        - D2_normal: Normal component in medium 2
        - difference: D₂n - D₁n
        - expected_jump: 4πσ
        - gauss_satisfied: True if boundary condition holds
        - inferred_charge: Surface charge from D jump

    Reference:
        Part IV, Arts. 668-669: Normal D boundary condition.

    Example:
        >>> D1 = np.array([0, 0, 100])
        >>> D2 = np.array([0, 0, 200])
        >>> n = np.array([0, 0, 1])
        >>> result = calc_normal_D_discontinuity(D1, D2, n)
        >>> print(f"Inferred σ = {result['inferred_charge']} statC/cm²")
    """
    normal = np.asarray(normal, dtype=np.float64)
    D1 = np.asarray(D1, dtype=np.float64)
    D2 = np.asarray(D2, dtype=np.float64)

    # Normal components
    D1_normal_mag = np.dot(D1, normal)
    D2_normal_mag = np.dot(D2, normal)

    D1_normal = D1_normal_mag * normal
    D2_normal = D2_normal_mag * normal

    # Tangential components
    D1_tangential = D1 - D1_normal
    D2_tangential = D2 - D2_normal

    # Discontinuity
    difference = D2_normal_mag - D1_normal_mag

    # Expected jump from surface charge
    if surface_charge is not None:
        expected_jump = 4.0 * np.pi * surface_charge
        gauss_tolerance = 1e-8 * max(abs(expected_jump), 1.0)
        gauss_satisfied = abs(difference - expected_jump) < gauss_tolerance
    else:
        expected_jump = None
        gauss_satisfied = None

    # Inferred surface charge
    inferred_charge = difference / (4.0 * np.pi)

    return {
        "D1_normal": D1_normal,
        "D2_normal": D2_normal,
        "D1_normal_magnitude": D1_normal_mag,
        "D2_normal_magnitude": D2_normal_mag,
        "difference": difference,
        "expected_jump": expected_jump,
        "gauss_satisfied": gauss_satisfied,
        "inferred_charge": inferred_charge,
        "D1_tangential": D1_tangential,
        "D2_tangential": D2_tangential,
    }


@maxwell_cite(
    670,
    671,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate tangential H field discontinuity at boundary",
)
def calc_tangential_H_discontinuity(
    H1: np.ndarray,
    H2: np.ndarray,
    normal: np.ndarray,
    surface_current: np.ndarray = None,
) -> dict[str, np.ndarray | float | bool]:
    """
    Calculate tangential magnetic field discontinuity at boundary.

    Art. 670-671: The tangential component of magnetic field H has
    a discontinuity proportional to the free surface current density:

        n̂ × (H₂ - H₁) = (4π/c) · i  or  H₂t - H₁t = (4π/c) · (n̂ × i)

    This follows from Ampere's law ∇ × H = (4π/c)J applied to a
    small loop at the current-carrying surface.

    In terms of B field (in linear media):
        B₂t/μ₂ - B₁t/μ₁ = (4π/c) · i

    Args:
        H1: Magnetic field in medium 1 (oersted).
        H2: Magnetic field in medium 2 (oersted).
        normal: Unit normal from medium 1 to 2.
        surface_current: Surface current density i (abamperes/cm).

    Returns:
        Dictionary with:
        - H1_tangential: Tangential component in medium 1
        - H2_tangential: Tangential component in medium 2
        - discontinuity: n̂ × (H₂ - H₁)
        - expected_jump: (4π/c) · i
        - boundary_satisfied: True if condition holds
        - inferred_current: Surface current from H jump

    Reference:
        Part IV, Arts. 670-671: Tangential H boundary condition.

    Example:
        >>> H1 = np.array([0, 0, 100])
        >>> H2 = np.array([0, 50, 100])
        >>> n = np.array([0, 0, 1])
        >>> i = np.array([100, 0])  # abamperes/cm
        >>> result = calc_tangential_H_discontinuity(H1, H2, n, i)
        >>> print(f"Boundary satisfied: {result['boundary_satisfied']}")
    """
    normal = np.asarray(normal, dtype=np.float64)
    H1 = np.asarray(H1, dtype=np.float64)
    H2 = np.asarray(H2, dtype=np.float64)

    # Tangential components: H_t = H - (H·n̂)n̂
    H1_normal = np.dot(H1, normal) * normal
    H2_normal = np.dot(H2, normal) * normal

    H1_tangential = H1 - H1_normal
    H2_tangential = H2 - H2_normal

    # Discontinuity: n̂ × (H₂ - H₁)
    delta_H = H2 - H1
    discontinuity = np.cross(normal, delta_H)

    # Expected jump from surface current
    if surface_current is not None:
        i_vec = np.asarray(surface_current, dtype=np.float64)
        # Extend to 3D (current in tangent plane)
        if len(i_vec) == 2:
            # Assume current is in xy-plane for z-normal
            i_3d = np.array([i_vec[0], i_vec[1], 0.0])
        else:
            i_3d = i_vec

        expected_jump = (4.0 * np.pi / CONST.C) * i_3d

        jump_tolerance = 1e-8 * max(np.linalg.norm(expected_jump), 1.0)
        boundary_satisfied = (
            np.linalg.norm(discontinuity - expected_jump) < jump_tolerance
        )

        # Inferred surface current
        # From n̂ × ΔH = (4π/c) · i, we get i = (c/4π) · (n̂ × ΔH)
        inferred_current = (CONST.C / (4.0 * np.pi)) * discontinuity
    else:
        expected_jump = None
        boundary_satisfied = np.linalg.norm(discontinuity) < 1e-10
        inferred_current = None

    return {
        "H1_tangential": H1_tangential,
        "H2_tangential": H2_tangential,
        "H1_normal_magnitude": np.dot(H1, normal),
        "H2_normal_magnitude": np.dot(H2, normal),
        "discontinuity": discontinuity,
        "discontinuity_magnitude": np.linalg.norm(discontinuity),
        "expected_jump": expected_jump,
        "boundary_satisfied": boundary_satisfied,
        "inferred_current": (
            inferred_current[:2] if inferred_current is not None else None
        ),
    }


@maxwell_cite(
    663,
    664,
    665,
    666,
    667,
    668,
    669,
    670,
    671,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Verify all electromagnetic boundary conditions",
)
def verify_boundary_conditions(
    boundary: ElectromagneticBoundary,
    E1: np.ndarray,
    B1: np.ndarray,
    E2: np.ndarray,
    B2: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, bool | dict]:
    """
    Verify all electromagnetic boundary conditions at an interface.

    Art. 663-671: This function performs a comprehensive check of all
    four electromagnetic boundary conditions:

    1. Tangential E continuity: n̂ × (E₂ - E₁) = 0
    2. Normal B continuity: n̂ · (B₂ - B₁) = 0
    3. Normal D discontinuity: n̂ · (D₂ - D₁) = 4πσ
    4. Tangential H discontinuity: n̂ × (H₂ - H₁) = (4π/c)i

    Args:
        boundary: ElectromagneticBoundary object defining the interface.
        E1: Electric field in medium 1 (statvolts/cm).
        B1: Magnetic flux density in medium 1 (gauss).
        E2: Electric field in medium 2 (statvolts/cm).
        B2: Magnetic flux density in medium 2 (gauss).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - all_satisfied: True if all boundary conditions hold
        - tangential_E: Tangential E condition results
        - normal_B: Normal B condition results
        - normal_D: Normal D condition results
        - tangential_H: Tangential H condition results

    Reference:
        Part IV, Arts. 663-671: Complete boundary condition verification.

    Example:
        >>> boundary = ElectromagneticBoundary.dielectric_interface(1.0, 2.0)
        >>> E1 = np.array([100, 0, 50])
        >>> B1 = np.array([0, 100, 500])
        >>> E2 = np.array([100, 0, 25])  # Normal E changes
        >>> B2 = np.array([0, 100, 500])  # Normal B same
        >>> result = verify_boundary_conditions(boundary, E1, B1, E2, B2)
        >>> assert result['all_satisfied']
    """
    n = boundary.normal

    # Compute D and H from E and B
    D1 = boundary.epsilon1 * E1
    D2 = boundary.epsilon2 * E2
    H1 = B1 / boundary.mu1
    H2 = B2 / boundary.mu2

    results = {}
    all_satisfied = True

    # 1. Tangential E continuity
    E_result = calc_tangential_E_discontinuity(E1, E2, n)
    results["tangential_E"] = E_result
    all_satisfied = all_satisfied and E_result["continuous"]

    # 2. Normal B continuity
    B_result = calc_normal_B_continuity(B1, B2, n)
    results["normal_B"] = B_result
    all_satisfied = all_satisfied and B_result["continuous"]

    # 3. Normal D discontinuity
    D_result = calc_normal_D_discontinuity(D1, D2, n, boundary.sigma_s)
    results["normal_D"] = D_result
    if D_result["gauss_satisfied"] is not None:
        all_satisfied = all_satisfied and D_result["gauss_satisfied"]

    # 4. Tangential H discontinuity
    H_result = calc_tangential_H_discontinuity(H1, H2, n, boundary.current_s)
    results["tangential_H"] = H_result
    all_satisfied = all_satisfied and H_result["boundary_satisfied"]

    results["all_satisfied"] = all_satisfied
    results["boundary"] = boundary

    return results


@maxwell_cite(
    672,
    673,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate boundary conditions for moving media",
)
def calc_moving_boundary_conditions(
    boundary: ElectromagneticBoundary,
    velocity: np.ndarray,
    E1: np.ndarray,
    B1: np.ndarray,
    E2: np.ndarray,
    B2: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Calculate boundary conditions for a moving interface.

    Art. 672-673: When the boundary between media moves with velocity v,
    the electromagnetic fields transform. The boundary conditions become:

        n̂ × (E₂ - E₁) = (v/c) · [n̂ × (B₂ - B₁)]
        n̂ · (B₂ - B₁) = 0  (unchanged)

    The motional EMF term (v/c) × B modifies the tangential E condition.

    Args:
        boundary: ElectromagneticBoundary object.
        velocity: Velocity of boundary (cm/s).
        E1: Electric field in medium 1 (statvolts/cm).
        B1: Magnetic flux density in medium 1 (gauss).
        E2: Electric field in medium 2 (statvolts/cm).
        B2: Magnetic flux density in medium 2 (gauss).

    Returns:
        Dictionary with:
        - modified_E_discontinuity: Including motional term
        - motional_emf: (v/c) × B contribution
        - normal_B: Normal B continuity (unchanged)
        - effective_E1: E₁ + (v/c) × B₁
        - effective_E2: E₂ + (v/c) × B₂

    Reference:
        Part IV, Arts. 672-673: Moving media boundary conditions.

    Example:
        >>> boundary = ElectromagneticBoundary.dielectric_interface(1.0, 2.0)
        >>> v = np.array([1e6, 0, 0])  # Moving in x-direction
        >>> result = calc_moving_boundary_conditions(boundary, v, E1, B1, E2, B2)
    """
    n = boundary.normal
    v = np.asarray(velocity, dtype=np.float64)
    E1 = np.asarray(E1, dtype=np.float64)
    B1 = np.asarray(B1, dtype=np.float64)
    E2 = np.asarray(E2, dtype=np.float64)
    B2 = np.asarray(B2, dtype=np.float64)

    # Motional EMF terms
    v_cross_B1 = np.cross(v, B1)
    v_cross_B2 = np.cross(v, B2)

    # Effective fields in moving frame
    E1_effective = E1 + (1.0 / CONST.C) * v_cross_B1
    E2_effective = E2 + (1.0 / CONST.C) * v_cross_B2

    # Modified tangential E discontinuity
    delta_E_effective = E2_effective - E1_effective
    modified_discontinuity = np.cross(n, delta_E_effective)

    # Normal B (unchanged)
    B_result = calc_normal_B_continuity(B1, B2, n)

    return {
        "modified_E_discontinuity": modified_discontinuity,
        "motional_emf_medium1": (1.0 / CONST.C) * v_cross_B1,
        "motional_emf_medium2": (1.0 / CONST.C) * v_cross_B2,
        "effective_E1": E1_effective,
        "effective_E2": E2_effective,
        "normal_B": B_result,
        "velocity": velocity,
    }


@maxwell_cite(
    674,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate energy flux (Poynting vector) at boundary",
)
def calc_boundary_energy_flux(
    E: np.ndarray,
    B: np.ndarray,
    normal: np.ndarray,
    medium_epsilon: float = 1.0,
    medium_mu: float = 1.0,
) -> dict[str, float | np.ndarray]:
    """
    Calculate electromagnetic energy flux at a boundary.

    Art. 674: The energy flux (Poynting vector) at a boundary determines
    the rate of energy transfer between media:

        S = (c/4π) · (E × H) = (c/4πμ) · (E × B)

    The normal component S · n̂ gives the energy flow across the boundary.

    In CGS:
        S in erg/(cm²·s)
        E in statvolts/cm
        B in gauss

    Args:
        E: Electric field at boundary (statvolts/cm).
        B: Magnetic flux density at boundary (gauss).
        normal: Unit normal to boundary.
        medium_epsilon: Permittivity of medium.
        medium_mu: Permeability of medium.

    Returns:
        Dictionary with:
        - poynting_vector: S (erg/(cm²·s))
        - normal_flux: S · n̂ (energy crossing boundary)
        - tangential_flux: Tangential component of S
        - energy_density: u = (εE² + B²/μ)/(8π)

    Reference:
        Part IV, Art. 674: Energy flux at boundaries.

    Example:
        >>> E = np.array([100, 0, 0])
        >>> B = np.array([0, 100, 0])
        >>> n = np.array([0, 0, 1])
        >>> result = calc_boundary_energy_flux(E, B, n)
        >>> print(f"Energy flux: {result['normal_flux']} erg/(cm²·s)")
    """
    E = np.asarray(E, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    normal = np.asarray(normal, dtype=np.float64)

    # H field
    H = B / medium_mu

    # Poynting vector: S = (c/4π) · (E × H)
    E_cross_H = np.cross(E, H)
    S = (CONST.C / (4.0 * np.pi)) * E_cross_H

    # Normal component (energy crossing boundary)
    normal_flux = np.dot(S, normal)

    # Tangential component
    S_normal = normal_flux * normal
    tangential_flux = S - S_normal

    # Energy density: u = (εE² + B²/μ)/(8π)
    E_sq = np.dot(E, E)
    B_sq = np.dot(B, B)
    energy_density = (medium_epsilon * E_sq + B_sq / medium_mu) / (8.0 * np.pi)

    return {
        "poynting_vector": S,
        "normal_flux": normal_flux,
        "tangential_flux": tangential_flux,
        "energy_density": energy_density,
        "poynting_magnitude": np.linalg.norm(S),
    }


@dataclass
class BoundaryConditionAnalyzer:
    """
    Comprehensive analyzer for electromagnetic boundary conditions.

    Art. 663-674: This class provides a unified interface for all
    boundary condition calculations at interfaces between media.

    Attributes:
        boundary: ElectromagneticBoundary object.
    """

    boundary: ElectromagneticBoundary

    @maxwell_cite(
        663,
        664,
        665,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Check tangential E continuity",
    )
    def check_tangential_E(self, E1: np.ndarray, E2: np.ndarray) -> dict:
        """Check tangential electric field continuity."""
        return calc_tangential_E_discontinuity(E1, E2, self.boundary.normal)

    @maxwell_cite(
        666,
        667,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Check normal B continuity",
    )
    def check_normal_B(self, B1: np.ndarray, B2: np.ndarray) -> dict:
        """Check normal magnetic flux continuity."""
        return calc_normal_B_continuity(B1, B2, self.boundary.normal)

    @maxwell_cite(
        668,
        669,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Check normal D discontinuity",
    )
    def check_normal_D(self, D1: np.ndarray, D2: np.ndarray) -> dict:
        """Check normal electric displacement discontinuity."""
        return calc_normal_D_discontinuity(
            D1, D2, self.boundary.normal, self.boundary.sigma_s
        )

    @maxwell_cite(
        670,
        671,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Check tangential H discontinuity",
    )
    def check_tangential_H(self, H1: np.ndarray, H2: np.ndarray) -> dict:
        """Check tangential magnetic field discontinuity."""
        return calc_tangential_H_discontinuity(
            H1, H2, self.boundary.normal, self.boundary.current_s
        )

    @maxwell_cite(
        663,
        664,
        665,
        666,
        667,
        668,
        669,
        670,
        671,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Verify all boundary conditions",
    )
    def verify_all(
        self,
        E1: np.ndarray,
        B1: np.ndarray,
        E2: np.ndarray,
        B2: np.ndarray,
    ) -> dict:
        """Verify all electromagnetic boundary conditions."""
        return verify_boundary_conditions(self.boundary, E1, B1, E2, B2)

    @maxwell_cite(
        672,
        673,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Analyze moving boundary",
    )
    def analyze_moving_boundary(
        self,
        velocity: np.ndarray,
        E1: np.ndarray,
        B1: np.ndarray,
        E2: np.ndarray,
        B2: np.ndarray,
    ) -> dict:
        """Analyze boundary conditions for moving interface."""
        return calc_moving_boundary_conditions(self.boundary, velocity, E1, B1, E2, B2)

    @maxwell_cite(
        674,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate energy flux",
    )
    def energy_flux(
        self,
        E: np.ndarray,
        B: np.ndarray,
        medium: int = 1,
    ) -> dict:
        """Calculate Poynting vector at boundary."""
        if medium == 1:
            eps = self.boundary.epsilon1
            mu = self.boundary.mu1
        else:
            eps = self.boundary.epsilon2
            mu = self.boundary.mu2

        return calc_boundary_energy_flux(E, B, self.boundary.normal, eps, mu)
