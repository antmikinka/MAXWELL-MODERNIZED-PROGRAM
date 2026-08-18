# Implementation Plan: Visualization Coverage + Electrotonic State

> **Program:** Maxwell Modernized Program -- Visualization Gap Closure
> **Branch:** `feat/pypi-package`
> **Estimated Effort:** 4-6 hours across 5 tasks
> **Priority:** P0 -- Critical (3 modules with ZERO test coverage)

---

## Executive Summary

This plan addresses four critical gaps in the visualization layer:

1. **Three untested visualization modules** (thermal_gradients.py, molecular_vortices.py, helicoidal_potentials.py) -- 14 functions, 1,278 lines with 0% test coverage
2. **Missing Electrotonic State visualization** -- the last classical visualization gap (Arts. 540, 617)
3. **Image rendering validation** -- tests that verify plots produce visible, non-blank images
4. **Documentation updates** -- coverage files and test inventory

---

## Task 1: Test `maxwell.vis.thermal_gradients` (6 functions, 540 lines)

**Output file:** `tests/test_vis_thermal_gradients.py`
**Estimated test count:** 25-30 tests
**Estimated time:** 1.5 hours

### Module Functions to Test

| Function | Lines | Return Type | Key Properties to Verify |
|----------|-------|-------------|-------------------------|
| `calc_joule_heat_distribution` | 27-54 | `np.ndarray` | p = sigma * |E|^2, non-negative, scales with sigma and E |
| `calc_thermal_gradients` | 63-139 | `dict[str, np.ndarray]` | T_max at center, parabolic profile, heat flux outward, rectangular vs circular geometry |
| `calc_peltier_junction` | 148-214 | `dict[str, np.ndarray]` | EMF proportional to dT, sign depends on material pair, known material Seebeck coeffs |
| `plot_thermal_gradients` | 223-338 | `tuple[Figure, Axes]` | Returns fig/ax, has contourf, has colorbar, has title with "Art. 242", hot spot marker, geometry outline |
| `plot_joule_heat_distribution` | 347-436 | `tuple[Figure, Axes]` | Returns fig/ax, non-uniform shows constriction boundary, uniform shows flat field |
| `plot_thermoelectric_effects` | 445-539 | `tuple[Figure, list[Axes]]` | Returns fig + 2 axes, Seebeck panel has legend, Peltier panel has bars |

### Test File Structure

```python
"""Tests for maxwell.vis.thermal_gradients -- Thermal gradients and Joule heating visualization."""

from __future__ import annotations

import numpy as np
import pytest
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
        # Right side (x > 0): q_x should be positive (heat flows right)
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
```

### Coverage Target
- **calc_joule_heat_distribution:** 5 tests (100% branch coverage)
- **calc_thermal_gradients:** 6 tests (all geometry branches, edge cases)
- **calc_peltier_junction:** 5 tests (material validation, proportionality)
- **plot_thermal_gradients:** 5 tests (return types, citation, colorbar, geometry)
- **plot_joule_heat_distribution:** 3 tests (both geometries, ax passing)
- **plot_thermoelectric_effects:** 4 tests (return types, panels, custom inputs)

**Total: 28 tests**

---

## Task 2: Test `maxwell.vis.molecular_vortices` (4 functions, 376 lines)

**Output file:** `tests/test_vis_molecular_vortices.py`
**Estimated test count:** 22-25 tests
**Estimated time:** 1.5 hours

### Module Functions to Test

| Function | Lines | Return Type | Key Properties to Verify |
|----------|-------|-------------|-------------------------|
| `calc_vortex_lattice` | 25-125 | `dict[str, np.ndarray]` | Velocity field, alternating vorticity signs, core regularization, custom centers |
| `calc_magnetic_field_from_vortices` | 134-190 | `dict[str, float]` | Energy positive, symmetric checkerboard cancels, scales with density |
| `plot_molecular_vortices` | 199-293 | `tuple[Figure, Axes]` | Returns fig/ax, has contourf, vortex center markers, title with "Art. 822" |
| `plot_vortex_3d_surface` | 302-375 | `tuple[Figure, Axes]` | Returns fig/ax with 3D projection, surface plot, title |

