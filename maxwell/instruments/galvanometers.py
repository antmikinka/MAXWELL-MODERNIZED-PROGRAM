"""maxwell.instruments.galvanometers — Standard galvanometers (Arts. 707-720).

Standard and sensitive galvanometers, tangent/sine principles,
Helmholtz coil, multi-coil designs, and sensitivity optimization.
Every class and function is cited to Maxwell's original articles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


# ---------------------------------------------------------------------------
# Art. 707-708: Standard galvanometer construction
# ---------------------------------------------------------------------------


@dataclass
class StandardGalvanometer:
    """Standard galvanometer coil (Arts. 707-708).

    A precisely wound coil of known geometry used as a reference
    instrument for measuring current by the deflection of a magnet.

    Attributes:
        n_turns: Number of turns in the coil.
        mean_radius: Mean radius of the coil (cm).
        wire_radius: Radius of the wire itself (cm).
        coil_depth: Axial depth of the winding (cm).
        coil_constant: Galvanometer constant G (computed).
    """

    n_turns: int
    mean_radius: float  # cm
    wire_radius: float  # cm
    coil_depth: float  # cm
    coil_constant: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        """Compute the galvanometer constant after initialization."""
        self.coil_constant = self._compute_coil_constant()

    @maxwell_cite(707, part=4, theory_class="standard_math")
    def _compute_coil_constant(self) -> float:
        """Compute G = 2*pi*n / R for a single-layer coil."""
        return 2.0 * PI * self.n_turns / self.mean_radius


@maxwell_cite(708, part=4, theory_class="standard_math")
def design_standard_coil(
    target_constant: float,
    wire_radius: float,
    max_radius: float,
) -> dict[str, float]:
    """Design a standard coil to achieve a target galvanometer constant.

    Args:
        target_constant: Desired G value.
        wire_radius: Radius of available wire (cm).
        max_radius: Maximum allowable coil radius (cm).

    Returns:
        Dictionary with n_turns, mean_radius, coil_depth.
    """
    # Start with largest possible radius for best uniformity
    mean_radius = max_radius * 0.9
    n_turns = int(np.ceil(target_constant * mean_radius / (2.0 * PI)))
    coil_depth = 2.0 * wire_radius * np.sqrt(n_turns)

    return {
        "n_turns": n_turns,
        "mean_radius": mean_radius,
        "coil_depth": coil_depth,
    }


# ---------------------------------------------------------------------------
# Art. 709: Mathematical theory of the galvanometer
# ---------------------------------------------------------------------------


@maxwell_cite(709, part=4, theory_class="standard_math")
def calc_galvanometer_response(
    current: float,
    coil_constant: float,
    horizontal_field: float,
    magnetic_moment: float,
    torsion_constant: float = 0.0,
) -> float:
    """Calculate needle deflection angle for a given current.

    From Art. 709, the equilibrium condition balances the torque
    from the coil field against the terrestrial horizontal field:

        tan(theta) = (G * I) / H

    Args:
        current: Current through coil (abamperes).
        coil_constant: G constant of the coil.
        horizontal_field: Terrestrial horizontal field H (oersted).
        magnetic_moment: Magnetic moment of the needle.
        torsion_constant: Optional torsion fiber constant.

    Returns:
        Deflection angle theta in radians.
    """
    coil_field = coil_constant * current
    restoring = horizontal_field + torsion_constant
    return np.arctan(coil_field / restoring)


@maxwell_cite(709, part=4, theory_class="standard_math")
def calc_field_at_center(
    current: float,
    n_turns: int,
    radius: float,
) -> float:
    """Calculate magnetic field at center of circular coil.

    H = 2*pi*n*I / R  (CGS, at center of circular coil)

    Args:
        current: Current in abamperes.
        n_turns: Number of turns.
        radius: Coil radius in cm.

    Returns:
        Field H in oersted.
    """
    return 2.0 * PI * n_turns * current / radius


# ---------------------------------------------------------------------------
# Art. 710: Tangent and sine galvanometer principles
# ---------------------------------------------------------------------------


@dataclass
class TangentGalvanometer:
    """Tangent galvanometer (Art. 710).

    Current is proportional to the tangent of the deflection angle:
        I = (H / G) * tan(theta)

    Attributes:
        coil_constant: G constant of the coil.
        horizontal_field: Terrestrial horizontal field H.
    """

    coil_constant: float
    horizontal_field: float

    @maxwell_cite(710, part=4, theory_class="standard_math")
    def current_from_deflection(self, theta_rad: float) -> float:
        """Calculate current from deflection angle.

        I = (H/G) * tan(theta)

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in abamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)

    @maxwell_cite(710, part=4, theory_class="standard_math")
    def deflection_from_current(self, current: float) -> float:
        """Calculate deflection angle from current.

        theta = arctan(G*I / H)

        Args:
            current: Current in abamperes.

        Returns:
            Deflection angle in radians.
        """
        return np.arctan(self.coil_constant * current / self.horizontal_field)


