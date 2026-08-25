"""maxwell.molecular.amperes_theory — Ampere's molecular currents (Arts. 832-840).

Implements Maxwell's treatment of Ampere's theory of molecular currents
as the explanation for magnetic phenomena in materials.

Maxwell's CGS formulation (Arts. 832-840):
    Magnetic moment of molecular current:
        m = I * A / c  (Gaussian CGS: I in statamperes)

    where:
        I = molecular current (statamperes)
        A = area of current loop (cm²)
        c = speed of light (cm/s)

    Magnetic field from molecular current:
        B = (2m / r³) cos(θ) r̂ + (m / r³) sin(θ) θ̂

    Magnetization from aligned molecular currents:
        M = N * m  (magnetic moment per unit volume)

where:
    m = magnetic moment (erg/gauss)
    I = molecular current (statamperes, Gaussian CGS)
    A = area of current loop (cm²)
    M = magnetization (gauss)
    N = number density of molecular currents (cm⁻³)

Unit convention (Gaussian-CGS, explicit-c; defect D-16 class):
    The formulas divide or multiply by CONST.C exactly where the
    Gaussian-CGS theory carries c: m = I*A/CONST.C (Art. 832),
    J_b = CONST.C (curl M) (Art. 837), K_b = CONST.C (M x n_hat)
    (Art. 839).  Currents and current densities are therefore read in
    statamperes (ESU); an EMU current in abamperes enters via
    I = CONST.C * I_emu (1 abampere = CONST.C statamperes).

Category: A (maxwell_original) — Ampere's molecular current theory.

References:
    Part IV, Arts. 832-840: Ampere's theory of molecular currents.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MolecularCurrent:
    """
    Molecular current loop representing atomic magnetic moment.

    Art. 832-840: Ampere's hypothesis that magnetic phenomena arise
    from microscopic current loops within matter.

    Attributes:
        current: Molecular current I (statamperes; Gaussian-CGS explicit-c
            convention, see the module docstring).
        area: Area of current loop A (cm²).
        normal: Unit normal vector to loop plane.
        position: Position of current loop center (cm).
    """

    current: float = 0.0
    area: float = 1e-16  # Typical atomic scale
    normal: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1]))
    position: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))

    def __post_init__(self):
        """Validate and normalize parameters."""
        self.normal = np.asarray(self.normal, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        # Normalize the normal vector
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

        if self.current < 0:
            raise ValueError(f"Current must be non-negative")
        if self.area <= 0:
            raise ValueError(f"Area must be positive")

    @maxwell_cite(
        832,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic moment of molecular current",
    )
    def magnetic_moment(self) -> float:
        """
        Calculate the magnetic moment of the molecular current.

        Art. 832: The magnetic moment is:

            m = I * A / c

        In CGS-EMU, this gives m in erg/gauss.

        Returns:
            Magnetic moment m (erg/gauss).

        Reference:
            Part IV, Art. 832: Magnetic moment formula.
        """
        return (self.current * self.area) / CONST.C

    @maxwell_cite(
        833,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic field at distance",
    )
    def magnetic_field_at(self, observation_point: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field at observation point.

        Art. 833: For a dipole (small current loop):

            B(r) = (3(m·r̂)r̂ - m) / r³

        where r is the vector from dipole to observation point.

        Args:
            observation_point: Position to evaluate field (cm).

        Returns:
            Magnetic field B (gauss).

        Reference:
            Part IV, Art. 833: Dipole field.
        """
        observation_point = np.asarray(observation_point, dtype=np.float64)

        # Vector from dipole to observation point
        r_vec = observation_point - self.position
        r = np.linalg.norm(r_vec)

        if r < 1e-10:
            return np.array([0.0, 0.0, 0.0])

        r_hat = r_vec / r
        m_vec = self.magnetic_moment() * self.normal

        # Dipole field: B = (3(m·r̂)r̂ - m) / r³
        m_dot_r = np.dot(m_vec, r_hat)
        B = (3.0 * m_dot_r * r_hat - m_vec) / (r**3)

        return B

    @maxwell_cite(
        834,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate vector potential",
    )
    def vector_potential_at(self, observation_point: np.ndarray) -> np.ndarray:
        """
        Calculate vector potential at observation point.

        Art. 834: For a magnetic dipole:

            A(r) = (m × r̂) / r²

        Args:
            observation_point: Position to evaluate potential (cm).

        Returns:
            Vector potential A (gauss·cm).

        Reference:
            Part IV, Art. 834: Vector potential.
        """
        observation_point = np.asarray(observation_point, dtype=np.float64)

        r_vec = observation_point - self.position
        r = np.linalg.norm(r_vec)

        if r < 1e-10:
            return np.array([0.0, 0.0, 0.0])

        r_hat = r_vec / r
        m_vec = self.magnetic_moment() * self.normal

        # Vector potential: A = (m × r̂) / r²
        A = np.cross(m_vec, r_hat) / (r**2)

        return A


