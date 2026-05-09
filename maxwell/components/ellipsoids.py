"""
Magnetic ellipsoids — analytical solutions for ellipsoidal magnetic bodies.

Implements the theory of magnetic ellipsoids from Part III of Maxwell's Treatise:
- Uniformly magnetized ellipsoid (Arts. 437-438)
- Demagnetizing factors for ellipsoids
- Ellipsoid in external field

The ellipsoid is the most general body shape that admits uniform
magnetization in a uniform external field. The three principal
demagnetizing factors N_x, N_y, N_z depend on the axis ratios.

Special cases:
- Sphere: N_x = N_y = N_z = 4π/3
- Prolate spheroid: N_x < N_y = N_z (elongated)
- Oblate spheroid: N_x = N_y < N_z (flattened)

Category: A (maxwell_original) — Maxwell's theory of magnetic ellipsoids.

References:
    Part III, Arts. 437-438: Magnetic ellipsoids.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticEllipsoid:
    """
    Triaxial ellipsoid with uniform magnetization.

    Arts. 437-438: An ellipsoid with semi-axes a, b, c and uniform
    magnetization I produces:

    - Inside: Uniform field H_i = -N_i × I_i (no sum)
    - Outside: Complex multipole field

    The demagnetizing factors N_x, N_y, N_z satisfy:
        N_x + N_y + N_z = 4π (CGS)

    and depend only on the axis ratios, not absolute size.

    Attributes:
        semi_axes: Semi-axes (a, b, c) in cm.
        magnetization: Uniform magnetization I (emu/cm³).
        center: Center position (cm).
    """

    semi_axes: np.ndarray = None  # (a, b, c), cm
    magnetization: np.ndarray = None  # I, emu/cm³, shape (3,)
    center: np.ndarray = None  # center, cm, shape (3,)

    def __post_init__(self):
        self.semi_axes = np.asarray(self.semi_axes, dtype=np.float64)
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
        """Volume of ellipsoid: V = (4/3)πabc."""
        a, b, c = self.semi_axes
        return (4 / 3) * np.pi * a * b * c

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment: m = I × V."""
        return self.magnetization * self.volume

    @maxwell_cite(
        437,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Calculate demagnetizing factors for ellipsoid",
    )
    def demagnetizing_factors(self) -> dict[str, float]:
        """
        Calculate demagnetizing factors for triaxial ellipsoid.

        Art. 437: The demagnetizing factors are given by integrals:

            N_x = 2πabc ∫₀^∞ ds / [(s+a²)√((s+a²)(s+b²)(s+c²))]

        with similar expressions for N_y, N_z.

        These satisfy N_x + N_y + N_z = 4π.

        Returns:
            Dictionary with N_x, N_y, N_z.

        Reference:
            Part III, Art. 437: Demagnetizing factors.
        """
        a, b, c = self.semi_axes

        # Check for special cases
        if np.abs(a - b) < 1e-10 and np.abs(b - c) < 1e-10:
            # Sphere
            N = 4 * np.pi / 3
            return {"N_x": N, "N_y": N, "N_z": N}

        elif np.abs(b - c) < 1e-10:
            # Prolate or oblate spheroid
            return self._spheroid_demagnetizing_factors(a, b)

        else:
            # General triaxial ellipsoid - numerical integration
            return self._triaxial_demagnetizing_factors()

    def _spheroid_demagnetizing_factors(
        self,
        a: float,
        b: float,
    ) -> dict[str, float]:
        """Calculate factors for spheroid (b = c)."""
        if a > b:
            # Prolate spheroid (cigar-shaped)
            e = np.sqrt(1 - (b / a) ** 2)  # Eccentricity
            if e > 1e-6:
                N_x = (
                    4
                    * np.pi
                    * (1 - e**2)
                    / (2 * e**3)
                    * (np.log((1 + e) / (1 - e)) - 2 * e)
                )
            else:
                N_x = 4 * np.pi / 3
            N_y = N_z = (4 * np.pi - N_x) / 2

        else:
            # Oblate spheroid (disk-shaped)
            e = np.sqrt((a / b) ** 2 - 1)
            if e > 1e-6:
                N_x = 4 * np.pi * (1 + e**2) / e**3 * (e - np.arctan(e))
            else:
                N_x = 4 * np.pi / 3
            N_y = N_z = (4 * np.pi - N_x) / 2

        return {"N_x": float(N_x), "N_y": float(N_y), "N_z": float(N_z)}

    def _triaxial_demagnetizing_factors(self) -> dict[str, float]:
        """Calculate factors for general triaxial ellipsoid."""
        a, b, c = self.semi_axes

        # Numerical integration using change of variables
        # Integral from 0 to ∞ transformed to [0, 1]

        def integrand(s, axis_sq):
            denom = np.sqrt((s + a**2) * (s + b**2) * (s + c**2))
            return (s + axis_sq) * denom

        # Gaussian quadrature points and weights
        from scipy.special import roots_legendre

        n_points = 64
        xi, wi = roots_legendre(n_points)

        # Transform from [-1, 1] to [0, ∞) using s = (1+x)/(1-x)
        # Actually use s = tan(π(x+1)/4) for better convergence
        N = np.zeros(3)

        for i, (x, w) in enumerate(zip(xi, wi)):
            s = np.tan(np.pi * (x + 1) / 4)
            ds = np.pi / 4 * (1 + s**2)

            denom = np.sqrt((s + a**2) * (s + b**2) * (s + c**2))

            N[0] += w * ds / ((s + a**2) * denom)
            N[1] += w * ds / ((s + b**2) * denom)
            N[2] += w * ds / ((s + c**2) * denom)

        # Scale factor
        scale = 2 * np.pi * a * b * c / 2  # Jacobian from transformation

        N *= scale

        # Normalize to sum to 4π
        total = np.sum(N)
        N *= 4 * np.pi / total

        return {"N_x": float(N[0]), "N_y": float(N[1]), "N_z": float(N[2])}

    @maxwell_cite(
        437,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Calculate internal field of magnetized ellipsoid",
    )
    def internal_field(self) -> np.ndarray:
        """
        Calculate uniform demagnetizing field inside ellipsoid.

        Art. 437: The internal field is uniform and given by:

            H_i = -N_i × I_i  (no sum over i)

        where N_i are the demagnetizing factors along principal
        axes aligned with the ellipsoid axes.

        Returns:
            Internal demagnetizing field H (gauss).

        Reference:
            Part III, Art. 437: Internal field.
        """
        N = self.demagnetizing_factors()

        H_demag = np.zeros(3)
        H_demag[0] = -N["N_x"] * self.magnetization[0]
        H_demag[1] = -N["N_y"] * self.magnetization[1]
        H_demag[2] = -N["N_z"] * self.magnetization[2]

        return H_demag

    @classmethod
    @maxwell_cite(
        438,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Create ellipsoid induced by external field",
    )
    def in_uniform_field(
        cls,
        semi_axes: np.ndarray,
        susceptibility: float,
        external_field: np.ndarray,
        center: np.ndarray = None,
    ) -> MagneticEllipsoid:
        """
        Create ellipsoid with induced magnetization in uniform field.

        Art. 438: When an ellipsoid of susceptibility κ is placed
        in uniform field H_ext, the induced magnetization is:

            I_i = κ H_ext_i / (1 + N_i κ)  (no sum)

        The magnetization is generally not parallel to H_ext
        unless the field is along a principal axis.

        Args:
            semi_axes: Semi-axes (a, b, c) in cm.
            susceptibility: Magnetic susceptibility κ.
            external_field: Applied field H_ext (gauss).
            center: Center position (cm).

        Returns:
            MagneticEllipsoid with induced magnetization.

        Reference:
            Part III, Art. 438: Induced ellipsoid.
        """
        H_ext = np.asarray(external_field, dtype=np.float64)

        # Create temporary ellipsoid to get demagnetizing factors
        temp = cls(semi_axes=semi_axes, center=center)
        N = temp.demagnetizing_factors()

        # Induced magnetization along each axis
        I = np.zeros(3)
        I[0] = susceptibility * H_ext[0] / (1 + N["N_x"] * susceptibility)
        I[1] = susceptibility * H_ext[1] / (1 + N["N_y"] * susceptibility)
        I[2] = susceptibility * H_ext[2] / (1 + N["N_z"] * susceptibility)

        return cls(
            semi_axes=semi_axes,
            magnetization=I,
            center=center,
        )


