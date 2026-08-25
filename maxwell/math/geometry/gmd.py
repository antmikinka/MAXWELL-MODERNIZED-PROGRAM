"""maxwell.math.geometry.gmd — Geometric mean distance (Arts. 691-693).

Implements Maxwell's geometric mean distance (GMD) calculations for
wire inductance and mutual inductance between conductors.

Maxwell's CGS formulation (Arts. 691-693):
    The geometric mean distance (GMD) between two areas A1 and A2 is:

        ln(GMD) = (1/A1*A2) * double_integral(ln(r) dA1 dA2)

    where r is the distance between points in the two areas.

    For mutual inductance of coils with finite cross-section:

        M = M_filament * correction(GMD)

    The GMD of a circular cross-section of radius a:

        GMD_self = a * exp(-1/4) ≈ 0.7788 * a

    For two parallel circular sections separated by d:

        GMD = d  EXACTLY, whenever the sections do not overlap
                 (mean-value property of the harmonic log kernel).

where:
    GMD = geometric mean distance (cm)
    M = mutual inductance (cm in CGS-EMU)
    a = wire radius (cm)
    d = separation (cm)

Category: A (maxwell_original) — Maxwell's GMD theory.

References:
    Part IV, Arts. 691-693: Geometric mean distance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


def _disk_log_potential(radius: float, rho: float) -> float:
    """Exact log potential of a uniform disk, ∫_disk ln|r − r'| dA'.

    Evaluated at a point at distance ``rho`` from the centre.  From
    Gauss's law in two dimensions (∇² ln r = 2π δ): inside the disk the
    field grows linearly, outside it decays as 1/rho, giving

        Phi(rho) = pi a^2 (ln a − 1/2 + rho²/(2a²)),  rho <= a,
        Phi(rho) = pi a^2 ln(rho),                     rho >= a.

    Continuous and C¹ at rho = a; at rho = 0 it yields the known mean
    ln-distance ln a − 1/2 over the disk.
    """
    area = np.pi * radius**2
    if rho <= radius:
        return float(area * (np.log(radius) - 0.5 + 0.5 * (rho / radius) ** 2))
    return float(area * np.log(rho))


def _gmd_overlapping_disks(a1: float, a2: float, d: float) -> float:
    """Exact mutual GMD of two (possibly overlapping) circular sections.

    Reduction of the defining double-area integral to ONE quadrature.
    With s = |r1 − c2| the inner average over disk 2 is

        (1/A2) ∫_{D2} ln|r1 − r2| dA2 = ln s            (s >= a2),
                                       = ln a2 − 1/2 + s²/(2a2²)  (s < a2),

    so with f(s) = ln a2 − 1/2 + s²/(2a2²) − ln s (continuous, f(a2) = 0):

        ln GMD = Phi_{D1}(d)/A1 + (1/A1) ∫_0^{a2} s f(s) Theta(s) ds,

    where Theta(s) is the angular measure of the part of the circle
    |r − c2| = s that lies inside disk 1:

        cos(theta0) = (s² + d² − a1²) / (2 s d),   Theta = 2 theta0,

    with Theta = 2π when the whole circle is inside (s + d <= a1) and
    Theta = 0 when it is fully outside.  Checks: for d >= a1 + a2 the
    integral vanishes and ln GMD = ln d exactly; for d = 0, a1 = a2 = a
    it evaluates by hand to ln a − 1/4 (the self-GMD a e^{−1/4}).
    """
    area1 = np.pi * a1**2

    def theta_measure(s: float) -> float:
        if d <= 1e-14:  # concentric limit
            return 2.0 * np.pi if s < a1 else 0.0
        if s <= 0.0:
            return 2.0 * np.pi if d < a1 else 0.0
        cos0 = (s * s + d * d - a1 * a1) / (2.0 * s * d)
        if cos0 >= 1.0:
            return 0.0
        if cos0 <= -1.0:
            return 2.0 * np.pi
        return float(2.0 * np.arccos(cos0))

    def integrand(s: float) -> float:
        if s <= 0.0:
            return 0.0
        f = np.log(a2) - 0.5 + s * s / (2.0 * a2 * a2) - np.log(s)
        return s * f * theta_measure(s)

    # Breakpoints of Theta(s) inside the integration range
    candidates = (abs(d - a1), d + a1, abs(a1 - d))
    points = sorted({p for p in candidates if 0.0 < p < a2})
    correction, _ = quad(integrand, 0.0, a2, points=points or None, limit=200)

    ln_gmd = (_disk_log_potential(a1, d) + correction) / area1
    return float(np.exp(ln_gmd))


@maxwell_cite(
    691,
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate GMD between two points",
)
def calc_gmd_points(
    points1: list[np.ndarray],
    points2: list[np.ndarray],
) -> float:
    """
    Calculate geometric mean distance between two point sets.

    Art. 691-693: The GMD between two sets of points is:

        GMD = exp(mean(ln(r_ij)))

    where r_ij is the distance between point i in set 1 and
    point j in set 2.

    Args:
        points1: First set of points (cm).
        points2: Second set of points (cm).

    Returns:
        Geometric mean distance (cm).
    """
    points1 = [np.asarray(p, dtype=np.float64) for p in points1]
    points2 = [np.asarray(p, dtype=np.float64) for p in points2]

    log_sum = 0.0
    count = 0

    for p1 in points1:
        for p2 in points2:
            r = np.linalg.norm(p1 - p2)
            if r > 1e-15:
                log_sum += np.log(r)
                count += 1

    if count == 0:
        return 0.0

    return np.exp(log_sum / count)


@maxwell_cite(
    691,
    692,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate self GMD of circular cross-section",
)
def calc_self_gmd_circle(
    radius: float,
) -> float:
    """
    Calculate self geometric mean distance of a circular cross-section.

    Art. 691-692: For a circular cross-section of radius a:

        GMD_self = a * exp(-1/4) ≈ 0.7788 * a

    This is EXACT (not an approximation): it follows by evaluating the
    defining double-area integral in polar coordinates (Maxwell,
    Treatise Art. 691; verified 2026-08-21 against the numerical
    quadruple integral in tests/test_articles_math_spine_691_706.py).
    Used in the self-inductance formula for a wire with finite
    cross-section.

    Args:
        radius: Wire radius (cm).

    Returns:
        Self GMD (cm).
    """
    return radius * np.exp(-0.25)


@maxwell_cite(
    691,
    692,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate GMD of rectangular cross-section",
)
def calc_self_gmd_rectangle(
    width: float,
    height: float,
) -> float:
    """
    Calculate self GMD of a rectangular cross-section.

    Art. 691-692: For a rectangle of width w and height h (Kennelly's
    approximation for the self-GMD of a rectangular section):

        GMD ≈ (0.44705 / 2) * (w + h)

    Accuracy (checked 2026-08-21 against the defining double-area
    integral, reduced to a single 2-D integral by the overlap-area
    trick and evaluated by tensor Gauss-Legendre quadrature; see
    tests/test_articles_math_spine_691_706.py): exact for a square to
    ~2e-6 relative (true value 0.44704916·a for side a), ≤ 8e-4
    relative for aspect ratios up to 10:1, and reproduces the thin-strip
    (segment) limit GMD → w·e^{−3/2} ≈ 0.22313·w to ~2e-3 as h → 0.

    NOTE: the pre-2026-08-21 code omitted the factor 1/2 (it returned
    0.44705·(w+h), twice the correct value — already 2x off for a
    square, and impossible in the thin-strip limit where the exact GMD
    is 0.2231·w).

    Args:
        width: Width of rectangle (cm).
        height: Height of rectangle (cm).

    Returns:
        Self GMD (cm).
    """
    # Kennelly approximation with the correct normalization (see note)
    return 0.44705 * (width + height) / 2.0


@maxwell_cite(
    691,
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate GMD between two parallel wires",
)
def calc_gmd_parallel_wires(
    wire1_center: np.ndarray,
    wire2_center: np.ndarray,
    wire1_radius: float,
    wire2_radius: float,
) -> float:
    """
    Calculate GMD between two parallel wires.

    Art. 691-693: For two parallel wires with circular cross-sections
    (radii a1, a2) whose centres are d apart:

        GMD = d  EXACTLY,  whenever the sections do not overlap
                 (d >= a1 + a2).

    Proof: ln|r1 − r2| is harmonic in r2 away from r1, so if r1 lies
    outside disk 2 the mean-value property gives the inner average
    (1/A2)∫ ln|r1−r2| dA2 = ln|r1−c2|; that function is in turn harmonic
    in r1 over disk 1 whenever c2 lies outside it, so the outer average
    is ln|c1−c2| = ln d.  EVERY correction term vanishes identically —
    this is the classical result behind the two-wire-line formula.

    For overlapping sections (d < a1 + a2, not a physical configuration
    for distinct wires but needed for continuity) the defining double
    integral is evaluated by the exact one-dimensional reduction in
    :func:`_gmd_overlapping_disks`; it reproduces the self-GMD
    a·e^{−1/4} at d = 0, a1 = a2 = a, and joins GMD = d continuously at
    contact.

    NOTE: the pre-2026-08-21 code returned d·(1 − (a1²+a2²)/(4d²)) for
    all d.  That correction is spurious at EVERY separation (the true
    disjoint value is exactly d; even the RMS-distance expansion has the
    opposite sign); it was caught by testing against the exact value and
    a direct tensor Gauss-Legendre quadrature of the defining integral
    (tests/test_articles_math_spine_691_706.py).

    Args:
        wire1_center: Center of first wire (cm).
        wire2_center: Center of second wire (cm).
        wire1_radius: Radius of first wire (cm).
        wire2_radius: Radius of second wire (cm).

    Returns:
        GMD between wires (cm).
    """
    wire1_center = np.asarray(wire1_center, dtype=np.float64)
    wire2_center = np.asarray(wire2_center, dtype=np.float64)

    d = float(np.linalg.norm(wire2_center - wire1_center))
    a1 = wire1_radius
    a2 = wire2_radius

    if d >= a1 + a2:
        # Disjoint circular sections: exact by the mean-value property
        # of the harmonic log kernel (see docstring).
        return d

    return _gmd_overlapping_disks(a1, a2, d)


@maxwell_cite(
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate GMD between two circular coils",
)
def calc_gmd_coaxial_circles(
    radius1: float,
    radius2: float,
    axial_separation: float,
    n_points: int = 100,
) -> float:
    """
    Calculate GMD between two coaxial circular loops.

    Art. 692-693: For two coaxial circular loops of radii a and b,
    separated by distance z, the GMD is the geometric mean of the
    distance over ALL pairs of points on the two loops:

        ln GMD = (2π)^{-2} ∬ ln|r(θ) − r'(θ')| dθ dθ'.

    Because |r − r'|² = a² + b² + z² − 2ab·cos(θ−θ') depends only on the
    difference angle, one integration is immediate and the other is the
    classical identity ∫₀^{2π} ln(A − B cos t) dt = 2π ln((A + √(A²−B²))/2),
    giving the EXACT closed form (no quadrature needed):

        GMD = sqrt( (A + sqrt(A² − B²)) / 2 ),
        A = a² + b² + z²,  B = 2ab.

    Limits: for z → 0, a = b this returns a (the known self-GMD of a
    circular filament); for z ≫ a, b it gives z·(1 + (a²+b²)/(2z²)),
    i.e. slightly LARGER than the center distance (ring, not disk,
    geometry).  NOTE: the pre-2026-08-21 code only paired points at
    EQUAL angles (effectively returning sqrt((a−b)² + z²)); the closed
    form above replaces that sampling bug.

    Args:
        radius1: Radius of first loop (cm).
        radius2: Radius of second loop (cm).
        axial_separation: Axial distance (cm).
        n_points: Retained for backward compatibility; the closed form
            is exact and does not use it.

    Returns:
        GMD between loops (cm).
    """
    del n_points  # closed form — sampling no longer required
    A = radius1**2 + radius2**2 + axial_separation**2
    B = 2.0 * radius1 * radius2
    return float(np.sqrt(0.5 * (A + np.sqrt(max(A * A - B * B, 0.0)))))


@maxwell_cite(
    691,
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate inductance correction from GMD",
)
def calc_inductance_from_gmd(
    filament_inductance: float,
    wire_radius: float,
    coil_radius: float,
) -> float:
    """
    Calculate inductance with GMD correction for finite wire thickness.

    Art. 691-693: The inductance of a coil with finite wire thickness
    is corrected from the filament value using the GMD:

        L = L_filament - 4*pi*N^2*R * (ln(8R/a) - ln(8R/GMD))

    where GMD = a*exp(-1/4) for a circular wire.

    The correction accounts for the current distribution within
    the wire cross-section.

    Args:
        filament_inductance: Inductance for infinitesimal wire (cm).
        wire_radius: Wire radius (cm).
        coil_radius: Mean coil radius (cm).

    Returns:
        Corrected inductance (cm).
    """
    gmd = calc_self_gmd_circle(wire_radius)

    # GMD correction: L_corrected = L_filament - 4*pi*N^2*R*ln(a/GMD)
    # For a single turn (N=1):
    # ln(a/GMD) = ln(a/(a*exp(-1/4))) = 1/4
    correction = 4.0 * np.pi * coil_radius * np.log(wire_radius / gmd)

    return filament_inductance - correction


@dataclass
class GMDCalculator:
    """
    Geometric mean distance calculator.

    Art. 691-693: Provides methods for calculating GMD for various
    conductor geometries, used in inductance corrections.

    Attributes:
        wire_radius: Wire radius for self-GMD calculations.
    """

    wire_radius: float

    @maxwell_cite(
        691,
        part=4,
        chapter="Geometric Mean Distance",
        theory_class="maxwell_original",
        description="Get self GMD",
    )
    def self_gmd(self) -> float:
        """Self GMD of wire cross-section."""
        return calc_self_gmd_circle(self.wire_radius)

    @maxwell_cite(
        691,
        692,
        part=4,
        chapter="Geometric Mean Distance",
        theory_class="maxwell_original",
        description="Get GMD to another wire",
    )
    def gmd_to(
        self, other_center: np.ndarray, my_center: np.ndarray, other_radius: float
    ) -> float:
        """GMD between this wire and another."""
        return calc_gmd_parallel_wires(
            my_center, other_center, self.wire_radius, other_radius
        )


@maxwell_cite(
    691,
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Verify GMD relations",
)
def verify_gmd_relations(
    tolerance: float = 1e-6,
) -> dict[str, float | bool]:
    """
    Verify geometric mean distance relations.

    Art. 691-693: This function verifies:
    1. Self GMD of circle = a*exp(-1/4)
    2. Mutual GMD of two DISJOINT circular sections equals the
       center-to-center distance EXACTLY (mean-value property of the
       harmonic log kernel) — checked at two separations.  (The
       pre-2026-08-21 version asserted GMD < d here, which is false
       for filled circular sections.)
    3. Self GMD < radius.

    Args:
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Self GMD of circle
    a = 1.0
    gmd_self = calc_self_gmd_circle(a)
    expected_self = a * np.exp(-0.25)
    self_error = abs(gmd_self - expected_self) / expected_self

    # GMD between distant wires: exactly the centre distance
    c1 = np.array([0.0, 0.0, 0.0])
    c2 = np.array([100.0, 0.0, 0.0])
    gmd_wires = calc_gmd_parallel_wires(c1, c2, 0.1, 0.1)
    expected_wires = 100.0
    wires_error = abs(gmd_wires - expected_wires) / expected_wires

    # Same exactness at a moderate separation (disjoint sections)
    c3 = np.array([1.0, 0.0, 0.0])
    gmd_close = calc_gmd_parallel_wires(c1, c3, 0.1, 0.1)
    gmd_equals_distance = abs(gmd_close - 1.0) <= 1e-12

    # Self GMD < radius always
    gmd_less_than_radius = gmd_self < a

    return {
        "self_gmd": gmd_self,
        "expected_self_gmd": expected_self,
        "self_gmd_error": self_error,
        "distant_wires_gmd": gmd_wires,
        "distant_wires_error": wires_error,
        "gmd_equals_distance": bool(gmd_equals_distance),
        "gmd_less_than_radius": bool(gmd_less_than_radius),
        "self_gmd_verified": bool(self_error < tolerance),
        "distant_wires_verified": bool(wires_error < tolerance),
        "verified": bool(
            self_error < tolerance
            and wires_error < tolerance
            and gmd_equals_distance
            and gmd_less_than_radius
        ),
    }


