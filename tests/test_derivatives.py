"""Tests for maxwell.math.derivatives.

Comprehensive test suite covering:
- Category A: Analytical verification against known derivatives
- Category B: Higher-order derivatives and Hessian
- Category C: Time derivatives
- Category D: Total/material derivative
- Category E: Jacobian and coordinate transforms
- Category F: Schwarz's theorem verification
- Category G: Vector identities via Schwarz
- Category H: Validation engine
- Category I: DerivativeCalculator class
- Category J: Edge cases

Quality Review:
- All tests use CGS units (cm, s, statvolt, etc.)
- Numerical tolerances account for finite-difference errors
- Analytical solutions verified independently
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.math.derivatives import (
    DT_DEFAULT,
    H_DEFAULT,
    H_MIXED,
    DerivativeCalculator,
    DerivativeResult,
    DiffMethod,
    ValidationReport,
    cartesian_to_cylindrical,
    cartesian_to_spherical,
    cylindrical_to_cartesian,
    find_optimal_step,
    hessian,
    jacobian,
    jacobian_determinant,
    mixed_partial_derivative,
    partial_derivative,
    partial_derivative_t,
    partial_derivative_t_vector,
    partial_gradient,
    second_partial_derivative,
    spherical_to_cartesian,
    total_derivative,
    total_derivative_vector,
    validate_derivative,
    verify_curl_grad_via_schwarz,
    verify_div_curl_via_schwarz,
    verify_schwarz_theorem,
)

# ═══════════════════════════════════════════════════════════════════
# Category A: Analytical Verification
# ═══════════════════════════════════════════════════════════════════


class TestPartialDerivative:
    """Category A: Analytical partial derivative tests."""

    def test_linear_function(self):
        """df/dx of f = ax + by + cz should be a."""

        def f(x, y, z):
            return 3.0 * x + 5.0 * y + 7.0 * z

        result = partial_derivative(f, (1.0, 2.0, 3.0), "x")
        assert result.value == pytest.approx(3.0, abs=1e-8)

    def test_quadratic_function(self):
        """df/dx of f = x^2 should be 2x."""

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = partial_derivative(f, (2.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(4.0, abs=1e-5)

    def test_cubic_function(self):
        """df/dx of f = x^3 should be 3x^2."""

        def f(x, y, z):
            return x**3

        result = partial_derivative(f, (2.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(12.0, abs=1e-5)

    def test_exponential(self):
        """df/dx of f = e^x should be e^x."""

        def f(x, y, z):
            return np.exp(x)

        result = partial_derivative(f, (1.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(np.exp(1.0), rel=1e-6)

    def test_sin_derivative(self):
        """df/dx of f = sin(x) should be cos(x)."""

        def f(x, y, z):
            return np.sin(x)

        result = partial_derivative(f, (0.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(1.0, abs=1e-6)

    def test_partial_y(self):
        """df/dy of f = x^2*y + z should be x^2."""

        def f(x, y, z):
            return x**2 * y + z

        result = partial_derivative(f, (3.0, 1.0, 0.0), "y")
        assert result.value == pytest.approx(9.0, abs=1e-5)

    def test_partial_z(self):
        """df/dz of f = x*y*z should be x*y."""

        def f(x, y, z):
            return x * y * z

        result = partial_derivative(f, (2.0, 3.0, 1.0), "z")
        assert result.value == pytest.approx(6.0, abs=1e-5)

    def test_forward_difference(self):
        """Forward difference should work with O(h) accuracy."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (2.0, 0.0, 0.0), "x", method=DiffMethod.FORWARD)
        assert result.value == pytest.approx(4.0, abs=1e-4)
        assert result.order == 1

    def test_backward_difference(self):
        """Backward difference should work with O(h) accuracy."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (2.0, 0.0, 0.0), "x", method=DiffMethod.BACKWARD)
        assert result.value == pytest.approx(4.0, abs=1e-4)
        assert result.order == 1

    def test_five_point_stencil(self):
        """Five-point stencil should give O(h^4) accuracy."""

        def f(x, y, z):
            return np.sin(x)

        result = partial_derivative(
            f, (1.0, 0.0, 0.0), "x", method=DiffMethod.FIVE_POINT
        )
        assert result.value == pytest.approx(np.cos(1.0), rel=1e-10)
        assert result.order == 4

    def test_invalid_variable(self):
        """Should raise ValueError for invalid variable name."""

        def f(x, y, z):
            return x

        with pytest.raises(ValueError):
            partial_derivative(f, (0, 0, 0), "w")

    def test_result_metadata(self):
        """DerivativeResult should contain correct metadata."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (1.0, 0.0, 0.0), "x")
        assert isinstance(result, DerivativeResult)
        assert result.method == DiffMethod.CENTRAL
        assert result.step_size == H_DEFAULT
        assert result.order == 2
        assert result.point == (1.0, 0.0, 0.0)
        assert result.variable == "x"
        assert result.order_derivative == 1


