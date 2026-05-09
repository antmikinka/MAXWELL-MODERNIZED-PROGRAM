"""Tests for Ohm's law JAX adapter -- Part II Electrokinematics (Arts. 230-280)."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax.electromagnetism.ohms_law import (
    ConductivityJAX,
    OhmsLawJAX,
    PowerDissipationJAX,
    ResistanceJAX,
    analyze_ohms_law_jax,
    calc_conductance_jax,
    calc_conductivity_jax,
    calc_current_jax,
    calc_power_from_I2R_jax,
    calc_power_from_IV_jax,
    calc_power_from_V2R_jax,
    calc_resistance_jax,
    calc_resistivity_jax,
    calc_voltage_jax,
    parallel_resistance_jax,
    series_resistance_jax,
    temperature_corrected_resistance_jax,
    verify_ohms_law_jax,
)

TOL = 1e-10


# -- TestOhmsLawJAXPytree ----------------------------------------------------------


class TestOhmsLawJAXPytree:
    """Flatten/unflatten, jit, vmap, grad."""

    def test_flatten_unflatten(self):
        obj = OhmsLawJAX(voltage=10.0, current=2.0, resistance=5.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 3
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.voltage) == pytest.approx(10.0)
        assert float(reconstructed.current) == pytest.approx(2.0)
        assert float(reconstructed.resistance) == pytest.approx(5.0)

    def test_jit_compatible(self):
        obj = OhmsLawJAX(voltage=10.0, current=2.0, resistance=5.0)
        jit_computed = jax.jit(lambda o: o.computed_voltage)(obj)
        assert float(jit_computed) == pytest.approx(10.0)

    def test_vmap_over_voltage(self):
        obj = OhmsLawJAX(voltage=0.0, current=1.0, resistance=1.0)
        voltages = jnp.array([1.0, 2.0, 3.0])
        results = jax.vmap(
            lambda v: OhmsLawJAX(
                voltage=v, current=1.0, resistance=1.0
            ).computed_current
        )(voltages)
        assert results.shape == (3,)
        assert float(results[0]) == pytest.approx(1.0)
        assert float(results[1]) == pytest.approx(2.0)
        assert float(results[2]) == pytest.approx(3.0)

    def test_grad_through_voltage(self):
        def compute_v(I, R):
            return OhmsLawJAX._voltage_jit(I, R)

        grad_fn = jax.grad(compute_v)
        g_I = grad_fn(2.0, 5.0)
        assert float(g_I) == pytest.approx(5.0, abs=1e-6)


# -- TestOhmsLawJAXProperties ------------------------------------------------------


class TestOhmsLawJAXProperties:
    """All 5 properties correct values."""

    def test_computed_voltage(self):
        obj = OhmsLawJAX(current=2.0, resistance=5.0)
        assert float(obj.computed_voltage) == pytest.approx(10.0)

    def test_computed_current(self):
        obj = OhmsLawJAX(voltage=10.0, resistance=5.0)
        assert float(obj.computed_current) == pytest.approx(2.0)

    def test_computed_resistance(self):
        obj = OhmsLawJAX(voltage=10.0, current=2.0)
        assert float(obj.computed_resistance) == pytest.approx(5.0)

    def test_conductance(self):
        obj = OhmsLawJAX(resistance=5.0)
        assert float(obj.conductance) == pytest.approx(0.2)

    def test_power(self):
        obj = OhmsLawJAX(voltage=10.0, current=2.0)
        assert float(obj.power) == pytest.approx(20.0)

    def test_computed_voltage_array(self):
        obj = OhmsLawJAX(current=jnp.array([1.0, 2.0, 3.0]), resistance=2.0)
        result = obj.computed_voltage
        assert jnp.allclose(result, jnp.array([2.0, 4.0, 6.0]))

    def test_computed_current_zero_resistance(self):
        obj = OhmsLawJAX(voltage=10.0, resistance=0.0)
        assert float(obj.computed_current) == pytest.approx(0.0)

    def test_computed_resistance_zero_current(self):
        obj = OhmsLawJAX(voltage=10.0, current=0.0)
        assert float(obj.computed_resistance) == pytest.approx(0.0)


# -- TestOhmsLawJAXMethods ---------------------------------------------------------


class TestOhmsLawJAXMethods:
    """voltage_from, current_from, resistance_from."""

    def test_voltage_from(self):
        obj = OhmsLawJAX()
        assert float(obj.voltage_from(3.0, 4.0)) == pytest.approx(12.0)

    def test_current_from(self):
        obj = OhmsLawJAX()
        assert float(obj.current_from(12.0, 4.0)) == pytest.approx(3.0)

    def test_resistance_from(self):
        obj = OhmsLawJAX()
        assert float(obj.resistance_from(12.0, 3.0)) == pytest.approx(4.0)

    def test_voltage_from_array(self):
        obj = OhmsLawJAX()
        result = obj.voltage_from(jnp.array([1.0, 2.0]), 3.0)
        assert jnp.allclose(result, jnp.array([3.0, 6.0]))

    def test_current_from_zero_R(self):
        obj = OhmsLawJAX()
        assert float(obj.current_from(10.0, 0.0)) == pytest.approx(0.0)

    def test_resistance_from_zero_I(self):
        obj = OhmsLawJAX()
        assert float(obj.resistance_from(10.0, 0.0)) == pytest.approx(0.0)


# -- TestOhmsLawJAXEdgeCases -------------------------------------------------------


class TestOhmsLawJAXEdgeCases:
    """Zero R, zero I, zero V."""

    def test_zero_resistance_voltage(self):
        obj = OhmsLawJAX(current=1.0, resistance=0.0)
        assert float(obj.computed_voltage) == pytest.approx(0.0)

    def test_zero_current_voltage(self):
        obj = OhmsLawJAX(current=0.0, resistance=5.0)
        assert float(obj.computed_voltage) == pytest.approx(0.0)

    def test_zero_voltage_current(self):
        obj = OhmsLawJAX(voltage=0.0, resistance=5.0)
        assert float(obj.computed_current) == pytest.approx(0.0)

    def test_zero_voltage_resistance(self):
        obj = OhmsLawJAX(voltage=0.0, current=2.0)
        assert float(obj.computed_resistance) == pytest.approx(0.0)


# -- TestResistanceJAXPytree -------------------------------------------------------


class TestResistanceJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = ResistanceJAX(base_resistance=10.0, temperature_coefficient=0.004)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 2
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.base_resistance) == pytest.approx(10.0)
        assert float(reconstructed.temperature_coefficient) == pytest.approx(0.004)

    def test_jit_series(self):
        obj = ResistanceJAX()
        jit_fn = jax.jit(lambda r: obj.series_combine(r))
        result = jit_fn(jnp.array([1.0, 2.0, 3.0]))
        assert float(result) == pytest.approx(6.0)

    def test_jit_parallel(self):
        obj = ResistanceJAX()
        jit_fn = jax.jit(lambda r: obj.parallel_combine(r))
        result = jit_fn(jnp.array([2.0, 2.0]))
        assert float(result) == pytest.approx(1.0)


# -- TestResistanceJAXSeries -------------------------------------------------------


class TestResistanceJAXSeries:
    """Single, dual, multi resistances."""

    def test_single_resistance(self):
        obj = ResistanceJAX()
        assert float(obj.series_combine(jnp.array([5.0]))) == pytest.approx(5.0)

    def test_dual_resistances(self):
        obj = ResistanceJAX()
        assert float(obj.series_combine(jnp.array([3.0, 7.0]))) == pytest.approx(10.0)

    def test_multi_resistances(self):
        obj = ResistanceJAX()
        result = obj.series_combine(jnp.array([1.0, 2.0, 3.0, 4.0]))
        assert float(result) == pytest.approx(10.0)

    def test_series_with_object(self):
        obj = ResistanceJAX(base_resistance=5.0)
        result = obj.series_combine(jnp.array([10.0, 20.0]))
        assert float(result) == pytest.approx(30.0)


# -- TestResistanceJAXParallel -----------------------------------------------------


class TestResistanceJAXParallel:
    """Single, dual, identical resistances."""

    def test_single_resistance(self):
        obj = ResistanceJAX()
        assert float(obj.parallel_combine(jnp.array([5.0]))) == pytest.approx(5.0)

    def test_dual_identical(self):
        obj = ResistanceJAX()
        assert float(obj.parallel_combine(jnp.array([10.0, 10.0]))) == pytest.approx(
            5.0
        )

    def test_dual_different(self):
        obj = ResistanceJAX()
        # 1/(1/2 + 1/3) = 1/(5/6) = 6/5 = 1.2
        result = obj.parallel_combine(jnp.array([2.0, 3.0]))
        assert float(result) == pytest.approx(1.2)

    def test_three_identical(self):
        obj = ResistanceJAX()
        # 1/(3/6) = 2
        result = obj.parallel_combine(jnp.array([6.0, 6.0, 6.0]))
        assert float(result) == pytest.approx(2.0)


# -- TestResistanceJAXTemperature --------------------------------------------------


class TestResistanceJAXTemperature:
    """Copper, batch, zero alpha."""

    def test_copper_at_higher_temp(self):
        # Copper: alpha = 0.004, R0 = 100 ohms at 20C
        obj = ResistanceJAX(base_resistance=100.0, temperature_coefficient=0.004)
        # At 70C: R = 100 * (1 + 0.004 * 50) = 100 * 1.2 = 120
        result = obj.at_temperature(70.0)
        assert float(result) == pytest.approx(120.0)

    def test_copper_at_lower_temp(self):
        obj = ResistanceJAX(base_resistance=100.0, temperature_coefficient=0.004)
        # At 0C: R = 100 * (1 + 0.004 * (-20)) = 100 * 0.92 = 92
        result = obj.at_temperature(0.0)
        assert float(result) == pytest.approx(92.0)

    def test_batch_temperatures(self):
        obj = ResistanceJAX(base_resistance=100.0, temperature_coefficient=0.004)
        temps = jnp.array([0.0, 20.0, 70.0])
        results = jax.vmap(lambda t: obj.at_temperature(t))(temps)
        assert float(results[0]) == pytest.approx(92.0)
        assert float(results[1]) == pytest.approx(100.0)
        assert float(results[2]) == pytest.approx(120.0)

    def test_zero_alpha(self):
        obj = ResistanceJAX(base_resistance=100.0, temperature_coefficient=0.0)
        result = obj.at_temperature(100.0)
        assert float(result) == pytest.approx(100.0)


# -- TestConductivityJAXPytree -----------------------------------------------------


class TestConductivityJAXPytree:
    """Flatten/unflatten."""

    def test_flatten_unflatten(self):
        obj = ConductivityJAX(conductivity=5.8e7)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.conductivity) == pytest.approx(5.8e7)

    def test_jit_compatible(self):
        obj = ConductivityJAX(conductivity=1.0)
        jit_fn = jax.jit(lambda o: o.resistivity)
        result = jit_fn(obj)
        assert float(result) == pytest.approx(1.0)

    def test_tree_map(self):
        obj = ConductivityJAX(conductivity=10.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.conductivity) == pytest.approx(20.0)


# -- TestConductivityJAXConversions ------------------------------------------------


class TestConductivityJAXConversions:
    """sigma->rho, J=sigma*E, E=J/sigma."""

    def test_resistivity_property(self):
        obj = ConductivityJAX(conductivity=0.5)
        assert float(obj.resistivity) == pytest.approx(2.0)

    def test_current_density(self):
        obj = ConductivityJAX(conductivity=2.0)
        E = jnp.array([1.0, 2.0, 3.0])
        J = obj.current_density(E)
        assert jnp.allclose(J, jnp.array([2.0, 4.0, 6.0]))

    def test_electric_field(self):
        obj = ConductivityJAX(conductivity=2.0)
        J = jnp.array([2.0, 4.0, 6.0])
        E = obj.electric_field(J)
        assert jnp.allclose(E, jnp.array([1.0, 2.0, 3.0]))

    def test_from_resistivity(self):
        obj = ConductivityJAX.from_resistivity(0.5)
        assert float(obj.conductivity) == pytest.approx(2.0)

    def test_roundtrip_sigma_rho(self):
        sigma_orig = 1.0e7
        obj = ConductivityJAX(conductivity=sigma_orig)
        rho = float(obj.resistivity)
        obj2 = ConductivityJAX.from_resistivity(rho)
        assert float(obj2.conductivity) == pytest.approx(sigma_orig, rel=1e-10)


# -- TestPowerDissipationJAXPytree -------------------------------------------------


class TestPowerDissipationJAXPytree:
    """Flatten/unflatten."""

    def test_flatten_unflatten(self):
        obj = PowerDissipationJAX(resistance=10.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.resistance) == pytest.approx(10.0)

    def test_jit_compatible(self):
        obj = PowerDissipationJAX(resistance=5.0)
        jit_fn = jax.jit(lambda o: o.from_current(2.0))
        result = jit_fn(obj)
        assert float(result) == pytest.approx(20.0)

    def test_tree_map(self):
        obj = PowerDissipationJAX(resistance=10.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.resistance) == pytest.approx(20.0)


# -- TestPowerDissipationJAXFormulas -----------------------------------------------


class TestPowerDissipationJAXFormulas:
    """I^2R, V^2/R, VI, cross-consistency."""

    def test_from_current(self):
        obj = PowerDissipationJAX(resistance=5.0)
        assert float(obj.from_current(2.0)) == pytest.approx(20.0)

    def test_from_voltage(self):
        obj = PowerDissipationJAX(resistance=5.0)
        assert float(obj.from_voltage(10.0)) == pytest.approx(20.0)

    def test_from_IV(self):
        obj = PowerDissipationJAX(resistance=5.0)
        assert float(obj.from_IV(10.0, 2.0)) == pytest.approx(20.0)

    def test_cross_consistency(self):
        """All three formulas give same result for V=10, I=2, R=5."""
        obj = PowerDissipationJAX(resistance=5.0)
        p_i2r = obj.from_current(2.0)
        p_v2r = obj.from_voltage(10.0)
        p_iv = obj.from_IV(10.0, 2.0)
        assert float(p_i2r) == pytest.approx(float(p_v2r))
        assert float(p_i2r) == pytest.approx(float(p_iv))

    def test_zero_resistance_from_voltage(self):
        obj = PowerDissipationJAX(resistance=0.0)
        assert float(obj.from_voltage(10.0)) == pytest.approx(0.0)


# -- TestStandaloneFunctions -------------------------------------------------------


class TestStandaloneFunctions:
    """All 14 standalone functions."""

    def test_calc_voltage(self):
        assert float(calc_voltage_jax(2.0, 5.0)) == pytest.approx(10.0)

    def test_calc_current(self):
        assert float(calc_current_jax(10.0, 5.0)) == pytest.approx(2.0)

    def test_calc_resistance(self):
        assert float(calc_resistance_jax(10.0, 2.0)) == pytest.approx(5.0)

    def test_calc_conductance(self):
        assert float(calc_conductance_jax(5.0)) == pytest.approx(0.2)

    def test_calc_resistivity(self):
        assert float(calc_resistivity_jax(0.5)) == pytest.approx(2.0)

    def test_calc_conductivity(self):
        assert float(calc_conductivity_jax(2.0)) == pytest.approx(0.5)

    def test_series_resistance(self):
        assert float(
            series_resistance_jax(jnp.array([1.0, 2.0, 3.0]))
        ) == pytest.approx(6.0)

    def test_parallel_resistance(self):
        assert float(parallel_resistance_jax(jnp.array([2.0, 2.0]))) == pytest.approx(
            1.0
        )

    def test_temperature_corrected_resistance(self):
        assert float(
            temperature_corrected_resistance_jax(100.0, 0.004, 70.0)
        ) == pytest.approx(120.0)

    def test_calc_power_from_IV(self):
        assert float(calc_power_from_IV_jax(10.0, 2.0)) == pytest.approx(20.0)

    def test_calc_power_from_I2R(self):
        assert float(calc_power_from_I2R_jax(2.0, 5.0)) == pytest.approx(20.0)

    def test_calc_power_from_V2R(self):
        assert float(calc_power_from_V2R_jax(10.0, 5.0)) == pytest.approx(20.0)

    def test_verify_ohms_law(self):
        result = verify_ohms_law_jax(V=10.0, I=2.0, R=5.0)
        assert bool(result["verified"]) is True

    def test_analyze_ohms_law(self):
        result = analyze_ohms_law_jax(voltage=10.0, current=2.0, conductivity=1.0)
        assert "resistance" in result
        assert "resistivity" in result


# -- TestJITOhmsLaw ----------------------------------------------------------------


class TestJITOhmsLaw:
    """JIT compilation for all classes."""

    def test_jit_ohms_law(self):
        @jax.jit
        def compute(v, i, r):
            obj = OhmsLawJAX(voltage=v, current=i, resistance=r)
            return obj.computed_voltage

        result = compute(10.0, 2.0, 5.0)
        assert float(result) == pytest.approx(10.0)

    def test_jit_resistance_series(self):
        obj = ResistanceJAX()
        jit_fn = jax.jit(obj.series_combine)
        result = jit_fn(jnp.array([1.0, 2.0, 3.0]))
        assert float(result) == pytest.approx(6.0)

    def test_jit_resistance_parallel(self):
        obj = ResistanceJAX()
        jit_fn = jax.jit(obj.parallel_combine)
        result = jit_fn(jnp.array([2.0, 2.0]))
        assert float(result) == pytest.approx(1.0)

    def test_jit_conductivity(self):
        obj = ConductivityJAX(conductivity=2.0)
        jit_fn = jax.jit(lambda o: o.current_density(jnp.array([1.0, 2.0])))
        result = jit_fn(obj)
        assert jnp.allclose(result, jnp.array([2.0, 4.0]))

    def test_jit_power(self):
        obj = PowerDissipationJAX(resistance=5.0)
        jit_fn = jax.jit(lambda o: o.from_current(2.0))
        result = jit_fn(obj)
        assert float(result) == pytest.approx(20.0)


# -- TestAutoDiffOhmsLaw -----------------------------------------------------------


class TestAutoDiffOhmsLaw:
    """Gradients: dV/dI=R, dV/dR=I, dP/dI=2IR, etc."""

    def test_grad_voltage_wrt_current(self):
        grad_fn = jax.grad(lambda I: OhmsLawJAX._voltage_jit(I, 5.0))
        g = grad_fn(2.0)
        assert float(g) == pytest.approx(5.0, abs=1e-6)

    def test_grad_voltage_wrt_resistance(self):
        grad_fn = jax.grad(lambda R: OhmsLawJAX._voltage_jit(2.0, R))
        g = grad_fn(5.0)
        assert float(g) == pytest.approx(2.0, abs=1e-6)

    def test_grad_power_I2R_wrt_current(self):
        grad_fn = jax.grad(lambda I: PowerDissipationJAX._i2r_jit(I, 5.0))
        g = grad_fn(2.0)
        # d/dI (I^2 * R) = 2*I*R = 2*2*5 = 20
        assert float(g) == pytest.approx(20.0, abs=1e-6)

    def test_grad_power_I2R_wrt_resistance(self):
        grad_fn = jax.grad(lambda R: PowerDissipationJAX._i2r_jit(2.0, R))
        g = grad_fn(5.0)
        # d/dR (I^2 * R) = I^2 = 4
        assert float(g) == pytest.approx(4.0, abs=1e-6)

    def test_grad_current_wrt_voltage(self):
        grad_fn = jax.grad(lambda V: OhmsLawJAX._current_jit(V, 5.0))
        g = grad_fn(10.0)
        # d/dV (V/R) = 1/R = 0.2
        assert float(g) == pytest.approx(0.2, abs=1e-6)


# -- TestVmapOhmsLaw ---------------------------------------------------------------


class TestVmapOhmsLaw:
    """Vmap over arrays of inputs."""

    def test_vmap_voltage(self):
        voltages = jax.vmap(lambda I, R: OhmsLawJAX._voltage_jit(I, R))(
            jnp.array([1.0, 2.0, 3.0]), jnp.array([10.0, 5.0, 2.0])
        )
        expected = jnp.array([10.0, 10.0, 6.0])
        assert jnp.allclose(voltages, expected)

    def test_vmap_current(self):
        currents = jax.vmap(lambda V, R: OhmsLawJAX._current_jit(V, R))(
            jnp.array([10.0, 10.0, 10.0]), jnp.array([1.0, 2.0, 5.0])
        )
        expected = jnp.array([10.0, 5.0, 2.0])
        assert jnp.allclose(currents, expected)

    def test_vmap_power_i2r(self):
        powers = jax.vmap(lambda I, R: PowerDissipationJAX._i2r_jit(I, R))(
            jnp.array([1.0, 2.0, 3.0]), jnp.array([1.0, 1.0, 1.0])
        )
        expected = jnp.array([1.0, 4.0, 9.0])
        assert jnp.allclose(powers, expected)

    def test_vmap_temperature(self):
        temps = jnp.array([0.0, 20.0, 40.0, 60.0])
        results = jax.vmap(
            lambda t: ResistanceJAX._temp_correct_jit(100.0, 0.004, t, 20.0)
        )(temps)
        assert float(results[0]) == pytest.approx(92.0)
        assert float(results[1]) == pytest.approx(100.0)
        assert float(results[2]) == pytest.approx(108.0)
        assert float(results[3]) == pytest.approx(116.0)

    def test_vmap_conductivity(self):
        sigmas = jnp.array([1.0, 2.0, 4.0])
        E = jnp.array([1.0, 1.0, 1.0])
        J = jax.vmap(lambda s, e: ConductivityJAX._current_density_jit(s, e))(sigmas, E)
        assert jnp.allclose(J, jnp.array([1.0, 2.0, 4.0]))


# -- TestNumPyOhmsLaw --------------------------------------------------------------


class TestNumPyOhmsLaw:
    """JAX vs NumPy comparison."""

    def test_voltage_numpy_equiv(self):
        np_result = np.array([1.0, 2.0, 3.0]) * 5.0
        jax_result = calc_voltage_jax(np.array([1.0, 2.0, 3.0]), 5.0)
        assert jnp.allclose(jnp.array(jax_result), jnp.array(np_result))

    def test_series_numpy_equiv(self):
        np_result = np.sum(np.array([1.0, 2.0, 3.0]))
        jax_result = series_resistance_jax(jnp.array([1.0, 2.0, 3.0]))
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_power_i2r_numpy_equiv(self):
        np_result = np.array([1.0, 2.0, 3.0]) ** 2 * 5.0
        jax_result = calc_power_from_I2R_jax(np.array([1.0, 2.0, 3.0]), 5.0)
        assert jnp.allclose(jnp.array(jax_result), jnp.array(np_result))

    def test_temperature_numpy_equiv(self):
        np_result = 100.0 * (1.0 + 0.004 * (70.0 - 20.0))
        jax_result = temperature_corrected_resistance_jax(100.0, 0.004, 70.0)
        assert float(jax_result) == pytest.approx(float(np_result))


# -- TestVerifyOhmsLaw -------------------------------------------------------------


class TestVerifyOhmsLaw:
    """verify_ohms_law_jax."""

    def test_verify_passes_valid(self):
        result = verify_ohms_law_jax(V=10.0, I=2.0, R=5.0)
        assert bool(result["verified"]) is True
        assert float(result["V_from_IR"]) == pytest.approx(10.0)
        assert float(result["I_from_VR"]) == pytest.approx(2.0)
        assert float(result["R_from_VI"]) == pytest.approx(5.0)

    def test_verify_power_consistency(self):
        result = verify_ohms_law_jax(V=10.0, I=2.0, R=5.0)
        assert float(result["power_IV"]) == pytest.approx(20.0)
        assert float(result["power_I2R"]) == pytest.approx(20.0)
        assert float(result["power_V2R"]) == pytest.approx(20.0)

    def test_verify_different_values(self):
        result = verify_ohms_law_jax(V=12.0, I=3.0, R=4.0)
        assert bool(result["verified"]) is True
        assert float(result["power_IV"]) == pytest.approx(36.0)

    def test_verify_all_keys_present(self):
        result = verify_ohms_law_jax()
        expected_keys = {
            "V_from_IR",
            "I_from_VR",
            "R_from_VI",
            "power_IV",
            "power_I2R",
            "power_V2R",
            "verified",
        }
        assert set(result.keys()) == expected_keys


# -- TestAnalyzeOhmsLaw ------------------------------------------------------------


class TestAnalyzeOhmsLaw:
    """analyze_ohms_law_jax."""

    def test_analyze_with_voltage_and_current(self):
        result = analyze_ohms_law_jax(voltage=10.0, current=2.0)
        assert "resistance" in result
        assert "power_IV" in result
        assert float(result["resistance"]) == pytest.approx(5.0)
        assert float(result["power_IV"]) == pytest.approx(20.0)

    def test_analyze_with_voltage_and_resistance(self):
        result = analyze_ohms_law_jax(voltage=10.0, resistance=5.0)
        assert "current" in result
        assert "conductance" in result
        assert float(result["current"]) == pytest.approx(2.0)
        assert float(result["conductance"]) == pytest.approx(0.2)

    def test_analyze_with_conductivity(self):
        result = analyze_ohms_law_jax(conductivity=1.0e7)
        assert "resistivity" in result
        assert float(result["resistivity"]) == pytest.approx(1.0e-7)