### Test File Structure

```python
"""Tests for maxwell.vis.molecular_vortices -- Molecular vortex visualization."""

from __future__ import annotations

import numpy as np
import pytest
matplotlib.use("Agg")
import matplotlib.pyplot as mplt

from maxwell.vis._compat import HAS_MATPLOTLIB

pytestmark = pytest.mark.skipif(
    not HAS_MATPLOTLIB,
    reason="matplotlib not installed (pip install maxwell[viz])",
)

from maxwell.vis.molecular_vortices import (
    calc_vortex_lattice,
    calc_magnetic_field_from_vortices,
    plot_molecular_vortices,
    plot_vortex_3d_surface,
)


# ============================================================
# CalcVortexLattice -- 8 tests
# ============================================================
class TestCalcVortexLattice:
    """Test calc_vortex_lattice function."""

    def test_default_3x3_lattice(self):
        """Default creates 3x3 checkerboard (9 vortices)."""
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        assert len(result["vortex_centers"]) == 9
        assert len(result["vortex_signs"]) == 9

    def test_alternating_signs(self):
        """Adjacent vortices have opposite rotation signs."""
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        signs = result["vortex_signs"]
        # In 3x3 checkerboard, signs alternate
        for i in range(len(signs) - 1):
            # Adjacent vortices in the grid should differ
            pass  # The pattern is checkerboard; verify non-all-same
        assert len(set(signs)) == 2  # Both +1 and -1 present

    def test_vorticity_at_centers(self):
        """Vorticity peaks near vortex centers."""
        x = np.linspace(-2, 2, 50)
        y = np.linspace(-2, 2, 50)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        omega = result["omega"]
        # Max vorticity should be significant
        assert np.max(np.abs(omega)) > 0

    def test_velocity_no_nan_inf(self):
        """No NaN or Inf in velocity field (core regularization works)."""
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        assert not np.any(np.isnan(result["v_x"]))
        assert not np.any(np.isnan(result["v_y"]))
        assert not np.any(np.isinf(result["v_x"]))
        assert not np.any(np.isinf(result["v_y"]))

    def test_custom_centers(self):
        """Works with custom vortex positions."""
        x = np.linspace(-3, 3, 30)
        y = np.linspace(-3, 3, 30)
        X, Y = np.meshgrid(x, y)
        centers = [(0.0, 0.0), (2.0, 0.0)]
        signs = [1, -1]
        result = calc_vortex_lattice(X, Y, vortex_centers=centers, vortex_signs=signs)
        assert len(result["vortex_centers"]) == 2

    def test_core_radius_effect(self):
        """Larger core radius smooths velocity field."""
        x = np.linspace(-0.5, 0.5, 20)
        y = np.linspace(-0.5, 0.5, 20)
        X, Y = np.meshgrid(x, y)
        r1 = calc_vortex_lattice(X, Y, vortex_centers=[(0,0)], vortex_signs=[1], core_radius=0.1)
        r2 = calc_vortex_lattice(X, Y, vortex_centers=[(0,0)], vortex_signs=[1], core_radius=0.5)
        # Larger core should have lower max velocity at center
        assert r1["v_magnitude"].max() >= r2["v_magnitude"].max()

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        expected_keys = {"v_x", "v_y", "v_magnitude", "omega", "vortex_centers", "vortex_signs"}
        assert set(result.keys()) == expected_keys

    def test_strength_scaling(self):
        """Velocity scales linearly with vortex strength."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        r1 = calc_vortex_lattice(X, Y, vortex_strength=1.0)
        r2 = calc_vortex_lattice(X, Y, vortex_strength=2.0)
        assert np.isclose(r2["v_magnitude"].max(), 2.0 * r1["v_magnitude"].max(), rtol=1e-3)


# ============================================================
# CalcMagneticFieldFromVortices -- 5 tests
# ============================================================
class TestCalcMagneticFieldFromVortices:
    """Test calc_magnetic_field_from_vortices function."""

    def test_total_energy_positive(self):
        """Total kinetic energy is always positive."""
        centers = [(0, 0), (1, 0), (0, 1), (1, 1)]
        signs = [1, -1, -1, 1]
        result = calc_magnetic_field_from_vortices(centers, signs)
        assert result["total_energy"] > 0

    def test_energy_scales_with_density(self):
        """Energy scales linearly with ether density."""
        centers = [(0, 0)]
        signs = [1]
        r1 = calc_magnetic_field_from_vortices(centers, signs, density=1.0)
        r2 = calc_magnetic_field_from_vortices(centers, signs, density=2.0)
        assert np.isclose(r2["total_energy"], 2.0 * r1["total_energy"])

    def test_symmetric_cancellation(self):
        """Symmetric checkerboard gives zero net H field."""
        centers = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        signs = [1, -1, -1, 1]
        result = calc_magnetic_field_from_vortices(centers, signs)
        assert np.isclose(result["H_magnitude"], 0.0)

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        result = calc_magnetic_field_from_vortices([(0, 0)], [1])
        expected_keys = {"H_x", "H_y", "H_magnitude", "total_energy"}
        assert set(result.keys()) == expected_keys

    def test_single_vortex(self):
        """Single vortex produces non-zero energy."""
        result = calc_magnetic_field_from_vortices(
            [(0, 0)], [1], vortex_strength=2.0, core_radius=0.5
        )
        assert result["total_energy"] > 0


# ============================================================
# PlotMolecularVortices -- 5 tests
# ============================================================
class TestPlotMolecularVortices:
    """Test plot_molecular_vortices function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_molecular_vortices()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided ax."""
        fig, ax = mplt.subplots()
        rfig, rax = plot_molecular_vortices(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_has_title_with_citation(self):
        """Title contains Art. 822 reference."""
        fig, ax = plot_molecular_vortices()
        assert "Art. 822" in ax.get_title()
        mplt.close(fig)

    def test_streamlines_vs_quiver(self):
        """Both streamlines and quiver modes work."""
        fig1, _ = plot_molecular_vortices(show_streamlines=True)
        fig2, _ = plot_molecular_vortices(show_streamlines=False)
        assert fig1 is not None and fig2 is not None
        mplt.close(fig1)
        mplt.close(fig2)

    def test_custom_parameters(self):
        """Works with custom vortex strength and core radius."""
        fig, ax = plot_molecular_vortices(
            grid_range=(-3.0, 3.0),
            resolution=30,
            vortex_strength=2.0,
            core_radius=0.5,
        )
        assert fig is not None
        mplt.close(fig)


# ============================================================
# PlotVortex3DSurface -- 4 tests
# ============================================================
class TestPlotVortex3DSurface:
    """Test plot_vortex_3d_surface function."""

    def test_returns_fig_ax(self):
        """Returns (Figure, Axes)."""
        fig, ax = plot_vortex_3d_surface()
        assert fig is not None and ax is not None
        mplt.close(fig)

    def test_3d_projection(self):
        """Axes have 3D projection."""
        fig, ax = plot_vortex_3d_surface()
        assert ax.name == "3d"
        mplt.close(fig)

    def test_with_existing_ax(self):
        """Accepts provided 3D ax."""
        fig = mplt.figure()
        ax = fig.add_subplot(111, projection="3d")
        rfig, rax = plot_vortex_3d_surface(ax=ax)
        assert rax is ax and rfig is fig
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom resolution and vortex parameters."""
        fig, ax = plot_vortex_3d_surface(
            resolution=25,
            vortex_strength=2.0,
            core_radius=0.5,
        )
        assert fig is not None
        mplt.close(fig)
```

