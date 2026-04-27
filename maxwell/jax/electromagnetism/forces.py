"""
JAX-compatible Lorentz force and Maxwell stress tensor.

Provides JAX-pytree versions of:
- maxwell.electromagnetism.forces.lorentz.LorentzForce
- maxwell.electromagnetism.forces.stress_tensor.MaxwellStressTensor

Enabling JIT compilation, automatic differentiation, and vectorized
evaluation of electromagnetic forces in CGS-EMU units.

Implemented (Arts. 490-492, 641-646):
    - LorentzForceJAX: force on current-carrying wire, moving charge,
      torque on current loop, force density, parallel currents
    - MaxwellStressTensorJAX: full 3x3 stress tensor, electromagnetic
      pressure, surface force, field line tension

Category: B (user_original) -- JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 490-492: Lorentz force on currents and charges.
    Part IV, Arts. 641-646: Maxwell stress tensor and electromagnetic forces.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit, vmap

from maxwell.jax._compat import jax_tree, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "LorentzForceJAX",
    "MaxwellStressTensorJAX",
    "force_on_wire_jax",
    "force_on_charge_jax",
    "torque_on_loop_jax",
    "force_density_jax",
    "parallel_current_force_jax",
    "stress_tensor_jax",
    "electromagnetic_pressure_jax",
    "surface_force_jax",
]


# ── LorentzForceJAX ─────────────────────────────────────────────


@jax_tree
@dataclass
class LorentzForceJAX:
    """Lorentz force calculator (JAX-compatible pytree).

    Art. 490-492: Force on a current-carrying conductor in a magnetic field.

        F = I * (L x B)  (dynes)

    Attributes:
        current: Current in abamperes (EMU).
        length: Conductor length vector in cm, shape (3,).
        B_field: Magnetic field vector in gauss, shape (3,).
    """

    current: float
    length: jax.Array  # shape (3,)
    B_field: jax.Array  # shape (3,)

    def __post_init__(self):
        self.length = jnp.asarray(self.length, dtype=jnp.float64)
        self.B_field = jnp.asarray(self.B_field, dtype=jnp.float64)

    @property
    def force_vector(self) -> jax.Array:
        """F = I * (L x B), shape (3,)."""
        return jnp.asarray(self.current, dtype=jnp.float64) * jnp.cross(
            self.length, self.B_field
        )

    @property
    def magnitude(self) -> jax.Array:
        """|F| = I * |L| * |B| * sin(theta)."""
        return safe_norm(self.force_vector[None, :], axis=-1)[0]

    @property
    def direction(self) -> jax.Array:
        """Unit vector in force direction (zero if force is zero)."""
        f = self.force_vector
        mag = safe_norm(f[None, :], axis=-1)[0]
        return jnp.where(mag > 1e-30, f / mag, jnp.zeros(3))


# ── Standalone Lorentz force functions ──────────────────────────


@maxwell_cite(490, 491, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Force on a straight current-carrying wire in CGS-EMU units")
def force_on_wire_jax(
    current: jax.Array,
    length: jax.Array,
    B_field: jax.Array,
) -> jax.Array:
    """Force on a straight current-carrying wire: F = I * (L x B).

    Art. 490-491.

    Args:
        current: Current (abamperes).
        length: Length vector (cm), shape (3,).
        B_field: Magnetic field (gauss), shape (3,).

    Returns:
        Force vector (dynes), shape (3,).
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    length = jnp.asarray(length, dtype=jnp.float64)
    B_field = jnp.asarray(B_field, dtype=jnp.float64)
    return current * jnp.cross(length, B_field)


