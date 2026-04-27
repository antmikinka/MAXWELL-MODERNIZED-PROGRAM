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

try:
    from maxwell.jax.electromagnetism.forces import (
        LorentzForceJAX,
        MaxwellStressTensorJAX,
        force_on_wire_jax,
        force_on_charge_jax,
        torque_on_loop_jax,
        force_density_jax,
        parallel_current_force_jax,
        stress_tensor_jax,
        electromagnetic_pressure_jax,
        surface_force_jax,
    )

    HAS_FORCES = True
except ImportError:
    HAS_FORCES = False

try:
    from maxwell.jax.electromagnetism.ampere_maxwell import (
        DisplacementCurrentJAX,
        AmpereMaxwellLawJAX,
        displacement_current_jax,
        total_current_jax,
        curl_H_jax,
        magnetic_field_from_current_jax,
        capacitor_paradox_jax,
    )

    HAS_AMPERE = True
except ImportError:
    HAS_AMPERE = False


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
        emf = self.coil.motional_emf(v, B, length)
        # |v x B| = 100 * 1000 = 1e5; emf_per = 1e5 * 5 = 5e5; total = 100 * 5e5 = 5e7
        expected = 100 * 1e5 * 5.0
        assert abs(emf - expected) < 1e-3

    def test_motional_emf_parallel(self):
        """Motional EMF is zero when v is parallel to B (cross product = 0)."""
        B = jnp.array([0.0, 0.0, 1000.0])
        v = jnp.array([0.0, 0.0, 100.0])
        emf = self.coil.motional_emf(v, B, jnp.array(5.0))
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
            "num_turns",
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


# ── Lorentz Force JAX ───────────────────────────────────────────────


@pytest.mark.skipif(not HAS_FORCES, reason="maxwell.jax.electromagnetism.forces not installed")
class TestLorentzForceJAX:
    """Test LorentzForceJAX against Maxwell's theory (Arts. 490-492)."""

    def test_force_on_wire_basic(self):
        """F = I * (L x B) for wire along x, B along z."""
        force = LorentzForceJAX(
            current=1.0,
            length=jnp.array([10.0, 0.0, 0.0]),
            B_field=jnp.array([0.0, 0.0, 1000.0]),
        )
        F = force.force_vector
        # L x B = (10,0,0) x (0,0,1000) = (0, -10000, 0)
        expected = jnp.array([0.0, -10000.0, 0.0])
        assert jnp.allclose(F, expected, atol=1e-10)

    def test_force_magnitude(self):
        """Magnitude |F| = I * |L| * |B| * sin(theta)."""
        force = LorentzForceJAX(
            current=1.0,
            length=jnp.array([5.0, 0.0, 0.0]),
            B_field=jnp.array([0.0, 0.0, 2000.0]),
        )
        assert abs(force.magnitude - 10000.0) < 1e-10

    def test_force_direction(self):
        """Force direction is unit vector."""
        force = LorentzForceJAX(
            current=1.0,
            length=jnp.array([3.0, 4.0, 0.0]),
            B_field=jnp.array([0.0, 0.0, 100.0]),
        )
        direction = force.direction
        mag = jnp.linalg.norm(direction)
        assert abs(mag - 1.0) < 1e-10

    def test_force_on_charge(self):
        """F = q * (v x B) for a moving charge."""
        F = force_on_charge_jax(
            charge=1.0,
            velocity=jnp.array([1e8, 0.0, 0.0]),
            B_field=jnp.array([0.0, 0.0, 100.0]),
        )
        # v x B = (1e8,0,0) x (0,0,100) = (0, -1e10, 0)
        expected = jnp.array([0.0, -1e10, 0.0])
        assert jnp.allclose(F, expected, atol=1e-6)

    def test_force_on_charge_zero_velocity(self):
        """Stationary charge experiences no magnetic force."""
        F = force_on_charge_jax(
            charge=1.0,
            velocity=jnp.zeros(3),
            B_field=jnp.array([0.0, 0.0, 100.0]),
        )
        assert jnp.allclose(F, jnp.zeros(3), atol=1e-15)

    def test_torque_on_loop(self):
        """tau = m x B for a current loop."""
        tau = torque_on_loop_jax(
            magnetic_moment=jnp.array([0.0, 0.0, 500.0]),
            B_field=jnp.array([100.0, 0.0, 0.0]),
        )
        # m x B = (0,0,500) x (100,0,0) = (0, 50000, 0)
        expected = jnp.array([0.0, 50000.0, 0.0])
        assert jnp.allclose(tau, expected, atol=1e-10)

    def test_force_density(self):
        """f = J x B for current density in magnetic field."""
        f = force_density_jax(
            J=jnp.array([1.0, 0.0, 0.0]),
            B=jnp.array([0.0, 0.0, 100.0]),
        )
        expected = jnp.array([0.0, -100.0, 0.0])
        assert jnp.allclose(f, expected, atol=1e-10)

    def test_parallel_current_force(self):
        """F = 2 * I1 * I2 * L / r for parallel wires."""
        F = parallel_current_force_jax(
            I1=1.0, I2=1.0, separation=1.0, wire_length=10.0,
        )
        expected = 2.0 * 1.0 * 1.0 * 10.0 / 1.0  # = 20
        assert abs(F - expected) < 1e-10

    def test_parallel_current_opposite_direction(self):
        """Opposite currents give repulsive (negative) force."""
        F = parallel_current_force_jax(
            I1=1.0, I2=-1.0, separation=1.0, wire_length=10.0,
        )
        assert F < 0  # Repulsive

    def test_standalone_force_on_wire(self):
        """Standalone force_on_wire_jax function."""
        F = force_on_wire_jax(
            current=2.0,
            length=jnp.array([0.0, 5.0, 0.0]),
            B_field=jnp.array([0.0, 0.0, 500.0]),
        )
        # L x B = (0,5,0) x (0,0,500) = (2500, 0, 0), F = 2 * 2500 = 5000
        expected = jnp.array([5000.0, 0.0, 0.0])
        assert jnp.allclose(F, expected, atol=1e-10)

    def test_jit_force_on_wire(self):
        """Force on wire works under JIT."""

        @jax.jit
        def jit_force(current, length, B):
            return force_on_wire_jax(current, length, B)

        F = jit_force(1.0, jnp.array([1.0, 0.0, 0.0]), jnp.array([0.0, 1.0, 0.0]))
        assert F.shape == (3,)

    def test_vmap_force_on_charge(self):
        """vmap over multiple charges."""

        def single_force(velocity):
            return force_on_charge_jax(1.0, velocity, jnp.array([0.0, 0.0, 100.0]))

        velocities = jnp.array([
            [1e6, 0.0, 0.0],
            [0.0, 1e6, 0.0],
            [0.0, 0.0, 1e6],
        ])
        forces = jax.vmap(single_force)(velocities)
        assert forces.shape == (3, 3)
        # Third velocity is parallel to B, so force should be zero
        assert jnp.allclose(forces[2], jnp.zeros(3), atol=1e-10)

    def test_grad_force_wrt_current(self):
        """dF/dI = L x B."""
        def force_mag(current):
            return force_on_wire_jax(
                current, jnp.array([1.0, 0.0, 0.0]), jnp.array([0.0, 0.0, 100.0])
            )[1]

        g = jax.grad(force_mag)(1.0)
        # dF_y/dI = -(L_x * B_z) = -100
        assert abs(g - (-100.0)) < 1e-10


# ── Maxwell Stress Tensor JAX ─────────────────────────────────────────


@pytest.mark.skipif(not HAS_FORCES, reason="maxwell.jax.electromagnetism.forces not installed")
class TestMaxwellStressTensorJAX:
    """Test MaxwellStressTensorJAX (Arts. 641-646)."""

    def test_stress_tensor_electric_only(self):
        """T_ij for pure electric field along z."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.array([0.0, 0.0, 100.0]),
            H_field=jnp.zeros(3),
        )
        T = tensor.stress_tensor()
        assert T.shape == (3, 3)
        # T_22 should be positive (tension along field lines)
        # T_zz = (Ez^2)/(4pi) - (Ez^2)/(8pi) = Ez^2/(8pi)
        expected_Tzz = 100.0**2 / (8.0 * jnp.pi)
        assert abs(T[2, 2] - expected_Tzz) < 1e-10

    def test_stress_tensor_magnetic_only(self):
        """T_ij for pure magnetic field along z."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.zeros(3),
            H_field=jnp.array([0.0, 0.0, 50.0]),
        )
        T = tensor.stress_tensor()
        expected_Tzz = 50.0**2 / (8.0 * jnp.pi)
        assert abs(T[2, 2] - expected_Tzz) < 1e-10

    def test_electromagnetic_pressure(self):
        """P = (1/8pi)(E^2 + H^2)."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.array([100.0, 0.0, 0.0]),
            H_field=jnp.array([0.0, 50.0, 0.0]),
        )
        P = tensor.electromagnetic_pressure
        expected = (100.0**2 + 50.0**2) / (8.0 * jnp.pi)
        assert abs(P - expected) < 1e-10

    def test_stress_tensor_symmetry(self):
        """T_ij = T_ji (stress tensor is symmetric)."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.array([1.0, 2.0, 3.0]),
            H_field=jnp.array([4.0, 5.0, 6.0]),
        )
        T = tensor.stress_tensor()
        assert abs(T[0, 1] - T[1, 0]) < 1e-15
        assert abs(T[0, 2] - T[2, 0]) < 1e-15
        assert abs(T[1, 2] - T[2, 1]) < 1e-15

    def test_stress_tensor_trace(self):
        """Tr(T) = -(1/4pi)(E^2 + H^2)."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.array([3.0, 0.0, 4.0]),
            H_field=jnp.array([0.0, 5.0, 0.0]),
        )
        T = tensor.stress_tensor()
        trace = T[0, 0] + T[1, 1] + T[2, 2]
        E_sq = 3.0**2 + 4.0**2  # = 25
        H_sq = 5.0**2  # = 25
        # Trace = (E^2+H^2)/(4pi) - 3*(E^2+H^2)/(8pi) = -(E^2+H^2)/(8pi)
        expected_trace = -(E_sq + H_sq) / (8.0 * jnp.pi)
        assert abs(trace - expected_trace) < 1e-10

    def test_surface_force(self):
        """F = T . n * A for a surface."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.array([0.0, 0.0, 100.0]),
            H_field=jnp.zeros(3),
        )
        normal = jnp.array([0.0, 0.0, 1.0])
        F = tensor.surface_force(normal, area=1.0)
        assert F.shape == (3,)
        # Force along z direction (field line tension)
        assert F[2] > 0

    def test_zero_fields_zero_tensor(self):
        """Zero fields produce zero stress tensor."""
        tensor = MaxwellStressTensorJAX(
            E_field=jnp.zeros(3),
            H_field=jnp.zeros(3),
        )
        T = tensor.stress_tensor()
        assert jnp.allclose(T, jnp.zeros((3, 3)), atol=1e-15)
        assert tensor.electromagnetic_pressure == 0.0

    def test_standalone_stress_tensor(self):
        """Standalone stress_tensor_jax function."""
        T = stress_tensor_jax(
            E_field=jnp.array([10.0, 0.0, 0.0]),
            H_field=jnp.array([0.0, 10.0, 0.0]),
        )
        assert T.shape == (3, 3)

    def test_standalone_electromagnetic_pressure(self):
        """Standalone electromagnetic_pressure_jax function."""
        P = electromagnetic_pressure_jax(
            E_field=jnp.array([100.0, 0.0, 0.0]),
            H_field=jnp.zeros(3),
        )
        expected = 100.0**2 / (8.0 * jnp.pi)
        assert abs(P - expected) < 1e-10

    def test_standalone_surface_force(self):
        """Standalone surface_force_jax function."""
        F = surface_force_jax(
            E_field=jnp.array([0.0, 0.0, 100.0]),
            H_field=jnp.zeros(3),
            normal=jnp.array([0.0, 0.0, 1.0]),
            area=1.0,
        )
        assert F.shape == (3,)

    def test_jit_stress_tensor(self):
        """Stress tensor works under JIT."""

        @jax.jit
        def jit_stress(E, H):
            return stress_tensor_jax(E, H)

        T = jit_stress(jnp.array([1.0, 0.0, 0.0]), jnp.array([0.0, 1.0, 0.0]))
        assert T.shape == (3, 3)

    def test_jit_electromagnetic_pressure(self):
        """Electromagnetic pressure works under JIT."""

        @jax.jit
        def jit_pressure(E, H):
            return electromagnetic_pressure_jax(E, H)

        P = jit_pressure(jnp.array([100.0, 0.0, 0.0]), jnp.zeros(3))
        assert P > 0

    def test_grad_pressure_wrt_field(self):
        """dP/dE = E/(4pi) for electromagnetic pressure."""

        def pressure_from_E(Ex):
            E = jnp.array([Ex, 0.0, 0.0])
            return electromagnetic_pressure_jax(E, jnp.zeros(3))

        g = jax.grad(pressure_from_E)(100.0)
        expected = 100.0 / (4.0 * jnp.pi)
        assert abs(g - expected) < 1e-10


# ── Ampere-Maxwell JAX ──────────────────────────────────────────────


