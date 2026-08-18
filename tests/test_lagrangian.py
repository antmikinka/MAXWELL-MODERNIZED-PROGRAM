"""Tests for maxwell.dynamics.lagrangian -- Lagrangian formulation with JAX auto-diff."""

from __future__ import annotations

import numpy as np
import pytest

jax = pytest.importorskip("jax")
jax.numpy = pytest.importorskip("jax.numpy")

import jax
import jax.numpy as jnp
from jax import grad, vmap

from maxwell.dynamics.lagrangian import GeneralizedSystem


class TestGeneralizedSystemBasic:
    """Test GeneralizedSystem core functionality."""

    def test_lagrangian_equals_T_minus_U(self):
        """L = T - U."""
        system = GeneralizedSystem(
            potential_fn=lambda q: jnp.sum(q**2),
            kinetic_fn=lambda q, qd: 0.5 * jnp.sum(qd**2),
        )
        q = jnp.array([1.0, 2.0])
        q_dot = jnp.array([3.0, 4.0])
        L = system.lagrangian(q, q_dot)
        T = 0.5 * (3.0**2 + 4.0**2)
        U = 1.0**2 + 2.0**2
        assert np.isclose(float(L), T - U)

    def test_potential_energy(self):
        """U(q) returns correct value."""
        system = GeneralizedSystem(
            potential_fn=lambda q: 2.0 * jnp.sum(q),
        )
        q = jnp.array([1.0, 3.0, 5.0])
        U = system.potential_energy(q)
        assert np.isclose(float(U), 2.0 * 9.0)

    def test_kinetic_energy_default(self):
        """Default T = 0.5 * sum(q_dot^2)."""
        system = GeneralizedSystem()
        q = jnp.array([0.0])
        q_dot = jnp.array([2.0, 3.0])
        T = system.kinetic_energy(q, q_dot)
        assert np.isclose(float(T), 0.5 * (4.0 + 9.0))


class TestForceDerivation:
    """Test force derivation via auto-diff."""

    def test_force_derivation_coulomb(self):
        """Derived force matches Coulomb's law within 1e-10."""
        system = GeneralizedSystem()
        q1 = 1.0
        q2 = 2.0
        r = jnp.array([3.0, 0.0, 0.0])

        force_auto = system.derive_electrostatic_force(q1, q2, r)
        force_direct = GeneralizedSystem.coulomb_force_direct(q1, q2, r)

        np.testing.assert_allclose(
            np.array(force_auto), np.array(force_direct), atol=1e-10
        )

    def test_coulomb_force_magnitude(self):
        """|F| = q1*q2/r^2."""
        system = GeneralizedSystem()
        q1 = 3.0
        q2 = 5.0
        r = jnp.array([4.0, 0.0, 0.0])

        force = system.derive_electrostatic_force(q1, q2, r)
        magnitude = jnp.linalg.norm(force)
        expected = q1 * q2 / (4.0**2)

        assert np.isclose(float(magnitude), expected, atol=1e-10)

    def test_coulomb_force_direction(self):
        """Force direction = r_hat."""
        system = GeneralizedSystem()
        q1 = 1.0
        q2 = 1.0
        r = jnp.array([1.0, 1.0, 0.0])

        force = system.derive_electrostatic_force(q1, q2, r)
        r_hat = r / jnp.linalg.norm(r)
        force_hat = force / jnp.linalg.norm(force)

        np.testing.assert_allclose(np.array(force_hat), np.array(r_hat), atol=1e-10)

    def test_derive_forces_static(self):
        """Static force = -dU/dq."""
        system = GeneralizedSystem(
            potential_fn=lambda q: 0.5 * jnp.sum(q**2),
        )
        q = jnp.array([1.0, 2.0, 3.0])
        q_dot = jnp.array([0.0, 0.0, 0.0])

        forces = system.derive_forces(q, q_dot)
        expected = -q

        np.testing.assert_allclose(np.array(forces), np.array(expected), atol=1e-10)

    def test_electrostatic_force_sign(self):
        """Like charges repel, opposite attract."""
        system = GeneralizedSystem()

        r = jnp.array([1.0, 0.0, 0.0])
        F_repel = system.derive_electrostatic_force(1.0, 1.0, r)
        F_attract = system.derive_electrostatic_force(1.0, -1.0, r)

        assert float(F_repel[0]) > 0
        assert float(F_attract[0]) < 0

    def test_gradient_computation(self):
        """jax.grad works on lagrangian."""
        system = GeneralizedSystem(
            potential_fn=lambda q: jnp.sum(q**2),
            kinetic_fn=lambda q, qd: 0.5 * jnp.sum(qd**2),
        )

        q = jnp.array([1.0, 2.0])
        q_dot = jnp.array([0.5, 0.5])

        g = grad(lambda q_: system.lagrangian(q_, q_dot))(q)
        expected = -2.0 * q  # dL/dq = -dU/dq = -2q
        np.testing.assert_allclose(np.array(g), np.array(expected), atol=1e-10)


