"""
Tests for maxwell.jax — JAX adapter package.

Tests cover:
1. Pytree registration (JAX compatibility)
2. PointChargeJAX correctness vs NumPy reference
3. JIT compilation
4. Automatic differentiation
5. Batched evaluation (vmap)
6. AGM elliptic integrals
7. JAX special function wrappers (legendre, lpmv, sph_harm_y)
8. Safe arithmetic operations
"""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax._compat import jax_tree, safe_div, safe_sqrt, safe_norm
from maxwell.jax._elliptic import (
    ellipk_jax,
    ellipe_jax,
    verify_elliptic_integrals,
)
from maxwell.jax._scipy_special import (
    lpmv_jax,
    legendre_jax,
    sph_harm_y_jax,
)
from maxwell.jax.core.charge import (
    PointChargeJAX,
    charge_system_field,
    charge_system_potential,
    field_gradient,
)

jax.config.update("jax_enable_x64", True)


# ── Pytree Registration ─────────────────────────────────────────


class TestPytreeRegistration:
    """Test that PointChargeJAX is a proper JAX pytree."""

    def test_pytree_flatten(self):
        """PointChargeJAX can be flattened and unflattened."""
        charge = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 0.0]))
        leaves, treedef = jax.tree_util.tree_flatten(charge)
        assert len(leaves) == 2  # q and position
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert restored.q == charge.q
        assert jnp.allclose(restored.position, charge.position)

    def test_jit_compatible(self):
        """PointChargeJAX works with jax.jit."""

        @jax.jit
        def compute_field(q, pos, point):
            c = PointChargeJAX(q=q, position=pos)
            return c.field_at(point)

        result = compute_field(1.0, jnp.zeros(3), jnp.array([1.0, 0.0, 0.0]))
        assert result.shape == (3,)

    def test_vmap_compatible(self):
        """PointChargeJAX works with jax.vmap."""

        def single_field(point):
            c = PointChargeJAX(q=1.0, position=jnp.zeros(3))
            return c.field_at(point)

        points = jnp.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
        result = jax.vmap(single_field)(points)
        assert result.shape == (3, 3)


# ── PointChargeJAX Correctness ──────────────────────────────────


class TestPointChargeJAX:
    """Test PointChargeJAX against NumPy reference implementation."""

    def setup_method(self):
        self.charge = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 0.0]))

    def test_field_at_single_point(self):
        """E = q/r^2 at 5 cm: E = 0.04 statvolt/cm."""
        point = jnp.array([5.0, 0.0, 0.0])
        E = self.charge.field_at(point)
        expected = jnp.array([0.04, 0.0, 0.0])
        assert jnp.allclose(E, expected, atol=1e-10)

    def test_field_at_origin_safe(self):
        """Field at charge position should be zero (safe division)."""
        E = self.charge.field_at(jnp.array([0.0, 0.0, 0.0]))
        assert jnp.allclose(E, jnp.zeros(3), atol=1e-15)

    def test_potential_at_single_point(self):
        """V = q/r at 5 cm: V = 0.2 statvolt."""
        point = jnp.array([5.0, 0.0, 0.0])
        V = self.charge.potential_at(point)
        assert abs(V - 0.2) < 1e-10

    def test_field_radial_direction(self):
        """Field points radially away from positive charge."""
        point = jnp.array([1.0, 1.0, 1.0])
        E = self.charge.field_at(point)
        r_hat = point / jnp.linalg.norm(point)
        E_hat = E / jnp.linalg.norm(E)
        assert jnp.allclose(E_hat, r_hat, atol=1e-10)

    def test_negative_charge_field(self):
        """Negative charge produces inward-pointing field."""
        neg_charge = PointChargeJAX(q=-1.0, position=jnp.zeros(3))
        point = jnp.array([1.0, 0.0, 0.0])
        E = neg_charge.field_at(point)
        assert E[0] < 0

    def test_matches_numpy_reference(self):
        """JAX results match NumPy PointCharge exactly."""
        from maxwell.core.charge import PointCharge

        point = np.array([5.0, 3.0, 2.0])
        np_charge = PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))
        E_np = np_charge.field_at(point)

        jax_charge = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 0.0]))
        E_jax = jax_charge.field_at(jnp.array(point))

        assert jnp.allclose(E_jax, E_np, atol=1e-10)
        V_np = np_charge.potential_at(point)
        V_jax = jax_charge.potential_at(jnp.array(point))
        assert abs(V_jax - V_np) < 1e-10

    def test_batched_field(self):
        """Batched field evaluation."""
        points = jnp.array([
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
        ])
        E = self.charge.field_at_batched(points)
        assert E.shape == (3, 3)
        # E magnitude = 1/r^2: 1.0, 0.25, 0.04
        expected_magnitudes = jnp.array([1.0, 0.25, 0.04])
        actual_magnitudes = jnp.linalg.norm(E, axis=1)
        assert jnp.allclose(actual_magnitudes, expected_magnitudes, atol=1e-10)

    def test_batched_potential(self):
        """Batched potential evaluation."""
        points = jnp.array([
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
        ])
        V = self.charge.potential_at_batched(points)
        assert V.shape == (3,)
        expected = jnp.array([1.0, 0.5, 0.2])
        assert jnp.allclose(V, expected, atol=1e-10)


