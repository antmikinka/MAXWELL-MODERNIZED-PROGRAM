"""
JAX-compatible magnetic primitives — Part III (Magnetism) adapter.

Provides MagneticPoleJAX and MagnetJAX: JAX-pytree versions of
maxwell.core.magnet.MagneticPole and Magnet that support JIT compilation,
automatic differentiation, and batched evaluation.

Key differences from the NumPy version:
- Uses jax.numpy exclusively (no np.* calls)
- Safe division via jnp.where (no Python if/else on array values)
- Pytree-registered for jax.jit compatibility
- Batch-aware: field_at/vmap works on (N, 3) point arrays

Category: B (user_original) — JAX adapter for Maxwell's magnetism theory.

References:
    Part III, Arts. 371-376: Magnetic poles and force law.
    Part III, Art. 392: Earth's magnetic action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree, safe_div, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "MagneticPoleJAX",
    "MagnetJAX",
    "pole_force_jax",
    "mutual_action_jax",
    "torque_on_magnet_jax",
]


@jax_tree
@dataclass
class MagneticPoleJAX:
    """A magnetic pole — elementary source of magnetic field (JAX-compatible).

    Art. 371: The fundamental property of a magnet is that it has two poles,
    north (N) and south (S), which exert forces on each other.

    Attributes:
        strength: Pole strength m (EMU units). Positive for N, negative for S.
        position: Position vector (x, y, z) in cm, shape (3,).
    """

    strength: float
    position: jax.Array  # shape (3,)

    def __post_init__(self):
        self.position = jnp.asarray(self.position, dtype=jnp.float64)

    # ── Single-point evaluation ─────────────────────────────────

    def field_at(self, point: jax.Array) -> jax.Array:
        """Magnetic field H at a point due to this pole.

        H = m * r_hat / r^2  (CGS-EMU, analogous to Coulomb's law)

        Uses safe division: returns zero field when point == position.

        Args:
            point: Position vector (cm), shape (3,).

        Returns:
            Magnetic field vector (gauss/oersted), shape (3,).
        """
        point = jnp.asarray(point, dtype=jnp.float64)
        r_vec = point - self.position
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        r_mag_sq = jnp.maximum(r_mag**2, 1e-30)
        H_mag = self.strength / r_mag_sq
        r_hat = jnp.where(r_mag > 1e-30, r_vec / r_mag, jnp.zeros(3))
        return H_mag * r_hat

    # ── Batched evaluation ──────────────────────────────────────

    def field_at_batched(self, points: jax.Array) -> jax.Array:
        """Magnetic field at many points simultaneously.

        Args:
            points: Array of position vectors, shape (N, 3).

        Returns:
            Magnetic field vectors, shape (N, 3).
        """
        return vmap(self.field_at)(points)

    # ── JIT-compiled variants ───────────────────────────────────

    @staticmethod
    @jit
    def _field_at_jit(strength: float, pos: jax.Array, point: jax.Array) -> jax.Array:
        """JIT-compiled field calculation (static method for jax.scan use)."""
        r_vec = point - pos
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        r_mag_sq = jnp.maximum(r_mag**2, 1e-30)
        H_mag = strength / r_mag_sq
        r_hat = jnp.where(r_mag > 1e-30, r_vec / r_mag, jnp.zeros(3))
        return H_mag * r_hat


@jax_tree
@dataclass
class MagnetJAX:
    """A permanent magnet with north and south poles (JAX-compatible).

    Art. 372-373: A magnet consists of two equal and opposite magnetic poles
    separated by a finite distance. The magnetic moment is the product of
    pole strength and the distance between poles.

    Attributes:
        pole_strength: Magnitude of pole strength (EMU).
        north_position: Position of N pole (cm), shape (3,).
        south_position: Position of S pole (cm), shape (3,).
    """

    pole_strength: float
    north_position: jax.Array  # shape (3,)
    south_position: jax.Array  # shape (3,)

    def __post_init__(self):
        self.north_position = jnp.asarray(self.north_position, dtype=jnp.float64)
        self.south_position = jnp.asarray(self.south_position, dtype=jnp.float64)

    # ── Properties ──────────────────────────────────────────────

    @property
    def magnetic_moment(self) -> jax.Array:
        """Magnetic moment vector.

        Art. 373: m = pole_strength * (r_N - r_S)

        Returns:
            Magnetic moment vector (emu), shape (3,).
        """
        return self.pole_strength * (self.north_position - self.south_position)

    @property
    def magnetic_length(self) -> jax.Array:
        """Distance between poles (magnetic length).

        Returns:
            Scalar magnetic length (cm).
        """
        return safe_norm((self.north_position - self.south_position)[None, :], axis=-1)[
            0
        ]

    @property
    def magnetic_axis(self) -> jax.Array:
        """Unit vector along magnetic axis (S to N direction).

        Returns:
            Unit vector, shape (3,).
        """
        axis_vec = self.north_position - self.south_position
        length = safe_norm(axis_vec[None, :], axis=-1)[0]
        return jnp.where(
            length > 1e-30,
            axis_vec / length,
            jnp.zeros(3),
        )

    # ── Field evaluation ────────────────────────────────────────

    def field_at(self, point: jax.Array) -> jax.Array:
        """Total magnetic field H at a point due to both poles.

        H = m_N * r_hat_N / r_N^2 + m_S * r_hat_S / r_S^2

        Args:
            point: Position vector (cm), shape (3,).

        Returns:
            Magnetic field vector (gauss), shape (3,).
        """
        point = jnp.asarray(point, dtype=jnp.float64)

        # North pole contribution (positive strength)
        r_n = point - self.north_position
        r_n_mag = safe_norm(r_n[None, :], axis=-1)[0]
        r_n_mag_sq = jnp.maximum(r_n_mag**2, 1e-30)
        H_n = self.pole_strength * jnp.where(
            r_n_mag > 1e-30, r_n / (r_n_mag_sq * r_n_mag), jnp.zeros(3)
        )

        # South pole contribution (negative strength)
        r_s = point - self.south_position
        r_s_mag = safe_norm(r_s[None, :], axis=-1)[0]
        r_s_mag_sq = jnp.maximum(r_s_mag**2, 1e-30)
        H_s = -self.pole_strength * jnp.where(
            r_s_mag > 1e-30, r_s / (r_s_mag_sq * r_s_mag), jnp.zeros(3)
        )

        return H_n + H_s

    def field_at_batched(self, points: jax.Array) -> jax.Array:
        """Magnetic field at many points simultaneously.

        Args:
            points: Array of position vectors, shape (N, 3).

        Returns:
            Magnetic field vectors, shape (N, 3).
        """
        return vmap(self.field_at)(points)

    # ── Force, torque, energy ───────────────────────────────────

    def force_in_field(self, H_north: jax.Array, H_south: jax.Array) -> jax.Array:
        """Resultant force on magnet in external field.

        Art. 371-372: Each pole experiences a force proportional to
        its strength and the local field intensity.

        F = m * H(r_N) - m * H(r_S)

        Args:
            H_north: H field at north pole position, shape (3,).
            H_south: H field at south pole position, shape (3,).

        Returns:
            Total force vector on magnet (dyne), shape (3,).
        """
        H_north = jnp.asarray(H_north, dtype=jnp.float64)
        H_south = jnp.asarray(H_south, dtype=jnp.float64)
        F_north = self.pole_strength * H_north
        F_south = -self.pole_strength * H_south
        return F_north + F_south

    def torque_in_uniform_field(self, H: jax.Array) -> jax.Array:
        """Torque on magnet in uniform magnetic field.

        Art. 373: tau = m x H (cross product of moment and field)

        Args:
            H: Uniform H field vector (gauss), shape (3,).

        Returns:
            Torque vector (dyne*cm), shape (3,).
        """
        H = jnp.asarray(H, dtype=jnp.float64)
        return jnp.cross(self.magnetic_moment, H)

    def potential_energy_in_field(self, H: jax.Array) -> jax.Array:
        """Potential energy of magnet in uniform magnetic field.

        Art. 375: W = -m dot H

        Args:
            H: Uniform H field vector (gauss), shape (3,).

        Returns:
            Potential energy (erg), scalar.
        """
        H = jnp.asarray(H, dtype=jnp.float64)
        return -jnp.dot(self.magnetic_moment, H)

    # ── JIT-compiled variants ───────────────────────────────────

    @staticmethod
    @jit
    def _field_at_jit(
        pole_strength: float,
        north_pos: jax.Array,
        south_pos: jax.Array,
        point: jax.Array,
    ) -> jax.Array:
        """JIT-compiled field calculation from both poles."""
        # North pole
        r_n = point - north_pos
        r_n_mag = safe_norm(r_n[None, :], axis=-1)[0]
        r_n_mag_sq = jnp.maximum(r_n_mag**2, 1e-30)
        H_n = pole_strength * jnp.where(
            r_n_mag > 1e-30, r_n / (r_n_mag_sq * r_n_mag), jnp.zeros(3)
        )

        # South pole
        r_s = point - south_pos
        r_s_mag = safe_norm(r_s[None, :], axis=-1)[0]
        r_s_mag_sq = jnp.maximum(r_s_mag**2, 1e-30)
        H_s = -pole_strength * jnp.where(
            r_s_mag > 1e-30, r_s / (r_s_mag_sq * r_s_mag), jnp.zeros(3)
        )

        return H_n + H_s

    @staticmethod
    @jit
    def _torque_jit(
        pole_strength: float,
        north_pos: jax.Array,
        south_pos: jax.Array,
        H: jax.Array,
    ) -> jax.Array:
        """JIT-compiled torque calculation."""
        moment = pole_strength * (north_pos - south_pos)
        return jnp.cross(moment, H)

    @staticmethod
    @jit
    def _energy_jit(
        pole_strength: float,
        north_pos: jax.Array,
        south_pos: jax.Array,
        H: jax.Array,
    ) -> jax.Array:
        """JIT-compiled potential energy calculation."""
        moment = pole_strength * (north_pos - south_pos)
        return -jnp.dot(moment, H)


# ── Standalone functions ─────────────────────────────────────────


@maxwell_cite(
    376,
    part=3,
    chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Coulomb's law for magnetic poles (JAX-compatible)",
)
def pole_force_jax(m1: float, m2: float, r: jax.Array) -> jax.Array:
    """Force between two magnetic poles (Coulomb's law for magnetism).

    Art. 376: The force between magnetic poles varies inversely as
    the square of the distance between them.

    F = m1 * m2 / r^2  (CGS-EMU)

    Args:
        m1: Strength of first pole (EMU).
        m2: Strength of second pole (EMU).
        r: Separation distance (cm), scalar or array.

    Returns:
        Force magnitude (dyne). Positive = repulsive, negative = attractive.
    """
    r = jnp.asarray(r, dtype=jnp.float64)
    r_sq = r**2
    return safe_div(m1 * m2, r_sq, safe_default=0.0)


@maxwell_cite(
    392,
    part=3,
    chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Mutual action between two magnets (JAX-compatible)",
)
def mutual_action_jax(
    m1_strength: float,
    m1_north: jax.Array,
    m1_south: jax.Array,
    m2_strength: float,
    m2_north: jax.Array,
    m2_south: jax.Array,
) -> dict[str, jax.Array]:
    """Calculate mutual force and torque between two magnets.

    Art. 392: Two magnets exert forces and torques on each other
    through the interaction of their poles.

    This computes the force on magnet2 due to magnet1's field,
    and the torque on magnet2 trying to align it with magnet1's field.

    Args:
        m1_strength: Pole strength of magnet 1 (EMU).
        m1_north: North pole position of magnet 1, shape (3,).
        m1_south: South pole position of magnet 1, shape (3,).
        m2_strength: Pole strength of magnet 2 (EMU).
        m2_north: North pole position of magnet 2, shape (3,).
        m2_south: South pole position of magnet 2, shape (3,).

    Returns:
        Dictionary with:
        - force_on_2: Force vector on magnet2 (dyne), shape (3,)
        - torque_on_2: Torque vector on magnet2 (dyne*cm), shape (3,)
        - potential_energy: Interaction energy (erg), scalar
    """
    m1_north = jnp.asarray(m1_north, dtype=jnp.float64)
    m1_south = jnp.asarray(m1_south, dtype=jnp.float64)
    m2_north = jnp.asarray(m2_north, dtype=jnp.float64)
    m2_south = jnp.asarray(m2_south, dtype=jnp.float64)

    def h_from_magnet1(point: jax.Array) -> jax.Array:
        """H field from magnet 1 at a point."""
        # North pole contribution
        r_n = point - m1_north
        r_n_mag = safe_norm(r_n[None, :], axis=-1)[0]
        r_n_mag_sq = jnp.maximum(r_n_mag**2, 1e-30)
        H_n = m1_strength * jnp.where(
            r_n_mag > 1e-30, r_n / (r_n_mag_sq * r_n_mag), jnp.zeros(3)
        )

        # South pole contribution
        r_s = point - m1_south
        r_s_mag = safe_norm(r_s[None, :], axis=-1)[0]
        r_s_mag_sq = jnp.maximum(r_s_mag**2, 1e-30)
        H_s = -m1_strength * jnp.where(
            r_s_mag > 1e-30, r_s / (r_s_mag_sq * r_s_mag), jnp.zeros(3)
        )

        return H_n + H_s

    # Force on magnet 2: F = m*H(r_N) - m*H(r_S)
    H_at_m2_north = h_from_magnet1(m2_north)
    H_at_m2_south = h_from_magnet1(m2_south)
    force_on_2 = m2_strength * H_at_m2_north - m2_strength * H_at_m2_south

    # Torque on magnet 2: field at center
    m2_center = (m2_north + m2_south) / 2.0
    H_at_m2_center = h_from_magnet1(m2_center)
    m2_moment = m2_strength * (m2_north - m2_south)
    torque_on_2 = jnp.cross(m2_moment, H_at_m2_center)

    # Potential energy: W = -m dot H at center
    potential_energy = -jnp.dot(m2_moment, H_at_m2_center)

    return {
        "force_on_2": force_on_2,
        "torque_on_2": torque_on_2,
        "potential_energy": potential_energy,
    }


@maxwell_cite(
    373,
    part=3,
    chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Torque on magnet in uniform magnetic field (JAX-compatible)",
)
def torque_on_magnet_jax(magnetic_moment: jax.Array, H_field: jax.Array) -> jax.Array:
    """Calculate torque on a magnet in a uniform magnetic field.

    Art. 373: tau = m x H (cross product of moment and field)

    Args:
        magnetic_moment: Magnetic moment vector (emu), shape (3,).
        H_field: Uniform H field vector (gauss), shape (3,).

    Returns:
        Torque vector (dyne*cm), shape (3,).
    """
    magnetic_moment = jnp.asarray(magnetic_moment, dtype=jnp.float64)
    H_field = jnp.asarray(H_field, dtype=jnp.float64)
    return jnp.cross(magnetic_moment, H_field)


# ── Automatic differentiation demo ──────────────────────────────


@maxwell_cite(
    371,
    376,
    part=3,
    chapter="Magnetic Poles",
    theory_class="maxwell_original",
    description="Gradient of pole force w.r.t. pole strength demonstrating auto-diff",
)
def pole_force_gradient(m1: float, m2: float, r: float) -> jax.Array:
    """Gradient of pole force with respect to m1.

    Demonstrates auto-differentiation on Maxwell's magnetic force law.

    Args:
        m1: Strength of first pole (differentiable).
        m2: Strength of second pole.
        r: Separation distance.

    Returns:
        dF/dm1 = m2/r^2
    """
    return grad(lambda m: pole_force_jax(m, m2, jnp.asarray(r)))(m1)