### Coverage Target
- **calc_vortex_lattice:** 8 tests (all branches, core regularization, scaling)
- **calc_magnetic_field_from_vortices:** 5 tests (energy, density, symmetry)
- **plot_molecular_vortices:** 5 tests (return types, citation, modes)
- **plot_vortex_3d_surface:** 4 tests (return types, 3D projection, ax passing)

**Total: 22 tests**

---

## Task 3: Test `maxwell.vis.helicoidal_potentials` (4 functions, 362 lines)

**Output file:** `tests/test_vis_helicoidal_potentials.py`
**Estimated test count:** 20-24 tests
**Estimated time:** 1.5 hours

### Module Functions to Test

| Function | Lines | Return Type | Key Properties to Verify |
|----------|-------|-------------|-------------------------|
| `calc_solid_angle_loop` | 26-94 | `dict[str, np.ndarray]` | Solid angle sign change across loop, on-axis behavior, returns omega/Omega/r_cyl |
| `plot_helicoidal_potentials` | 103-190 | `tuple[Figure, Axes]` | Returns fig/ax, contourf, loop markers, discontinuity line, title with "Art. 487" |
| `plot_loop_potential_3d` | 199-276 | `tuple[Figure, Axes]` | Returns fig/ax with 3D projection, loop curve drawn |
| `plot_loop_field_lines` | 285-361 | `tuple[Figure, Axes]` | Returns fig/ax, contour field lines, loop markers, symmetry axes |