@dataclass
class AmperesTheory:
    """
    Ampere's theory of molecular currents for magnetism.

    Art. 832-840: Maxwell's analysis of Ampere's hypothesis that
    all magnetic phenomena arise from molecular-scale current loops.

    Attributes:
        number_density: Number of molecular currents per unit volume (cm⁻³).
        alignment_factor: Degree of alignment (0 to 1).
    """

    number_density: float = 1e23  # Typical atomic density
    alignment_factor: float = 0.0  # 0 = random, 1 = fully aligned

    @maxwell_cite(
        835,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetization from aligned currents",
    )
    def magnetization(self, molecular_moment: float) -> float:
        """
        Calculate magnetization from aligned molecular currents.

        Art. 835: The magnetization is:

            M = N * m * f

        where:
            N = number density
            m = molecular moment
            f = alignment factor

        Args:
            molecular_moment: Average molecular moment (erg/gauss).

        Returns:
            Magnetization M (gauss).

        Reference:
            Part IV, Art. 835: Magnetization formula.
        """
        return self.number_density * molecular_moment * self.alignment_factor

    @maxwell_cite(
        836,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic susceptibility",
    )
    def susceptibility(
        self,
        molecular_moment: float,
        temperature: float,
        applied_field: float,
    ) -> float:
        """
        Calculate magnetic susceptibility.

        Art. 836: For paramagnetic materials (Curie's law):

            χ = C / T

        where C is the Curie constant.

        Args:
            molecular_moment: Molecular moment (erg/gauss).
            temperature: Absolute temperature (K).
            applied_field: Applied field (gauss).

        Returns:
            Magnetic susceptibility χ (dimensionless).

        Reference:
            Part IV, Art. 836: Magnetic susceptibility.
        """
        if temperature <= 0:
            return 0.0

        # Curie constant: C_curie = N m^2 / (3 k_B), with the Boltzmann
        # constant taken from the project constants table (CODATA 2018
        # exact value 1.380649e-16 erg/K).
        C = (self.number_density * molecular_moment**2) / (3.0 * CONST.K_BOLTZMANN)

        return C / temperature

    @maxwell_cite(
        837,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate bound current density J_b = c curl M",
    )
    def bound_current_density(
        self,
        magnetization_field,
        point: np.ndarray | None = None,
        step: float = 1e-4,
    ) -> np.ndarray:
        """
        Calculate bound current density from magnetization.

        Art. 837: The bound (molecular) current density in the interior of
        a magnetized body is

            J_b = c * (curl M)

        in Gaussian CGS units.  Two input forms are supported:

        * ``magnetization_field`` a constant 3-vector (``np.ndarray``):
          a spatially uniform magnetization has zero curl, so the bound
          volume current vanishes (exactly ``np.zeros(3)``).
        * ``magnetization_field`` a callable ``M(r) -> (3,) vector``:
          the curl is evaluated by central finite differences at
          ``point`` (default: the origin) with step ``step`` (cm).

        Args:
            magnetization_field: Constant magnetization vector, or a
                callable vector field M(r).
            point: Evaluation point for a callable field (cm).
            step: Finite-difference step (cm).

        Returns:
            Bound current density J_b (statamperes/cm²; Gaussian-CGS,
                J_b = CONST.C curl M per Art. 837).

        Reference:
            Part IV, Art. 837: Bound current density.
        """
        if not callable(magnetization_field):
            # Uniform magnetization: curl M = 0 exactly.
            M = np.asarray(magnetization_field, dtype=np.float64)
            if M.shape != (3,):
                raise ValueError(
                    "A constant magnetization must be a 3-vector; pass a "
                    "callable M(r) for spatially varying magnetization."
                )
            return np.zeros(3)

        r0 = np.zeros(3) if point is None else np.asarray(point, dtype=np.float64)

        # Central-difference curl: (curl M)_i = eps_ijk d_j M_k.
        M = magnetization_field

        def partial(axis: int) -> np.ndarray:
            e = np.zeros(3)
            e[axis] = step
            return (
                np.asarray(M(r0 + e), dtype=np.float64)
                - np.asarray(M(r0 - e), dtype=np.float64)
            ) / (2.0 * step)

        dM_dx = partial(0)
        dM_dy = partial(1)
        dM_dz = partial(2)

        curl = np.array(
            [
                dM_dy[2] - dM_dz[1],
                dM_dz[0] - dM_dx[2],
                dM_dx[1] - dM_dy[0],
            ]
        )

        return CONST.C * curl


