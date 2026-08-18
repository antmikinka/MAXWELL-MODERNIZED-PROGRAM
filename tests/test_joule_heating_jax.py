"""Tests for JouleHeatingJAX -- Part II Joule Heating and Substance Resistance (Arts. 351-370)."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax.electromagnetism.joule_heating import (
    HeatDissipationJAX,
    JouleHeatingJAX,
    SubstanceResistanceJAX,
    analyze_joule_heating_jax,
    cooling_rate_jax,
    joule_energy_dissipated_jax,
    joule_heating_from_voltage_jax,
    joule_heating_power_jax,
    joule_power_density_jax,
    joule_temperature_rise_jax,
    steady_state_temperature_jax,
    substance_resistance_jax,
    substance_resistivity_at_temp_jax,
    verify_joule_heating_jax,
)

TOL = 1e-10


# -- TestJouleHeatingJAXPytree -----------------------------------------------------


class TestJouleHeatingJAXPytree:
    """Flatten/unflatten, jit, vmap."""

    def test_flatten_unflatten_default(self):
        obj = JouleHeatingJAX()
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.resistance) == pytest.approx(0.0)

    def test_flatten_unflatten_custom(self):
        obj = JouleHeatingJAX(resistance=5.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.resistance) == pytest.approx(5.0)

    def test_jit_compatible(self):
        obj = JouleHeatingJAX(resistance=5.0)
        jit_fn = jax.jit(lambda o: o.power(jnp.array(2.0)))
        result = jit_fn(obj)
        assert float(result) == pytest.approx(20.0)

    def test_tree_map(self):
        obj = JouleHeatingJAX(resistance=5.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.resistance) == pytest.approx(10.0)


# -- TestJouleHeatingJAXPower ------------------------------------------------------


class TestJouleHeatingJAXPower:
    """Computation correctness for power and energy."""

    def test_power_basic(self):
        obj = JouleHeatingJAX(resistance=5.0)
        P = obj.power(jnp.array(2.0))
        expected = 2.0**2 * 5.0
        assert float(P) == pytest.approx(expected, rel=TOL)

    def test_power_zero_current(self):
        obj = JouleHeatingJAX(resistance=5.0)
        P = obj.power(jnp.array(0.0))
        assert float(P) == pytest.approx(0.0, abs=1e-15)

    def test_power_zero_resistance(self):
        obj = JouleHeatingJAX(resistance=0.0)
        P = obj.power(jnp.array(2.0))
        assert float(P) == pytest.approx(0.0, abs=1e-15)

    def test_energy_dissipated(self):
        obj = JouleHeatingJAX(resistance=5.0)
        E = obj.energy_dissipated(jnp.array(2.0), jnp.array(10.0))
        expected = 2.0**2 * 5.0 * 10.0
        assert float(E) == pytest.approx(expected, rel=TOL)

    def test_energy_zero_time(self):
        obj = JouleHeatingJAX(resistance=5.0)
        E = obj.energy_dissipated(jnp.array(2.0), jnp.array(0.0))
        assert float(E) == pytest.approx(0.0, abs=1e-15)

    def test_power_density(self):
        obj = JouleHeatingJAX(resistance=1.0)
        p = obj.power_density(jnp.array(3.0), jnp.array(2.0))
        expected = 3.0**2 * 2.0
        assert float(p) == pytest.approx(expected, rel=TOL)

    def test_temperature_rise(self):
        obj = JouleHeatingJAX(resistance=5.0)
        # I=2, R=5, t=10, m=10, c=4.18e7 (water)
        dT = obj.temperature_rise(
            jnp.array(2.0), jnp.array(10.0), jnp.array(10.0), jnp.array(4.18e7)
        )
        E = 2.0**2 * 5.0 * 10.0
        expected = E / (10.0 * 4.18e7)
        assert float(dT) == pytest.approx(expected, rel=TOL)

    def test_temperature_rise_zero_mass_safe(self):
        obj = JouleHeatingJAX(resistance=5.0)
        dT = obj.temperature_rise(
            jnp.array(2.0), jnp.array(10.0), jnp.array(0.0), jnp.array(4.18e7)
        )
        # safe_div returns 0.0 for division by zero
        assert float(dT) == pytest.approx(0.0, abs=1e-15)

    def test_from_voltage(self):
        obj = JouleHeatingJAX(resistance=5.0)
        P = obj.from_voltage(jnp.array(10.0))
        expected = 10.0**2 / 5.0
        assert float(P) == pytest.approx(expected, rel=TOL)

    def test_from_voltage_zero_resistance_safe(self):
        obj = JouleHeatingJAX(resistance=0.0)
        P = obj.from_voltage(jnp.array(10.0))
        assert float(P) == pytest.approx(0.0, abs=1e-15)

    def test_power_voltage_consistency(self):
        obj = JouleHeatingJAX(resistance=5.0)
        I = 2.0
        V = I * 5.0  # V = I*R
        P_I2R = obj.power(jnp.array(I))
        P_V2R = obj.from_voltage(jnp.array(V))
        assert float(P_I2R) == pytest.approx(float(P_V2R), rel=TOL)


# -- TestJouleHeatingJAXEdgeCases --------------------------------------------------


class TestJouleHeatingJAXEdgeCases:
    """Edge cases and boundary conditions."""

    def test_negative_current_gives_positive_power(self):
        obj = JouleHeatingJAX(resistance=5.0)
        P = obj.power(jnp.array(-2.0))
        expected = (-2.0) ** 2 * 5.0
        assert float(P) == pytest.approx(expected, rel=TOL)

    def test_power_quadratic_in_current(self):
        obj = JouleHeatingJAX(resistance=5.0)
        P1 = obj.power(jnp.array(1.0))
        P2 = obj.power(jnp.array(2.0))
        assert float(P2) == pytest.approx(4.0 * float(P1), rel=TOL)

    def test_energy_linear_in_time(self):
        obj = JouleHeatingJAX(resistance=5.0)
        E1 = obj.energy_dissipated(jnp.array(2.0), jnp.array(5.0))
        E2 = obj.energy_dissipated(jnp.array(2.0), jnp.array(10.0))
        assert float(E2) == pytest.approx(2.0 * float(E1), rel=TOL)


# -- TestHeatDissipationJAXPytree --------------------------------------------------


class TestHeatDissipationJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 3
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.specific_heat) == pytest.approx(4.18e7)
        assert float(reconstructed.mass) == pytest.approx(10.0)

    def test_jit_compatible(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        jit_fn = jax.jit(lambda o: o.temperature_from_energy(jnp.array(1000.0)))
        result = jit_fn(obj)
        assert float(result) > 0

    def test_tree_map(self):
        obj = HeatDissipationJAX(specific_heat=1.0, mass=2.0, thermal_conductivity=3.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.specific_heat) == pytest.approx(2.0)
        assert float(doubled.mass) == pytest.approx(4.0)
        assert float(doubled.thermal_conductivity) == pytest.approx(6.0)


# -- TestHeatDissipationJAXTemperature ---------------------------------------------


class TestHeatDissipationJAXTemperature:
    """Computation correctness for temperature calculations."""

    def test_temperature_from_energy(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        dT = obj.temperature_from_energy(jnp.array(4.18e8))
        expected = 4.18e8 / (10.0 * 4.18e7)
        assert float(dT) == pytest.approx(expected, rel=TOL)

    def test_temperature_from_energy_zero(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        dT = obj.temperature_from_energy(jnp.array(0.0))
        assert float(dT) == pytest.approx(0.0, abs=1e-15)

    def test_temperature_from_energy_zero_mass_safe(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=0.0, thermal_conductivity=4.01e8
        )
        dT = obj.temperature_from_energy(jnp.array(1000.0))
        assert float(dT) == pytest.approx(0.0, abs=1e-15)

    def test_cooling_rate(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        dQ = obj.cooling_rate(jnp.array(1.0), jnp.array(10.0), jnp.array(1.0e5))
        expected = 1.0e5 * 1.0 * 10.0
        assert float(dQ) == pytest.approx(expected, rel=TOL)

    def test_cooling_rate_zero_temp_diff(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        dQ = obj.cooling_rate(jnp.array(1.0), jnp.array(0.0), jnp.array(1.0e5))
        assert float(dQ) == pytest.approx(0.0, abs=1e-15)

    def test_steady_state_temperature(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        T_ss = obj.steady_state_temperature(
            jnp.array(1.0e6), jnp.array(293.15), jnp.array(1.0), jnp.array(1.0e5)
        )
        expected = 293.15 + 1.0e6 / (1.0e5 * 1.0)
        assert float(T_ss) == pytest.approx(expected, rel=TOL)

    def test_steady_state_zero_power(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        T_ss = obj.steady_state_temperature(
            jnp.array(0.0), jnp.array(293.15), jnp.array(1.0), jnp.array(1.0e5)
        )
        assert float(T_ss) == pytest.approx(293.15, rel=TOL)


# -- TestHeatDissipationJAXCooling -------------------------------------------------


class TestHeatDissipationJAXCooling:
    """Transient and cooling behavior."""

    def test_transient_temperature_initial(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        T_t = obj.transient_temperature(
            jnp.array(1.0e6),
            jnp.array(0.0),
            jnp.array(293.15),
            jnp.array(1.0),
            jnp.array(1.0e5),
        )
        # At t=0, should equal ambient
        assert float(T_t) == pytest.approx(293.15, rel=TOL)

    def test_transient_temperature_approaches_steady_state(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        P = jnp.array(1.0e6)
        T_amb = jnp.array(293.15)
        A = jnp.array(1.0)
        h = jnp.array(1.0e5)

        # Long time -> should approach steady state
        T_long = obj.transient_temperature(P, jnp.array(1e6), T_amb, A, h)
        T_ss = obj.steady_state_temperature(P, T_amb, A, h)
        assert float(T_long) == pytest.approx(float(T_ss), rel=1e-6)

    def test_transient_temperature_monotonic(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        P = jnp.array(1.0e6)
        T_amb = jnp.array(293.15)
        A = jnp.array(1.0)
        h = jnp.array(1.0e5)

        T1 = obj.transient_temperature(P, jnp.array(1.0), T_amb, A, h)
        T2 = obj.transient_temperature(P, jnp.array(10.0), T_amb, A, h)
        T3 = obj.transient_temperature(P, jnp.array(100.0), T_amb, A, h)
        # Temperature should increase over time (approaching steady state)
        assert float(T3) >= float(T2) >= float(T1)

    def test_transient_zero_power(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        T_t = obj.transient_temperature(
            jnp.array(0.0),
            jnp.array(100.0),
            jnp.array(293.15),
            jnp.array(1.0),
            jnp.array(1.0e5),
        )
        assert float(T_t) == pytest.approx(293.15, rel=TOL)


# -- TestSubstanceResistanceJAXPytree ----------------------------------------------


class TestSubstanceResistanceJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6,
            temperature_coefficient=0.00393,
            reference_temp=20.0,
        )
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 3
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.base_resistivity) == pytest.approx(1.7e-6)
        assert float(reconstructed.temperature_coefficient) == pytest.approx(0.00393)

    def test_jit_compatible(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.00393
        )
        jit_fn = jax.jit(lambda o: o.at_temperature(jnp.array(50.0)))
        result = jit_fn(obj)
        assert float(result) > 0

    def test_tree_map(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.0, temperature_coefficient=0.004, reference_temp=20.0
        )
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.base_resistivity) == pytest.approx(2.0)
        assert float(doubled.temperature_coefficient) == pytest.approx(0.008)


# -- TestSubstanceResistanceJAXTemperature -----------------------------------------


class TestSubstanceResistanceJAXTemperature:
    """Temperature-dependent resistivity calculations."""

    def test_at_reference_temp(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6,
            temperature_coefficient=0.00393,
            reference_temp=20.0,
        )
        rho = obj.at_temperature(jnp.array(20.0))
        assert float(rho) == pytest.approx(1.7e-6, rel=TOL)

    def test_at_higher_temp(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6,
            temperature_coefficient=0.00393,
            reference_temp=20.0,
        )
        rho = obj.at_temperature(jnp.array(70.0))
        # rho = 1.7e-6 * (1 + 0.00393 * 50)
        expected = 1.7e-6 * (1.0 + 0.00393 * 50.0)
        assert float(rho) == pytest.approx(expected, rel=TOL)

    def test_at_lower_temp(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6,
            temperature_coefficient=0.00393,
            reference_temp=20.0,
        )
        rho = obj.at_temperature(jnp.array(-30.0))
        expected = 1.7e-6 * (1.0 + 0.00393 * (-50.0))
        assert float(rho) == pytest.approx(expected, rel=TOL)

    def test_zero_coefficient_constant_resistivity(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.0, reference_temp=20.0
        )
        rho1 = obj.at_temperature(jnp.array(20.0))
        rho2 = obj.at_temperature(jnp.array(100.0))
        assert float(rho1) == pytest.approx(float(rho2), rel=TOL)

    def test_resistivity_increases_with_temp(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.00393
        )
        rho_cold = obj.at_temperature(jnp.array(0.0))
        rho_hot = obj.at_temperature(jnp.array(100.0))
        assert float(rho_hot) > float(rho_cold)


# -- TestSubstanceResistanceJAXGeometry --------------------------------------------


class TestSubstanceResistanceJAXGeometry:
    """Geometry-based resistance calculations."""

    def test_resistance_from_geometry(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6,
            temperature_coefficient=0.00393,
            reference_temp=20.0,
        )
        # Copper wire at 20C: L=100cm, A=0.01cm^2
        R = obj.resistance_from_geometry(
            jnp.array(100.0), jnp.array(0.01), jnp.array(20.0)
        )
        expected = 1.7e-6 * 100.0 / 0.01
        assert float(R) == pytest.approx(expected, rel=TOL)

    def test_resistance_proportional_to_length(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.0
        )
        R1 = obj.resistance_from_geometry(
            jnp.array(100.0), jnp.array(0.01), jnp.array(20.0)
        )
        R2 = obj.resistance_from_geometry(
            jnp.array(200.0), jnp.array(0.01), jnp.array(20.0)
        )
        assert float(R2) == pytest.approx(2.0 * float(R1), rel=TOL)

    def test_resistance_inversely_proportional_to_area(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.0
        )
        R1 = obj.resistance_from_geometry(
            jnp.array(100.0), jnp.array(0.01), jnp.array(20.0)
        )
        R2 = obj.resistance_from_geometry(
            jnp.array(100.0), jnp.array(0.02), jnp.array(20.0)
        )
        assert float(R2) == pytest.approx(0.5 * float(R1), rel=TOL)

    def test_compare_substances(self):
        obj = SubstanceResistanceJAX(reference_temp=20.0)
        # Copper vs aluminum at 20C
        rhos = jnp.array([1.7e-6, 2.82e-6])  # Cu, Al
        alphas = jnp.array([0.00393, 0.00429])
        Rs = obj.compare_substances(
            rhos, alphas, jnp.array(20.0), jnp.array(100.0), jnp.array(0.01)
        )
        # At reference temp, rho = rho_0
        assert float(Rs[0]) == pytest.approx(1.7e-6 * 100.0 / 0.01, rel=TOL)
        assert float(Rs[1]) == pytest.approx(2.82e-6 * 100.0 / 0.01, rel=TOL)

    def test_compare_substances_at_elevated_temp(self):
        obj = SubstanceResistanceJAX(reference_temp=20.0)
        rhos = jnp.array([1.7e-6, 2.82e-6])
        alphas = jnp.array([0.00393, 0.00429])
        Rs = obj.compare_substances(
            rhos, alphas, jnp.array(100.0), jnp.array(100.0), jnp.array(0.01)
        )
        # Both should increase at higher temp (positive alpha)
        R_20 = obj.compare_substances(
            rhos, alphas, jnp.array(20.0), jnp.array(100.0), jnp.array(0.01)
        )
        assert float(Rs[0]) > float(R_20[0])
        assert float(Rs[1]) > float(R_20[1])


# -- TestStandaloneJouleFunctions --------------------------------------------------


class TestStandaloneJouleFunctions:
    """All standalone function correctness."""

    def test_joule_heating_power(self):
        P = joule_heating_power_jax(jnp.array(2.0), jnp.array(5.0))
        expected = 2.0**2 * 5.0
        assert float(P) == pytest.approx(expected, rel=TOL)

    def test_joule_energy_dissipated(self):
        E = joule_energy_dissipated_jax(jnp.array(2.0), jnp.array(5.0), jnp.array(10.0))
        expected = 2.0**2 * 5.0 * 10.0
        assert float(E) == pytest.approx(expected, rel=TOL)

    def test_joule_power_density(self):
        p = joule_power_density_jax(jnp.array(3.0), jnp.array(2.0))
        expected = 3.0**2 * 2.0
        assert float(p) == pytest.approx(expected, rel=TOL)

    def test_joule_temperature_rise(self):
        dT = joule_temperature_rise_jax(
            jnp.array(2.0),
            jnp.array(5.0),
            jnp.array(10.0),
            jnp.array(10.0),
            jnp.array(4.18e7),
        )
        E = 2.0**2 * 5.0 * 10.0
        expected = E / (10.0 * 4.18e7)
        assert float(dT) == pytest.approx(expected, rel=TOL)

    def test_joule_heating_from_voltage(self):
        P = joule_heating_from_voltage_jax(jnp.array(10.0), jnp.array(5.0))
        expected = 10.0**2 / 5.0
        assert float(P) == pytest.approx(expected, rel=TOL)

    def test_cooling_rate(self):
        dQ = cooling_rate_jax(jnp.array(1.0), jnp.array(10.0), jnp.array(1.0e5))
        expected = 1.0e5 * 1.0 * 10.0
        assert float(dQ) == pytest.approx(expected, rel=TOL)

    def test_steady_state_temperature(self):
        T_ss = steady_state_temperature_jax(
            jnp.array(1.0e6), jnp.array(293.15), jnp.array(1.0), jnp.array(1.0e5)
        )
        expected = 293.15 + 1.0e6 / (1.0e5 * 1.0)
        assert float(T_ss) == pytest.approx(expected, rel=TOL)

    def test_substance_resistivity_at_temp(self):
        rho = substance_resistivity_at_temp_jax(
            jnp.array(1.7e-6), jnp.array(0.00393), jnp.array(70.0), jnp.array(20.0)
        )
        expected = 1.7e-6 * (1.0 + 0.00393 * 50.0)
        assert float(rho) == pytest.approx(expected, rel=TOL)

    def test_substance_resistance(self):
        R = substance_resistance_jax(
            jnp.array(1.7e-6), jnp.array(100.0), jnp.array(0.01)
        )
        expected = 1.7e-6 * 100.0 / 0.01
        assert float(R) == pytest.approx(expected, rel=TOL)


# -- TestJITJouleHeating -----------------------------------------------------------


class TestJITJouleHeating:
    """JIT compilation for all classes."""

    def test_jit_joule_heating(self):
        obj = JouleHeatingJAX(resistance=5.0)
        jit_fn = jax.jit(
            lambda o: (
                o.power(jnp.array(2.0)),
                o.energy_dissipated(jnp.array(2.0), jnp.array(10.0)),
                o.from_voltage(jnp.array(10.0)),
            )
        )
        results = jit_fn(obj)
        assert float(results[0]) == pytest.approx(20.0)
        assert float(results[1]) == pytest.approx(200.0)
        assert float(results[2]) == pytest.approx(20.0)

    def test_jit_heat_dissipation(self):
        obj = HeatDissipationJAX(
            specific_heat=4.18e7, mass=10.0, thermal_conductivity=4.01e8
        )
        jit_fn = jax.jit(
            lambda o: (
                o.temperature_from_energy(jnp.array(1000.0)),
                o.cooling_rate(jnp.array(1.0), jnp.array(10.0), jnp.array(1.0e5)),
                o.steady_state_temperature(
                    jnp.array(1.0e6),
                    jnp.array(293.15),
                    jnp.array(1.0),
                    jnp.array(1.0e5),
                ),
            )
        )
        results = jit_fn(obj)
        assert float(results[0]) > 0
        assert float(results[1]) > 0
        assert float(results[2]) > 293.15

    def test_jit_substance_resistance(self):
        obj = SubstanceResistanceJAX(
            base_resistivity=1.7e-6, temperature_coefficient=0.00393
        )
        jit_fn = jax.jit(
            lambda o: (
                o.at_temperature(jnp.array(50.0)),
                o.resistance_from_geometry(
                    jnp.array(100.0), jnp.array(0.01), jnp.array(50.0)
                ),
            )
        )
        results = jit_fn(obj)
        assert float(results[0]) > 0
        assert float(results[1]) > 0

    def test_jit_standalone_functions(self):
        @jax.jit
        def compute(I, R, t):
            P = joule_heating_power_jax(I, R)
            E = joule_energy_dissipated_jax(I, R, t)
            return P, E

        P, E = compute(2.0, 5.0, 10.0)
        assert float(P) == pytest.approx(20.0)
        assert float(E) == pytest.approx(200.0)


# -- TestAutoDiffJouleHeating ------------------------------------------------------


class TestAutoDiffJouleHeating:
    """Gradients through Joule heating functions."""

    def test_grad_power_wrt_current(self):
        grad_fn = jax.grad(lambda I: joule_heating_power_jax(I, jnp.array(5.0)))
        g = grad_fn(2.0)
        # d/dI (I^2 * R) = 2*I*R = 2*2*5 = 20
        expected = 2.0 * 2.0 * 5.0
        assert float(g) == pytest.approx(expected, rel=TOL)

    def test_grad_power_wrt_resistance(self):
        grad_fn = jax.grad(lambda R: joule_heating_power_jax(jnp.array(2.0), R))
        g = grad_fn(5.0)
        # d/dR (I^2 * R) = I^2 = 4
        expected = 2.0**2
        assert float(g) == pytest.approx(expected, rel=TOL)

    def test_grad_energy_wrt_time(self):
        grad_fn = jax.grad(
            lambda t: joule_energy_dissipated_jax(jnp.array(2.0), jnp.array(5.0), t)
        )
        g = grad_fn(10.0)
        # d/dt (I^2 * R * t) = I^2 * R = 20
        expected = 2.0**2 * 5.0
        assert float(g) == pytest.approx(expected, rel=TOL)

    def test_grad_temperature_rise_wrt_current(self):
        grad_fn = jax.grad(
            lambda I: joule_temperature_rise_jax(
                I, jnp.array(5.0), jnp.array(10.0), jnp.array(10.0), jnp.array(4.18e7)
            )
        )
        g = grad_fn(2.0)
        # d/dI (I^2 * R * t / (m*c)) = 2*I*R*t/(m*c)
        expected = 2.0 * 2.0 * 5.0 * 10.0 / (10.0 * 4.18e7)
        assert float(g) == pytest.approx(expected, rel=TOL)

    def test_grad_steady_state_wrt_power(self):
        grad_fn = jax.grad(
            lambda P: steady_state_temperature_jax(
                P, jnp.array(293.15), jnp.array(1.0), jnp.array(1.0e5)
            )
        )
        g = grad_fn(1.0e6)
        # d/dP (T_amb + P/(h*A)) = 1/(h*A) = 1/(1e5*1)
        expected = 1.0 / (1.0e5 * 1.0)
        assert float(g) == pytest.approx(expected, rel=TOL)


# -- TestVmapJouleHeating ----------------------------------------------------------


class TestVmapJouleHeating:
    """Vectorization over arrays of inputs."""

    def test_vmap_joule_power(self):
        currents = jnp.array([1.0, 2.0, 3.0])
        powers = jax.vmap(lambda I: joule_heating_power_jax(I, jnp.array(5.0)))(
            currents
        )
        assert powers.shape == (3,)
        # Monotonically increasing
        assert jnp.all(jnp.diff(powers) > 0)

    def test_vmap_joule_energy(self):
        times = jnp.array([1.0, 5.0, 10.0])
        energies = jax.vmap(
            lambda t: joule_energy_dissipated_jax(jnp.array(2.0), jnp.array(5.0), t)
        )(times)
        assert energies.shape == (3,)
        assert jnp.all(jnp.diff(energies) > 0)

    def test_vmap_substance_resistivity(self):
        temps = jnp.array([0.0, 20.0, 50.0, 100.0])
        rhos = jax.vmap(
            lambda T: substance_resistivity_at_temp_jax(
                jnp.array(1.7e-6), jnp.array(0.00393), T, jnp.array(20.0)
            )
        )(temps)
        assert rhos.shape == (4,)
        # At 20C should equal base resistivity
        assert float(rhos[1]) == pytest.approx(1.7e-6, rel=TOL)
        # Higher temp -> higher resistivity
        assert float(rhos[3]) > float(rhos[0])

    def test_vmap_cooling_rate(self):
        temp_diffs = jnp.array([5.0, 10.0, 20.0])
        rates = jax.vmap(
            lambda dT: cooling_rate_jax(jnp.array(1.0), dT, jnp.array(1.0e5))
        )(temp_diffs)
        assert rates.shape == (3,)
        assert jnp.all(jnp.diff(rates) > 0)


# -- TestNumPyJouleComparison ------------------------------------------------------


class TestNumPyJouleComparison:
    """JAX vs NumPy comparison."""

    def test_joule_power_numpy_equiv(self):
        I, R = 2.0, 5.0
        np_result = I**2 * R
        jax_result = joule_heating_power_jax(jnp.array(I), jnp.array(R))
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_substance_resistivity_numpy_equiv(self):
        rho_0, alpha, T, T0 = 1.7e-6, 0.00393, 70.0, 20.0
        np_result = rho_0 * (1.0 + alpha * (T - T0))
        jax_result = substance_resistivity_at_temp_jax(
            jnp.array(rho_0), jnp.array(alpha), jnp.array(T), jnp.array(T0)
        )
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_cooling_rate_numpy_equiv(self):
        A, dT, h = 1.0, 10.0, 1.0e5
        np_result = h * A * dT
        jax_result = cooling_rate_jax(jnp.array(A), jnp.array(dT), jnp.array(h))
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_substance_resistance_numpy_equiv(self):
        rho, L, A = 1.7e-6, 100.0, 0.01
        np_result = rho * L / A
        jax_result = substance_resistance_jax(
            jnp.array(rho), jnp.array(L), jnp.array(A)
        )
        assert float(jax_result) == pytest.approx(float(np_result))


# -- TestVerifyJouleHeating --------------------------------------------------------


class TestVerifyJouleHeating:
    """verify_joule_heating_jax behavior."""

    def test_verify_passes(self):
        result = verify_joule_heating_jax()
        assert result["verified"] is True

    def test_verify_keys_present(self):
        result = verify_joule_heating_jax()
        expected_keys = {
            "P_I2R",
            "P_V2R",
            "power_consistent",
            "E",
            "E_expected",
            "energy_consistent",
            "P_from_density",
            "density_consistent",
            "dT",
            "dT_expected",
            "temp_consistent",
            "verified",
        }
        assert set(result.keys()) == expected_keys

    def test_verify_power_consistency(self):
        result = verify_joule_heating_jax()
        assert float(result["P_I2R"]) == pytest.approx(
            float(result["P_V2R"]), rel=1e-10
        )

    def test_verify_energy_consistency(self):
        result = verify_joule_heating_jax()
        assert float(result["E"]) == pytest.approx(
            float(result["E_expected"]), rel=1e-10
        )


# -- TestAnalyzeJouleHeating -------------------------------------------------------


class TestAnalyzeJouleHeating:
    """analyze_joule_heating_jax behavior."""

    def test_analyze_returns_dict(self):
        result = analyze_joule_heating_jax(current=1.0, resistance=1.0, time=1.0)
        assert isinstance(result, dict)

    def test_analyze_keys_present(self):
        result = analyze_joule_heating_jax()
        expected_keys = {
            "current_abA",
            "resistance_abohm",
            "voltage_abV",
            "power_erg_s",
            "power_from_voltage_erg_s",
            "energy_erg",
            "temperature_rise_K",
            "steady_state_temp_K",
            "cooling_rate_erg_s",
            "resistivity_at_temp",
            "resistance_from_geometry",
        }
        assert set(result.keys()) == expected_keys

    def test_analyze_positive_values(self):
        result = analyze_joule_heating_jax(
            current=1.0, resistance=1.0, time=1.0, mass=1.0, specific_heat=4.18e7
        )
        assert float(result["power_erg_s"]) > 0
        assert float(result["energy_erg"]) > 0
        assert float(result["temperature_rise_K"]) > 0
        assert float(result["steady_state_temp_K"]) > 0

    def test_analyze_power_consistency(self):
        result = analyze_joule_heating_jax(current=2.0, resistance=5.0, time=10.0)
        # P = I^2*R = V^2/R when V=I*R
        assert float(result["power_erg_s"]) == pytest.approx(
            float(result["power_from_voltage_erg_s"]), rel=1e-10
        )

    def test_analyze_with_custom_voltage(self):
        result = analyze_joule_heating_jax(current=1.0, resistance=10.0, voltage=10.0)
        # With V=10, R=10: P = V^2/R = 10
        assert float(result["power_from_voltage_erg_s"]) == pytest.approx(10.0)