@maxwell_cite(
    691,
    692,
    693,
    part=4,
    chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Complete GMD analysis",
)
def analyze_gmd(
    wire_radius: float = 0.1,
    coil_radius: float = 10.0,
    separations: list[float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of geometric mean distance.

    Art. 691-693: Comprehensive analysis including:
    1. Self GMD for various wire radii
    2. GMD between wires at various separations
    3. Inductance correction from GMD

    Args:
        wire_radius: Wire radius (cm).
        coil_radius: Coil radius (cm).
        separations: Wire separations to test (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    if separations is None:
        separations = [1.0, 2.0, 5.0, 10.0, 20.0]

    # Self GMD
    gmd_self = calc_self_gmd_circle(wire_radius)

    # GMD between wires
    c1 = np.array([0.0, 0.0, 0.0])
    gmd_values = []
    for sep in separations:
        c2 = np.array([sep, 0.0, 0.0])
        gmd = calc_gmd_parallel_wires(c1, c2, wire_radius, wire_radius)
        gmd_values.append(gmd)

    # Inductance correction
    L_filament = (
        4.0 * np.pi * coil_radius * (np.log(8 * coil_radius / wire_radius) - 2.0)
    )
    L_corrected = calc_inductance_from_gmd(L_filament, wire_radius, coil_radius)

    return {
        "wire_radius": wire_radius,
        "coil_radius": coil_radius,
        "self_gmd": gmd_self,
        "gmd_ratio": gmd_self / wire_radius,
        "separations": separations,
        "gmd_values": gmd_values,
        "filament_inductance": L_filament,
        "corrected_inductance": L_corrected,
        "gmd_correction": L_filament - L_corrected,
    }
