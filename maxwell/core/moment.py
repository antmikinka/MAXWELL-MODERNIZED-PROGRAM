"""
Magnetic moment and magnetization — vector theory of magnetization.

Implements the theory of magnetic moments from Part III of Maxwell's Treatise:
- Vector nature of magnetization (Arts. 381-382)
- Magnetic polarization and particle moments (Arts. 383-384)
- Resultant moment and axis determination (Art. 390)
- Magnetization intensity and components

Maxwell establishes that magnetization is a vector quantity, with
direction and magnitude, defined at each point in a magnetic material.

Category: A (maxwell_original) — Maxwell's vector theory of magnetization.

References:
    Part III, Arts. 381-384: Magnetization as a vector.
    Part III, Art. 390: Resultant magnetization.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MagnetizationVector:
    """
    Magnetization vector at a point — magnetic moment per unit volume.

    Art. 381-382: The magnetization at any point is a vector quantity
    representing the magnetic moment per unit volume. It has both
    magnitude (intensity) and direction (axis of magnetization).

    In CGS units:
        I = magnetic moment / volume  (emu/cm³)

    Attributes:
        value: Magnetization vector (I_x, I_y, I_z) in emu/cm³.
        position: Position where magnetization is defined (cm).
    """

    value: np.ndarray  # shape (3,)
    position: np.ndarray  # shape (3,)

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.value.shape != (3,):
            raise ValueError(f"Magnetization must be 3D, got {self.value.shape}")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got {self.position.shape}")

    @property
    def intensity(self) -> float:
        """Magnitude of magnetization vector |I|."""
        return float(np.linalg.norm(self.value))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in direction of magnetization."""
        mag = self.intensity
        if mag == 0:
            return np.zeros(3)
        return self.value / mag

    @property
    def components(self) -> MagnetizationComponents:
        """Get magnetization components (I_x, I_y, I_z)."""
        return MagnetizationComponents(
            I_x=self.value[0],
            I_y=self.value[1],
            I_z=self.value[2],
        )

    @classmethod
    @maxwell_cite(
        381,
        part=3, chapter="Magnetic Moment",
        theory_class="maxwell_original",
        description="Create magnetization from moment and volume",
    )
    def from_moment_and_volume(
        cls,
        magnetic_moment: np.ndarray,
        volume: float,
        position: np.ndarray,
    ) -> MagnetizationVector:
        """
        Create magnetization from magnetic moment and volume.

        Art. 381: Magnetization is the magnetic moment divided by
        the volume in which it is contained.

        I = m / V

        Args:
            magnetic_moment: Magnetic moment vector (emu).
            volume: Volume element (cm³).
            position: Position of volume element (cm).

        Returns:
            MagnetizationVector object.

        Reference:
            Part III, Art. 381: Magnetization definition.
        """
        if volume <= 0:
            raise ValueError("Volume must be positive")

        value = np.asarray(magnetic_moment, dtype=np.float64) / volume
        return cls(value=value, position=position)

    @classmethod
    @maxwell_cite(
        382,
        part=3, chapter="Magnetic Moment",
        theory_class="maxwell_original",
        description="Create magnetization from intensity and direction",
    )
    def from_intensity_and_direction(
        cls,
        intensity: float,
        direction: np.ndarray,
        position: np.ndarray,
    ) -> MagnetizationVector:
        """
        Create magnetization from intensity and direction.

        Art. 382: The magnetization vector is specified by its
        intensity (magnitude) and the direction of its axis.

        Args:
            intensity: Magnetization magnitude I (emu/cm³).
            direction: Unit vector along magnetization axis.
            position: Position (cm).

        Returns:
            MagnetizationVector object.

        Reference:
            Part III, Art. 382: Magnetization intensity and direction.
        """
        direction = np.asarray(direction, dtype=np.float64)
        dir_mag = np.linalg.norm(direction)

        if dir_mag == 0:
            raise ValueError("Direction cannot be zero vector")

        direction = direction / dir_mag
        value = intensity * direction

        return cls(value=value, position=position)

    @maxwell_cite(
        382,
        part=3, chapter="Magnetic Moment",
        theory_class="maxwell_original",
        description="Magnetization direction cosines",
    )
    def direction_cosines(self) -> tuple[float, float, float]:
        """
        Calculate direction cosines of magnetization axis.

        Art. 382: The direction of magnetization is specified by
        the cosines of the angles it makes with the coordinate axes.

        Returns:
            Tuple (cos_alpha, cos_beta, cos_gamma) where:
            - cos_alpha = angle with x-axis
            - cos_beta = angle with y-axis
            - cos_gamma = angle with z-axis

        Reference:
            Part III, Art. 382: Direction of magnetization.
        """
        direction = self.direction
        return (float(direction[0]), float(direction[1]), float(direction[2]))


