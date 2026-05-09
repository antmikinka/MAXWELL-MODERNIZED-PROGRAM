"""
Magnetic potential energy — energy of dipoles in magnetic fields.

Implements the theory of magnetic energy from Part III of Maxwell's Treatise:
- Potential energy of dipole in field: W = -m·B (Art. 389)
- Work done rotating magnetic moments
- Energy of magnetized bodies

Maxwell shows that a magnetic dipole in an external field has
potential energy depending on its orientation:

    W = -m · B = -mB cos(θ)

where θ is the angle between the moment and the field.

Category: A (maxwell_original) — Maxwell's theory of magnetic energy.

References:
    Part III, Art. 389: Magnetic potential energy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticPotentialEnergy:
    """
    Magnetic potential energy of a dipole in external field.

    Art. 389: A magnetic dipole with moment m in an external
    magnetic field B has potential energy:

        W = -m · B

    The energy is minimum when m is aligned with B (stable
    equilibrium) and maximum when anti-aligned (unstable).

    Attributes:
        magnetic_moment: Dipole moment m (emu).
        field: External field B (gauss).
        energy: Potential energy W (erg).
    """

    magnetic_moment: np.ndarray  # shape (3,), emu
    field: np.ndarray  # shape (3,), gauss

    def __post_init__(self):
        self.magnetic_moment = np.asarray(self.magnetic_moment, dtype=np.float64)
        self.field = np.asarray(self.field, dtype=np.float64)

        if self.magnetic_moment.shape != (3,):
            raise ValueError("magnetic_moment must be 3D")
        if self.field.shape != (3,):
            raise ValueError("field must be 3D")

    @property
    def energy(self) -> float:
        """Calculate potential energy W = -m·B."""
        return -float(np.dot(self.magnetic_moment, self.field))

    @property
    def torque(self) -> np.ndarray:
        """Calculate torque τ = m × B."""
        return np.cross(self.magnetic_moment, self.field)

    @property
    def alignment_angle(self) -> float:
        """Angle between moment and field (radians)."""
        m_mag = np.linalg.norm(self.magnetic_moment)
        B_mag = np.linalg.norm(self.field)

        if m_mag * B_mag == 0:
            return 0.0

        cos_theta = float(np.dot(self.magnetic_moment, self.field)) / (m_mag * B_mag)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        return float(np.arccos(cos_theta))

    @classmethod
    @maxwell_cite(
        389,
        part=3,
        chapter="Magnetic Energy",
        theory_class="maxwell_original",
        description="Create energy from moment and field",
    )
    def from_moment_and_field(
        cls,
        magnetic_moment: np.ndarray,
        field: np.ndarray,
    ) -> MagneticPotentialEnergy:
        """
        Create magnetic potential energy from moment and field.

        Args:
            magnetic_moment: Magnetic moment m (emu).
            field: External field B (gauss).

        Returns:
            MagneticPotentialEnergy object.

        Reference:
            Part III, Art. 389: W = -m·B.
        """
        return cls(magnetic_moment=magnetic_moment, field=field)


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Calculate dipole potential energy W = -m·B",
)
def calc_dipole_potential_energy(
    magnetic_moment: np.ndarray,
    field: np.ndarray,
) -> float:
    """
    Calculate potential energy of magnetic dipole in external field.

    Art. 389: The potential energy of a magnetic dipole with
    moment m in a field B is:

        W = -m · B

    This energy represents the work required to bring the dipole
    from infinity (where W = 0) to its current position and
    orientation.

    The negative sign means:
    - Aligned (m ∥ B): W < 0, stable equilibrium
    - Anti-aligned (m ∥ -B): W > 0, unstable equilibrium
    - Perpendicular (m ⊥ B): W = 0

    Args:
        magnetic_moment: Magnetic moment vector m (emu).
        field: External magnetic field B (gauss).

    Returns:
        Potential energy W (erg).

    Reference:
        Part III, Art. 389: Magnetic dipole energy.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    field = np.asarray(field, dtype=np.float64)

    return -float(np.dot(magnetic_moment, field))


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Work done rotating dipole in field",
)
def work_rotating_dipole(
    magnetic_moment: np.ndarray,
    initial_angle: float,
    final_angle: float,
    field_magnitude: float,
) -> float:
    """
    Calculate work done rotating a magnetic dipole in a field.

    Art. 389: The work required to rotate a dipole from angle θ₁
    to θ₂ in a uniform field B is:

        W = ∫ τ dθ = ∫ mB sin(θ) dθ
          = mB (cos(θ₁) - cos(θ₂))

    where τ = mB sin(θ) is the torque.

    Args:
        magnetic_moment: Magnitude of magnetic moment |m| (emu).
        initial_angle: Initial angle θ₁ (radians).
        final_angle: Final angle θ₂ (radians).
        field_magnitude: Field magnitude |B| (gauss).

    Returns:
        Work done (erg). Positive = work done on dipole.

    Reference:
        Part III, Art. 389: Work of rotation.
    """
    m_mag = abs(magnetic_moment)
    B_mag = abs(field_magnitude)

    # W = mB (cos θ₁ - cos θ₂)
    return float(m_mag * B_mag * (np.cos(initial_angle) - np.cos(final_angle)))


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Torque on dipole in magnetic field",
)
def torque_on_dipole(
    magnetic_moment: np.ndarray,
    field: np.ndarray,
) -> np.ndarray:
    """
    Calculate torque on magnetic dipole in external field.

    Art. 389: A magnetic dipole in an external field experiences
    a torque:

        τ = m × B

    This torque tends to align the dipole with the field.
    The magnitude is τ = mB sin(θ).

    Args:
        magnetic_moment: Magnetic moment m (emu).
        field: External field B (gauss).

    Returns:
        Torque vector τ (dyne·cm).

    Reference:
        Part III, Art. 389: Magnetic torque.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    field = np.asarray(field, dtype=np.float64)

    return np.cross(magnetic_moment, field)


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Force on dipole in non-uniform field",
)
def force_on_dipole(
    magnetic_moment: np.ndarray,
    field_func: callable,
    position: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate force on magnetic dipole in non-uniform field.

    Art. 389: In a non-uniform field, a dipole experiences a net
    force (not just torque):

        F = ∇(m · B)

    In components:
        F_i = Σ_j m_j ∂B_j/∂x_i

    Args:
        magnetic_moment: Magnetic moment m (emu).
        field_func: Function returning B at a position.
        position: Position of dipole (cm).
        h: Step size for numerical gradient.

    Returns:
        Force vector F (dyne).

    Reference:
        Part III, Art. 389: Force in non-uniform field.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    # Compute gradient of (m · B)
    F = np.zeros(3)

    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h

        B_plus = field_func(position + delta)
        B_minus = field_func(position - delta)

        m_dot_B_plus = float(np.dot(magnetic_moment, B_plus))
        m_dot_B_minus = float(np.dot(magnetic_moment, B_minus))

        F[i] = (m_dot_B_plus - m_dot_B_minus) / (2 * h)

    return F


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Stable equilibrium orientation of dipole",
)
def stable_equilibrium_orientation(
    magnetic_moment: np.ndarray,
    field: np.ndarray,
) -> dict[str, any]:
    """
    Find stable equilibrium orientation for magnetic dipole.

    Art. 389: A dipole has stable equilibrium when aligned with
    the field (minimum energy) and unstable equilibrium when
    anti-aligned (maximum energy).

    Stable: m ∥ B, W = -|m||B|
    Unstable: m ∥ -B, W = +|m||B|

    Args:
        magnetic_moment: Current magnetic moment (emu).
        field: External field B (gauss).

    Returns:
        Dictionary with:
        - stable_orientation: Unit vector for stable orientation
        - stable_energy: Minimum energy
        - unstable_orientation: Unit vector for unstable orientation
        - unstable_energy: Maximum energy
        - current_energy: Energy in current orientation
        - energy_to_rotate: Work needed to flip 180°

    Reference:
        Part III, Art. 389: Equilibrium orientations.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    field = np.asarray(field, dtype=np.float64)

    m_mag = np.linalg.norm(magnetic_moment)
    B_mag = np.linalg.norm(field)

    if B_mag == 0:
        return {
            "stable_orientation": np.zeros(3),
            "stable_energy": 0.0,
            "unstable_orientation": np.zeros(3),
            "unstable_energy": 0.0,
            "current_energy": 0.0,
            "energy_to_rotate": 0.0,
        }

    # Unit vector along field
    field_direction = field / B_mag

    # Energies
    stable_energy = -m_mag * B_mag
    unstable_energy = +m_mag * B_mag
    current_energy = -float(np.dot(magnetic_moment, field))

    # Work to flip 180° (from stable to unstable)
    energy_to_rotate = unstable_energy - stable_energy

    return {
        "stable_orientation": field_direction.copy(),
        "stable_energy": stable_energy,
        "unstable_orientation": -field_direction.copy(),
        "unstable_energy": unstable_energy,
        "current_energy": current_energy,
        "energy_to_rotate": energy_to_rotate,
    }