@dataclass
class ProlateSpheroid(MagneticEllipsoid):
    """
    Prolate spheroid (cigar-shaped ellipsoid).

    Arts. 437-438: A prolate spheroid has semi-axes a > b = c.
    It models elongated magnets like rod magnets.

    Demagnetizing factors:
    - N_x < N_y = N_z (easier to magnetize along long axis)
    - As a/b → ∞: N_x → 0, N_y = N_z → 2π

    Attributes:
        length: Semi-axis a (cm) along symmetry axis.
        radius: Semi-axes b = c (cm) transverse.
        magnetization: Uniform magnetization I (emu/cm³).
    """

    length: float = 1.0  # Semi-axis a, cm
    radius: float = 1.0  # Semi-axes b = c, cm
    magnetization: np.ndarray = None
    center: np.ndarray = None

    def __post_init__(self):
        semi_axes = np.array([self.length, self.radius, self.radius])
        super().__init__(
            semi_axes=semi_axes,
            magnetization=self.magnetization,
            center=self.center,
        )

    @maxwell_cite(
        437,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Calculate prolate spheroid demagnetizing factors",
    )
    def demagnetizing_factors(self) -> dict[str, float]:
        """
        Calculate demagnetizing factors for prolate spheroid.

        Art. 437: For a prolate spheroid with aspect ratio m = a/b:

            N_x = 4π(1-e²)/(2e³) × [ln((1+e)/(1-e)) - 2e]
            N_y = N_z = (4π - N_x)/2

        where e = √(1 - 1/m²) is the eccentricity.

        Returns:
            Dictionary with N_x, N_y, N_z.

        Reference:
            Part III, Art. 437: Prolate factors.
        """
        return self._spheroid_demagnetizing_factors(self.length, self.radius)

    @classmethod
    @maxwell_cite(
        438,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Create prolate spheroid for rod magnet",
    )
    def for_rod_magnet(
        cls,
        length: float,
        diameter: float,
        magnetization: np.ndarray,
        center: np.ndarray = None,
    ) -> ProlateSpheroid:
        """
        Create prolate spheroid approximating a cylindrical rod magnet.

        Art. 438: A rod magnet of length L and diameter D can be
        approximated by a prolate spheroid with:
            a = L/2, b = c = D/2

        Args:
            length: Rod length L (cm).
            diameter: Rod diameter D (cm).
            magnetization: Magnetization I (emu/cm³).
            center: Center position (cm).

        Returns:
            ProlateSpheroid object.

        Reference:
            Part III, Art. 438: Rod magnet approximation.
        """
        return cls(
            length=length / 2,
            radius=diameter / 2,
            magnetization=magnetization,
            center=center,
        )


