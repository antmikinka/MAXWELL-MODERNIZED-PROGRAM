"""
Magnetic spheres — analytical solutions for spherical magnetic bodies.

Implements the theory of magnetic spheres from Part III of Maxwell's Treatise:
- Uniformly magnetized sphere (Arts. 431-433)
- Sphere in external field (Art. 434)
- Hollow magnetic sphere (Arts. 435-436)

The sphere is the most symmetric magnetic body and admits complete
analytical solutions. Key results include:
- External field of uniformly magnetized sphere = dipole field
- Demagnetizing factor N = 4π/3 (CGS) for sphere
- Induced magnetization in uniform field is uniform

Category: A (maxwell_original) — Maxwell's theory of magnetic spheres.

References:
    Part III, Arts. 431-436: Magnetic spheres.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.magnet import Magnet
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticSphere:
    """
    Spherical magnetic body with uniform magnetization.

    Arts. 431-433: A sphere of radius R with uniform magnetization
    I produces:
    - Inside: Uniform field H = -(4π/3)I
    - Outside: Pure dipole field with m = (4πR³/3)I

    The sphere is special because the demagnetizing field is
    uniform, making the induced magnetization uniform when
    placed in a uniform external field.

    Attributes:
        radius: Sphere radius R (cm).
        magnetization: Uniform magnetization I (emu/cm³).
        center: Center position (cm).
    """

    radius: float  # R, cm
    magnetization: np.ndarray = None  # I, emu/cm³, shape (3,)
    center: np.ndarray = None  # center, cm, shape (3,)

    def __post_init__(self):
        self.center = (
            np.asarray(self.center, dtype=np.float64)
            if self.center is not None
            else np.zeros(3)
        )
        self.magnetization = (
            np.asarray(self.magnetization, dtype=np.float64)
            if self.magnetization is not None
            else np.zeros(3)
        )

    @property
    def volume(self) -> float:
        """Volume of sphere: V = (4/3)πR³."""
        return (4 / 3) * np.pi * self.radius**3

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment: m = I × V."""
        return self.magnetization * self.volume

    @maxwell_cite(
        431,
        part=3,
        chapter="Magnetic Spheres",
        theory_class="maxwell_original",
        description="Calculate external field of magnetized sphere",
    )
    def external_field(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field outside uniformly magnetized sphere.

        Art. 431: Outside the sphere (r > R), the field is exactly
        that of a point dipole at the center with moment m = IV:

            H(r) = (3(m·r̂)r̂ - m) / r³

        Args:
            position: Point to evaluate (cm).

        Returns:
            Magnetic field H (gauss).

        Reference:
            Part III, Art. 431: External field of sphere.
        """
        position = np.asarray(position, dtype=np.float64)
        r = position - self.center
        r_mag = np.linalg.norm(r)

        if r_mag <= self.radius:
            # Inside sphere - use internal field formula
            return self.internal_field(position)

        r_hat = r / r_mag
        m = self.total_magnetic_moment

        # Dipole field
        H = (3 * np.dot(m, r_hat) * r_hat - m) / (r_mag**3)

        return H

    @maxwell_cite(
        432,
        part=3,
        chapter="Magnetic Spheres",
        theory_class="maxwell_original",
        description="Calculate internal field of magnetized sphere",
    )
    def internal_field(self, position: np.ndarray = None) -> np.ndarray:
        """
        Calculate magnetic field inside uniformly magnetized sphere.

        Art. 432: Inside the sphere (r < R), the field is uniform:

            H = -(4π/3) × I

        This is the demagnetizing field. The negative sign means
        it opposes the magnetization.

        Args:
            position: Point inside sphere (unused, field is uniform).

        Returns:
            Uniform internal field H (gauss).

        Reference:
            Part III, Art. 432: Internal field of sphere.
        """
        # Uniform demagnetizing field
        N = 4 * np.pi / 3  # Demagnetizing factor for sphere
        return -N * self.magnetization

    @maxwell_cite(
        431,
        part=3,
        chapter="Magnetic Spheres",
        theory_class="maxwell_original",
        description="Calculate scalar potential of magnetized sphere",
    )
    def scalar_potential(self, position: np.ndarray) -> float:
        """
        Calculate magnetic scalar potential of sphere.

        Art. 431: The potential outside a uniformly magnetized
        sphere is:

            Ω(r) = (m·r) / r³

        Inside, the potential is linear in coordinates:
            Ω(r) = -(4π/3)I·r

        Args:
            position: Point to evaluate (cm).

        Returns:
            Scalar potential Ω (gauss·cm).

        Reference:
            Part III, Art. 431: Sphere potential.
        """
        position = np.asarray(position, dtype=np.float64)
        r = position - self.center
        r_mag = np.linalg.norm(r)

        if r_mag <= self.radius:
            # Inside: linear potential
            return -float((4 * np.pi / 3) * np.dot(self.magnetization, r))
        else:
            # Outside: dipole potential
            return float(np.dot(self.total_magnetic_moment, r) / (r_mag**3))

    @classmethod
    @maxwell_cite(
        433,
        part=3,
        chapter="Magnetic Spheres",
        theory_class="maxwell_original",
        description="Create sphere from total magnetic moment",
    )
    def from_magnetic_moment(
        cls,
        radius: float,
        total_moment: np.ndarray,
        center: np.ndarray = None,
    ) -> MagneticSphere:
        """
        Create magnetic sphere from total magnetic moment.

        Art. 433: Given total moment m and radius R, the uniform
        magnetization is:

            I = m / V = 3m / (4πR³)

        Args:
            radius: Sphere radius R (cm).
            total_moment: Total magnetic moment m (emu).
            center: Center position (cm).

        Returns:
            MagneticSphere object.

        Reference:
            Part III, Art. 433: Sphere from moment.
        """
        volume = (4 / 3) * np.pi * radius**3
        magnetization = np.asarray(total_moment, dtype=np.float64) / volume

        return cls(
            radius=radius,
            magnetization=magnetization,
            center=center,
        )

    @classmethod
    @maxwell_cite(
        434,
        part=3,
        chapter="Magnetic Spheres",
        theory_class="maxwell_original",
        description="Create induced sphere in external field",
    )
    def in_uniform_field(
        cls,
        radius: float,
        susceptibility: float,
        external_field: np.ndarray,
        center: np.ndarray = None,
    ) -> MagneticSphere:
        """
        Create sphere with induced magnetization in uniform field.

        Art. 434: When a sphere of susceptibility κ is placed in
        a uniform external field H_ext, the induced magnetization
        is uniform and given by:

            I = κ H_ext / (1 + 4πκ/3)

        The denominator accounts for the demagnetizing field.

        Args:
            radius: Sphere radius R (cm).
            susceptibility: Magnetic susceptibility κ.
            external_field: Applied field H_ext (gauss).
            center: Center position (cm).

        Returns:
            MagneticSphere with induced magnetization.

        Reference:
            Part III, Art. 434: Induced sphere.
        """
        H_ext = np.asarray(external_field, dtype=np.float64)

        # Demagnetizing factor for sphere
        N = 4 * np.pi / 3

        # Induced magnetization (reduced by demagnetizing field)
        magnetization = susceptibility * H_ext / (1 + N * susceptibility)

        return cls(
            radius=radius,
            magnetization=magnetization,
            center=center,
        )


@maxwell_cite(
    431,
    part=3,
    chapter="Magnetic Spheres",
    theory_class="maxwell_original",
    description="Calculate field of uniformly magnetized sphere",
)
def sphere_field(
    radius: float,
    magnetization: np.ndarray,
    position: np.ndarray,
    center: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate magnetic field of uniformly magnetized sphere.

    Art. 431-432: The field of a uniformly magnetized sphere is:

    Outside (r > R):
        H = (3(m·r̂)r̂ - m) / r³  where m = (4πR³/3)I

    Inside (r < R):
        H = -(4π/3)I  (uniform demagnetizing field)

    Args:
        radius: Sphere radius R (cm).
        magnetization: Uniform magnetization I (emu/cm³).
        position: Point to evaluate (cm).
        center: Sphere center (cm).

    Returns:
        Magnetic field H (gauss).

    Reference:
        Part III, Arts. 431-432: Sphere field.
    """
    if center is None:
        center = np.zeros(3)

    sphere = MagneticSphere(
        radius=radius,
        magnetization=magnetization,
        center=center,
    )

    return (
        sphere.external_field(position)
        if np.linalg.norm(position - center) > radius
        else sphere.internal_field(position)
    )


@maxwell_cite(
    432,
    part=3,
    chapter="Magnetic Spheres",
    theory_class="maxwell_original",
    description="Calculate demagnetizing field of sphere",
)
def sphere_demagnetizing_field(
    magnetization: np.ndarray,
) -> np.ndarray:
    """
    Calculate demagnetizing field inside uniformly magnetized sphere.

    Art. 432: The demagnetizing field inside a sphere is:

        H_d = -N I  where N = 4π/3

    This uniform field opposes the magnetization.

    Args:
        magnetization: Magnetization I (emu/cm³).

    Returns:
        Demagnetizing field H_d (gauss).

    Reference:
        Part III, Art. 432: Sphere demagnetizing field.
    """
    N = 4 * np.pi / 3
    return -N * np.asarray(magnetization, dtype=np.float64)


@maxwell_cite(
    433,
    part=3,
    chapter="Magnetic Spheres",
    theory_class="maxwell_original",
    description="Calculate equivalent dipole moment of sphere",
)
def sphere_equivalent_dipole(
    radius: float,
    magnetization: np.ndarray,
) -> np.ndarray:
    """
    Calculate equivalent dipole moment of uniformly magnetized sphere.

    Art. 433: A uniformly magnetized sphere is equivalent to a
    point dipole at its center with moment:

        m = I × V = I × (4πR³/3)

    Args:
        radius: Sphere radius R (cm).
        magnetization: Magnetization I (emu/cm³).

    Returns:
        Magnetic moment m (emu).

    Reference:
        Part III, Art. 433: Equivalent dipole.
    """
    volume = (4 / 3) * np.pi * radius**3
    return np.asarray(magnetization, dtype=np.float64) * volume


@maxwell_cite(
    434,
    part=3,
    chapter="Magnetic Spheres",
    theory_class="maxwell_original",
    description="Calculate induced magnetization of sphere in field",
)
def sphere_induced_magnetization(
    susceptibility: float,
    external_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate induced magnetization of sphere in uniform field.

    Art. 434: For a sphere with susceptibility κ in uniform
    field H_ext:

        I = κ H_ext / (1 + 4πκ/3)

    The factor (1 + 4πκ/3) accounts for the demagnetizing field
    which reduces the effective field inside.

    Args:
        susceptibility: Magnetic susceptibility κ.
        external_field: Applied field H_ext (gauss).

    Returns:
        Induced magnetization I (emu/cm³).

    Reference:
        Part III, Art. 434: Induced sphere magnetization.
    """
    H_ext = np.asarray(external_field, dtype=np.float64)
    N = 4 * np.pi / 3

    return susceptibility * H_ext / (1 + N * susceptibility)


@dataclass
class HollowMagneticSphere:
    """
    Hollow spherical shell with uniform magnetization.

    Arts. 435-436: A hollow sphere (spherical shell) with inner
    radius a and outer radius b, uniformly magnetized with I:

    - Cavity (r < a): Zero field (magnetic shielding)
    - Shell (a < r < b): H = -(4π/3)I (uniform)
    - Outside (r > b): Dipole field with m = (4π/3)(b³-a³)I

    The hollow sphere provides magnetic shielding: the field
    inside the cavity is zero regardless of external fields.

    Attributes:
        inner_radius: Inner radius a (cm).
        outer_radius: Outer radius b (cm).
        magnetization: Uniform magnetization I (emu/cm³).
        center: Center position (cm).
    """

    inner_radius: float  # a, cm
    outer_radius: float  # b, cm
    magnetization: np.ndarray = None
    center: np.ndarray = None

    def __post_init__(self):
        self.center = (
            np.asarray(self.center, dtype=np.float64)
            if self.center is not None
            else np.zeros(3)
        )
        self.magnetization = (
            np.asarray(self.magnetization, dtype=np.float64)
            if self.magnetization is not None
            else np.zeros(3)
        )

    @property
    def shell_volume(self) -> float:
        """Volume of shell material: V = (4/3)π(b³ - a³)."""
        return (4 / 3) * np.pi * (self.outer_radius**3 - self.inner_radius**3)

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment: m = I × V_shell."""
        return self.magnetization * self.shell_volume

    @maxwell_cite(
        435,
        part=3,
        chapter="Hollow Magnetic Spheres",
        theory_class="maxwell_original",
        description="Calculate field of hollow magnetized sphere",
    )
    def field(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field of hollow uniformly magnetized sphere.

        Art. 435: The field at any point:

        - Cavity (r < a): H = 0
        - Shell (a < r < b): H = -(4π/3)I
        - Outside (r > b): Dipole field

        Args:
            position: Point to evaluate (cm).

        Returns:
            Magnetic field H (gauss).

        Reference:
            Part III, Art. 435: Hollow sphere field.
        """
        position = np.asarray(position, dtype=np.float64)
        r = position - self.center
        r_mag = np.linalg.norm(r)

        if r_mag < self.inner_radius:
            # Cavity: zero field
            return np.zeros(3)

        elif r_mag < self.outer_radius:
            # Inside shell material: uniform demagnetizing field
            N = 4 * np.pi / 3
            return -N * self.magnetization

        else:
            # Outside: dipole field
            r_hat = r / r_mag
            m = self.total_magnetic_moment
            return (3 * np.dot(m, r_hat) * r_hat - m) / (r_mag**3)

    @maxwell_cite(
        436,
        part=3,
        chapter="Hollow Magnetic Spheres",
        theory_class="maxwell_original",
        description="Calculate shielding factor of hollow sphere",
    )
    def shielding_factor(self, susceptibility: float = None) -> float:
        """
        Calculate magnetic shielding factor of hollow sphere.

        Art. 436: For a hollow sphere of high-permeability material
        in an external field, the shielding factor S is the ratio
        of external field to internal field:

            S = H_out / H_in = 1 + (2/9) × μ_r × (1 - (a/b)³)

        where μ_r = 1 + 4πκ is relative permeability.

        For μ_r >> 1 and thick shell: S ≈ (2/9) μ_r

        Args:
            susceptibility: κ of shell material (for shielding calc).

        Returns:
            Shielding factor S (dimensionless).

        Reference:
            Part III, Art. 436: Magnetic shielding.
        """
        if susceptibility is None:
            # For permanent magnetization, return geometric factor
            return float(
                self.outer_radius**3 / (self.outer_radius**3 - self.inner_radius**3)
            )

        # Relative permeability
        mu_r = 1 + 4 * np.pi * susceptibility

        # Shielding factor
        ratio = (self.inner_radius / self.outer_radius) ** 3
        S = 1 + (2 / 9) * mu_r * (1 - ratio)

        return float(S)

    @classmethod
    @maxwell_cite(
        436,
        part=3,
        chapter="Hollow Magnetic Spheres",
        theory_class="maxwell_original",
        description="Create hollow sphere for magnetic shielding",
    )
    def for_magnetic_shielding(
        cls,
        inner_radius: float,
        susceptibility: float,
        target_shielding: float,
    ) -> HollowMagneticSphere:
        """
        Design hollow sphere for specified magnetic shielding.

        Art. 436: Given desired shielding factor S and material
        susceptibility κ, determine required outer radius.

        From: S = 1 + (2/9)μ_r(1 - (a/b)³)

        Solve for b/a:
            (b/a)³ = 1 / (1 - 9(S-1)/(2μ_r))

        Args:
            inner_radius: Inner cavity radius a (cm).
            susceptibility: Material susceptibility κ.
            target_shielding: Desired shielding factor S.

        Returns:
            HollowMagneticSphere object.

        Reference:
            Part III, Art. 436: Shielding design.
        """
        mu_r = 1 + 4 * np.pi * susceptibility

        # Solve for outer radius
        # S = 1 + (2/9) * mu_r * (1 - (a/b)^3)
        # (S-1) * 9 / (2 * mu_r) = 1 - (a/b)^3
        # (a/b)^3 = 1 - 9(S-1)/(2*mu_r)
        # b = a / (1 - 9(S-1)/(2*mu_r))^(1/3)

        term = 1 - 9 * (target_shielding - 1) / (2 * mu_r)

        if term <= 0:
            # Cannot achieve with this material
            raise ValueError(
                f"Shielding factor {target_shielding} not achievable "
                f"with susceptibility {susceptibility}"
            )

        outer_radius = inner_radius / (term ** (1 / 3))

        return cls(
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            magnetization=np.zeros(3),  # For shielding, magnetization is induced
            center=np.zeros(3),
        )


@maxwell_cite(
    435,
    436,
    part=3,
    chapter="Hollow Magnetic Spheres",
    theory_class="maxwell_original",
    description="Calculate field inside hollow sphere in external field",
)
def hollow_sphere_in_field(
    inner_radius: float,
    outer_radius: float,
    susceptibility: float,
    external_field: np.ndarray,
    position: np.ndarray,
    center: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate field inside hollow sphere placed in external field.

    Arts. 435-436: A hollow sphere of susceptibility κ in uniform
    external field H_ext produces a reduced field inside the cavity:

        H_cavity = H_ext / S

    where S is the shielding factor.

    Args:
        inner_radius: Inner radius a (cm).
        outer_radius: Outer radius b (cm).
        susceptibility: Material susceptibility κ.
        external_field: Applied field H_ext (gauss).
        position: Point inside cavity (cm).
        center: Sphere center (cm).

    Returns:
        Field inside cavity H (gauss).

    Reference:
        Part III, Arts. 435-436: Hollow sphere in field.
    """
    if center is None:
        center = np.zeros(3)

    # Check if position is inside cavity
    r = np.asarray(position, dtype=np.float64) - center
    r_mag = np.linalg.norm(r)

    if r_mag >= inner_radius:
        # Not in cavity - use full solution
        # (simplified: just return external field)
        return np.asarray(external_field, dtype=np.float64)

    # Calculate shielding factor
    mu_r = 1 + 4 * np.pi * susceptibility
    ratio = (inner_radius / outer_radius) ** 3
    S = 1 + (2 / 9) * mu_r * (1 - ratio)

    # Field in cavity is uniform and reduced
    H_ext = np.asarray(external_field, dtype=np.float64)
    return H_ext / S


@maxwell_cite(
    431,
    432,
    433,
    434,
    435,
    436,
    part=3,
    chapter="Magnetic Spheres",
    theory_class="maxwell_original",
    description="Verify sphere magnetism calculations",
)
def verify_sphere_magnetism() -> dict[str, any]:
    """
    Verify analytical formulas for magnetic spheres.

    Arts. 431-436: Test cases:

    1. Sphere external field = dipole field
    2. Sphere internal field = -(4π/3)I
    3. Induced magnetization formula
    4. Hollow sphere cavity field = 0

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Arts. 431-436: Sphere verification.
    """
    results = {}

    # Test 1: External field equals dipole field
    R = 1.0
    I = np.array([0, 0, 1000])  # emu/cm³
    sphere = MagneticSphere(radius=R, magnetization=I)

    # Point outside sphere
    pos = np.array([0, 0, 3])  # 3 cm from center

    H_sphere = sphere.external_field(pos)

    # Dipole field at same point
    m = sphere.total_magnetic_moment
    r = 3.0
    H_dipole = np.array([0, 0, -m[2] / r**3])  # On axis, H = -m/r³

    match = np.allclose(H_sphere, H_dipole, rtol=1e-6)

    results["external_field_dipole"] = {
        "sphere_field": H_sphere.tolist(),
        "dipole_field": H_dipole.tolist(),
        "match": match,
    }

    # Test 2: Internal field = -(4π/3)I
    H_internal = sphere.internal_field()
    expected = -(4 * np.pi / 3) * I
    internal_match = np.allclose(H_internal, expected)

    results["internal_field"] = {
        "computed": H_internal.tolist(),
        "expected": expected.tolist(),
        "match": internal_match,
    }

    # Test 3: Induced magnetization
    kappa = 0.5
    H_ext = np.array([100, 0, 0])
    I_induced = sphere_induced_magnetization(kappa, H_ext)
    N = 4 * np.pi / 3
    expected_I = kappa * H_ext / (1 + N * kappa)
    induced_match = np.allclose(I_induced, expected_I)

    results["induced_magnetization"] = {
        "computed": I_induced.tolist(),
        "expected": expected_I.tolist(),
        "match": induced_match,
    }

    # Test 4: Hollow sphere cavity field
    hollow = HollowMagneticSphere(
        inner_radius=1.0,
        outer_radius=2.0,
        magnetization=np.array([0, 0, 100]),
    )

    H_cavity = hollow.field(np.array([0, 0, 0.5]))  # Inside cavity
    cavity_zero = np.allclose(H_cavity, np.zeros(3))

    results["hollow_sphere_cavity"] = {
        "field_at_center": H_cavity.tolist(),
        "is_zero": cavity_zero,
    }

    return results