@pytest.mark.skipif(not HAS_AMPERE, reason="maxwell.jax.electromagnetism.ampere_maxwell not installed")
class TestDisplacementCurrentJAX:
    """Test DisplacementCurrentJAX (Arts. 606-607)."""

    def test_D_field(self):
        """D = epsilon * E."""
        dc = DisplacementCurrentJAX(
            E_field=jnp.array([100.0, 0.0, 0.0]),
            dE_dt=jnp.array([1e10, 0.0, 0.0]),
            permittivity=2.0,
        )
        D = dc.D_field
        assert jnp.allclose(D, jnp.array([200.0, 0.0, 0.0]), atol=1e-10)

    def test_dD_dt(self):
        """dD/dt = epsilon * dE/dt."""
        dc = DisplacementCurrentJAX(
            E_field=jnp.zeros(3),
            dE_dt=jnp.array([1e10, 0.0, 0.0]),
            permittivity=2.0,
        )
        dD = dc.dD_dt
        assert jnp.allclose(dD, jnp.array([2e10, 0.0, 0.0]), atol=1e-10)

    def test_J_displacement(self):
        """J_d = (1/4pi) * dD/dt."""
        dc = DisplacementCurrentJAX(
            E_field=jnp.zeros(3),
            dE_dt=jnp.array([4.0 * jnp.pi * 1e6, 0.0, 0.0]),
            permittivity=1.0,
        )
        J_d = dc.J_displacement
        # J_d = (1/4pi) * 4pi * 1e6 = 1e6
        assert jnp.allclose(J_d, jnp.array([1e6, 0.0, 0.0]), atol=1e-6)

    def test_magnitude(self):
        """|J_d| returns scalar magnitude."""
        dc = DisplacementCurrentJAX(
            E_field=jnp.zeros(3),
            dE_dt=jnp.array([0.0, 4.0 * jnp.pi * 1e6, 0.0]),
            permittivity=1.0,
        )
        mag = dc.magnitude
        assert abs(mag - 1e6) < 1e-6

    def test_jit_compatible(self):
        """DisplacementCurrentJAX works under JIT."""

        @jax.jit
        def jit_J_disp(dE_dt):
            dc = DisplacementCurrentJAX(dE_dt=dE_dt)
            return dc.J_displacement

        J = jit_J_disp(jnp.array([1e10, 0.0, 0.0]))
        expected = jnp.array([1e10 / (4.0 * jnp.pi), 0.0, 0.0])
        assert jnp.allclose(J, expected, atol=1e-6)


@pytest.mark.skipif(not HAS_AMPERE, reason="maxwell.jax.electromagnetism.ampere_maxwell not installed")
class TestAmpereMaxwellLawJAX:
    """Test AmpereMaxwellLawJAX (Arts. 606-607)."""

    def test_J_displacement(self):
        """J_d = (epsilon/4pi) * dE/dt."""
        aml = AmpereMaxwellLawJAX(
            J_conduction=jnp.zeros(3),
            dE_dt=jnp.array([4.0 * jnp.pi * 1e6, 0.0, 0.0]),
            permittivity=1.0,
        )
        J_d = aml.J_displacement
        assert jnp.allclose(J_d, jnp.array([1e6, 0.0, 0.0]), atol=1e-6)

    def test_J_total(self):
        """J_total = J_cond + J_disp."""
        aml = AmpereMaxwellLawJAX(
            J_conduction=jnp.array([2e6, 0.0, 0.0]),
            dE_dt=jnp.array([4.0 * jnp.pi * 1e6, 0.0, 0.0]),
            permittivity=1.0,
        )
        J_total = aml.J_total
        # J_cond = 2e6, J_disp = 1e6 => total = 3e6
        assert jnp.allclose(J_total, jnp.array([3e6, 0.0, 0.0]), atol=1e-6)

    def test_curl_H(self):
        """curl(H) = 4pi * J_total."""
        aml = AmpereMaxwellLawJAX(
            J_conduction=jnp.array([1.0, 0.0, 0.0]),
            dE_dt=jnp.zeros(3),
            permittivity=1.0,
        )
        curl_H = aml.curl_H
        expected = 4.0 * jnp.pi * jnp.array([1.0, 0.0, 0.0])
        assert jnp.allclose(curl_H, expected, atol=1e-10)

    def test_compute_curl_H_override(self):
        """compute_curl_H with override parameters."""
        aml = AmpereMaxwellLawJAX(
            J_conduction=jnp.array([1.0, 0.0, 0.0]),
            dE_dt=jnp.zeros(3),
        )
        curl = aml.compute_curl_H(
            J_conduction=jnp.array([0.0, 2.0, 0.0]),
            dE_dt=jnp.zeros(3),
        )
        expected = 4.0 * jnp.pi * jnp.array([0.0, 2.0, 0.0])
        assert jnp.allclose(curl, expected, atol=1e-10)

    def test_pure_displacement_current(self):
        """No conduction current: only displacement contributes."""
        aml = AmpereMaxwellLawJAX(
            J_conduction=jnp.zeros(3),
            dE_dt=jnp.array([1e10, 0.0, 0.0]),
        )
        curl_H = aml.curl_H
        expected = jnp.array([1e10, 0.0, 0.0])  # (epsilon/4pi)*4pi = 1
        assert jnp.allclose(curl_H, expected, atol=1e-6)

    def test_jit_compatible(self):
        """AmpereMaxwellLawJAX works under JIT."""

        @jax.jit
        def jit_curl_H(J_c, dE):
            aml = AmpereMaxwellLawJAX(J_conduction=J_c, dE_dt=dE)
            return aml.curl_H

        curl = jit_curl_H(jnp.array([1.0, 0.0, 0.0]), jnp.zeros(3))
        assert curl.shape == (3,)


@pytest.mark.skipif(not HAS_AMPERE, reason="maxwell.jax.electromagnetism.ampere_maxwell not installed")
class TestAmpereStandaloneJAX:
    """Test standalone Ampere-Maxwell JAX functions."""

    def test_displacement_current_jax(self):
        """J_d = (epsilon/4pi) * dE/dt."""
        J_d = displacement_current_jax(
            dE_dt=jnp.array([4.0 * jnp.pi * 1e8, 0.0, 0.0]),
            permittivity=1.0,
        )
        assert jnp.allclose(J_d, jnp.array([1e8, 0.0, 0.0]), atol=1e-6)

    def test_total_current_jax(self):
        """J_total = J_cond + J_disp."""
        J_total = total_current_jax(
            J_conduction=jnp.array([1e6, 0.0, 0.0]),
            dE_dt=jnp.array([4.0 * jnp.pi * 1e6, 0.0, 0.0]),
        )
        assert jnp.allclose(J_total, jnp.array([2e6, 0.0, 0.0]), atol=1e-6)

    def test_curl_H_jax(self):
        """curl(H) = 4pi * J_total."""
        curl = curl_H_jax(
            J_conduction=jnp.array([1.0, 0.0, 0.0]),
            dE_dt=jnp.zeros(3),
        )
        expected = 4.0 * jnp.pi * jnp.array([1.0, 0.0, 0.0])
        assert jnp.allclose(curl, expected, atol=1e-10)

    def test_magnetic_field_from_current_jax(self):
        """dH = (1/4pi) * (Idl x r) / r^3."""
        Idl = jnp.array([0.0, 0.0, 1.0])  # Current element along z
        r = jnp.array([1.0, 0.0, 0.0])  # Position along x
        H = magnetic_field_from_current_jax(Idl, r)
        # Idl x r = (0,0,1) x (1,0,0) = (0, 1, 0)
        # dH = (1/4pi) * (0, 1, 0) / 1 = (0, 1/(4pi), 0)
        expected = jnp.array([0.0, 1.0 / (4.0 * jnp.pi), 0.0])
        assert jnp.allclose(H, expected, atol=1e-10)

    def test_magnetic_field_zero_distance(self):
        """Zero distance gives zero field (safe norm)."""
        H = magnetic_field_from_current_jax(
            jnp.array([0.0, 0.0, 1.0]),
            jnp.zeros(3),
        )
        assert jnp.allclose(H, jnp.zeros(3), atol=1e-15)

    def test_capacitor_paradox_jax(self):
        """Displacement current equals conduction current for capacitor."""
        result = capacitor_paradox_jax(
            charging_current=1.0,
            plate_area=100.0,
        )
        assert jnp.isclose(result["displacement_current"], 1.0, atol=1e-10)
        assert bool(result["paradox_resolved"]) is True

    def test_jit_displacement_current(self):
        """Displacement current works under JIT."""

        @jax.jit
        def jit_J(dE):
            return displacement_current_jax(dE)

        J = jit_J(jnp.array([1e10, 0.0, 0.0]))
        assert J.shape == (3,)

    def test_grad_J_disp_wrt_dE_dt(self):
        """dJ_d/d(dE/dt) = epsilon/(4pi)."""

        def J_disp_from_dE(dE_x):
            return displacement_current_jax(jnp.array([dE_x, 0.0, 0.0]))[0]

        g = jax.grad(J_disp_from_dE)(1e10)
        expected = 1.0 / (4.0 * jnp.pi)
        assert abs(g - expected) < 1e-10

    def test_vmap_over_dE_dt(self):
        """vmap over multiple dE/dt values."""
        dE_dt_batch = jnp.array([
            [1e10, 0.0, 0.0],
            [0.0, 2e10, 0.0],
            [0.0, 0.0, 3e10],
        ])
        J_d_batch = jax.vmap(displacement_current_jax)(dE_dt_batch)
        assert J_d_batch.shape == (3, 3)


# ── Imports for ElectricFieldJAX ────────────────────────────────────

try:
    from maxwell.jax.electromagnetism.field import (
        ElectricFieldJAX,
        electric_flux_jax,
        electric_tension_jax,
        electromotive_force_jax,
        field_from_potential_jax,
        gauss_law_closed_surface_jax,
        superposition_field_jax,
    )

    HAS_EFIELD = True
except ImportError:
    HAS_EFIELD = False


# ── Electric Field JAX ──────────────────────────────────────────────


@pytest.mark.skipif(not HAS_EFIELD, reason="maxwell.jax.electromagnetism.field not installed")
class TestElectricFieldJAX:
    """Test ElectricFieldJAX against Maxwell's theory (Arts. 44-49, 68-76)."""

    def test_magnitude(self):
        """|E| = sqrt(Ex^2 + Ey^2 + Ez^2)."""
        E = ElectricFieldJAX(
            value=jnp.array([3.0, 0.0, 4.0]),
            position=jnp.array([1.0, 0.0, 0.0]),
        )
        assert abs(E.magnitude - 5.0) < 1e-15

    def test_magnitude_zero(self):
        """Zero field has zero magnitude."""
        E = ElectricFieldJAX(
            value=jnp.zeros(3),
            position=jnp.zeros(3),
        )
        assert E.magnitude == 0.0

    def test_direction_unit_vector(self):
        """Direction is a unit vector."""
        E = ElectricFieldJAX(
            value=jnp.array([3.0, 0.0, 4.0]),
            position=jnp.array([1.0, 0.0, 0.0]),
        )
        d = E.direction
        mag = jnp.linalg.norm(d)
        assert abs(mag - 1.0) < 1e-15

    def test_direction_zero_field(self):
        """Zero field returns zero direction (safe)."""
        E = ElectricFieldJAX(
            value=jnp.zeros(3),
            position=jnp.zeros(3),
        )
        d = E.direction
        assert jnp.allclose(d, jnp.zeros(3), atol=1e-15)

    def test_from_point_charge(self):
        """E from a point charge matches Coulomb's law."""
        charge = PointChargeJAX(q=1.0, position=jnp.zeros(3))
        point = jnp.array([5.0, 0.0, 0.0])
        E = ElectricFieldJAX.from_point_charge(charge, point)
        # E = q/r^2 = 1/25 = 0.04 along x
        expected_E = jnp.array([0.04, 0.0, 0.0])
        assert jnp.allclose(E.value, expected_E, atol=1e-15)
        assert jnp.allclose(E.position, point)

    def test_superposition_two_charges(self):
        """Superposition of two charges: E_total = E1 + E2."""
        q1 = PointChargeJAX(q=1.0, position=jnp.array([-1.0, 0.0, 0.0]))
        q2 = PointChargeJAX(q=1.0, position=jnp.array([1.0, 0.0, 0.0]))
        point = jnp.array([0.0, 0.0, 0.0])
        E = ElectricFieldJAX.superposition([q1, q2], point)
        # By symmetry, the x-components cancel: E1 = (1,0,0), E2 = (-1,0,0)
        # Actually at origin: E1 from q1 at (-1,0,0): r = (1,0,0), E = 1/1^2 * (1,0,0) = (1,0,0)
        # E2 from q2 at (1,0,0): r = (-1,0,0), E = 1/1^2 * (-1,0,0) = (-1,0,0)
        # Total: (0, 0, 0)
        assert jnp.allclose(E.value, jnp.zeros(3), atol=1e-15)

    def test_superposition_asymmetric(self):
        """Superposition with asymmetric charges."""
        q1 = PointChargeJAX(q=2.0, position=jnp.array([-1.0, 0.0, 0.0]))
        q2 = PointChargeJAX(q=1.0, position=jnp.array([2.0, 0.0, 0.0]))
        point = jnp.array([0.0, 0.0, 0.0])
        E = ElectricFieldJAX.superposition([q1, q2], point)
        # E1: r = (1,0,0), r^2=1, E1 = 2*(1,0,0)/1 = (2,0,0)
        # E2: r = (-2,0,0), r^2=4, E2 = 1*(-1,0,0)/4 = (-0.25,0,0)
        expected = jnp.array([2.0 - 0.25, 0.0, 0.0])
        assert jnp.allclose(E.value, expected, atol=1e-15)

    def test_intensity(self):
        """intensity() returns the magnitude."""
        E = ElectricFieldJAX(
            value=jnp.array([0.0, 100.0, 0.0]),
            position=jnp.zeros(3),
        )
        assert abs(E.intensity() - 100.0) < 1e-15

    def test_electromotive_force_uniform(self):
        """EMF = E . (end - start) for uniform field."""
        E = ElectricFieldJAX(
            value=jnp.array([10.0, 0.0, 0.0]),
            position=jnp.array([0.0, 0.0, 0.0]),
        )
        emf = E.electromotive_force(
            path_end=jnp.array([5.0, 0.0, 0.0]),
            num_steps=100,
        )
        # EMF = 10 * 5 = 50
        assert abs(emf - 50.0) < 1e-10

    def test_electromotive_force_perpendicular(self):
        """EMF = 0 when displacement is perpendicular to field."""
        E = ElectricFieldJAX(
            value=jnp.array([0.0, 0.0, 100.0]),
            position=jnp.array([0.0, 0.0, 0.0]),
        )
        emf = E.electromotive_force(
            path_end=jnp.array([5.0, 0.0, 0.0]),
            num_steps=100,
        )
        assert abs(emf) < 1e-10

    def test_field_at_batched(self):
        """Batched evaluation broadcasts uniform field."""
        E = ElectricFieldJAX(
            value=jnp.array([1.0, 2.0, 3.0]),
            position=jnp.zeros(3),
        )
        positions = jnp.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        fields = E.field_at_batched(positions)
        assert fields.shape == (3, 3)
        assert jnp.allclose(fields[0], jnp.array([1.0, 2.0, 3.0]))
        assert jnp.allclose(fields[1], jnp.array([1.0, 2.0, 3.0]))
        assert jnp.allclose(fields[2], jnp.array([1.0, 2.0, 3.0]))

    def test_pytree_flatten(self):
        """ElectricFieldJAX can be flattened and unflattened."""
        E = ElectricFieldJAX(
            value=jnp.array([1.0, 2.0, 3.0]),
            position=jnp.array([0.0, 0.0, 0.0]),
        )
        leaves, treedef = jax.tree_util.tree_flatten(E)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(restored.value, E.value)
        assert jnp.allclose(restored.position, E.position)

    def test_jit_field_properties(self):
        """Field magnitude and direction work under JIT."""

        @jax.jit
        def jit_magnitude(value):
            E = ElectricFieldJAX(value=value, position=jnp.zeros(3))
            return E.magnitude

        mag = jit_magnitude(jnp.array([3.0, 0.0, 4.0]))
        assert abs(mag - 5.0) < 1e-15

    def test_grad_magnitude_wrt_field(self):
        """d|E|/dE = E/|E| (unit direction)."""

        def mag(Ex):
            E = ElectricFieldJAX(
                value=jnp.array([Ex, 0.0, 0.0]),
                position=jnp.zeros(3),
            )
            return E.magnitude

        g = jax.grad(mag)(3.0)
        # d|E|/dEx = Ex/|E| = 3/3 = 1
        assert abs(g - 1.0) < 1e-15


