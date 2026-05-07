"""Tests for maxwell.vis.thermal_gradients -- Thermal gradients and Joule heating visualization."""

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

from maxwell.vis.thermal_gradients import (
    calc_joule_heat_distribution,
    calc_thermal_gradients,
    calc_peltier_junction,
    plot_thermal_gradients,
    plot_joule_heat_distribution,
    plot_thermoelectric_effects,
)


# ============================================================
# CalcJouleHeatDistribution -- 5 tests
# ============================================================
class TestCalcJouleHeatDistribution:
    """Test calc_joule_heat_distribution function."""

    def test_uniform_field(self):
        """p = sigma * E^2 for uniform field."""
        E_x = np.array([1e-8])
        E_y = np.array([0.0])
        sigma = 5.8e17
        p = calc_joule_heat_distribution(E_x, E_y, sigma)
        expected = sigma * 1e-16
        assert np.isclose(p[0], expected)

    def test_non_negative(self):
        """Power density is always non-negative."""
        E_x = np.random.randn(10, 10)
        E_y = np.random.randn(10, 10)
        p = calc_joule_heat_distribution(E_x, E_y)
        assert np.all(p >= 0)

    def test_scales_with_sigma(self):
        """Doubling sigma doubles power density."""
        E_x, E_y = np.array([1e-8]), np.array([1e-8])
        p1 = calc_joule_heat_distribution(E_x, E_y, sigma=1e17)
        p2 = calc_joule_heat_distribution(E_x, E_y, sigma=2e17)
        assert np.isclose(p2[0], 2.0 * p1[0])

    def test_scales_with_E_squared(self):
        """Doubling E quadruples power density."""
        E_x1, E_y1 = np.array([1e-8]), np.array([0.0])
        E_x2, E_y2 = np.array([2e-8]), np.array([0.0])
        p1 = calc_joule_heat_distribution(E_x1, E_y1)
        p2 = calc_joule_heat_distribution(E_x2, E_y2)
        assert np.isclose(p2[0], 4.0 * p1[0])

    def test_no_nan_inf(self):
        """Output contains no NaN or Inf."""
        E_x = np.linspace(-1e-8, 1e-8, 50)
        E_y = np.zeros(50)
        p = calc_joule_heat_distribution(E_x, E_y)
        assert not np.any(np.isnan(p))
        assert not np.any(np.isinf(p))