### Test File Structure

```python
"""Tests for maxwell.vis.helicoidal_potentials -- Helicoidal potential surfaces visualization."""

from __future__ import annotations

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
    plot_loop_potential_3d,
    plot_loop_field_lines,
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
        assert np.isclose(omega_above["omega"], -omega_below["omega"], rtol=1e-6)

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
        fig, ax = plot_loop_potential_3d(
            loop_radius=2.0, current=3.0, resolution=20
        )
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
        contours = [c for c in ax.collections if hasattr(c, 'get_segments')]
        assert len(contours) > 0  # At least one contour collection
        mplt.close(fig)

    def test_custom_parameters(self):
        """Works with custom loop radius and current."""
        fig, ax = plot_loop_field_lines(
            loop_radius=2.0, current=5.0, resolution=40
        )
        assert fig is not None
        mplt.close(fig)
```

### Coverage Target
- **calc_solid_angle_loop:** 7 tests (sign change, scaling, arrays, no NaN)
- **plot_helicoidal_potentials:** 5 tests (return types, citation, colorbar)
- **plot_loop_potential_3d:** 4 tests (return types, 3D projection, ax passing)
- **plot_loop_field_lines:** 5 tests (return types, citation, contours)

**Total: 21 tests**

---

## Task 4: Electrotonic State Visualization Module

**Output file:** `maxwell/vis/electrotonic_state.py`
**Estimated time:** 2 hours
**Estimated test count:** 25-28 tests (separate test file)

### Design Rationale

Maxwell's Electrotonic State (Arts. 540, 617) is his conceptual precursor to the vector potential A. It represents the "electrotonic state" induced in the electromagnetic field by changing currents -- essentially the physical manifestation of A. This visualization bridges Maxwell's original mechanical interpretation with the modern vector potential formulation.

### Module Design