@pytest.mark.skipif(not HAS_EFIELD, reason="maxwell.jax.electromagnetism.field not installed")
class TestElectricFieldStandaloneJAX:
    """Test standalone electric field functions."""

    def test_electric_tension_jax(self):
        """Tension = |E|."""
        T = electric_tension_jax(jnp.array([3.0, 0.0, 4.0]))
        assert abs(T - 5.0) < 1e-15

    def test_electric_tension_zero(self):
        """Zero field gives zero tension."""
        T = electric_tension_jax(jnp.zeros(3))
        assert T == 0.0

    def test_electric_flux_jax(self):
        """Flux = E . n * A for uniform field."""
        E = jnp.array([100.0, 0.0, 0.0])
        n = jnp.array([1.0, 0.0, 0.0])
        flux = electric_flux_jax(E, n, area=10.0)
        # Flux = 100 * 1 * 10 = 1000
        assert abs(flux - 1000.0) < 1e-15

    def test_electric_flux_jax_perpendicular(self):
        """Zero flux when field is perpendicular to surface."""
        E = jnp.array([0.0, 0.0, 100.0])
        n = jnp.array([1.0, 0.0, 0.0])
        flux = electric_flux_jax(E, n, area=10.0)
        assert abs(flux) < 1e-15

    def test_electric_flux_jax_oblique(self):
        """Flux at oblique angle: E . n = |E| * cos(theta)."""
        E = jnp.array([100.0, 100.0, 0.0])
        n = jnp.array([1.0, 0.0, 0.0])
        flux = electric_flux_jax(E, n, area=1.0)
        # E . n = 100
        assert abs(flux - 100.0) < 1e-15

    def test_gauss_law_jax(self):
        """Gauss's law: Flux = 4*pi*Q."""
        Q = 1.0
        flux = gauss_law_closed_surface_jax(Q)
        expected = 4.0 * jnp.pi * 1.0
        assert abs(flux - expected) < 1e-15

    def test_gauss_law_jax_zero_charge(self):
        """Zero enclosed charge gives zero flux."""
        flux = gauss_law_closed_surface_jax(0.0)
        assert flux == 0.0

    def test_gauss_law_jax_negative(self):
        """Negative charge gives negative flux."""
        Q = -2.0
        flux = gauss_law_closed_surface_jax(Q)
        expected = 4.0 * jnp.pi * (-2.0)
        assert abs(flux - expected) < 1e-15

    def test_field_from_potential_jax(self):
        """E = -grad(V) for V = q/r."""
        def V(point):
            r = jnp.linalg.norm(point)
            return 1.0 / r

        point = jnp.array([1.0, 0.0, 0.0])
        E = field_from_potential_jax(V, point)
        # For V = 1/r, E = -grad(V) = r_hat/r^2 = (1,0,0)
        expected = jnp.array([1.0, 0.0, 0.0])
        assert jnp.allclose(E, expected, atol=1e-6)

    def test_field_from_potential_jax_quadratic(self):
        """E = -grad(V) for V = x^2 + y^2 + z^2."""
        def V(point):
            return jnp.sum(point ** 2)

        point = jnp.array([1.0, 2.0, 3.0])
        E = field_from_potential_jax(V, point)
        # grad(V) = (2x, 2y, 2z), E = -(2x, 2y, 2z)
        expected = jnp.array([-2.0, -4.0, -6.0])
        assert jnp.allclose(E, expected, atol=1e-10)

    def test_electromotive_force_jax_uniform(self):
        """EMF line integral for uniform field."""
        def E_func(pos):
            return jnp.array([10.0, 0.0, 0.0])

        start = jnp.array([0.0, 0.0, 0.0])
        end = jnp.array([5.0, 0.0, 0.0])
        emf = electromotive_force_jax(E_func, start, end, num_steps=100)
        # EMF = 10 * 5 = 50
        assert abs(emf - 50.0) < 1e-6

    def test_electromotive_force_jax_zero(self):
        """EMF = 0 for perpendicular path."""
        def E_func(pos):
            return jnp.array([0.0, 0.0, 100.0])

        start = jnp.array([0.0, 0.0, 0.0])
        end = jnp.array([5.0, 0.0, 0.0])
        emf = electromotive_force_jax(E_func, start, end, num_steps=100)
        assert abs(emf) < 1e-6

    def test_superposition_field_jax(self):
        """Superposition field at multiple points."""
        q1 = PointChargeJAX(q=1.0, position=jnp.zeros(3))
        q2 = PointChargeJAX(q=2.0, position=jnp.array([3.0, 0.0, 0.0]))
        points = jnp.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        fields = superposition_field_jax([q1, q2], points)
        assert fields.shape == (2, 3)
        # At (1,0,0): E1 from q1: r=1, E=(1,0,0); E2 from q2: r=(-2,0,0), E=2*(-1,0,0)/4=(-0.5,0,0)
        # Total: (0.5, 0, 0)
        assert jnp.allclose(fields[0, 0], 0.5, atol=1e-10)

    def test_jit_electric_flux(self):
        """Electric flux works under JIT."""

        @jax.jit
        def jit_flux(E, n, area):
            return electric_flux_jax(E, n, area)

        flux = jit_flux(
            jnp.array([50.0, 0.0, 0.0]),
            jnp.array([1.0, 0.0, 0.0]),
            20.0,
        )
        assert abs(flux - 1000.0) < 1e-15

    def test_jit_field_from_potential(self):
        """field_from_potential works under JIT."""

        @jax.jit
        def jit_field(px, py, pz):
            point = jnp.array([px, py, pz])

            def V(p):
                return jnp.sum(p ** 2)

            return field_from_potential_jax(V, point)

        E = jit_field(1.0, 0.0, 0.0)
        assert E.shape == (3,)
        assert abs(E[0] - (-2.0)) < 1e-10

    def test_grad_flux_wrt_field(self):
        """d(Flux)/dE = n * A."""

        def flux_from_Ex(Ex):
            E = jnp.array([Ex, 0.0, 0.0])
            n = jnp.array([1.0, 0.0, 0.0])
            return electric_flux_jax(E, n, 10.0)

        g = jax.grad(flux_from_Ex)(100.0)
        # d(Flux)/dEx = n_x * A = 1 * 10 = 10
        assert abs(g - 10.0) < 1e-15

    def test_jit_emf_line_integral(self):
        """EMF line integral works under JIT."""

        @jax.jit
        def jit_emf(start, end):
            def E_func(pos):
                return jnp.array([5.0, 0.0, 0.0])
            return electromotive_force_jax(E_func, start, end, num_steps=50)

        emf = jit_emf(jnp.zeros(3), jnp.array([10.0, 0.0, 0.0]))
        assert abs(emf - 50.0) < 1e-3


# ── Imports for MagnetJAX ────────────────────────────────────────────

try:
    from maxwell.jax.core.magnet import (
        MagneticPoleJAX,
        MagnetJAX,
        pole_force_jax,
        mutual_action_jax,
        torque_on_magnet_jax,
        pole_force_gradient,
    )

    HAS_MAGNET = True
except ImportError:
    HAS_MAGNET = False


# ── MagneticPoleJAX ───────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagneticPoleJAX:
    """Test MagneticPoleJAX against NumPy reference (Art. 371)."""

    def setup_method(self):
        self.pole = MagneticPoleJAX(
            strength=100.0, position=jnp.array([0.0, 0.0, 0.0])
        )

    def test_field_at_single_point(self):
        """H = m/r^2 at 5 cm: H = 100/25 = 4 gauss."""
        point = jnp.array([5.0, 0.0, 0.0])
        H = self.pole.field_at(point)
        expected = jnp.array([4.0, 0.0, 0.0])
        assert jnp.allclose(H, expected, atol=1e-10)

    def test_field_at_origin_safe(self):
        """Field at pole position should be zero (safe division)."""
        H = self.pole.field_at(jnp.array([0.0, 0.0, 0.0]))
        assert jnp.allclose(H, jnp.zeros(3), atol=1e-15)

    def test_field_radial_direction(self):
        """Field points radially away from positive (N) pole."""
        point = jnp.array([1.0, 1.0, 1.0])
        H = self.pole.field_at(point)
        r_hat = point / jnp.linalg.norm(point)
        H_hat = H / jnp.linalg.norm(H)
        assert jnp.allclose(H_hat, r_hat, atol=1e-10)

    def test_negative_pole_field(self):
        """South pole produces inward-pointing field."""
        s_pole = MagneticPoleJAX(strength=-100.0, position=jnp.zeros(3))
        point = jnp.array([1.0, 0.0, 0.0])
        H = s_pole.field_at(point)
        assert H[0] < 0

    def test_field_inverse_square(self):
        """Field magnitude follows inverse square law."""
        H1 = self.pole.field_at(jnp.array([1.0, 0.0, 0.0]))
        H2 = self.pole.field_at(jnp.array([2.0, 0.0, 0.0]))
        H4 = self.pole.field_at(jnp.array([4.0, 0.0, 0.0]))
        # H(1) = 100, H(2) = 25, H(4) = 6.25
        assert abs(jnp.linalg.norm(H1) - 100.0) < 1e-10
        assert abs(jnp.linalg.norm(H2) - 25.0) < 1e-10
        assert abs(jnp.linalg.norm(H4) - 6.25) < 1e-10

    def test_batched_field(self):
        """Batched field evaluation."""
        points = jnp.array([
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
        ])
        H = self.pole.field_at_batched(points)
        assert H.shape == (3, 3)
        expected_magnitudes = jnp.array([100.0, 25.0, 4.0])
        actual_magnitudes = jnp.linalg.norm(H, axis=1)
        assert jnp.allclose(actual_magnitudes, expected_magnitudes, atol=1e-10)

    def test_field_at_off_axis(self):
        """Field at off-axis point has correct direction and magnitude."""
        point = jnp.array([3.0, 4.0, 0.0])
        H = self.pole.field_at(point)
        r = jnp.linalg.norm(point)  # 5
        expected_mag = 100.0 / (r ** 2)  # 4.0
        assert abs(jnp.linalg.norm(H) - expected_mag) < 1e-10
        # Direction should be along r_hat
        r_hat = point / r
        H_hat = H / jnp.linalg.norm(H)
        assert jnp.allclose(H_hat, r_hat, atol=1e-10)

    def test_matches_numpy_reference(self):
        """JAX results match NumPy MagneticPole exactly."""
        from maxwell.core.magnet import MagneticPole

        point = np.array([5.0, 3.0, 2.0])
        np_pole = MagneticPole(
            strength=100.0, position=np.array([0.0, 0.0, 0.0]), pole_type="N"
        )
        # NumPy field: H = m * r / r^3
        r_vec = point - np_pole.position
        r_mag = np.linalg.norm(r_vec)
        H_np = np_pole.signed_strength * r_vec / (r_mag ** 3)

        jax_pole = MagneticPoleJAX(
            strength=100.0, position=jnp.array([0.0, 0.0, 0.0])
        )
        H_jax = jax_pole.field_at(jnp.array(point))

        assert jnp.allclose(H_jax, H_np, atol=1e-8)