@dataclass
class OblateSpheroid(MagneticEllipsoid):
    """
    Oblate spheroid (disk-shaped ellipsoid).

    Arts. 437-438: An oblate spheroid has semi-axes a = b > c.
    It models flat magnets like disk magnets or thin films.

    Demagnetizing factors:
    - N_x = N_y < N_z (harder to magnetize perpendicular to plane)
    - As c/a → 0: N_z → 4π, N_x = N_y → 0

    Attributes:
        radius: Semi-axes a = b (cm) in plane.
        thickness: Semi-axis c (cm) perpendicular.
        magnetization: Uniform magnetization I (emu/cm³).
    """

    radius: float = 1.0  # Semi-axes a = b, cm
    thickness: float = 1.0  # Semi-axis c, cm
    magnetization: np.ndarray = None
    center: np.ndarray = None

    def __post_init__(self):
        semi_axes = np.array([self.radius, self.radius, self.thickness])
        super().__init__(
            semi_axes=semi_axes,
            magnetization=self.magnetization,
            center=self.center,
        )

    @maxwell_cite(
        437,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Calculate oblate spheroid demagnetizing factors",
    )
    def demagnetizing_factors(self) -> dict[str, float]:
        """
        Calculate demagnetizing factors for oblate spheroid.

        Art. 437: For an oblate spheroid with aspect ratio m = a/c:

            N_z = 4π(1+e²)/e³ × [e - arctan(e)]
            N_x = N_y = (4π - N_z)/2

        where e = √(m² - 1) is the eccentricity.

        Returns:
            Dictionary with N_x, N_y, N_z.

        Reference:
            Part III, Art. 437: Oblate factors.
        """
        return self._spheroid_demagnetizing_factors(self.thickness, self.radius)

    @classmethod
    @maxwell_cite(
        438,
        part=3,
        chapter="Magnetic Ellipsoids",
        theory_class="maxwell_original",
        description="Create oblate spheroid for disk magnet",
    )
    def for_disk_magnet(
        cls,
        diameter: float,
        thickness: float,
        magnetization: np.ndarray,
        center: np.ndarray = None,
    ) -> OblateSpheroid:
        """
        Create oblate spheroid approximating a cylindrical disk magnet.

        Art. 438: A disk magnet of diameter D and thickness t can be
        approximated by an oblate spheroid with:
            a = b = D/2, c = t/2

        Args:
            diameter: Disk diameter D (cm).
            thickness: Disk thickness t (cm).
            magnetization: Magnetization I (emu/cm³).
            center: Center position (cm).

        Returns:
            OblateSpheroid object.

        Reference:
            Part III, Art. 438: Disk magnet approximation.
        """
        return cls(
            radius=diameter / 2,
            thickness=thickness / 2,
            magnetization=magnetization,
            center=center,
        )


