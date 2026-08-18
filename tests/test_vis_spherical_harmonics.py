"""Tests for maxwell.vis.spherical_harmonics -- Spherical harmonic globe visualization."""

from __future__ import annotations

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as mplt

from maxwell.vis._compat import HAS_MATPLOTLIB

pytestmark = pytest.mark.skipif(
    not HAS_MATPLOTLIB,
    reason="matplotlib not installed (pip install maxwell[viz])",
)

from maxwell.vis.spherical_harmonics import (
    calc_field_intensity,
    calc_gauss_harmonics,
    plot_harmonic_contour,
    plot_harmonic_globe,
    plot_harmonic_modes,
)


class TestCalcGaussHarmonics:
    """Test calc_gauss_harmonics function."""

    def test_dipole_only(self):
        """Pure axial dipole gives cos(theta) pattern."""
        coeffs = {(1, 0): (1.0, 0.0)}
        theta = np.array([0.0, np.pi / 2, np.pi])
        phi = np.zeros(3)
        V = calc_gauss_harmonics(1, 0, coeffs, theta, phi)
        # P_1^0(cos(theta)) = cos(theta), so V = g_1^0 * cos(theta)
        expected = np.array([1.0, 0.0, -1.0])
        np.testing.assert_allclose(V, expected, atol=1e-6)

    def test_zero_coefficients(self):
        """Zero coefficients give zero potential."""
        coeffs = {(1, 0): (0.0, 0.0)}
        theta = np.linspace(0, np.pi, 10)
        phi = np.linspace(0, 2 * np.pi, 10)
        V = calc_gauss_harmonics(1, 0, coeffs, theta, phi)
        np.testing.assert_allclose(V, np.zeros(10), atol=1e-10)

    def test_multiple_coefficients_sum(self):
        """Multiple coefficients produce superposition."""
        coeffs = {
            (1, 0): (1.0, 0.0),
            (2, 0): (0.5, 0.0),
        }
        theta = np.array([np.pi / 3])
        phi = np.zeros(1)
        V_total = calc_gauss_harmonics(2, 0, coeffs, theta, phi)
        V_1 = calc_gauss_harmonics(2, 0, {(1, 0): (1.0, 0.0)}, theta, phi)
        V_2 = calc_gauss_harmonics(2, 0, {(2, 0): (0.5, 0.0)}, theta, phi)
        np.testing.assert_allclose(V_total, V_1 + V_2, atol=1e-10)

    def test_phi_independence_for_m0(self):
        """m=0 modes are independent of phi."""
        coeffs = {(2, 0): (1.0, 0.0)}
        theta = np.full(5, np.pi / 4)
        phi = np.linspace(0, 2 * np.pi, 5)
        V = calc_gauss_harmonics(2, 0, coeffs, theta, phi)
        assert np.allclose(V, V[0], atol=1e-10)

    def test_phi_dependence_for_m1(self):
        """m>0 modes depend on phi."""
        coeffs = {(1, 1): (1.0, 0.0)}
        theta = np.full(4, np.pi / 3)
        phi = np.array([0.0, np.pi / 2, np.pi, 3 * np.pi / 2])
        V = calc_gauss_harmonics(1, 1, coeffs, theta, phi)
        # V = g_1^1 * cos(phi) * P_1^1(cos(theta))
        # P_1^1(x) = -sin(theta), so V = g_1^1 * cos(phi) * (-sin(theta))
        assert not np.allclose(V, V[0], atol=1e-6)

    def test_array_shapes_match(self):
        """Output shape matches input shape."""
        coeffs = {(1, 0): (1.0, 0.0)}
        theta = np.linspace(0, np.pi, 20).reshape(4, 5)
        phi = np.linspace(0, 2 * np.pi, 20).reshape(4, 5)
        V = calc_gauss_harmonics(1, 0, coeffs, theta, phi)
        assert V.shape == (4, 5)