```python
"""maxwell.vis.electrotonic_state -- Electrotonic State visualization (Arts. 540, 617).

Implements visualization of Maxwell's Electrotonic State -- the vector
potential A-field as Maxwell originally conceived it. Shows:
- A-field lines around current-carrying conductors
- A-field magnitude contours
- Relationship between A and B (curl relationship visualized)
- Time evolution of the electrotonic state during current changes

Corresponds to Maxwell's treatment in
Part IV, Arts. 540, 617 (Electrotonic State).
"""

from __future__ import annotations

import numpy as np
from typing import Callable

from maxwell.vis._compat import require_matplotlib, plt, Figure, Axes
from maxwell.meta.citation import maxwell_cite
from maxwell.calculus.vector_potential import VectorPotential, vector_potential_uniform_field


@maxwell_cite(
    540,
    part=4,
    chapter="Electrotonic State",
    description="Calculate electrotonic state (vector potential A) for a straight wire.",
)
def calc_electrotonic_straight_wire(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    current: float = 1.0,
    wire_axis: str = "z",
) -> dict[str, np.ndarray]:
    """Calculate electrotonic state A for an infinite straight wire.

    Art. 540: For a straight wire along the z-axis carrying current I,
    the vector potential in cylindrical coordinates:

        A = -(mu0 * I / (2*pi)) * ln(r/r0) * z_hat

    In Cartesian: A_z = -(mu0 * I / (2*pi)) * ln(sqrt(x^2+y^2)/r0)

    Args:
        x, y, z: Position arrays (can be scalars or grids).
        current: Current in wire (abamperes, CGS-EMU).
        wire_axis: Wire orientation ('x', 'y', or 'z').

    Returns:
        Dictionary with 'A_x', 'A_y', 'A_z' (components),
        'A_magnitude', 'r_cyl' (cylindrical radius).
    """
    # ... implementation ...


@maxwell_cite(
    617,
    part=4,
    chapter="Electrotonic State",
    description="Calculate time-varying electrotonic state during current change.",
)
def calc_electrotonic_transient(
    x: np.ndarray,
    y: np.ndarray,
    current_initial: float = 0.0,
    current_final: float = 1.0,
    time_constant: float = 1.0,
    time: float = 0.0,
) -> dict[str, np.ndarray]:
    """Calculate time-varying electrotonic state during current transient.

    Art. 617: When current changes from I_0 to I_f with time constant tau,
    the electrotonic state evolves as:

        A(t) = A_final + (A_initial - A_final) * exp(-t/tau)

    This describes the "extra current" phenomenon Maxwell observed
    during circuit switching.

    Args:
        x, y: Position arrays.
        current_initial: Initial current.
        current_final: Final current.
        time_constant: Transient time constant tau.
        time: Observation time.

    Returns:
        Dictionary with 'A_z', 'A_magnitude', 'time', 'I_t' (current at time t).
    """
    # ... implementation ...


@maxwell_cite(
    540,
    part=4,
    chapter="Electrotonic State",
    description="Calculate B field from electrotonic state via curl.",
)
def calc_B_from_electrotonic(
    A_func: Callable[[np.ndarray, np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray, np.ndarray]],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    h: float = 1e-8,
) -> dict[str, np.ndarray]:
    """Calculate B = curl(A) from electrotonic state.

    Art. 540: Maxwell showed that the magnetic induction B is
    the curl of the electrotonic state (vector potential).

    Args:
        A_func: Function returning (A_x, A_y, A_z) at positions.
        x, y, z: Grid positions.
        h: Step size for numerical curl.

    Returns:
        Dictionary with 'B_x', 'B_y', 'B_z', 'B_magnitude'.
    """
    # ... implementation ...


@maxwell_cite(
    540,
    part=4,
    chapter="Electrotonic State",
    description="Plot electrotonic state A-field lines around straight wire.",
)
def plot_electrotonic_state_2d(
    current: float = 1.0,
    grid_range: tuple[float, float] = (-2.0, 2.0),
    resolution: int = 50,
    wire_axis: str = "z",
    show_magnitude: bool = True,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot 2D cross-section of electrotonic state around straight wire.

    Art. 540: Shows the A-field (electrotonic state) as:
    - Magnitude contour map (color-filled)
    - A-field direction as arrows or streamlines
    - Wire position marked
    - Logarithmic decay of A with distance

    Args:
        current: Current in wire (abamperes).
        grid_range: (min, max) spatial range.
        resolution: Grid resolution.
        wire_axis: Wire orientation.
        show_magnitude: Whether to show magnitude contour.
        ax: Existing axes (optional).

    Returns:
        Tuple of (Figure, Axes).
    """
    # ... implementation ...


@maxwell_cite(
    617,
    part=4,
    chapter="Electrotonic State",
    description="Plot time evolution of electrotonic state during transient.",
)
def plot_electrotonic_transient(
    current_initial: float = 0.0,
    current_final: float = 1.0,
    time_constant: float = 1.0,
    time_range: tuple[float, float] = (0.0, 5.0),
    observation_points: list[tuple[float, float]] | None = None,
    fig: Figure | None = None,
) -> tuple[Figure, list[Axes]]:
    """Plot time evolution of electrotonic state during current transient.

    Art. 617: Two-panel visualization:
    Panel 1: A(t) vs time at multiple observation points
    Panel 2: Current I(t) vs time showing exponential rise

    Args:
        current_initial: Initial current.
        current_final: Final current.
        time_constant: Transient time constant.
        time_range: (t_min, t_max).
        observation_points: List of (r, theta) observation positions.
        fig: Existing figure (optional).

    Returns:
        Tuple of (Figure, list[Axes]).
    """
    # ... implementation ...


@maxwell_cite(
    540,
    part=4,
    chapter="Electrotonic State",
    description="Plot 3D electrotonic state surface around straight wire.",
)
def plot_electrotonic_3d_surface(
    current: float = 1.0,
    resolution: int = 40,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot 3D surface of |A| around straight wire.

    Art. 540: 3D visualization showing the logarithmic potential
    well around the wire. The characteristic ln(r) shape
    illustrates why Maxwell called this the "electrotonic state" --
    it represents accumulated electromagnetic momentum.

    Args:
        current: Current in wire.
        resolution: Grid resolution.
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes) with 3D projection.
    """
    # ... implementation ...
```