@maxwell_cite(491, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Lorentz force on a moving charge in CGS-EMU units")
def force_on_charge_jax(
    charge: jax.Array,
    velocity: jax.Array,
    B_field: jax.Array,
) -> jax.Array:
    """Force on a moving charge: F = q * (v x B).

    Art. 491.

    Args:
        charge: Charge (abcoulombs EMU).
        velocity: Velocity (cm/s), shape (3,).
        B_field: Magnetic field (gauss), shape (3,).

    Returns:
        Force vector (dynes), shape (3,).
    """
    charge = jnp.asarray(charge, dtype=jnp.float64)
    velocity = jnp.asarray(velocity, dtype=jnp.float64)
    B_field = jnp.asarray(B_field, dtype=jnp.float64)
    return charge * jnp.cross(velocity, B_field)


@maxwell_cite(490, 491, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Torque on a current loop in magnetic field")
def torque_on_loop_jax(
    magnetic_moment: jax.Array,
    B_field: jax.Array,
) -> jax.Array:
    """Torque on a current loop: tau = m x B.

    Art. 490-491.

    Args:
        magnetic_moment: Magnetic moment vector, shape (3,).
        B_field: Magnetic field (gauss), shape (3,).

    Returns:
        Torque vector (dyne*cm), shape (3,).
    """
    magnetic_moment = jnp.asarray(magnetic_moment, dtype=jnp.float64)
    B_field = jnp.asarray(B_field, dtype=jnp.float64)
    return jnp.cross(magnetic_moment, B_field)


@maxwell_cite(490, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Force density from current in magnetic field")
def force_density_jax(
    J: jax.Array,
    B: jax.Array,
) -> jax.Array:
    """Force density: f = J x B.

    Art. 490.

    Args:
        J: Current density (abamperes/cm^2), shape (3,).
        B: Magnetic field (gauss), shape (3,).

    Returns:
        Force density (dynes/cm^3), shape (3,).
    """
    J = jnp.asarray(J, dtype=jnp.float64)
    B = jnp.asarray(B, dtype=jnp.float64)
    return jnp.cross(J, B)


@maxwell_cite(492, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Force between parallel current-carrying conductors")
def parallel_current_force_jax(
    I1: jax.Array,
    I2: jax.Array,
    separation: jax.Array,
    wire_length: jax.Array,
) -> jax.Array:
    """Force between parallel currents: F = 2 * I1 * I2 * L / r.

    Art. 492. Positive = attractive (same direction).

    Args:
        I1: Current in first wire (abamperes).
        I2: Current in second wire (abamperes).
        separation: Distance between wires (cm).
        wire_length: Wire segment length (cm).

    Returns:
        Force (dynes). Positive = attractive.
    """
    I1 = jnp.asarray(I1, dtype=jnp.float64)
    I2 = jnp.asarray(I2, dtype=jnp.float64)
    separation = jnp.asarray(separation, dtype=jnp.float64)
    wire_length = jnp.asarray(wire_length, dtype=jnp.float64)
    return 2.0 * I1 * I2 * wire_length / separation


# ── MaxwellStressTensorJAX ──────────────────────────────────────


@jax_tree
@dataclass
class MaxwellStressTensorJAX:
    """Maxwell stress tensor calculator (JAX-compatible pytree).

    Art. 641-646: The stress tensor describes how EM fields transmit force.

        T_ij = (1/4pi)[E_i*E_j + H_i*H_j - (1/2)*delta_ij*(E^2 + H^2)]

    Attributes:
        E_field: Electric field vector (statvolts/cm), shape (3,).
        H_field: Magnetic field intensity (oersted), shape (3,).
    """

    E_field: jax.Array = None  # type: ignore[assignment]
    H_field: jax.Array = None  # type: ignore[assignment]

    def __post_init__(self):
        zero3 = jnp.zeros(3, dtype=jnp.float64)
        object.__setattr__(
            self, 'E_field',
            jnp.asarray(
                self.E_field if self.E_field is not None else zero3,
                dtype=jnp.float64,
            ),
        )
        object.__setattr__(
            self, 'H_field',
            jnp.asarray(
                self.H_field if self.H_field is not None else zero3,
                dtype=jnp.float64,
            ),
        )

    @property
    def E_squared(self) -> jax.Array:
        """E^2 = E . E."""
        return jnp.dot(self.E_field, self.E_field)

    @property
    def H_squared(self) -> jax.Array:
        """H^2 = H . H."""
        return jnp.dot(self.H_field, self.H_field)

    @property
    def electromagnetic_pressure(self) -> jax.Array:
        """P = (1/8pi)(E^2 + H^2)."""
        return (self.E_squared + self.H_squared) / (8.0 * jnp.pi)

    def stress_tensor(self) -> jax.Array:
        """Full 3x3 Maxwell stress tensor.

        Returns:
            T_ij array, shape (3, 3), in dynes/cm^2.
        """
        E_sq = self.E_squared
        H_sq = self.H_squared
        total_sq = E_sq + H_sq

        # Outer products: E_i E_j + H_i H_j
        field_product = (
            jnp.outer(self.E_field, self.E_field)
            + jnp.outer(self.H_field, self.H_field)
        )

        # Isotropic pressure term: -(1/8pi)(E^2+H^2) * I
        pressure_term = -(total_sq / (8.0 * jnp.pi)) * jnp.eye(3, dtype=jnp.float64)

        return field_product / (4.0 * jnp.pi) + pressure_term

    def surface_force(self, normal: jax.Array, area: jax.Array) -> jax.Array:
        """Force on a surface: F = T . n * A.

        Art. 644.

        Args:
            normal: Unit normal vector, shape (3,).
            area: Surface area (cm^2).

        Returns:
            Force vector (dynes), shape (3,).
        """
        normal = jnp.asarray(normal, dtype=jnp.float64)
        area = jnp.asarray(area, dtype=jnp.float64)
        n_mag = safe_norm(normal[None, :], axis=-1)[0]
        n = jnp.where(n_mag > 1e-30, normal / n_mag, jnp.array([0.0, 0.0, 1.0]))
        T = self.stress_tensor()
        return jnp.dot(T, n) * area


# ── Standalone stress tensor functions ──────────────────────────


@maxwell_cite(641, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Maxwell stress tensor for electromagnetic force transmission")
def stress_tensor_jax(
    E_field: jax.Array,
    H_field: jax.Array,
) -> jax.Array:
    """Maxwell stress tensor: T_ij = (1/4pi)[E_i E_j + H_i H_j - (1/2)delta_ij(E^2+H^2)].

    Art. 641.

    Args:
        E_field: Electric field, shape (3,).
        H_field: Magnetic field intensity, shape (3,).

    Returns:
        3x3 stress tensor, shape (3, 3).
    """
    E = jnp.asarray(E_field, dtype=jnp.float64)
    H = jnp.asarray(H_field, dtype=jnp.float64)
    E_sq = jnp.dot(E, E)
    H_sq = jnp.dot(H, H)
    total_sq = E_sq + H_sq

    field_product = jnp.outer(E, E) + jnp.outer(H, H)
    pressure = -(total_sq / (8.0 * jnp.pi)) * jnp.eye(3, dtype=jnp.float64)
    return field_product / (4.0 * jnp.pi) + pressure


@maxwell_cite(643, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Electromagnetic pressure from field energy density")
def electromagnetic_pressure_jax(
    E_field: jax.Array,
    H_field: jax.Array,
) -> jax.Array:
    """P = (1/8pi)(E^2 + H^2).

    Art. 643.
    """
    E = jnp.asarray(E_field, dtype=jnp.float64)
    H = jnp.asarray(H_field, dtype=jnp.float64)
    return (jnp.dot(E, E) + jnp.dot(H, H)) / (8.0 * jnp.pi)


@maxwell_cite(644, part=4, chapter="Electromagnetism",
              theory_class="maxwell_original",
              description="Surface force from Maxwell stress tensor integration")
def surface_force_jax(
    E_field: jax.Array,
    H_field: jax.Array,
    normal: jax.Array,
    area: jax.Array,
) -> jax.Array:
    """F = T(E,H) . n * A.

    Art. 644.
    """
    T = stress_tensor_jax(E_field, H_field)
    normal = jnp.asarray(normal, dtype=jnp.float64)
    area = jnp.asarray(area, dtype=jnp.float64)
    n_mag = safe_norm(normal[None, :], axis=-1)[0]
    n = jnp.where(n_mag > 1e-30, normal / n_mag, jnp.array([0.0, 0.0, 1.0]))
    return jnp.dot(T, n) * area
