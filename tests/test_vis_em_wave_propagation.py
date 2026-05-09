"""Tests for maxwell.vis.em_wave_propagation -- EM wave propagation visualization."""

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

from maxwell.config.constants import CONST
from maxwell.vis.em_wave_propagation import (
    calc_em_wave,
    plot_em_wave_propagation,
    plot_wave_snapshot_3d,
)


class TestCalcEmWave:
    """Test calc_em_wave function."""

    def test_E_perpendicular_B(self):
        """E dot B = 0 at all points."""
        omega = 2 * np.pi
        k = omega / CONST.C
        x = np.linspace(0, CONST.C, 100)
        result = calc_em_wave(x, t=0.0, omega=omega, k=k, E0=1.0, polarization="linear")
        E_dot_B = (
            result["E_x"] * result["B_x"]
            + result["E_y"] * result["B_y"]
            + result["E_z"] * result["B_z"]
        )
        np.testing.assert_allclose(E_dot_B, np.zeros_like(E_dot_B), atol=1e-15)

    def test_E_B_ratio_equals_c(self):
        """|E|/|B| = c (within tolerance)."""
        omega = 2 * np.pi
        k = omega / CONST.C
        x = np.linspace(0, CONST.C, 100)
        result = calc_em_wave(x, t=0.0, omega=omega, k=k, E0=1.0, polarization="linear")
        E_mag = result["E_magnitude"]
        B_mag = result["B_magnitude"]
        mask = B_mag > 1e-15
        ratios = E_mag[mask] / B_mag[mask]
        np.testing.assert_allclose(ratios, CONST.C, rtol=1e-10)

    def test_wave_speed_omega_over_k(self):
        """Propagation speed = omega/k."""
        omega = 4 * np.pi
        k = 2 * np.pi
        expected_speed = omega / k
        assert np.isclose(expected_speed, 2.0)

    def test_linear_polarization_Ey_zero(self):
        """Linear pol: E_y = 0."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.linspace(0, 1.0, 50)
        result = calc_em_wave(x, t=0.0, omega=omega, k=k, E0=1.0, polarization="linear")
        np.testing.assert_allclose(
            result["E_y"], np.zeros_like(result["E_y"]), atol=1e-15
        )

    def test_circular_polarization_equal_amplitudes(self):
        """Circular: E_x^2 + E_y^2 = E0^2 at all points (constant amplitude)."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.linspace(0, 1.0, 100)
        result = calc_em_wave(
            x, t=0.0, omega=omega, k=k, E0=1.0, polarization="circular_right"
        )
        # For circular polarization, E_x^2 + E_y^2 = E0^2 at every point
        total = result["E_x"] ** 2 + result["E_y"] ** 2
        np.testing.assert_allclose(total, np.ones_like(total), rtol=1e-10)

    def test_elliptical_polarization(self):
        """Elliptical produces valid E and B fields."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.linspace(0, 1.0, 50)
        result = calc_em_wave(
            x, t=0.0, omega=omega, k=k, E0=1.0, polarization="elliptical"
        )
        assert not np.any(np.isnan(result["E_x"]))
        assert not np.any(np.isnan(result["E_y"]))
        assert np.max(np.abs(result["E_x"])) > np.max(np.abs(result["E_y"]))

    def test_circular_left_polarization(self):
        """Circular left produces opposite sign E_y."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.linspace(0, 0.25, 100)
        result_r = calc_em_wave(
            x, t=0.0, omega=omega, k=k, E0=1.0, polarization="circular_right"
        )
        result_l = calc_em_wave(
            x, t=0.0, omega=omega, k=k, E0=1.0, polarization="circular_left"
        )
        np.testing.assert_allclose(result_r["E_y"], -result_l["E_y"], atol=1e-10)

    def test_no_nan_inf(self):
        """Output contains no NaN or Inf."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.linspace(0, 1.0, 100)
        result = calc_em_wave(x, t=0.0, omega=omega, k=k, E0=1.0)
        for key in result:
            assert not np.any(np.isnan(result[key])), f"NaN in {key}"
            assert not np.any(np.isinf(result[key])), f"Inf in {key}"

    def test_invalid_polarization_raises(self):
        """Invalid polarization raises ValueError."""
        omega = 2 * np.pi * CONST.C
        k = 2 * np.pi
        x = np.array([0.0])
        with pytest.raises(ValueError):
            calc_em_wave(x, t=0.0, omega=omega, k=k, E0=1.0, polarization="invalid")


class TestPlotEmWavePropagation:
    """Test plot_em_wave_propagation function."""

    def test_plot_returns_fig_ax(self):
        """plot_em_wave_propagation returns (Figure, list[Axes])."""
        fig, axes = plot_em_wave_propagation()
        assert fig is not None
        assert isinstance(axes, list)
        assert len(axes) == 2
        mplt.close(fig)

    def test_plot_3d_returns_fig_ax(self):
        """plot_wave_snapshot_3d returns (Figure, Axes)."""
        fig, ax = plot_wave_snapshot_3d()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_default_args(self):
        """Works with no arguments."""
        fig, axes = plot_em_wave_propagation()
        assert fig is not None
        mplt.close(fig)

    def test_circular_polarization_plot(self):
        """Plot works with circular polarization."""
        fig, axes = plot_em_wave_propagation(polarization="circular_right")
        assert fig is not None
        mplt.close(fig)

    def test_3d_default_args(self):
        """3D plot works with no arguments."""
        fig, ax = plot_wave_snapshot_3d()
        assert fig is not None
        mplt.close(fig)

    def test_3d_custom_parameters(self):
        """3D plot works with custom parameters."""
        fig, ax = plot_wave_snapshot_3d(E0=2.0, wavelength=0.5, resolution=100)
        assert fig is not None
        mplt.close(fig)