# ── MagneticPoleJAX: JIT and Auto-Diff ────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagneticPoleJAXJIT:
    """Test JIT compilation and auto-diff for MagneticPoleJAX."""

    def test_jit_field(self):
        """MagneticPoleJAX field works under JIT."""

        @jax.jit
        def compute_field(strength, pos, point):
            p = MagneticPoleJAX(strength=strength, position=pos)
            return p.field_at(point)

        result = compute_field(100.0, jnp.zeros(3), jnp.array([5.0, 0.0, 0.0]))
        assert result.shape == (3,)
        assert abs(result[0] - 4.0) < 1e-10

    def test_vmap_field(self):
        """MagneticPoleJAX works with vmap."""

        def single_field(point):
            p = MagneticPoleJAX(strength=100.0, position=jnp.zeros(3))
            return p.field_at(point)

        points = jnp.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
        result = jax.vmap(single_field)(points)
        assert result.shape == (3, 3)

    def test_static_jit_field(self):
        """Static JIT-compiled field method works."""
        H = MagneticPoleJAX._field_at_jit(
            100.0, jnp.zeros(3), jnp.array([10.0, 0.0, 0.0])
        )
        # H = 100/100 = 1 along x
        assert jnp.allclose(H, jnp.array([1.0, 0.0, 0.0]), atol=1e-10)

    def test_grad_field_wrt_strength(self):
        """d|H|/dm = |H|/m for magnetic pole (linearity)."""

        def field_mag(strength):
            p = MagneticPoleJAX(strength=strength, position=jnp.zeros(3))
            H = p.field_at(jnp.array([5.0, 0.0, 0.0]))
            return jnp.linalg.norm(H)

        g = jax.grad(field_mag)(100.0)
        # |H| = m/r^2 = 100/25 = 4, d|H|/dm = 1/r^2 = 0.04
        assert abs(g - 0.04) < 1e-10

    def test_grad_potential_wrt_position(self):
        """Gradient of field magnitude w.r.t. pole position."""

        def field_mag_at_pos(pos):
            p = MagneticPoleJAX(strength=100.0, position=pos)
            H = p.field_at(jnp.array([5.0, 0.0, 0.0]))
            return jnp.linalg.norm(H)

        g = jax.grad(field_mag_at_pos)(jnp.zeros(3))
        assert g.shape == (3,)
        assert jnp.isfinite(g).all()


# ── MagnetJAX ─────────────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagnetJAX:
    """Test MagnetJAX against NumPy reference (Arts. 372-376)."""

    def setup_method(self):
        # Bar magnet along z-axis: N at (0,0,1), S at (0,0,-1), strength=50
        self.magnet = MagnetJAX(
            pole_strength=50.0,
            north_position=jnp.array([0.0, 0.0, 1.0]),
            south_position=jnp.array([0.0, 0.0, -1.0]),
        )

    def test_magnetic_moment(self):
        """m = strength * (r_N - r_S) = 50 * (0,0,2) = (0,0,100)."""
        moment = self.magnet.magnetic_moment
        expected = jnp.array([0.0, 0.0, 100.0])
        assert jnp.allclose(moment, expected, atol=1e-10)

    def test_magnetic_length(self):
        """Distance between poles = 2 cm."""
        length = self.magnet.magnetic_length
        assert abs(length - 2.0) < 1e-10

    def test_magnetic_axis(self):
        """Unit vector from S to N = (0,0,1)."""
        axis = self.magnet.magnetic_axis
        expected = jnp.array([0.0, 0.0, 1.0])
        assert jnp.allclose(axis, expected, atol=1e-10)

    def test_field_on_axis(self):
        """Field on the magnetic axis (beyond N pole)."""
        point = jnp.array([0.0, 0.0, 3.0])
        H = self.magnet.field_at(point)
        # r_N = (0,0,2), r_S = (0,0,4)
        # H_N = 50 * (0,0,2) / 8 = (0,0,12.5)
        # H_S = -50 * (0,0,4) / 64 = (0,0,-3.125)
        # Total = (0,0,9.375)
        expected = jnp.array([0.0, 0.0, 9.375])
        assert jnp.allclose(H, expected, atol=1e-10)

    def test_field_at_origin_safe(self):
        """Field at center of magnet should be finite."""
        H = self.magnet.field_at(jnp.array([0.0, 0.0, 0.0]))
        # Both poles contribute equally, field points S to N
        # H_N: r = (0,0,-1), r^2=1, H_N = 50*(0,0,-1)/1 = (0,0,-50)
        # H_S: r = (0,0,1), r^2=1, H_S = -50*(0,0,1)/1 = (0,0,-50)
        # Total = (0,0,-100)
        expected = jnp.array([0.0, 0.0, -100.0])
        assert jnp.allclose(H, expected, atol=1e-10)

    def test_field_far_away_dipole_approximation(self):
        """Field at large distance approximates dipole field."""
        point = jnp.array([0.0, 0.0, 100.0])
        H = self.magnet.field_at(point)
        # Dipole approximation: H = 2*m/r^3 along axis
        # m = 100, r = 99 (from center to point, approx)
        # More precisely: exact calculation
        assert jnp.all(jnp.isfinite(H))
        assert H[2] > 0  # Points away from magnet on N side

    def test_batched_field(self):
        """Batched field evaluation."""
        points = jnp.array([
            [0.0, 0.0, 3.0],
            [0.0, 0.0, 5.0],
            [0.0, 0.0, 10.0],
        ])
        H = self.magnet.field_at_batched(points)
        assert H.shape == (3, 3)

    def test_force_in_nonuniform_field(self):
        """Force on magnet in nonuniform field."""
        H_north = jnp.array([0.0, 0.0, 100.0])
        H_south = jnp.array([0.0, 0.0, 80.0])
        F = self.magnet.force_in_field(H_north, H_south)
        # F = 50*(0,0,100) - 50*(0,0,80) = (0,0,1000)
        expected = jnp.array([0.0, 0.0, 1000.0])
        assert jnp.allclose(F, expected, atol=1e-10)

    def test_force_in_uniform_field(self):
        """Force on magnet in uniform field is zero."""
        H_uniform = jnp.array([0.0, 0.0, 50.0])
        F = self.magnet.force_in_field(H_uniform, H_uniform)
        assert jnp.allclose(F, jnp.zeros(3), atol=1e-15)

    def test_torque_in_uniform_field(self):
        """tau = m x H."""
        H = jnp.array([100.0, 0.0, 0.0])
        tau = self.magnet.torque_in_uniform_field(H)
        # m = (0,0,100), H = (100,0,0)
        # m x H = (0, 10000, 0)
        expected = jnp.array([0.0, 10000.0, 0.0])
        assert jnp.allclose(tau, expected, atol=1e-10)

    def test_torque_aligned_field(self):
        """Zero torque when magnet is aligned with field."""
        H = jnp.array([0.0, 0.0, 50.0])
        tau = self.magnet.torque_in_uniform_field(H)
        assert jnp.allclose(tau, jnp.zeros(3), atol=1e-15)

    def test_potential_energy_uniform_field(self):
        """W = -m dot H."""
        H = jnp.array([0.0, 0.0, 50.0])
        W = self.magnet.potential_energy_in_field(H)
        # W = -(0,0,100) . (0,0,50) = -5000
        assert abs(W - (-5000.0)) < 1e-10

    def test_potential_energy_perpendicular(self):
        """Zero energy when m is perpendicular to H."""
        H = jnp.array([100.0, 0.0, 0.0])
        W = self.magnet.potential_energy_in_field(H)
        assert abs(W) < 1e-15

    def test_potential_energy_minimum(self):
        """Energy is minimum (most negative) when m parallel to H."""
        H = jnp.array([0.0, 0.0, 50.0])
        W_parallel = self.magnet.potential_energy_in_field(H)
        H_anti = jnp.array([0.0, 0.0, -50.0])
        W_anti = self.magnet.potential_energy_in_field(H_anti)
        assert W_parallel < W_anti  # Parallel = lower energy

    def test_static_jit_field(self):
        """Static JIT-compiled field method works."""
        H = MagnetJAX._field_at_jit(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            jnp.array([0.0, 0.0, 3.0]),
        )
        assert H.shape == (3,)
        assert jnp.isfinite(H).all()

    def test_static_jit_torque(self):
        """Static JIT-compiled torque method works."""
        tau = MagnetJAX._torque_jit(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            jnp.array([100.0, 0.0, 0.0]),
        )
        expected = jnp.array([0.0, 10000.0, 0.0])
        assert jnp.allclose(tau, expected, atol=1e-10)

    def test_static_jit_energy(self):
        """Static JIT-compiled energy method works."""
        W = MagnetJAX._energy_jit(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            jnp.array([0.0, 0.0, 50.0]),
        )
        assert abs(W - (-5000.0)) < 1e-10


# ── MagnetJAX: JIT and Auto-Diff ──────────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagnetJAXJIT:
    """Test JIT compilation and auto-diff for MagnetJAX."""

    def test_jit_magnetic_moment(self):
        """Magnetic moment calculation works under JIT."""

        @jax.jit
        def compute_moment(strength, n_pos, s_pos):
            m = MagnetJAX(
                pole_strength=strength, north_position=n_pos, south_position=s_pos
            )
            return m.magnetic_moment

        result = compute_moment(
            50.0, jnp.array([0.0, 0.0, 1.0]), jnp.array([0.0, 0.0, -1.0])
        )
        assert jnp.allclose(result, jnp.array([0.0, 0.0, 100.0]), atol=1e-10)

    def test_jit_torque(self):
        """Torque calculation works under JIT."""

        @jax.jit
        def compute_torque(strength, n_pos, s_pos, H):
            m = MagnetJAX(
                pole_strength=strength, north_position=n_pos, south_position=s_pos
            )
            return m.torque_in_uniform_field(H)

        tau = compute_torque(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            jnp.array([100.0, 0.0, 0.0]),
        )
        assert jnp.allclose(tau, jnp.array([0.0, 10000.0, 0.0]), atol=1e-10)

    def test_jit_energy(self):
        """Energy calculation works under JIT."""

        @jax.jit
        def compute_energy(strength, n_pos, s_pos, H):
            m = MagnetJAX(
                pole_strength=strength, north_position=n_pos, south_position=s_pos
            )
            return m.potential_energy_in_field(H)

        W = compute_energy(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            jnp.array([0.0, 0.0, 50.0]),
        )
        assert abs(W - (-5000.0)) < 1e-10

    def test_grad_energy_wrt_moment(self):
        """dW/dm = -H (since W = -m dot H)."""

        def energy_from_mz(mz):
            moment = jnp.array([0.0, 0.0, mz])
            H = jnp.array([0.0, 0.0, 50.0])
            return -jnp.dot(moment, H)

        g = jax.grad(energy_from_mz)(100.0)
        # dW/dmz = -Hz = -50
        assert abs(g - (-50.0)) < 1e-10

    def test_grad_torque_wrt_field(self):
        """Gradient of torque magnitude w.r.t. field component."""

        def torque_mag(Hx):
            m = MagnetJAX(
                pole_strength=50.0,
                north_position=jnp.array([0.0, 0.0, 1.0]),
                south_position=jnp.array([0.0, 0.0, -1.0]),
            )
            H = jnp.array([Hx, 0.0, 0.0])
            tau = m.torque_in_uniform_field(H)
            return jnp.linalg.norm(tau)

        g = jax.grad(torque_mag)(100.0)
        assert jnp.isfinite(g)


# ── Pytree Registration ───────────────────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagnetPytreeRegistration:
    """Test that MagnetJAX and MagneticPoleJAX are proper JAX pytrees."""

    def test_pole_pytree_flatten(self):
        """MagneticPoleJAX can be flattened and unflattened."""
        pole = MagneticPoleJAX(
            strength=100.0, position=jnp.array([0.0, 0.0, 0.0])
        )
        leaves, treedef = jax.tree_util.tree_flatten(pole)
        assert len(leaves) == 2  # strength and position
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert restored.strength == pole.strength
        assert jnp.allclose(restored.position, pole.position)

    def test_magnet_pytree_flatten(self):
        """MagnetJAX can be flattened and unflattened."""
        magnet = MagnetJAX(
            pole_strength=50.0,
            north_position=jnp.array([0.0, 0.0, 1.0]),
            south_position=jnp.array([0.0, 0.0, -1.0]),
        )
        leaves, treedef = jax.tree_util.tree_flatten(magnet)
        assert len(leaves) == 3  # pole_strength, north_position, south_position
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert restored.pole_strength == magnet.pole_strength
        assert jnp.allclose(restored.north_position, magnet.north_position)
        assert jnp.allclose(restored.south_position, magnet.south_position)

    def test_magnet_jit_compatible(self):
        """MagnetJAX works with jax.jit."""

        @jax.jit
        def compute_moment(strength, n_pos, s_pos):
            m = MagnetJAX(
                pole_strength=strength, north_position=n_pos, south_position=s_pos
            )
            return m.magnetic_moment

        result = compute_moment(
            50.0, jnp.array([0.0, 0.0, 1.0]), jnp.array([0.0, 0.0, -1.0])
        )
        assert result.shape == (3,)

    def test_magnet_vmap_compatible(self):
        """MagnetJAX works with jax.vmap."""

        def single_field(n_pos):
            m = MagnetJAX(
                pole_strength=50.0, north_position=n_pos, south_position=jnp.array([0.0, 0.0, -1.0])
            )
            return m.field_at(jnp.array([0.0, 0.0, 3.0]))

        n_positions = jnp.array([
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 2.0],
            [0.0, 0.0, 3.0],
        ])
        result = jax.vmap(single_field)(n_positions)
        assert result.shape == (3, 3)


# ── Standalone Functions ──────────────────────────────────────────────