class TestJaxCompatibility:
    """Test JAX-specific features."""

    @pytest.mark.jax
    def test_jit_compatibility(self):
        """JIT-compiled coulomb_force_direct works."""
        q1 = 2.0
        q2 = 3.0
        r = jnp.array([1.0, 2.0, 3.0])

        force = GeneralizedSystem.coulomb_force_direct(q1, q2, r)
        assert force.shape == (3,)
        assert not jnp.any(jnp.isnan(force))
        assert not jnp.any(jnp.isinf(force))

    @pytest.mark.jax
    def test_custom_potential_fn(self):
        """Custom potential function works."""

        def harmonic_oscillator(q):
            return 0.5 * 10.0 * jnp.sum(q**2)

        system = GeneralizedSystem(potential_fn=harmonic_oscillator)
        q = jnp.array([1.0])
        U = system.potential_energy(q)
        assert np.isclose(float(U), 5.0)

    @pytest.mark.jax
    def test_custom_kinetic_fn(self):
        """Custom kinetic function works."""

        def relativistic_kinetic(q, qd):
            m = 1.0
            c = 1.0
            gamma = 1.0 / jnp.sqrt(1.0 - jnp.sum(qd**2) / (c**2) + 1e-30)
            return (gamma - 1.0) * m * c**2

        system = GeneralizedSystem(
            kinetic_fn=relativistic_kinetic,
            potential_fn=lambda q: 0.0,
        )
        q = jnp.array([0.0])
        q_dot = jnp.array([0.1])
        T = system.kinetic_energy(q, q_dot)
        assert float(T) > 0.0

    def test_zero_separation_safety(self):
        """No division by zero at r=0."""
        system = GeneralizedSystem()
        r = jnp.array([1e-15, 1e-15, 1e-15])
        force = system.derive_electrostatic_force(1.0, 1.0, r)
        assert not jnp.any(jnp.isnan(force))
        assert not jnp.any(jnp.isinf(force))

    @pytest.mark.jax
    def test_pytree_registration(self):
        """GeneralizedSystem works with jax.tree_util."""
        system = GeneralizedSystem(
            potential_fn=lambda q: jnp.sum(q**2),
            kinetic_fn=lambda q, qd: 0.5 * jnp.sum(qd**2),
        )
        leaves, treedef = jax.tree_util.tree_flatten(system)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)

        q = jnp.array([1.0, 2.0])
        q_dot = jnp.array([0.5, 1.0])
        L_orig = system.lagrangian(q, q_dot)
        L_restored = restored.lagrangian(q, q_dot)
        assert np.isclose(float(L_orig), float(L_restored))

    @pytest.mark.jax
    def test_batched_force_derivation(self):
        """vmap works over multiple positions."""
        system = GeneralizedSystem()

        def single_force(r):
            return system.derive_electrostatic_force(1.0, 1.0, r)

        positions = jnp.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 2.0, 0.0],
                [0.0, 0.0, 3.0],
            ]
        )

        forces = vmap(single_force)(positions)
        assert forces.shape == (3, 3)

        for i, r in enumerate(positions):
            expected = GeneralizedSystem.coulomb_force_direct(1.0, 1.0, r)
            np.testing.assert_allclose(
                np.array(forces[i]), np.array(expected), atol=1e-10
            )


class TestLagrangianProperties:
    """Test additional Lagrangian properties."""

    def test_default_zero_potential(self):
        """Default potential is zero."""
        system = GeneralizedSystem()
        q = jnp.array([1.0, 2.0, 3.0])
        U = system.potential_energy(q)
        assert np.isclose(float(U), 0.0)

    def test_lagrangian_with_no_velocity(self):
        """L = -U when q_dot = 0."""
        system = GeneralizedSystem(
            potential_fn=lambda q: jnp.sum(q),
        )
        q = jnp.array([1.0, 2.0])
        q_dot = jnp.array([0.0, 0.0])
        L = system.lagrangian(q, q_dot)
        assert np.isclose(float(L), -3.0)

    def test_derive_forces_with_velocity(self):
        """Forces computed with non-zero velocity."""
        system = GeneralizedSystem(
            potential_fn=lambda q: 0.5 * jnp.sum(q**2),
        )
        q = jnp.array([1.0])
        q_dot = jnp.array([5.0])
        forces = system.derive_forces(q, q_dot)
        np.testing.assert_allclose(np.array(forces), np.array([-1.0]), atol=1e-10)