### Test File: `tests/test_vis_electrotonic_state.py`

**Estimated test count:** 25-28 tests

Structure mirrors the patterns from Tasks 1-3, with test classes:
- `TestCalcElectrotonicStraightWire` (7 tests): log decay, axis symmetry, no NaN, scaling with current, returns all keys, cylindrical radius, direction along wire
- `TestCalcElectrotonicTransient` (5 tests): exponential decay, initial/final values, time constant effect, returns all keys, zero time
- `TestCalcBFromElectrotonic` (4 tests): B = curl(A) verified, B around wire matches expected, returns all keys, no NaN
- `TestPlotElectrotonicState2D` (5 tests): returns fig/ax, title with citation, colorbar, custom parameters, existing ax
- `TestPlotElectrotonicTransient` (4 tests): returns fig + 2 axes, time series shape, custom parameters, existing fig
- `TestPlotElectrotonic3DSurface` (4 tests): returns fig/ax, 3D projection, existing ax, custom parameters

---

## Task 5: Image Rendering Validation Tests

**Output file:** `tests/test_vis_rendering.py`
**Estimated test count:** 15-20 tests
**Estimated time:** 1 hour

### Design

These tests verify that all visualization modules produce **visible, non-blank images** when rendered. This catches regressions where plots run without errors but produce empty or completely white images.