class TestGradient:
    """Gradient (all partial derivatives) tests."""

    def test_quadratic_gradient(self):
        """grad(x^2 + y^2 + z^2) = (2x, 2y, 2z)."""

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = partial_gradient(f, (1.0, 2.0, 3.0))
        expected = np.array([2.0, 4.0, 6.0])
        np.testing.assert_allclose(result.value, expected, atol=1e-5)

    def test_zero_gradient_at_origin(self):
        """grad(x^2 + y^2 + z^2) at origin should be (0,0,0)."""

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = partial_gradient(f, (0.0, 0.0, 0.0))
        np.testing.assert_allclose(result.value, [0, 0, 0], atol=1e-6)

    def test_constant_gradient(self):
        """grad(3x + 5y + 7z) = (3, 5, 7)."""

        def f(x, y, z):
            return 3.0 * x + 5.0 * y + 7.0 * z

        result = partial_gradient(f, (0.0, 0.0, 0.0))
        np.testing.assert_allclose(result.value, [3.0, 5.0, 7.0], atol=1e-8)


# ═══════════════════════════════════════════════════════════════════
# Category B: Higher-Order Derivatives
# ═══════════════════════════════════════════════════════════════════


class TestSecondPartialDerivative:
    """Second partial derivative tests."""

    def test_quadratic_second_deriv(self):
        """d^2/dx^2(x^2) = 2."""

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = second_partial_derivative(f, (1.0, 2.0, 3.0), "x", h=1e-4)
        assert result.value == pytest.approx(2.0, abs=1e-6)

    def test_cubic_second_deriv(self):
        """d^2/dx^2(x^3) = 6x."""

        def f(x, y, z):
            return x**3

        result = second_partial_derivative(f, (2.0, 0.0, 0.0), "x", h=1e-4)
        assert result.value == pytest.approx(12.0, abs=1e-5)

    def test_sin_second_deriv(self):
        """d^2/dx^2(sin(x)) = -sin(x)."""

        def f(x, y, z):
            return np.sin(x)

        result = second_partial_derivative(f, (np.pi / 2, 0.0, 0.0), "x")
        assert result.value == pytest.approx(-1.0, abs=1e-4)

    def test_zero_second_deriv(self):
        """d^2/dx^2(3x + 5) = 0."""

        def f(x, y, z):
            return 3.0 * x + 5.0

        result = second_partial_derivative(f, (0.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(0.0, abs=1e-6)


class TestMixedPartialDerivative:
    """Mixed partial derivative tests."""

    def test_xy_mixed(self):
        """d^2/dxdy(x^2*y) = 2x."""

        def f(x, y, z):
            return x**2 * y + y**2 * z

        result = mixed_partial_derivative(f, (1.0, 2.0, 3.0), "x", "y")
        assert result.value == pytest.approx(2.0, abs=1e-4)

    def test_yz_mixed(self):
        """d^2/dydz(x + y*z) = 1."""

        def f(x, y, z):
            return x + y * z

        result = mixed_partial_derivative(f, (0.0, 0.0, 0.0), "y", "z")
        assert result.value == pytest.approx(1.0, abs=1e-6)

    def test_xyz_mixed(self):
        """d^2/dxdz(x*y*z) = y."""

        def f(x, y, z):
            return x * y * z

        result = mixed_partial_derivative(f, (1.0, 2.0, 3.0), "x", "z")
        assert result.value == pytest.approx(2.0, abs=1e-4)

    def test_zero_mixed(self):
        """d^2/dxdy(x^2 + y^2) = 0."""

        def f(x, y, z):
            return x**2 + y**2

        result = mixed_partial_derivative(f, (0.0, 0.0, 0.0), "x", "y")
        assert result.value == pytest.approx(0.0, abs=1e-6)


class TestHessian:
    """Hessian matrix tests."""

    def test_quadratic_hessian(self):
        """Hessian of x^2 + 2*y^2 + 3*z^2 = diag(2, 4, 6)."""

        def f(x, y, z):
            return x**2 + 2.0 * y**2 + 3.0 * z**2

        H = hessian(f, (0.0, 0.0, 0.0))
        expected = np.diag([2.0, 4.0, 6.0])
        np.testing.assert_allclose(H, expected, atol=1e-3)

    def test_cross_term_hessian(self):
        """Hessian of x*y + y*z + z*x has off-diagonal 1s."""

        def f(x, y, z):
            return x * y + y * z + z * x

        H = hessian(f, (0.0, 0.0, 0.0))
        expected = np.array(
            [
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 0],
            ],
            dtype=float,
        )
        np.testing.assert_allclose(H, expected, atol=1e-3)

    def test_symmetric_hessian(self):
        """Hessian should be symmetric (Schwarz's theorem)."""

        def f(x, y, z):
            return x**2 * y + y**2 * z + z**2 * x

        H = hessian(f, (1.0, 2.0, 3.0))
        np.testing.assert_allclose(H, H.T, atol=1e-3)


# ═══════════════════════════════════════════════════════════════════
# Category C: Time Derivatives
# ═══════════════════════════════════════════════════════════════════


class TestTimeDerivative:
    """Time partial derivative tests."""

    def test_oscillating_field(self):
        """d/dt(E0*sin(omega*t)) at t=0 = E0*omega."""
        omega = 2.0 * np.pi * 60.0  # 60 Hz
        E0 = 100.0  # statvolt/cm

        def E(x, y, z, t):
            return E0 * np.sin(omega * t)

        result = partial_derivative_t(E, (0.0, 0.0, 0.0, 0.0), dt=1e-8)
        assert result.value == pytest.approx(E0 * omega, rel=1e-5)

    def test_linear_time(self):
        """d/dt(a*t + b) = a."""

        def f(x, y, z, t):
            return 5.0 * t + 3.0

        result = partial_derivative_t(f, (0, 0, 0, 0))
        assert result.value == pytest.approx(5.0, abs=1e-5)

    def test_quadratic_time(self):
        """d/dt(a*t^2) = 2*a*t."""

        def f(x, y, z, t):
            return 3.0 * t**2

        result = partial_derivative_t(f, (0, 0, 0, 1.0))
        assert result.value == pytest.approx(6.0, abs=1e-5)

    def test_exponential_time(self):
        """d/dt(e^(kt)) = k*e^(kt)."""
        k = 2.0

        def f(x, y, z, t):
            return np.exp(k * t)

        result = partial_derivative_t(f, (0, 0, 0, 0.5))
        expected = k * np.exp(k * 0.5)
        assert result.value == pytest.approx(expected, rel=1e-6)


class TestTimeDerivativeVector:
    """Vector time derivative tests."""

    def test_rotating_field(self):
        """d/dt(cos(t), sin(t), 0) at t=0 = (0, 1, 0)."""

        def Bx(x, y, z, t):
            return np.cos(t)

        def By(x, y, z, t):
            return np.sin(t)

        def Bz(x, y, z, t):
            return 0.0

        result = partial_derivative_t_vector(Bx, By, Bz, (0, 0, 0, 0))
        np.testing.assert_allclose(result, [0.0, 1.0, 0.0], atol=1e-6)


# ═══════════════════════════════════════════════════════════════════
# Category D: Total/Material Derivative
# ═══════════════════════════════════════════════════════════════════


class TestTotalDerivative:
    """Total (material) derivative tests."""

    def test_spatial_only(self):
        """For f = x*t: d/dt = t + v_x. At (1,0,0,1) v=(1,0,0): 1+1=2."""

        def f(x, y, z, t):
            return x * t

        result = total_derivative(f, (1.0, 0.0, 0.0, 1.0), velocity=(1.0, 0.0, 0.0))
        assert result.value == pytest.approx(2.0, abs=1e-5)

    def test_time_only(self):
        """For f = t^2 with v=0: d/dt = 2t."""

        def f(x, y, z, t):
            return t**2

        result = total_derivative(f, (0, 0, 0, 3.0), velocity=(0, 0, 0))
        assert result.value == pytest.approx(6.0, abs=1e-5)

    def test_stationary_observer(self):
        """Total derivative with v=0 should equal partial_t."""
        omega = 10.0

        def f(x, y, z, t):
            return np.sin(omega * t)

        result = total_derivative(f, (0, 0, 0, 0.5), velocity=(0, 0, 0))
        expected = omega * np.cos(omega * 0.5)
        assert result.value == pytest.approx(expected, rel=1e-5)

    def test_3d_velocity(self):
        """Total derivative with velocity in all directions."""

        def f(x, y, z, t):
            return x + 2 * y + 3 * z + 4 * t

        result = total_derivative(f, (0, 0, 0, 0), velocity=(1, 1, 1))
        # d/dt = 4 + 1*1 + 1*2 + 1*3 = 10
        assert result.value == pytest.approx(10.0, abs=1e-5)


class TestTotalDerivativeVector:
    """Vector total derivative tests."""

    def test_vector_total_deriv(self):
        """Total derivative of vector field F = (x*t, y*t, z*t)."""

        def Fx(x, y, z, t):
            return x * t

        def Fy(x, y, z, t):
            return y * t

        def Fz(x, y, z, t):
            return z * t

        result = total_derivative_vector(
            Fx, Fy, Fz, (1.0, 2.0, 3.0, 1.0), velocity=(1.0, 1.0, 1.0)
        )
        # dFx/dt = t + vx*t_coeff = 1 + 1 = 2
        # dFy/dt = y/t_coeff*t + vy*t_coeff = y + vy*t... no:
        # dFy/dt = partial_t(y*t) + vy*partial_y(y*t) = y + vy*t
        #   Wait: partial_t(y*t) = y = 2, vy*partial_y(y*t) = 1*t = 1, so = 3
        # Actually: partial_t(y*t) = y (treating y as const in partial_t) = 2
        # vy * dFy/dy = vy * t = 1 * 1 = 1
        # Total: 2 + 1 = 3
        # dFz/dt = partial_t(z*t) + vz*dFz/dz = z + vz*t = 3 + 1 = 4
        np.testing.assert_allclose(result, [2.0, 3.0, 4.0], atol=1e-4)


# ═══════════════════════════════════════════════════════════════════
# Category E: Jacobian and Coordinate Transforms
# ═══════════════════════════════════════════════════════════════════


class TestJacobian:
    """Jacobian matrix tests."""

    def test_identity_transform(self):
        """Jacobian of identity transform should be I."""

        def identity(x):
            return x.copy()

        J = jacobian(identity, np.array([1.0, 2.0, 3.0]))
        np.testing.assert_allclose(J, np.eye(3), atol=1e-5)

    def test_scaling_transform(self):
        """Jacobian of T(x,y,z) = (2x, 3y, 4z) = diag(2,3,4)."""

        def scale(x):
            return np.array([2 * x[0], 3 * x[1], 4 * x[2]])

        J = jacobian(scale, np.array([1.0, 2.0, 3.0]))
        np.testing.assert_allclose(J, np.diag([2.0, 3.0, 4.0]), atol=1e-5)

    def test_spherical_jacobian_determinant(self):
        """det(d(x,y,z)/d(r,theta,phi)) = r^2*sin(theta)."""
        point = np.array([2.0, np.pi / 4, np.pi / 3])
        det = jacobian_determinant(spherical_to_cartesian, point)
        expected = point[0] ** 2 * np.sin(point[1])
        assert det == pytest.approx(expected, rel=1e-4)

    def test_cartesian_to_spherical_determinant(self):
        """det(d(r,theta,phi)/d(x,y,z)) = 1/(r^2*sin(theta))."""
        point = np.array([1.0, 1.0, 1.0])
        sph = cartesian_to_spherical(point)
        r = sph[0]
        theta = sph[1]
        det = jacobian_determinant(cartesian_to_spherical, point)
        expected = 1.0 / (r**2 * np.sin(theta))
        assert det == pytest.approx(expected, rel=1e-4)

    def test_inverse_jacobian_property(self):
        """J_forward @ J_inverse = I."""
        cart = np.array([1.0, 1.0, 1.0])
        sph = cartesian_to_spherical(cart)
        J_fwd = jacobian(cartesian_to_spherical, cart)
        J_inv = jacobian(spherical_to_cartesian, sph)
        product = J_fwd @ J_inv
        np.testing.assert_allclose(product, np.eye(3), atol=1e-4)

    def test_cylindrical_jacobian_determinant(self):
        """det(d(x,y,z)/d(rho,phi,z)) = rho."""
        point = np.array([3.0, np.pi / 4, 5.0])
        det = jacobian_determinant(cylindrical_to_cartesian, point)
        assert det == pytest.approx(point[0], rel=1e-4)


class TestCoordinateTransforms:
    """Coordinate transform round-trip tests."""

    def test_spherical_roundtrip(self):
        """Cartesian -> spherical -> Cartesian should return original."""
        cart = np.array([1.0, 2.0, 3.0])
        sph = cartesian_to_spherical(cart)
        cart_back = spherical_to_cartesian(sph)
        np.testing.assert_allclose(cart_back, cart, atol=1e-10)

    def test_cylindrical_roundtrip(self):
        """Cartesian -> cylindrical -> Cartesian should return original."""
        cart = np.array([1.0, 2.0, 3.0])
        cyl = cartesian_to_cylindrical(cart)
        cart_back = cylindrical_to_cartesian(cyl)
        np.testing.assert_allclose(cart_back, cart, atol=1e-10)

    def test_origin_handling(self):
        """Spherical coordinates at origin should be (0,0,0)."""
        result = cartesian_to_spherical(np.array([0.0, 0.0, 0.0]))
        np.testing.assert_allclose(result, [0.0, 0.0, 0.0], atol=1e-10)

    def test_spherical_on_z_axis(self):
        """Point on z-axis: theta=0."""
        result = cartesian_to_spherical(np.array([0.0, 0.0, 5.0]))
        assert result[0] == pytest.approx(5.0)
        assert result[1] == pytest.approx(0.0, abs=1e-10)


# ═══════════════════════════════════════════════════════════════════
# Category F: Schwarz's Theorem
# ═══════════════════════════════════════════════════════════════════


class TestSchwarzTheorem:
    """Schwarz's theorem (equality of mixed partials) tests."""

    def test_polynomial(self):
        """d^2/dxdy(x^2*y + y^2*z) = d^2/dydx(x^2*y + y^2*z)."""

        def f(x, y, z):
            return x**2 * y + y**2 * z

        result = verify_schwarz_theorem(f, (1.0, 2.0, 3.0), "x", "y")
        assert result["verified"] is True
        assert result["difference"] < 1e-6

    def test_trigonometric(self):
        """d^2/dxdy(sin(x)*cos(y)) = d^2/dydx(sin(x)*cos(y))."""

        def f(x, y, z):
            return np.sin(x) * np.cos(y)

        result = verify_schwarz_theorem(f, (1.0, 1.0, 0.0), "x", "y")
        assert result["verified"] is True
        assert result["difference"] < 1e-6

    def test_exponential(self):
        """d^2/dxdz(e^(x+z)) = d^2/dzdx(e^(x+z))."""

        def f(x, y, z):
            return np.exp(x + z)

        result = verify_schwarz_theorem(f, (1.0, 0.0, 1.0), "x", "z")
        assert result["verified"] is True

    def test_same_variable(self):
        """When var1=var2, both should be second partial derivative."""

        def f(x, y, z):
            return x**3

        result = verify_schwarz_theorem(f, (2.0, 0.0, 0.0), "x", "x")
        assert result["verified"] is True


# ═══════════════════════════════════════════════════════════════════
# Category G: Vector Identities via Schwarz
# ═══════════════════════════════════════════════════════════════════


class TestVectorIdentities:
    """Vector identity verification via Schwarz's theorem."""

    def test_curl_grad_zero(self):
        """curl(grad phi) = 0 for phi = x^3 + y^2*z + x*z^2."""

        def phi(x, y, z):
            return x**3 + y**2 * z + x * z**2

        result = verify_curl_grad_via_schwarz(phi, (1.0, 2.0, 3.0))
        assert result["all_verified"] is True
        assert result["max_difference"] < 1e-6

    def test_curl_grad_zero_simple(self):
        """curl(grad(x^2 + y^2 + z^2)) = 0."""

        def phi(x, y, z):
            return x**2 + y**2 + z**2

        result = verify_curl_grad_via_schwarz(phi, (1.0, 1.0, 1.0))
        assert result["all_verified"] is True

    def test_div_curl_zero(self):
        """div(curl F) = 0 for F = (yz, xz, xy)."""

        def Fx(x, y, z):
            return y * z

        def Fy(x, y, z):
            return x * z

        def Fz(x, y, z):
            return x * y

        result = verify_div_curl_via_schwarz(Fx, Fy, Fz, (1.0, 2.0, 3.0))
        assert result["verified"] is True
        assert abs(result["div_curl"]) < 1e-6

    def test_div_curl_zero_polynomial(self):
        """div(curl F) = 0 for F = (x^2*y, y^2*z, z^2*x)."""

        def Fx(x, y, z):
            return x**2 * y

        def Fy(x, y, z):
            return y**2 * z

        def Fz(x, y, z):
            return z**2 * x

        result = verify_div_curl_via_schwarz(Fx, Fy, Fz, (1.0, 1.0, 1.0))
        assert result["verified"] is True


# ═══════════════════════════════════════════════════════════════════
# Category H: Validation Engine
# ═══════════════════════════════════════════════════════════════════


class TestValidation:
    """Derivative validation engine tests."""

    def test_validate_quadratic(self):
        """Validate d/dx(x^2) = 2x."""

        def f(x, y, z):
            return x**2

        def dfdx(x, y, z):
            return 2.0 * x

        report = validate_derivative(f, dfdx, (3.0, 0.0, 0.0), "x")
        assert report.passed is True
        assert report.numerical == pytest.approx(6.0, abs=1e-5)
        assert report.analytical == 6.0
        assert report.absolute_error < 1e-4

    def test_validate_cubic(self):
        """Validate d/dx(x^3) = 3x^2."""

        def f(x, y, z):
            return x**3

        def dfdx(x, y, z):
            return 3.0 * x**2

        report = validate_derivative(f, dfdx, (2.0, 0.0, 0.0), "x")
        assert report.passed is True
        assert report.relative_error < 1e-5

    def test_validate_report_fields(self):
        """ValidationReport should have all required fields."""

        def f(x, y, z):
            return x

        def dfdx(x, y, z):
            return 1.0

        report = validate_derivative(f, dfdx, (0, 0, 0), "x")
        assert isinstance(report, ValidationReport)
        assert hasattr(report, "numerical")
        assert hasattr(report, "analytical")
        assert hasattr(report, "absolute_error")
        assert hasattr(report, "relative_error")
        assert hasattr(report, "passed")
        assert hasattr(report, "method")
        assert hasattr(report, "step_size")

    def test_find_optimal_step(self):
        """Should find a reasonable step size."""

        def f(x, y, z):
            return np.sin(x)

        def dfdx(x, y, z):
            return np.cos(x)

        result = find_optimal_step(f, dfdx, (1.0, 0.0, 0.0), "x")
        assert "optimal_h" in result
        assert "min_relative_error" in result
        assert "errors" in result
        assert "recommended_h" in result
        assert result["optimal_h"] > 0
        assert result["min_relative_error"] >= 0

    def test_find_optimal_step_range(self):
        """Optimal h should be within the search range."""

        def f(x, y, z):
            return x**2

        def dfdx(x, y, z):
            return 2.0 * x

        result = find_optimal_step(f, dfdx, (1.0, 0.0, 0.0), "x", h_range=(1e-10, 1e-2))
        assert 1e-10 <= result["optimal_h"] <= 1e-2


# ═══════════════════════════════════════════════════════════════════
# Category I: DerivativeCalculator Class
# ═══════════════════════════════════════════════════════════════════


class TestDerivativeCalculator:
    """DerivativeCalculator class tests."""

    def test_partial_via_calculator(self):
        """Calculator partial should match standalone function."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2 + y**2

        result = calc.partial(f, (2.0, 0.0, 0.0), "x")
        assert result.value == pytest.approx(4.0, abs=1e-5)

    def test_gradient_via_calculator(self):
        """Calculator gradient should work."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = calc.gradient(f, (1.0, 2.0, 3.0))
        np.testing.assert_allclose(result.value, [2, 4, 6], atol=1e-5)

    def test_second_partial_via_calculator(self):
        """Calculator second partial should work."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**3

        result = calc.second_partial(f, (2.0, 0.0, 0.0), "x", h=1e-4)
        assert result.value == pytest.approx(12.0, abs=1e-5)

    def test_hessian_via_calculator(self):
        """Calculator hessian should work."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2 + 2 * y**2 + 3 * z**2

        H = calc.hessian(f, (0, 0, 0))
        np.testing.assert_allclose(H, np.diag([2, 4, 6]), atol=1e-3)

    def test_partial_t_via_calculator(self):
        """Calculator time derivative should work."""
        calc = DerivativeCalculator()

        def f(x, y, z, t):
            return 5.0 * t + 3.0

        result = calc.partial_t(f, (0, 0, 0, 0))
        assert result.value == pytest.approx(5.0, abs=1e-5)

    def test_total_via_calculator(self):
        """Calculator total derivative should work."""
        calc = DerivativeCalculator()

        def f(x, y, z, t):
            return x * t

        result = calc.total(f, (1, 0, 0, 1), velocity=(1, 0, 0))
        assert result.value == pytest.approx(2.0, abs=1e-4)

    def test_jacobian_via_calculator(self):
        """Calculator jacobian should work."""
        calc = DerivativeCalculator()
        J = calc.jacobian(spherical_to_cartesian, np.array([2.0, np.pi / 4, np.pi / 3]))
        assert J.shape == (3, 3)

    def test_jacobian_det_via_calculator(self):
        """Calculator jacobian determinant should work."""
        calc = DerivativeCalculator()
        det = calc.jacobian_det(
            spherical_to_cartesian, np.array([2.0, np.pi / 4, np.pi / 3])
        )
        expected = 4.0 * np.sin(np.pi / 4)
        assert det == pytest.approx(expected, rel=1e-3)

    def test_schwarz_via_calculator(self):
        """Calculator Schwarz verification should work."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2 * y

        result = calc.verify_schwarz(f, (1, 2, 3), "x", "y")
        assert result["verified"] is True

    def test_validate_via_calculator(self):
        """Calculator validation should work."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2

        def dfdx(x, y, z):
            return 2.0 * x

        report = calc.validate(f, dfdx, (3, 0, 0), "x")
        assert report.passed is True

    def test_history_tracking(self):
        """Calculator should track computation history."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2

        calc.partial(f, (1, 0, 0), "x")
        calc.partial(f, (2, 0, 0), "x")
        assert len(calc.get_history()) == 2

    def test_clear_history(self):
        """Calculator should support clearing history."""
        calc = DerivativeCalculator()

        def f(x, y, z):
            return x**2

        calc.partial(f, (1, 0, 0), "x")
        calc.clear_history()
        assert len(calc.get_history()) == 0

    def test_custom_step_size(self):
        """Calculator should accept custom step sizes."""
        calc = DerivativeCalculator(h=1e-4, dt=1e-5)

        def f(x, y, z):
            return x**2

        result = calc.partial(f, (2, 0, 0), "x")
        assert result.value == pytest.approx(4.0, abs=1e-3)

    def test_custom_method(self):
        """Calculator should support custom method."""
        calc = DerivativeCalculator(method=DiffMethod.FIVE_POINT)

        def f(x, y, z):
            return np.sin(x)

        result = calc.partial(f, (1, 0, 0), "x")
        assert result.value == pytest.approx(np.cos(1.0), rel=1e-9)


# ═══════════════════════════════════════════════════════════════════
# Category J: Edge Cases
# ═══════════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Edge case and robustness tests."""

    def test_constant_function(self):
        """All derivatives of a constant should be zero."""

        def f(x, y, z):
            return 42.0

        r = partial_derivative(f, (0, 0, 0), "x")
        assert abs(r.value) < 1e-8
        r2 = second_partial_derivative(f, (0, 0, 0), "x")
        assert abs(r2.value) < 1e-8
        mixed = mixed_partial_derivative(f, (0, 0, 0), "x", "y")
        assert abs(mixed.value) < 1e-8

    def test_zero_point(self):
        """Derivatives at origin should work for smooth functions."""

        def f(x, y, z):
            return x**2 + y**2 + z**2

        result = partial_gradient(f, (0.0, 0.0, 0.0))
        np.testing.assert_allclose(result.value, [0, 0, 0], atol=1e-8)

    def test_large_coordinates(self):
        """Derivatives at large coordinates should work."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (1e6, 0, 0), "x")
        assert result.value == pytest.approx(2e6, rel=1e-4)

    def test_small_step_size(self):
        """Very small step sizes should not crash (may lose precision)."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (1.0, 0, 0), "x", h=1e-12)
        # May not be accurate but should not raise
        assert isinstance(result.value, float)

    def test_large_step_size(self):
        """Large step sizes should work (lower accuracy)."""

        def f(x, y, z):
            return x**2

        result = partial_derivative(f, (1.0, 0, 0), "x", h=0.1)
        assert abs(result.value - 2.0) < 0.1  # Rough accuracy

    def test_high_order_polynomial(self):
        """Derivatives of x^10 at x=1."""

        def f(x, y, z):
            return x**10

        result = partial_derivative(f, (1.0, 0, 0), "x")
        assert result.value == pytest.approx(10.0, rel=1e-4)

    def test_product_rule(self):
        """d/dx(x^2 * sin(x)) = 2x*sin(x) + x^2*cos(x)."""

        def f(x, y, z):
            return x**2 * np.sin(x)

        result = partial_derivative(f, (1.0, 0, 0), "x", method=DiffMethod.FIVE_POINT)
        expected = 2.0 * 1.0 * np.sin(1.0) + 1.0**2 * np.cos(1.0)
        assert result.value == pytest.approx(expected, rel=1e-8)

    def test_chain_rule(self):
        """d/dx(sin(x^2)) = 2x*cos(x^2)."""

        def f(x, y, z):
            return np.sin(x**2)

        result = partial_derivative(f, (1.0, 0, 0), "x", method=DiffMethod.FIVE_POINT)
        expected = 2.0 * 1.0 * np.cos(1.0)
        assert result.value == pytest.approx(expected, rel=1e-8)

    def test_invalid_method(self):
        """Should raise ValueError for unknown method."""

        def f(x, y, z):
            return x

        with pytest.raises(ValueError):
            partial_derivative(f, (0, 0, 0), "x", method=DiffMethod("invalid"))

    def test_jacobian_2d_transform(self):
        """Jacobian of 2D->2D transform."""

        def transform_2d(xy):
            x, y = xy
            return np.array([x + y, x - y])

        J = jacobian(transform_2d, np.array([1.0, 2.0]))
        assert J.shape == (2, 2)
        expected = np.array([[1, 1], [1, -1]], dtype=float)
        np.testing.assert_allclose(J, expected, atol=1e-5)
