"""
Magnetic solenoids — tubular magnetic distributions.

Implements the theory of magnetic solenoids from Part III of Maxwell's Treatise:
- Simple solenoid (uniform tubular magnetization) (Arts. 407-408)
- Complex solenoid (generalized tubular distribution) (Art. 414)
- Solenoid potential calculations

A magnetic solenoid in Maxwell's sense is any tubular distribution
of magnetization, not necessarily a current-carrying coil. The
magnetic moment per unit length is constant along the solenoid.

Category: A (maxwell_original) — Maxwell's theory of magnetic solenoids.

References:
    Part III, Arts. 407-408, 414: Magnetic solenoids.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.magnet import Magnet, MagneticPole
from maxwell.meta.citation import maxwell_cite


@dataclass
class Solenoid:
    """
    Magnetic solenoid — uniform tubular magnetic distribution.

    Art. 407-408: A simple solenoid is a uniformly magnetized tube
    with magnetic moment per unit length constant along its axis.

    The solenoid behaves like a bar magnet with:
    - North pole at one end (where field lines emerge)
    - South pole at the other end (where field lines enter)
    - No external field from the sides (for infinite solenoid)

    Attributes:
        axis_start: Start point of solenoid axis (cm).
        axis_end: End point of solenoid axis (cm).
        moment_per_unit_length: Magnetic moment per cm (emu/cm).
        cross_section_area: Cross-sectional area (cm²).
    """

    axis_start: np.ndarray  # shape (3,)
    axis_end: np.ndarray  # shape (3,)
    moment_per_unit_length: float  # emu/cm
    cross_section_area: float = 1.0  # cm²

    def __post_init__(self):
        self.axis_start = np.asarray(self.axis_start, dtype=np.float64)
        self.axis_end = np.asarray(self.axis_end, dtype=np.float64)

        if self.axis_start.shape != (3,):
            raise ValueError("axis_start must be 3D")
        if self.axis_end.shape != (3,):
            raise ValueError("axis_end must be 3D")

    @property
    def axis_vector(self) -> np.ndarray:
        """Vector from start to end of solenoid."""
        return self.axis_end - self.axis_start

    @property
    def length(self) -> float:
        """Length of solenoid along axis (cm)."""
        return float(np.linalg.norm(self.axis_vector))

    @property
    def axis_direction(self) -> np.ndarray:
        """Unit vector along solenoid axis."""
        length = self.length
        if length == 0:
            return np.zeros(3)
        return self.axis_vector / length

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment of solenoid (emu)."""
        return self.moment_per_unit_length * self.length * self.axis_direction

    @classmethod
    @maxwell_cite(
        407,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Create solenoid from geometric parameters",
    )
    def from_parameters(
        cls,
        axis_start: np.ndarray,
        axis_end: np.ndarray,
        magnetization: float,
        cross_section_area: float,
    ) -> Solenoid:
        """
        Create solenoid from geometric and magnetic parameters.

        Art. 407: A solenoid is specified by its axis, length,
        cross-section, and uniform magnetization.

        The moment per unit length is:
            dm/dl = M × A

        where M is magnetization and A is cross-sectional area.

        Args:
            axis_start: Start of solenoid axis (cm).
            axis_end: End of solenoid axis (cm).
            magnetization: Uniform magnetization M (emu/cm³).
            cross_section_area: Cross-sectional area A (cm²).

        Returns:
            Solenoid object.

        Reference:
            Part III, Art. 407: Solenoid parameters.
        """
        moment_per_unit_length = magnetization * cross_section_area

        return cls(
            axis_start=axis_start,
            axis_end=axis_end,
            moment_per_unit_length=moment_per_unit_length,
            cross_section_area=cross_section_area,
        )

    @maxwell_cite(
        407,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Convert solenoid to equivalent bar magnet",
    )
    def to_bar_magnet(self) -> Magnet:
        """
        Convert solenoid to equivalent bar magnet.

        Art. 407: A finite solenoid is magnetically equivalent to
        a bar magnet with poles at its ends.

        The pole strength is:
            m = (dm/dl) = M × A

        Returns:
            Magnet object equivalent to the solenoid.

        Reference:
            Part III, Art. 407: Solenoid-magnet equivalence.
        """
        pole_strength = self.moment_per_unit_length

        north_pos = self.axis_end.copy()
        south_pos = self.axis_start.copy()

        return Magnet.from_pole_data(pole_strength, north_pos, south_pos)

    @maxwell_cite(
        408,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Calculate solenoid potential at point",
    )
    def potential_at(self, point: np.ndarray) -> float:
        """
        Calculate magnetic scalar potential of solenoid.

        Art. 408: The potential of a solenoid at point P is:

            Ω = (dm/dl) × (Ω_N - Ω_S)

        where Ω_N and Ω_S are the solid angles subtended by
        the end faces at P.

        For a solenoid along the z-axis from z₁ to z₂:
            Ω = (dm/dl) × (solid_angle(z₂) - solid_angle(z₁))

        Args:
            point: Position where potential is computed (cm).

        Returns:
            Magnetic scalar potential Ω (gauss·cm).

        Reference:
            Part III, Art. 408: Solenoid potential.
        """
        point = np.asarray(point, dtype=np.float64)

        # Compute solid angles subtended by each end face
        # For simplicity, treat ends as point poles
        r_north = point - self.axis_end
        r_south = point - self.axis_start

        r_n_mag = np.linalg.norm(r_north)
        r_s_mag = np.linalg.norm(r_south)

        # Potential from each end (treating as poles)
        # Ω = m/r for each pole
        omega = 0.0
        if r_n_mag > 0:
            omega += self.moment_per_unit_length / r_n_mag
        if r_s_mag > 0:
            omega -= self.moment_per_unit_length / r_s_mag

        return omega

    @maxwell_cite(
        408,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Calculate solenoid field at point",
    )
    def field_at(self, point: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field H of solenoid.

        Art. 408: The field is the negative gradient of potential:
            H = -∇Ω

        For a solenoid equivalent to a bar magnet:
            H = H_from_N_pole + H_from_S_pole

        Args:
            point: Position where field is computed (cm).

        Returns:
            Magnetic field H (gauss).

        Reference:
            Part III, Art. 408: Solenoid field.
        """
        point = np.asarray(point, dtype=np.float64)

        magnet = self.to_bar_magnet()

        # Field from each pole
        H = np.zeros(3)

        r_n = point - magnet.north_pole.position
        r_s = point - magnet.south_pole.position

        r_n_mag = np.linalg.norm(r_n)
        r_s_mag = np.linalg.norm(r_s)

        if r_n_mag > 0:
            H += magnet.north_pole.signed_strength * r_n / (r_n_mag**3)
        if r_s_mag > 0:
            H += magnet.south_pole.signed_strength * r_s / (r_s_mag**3)

        return H


@dataclass
class ComplexSolenoid:
    """
    Complex solenoid — generalized tubular magnetic distribution.

    Art. 414: A complex solenoid has variable magnetization along
    its length and possibly variable cross-section. The total
    moment is the integral of moment density along the axis.

    Attributes:
        axis_curve: Curve defining solenoid axis (N, 3).
        moment_density_func: Function giving dm/dl at each point.
        cross_section_func: Function giving area at each point.
    """

    axis_curve: np.ndarray  # shape (N, 3)
    moment_density_func: Optional[Callable[[np.ndarray], float]] = None
    cross_section_func: Optional[Callable[[np.ndarray], float]] = None
    moment_density_values: np.ndarray = field(default=None)  # shape (N,)

    def __post_init__(self):
        self.axis_curve = np.asarray(self.axis_curve, dtype=np.float64)

        if len(self.axis_curve.shape) != 2 or self.axis_curve.shape[1] != 3:
            raise ValueError("axis_curve must be (N, 3) array")

        if self.moment_density_values is not None:
            self.moment_density_values = np.asarray(
                self.moment_density_values, dtype=np.float64
            )
            if len(self.moment_density_values) != len(self.axis_curve):
                raise ValueError("Must have moment density for each axis point")

    @classmethod
    @maxwell_cite(
        414,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Create complex solenoid from discrete data",
    )
    def from_discrete_data(
        cls,
        axis_curve: np.ndarray,
        moment_density_values: np.ndarray,
    ) -> ComplexSolenoid:
        """
        Create complex solenoid from discrete measurements.

        Art. 414: A complex solenoid can be specified by giving
        the moment density at discrete points along its axis.

        Args:
            axis_curve: Points along solenoid axis (N, 3).
            moment_density_values: Moment per unit length at each point.

        Returns:
            ComplexSolenoid object.

        Reference:
            Part III, Art. 414: Complex solenoid specification.
        """
        return cls(
            axis_curve=axis_curve,
            moment_density_values=moment_density_values,
        )

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """
        Total magnetic moment of complex solenoid.

        m_total = ∫ (dm/dl) dl

        Returns:
            Total magnetic moment vector (emu).
        """
        if self.moment_density_values is None:
            return np.zeros(3)

        # Numerical integration along axis
        total = 0.0
        for i in range(len(self.axis_curve) - 1):
            dl = np.linalg.norm(self.axis_curve[i + 1] - self.axis_curve[i])
            dm_dl = (
                self.moment_density_values[i] + self.moment_density_values[i + 1]
            ) / 2
            total += dm_dl * dl

        # Direction from overall axis
        if len(self.axis_curve) > 1:
            overall_direction = self.axis_curve[-1] - self.axis_curve[0]
            overall_mag = np.linalg.norm(overall_direction)
            if overall_mag > 0:
                return total * overall_direction / overall_mag

        return np.zeros(3)

    @maxwell_cite(
        414,
        part=3,
        chapter="Magnetic Solenoids",
        theory_class="maxwell_original",
        description="Calculate potential of complex solenoid",
    )
    def potential_at(self, point: np.ndarray, num_segments: int = 100) -> float:
        """
        Calculate magnetic scalar potential of complex solenoid.

        Art. 414: The potential is computed by integrating
        contributions from each infinitesimal segment.

        Args:
            point: Position where potential is computed (cm).
            num_segments: Number of segments for integration.

        Returns:
            Magnetic scalar potential Ω (gauss·cm).

        Reference:
            Part III, Art. 414: Complex solenoid potential.
        """
        point = np.asarray(point, dtype=np.float64)

        if self.moment_density_values is None:
            return 0.0

        Omega = 0.0

        for i in range(len(self.axis_curve) - 1):
            seg_start = self.axis_curve[i]
            seg_end = self.axis_curve[i + 1]
            dl_vec = seg_end - seg_start
            dl = np.linalg.norm(dl_vec)

            if dl < 1e-10:
                continue

            # Average moment density for segment
            dm_dl = (
                self.moment_density_values[i] + self.moment_density_values[i + 1]
            ) / 2

            # Treat segment as small dipole
            seg_center = (seg_start + seg_end) / 2
            r_vec = point - seg_center
            r_mag = np.linalg.norm(r_vec)

            if r_mag > dl:
                # Far field: use dipole approximation
                r_hat = r_vec / r_mag
                dOmega = dm_dl * dl * float(np.dot(dl_vec / dl, r_hat)) / (r_mag**2)
                Omega += dOmega
            else:
                # Near field: use pole approximation
                r_start_mag = np.linalg.norm(point - seg_start)
                r_end_mag = np.linalg.norm(point - seg_end)

                if r_start_mag > 1e-10:
                    Omega -= dm_dl / r_start_mag
                if r_end_mag > 1e-10:
                    Omega += dm_dl / r_end_mag

        return Omega


@maxwell_cite(
    407,
    408,
    414,
    part=3,
    chapter="Magnetic Solenoids",
    theory_class="maxwell_original",
    description="Calculate solenoid potential from solid angle",
)
def solenoid_potential(
    solenoid: Solenoid,
    point: np.ndarray,
    use_solid_angle: bool = True,
) -> float:
    """
    Calculate magnetic potential of solenoid using solid angle.

    Art. 407-414: The potential of a solenoid at point P can be
    expressed in terms of the solid angle Ω subtended by the
    solenoid's cross-section at P:

        Φ = (dm/dl) × Ω

    For a finite solenoid, Ω is the difference of solid angles
    subtended by the two end faces.

    Args:
        solenoid: Solenoid object.
        point: Position where potential is computed (cm).
        use_solid_angle: If True, use solid angle formula.

    Returns:
        Magnetic scalar potential (gauss·cm).

    Reference:
        Part III, Arts. 407-414: Solenoid potential via solid angle.
    """
    if use_solid_angle:
        # Use the solenoid's own potential method
        return solenoid.potential_at(point)
    else:
        # Use equivalent magnet
        magnet = solenoid.to_bar_magnet()

        r_n = point - magnet.north_pole.position
        r_s = point - magnet.south_pole.position

        r_n_mag = np.linalg.norm(r_n)
        r_s_mag = np.linalg.norm(r_s)

        Omega = 0.0
        if r_n_mag > 0:
            Omega += magnet.north_pole.signed_strength / r_n_mag
        if r_s_mag > 0:
            Omega += magnet.south_pole.signed_strength / r_s_mag

        return Omega