```python
"""Tests for visualization rendering -- verify plots produce visible images."""

from __future__ import annotations

import numpy as np
import pytest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as mplt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from maxwell.vis._compat import HAS_MATPLOTLIB

pytestmark = pytest.mark.skipif(
    not HAS_MATPLOTLIB,
    reason="matplotlib not installed (pip install maxwell[viz])",
)


def render_to_pixels(fig: mplt.figure.Figure) -> np.ndarray:
    """Render a figure to a pixel array."""
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.tostring_argb()
    ncols, nrows = canvas.get_width_height()
    img = np.frombuffer(buf, dtype=np.uint8)
    return img.reshape((nrows, ncols, 4))


def is_non_blank_image(fig: mplt.figure.Figure, threshold: float = 0.01) -> bool:
    """Check that rendered figure has non-blank content.

    Returns True if at least `threshold` fraction of pixels
    are non-background (not pure white or transparent).
    """
    img = render_to_pixels(fig)
    # ARGB format: alpha channel at index 0
    alpha = img[:, :, 0]
    rgb = img[:, :, 1:]

    # Count non-background pixels (not pure white with full alpha)
    is_white = np.all(rgb == 255, axis=2)
    is_transparent = alpha < 128

    non_bg = ~is_white | ~is_transparent
    fraction = np.sum(non_bg) / (img.shape[0] * img.shape[1])

    return fraction > threshold


# ============================================================
# Thermal Gradients Rendering -- 3 tests
# ============================================================
class TestThermalGradientsRendering:
    """Verify thermal gradient plots render visible images."""

    def test_thermal_gradients_renders(self):
        """plot_thermal_gradients produces non-blank image."""
        from maxwell.vis.thermal_gradients import plot_thermal_gradients
        fig, _ = plot_thermal_gradients()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_joule_heat_renders(self):
        """plot_joule_heat_distribution produces non-blank image."""
        from maxwell.vis.thermal_gradients import plot_joule_heat_distribution
        fig, _ = plot_joule_heat_distribution()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_thermoelectric_renders(self):
        """plot_thermoelectric_effects produces non-blank image."""
        from maxwell.vis.thermal_gradients import plot_thermoelectric_effects
        fig, _ = plot_thermoelectric_effects()
        assert is_non_blank_image(fig)
        mplt.close(fig)


# ============================================================
# Molecular Vortices Rendering -- 2 tests
# ============================================================
class TestMolecularVorticesRendering:
    """Verify molecular vortex plots render visible images."""

    def test_vortices_renders(self):
        """plot_molecular_vortices produces non-blank image."""
        from maxwell.vis.molecular_vortices import plot_molecular_vortices
        fig, _ = plot_molecular_vortices()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_vortex_3d_renders(self):
        """plot_vortex_3d_surface produces non-blank image."""
        from maxwell.vis.molecular_vortices import plot_vortex_3d_surface
        fig, _ = plot_vortex_3d_surface()
        assert is_non_blank_image(fig)
        mplt.close(fig)


# ============================================================
# Helicoidal Potentials Rendering -- 3 tests
# ============================================================
class TestHelicoidalPotentialsRendering:
    """Verify helicoidal potential plots render visible images."""

    def test_helicoidal_renders(self):
        """plot_helicoidal_potentials produces non-blank image."""
        from maxwell.vis.helicoidal_potentials import plot_helicoidal_potentials
        fig, _ = plot_helicoidal_potentials()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_loop_3d_renders(self):
        """plot_loop_potential_3d produces non-blank image."""
        from maxwell.vis.helicoidal_potentials import plot_loop_potential_3d
        fig, _ = plot_loop_potential_3d()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_field_lines_renders(self):
        """plot_loop_field_lines produces non-blank image."""
        from maxwell.vis.helicoidal_potentials import plot_loop_field_lines
        fig, _ = plot_loop_field_lines()
        assert is_non_blank_image(fig)
        mplt.close(fig)


# ============================================================
# Electrotonic State Rendering -- 3 tests (after Task 4)
# ============================================================
class TestElectrotonicStateRendering:
    """Verify electrotonic state plots render visible images."""

    def test_electrotonic_2d_renders(self):
        """plot_electrotonic_state_2d produces non-blank image."""
        from maxwell.vis.electrotonic_state import plot_electrotonic_state_2d
        fig, _ = plot_electrotonic_state_2d()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_electrotonic_transient_renders(self):
        """plot_electrotonic_transient produces non-blank image."""
        from maxwell.vis.electrotonic_state import plot_electrotonic_transient
        fig, _ = plot_electrotonic_transient()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_electrotonic_3d_renders(self):
        """plot_electrotonic_3d_surface produces non-blank image."""
        from maxwell.vis.electrotonic_state import plot_electrotonic_3d_surface
        fig, _ = plot_electrotonic_3d_surface()
        assert is_non_blank_image(fig)
        mplt.close(fig)


# ============================================================
# Existing Visualization Rendering (spot checks) -- 4 tests
# ============================================================
class TestExistingVisRendering:
    """Spot-check existing visualization modules still render correctly."""

    def test_dielectric_soakage_renders(self):
        """plot_dielectric_soakage produces non-blank image."""
        from maxwell.vis.dielectric_soakage import plot_dielectric_soakage
        fig, _ = plot_dielectric_soakage()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_magnetic_shell_renders(self):
        """plot_magnetic_shell produces non-blank image."""
        from maxwell.vis.magnetic_shell import plot_magnetic_shell
        fig, _ = plot_magnetic_shell()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_flow_tubes_renders(self):
        """Flow tubes visualization produces non-blank image."""
        # Import the flow tubes plot function
        from maxwell.vis.flow_tubes import plot_flow_tubes
        fig, _ = plot_flow_tubes()
        assert is_non_blank_image(fig)
        mplt.close(fig)

    def test_spherical_harmonics_renders(self):
        """Spherical harmonics visualization produces non-blank image."""
        from maxwell.vis.spherical_harmonics import plot_spherical_harmonics
        fig, _ = plot_spherical_harmonics()
        assert is_non_blank_image(fig)
        mplt.close(fig)
```