# ── Multi-charge Systems ────────────────────────────────────────


class TestChargeSystem:
    """Test superposition of multiple charges."""

    def test_dipole_field(self):
        """Electric field of a dipole (equal and opposite charges)."""
        pos = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 0.5]))
        neg = PointChargeJAX(q=-1.0, position=jnp.array([0.0, 0.0, -0.5]))

        point = jnp.array([1.0, 0.0, 0.0])
        E = charge_system_field([pos, neg], point[None, :])
        assert E.shape == (1, 3)
        # Field should point along z (dipole axis) at equatorial point
        assert E[0, 2] < 0  # Points toward negative charge

    def test_dipole_potential_zero_at_midplane(self):
        """Dipole potential is zero at the equatorial plane."""
        pos = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 1.0]))
        neg = PointChargeJAX(q=-1.0, position=jnp.array([0.0, 0.0, -1.0]))

        point = jnp.array([[1.0, 0.0, 0.0]])
        V = charge_system_potential([pos, neg], point)
        assert abs(V[0]) < 1e-10

    def test_charge_conservation(self):
        """Net charge of dipole is zero."""
        pos = PointChargeJAX(q=1.0, position=jnp.zeros(3))
        neg = PointChargeJAX(q=-1.0, position=jnp.ones(3))
        total_charge = pos.q + neg.q
        assert abs(total_charge) < 1e-15


# ── Automatic Differentiation ───────────────────────────────────


class TestAutoDiff:
    """Test JAX auto-differentiation on Maxwell's formulas."""

    def test_field_gradient_wrt_charge(self):
        """d|E|/dq = |E|/q for point charge (linearity)."""
        q = 1.0
        point = jnp.array([1.0, 0.0, 0.0])
        g = field_gradient(q, point)
        # For E = q/r^2, dE/dq = 1/r^2 = E/q
        E_mag = 1.0  # q=1, r=1 -> E=1
        assert abs(g - 1.0) < 1e-8

    def test_potential_gradient_wrt_position(self):
        """Gradient of V w.r.t. position = E (since V = q/|point-pos|, dV/dpos = q*r_vec/r^3)."""

        def potential_at_pos(pos):
            c = PointChargeJAX(q=1.0, position=pos)
            return c.potential_at(jnp.array([1.0, 0.0, 0.0]))

        grad_v = jax.grad(potential_at_pos)(jnp.zeros(3))
        # dV/dpos = q*r_vec/r^3 = (1,0,0) at r=1
        assert jnp.allclose(grad_v, jnp.array([1.0, 0.0, 0.0]), atol=1e-6)


# ── AGM Elliptic Integrals ──────────────────────────────────────