@maxwell_cite(
    389,
    part=3,
    chapter="Magnetic Energy",
    theory_class="maxwell_original",
    description="Energy of magnetized body in external field",
)
def energy_of_magnetized_body(
    magnetization_func: callable,
    H_field_func: callable,
    volume_points: np.ndarray,
) -> float:
    """
    Calculate total energy of magnetized body in external field.

    Art. 389: For an extended body with magnetization M(r) in
    an external field H(r), the total energy is:

        W = -∫ M · H dV

    This sums the energy of all molecular dipoles.

    Args:
        magnetization_func: Function returning M at a position.
        H_field_func: Function returning H at a position.
        volume_points: Sample points within the body (N, 3).

    Returns:
        Total potential energy (erg).

    Reference:
        Part III, Art. 389: Extended body energy.
    """
    volume_points = np.asarray(volume_points, dtype=np.float64)

    if len(volume_points.shape) != 2 or volume_points.shape[1] != 3:
        raise ValueError("volume_points must be (N, 3) array")

    # Estimate volume element
    if len(volume_points) > 1:
        bounds = np.max(volume_points, axis=0) - np.min(volume_points, axis=0)
        dV = np.prod(bounds) / len(volume_points)
    else:
        dV = 1.0

    total_energy = 0.0

    for point in volume_points:
        M = magnetization_func(point)
        H = H_field_func(point)

        # dW = -M · H dV
        total_energy -= float(np.dot(M, H)) * dV

    return total_energy