# ============================================================
# CalcThermalGradients -- 6 tests
# ============================================================
class TestCalcThermalGradients:
    """Test calc_thermal_gradients function."""

    def test_rectangular_parabolic_profile(self):
        """Rectangular geometry: T is parabolic, max at center."""
        x = np.linspace(-1.0, 1.0, 30)
        y = np.linspace(-0.5, 0.5, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_thermal_gradients(X, Y)
        T = result["T"]
        center_idx = (T.shape[0] // 2, T.shape[1] // 2)
        assert T[center_idx] == result["T_max"]

    def test_circular_geometry(self):
        """Circular geometry: temperature zero outside radius."""
        x = np.linspace(-2.0, 2.0, 30)
        y = np.linspace(-2.0, 2.0, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_thermal_gradients(X, Y, geometry="circular")
        r = np.sqrt(X**2 + Y**2)
        outside = r > 1.0
        dT_outside = result["dT"][outside]
        assert np.allclose(dT_outside, 0)

    def test_invalid_geometry_raises(self):
        """Raises ValueError for unknown geometry."""
        x = np.array([[0.0]])
        y = np.array([[0.0]])
        with pytest.raises(ValueError):
            calc_thermal_gradients(x, y, geometry="hexagonal")

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        x = np.linspace(-1, 1, 10)
        y = np.linspace(-0.5, 0.5, 10)
        X, Y = np.meshgrid(x, y)
        result = calc_thermal_gradients(X, Y)
        expected_keys = {"T", "T_max", "dT", "q_x", "q_y", "p"}
        assert set(result.keys()) == expected_keys

    def test_heat_flux_outward(self):
        """Heat flux points from hot center toward cool edges."""
        x = np.linspace(-1.5, 1.5, 30)
        y = np.linspace(-0.75, 0.75, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_thermal_gradients(X, Y, geometry="rectangular")
        right_mask = X > 1.0
        assert np.mean(result["q_x"][right_mask]) > 0

    def test_boundary_temperature(self):
        """Edge temperature equals T_boundary."""
        x = np.linspace(-1.5, 1.5, 30)
        y = np.linspace(-0.75, 0.75, 30)
        X, Y = np.meshgrid(x, y)
        T_boundary = 350.0
        result = calc_thermal_gradients(X, Y, T_boundary=T_boundary, geometry="rectangular")
        T_edges = np.concatenate([result["T"][0, :], result["T"][-1, :], result["T"][:, 0], result["T"][:, -1]])
        assert np.allclose(T_edges, T_boundary, atol=1e-6)


# ============================================================
# CalcPeltierJunction -- 5 tests
# ============================================================
class TestCalcPeltierJunction:
    """Test calc_peltier_junction function."""

    def test_emf_proportional_to_dT(self):
        """EMF scales linearly with temperature difference."""
        result1 = calc_peltier_junction(np.array([10.0]), "copper", "iron")
        result2 = calc_peltier_junction(np.array([20.0]), "copper", "iron")
        assert np.isclose(result2["EMF"][0], 2.0 * result1["EMF"][0])

    def test_material_pair_sign(self):
        """Swapping materials reverses EMF sign."""
        result_AB = calc_peltier_junction(np.array([50.0]), "copper", "iron")
        result_BA = calc_peltier_junction(np.array([50.0]), "iron", "copper")
        assert np.isclose(result_AB["EMF"][0], -result_BA["EMF"][0])

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        result = calc_peltier_junction(np.array([1.0]), "copper", "iron")
        expected_keys = {"EMF", "Pi_AB", "S_A", "S_B", "S_AB"}
        assert set(result.keys()) == expected_keys

    def test_unknown_material_raises(self):
        """Raises ValueError for unknown material."""
        with pytest.raises(ValueError):
            calc_peltier_junction(np.array([1.0]), "adamantium", "iron")

    def test_zero_dT_zero_EMF(self):
        """Zero temperature difference gives zero EMF."""
        result = calc_peltier_junction(np.array([0.0]), "copper", "iron")
        assert np.isclose(result["EMF"][0], 0.0)


# ============================================================
# PlotThermalGradients -- 5 tests
# ============================================================
class TestPlotThermalGradients:
    """Test plot_thermal_gradients function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_thermal_gradients()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_thermal_gradients(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_has_title_with_citation(self):
        """Title contains Art. 242 reference."""
        fig, ax = plot_thermal_gradients()
        assert "Art. 242" in ax.get_title()
        mplt.close(fig)

    def test_has_colorbar(self):
        """Figure has colorbar (multiple axes)."""
        fig, ax = plot_thermal_gradients()
        assert len(fig.get_axes()) >= 2
        mplt.close(fig)

    def test_circular_geometry(self):
        """Works with circular geometry."""
        fig, ax = plot_thermal_gradients(geometry="circular")
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotJouleHeatDistribution -- 3 tests
# ============================================================
class TestPlotJouleHeatDistribution:
    """Test plot_joule_heat_distribution function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_joule_heat_distribution()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_uniform_vs_nonuniform(self):
        """Both geometries produce valid plots."""
        fig1, _ = plot_joule_heat_distribution(geometry="uniform")
        fig2, _ = plot_joule_heat_distribution(geometry="nonuniform")
        assert fig1 is not None and fig2 is not None
        mplt.close(fig1)
        mplt.close(fig2)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_joule_heat_distribution(ax=ax)
        assert rax is ax
        mplt.close(fig)


# ============================================================
# PlotThermoelectricEffects -- 4 tests
# ============================================================
class TestPlotThermoelectricEffects:
    """Test plot_thermoelectric_effects function."""

    def test_returns_fig_axes(self):
        """Returns (Figure, list[Axes]) with 2 axes."""
        fig, axes = plot_thermoelectric_effects()
        assert fig is not None and len(axes) == 2
        mplt.close(fig)

    def test_seebeck_panel_has_legend(self):
        """Seebeck panel (ax1) has legend."""
        fig, axes = plot_thermoelectric_effects()
        assert axes[0].get_legend() is not None
        mplt.close(fig)

    def test_custom_material_pairs(self):
        """Works with custom material pairs."""
        fig, axes = plot_thermoelectric_effects(
            material_pairs=[("copper", "gold"), ("aluminum", "chromel")]
        )
        assert fig is not None
        mplt.close(fig)

    def test_with_existing_fig(self):
        """Accepts provided figure."""
        fig, _ = mplt.subplots(1, 2, figsize=(14, 5))
        rfig, raxes = plot_thermoelectric_effects(fig=fig)
        assert rfig is fig and len(raxes) == 2
        mplt.close(fig)
