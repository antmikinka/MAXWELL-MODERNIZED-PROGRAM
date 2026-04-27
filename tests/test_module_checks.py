"""Tests for maxwell.verification.module_checks."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.verification.module_checks import (
    verify_spherical_harmonics,
    verify_electrostatics,
    verify_magnetism,
    verify_electromagnetism,
    verify_vector_calculus,
    verify_elliptic_integrals,
    verify_units_and_dimensions,
    verify_optics_and_waves,
)


class TestVerifySphericalHarmonics:
    """Test spherical harmonic verification."""

    def test_returns_results(self):
        results = verify_spherical_harmonics()
        assert isinstance(results, list)
        assert len(results) >= 5

    def test_legendre_p0(self):
        results = verify_spherical_harmonics()
        p0 = [r for r in results if r.test_name == "P_0(0.5) = 1"]
        assert len(p0) == 1
        assert p0[0].passed
        assert p0[0].expected == 1.0

    def test_legendre_p1(self):
        results = verify_spherical_harmonics()
        p1 = [r for r in results if "P_1(0.7)" in r.test_name]
        assert len(p1) == 1
        assert p1[0].passed
        assert p1[0].expected == 0.7

    def test_legendre_p2(self):
        results = verify_spherical_harmonics()
        p2 = [r for r in results if "P_2(0.5)" in r.test_name]
        assert len(p2) == 1
        assert p2[0].passed
        expected = (3 * 0.5**2 - 1) / 2
        assert p2[0].expected == expected

    def test_y00_magnitude(self):
        results = verify_spherical_harmonics()
        y00 = [r for r in results if "Y_00" in r.test_name]
        assert len(y00) == 1
        assert y00[0].passed
        assert y00[0].expected == pytest.approx(1.0 / np.sqrt(4 * np.pi))

    def test_addition_theorem(self):
        results = verify_spherical_harmonics()
        add = [r for r in results if "Addition theorem" in r.test_name]
        assert len(add) == 2  # l=0 and l=1
        for r in add:
            assert r.passed

    def test_all_pass(self):
        results = verify_spherical_harmonics()
        for r in results:
            assert r.passed, f"{r.test_name} failed: {r.relative_error}"


class TestVerifyElectrostatics:
    """Test electrostatics verification."""

    def test_returns_results(self):
        results = verify_electrostatics()
        assert isinstance(results, list)
        assert len(results) >= 3

    def test_point_charge_field(self):
        results = verify_electrostatics()
        e_field = [r for r in results if "Point charge E" in r.test_name]
        assert len(e_field) == 1
        assert e_field[0].passed
        assert e_field[0].expected == pytest.approx(1.0 / 5.0**2)

    def test_point_charge_potential(self):
        results = verify_electrostatics()
        pot = [r for r in results if "Point charge V" in r.test_name]
        assert len(pot) == 1
        assert pot[0].passed
        assert pot[0].expected == pytest.approx(1.0 / 5.0)

    def test_gauss_law_flux(self):
        results = verify_electrostatics()
        flux = [r for r in results if "Gauss law" in r.test_name]
        assert len(flux) == 1
        assert flux[0].passed
        assert flux[0].expected == pytest.approx(4 * np.pi, abs=0.1)

    def test_all_pass(self):
        results = verify_electrostatics()
        for r in results:
            assert r.passed, f"{r.test_name} failed"


class TestVerifyMagnetism:
    """Test magnetism verification."""

    def test_returns_results(self):
        results = verify_magnetism()
        assert isinstance(results, list)
        assert len(results) >= 2

    def test_helmholtz_coil(self):
        results = verify_magnetism()
        helm = [r for r in results if "Helmholtz" in r.test_name]
        assert len(helm) == 1
        # B_center > 0 check: actual should be positive
        assert helm[0].actual > 0.0

    def test_magnetic_moment(self):
        results = verify_magnetism()
        mag = [r for r in results if "Magnetic moment" in r.test_name]
        assert len(mag) == 1
        assert mag[0].passed
        assert mag[0].actual > 0.0


class TestVerifyElectromagnetism:
    """Test electromagnetism verification."""

    def test_returns_results(self):
        results = verify_electromagnetism()
        assert isinstance(results, list)
        assert len(results) >= 3

    def test_lorentz_force(self):
        results = verify_electromagnetism()
        lorentz = [r for r in results if "Lorentz" in r.test_name]
        assert len(lorentz) == 1
        assert lorentz[0].passed
        # F = I * (L x B), L=(10,0,0), B=(0,0,100)
        # L x B = (0, -1000, 0), so Fy = -1000
        assert lorentz[0].actual == pytest.approx(-1000.0)

    def test_stress_tensor_symmetry(self):
        results = verify_electromagnetism()
        sym = [r for r in results if "symmetry" in r.test_name]
        assert len(sym) == 1
        assert sym[0].passed

    def test_stress_tensor_trace(self):
        results = verify_electromagnetism()
        trace = [r for r in results if "trace" in r.test_name.lower()]
        assert len(trace) == 1
        assert trace[0].passed


class TestVerifyVectorCalculus:
    """Test vector calculus verification."""

    def test_returns_results(self):
        results = verify_vector_calculus()
        assert isinstance(results, list)
        assert len(results) >= 2

    def test_curl_grad_zero(self):
        results = verify_vector_calculus()
        curl_grad = [r for r in results if "curl(grad" in r.test_name]
        assert len(curl_grad) == 1
        assert curl_grad[0].passed

    def test_gradient_1_over_r(self):
        results = verify_vector_calculus()
        grad = [r for r in results if r.test_name.startswith("grad(1/r)")]
        assert len(grad) == 1
        assert grad[0].passed
        assert grad[0].expected == pytest.approx(-1.0 / 9.0, rel=1e-3)


class TestVerifyEllipticIntegrals:
    """Test elliptic integral verification."""

    def test_returns_results(self):
        results = verify_elliptic_integrals()
        assert isinstance(results, list)
        assert len(results) >= 4

    def test_K_zero(self):
        results = verify_elliptic_integrals()
        k0 = [r for r in results if "K(0)" in r.test_name]
        assert len(k0) == 1
        assert k0[0].passed
        assert k0[0].expected == pytest.approx(np.pi / 2)

    def test_E_zero(self):
        results = verify_elliptic_integrals()
        e0 = [r for r in results if "E(0)" in r.test_name]
        assert len(e0) == 1
        assert e0[0].passed
        assert e0[0].expected == pytest.approx(np.pi / 2)

    def test_K_half(self):
        results = verify_elliptic_integrals()
        k05 = [r for r in results if "K(0.5)" in r.test_name]
        assert len(k05) == 1
        assert k05[0].passed

    def test_E_half(self):
        results = verify_elliptic_integrals()
        e05 = [r for r in results if "E(0.5)" in r.test_name]
        assert len(e05) == 1
        assert e05[0].passed


class TestVerifyUnitsAndDimensions:
    """Test units and dimensions verification."""

    def test_returns_results(self):
        results = verify_units_and_dimensions()
        assert isinstance(results, list)
        assert len(results) >= 2

    def test_esu_emu_ratio(self):
        results = verify_units_and_dimensions()
        ratio = [r for r in results if "ESU/EMU" in r.test_name]
        assert len(ratio) == 1
        assert ratio[0].passed
        assert ratio[0].expected == 1.0

    def test_speed_of_light(self):
        results = verify_units_and_dimensions()
        c = [r for r in results if "c = 2.9979e10" in r.test_name]
        assert len(c) == 1
        assert c[0].passed
        assert c[0].expected == pytest.approx(2.9979e10, rel=1e-3)


class TestVerifyOpticsAndWaves:
    """Test optics and waves verification."""

    def test_returns_results(self):
        results = verify_optics_and_waves()
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_plane_wave_wavelength(self):
        results = verify_optics_and_waves()
        lam = [r for r in results if "lambda" in r.test_name.lower() or "wavelength" in r.test_name.lower()]
        assert len(lam) == 1
        assert lam[0].passed
        from maxwell.config.constants import C
        assert lam[0].expected == pytest.approx(C / 1e14, rel=1e-6)
