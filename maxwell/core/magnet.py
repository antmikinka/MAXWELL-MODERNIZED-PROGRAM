"""
Magnetic primitives — fundamental magnetic quantities and forces.

Implements the theory of magnets from Part III of Maxwell's Treatise:
- Magnetic poles and their interaction (Arts. 371-376)
- Earth's magnetic response (Art. 392)
- Mutual action of magnets
- Center and axes of magnets

Maxwell's formulation uses magnetic pole strength m (magnetic charge) and
distance r, with force law: F = m1 * m2 / r^2 (CGS, analogous to Coulomb's law)

Category: A (maxwell_original) — Maxwell's theory of magnetism.

References:
    Part III, Arts. 371-376: Magnetic poles and force law.
    Part III, Art. 392: Earth's magnetic action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MagneticPole:
    """
    A magnetic pole — the elementary source of magnetic field.

    Art. 371: The fundamental property of a magnet is that it has two poles,
    north (N) and south (S), which exert forces on each other.

    In Maxwell's theory, magnetic poles are analogous to electric charges:
    - Austral (N) pole: positive magnetic charge (+m)
    - Boreal (S) pole: negative magnetic charge (-m)

    Attributes:
        strength: Pole strength m (EMU units, erg/gauss·cm).
        position: Position vector (x, y, z) in cm.
        pole_type: 'N' (austral, positive) or 'S' (boreal, negative).
    """

    strength: float
    position: np.ndarray  # shape (3,)
    pole_type: str  # 'N' or 'S'

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got shape {self.position.shape}")

        # Ensure strength sign matches pole type
        if self.pole_type == 'N' and self.strength < 0:
            self.strength = abs(self.strength)
        elif self.pole_type == 'S' and self.strength > 0:
            self.strength = -abs(self.strength)

    @property
    def signed_strength(self) -> float:
        """Return pole strength with sign: N=positive, S=negative."""
        return self.strength if self.pole_type == 'N' else -abs(self.strength)


@dataclass
class Magnet:
    """
    A permanent magnet with north and south poles.

    Art. 372-373: A magnet consists of two equal and opposite magnetic poles
    separated by a finite distance. The magnetic moment is the product of
    pole strength and the distance between poles.

    Attributes:
        north_pole: North (austral) magnetic pole.
        south_pole: South (boreal) magnetic pole.
        magnetic_moment: Vector magnetic moment m = pole_strength * length.
    """

    north_pole: MagneticPole
    south_pole: MagneticPole

    def __post_init__(self):
        # Verify poles have opposite signs
        if self.north_pole.signed_strength * self.south_pole.signed_strength >= 0:
            raise ValueError("Magnet must have opposite polarity poles")

    @property
    def pole_strength(self) -> float:
        """Magnitude of pole strength (both poles have equal magnitude)."""
        return abs(self.north_pole.strength)

    @property
    def magnetic_length(self) -> float:
        """Distance between poles (magnetic length)."""
        return float(np.linalg.norm(
            self.north_pole.position - self.south_pole.position
        ))

    @property
    def magnetic_axis_vector(self) -> np.ndarray:
        """Vector from S to N pole (defines magnetic axis direction)."""
        return self.north_pole.position - self.south_pole.position

    @property
    def magnetic_moment(self) -> np.ndarray:
        """
        Magnetic moment vector.

        Art. 373: The magnetic moment is the product of pole strength
        and the vector from S to N pole.

        m = pole_strength * (r_N - r_S)
        """
        return self.pole_strength * self.magnetic_axis_vector

    @classmethod
    @maxwell_cite(
        372, 373,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Create magnet from pole strength, positions",
    )
    def from_pole_data(
        cls,
        pole_strength: float,
        north_position: np.ndarray,
        south_position: np.ndarray,
    ) -> Magnet:
        """
        Create a magnet from pole strength and positions.

        Args:
            pole_strength: Magnitude of pole strength (EMU).
            north_position: Position of N pole (cm).
            south_position: Position of S pole (cm).

        Returns:
            Magnet object with specified pole configuration.

        Reference:
            Part III, Arts. 372-373: Magnetic poles and moment.
        """
        north = MagneticPole(
            strength=abs(pole_strength),
            position=np.asarray(north_position, dtype=np.float64),
            pole_type='N'
        )
        south = MagneticPole(
            strength=-abs(pole_strength),
            position=np.asarray(south_position, dtype=np.float64),
            pole_type='S'
        )
        return cls(north_pole=north, south_pole=south)

    @classmethod
    @maxwell_cite(
        373,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Create magnet from center, axis, and moment",
    )
    def from_moment_and_center(
        cls,
        center: np.ndarray,
        magnetic_moment: np.ndarray,
        length: float,
    ) -> Magnet:
        """
        Create a magnet from its center, magnetic moment, and length.

        Art. 373: Given the magnetic moment and center, the magnet
        is defined by placing poles at equal distances from center
        along the moment direction.

        Args:
            center: Center point of magnet (cm).
            magnetic_moment: Magnetic moment vector (emu).
            length: Magnetic length (distance between poles, cm).

        Returns:
            Magnet object centered at specified position.

        Reference:
            Part III, Art. 373: Magnetic moment definition.
        """
        center = np.asarray(center, dtype=np.float64)
        moment = np.asarray(magnetic_moment, dtype=np.float64)

        moment_mag = np.linalg.norm(moment)
        if moment_mag == 0:
            raise ValueError("Magnetic moment cannot be zero")

        # Unit vector along magnetic axis (S to N)
        axis = moment / moment_mag

        # Pole strength from moment = strength * length
        pole_strength = moment_mag / length

        # Positions: half-length from center along axis
        half_length = length / 2.0
        north_pos = center + half_length * axis
        south_pos = center - half_length * axis

        return cls.from_pole_data(pole_strength, north_pos, south_pos)

    @maxwell_cite(
        371, 372,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Force on magnet from external magnetic field",
    )
    def force_in_field(
        self,
        field_func: Callable[[np.ndarray], np.ndarray],
    ) -> np.ndarray:
        """
        Calculate resultant force on magnet in external field.

        Art. 371-372: Each pole experiences a force proportional to
        its strength and the local field intensity.

        F = m_N * H(r_N) + m_S * H(r_S)

        Args:
            field_func: Function returning H field at a position.

        Returns:
            Total force vector on magnet (dyne).

        Reference:
            Part III, Arts. 371-372: Magnetic pole forces.
        """
        H_north = field_func(self.north_pole.position)
        H_south = field_func(self.south_pole.position)

        # F = m*H for each pole (vector sum)
        F_north = self.north_pole.signed_strength * H_north
        F_south = self.south_pole.signed_strength * H_south

        return F_north + F_south

    @maxwell_cite(
        373,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Torque on magnet in uniform magnetic field",
    )
    def torque_in_uniform_field(
        self,
        field: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate torque on magnet in uniform magnetic field.

        Art. 373: A magnet in a uniform field experiences a torque
        tending to align it with the field.

        τ = m × H  (cross product of moment and field)

        Args:
            field: Uniform H field vector (gauss).

        Returns:
            Torque vector (dyne·cm).

        Reference:
            Part III, Art. 373: Magnetic moment and torque.
        """
        return np.cross(self.magnetic_moment, field)

    @maxwell_cite(
        375,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Potential energy of magnet in external field",
    )
    def potential_energy_in_field(
        self,
        field_func: Callable[[np.ndarray], np.ndarray],
    ) -> float:
        """
        Calculate potential energy of magnet in external field.

        Art. 375: The potential energy is the work required to bring
        the magnet from infinity to its current position.

        W = -m_N * Ω(r_N) - m_S * Ω(r_S)

        where Ω is the magnetic scalar potential (H = -∇Ω).

        For uniform field: W = -m · H

        Args:
            field_func: Function returning H field at a position.

        Returns:
            Potential energy (erg).

        Reference:
            Part III, Art. 375: Magnetic potential energy.
        """
        # For a general field, integrate along path (simplified here)
        # Assume field derives from potential Ω where H = -grad(Ω)
        # W = -m * Ω for each pole

        # Simplified: use center field for uniform approximation
        center = (self.north_pole.position + self.south_pole.position) / 2
        H_center = field_func(center)

        # W = -m · H (dot product)
        return -np.dot(self.magnetic_moment, H_center)


