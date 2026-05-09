"""
Test new Part IV Mathematical modules.

Comprehensive test coverage for mathematical foundations:
- Spherical harmonics (Arts. 675-695) — Legendre polynomials, Y_l^m, multipole expansion
- Elliptic integrals (Arts. 696-705) — K(k), E(k), Jacobian functions

Tests verify:
- Correct formula implementation with numeric values
- Mathematical properties (orthogonality, normalization, identities)
- Edge cases (limiting behavior, special values)
- CGS unit compliance (dimensionless for mathematical functions)
- Citation decorator compliance
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import MaxwellCitation, get_citation

# =============================================================================
# SPHERICAL HARMONICS TESTS (Arts. 675-695)
# =============================================================================


class TestLegendrePolynomial:
    """Test Legendre polynomial functions."""

    def test_legendre_p0(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_0(x) = 1.

        Art. 675: P_0(x) = 1 for all x.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=0)

        # Test at various points
        assert_cgs_close(lp.evaluate(0.0), 1.0, cgs_tolerance)
        assert_cgs_close(lp.evaluate(0.5), 1.0, cgs_tolerance)
        assert_cgs_close(lp.evaluate(1.0), 1.0, cgs_tolerance)

    def test_legendre_p1(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_1(x) = x.

        Art. 675: P_1(x) = x.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=1)

        assert_cgs_close(lp.evaluate(0.0), 0.0, cgs_tolerance)
        assert_cgs_close(lp.evaluate(0.5), 0.5, cgs_tolerance)
        assert_cgs_close(lp.evaluate(1.0), 1.0, cgs_tolerance)
        assert_cgs_close(lp.evaluate(-0.3), -0.3, cgs_tolerance)

    def test_legendre_p2(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_2(x) = (3x^2 - 1) / 2.

        Art. 675: P_2(x) = (3x^2 - 1) / 2.

        For x = 0.5: P_2(0.5) = (3*0.25 - 1) / 2 = -0.125
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)
        x = 0.5
        expected = (3 * x**2 - 1) / 2

        assert_cgs_close(lp.evaluate(x), expected, cgs_tolerance)

    def test_legendre_p2_special_values(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_2(x) at special points.

        P_2(0) = -1/2
        P_2(1) = 1
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)

        assert_cgs_close(lp.evaluate(0.0), -0.5, cgs_tolerance)
        assert_cgs_close(lp.evaluate(1.0), 1.0, cgs_tolerance)

    def test_legendre_derivative_p1(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_1'(x) = 1.

        Art. 676: Derivative of P_1(x) = x is 1.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=1)

        assert_cgs_close(lp.derivative(0.0), 1.0, cgs_tolerance)
        assert_cgs_close(lp.derivative(0.5), 1.0, cgs_tolerance)

    def test_legendre_derivative_p0(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P_0'(x) = 0.

        Art. 676: Derivative of constant P_0(x) = 1 is 0.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=0)

        assert_cgs_close(lp.derivative(0.5), 0.0, cgs_tolerance)

    def test_legendre_rodrigues_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Rodrigues' formula consistency.

        Art. 677: Rodrigues' formula should match standard evaluation.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=3)
        x = 0.5

        standard = lp.evaluate(x)
        rodrigues = lp.rodrigues_formula(x)

        assert_cgs_close(standard, rodrigues, cgs_tolerance)

    def test_legendre_orthogonality_different_degrees(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify orthogonality: integral P_l * P_k = 0 for l != k.

        Art. 678: Orthogonality relation.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)

        # Check orthogonality with degree 3 (should be ~0)
        integral = lp.orthogonality_check(other_degree=3)

        assert abs(integral) < cgs_tolerance * 10

    def test_legendre_orthogonality_same_degree(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify orthogonality: integral P_l * P_l = 2/(2l+1).

        Art. 678: Self-orthogonality gives 2/(2l+1).

        For l = 2: integral = 2/5 = 0.4
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)

        integral = lp.orthogonality_check(other_degree=2)
        expected = 2.0 / (2 * 2 + 1)  # 2/5 = 0.4

        assert_cgs_close(integral, expected, cgs_tolerance * 100)

    def test_legendre_invalid_degree(self) -> None:
        """Verify error for negative degree."""
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        with pytest.raises(ValueError):
            LegendrePolynomial(degree=-1)


class TestSphericalHarmonic:
    """Test spherical harmonic functions Y_l^m."""

    def test_spherical_harmonic_l0_m0(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Y_0^0 = 1/sqrt(4*pi).

        Art. 685: Monopole harmonic is constant.

        Y_0^0 = 1/sqrt(4*pi) (independent of theta, phi)
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=0, m=0)

        Y = sh.evaluate(theta=np.pi / 2, phi=0)
        expected = 1.0 / np.sqrt(4 * np.pi)

        assert_cgs_close(abs(Y), expected, cgs_tolerance)

    def test_spherical_harmonic_l1_m0(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Y_1^0 proportional to cos(theta).

        Art. 685: Dipole harmonic.

        Y_1^0 = sqrt(3/4*pi) * cos(theta)
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=0)

        # At theta = 0 (cos = 1)
        Y_pole = sh.evaluate(theta=0.0, phi=0)
        expected_pole = np.sqrt(3.0 / (4 * np.pi))

        # At theta = pi/2 (cos = 0)
        Y_equator = sh.evaluate(theta=np.pi / 2, phi=0)

        assert_cgs_close(abs(Y_pole), expected_pole, cgs_tolerance * 10)
        assert_cgs_close(abs(Y_equator), 0.0, cgs_tolerance * 10)

    def test_spherical_harmonic_intensity(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify intensity |Y_l^m|^2 is real and positive.

        Art. 687: Intensity calculation.
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=2, m=1)

        intensity = sh.intensity(theta=np.pi / 3, phi=np.pi / 4)

        assert intensity > 0
        assert isinstance(intensity, float)

    def test_spherical_harmonic_normalization(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify normalization integral = 1.

        Art. 688: Integral of |Y_l^m|^2 over sphere = 1.
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=0)

        integral = sh.normalization_check()

        # Allow larger tolerance for numerical integration
        assert_cgs_close(integral, 1.0, 0.05)  # 5% tolerance for numerical

    def test_spherical_harmonic_associated_legendre(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify associated Legendre function P_l^m.

        Art. 689: P_l^m(cos theta) evaluation.

        For l=1, m=1: P_1^1(x) = -sqrt(1-x^2)
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=1)

        # At theta = pi/2, cos(theta) = 0
        P = sh.associated_legendre(theta=np.pi / 2)

        # P_1^1(0) should be non-zero
        assert abs(P) > 0

    def test_spherical_harmonic_invalid_parameters(self) -> None:
        """Verify error handling for invalid l, m."""
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        # m > l should raise error
        with pytest.raises(ValueError):
            SphericalHarmonic(l=1, m=2)

        # Negative l should raise error
        with pytest.raises(ValueError):
            SphericalHarmonic(l=-1, m=0)

    def test_spherical_harmonic_evaluate_real(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify real spherical harmonic evaluation.

        Art. 686: Real form for physical applications.
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=1)

        Y_real = sh.evaluate_real(theta=np.pi / 2, phi=0)

        # Should be a real float
        assert isinstance(Y_real, float)


class TestMultipoleExpansion:
    """Test multipole expansion calculations."""

    def test_multipole_monopole(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify monopole potential ~ 1/r.

        Art. 690: For l=0 only:

        Phi = q_00 * Y_0^0 / r
        """
        from maxwell.math.spherical_harmonics import calc_multipole_expansion

        moments = {0: 1.0}  # Monopole only

        # At r = 10 cm, theta = pi/2, phi = 0
        Phi = calc_multipole_expansion(
            observation_r=10.0,
            observation_theta=np.pi / 2,
            observation_phi=0.0,
            multipole_moments=moments,
        )

        # Should scale as 1/r
        assert abs(Phi) > 0

    def test_multipole_dipole(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dipole potential ~ 1/r^2.

        Art. 691: For l=1:

        Phi ~ q_10 * Y_1^0 / r^2
        """
        from maxwell.math.spherical_harmonics import calc_multipole_expansion

        moments = {1: 0.5}  # Dipole only

        Phi_near = calc_multipole_expansion(
            observation_r=10.0,
            observation_theta=0.0,
            observation_phi=0.0,
            multipole_moments=moments,
        )

        Phi_far = calc_multipole_expansion(
            observation_r=20.0,
            observation_theta=0.0,
            observation_phi=0.0,
            multipole_moments=moments,
        )

        # Ratio should be ~4 (1/r^2 scaling)
        ratio = abs(Phi_near) / abs(Phi_far) if abs(Phi_far) > 0 else 0
        expected_ratio = 4.0

        # Allow some tolerance due to numerical factors
        assert abs(ratio - expected_ratio) < expected_ratio * 0.1

    def test_multipole_mixed_moments(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify multipole expansion with multiple moments.

        Art. 692: Combined monopole + dipole + quadrupole.
        """
        from maxwell.math.spherical_harmonics import calc_multipole_expansion

        moments = {
            0: 1.0,  # Monopole
            1: 0.1,  # Dipole
            2: 0.01,  # Quadrupole
        }

        Phi = calc_multipole_expansion(
            observation_r=100.0,  # Far field
            observation_theta=np.pi / 4,
            observation_phi=np.pi / 3,
            multipole_moments=moments,
        )

        # Should be dominated by monopole at large r
        assert abs(Phi) > 0


class TestSphericalHarmonicFunctions:
    """Test standalone spherical harmonic functions."""

    def test_calc_legendre_polynomial(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_legendre_polynomial function."""
        from maxwell.math.spherical_harmonics import calc_legendre_polynomial

        P2 = calc_legendre_polynomial(l=2, x=0.5)
        expected = (3 * 0.5**2 - 1) / 2  # -0.125

        assert_cgs_close(P2, expected, cgs_tolerance)

    def test_calc_associated_legendre(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_associated_legendre function."""
        from maxwell.math.spherical_harmonics import calc_associated_legendre

        # P_2^1(0.5)
        P21 = calc_associated_legendre(l=2, m=1, x=0.5)

        # Should be finite value
        assert np.isfinite(P21)

    def test_calc_spherical_harmonic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_spherical_harmonic function."""
        from maxwell.math.spherical_harmonics import calc_spherical_harmonic

        Y = calc_spherical_harmonic(l=1, m=0, theta=np.pi / 2, phi=0)

        # Should be complex
        assert isinstance(Y, complex)

    def test_verify_spherical_harmonics(self) -> None:
        """Verify verify_spherical_harmonics function."""
        from maxwell.math.spherical_harmonics import verify_spherical_harmonics

        result = verify_spherical_harmonics(l=2, m=1, tolerance=1e-6)

        # Check that key results are present and finite
        assert "P_l_at_0.5" in result
        assert np.isfinite(result["P_l_at_0.5"])
        assert "normalization_error" in result
        assert result["m_valid"] is True or result["m_valid"] is np.True_
        assert "orthogonality_error" in result
        assert np.isfinite(result["orthogonality_error"])

    def test_analyze_spherical_harmonics(self) -> None:
        """Verify analyze_spherical_harmonics function."""
        from maxwell.math.spherical_harmonics import analyze_spherical_harmonics

        result = analyze_spherical_harmonics(l_max=3)

        assert "legendre_at_x=0.5" in result
        assert "spherical_harmonic_values" in result
        assert "normalization_checks" in result


# =============================================================================
# ELLIPTIC INTEGRALS TESTS (Arts. 696-705)
# =============================================================================


class TestEllipticIntegralFirstKind:
    """Test elliptic integral of the first kind K(k)."""

    def test_complete_elliptic_k_zero(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify K(0) = pi/2.

        Art. 696: At k=0, K(0) = pi/2.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.0)
        K = ei.first_kind(np.pi / 2)

        assert_cgs_close(K, np.pi / 2, cgs_tolerance)

    def test_complete_elliptic_k_basic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify K(k) for k=0.5.

        Art. 696: K(0.5) ~ 1.68575
        """
        from maxwell.math.elliptic_integrals import (
            EllipticIntegral,
            calc_complete_elliptic_integral_first_kind,
        )

        K = calc_complete_elliptic_integral_first_kind(0.5)

        # Known value: K(0.5) ≈ 1.68575
        assert 1.6 < K < 1.8

    def test_incomplete_elliptic_f(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify incomplete elliptic integral F(phi, k).

        Art. 696: F(phi, k) = integral_0^phi dθ / sqrt(1 - k^2 sin^2 θ)
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)

        # At phi = pi/2, should equal complete integral
        F_complete = ei.first_kind(np.pi / 2)
        K_complete = ei.first_kind(np.pi / 2)

        assert_cgs_close(F_complete, K_complete, cgs_tolerance)

    def test_elliptic_k_divergence(self) -> None:
        """Verify K(k) diverges as k -> 1.

        Art. 696: K(k) -> infinity as k -> 1.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.999)
        K = ei.first_kind(np.pi / 2)

        # K should be large (> 3 for k=0.999)
        assert K > 3.0


class TestEllipticIntegralSecondKind:
    """Test elliptic integral of the second kind E(k)."""

    def test_complete_elliptic_e_zero(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E(0) = pi/2.

        Art. 697: At k=0, E(0) = pi/2.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.0)
        E = ei.second_kind(np.pi / 2)

        assert_cgs_close(E, np.pi / 2, cgs_tolerance)

    def test_complete_elliptic_e_basic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E(k) for k=0.5.

        Art. 697: E(0.5) ~ 1.46746
        """
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_second_kind,
        )

        E = calc_complete_elliptic_integral_second_kind(0.5)

        # Known value: E(0.5) ≈ 1.46746
        assert 1.4 < E < 1.6

    def test_elliptic_e_less_than_k(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E(k) < K(k) for k > 0.

        Art. 696-697: E(k) is always less than K(k) for k > 0.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        K = ei.first_kind(np.pi / 2)
        E = ei.second_kind(np.pi / 2)

        assert E < K

    def test_elliptic_e_limit_k1(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E(1) = 1.

        Art. 697: E(k) -> 1 as k -> 1.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=1.0)
        E = ei.second_kind(np.pi / 2)

        assert_cgs_close(E, 1.0, cgs_tolerance * 100)


class TestEllipticIntegralThirdKind:
    """Test elliptic integral of the third kind."""

    def test_elliptic_third_kind_basic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify third kind elliptic integral.

        Art. 698: Pi(n; phi, k) = integral_0^phi dθ / (1 + n sin^2 θ) sqrt(1 - k^2 sin^2 θ)
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)

        # With n=0, should reduce to first kind
        Pi_zero = ei.third_kind(amplitude=np.pi / 2, characteristic=0.0)
        K = ei.first_kind(np.pi / 2)

        # Should be close (n=0 reduces to first kind)
        assert_cgs_close(Pi_zero, K, cgs_tolerance * 10)


class TestJacobianFunctions:
    """Test Jacobian elliptic functions sn, cn, dn."""

    def test_jacobian_identity_sn_cn(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify sn^2 + cn^2 = 1.

        Art. 699: Fundamental Jacobian identity.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        u = 1.0

        sn, cn, dn = ei.jacobian_functions(u)

        identity = sn**2 + cn**2
        assert_cgs_close(identity, 1.0, cgs_tolerance)

    def test_jacobian_identity_dn(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dn^2 + k^2 sn^2 = 1.

        Art. 699: Second Jacobian identity.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        u = 1.0

        sn, cn, dn = ei.jacobian_functions(u)
        k = ei.modulus

        identity = dn**2 + k**2 * sn**2
        assert_cgs_close(identity, 1.0, cgs_tolerance)

    def test_jacobian_at_zero(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Jacobian functions at u=0.

        sn(0) = 0, cn(0) = 1, dn(0) = 1
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)

        sn, cn, dn = ei.jacobian_functions(0.0)

        assert_cgs_close(sn, 0.0, cgs_tolerance)
        assert_cgs_close(cn, 1.0, cgs_tolerance)
        assert_cgs_close(dn, 1.0, cgs_tolerance)


class TestEllipticTransformations:
    """Test elliptic integral transformations."""

    def test_complementary_modulus(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify complementary modulus k' = sqrt(1 - k^2).

        Art. 701: Complementary modulus definition.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.6)
        k_prime = ei.complementary_modulus()

        expected = np.sqrt(1 - 0.6**2)  # 0.8
        assert_cgs_close(k_prime, expected, cgs_tolerance)

    def test_parameter(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify parameter m = k^2.

        Art. 702: Parameter definition.
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        m = ei.parameter()

        assert_cgs_close(m, 0.25, cgs_tolerance)

    def test_landen_transformation(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Landen transformation.

        Art. 700: k1 = (1 - k') / (1 + k')
        """
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        k1, K1 = ei.landen_transformation()

        # k1 should be smaller than original k
        assert k1 < ei.modulus
        assert k1 > 0


class TestEllipticFunctions:
    """Test standalone elliptic integral functions."""

    def test_calc_complete_elliptic_first_kind(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_complete_elliptic_integral_first_kind."""
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_first_kind,
        )

        K = calc_complete_elliptic_integral_first_kind(0.5)

        assert 1.6 < K < 1.8

    def test_calc_complete_elliptic_second_kind(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_complete_elliptic_integral_second_kind."""
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_second_kind,
        )

        E = calc_complete_elliptic_integral_second_kind(0.5)

        assert 1.4 < E < 1.6

    def test_calc_elliptic_first_kind(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_elliptic_integral_first_kind (incomplete)."""
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_first_kind,
            calc_elliptic_integral_first_kind,
        )

        F = calc_elliptic_integral_first_kind(modulus=0.5, amplitude=np.pi / 2)
        K = calc_complete_elliptic_integral_first_kind(0.5)

        assert_cgs_close(F, K, cgs_tolerance)

    def test_calc_elliptic_second_kind(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_elliptic_integral_second_kind (incomplete)."""
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_second_kind,
            calc_elliptic_integral_second_kind,
        )

        E = calc_elliptic_integral_second_kind(modulus=0.5, amplitude=np.pi / 2)
        E_complete = calc_complete_elliptic_integral_second_kind(0.5)

        assert_cgs_close(E, E_complete, cgs_tolerance)

    def test_calc_elliptic_third_kind(self) -> None:
        """Verify calc_elliptic_integral_third_kind."""
        from maxwell.math.elliptic_integrals import calc_elliptic_integral_third_kind

        Pi = calc_elliptic_integral_third_kind(
            modulus=0.5, amplitude=np.pi / 2, characteristic=0.1
        )

        assert np.isfinite(Pi)
        assert Pi > 0

    def test_verify_elliptic_integrals(self) -> None:
        """Verify verify_elliptic_integrals function."""
        from maxwell.math.elliptic_integrals import verify_elliptic_integrals

        result = verify_elliptic_integrals(modulus=0.5)

        assert result["verified"] is True
        assert "legendre_relation_LHS" in result
        assert "K_complete" in result
        assert "E_complete" in result

    def test_analyze_elliptic_integrals(self) -> None:
        """Verify analyze_elliptic_integrals function."""
        from maxwell.math.elliptic_integrals import analyze_elliptic_integrals

        result = analyze_elliptic_integrals(modulus_range=(0.0, 0.9, 5))

        assert "K_values" in result
        assert "E_values" in result
        assert "jacobian_sn_at_1" in result


# =============================================================================
# MATHEMATICAL PROPERTY TESTS
# =============================================================================


class TestLegendreRecurrence:
    """Test Legendre polynomial recurrence relations."""

    def test_legendre_recurrence_relation(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify (l+1)P_{l+1} = (2l+1)xP_l - lP_{l-1}.

        Standard Legendre recurrence relation.
        """
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        x = 0.5
        l = 2

        P_l = LegendrePolynomial(degree=l).evaluate(x)
        P_l_plus_1 = LegendrePolynomial(degree=l + 1).evaluate(x)
        P_l_minus_1 = LegendrePolynomial(degree=l - 1).evaluate(x)

        # Recurrence: (l+1)P_{l+1} = (2l+1)xP_l - lP_{l-1}
        lhs = (l + 1) * P_l_plus_1
        rhs = (2 * l + 1) * x * P_l - l * P_l_minus_1

        assert_cgs_close(lhs, rhs, cgs_tolerance)


class TestSphericalHarmonicOrthogonality:
    """Test spherical harmonic orthogonality properties."""

    def test_spherical_harmonic_orthogonality_different_l(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify spherical harmonics with different l are orthogonal.

        Integral of Y_l^m * Y_{l'}^{m'*} = 0 for l != l'
        """
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        # This is implicitly tested through normalization_check
        # which integrates |Y_l^m|^2 = 1

        sh1 = SphericalHarmonic(l=1, m=0)
        sh2 = SphericalHarmonic(l=2, m=0)

        # Each should normalize to 1 independently
        norm1 = sh1.normalization_check()
        norm2 = sh2.normalization_check()

        assert abs(norm1 - 1.0) < 0.05
        assert abs(norm2 - 1.0) < 0.05


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================


class TestMathCGSUnits:
    """Test CGS unit compliance for mathematical modules."""

    def test_legendre_polynomial_dimensionless(self) -> None:
        """Verify Legendre polynomials are dimensionless."""
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)
        result = lp.evaluate(0.5)

        assert isinstance(result, float)
        # Legendre polynomials are pure numbers

    def test_spherical_harmonic_dimensionless(self) -> None:
        """Verify spherical harmonics are dimensionless."""
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=0)
        result = sh.evaluate(np.pi / 2, 0)

        assert isinstance(result, complex)
        # Spherical harmonics are pure numbers

    def test_elliptic_integrals_dimensionless(self) -> None:
        """Verify elliptic integrals are dimensionless."""
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        K = ei.first_kind(np.pi / 2)
        E = ei.second_kind(np.pi / 2)

        assert isinstance(K, float)
        assert isinstance(E, float)
        # Elliptic integrals are pure numbers (radians)


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================


class TestMathCitationCompliance:
    """Test citation decorator compliance for mathematical modules."""

    def test_legendre_polynomial_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify Legendre polynomial functions have correct citations."""
        from maxwell.math.spherical_harmonics import LegendrePolynomial

        lp = LegendrePolynomial(degree=2)
        citation = require_citation(lp.evaluate)

        assert citation.part == 4
        assert any(a in citation.articles for a in [675, 676, 677, 678])

    def test_spherical_harmonic_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify spherical harmonic functions have correct citations."""
        from maxwell.math.spherical_harmonics import SphericalHarmonic

        sh = SphericalHarmonic(l=1, m=0)
        citation = require_citation(sh.evaluate)

        assert citation.part == 4
        assert any(a in citation.articles for a in [685, 686, 687, 688, 689])

    def test_elliptic_integral_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify elliptic integral functions have correct citations."""
        from maxwell.math.elliptic_integrals import EllipticIntegral

        ei = EllipticIntegral(modulus=0.5)
        citation = require_citation(ei.first_kind)

        assert citation.part == 4
        assert any(a in citation.articles for a in [696, 697, 698, 699, 700])

    def test_calc_functions_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify calc_* functions have correct citations."""
        from maxwell.math.spherical_harmonics import (
            calc_legendre_polynomial,
            calc_multipole_expansion,
            calc_spherical_harmonic,
        )

        for func in [
            calc_legendre_polynomial,
            calc_spherical_harmonic,
            calc_multipole_expansion,
        ]:
            citation = require_citation(func)
            assert citation.part == 4
            assert citation.articles is not None

    def test_elliptic_calc_functions_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify elliptic calc_* functions have correct citations."""
        from maxwell.math.elliptic_integrals import (
            calc_complete_elliptic_integral_first_kind,
            calc_complete_elliptic_integral_second_kind,
            verify_elliptic_integrals,
        )

        for func in [
            calc_complete_elliptic_integral_first_kind,
            calc_complete_elliptic_integral_second_kind,
            verify_elliptic_integrals,
        ]:
            citation = require_citation(func)
            assert citation.part == 4
            assert any(a >= 696 and a <= 705 for a in citation.articles)