class TestEllipticIntegrals:
    """Test pure JAX elliptic integrals against known values."""

    def test_K_zero(self):
        """K(0) = pi/2."""
        result = ellipk_jax(0.0)
        assert abs(result - jnp.pi / 2.0) < 1e-10

    def test_E_zero(self):
        """E(0) = pi/2."""
        result = ellipe_jax(0.0)
        assert abs(result - jnp.pi / 2.0) < 1e-10

    def test_K_half(self):
        """K(0.5) ~ 1.8540746773013719."""
        result = ellipk_jax(0.5)
        expected = 1.8540746773013719
        assert abs(result - expected) < 1e-10

    def test_E_half(self):
        """E(0.5) ~ 1.3506438810476755."""
        result = ellipe_jax(0.5)
        expected = 1.3506438810476755
        assert abs(result - expected) < 1e-10

    def test_K_increasing(self):
        """K(m) increases with m."""
        k1 = ellipk_jax(0.1)
        k2 = ellipk_jax(0.9)
        assert k2 > k1

    def test_verification_suite(self):
        """Run the full verification suite."""
        results = verify_elliptic_integrals()
        assert results["all_pass"] is True

    def test_jit_compatible(self):
        """Elliptic integrals work under JIT."""

        @jax.jit
        def compute_k(m):
            return ellipk_jax(m)

        result = compute_k(0.5)
        assert abs(result - 1.8540746773013719) < 1e-10

    def test_vmap_compatible(self):
        """Elliptic integrals work with vmap."""
        params = jnp.array([0.0, 0.25, 0.5, 0.75])
        results = jax.vmap(ellipk_jax)(params)
        assert results.shape == (4,)
        # K should be monotonically increasing
        assert jnp.all(jnp.diff(results) > 0)


# ── JAX Special Functions ───────────────────────────────────────


class TestJAXSpecialFunctions:
    """Test pure JAX special function wrappers."""

    def test_legendre_P0(self):
        """P_0(x) = 1."""
        x = jnp.linspace(-1, 1, 100)
        result = legendre_jax(0, x)
        assert jnp.allclose(result, jnp.ones_like(x), atol=1e-10)

    def test_legendre_P1(self):
        """P_1(x) = x."""
        x = jnp.linspace(-1, 1, 100)
        result = legendre_jax(1, x)
        assert jnp.allclose(result, x, atol=1e-10)

    def test_legendre_P2(self):
        """P_2(x) = (3x^2 - 1)/2."""
        x = jnp.array([0.5, 0.0, -0.5, 1.0])
        result = legendre_jax(2, x)
        expected = (3 * x ** 2 - 1) / 2.0
        assert jnp.allclose(result, expected, atol=1e-10)

    def test_lpmv_P00(self):
        """P_0^0(x) = 1."""
        x = jnp.linspace(-1, 1, 50)
        result = lpmv_jax(0, 0, x)
        assert jnp.allclose(result, jnp.ones_like(x), atol=1e-10)

    def test_lpmv_P11(self):
        """P_1^1(x) = -sqrt(1-x^2)."""
        x = jnp.array([0.0, 0.5, 1.0])
        result = lpmv_jax(1, 1, x)
        expected = -jnp.sqrt(1.0 - x ** 2)
        assert jnp.allclose(result, expected, atol=1e-10)

    def test_sph_harm_y_normalization(self):
        """Y_00 = 1/(2*sqrt(pi))."""
        y00 = sph_harm_y_jax(0, 0, jnp.array([0.0]), jnp.array([0.0]))
        expected = 1.0 / (2.0 * jnp.sqrt(jnp.pi))
        # Wrapper squeezes single-element results back to scalar
        val = float(jnp.abs(y00)) if y00.ndim == 0 else float(jnp.abs(y00)[0])
        assert abs(val - float(expected)) < 1e-6

    def test_sph_harm_y_batched(self):
        """Spherical harmonics work on arrays."""
        phi = jnp.linspace(0, 2 * jnp.pi, 10)
        theta = jnp.linspace(0, jnp.pi, 10)
        y10 = sph_harm_y_jax(0, 1, phi, theta)
        assert y10.shape == (10,)

    def test_jit_legendre(self):
        """Legendre polynomial works under JIT."""

        @jax.jit
        def compute_legendre(x):
            return legendre_jax(5, x)

        result = compute_legendre(jnp.array(0.5))
        assert jnp.isfinite(result)


# ── Safe Arithmetic ─────────────────────────────────────────────


class TestSafeArithmetic:
    """Test safe arithmetic operations."""

    def test_safe_div_normal(self):
        """Normal division works."""
        result = safe_div(jnp.array(10.0), jnp.array(2.0))
        assert abs(result - 5.0) < 1e-15

    def test_safe_div_zero(self):
        """Division by zero returns safe_default."""
        result = safe_div(jnp.array(1.0), jnp.array(0.0), safe_default=0.0)
        assert result == 0.0

    def test_safe_sqrt_negative(self):
        """Sqrt of negative returns safe_default."""
        result = safe_sqrt(jnp.array(-1.0), safe_default=0.0)
        assert result == 0.0

    def test_safe_norm_nonzero(self):
        """Norm of non-zero vector."""
        v = jnp.array([3.0, 4.0, 0.0])
        result = safe_norm(v[None, :], axis=-1)[0]
        assert abs(result - 5.0) < 1e-15

    def test_safe_norm_zero(self):
        """Norm of zero vector returns safe_default."""
        v = jnp.zeros(3)
        result = safe_norm(v[None, :], axis=-1, safe_default=1e-30)[0]
        assert result == 1e-30


