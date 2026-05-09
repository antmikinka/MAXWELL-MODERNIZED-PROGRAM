"""Tests for maxwell.vis.molecular_vortices -- Molecular vortex visualization."""

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

from maxwell.vis.molecular_vortices import (
    calc_magnetic_field_from_vortices,
    calc_vortex_lattice,
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
        assert len(set(signs)) == 2  # Both +1 and -1 present

    def test_vorticity_at_centers(self):
        """Vorticity Peaks near vortex centers."""
        x = np.linspace(-2, 2, 50)
        y = np.linspace(-2, 2, 50)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        omega = result["omega"]
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
        r1 = calc_vortex_lattice(
            X, Y, vortex_centers=[(0, 0)], vortex_signs=[1], core_radius=0.1
        )
        r2 = calc_vortex_lattice(
            X, Y, vortex_centers=[(0, 0)], vortex_signs=[1], core_radius=0.5
        )
        assert r1["v_magnitude"].max() >= r2["v_magnitude"].max()

    def test_returns_all_keys(self):
        """Returns dictionary with all expected keys."""
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        result = calc_vortex_lattice(X, Y)
        expected_keys = {
            "v_x",
            "v_y",
            "v_magnitude",
            "omega",
            "vortex_centers",
            "vortex_signs",
        }
        assert set(result.keys()) == expected_keys

    def test_strength_scaling(self):
        """Velocity scales linearly with vortex strength."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        r1 = calc_vortex_lattice(X, Y, vortex_strength=1.0)
        r2 = calc_vortex_lattice(X, Y, vortex_strength=2.0)
        assert np.isclose(
            r2["v_magnitude"].max(), 2.0 * r1["v_magnitude"].max(), rtol=1e-3
        )


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