@dataclass
class MagneticPolarization:
    """
    Magnetic polarization — alternative term for magnetization.

    Art. 383: Magnetic polarization is synonymous with magnetization,
    emphasizing the polar nature of magnetic matter. The term
    "polarization" highlights that each particle has opposite poles.

    Attributes:
        magnetization: Associated MagnetizationVector.
        pole_density: Magnetic pole surface density (emu/cm²).
    """

    magnetization: MagnetizationVector
    pole_density: float = 0.0  # emu/cm²

    @classmethod
    @maxwell_cite(
        383,
        part=3, chapter="Magnetic Polarization",
        theory_class="maxwell_original",
        description="Create magnetic polarization from magnetization",
    )
    def from_magnetization(
        cls,
        magnetization: MagnetizationVector,
    ) -> MagneticPolarization:
        """
        Create magnetic polarization from magnetization.

        Art. 383: The polarization of a magnet is its magnetization
        considered as arising from the polarity of its particles.

        Args:
            magnetization: MagnetizationVector object.

        Returns:
            MagneticPolarization object.

        Reference:
            Part III, Art. 383: Magnetic polarization.
        """
        return cls(magnetization=magnetization)

    @property
    def intensity(self) -> float:
        """Intensity of polarization (same as magnetization intensity)."""
        return self.magnetization.intensity

    @property
    def direction(self) -> np.ndarray:
        """Direction of polarization axis."""
        return self.magnetization.direction

    @maxwell_cite(
        383,
        part=3, chapter="Magnetic Polarization",
        theory_class="maxwell_original",
        description="Pole density on magnetized surface",
    )
    def surface_pole_density(self, surface_normal: np.ndarray) -> float:
        """
        Calculate magnetic pole density on a surface.

        Art. 383: The surface density of magnetic poles on a
        magnetized surface equals the normal component of
        magnetization.

        σ = I · n = I * cos(theta)

        where theta is the angle between magnetization and surface normal.

        Args:
            surface_normal: Unit normal vector to the surface.

        Returns:
            Pole surface density σ (emu/cm²).
            Positive = north poles, negative = south poles.

        Reference:
            Part III, Art. 383: Surface pole density.
        """
        surface_normal = np.asarray(surface_normal, dtype=np.float64)
        normal_mag = np.linalg.norm(surface_normal)

        if normal_mag == 0:
            raise ValueError("Surface normal cannot be zero")

        surface_normal = surface_normal / normal_mag
        return float(np.dot(self.magnetization.value, surface_normal))


