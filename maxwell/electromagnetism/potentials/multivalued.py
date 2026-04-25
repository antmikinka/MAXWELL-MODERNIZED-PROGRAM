"""maxwell.electromagnetism.potentials.multivalued — Cyclic potential around wires (Art. 480).

Implements Maxwell's treatment of the magnetic potential around a current-carrying wire,
which is multivalued (cyclic) due to the non-conservative nature of the magnetic field
in the presence of currents.

Maxwell's CGS formulation (Art. 480):
    For a wire carrying current I, the magnetic scalar potential Omega is:
        Omega = -2I * phi  (where phi is the azimuthal angle)

    The potential increases by -4*pi*I for each complete circuit around the wire.
    This cyclic property reflects the fact that H is not derivable from a single-valued
    potential when currents are present.

where:
    I = current in abamperes (EMU)
    phi = azimuthal angle (radians)
    Omega = magnetic scalar potential (oersted*cm)

Category: A (maxwell_original) — Maxwell's theory of cyclic potentials.

References:
    Part IV, Art. 480: Cyclic nature of magnetic potential around currents.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class CyclicPotential:
    """
    Multivalued magnetic potential around a current-carrying wire.

    Art. 480: Maxwell showed that the magnetic field around a straight wire
    cannot be described by a single-valued scalar potential. Instead, the
    potential is cyclic (multivalued), increasing by -4*pi*I for each complete
    circuit around the wire.

    The magnetic field H = -grad(Omega) locally, but Omega is not single-valued:
        Omega(phi) = -2I * phi

    where phi is the azimuthal angle around the wire. After one complete
    circuit (phi -> phi + 2*pi), the potential changes by:
        Delta(Omega) = -4*pi*I

    Attributes:
        current: Current in the wire (abamperes).
        wire_position: Position of the wire (cm).
        wire_axis: Unit vector along wire direction.
    """

    current: float
    wire_position: np.ndarray = None
    wire_axis: np.ndarray = None

    def __post_init__(self):
        """Validate parameters and set defaults."""
        self.wire_position = np.asarray(self.wire_position, dtype=np.float64) if self.wire_position is not None else np.zeros(3)
        self.wire_axis = np.asarray(self.wire_axis, dtype=np.float64) if self.wire_axis is not None else np.array([0.0, 0.0, 1.0])

        # Normalize wire axis
        axis_norm = np.linalg.norm(self.wire_axis)
        if axis_norm > 0:
            self.wire_axis = self.wire_axis / axis_norm

    @maxwell_cite(
        480,
        part=4, chapter="Magnetic Potential",
        theory_class="maxwell_original",
        description="Calculate cyclic potential at position",
    )
    def potential_at(self, position: np.ndarray, branch: int = 0) -> float:
        """
        Calculate the multivalued magnetic potential at a position.

        Art. 480: The potential Omega at a point is given by:
            Omega = -2I * phi + branch_constant

        where phi is the azimuthal angle and branch is an integer indicating
        which "branch" of the multivalued function we are on.

        Args:
            position: Position vector (cm) where potential is evaluated.
            branch: Branch number (default 0). Each increment adds -4*pi*I.

        Returns:
            Magnetic scalar potential (oersted*cm).

        Reference:
            Part IV, Art. 480: Multivalued potential around currents.
        """
        position = np.asarray(position, dtype=np.float64)

        # Vector from wire to position (perpendicular to wire)
        r_vec = position - self.wire_position
        z_component = np.dot(r_vec, self.wire_axis)
        perp_vec = r_vec - z_component * self.wire_axis

        # Azimuthal angle (using x-axis as reference)
        # Choose a reference direction perpendicular to wire
        if np.abs(self.wire_axis[0]) < 0.9:
            ref_dir = np.cross(self.wire_axis, np.array([1.0, 0.0, 0.0]))
        else:
            ref_dir = np.cross(self.wire_axis, np.array([0.0, 1.0, 0.0]))
        ref_dir = ref_dir / np.linalg.norm(ref_dir)

        # Perpendicular radial direction
        r_perp = np.linalg.norm(perp_vec)
        if r_perp < 1e-15:
            return 0.0  # On the wire (singularity)

        perp_unit = perp_vec / r_perp

        # Calculate angle using dot and cross products
        cos_phi = np.dot(ref_dir, perp_unit)
        sin_phi = np.dot(np.cross(self.wire_axis, ref_dir), perp_unit)
        phi = np.arctan2(sin_phi, cos_phi)

        # Potential: Omega = -2I * phi + branch * (-4*pi*I)
        omega = -2.0 * self.current * phi + branch * (-4.0 * np.pi * self.current)

        return omega

    @maxwell_cite(
        480,
        part=4, chapter="Magnetic Potential",
        theory_class="maxwell_original",
        description="Calculate potential change around closed loop",
    )
    def cyclic_change(self, loops: int = 1) -> float:
        """
        Calculate the change in potential after circling the wire.

        Art. 480: After one complete circuit around the wire, the potential
        changes by a fixed amount:
            Delta(Omega) = -4*pi*I

        This is the cyclic constant that characterizes the multivalued nature
        of the potential.

        Args:
            loops: Number of complete circuits (default 1).

        Returns:
            Total change in potential (oersted*cm).

        Reference:
            Part IV, Art. 480: Cyclic change in potential.
        """
        return -4.0 * np.pi * self.current * loops

    @property
    def cyclic_constant(self) -> float:
        """
        The cyclic constant - potential change per circuit.

        Returns:
            Delta(Omega) = -4*pi*I (oersted*cm).
        """
        return -4.0 * np.pi * self.current


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Calculate cyclic potential around straight wire: Omega = -2I*phi",
)
def calc_cyclic_potential(
    current: float,
    azimuthal_angle: float,
    branch: int = 0,
) -> float:
    """
    Calculate the multivalued magnetic potential around a straight wire.

    Art. 480: For an infinite straight wire carrying current I, the magnetic
    scalar potential at azimuthal angle phi is:

        Omega = -2I * phi - 4*pi*I * branch

    where:
        I = current in abamperes
        phi = azimuthal angle (radians) from reference direction
        branch = integer indicating which branch of the multivalued function

    The potential is multivalued because H is not conservative when currents
    are present. Each complete circuit around the wire changes the potential
    by -4*pi*I.

    Args:
        current: Current in the wire (abamperes).
        azimuthal_angle: Azimuthal angle phi (radians).
        branch: Branch number (default 0).

    Returns:
        Magnetic scalar potential (oersted*cm).

    Reference:
        Part IV, Art. 480: Cyclic potential formulation.

    Example:
        >>> # Potential at 90 degrees from reference
        >>> Omega = calc_cyclic_potential(1.0, np.pi/2)
        >>> print(f"Omega = {Omega:.2f} oersted*cm")  # Omega = -3.14 oersted*cm
    """
    return -2.0 * current * azimuthal_angle - 4.0 * np.pi * current * branch


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Calculate potential difference between two points",
)
def calc_potential_difference(
    current: float,
    angle1: float,
    angle2: float,
) -> float:
    """
    Calculate the potential difference between two azimuthal positions.

    Art. 480: The potential difference between two points at angles phi1 and phi2
    is independent of the branch:

        Delta(Omega) = Omega(phi2) - Omega(phi1) = -2I * (phi2 - phi1)

    This is the physically measurable quantity (related to work done moving
    a magnetic pole).

    Args:
        current: Current in the wire (abamperes).
        angle1: Initial azimuthal angle (radians).
        angle2: Final azimuthal angle (radians).

    Returns:
        Potential difference (oersted*cm).

    Reference:
        Part IV, Art. 480: Potential differences.
    """
    return -2.0 * current * (angle2 - angle1)


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Verify cyclic nature of magnetic potential",
)
def verify_cyclic_potential(
    current: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the cyclic property of the magnetic potential.

    Art. 480: This function verifies that:
    1. The potential changes by -4*pi*I after one complete circuit
    2. The field H = -grad(Omega) gives the correct Oersted field

    Args:
        current: Test current (abamperes, default 1.0).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with verification results:
        - cyclic_change: Actual change after one circuit
        - expected_change: Expected -4*pi*I
        - field_verified: True if H = -grad(Omega) matches Oersted field
        - verified: True if all checks pass

    Reference:
        Part IV, Art. 480: Cyclic potential verification.
    """
    # Expected cyclic change
    expected_change = -4.0 * np.pi * current

    # Calculate potential at phi = 0 and phi = 2*pi
    omega_0 = calc_cyclic_potential(current, 0.0, branch=0)
    omega_2pi = calc_cyclic_potential(current, 2.0 * np.pi, branch=0)

    # Should differ by cyclic constant
    actual_change = omega_2pi - omega_0

    # Verify field from potential gradient
    # H_phi = -dOmega/d(phi) / r = 2I/r (Oersted field)
    delta_phi = 1e-6
    omega_plus = calc_cyclic_potential(current, delta_phi)
    dOmega_dphi = (omega_plus - omega_0) / delta_phi

    # At r = 1, H should be 2I
    H_from_potential = -dOmega_dphi  # H = -grad(Omega), for r=1
    H_expected = 2.0 * current

    field_error = abs(H_from_potential - H_expected) / H_expected if H_expected != 0 else 0

    verified = (
        abs(actual_change - expected_change) < tolerance * abs(expected_change) and
        field_error < tolerance
    )

    return {
        "cyclic_change": actual_change,
        "expected_change": expected_change,
        "field_from_potential": H_from_potential,
        "expected_field": H_expected,
        "field_error": field_error,
        "field_verified": field_error < tolerance,
        "verified": verified,
    }


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Calculate work done moving magnetic pole around wire",
)
def calc_work_on_magnetic_pole(
    pole_strength: float,
    current: float,
    loops: float,
) -> float:
    """
    Calculate work done moving a magnetic pole around a current-carrying wire.

    Art. 480: When a magnetic pole of strength m is moved once around a wire
    carrying current I, the work done is:

        W = -m * Delta(Omega) = m * 4*pi*I

    This work is independent of the path (as long as it encircles the wire)
    and is a fundamental result linking magnetic and electric quantities.

    In CGS-EMU:
        m = pole strength (EMU)
        I = current (abamperes)
        W = work (ergs)

    Args:
        pole_strength: Magnetic pole strength m (EMU).
        current: Current in wire (abamperes).
        loops: Number of complete circuits around wire.

    Returns:
        Work done (ergs). Positive if pole moves with field.

    Reference:
        Part IV, Art. 480: Work on magnetic pole in cyclic field.

    Example:
        >>> # Unit N pole moved once around 1 abampere wire
        >>> W = calc_work_on_magnetic_pole(1.0, 1.0, 1)
        >>> print(f"W = {W:.2f} ergs")  # W = 12.57 ergs
    """
    # Work = -m * Delta(Omega) = -m * (-4*pi*I) = 4*pi*m*I
    return 4.0 * np.pi * pole_strength * current * loops


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Determine branch number from position history",
)
def determine_branch(
    current: float,
    measured_potential: float,
    position_angle: float,
) -> int:
    """
    Determine the branch number from a measured potential.

    Art. 480: Given a measured potential and position, we can determine which
    branch of the multivalued function we are on:

        branch = round((Omega_measured + 2I*phi) / (-4*pi*I))

    This is useful for tracking the history of a magnetic pole that has
    been moved around the wire multiple times.

    Args:
        current: Current in wire (abamperes).
        measured_potential: Measured potential (oersted*cm).
        position_angle: Current azimuthal angle (radians).

    Returns:
        Branch number (integer).

    Reference:
        Part IV, Art. 480: Branch determination.
    """
    if current == 0:
        return 0

    base_potential = -2.0 * current * position_angle
    branch = round((measured_potential - base_potential) / (-4.0 * np.pi * current))

    return int(branch)