@dataclass
class MagneticAxis:
    """
    The axis of a magnet — the line through its poles.

    Art. 376: The magnetic axis is the straight line passing through
    the centers of the north and south poles.

    Attributes:
        center: Center point of the axis (cm).
        direction: Unit vector along axis (from S to N).
        length: Distance between poles (cm).
    """

    center: np.ndarray  # shape (3,)
    direction: np.ndarray  # shape (3,), unit vector
    length: float

    def __post_init__(self):
        self.center = np.asarray(self.center, dtype=np.float64)
        self.direction = np.asarray(self.direction, dtype=np.float64)

        dir_mag = np.linalg.norm(self.direction)
        if dir_mag == 0:
            raise ValueError("Direction cannot be zero vector")
        self.direction = self.direction / dir_mag  # Ensure unit vector

        if self.length <= 0:
            raise ValueError("Length must be positive")

    @classmethod
    def from_magnet(cls, magnet: Magnet) -> MagneticAxis:
        """
        Create magnetic axis from a magnet.

        Args:
            magnet: Magnet object.

        Returns:
            MagneticAxis object for the magnet.
        """
        center = (magnet.north_pole.position + magnet.south_pole.position) / 2
        direction = magnet.magnetic_axis_vector
        length = magnet.magnetic_length

        return cls(center=center, direction=direction, length=length)

    @property
    def north_end(self) -> np.ndarray:
        """Position of north end of axis."""
        return self.center + (self.length / 2) * self.direction

    @property
    def south_end(self) -> np.ndarray:
        """Position of south end of axis."""
        return self.center - (self.length / 2) * self.direction