# ── Imports for new JAX adapter modules ────────────────────────────

try:
    from maxwell.jax.electromagnetism.induction import (
        FaradayInductionJAX,
        analyze_faraday_induction_jax,
        emf_wrt_flux_rate,
        flux_wrt_bfield,
        flux_over_batch,
    )

    HAS_INDUCTION = True
except ImportError:
    HAS_INDUCTION = False

try:
    from maxwell.jax.electromagnetism.equations import (
        MaxwellEquationsJAX,
        verify_maxwell_equations_jax,
    )

    HAS_EQUATIONS = True
except ImportError:
    HAS_EQUATIONS = False

try:
    from maxwell.jax.math.spherical_harmonics import (
        SphericalHarmonicExpansionJAX,
        addition_theorem_jax,
        legendre_batched,
    )

    HAS_SPH_HARM = True
except ImportError:
    HAS_SPH_HARM = False


# ── Faraday Induction JAX ─────────────────────────────────────────


@pytest.mark.skipif(not HAS_INDUCTION, reason="maxwell.jax.electromagnetism.induction not installed")
class TestFaradayInductionJAX:
    """Test FaradayInductionJAX against Faraday's law (Art. 528-531, 542)."""

    def setup_method(self):
        self.coil = FaradayInductionJAX(num_turns=100, resistance=50.0)

    def test_magnetic_flux_uniform_parallel(self):
        """Phi = B * A for B parallel to normal (z-axis)."""
        B = jnp.array([0.0, 0.0, 1000.0])
        flux = self.coil.magnetic_flux(B, area=10.0)
        # N * B * A = 100 * 1000 * 10 = 1_000_000
        assert abs(flux - 1e6) < 1e-6

    def test_magnetic_flux_perpendicular(self):
        """Phi = 0 when B is perpendicular to normal."""
        B = jnp.array([1000.0, 0.0, 0.0])
        flux = self.coil.magnetic_flux(B, area=10.0)
        assert abs(flux) < 1e-15

    def test_magnetic_flux_custom_normal(self):
        """Flux with a custom (non-unit) normal vector."""
        B = jnp.array([0.0, 0.0, 500.0])
        normal = jnp.array([0.0, 0.0, 2.0])  # non-unit, should be normalized
        flux = self.coil.magnetic_flux(B, area=10.0, normal=normal)
        expected = 100 * 500 * 10  # normal is normalized to [0,0,1]
        assert abs(flux - expected) < 1e-6

    def test_induced_emf_lenz_sign(self):
        """EMF = -N * dPhi/dt; verify the Lenz's law negative sign."""
        rate = jnp.array(10000.0)
        emf = self.coil.induced_emf(rate)
        expected = -100 * 10000.0  # -N * rate
        assert abs(emf - expected) < 1e-6
        # Sign must be negative (Lenz)
        assert emf < 0

    def test_induced_emf_zero_rate(self):
        """Zero flux change rate produces zero EMF."""
        emf = self.coil.induced_emf(jnp.array(0.0))
        assert abs(emf) < 1e-15

    def test_motional_emf_perpendicular(self):
        """Motional EMF for v perpendicular to B: |v x B| * L * N."""
        B = jnp.array([0.0, 0.0, 1000.0])
        v = jnp.array([100.0, 0.0, 0.0])
        length = jnp.array(5.0)
        emf = self.coil.motional_emf(B, length, v)
        # |v x B| = 100 * 1000 = 1e5; emf_per = 1e5 * 5 = 5e5; total = 100 * 5e5 = 5e7
        expected = 100 * 1e5 * 5.0
        assert abs(emf - expected) < 1e-3

    def test_motional_emf_parallel(self):
        """Motional EMF is zero when v is parallel to B (cross product = 0)."""
        B = jnp.array([0.0, 0.0, 1000.0])
        v = jnp.array([0.0, 0.0, 100.0])
        emf = self.coil.motional_emf(B, jnp.array(5.0), v)
        assert abs(emf) < 1e-15

    def test_lenz_law_check_opposing(self):
        """Lenz's law holds when product of flux_change and current is negative."""
        # Positive flux change, negative induced current -> opposes change
        result = self.coil.lenz_law_check(
            jnp.array(1000.0),
            jnp.array(-5.0),
        )
        assert bool(result) is True

    def test_lenz_law_check_non_opposing(self):
        """Lenz's law fails when product is positive."""
        result = self.coil.lenz_law_check(
            jnp.array(1000.0),
            jnp.array(5.0),
        )
        assert bool(result) is False

    def test_lenz_law_check_zero(self):
        """Lenz's law check with zero product returns True (borderline)."""
        result = self.coil.lenz_law_check(
            jnp.array(0.0),
            jnp.array(5.0),
        )
        assert bool(result) is True

    def test_analyze_faraday_induction(self):
        """Complete Faraday induction analysis returns all expected keys."""
        B0 = jnp.array([0.0, 0.0, 0.0])
        B1 = jnp.array([0.0, 0.0, 1000.0])
        result = analyze_faraday_induction_jax(
            B_initial=B0,
            B_final=B1,
            loop_area=10.0,
            loop_normal=jnp.array([0.0, 0.0, 1.0]),
            time_interval=0.5,
            resistance=100.0,
            num_turns=100,
        )
        expected_keys = {
            "flux_initial",
            "flux_final",
            "flux_change",
            "total_flux_change",
            "flux_change_rate",
            "average_emf",
            "average_current",
            "charge_transferred",
        }
        assert set(result.keys()) == expected_keys
        # flux_initial should be 0
        assert abs(result["flux_initial"]) < 1e-15
        # flux_final = B * A (per turn) = 1000 * 10 = 10000
        assert abs(result["flux_final"] - 10000.0) < 1e-3
        # EMF = -N * dPhi/dt = -100 * (1e6 / 0.5) = -2e8
        assert abs(result["average_emf"] - (-2e8)) < 1e3
        # I = EMF / R = -2e8 / 100 = -2e6
        assert abs(result["average_current"] - (-2e6)) < 1e3
        # charge_transferred = -total_flux_change / R = -1e6 / 100 = -10000
        assert abs(result["charge_transferred"] - (-10000.0)) < 1e-3

    def test_jit_compatibility(self):
        """FaradayInductionJAX methods work under JIT compilation."""

        @jax.jit
        def compute_flux(B):
            coil = FaradayInductionJAX(num_turns=100, resistance=50.0)
            return coil.magnetic_flux(B, area=10.0)

        @jax.jit
        def compute_emf(rate):
            coil = FaradayInductionJAX(num_turns=100, resistance=50.0)
            return coil.induced_emf(rate)

        B = jnp.array([0.0, 0.0, 500.0])
        flux = compute_flux(B)
        assert abs(flux - 500000.0) < 1e-3

        emf = compute_emf(jnp.array(10000.0))
        assert abs(emf - (-1e6)) < 1e-3

    def test_gradient_emf_wrt_flux_rate(self):
        """d(EMF)/d(flux_change_rate) = -N."""
        N = 100
        rate = jnp.array(5000.0)
        gradient = emf_wrt_flux_rate(N, rate)
        expected = float(-N)
        assert abs(gradient - expected) < 1e-10

    def test_gradient_flux_wrt_bfield(self):
        """Grad_B Phi = N * A * n_hat."""
        N = 100
        B = jnp.array([0.0, 0.0, 500.0])
        area = 10.0
        normal = jnp.array([0.0, 0.0, 1.0])
        grad = flux_wrt_bfield(N, B, area, normal)
        expected = jnp.array([0.0, 0.0, N * area])  # [0, 0, 1000]
        assert jnp.allclose(grad, expected, atol=1e-10)

    def test_vmap_over_b_fields(self):
        """vmap over a batch of B-fields returns per-field flux values."""
        B_fields = jnp.array([
            [0.0, 0.0, 100.0],
            [0.0, 0.0, 500.0],
            [0.0, 0.0, 1000.0],
        ])
        normal = jnp.array([0.0, 0.0, 1.0])
        fluxes = flux_over_batch(self.coil, B_fields, area=10.0, normal=normal)
        assert fluxes.shape == (3,)
        expected = jnp.array([100 * 100 * 10, 100 * 500 * 10, 100 * 1000 * 10])
        assert jnp.allclose(fluxes, expected, atol=1e-3)