@dataclass
class SineGalvanometer:
    """Sine galvanometer (Art. 710).

    The coil is rotated until the needle is at zero; current is
    proportional to the sine of the rotation angle:
        I = (H / G) * sin(alpha)

    Attributes:
        coil_constant: G constant of the coil.
        horizontal_field: Terrestrial horizontal field H.
    """

    coil_constant: float
    horizontal_field: float

    @maxwell_cite(710, part=4, theory_class="standard_math")
    def current_from_rotation(self, alpha_rad: float) -> float:
        """Calculate current from coil rotation angle.

        I = (H/G) * sin(alpha)

        Args:
            alpha_rad: Rotation angle in radians.

        Returns:
            Current in abamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.sin(alpha_rad)


# ---------------------------------------------------------------------------
# Art. 711: Single-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class SingleCoilGalvanometer:
    """Galvanometer with a single circular coil (Art. 711).

    Simplest form: one coil with a suspended needle at the center.
    """

    n_turns: int
    radius: float
    horizontal_field: float

    @property
    def coil_constant(self) -> float:
        """G = 2*pi*n / R."""
        return 2.0 * PI * self.n_turns / self.radius

    @maxwell_cite(711, part=4, theory_class="standard_math")
    def measure_current(self, theta_rad: float) -> float:
        """Measure current from tangent-law deflection.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in abamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 712: Gaugain's eccentric suspension
# ---------------------------------------------------------------------------


@maxwell_cite(712, part=4, theory_class="standard_math")
def apply_gaugain_suspension(
    radius: float,
    needle_offset: float,
    n_turns: int,
    current: float,
) -> float:
    """Calculate field with Gaugain's eccentric needle suspension.

    Gaugain placed the needle so its center of oscillation is
    offset from the coil center by a specific distance to
    improve the accuracy of the tangent law.

    Args:
        radius: Coil radius (cm).
        needle_offset: Distance of needle from coil center (cm).
        n_turns: Number of turns.
        current: Current (abamperes).

    Returns:
        Field at the offset position (oersted).
    """
    # For offset z along axis: H = 2*pi*n*R^2*I / (R^2 + z^2)^(3/2)
    R2 = radius**2
    z2 = needle_offset**2
    return 2.0 * PI * n_turns * current * R2 / (R2 + z2) ** 1.5


# ---------------------------------------------------------------------------
# Art. 714: Four-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class FourCoilGalvanometer:
    """Galvanometer with four coils (Art. 714).

    Four coils arranged to produce a more uniform field at
    the center, eliminating higher-order correction terms.
    """

    inner_radius: float
    outer_radius: float
    n_turns_inner: int
    n_turns_outer: int
    horizontal_field: float

    @maxwell_cite(714, part=4, theory_class="standard_math")
    def combined_coil_constant(self) -> float:
        """Calculate combined G constant for four-coil arrangement.

        G = G_inner + G_outer with appropriate signs for uniformity.
        """
        G_inner = 2.0 * PI * self.n_turns_inner / self.inner_radius
        G_outer = 2.0 * PI * self.n_turns_outer / self.outer_radius
        return G_inner + G_outer

    @maxwell_cite(714, part=4, theory_class="standard_math")
    def measure_current(self, theta_rad: float) -> float:
        """Measure current using tangent law with combined constant.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in abamperes.
        """
        G = self.combined_coil_constant()
        return (self.horizontal_field / G) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 715: Three-coil galvanometer