@pytest.mark.skipif(not HAS_MAGNET, reason="maxwell.jax.core.magnet not installed")
class TestMagnetStandaloneJAX:
    """Test standalone magnet functions."""

    def test_pole_force_jax_basic(self):
        """F = m1*m2/r^2 for two like poles."""
        F = pole_force_jax(10.0, 10.0, jnp.array(5.0))
        # F = 100/25 = 4 dyne (repulsive)
        assert abs(F - 4.0) < 1e-10

    def test_pole_force_jax_attractive(self):
        """Opposite poles give negative (attractive) force."""
        F = pole_force_jax(10.0, -10.0, jnp.array(5.0))
        assert F < 0  # Attractive
        assert abs(F - (-4.0)) < 1e-10

    def test_pole_force_jax_zero_distance(self):
        """Zero distance gives zero force (safe division)."""
        F = pole_force_jax(10.0, 10.0, jnp.array(0.0))
        assert abs(F) < 1e-15

    def test_pole_force_jax_array(self):
        """Pole force works with array of distances."""
        distances = jnp.array([1.0, 2.0, 5.0, 10.0])
        forces = pole_force_jax(10.0, 10.0, distances)
        expected = jnp.array([100.0, 25.0, 4.0, 1.0])
        assert jnp.allclose(forces, expected, atol=1e-10)

    def test_pole_force_jax_inverse_square(self):
        """Force follows inverse square law."""
        F1 = pole_force_jax(1.0, 1.0, jnp.array(1.0))
        F2 = pole_force_jax(1.0, 1.0, jnp.array(2.0))
        F4 = pole_force_jax(1.0, 1.0, jnp.array(4.0))
        assert abs(F1 - 1.0) < 1e-10
        assert abs(F2 - 0.25) < 1e-10
        assert abs(F4 - 0.0625) < 1e-10

    def test_torque_on_magnet_jax(self):
        """tau = m x H."""
        tau = torque_on_magnet_jax(
            magnetic_moment=jnp.array([0.0, 0.0, 100.0]),
            H_field=jnp.array([100.0, 0.0, 0.0]),
        )
        # (0,0,100) x (100,0,0) = (0, 10000, 0)
        expected = jnp.array([0.0, 10000.0, 0.0])
        assert jnp.allclose(tau, expected, atol=1e-10)

    def test_torque_on_magnet_jax_aligned(self):
        """Zero torque when aligned."""
        tau = torque_on_magnet_jax(
            magnetic_moment=jnp.array([0.0, 0.0, 100.0]),
            H_field=jnp.array([0.0, 0.0, 50.0]),
        )
        assert jnp.allclose(tau, jnp.zeros(3), atol=1e-15)

    def test_torque_on_magnet_jax_zero_moment(self):
        """Zero moment gives zero torque."""
        tau = torque_on_magnet_jax(
            magnetic_moment=jnp.zeros(3),
            H_field=jnp.array([100.0, 0.0, 0.0]),
        )
        assert jnp.allclose(tau, jnp.zeros(3), atol=1e-15)

    def test_mutual_action_jax(self):
        """Mutual action between two magnets returns all expected keys."""
        result = mutual_action_jax(
            m1_strength=50.0,
            m1_north=jnp.array([0.0, 0.0, 1.0]),
            m1_south=jnp.array([0.0, 0.0, -1.0]),
            m2_strength=30.0,
            m2_north=jnp.array([10.0, 0.0, 1.0]),
            m2_south=jnp.array([10.0, 0.0, -1.0]),
        )
        assert "force_on_2" in result
        assert "torque_on_2" in result
        assert "potential_energy" in result
        assert result["force_on_2"].shape == (3,)
        assert result["torque_on_2"].shape == (3,)
        assert jnp.isfinite(result["potential_energy"])

    def test_mutual_action_jax_symmetric(self):
        """Mutual action produces finite, reasonable values."""
        # Two identical magnets side by side
        result = mutual_action_jax(
            m1_strength=10.0,
            m1_north=jnp.array([0.0, 0.0, 0.5]),
            m1_south=jnp.array([0.0, 0.0, -0.5]),
            m2_strength=10.0,
            m2_north=jnp.array([5.0, 0.0, 0.5]),
            m2_south=jnp.array([5.0, 0.0, -0.5]),
        )
        # Forces should be small at this distance
        assert jnp.linalg.norm(result["force_on_2"]) < 1.0

    def test_mutual_action_jax_far_apart(self):
        """Mutual action decreases with distance."""
        result_near = mutual_action_jax(
            m1_strength=10.0,
            m1_north=jnp.array([0.0, 0.0, 0.5]),
            m1_south=jnp.array([0.0, 0.0, -0.5]),
            m2_strength=10.0,
            m2_north=jnp.array([5.0, 0.0, 0.5]),
            m2_south=jnp.array([5.0, 0.0, -0.5]),
        )
        result_far = mutual_action_jax(
            m1_strength=10.0,
            m1_north=jnp.array([0.0, 0.0, 0.5]),
            m1_south=jnp.array([0.0, 0.0, -0.5]),
            m2_strength=10.0,
            m2_north=jnp.array([50.0, 0.0, 0.5]),
            m2_south=jnp.array([50.0, 0.0, -0.5]),
        )
        # Force should be much smaller at greater distance
        assert jnp.linalg.norm(result_far["force_on_2"]) < jnp.linalg.norm(
            result_near["force_on_2"]
        )

    def test_pole_force_gradient(self):
        """dF/dm1 = m2/r^2."""
        g = pole_force_gradient(10.0, 5.0, 2.0)
        expected = 5.0 / 4.0  # m2/r^2 = 5/4 = 1.25
        assert abs(g - expected) < 1e-10

    def test_jit_pole_force(self):
        """Pole force works under JIT."""

        @jax.jit
        def jit_pole_force(m1, m2, r):
            return pole_force_jax(m1, m2, r)

        F = jit_pole_force(10.0, 10.0, jnp.array(5.0))
        assert abs(F - 4.0) < 1e-10

    def test_jit_torque(self):
        """Torque function works under JIT."""

        @jax.jit
        def jit_torque(moment, H):
            return torque_on_magnet_jax(moment, H)

        tau = jit_torque(jnp.array([0.0, 0.0, 100.0]), jnp.array([100.0, 0.0, 0.0]))
        assert jnp.allclose(tau, jnp.array([0.0, 10000.0, 0.0]), atol=1e-10)

    def test_jit_mutual_action(self):
        """Mutual action works under JIT."""

        @jax.jit
        def jit_mutual(m1s, m1n, m1s_pos, m2s, m2n, m2s_pos):
            result = mutual_action_jax(m1s, m1n, m1s_pos, m2s, m2n, m2s_pos)
            return result["force_on_2"]

        force = jit_mutual(
            50.0,
            jnp.array([0.0, 0.0, 1.0]),
            jnp.array([0.0, 0.0, -1.0]),
            30.0,
            jnp.array([10.0, 0.0, 1.0]),
            jnp.array([10.0, 0.0, -1.0]),
        )
        assert force.shape == (3,)

    def test_vmap_pole_force(self):
        """vmap over multiple distances."""
        distances = jnp.array([1.0, 2.0, 5.0, 10.0])
        forces = jax.vmap(lambda r: pole_force_jax(10.0, 10.0, r))(distances)
        expected = jnp.array([100.0, 25.0, 4.0, 1.0])
        assert jnp.allclose(forces, expected, atol=1e-10)

    def test_grad_pole_force_wrt_distance(self):
        """dF/dr = -2*m1*m2/r^3."""
        def F(r):
            return pole_force_jax(10.0, 10.0, r)

        g = jax.grad(F)(5.0)
        expected = -2.0 * 10.0 * 10.0 / (5.0 ** 3)  # -200/125 = -1.6
        assert abs(g - expected) < 1e-10

    def test_grad_torque_wrt_moment(self):
        """d|tau|/dm for torque."""
        def torque_mag(mx):
            moment = jnp.array([mx, 0.0, 0.0])
            H = jnp.array([0.0, 100.0, 0.0])
            tau = torque_on_magnet_jax(moment, H)
            return jnp.linalg.norm(tau)

        g = jax.grad(torque_mag)(50.0)
        # |tau| = |mx| * |Hz| = mx * 100, d|tau|/dmx = 100
        assert abs(g - 100.0) < 1e-8

    def test_cross_validation_with_numpy(self):
        """JAX MagnetJAX field matches NumPy Magnet field."""
        from maxwell.core.magnet import Magnet, MagneticPole

        # Create NumPy magnet
        np_north = MagneticPole(
            strength=50.0, position=np.array([0.0, 0.0, 1.0]), pole_type="N"
        )
        np_south = MagneticPole(
            strength=-50.0, position=np.array([0.0, 0.0, -1.0]), pole_type="S"
        )
        np_magnet = Magnet(north_pole=np_north, south_pole=np_south)

        # Create JAX magnet
        jax_magnet = MagnetJAX(
            pole_strength=50.0,
            north_position=jnp.array([0.0, 0.0, 1.0]),
            south_position=jnp.array([0.0, 0.0, -1.0]),
        )

        # Compare fields at several points
        test_points = [
            np.array([0.0, 0.0, 3.0]),
            np.array([0.0, 0.0, 5.0]),
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 2.0, 0.0]),
        ]

        for point in test_points:
            # NumPy: H = m_N * r_N/r_N^3 + m_S * r_S/r_S^3
            r_n = point - np_magnet.north_pole.position
            r_s = point - np_magnet.south_pole.position
            r_n_mag = np.linalg.norm(r_n)
            r_s_mag = np.linalg.norm(r_s)
            H_np = (
                np_magnet.north_pole.signed_strength * r_n / (r_n_mag ** 3)
                + np_magnet.south_pole.signed_strength * r_s / (r_s_mag ** 3)
            )

            H_jax = jax_magnet.field_at(jnp.array(point))
            assert jnp.allclose(H_jax, H_np, atol=1e-8), (
                f"Field mismatch at {point}: JAX={H_jax}, NumPy={H_np}"
            )


# ── Imports for ElectrostaticEnergyJAX ────────────────────────────────────

try:
    from maxwell.jax.electromagnetism.energy import (
        ElectrostaticEnergyJAX,
        CapacitorEnergyJAX,
        calc_electrostatic_energy_density_jax,
        calc_energy_density_from_ED_dot_jax,
        calc_capacitor_energy_jax,
        calc_total_electrostatic_energy_jax,
        verify_electrostatic_energy_density_jax,
        analyze_electrostatic_energy_jax,
    )
    from maxwell.jax.electromagnetism.magnetic_energy import (
        MagneticEnergyJAX,
        InductorEnergyJAX,
        calc_magnetic_energy_density_jax,
        calc_energy_density_from_BH_dot_jax,
        calc_inductor_energy_jax,
        calc_total_magnetic_energy_jax,
        verify_magnetic_energy_density_jax,
        analyze_magnetic_energy_jax,
    )

    HAS_ENERGY = True
    HAS_MAGNETIC_ENERGY = True
except ImportError:
    HAS_ENERGY = False
    HAS_MAGNETIC_ENERGY = False


# ── ElectrostaticEnergyJAX ────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestElectrostaticEnergyJAX:
    """Test ElectrostaticEnergyJAX against NumPy reference (Arts. 630-631)."""

    def setup_method(self):
        self.energy = ElectrostaticEnergyJAX(
            E_field=jnp.array([1000.0, 0.0, 0.0]),
            permittivity=1.0,
        )

    def test_D_field_vacuum(self):
        """D = eps * E for vacuum (eps=1)."""
        D = self.energy.D_field
        expected = jnp.array([1000.0, 0.0, 0.0])
        assert jnp.allclose(D, expected, atol=1e-10)

    def test_D_field_dielectric(self):
        """D = eps * E for dielectric (eps=2.5)."""
        energy = ElectrostaticEnergyJAX(
            E_field=jnp.array([500.0, 0.0, 0.0]),
            permittivity=2.5,
        )
        D = energy.D_field
        expected = jnp.array([1250.0, 0.0, 0.0])
        assert jnp.allclose(D, expected, atol=1e-10)

    def test_energy_density_vacuum(self):
        """u = (1/8*pi) * E^2 for E=1000 statV/cm."""
        u = self.energy.energy_density
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_dielectric(self):
        """u = (1/8*pi) * eps * E^2 with eps=2.5."""
        energy = ElectrostaticEnergyJAX(
            E_field=jnp.array([500.0, 0.0, 0.0]),
            permittivity=2.5,
        )
        u = energy.energy_density
        expected = 2.5 * 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_zero_field(self):
        """Zero field gives zero energy density."""
        energy = ElectrostaticEnergyJAX(
            E_field=jnp.zeros(3),
            permittivity=1.0,
        )
        assert energy.energy_density == 0.0

    def test_energy_density_arbitrary_direction(self):
        """Energy density depends on E^2, not direction."""
        E_mag = 1000.0
        e_x = ElectrostaticEnergyJAX(E_field=jnp.array([E_mag, 0.0, 0.0]))
        e_y = ElectrostaticEnergyJAX(E_field=jnp.array([0.0, E_mag, 0.0]))
        e_z = ElectrostaticEnergyJAX(E_field=jnp.array([0.0, 0.0, E_mag]))
        e_diag = ElectrostaticEnergyJAX(
            E_field=jnp.array([E_mag / jnp.sqrt(3), E_mag / jnp.sqrt(3), E_mag / jnp.sqrt(3)])
        )
        # Diagonal: E^2 = E_mag^2 * (1/3 + 1/3 + 1/3) = E_mag^2
        assert abs(e_x.energy_density - e_diag.energy_density) < 1e-6
        assert abs(e_x.energy_density - e_y.energy_density) < 1e-6
        assert abs(e_y.energy_density - e_z.energy_density) < 1e-6

    def test_total_energy_uniform_field(self):
        """U = u * V for uniform field."""
        u = self.energy.energy_density
        V = 1.0  # cm^3
        U = self.energy.total_energy(V)
        assert abs(U - u * V) < 1e-10

    def test_total_energy_various_volumes(self):
        """Total energy scales linearly with volume."""
        U1 = self.energy.total_energy(1.0)
        U10 = self.energy.total_energy(10.0)
        assert abs(U10 - 10.0 * U1) < 1e-6

    def test_energy_density_at_override(self):
        """energy_density_at uses custom E field."""
        E_override = jnp.array([500.0, 0.0, 0.0])
        u = self.energy.energy_density_at(E_override)
        expected = 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_from_E_and_D_linear(self):
        """from_E_and_D recovers correct permittivity for linear dielectric."""
        E = jnp.array([100.0, 0.0, 0.0])
        D = jnp.array([250.0, 0.0, 0.0])  # eps = 2.5
        energy = ElectrostaticEnergyJAX.from_E_and_D(E, D)
        assert abs(energy.permittivity - 2.5) < 1e-10

    def test_from_E_and_D_vacuum(self):
        """from_E_and_D for vacuum (eps=1)."""
        E = jnp.array([100.0, 0.0, 0.0])
        D = jnp.array([100.0, 0.0, 0.0])
        energy = ElectrostaticEnergyJAX.from_E_and_D(E, D)
        assert abs(energy.permittivity - 1.0) < 1e-10

    def test_pytree_flatten(self):
        """ElectrostaticEnergyJAX can be flattened and unflattened."""
        energy = ElectrostaticEnergyJAX(
            E_field=jnp.array([100.0, 0.0, 0.0]),
            permittivity=2.0,
        )
        leaves, treedef = jax.tree_util.tree_flatten(energy)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(restored.E_field, energy.E_field)
        assert restored.permittivity == energy.permittivity


