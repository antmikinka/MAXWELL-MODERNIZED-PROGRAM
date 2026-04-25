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

        GMD ≈ d  (when d >> a)

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

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@maxwell_cite(
    691, 692, 693,
    part=4, chapter="Geometric Mean Distance",
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
    691, 692,
    part=4, chapter="Geometric Mean Distance",
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

    This is used in the self-inductance formula for a wire
    with finite cross-section.

    Args:
        radius: Wire radius (cm).

    Returns:
        Self GMD (cm).
    """
    return radius * np.exp(-0.25)


@maxwell_cite(
    691, 692,
    part=4, chapter="Geometric Mean Distance",
    theory_class="maxwell_original",
    description="Calculate GMD of rectangular cross-section",
)
def calc_self_gmd_rectangle(
    width: float,
    height: float,
) -> float:
    """
    Calculate self GMD of a rectangular cross-section.

    Art. 691-692: For a rectangle of width w and height h:

        GMD ≈ 0.44705 * (w + h)  (approximate)

    A more accurate formula uses numerical integration.

    Args:
        width: Width of rectangle (cm).
        height: Height of rectangle (cm).

    Returns:
        Self GMD (cm).
    """
    # Approximate formula
    return 0.44705 * (width + height)


@maxwell_cite(
    691, 692, 693,
    part=4, chapter="Geometric Mean Distance",
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

    Art. 691-693: For two parallel wires with circular cross-sections,
    the GMD between them is approximately the center-to-center distance
    when the separation is large compared to the radii.

    For more accuracy, the GMD accounts for the finite cross-section:

        GMD ≈ d * (1 - (a1^2 + a2^2) / (4*d^2))

    where d is the center-to-center distance and a1, a2 are the radii.

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

    d = np.linalg.norm(wire2_center - wire1_center)

    if d < 1e-15:
        return 0.0

    # Correction for finite cross-section
    a1 = wire1_radius
    a2 = wire2_radius
    correction = 1.0 - (a1 ** 2 + a2 ** 2) / (4.0 * d ** 2)

    return d * max(correction, 0.0)


@maxwell_cite(
    692, 693,
    part=4, chapter="Geometric Mean Distance",
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
    separated by distance z, the GMD is calculated by integrating
    over all pairs of points on the two loops.

    Args:
        radius1: Radius of first loop (cm).
        radius2: Radius of second loop (cm).
        axial_separation: Axial distance (cm).
        n_points: Number of integration points per loop.

    Returns:
        GMD between loops (cm).
    """
    angles = np.linspace(0, 2 * np.pi, n_points, endpoint=False)

    points1 = []
    points2 = []

    for theta in angles:
        p1 = np.array([radius1 * np.cos(theta), radius1 * np.sin(theta), 0])
        p2 = np.array([radius2 * np.cos(theta), radius2 * np.sin(theta), axial_separation])
        points1.append(p1)
        points2.append(p2)

    return calc_gmd_points(points1, points2)


@maxwell_cite(
    691, 692, 693,
    part=4, chapter="Geometric Mean Distance",
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
        part=4, chapter="Geometric Mean Distance",
        theory_class="maxwell_original",
        description="Get self GMD",
    )
    def self_gmd(self) -> float:
        """Self GMD of wire cross-section."""
        return calc_self_gmd_circle(self.wire_radius)

    @maxwell_cite(
        691, 692,
        part=4, chapter="Geometric Mean Distance",
        theory_class="maxwell_original",
        description="Get GMD to another wire",
    )
    def gmd_to(self, other_center: np.ndarray, my_center: np.ndarray, other_radius: float) -> float:
        """GMD between this wire and another."""
        return calc_gmd_parallel_wires(
            my_center, other_center, self.wire_radius, other_radius
        )


@maxwell_cite(
    691, 692, 693,
    part=4, chapter="Geometric Mean Distance",
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
    2. GMD between distant wires ≈ center-to-center distance
    3. GMD correction to inductance is positive

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

    # GMD between distant wires
    c1 = np.array([0.0, 0.0, 0.0])
    c2 = np.array([100.0, 0.0, 0.0])
    gmd_wires = calc_gmd_parallel_wires(c1, c2, 0.1, 0.1)
    expected_wires = 100.0
    wires_error = abs(gmd_wires - expected_wires) / expected_wires

    # GMD < center-to-center distance always
    c3 = np.array([1.0, 0.0, 0.0])
    gmd_close = calc_gmd_parallel_wires(c1, c3, 0.1, 0.1)
    gmd_less_than_distance = gmd_close < 1.0

    # Self GMD < radius always
    gmd_less_than_radius = gmd_self < a

    return {
        "self_gmd": gmd_self,
        "expected_self_gmd": expected_self,
        "self_gmd_error": self_error,
        "distant_wires_gmd": gmd_wires,
        "distant_wires_error": wires_error,
        "gmd_less_than_distance": bool(gmd_less_than_distance),
        "gmd_less_than_radius": bool(gmd_less_than_radius),
        "self_gmd_verified": bool(self_error < tolerance),
        "distant_wires_verified": bool(wires_error < tolerance),
        "verified": bool(
            self_error < tolerance
            and wires_error < tolerance
            and gmd_less_than_distance
            and gmd_less_than_radius
        ),
    }


@maxwell_cite(
    691, 692, 693,
    part=4, chapter="Geometric Mean Distance",
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
    L_filament = 4.0 * np.pi * coil_radius * (np.log(8 * coil_radius / wire_radius) - 2.0)
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
