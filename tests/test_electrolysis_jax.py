"""Tests for ElectrolysisJAX -- Part II Electrolysis (Arts. 249-263)."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax.electromagnetism.electrolysis import (
    AVOGADRO_NUMBER_JAX,
    ELEMENTARY_CHARGE_EMU_JAX,
    FARADAY_CONSTANT_JAX,
    R_GAS_CGS_JAX,
    ElectrolysisCellJAX,
    FaradayLawsJAX,
    IonTransportJAX,
    PolarizationJAX,
    battery_back_emf_jax,
    concentration_polarization_jax,
    decomposition_voltage_jax,
    electrochemical_equivalent_jax,
    electrolyte_conductivity_jax,
    faraday_first_law_jax,
    faraday_second_law_jax,
    ion_migration_velocity_jax,
    kohlrausch_law_jax,
    polarization_emf_jax,
    transference_number_jax,
    verify_electrolysis_jax,
)

TOL = 1e-10


# -- TestFaradayLawsJAXPytree ----------------------------------------------------


class TestFaradayLawsJAXPytree:
    """Flatten/unflatten, jit, vmap."""

    def test_flatten_unflatten_default(self):
        obj = FaradayLawsJAX()
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.faraday_constant) == pytest.approx(96485.33212)

    def test_flatten_unflatten_custom(self):
        obj = FaradayLawsJAX(faraday_constant=100000.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 1
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.faraday_constant) == pytest.approx(100000.0)

    def test_jit_compatible(self):
        obj = FaradayLawsJAX()
        jit_fn = jax.jit(
            lambda o: o.mass_from_charge(
                jnp.array(100.0), jnp.array(107.87), jnp.array(1.0)
            )
        )
        result = jit_fn(obj)
        assert float(result) > 0

    def test_tree_map(self):
        obj = FaradayLawsJAX(faraday_constant=100000.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.faraday_constant) == pytest.approx(200000.0)


# -- TestFaradayLawsJAXComputation -----------------------------------------------


class TestFaradayLawsJAXComputation:
    """Computation correctness."""

    def test_mass_from_charge_silver(self):
        obj = FaradayLawsJAX()
        # Silver: M=107.87, n=1, Q=100 abC
        m = obj.mass_from_charge(jnp.array(100.0), jnp.array(107.87), jnp.array(1.0))
        expected = 100.0 * 107.87 / 96485.33212
        assert float(m) == pytest.approx(expected, rel=1e-10)

    def test_mass_from_current_time(self):
        obj = FaradayLawsJAX()
        # I=1 abA, t=100s, M=63.55 (Cu), n=2
        m = obj.mass_from_current_time(
            jnp.array(1.0), jnp.array(100.0), jnp.array(63.55), jnp.array(2.0)
        )
        expected = 1.0 * 100.0 * 63.55 / (2.0 * 96485.33212)
        assert float(m) == pytest.approx(expected, rel=1e-10)

    def test_electrochemical_equivalent(self):
        obj = FaradayLawsJAX()
        Z = obj.electrochemical_equivalent(jnp.array(107.87), jnp.array(1.0))
        expected = 107.87 / 96485.33212
        assert float(Z) == pytest.approx(expected, rel=1e-10)

    def test_required_charge(self):
        obj = FaradayLawsJAX()
        mass = jnp.array(0.1)  # 0.1 g silver
        Q = obj.required_charge(mass, jnp.array(107.87), jnp.array(1.0))
        expected = 0.1 * 1.0 * 96485.33212 / 107.87
        assert float(Q) == pytest.approx(expected, rel=1e-10)

    def test_current_for_mass_time(self):
        obj = FaradayLawsJAX()
        I = obj.current_for_mass_time(
            jnp.array(0.1), jnp.array(100.0), jnp.array(107.87), jnp.array(1.0)
        )
        expected = 0.1 * 1.0 * 96485.33212 / (107.87 * 100.0)
        assert float(I) == pytest.approx(expected, rel=1e-10)

    def test_mass_from_charge_roundtrip(self):
        obj = FaradayLawsJAX()
        Q_orig = jnp.array(500.0)
        m = obj.mass_from_charge(Q_orig, jnp.array(63.55), jnp.array(2.0))
        Q_recovered = obj.required_charge(m, jnp.array(63.55), jnp.array(2.0))
        assert float(Q_recovered) == pytest.approx(float(Q_orig), rel=1e-10)

    def test_mass_current_time_consistency(self):
        obj = FaradayLawsJAX()
        # Both methods should give same result for same physical scenario
        m1 = obj.mass_from_charge(jnp.array(100.0), jnp.array(107.87), jnp.array(1.0))
        m2 = obj.mass_from_current_time(
            jnp.array(1.0), jnp.array(100.0), jnp.array(107.87), jnp.array(1.0)
        )
        assert float(m1) == pytest.approx(float(m2), rel=1e-10)

    def test_mass_proportional_to_charge(self):
        obj = FaradayLawsJAX()
        m1 = obj.mass_from_charge(jnp.array(100.0), jnp.array(107.87), jnp.array(1.0))
        m2 = obj.mass_from_charge(jnp.array(200.0), jnp.array(107.87), jnp.array(1.0))
        assert float(m2) == pytest.approx(2.0 * float(m1), rel=1e-10)


# -- TestIonTransportJAXPytree ---------------------------------------------------


class TestIonTransportJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        mobilities = jnp.array([5.19e-4, 7.91e-4])
        charges = jnp.array([1.0, -1.0])
        obj = IonTransportJAX(ion_mobilities=mobilities, ion_charges=charges)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 2
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(reconstructed.ion_mobilities, mobilities)
        assert jnp.allclose(reconstructed.ion_charges, charges)

    def test_jit_migration(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4]), ion_charges=jnp.array([1.0])
        )
        jit_fn = jax.jit(lambda o: o.migration_velocity(jnp.array(1e6)))
        result = jit_fn(obj)
        assert float(result[0]) > 0

    def test_tree_map(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([1.0, 2.0]), ion_charges=jnp.array([1.0, -1.0])
        )
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert jnp.allclose(doubled.ion_mobilities, jnp.array([2.0, 4.0]))
        assert jnp.allclose(doubled.ion_charges, jnp.array([2.0, -2.0]))


# -- TestIonTransportJAXComputation ----------------------------------------------


class TestIonTransportJAXComputation:
    """Computation correctness."""

    def test_migration_velocity_single_ion(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4]), ion_charges=jnp.array([1.0])
        )
        v = obj.migration_velocity(jnp.array(1e6))
        expected = 5.19e-4 * 1.0 * 1e6
        assert float(v[0]) == pytest.approx(expected, rel=1e-10)

    def test_migration_velocity_multiple_ions(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4, 7.91e-4]),
            ion_charges=jnp.array([1.0, -1.0]),
        )
        v = obj.migration_velocity(jnp.array(1e6))
        assert float(v[0]) == pytest.approx(5.19e-4 * 1.0 * 1e6)
        assert float(v[1]) == pytest.approx(7.91e-4 * (-1.0) * 1e6)

    def test_electrolyte_conductivity(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4, 7.91e-4]),
            ion_charges=jnp.array([1.0, -1.0]),
        )
        conc = jnp.array([1e-4, 1e-4])  # 0.1 M = 1e-4 mol/cm^3
        sigma = obj.electrolyte_conductivity(conc)
        expected = 96485.33212 * (1e-4 * 1.0 * 5.19e-4 + 1e-4 * 1.0 * 7.91e-4)
        assert float(sigma) == pytest.approx(expected, rel=1e-10)

    def test_transference_numbers(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4, 7.91e-4]),
            ion_charges=jnp.array([1.0, -1.0]),
        )
        t = obj.transference_numbers()
        # contributions: 5.19e-4, 7.91e-4
        # total: 13.10e-4
        # t_cation = 5.19/13.10, t_anion = 7.91/13.10
        assert float(t["t_i"][0]) == pytest.approx(5.19 / 13.10, rel=1e-10)
        assert float(t["t_i"][1]) == pytest.approx(7.91 / 13.10, rel=1e-10)

    def test_transference_numbers_sum_to_one(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4, 7.91e-4]),
            ion_charges=jnp.array([1.0, -1.0]),
        )
        t = obj.transference_numbers()
        t_sum = float(t["t_i"][0] + t["t_i"][1])
        assert t_sum == pytest.approx(1.0, rel=1e-10)

    def test_limiting_current_density(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4]), ion_charges=jnp.array([2.0])
        )
        i_L = obj.limiting_current_density(
            concentrations=jnp.array([1e-4]),
            diffusion_coeffs=jnp.array([7e-6]),
            layer_thickness=jnp.array([0.01]),
            charge_numbers=jnp.array([2.0]),
        )
        expected = 2.0 * 96485.33212 * 7e-6 * 1e-4 / 0.01
        assert float(i_L[0]) == pytest.approx(expected, rel=1e-10)

    def test_conductivity_proportional_to_concentration(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4]), ion_charges=jnp.array([1.0])
        )
        s1 = obj.electrolyte_conductivity(jnp.array([1e-4]))
        s2 = obj.electrolyte_conductivity(jnp.array([2e-4]))
        assert float(s2) == pytest.approx(2.0 * float(s1), rel=1e-10)

    def test_migration_velocity_sign_follows_charge(self):
        obj = IonTransportJAX(
            ion_mobilities=jnp.array([5.19e-4, 7.91e-4]),
            ion_charges=jnp.array([1.0, -1.0]),
        )
        v = obj.migration_velocity(jnp.array(1e6))
        # Cation moves positive, anion moves negative
        assert float(v[0]) > 0
        assert float(v[1]) < 0


# -- TestPolarizationJAXPytree ---------------------------------------------------


class TestPolarizationJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 4
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.reversible_emf) == pytest.approx(1.23e8)

    def test_jit_activation(self):
        obj = PolarizationJAX(reversible_emf=1.23e8, exchange_current_density=1e-6)
        jit_fn = jax.jit(lambda o: o.activation_overpotential(jnp.array(0.01)))
        result = jit_fn(obj)
        assert float(result) > 0

    def test_tree_map(self):
        obj = PolarizationJAX(
            reversible_emf=1.0e8,
            exchange_current_density=1.0,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.reversible_emf) == pytest.approx(2.0e8)
        assert float(doubled.exchange_current_density) == pytest.approx(2.0)


# -- TestPolarizationJAXComputation ----------------------------------------------


class TestPolarizationJAXComputation:
    """Computation correctness."""

    def test_activation_overpotential_positive_current(self):
        obj = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        eta = obj.activation_overpotential(jnp.array(0.01))
        assert float(eta) > 0

    def test_activation_zero_current(self):
        obj = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        eta = obj.activation_overpotential(jnp.array(0.0))
        # asinh(0) = 0, so eta should be 0
        assert float(eta) == pytest.approx(0.0, abs=1e-15)

    def test_activation_scales_with_current(self):
        obj = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        eta1 = obj.activation_overpotential(jnp.array(0.01))
        eta2 = obj.activation_overpotential(jnp.array(0.1))
        assert float(eta2) > float(eta1)

    def test_decomposition_voltage(self):
        obj = PolarizationJAX(reversible_emf=1.23e8, exchange_current_density=1e-6)
        V = obj.decomposition_voltage(
            anode_overpotential=jnp.array(0.4e8),
            cathode_overpotential=jnp.array(-0.1e8),
            ohmic_drop=jnp.array(0.05e8),
        )
        expected = 1.23e8 + 0.4e8 + 0.1e8 + 0.05e8
        assert float(V) == pytest.approx(expected, rel=1e-10)

    def test_decomposition_voltage_positive_cathode(self):
        obj = PolarizationJAX(reversible_emf=1.0e8, exchange_current_density=1e-6)
        V = obj.decomposition_voltage(
            anode_overpotential=jnp.array(0.2e8),
            cathode_overpotential=jnp.array(0.1e8),
            ohmic_drop=jnp.array(0.05e8),
        )
        # |0.1e8| = 0.1e8
        expected = 1.0e8 + 0.2e8 + 0.1e8 + 0.05e8
        assert float(V) == pytest.approx(expected, rel=1e-10)

    def test_concentration_overpotential(self):
        obj = PolarizationJAX(reversible_emf=1.23e8, exchange_current_density=1e-6)
        eta = obj.concentration_overpotential(
            bulk_conc=jnp.array(1e-4),
            surface_conc=jnp.array(1e-5),
            diffusion_coeff=jnp.array(7e-6),
            diffusion_thickness=jnp.array(0.01),
            current_density=jnp.array(0.01),
            charge_number=jnp.array(2.0),
        )
        # Should be negative (depletion)
        assert float(eta) < 0

    def test_total_polarization_emf(self):
        obj = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=298.15,
        )
        E_total = obj.total_polarization_emf(jnp.array(0.01))
        eta = obj.activation_overpotential(jnp.array(0.01))
        expected = 1.23e8 + float(eta)
        assert float(E_total) == pytest.approx(expected, rel=1e-10)

    def test_temperature_affects_overpotential(self):
        obj_hot = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=350.0,
        )
        obj_cold = PolarizationJAX(
            reversible_emf=1.23e8,
            exchange_current_density=1e-6,
            transfer_coefficient=0.5,
            temperature=250.0,
        )
        eta_hot = obj_hot.activation_overpotential(jnp.array(0.01))
        eta_cold = obj_cold.activation_overpotential(jnp.array(0.01))
        # Higher temperature -> larger thermal voltage -> larger overpotential
        assert float(eta_hot) > float(eta_cold)


# -- TestElectrolysisCellJAXPytree -----------------------------------------------


class TestElectrolysisCellJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
            temperature=298.15,
        )
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 7
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.electrode_area) == pytest.approx(1.0)
        assert int(float(reconstructed.valence)) == 2

    def test_jit_mass_deposited(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        jit_fn = jax.jit(lambda o: o.mass_deposited(jnp.array(1.0), jnp.array(100.0)))
        result = jit_fn(obj)
        assert float(result) > 0

    def test_tree_map(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.0e8,
            temperature=298.15,
        )
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.electrode_area) == pytest.approx(2.0)
        assert float(doubled.molar_mass) == pytest.approx(127.1)


# -- TestElectrolysisCellJAXComputation ------------------------------------------


class TestElectrolysisCellJAXComputation:
    """Computation correctness."""

    def test_cell_resistance(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        R = obj.cell_resistance()
        expected = 1.0 / (0.1 * 1.0)
        assert float(R) == pytest.approx(expected, rel=1e-10)

    def test_mass_deposited(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        m = obj.mass_deposited(jnp.array(1.0), jnp.array(100.0))
        expected = 1.0 * 100.0 * 63.55 / (2.0 * 96485.33212)
        assert float(m) == pytest.approx(expected, rel=1e-10)

    def test_required_voltage(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        V = obj.required_voltage(jnp.array(1.0))
        # Must be >= reversible_emf
        assert float(V) >= float(obj.reversible_emf)

    def test_energy_per_gram_positive(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        E = obj.energy_per_gram(jnp.array(1.0))
        assert float(E) > 0

    def test_analyze_returns_dict(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        result = obj.analyze(jnp.array(1.0), jnp.array(100.0))
        expected_keys = {
            "mass_deposited",
            "charge_passed",
            "cell_resistance",
            "ir_drop",
            "overpotential",
            "required_voltage",
            "energy_consumed",
            "energy_per_gram",
            "power",
        }
        assert set(result.keys()) == expected_keys

    def test_analyze_mass_consistency(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        result = obj.analyze(jnp.array(1.0), jnp.array(100.0))
        m_direct = obj.mass_deposited(jnp.array(1.0), jnp.array(100.0))
        assert float(result["mass_deposited"]) == pytest.approx(
            float(m_direct), rel=1e-10
        )


# -- TestStandaloneElectrolysisFunctions -----------------------------------------


class TestStandaloneElectrolysisFunctions:
    """All standalone function correctness."""

    def test_faraday_first_law(self):
        m = faraday_first_law_jax(jnp.array(1.0), jnp.array(100.0), jnp.array(0.001))
        expected = 1.0 * 100.0 * 0.001
        assert float(m) == pytest.approx(expected)

    def test_faraday_second_law(self):
        m = faraday_second_law_jax(
            jnp.array(1.0), jnp.array(100.0), jnp.array(107.87), jnp.array(1.0)
        )
        expected = 1.0 * 100.0 * 107.87 / (1.0 * 96485.33212)
        assert float(m) == pytest.approx(expected, rel=1e-10)

    def test_electrochemical_equivalent(self):
        Z = electrochemical_equivalent_jax(jnp.array(107.87), jnp.array(1.0))
        expected = 107.87 / 96485.33212
        assert float(Z) == pytest.approx(expected, rel=1e-10)

    def test_polarization_emf(self):
        E = polarization_emf_jax(
            jnp.array(1.23e8),
            jnp.array(0.01),
            jnp.array(1e-6),
            jnp.array(0.5),
            jnp.array(298.15),
        )
        assert float(E) > 1.23e8  # Should be greater than reversible

    def test_decomposition_voltage(self):
        V = decomposition_voltage_jax(
            jnp.array(1.23e8), jnp.array(0.4e8), jnp.array(-0.1e8), jnp.array(0.05e8)
        )
        expected = 1.23e8 + 0.4e8 + 0.1e8 + 0.05e8
        assert float(V) == pytest.approx(expected)

    def test_ion_migration_velocity(self):
        v = ion_migration_velocity_jax(
            jnp.array(5.19e-4), jnp.array(1e6), jnp.array(1.0)
        )
        expected = 5.19e-4 * 1e6 * 1.0
        assert float(v) == pytest.approx(expected)

    def test_electrolyte_conductivity(self):
        sigma = electrolyte_conductivity_jax(
            jnp.array([1e-4, 1e-4]),
            jnp.array([1.0, -1.0]),
            jnp.array([5.19e-4, 7.91e-4]),
        )
        expected = 96485.33212 * (1e-4 * 1.0 * 5.19e-4 + 1e-4 * 1.0 * 7.91e-4)
        assert float(sigma) == pytest.approx(expected, rel=1e-10)

    def test_kohlrausch_law(self):
        Lambda = kohlrausch_law_jax(jnp.array(149.9), jnp.array(0.01), jnp.array(94.0))
        expected = 149.9 - 94.0 * np.sqrt(0.01)
        assert float(Lambda) == pytest.approx(expected, rel=1e-10)

    def test_concentration_polarization(self):
        eta = concentration_polarization_jax(
            jnp.array(1e-4),
            jnp.array(1e-5),
            jnp.array(7e-6),
            jnp.array(0.01),
            jnp.array(0.01),
            jnp.array(2.0),
            jnp.array(298.15),
        )
        assert float(eta) < 0  # Depletion -> negative overpotential

    def test_battery_back_emf(self):
        V = battery_back_emf_jax(
            jnp.array(1.1e8), jnp.array(1e9), jnp.array(0.1), jnp.array(0.0)
        )
        expected = 1.1e8 - 0.1 * 1e9
        assert float(V) == pytest.approx(expected)

    def test_transference_number(self):
        t = transference_number_jax(jnp.array(50.1), jnp.array(76.3))
        Lambda_0 = 50.1 + 76.3
        assert float(t["t_cation"]) == pytest.approx(50.1 / Lambda_0, rel=1e-10)
        assert float(t["t_anion"]) == pytest.approx(76.3 / Lambda_0, rel=1e-10)
        assert float(t["t_cation"] + t["t_anion"]) == pytest.approx(1.0, rel=1e-10)


# -- TestJITElectrolysis ---------------------------------------------------------


class TestJITElectrolysis:
    """JIT compilation for all classes."""

    def test_jit_faraday_laws(self):
        @jax.jit
        def compute(I, t, M, n):
            obj = FaradayLawsJAX()
            return obj.mass_from_current_time(I, t, M, n)

        result = compute(1.0, 100.0, 63.55, 2.0)
        assert float(result) > 0

    def test_jit_ion_transport(self):
        mobilities = jnp.array([5.19e-4, 7.91e-4])
        charges = jnp.array([1.0, -1.0])
        obj = IonTransportJAX(ion_mobilities=mobilities, ion_charges=charges)
        jit_fn = jax.jit(
            lambda o: (
                o.migration_velocity(jnp.array(1e6)),
                o.electrolyte_conductivity(jnp.array([1e-4, 1e-4])),
            )
        )
        results = jit_fn(obj)
        # velocity can be negative, just check shape
        assert results[0].shape == (2,)
        assert float(results[1]) > 0

    def test_jit_polarization(self):
        obj = PolarizationJAX(reversible_emf=1.23e8, exchange_current_density=1e-6)
        jit_fn = jax.jit(
            lambda o: (
                o.activation_overpotential(jnp.array(0.01)),
                o.decomposition_voltage(
                    jnp.array(0.4e8), jnp.array(-0.1e8), jnp.array(0.05e8)
                ),
            )
        )
        results = jit_fn(obj)
        assert float(results[0]) > 0
        assert float(results[1]) > 0

    def test_jit_electrolysis_cell(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.1,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        jit_fn = jax.jit(lambda o: o.cell_resistance())
        result = jit_fn(obj)
        assert float(result) == pytest.approx(10.0)


# -- TestAutoDiffElectrolysis ----------------------------------------------------


class TestAutoDiffElectrolysis:
    """Gradients through electrolysis functions."""

    def test_grad_mass_wrt_current(self):
        grad_fn = jax.grad(
            lambda I: faraday_second_law_jax(
                I, jnp.array(100.0), jnp.array(63.55), jnp.array(2.0)
            )
        )
        g = grad_fn(1.0)
        expected = 100.0 * 63.55 / (2.0 * 96485.33212)
        assert float(g) == pytest.approx(expected, rel=1e-10)

    def test_grad_mass_wrt_molar_mass(self):
        grad_fn = jax.grad(
            lambda M: faraday_second_law_jax(
                jnp.array(1.0), jnp.array(100.0), M, jnp.array(2.0)
            )
        )
        g = grad_fn(63.55)
        expected = 1.0 * 100.0 / (2.0 * 96485.33212)
        assert float(g) == pytest.approx(expected, rel=1e-10)

    def test_grad_activation_wrt_current_density(self):
        grad_fn = jax.grad(
            lambda j: polarization_emf_jax(
                jnp.array(1.23e8), j, jnp.array(1e-6), jnp.array(0.5), jnp.array(298.15)
            )
        )
        g = grad_fn(0.01)
        # Positive current -> positive gradient
        assert float(g) > 0

    def test_grad_conductivity_wrt_concentration(self):
        grad_fn = jax.grad(
            lambda c: electrolyte_conductivity_jax(
                jnp.array([c, c]), jnp.array([1.0, -1.0]), jnp.array([5.19e-4, 7.91e-4])
            )
        )
        g = grad_fn(1e-4)
        assert float(g) > 0

    def test_grad_cell_resistance_wrt_spacing(self):
        grad_fn = jax.grad(
            lambda d: ElectrolysisCellJAX(
                electrode_area=1.0,
                electrode_spacing=d,
                electrolyte_conductivity=0.1,
                molar_mass=63.55,
                valence=2,
                reversible_emf=1.1e8,
            ).cell_resistance()
        )
        g = grad_fn(1.0)
        expected = 1.0 / (0.1 * 1.0)
        assert float(g) == pytest.approx(expected, rel=1e-10)


# -- TestVmapElectrolysis --------------------------------------------------------


class TestVmapElectrolysis:
    """Vectorization over arrays of inputs."""

    def test_vmap_faraday_second_law(self):
        currents = jnp.array([0.5, 1.0, 2.0])
        masses = jax.vmap(
            lambda I: faraday_second_law_jax(
                I, jnp.array(100.0), jnp.array(63.55), jnp.array(2.0)
            )
        )(currents)
        assert masses.shape == (3,)
        # Monotonically increasing
        assert jnp.all(jnp.diff(masses) > 0)

    def test_vmap_migration_velocity(self):
        fields = jnp.array([1e5, 1e6, 1e7])
        velocities = jax.vmap(
            lambda E: ion_migration_velocity_jax(jnp.array(5.19e-4), E, jnp.array(1.0))
        )(fields)
        assert velocities.shape == (3,)
        assert float(velocities[2]) > float(velocities[1]) > float(velocities[0])

    def test_vmap_kohlrausch_law(self):
        concs = jnp.array([0.001, 0.01, 0.1])
        lambdas = jax.vmap(
            lambda c: kohlrausch_law_jax(jnp.array(149.9), c, jnp.array(94.0))
        )(concs)
        assert lambdas.shape == (3,)
        # Higher concentration -> lower molar conductivity
        assert jnp.all(jnp.diff(lambdas) < 0)

    def test_vmap_decomposition_voltage(self):
        ohmic_drops = jnp.array([0.01e8, 0.05e8, 0.1e8])
        voltages = jax.vmap(
            lambda ir: decomposition_voltage_jax(
                jnp.array(1.23e8), jnp.array(0.4e8), jnp.array(-0.1e8), ir
            )
        )(ohmic_drops)
        assert voltages.shape == (3,)
        assert jnp.all(jnp.diff(voltages) > 0)


# -- TestNumPyElectrolysisComparison ---------------------------------------------


class TestNumPyElectrolysisComparison:
    """JAX vs NumPy comparison."""

    def test_faraday_second_law_numpy_equiv(self):
        I, t, M, n = 1.0, 100.0, 63.55, 2.0
        np_result = I * t * M / (n * 96485.33212)
        jax_result = faraday_second_law_jax(
            jnp.array(I), jnp.array(t), jnp.array(M), jnp.array(n)
        )
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_kohlrausch_law_numpy_equiv(self):
        L0, c, K = 149.9, 0.01, 94.0
        np_result = L0 - K * np.sqrt(c)
        jax_result = kohlrausch_law_jax(jnp.array(L0), jnp.array(c), jnp.array(K))
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_electrolyte_conductivity_numpy_equiv(self):
        c = np.array([1e-4, 1e-4])
        z = np.array([1.0, -1.0])
        u = np.array([5.19e-4, 7.91e-4])
        np_result = 96485.33212 * np.sum(c * np.abs(z) * u)
        jax_result = electrolyte_conductivity_jax(
            jnp.array(c), jnp.array(z), jnp.array(u)
        )
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_decomposition_voltage_numpy_equiv(self):
        E_rev, eta_a, eta_c, ir = 1.23e8, 0.4e8, -0.1e8, 0.05e8
        np_result = E_rev + eta_a + abs(eta_c) + ir
        jax_result = decomposition_voltage_jax(
            jnp.array(E_rev), jnp.array(eta_a), jnp.array(eta_c), jnp.array(ir)
        )
        assert float(jax_result) == pytest.approx(float(np_result))

    def test_constants_match_numpy(self):
        assert float(FARADAY_CONSTANT_JAX) == pytest.approx(96485.33212)
        assert float(ELEMENTARY_CHARGE_EMU_JAX) == pytest.approx(1.602176634e-20)
        assert float(AVOGADRO_NUMBER_JAX) == pytest.approx(6.02214076e23)
        assert float(R_GAS_CGS_JAX) == pytest.approx(8.314462618e7)


# -- TestVerifyElectrolysis ------------------------------------------------------


class TestVerifyElectrolysis:
    """verify_electrolysis_jax behavior."""

    def test_verify_passes(self):
        result = verify_electrolysis_jax()
        assert result["verified"] is True

    def test_verify_keys_present(self):
        result = verify_electrolysis_jax()
        expected_keys = {
            "first_law_ok",
            "roundtrip_ok",
            "transference_ok",
            "decomposition_ok",
            "m_first",
            "m_second",
            "Q_recovered",
            "t_sum",
            "V_decomp",
            "verified",
        }
        assert set(result.keys()) == expected_keys

    def test_verify_mass_consistency(self):
        result = verify_electrolysis_jax()
        assert float(result["m_first"]) == pytest.approx(
            float(result["m_second"]), rel=1e-10
        )


# -- TestEdgeCasesElectrolysis ---------------------------------------------------


class TestEdgeCasesElectrolysis:
    """Edge cases and boundary conditions."""

    def test_zero_current_gives_zero_mass(self):
        m = faraday_second_law_jax(
            jnp.array(0.0), jnp.array(100.0), jnp.array(63.55), jnp.array(2.0)
        )
        assert float(m) == pytest.approx(0.0, abs=1e-15)

    def test_zero_time_gives_zero_mass(self):
        m = faraday_second_law_jax(
            jnp.array(1.0), jnp.array(0.0), jnp.array(63.55), jnp.array(2.0)
        )
        assert float(m) == pytest.approx(0.0, abs=1e-15)

    def test_zero_conductivity_safe_div(self):
        obj = ElectrolysisCellJAX(
            electrode_area=1.0,
            electrode_spacing=1.0,
            electrolyte_conductivity=0.0,
            molar_mass=63.55,
            valence=2,
            reversible_emf=1.1e8,
        )
        R = obj.cell_resistance()
        # safe_div returns 0.0 for division by zero
        assert float(R) == pytest.approx(0.0, abs=1e-15)

    def test_negative_cathode_overpotential_uses_abs(self):
        V = decomposition_voltage_jax(
            jnp.array(1.0e8), jnp.array(0.2e8), jnp.array(-0.3e8), jnp.array(0.05e8)
        )
        expected = 1.0e8 + 0.2e8 + 0.3e8 + 0.05e8
        assert float(V) == pytest.approx(expected)

    def test_kohlrausch_zero_concentration(self):
        Lambda = kohlrausch_law_jax(jnp.array(149.9), jnp.array(0.0), jnp.array(94.0))
        assert float(Lambda) == pytest.approx(149.9)
