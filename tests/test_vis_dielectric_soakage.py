"""Tests for maxwell.vis.dielectric_soakage -- Dielectric absorption visualization."""

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

from maxwell.vis.dielectric_soakage import (
    calc_dielectric_absorption,
    plot_dielectric_soakage,
)


class TestCalcDielectricAbsorption:
    """Test calc_dielectric_absorption function."""

    def test_decay_monotonic(self):
        """Total current decreases with time."""
        t = np.linspace(0.01, 100.0, 200)
        I = calc_dielectric_absorption(t)
        assert I[0] > I[-1]

    def test_single_tau_exponential(self):
        """Single tau gives pure exponential decay."""
        tau = [5.0]
        A = [2.0]
        t = np.array([0.0, 5.0, 10.0])
        I = calc_dielectric_absorption(t, tau=tau, A=A)
        expected = 2.0 * np.exp(-t / 5.0)
        np.testing.assert_allclose(I, expected, atol=1e-10)

    def test_multi_tau_sum(self):
        """Multi-tau equals sum of individual exponentials."""
        tau = [1.0, 10.0]
        A = [1.0, 0.5]
        t = np.linspace(0.1, 20.0, 50)
        I_total = calc_dielectric_absorption(t, tau=tau, A=A)
        I_1 = 1.0 * np.exp(-t / 1.0)
        I_2 = 0.5 * np.exp(-t / 10.0)
        np.testing.assert_allclose(I_total, I_1 + I_2, atol=1e-10)

    def test_current_at_zero(self):
        """I(0) = sum(A_i)."""
        tau = [1.0, 10.0, 100.0]
        A = [1.0, 0.3, 0.1]
        t_zero = np.array([0.0])
        I = calc_dielectric_absorption(t_zero, tau=tau, A=A)
        expected = sum(A)
        assert np.isclose(I[0], expected)

    def test_long_time_decay(self):
        """Current approaches 0 as t >> max(tau)."""
        tau = [1.0, 10.0]
        A = [1.0, 0.5]
        t_large = np.array([10000.0])
        I = calc_dielectric_absorption(t_large, tau=tau, A=A)
        assert I[0] < 1e-10

    def test_no_nan_inf(self):
        """Output contains no NaN or Inf."""
        t = np.linspace(0.01, 1000.0, 500)
        I = calc_dielectric_absorption(t)
        assert not np.any(np.isnan(I))
        assert not np.any(np.isinf(I))

    def test_raises_on_length_mismatch(self):
        """Raises ValueError if tau and A have different lengths."""
        t = np.array([1.0])
        with pytest.raises(ValueError):
            calc_dielectric_absorption(t, tau=[1.0, 2.0], A=[1.0])

    def test_custom_parameters(self):
        """Works with custom tau and A values."""
        tau = [0.5, 2.0, 50.0]
        A = [0.8, 0.4, 0.05]
        t = np.array([1.0])
        I = calc_dielectric_absorption(t, tau=tau, A=A)
        expected = (
            0.8 * np.exp(-1.0 / 0.5)
            + 0.4 * np.exp(-1.0 / 2.0)
            + 0.05 * np.exp(-1.0 / 50.0)
        )
        assert np.isclose(I[0], expected)


class TestPlotDielectricSoakage:
    """Test plot_dielectric_soakage function."""

    def test_plot_returns_fig_ax(self):
        """plot_dielectric_soakage returns (Figure, Axes)."""
        fig, ax = plot_dielectric_soakage()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_dielectric_soakage(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_default_args(self):
        """Works with no arguments."""
        fig, ax = plot_dielectric_soakage()
        assert fig is not None
        mplt.close(fig)

    def test_log_scale_has_labels(self):
        """Log scale plot has appropriate axis labels."""
        fig, ax = plot_dielectric_soakage(log_scale=True)
        assert ax.get_xlabel() != ""
        assert ax.get_ylabel() != ""
        assert ax.get_xscale() == "log"
        assert ax.get_yscale() == "log"
        mplt.close(fig)

    def test_linear_scale_works(self):
        """Linear scale plot works correctly."""
        fig, ax = plot_dielectric_soakage(log_scale=False)
        assert ax.get_xscale() == "linear"
        assert ax.get_yscale() == "linear"
        mplt.close(fig)

    def test_custom_parameters_plot(self):
        """Plot works with custom tau and A."""
        fig, ax = plot_dielectric_soakage(
            tau=[0.5, 5.0],
            A=[2.0, 1.0],
            t_range=(0.1, 100.0),
            resolution=200,
        )
        assert fig is not None
        mplt.close(fig)

    def test_plot_has_legend(self):
        """Plot contains a legend."""
        fig, ax = plot_dielectric_soakage()
        legend = ax.get_legend()
        assert legend is not None
        mplt.close(fig)
