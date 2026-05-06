"""Tests for maxwell.vis.magnetic_shell -- Magnetic shell visualization."""

from __future__ import annotations

import numpy as np
import pytest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as mplt

from maxwell.vis._compat import HAS_MATPLOTLIB

pytestmark = pytest.mark.skipif(
    not HAS_MATPLOTLIB,
    reason="matplotlib not installed (pip install maxwell[viz])",
)

from maxwell.vis.magnetic_shell import (
    calc_solid_angle,
    calc_shell_potential,
    plot_magnetic_shell,
    plot_shell_potential,
)


class TestCalcSolidAngle:
    """Test calc_solid_angle function."""

    def test_on_axis_formula(self):
        """On-axis solid angle matches analytic formula."""
        z = np.array([1.0, 2.0, 5.0])
        omega = calc_solid_angle(np.zeros(3), np.zeros(3), z, loop_radius=1.0)
        # On axis: Omega = 2*pi * (1 - z/sqrt(z^2 + a^2)) * sign(z)
        for i, zi in enumerate(z):
            expected = 2.0 * np.pi * (1.0 - abs(zi) / np.sqrt(zi**2 + 1.0)) * np.sign(zi)
            assert np.isclose(omega[i], expected, rtol=1e-6)

    def test_far_field_decay(self):
        """Solid angle decreases with distance."""
        omega_near = calc_solid_angle(0.0, 0.0, 1.0, loop_radius=1.0)
        omega_far = calc_solid_angle(0.0, 0.0, 10.0, loop_radius=1.0)
        assert abs(omega_near) > abs(omega_far)

    def test_symmetry_above_below(self):
        """Solid angle changes sign when crossing the loop plane."""
        omega_above = calc_solid_angle(0.0, 0.0, 1.0, loop_radius=1.0)
        omega_below = calc_solid_angle(0.0, 0.0, -1.0, loop_radius=1.0)
        assert np.isclose(omega_above, -omega_below, rtol=1e-6)

    def test_shifted_loop_center(self):
        """Solid angle works with shifted loop center."""
        omega_centered = calc_solid_angle(1.0, 0.0, 1.0, loop_center=[0, 0, 0], loop_radius=1.0)
        omega_shifted = calc_solid_angle(0.0, 0.0, 1.0, loop_center=[-1, 0, 0], loop_radius=1.0)
        assert np.isclose(omega_centered, omega_shifted, rtol=1e-6)

    def test_radius_effect(self):
        """Larger loop gives larger solid angle at same distance."""
        omega_small = calc_solid_angle(0.0, 0.0, 1.0, loop_radius=0.5)
        omega_large = calc_solid_angle(0.0, 0.0, 1.0, loop_radius=2.0)
        assert abs(omega_large) > abs(omega_small)

    def test_no_nan_inf(self):
        """Output contains no NaN or Inf."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.ones_like(X) * 0.5
        omega = calc_solid_angle(X, Y, Z, loop_radius=1.0)
        assert not np.any(np.isnan(omega))
        assert not np.any(np.isinf(omega))

    def test_array_input(self):
        """Works with array inputs."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([0.0, 0.0, 0.0])
        z = np.array([1.0, 1.0, 1.0])
        omega = calc_solid_angle(x, y, z, loop_radius=1.0)
        assert omega.shape == (3,)

    def test_scalar_input(self):
        """Works with scalar inputs."""
        omega = calc_solid_angle(0.0, 0.0, 1.0, loop_radius=1.0)
        assert np.isscalar(omega) or omega.shape == ()


class TestCalcShellPotential:
    """Test calc_shell_potential function."""

    def test_potential_proportional_to_current(self):
        """V_m scales linearly with current."""
        V1 = calc_shell_potential(0.0, 0.0, 1.0, current=1.0, loop_radius=1.0)
        V2 = calc_shell_potential(0.0, 0.0, 1.0, current=2.0, loop_radius=1.0)
        assert np.isclose(V2, 2.0 * V1, rtol=1e-6)

    def test_potential_sign_flip(self):
        """Potential changes sign across loop plane."""
        V_above = calc_shell_potential(0.0, 0.0, 1.0, current=1.0, loop_radius=1.0)
        V_below = calc_shell_potential(0.0, 0.0, -1.0, current=1.0, loop_radius=1.0)
        assert np.isclose(V_above, -V_below, rtol=1e-6)

    def test_potential_at_large_distance(self):
        """Potential decreases with distance."""
        V_near = calc_shell_potential(0.0, 0.0, 1.0, current=1.0, loop_radius=1.0)
        V_far = calc_shell_potential(0.0, 0.0, 10.0, current=1.0, loop_radius=1.0)
        assert abs(V_near) > abs(V_far)


class TestPlotMagneticShell:
    """Test plot_magnetic_shell function."""

    def test_plot_returns_fig_ax(self):
        """plot_magnetic_shell returns (Figure, Axes)."""
        fig, ax = plot_magnetic_shell()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided 3D ax."""
        fig = mplt.figure()
        ax = fig.add_subplot(111, projection="3d")
        result_fig, result_ax = plot_magnetic_shell(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_custom_current(self):
        """Plot works with different current values."""
        fig, ax = plot_magnetic_shell(current=5.0, loop_radius=2.0)
        assert fig is not None
        mplt.close(fig)

    def test_plot_has_title(self):
        """Plot has a descriptive title."""
        fig, ax = plot_magnetic_shell()
        title = ax.get_title()
        assert "Art. 409" in title
        mplt.close(fig)

    def test_default_resolution(self):
        """Plot works with default resolution."""
        fig, ax = plot_magnetic_shell(resolution=30)
        assert fig is not None
        mplt.close(fig)


class TestPlotShellPotential:
    """Test plot_shell_potential function."""

    def test_plot_returns_fig_ax(self):
        """plot_shell_potential returns (Figure, Axes)."""
        fig, ax = plot_shell_potential()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_shell_potential(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_plot_has_labels(self):
        """Plot has axis labels."""
        fig, ax = plot_shell_potential()
        assert ax.get_xlabel() != ""
        assert ax.get_ylabel() != ""
        mplt.close(fig)

    def test_plot_has_colorbar(self):
        """Plot has a colorbar."""
        fig, ax = plot_shell_potential()
        # Colorbar axes are added as child axes to the figure
        # A figure with a colorbar will have more than 2 axes
        all_axes = fig.get_axes()
        assert len(all_axes) >= 2  # Main ax + colorbar ax
        mplt.close(fig)

    def test_custom_range(self):
        """Plot works with custom x_range and z_range."""
        fig, ax = plot_shell_potential(
            x_range=(-5.0, 5.0),
            z_range=(-5.0, 5.0),
            resolution=50,
        )
        assert fig is not None
        mplt.close(fig)

    def test_different_current(self):
        """Plot works with different current values."""
        fig, ax = plot_shell_potential(current=10.0, loop_radius=0.5)
        assert fig is not None
        mplt.close(fig)