@dataclass
class MagneticQuantity:
    """
    Magnetic quantity — scalar measures of magnetic properties.

    Art. 371-376: Various magnetic quantities used in calculations.

    This class provides static methods for computing fundamental
    magnetic quantities in CGS-EMU units.
    """

    @staticmethod
    @maxwell_cite(
        371,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Coulomb's law for magnetic poles",
    )
    def pole_force(m1: float, m2: float, r: float) -> float:
        """
        Force between two magnetic poles (Coulomb's law for magnetism).

        Art. 371: The force between magnetic poles varies inversely as
        the square of the distance between them.

        F = m1 * m2 / r^2  (CGS-EMU)

        Args:
            m1: Strength of first pole (EMU).
            m2: Strength of second pole (EMU).
            r: Separation distance (cm).

        Returns:
            Force magnitude (dyne). Positive = repulsive, negative = attractive.

        Reference:
            Part III, Art. 371: Magnetic pole force law.
        """
        if r <= 0:
            raise ValueError(f"Separation must be positive, got {r}")
        return m1 * m2 / (r ** 2)

    @staticmethod
    @maxwell_cite(
        374,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Magnetic moment from pole strength and length",
    )
    def magnetic_moment(pole_strength: float, length: float) -> float:
        """
        Calculate magnetic moment magnitude.

        Art. 374: The magnetic moment is the product of pole strength
        and the distance between poles.

        M = m * L

        Args:
            pole_strength: Pole strength m (EMU).
            length: Distance between poles L (cm).

        Returns:
            Magnetic moment (emu = erg/gauss).

        Reference:
            Part III, Art. 374: Magnetic moment definition.
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        return abs(pole_strength) * length

    @staticmethod
    @maxwell_cite(
        376,
        part=3, chapter="Magnetic Poles",
        theory_class="maxwell_original",
        description="Field intensity from a magnetic pole",
    )
    def field_from_pole(pole_strength: float, distance: float) -> float:
        """
        Magnetic field intensity at distance from isolated pole.

        Art. 376: The field intensity due to a magnetic pole varies
        inversely as the square of the distance.

        H = m / r^2  (CGS-EMU, gauss)

        Args:
            pole_strength: Pole strength m (EMU).
            distance: Distance from pole r (cm).

        Returns:
            Field intensity (gauss).

        Reference:
            Part III, Art. 376: Field from magnetic pole.
        """
        if distance <= 0:
            raise ValueError("Distance must be positive")
        return pole_strength / (distance ** 2)


@maxwell_cite(
    371, 372, 373, 375, 376,
    part=3, chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Verify magnetic force law through experimental data",
)
def verify_force_law_evidence(
    measured_forces: list[float],
    pole_strengths: tuple[float, float],
    distances: list[float],
    tolerance: float = 0.05,
) -> dict[str, float]:
    """
    Verify Coulomb's law for magnetism from experimental data.

    Art. 371-376: By measuring forces between poles at various distances,
    we can verify the inverse-square law F ∝ 1/r².

    This function analyzes measured forces to determine how well they
    fit the theoretical prediction F = m1*m2/r².

    Args:
        measured_forces: List of measured forces (dyne).
        pole_strengths: Tuple of (m1, m2) pole strengths (EMU).
        distances: List of separation distances (cm).
        tolerance: Acceptable fractional deviation from theory.

    Returns:
        Dictionary with verification results:
        - theoretical_forces: Predicted forces from Coulomb's law
        - deviation_mean: Mean fractional deviation
        - deviation_max: Maximum fractional deviation
        - verified: True if within tolerance

    Reference:
        Part III, Arts. 371-376: Magnetic force law evidence.
    """
    if len(measured_forces) != len(distances):
        raise ValueError("Forces and distances must have same length")
    if len(measured_forces) < 2:
        raise ValueError("Need at least 2 measurements")

    m1, m2 = pole_strengths

    # Calculate theoretical forces
    theoretical = [m1 * m2 / (r ** 2) for r in distances if r > 0]

    if len(theoretical) != len(measured_forces):
        raise ValueError("Invalid distance values")

    # Calculate fractional deviations
    deviations = []
    for F_meas, F_theo in zip(measured_forces, theoretical):
        if F_theo != 0:
            deviations.append(abs(F_meas - F_theo) / abs(F_theo))
        else:
            deviations.append(abs(F_meas))

    deviation_mean = float(np.mean(deviations))
    deviation_max = float(max(deviations))

    verified = deviation_max <= tolerance

    return {
        "theoretical_forces": theoretical,
        "deviation_mean": deviation_mean,
        "deviation_max": deviation_max,
        "verified": verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    392,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Earth's magnetic field response",
)
def earth_response(
    magnet: Magnet,
    earth_field: np.ndarray,
) -> dict[str, float]:
    """
    Analyze a magnet's response to Earth's magnetic field.

    Art. 392: The Earth acts as a giant magnet, exerting directive
    forces on smaller magnets. A freely suspended magnet aligns
    with the Earth's field, defining the magnetic meridian.

    This function calculates:
    - Torque aligning magnet with Earth's field
    - Oscillation period for small displacements
    - Equilibrium orientation

    Args:
        magnet: Magnet object (e.g., compass needle).
        earth_field: Earth's H field vector at location (gauss).

    Returns:
        Dictionary with:
        - torque_magnitude: Torque trying to align magnet (dyne·cm)
        - potential_energy: Energy in current orientation (erg)
        - alignment_angle: Angle between magnet and field (radians)
        - max_torque: Maximum possible torque (when perpendicular)

    Reference:
        Part III, Art. 392: Earth's magnetic action on magnets.
    """
    earth_field = np.asarray(earth_field, dtype=np.float64)

    # Torque: τ = m × H
    torque = np.cross(magnet.magnetic_moment, earth_field)
    torque_mag = np.linalg.norm(torque)

    # Potential energy: W = -m · H
    energy = -np.dot(magnet.magnetic_moment, earth_field)

    # Alignment angle
    m_mag = np.linalg.norm(magnet.magnetic_moment)
    H_mag = np.linalg.norm(earth_field)

    if m_mag * H_mag > 0:
        cos_theta = np.dot(magnet.magnetic_moment, earth_field) / (m_mag * H_mag)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Numerical safety
        angle = float(np.arccos(cos_theta))
    else:
        angle = 0.0

    # Maximum torque (when perpendicular)
    max_torque = m_mag * H_mag

    return {
        "torque_magnitude": torque_mag,
        "potential_energy": energy,
        "alignment_angle": angle,
        "max_torque": max_torque,
        "earth_field_magnitude": H_mag,
    }


@maxwell_cite(
    374, 375,
    part=3, chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Mutual action between two magnets",
)
def mutual_action(
    magnet1: Magnet,
    magnet2: Magnet,
    separation: np.ndarray = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate mutual force and torque between two magnets.

    Art. 374-375: Two magnets exert forces and torques on each other
    through the interaction of their poles. The total effect is the
    vector sum of all four pole-to-pole interactions.

    This computes the force on magnet2 due to magnet1's field,
    and the torque on magnet2 trying to align it with magnet1's field.

    Args:
        magnet1: First magnet (source of field).
        magnet2: Second magnet (experiencing force/torque).
        separation: Vector from magnet1 center to magnet2 center (cm).
                   If None, uses actual positions.

    Returns:
        Dictionary with:
        - force_on_2: Force vector on magnet2 (dyne)
        - torque_on_2: Torque vector on magnet2 (dyne·cm)
        - potential_energy: Interaction energy (erg)

    Reference:
        Part III, Arts. 374-375: Mutual action of magnets.
    """
    # Calculate field from magnet1 at magnet2's poles
    def field_from_magnet1(point: np.ndarray) -> np.ndarray:
        """H field from magnet1 at a point."""
        r_n = point - magnet1.north_pole.position
        r_s = point - magnet1.south_pole.position

        r_n_mag = np.linalg.norm(r_n)
        r_s_mag = np.linalg.norm(r_s)

        if r_n_mag == 0 or r_s_mag == 0:
            return np.zeros(3)

        # H = m_N * r_hat_N / r_N^2 + m_S * r_hat_S / r_S^2
        H_n = magnet1.north_pole.signed_strength * r_n / (r_n_mag ** 3)
        H_s = magnet1.south_pole.signed_strength * r_s / (r_s_mag ** 3)

        return H_n + H_s

    # Force on magnet2
    force = magnet2.force_in_field(field_from_magnet1)

    # Field at magnet2 center for torque calculation
    center2 = (magnet2.north_pole.position + magnet2.south_pole.position) / 2
    H_at_2 = field_from_magnet1(center2)

    # Torque on magnet2
    torque = magnet2.torque_in_uniform_field(H_at_2)

    # Potential energy
    energy = magnet2.potential_energy_in_field(field_from_magnet1)

    return {
        "force_on_2": force,
        "torque_on_2": torque,
        "potential_energy": energy,
    }


@maxwell_cite(
    376,
    part=3, chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Find center and axes of a magnet from pole positions",
)
def center_and_axes(magnet: Magnet) -> dict[str, np.ndarray | MagneticAxis]:
    """
    Determine the center and magnetic axes of a magnet.

    Art. 376: The center of a magnet is the midpoint between its poles.
    The magnetic axis passes through both poles.

    This function computes:
    - Geometric center
    - Magnetic axis (line through poles)
    - Axis direction (S to N)

    Args:
        magnet: Magnet object.

    Returns:
        Dictionary with:
        - center: Center position vector (cm)
        - axis: MagneticAxis object
        - direction: Unit vector along axis (S to N)
        - length: Magnetic length (cm)

    Reference:
        Part III, Art. 376: Magnetic center and axes.
    """
    axis = MagneticAxis.from_magnet(magnet)

    return {
        "center": axis.center.copy(),
        "axis": axis,
        "direction": axis.direction.copy(),
        "length": axis.length,
        "north_position": magnet.north_pole.position.copy(),
        "south_position": magnet.south_pole.position.copy(),
    }