# ── CapacitorEnergyJAX ────────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestCapacitorEnergyJAX:
    """Test CapacitorEnergyJAX (Art. 631)."""

    def setup_method(self):
        self.cap = CapacitorEnergyJAX(capacitance=10.0)

    def test_from_voltage_basic(self):
        """U = (1/2) * C * V^2 for C=10, V=100: U = 50000."""
        U = self.cap.from_voltage(100.0)
        expected = 0.5 * 10.0 * 100.0 ** 2  # = 50000
        assert abs(U - expected) < 1e-10

    def test_from_voltage_zero(self):
        """Zero voltage gives zero energy."""
        U = self.cap.from_voltage(0.0)
        assert U == 0.0

    def test_from_charge_basic(self):
        """U = Q^2/(2*C) for Q=1000, C=10: U = 50000."""
        U = self.cap.from_charge(1000.0)
        expected = 1000.0 ** 2 / (2.0 * 10.0)  # = 50000
        assert abs(U - expected) < 1e-10

    def test_from_charge_zero(self):
        """Zero charge gives zero energy."""
        U = self.cap.from_charge(0.0)
        assert U == 0.0

    def test_from_QV_basic(self):
        """U = (1/2) * Q * V for Q=1000, V=100: U = 50000."""
        U = self.cap.from_QV(1000.0, 100.0)
        expected = 0.5 * 1000.0 * 100.0  # = 50000
        assert abs(U - expected) < 1e-10

    def test_consistency_CV2_vs_Q2C(self):
        """CV^2 and Q^2/C forms give same result (Q=CV)."""
        C = 10.0
        V = 100.0
        Q = C * V  # = 1000
        cap = CapacitorEnergyJAX(capacitance=C)
        U_cv2 = cap.from_voltage(V)
        U_q2c = cap.from_charge(Q)
        assert abs(U_cv2 - U_q2c) < 1e-10

    def test_consistency_CV2_vs_QV(self):
        """CV^2 and QV forms give same result (Q=CV)."""
        C = 10.0
        V = 100.0
        Q = C * V
        cap = CapacitorEnergyJAX(capacitance=C)
        U_cv2 = cap.from_voltage(V)
        U_qv = cap.from_QV(Q, V)
        assert abs(U_cv2 - U_qv) < 1e-10

    def test_consistency_Q2C_vs_QV(self):
        """Q^2/C and QV forms give same result."""
        C = 10.0
        V = 100.0
        Q = C * V
        cap = CapacitorEnergyJAX(capacitance=C)
        U_q2c = cap.from_charge(Q)
        U_qv = cap.from_QV(Q, V)
        assert abs(U_q2c - U_qv) < 1e-10

    def test_pytree_flatten(self):
        """CapacitorEnergyJAX can be flattened and unflattened."""
        cap = CapacitorEnergyJAX(capacitance=10.0)
        leaves, treedef = jax.tree_util.tree_flatten(cap)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert restored.capacitance == cap.capacitance


# ── Standalone Energy Functions ───────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestStandaloneEnergyFunctions:
    """Test standalone electrostatic energy JAX functions."""

    def test_energy_density_vacuum(self):
        """u = (1/8*pi) * E^2 for vacuum."""
        E = jnp.array([1000.0, 0.0, 0.0])
        u = calc_electrostatic_energy_density_jax(E)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_dielectric(self):
        """u = (1/8*pi) * eps * E^2 for eps=2.5."""
        E = jnp.array([500.0, 0.0, 0.0])
        u = calc_electrostatic_energy_density_jax(E, permittivity=2.5)
        expected = 2.5 * 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_zero_field(self):
        """Zero field gives zero energy density."""
        u = calc_electrostatic_energy_density_jax(jnp.zeros(3))
        assert u == 0.0

    def test_energy_density_arbitrary_direction(self):
        """Energy density is isotropic."""
        E_mag = 1000.0
        u_x = calc_electrostatic_energy_density_jax(jnp.array([E_mag, 0.0, 0.0]))
        u_y = calc_electrostatic_energy_density_jax(jnp.array([0.0, E_mag, 0.0]))
        u_z = calc_electrostatic_energy_density_jax(jnp.array([0.0, 0.0, E_mag]))
        assert jnp.isclose(u_x, u_y, rtol=1e-10)
        assert jnp.isclose(u_y, u_z, rtol=1e-10)

    def test_energy_density_from_ED_dot_parallel(self):
        """u = (1/8*pi) * E.D for parallel E and D."""
        E = jnp.array([100.0, 0.0, 0.0])
        D = jnp.array([250.0, 0.0, 0.0])  # eps=2.5
        u = calc_energy_density_from_ED_dot_jax(E, D)
        # E.D = 100 * 250 = 25000
        expected = 25000.0 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_from_ED_dot_non_parallel(self):
        """u = (1/8*pi) * E.D for non-parallel E and D."""
        E = jnp.array([100.0, 0.0, 0.0])
        D = jnp.array([80.0, 60.0, 0.0])  # anisotropic
        u = calc_energy_density_from_ED_dot_jax(E, D)
        # E.D = 100*80 + 0*60 = 8000
        expected = 8000.0 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_from_ED_dot_zero(self):
        """Perpendicular E and D gives zero energy density."""
        E = jnp.array([100.0, 0.0, 0.0])
        D = jnp.array([0.0, 100.0, 0.0])
        u = calc_energy_density_from_ED_dot_jax(E, D)
        assert abs(u) < 1e-15

    def test_capacitor_energy_CV2(self):
        """U = (1/2)*C*V^2."""
        U = calc_capacitor_energy_jax(capacitance=10.0, voltage=100.0)
        expected = 0.5 * 10.0 * 100.0 ** 2
        assert abs(U - expected) < 1e-10

    def test_capacitor_energy_Q2C(self):
        """U = Q^2/(2*C)."""
        U = calc_capacitor_energy_jax(capacitance=10.0, charge=1000.0)
        expected = 1000.0 ** 2 / (2.0 * 10.0)
        assert abs(U - expected) < 1e-10

    def test_capacitor_energy_no_params(self):
        """Missing voltage and charge raises error."""
        with pytest.raises(ValueError):
            calc_capacitor_energy_jax(capacitance=10.0)

    def test_total_energy_jax(self):
        """U = u * V for uniform field."""
        E = jnp.array([1000.0, 0.0, 0.0])
        U = calc_total_electrostatic_energy_jax(E, volume=1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi) * 1.0
        assert abs(U - expected) < 1e-6

    def test_total_energy_various_volumes(self):
        """Total energy scales with volume."""
        E = jnp.array([500.0, 0.0, 0.0])
        U1 = calc_total_electrostatic_energy_jax(E, volume=1.0)
        U10 = calc_total_electrostatic_energy_jax(E, volume=10.0)
        assert abs(U10 - 10.0 * U1) < 1e-6


# ── Energy: Verification and Analysis ─────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestEnergyVerification:
    """Test verification and analysis functions."""

    def test_verify_isotropy(self):
        """verify_electrostatic_energy_density_jax confirms isotropy."""
        result = verify_electrostatic_energy_density_jax(
            E_magnitude=1000.0, permittivity=1.0
        )
        assert result["verified"] is True
        assert result["all_match"] is True

    def test_verify_expected_value(self):
        """Verification matches expected (1/8*pi)*eps*E^2."""
        E_mag = 1000.0
        eps = 1.0
        result = verify_electrostatic_energy_density_jax(E_magnitude=E_mag, permittivity=eps)
        expected = eps * E_mag ** 2 / (8.0 * jnp.pi)
        assert abs(result["expected"] - expected) < 1e-10

    def test_verify_dielectric(self):
        """Verification works for dielectric (eps != 1)."""
        result = verify_electrostatic_energy_density_jax(
            E_magnitude=500.0, permittivity=2.5
        )
        assert result["verified"] is True

    def test_analyze_electrostatic_energy_basic(self):
        """Basic analysis returns expected keys."""
        E = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_electrostatic_energy_jax(E)
        expected_keys = {
            "E_field", "E_magnitude", "E_direction",
            "D_field", "permittivity", "energy_density",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_analyze_with_volume(self):
        """Analysis with volume includes total_energy."""
        E = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_electrostatic_energy_jax(E, volume=1.0)
        assert "total_energy" in result
        assert "volume" in result

    def test_analyze_with_capacitor(self):
        """Analysis with capacitor params includes capacitor_energy."""
        E = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_electrostatic_energy_jax(
            E, volume=1.0, capacitance=10.0, voltage=100.0
        )
        assert "capacitor_energy" in result
        assert "energy_ratio" in result


# ── Energy: Auto-Diff ─────────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestEnergyAutoDiff:
    """Test JAX auto-differentiation on energy formulas."""

    def test_grad_density_wrt_E(self):
        """dU/dE_x = (eps/(4*pi)) * E_x for energy density."""
        def density(Ex):
            E = jnp.array([Ex, 0.0, 0.0])
            return calc_electrostatic_energy_density_jax(E)

        g = jax.grad(density)(1000.0)
        expected = 1000.0 / (4.0 * jnp.pi)
        assert abs(g - expected) < 1e-8

    def test_grad_density_wrt_permittivity(self):
        """dU/d(eps) = E^2/(8*pi)."""
        def density_eps(eps):
            return calc_electrostatic_energy_density_jax(
                jnp.array([1000.0, 0.0, 0.0]), permittivity=eps
            )

        g = jax.grad(density_eps)(1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-6

    def test_grad_capacitor_energy_wrt_V(self):
        """dU/dV = C*V for U = (1/2)*C*V^2."""
        def energy_V(V):
            return calc_capacitor_energy_jax(capacitance=10.0, voltage=V)

        g = jax.grad(energy_V)(100.0)
        expected = 10.0 * 100.0  # = 1000
        assert abs(g - expected) < 1e-10

    def test_grad_capacitor_energy_wrt_C(self):
        """dU/dC = (1/2)*V^2."""
        def energy_C(C):
            return calc_capacitor_energy_jax(capacitance=C, voltage=100.0)

        g = jax.grad(energy_C)(10.0)
        expected = 0.5 * 100.0 ** 2  # = 5000
        assert abs(g - expected) < 1e-10

    def test_grad_total_energy_wrt_volume(self):
        """dU/dV = u (energy density)."""
        def total_energy_V(vol):
            return calc_total_electrostatic_energy_jax(
                jnp.array([1000.0, 0.0, 0.0]), vol
            )

        g = jax.grad(total_energy_V)(1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-6

    def test_grad_ED_dot_wrt_E(self):
        """d(E.D)/dE = D for dot product density."""
        D = jnp.array([250.0, 0.0, 0.0])

        def density_ED(Ex):
            E = jnp.array([Ex, 0.0, 0.0])
            return calc_energy_density_from_ED_dot_jax(E, D)

        g = jax.grad(density_ED)(100.0)
        expected = 250.0 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-10


# ── Energy: JIT ───────────────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestEnergyJIT:
    """Test JIT compilation compatibility."""

    def test_jit_energy_density(self):
        """Energy density works under JIT."""

        @jax.jit
        def jit_density(E, eps):
            return calc_electrostatic_energy_density_jax(E, permittivity=eps)

        u = jit_density(jnp.array([1000.0, 0.0, 0.0]), 1.0)
        assert u > 0

    def test_jit_total_energy(self):
        """Total energy works under JIT."""

        @jax.jit
        def jit_total(E, vol, eps):
            return calc_total_electrostatic_energy_jax(E, vol, permittivity=eps)

        U = jit_total(jnp.array([1000.0, 0.0, 0.0]), 1.0, 1.0)
        assert U > 0

    def test_jit_capacitor_energy(self):
        """Capacitor energy works under JIT."""

        @jax.jit
        def jit_cap(C, V):
            return calc_capacitor_energy_jax(C, voltage=V)

        U = jit_cap(10.0, 100.0)
        expected = 0.5 * 10.0 * 100.0 ** 2
        assert abs(U - expected) < 1e-10

    def test_jit_electrostatic_energy_class(self):
        """ElectrostaticEnergyJAX works under JIT."""

        @jax.jit
        def jit_class_density(E, eps):
            e = ElectrostaticEnergyJAX(E_field=E, permittivity=eps)
            return e.energy_density

        u = jit_class_density(jnp.array([500.0, 0.0, 0.0]), 2.0)
        expected = 2.0 * 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_jit_capacitor_class(self):
        """CapacitorEnergyJAX works under JIT."""

        @jax.jit
        def jit_cap_class(C, V):
            cap = CapacitorEnergyJAX(capacitance=C)
            return cap.from_voltage(V)

        U = jit_cap_class(10.0, 100.0)
        expected = 0.5 * 10.0 * 100.0 ** 2
        assert abs(U - expected) < 1e-10


# ── Energy: vmap ──────────────────────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestEnergyVmap:
    """Test batched evaluation via vmap."""

    def test_vmap_energy_density(self):
        """vmap over batch of E fields."""
        E_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [500.0, 0.0, 0.0],
        ])
        densities = jax.vmap(calc_electrostatic_energy_density_jax)(E_batch)
        assert densities.shape == (3,)
        # Densities should be monotonically increasing (E^2 relationship)
        assert densities[0] < densities[1] < densities[2]

    def test_vmap_energy_density_dielectric(self):
        """vmap with fixed permittivity over batch of E fields."""
        E_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
        ])
        densities = jax.vmap(lambda E: calc_electrostatic_energy_density_jax(E, 2.5))(E_batch)
        assert densities.shape == (2,)

    def test_vmap_capacitor_energy(self):
        """vmap over batch of voltages."""
        voltages = jnp.array([10.0, 50.0, 100.0, 200.0])
        energies = jax.vmap(lambda V: calc_capacitor_energy_jax(10.0, voltage=V))(voltages)
        assert energies.shape == (4,)
        # U = 0.5*10*V^2: 500, 12500, 50000, 200000
        expected = 0.5 * 10.0 * voltages ** 2
        assert jnp.allclose(energies, expected, atol=1e-10)

    def test_vmap_total_energy(self):
        """vmap over batch of E fields for total energy."""
        E_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [300.0, 0.0, 0.0],
        ])
        energies = jax.vmap(lambda E: calc_total_electrostatic_energy_jax(E, volume=1.0))(E_batch)
        assert energies.shape == (3,)
        assert energies[0] < energies[1] < energies[2]