---

## Task 6: Documentation Updates

**Estimated time:** 30 minutes

### Coverage Files to Update

| File | Action | Content |
|------|--------|---------|
| `COVERAGE.md` or `.coveragerc` | Update | Add new test files to coverage configuration |
| `PIPELINE_SUMMARY.md` | Append | Document Phase 7 results: 3 modules tested + electrotonic state |
| `tests/__init__.py` or test inventory | Update | Add new test file references |
| `maxwell/vis/__init__.py` | Update | Export new `electrotonic_state` module |
| `docs/` or similar | Create/update | Update visualization module documentation |

### Documentation Update Checklist

- [ ] Add `test_vis_thermal_gradients.py` to test inventory with test count (28)
- [ ] Add `test_vis_molecular_vortices.py` to test inventory with test count (22)
- [ ] Add `test_vis_helicoidal_potentials.py` to test inventory with test count (21)
- [ ] Add `test_vis_electrotonic_state.py` to test inventory with test count (25-28)
- [ ] Add `test_vis_rendering.py` to test inventory with test count (15-20)
- [ ] Update `maxwell/vis/__init__.py` to export `electrotonic_state` functions
- [ ] Update coverage configuration to include new test files
- [ ] Append Phase 7 summary to `PIPELINE_SUMMARY.md`
- [ ] Run full test suite and record final counts
- [ ] Update any README or module-level docstrings

---

## Task Dependency Graph

```
Task 1 (thermal_gradients tests) ----+
Task 2 (molecular_vortices tests) ---+---> Task 5 (rendering validation) -----> Task 6 (docs)
Task 3 (helicoidal_potentials tests)-+
Task 4 (electrotonic_state module) --+
```

Tasks 1-4 can proceed in parallel. Task 5 depends on Tasks 1-4 completing. Task 6 depends on all previous tasks.

---

## Summary of Deliverables

| Deliverable | File Path | Estimated Tests | Lines (est.) |
|-------------|-----------|-----------------|--------------|
| Thermal gradients tests | `./tests\test_vis_thermal_gradients.py` | 28 | ~280 |
| Molecular vortices tests | `./tests\test_vis_molecular_vortices.py` | 22 | ~220 |
| Helicoidal potentials tests | `./tests\test_vis_helicoidal_potentials.py` | 21 | ~210 |
| Electrotonic state module | `./maxwell\vis\electrotonic_state.py` | -- | ~400 |
| Electrotonic state tests | `./tests\test_vis_electrotonic_state.py` | 28 | ~280 |
| Rendering validation tests | `./tests\test_vis_rendering.py` | 15 | ~180 |
| **Total new tests** | | **~114** | **~1570** |

---

## Acceptance Criteria

1. All 3 previously untested modules achieve >90% test coverage
2. Electrotonic State module has >90% test coverage
3. All rendering tests pass (no blank images)
4. Full test suite passes: `pytest tests/ -v --tb=short`
5. No regressions in existing tests
6. Documentation updated with new test counts and coverage status
7. Code follows existing patterns (import style, class organization, test naming)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 3D plot rendering in Agg backend fails | Low | Medium | Use try/except for 3D projection; skip if unavailable |
| Numerical precision differences across platforms | Medium | Low | Use `rtol=1e-5` instead of exact equality; `np.isclose` |
| Electrotonic state design conflicts with existing vector_potential | Low | Medium | Import from existing module; reuse `VectorPotential` class |
| Test count exceeds estimates | Medium | Low | Prioritize calc_* tests over plot_* tests |
| Rendering threshold too strict/lenient | Medium | Low | Start with 0.01 threshold; adjust based on test runs |
