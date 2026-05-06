"""Tests for maxwell.vis.flow_tubes -- Unit Tubes of Flow visualization."""

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

from maxwell.vis.flow_tubes import (
    calc_unit_tubes,
    plot_unit_tubes_of_flow,
    plot_unit_tubes_3d,
)


class TestCalcUnitTubes:
    """Test calc_unit_tubes function."""

    def test_returns_required_keys(self):
        """Output dictionary contains all required keys."""
        positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
        magnitudes = np.array([1.0, -1.0])
        result = calc_unit_tubes(positions, magnitudes, resolution=10)
        for key in ["Jx", "Jy", "Jz", "J_magnitude", "x", "y", "z", "X", "Y", "Z"]:
            assert key in result

    def test_field_shapes(self):
        """Field arrays have correct 3D shape."""
        positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
        magnitudes = np.array([1.0, -1.0])
        res = 10
        result = calc_unit_tubes(positions, magnitudes, resolution=res)
        expected_shape = (res, res, res)
        assert result["Jx"].shape == expected_shape
        assert result["Jy"].shape == expected_shape
        assert result["Jz"].shape == expected_shape
        assert result["J_magnitude"].shape == expected_shape

    def test_single_charge_radial(self):
        """Single charge produces radially outward field."""
        positions = np.array([[0.0, 0.0, 0.0]])
        magnitudes = np.array([1.0])
        result = calc_unit_tubes(positions, magnitudes,
                                 grid_range=(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0),
                                 resolution=15)
        # At point away from origin, field should point outward (positive x component for x>0)
        # Grid: -2..2 with 15 points -> index 11 is at x ~ 0.57
        ix = 11
        mid = 7  # center ~ 0
        assert result["Jx"][ix, mid, mid] > 0

    def test_dipole_field_between_charges(self):
        """Between dipole charges, field points from +q to -q (positive x direction)."""
        positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
        magnitudes = np.array([1.0, -1.0])
        result = calc_unit_tubes(positions, magnitudes,
                                 grid_range=(-3.0, 3.0, -3.0, 3.0, -3.0, 3.0),
                                 resolution=20)
        # At origin (midpoint between +1 and -1 on x axis),
        # field from +q (at x=1) points left (negative x),
        # field from -q (at x=-1) points left (toward -q, also negative x)
        # So total Jx at origin should be negative
        mid = 10  # approximate center index for 20 points
        assert result["Jx"][mid, mid, mid] < 0

    def test_no_nan_or_inf(self):
        """Output contains no NaN or Inf values."""
        positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
        magnitudes = np.array([1.0, -1.0])
        result = calc_unit_tubes(positions, magnitudes, resolution=15)
        assert not np.any(np.isnan(result["J_magnitude"]))
        assert not np.any(np.isinf(result["J_magnitude"]))

    def test_magnitude_is_positive(self):
        """Field magnitude is always non-negative."""
        positions = np.array([[0.5, 0.0, 0.0], [-0.5, 0.0, 0.0]])
        magnitudes = np.array([1.0, -1.0])
        result = calc_unit_tubes(positions, magnitudes, resolution=10)
        assert np.all(result["J_magnitude"] >= 0)

    def test_custom_grid_range(self):
        """Custom grid range is respected."""
        positions = np.array([[0.0, 0.0, 0.0]])
        magnitudes = np.array([1.0])
        result = calc_unit_tubes(positions, magnitudes,
                                 grid_range=(-5.0, 5.0, -3.0, 3.0, -2.0, 2.0),
                                 resolution=10)
        assert np.isclose(result["x"][0], -5.0, atol=0.6)
        assert np.isclose(result["x"][-1], 5.0, atol=0.6)
        assert np.isclose(result["y"][0], -3.0, atol=0.4)
        assert np.isclose(result["y"][-1], 3.0, atol=0.4)

    def test_charge_far_from_slice(self):
        """Field weakens with distance from charges."""
        positions = np.array([[0.0, 0.0, 0.0]])
        magnitudes = np.array([1.0])
        result = calc_unit_tubes(positions, magnitudes,
                                 grid_range=(-5.0, 5.0, -5.0, 5.0, -5.0, 5.0),
                                 resolution=20)
        # Center (near charge) should have stronger field than corners
        center_mag = result["J_magnitude"][10, 10, 10]
        corner_mag = result["J_magnitude"][0, 0, 0]
        assert center_mag > corner_mag


class TestPlotUnitTubesOfFlow:
    """Test plot_unit_tubes_of_flow function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_unit_tubes_of_flow()
        assert fig is not None
        assert ax is not None
        mplt.close(fig)

    def test_default_dipole(self):
        """Works with default dipole charges."""
        fig, ax = plot_unit_tubes_of_flow()
        assert ax.get_title() != ""
        mplt.close(fig)

    def test_streamplot_mode(self):
        """Streamplot mode works."""
        fig, ax = plot_unit_tubes_of_flow(plot_mode="streamplot")
        assert fig is not None
        mplt.close(fig)

    def test_quiver_mode(self):
        """Quiver mode works."""
        fig, ax = plot_unit_tubes_of_flow(plot_mode="quiver")
        assert fig is not None
        mplt.close(fig)

    def test_invalid_mode_raises(self):
        """Invalid plot_mode raises ValueError."""
        with pytest.raises(ValueError, match="Unknown plot_mode"):
            plot_unit_tubes_of_flow(plot_mode="invalid")

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_unit_tubes_of_flow(ax=ax)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)

    def test_hide_charges(self):
        """Works with show_charges=False."""
        fig, ax = plot_unit_tubes_of_flow(show_charges=False)
        assert fig is not None
        mplt.close(fig)

    def test_custom_charges(self):
        """Works with custom charge configuration."""
        positions = np.array([[2.0, 0.0, 0.0], [-2.0, 0.0, 0.0]])
        magnitudes = np.array([2.0, -2.0])
        fig, ax = plot_unit_tubes_of_flow(
            charge_positions=positions,
            charge_magnitudes=magnitudes,
            resolution=40,
        )
        assert fig is not None
        mplt.close(fig)

    def test_custom_slice_z(self):
        """Works with non-zero slice_z."""
        fig, ax = plot_unit_tubes_of_flow(slice_z=1.0)
        assert fig is not None
        mplt.close(fig)

    def test_custom_density(self):
        """Works with custom streamplot density."""
        fig, ax = plot_unit_tubes_of_flow(density=2.0)
        assert fig is not None
        mplt.close(fig)


class TestPlotUnitTubes3D:
    """Test plot_unit_tubes_3d function."""

    def test_returns_figure(self):
        """Returns a matplotlib Figure."""
        fig = plot_unit_tubes_3d()
        assert fig is not None
        mplt.close(fig)

    def test_default_dipole_3d(self):
        """Works with default dipole in 3D."""
        fig = plot_unit_tubes_3d()
        assert fig is not None
        mplt.close(fig)

    def test_custom_resolution(self):
        """Works with custom grid resolution."""
        fig = plot_unit_tubes_3d(resolution=6, skip=1)
        assert fig is not None
        mplt.close(fig)
