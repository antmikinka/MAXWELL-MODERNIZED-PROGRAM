"""Tests for maxwell.math.calculus_calculator.

Comprehensive test suite covering:
- Category A: Analytical verification (exact solutions)
- Category B: Theorem verification (Divergence, Stokes', Green's)
- Category C: Maxwell physics applications
- Category D: Edge cases

Quality Review Fixes Applied:
- QR Issue 2: Stokes' theorem uses explicit hemisphere parameterization with
  analytical expected value (both sides = 0 for F=(yz,xz,xy) over hemisphere)
- QR Issue 3: Green's theorem uses scipy.integrate.dblquad directly (no thin z-slice)
- QR Issue 4: Ampere's law test uses Gaussian CGS consistently: H = 2*I/(c*r)
- QR Issue 5: Potential at center of sphere uses 3*Q/(2*R), not Q/R
- QR Issue 8: Added edge cases for negative limits, zero-width domains,
  non-differentiable parameterizations
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST
from maxwell.math.calculus_calculator import (
    CalculusCalculator,
    line_integral_circle,
    line_integral_polygonal,
    line_integral_scalar,
    line_integral_vector,
    surface_integral_scalar,
    surface_integral_sphere,
    surface_integral_vector,
    verify_divergence_theorem,
    verify_greens_theorem,
    verify_stokes_theorem,
    volume_integral_scalar,
    volume_integral_spherical,
    volume_integral_vector,
)

# ═══════════════════════════════════════════════════════════════════
# Category A: Analytical Verification
# ═══════════════════════════════════════════════════════════════════


class TestVolumeIntegrals:
    """Category A: Analytical volume integral tests."""

    def test_constant_over_unit_cube(self):
        """V-001: Triple integral of 1 over [0,1]^3 = 1."""
        result = volume_integral_scalar(
            lambda x, y, z: 1.0,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result - 1.0) < 1e-6

    def test_x_over_unit_cube(self):
        """V-002: Triple integral of x over [0,1]^3 = 0.5."""
        result = volume_integral_scalar(
            lambda x, y, z: x,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result - 0.5) < 1e-6

    def test_r_squared_over_unit_sphere(self):
        """V-003: Volume integral of r^2 over unit sphere.

        Derivation: I = integral_0^R r^4 dr * integral_0^pi sin(theta) dtheta
                    * integral_0^{2pi} dphi
                  = (R^5/5) * 2 * 2*pi = 4*pi*R^5/5
        For R=1: 4*pi/5
        """
        R = 1.0
        expected = 4 * np.pi * R**5 / 5.0

        result = volume_integral_spherical(
            lambda x, y, z: x**2 + y**2 + z**2,
            (0, R),
            (0, np.pi),
            (0, 2 * np.pi),
        )
        assert abs(result - expected) / expected < 0.005

    def test_uniform_sphere_charge(self):
        """V-004: Total charge of uniform sphere = (4/3)*pi*R^3*rho."""
        R, rho0 = 3.0, 2.0
        expected = (4 / 3) * np.pi * R**3 * rho0

        def rho(x, y, z):
            return rho0 if x**2 + y**2 + z**2 <= R**2 else 0.0

        result = volume_integral_scalar(
            rho,
            (-R, R),
            lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
            lambda x, y: (
                -np.sqrt(max(0, R**2 - x**2 - y**2)),
                np.sqrt(max(0, R**2 - x**2 - y**2)),
            ),
        )
        # Discontinuous integrand: allow 1% tolerance
        assert abs(result - expected) / expected < 0.01

    def test_y_over_unit_cube(self):
        """Triple integral of y over [0,1]^3 = 0.5."""
        result = volume_integral_scalar(
            lambda x, y, z: y,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result - 0.5) < 1e-6

    def test_xyz_over_unit_cube(self):
        """Triple integral of xyz over [0,1]^3 = 1/8."""
        result = volume_integral_scalar(
            lambda x, y, z: x * y * z,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result - 0.125) < 1e-6


class TestVolumeIntegralVector:
    """Vector volume integral tests."""

    def test_constant_vector_field_unit_cube(self):
        """Volume integral of F=(1,2,3) over unit cube = (1, 2, 3)."""
        result = volume_integral_vector(
            lambda x, y, z: 1.0,
            lambda x, y, z: 2.0,
            lambda x, y, z: 3.0,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result[0] - 1.0) < 1e-6
        assert abs(result[1] - 2.0) < 1e-6
        assert abs(result[2] - 3.0) < 1e-6

    def test_linear_vector_field(self):
        """Volume integral of F=(x,y,z) over unit cube = (0.5, 0.5, 0.5)."""
        result = volume_integral_vector(
            lambda x, y, z: x,
            lambda x, y, z: y,
            lambda x, y, z: z,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        for val in result:
            assert abs(val - 0.5) < 1e-6


class TestSphericalVolumeIntegral:
    """Spherical coordinate volume integral tests."""

    def test_unit_sphere_volume(self):
        """Volume of unit sphere via spherical coordinates = 4*pi/3."""
        result = volume_integral_spherical(
            lambda x, y, z: 1.0,
            (0, 1),
            (0, np.pi),
            (0, 2 * np.pi),
        )
        expected = 4 * np.pi / 3
        assert abs(result - expected) / expected < 1e-6

    def test_spherical_constant_full_sphere(self):
        """Spherical integral of constant over sphere radius R = 4*pi*R^3/3 * const."""
        R = 2.0
        result = volume_integral_spherical(
            lambda x, y, z: 5.0,
            (0, R),
        )
        expected = 5.0 * 4 * np.pi * R**3 / 3
        assert abs(result - expected) / expected < 1e-5


# ═══════════════════════════════════════════════════════════════════
# Surface Integral Tests
# ═══════════════════════════════════════════════════════════════════


class TestSurfaceIntegrals:
    """Category A: Analytical surface integral tests."""

    def test_unit_sphere_area(self):
        """S-001: Surface integral of g=1 over unit sphere = 4*pi."""
        R = 1.0

        def r_func(theta, phi):
            return (
                R * np.sin(theta) * np.cos(phi),
                R * np.sin(theta) * np.sin(phi),
                R * np.cos(theta),
            )

        result = surface_integral_scalar(
            lambda x, y, z: 1.0,
            (0, np.pi),
            (0, 2 * np.pi),
            r_func,
        )
        expected = 4 * np.pi
        assert abs(result - expected) / expected < 0.01

    def test_radial_field_flux(self):
        """S-002: Flux of r/r^3 through unit sphere = 4*pi.

        This is Gauss's law: for a point charge, E = r/r^3,
        and ∯ E · dA = 4*pi*q (in CGS with q=1).
        """
        R = 1.0

        def r_func(theta, phi):
            return (
                R * np.sin(theta) * np.cos(phi),
                R * np.sin(theta) * np.sin(phi),
                R * np.cos(theta),
            )

        def inv_r3_x(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return x / r3 if r3 > 0 else 0

        def inv_r3_y(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return y / r3 if r3 > 0 else 0

        def inv_r3_z(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return z / r3 if r3 > 0 else 0

        result = surface_integral_vector(
            inv_r3_x,
            inv_r3_y,
            inv_r3_z,
            (0, np.pi),
            (0, 2 * np.pi),
            r_func,
        )
        expected = 4 * np.pi
        assert abs(result - expected) / expected < 0.01

    def test_uniform_field_closed_surface(self):
        """S-003: Flux of uniform field through closed surface = 0."""
        R = 3.0

        def r_func(theta, phi):
            return (
                R * np.sin(theta) * np.cos(phi),
                R * np.sin(theta) * np.sin(phi),
                R * np.cos(theta),
            )

        # Uniform field in x direction
        result = surface_integral_vector(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            (0, np.pi),
            (0, 2 * np.pi),
            r_func,
        )
        # Net flux through closed surface for uniform field should be ~0
        assert abs(result) < 0.1


class TestSurfaceIntegralSphere:
    """Surface integral over spherical surface convenience function tests."""

    def test_sphere_flux_radial_field(self):
        """Flux of point charge field through sphere of radius R = 4*pi."""
        R = 5.0

        def inv_r3_x(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return x / r3 if r3 > 0 else 0

        def inv_r3_y(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return y / r3 if r3 > 0 else 0

        def inv_r3_z(x, y, z):
            r3 = (x**2 + y**2 + z**2) ** 1.5
            return z / r3 if r3 > 0 else 0

        result = surface_integral_sphere(
            inv_r3_x,
            inv_r3_y,
            inv_r3_z,
            radius=R,
        )
        expected = 4 * np.pi
        assert abs(result - expected) / expected < 0.01


# ═══════════════════════════════════════════════════════════════════
# Line Integral Tests
# ═══════════════════════════════════════════════════════════════════


class TestLineIntegrals:
    """Category A: Analytical line integral tests."""

    def test_constant_along_x_axis(self):
        """L-001: Line integral of F=(1,0,0) along x-axis [0,L] = L."""
        L = 5.0

        def line(t):
            return (t, 0.0, 0.0)

        result = line_integral_vector(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            (0, L),
            line,
        )
        assert abs(result - L) < 1e-6

    def test_rotational_field_unit_circle(self):
        """L-002: Line integral of F=(-y,x,0) around unit circle = 2*pi."""
        R = 1.0

        def circle(t):
            return (R * np.cos(t), R * np.sin(t), 0.0)

        result = line_integral_vector(
            lambda x, y, z: -y,
            lambda x, y, z: x,
            lambda x, y, z: 0.0,
            (0, 2 * np.pi),
            circle,
        )
        expected = 2 * np.pi
        assert abs(result - expected) / expected < 1e-5

    def test_gradient_field_closed_path(self):
        """L-003: Line integral of gradient field around closed path = 0.

        For phi = x^2 + y^2, grad(phi) = (2x, 2y, 0).
        The line integral around any closed path is 0.
        """

        def circle(t):
            return (np.cos(t), np.sin(t), 0.0)

        result = line_integral_vector(
            lambda x, y, z: 2 * x,
            lambda x, y, z: 2 * y,
            lambda x, y, z: 0.0,
            (0, 2 * np.pi),
            circle,
        )
        assert abs(result) < 1e-5

    def test_scalar_line_integral_arc_length(self):
        """Line integral of g=1 along line gives arc length."""
        # Line from (0,0,0) to (3,4,0), length = 5

        def line(t):
            return (3 * t, 4 * t, 0.0)

        result = line_integral_scalar(
            lambda x, y, z: 1.0,
            (0, 1),
            line,
        )
        assert abs(result - 5.0) < 1e-6


class TestLineIntegralCircle:
    """Circle path line integral tests."""

    def test_zero_field_circle(self):
        """Line integral of zero field around any circle = 0."""
        result = line_integral_circle(
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            radius=5.0,
        )
        assert abs(result) < 1e-10


class TestLineIntegralPolygonal:
    """Polygonal path line integral tests."""

    def test_constant_field_square_path(self):
        """Line integral of F=(1,0,0) along square path."""
        # Square with vertices at (0,0,0), (1,0,0), (1,1,0), (0,1,0)
        # F · dl = dx for each segment
        # Segment 1: dx=1, segment 2: dx=0, segment 3: dx=-1, segment 4: dx=0
        vertices = np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]
        )
        result = line_integral_polygonal(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            vertices,
            closed=True,
        )
        # Net: 1 + 0 + (-1) + 0 = 0
        assert abs(result) < 1e-10

    def test_open_path(self):
        """Line integral along open path from (0,0,0) to (1,0,0)."""
        vertices = np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
            ]
        )
        result = line_integral_polygonal(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            vertices,
            closed=False,
        )
        assert abs(result - 1.0) < 1e-10


# ═══════════════════════════════════════════════════════════════════
# Category B: Theorem Verification
# ═══════════════════════════════════════════════════════════════════


class TestTheoremVerifications:
    """Category B: Fundamental theorem verifications."""

    def test_divergence_theorem_identity_field(self):
        """T-001: F=(x,y,z) over unit cube, div(F)=3, volume integral = 3."""
        result = verify_divergence_theorem(
            lambda x, y, z: x,
            lambda x, y, z: y,
            lambda x, y, z: z,
            ((0, 1), (0, 1), (0, 1)),
        )
        assert result["verified"] is True
        assert abs(result["volume_integral"] - 3.0) < 0.01

    def test_divergence_theorem_quadratic_field(self):
        """T-002: F=(x^2,y^2,z^2) over [0,1]^3, div(F)=2(x+y+z), vol int = 3."""
        result = verify_divergence_theorem(
            lambda x, y, z: x**2,
            lambda x, y, z: y**2,
            lambda x, y, z: z**2,
            ((0, 1), (0, 1), (0, 1)),
        )
        assert result["verified"] is True
        # div(F) = 2x+2y+2z, integral over unit cube = 2*(0.5+0.5+0.5) = 3
        assert abs(result["volume_integral"] - 3.0) < 0.05

    def test_stokes_theorem_rotational_field(self):
        """T-003: F=(-y,x,0) over unit disk, curl(F)=(0,0,2), both sides = 2*pi."""
        R = 1.0

        def disk(r, theta):
            return (r * np.cos(theta), r * np.sin(theta), 0.0)

        def boundary(t):
            return (R * np.cos(t), R * np.sin(t), 0.0)

        result = verify_stokes_theorem(
            lambda x, y, z: -y,
            lambda x, y, z: x,
            lambda x, y, z: 0.0,
            disk,
            (0, R),
            (0, 2 * np.pi),
            boundary,
            (0, 2 * np.pi),
        )
        assert result["verified"] is True
        expected = 2 * np.pi
        assert abs(result["line_integral"] - expected) / expected < 0.01

    def test_stokes_theorem_hemisphere(self):
        """T-004: F=(yz,xz,xy) over upper hemisphere.

        Explicit hemisphere parameterization:
            r(theta, phi) = (sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta))
            theta in [0, pi/2], phi in [0, 2*pi]

        Boundary: boundary(t) = (cos(t), sin(t), 0), t in [0, 2*pi]

        curl(F) = (x-y, y-z, z-x)

        On the boundary (z=0): F = (0, 0, xy)
        F · dr = 0*cos(t) + 0*(-sin(t)) + cos(t)*sin(t)*0 = 0
        Line integral = 0

        On the z=0 plane: curl(F)·n = (x-y, y, -x)·(0,0,1) = -x
        By symmetry, integral of -x over the disk = 0

        Both sides should equal 0.
        """

        def hemisphere(theta, phi):
            return (
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta),
            )

        def boundary(t):
            return (np.cos(t), np.sin(t), 0.0)

        result = verify_stokes_theorem(
            lambda x, y, z: y * z,
            lambda x, y, z: x * z,
            lambda x, y, z: x * y,
            hemisphere,
            (0, np.pi / 2),
            (0, 2 * np.pi),
            boundary,
            (0, 2 * np.pi),
            tolerance=0.1,  # Relaxed for numerical integration
        )
        assert result["verified"] is True
        # Both should be near 0
        assert abs(result["line_integral"]) < 0.1
        assert abs(result["surface_integral"]) < 0.5

    def test_greens_theorem_rotational_2d(self):
        """T-005: P=-y, Q=x over unit disk.

        ∮(-y dx + x dy) over unit circle = 2*pi
        ∬(∂Q/∂x - ∂P/∂y) dA = ∬(1 - (-1)) dA = 2 * Area = 2*pi
        """

        def boundary(t):
            return (np.cos(t), np.sin(t))

        def P(x, y):
            return -y

        def Q(x, y):
            return x

        result = verify_greens_theorem(
            P,
            Q,
            (
                (-1, 1),
                lambda x: -np.sqrt(max(0, 1 - x**2)),
                lambda x: np.sqrt(max(0, 1 - x**2)),
            ),
            boundary,
            (0, 2 * np.pi),
        )
        assert result["verified"] is True
        expected = 2 * np.pi
        assert abs(result["line_integral"] - expected) / expected < 0.02

    def test_greens_theorem_quadratic_2d(self):
        """T-006: P=x^2, Q=y^2 over unit square.

        ∂Q/∂x - ∂P/∂y = 0 - 0 = 0
        Line integral around square should also be 0.
        """

        def boundary(t):
            # Parameterize square perimeter in 4 segments
            t = t % 4
            if t < 1:
                return (t, 0.0)
            elif t < 2:
                return (1.0, t - 1)
            elif t < 3:
                return (3 - t, 1.0)
            else:
                return (0.0, 4 - t)

        def P(x, y):
            return x**2

        def Q(x, y):
            return y**2

        result = verify_greens_theorem(
            P,
            Q,
            ((0, 1), 0.0, 1.0),
            boundary,
            (0, 4),
            tolerance=0.05,
        )
        assert result["verified"] is True
        assert abs(result["double_integral"]) < 1e-6


# ═══════════════════════════════════════════════════════════════════
# Category C: Maxwell Physics Applications
# ═══════════════════════════════════════════════════════════════════


class TestMaxwellPhysicsApplications:
    """Category C: Maxwell physics application tests."""

    def test_total_charge_uniform_sphere(self):
        """M-001: Total charge of uniform sphere = (4/3)*pi*R^3*rho."""
        R, rho0 = 4.0, 1.5
        expected = (4 / 3) * np.pi * R**3 * rho0

        def rho(x, y, z):
            return rho0 if x**2 + y**2 + z**2 <= R**2 else 0.0

        result = volume_integral_scalar(
            rho,
            (-R, R),
            lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
            lambda x, y: (
                -np.sqrt(max(0, R**2 - x**2 - y**2)),
                np.sqrt(max(0, R**2 - x**2 - y**2)),
            ),
        )
        assert abs(result - expected) / expected < 0.01

    def test_potential_at_center_charged_sphere(self):
        """M-002: Potential at center of uniformly charged sphere.

        phi(0) = ∭ rho/|r'| dV' = integral_0^R rho * 4*pi*r^2 dr / r
               = rho * 4*pi * R^2/2 = 2*pi*rho*R^2
        With Q = (4/3)*pi*R^3*rho => rho = 3*Q/(4*pi*R^3):
               phi(0) = 2*pi * 3*Q/(4*pi*R^3) * R^2 = 3*Q/(2*R)

        FIX: Quality review issue 5 - expected value is 3*Q/(2*R), NOT Q/R.
        """
        R = 3.0
        rho0 = 2.0
        Q = (4 / 3) * np.pi * R**3 * rho0
        expected = 3 * Q / (2 * R)  # Correct formula: 3Q/(2R)

        def integrand(x, y, z):
            r = np.sqrt(x**2 + y**2 + z**2)
            if r == 0:
                return 0.0  # The limit as r->0 of rho*r is 0
            return rho0 / r

        result = volume_integral_scalar(
            integrand,
            (-R, R),
            lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
            lambda x, y: (
                -np.sqrt(max(0, R**2 - x**2 - y**2)),
                np.sqrt(max(0, R**2 - x**2 - y**2)),
            ),
        )
        assert abs(result - expected) / expected < 0.01

    def test_emf_conservative_field(self):
        """M-003: EMF of conservative E-field around closed loop = 0.

        E = -grad(phi) is conservative, so ∮ E · dl = 0.
        """

        def circle(t):
            return (np.cos(t), np.sin(t), 0.0)

        # E = -grad(phi) for phi = x^2 + y^2 + z^2 => E = (-2x, -2y, -2z)
        result = line_integral_vector(
            lambda x, y, z: -2 * x,
            lambda x, y, z: -2 * y,
            lambda x, y, z: -2 * z,
            (0, 2 * np.pi),
            circle,
        )
        assert abs(result) < 1e-5

    def test_ampere_law_mmf(self):
        """M-004: MMF around infinite wire in Gaussian CGS.

        H field around wire: H_phi = 2*I/(c*r)
        Expected: ∮ H · dl = 4*pi*I/c

        FIX: Quality review issue 4 - use Gaussian CGS explicitly.
        """
        I = 1.0
        c = CONST.C
        R = 5.0
        expected = 4 * np.pi * I / c

        # H field in azimuthal direction
        def H_x(x, y, z):
            r = np.sqrt(x**2 + y**2)
            if r == 0:
                return 0.0
            H_phi = 2 * I / (c * r)
            return -H_phi * y / r  # -sin(phi) * H_phi

        def H_y(x, y, z):
            r = np.sqrt(x**2 + y**2)
            if r == 0:
                return 0.0
            H_phi = 2 * I / (c * r)
            return H_phi * x / r  # cos(phi) * H_phi

        def H_z(x, y, z):
            return 0.0

        def circle(t):
            return (R * np.cos(t), R * np.sin(t), 0.0)

        result = line_integral_vector(H_x, H_y, H_z, (0, 2 * np.pi), circle)
        assert abs(result - expected) / expected < 0.01

    def test_magnetic_flux_dipole_through_sphere(self):
        """M-005: Magnetic flux of dipole B-field through enclosing sphere.

        For a magnetic dipole, ∯ B · dA = 0 (no magnetic monopole).
        """
        R = 10.0

        # Dipole field (m = m0 * z_hat at origin)
        m0 = 1.0

        def B_dipole_x(x, y, z):
            r2 = x**2 + y**2 + z**2
            r5 = r2**2.5
            if r5 == 0:
                return 0.0
            return 3 * m0 * x * z / r5

        def B_dipole_y(x, y, z):
            r2 = x**2 + y**2 + z**2
            r5 = r2**2.5
            if r5 == 0:
                return 0.0
            return 3 * m0 * y * z / r5

        def B_dipole_z(x, y, z):
            r2 = x**2 + y**2 + z**2
            r5 = r2**2.5
            if r5 == 0:
                return 0.0
            return m0 * (3 * z**2 / r2 - 1) / (r2**1.5)

        result = surface_integral_sphere(B_dipole_x, B_dipole_y, B_dipole_z, radius=R)
        # Net magnetic flux through closed surface = 0 (Gauss's law for magnetism)
        assert abs(result) < 0.5

    def test_field_energy_uniform_sphere(self):
        """M-006: Field energy density integral over sphere with uniform E.

        U = ∭ (E^2/(8*pi)) dV = E^2/(8*pi) * (4/3)*pi*R^3
        """
        R = 4.0
        E0 = 2.0
        expected = E0**2 / (8 * np.pi) * (4 / 3) * np.pi * R**3

        result = volume_integral_scalar(
            lambda x, y, z: E0**2 / (8 * np.pi) if x**2 + y**2 + z**2 <= R**2 else 0.0,
            (-R, R),
            lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
            lambda x, y: (
                -np.sqrt(max(0, R**2 - x**2 - y**2)),
                np.sqrt(max(0, R**2 - x**2 - y**2)),
            ),
        )
        assert abs(result - expected) / expected < 0.01


# ═══════════════════════════════════════════════════════════════════
# Category D: Edge Cases
# ═══════════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Category D: Edge case tests (QR Issue 8 fixes)."""

    def test_singular_field_at_origin(self):
        """E-001: 1/r field near origin - should handle gracefully."""
        # Volume integral of 1/r over sphere radius 1
        # Analytical: ∭ (1/r) dV = integral_0^1 (1/r) * 4*pi*r^2 dr = 4*pi * R^2/2 = 2*pi
        R = 1.0

        def integrand(x, y, z):
            r = np.sqrt(x**2 + y**2 + z**2)
            return 1.0 / r if r > 1e-10 else 0.0

        # Using spherical coordinates avoids singularity
        result = volume_integral_spherical(
            integrand,
            (0.001, R),  # Start slightly away from origin
            (0, np.pi),
            (0, 2 * np.pi),
        )
        # Should produce a finite result
        assert np.isfinite(result)
        assert result > 0

    def test_discontinuous_integrand(self):
        """E-002: Step function integrand - converges with reduced accuracy."""
        R = 2.0
        rho0 = 3.0
        expected = rho0 * (4 / 3) * np.pi * R**3

        def rho(x, y, z):
            return rho0 if x**2 + y**2 + z**2 <= R**2 else 0.0

        result = volume_integral_scalar(
            rho,
            (-R, R),
            lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
            lambda x, y: (
                -np.sqrt(max(0, R**2 - x**2 - y**2)),
                np.sqrt(max(0, R**2 - x**2 - y**2)),
            ),
        )
        # Should converge within 2% for discontinuous integrand
        assert abs(result - expected) / expected < 0.02

    def test_large_domain(self):
        """E-003: Large integration domain - handles without overflow."""
        L = 10.0
        result = volume_integral_scalar(
            lambda x, y, z: 1.0,
            (0, L),
            (0, L),
            (0, L),
        )
        expected = L**3
        assert abs(result - expected) / expected < 1e-5

    def test_zero_length_path(self):
        """E-004: Zero-length path returns 0."""
        # Integrate from t=0 to t=0
        result = line_integral_vector(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            (0, 0),  # Zero-length
            lambda t: (t, 0.0, 0.0),
        )
        assert abs(result) < 1e-10

    def test_zero_area_surface(self):
        """E-005: Zero-area surface returns 0."""
        # Integrate over zero range
        R = 1.0

        def r_func(theta, phi):
            return (
                R * np.sin(theta) * np.cos(phi),
                R * np.sin(theta) * np.sin(phi),
                R * np.cos(theta),
            )

        result = surface_integral_scalar(
            lambda x, y, z: 1.0,
            (0, 0),  # Zero theta range
            (0, 2 * np.pi),
            r_func,
        )
        assert abs(result) < 1e-10

    def test_negative_integration_limits(self):
        """E-006: Negative integration limits work correctly.

        Integral from -1 to 1 of x^2 = 2/3
        """
        result = volume_integral_scalar(
            lambda x, y, z: x**2,
            (-1, 1),
            (0, 1),
            (0, 1),
        )
        expected = 2.0 / 3.0
        assert abs(result - expected) < 1e-6

    def test_negative_coordinate_integration(self):
        """E-007: Integration over negative coordinate domain.

        Integral of x over [-1,0] = -0.5
        """
        result = volume_integral_scalar(
            lambda x, y, z: x,
            (-1, 0),
            (0, 1),
            (0, 1),
        )
        expected = -0.5
        assert abs(result - expected) < 1e-6

    def test_small_domain(self):
        """E-008: Very small integration domain."""
        eps = 1e-6
        result = volume_integral_scalar(
            lambda x, y, z: 1.0,
            (0, eps),
            (0, eps),
            (0, eps),
        )
        expected = eps**3
        assert abs(result - expected) / max(expected, 1e-20) < 0.1

    def test_calculus_calculator_history(self):
        """E-009: CalculusCalculator tracks computation history."""
        calc = CalculusCalculator()
        calc.volume_integral(
            lambda x, y, z: 1.0,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        history = calc.get_history()
        assert len(history) >= 1
        assert history[-1]["operation"] == "volume_integral"

    def test_calculus_calculator_clear(self):
        """E-010: CalculusCalculator cache and history can be cleared."""
        calc = CalculusCalculator()
        calc.clear_cache()
        calc.clear_history()
        assert len(calc.get_history()) == 0
        assert len(calc._cache) == 0


# ═══════════════════════════════════════════════════════════════════
# CalculusCalculator Class Tests
# ═══════════════════════════════════════════════════════════════════


class TestCalculusCalculator:
    """Tests for the unified CalculusCalculator class."""

    def test_volume_integral_delegation(self):
        """CalculusCalculator.volume_integral delegates correctly."""
        calc = CalculusCalculator()
        result = calc.volume_integral(
            lambda x, y, z: 1.0,
            (0, 1),
            (0, 1),
            (0, 1),
        )
        assert abs(result - 1.0) < 1e-6

    def test_line_integral_delegation(self):
        """CalculusCalculator.line_integral delegates correctly."""
        calc = CalculusCalculator()
        result = calc.line_integral(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            (0, 5),
            lambda t: (t, 0.0, 0.0),
        )
        assert abs(result - 5.0) < 1e-6

    def test_divergence_theorem_via_calculator(self):
        """CalculusCalculator.verify_divergence_theorem works."""
        calc = CalculusCalculator()
        result = calc.verify_divergence_theorem(
            lambda x, y, z: x,
            lambda x, y, z: y,
            lambda x, y, z: z,
            ((0, 1), (0, 1), (0, 1)),
        )
        assert result["verified"] is True

    def test_stokes_theorem_via_calculator(self):
        """CalculusCalculator.verify_stokes_theorem works."""
        calc = CalculusCalculator()

        def disk(r, theta):
            return (r * np.cos(theta), r * np.sin(theta), 0.0)

        def boundary(t):
            return (np.cos(t), np.sin(t), 0.0)

        result = calc.verify_stokes_theorem(
            lambda x, y, z: -y,
            lambda x, y, z: x,
            lambda x, y, z: 0.0,
            disk,
            (0, 1),
            (0, 2 * np.pi),
            boundary,
            (0, 2 * np.pi),
        )
        assert result["verified"] is True

    def test_greens_theorem_via_calculator(self):
        """CalculusCalculator.verify_greens_theorem works."""
        calc = CalculusCalculator()

        def boundary(t):
            return (np.cos(t), np.sin(t))

        result = calc.verify_greens_theorem(
            lambda x, y: -y,
            lambda x, y: x,
            (
                (-1, 1),
                lambda x: -np.sqrt(max(0, 1 - x**2)),
                lambda x: np.sqrt(max(0, 1 - x**2)),
            ),
            boundary,
            (0, 2 * np.pi),
        )
        assert result["verified"] is True

    def test_precision_config(self):
        """CalculusCalculator respects precision setting."""
        calc = CalculusCalculator(precision=1e-12)
        assert calc.precision == 1e-12

    def test_unit_system_tracking(self):
        """CalculusCalculator tracks unit system."""
        calc = CalculusCalculator(unit_system="CGS-Gaussian")
        assert calc.unit_system == "CGS-Gaussian"

    def test_surface_integral_delegation(self):
        """CalculusCalculator.surface_integral delegates correctly."""
        calc = CalculusCalculator()
        R = 1.0

        def r_func(theta, phi):
            return (
                R * np.sin(theta) * np.cos(phi),
                R * np.sin(theta) * np.sin(phi),
                R * np.cos(theta),
            )

        result = calc.surface_integral(
            lambda x, y, z: 1.0,
            lambda x, y, z: 0.0,
            lambda x, y, z: 0.0,
            (0, np.pi),
            (0, 2 * np.pi),
            r_func,
        )
        # Uniform field through closed sphere = 0
        assert abs(result) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