class TestCalcFieldIntensity:
    """Test calc_field_intensity function."""

    def test_returns_all_components(self):
        """Returns B_r, B_theta, B_phi, B_total, V."""
        coeffs = {(1, 0): (1.0, 0.0)}
        theta = np.array([np.pi / 4])
        phi = np.array([0.0])
        result = calc_field_intensity(1, 0, coeffs, theta, phi)
        assert "B_r" in result
        assert "B_theta" in result
        assert "B_phi" in result
        assert "B_total" in result
        assert "V" in result

    def test_field_magnitude_positive(self):
        """Total field magnitude is non-negative."""
        coeffs = {(1, 0): (1.0, 0.0)}
        theta = np.linspace(0.1, np.pi - 0.1, 10)
        phi = np.zeros(10)
        result = calc_field_intensity(1, 0, coeffs, theta, phi)
        assert np.all(result["B_total"] >= 0)

    def test_dipole_field_pattern(self):
        """Dipole field is strongest at poles."""
        coeffs = {(1, 0): (1.0, 0.0)}
        theta_pole = np.array([0.1])
        theta_eq = np.array([np.pi / 2])
        phi = np.zeros(1)
        r_pole = calc_field_intensity(1, 0, coeffs, theta_pole, phi)
        r_eq = calc_field_intensity(1, 0, coeffs, theta_eq, phi)
        # Dipole field should be stronger at poles than equator
        assert r_pole["B_total"][0] > r_eq["B_total"][0]


class TestPlotHarmonicGlobe:
    """Test plot_harmonic_globe function."""

    def test_plot_returns_fig_ax(self):
        """plot_harmonic_globe returns (Figure, Axes)."""
        fig, ax = plot_harmonic_globe()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided 3D ax."""
        fig = mplt.figure()
        ax = fig.add_subplot(111, projection="3d")
        result_fig, result_ax = plot_harmonic_globe(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_custom_coefficients(self):
        """Plot works with custom Gauss coefficients."""
        coeffs = {(1, 0): (2.0, 0.0), (3, 0): (0.5, 0.0)}
        fig, ax = plot_harmonic_globe(n=3, m=0, coeffs=coeffs)
        assert fig is not None
        mplt.close(fig)

    def test_plot_has_title(self):
        """Plot has a descriptive title."""
        fig, ax = plot_harmonic_globe(n=2)
        title = ax.get_title()
        assert "Art. 467" in title
        mplt.close(fig)


class TestPlotHarmonicModes:
    """Test plot_harmonic_modes function."""

    def test_plot_returns_fig_axes(self):
        """plot_harmonic_modes returns (Figure, axes array)."""
        fig, axes = plot_harmonic_modes(max_n=2)
        assert fig is not None
        assert axes is not None
        mplt.close(fig)

    def test_axes_grid_size(self):
        """Returns correct number of subplots."""
        max_n = 3
        fig, axes = plot_harmonic_modes(max_n=max_n)
        assert axes.shape == (max_n + 1, max_n + 1)
        mplt.close(fig)

    def test_invalid_modes_hidden(self):
        """Subplots with m > l are hidden."""
        max_n = 2
        fig, axes = plot_harmonic_modes(max_n=max_n)
        # (l=1, m=2) and (l=0, m=1), (l=0, m=2) should be hidden
        assert not axes[0, 1].get_visible()  # l=0, m=1
        assert not axes[0, 2].get_visible()  # l=0, m=2
        assert not axes[1, 2].get_visible()  # l=1, m=2
        mplt.close(fig)

    def test_valid_modes_visible(self):
        """Valid (l, m) subplots are visible."""
        max_n = 2
        fig, axes = plot_harmonic_modes(max_n=max_n)
        assert axes[0, 0].get_visible()  # l=0, m=0 (monopole)
        assert axes[1, 0].get_visible()  # l=1, m=0 (dipole zonal)
        assert axes[1, 1].get_visible()  # l=1, m=1 (dipole sectorial)
        assert axes[2, 2].get_visible()  # l=2, m=2 (quadrupole sectorial)
        mplt.close(fig)


class TestPlotHarmonicContour:
    """Test plot_harmonic_contour function."""

    def test_plot_returns_fig_ax(self):
        """plot_harmonic_contour returns (Figure, Axes)."""
        fig, ax = plot_harmonic_contour()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_harmonic_contour(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_plot_has_labels(self):
        """Plot has axis labels."""
        fig, ax = plot_harmonic_contour()
        assert ax.get_xlabel() != ""
        assert ax.get_ylabel() != ""
        mplt.close(fig)

    def test_plot_has_colorbar(self):
        """Plot has a colorbar."""
        fig, ax = plot_harmonic_contour()
        # A figure with a colorbar will have more than 1 axes
        all_axes = fig.get_axes()
        assert len(all_axes) >= 2  # Main ax + colorbar ax
        mplt.close(fig)

    def test_custom_resolution(self):
        """Plot works with custom resolution."""
        fig, ax = plot_harmonic_contour(resolution=50)
        assert fig is not None
        mplt.close(fig)