# ---------------------------------------------------------------------------


@dataclass
class ThreeCoilGalvanometer:
    """Galvanometer with three coils (Art. 715).

    Three-coil arrangement for intermediate uniformity between
    single-coil and four-coil designs.
    """

    radii: tuple[float, float, float]
    n_turns: tuple[int, int, int]
    horizontal_field: float

    @maxwell_cite(715, part=4, theory_class="standard_math")
    def combined_coil_constant(self) -> float:
        """Calculate combined G constant for three-coil arrangement."""
        return sum(
            2.0 * PI * n / r for n, r in zip(self.n_turns, self.radii)
        )

    @maxwell_cite(715, part=4, theory_class="standard_math")
    def measure_current(self, theta_rad: float) -> float:
        """Measure current using tangent law.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in abamperes.
        """
        G = self.combined_coil_constant()
        return (self.horizontal_field / G) * np.tan(theta_rad)


# ---------------------------------------------------------------------------
# Art. 717-718: Sensitivity optimization
# ---------------------------------------------------------------------------


@maxwell_cite(717, part=4, theory_class="standard_math")
def design_sensitive_galvanometer(
    wire_length: float,
    wire_resistance: float,
    target_resistance: float,
) -> dict[str, float]:
    """Design a galvanometer for maximum sensitivity.

    For greatest sensitivity, the coil resistance should equal
    the external circuit resistance (Art. 718).

    Args:
        wire_length: Total available wire length (cm).
        wire_resistance: Resistance per unit length.
        target_resistance: External circuit resistance to match.

    Returns:
        Design parameters dict.
    """
    # Optimal: coil resistance = external resistance
    optimal_coil_r = target_resistance
    n_turns = int(optimal_coil_r / wire_resistance)

    # For fixed wire length L = 2*pi*R*n, maximize R*n^2
    # which means use as large a radius as practical
    mean_radius = wire_length / (2.0 * PI * n_turns) if n_turns > 0 else 1.0

    return {
        "n_turns": n_turns,
        "mean_radius": mean_radius,
        "coil_resistance": optimal_coil_r,
    }


@maxwell_cite(720, part=4, theory_class="standard_math")
def calc_uniform_wire_sensitivity(
    n_turns: int,
    radius: float,
    horizontal_field: float,
) -> float:
    """Calculate sensitivity of uniform-wire galvanometer.

    Sensitivity = d(theta)/dI at zero deflection = G/H.

    Args:
        n_turns: Number of turns.
        radius: Coil radius (cm).
        horizontal_field: Terrestrial horizontal field.

    Returns:
        Sensitivity in radians per abampere.
    """
    G = 2.0 * PI * n_turns / radius
    return G / horizontal_field


@dataclass
class UniformWireGalvanometer:
    """Galvanometer with uniform thickness wire (Art. 720).

    The simplest and most common construction, using wire of
    constant gauge throughout the winding.
    """

    n_turns: int
    radius: float
    wire_gauge: float  # cm
    horizontal_field: float

    @property
    def coil_constant(self) -> float:
        return 2.0 * PI * self.n_turns / self.radius

    @maxwell_cite(720, part=4, theory_class="standard_math")
    def sensitivity(self) -> float:
        """Sensitivity d(theta)/dI at zero deflection."""
        return self.coil_constant / self.horizontal_field

    @maxwell_cite(720, part=4, theory_class="standard_math")
    def measure_current(self, theta_rad: float) -> float:
        """Measure current from deflection.

        Args:
            theta_rad: Deflection angle in radians.

        Returns:
            Current in abamperes.
        """
        return (self.horizontal_field / self.coil_constant) * np.tan(theta_rad)
