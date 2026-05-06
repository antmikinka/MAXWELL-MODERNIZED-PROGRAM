"""Tests for maxwell.vis.hysteresis_loops -- Hysteresis loop visualization."""

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

from maxwell.vis.hysteresis_loops import (
    calc_hysteresis_loop,
    plot_hysteresis_loops,
    plot_material_comparison,
)


class TestCalcHysteresisLoop:
    """Test calc_hysteresis_loop function."""

    def test_loop_closure(self):
        """Loop starts and ends near same B value (approximate closure)."""
        result = calc_hysteresis_loop(H_max=1000, mu_r=1000, alpha=0.001, n_points=300)
        B = result["B_values"]
        B_max_abs = np.max(np.abs(B))
        closure_error = abs(B[0] - B[-1]) / B_max_abs if B_max_abs > 0 else 0
        assert closure_error < 0.5

    def test_coercivity_positive(self):
        """Extracted H_c > 0."""
        result = calc_hysteresis_loop(H_max=1000, mu_r=1000, alpha=0.001, n_points=300)
        H = result["H_values"]
        B = result["B_values"]
        idx = np.argmin(np.abs(B[:len(B)//2]))
        H_c = abs(H[idx])
        assert H_c > 0

    def test_retentivity_positive(self):
        """Extracted B_r > 0."""
        result = calc_hysteresis_loop(H_max=1000, mu_r=1000, alpha=0.001, n_points=300)
        B = result["B_values"]
        H = result["H_values"]
        idx = np.argmin(np.abs(H[:len(H)//2]))
        B_r = abs(B[idx])
        assert B_r > 0

    def test_loop_area_positive(self):
        """Enclosed area > 0 (energy dissipation)."""
        result = calc_hysteresis_loop(H_max=1000, mu_r=1000, alpha=0.001, n_points=300)
        H_asc = result["H_branch1"]
        B_asc = result["B_branch1"]
        H_desc = result["H_branch2"]
        B_desc = result["B_branch2"]

        H_full = np.concatenate([H_asc, H_desc])
        B_full = np.concatenate([B_asc, B_desc])

        area = abs(np.trapezoid(B_full, H_full))
        assert area > 0

    def test_calc_hysteresis_loop_keys(self):
        """Returns dict with expected keys."""
        result = calc_hysteresis_loop(H_max=500, mu_r=500, alpha=0.01, n_points=100)
        for key in ["H_values", "B_values", "H_branch1", "B_branch1", "H_branch2", "B_branch2"]:
            assert key in result
            assert isinstance(result[key], np.ndarray)

    def test_soft_vs_hard_coercivity(self):
        """Hard material has larger H_c than soft."""
        soft = calc_hysteresis_loop(H_max=50, mu_r=5000, alpha=0.002, n_points=200)
        hard = calc_hysteresis_loop(H_max=1000, mu_r=20, alpha=0.6, n_points=200)

        B_soft = soft["B_values"]
        H_soft = soft["H_values"]
        idx_soft = np.argmin(np.abs(B_soft[:len(B_soft)//2]))
        H_c_soft = abs(H_soft[idx_soft])

        B_hard = hard["B_values"]
        H_hard = hard["H_values"]
        idx_hard = np.argmin(np.abs(B_hard[:len(B_hard)//2]))
        H_c_hard = abs(H_hard[idx_hard])

        assert H_c_hard > H_c_soft


class TestPlotHysteresisLoops:
    """Test plot_hysteresis_loops function."""

    def test_plot_returns_fig_ax(self):
        """plot_hysteresis_loops returns (Figure, Axes)."""
        fig, ax = plot_hysteresis_loops()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_plot_with_existing_ax(self):
        """Accepts and uses provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_hysteresis_loops(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_default_args(self):
        """Works with no arguments."""
        fig, ax = plot_hysteresis_loops()
        assert fig is not None
        mplt.close(fig)

    def test_no_coercivity_annotation(self):
        """Plot works with coercivity annotation disabled."""
        fig, ax = plot_hysteresis_loops(show_coercivity=False)
        assert fig is not None
        mplt.close(fig)

    def test_no_retentivity_annotation(self):
        """Plot works with retentivity annotation disabled."""
        fig, ax = plot_hysteresis_loops(show_retentivity=False)
        assert fig is not None
        mplt.close(fig)


class TestPlotMaterialComparison:
    """Test plot_material_comparison function."""

    def test_material_comparison_returns_fig(self):
        """plot_material_comparison returns figure."""
        fig, ax = plot_material_comparison()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_material_comparison_with_existing_ax(self):
        """Accepts and uses provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_material_comparison(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_material_comparison_has_legend(self):
        """Plot contains a legend with material names."""
        fig, ax = plot_material_comparison()
        legend = ax.get_legend()
        assert legend is not None
        mplt.close(fig)
