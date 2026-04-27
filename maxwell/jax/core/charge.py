"""
JAX-compatible electric charge and electrification.

Provides PointChargeJAX: a JAX-pytree version of maxwell.core.charge.PointCharge
that supports JIT compilation, automatic differentiation, and batched evaluation
via vmap over thousands of field points simultaneously.

Key differences from the NumPy version:
- Uses jax.numpy exclusively (no np.* calls)
- Safe division via jnp.where (no Python if/else on array values)
- Pytree-registered for jax.jit compatibility
- Batch-aware: field_at/vmap works on (N, 3) point arrays

Category: B (user_original) — JAX adapter for Maxwell's theory.

References:
    Part I, Arts. 29-32: Electrification by friction.
    Part I, Art. 45: Faraday's doctrine of no absolute charge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import jax
import jax.numpy as jnp
from jax import vmap, grad, jit

from maxwell.jax._compat import jax_tree, safe_div, safe_norm

__all__ = [
    "PointChargeJAX",
    "charge_system_field",
    "charge_system_potential",
]


@jax_tree
@dataclass
class PointChargeJAX:
    """A point charge in the electrostatic field (JAX-compatible).

    Art. 29: The quantity of electrification of a body.

    Attributes:
        q: Charge in esu (statcoulombs). Positive = vitreous, negative = resinous.
        position: Position vector (x, y, z) in cm, shape (3,).
    """

    q: float
    position: jax.Array  # shape (3,)

    def __post_init__(self):
        self.position = jnp.asarray(self.position, dtype=jnp.float64)

    # ── Single-point evaluation ─────────────────────────────────

    def field_at(self, point: jax.Array) -> jax.Array:
        """Electric field at a point due to this charge.

        E = q * r_hat / r^2  (Coulomb's law in CGS-ESU)

        Uses safe division: returns zero field when point == position.

        Args:
            point: Position vector (cm), shape (3,).

        Returns:
            Electric field vector (statvolt/cm), shape (3,).
        """
        point = jnp.asarray(point, dtype=jnp.float64)
        r_vec = point - self.position
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        r_mag_sq = jnp.maximum(r_mag ** 2, 1e-30)
        E_mag = self.q / r_mag_sq
        r_hat = jnp.where(r_mag > 1e-30, r_vec / r_mag, jnp.zeros(3))
        return E_mag * r_hat

    def potential_at(self, point: jax.Array) -> jax.Array:
        """Electric potential at a point.

        V = q / r  (CGS-ESU)

        Args:
            point: Position vector (cm), shape (3,).

        Returns:
            Electric potential (statvolt), scalar.
        """
        point = jnp.asarray(point, dtype=jnp.float64)
        r_vec = point - self.position
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        return safe_div(self.q, r_mag, safe_default=1e30)

    # ── Batched evaluation ──────────────────────────────────────

    def field_at_batched(self, points: jax.Array) -> jax.Array:
        """Electric field at many points simultaneously.

        Args:
            points: Array of position vectors, shape (N, 3).

        Returns:
            Electric field vectors, shape (N, 3).
        """
        return vmap(self.field_at)(points)

    def potential_at_batched(self, points: jax.Array) -> jax.Array:
        """Electric potential at many points simultaneously.

        Args:
            points: Array of position vectors, shape (N, 3).

        Returns:
            Electric potentials, shape (N,).
        """
        return vmap(self.potential_at)(points)

    # ── JIT-compiled variants ───────────────────────────────────

    @staticmethod
    @jit
    def _field_at_jit(q: float, pos: jax.Array, point: jax.Array) -> jax.Array:
        """JIT-compiled field calculation (static method for jax.scan use)."""
        r_vec = point - pos
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        r_mag_sq = jnp.maximum(r_mag ** 2, 1e-30)
        E_mag = q / r_mag_sq
        r_hat = jnp.where(r_mag > 1e-30, r_vec / r_mag, jnp.zeros(3))
        return E_mag * r_hat

    @staticmethod
    @jit
    def _potential_at_jit(q: float, pos: jax.Array, point: jax.Array) -> jax.Array:
        """JIT-compiled potential calculation."""
        r_vec = point - pos
        r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
        return safe_div(q, r_mag, safe_default=1e30)


# ── Multi-charge systems ────────────────────────────────────────

def charge_system_field(
    charges: Sequence[PointChargeJAX],
    points: jax.Array,
) -> jax.Array:
    """Total electric field from multiple point charges at many points.

    Uses superposition principle (linearity of Maxwell's equations).

    Args:
        charges: List of PointChargeJAX objects.
        points: Evaluation points, shape (N, 3).

    Returns:
        Total electric field, shape (N, 3).
    """

    def single_charge_field(charge: PointChargeJAX) -> jax.Array:
        return charge.field_at_batched(points)

    total = jnp.zeros_like(points)
    for charge in charges:
        total = total + single_charge_field(charge)
    return total


def charge_system_potential(
    charges: Sequence[PointChargeJAX],
    points: jax.Array,
) -> jax.Array:
    """Total electric potential from multiple point charges at many points.

    Args:
        charges: List of PointChargeJAX objects.
        points: Evaluation points, shape (N, 3).

    Returns:
        Total electric potential, shape (N,).
    """
    total = jnp.zeros(points.shape[0])
    for charge in charges:
        total = total + charge.potential_at_batched(points)
    return total


# ── Automatic differentiation demo ──────────────────────────────

def field_gradient(charge_q: float, point: jax.Array) -> jax.Array:
    """Gradient of E-field magnitude with respect to charge.

    Demonstrates auto-differentiation on Maxwell's formula.

    Args:
        charge_q: Charge value (differentiable).
        point: Evaluation point, shape (3,).

    Returns:
        d|E|/dq at the given point, shape (3,).
    """
    charge = PointChargeJAX(q=charge_q, position=jnp.zeros(3))

    def field_mag(q):
        c = PointChargeJAX(q=q, position=jnp.zeros(3))
        e = c.field_at(point)
        return jnp.linalg.norm(e)

    return grad(field_mag)(charge_q)
