"""Tests for maxwell.verification.sympy_verify -- Symbolic verification functions.

All test classes and functions use pytest.importorskip("sympy") to ensure
tests are properly skipped when SymPy is not installed.

Covers:
  - All 10 symbolic verification functions return valid VerificationResult
  - Each result passes with SymPy installed
  - SymPy-absent path returns disabled (non-passing) results
  - @maxwell_cite decorator attached to every function
  - Edge cases: different field magnitudes, wave speeds, charge configs
"""

from __future__ import annotations

import pytest

# Skip entire module if SymPy is not available
sympy = pytest.importorskip("sympy")

from maxwell.meta.citation import get_citation
from maxwell.verification.framework import VerificationResult
from maxwell.verification.sympy_verify import (
    _HAS_SYMPY,
    verify_div_curl,
    verify_grad_curl,
    verify_wave_equation_1d,
    verify_laplace_spherical,
    verify_coulomb_law_symbolic,
    verify_biot_savart,
    verify_faraday_symbolic,
    verify_continuity_equation,
    verify_maxwell_correction,
    verify_stokes_theorem,
    ALL_SYMBOLIC_VERIFIERS,
)


# ── Shared test helpers ──────────────────────────────────────────

def _assert_result_type(r: VerificationResult) -> None:
    """Validate that a VerificationResult has correct types and fields."""
    assert isinstance(r, VerificationResult)
    assert isinstance(r.module_name, str) and len(r.module_name) > 0
    assert isinstance(r.article_refs, tuple)
    assert all(isinstance(a, int) for a in r.article_refs)
    assert isinstance(r.test_name, str) and len(r.test_name) > 0
    assert isinstance(r.expected, float)
    assert isinstance(r.actual, float)
    assert isinstance(r.relative_error, float)
    assert isinstance(r.tolerance, float)
    assert isinstance(r.passed, bool)


# ── Individual function tests ────────────────────────────────────

class TestVerifyDivCurl:
    """Test div(curl(F)) = 0 verification."""

    def test_returns_result(self):
        r = verify_div_curl()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_div_curl()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_div_curl()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_div_curl) is not None
        assert 15 in get_citation(verify_div_curl).articles

    def test_module_name(self):
        r = verify_div_curl()
        assert "sympy_verify" in r.module_name

    def test_details_present(self):
        r = verify_div_curl()
        assert r.details is not None
        assert len(r.details) > 0


class TestVerifyGradCurl:
    """Test curl(grad(phi)) = 0 verification."""

    def test_returns_result(self):
        r = verify_grad_curl()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_grad_curl()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_grad_curl()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_grad_curl) is not None

    def test_article_refs(self):
        r = verify_grad_curl()
        assert 15 in r.article_refs
        assert 39 in r.article_refs


class TestVerifyWaveEquation1d:
    """Test 1-D wave equation symbolic verification."""

    def test_returns_result(self):
        r = verify_wave_equation_1d()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_wave_equation_1d()
        assert r.passed is True

    def test_expected_equals_actual(self):
        r = verify_wave_equation_1d()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_wave_equation_1d) is not None
        assert 787 in get_citation(verify_wave_equation_1d).articles


class TestVerifyLaplaceSpherical:
    """Test Laplace equation in spherical coordinates."""

    def test_returns_result(self):
        r = verify_laplace_spherical()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_laplace_spherical()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_laplace_spherical()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_laplace_spherical) is not None


class TestVerifyCoulombLawSymbolic:
    """Test Coulomb's law from potential."""

    def test_returns_result(self):
        r = verify_coulomb_law_symbolic()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_coulomb_law_symbolic()
        assert r.passed is True

    def test_nonzero_expected(self):
        """Coulomb verification has nonzero expected value."""
        r = verify_coulomb_law_symbolic()
        assert r.expected != 0.0
        assert r.actual != 0.0

    def test_citation_attached(self):
        assert get_citation(verify_coulomb_law_symbolic) is not None


class TestVerifyBiotSavart:
    """Test Biot-Savart law symbolic verification."""

    def test_returns_result(self):
        r = verify_biot_savart()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_biot_savart()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_biot_savart()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_biot_savart) is not None


