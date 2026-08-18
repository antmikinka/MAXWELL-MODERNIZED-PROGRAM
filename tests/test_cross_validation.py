"""Tests for maxwell.verification.cross_validation."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.verification.cross_validation import (
    validate_cgs_si_roundtrip,
    validate_faraday_self_consistency,
    validate_maxwell_equations_consistency,
    validate_stress_energy_consistency,
)


class TestValidateStressEnergyConsistency:
    """Test stress-energy cross-validation."""

    def test_returns_results(self):
        results = validate_stress_energy_consistency()
        assert isinstance(results, list)
        assert len(results) == 2

    def test_stress_trace(self):
        results = validate_stress_energy_consistency()
        trace = [r for r in results if "Stress tensor trace" in r.test_name]
        assert len(trace) == 1
        assert trace[0].passed
        # Trace should be negative (energy density)
        assert trace[0].expected < 0
        assert trace[0].actual < 0

    def test_energy_density(self):
        results = validate_stress_energy_consistency()
        energy = [r for r in results if "EM pressure" in r.test_name]
        assert len(energy) == 1
        assert energy[0].passed
        # Energy density should be positive
        assert energy[0].expected > 0
        assert energy[0].actual > 0

    def test_error_within_tolerance(self):
        results = validate_stress_energy_consistency()
        for r in results:
            assert r.relative_error <= r.tolerance


class TestValidateFaradaySelfConsistency:
    """Test Faraday self-consistency validation."""

    def test_returns_results(self):
        results = validate_faraday_self_consistency()
        assert isinstance(results, list)
        assert len(results) == 1

    def test_faraday_emf(self):
        results = validate_faraday_self_consistency()
        emf = results[0]
        assert emf.passed
        assert "Faraday" in emf.test_name
        # EMF should be negative for positive flux change rate
        assert emf.expected < 0
        assert emf.actual < 0

    def test_error_within_tolerance(self):
        results = validate_faraday_self_consistency()
        for r in results:
            assert r.relative_error <= r.tolerance


class TestValidateMaxwellEquationsConsistency:
    """Test Maxwell equations consistency validation."""

    def test_returns_results(self):
        results = validate_maxwell_equations_consistency()
        assert isinstance(results, list)
        assert len(results) == 2

    def test_gauss_law_electric(self):
        results = validate_maxwell_equations_consistency()
        gauss_e = [r for r in results if "Gauss law electric" in r.test_name]
        assert len(gauss_e) == 1
        assert gauss_e[0].passed

    def test_gauss_law_magnetic(self):
        results = validate_maxwell_equations_consistency()
        gauss_m = [r for r in results if "Gauss law magnetic" in r.test_name]
        assert len(gauss_m) == 1
        assert gauss_m[0].passed


class TestValidateCgsSiRoundtrip:
    """Test CGS-SI roundtrip validation."""

    def test_returns_results(self):
        results = validate_cgs_si_roundtrip()
        assert isinstance(results, list)
        assert len(results) == 3

    def test_charge_roundtrip(self):
        results = validate_cgs_si_roundtrip()
        q_test = [r for r in results if "charge" in r.test_name.lower()]
        assert len(q_test) == 1
        assert q_test[0].passed
        assert q_test[0].expected == pytest.approx(1.0)
        assert q_test[0].actual == pytest.approx(1.0, rel=1e-10)

    def test_potential_roundtrip(self):
        results = validate_cgs_si_roundtrip()
        v_test = [r for r in results if "potential" in r.test_name.lower()]
        assert len(v_test) == 1
        assert v_test[0].passed
        assert v_test[0].expected == pytest.approx(1.0)
        assert v_test[0].actual == pytest.approx(1.0, rel=1e-10)

    def test_tesla_gauss_roundtrip(self):
        results = validate_cgs_si_roundtrip()
        b_test = [
            r for r in results if "Gauss" in r.test_name and "Tesla" in r.test_name
        ]
        assert len(b_test) == 1
        assert b_test[0].passed

    def test_tight_tolerance(self):
        results = validate_cgs_si_roundtrip()
        for r in results:
            assert r.tolerance <= 1e-12
            assert r.relative_error <= r.tolerance