# ── Energy: NumPy Cross-Validation ────────────────────────────────────────


@pytest.mark.skipif(not HAS_ENERGY, reason="maxwell.jax.electromagnetism.energy not installed")
class TestEnergyNumpyCrossValidation:
    """Test JAX results against NumPy reference implementation."""

    def test_energy_density_matches_numpy(self):
        """JAX energy density matches NumPy."""
        from maxwell.electromagnetism.energy.electrostatic import (
            calc_electrostatic_energy_density,
        )

        E_np = np.array([1000.0, 500.0, 250.0])
        E_jax = jnp.array([1000.0, 500.0, 250.0])

        u_np = calc_electrostatic_energy_density(E_np, permittivity=2.5)
        u_jax = calc_electrostatic_energy_density_jax(E_jax, permittivity=2.5)

        assert abs(float(u_jax) - u_np) < 1e-10

    def test_total_energy_matches_numpy(self):
        """JAX total energy matches NumPy."""
        from maxwell.electromagnetism.energy.electrostatic import (
            calc_total_electrostatic_energy,
        )

        E_np = np.array([1000.0, 0.0, 0.0])
        E_jax = jnp.array([1000.0, 0.0, 0.0])

        U_np = calc_total_electrostatic_energy(E_np, volume=5.0, permittivity=1.0)
        U_jax = calc_total_electrostatic_energy_jax(E_jax, volume=5.0, permittivity=1.0)

        assert abs(float(U_jax) - U_np) < 1e-10

    def test_capacitor_energy_matches_numpy(self):
        """JAX capacitor energy matches NumPy."""
        from maxwell.electromagnetism.energy.electrostatic import (
            calc_capacitor_energy,
        )

        U_np = calc_capacitor_energy(capacitance=10.0, voltage=100.0)
        U_jax = calc_capacitor_energy_jax(capacitance=10.0, voltage=100.0)

        assert abs(float(U_jax) - U_np) < 1e-10

    def test_ED_dot_matches_numpy(self):
        """JAX E.D dot product matches NumPy."""
        from maxwell.electromagnetism.energy.electrostatic import (
            calc_energy_density_from_ED_dot,
        )

        E_np = np.array([100.0, 50.0, 0.0])
        D_np = np.array([250.0, 125.0, 0.0])
        E_jax = jnp.array([100.0, 50.0, 0.0])
        D_jax = jnp.array([250.0, 125.0, 0.0])

        u_np = calc_energy_density_from_ED_dot(E_np, D_np)
        u_jax = calc_energy_density_from_ED_dot_jax(E_jax, D_jax)

        assert abs(float(u_jax) - u_np) < 1e-10

    def test_class_energy_density_matches_numpy(self):
        """ElectrostaticEnergyJAX.energy_density matches NumPy."""
        from maxwell.electromagnetism.energy.electrostatic import ElectrostaticEnergy

        E_np = np.array([1000.0, 0.0, 0.0])
        np_energy = ElectrostaticEnergy(E_field=E_np, permittivity=2.0)

        jax_energy = ElectrostaticEnergyJAX(
            E_field=jnp.array([1000.0, 0.0, 0.0]),
            permittivity=2.0,
        )

        assert abs(float(jax_energy.energy_density) - np_energy.energy_density) < 1e-10


# -- MagneticEnergyJAX --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticEnergyJAX:
    """Test MagneticEnergyJAX against NumPy reference (Arts. 632-633)."""

    def setup_method(self):
        self.energy = MagneticEnergyJAX(
            H_field=jnp.array([1000.0, 0.0, 0.0]),
            permeability=1.0,
        )

    def test_B_field_vacuum(self):
        """B = mu * H for vacuum (mu=1)."""
        B = self.energy.B_field
        expected = jnp.array([1000.0, 0.0, 0.0])
        assert jnp.allclose(B, expected, atol=1e-10)

    def test_B_field_magnetic_material(self):
        """B = mu * H for magnetic material (mu=5000)."""
        energy = MagneticEnergyJAX(
            H_field=jnp.array([1000.0, 0.0, 0.0]),
            permeability=5000.0,
        )
        B = energy.B_field
        expected = jnp.array([5_000_000.0, 0.0, 0.0])
        assert jnp.allclose(B, expected, atol=1e-6)

    def test_energy_density_vacuum(self):
        """u = (1/8*pi) * H^2 for H=1000 oersted."""
        u = self.energy.energy_density
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_magnetic_material(self):
        """u = (1/8*pi) * mu * H^2 with mu=5000."""
        energy = MagneticEnergyJAX(
            H_field=jnp.array([1000.0, 0.0, 0.0]),
            permeability=5000.0,
        )
        u = energy.energy_density
        expected = 5000.0 * 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_zero_field(self):
        """Zero field gives zero energy density."""
        energy = MagneticEnergyJAX(
            H_field=jnp.zeros(3),
            permeability=1.0,
        )
        assert energy.energy_density == 0.0

    def test_energy_density_arbitrary_direction(self):
        """Energy density depends on H^2, not direction."""
        H_mag = 1000.0
        h_x = MagneticEnergyJAX(H_field=jnp.array([H_mag, 0.0, 0.0]))
        h_y = MagneticEnergyJAX(H_field=jnp.array([0.0, H_mag, 0.0]))
        h_z = MagneticEnergyJAX(H_field=jnp.array([0.0, 0.0, H_mag]))
        h_diag = MagneticEnergyJAX(
            H_field=jnp.array([H_mag / jnp.sqrt(3), H_mag / jnp.sqrt(3), H_mag / jnp.sqrt(3)])
        )
        assert abs(h_x.energy_density - h_diag.energy_density) < 1e-6
        assert abs(h_x.energy_density - h_y.energy_density) < 1e-6
        assert abs(h_y.energy_density - h_z.energy_density) < 1e-6

    def test_total_energy_uniform_field(self):
        """U = u * V for uniform field."""
        u = self.energy.energy_density
        V = 1.0  # cm^3
        U = self.energy.total_energy(V)
        assert abs(U - u * V) < 1e-10

    def test_total_energy_various_volumes(self):
        """Total energy scales linearly with volume."""
        U1 = self.energy.total_energy(1.0)
        U10 = self.energy.total_energy(10.0)
        assert abs(U10 - 10.0 * U1) < 1e-6

    def test_energy_density_at_override(self):
        """energy_density_at uses custom H field."""
        H_override = jnp.array([500.0, 0.0, 0.0])
        u = self.energy.energy_density_at(H_override)
        expected = 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_from_B_and_H_linear(self):
        """from_B_and_H recovers correct permeability for linear material."""
        H = jnp.array([100.0, 0.0, 0.0])
        B = jnp.array([50000.0, 0.0, 0.0])  # mu = 500
        energy = MagneticEnergyJAX.from_B_and_H(B, H)
        assert abs(energy.permeability - 500.0) < 1e-10

    def test_from_B_and_H_vacuum(self):
        """from_B_and_H for vacuum (mu=1)."""
        H = jnp.array([100.0, 0.0, 0.0])
        B = jnp.array([100.0, 0.0, 0.0])
        energy = MagneticEnergyJAX.from_B_and_H(B, H)
        assert abs(energy.permeability - 1.0) < 1e-10

    def test_pytree_flatten(self):
        """MagneticEnergyJAX can be flattened and unflattened."""
        energy = MagneticEnergyJAX(
            H_field=jnp.array([100.0, 0.0, 0.0]),
            permeability=5000.0,
        )
        leaves, treedef = jax.tree_util.tree_flatten(energy)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(restored.H_field, energy.H_field)
        assert restored.permeability == energy.permeability


# -- InductorEnergyJAX --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestInductorEnergyJAX:
    """Test InductorEnergyJAX (Art. 633)."""

    def setup_method(self):
        self.ind = InductorEnergyJAX(inductance=10.0)

    def test_from_current_basic(self):
        """U = (1/2) * L * I^2 for L=10, I=5: U = 125."""
        U = self.ind.from_current(5.0)
        expected = 0.5 * 10.0 * 5.0 ** 2  # = 125
        assert abs(U - expected) < 1e-10

    def test_from_current_zero(self):
        """Zero current gives zero energy."""
        U = self.ind.from_current(0.0)
        assert U == 0.0

    def test_from_flux_basic(self):
        """U = Phi^2/(2*L) for Phi=50, L=10: U = 125."""
        U = self.ind.from_flux(50.0)
        expected = 50.0 ** 2 / (2.0 * 10.0)  # = 125
        assert abs(U - expected) < 1e-10

    def test_from_flux_zero(self):
        """Zero flux gives zero energy."""
        U = self.ind.from_flux(0.0)
        assert U == 0.0

    def test_from_flux_current_basic(self):
        """U = (1/2) * Phi * I for Phi=50, I=5: U = 125."""
        U = self.ind.from_flux_current(50.0, 5.0)
        expected = 0.5 * 50.0 * 5.0  # = 125
        assert abs(U - expected) < 1e-10

    def test_consistency_LI2_vs_Phi2L(self):
        """LI^2 and Phi^2/L forms give same result (Phi=LI)."""
        L = 10.0
        I = 5.0
        Phi = L * I  # = 50
        ind = InductorEnergyJAX(inductance=L)
        U_li2 = ind.from_current(I)
        U_phi2l = ind.from_flux(Phi)
        assert abs(U_li2 - U_phi2l) < 1e-10

    def test_consistency_LI2_vs_PhiI(self):
        """LI^2 and PhiI forms give same result (Phi=LI)."""
        L = 10.0
        I = 5.0
        Phi = L * I
        ind = InductorEnergyJAX(inductance=L)
        U_li2 = ind.from_current(I)
        U_phi_i = ind.from_flux_current(Phi, I)
        assert abs(U_li2 - U_phi_i) < 1e-10

    def test_consistency_Phi2L_vs_PhiI(self):
        """Phi^2/L and PhiI forms give same result."""
        L = 10.0
        I = 5.0
        Phi = L * I
        ind = InductorEnergyJAX(inductance=L)
        U_phi2l = ind.from_flux(Phi)
        U_phi_i = ind.from_flux_current(Phi, I)
        assert abs(U_phi2l - U_phi_i) < 1e-10

    def test_pytree_flatten(self):
        """InductorEnergyJAX can be flattened and unflattened."""
        ind = InductorEnergyJAX(inductance=10.0)
        leaves, treedef = jax.tree_util.tree_flatten(ind)
        restored = jax.tree_util.tree_unflatten(treedef, leaves)
        assert restored.inductance == ind.inductance