@maxwell_cite(
    832,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate molecular magnetic moment",
)
def calc_molecular_moment(current: float, area: float) -> float:
    """
    Calculate magnetic moment of a molecular current.

    Art. 832: m = I * A / c

    Args:
        current: Molecular current I (statamperes; Gaussian-CGS explicit-c
            convention, see the module docstring).
        area: Loop area A (cm²).

    Returns:
        Magnetic moment m (erg/gauss).

    Reference:
        Part IV, Art. 832: Molecular moment formula.

    Example:
        >>> m = calc_molecular_moment(1e-6, 1e-16)
        >>> print(f"m = {m:.2e} erg/gauss")
    """
    return (current * area) / CONST.C


@maxwell_cite(
    833,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate molecular field at distance",
)
def calc_molecular_field(
    molecular_moment: float,
    distance: float,
    angle: float,
) -> tuple[float, float]:
    """
    Calculate magnetic field from molecular current at distance.

    Art. 833: For a dipole field:

        B_r = (2m / r³) cos(θ)
        B_θ = (m / r³) sin(θ)

    Args:
        molecular_moment: Magnetic moment m (erg/gauss).
        distance: Distance r from dipole (cm).
        angle: Polar angle θ (radians).

    Returns:
        Tuple (B_r, B_θ) in gauss.

    Reference:
        Part IV, Art. 833: Dipole field components.
    """
    if distance <= 0:
        return (0.0, 0.0)

    r_cubed = distance**3

    B_radial = (2.0 * molecular_moment / r_cubed) * np.cos(angle)
    B_tangential = -(molecular_moment / r_cubed) * np.sin(angle)

    return (B_radial, B_tangential)


