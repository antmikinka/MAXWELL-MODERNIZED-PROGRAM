"""Tests for maxwell.vis.helicoidal_potentials -- Helicoidal potential surfaces visualization."""

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

from maxwell.vis.helicoidal_potentials import (
    calc_solid_angle_loop,
    plot_helicoidal_potentials,
    plot_loop_field_lines,
    plot_loop_potential_3d,
)


# ============================================================
# CalcSolidAngleLoop -- 7 tests
# ============================================================
class TestCalcSolidAngleLoop:
    """Test calc_solid_angle_loop function."""

    def test_sign_change_across_loop_plane(self):
        """Solid angle changes sign when crossing z=0."""
        omega_above = calc_solid_angle_loop(0.0, 0.0, 1.0, loop_radius=1.0)
        omega_below = calc_solid_angle_loop(0.0, 0.0, -1.0, loop_radius=1.0)
        # Sign changes across the plane (magnitude differs due to off-axis approx)
        assert np.sign(omega_above["omega"]) != np.sign(omega_below["omega"])

    def test_on_axis_max_at_center(self):
        """Solid angle is largest near the loop center on axis."""
        omega_near = calc_solid_angle_loop(0.0, 0.0, 0.1, loop_radius=1.0)
        omega_far = calc_solid_angle_loop(0.0, 0.0, 5.0, loop_radius=1.0)
        assert abs(omega_near["omega"]) > abs(omega_far["omega"])

    def test_scales_with_current(self):
        """Omega = current * omega (magnetic potential scales with current)."""
        r1 = calc_solid_angle_loop(0.0, 0.0, 1.0, current=1.0, loop_radius=1.0)
        r2 = calc_solid_angle_loop(0.0, 0.0, 1.0, current=2.0, loop_radius=1.0)
        assert np.isclose(r2["Omega"], 2.0 * r1["Omega"])

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        result = calc_solid_angle_loop(0.0, 0.0, 1.0, loop_radius=1.0)
        expected_keys = {"omega", "Omega", "r_cyl"}
        assert set(result.keys()) == expected_keys

    def test_array_inputs(self):
        """Works with array inputs."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([0.0, 0.0, 0.0])
        z = np.array([1.0, 1.0, 1.0])
        result = calc_solid_angle_loop(x, y, z, loop_radius=1.0)
        assert result["omega"].shape == (3,)

    def test_no_nan_inf(self):
        """No NaN or Inf in output."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        z = np.full((20, 20), 0.5)
        result = calc_solid_angle_loop(x, y, z, loop_radius=1.0)
        assert not np.any(np.isnan(result["omega"]))
        assert not np.any(np.isinf(result["omega"]))

    def test_loop_radius_effect(self):
        """Larger loop radius gives larger solid angle at same distance."""
        omega_small = calc_solid_angle_loop(0.0, 0.0, 1.0, loop_radius=0.5)
        omega_large = calc_solid_angle_loop(0.0, 0.0, 1.0, loop_radius=2.0)
        assert abs(omega_large["omega"]) > abs(omega_small["omega"])


# ============================================================
# PlotHelicoidalPotentials -- 5 tests
# ============================================================
class TestPlotHelicoidalPotentials:
    """Test plot_helicoidal_potentials function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_helicoidal_potentials()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_helicoidal_potentials(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_has_title_with_citation(self):
        """Title contains Art. 487 reference."""
        fig, ax = plot_helicoidal_potentials()
        assert "Art. 487" in ax.get_title()
        mplt.close(fig)

    def test_has_colorbar(self):
        """Figure has colorbar."""
        fig, ax = plot_helicoidal_potentials()
        assert len(fig.get_axes()) >= 2
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom loop radius and current."""
        fig, ax = plot_helicoidal_potentials(
            loop_radius=2.0, current=5.0, resolution=30
        )
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotLoopPotential3D -- 4 tests
# ============================================================
class TestPlotLoopPotential3D:
    """Test plot_loop_potential_3d function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_loop_potential_3d()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_3d_projection(self):
        """Axes have 3D projection."""
        fig, ax = plot_loop_potential_3d()
        assert ax.name == "3d"
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided 3D ax."""
        fig = mplt.figure()
        ax = fig.add_subplot(111, projection="3d")
        rfig, rax = plot_loop_potential_3d(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom loop radius and resolution."""
        fig, ax = plot_loop_potential_3d(loop_radius=2.0, current=3.0, resolution=20)
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotLoopFieldLines -- 5 tests
# ============================================================
class TestPlotLoopFieldLines:
    """Test plot_loop_field_lines function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_loop_field_lines()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_loop_field_lines(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_has_title_with_citation(self):
        """Title contains Art. 486 reference."""
        fig, ax = plot_loop_field_lines()
        assert "Art. 486" in ax.get_title()
        mplt.close(fig)

    def test_has_contour_lines(self):
        """Plot contains contour collections (field lines)."""
        fig, ax = plot_loop_field_lines()
        # ax.contour creates a QuadContourSet with .collections
        contours = [c for c in ax.collections]
        assert len(contours) > 0
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom loop radius and current."""
        fig, ax = plot_loop_field_lines(loop_radius=2.0, current=5.0, resolution=40)
        assert fig is not None
        mplt.close(fig)