# ── Maxwell Equations JAX ─────────────────────────────────────────


@pytest.mark.skipif(not HAS_EQUATIONS, reason="maxwell.jax.electromagnetism.equations not installed")
class TestMaxwellEquationsJAX:
    """Test MaxwellEquationsJAX against CGS Gaussian equations (Art. 594-603)."""

    def setup_method(self):
        self.meq = MaxwellEquationsJAX()

    def test_gauss_law_electric_uniform(self):
        """Uniform D field has zero divergence."""
        x = jnp.linspace(-1.0, 1.0, 50)
        dx = float(x[1] - x[0])
        D = jnp.stack([
            jnp.full(50, 1000.0),
            jnp.zeros(50),
            jnp.zeros(50),
        ], axis=0)
        result = self.meq.gauss_law_electric(D, dx=dx)
        div_val = result["divergence"]
        max_div = float(jnp.max(jnp.abs(div_val))) if div_val.ndim > 0 else float(jnp.abs(div_val))
        assert max_div < 1e-6

    def test_gauss_law_electric_with_rho(self):
        """Non-uniform D field with known charge density."""
        x = jnp.linspace(-1.0, 1.0, 50)
        dx = float(x[1] - x[0])
        alpha = 500.0
        D0 = 1000.0
        D = jnp.stack([
            D0 + alpha * x,
            jnp.zeros(50),
            jnp.zeros(50),
        ], axis=0)
        rho_expected = alpha / (4.0 * jnp.pi)
        result = self.meq.gauss_law_electric(D, dx=dx, rho=float(rho_expected))
        assert result["expected"] is not None
        assert result["residual"] is not None
        max_res = float(jnp.max(jnp.abs(result["residual"])))
        assert max_res < 1e-3

    def test_gauss_law_magnetic_uniform(self):
        """Uniform B field has zero divergence (no monopoles)."""
        B = jnp.stack([
            jnp.full(50, 500.0),
            jnp.zeros(50),
            jnp.zeros(50),
        ], axis=0)
        result = self.meq.gauss_law_magnetic(B, dx=0.04)
        assert result["max_abs_div"] < 1e-6

    def test_gauss_law_magnetic_zero_divergence(self):
        """div B = 0 explicitly for constant B field."""
        B = jnp.stack([
            jnp.ones(50) * 100.0,
            jnp.ones(50) * 200.0,
            jnp.ones(50) * 300.0,
        ], axis=0)
        result = self.meq.gauss_law_magnetic(B, dx=0.04)
        assert result["max_abs_div"] < 1e-10

    def test_faraday_law(self):
        """curl E = -(1/c) * dB/dt."""
        from maxwell.config.constants import C

        dB_dt = jnp.array([1e10, 0.0, 0.0])
        curl_E = self.meq.equation_A_faraday(dB_dt)
        expected = -(1.0 / C) * dB_dt
        assert jnp.allclose(curl_E, expected, atol=1e-6)

    def test_faraday_law_direction(self):
        """curl E has opposite sign to dB/dt (Lenz)."""
        dB_dt = jnp.array([1e10, 0.0, 0.0])
        curl_E = self.meq.equation_A_faraday(dB_dt)
        # Since c > 0, the sign of curl_E should be opposite to dB/dt
        assert curl_E[0] * dB_dt[0] < 0

    def test_ampere_maxwell_law(self):
        """Ampere-Maxwell: curl H = (4*pi/c)*J + (1/c)*dD/dt."""
        J = jnp.array([1.0, 0.0, 0.0])
        dD_dt = jnp.array([0.0, 1e5, 0.0])
        result = self.meq.equation_B_ampere(J, dD_dt=dD_dt)
        assert "curl_H" in result
        assert "conduction_term" in result
        assert "displacement_term" in result
        # Verify the terms independently
        from maxwell.config.constants import C

        expected_cond = (4.0 * jnp.pi / C) * J
        expected_disp = (1.0 / C) * dD_dt
        assert jnp.allclose(result["conduction_term"], expected_cond, atol=1e-6)
        assert jnp.allclose(result["displacement_term"], expected_disp, atol=1e-6)

    def test_ampere_maxwell_no_displacement(self):
        """Ampere-Maxwell with no displacement current (dD/dt = 0)."""
        J = jnp.array([1.0, 0.0, 0.0])
        result = self.meq.equation_B_ampere(J)
        assert jnp.allclose(result["displacement_term"], jnp.zeros(3), atol=1e-15)

    def test_verify_no_monopoles(self):
        """verify_no_monopoles passes for a uniform B field."""
        B = jnp.stack([
            jnp.full(50, 500.0),
            jnp.zeros(50),
            jnp.zeros(50),
        ], axis=0)
        result = self.meq.verify_no_monopoles(B, dx=0.04, atol=1e-6)
        assert bool(result["passed"]) is True
        assert result["max_abs_div"] < 1e-6

    def test_verify_maxwell_equations_jax(self):
        """verify_maxwell_equations_jax returns all_verified=True."""
        report = verify_maxwell_equations_jax(atol=1e-6)
        assert report["all_verified"] is True
        assert "gauss_electric_uniform" in report
        assert "gauss_electric_nonuniform" in report
        assert "gauss_magnetic_uniform" in report
        assert "faraday_law" in report
        assert "ampere_maxwell" in report

    def test_jit_compatibility(self):
        """MaxwellEquationsJAX methods work under JIT."""

        @jax.jit
        def faraday_jit(dB_dt):
            meq = MaxwellEquationsJAX()
            return meq.equation_A_faraday(dB_dt)

        dB_dt = jnp.array([1e10, 0.0, 0.0])
        curl_E = faraday_jit(dB_dt)
        assert curl_E.shape == (3,)
        assert curl_E[0] < 0


