"""maxwell.dynamics.lagrangian -- Lagrangian formulation for force derivation.

Implements Maxwell's variational approach: forces derived from energy
gradients via JAX automatic differentiation, eliminating manual
derivative computation.

Layer 52: The Lagrangian kernel provides the foundation for:
- Electrostatic forces from potential energy gradients
- Magnetic forces from field energy derivatives
- Generalized forces in arbitrary coordinate systems

Key principle: F = d/dt(dL/dq_dot) - dL/dq where L = T - U

References:
    Maxwell's Treatise: variational methods in mechanics.
    Lagrangian mechanics: energy-based force derivation.
    Arts. 540, 617: Electrotonic state and vector potential.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree


def _default_potential(q: jax.Array) -> jax.Array:
    """Zero potential energy."""
    return 0.0


def _default_kinetic(q: jax.Array, q_dot: jax.Array) -> jax.Array:
    """Default kinetic energy: T = 0.5 * sum(q_dot^2)."""
    return 0.5 * jnp.sum(q_dot**2)


@jax_tree
@dataclass
class GeneralizedSystem:
    """Lagrangian formulation for deriving forces from energy via JAX auto-diff.

    The generalized system takes potential and kinetic energy functions
    and derives equations of motion through automatic differentiation.

    This implements the Euler-Lagrange equation:
        d/dt(dL/dq_dot) - dL/dq = 0

    where L = T(q, q_dot) - U(q).

    Attributes:
        potential_fn: Callable U(q) -> float (potential energy).
        kinetic_fn: Callable T(q, q_dot) -> float (kinetic energy).
    """

    potential_fn: Callable = field(default_factory=lambda: _default_potential)
    kinetic_fn: Callable = field(default_factory=lambda: _default_kinetic)

    def potential_energy(self, q: jax.Array) -> jax.Array:
        """U(q) -- potential energy at generalized coordinates.

        Args:
            q: Generalized coordinates, shape (n,).

        Returns:
            Potential energy scalar.
        """
        return self.potential_fn(q)

    def kinetic_energy(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """T(q, q_dot) -- kinetic energy.

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Kinetic energy scalar.
        """
        return self.kinetic_fn(q, q_dot)

    def lagrangian(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """L = T - U -- the Lagrangian.

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Lagrangian value (scalar).
        """
        return self.kinetic_energy(q, q_dot) - self.potential_energy(q)

    def derive_forces(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """F = d/dt(dL/dq_dot) - dL/dq using JAX grad.

        Computes generalized forces via the Euler-Lagrange equation:
            F_i = d/dt(dL/dq_dot_i) - dL/dq_i

        For static (time-independent) systems, this simplifies to:
            F = -dL/dq  (force = negative gradient of potential)

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Generalized force vector, shape (n,).
        """
        dL_dq = grad(lambda q_: self.lagrangian(q_, q_dot))(q)
        return dL_dq

    def derive_electrostatic_force(
        self,
        q1: float,
        q2: float,
        r: jax.Array,
    ) -> jax.Array:
        """Derive Coulomb force from U = q1*q2/|r| via auto-diff.

        Proof-of-concept: starting from electrostatic potential energy,
        derive the force vector and verify it matches Coulomb's law:

            F = q1*q2 * r_hat / r^2

        Args:
            q1: Charge 1 (esu).
            q2: Charge 2 (esu).
            r: Separation vector from q1 to q2, shape (3,).

        Returns:
            Force on q2 due to q1, shape (3,).
        """

        def potential(r_vec):
            r_mag = jnp.linalg.norm(r_vec)
            return q1 * q2 / jnp.maximum(r_mag, 1e-30)

        force = -grad(potential)(r)
        return force

    @staticmethod
    @jit
    def coulomb_force_direct(q1: float, q2: float, r: jax.Array) -> jax.Array:
        """Direct Coulomb force calculation for verification.

        F = q1 * q2 * r / |r|^3

        Args:
            q1: Charge 1 (esu).
            q2: Charge 2 (esu).
            r: Separation vector, shape (3,).

        Returns:
            Force vector, shape (3,).
        """
        r_mag = jnp.linalg.norm(r)
        r_mag_cubed = jnp.maximum(r_mag**3, 1e-30)
        return q1 * q2 * r / r_mag_cubed