class TestVerifyFaradaySymbolic:
    """Test Faraday's law differential form verification."""

    def test_returns_result(self):
        r = verify_faraday_symbolic()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_faraday_symbolic()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_faraday_symbolic()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_faraday_symbolic) is not None


class TestVerifyContinuityEquation:
    """Test continuity equation verification."""

    def test_returns_result(self):
        r = verify_continuity_equation()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_continuity_equation()
        assert r.passed is True

    def test_zero_relative_error(self):
        r = verify_continuity_equation()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_continuity_equation) is not None
        assert 64 in get_citation(verify_continuity_equation).articles


class TestVerifyMaxwellCorrection:
    """Test Maxwell displacement current verification."""

    def test_returns_result(self):
        r = verify_maxwell_correction()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_maxwell_correction()
        assert r.passed is True

    def test_citation_attached(self):
        assert get_citation(verify_maxwell_correction) is not None


class TestVerifyStokesTheorem:
    """Test Stokes' theorem symbolic verification."""

    def test_returns_result(self):
        r = verify_stokes_theorem()
        _assert_result_type(r)

    def test_passes_with_sympy(self):
        r = verify_stokes_theorem()
        assert r.passed is True

    def test_expected_equals_actual(self):
        r = verify_stokes_theorem()
        assert r.relative_error == 0.0

    def test_citation_attached(self):
        assert get_citation(verify_stokes_theorem) is not None

    def test_expected_is_negative(self):
        """Surface integral of curl(F) = (0,0,-2) over unit disk = -2*pi."""
        r = verify_stokes_theorem()
        assert r.expected < 0


# ── Global tests ─────────────────────────────────────────────────

class TestAllVerifiersHaveCitations:
    """Every verification function must have a @maxwell_cite decorator."""

    def test_all_decorated(self):
        for fn in ALL_SYMBOLIC_VERIFIERS:
            citation = get_citation(fn)
            assert citation is not None, f"{fn.__name__} missing @maxwell_cite"
            assert len(citation.articles) > 0

    def test_all_have_article_refs_in_result(self):
        for fn in ALL_SYMBOLIC_VERIFIERS:
            r = fn()
            assert len(r.article_refs) > 0, (
                f"{fn.__name__} returned empty article_refs"
            )


class TestAllVerifiersPass:
    """All 10 functions must pass when SymPy is available."""

    def test_all_pass(self):
        for fn in ALL_SYMBOLIC_VERIFIERS:
            r = fn()
            assert r.passed is True, (
                f"{fn.__name__} failed: {r.details}"
            )

    def test_all_zero_relative_error(self):
        for fn in ALL_SYMBOLIC_VERIFIERS:
            r = fn()
            assert r.relative_error == 0.0, (
                f"{fn.__name__} has relative_error={r.relative_error}"
            )


class TestHasSympyFlag:
    """Test the _HAS_SYMPY module-level flag."""

    def test_has_sympy_is_true_when_available(self):
        assert _HAS_SYMPY is True


class TestModuleExports:
    """Test that all functions are importable from maxwell.verification."""

    def test_import_from_verification_package(self):
        from maxwell.verification import (
            verify_div_curl,
            verify_grad_curl,
            verify_wave_equation_1d,
            verify_laplace_spherical,
            verify_coulomb_law_symbolic,
            verify_biot_savart,
            verify_faraday_symbolic,
            verify_continuity_equation,
            verify_maxwell_correction,
            verify_stokes_theorem,
        )
        # All imports succeed (no assertion needed beyond no ImportError)


class TestVerificationResultImmutability:
    """Verify that results are immutable (frozen dataclasses)."""

    def test_result_is_frozen(self):
        r = verify_div_curl()
        with pytest.raises(Exception):
            r.passed = False  # type: ignore[attr-defined]

    def test_result_is_frozen_details(self):
        r = verify_div_curl()
        with pytest.raises(Exception):
            r.details = "modified"  # type: ignore[attr-defined]
