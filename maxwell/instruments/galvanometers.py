"""maxwell.instruments.galvanometers — Standard galvanometers (Arts. 707-720).

Part IV, Chapter XV "Electromagnetic Instruments": standard and sensitive
galvanometers, tangent/sine principles, single- and multi-coil designs,
Gaugain's eccentric suspension, and uniform-wire sensitivity.

Unit convention — Gaussian CGS with explicit c (repo convention,
Stage-3 defect D-16 resolution; c is always ``CONST.C`` from
``maxwell.config.constants``, never a bare literal):
    currents      : statampere (statA)
    fields        : gauss (= oersted in vacuum)
    torques       : dyne.cm
    magnetic moment: emu (erg/gauss)
The Gaussian Biot-Savart law reads dB = (I/c) dl x r_hat / r^2, so the
field at the centre of a circular coil is B = 2.pi.n.I/(c.R) and the
galvanometer constant is G = 2.pi.n/(c.R) (gauss per statampere). This is
the same convention used by ``maxwell.electromagnetism.components.
circular_coils``; the direct agreement of the two modules for the same
physical coil is pinned by ``tests/test_d16_c_convention_consistency.py``
(D-16 consistency test). A current of I_stat statamperes corresponds to
I_stat/CONST.C abamperes, so these formulas equal the EMU forms divided
by c.

Article correspondence (Treatise Vol. II, Part IV, Ch. XV):
    707-708  standard galvanometer; principles of construction
    709      mathematical theory: torque balance, tangent law with torsion
    710      tangent and sine galvanometers
    711      single-coil galvanometer
    712      Gaugain's eccentric suspension
    714      four-coil galvanometer
    715      three-coil galvanometer
    717      design of a sensitive galvanometer
    720      uniform-wire galvanometer; sensitivity at zero deflection
(Arts. 713, 716, 718, 719 live in ``maxwell.instruments.helmholtz`` and
``maxwell.instruments.optimization.sensitivity``.)
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi


def _bisect_root(f, lo: float, hi: float, iterations: int = 100) -> float:
    """Bisection root of a continuous ``f`` with ``f(lo)*f(hi) <= 0``.

    Pure-python bisection (no LAPACK involvement): 100 halvings shrink the
    bracket by 2**-100, which is far below double-precision resolution.
    """
    flo = f(lo)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if flo * fmid <= 0.0:
            hi = mid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Art. 707-708: Standard galvanometer construction
# ---------------------------------------------------------------------------


@dataclass
class StandardGalvanometer:
    """Standard galvanometer coil (Arts. 707-708).

    A precisely wound coil of known geometry used as a reference
    instrument for measuring current by the deflection of a suspended
    magnet at its centre.

    Attributes:
        n_turns: Number of turns in the coil.
        mean_radius: Mean radius of the coil (cm).
        wire_radius: Radius of the wire itself (cm).
        coil_depth: Axial depth of the winding (cm).
        coil_constant: Galvanometer constant G (computed, gauss per
            statampere: G.I is the field in gauss produced at the centre
            by current I in statamperes).
    """

    n_turns: int
    mean_radius: float  # cm
    wire_radius: float  # cm
    coil_depth: float  # cm
    coil_constant: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        """Compute the galvanometer constant after initialization."""
        self.coil_constant = self._compute_coil_constant()

    @maxwell_cite(
        707,
        part=4,
        theory_class="standard_math",
        description="Galvanometer constant G = 2.pi.n/(c.R) of a thin circular coil",
    )
    def _compute_coil_constant(self) -> float:
        """Compute G = 2.pi.n/(c.R) for a single-layer coil.

        Leading-order Gaussian result (explicit c per the D-16 repo
        convention) for a coil thin compared with its radius: the field at
        the centre is B = G.I with G = 2.pi.n/(CONST.C.R) (gauss per
        statampere). Corrections from the finite winding cross-section are
        of relative order (coil_depth/R)^2 and (wire_radius/R)^2 and are
        neglected at this tier (they are the subject of the Art. 709
        figure-of-coil analysis).
        """
        return 2.0 * PI * self.n_turns / (CONST.C * self.mean_radius)


@maxwell_cite(
    708,
    part=4,
    theory_class="standard_math",
    description="Design a standard coil: radius, turn count and winding depth",
)
def design_standard_coil(
    target_constant: float,
    wire_radius: float,
    max_radius: float,
) -> dict[str, float]:
    """Design a standard coil to achieve a target galvanometer constant.

    Construction rules (replacing the former 0.9*max_radius /
    2*r_wire*sqrt(n) heuristics flagged as Stage-3 defect D-31):

    1. Mean radius: wind at the largest available radius. Art. 708 requires
       the field to be sensibly uniform over the whole excursion of the
       suspended magnet; the leading spatial-gradient correction to the
       centre field scales as (magnet size / R)^2, so larger R is better,
       and the target constant then fixes the turn count.
    2. Turn count: from G = 2.pi.n/(c.R), n = ceil(G.c.R/(2.pi)) so the
       achieved constant meets or exceeds the target by less than one
       turn's worth.
    3. Winding depth: close-wound layers. Turns per layer =
       floor(2.pi.R / (2*r_wire)); layers = ceil(n / turns_per_layer);
       axial depth = layers * 2*r_wire.

    Args:
        target_constant: Desired G value (cm^-1).
        wire_radius: Radius of available wire (cm).
        max_radius: Maximum allowable coil radius (cm).

    Returns:
        Dictionary with n_turns, mean_radius, coil_depth and the achieved
        coil_constant.

    Raises:
        ValueError: for non-positive inputs or wire too thick to place one
            turn per layer at max_radius.
    """
    if target_constant <= 0.0 or wire_radius <= 0.0 or max_radius <= 0.0:
        raise ValueError("target_constant, wire_radius and max_radius must be positive")

    mean_radius = float(max_radius)

    n_turns = int(np.ceil(target_constant * CONST.C * mean_radius / (2.0 * PI)))

    turns_per_layer = int(np.floor(2.0 * PI * mean_radius / (2.0 * wire_radius)))
    if turns_per_layer < 1:
        raise ValueError(
            "wire too thick to wind one turn per layer at the given radius"
        )
    n_layers = int(np.ceil(n_turns / turns_per_layer))
    coil_depth = 2.0 * wire_radius * n_layers

    return {
        "n_turns": n_turns,
        "mean_radius": mean_radius,
        "coil_depth": coil_depth,
        "coil_constant": 2.0 * PI * n_turns / (CONST.C * mean_radius),
    }


# ---------------------------------------------------------------------------
# Art. 709: Mathematical theory of the galvanometer
# ---------------------------------------------------------------------------


@maxwell_cite(
    709,
    part=4,
    theory_class="standard_math",
    description="Implicit torque balance mGI cos(t) = mH sin(t) + tau*t",
)
def calc_galvanometer_response(
    current: float,
    coil_constant: float,
    horizontal_field: float,
    magnetic_moment: float,
    torsion_constant: float = 0.0,
) -> float:
    """Calculate needle deflection angle for a given current (Art. 709).

    The magnet of moment ``m`` hangs at the centre of a coil whose plane
    contains the magnetic meridian, so the coil field G.I acts at right
    angles to the terrestrial horizontal field H. With the needle deflected
    by theta from the meridian and a suspension fiber of torsion constant
    tau (dyne.cm/rad), the torque balance is

        m.G.I.cos(theta) = m.H.sin(theta) + tau.theta

    (deflecting coil torque = terrestrial restoring torque + torsion).
    For tau = 0 this reduces to the tangent law tan(theta) = G.I/H; with
    torsion the equation is implicit in theta and is solved by bisection.
    Fixes Stage-3 defect D-15 (the torsion term previously added a torque
    constant to a field without division by the magnetic moment). The
    balance is convention-invariant in form: G.I is the coil field in
    gauss, so with the D-16 Gaussian convention G (gauss per statampere)
    and I (statamperes) the same equation holds.

    Args:
        current: Current through coil (statamperes).
        coil_constant: G constant of the coil (gauss per statampere).
        horizontal_field: Terrestrial horizontal field H (gauss).
        magnetic_moment: Magnetic moment of the needle (emu), must be > 0.
        torsion_constant: Suspension torsion constant (dyne.cm/rad), >= 0.

    Returns:
        Deflection angle theta in radians (sign follows the current).

    Raises:
        ValueError: if magnetic_moment or horizontal_field is not positive,
            or torsion_constant is negative.
    """
    if magnetic_moment <= 0.0:
        raise ValueError("magnetic_moment must be positive")
    if horizontal_field <= 0.0:
        raise ValueError("horizontal_field must be positive")
    if torsion_constant < 0.0:
        raise ValueError("torsion_constant must be non-negative")

    if current == 0.0:
        return 0.0

    m = magnetic_moment
    sign = 1.0 if current > 0.0 else -1.0
    gi = coil_constant * abs(current)

    def balance(theta: float) -> float:
        return (
            m * gi * np.cos(theta)
            - m * horizontal_field * np.sin(theta)
            - torsion_constant * theta
        )

    # balance(0) = m*gi >= 0 and balance(pi/2) = -m*H - tau*pi/2 < 0, and
    # balance'(theta) = -m*gi*sin - m*H*cos - tau < 0 on (0, pi/2), so the
    # root is unique.
    theta = _bisect_root(balance, 0.0, 0.5 * PI)
    return sign * theta


@maxwell_cite(
    709,
    part=4,
    theory_class="standard_math",
    description="Field at the centre of a circular coil, Gaussian Biot-Savart",
)
def calc_field_at_center(
    current: float,
    n_turns: int,
    radius: float,
) -> float:
    """Calculate magnetic field at center of circular coil.

    Gaussian Biot-Savart with explicit c (D-16 repo convention; current in
    statamperes):

        B = 2.pi.n.I / (c.R)   (gauss, at the centre of a circular coil)

    Args:
        current: Current in statamperes.
        n_turns: Number of turns.
        radius: Coil radius in cm.

    Returns:
        Field B in gauss.
    """
    return 2.0 * PI * n_turns * current / (CONST.C * radius)


# ---------------------------------------------------------------------------
# Art. 710: Tangent and sine galvanometer principles
# ---------------------------------------------------------------------------


@dataclass
class TangentGalvanometer:
    """Tangent galvanometer (Art. 710).

    The coil is fixed with its plane in the magnetic meridian; the current
    is proportional to the tangent of the needle deflection:

        I = (H / G) * tan(theta)

    Attributes:
        coil_constant: G constant of the coil (gauss per statampere).
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    coil_constant: float
    horizontal_field: float

    @maxwell_cite(
        710,
        part=4,
        theory_class="standard_math",
        description="Tangent law I = (H/G) tan(theta)",
    )
    def current_from_deflection(self, theta_rad: float) -> float:
        """Calculate current from deflection angle.

        I = (H/G) * tan(theta)

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in statamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)

    @maxwell_cite(
        710,
        part=4,
        theory_class="standard_math",
        description="Inverse tangent law theta = arctan(G I / H)",
    )
    def deflection_from_current(self, current: float) -> float:
        """Calculate deflection angle from current.

        theta = arctan(G*I / H)

        Args:
            current: Current in statamperes.

        Returns:
            Deflection angle in radians.
        """
        return np.arctan(self.coil_constant * current / self.horizontal_field)


@dataclass
class SineGalvanometer:
    """Sine galvanometer (Art. 710).

    The coil is rotated about its vertical axis until the needle reads zero
    (needle lying in the plane of the coil); the current is then
    proportional to the sine of the rotation angle alpha measured between
    the plane of the coil and the magnetic meridian:

        I = (H / G) * sin(alpha)

    Derivation: with the needle back in the meridian, the total field
    (terrestrial H along the meridian plus coil field G.I along the coil
    normal) must lie along the needle; resolving perpendicular to the
    needle gives G.I = H.sin(alpha).

    Attributes:
        coil_constant: G constant of the coil (gauss per statampere).
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    coil_constant: float
    horizontal_field: float

    @maxwell_cite(
        710,
        part=4,
        theory_class="standard_math",
        description="Sine law I = (H/G) sin(alpha)",
    )
    def current_from_rotation(self, alpha_rad: float) -> float:
        """Calculate current from coil rotation angle.

        I = (H/G) * sin(alpha)

        Args:
            alpha_rad: Rotation angle in radians (coil plane vs meridian).

        Returns:
            Current in statamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.sin(alpha_rad)


# ---------------------------------------------------------------------------
# Art. 711: Single-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class SingleCoilGalvanometer:
    """Galvanometer with a single circular coil (Art. 711).

    Simplest form: one coil with a suspended needle at the center.

    Attributes:
        n_turns: Number of turns.
        radius: Coil radius (cm).
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    n_turns: int
    radius: float
    horizontal_field: float

    @property
    def coil_constant(self) -> float:
        """G = 2.pi.n / (c.R) (gauss per statampere)."""
        return 2.0 * PI * self.n_turns / (CONST.C * self.radius)

    @maxwell_cite(
        711,
        part=4,
        theory_class="standard_math",
        description="Single-coil tangent-law current measurement",
    )
    def measure_current(self, theta_rad: float) -> float:
        """Measure current from tangent-law deflection.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in statamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 712: Gaugain's eccentric suspension
# ---------------------------------------------------------------------------


def gaugain_offset(radius: float) -> float:
    """Gaugain's eccentric suspension point (Art. 712).

    Gaugain suspended the needle on the coil axis at a distance of half
    the radius from the centre; at this point the leading correction to
    the tangent law due to the finite length of the needle cancels,
    extending the angular range over which I = (H/G) tan(theta) holds.

    Args:
        radius: Coil radius (cm).

    Returns:
        Axial offset of the suspension point from the coil centre (cm).
    """
    return 0.5 * radius


@maxwell_cite(
    712,
    part=4,
    theory_class="standard_math",
    description="Axial field at the Gaugain eccentric suspension point",
)
def apply_gaugain_suspension(
    radius: float,
    needle_offset: float,
    n_turns: int,
    current: float,
) -> float:
    """Calculate field at the Gaugain eccentric needle position.

    Gaussian axial field of a circular coil at offset z along its axis
    (explicit c per the D-16 repo convention):

        B(z) = 2.pi.n.I.R^2 / (c.(R^2 + z^2)^(3/2))

    With ``needle_offset = gaugain_offset(radius) = R/2`` this evaluates to
    B = (2.pi.n.I/(c.R)) * (4/5)^(3/2).

    Args:
        radius: Coil radius (cm).
        needle_offset: Distance of needle from coil center along the
            axis (cm); use :func:`gaugain_offset` for the Gaugain point.
        n_turns: Number of turns.
        current: Current (statamperes).

    Returns:
        Field at the offset position (gauss).
    """
    r2 = radius**2
    z2 = needle_offset**2
    return 2.0 * PI * n_turns * current * r2 / (CONST.C * (r2 + z2) ** 1.5)


# ---------------------------------------------------------------------------
# Art. 714: Four-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class FourCoilGalvanometer:
    """Galvanometer with four coils (Art. 714).

    Four coaxial coils (two inner, two outer) connected so their fields
    aid at the common centre, giving a stronger and more uniform field
    than a single coil of the same resistance budget. The combined
    constant is the sum of the individual constants.

    Attributes:
        inner_radius: Radius of each inner coil (cm).
        outer_radius: Radius of each outer coil (cm).
        n_turns_inner: Total turns on the inner pair.
        n_turns_outer: Total turns on the outer pair.
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    inner_radius: float
    outer_radius: float
    n_turns_inner: int
    n_turns_outer: int
    horizontal_field: float

    @maxwell_cite(
        714,
        part=4,
        theory_class="standard_math",
        description="Combined constant G = sum 2.pi.n_i/R_i of aiding coaxial coils",
    )
    def combined_coil_constant(self) -> float:
        """Calculate combined G constant for the four-coil arrangement.

        G = G_inner + G_outer; all coils are coaxial and connected so
        their centre fields add. Each G_i = 2.pi.n_i/(c.R_i) (gauss per
        statampere, D-16 convention).
        """
        g_inner = 2.0 * PI * self.n_turns_inner / (CONST.C * self.inner_radius)
        g_outer = 2.0 * PI * self.n_turns_outer / (CONST.C * self.outer_radius)
        return g_inner + g_outer

    @maxwell_cite(
        714,
        part=4,
        theory_class="standard_math",
        description="Tangent-law measurement with the combined constant",
    )
    def measure_current(self, theta_rad: float) -> float:
        """Measure current using tangent law with combined constant.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in statamperes.
        """
        g = self.combined_coil_constant()
        return (self.horizontal_field / g) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 715: Three-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class ThreeCoilGalvanometer:
    """Galvanometer with three coils (Art. 715).

    Three coaxial aiding coils, an intermediate arrangement between the
    single coil and the four-coil design.

    Attributes:
        radii: Radii of the three coils (cm).
        n_turns: Turns on each coil.
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    radii: tuple[float, float, float]
    n_turns: tuple[int, int, int]
    horizontal_field: float

    @maxwell_cite(
        715,
        part=4,
        theory_class="standard_math",
        description="Combined constant G = sum 2.pi.n_i/R_i of three coaxial coils",
    )
    def combined_coil_constant(self) -> float:
        """Calculate combined G constant for three-coil arrangement.

        Each G_i = 2.pi.n_i/(c.R_i) (gauss per statampere, D-16 convention).
        """
        return sum(
            2.0 * PI * n / (CONST.C * r) for n, r in zip(self.n_turns, self.radii)
        )

    @maxwell_cite(
        715,
        part=4,
        theory_class="standard_math",
        description="Tangent-law measurement with the combined constant",
    )
    def measure_current(self, theta_rad: float) -> float:
        """Measure current using tangent law.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in statamperes.
        """
        g = self.combined_coil_constant()
        return (self.horizontal_field / g) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 717: Design of a sensitive galvanometer
# ---------------------------------------------------------------------------


@maxwell_cite(
    717,
    part=4,
    theory_class="standard_math",
    description="Design with a given wire: all wire used; R_coil vs R_ext reported",
)
def design_sensitive_galvanometer(
    wire_length: float,
    wire_resistance: float,
    target_resistance: float,
    mean_radius: float,
) -> dict[str, float]:
    """Design a sensitive galvanometer from a given length of wire (Art. 717).

    For a coil of given mean radius R wound from wire of resistance
    rho_l per unit length, the deflection produced by a battery of EMF E
    and external resistance R_ext is proportional to

        G.I = (L/R^2) * E / (R_ext + rho_l.L),      L = wire length used,

    since G = 2.pi.n/(c.R) with n = L/(2.pi.R). The derivative with
    respect to L is E.R_ext / (c.R^2 (R_ext + rho_l.L)^2) > 0, so the
    whole available wire should be wound on. The coil is therefore wound
    with n = floor(L/(2.pi.R)) turns; the achieved coil resistance
    rho_l.2.pi.R.n is reported against the Art.-718 matching target
    R_ext (see ``optimization.sensitivity.optimize_galvanometer_sensitivity``
    for the re-winding optimum when the wire volume, not length, is fixed).

    Args:
        wire_length: Total available wire length (cm).
        wire_resistance: Resistance per unit length (statohm/cm).
        target_resistance: External circuit resistance to match (statohm).
        mean_radius: Mean coil radius to wind on (cm).

    Returns:
        Design parameters dict: n_turns, mean_radius, coil_resistance,
        galvanometer_constant, sensitivity_merit (= G/(R_coil + R_ext),
        proportional to deflection per unit EMF at fixed H), matched
        (True when coil and external resistances agree within 1%).

    Raises:
        ValueError: for non-positive inputs or wire shorter than one turn.
    """
    if (
        wire_length <= 0.0
        or wire_resistance <= 0.0
        or target_resistance <= 0.0
        or mean_radius <= 0.0
    ):
        raise ValueError("all design inputs must be positive")

    n_turns = int(np.floor(wire_length / (2.0 * PI * mean_radius)))
    if n_turns < 1:
        raise ValueError("wire too short for a single turn at the given radius")

    used_length = n_turns * 2.0 * PI * mean_radius
    coil_resistance = wire_resistance * used_length
    galvanometer_constant = 2.0 * PI * n_turns / (CONST.C * mean_radius)
    merit = galvanometer_constant / (coil_resistance + target_resistance)

    return {
        "n_turns": n_turns,
        "mean_radius": mean_radius,
        "coil_resistance": coil_resistance,
        "galvanometer_constant": galvanometer_constant,
        "sensitivity_merit": merit,
        "matched": bool(
            abs(coil_resistance - target_resistance) <= 0.01 * target_resistance
        ),
    }


# ---------------------------------------------------------------------------
# Art. 720: Uniform-wire galvanometer and zero-deflection sensitivity
# ---------------------------------------------------------------------------


@maxwell_cite(
    720,
    part=4,
    theory_class="standard_math",
    description="Zero-deflection sensitivity d(theta)/dI = G/H",
)
def calc_uniform_wire_sensitivity(
    n_turns: int,
    radius: float,
    horizontal_field: float,
) -> float:
    """Calculate sensitivity of uniform-wire galvanometer.

    Sensitivity = d(theta)/dI at zero deflection = G/H, since
    theta = arctan(G.I/H).

    Args:
        n_turns: Number of turns.
        radius: Coil radius (cm).
        horizontal_field: Terrestrial horizontal field (gauss).

    Returns:
        Sensitivity in radians per statampere.
    """
    g = 2.0 * PI * n_turns / (CONST.C * radius)
    return g / horizontal_field


@dataclass
class UniformWireGalvanometer:
    """Galvanometer with uniform thickness wire (Art. 720).

    The simplest and most common construction, using wire of
    constant gauge throughout the winding.

    Attributes:
        n_turns: Number of turns.
        radius: Coil radius (cm).
        wire_gauge: Wire radius (cm).
        horizontal_field: Terrestrial horizontal field (gauss).
    """

    n_turns: int
    radius: float
    wire_gauge: float  # cm
    horizontal_field: float

    @property
    def coil_constant(self) -> float:
        """G = 2.pi.n / (c.R) (gauss per statampere)."""
        return 2.0 * PI * self.n_turns / (CONST.C * self.radius)

    @maxwell_cite(
        720,
        part=4,
        theory_class="standard_math",
        description="Sensitivity d(theta)/dI at zero deflection = G/H",
    )
    def sensitivity(self) -> float:
        """Sensitivity d(theta)/dI at zero deflection (rad/statampere)."""
        return self.coil_constant / self.horizontal_field

    @maxwell_cite(
        720,
        part=4,
        theory_class="standard_math",
        description="Tangent-law current measurement",
    )
    def measure_current(self, theta_rad: float) -> float:
        """Measure current from deflection.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in statamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)