@maxwell_cite(
    437,
    part=3,
    chapter="Magnetic Ellipsoids",
    theory_class="maxwell_original",
    description="Calculate field of uniformly magnetized ellipsoid",
)
def ellipsoid_field(
    semi_axes: np.ndarray,
    magnetization: np.ndarray,
    position: np.ndarray,
    center: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate magnetic field of uniformly magnetized ellipsoid.

    Art. 437: Inside the ellipsoid, the field is uniform:
        H = -(N_x I_x, N_y I_y, N_z I_z)

    Outside, the field is complex. For approximate calculations,
    we use the dipole field with m = IV.

    Args:
        semi_axes: Semi-axes (a, b, c) in cm.
        magnetization: Magnetization I (emu/cm³).
        position: Point to evaluate (cm).
        center: Ellipsoid center (cm).

    Returns:
        Magnetic field H (gauss).

    Reference:
        Part III, Art. 437: Ellipsoid field.
    """
    if center is None:
        center = np.zeros(3)

    magnetization = np.asarray(magnetization, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)
    semi_axes = np.asarray(semi_axes, dtype=np.float64)

    # Check if inside ellipsoid: (x/a)² + (y/b)² + (z/c)² < 1
    r = position - center
    normalized = (
        (r[0] / semi_axes[0]) ** 2
        + (r[1] / semi_axes[1]) ** 2
        + (r[2] / semi_axes[2]) ** 2
    )

    if normalized < 1:
        # Inside: uniform demagnetizing field
        ellipsoid = MagneticEllipsoid(semi_axes=semi_axes, magnetization=magnetization)
        return ellipsoid.internal_field()
    else:
        # Outside: approximate as dipole
        volume = (4 / 3) * np.pi * semi_axes[0] * semi_axes[1] * semi_axes[2]
        m = magnetization * volume

        r_mag = np.linalg.norm(r)
        r_hat = r / r_mag

        H = (3 * np.dot(m, r_hat) * r_hat - m) / (r_mag**3)
        return H


@maxwell_cite(
    438,
    part=3,
    chapter="Magnetic Ellipsoids",
    theory_class="maxwell_original",
    description="Calculate induced magnetization of ellipsoid",
)
def ellipsoid_induced_magnetization(
    semi_axes: np.ndarray,
    susceptibility: float,
    external_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate induced magnetization of ellipsoid in uniform field.

    Art. 438: For an ellipsoid with susceptibility κ in uniform
    field H_ext, the induced magnetization is:

        I_i = κ H_ext_i / (1 + N_i κ)  (no sum)

    Args:
        semi_axes: Semi-axes (a, b, c) in cm.
        susceptibility: Magnetic susceptibility κ.
        external_field: Applied field H_ext (gauss).

    Returns:
        Induced magnetization I (emu/cm³).

    Reference:
        Part III, Art. 438: Induced ellipsoid magnetization.
    """
    ellipsoid = MagneticEllipsoid(semi_axes=semi_axes)
    N = ellipsoid.demagnetizing_factors()

    H_ext = np.asarray(external_field, dtype=np.float64)

    I = np.zeros(3)
    I[0] = susceptibility * H_ext[0] / (1 + N["N_x"] * susceptibility)
    I[1] = susceptibility * H_ext[1] / (1 + N["N_y"] * susceptibility)
    I[2] = susceptibility * H_ext[2] / (1 + N["N_z"] * susceptibility)

    return I


@maxwell_cite(
    437,
    part=3,
    chapter="Magnetic Ellipsoids",
    theory_class="maxwell_original",
    description="Calculate demagnetizing energy of ellipsoid",
)
def ellipsoid_demagnetizing_energy(
    semi_axes: np.ndarray,
    magnetization: np.ndarray,
    volume: float = None,
) -> float:
    """
    Calculate demagnetizing (self) energy of magnetized ellipsoid.

    Art. 437: The magnetostatic self-energy of a uniformly
    magnetized ellipsoid is:

        W = (1/2) V × (N_x I_x² + N_y I_y² + N_z I_z²)

    This energy is minimized when magnetization aligns with
    the axis of smallest N (easy axis).

    Args:
        semi_axes: Semi-axes (a, b, c) in cm.
        magnetization: Magnetization I (emu/cm³).
        volume: Volume (if None, calculated from semi-axes).

    Returns:
        Demagnetizing energy W (erg).

    Reference:
        Part III, Art. 437: Demagnetizing energy.
    """
    if volume is None:
        volume = (4 / 3) * np.pi * semi_axes[0] * semi_axes[1] * semi_axes[2]

    ellipsoid = MagneticEllipsoid(semi_axes=semi_axes, magnetization=magnetization)
    N = ellipsoid.demagnetizing_factors()

    I = np.asarray(magnetization, dtype=np.float64)

    W = (
        0.5
        * volume
        * (N["N_x"] * I[0] ** 2 + N["N_y"] * I[1] ** 2 + N["N_z"] * I[2] ** 2)
    )

    return float(W)


@maxwell_cite(
    437,
    438,
    part=3,
    chapter="Magnetic Ellipsoids",
    theory_class="maxwell_original",
    description="Find easy axis of ellipsoidal magnet",
)
def find_easy_axis(semi_axes: np.ndarray) -> tuple[str, np.ndarray]:
    """
    Find the magnetic easy axis of an ellipsoid.

    Arts. 437-438: The easy axis is the direction along which
    the demagnetizing factor is smallest. Magnetization along
    this direction has minimum demagnetizing energy.

    For prolate spheroid: easy axis is along long axis (x)
    For oblate spheroid: easy axis is in the plane (x or y)

    Args:
        semi_axes: Semi-axes (a, b, c) in cm.

    Returns:
        Tuple of (axis_name, unit_vector).

    Reference:
        Part III, Arts. 437-438: Easy axis.
    """
    ellipsoid = MagneticEllipsoid(semi_axes=semi_axes)
    N = ellipsoid.demagnetizing_factors()

    factors = {"x": N["N_x"], "y": N["N_y"], "z": N["N_z"]}

    # Easy axis has smallest demagnetizing factor
    easy = min(factors, key=factors.get)

    unit_vectors = {
        "x": np.array([1, 0, 0]),
        "y": np.array([0, 1, 0]),
        "z": np.array([0, 0, 1]),
    }

    return easy, unit_vectors[easy]


@maxwell_cite(
    437,
    438,
    part=3,
    chapter="Magnetic Ellipsoids",
    theory_class="maxwell_original",
    description="Verify ellipsoid magnetism calculations",
)
def verify_ellipsoid_magnetism() -> dict[str, any]:
    """
    Verify analytical formulas for magnetic ellipsoids.

    Arts. 437-438: Test cases:

    1. Sphere limit: a = b = c gives N = 4π/3
    2. Prolate spheroid factors
    3. Oblate spheroid factors
    4. Sum rule: N_x + N_y + N_z = 4π
    5. Easy axis identification

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Arts. 437-438: Ellipsoid verification.
    """
    results = {}

    # Test 1: Sphere limit
    sphere = MagneticEllipsoid(semi_axes=np.array([1, 1, 1]))
    N_sphere = sphere.demagnetizing_factors()
    expected = 4 * np.pi / 3

    sphere_error_x = abs(N_sphere["N_x"] - expected) / expected
    sphere_error_y = abs(N_sphere["N_y"] - expected) / expected
    sphere_error_z = abs(N_sphere["N_z"] - expected) / expected

    results["sphere_limit"] = {
        "N_x": N_sphere["N_x"],
        "N_y": N_sphere["N_y"],
        "N_z": N_sphere["N_z"],
        "expected": expected,
        "max_error": max(sphere_error_x, sphere_error_y, sphere_error_z),
        "passes": max(sphere_error_x, sphere_error_y, sphere_error_z) < 1e-6,
    }

    # Test 2: Sum rule
    ellipsoid = MagneticEllipsoid(semi_axes=np.array([2, 1, 0.5]))
    N = ellipsoid.demagnetizing_factors()
    total = N["N_x"] + N["N_y"] + N["N_z"]
    sum_error = abs(total - 4 * np.pi) / (4 * np.pi)

    results["sum_rule"] = {
        "N_x": N["N_x"],
        "N_y": N["N_y"],
        "N_z": N["N_z"],
        "total": total,
        "expected": 4 * np.pi,
        "error": sum_error,
        "passes": sum_error < 1e-6,
    }

    # Test 3: Prolate spheroid (easy axis along length)
    prolate = ProlateSpheroid(length=5, radius=1)
    N_prolate = prolate.demagnetizing_factors()
    easy_axis = N_prolate["N_x"] < N_prolate["N_y"]

    results["prolate_spheroid"] = {
        "N_x": N_prolate["N_x"],
        "N_y": N_prolate["N_y"],
        "N_z": N_prolate["N_z"],
        "easy_axis_is_x": easy_axis,
    }

    # Test 4: Oblate spheroid (hard axis perpendicular to plane)
    oblate = OblateSpheroid(radius=5, thickness=1)
    N_oblate = oblate.demagnetizing_factors()
    hard_axis = N_oblate["N_z"] > N_oblate["N_x"]

    results["oblate_spheroid"] = {
        "N_x": N_oblate["N_x"],
        "N_y": N_oblate["N_y"],
        "N_z": N_oblate["N_z"],
        "hard_axis_is_z": hard_axis,
    }

    # Test 5: Easy axis finding
    easy_name, easy_vec = find_easy_axis(np.array([3, 1, 1]))
    easy_correct = easy_name == "x"

    results["easy_axis"] = {
        "axis_name": easy_name,
        "axis_vector": easy_vec.tolist(),
        "correct": easy_correct,
    }

    return results