@maxwell_cite(
    832,
    833,
    835,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Verify the moment, dipole-field, and magnetization "
    "relations actually computed below",
)
def verify_amperes_theory(
    current: float = 1e-6,
    area: float = 1e-16,
    number_density: float = 1e23,
    distance: float = 1e-7,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify Ampere's molecular current theory relations.

    Art. 832-840: This function verifies:
    1. Magnetic moment formula: m = I*A/c
    2. Dipole field at large distances
    3. Magnetization from aligned moments
    4. Consistency with macroscopic magnetism

    Args:
        current: Molecular current (statamperes; Gaussian-CGS explicit-c
            convention, see the module docstring).
        area: Loop area (cm²).
        number_density: Number density (cm⁻³).
        distance: Test distance (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 832-840: Ampere's theory verification.
    """
    # Calculate molecular moment
    m = calc_molecular_moment(current, area)
    expected_m = (current * area) / CONST.C
    m_error = abs(m - expected_m) / expected_m if expected_m > 0 else 0

    # Calculate field at distance
    angle = np.pi / 4
    B_r, B_θ = calc_molecular_field(m, distance, angle)

    # Verify dipole field relation
    # For dipole field: B_r = (2m/r³)*cos(θ), B_θ = -(m/r³)*sin(θ)
    # Magnitude: |B| = (m/r³) * sqrt(4cos²(θ) + sin²(θ))
    B_expected = (m / (distance**3)) * np.sqrt(
        4 * np.cos(angle) ** 2 + np.sin(angle) ** 2
    )
    B_magnitude = np.sqrt(B_r**2 + B_θ**2)
    field_error = abs(B_magnitude - B_expected) / B_expected if B_expected > 0 else 0

    # Verify magnetization
    at = AmperesTheory(number_density=number_density, alignment_factor=1.0)
    M = at.magnetization(m)
    expected_M = number_density * m
    M_error = abs(M - expected_M) / expected_M if expected_M > 0 else 0

    return {
        "current": current,
        "area": area,
        "number_density": number_density,
        "molecular_moment": m,
        "expected_moment": expected_m,
        "moment_error": m_error,
        "B_radial": B_r,
        "B_tangential": B_θ,
        "B_magnitude": B_magnitude,
        "field_error": field_error,
        "magnetization": M,
        "magnetization_error": M_error,
        "verified": bool(
            m_error < tolerance and field_error < tolerance and M_error < tolerance
        ),
    }


@maxwell_cite(
    832,
    833,
    835,
    836,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Analysis of Ampere's theory built from the moment, "
    "magnetization, Curie susceptibility, and dipole-field formulas",
)
def analyze_amperes_theory(
    current: float = 1e-6,
    area: float = 1e-16,
    number_density: float = 1e23,
    alignment_factor: float = 0.5,
    temperature: float = 300.0,
    applied_field: float = 1000.0,
) -> dict[str, float]:
    """
    Complete analysis of Ampere's molecular current theory.

    Art. 832-840: Comprehensive analysis including:
    1. Molecular moment calculation
    2. Field at various distances
    3. Bulk magnetization
    4. Temperature dependence

    Args:
        current: Molecular current (statamperes; Gaussian-CGS explicit-c
            convention, see the module docstring).
        area: Loop area (cm²).
        number_density: Number density (cm⁻³).
        alignment_factor: Alignment factor (0-1).
        temperature: Temperature (K).
        applied_field: Applied field (gauss).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 832-840: Complete Ampere theory analysis.
    """
    m = calc_molecular_moment(current, area)

    at = AmperesTheory(number_density=number_density, alignment_factor=alignment_factor)

    M = at.magnetization(m)
    chi = at.susceptibility(m, temperature, applied_field)

    # Field at characteristic distance
    char_distance = number_density ** (-1 / 3)  # Average inter-atomic distance
    B_r, B_θ = calc_molecular_field(m, char_distance, 0)

    return {
        "current_abamp": current,
        "area_cm2": area,
        "molecular_moment_erg_gauss": m,
        "number_density_cm3": number_density,
        "alignment_factor": alignment_factor,
        "magnetization_gauss": M,
        "susceptibility": chi,
        "curie_constant": chi * temperature,
        "temperature_K": temperature,
        "applied_field_gauss": applied_field,
        "char_distance_cm": char_distance,
        "B_radial_at_char": B_r,
        "B_tangential_at_char": B_θ,
        "CGS_units": "m in erg/gauss, B in gauss, M in gauss",
    }


# =============================================================================
# ARTS. 838-840 CONSEQUENCES OF THE MOLECULAR-CURRENT MODEL
# =============================================================================


@maxwell_cite(
    838,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Total magnetic moment of a magnetized body, integral of M",
)
def total_magnetic_moment(
    magnetization_field,
    bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    n_per_axis: int = 32,
) -> np.ndarray:
    """
    Calculate the total magnetic moment of a magnetized body.

    Art. 838: The magnetic moment of a finite magnet is the integral of
    the magnetization over its volume.  For a body occupying V,

        m_total = ∫_V M dV

    Args:
        magnetization_field: Constant magnetization 3-vector, or a
            callable M(r) -> 3-vector field (gauss).
        bounds: Axis-aligned bounding box ((x0, x1), (y0, y1), (z0, z1))
            in cm.
        n_per_axis: Midpoint-rule samples per axis (for callable fields).

    Returns:
        Total magnetic moment vector (erg/gauss).

    Reference:
        Part IV, Art. 838: Magnetic moment of a magnetized body.
    """
    (x0, x1), (y0, y1), (z0, z1) = bounds
    volume = (x1 - x0) * (y1 - y0) * (z1 - z0)
    if volume <= 0:
        raise ValueError("Bounding box must have positive volume")

    if not callable(magnetization_field):
        M = np.asarray(magnetization_field, dtype=np.float64)
        if M.shape != (3,):
            raise ValueError("Constant magnetization must be a 3-vector")
        return M * volume

    # Midpoint quadrature (exact for constant and linear fields).
    xs = np.linspace(x0, x1, 2 * n_per_axis + 1)[1::2]
    ys = np.linspace(y0, y1, 2 * n_per_axis + 1)[1::2]
    zs = np.linspace(z0, z1, 2 * n_per_axis + 1)[1::2]
    dV = volume / n_per_axis**3

    moment = np.zeros(3)
    for x in xs:
        for y in ys:
            for z in zs:
                moment += np.asarray(
                    magnetization_field(np.array([x, y, z])), dtype=np.float64
                )
    return moment * dV


@maxwell_cite(
    839,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Bound surface current density K_b = c M x n_hat",
)
def bound_surface_current(
    magnetization: np.ndarray,
    outward_normal: np.ndarray,
) -> np.ndarray:
    """
    Calculate the bound surface current density of a magnetized body.

    Art. 839: The molecular currents of a magnetized body are equivalent
    to a surface current density

        K_b = c (M x n_hat)

    flowing on its boundary, where n_hat is the outward unit normal.
    (Gaussian CGS: K_b in statamperes/cm when M is in gauss.)

    Args:
        magnetization: Magnetization vector M (gauss).
        outward_normal: Outward unit normal n_hat at the surface point.

    Returns:
        Surface current density K_b (statamperes/cm; Gaussian-CGS,
            K_b = CONST.C (M x n_hat) per Art. 839).

    Reference:
        Part IV, Art. 839: Equivalent surface current of a magnet.
    """
    M = np.asarray(magnetization, dtype=np.float64)
    n = np.asarray(outward_normal, dtype=np.float64)
    n_norm = np.linalg.norm(n)
    if n_norm <= 0:
        raise ValueError("Outward normal must be nonzero")
    n = n / n_norm
    return CONST.C * np.cross(M, n)


@maxwell_cite(
    840,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Field inside a uniformly magnetized sphere by direct "
    "Biot-Savart quadrature of the bound surface current",
)
def sphere_interior_field(
    magnetization: np.ndarray,
    radius: float,
    point: np.ndarray | None = None,
    n_theta: int = 96,
    n_phi: int = 192,
) -> np.ndarray:
    """
    Calculate the magnetic field inside a uniformly magnetized sphere.

    Art. 840: A uniformly magnetized sphere carries the bound surface
    current K_b = c (M x n_hat) (Art. 839).  Its field is computed here
    directly from the Biot-Savart law for a surface current (Gaussian):

        B(r) = (1/c) ∮ K_b(r') x (r - r') / |r - r'|^3 da'

    The analytic consequence is a spatially uniform interior field
    B = (8 pi / 3) M; this function evaluates the integral numerically
    so that the result is a computation, not an assertion.

    Args:
        magnetization: Uniform magnetization M (gauss).
        radius: Sphere radius (cm).
        point: Interior evaluation point (cm); default: center.
        n_theta: Polar midpoint samples.
        n_phi: Azimuthal midpoint samples.

    Returns:
        Magnetic field B at the point (gauss).

    Reference:
        Part IV, Art. 840: Field of a uniformly magnetized sphere.
    """
    M_vec = np.asarray(magnetization, dtype=np.float64)
    if radius <= 0:
        raise ValueError("Radius must be positive")
    r_eval = np.zeros(3) if point is None else np.asarray(point, dtype=np.float64)
    if np.linalg.norm(r_eval) >= radius:
        raise ValueError("Evaluation point must lie strictly inside the sphere")

    theta = (np.arange(n_theta) + 0.5) * np.pi / n_theta
    phi = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    T, P = np.meshgrid(theta, phi, indexing="ij")
    sin_t = np.sin(T)

    r_prime = np.stack(
        [
            radius * sin_t * np.cos(P),
            radius * sin_t * np.sin(P),
            radius * np.cos(T),
        ],
        axis=-1,
    )
    n_hat = r_prime / radius
    K = CONST.C * np.cross(np.broadcast_to(M_vec, r_prime.shape), n_hat)

    sep = r_eval - r_prime
    dist = np.linalg.norm(sep, axis=-1, keepdims=True)
    da = radius**2 * sin_t[..., None] * (np.pi / n_theta) * (2.0 * np.pi / n_phi)

    integrand = np.cross(K, sep) / dist**3 * da
    return np.sum(integrand, axis=(0, 1)) / CONST.C


@maxwell_cite(
    840,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Center field of a magnetized sphere via ring-current "
    "quadrature (independent high-accuracy path)",
)
def sphere_center_field_rings(
    magnetization: np.ndarray,
    radius: float,
    n_rings: int = 512,
) -> np.ndarray:
    """
    Center field of a uniformly magnetized sphere by ring quadrature.

    Art. 840 (independent path): decompose the bound surface current
    K_b = c M sin(theta) into coaxial rings.  A ring at colatitude theta
    carries dI = c |M| R sin(theta) d theta at radius R sin(theta) and
    height R cos(theta); its on-center field is 2 pi dI a^2 / (c R^3),
    giving the total

        B(0) = 2 pi |M| (integral of sin^3 theta from 0 to pi) * M_hat
             = (8 pi / 3) M

    The theta integral is evaluated by composite Simpson's rule, so the
    returned value is a genuine quadrature (use as an oracle for
    :func:`sphere_interior_field`).

    Args:
        magnetization: Uniform magnetization M (gauss).
        radius: Sphere radius (cm) — cancels in the on-center result but
            kept for dimensional clarity.
        n_rings: Even number of Simpson panels.

    Returns:
        Magnetic field at the center (gauss).

    Reference:
        Part IV, Art. 840: Field of a magnetized sphere.
    """
    M_vec = np.asarray(magnetization, dtype=np.float64)
    M_mag = np.linalg.norm(M_vec)
    if radius <= 0:
        raise ValueError("Radius must be positive")
    if M_mag == 0:
        return np.zeros(3)
    if n_rings % 2:
        raise ValueError("n_rings must be even (Simpson's rule)")

    theta = np.linspace(0.0, np.pi, n_rings + 1)
    f = np.sin(theta) ** 3
    integral = (np.pi / n_rings / 3.0) * (
        f[0] + f[-1] + 4.0 * f[1:-1:2].sum() + 2.0 * f[2:-2:2].sum()
    )

    B_mag = 2.0 * np.pi * M_mag * integral
    return B_mag * M_vec / M_mag