# ── Spherical Harmonics JAX ───────────────────────────────────────


@pytest.mark.skipif(not HAS_SPH_HARM, reason="maxwell.jax.math.spherical_harmonics not installed")
class TestSphericalHarmonicsJAX:
    """Test spherical harmonics and Legendre polynomials (Art. 128-146)."""

    def test_legendre_p0(self):
        """P_0(x) = 1 for all x."""
        x = jnp.linspace(-1.0, 1.0, 100)
        result = legendre_batched(0, x)
        assert jnp.allclose(result, jnp.ones_like(x), atol=1e-10)

    def test_legendre_p1(self):
        """P_1(x) = x."""
        x = jnp.linspace(-1.0, 1.0, 100)
        result = legendre_batched(1, x)
        assert jnp.allclose(result, x, atol=1e-10)

    def test_legendre_p2(self):
        """P_2(x) = (3x^2 - 1) / 2."""
        x = jnp.array([0.5, 0.0, -0.5, 1.0, -1.0])
        result = legendre_batched(2, x)
        expected = (3.0 * x ** 2 - 1.0) / 2.0
        assert jnp.allclose(result, expected, atol=1e-10)

    def test_legendre_p3(self):
        """P_3(x) = (5x^3 - 3x) / 2."""
        x = jnp.array([0.3, 0.7, -0.2, 1.0])
        result = legendre_batched(3, x)
        expected = (5.0 * x ** 3 - 3.0 * x) / 2.0
        assert jnp.allclose(result, expected, atol=1e-10)

    def test_legendre_p4(self):
        """P_4(x) = (35x^4 - 30x^2 + 3) / 8."""
        x = jnp.array([0.25, 0.5, 0.75, 1.0])
        result = legendre_batched(4, x)
        expected = (35.0 * x ** 4 - 30.0 * x ** 2 + 3.0) / 8.0
        assert jnp.allclose(result, expected, atol=1e-10)

    def test_addition_theorem_agreement(self):
        """Addition theorem P_l(cos gamma) matches direct Legendre evaluation."""
        l = 3
        theta1 = jnp.array(0.5)
        phi1 = jnp.array(0.3)
        theta2 = jnp.array(1.2)
        phi2 = jnp.array(2.1)
        P_add, P_direct = addition_theorem_jax(l, theta1, phi1, theta2, phi2)
        assert jnp.allclose(P_add, P_direct, atol=1e-8)

    def test_addition_theorem_l0(self):
        """Addition theorem for l=0 gives P_0=1 everywhere."""
        theta1 = jnp.array(0.5)
        phi1 = jnp.array(0.0)
        theta2 = jnp.array(1.0)
        phi2 = jnp.array(0.0)
        P_add, P_direct = addition_theorem_jax(0, theta1, phi1, theta2, phi2)
        assert abs(float(P_add) - 1.0) < 1e-8
        assert abs(float(P_direct) - 1.0) < 1e-8

    def test_addition_theorem_l1(self):
        """Addition theorem for l=1."""
        theta1 = jnp.array(0.8)
        phi1 = jnp.array(0.4)
        theta2 = jnp.array(1.1)
        phi2 = jnp.array(1.7)
        P_add, P_direct = addition_theorem_jax(1, theta1, phi1, theta2, phi2)
        # cos(gamma) = cos(t1)*cos(t2) + sin(t1)*sin(t2)*cos(p1-p2)
        cos_gamma = (jnp.cos(theta1) * jnp.cos(theta2)
                     + jnp.sin(theta1) * jnp.sin(theta2) * jnp.cos(phi1 - phi2))
        expected = cos_gamma  # P_1 = x
        assert abs(float(P_direct) - float(expected)) < 1e-8
        assert abs(float(P_add) - float(expected)) < 1e-6

    def test_reconstruct_cos_theta(self):
        """Expansion of cos(theta) should be exact with l_max >= 1."""
        expansion = SphericalHarmonicExpansionJAX(max_l=4)
        theta_grid = jnp.linspace(0.01, jnp.pi - 0.01, 200)
        expansion.compute_coefficients(lambda th: jnp.cos(th), theta_grid)
        recon = expansion.reconstruct(theta_grid, jnp.zeros_like(theta_grid))
        exact = jnp.cos(theta_grid)
        assert jnp.allclose(recon, exact, atol=2e-2)

    def test_reconstruct_constant(self):
        """Expansion of f(theta)=1 should be exact with l_max >= 0."""
        expansion = SphericalHarmonicExpansionJAX(max_l=2)
        theta_grid = jnp.linspace(0.01, jnp.pi - 0.01, 200)
        expansion.compute_coefficients(lambda th: jnp.ones_like(th), theta_grid)
        recon = expansion.reconstruct(theta_grid, jnp.zeros_like(theta_grid))
        assert jnp.allclose(recon, jnp.ones_like(theta_grid), atol=2e-2)

    def test_reconstruct_cos_sq(self):
        """Expansion of cos^2(theta) should converge with l_max >= 2."""
        expansion = SphericalHarmonicExpansionJAX(max_l=4)
        theta_grid = jnp.linspace(0.01, jnp.pi - 0.01, 200)
        expansion.compute_coefficients(lambda th: jnp.cos(th) ** 2, theta_grid)
        recon = expansion.reconstruct(theta_grid, jnp.zeros_like(theta_grid))
        exact = jnp.cos(theta_grid) ** 2
        assert jnp.allclose(recon, exact, atol=2e-2)

    def test_convergence_analysis_decreasing(self):
        """Convergence analysis returns decreasing errors as l_max increases."""
        expansion = SphericalHarmonicExpansionJAX(max_l=8)
        theta_grid = jnp.linspace(0.01, jnp.pi - 0.01, 200)
        expansion.compute_coefficients(lambda th: jnp.cos(th), theta_grid)
        errors = expansion.convergence_analysis(
            lambda th: jnp.cos(th), theta_grid
        )
        assert errors.shape == (9,)  # l_max + 1 = 9
        # Errors should generally decrease
        assert errors[-1] < errors[0]

    def test_jit_reconstruction(self):
        """Reconstruction is JIT-compatible."""
        expansion = SphericalHarmonicExpansionJAX(max_l=2)
        theta_grid = jnp.linspace(0.01, jnp.pi - 0.01, 100)
        expansion.compute_coefficients(lambda th: jnp.cos(th), theta_grid)

        @jax.jit
        def jit_reconstruct(theta, phi):
            return expansion.reconstruct(theta, phi)

        theta_test = jnp.array([0.5, 1.0, 1.5])
        phi_test = jnp.zeros(3)
        recon = jit_reconstruct(theta_test, phi_test)
        exact = jnp.cos(theta_test)
        assert jnp.allclose(recon, exact, atol=2e-2)

    def test_coefficients_zeros_initially(self):
        """Fresh expansion has zero coefficients."""
        expansion = SphericalHarmonicExpansionJAX(max_l=3)
        assert expansion.coefficients.shape == (4, 7)
        assert jnp.allclose(expansion.coefficients, 0.0, atol=1e-15)
