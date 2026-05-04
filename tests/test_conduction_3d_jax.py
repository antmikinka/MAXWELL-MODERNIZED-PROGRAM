"""Tests for Conduction3DJAX -- Part II Electrokinematics (Arts. 285-296, 297-324)."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax.electromagnetism.conduction_3d import (
    Conduction3DJAX,
    SpreadingResistanceJAX,
    EffectiveConductivityJAX,
    ohms_law_3d_jax,
    electric_field_from_current_density_jax,
    conduction_power_density_jax,
    spherical_spreading_resistance_jax,
    hemispherical_spreading_resistance_jax,
    circular_contact_resistance_jax,
    maxwell_garnett_conductivity_jax,
    effective_conductivity_series_jax,
    effective_conductivity_parallel_jax,
    verify_conduction_3d_jax,
    analyze_conduction_jax,
)

TOL = 1e-10


# -- TestConduction3DJAXPytree ----------------------------------------------------

class TestConduction3DJAXPytree:
    """Flatten/unflatten, jit, vmap."""

    def test_flatten_unflatten_scalar(self):
        obj = Conduction3DJAX(conductivity=1.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.conductivity) == pytest.approx(1.0)

    def test_flatten_unflatten_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        obj = Conduction3DJAX(conductivity=sigma)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(reconstructed.conductivity, sigma)

    def test_jit_compatible(self):
        obj = Conduction3DJAX(conductivity=2.0)
        jit_fn = jax.jit(lambda o: o.current_density(jnp.array([1.0, 0.0, 0.0])))
        result = jit_fn(obj)
        assert jnp.allclose(result, jnp.array([2.0, 0.0, 0.0]))


# -- TestConduction3DJAXScalar ----------------------------------------------------

class TestConduction3DJAXScalar:
    """Scalar (isotropic) conductivity operations."""

    def test_current_density_scalar(self):
        obj = Conduction3DJAX(conductivity=2.0)
        E = jnp.array([1.0, 2.0, 3.0])
        J = obj.current_density(E)
        assert jnp.allclose(J, jnp.array([2.0, 4.0, 6.0]))

    def test_electric_field_scalar(self):
        obj = Conduction3DJAX(conductivity=2.0)
        J = jnp.array([2.0, 4.0, 6.0])
        E = obj.electric_field(J)
        assert jnp.allclose(E, jnp.array([1.0, 2.0, 3.0]))

    def test_power_density_scalar(self):
        obj = Conduction3DJAX(conductivity=2.0)
        E = jnp.array([1.0, 0.0, 0.0])
        P = obj.power_density(E)
        assert float(P) == pytest.approx(2.0)

    def test_power_density_multi_axis(self):
        obj = Conduction3DJAX(conductivity=1.0)
        E = jnp.array([1.0, 2.0, 3.0])
        P = obj.power_density(E)
        # P = sigma * (1+4+9) = 14
        assert float(P) == pytest.approx(14.0)

    def test_from_resistivity_scalar(self):
        obj = Conduction3DJAX.from_resistivity(jnp.array(0.5))
        assert float(obj.conductivity) == pytest.approx(2.0)

    def test_is_anisotropic_scalar(self):
        obj = Conduction3DJAX(conductivity=1.0)
        assert obj.is_anisotropic is False


# -- TestConduction3DJAXTensor ----------------------------------------------------

class TestConduction3DJAXTensor:
    """Tensor (anisotropic) conductivity operations."""

    def test_current_density_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        obj = Conduction3DJAX(conductivity=sigma)
        E = jnp.array([1.0, 1.0, 1.0])
        J = obj.current_density(E)
        assert jnp.allclose(J, jnp.array([2.0, 1.0, 0.5]))

    def test_electric_field_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        obj = Conduction3DJAX(conductivity=sigma)
        J = jnp.array([2.0, 1.0, 0.5])
        E = obj.electric_field(J)
        assert jnp.allclose(E, jnp.array([1.0, 1.0, 1.0]))

    def test_power_density_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        obj = Conduction3DJAX(conductivity=sigma)
        E = jnp.array([1.0, 1.0, 1.0])
        P = obj.power_density(E)
        # P = 2*1 + 1*1 + 0.5*1 = 3.5
        assert float(P) == pytest.approx(3.5)

    def test_is_anisotropic_tensor(self):
        sigma = jnp.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])
        obj = Conduction3DJAX(conductivity=sigma)
        assert obj.is_anisotropic is True

    def test_from_resistivity_tensor(self):
        rho = jnp.array([[0.5, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        obj = Conduction3DJAX.from_resistivity(rho)
        # sigma = rho^-1 = diag(2, 1, 0.5)
        assert jnp.allclose(obj.conductivity, jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]]))


# -- TestConduction3DJAXEdgeCases -------------------------------------------------

class TestConduction3DJAXEdgeCases:
    """Zero conductivity, unit E, roundtrip."""

    def test_zero_conductivity(self):
        obj = Conduction3DJAX(conductivity=0.0)
        E = jnp.array([1.0, 0.0, 0.0])
        J = obj.current_density(E)
        assert jnp.allclose(J, jnp.array([0.0, 0.0, 0.0]))

    def test_unit_field(self):
        obj = Conduction3DJAX(conductivity=3.0)
        E = jnp.array([1.0, 0.0, 0.0])
        J = obj.current_density(E)
        assert float(J[0]) == pytest.approx(3.0)

    def test_roundtrip_scalar(self):
        obj = Conduction3DJAX(conductivity=2.5)
        E_orig = jnp.array([1.0, 2.0, 3.0])
        J = obj.current_density(E_orig)
        E_recovered = obj.electric_field(J)
        assert jnp.allclose(E_recovered, E_orig)

    def test_roundtrip_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        obj = Conduction3DJAX(conductivity=sigma)
        E_orig = jnp.array([1.0, 2.0, 3.0])
        J = obj.current_density(E_orig)
        E_recovered = obj.electric_field(J)
        assert jnp.allclose(E_recovered, E_orig)


# -- TestSpreadingResistanceJAXPytree ---------------------------------------------

class TestSpreadingResistanceJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.conductivity) == pytest.approx(1.0)

    def test_jit_spherical(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        jit_fn = jax.jit(lambda o: o.spherical_surface(0.1))
        result = jit_fn(obj)
        expected = 1.0 / (4.0 * np.pi * 1.0 * 0.1)
        assert float(result) == pytest.approx(expected)

    def test_tree_map(self):
        obj = SpreadingResistanceJAX(conductivity=2.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.conductivity) == pytest.approx(4.0)


# -- TestSpreadingResistanceJAXSpherical ------------------------------------------

class TestSpreadingResistanceJAXSpherical:
    """Spherical spreading resistance values."""

    def test_sphere_r01_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.spherical_surface(0.1)
        expected = 1.0 / (4.0 * np.pi * 1.0 * 0.1)
        assert float(R) == pytest.approx(expected)

    def test_sphere_r1_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.spherical_surface(1.0)
        expected = 1.0 / (4.0 * np.pi)
        assert float(R) == pytest.approx(expected)

    def test_sphere_higher_sigma(self):
        obj = SpreadingResistanceJAX(conductivity=10.0)
        R = obj.spherical_surface(0.1)
        expected = 1.0 / (4.0 * np.pi * 10.0 * 0.1)
        assert float(R) == pytest.approx(expected)

    def test_standalone_spherical(self):
        R = spherical_spreading_resistance_jax(1.0, 0.1)
        expected = 1.0 / (4.0 * np.pi * 1.0 * 0.1)
        assert float(R) == pytest.approx(expected)


# -- TestSpreadingResistanceJAXHemispherical --------------------------------------

class TestSpreadingResistanceJAXHemispherical:
    """Hemispherical spreading resistance values."""

    def test_hemisphere_r01_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.hemispherical_surface(0.1)
        expected = 1.0 / (2.0 * np.pi * 1.0 * 0.1)
        assert float(R) == pytest.approx(expected)

    def test_hemisphere_r1_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.hemispherical_surface(1.0)
        expected = 1.0 / (2.0 * np.pi)
        assert float(R) == pytest.approx(expected)

    def test_hemisphere_ratio_to_sphere(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R_hemi = obj.hemispherical_surface(0.1)
        R_sphere = obj.spherical_surface(0.1)
        assert float(R_hemi) == pytest.approx(float(R_sphere) * 2.0)

    def test_standalone_hemispherical(self):
        R = hemispherical_spreading_resistance_jax(1.0, 0.5)
        expected = 1.0 / (2.0 * np.pi * 1.0 * 0.5)
        assert float(R) == pytest.approx(expected)


# -- TestSpreadingResistanceJAXCircular -------------------------------------------

class TestSpreadingResistanceJAXCircular:
    """Circular contact resistance."""

    def test_circular_r01_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.circular_contact(0.1)
        expected = 1.0 / (4.0 * 1.0 * 0.1)
        assert float(R) == pytest.approx(expected)

    def test_circular_r1_sigma1(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R = obj.circular_contact(1.0)
        expected = 1.0 / 4.0
        assert float(R) == pytest.approx(expected)

    def test_standalone_circular(self):
        R = circular_contact_resistance_jax(1.0, 0.1)
        expected = 1.0 / (4.0 * 1.0 * 0.1)
        assert float(R) == pytest.approx(expected)

    def test_circular_vs_hemispherical(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        R_circular = obj.circular_contact(0.1)
        R_hemi = obj.hemispherical_surface(0.1)
        # Circular = 1/(4*sigma*r), Hemisphere = 1/(2*pi*sigma*r)
        # circular/hemi = pi/2
        ratio = float(R_circular) / float(R_hemi)
        assert ratio == pytest.approx(np.pi / 2.0)


# -- TestEffectiveConductivityJAXPytree -------------------------------------------

class TestEffectiveConductivityJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = EffectiveConductivityJAX(
            sigma_matrix=1.0, sigma_inclusion=0.5, volume_fraction=0.3
        )
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 3
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.sigma_matrix) == pytest.approx(1.0)
        assert float(reconstructed.sigma_inclusion) == pytest.approx(0.5)
        assert float(reconstructed.volume_fraction) == pytest.approx(0.3)

    def test_jit_compatible(self):
        obj = EffectiveConductivityJAX(sigma_matrix=1.0, sigma_inclusion=0.5, volume_fraction=0.3)
        jit_fn = jax.jit(lambda o: o.parallel_mix())
        result = jit_fn(obj)
        assert float(result) == pytest.approx(0.85)

    def test_tree_map(self):
        obj = EffectiveConductivityJAX(sigma_matrix=1.0, sigma_inclusion=2.0, volume_fraction=0.5)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.sigma_matrix) == pytest.approx(2.0)
        assert float(doubled.sigma_inclusion) == pytest.approx(4.0)
        assert float(doubled.volume_fraction) == pytest.approx(1.0)


# -- TestEffectiveConductivityJAXMixing -------------------------------------------

class TestEffectiveConductivityJAXMixing:
    """Series and parallel mixing models."""

    def test_series_equal_sigma(self):
        # f=0.3, sigma1=1, sigma2=1 -> sigma_eff = 1
        result = effective_conductivity_series_jax(1.0, 1.0, 0.3)
        assert float(result) == pytest.approx(1.0)

    def test_parallel_equal_sigma(self):
        # f=0.3, sigma1=1, sigma2=1 -> sigma_eff = 1
        result = effective_conductivity_parallel_jax(1.0, 1.0, 0.3)
        assert float(result) == pytest.approx(1.0)

    def test_series_between_bounds(self):
        # Series mixing (harmonic mean) gives value between sigma1 and sigma2
        sigma1, sigma2, f = 1.0, 10.0, 0.5
        result = effective_conductivity_series_jax(sigma1, sigma2, f)
        # Harmonic mean is always between the two values
        assert min(sigma1, sigma2) <= float(result) <= max(sigma1, sigma2)

    def test_parallel_upper_bound(self):
        # Parallel should be between sigma1 and sigma2
        sigma1, sigma2, f = 1.0, 10.0, 0.5
        result = effective_conductivity_parallel_jax(sigma1, sigma2, f)
        expected = 0.5 * 1.0 + 0.5 * 10.0
        assert float(result) == pytest.approx(expected)

    def test_series_zero_inclusion(self):
        # sigma2=0 -> safe_div(f, 0) = 0, so inv_sigma = 0 + (1-f)/sigma1
        # sigma_eff = 1 / ((1-f)/sigma1) = sigma1/(1-f) = 1/0.5 = 2
        result = effective_conductivity_series_jax(1.0, 0.0, 0.5)
        assert float(result) == pytest.approx(2.0)


# -- TestEffectiveConductivityJAXMaxwellGarnett -----------------------------------

class TestEffectiveConductivityJAXMaxwellGarnett:
    """Maxwell-Garnett formula behavior."""

    def test_equal_conductivities(self):
        # sigma_m = sigma_i -> sigma_eff = sigma_m
        result = maxwell_garnett_conductivity_jax(1.0, 1.0, 0.3)
        assert float(result) == pytest.approx(1.0)

    def test_zero_volume_fraction(self):
        # f=0 -> sigma_eff = sigma_m
        result = maxwell_garnett_conductivity_jax(1.0, 10.0, 0.0)
        assert float(result) == pytest.approx(1.0)

    def test_highly_conductive_inclusions(self):
        # sigma_i >> sigma_m, f>0 -> sigma_eff > sigma_m
        result = maxwell_garnett_conductivity_jax(1.0, 1000.0, 0.3)
        assert float(result) > 1.0

    def test_insulating_inclusions(self):
        # sigma_i = 0, f>0 -> sigma_eff < sigma_m
        result = maxwell_garnett_conductivity_jax(1.0, 0.0, 0.3)
        assert float(result) < 1.0


# -- TestStandaloneConductionFunctions --------------------------------------------

class TestStandaloneConductionFunctions:
    """All standalone function correctness."""

    def test_ohms_law_3d_scalar(self):
        E = jnp.array([1.0, 2.0, 3.0])
        J = ohms_law_3d_jax(E, jnp.array(2.0))
        assert jnp.allclose(J, jnp.array([2.0, 4.0, 6.0]))

    def test_ohms_law_3d_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        E = jnp.array([1.0, 1.0, 1.0])
        J = ohms_law_3d_jax(E, sigma)
        assert jnp.allclose(J, jnp.array([2.0, 1.0, 0.5]))

    def test_electric_field_from_j_scalar(self):
        J = jnp.array([2.0, 4.0, 6.0])
        E = electric_field_from_current_density_jax(J, jnp.array(2.0))
        assert jnp.allclose(E, jnp.array([1.0, 2.0, 3.0]))

    def test_electric_field_from_j_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        J = jnp.array([2.0, 1.0, 0.5])
        E = electric_field_from_current_density_jax(J, sigma)
        assert jnp.allclose(E, jnp.array([1.0, 1.0, 1.0]))

    def test_conduction_power_density_scalar(self):
        E = jnp.array([1.0, 2.0, 3.0])
        P = conduction_power_density_jax(E, jnp.array(1.0))
        assert float(P) == pytest.approx(14.0)

    def test_conduction_power_density_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        E = jnp.array([1.0, 1.0, 1.0])
        P = conduction_power_density_jax(E, sigma)
        assert float(P) == pytest.approx(3.5)

    def test_maxwell_garnett_standalone(self):
        result = maxwell_garnett_conductivity_jax(1.0, 2.0, 0.5)
        # sigma_eff = 1 * (2+2-2*0.5*(-1)) / (2+2+0.5*(-1)) = 1 * (4+1) / (4-0.5) = 5/3.5
        expected = 1.0 * (2.0 + 2.0 - 2.0 * 0.5 * (1.0 - 2.0)) / (2.0 + 2.0 + 0.5 * (1.0 - 2.0))
        assert float(result) == pytest.approx(expected)

    def test_effective_series_standalone(self):
        result = effective_conductivity_series_jax(1.0, 2.0, 0.5)
        # 1 / (0.5/2 + 0.5/1) = 1 / (0.25 + 0.5) = 1/0.75 = 4/3
        assert float(result) == pytest.approx(4.0 / 3.0)


# -- TestJITConduction3D ----------------------------------------------------------

class TestJITConduction3D:
    """JIT compilation for all classes."""

    def test_jit_conduction3d_current_density(self):
        @jax.jit
        def compute(sigma_val, E):
            obj = Conduction3DJAX(conductivity=sigma_val)
            return obj.current_density(E)
        result = compute(3.0, jnp.array([1.0, 0.0, 0.0]))
        assert jnp.allclose(result, jnp.array([3.0, 0.0, 0.0]))

    def test_jit_spreading_resistance(self):
        obj = SpreadingResistanceJAX(conductivity=1.0)
        jit_fn = jax.jit(lambda o: (o.spherical_surface(0.1), o.hemispherical_surface(0.1), o.circular_contact(0.1)))
        results = jit_fn(obj)
        assert all(float(r) > 0 for r in results)

    def test_jit_effective_conductivity(self):
        obj = EffectiveConductivityJAX(sigma_matrix=1.0, sigma_inclusion=2.0, volume_fraction=0.3)
        jit_fn = jax.jit(lambda o: (o.series_mix(), o.parallel_mix(), o.maxwell_garnett(), o.brickell()))
        results = jit_fn(obj)
        assert all(float(r) > 0 for r in results)

    def test_jit_verify_conduction(self):
        # verify_conduction_3d_jax uses bool() so it can't be JIT'd directly.
        # Instead, JIT the core computations it uses.
        @jax.jit
        def compute_J_and_E_roundtrip(E, sigma):
            J = ohms_law_3d_jax(E, sigma)
            E_recovered = electric_field_from_current_density_jax(J, sigma)
            return E_recovered
        E_recovered = compute_J_and_E_roundtrip(jnp.array([1.0, 0.0, 0.0]), jnp.array(2.0))
        assert jnp.allclose(E_recovered, jnp.array([1.0, 0.0, 0.0]))


# -- TestAutoDiffConduction -------------------------------------------------------

class TestAutoDiffConduction:
    """Gradients through conduction functions."""

    def test_grad_current_density_wrt_E(self):
        grad_fn = jax.grad(lambda Ex: ohms_law_3d_jax(jnp.array([Ex, 0.0, 0.0]), jnp.array(2.0))[0])
        g = grad_fn(1.0)
        assert float(g) == pytest.approx(2.0, abs=1e-6)

    def test_grad_power_density_wrt_E(self):
        grad_fn = jax.grad(lambda Ex: conduction_power_density_jax(jnp.array([Ex, 0.0, 0.0]), jnp.array(2.0)))
        g = grad_fn(1.0)
        # P = 2*Ex^2, dP/dEx = 4*Ex = 4
        assert float(g) == pytest.approx(4.0, abs=1e-6)

    def test_grad_spherical_resistance_wrt_sigma(self):
        grad_fn = jax.grad(lambda s: spherical_spreading_resistance_jax(s, 0.1))
        g = grad_fn(1.0)
        # R = 1/(4*pi*sigma*r), dR/dsigma = -1/(4*pi*sigma^2*r)
        expected = -1.0 / (4.0 * np.pi * 1.0 ** 2 * 0.1)
        assert float(g) == pytest.approx(expected, abs=1e-6)

    def test_grad_maxwell_garnett_wrt_vol_frac(self):
        grad_fn = jax.grad(lambda f: maxwell_garnett_conductivity_jax(1.0, 2.0, f))
        g = grad_fn(0.3)
        assert float(g) > 0  # Higher inclusion fraction -> higher sigma_eff


# -- TestVmapConduction -----------------------------------------------------------

class TestVmapConduction:
    """Vectorization over arrays of inputs."""

    def test_vmap_current_density(self):
        E_batch = jnp.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]])
        Js = jax.vmap(lambda E: ohms_law_3d_jax(E, jnp.array(2.0)))(E_batch)
        expected = jnp.array([[2.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 6.0]])
        assert jnp.allclose(Js, expected)

    def test_vmap_power_density(self):
        E_batch = jnp.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
        Ps = jax.vmap(lambda E: conduction_power_density_jax(E, jnp.array(1.0)))(E_batch)
        expected = jnp.array([1.0, 4.0, 9.0])
        assert jnp.allclose(Ps, expected)

    def test_vmap_spreading_resistance(self):
        radii = jnp.array([0.1, 0.2, 0.5])
        Rs = jax.vmap(lambda r: spherical_spreading_resistance_jax(1.0, r))(radii)
        assert Rs.shape == (3,)
        assert float(Rs[0]) > float(Rs[1]) > float(Rs[2])

    def test_vmap_effective_conductivity(self):
        fracs = jnp.array([0.1, 0.3, 0.5, 0.7, 0.9])
        results = jax.vmap(lambda f: effective_conductivity_parallel_jax(1.0, 10.0, f))(fracs)
        assert results.shape == (5,)
        # Monotonically increasing with f
        assert jnp.all(jnp.diff(results) > 0)


# -- TestNumPyConductionComparison ------------------------------------------------

class TestNumPyConductionComparison:
    """JAX vs NumPy comparison."""

    def test_ohms_law_numpy_equiv(self):
        E = np.array([1.0, 2.0, 3.0])
        sigma = 2.0
        np_result = sigma * E
        jax_result = ohms_law_3d_jax(jnp.array(E), jnp.array(sigma))
        assert jnp.allclose(jnp.array(jax_result), jnp.array(np_result))

    def test_spreading_resistance_numpy_equiv(self):
        sigma, r = 1.0, 0.1
        np_result = 1.0 / (4.0 * np.pi * sigma * r)
        jax_result = spherical_spreading_resistance_jax(sigma, r)
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_effective_parallel_numpy_equiv(self):
        sigma1, sigma2, f = 1.0, 10.0, 0.3
        np_result = (1.0 - f) * sigma1 + f * sigma2
        jax_result = effective_conductivity_parallel_jax(sigma1, sigma2, f)
        assert float(jax_result) == pytest.approx(float(np_result))


# -- TestVerifyConduction3D -------------------------------------------------------

class TestVerifyConduction3D:
    """verify_conduction_3d_jax behavior."""

    def test_verify_passes_scalar(self):
        result = verify_conduction_3d_jax(
            E=jnp.array([1.0, 2.0, 3.0]),
            sigma=jnp.array(2.0),
        )
        assert bool(result["verified"]) is True
        assert jnp.allclose(result["J"], jnp.array([2.0, 4.0, 6.0]))

    def test_verify_passes_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        result = verify_conduction_3d_jax(
            E=jnp.array([1.0, 1.0, 1.0]),
            sigma=sigma,
        )
        assert bool(result["verified"]) is True

    def test_verify_keys_present(self):
        result = verify_conduction_3d_jax()
        expected_keys = {"J", "E_recovered", "E_error", "P_direct", "P_from_JE",
                        "P_error", "E_roundtrip_ok", "P_consistent", "verified"}
        assert set(result.keys()) == expected_keys


# -- TestAnalyzeConduction --------------------------------------------------------

class TestAnalyzeConduction:
    """analyze_conduction_jax behavior."""

    def test_analyze_scalar(self):
        result = analyze_conduction_jax(
            E=jnp.array([1.0, 0.0, 0.0]),
            sigma=jnp.array(2.0),
        )
        assert "current_density" in result
        assert "power_density" in result
        assert result["is_anisotropic"] is False
        assert jnp.allclose(result["current_density"], jnp.array([2.0, 0.0, 0.0]))

    def test_analyze_tensor(self):
        sigma = jnp.array([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]])
        result = analyze_conduction_jax(
            E=jnp.array([1.0, 1.0, 1.0]),
            sigma=sigma,
        )
        assert result["is_anisotropic"] is True
        assert "principal_conductivities" in result
        assert "anisotropy_ratio" in result

    def test_analyze_with_geometry(self):
        result = analyze_conduction_jax(
            E=jnp.array([1.0, 0.0, 0.0]),
            sigma=jnp.array(1.0),
            geometry={"type": "sphere", "radius": 0.1},
        )
        assert "spreading_resistance" in result
        expected_R = 1.0 / (4.0 * np.pi * 1.0 * 0.1)
        assert float(result["spreading_resistance"]) == pytest.approx(expected_R)

    def test_analyze_with_hemisphere_geometry(self):
        result = analyze_conduction_jax(
            E=jnp.array([1.0, 0.0, 0.0]),
            sigma=jnp.array(1.0),
            geometry={"type": "hemisphere", "radius": 0.5},
        )
        assert "spreading_resistance" in result
        expected_R = 1.0 / (2.0 * np.pi * 1.0 * 0.5)
        assert float(result["spreading_resistance"]) == pytest.approx(expected_R)