# -- Magnetic: Standalone Functions --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticStandaloneFunctions:
    """Test standalone magnetic energy JAX functions."""

    def test_energy_density_vacuum(self):
        """u = (1/8*pi) * H^2 for vacuum."""
        H = jnp.array([1000.0, 0.0, 0.0])
        u = calc_magnetic_energy_density_jax(H)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_magnetic_material(self):
        """u = (1/8*pi) * mu * H^2 for mu=5000."""
        H = jnp.array([1000.0, 0.0, 0.0])
        u = calc_magnetic_energy_density_jax(H, permeability=5000.0)
        expected = 5000.0 * 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_zero_field(self):
        """Zero field gives zero energy density."""
        u = calc_magnetic_energy_density_jax(jnp.zeros(3))
        assert u == 0.0

    def test_energy_density_arbitrary_direction(self):
        """Energy density is isotropic."""
        H_mag = 1000.0
        u_x = calc_magnetic_energy_density_jax(jnp.array([H_mag, 0.0, 0.0]))
        u_y = calc_magnetic_energy_density_jax(jnp.array([0.0, H_mag, 0.0]))
        u_z = calc_magnetic_energy_density_jax(jnp.array([0.0, 0.0, H_mag]))
        assert jnp.isclose(u_x, u_y, rtol=1e-10)
        assert jnp.isclose(u_y, u_z, rtol=1e-10)

    def test_energy_density_from_BH_dot_parallel(self):
        """u = (1/8*pi) * B.H for parallel B and H."""
        H = jnp.array([100.0, 0.0, 0.0])
        B = jnp.array([50000.0, 0.0, 0.0])  # mu=500
        u = calc_energy_density_from_BH_dot_jax(B, H)
        # B.H = 100 * 50000 = 5_000_000
        expected = 5_000_000.0 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_from_BH_dot_non_parallel(self):
        """u = (1/8*pi) * B.H for non-parallel B and H."""
        H = jnp.array([100.0, 0.0, 0.0])
        B = jnp.array([80.0, 60.0, 0.0])  # anisotropic
        u = calc_energy_density_from_BH_dot_jax(B, H)
        # B.H = 100*80 + 0*60 = 8000
        expected = 8000.0 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_energy_density_from_BH_dot_zero(self):
        """Perpendicular B and H gives zero energy density."""
        H = jnp.array([100.0, 0.0, 0.0])
        B = jnp.array([0.0, 100.0, 0.0])
        u = calc_energy_density_from_BH_dot_jax(B, H)
        assert abs(u) < 1e-15

    def test_inductor_energy_LI2(self):
        """U = (1/2)*L*I^2."""
        U = calc_inductor_energy_jax(inductance=10.0, current=5.0)
        expected = 0.5 * 10.0 * 5.0 ** 2
        assert abs(U - expected) < 1e-10

    def test_inductor_energy_Phi2L(self):
        """U = Phi^2/(2*L)."""
        U = calc_inductor_energy_jax(inductance=10.0, flux=50.0)
        expected = 50.0 ** 2 / (2.0 * 10.0)
        assert abs(U - expected) < 1e-10

    def test_inductor_energy_no_params(self):
        """Missing current and flux raises error."""
        with pytest.raises(ValueError):
            calc_inductor_energy_jax(inductance=10.0)

    def test_total_magnetic_energy_jax(self):
        """U = u * V for uniform field."""
        H = jnp.array([1000.0, 0.0, 0.0])
        U = calc_total_magnetic_energy_jax(H, volume=1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi) * 1.0
        assert abs(U - expected) < 1e-6

    def test_total_magnetic_energy_various_volumes(self):
        """Total energy scales with volume."""
        H = jnp.array([500.0, 0.0, 0.0])
        U1 = calc_total_magnetic_energy_jax(H, volume=1.0)
        U10 = calc_total_magnetic_energy_jax(H, volume=10.0)
        assert abs(U10 - 10.0 * U1) < 1e-6


# -- Magnetic: Verification and Analysis --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticVerification:
    """Test verification and analysis functions for magnetic energy."""

    def test_verify_isotropy(self):
        """verify_magnetic_energy_density_jax confirms isotropy."""
        result = verify_magnetic_energy_density_jax(
            H_magnitude=1000.0, permeability=1.0
        )
        assert result["verified"] is True
        assert result["all_match"] is True

    def test_verify_expected_value(self):
        """Verification matches expected (1/8*pi)*mu*H^2."""
        H_mag = 1000.0
        mu = 1.0
        result = verify_magnetic_energy_density_jax(H_magnitude=H_mag, permeability=mu)
        expected = mu * H_mag ** 2 / (8.0 * jnp.pi)
        assert abs(result["expected"] - expected) < 1e-10

    def test_verify_magnetic_material(self):
        """Verification works for magnetic material (mu != 1)."""
        result = verify_magnetic_energy_density_jax(
            H_magnitude=500.0, permeability=5000.0
        )
        assert result["verified"] is True

    def test_analyze_magnetic_energy_basic(self):
        """Basic analysis returns expected keys."""
        H = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_magnetic_energy_jax(H)
        expected_keys = {
            "H_field", "H_magnitude", "H_direction",
            "B_field", "permeability", "energy_density",
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_analyze_with_volume(self):
        """Analysis with volume includes total_energy."""
        H = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_magnetic_energy_jax(H, volume=1.0)
        assert "total_energy" in result
        assert "volume" in result

    def test_analyze_with_inductor(self):
        """Analysis with inductor params includes inductor_energy."""
        H = jnp.array([1000.0, 0.0, 0.0])
        result = analyze_magnetic_energy_jax(
            H, volume=1.0, inductance=10.0, current=5.0
        )
        assert "inductor_energy" in result
        assert "energy_ratio" in result


# -- Magnetic: Auto-Diff --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticAutoDiff:
    """Test JAX auto-differentiation on magnetic energy formulas."""

    def test_grad_density_wrt_H(self):
        """dU/dH_x = (mu/(4*pi)) * H_x for energy density."""
        def density(Hx):
            H = jnp.array([Hx, 0.0, 0.0])
            return calc_magnetic_energy_density_jax(H)

        g = jax.grad(density)(1000.0)
        expected = 1000.0 / (4.0 * jnp.pi)
        assert abs(g - expected) < 1e-8

    def test_grad_density_wrt_permeability(self):
        """dU/d(mu) = H^2/(8*pi)."""
        def density_mu(mu):
            return calc_magnetic_energy_density_jax(
                jnp.array([1000.0, 0.0, 0.0]), permeability=mu
            )

        g = jax.grad(density_mu)(1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-6

    def test_grad_inductor_energy_wrt_I(self):
        """dU/dI = L*I for U = (1/2)*L*I^2."""
        def energy_I(I):
            return calc_inductor_energy_jax(inductance=10.0, current=I)

        g = jax.grad(energy_I)(5.0)
        expected = 10.0 * 5.0  # = 50
        assert abs(g - expected) < 1e-10

    def test_grad_inductor_energy_wrt_L(self):
        """dU/dL = (1/2)*I^2."""
        def energy_L(L):
            return calc_inductor_energy_jax(inductance=L, current=5.0)

        g = jax.grad(energy_L)(10.0)
        expected = 0.5 * 5.0 ** 2  # = 12.5
        assert abs(g - expected) < 1e-10

    def test_grad_inductor_energy_wrt_flux(self):
        """dU/dPhi = Phi/L for U = Phi^2/(2*L)."""
        def energy_phi(Phi):
            return calc_inductor_energy_jax(inductance=10.0, flux=Phi)

        g = jax.grad(energy_phi)(50.0)
        expected = 50.0 / 10.0  # = 5
        assert abs(g - expected) < 1e-10

    def test_grad_total_energy_wrt_volume(self):
        """dU/dV = u (energy density)."""
        def total_energy_V(vol):
            return calc_total_magnetic_energy_jax(
                jnp.array([1000.0, 0.0, 0.0]), vol
            )

        g = jax.grad(total_energy_V)(1.0)
        expected = 1000.0 ** 2 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-6

    def test_grad_BH_dot_wrt_H(self):
        """d(B.H)/dH = B for dot product density."""
        B = jnp.array([50000.0, 0.0, 0.0])

        def density_BH(Hx):
            H = jnp.array([Hx, 0.0, 0.0])
            return calc_energy_density_from_BH_dot_jax(B, H)

        g = jax.grad(density_BH)(100.0)
        expected = 50000.0 / (8.0 * jnp.pi)
        assert abs(g - expected) < 1e-10


# -- Magnetic: JIT --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticJIT:
    """Test JIT compilation compatibility for magnetic energy."""

    def test_jit_energy_density(self):
        """Energy density works under JIT."""

        @jax.jit
        def jit_density(H, mu):
            return calc_magnetic_energy_density_jax(H, permeability=mu)

        u = jit_density(jnp.array([1000.0, 0.0, 0.0]), 1.0)
        assert u > 0

    def test_jit_total_energy(self):
        """Total energy works under JIT."""

        @jax.jit
        def jit_total(H, vol, mu):
            return calc_total_magnetic_energy_jax(H, vol, permeability=mu)

        U = jit_total(jnp.array([1000.0, 0.0, 0.0]), 1.0, 1.0)
        assert U > 0

    def test_jit_inductor_energy(self):
        """Inductor energy works under JIT."""

        @jax.jit
        def jit_ind(L, I):
            return calc_inductor_energy_jax(L, current=I)

        U = jit_ind(10.0, 5.0)
        expected = 0.5 * 10.0 * 5.0 ** 2
        assert abs(U - expected) < 1e-10

    def test_jit_magnetic_energy_class(self):
        """MagneticEnergyJAX works under JIT."""

        @jax.jit
        def jit_class_density(H, mu):
            e = MagneticEnergyJAX(H_field=H, permeability=mu)
            return e.energy_density

        u = jit_class_density(jnp.array([500.0, 0.0, 0.0]), 5000.0)
        expected = 5000.0 * 500.0 ** 2 / (8.0 * jnp.pi)
        assert abs(u - expected) < 1e-6

    def test_jit_inductor_class(self):
        """InductorEnergyJAX works under JIT."""

        @jax.jit
        def jit_ind_class(L, I):
            ind = InductorEnergyJAX(inductance=L)
            return ind.from_current(I)

        U = jit_ind_class(10.0, 5.0)
        expected = 0.5 * 10.0 * 5.0 ** 2
        assert abs(U - expected) < 1e-10


# -- Magnetic: vmap --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticVmap:
    """Test batched evaluation via vmap for magnetic energy."""

    def test_vmap_energy_density(self):
        """vmap over batch of H fields."""
        H_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [500.0, 0.0, 0.0],
        ])
        densities = jax.vmap(calc_magnetic_energy_density_jax)(H_batch)
        assert densities.shape == (3,)
        # Densities should be monotonically increasing (H^2 relationship)
        assert densities[0] < densities[1] < densities[2]

    def test_vmap_energy_density_magnetic_material(self):
        """vmap with fixed permeability over batch of H fields."""
        H_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
        ])
        densities = jax.vmap(lambda H: calc_magnetic_energy_density_jax(H, 5000.0))(H_batch)
        assert densities.shape == (2,)

    def test_vmap_inductor_energy(self):
        """vmap over batch of currents."""
        currents = jnp.array([1.0, 5.0, 10.0, 20.0])
        energies = jax.vmap(lambda I: calc_inductor_energy_jax(10.0, current=I))(currents)
        assert energies.shape == (4,)
        # U = 0.5*10*I^2: 5, 125, 500, 2000
        expected = 0.5 * 10.0 * currents ** 2
        assert jnp.allclose(energies, expected, atol=1e-10)

    def test_vmap_total_energy(self):
        """vmap over batch of H fields for total energy."""
        H_batch = jnp.array([
            [100.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [300.0, 0.0, 0.0],
        ])
        energies = jax.vmap(lambda H: calc_total_magnetic_energy_jax(H, volume=1.0))(H_batch)
        assert energies.shape == (3,)
        assert energies[0] < energies[1] < energies[2]


# -- Magnetic: NumPy Cross-Validation --


@pytest.mark.skipif(not HAS_MAGNETIC_ENERGY, reason="maxwell.jax.electromagnetism.magnetic_energy not installed")
class TestMagneticNumpyCrossValidation:
    """Test JAX magnetic energy results against NumPy reference implementation."""

    def test_energy_density_matches_numpy(self):
        """JAX magnetic energy density matches NumPy."""
        from maxwell.electromagnetism.energy.magnetic import (
            calc_magnetic_energy_density,
        )

        H_np = np.array([1000.0, 500.0, 250.0])
        H_jax = jnp.array([1000.0, 500.0, 250.0])

        u_np = calc_magnetic_energy_density(H_np, permeability=5000.0)
        u_jax = calc_magnetic_energy_density_jax(H_jax, permeability=5000.0)

        assert abs(float(u_jax) - u_np) < 1e-10

    def test_total_energy_matches_numpy(self):
        """JAX total magnetic energy matches NumPy."""
        from maxwell.electromagnetism.energy.magnetic import (
            calc_total_magnetic_energy,
        )

        H_np = np.array([1000.0, 0.0, 0.0])
        H_jax = jnp.array([1000.0, 0.0, 0.0])

        U_np = calc_total_magnetic_energy(H_np, volume=5.0, permeability=1.0)
        U_jax = calc_total_magnetic_energy_jax(H_jax, volume=5.0, permeability=1.0)

        assert abs(float(U_jax) - U_np) < 1e-10

    def test_BH_dot_matches_numpy(self):
        """JAX B.H dot product matches NumPy."""
        from maxwell.electromagnetism.energy.magnetic import (
            calc_energy_density_from_BH_dot,
        )

        B_np = np.array([50000.0, 25000.0, 0.0])
        H_np = np.array([100.0, 50.0, 0.0])
        B_jax = jnp.array([50000.0, 25000.0, 0.0])
        H_jax = jnp.array([100.0, 50.0, 0.0])

        u_np = calc_energy_density_from_BH_dot(B_np, H_np)
        u_jax = calc_energy_density_from_BH_dot_jax(B_jax, H_jax)

        assert abs(float(u_jax) - u_np) < 1e-10

    def test_class_energy_density_matches_numpy(self):
        """MagneticEnergyJAX.energy_density matches NumPy."""
        from maxwell.electromagnetism.energy.magnetic import MagneticEnergy

        H_np = np.array([1000.0, 0.0, 0.0])
        np_energy = MagneticEnergy(H_field=H_np, permeability=5000.0)

        jax_energy = MagneticEnergyJAX(
            H_field=jnp.array([1000.0, 0.0, 0.0]),
            permeability=5000.0,
        )

        assert abs(float(jax_energy.energy_density) - np_energy.energy_density) < 1e-10