@dataclass
class MagneticParticle:
    """
    Elementary magnetic particle — fundamental dipole unit.

    Art. 384: The elementary magnetic particle is the smallest
    division of magnetic matter that retains magnetic properties.
    Each particle is itself a complete magnet with definite moment.

    Attributes:
        magnetic_moment: Particle's magnetic moment (emu).
        position: Particle center position (cm).
        volume: Particle volume (cm³).
    """

    magnetic_moment: np.ndarray  # shape (3,)
    position: np.ndarray  # shape (3,)
    volume: float  # cm³

    def __post_init__(self):
        self.magnetic_moment = np.asarray(self.magnetic_moment, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.magnetic_moment.shape != (3,):
            raise ValueError(f"Magnetic moment must be 3D")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D")
        if self.volume <= 0:
            raise ValueError("Volume must be positive")

    @property
    def magnetization(self) -> MagnetizationVector:
        """Magnetization of the particle."""
        return MagnetizationVector.from_moment_and_volume(
            magnetic_moment=self.magnetic_moment,
            volume=self.volume,
            position=self.position,
        )

    @classmethod
    @maxwell_cite(
        384,
        part=3, chapter="Magnetic Particles",
        theory_class="maxwell_original",
        description="Create elementary magnetic particle",
    )
    def create_elementary_particle(
        cls,
        magnetic_moment: np.ndarray,
        position: np.ndarray,
        volume: float,
    ) -> MagneticParticle:
        """
        Create an elementary magnetic particle.

        Art. 384: Every elementary particle of magnetic matter
        possesses a magnetic moment and occupies a definite volume.

        Args:
            magnetic_moment: Magnetic moment vector (emu).
            position: Position of particle center (cm).
            volume: Particle volume (cm³).

        Returns:
            MagneticParticle object.

        Reference:
            Part III, Art. 384: Elementary magnetic particles.
        """
        return cls(
            magnetic_moment=magnetic_moment,
            position=position,
            volume=volume,
        )

    @maxwell_cite(
        384,
        part=3, chapter="Magnetic Particles",
        theory_class="maxwell_original",
        description="Field from elementary magnetic particle",
    )
    def field_at_point(self, point: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field from particle at a point.

        Art. 384: An elementary magnetic particle produces a dipole
        field that varies with distance and orientation.

        For a dipole at origin with moment m:
        H(r) = (3(m·r̂)r̂ - m) / r³

        Args:
            point: Position where field is calculated (cm).

        Returns:
            Magnetic field vector H (gauss).

        Reference:
            Part III, Art. 384: Field from magnetic particle.
        """
        r_vec = np.asarray(point, dtype=np.float64) - self.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return np.zeros(3)

        r_hat = r_vec / r_mag
        m = self.magnetic_moment

        # Dipole field formula
        m_dot_r = np.dot(m, r_hat)
        H = (3 * m_dot_r * r_hat - m) / (r_mag ** 3)

        return H

    @maxwell_cite(
        384,
        part=3, chapter="Magnetic Particles",
        theory_class="maxwell_original",
        description="Potential from elementary magnetic particle",
    )
    def potential_at_point(self, point: np.ndarray) -> float:
        """
        Calculate magnetic scalar potential from particle.

        Art. 384: The potential of a magnetic dipole at distance r
        is proportional to the cosine of the angle between the
        moment vector and the position vector.

        Ω(r) = (m·r) / r³ = (m·r̂) / r²

        Args:
            point: Position where potential is calculated (cm).

        Returns:
            Magnetic scalar potential Ω (gauss·cm).

        Reference:
            Part III, Art. 384: Magnetic potential of particle.
        """
        r_vec = np.asarray(point, dtype=np.float64) - self.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return 0.0

        return float(np.dot(self.magnetic_moment, r_vec) / (r_mag ** 3))


@dataclass
class MagneticMoment:
    """
    Magnetic moment — fundamental measure of magnetic strength.

    Art. 381-384: The magnetic moment is the product of pole strength
    and the distance between poles. It is a vector quantity pointing
    from south to north pole.

    This dataclass provides utilities for magnetic moment calculations.
    """

    value: np.ndarray  # shape (3,), magnetic moment in emu

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        if self.value.shape != (3,):
            raise ValueError(f"Magnetic moment must be 3D")

    @property
    def magnitude(self) -> float:
        """Magnitude of magnetic moment."""
        return float(np.linalg.norm(self.value))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector along moment direction (S to N)."""
        mag = self.magnitude
        if mag == 0:
            return np.zeros(3)
        return self.value / mag

    @classmethod
    @maxwell_cite(
        381,
        part=3, chapter="Magnetic Moment",
        theory_class="maxwell_original",
        description="Create magnetic moment from pole strength and length",
    )
    def from_pole_strength(
        cls,
        pole_strength: float,
        length: float,
        direction: np.ndarray,
    ) -> MagneticMoment:
        """
        Create magnetic moment from pole strength and length.

        Art. 381: The magnetic moment equals pole strength times
        the length of the magnet.

        m = p * L

        Args:
            pole_strength: Pole strength p (emu).
            length: Distance between poles L (cm).
            direction: Unit vector from S to N pole.

        Returns:
            MagneticMoment object.

        Reference:
            Part III, Art. 381: Magnetic moment from poles.
        """
        direction = np.asarray(direction, dtype=np.float64)
        dir_mag = np.linalg.norm(direction)

        if dir_mag == 0:
            raise ValueError("Direction cannot be zero")

        direction = direction / dir_mag
        magnitude = abs(pole_strength) * length

        return cls(value=magnitude * direction)

    @maxwell_cite(
        389,
        part=3, chapter="Magnetic Energy",
        theory_class="maxwell_original",
        description="Torque on magnetic moment in field",
    )
    def torque_in_field(self, field: np.ndarray) -> np.ndarray:
        """
        Calculate torque on magnetic moment in external field.

        τ = m × H

        Args:
            field: External H field (gauss).

        Returns:
            Torque vector (dyne·cm).

        Reference:
            Part III, Art. 389: Magnetic torque.
        """
        field = np.asarray(field, dtype=np.float64)
        return np.cross(self.value, field)

    @maxwell_cite(
        389,
        part=3, chapter="Magnetic Energy",
        theory_class="maxwell_original",
        description="Potential energy of magnetic moment in field",
    )
    def potential_energy_in_field(self, field: np.ndarray) -> float:
        """
        Calculate potential energy of magnetic moment in field.

        W = -m · H

        Args:
            field: External H field (gauss).

        Returns:
            Potential energy (erg).

        Reference:
            Part III, Art. 389: Magnetic potential energy.
        """
        field = np.asarray(field, dtype=np.float64)
        return -float(np.dot(self.value, field))


@dataclass
class MagnetizationIntensity:
    """
    Magnetization intensity — scalar magnitude of magnetization.

    Art. 382: The intensity of magnetization is the magnitude of
    the magnetization vector, representing the strength of
    magnetization regardless of direction.

    Attributes:
        value: Intensity value I (emu/cm³).
    """

    value: float  # emu/cm³

    @classmethod
    @maxwell_cite(
        382,
        part=3, chapter="Magnetization Intensity",
        theory_class="maxwell_original",
        description="Create intensity from magnetization vector",
    )
    def from_magnetization_vector(
        cls,
        magnetization: MagnetizationVector,
    ) -> MagnetizationIntensity:
        """
        Create intensity from magnetization vector.

        Args:
            magnetization: MagnetizationVector object.

        Returns:
            MagnetizationIntensity object.
        """
        return cls(value=magnetization.intensity)

    @classmethod
    @maxwell_cite(
        382,
        part=3, chapter="Magnetization Intensity",
        theory_class="maxwell_original",
        description="Create intensity from moment and volume",
    )
    def from_moment_and_volume(
        cls,
        moment_magnitude: float,
        volume: float,
    ) -> MagnetizationIntensity:
        """
        Create intensity from moment magnitude and volume.

        I = |m| / V

        Args:
            moment_magnitude: Magnetic moment magnitude (emu).
            volume: Volume (cm³).

        Returns:
            MagnetizationIntensity object.
        """
        if volume <= 0:
            raise ValueError("Volume must be positive")
        return cls(value=abs(moment_magnitude) / volume)


@dataclass
class MagnetizationComponents:
    """
    Components of magnetization along coordinate axes.

    Art. 382: The magnetization vector can be resolved into three
    components along the coordinate axes, which fully specify
    the direction and magnitude of magnetization.

    Attributes:
        I_x: x-component of magnetization (emu/cm³).
        I_y: y-component of magnetization (emu/cm³).
        I_z: z-component of magnetization (emu/cm³).
    """

    I_x: float
    I_y: float
    I_z: float

    @property
    def as_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.I_x, self.I_y, self.I_z], dtype=np.float64)

    @property
    def intensity(self) -> float:
        """Resultant intensity |I|."""
        return float(np.linalg.norm(self.as_array))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in magnetization direction."""
        mag = self.intensity
        if mag == 0:
            return np.zeros(3)
        return self.as_array / mag

    @classmethod
    @maxwell_cite(
        382,
        part=3, chapter="Magnetization Components",
        theory_class="maxwell_original",
        description="Create components from intensity and direction cosines",
    )
    def from_intensity_and_cosines(
        cls,
        intensity: float,
        cos_alpha: float,
        cos_beta: float,
        cos_gamma: float,
    ) -> MagnetizationComponents:
        """
        Create components from intensity and direction cosines.

        Art. 382: Given the intensity I and direction cosines
        (cos α, cos β, cos γ), the components are:
        I_x = I * cos α, I_y = I * cos β, I_z = I * cos γ

        Args:
            intensity: Magnetization intensity I.
            cos_alpha: Cosine of angle with x-axis.
            cos_beta: Cosine of angle with y-axis.
            cos_gamma: Cosine of angle with z-axis.

        Returns:
            MagnetizationComponents object.

        Reference:
            Part III, Art. 382: Components from direction cosines.
        """
        return cls(
            I_x=intensity * cos_alpha,
            I_y=intensity * cos_beta,
            I_z=intensity * cos_gamma,
        )

    @maxwell_cite(
        382,
        part=3, chapter="Magnetization Components",
        theory_class="maxwell_original",
        description="Get direction cosines from components",
    )
    def direction_cosines(self) -> tuple[float, float, float]:
        """
        Calculate direction cosines from components.

        Returns:
            Tuple (cos α, cos β, cos γ) of direction cosines.
        """
        direction = self.direction
        return (float(direction[0]), float(direction[1]), float(direction[2]))


@maxwell_cite(
    381, 382, 383, 384, 390,
    part=3, chapter="Magnetic Moment and Magnetization",
    theory_class="maxwell_original",
    description="Calculate resultant moment and axis of magnetized body",
)
def resultant_moment_and_axis(
    magnetization_field: list[MagnetizationVector],
) -> dict[str, np.ndarray | float]:
    """
    Calculate resultant magnetic moment and axis of magnetized body.

    Art. 390: The resultant magnetic moment of a magnetized body is
    the vector sum of the moments of all volume elements. The
    resultant axis is the direction of this total moment.

    For a continuously magnetized body:
        m_total = ∫ I dV

    where I is the magnetization at each point.

    Args:
        magnetization_field: List of MagnetizationVector objects
                           representing discretized magnetization.

    Returns:
        Dictionary with:
        - total_moment: Total magnetic moment vector (emu)
        - moment_magnitude: Magnitude of total moment
        - axis_direction: Unit vector along resultant axis
        - average_magnetization: Mean I vector (emu/cm³)
        - individual_moments: List of individual moment magnitudes

    Reference:
        Part III, Art. 390: Resultant moment and axis.
    """
    if not magnetization_field:
        return {
            "total_moment": np.zeros(3),
            "moment_magnitude": 0.0,
            "axis_direction": np.zeros(3),
            "average_magnetization": np.zeros(3),
            "individual_moments": [],
        }

    # Sum all magnetization vectors (assuming equal volume elements)
    total_moment = np.zeros(3)
    individual_moments = []

    for mag_vec in magnetization_field:
        # Each magnetization vector represents moment per unit volume
        # For simplicity, assume unit volume elements
        total_moment += mag_vec.value
        individual_moments.append(mag_vec.intensity)

    moment_magnitude = float(np.linalg.norm(total_moment))

    if moment_magnitude > 0:
        axis_direction = total_moment / moment_magnitude
    else:
        axis_direction = np.zeros(3)

    # Average magnetization
    avg_I = total_moment / len(magnetization_field)

    return {
        "total_moment": total_moment,
        "moment_magnitude": moment_magnitude,
        "axis_direction": axis_direction,
        "average_magnetization": avg_I,
        "individual_moments": individual_moments,
    }
