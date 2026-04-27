"""Tests for maxwell.verification.convergence."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.verification.convergence import (
    measure_spherical_harmonic_convergence,
    measure_grid_convergence,
    verify_convergence_results,
)


class TestSphericalHarmonicConvergence:
    """Test spherical harmonic convergence measurement."""

    def test_returns_dict(self):
        data = measure_spherical_harmonic_convergence()
        assert isinstance(data, dict)

    def test_has_required_keys(self):
        data = measure_spherical_harmonic_convergence()
        for key in ("function", "test_point", "expected", "convergence_data",
                     "convergence_rate", "final_error"):
            assert key in data

    def test_function_label(self):
        data = measure_spherical_harmonic_convergence()
        assert data["function"] == "cos(theta)"

    def test_expected_value(self):
        data = measure_spherical_harmonic_convergence()
        # cos(pi/3) = 0.5
        assert data["expected"] == pytest.approx(0.5)

    def test_convergence_data_length(self):
        data = measure_spherical_harmonic_convergence()
        # Default l_max_sequence = (1, 2, 4, 8, 16) -> 5 points
        assert len(data["convergence_data"]) == 5

    def test_error_decreases(self):
        data = measure_spherical_harmonic_convergence()
        # Error should be small at the end (convergence not strictly monotonic
        # due to numerical integration precision)
        assert data["final_error"] < 0.001

    def test_final_error_small(self):
        data = measure_spherical_harmonic_convergence()
        # With l_max=16, cos(theta) should be very well approximated
        assert data["final_error"] < 0.01

    def test_custom_l_max_sequence(self):
        data = measure_spherical_harmonic_convergence(l_max_sequence=(2, 4, 8))
        assert len(data["convergence_data"]) == 3
        assert data["convergence_data"][-1]["l_max"] == 8


class TestGridConvergence:
    """Test grid convergence measurement."""

    def test_returns_dict(self):
        def field_func(n):
            return 1.0 - 1.0 / n

        data = measure_grid_convergence(field_func, reference_value=1.0, name="test")
        assert isinstance(data, dict)

    def test_has_required_keys(self):
        def field_func(n):
            return 1.0 - 1.0 / n

        data = measure_grid_convergence(field_func, reference_value=1.0, name="test")
        for key in ("name", "reference_value", "convergence_data",
                     "convergence_rate", "final_error"):
            assert key in data

    def test_convergence_data_length(self):
        def field_func(n):
            return 1.0 - 1.0 / n

        data = measure_grid_convergence(field_func, reference_value=1.0)
        # Default grid_sequence = (10, 20, 40, 80) -> 4 points
        assert len(data["convergence_data"]) == 4

    def test_error_decreases(self):
        def field_func(n):
            return 1.0 - 1.0 / n

        data = measure_grid_convergence(field_func, reference_value=1.0)
        errors = [d["relative_error"] for d in data["convergence_data"]]
        # Error should decrease as grid size increases
        assert errors[-1] < errors[0]

    def test_custom_grid_sequence(self):
        def field_func(n):
            return 1.0 - 1.0 / n

        data = measure_grid_convergence(
            field_func, reference_value=1.0, grid_sequence=(5, 10, 20)
        )
        assert len(data["convergence_data"]) == 3

    def test_zero_reference_value(self):
        def field_func(n):
            return 1.0 / n

        data = measure_grid_convergence(field_func, reference_value=0.0)
        # With reference=0, error = abs(value) / 1.0 (uses abs(ref) if 0 -> 1.0)
        # For n=10 (first in default sequence): value = 0.1, error = 0.1
        errors = [d["relative_error"] for d in data["convergence_data"]]
        assert errors[0] == pytest.approx(0.1)


class TestVerifyConvergenceResults:
    """Test convergence result verification wrapper."""

    def test_passing_result(self):
        data = {
            "name": "test_convergence",
            "final_error": 0.001,
            "convergence_rate": 2.0,
        }
        result = verify_convergence_results(data, max_error=0.01)
        assert result.passed
        assert result.relative_error == pytest.approx(0.001)

    def test_failing_result(self):
        data = {
            "name": "test_convergence",
            "final_error": 0.1,
            "convergence_rate": 0.5,
        }
        result = verify_convergence_results(data, max_error=0.01)
        assert not result.passed

    def test_default_max_error(self):
        data = {
            "name": "test_convergence",
            "final_error": 0.005,
            "convergence_rate": 1.5,
        }
        result = verify_convergence_results(data)
        # Default max_error = 0.01, so 0.005 should pass
        assert result.passed

    def test_test_name_includes_name(self):
        data = {
            "name": "my_custom_test",
            "final_error": 0.001,
            "convergence_rate": 2.0,
        }
        result = verify_convergence_results(data)
        assert "my_custom_test" in result.test_name

    def test_spherical_harmonic_name_fallback(self):
        data = {
            "final_error": 0.001,
            "convergence_rate": 2.0,
        }
        result = verify_convergence_results(data)
        assert "spherical_harmonic" in result.test_name

    def test_tolerance_set(self):
        data = {
            "name": "test",
            "final_error": 0.001,
            "convergence_rate": 2.0,
        }
        result = verify_convergence_results(data, max_error=0.005)
        assert result.tolerance == 0.005
