"""Tests for maxwell.vis.electrotonic_state -- Electrotonic State visualization."""

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

from maxwell.vis.electrotonic_state import (
    calc_electrotonic_straight_wire,
    calc_electrotonic_transient,
    calc_B_from_electrotonic,
    plot_electrotonic_state_2d,
    plot_A_and_B_fields,
    plot_A_transient,
    plot_electrotonic_3d_surface,
)


# ============================================================
# CalcElectrotonicStraightWire -- 7 tests
# ============================================================
class TestCalcElectrotonicStraightWire:
    """Test calc_electrotonic_straight_wire function."""

    def test_log_decay_with_distance(self):
        """|A| decreases logarithmically with distance from wire."""
        result_near = calc_electrotonic_straight_wire(
            np.array([0.3]), np.array([0.0]), np.array([0.0]), current=1.0
        )
        result_far = calc_electrotonic_straight_wire(
            np.array([2.0]), np.array([0.0]), np.array([0.0]), current=1.0
        )
        assert result_near["A_magnitude"][0] > result_far["A_magnitude"][0]

    def test_scaling_with_current(self):
        """A scales linearly with current."""
        r1 = calc_electrotonic_straight_wire(
            np.array([1.0]), np.array([0.0]), np.array([0.0]), current=1.0
        )
        r2 = calc_electrotonic_straight_wire(
            np.array([1.0]), np.array([0.0]), np.array([0.0]), current=2.0
        )
        assert np.isclose(r2["A_magnitude"][0], 2.0 * r1["A_magnitude"][0])

    def test_z_axis_wire_A_along_z(self):
        """For z-axis wire, A points along z (A_x = A_y = 0)."""
        result = calc_electrotonic_straight_wire(
            np.array([1.0]), np.array([1.0]), np.array([0.0]),
            current=1.0, wire_axis="z",
        )
        assert result["A_x"][0] == 0.0
        assert result["A_y"][0] == 0.0
        assert result["A_z"][0] != 0.0

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        result = calc_electrotonic_straight_wire(
            np.array([1.0]), np.array([1.0]), np.array([0.0]),
        )
        expected_keys = {"A_x", "A_y", "A_z", "A_magnitude", "r_cyl"}
        assert set(result.keys()) == expected_keys

    def test_cylindrical_radius(self):
        """r_cyl = sqrt(x^2 + y^2) for z-axis wire."""
        result = calc_electrotonic_straight_wire(
            np.array([3.0]), np.array([4.0]), np.array([0.0]),
        )
        assert np.isclose(result["r_cyl"][0], 5.0)

    def test_no_nan_inf(self):
        """No NaN or Inf in output (core regularization works)."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        result = calc_electrotonic_straight_wire(X, Y, Z)
        assert not np.any(np.isnan(result["A_magnitude"]))
        assert not np.any(np.isinf(result["A_magnitude"]))

    def test_invalid_axis_raises(self):
        """Raises ValueError for unknown wire axis."""
        with pytest.raises(ValueError):
            calc_electrotonic_straight_wire(
                np.array([0.0]), np.array([0.0]), np.array([0.0]),
                wire_axis="w",
            )


# ============================================================
# CalcElectrotonicTransient -- 5 tests
# ============================================================
class TestCalcElectrotonicTransient:
    """Test calc_electrotonic_transient function."""

    def test_exponential_decay(self):
        """A(t) follows exponential transient."""
        # At t=0, current = 0; at t=inf, current = 1
        r0 = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=1.0, time=0.0,
        )
        r_inf = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=1.0, time=100.0,
        )
        I_0 = r0["I_t"] if np.isscalar(r0["I_t"]) else r0["I_t"][0]
        I_inf = r_inf["I_t"] if np.isscalar(r_inf["I_t"]) else r_inf["I_t"][0]
        assert I_inf > I_0

    def test_initial_value(self):
        """At t=0, current equals initial."""
        result = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=1.0, time=0.0,
        )
        I_0 = result["I_t"] if np.isscalar(result["I_t"]) else result["I_t"][0]
        assert np.isclose(I_0, 0.0)

    def test_final_value(self):
        """At t >> tau, current approaches final."""
        result = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=1.0, time=100.0,
        )
        I_f = result["I_t"] if np.isscalar(result["I_t"]) else result["I_t"][0]
        assert np.isclose(I_f, 1.0, rtol=1e-6)

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        result = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
        )
        expected_keys = {"A_z", "A_magnitude", "time", "I_t"}
        assert set(result.keys()) == expected_keys

    def test_time_constant_effect(self):
        """Larger time constant means slower approach to final."""
        r_fast = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=0.1, time=1.0,
        )
        r_slow = calc_electrotonic_transient(
            np.array([1.0]), np.array([0.0]),
            current_initial=0.0, current_final=1.0,
            time_constant=10.0, time=1.0,
        )
        I_fast = r_fast["I_t"] if np.isscalar(r_fast["I_t"]) else r_fast["I_t"][0]
        I_slow = r_slow["I_t"] if np.isscalar(r_slow["I_t"]) else r_slow["I_t"][0]
        # Faster tau means closer to final at same t
        assert I_fast > I_slow


# ============================================================
# CalcBFromElectrotonic -- 4 tests
# ============================================================
class TestCalcBFromElectrotonic:
    """Test calc_B_from_electrotonic function."""

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        A_func = lambda x, y, z: (
            np.zeros_like(x), np.zeros_like(y),
            -2.0 * np.log(np.sqrt(x**2 + y**2) + 1e-10)
        )
        x = np.array([[0.5, 1.0], [0.5, 1.0]])
        y = np.array([[0.5, 0.5], [1.0, 1.0]])
        z = np.zeros_like(x)
        result = calc_B_from_electrotonic(A_func, x, y, z)
        expected_keys = {"B_x", "B_y", "B_z", "B_magnitude"}
        assert set(result.keys()) == expected_keys

    def test_B_nonzero_around_wire(self):
        """B field is non-zero around current-carrying wire."""
        current = 1.0
        A_func = lambda x, y, z: calc_electrotonic_straight_wire(
            x, y, z, current=current, wire_axis="z"
        )
        # Use a function that returns tuple
        def A_tuple(x, y, z):
            r = calc_electrotonic_straight_wire(x, y, z, current=current)
            return r["A_x"], r["A_y"], r["A_z"]

        x = np.array([[1.0]])
        y = np.array([[0.0]])
        z = np.array([[0.0]])
        result = calc_B_from_electrotonic(A_tuple, x, y, z)
        assert result["B_magnitude"][0, 0] > 0

    def test_B_matches_biot_savart_order(self):
        """B magnitude is approximately 2*I/r (CGS-EMU) for z-axis wire."""
        current = 1.0
        def A_tuple(x, y, z):
            r = calc_electrotonic_straight_wire(x, y, z, current=current)
            return r["A_x"], r["A_y"], r["A_z"]

        # Test at r=1
        x = np.array([[1.0]])
        y = np.array([[0.0]])
        z = np.array([[0.0]])
        result = calc_B_from_electrotonic(A_tuple, x, y, z, h=1e-7)
        # B_theta = 2*I/r = 2.0 at r=1
        expected_B = 2.0 * current / 1.0
        assert np.isclose(result["B_magnitude"][0, 0], expected_B, rtol=1e-3)

    def test_no_nan_inf(self):
        """No NaN or Inf in B field output."""
        def A_tuple(x, y, z):
            r = calc_electrotonic_straight_wire(x, y, z)
            return r["A_x"], r["A_y"], r["A_z"]

        x = np.array([[0.5, 1.0, 1.5], [0.5, 1.0, 1.5], [0.5, 1.0, 1.5]])
        y = np.array([[0.5, 0.5, 0.5], [1.0, 1.0, 1.0], [1.5, 1.5, 1.5]])
        z = np.zeros_like(x)
        result = calc_B_from_electrotonic(A_tuple, x, y, z)
        assert not np.any(np.isnan(result["B_magnitude"]))
        assert not np.any(np.isinf(result["B_magnitude"]))


# ============================================================
# PlotElectrotonicState2D -- 5 tests
# ============================================================
class TestPlotElectrotonicState2D:
    """Test plot_electrotonic_state_2d function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_electrotonic_state_2d()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_electrotonic_state_2d(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_has_title_with_citation(self):
        """Title contains Art. 540 reference."""
        fig, ax = plot_electrotonic_state_2d()
        assert "Art. 540" in ax.get_title()
        mplt.close(fig)

    def test_has_colorbar(self):
        """Figure has colorbar."""
        fig, ax = plot_electrotonic_state_2d()
        assert len(fig.get_axes()) >= 2
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom current and grid range."""
        fig, ax = plot_electrotonic_state_2d(
            current=2.0,
            grid_range=(-3.0, 3.0),
            resolution=30,
        )
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotAAndBFields -- 4 tests
# ============================================================
class TestPlotAAndBFields:
    """Test plot_A_and_B_fields function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_A_and_B_fields()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_creates_two_panels(self):
        """Creates figure with 2 axes (A-field and B-field panels)."""
        fig, _ = plot_A_and_B_fields()
        assert len(fig.get_axes()) >= 2
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax for A-field panel."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_A_and_B_fields(ax=ax)
        # Function creates 2-panel layout; ax becomes the first panel
        assert rfig is fig
        assert len(fig.get_axes()) >= 2
        mplt.close(fig)

    def test_custom_current(self):
        """Works with custom current value."""
        fig, ax = plot_A_and_B_fields(current=2.0, resolution=20)
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotATransient -- 4 tests
# ============================================================
class TestPlotATransient:
    """Test plot_A_transient function."""

    def test_returns_fig_axes(self):
        """Returns (Figure, list[Axes]) with 2 axes."""
        fig, axes = plot_A_transient()
        assert fig is not None and len(axes) == 2
        mplt.close(fig)

    def test_time_series_shape(self):
        """Panel 1 has proper time series data."""
        fig, axes = plot_A_transient()
        lines = axes[0].get_lines()
        assert len(lines) == 3  # 3 default observation points
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom transient parameters."""
        fig, axes = plot_A_transient(
            current_initial=0.0,
            current_final=2.0,
            time_constant=0.5,
            time_range=(0.0, 3.0),
            observation_points=[(1.0, 0.0)],
        )
        assert fig is not None
        mplt.close(fig)

    def test_with_existing_fig(self):
        """Accepts provided figure."""
        fig, _ = mplt.subplots(1, 2, figsize=(14, 5))
        rfig, raxes = plot_A_transient(fig=fig)
        assert rfig is fig and len(raxes) == 2
        mplt.close(fig)


# ============================================================
# PlotElectrotonic3DSurface -- 4 tests
# ============================================================
class TestPlotElectrotonic3DSurface:
    """Test plot_electrotonic_3d_surface function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_electrotonic_3d_surface()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_3d_projection(self):
        """Axes have 3D projection."""
        fig, ax = plot_electrotonic_3d_surface()
        assert ax.name == "3d"
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided 3D ax."""
        fig = mplt.figure()
        ax = fig.add_subplot(111, projection="3d")
        rfig, rax = plot_electrotonic_3d_surface(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom current and resolution."""
        fig, ax = plot_electrotonic_3d_surface(
            current=2.0,
            resolution=25,
        )
        assert fig is not None
        mplt.close(fig)