@maxwell_cite(
    480,
    part=4, chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Complete cyclic potential analysis",
)
def analyze_cyclic_potential(
    current: float,
    positions: list[np.ndarray] = None,
    wire_position: np.ndarray = None,
    wire_axis: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform complete analysis of cyclic potential around a wire.

    Art. 480: Comprehensive analysis including:
    1. Potential at various positions
    2. Potential differences
    3. Cyclic constant verification
    4. Field from potential gradient

    Args:
        current: Current in wire (abamperes).
        positions: Optional list of position vectors to evaluate.
        wire_position: Position of wire (default: origin).
        wire_axis: Direction of wire (default: z-axis).

    Returns:
        Dictionary with analysis results:
        - cyclic_constant: -4*pi*I
        - potentials: Potential at each position (if provided)
        - field_magnitude_at_1cm: H at r=1cm (= 2I)
        - work_per_loop: Work to move unit pole once around

    Reference:
        Part IV, Art. 480: Complete cyclic potential analysis.
    """
    wire_position = np.asarray(wire_position, dtype=np.float64) if wire_position is not None else np.zeros(3)
    wire_axis = np.asarray(wire_axis, dtype=np.float64) if wire_axis is not None else np.array([0.0, 0.0, 1.0])

    result = {
        "current": current,
        "cyclic_constant": -4.0 * np.pi * current,
        "field_magnitude_at_1cm": 2.0 * current,
        "work_per_loop_unit_pole": 4.0 * np.pi * current,
    }

    if positions is not None:
        cp = CyclicPotential(current=current, wire_position=wire_position, wire_axis=wire_axis)
        potentials = [cp.potential_at(np.asarray(p, dtype=np.float64)) for p in positions]
        result["potentials"] = potentials

    return result
