"""Tests for maxwell.vis visualization package."""

from __future__ import annotations

import os
import tempfile

import numpy as np
import pytest

from maxwell.vis._compat import HAS_MATPLOTLIB, plt

# Conditional Pillow import for rendering validation
HAS_PILLOW = True
try:
    from PIL import Image
except ImportError:
    HAS_PILLOW = False

render_skip = pytest.mark.skipif(not HAS_PILLOW, reason="Pillow not installed")

# Skip all tests if matplotlib is not installed
pytestmark = pytest.mark.skipif(
    not HAS_MATPLOTLIB,
    reason="matplotlib not installed (pip install maxwell[viz])",
)


class TestCompat:
    """Test _compat module graceful degradation."""

    def test_has_matplotlib(self):
        assert HAS_MATPLOTLIB is True

    def test_plt_is_not_none(self):
        assert plt is not None

    def test_require_matplotlib_no_raise(self):
        from maxwell.vis._compat import require_matplotlib

        require_matplotlib()  # Should not raise

    def test_get_default_colormap(self):
        from maxwell.vis._compat import get_default_colormap

        cmap = get_default_colormap("viridis")
        assert cmap is not None

    def test_create_figure(self):
        from maxwell.vis._compat import create_figure

        fig, ax = create_figure(figsize=(8, 6), dpi=80)
        assert fig is not None
        assert ax is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)


class TestBase:
    """Test _base grid utilities."""

    def test_create_meshgrid_shape(self):
        from maxwell.vis._base import create_meshgrid

        X, Y = create_meshgrid(-5, 5, -3, 3, 20, 15)
        assert X.shape == (15, 20)
        assert Y.shape == (15, 20)

    def test_create_meshgrid_bounds(self):
        from maxwell.vis._base import create_meshgrid

        X, Y = create_meshgrid(-1, 1, 0, 2, 5, 5)
        assert np.isclose(X[0, 0], -1)
        assert np.isclose(X[0, -1], 1)
        assert np.isclose(Y[0, 0], 0)
        assert np.isclose(Y[-1, 0], 2)

    def test_evaluate_on_grid_vector(self):
        from maxwell.vis._base import create_meshgrid, evaluate_on_grid

        def vec_field(x, y):
            return np.stack([x, y], axis=-1)

        X, Y = create_meshgrid(-1, 1, -1, 1, 5, 5)
        result = evaluate_on_grid(vec_field, X, Y, component=0)
        assert result.shape == (5, 5)
        assert np.allclose(result, X)

    def test_evaluate_on_grid_scalar(self):
        from maxwell.vis._base import create_meshgrid, evaluate_on_grid

        def scalar_field(x, y):
            return x**2 + y**2

        X, Y = create_meshgrid(-1, 1, -1, 1, 5, 5)
        result = evaluate_on_grid(scalar_field, X, Y)
        assert result.shape == (5, 5)
        assert np.allclose(result, X**2 + Y**2)

    def test_format_axis_labels(self):
        import matplotlib.pyplot as mplt

        from maxwell.vis._base import format_axis_labels

        fig, ax = mplt.subplots()
        format_axis_labels(ax, xlabel="X", ylabel="Y", title="Test")
        assert ax.get_xlabel() == "X"
        assert ax.get_ylabel() == "Y"
        assert ax.get_title() == "Test"
        mplt.close(fig)


class TestFieldLines:
    """Test field line plotting."""

    def test_plot_field_lines_returns_figure(self):
        from maxwell.vis.field_lines import plot_field_lines_2d

        def field(x, y):
            return x, y

        fig = plot_field_lines_2d(field, nx=10, ny=10)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_plot_dipole_field_lines(self):
        from maxwell.vis.field_lines import plot_dipole_field_lines

        fig = plot_dipole_field_lines(nx=10, ny=10)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_field_lines_with_charges(self):
        from maxwell.vis.field_lines import plot_field_lines_2d

        def field(x, y):
            return np.ones_like(x), np.zeros_like(x)

        fig = plot_field_lines_2d(
            field,
            nx=10,
            ny=10,
            charge_positions=[(0, 0)],
            charge_signs=[1],
        )
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)


class TestEquipotentials:
    """Test equipotential contour plotting."""

    def test_plot_equipotentials_returns_figure(self):
        from maxwell.vis.equipotential import plot_equipotentials_2d

        def potential(x, y):
            return 1.0 / np.sqrt(x**2 + y**2 + 0.01)

        fig = plot_equipotentials_2d(potential, nx=20, ny=20)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_plot_equipotentials_filled_false(self):
        from maxwell.vis.equipotential import plot_equipotentials_2d

        def potential(x, y):
            return x**2 + y**2

        fig = plot_equipotentials_2d(potential, filled=False, nx=20, ny=20)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_plot_dipole_equipotentials(self):
        from maxwell.vis.equipotential import plot_dipole_equipotentials

        fig = plot_dipole_equipotentials(nx=20, ny=20)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_equipotentials_with_explicit_levels(self):
        from maxwell.vis.equipotential import plot_equipotentials_2d

        def potential(x, y):
            return x**2 + y**2

        levels = np.array([0.5, 1.0, 2.0, 4.0])
        fig = plot_equipotentials_2d(potential, levels=levels, nx=20, ny=20)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)


class TestStressTensor:
    """Test Maxwell stress tensor visualization."""

    def test_plot_stress_tensor_returns_figure(self):
        from maxwell.vis.stress import plot_stress_tensor_2d

        def field(x, y):
            return np.ones_like(x) * 1.0, np.zeros_like(x)

        fig = plot_stress_tensor_2d(field, nx=10, ny=10)
        assert fig is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_verify_stress_tensor_symmetric(self):
        from maxwell.vis.stress import verify_stress_tensor_plot

        result = verify_stress_tensor_plot(
            E_field=(1.0, 0.0, 0.0),
            B_field=(0.0, 0.0, 0.0),
        )
        assert result["symmetric"] is True
        assert result["trace_error"] < 1e-10

    def test_verify_stress_tensor_with_both_fields(self):
        from maxwell.vis.stress import verify_stress_tensor_plot

        result = verify_stress_tensor_plot(
            E_field=(1.0, 2.0, 0.0),
            B_field=(0.0, 1.0, 3.0),
        )
        assert result["symmetric"] is True
        assert result["all_real_eigenvalues"]  # numpy bool, not Python bool
        assert result["trace_error"] < 1e-10

    def test_verify_stress_tensor_energy_density(self):
        import numpy as np

        from maxwell.vis.stress import verify_stress_tensor_plot

        E_mag = 3.0
        result = verify_stress_tensor_plot(
            E_field=(E_mag, 0.0, 0.0),
            B_field=(0.0, 0.0, 0.0),
        )
        expected_u = E_mag**2 / (8.0 * np.pi)
        assert np.isclose(result["energy_density"], expected_u, rtol=1e-10)


class TestVisIntegration:
    """Test vis package integration with maxwell core classes."""

    def test_vis_import_from_package(self):
        from maxwell import vis

        assert hasattr(vis, "HAS_MATPLOTLIB")
        assert vis.HAS_MATPLOTLIB is True

    def test_vis_all_exports(self):
        from maxwell.vis import (
            calc_edge_singularity,
            calc_method_of_images,
            calc_wedge_field,
            create_meshgrid,
            evaluate_on_grid,
            plot_dipole_equipotentials,
            plot_dipole_field_lines,
            plot_edge_singularity,
            plot_equipotentials_2d,
            plot_field_lines_2d,
            plot_method_of_images,
            plot_singularity_comparison,
            plot_stress_tensor_2d,
            verify_stress_tensor_plot,
        )

        assert callable(create_meshgrid)
        assert callable(evaluate_on_grid)
        assert callable(plot_field_lines_2d)
        assert callable(plot_dipole_field_lines)
        assert callable(plot_equipotentials_2d)
        assert callable(plot_dipole_equipotentials)
        assert callable(plot_stress_tensor_2d)
        assert callable(verify_stress_tensor_plot)
        assert callable(calc_method_of_images)
        assert callable(plot_method_of_images)
        assert callable(calc_wedge_field)
        assert callable(calc_edge_singularity)
        assert callable(plot_edge_singularity)
        assert callable(plot_singularity_comparison)


class TestMethodOfImages:
    """Test Method of Images visualization (Art. 155)."""

    def test_method_of_images_potential_zero_on_plane(self):
        """V=0 at x=0 (conducting plane symmetry)."""
        from maxwell.vis._base import create_meshgrid
        from maxwell.vis.method_of_images import calc_method_of_images

        # Use odd number of points so x=0 is exactly in the grid
        X, Y = create_meshgrid(-2, 2, -2, 2, 41, 41)
        V, Ex, Ey = calc_method_of_images(q=1.0, d=1.0, x_grid=X, y_grid=Y)

        # Find the column at x=0
        x_zero_col = np.argmin(np.abs(X[0, :]))
        assert np.abs(X[0, x_zero_col]) < 1e-10
        v_at_plane = V[:, x_zero_col]
        assert np.allclose(v_at_plane, 0.0, atol=1e-6)

    def test_method_of_images_field_symmetry(self):
        """Ex is symmetric and Ey is symmetric about x=0 for charge+image pair."""
        from maxwell.vis._base import create_meshgrid
        from maxwell.vis.method_of_images import calc_method_of_images

        # Use odd number of points so x=0 is exactly centered
        X, Y = create_meshgrid(-2, 2, -2, 2, 41, 41)
        V, Ex, Ey = calc_method_of_images(q=1.0, d=1.0, x_grid=X, y_grid=Y)

        # For points symmetric about x=0 (columns equidistant from center)
        mid = X.shape[1] // 2  # This is column 20, x=0
        offset = 5  # 5 columns away from center

        left_col = mid - offset
        right_col = mid + offset

        # Verify x positions are symmetric
        assert np.isclose(X[0, left_col], -X[0, right_col])

        # Ex is symmetric: Ex(-x) = Ex(+x) for the charge+image configuration
        # (The +q/-q arrangement means field points same direction on both sides)
        assert np.allclose(Ex[:, left_col], Ex[:, right_col], atol=1e-6)

        # Ey is antisymmetric: Ey(-x) = -Ey(+x)
        # (y-component flips sign when reflected about x=0 due to charge asymmetry)
        assert np.allclose(Ey[:, left_col], -Ey[:, right_col], atol=1e-6)

        # V is antisymmetric: V(-x) = -V(+x)
        assert np.allclose(V[:, left_col], -V[:, right_col], atol=1e-6)

    def test_method_of_images_plot_returns_fig_ax(self):
        """plot_method_of_images returns matplotlib figure and axis."""
        from maxwell.vis.method_of_images import plot_method_of_images

        fig, ax = plot_method_of_images(q=1.0, d=1.0, resolution=30)
        assert fig is not None
        assert ax is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_method_of_images_default_args(self):
        """Works with no arguments (all defaults)."""
        from maxwell.vis.method_of_images import plot_method_of_images

        fig, ax = plot_method_of_images()
        assert fig is not None
        assert ax is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_method_of_images_calc_returns_arrays(self):
        """calc_method_of_images returns correctly shaped arrays."""
        from maxwell.vis._base import create_meshgrid
        from maxwell.vis.method_of_images import calc_method_of_images

        X, Y = create_meshgrid(-3, 3, -3, 3, 40, 40)
        V, Ex, Ey = calc_method_of_images(q=2.0, d=0.5, x_grid=X, y_grid=Y)

        assert V.shape == (40, 40)
        assert Ex.shape == (40, 40)
        assert Ey.shape == (40, 40)
        assert not np.any(np.isnan(V))
        assert not np.any(np.isnan(Ex))
        assert not np.any(np.isnan(Ey))

    def test_method_of_images_with_existing_ax(self):
        """Plots onto an existing axes."""
        import matplotlib.pyplot as mplt

        from maxwell.vis.method_of_images import plot_method_of_images

        fig, ax = mplt.subplots()
        result_fig, result_ax = plot_method_of_images(ax=ax, resolution=20)
        assert result_ax is ax
        assert result_fig is fig
        mplt.close(fig)


class TestEdgeSingularities:
    """Test Edge Singularity visualization (Art. 191)."""

    def test_wedge_field_scaling(self):
        """E ~ r^(pi/alpha - 1) power law."""
        from maxwell.vis.edge_singularities import calc_wedge_field

        alpha = np.pi / 2
        exponent = np.pi / alpha - 1.0  # Should be 1.0 for 90-degree wedge

        r_vals = np.linspace(0.1, 2.0, 20)
        theta_vals = np.full_like(r_vals, np.pi / 4)

        E_vals = calc_wedge_field(r_vals, theta_vals, alpha)

        # Check power law: E / r^exponent should be approximately constant
        ratio = E_vals / (r_vals**exponent)
        # Normalize by sin(pi * theta / alpha)
        expected = np.abs(np.sin(np.pi * theta_vals / alpha))
        assert np.allclose(ratio, expected, rtol=1e-10)

    def test_edge_singularity_90_degree(self):
        """Correct behavior for alpha = pi/2."""
        from maxwell.vis._base import create_meshgrid
        from maxwell.vis.edge_singularities import calc_edge_singularity

        X, Y = create_meshgrid(0.1, 3, -3, 3, 30, 30)
        E = calc_edge_singularity(X, Y, alpha=np.pi / 2)

        assert E.shape == (30, 30)
        assert np.all(E >= 0)
        # Field should increase with distance for 90-degree wedge (n=1)
        # Points farther from origin should generally have higher field
        far_mask = (X > 2) & (np.abs(Y) < 1)
        near_mask = (X < 0.5) & (np.abs(Y) < 0.5)
        assert np.nanmean(E[far_mask]) > np.nanmean(E[near_mask])

    def test_edge_singularity_sharp_edge(self):
        """Stronger singularity for smaller alpha (sharp edge)."""
        from maxwell.vis.edge_singularities import calc_wedge_field

        # Use r > 1 so that larger exponent means larger field value
        r_test = np.array([2.0])
        # Use a theta that's within all wedges
        theta_test = np.array([np.pi / 8])

        # Smaller alpha -> larger exponent -> stronger field at r > 1
        E_sharp = calc_wedge_field(r_test, theta_test, alpha=np.pi / 4)
        E_obtuse = calc_wedge_field(r_test, theta_test, alpha=3 * np.pi / 4)

        # For r > 1, sharper wedge (larger exponent) produces stronger field
        assert E_sharp[0] > E_obtuse[0]

    def test_plot_edge_singularity_returns_fig_ax(self):
        """plot_edge_singularity returns matplotlib figure and axis."""
        from maxwell.vis.edge_singularities import plot_edge_singularity

        fig, ax = plot_edge_singularity(alpha=np.pi / 2, resolution=30)
        assert fig is not None
        assert ax is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_plot_singularity_comparison_returns_fig_ax(self):
        """plot_singularity_comparison returns matplotlib figure and axis."""
        from maxwell.vis.edge_singularities import plot_singularity_comparison

        fig, ax = plot_singularity_comparison(resolution=30)
        assert fig is not None
        assert ax is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig)

    def test_edge_singularity_default_args(self):
        """Works with no arguments (all defaults)."""
        from maxwell.vis.edge_singularities import (
            plot_edge_singularity,
            plot_singularity_comparison,
        )

        fig1, ax1 = plot_edge_singularity()
        assert fig1 is not None
        import matplotlib.pyplot as mplt

        mplt.close(fig1)

        fig2, ax2 = plot_singularity_comparison()
        assert fig2 is not None
        mplt.close(fig2)

    def test_calc_edge_singularity_no_nan(self):
        """calc_edge_singularity produces no NaN values."""
        from maxwell.vis._base import create_meshgrid
        from maxwell.vis.edge_singularities import calc_edge_singularity

        X, Y = create_meshgrid(0.01, 3, -3, 3, 50, 50)
        E = calc_edge_singularity(X, Y, alpha=np.pi / 2)

        assert not np.any(np.isnan(E))
        assert not np.any(np.isinf(E))

    def test_calc_wedge_field_multiple_angles(self):
        """Wedge field works for multiple wedge angles."""
        from maxwell.vis.edge_singularities import calc_wedge_field

        r = np.linspace(0.1, 2.0, 10)
        theta = np.full_like(r, np.pi / 4)

        for alpha in [np.pi / 6, np.pi / 4, np.pi / 2, np.pi]:
            E = calc_wedge_field(r, theta, alpha)
            assert E.shape == (10,)
            assert np.all(E >= 0)


class TestRenderingValidation:
    """Validate that visualization functions produce renderable PNG output."""

    def _save_and_validate(self, fig, min_pixels=1000):
        """Save figure to temp file and validate pixel count."""
        tmp_path = None
        try:
            # On Windows we need delete=False and manual cleanup
            f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp_path = f.name
            f.close()  # Release handle so savefig can write

            fig.savefig(tmp_path, dpi=80, bbox_inches="tight")
            assert os.path.exists(tmp_path), "PNG file was not created"
            assert os.path.getsize(tmp_path) > 0, "PNG file is empty"

            img = Image.open(tmp_path)
            width, height = img.size
            assert width * height >= min_pixels, (
                f"Image too small: {width}x{height} = {width*height} pixels "
                f"(minimum {min_pixels})"
            )
            img.close()
        finally:
            import matplotlib.pyplot as mplt

            mplt.close(fig)
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except PermissionError:
                    pass  # Best-effort cleanup on Windows

    @render_skip
    def test_field_lines_rendering(self):
        """plot_field_lines_2d produces a valid PNG."""
        from maxwell.vis.field_lines import plot_field_lines_2d

        def field(x, y):
            return x, y

        fig = plot_field_lines_2d(field, nx=20, ny=20)
        self._save_and_validate(fig)

    @render_skip
    def test_dipole_field_lines_rendering(self):
        """plot_dipole_field_lines produces a valid PNG."""
        from maxwell.vis.field_lines import plot_dipole_field_lines

        fig = plot_dipole_field_lines(nx=20, ny=20)
        self._save_and_validate(fig)

    @render_skip
    def test_equipotentials_rendering(self):
        """plot_equipotentials_2d produces a valid PNG."""
        from maxwell.vis.equipotential import plot_equipotentials_2d

        def potential(x, y):
            return 1.0 / np.sqrt(x**2 + y**2 + 0.01)

        fig = plot_equipotentials_2d(potential, nx=50, ny=50)
        self._save_and_validate(fig)

    @render_skip
    def test_dipole_equipotentials_rendering(self):
        """plot_dipole_equipotentials produces a valid PNG."""
        from maxwell.vis.equipotential import plot_dipole_equipotentials

        fig = plot_dipole_equipotentials(nx=50, ny=50)
        self._save_and_validate(fig)

    @render_skip
    def test_stress_tensor_rendering(self):
        """plot_stress_tensor_2d produces a valid PNG."""
        from maxwell.vis.stress import plot_stress_tensor_2d

        def field(x, y):
            return np.ones_like(x) * 1.0, np.zeros_like(x)

        fig = plot_stress_tensor_2d(field, nx=15, ny=15)
        self._save_and_validate(fig)

    @render_skip
    def test_method_of_images_rendering(self):
        """plot_method_of_images produces a valid PNG."""
        from maxwell.vis import plot_method_of_images

        fig, ax = plot_method_of_images(resolution=50)
        self._save_and_validate(fig)

    @render_skip
    def test_edge_singularity_rendering(self):
        """plot_edge_singularity produces a valid PNG."""
        from maxwell.vis import plot_edge_singularity

        fig, ax = plot_edge_singularity(alpha=np.pi / 2, resolution=50)
        self._save_and_validate(fig)

    @render_skip
    def test_singularity_comparison_rendering(self):
        """plot_singularity_comparison produces a valid PNG."""
        from maxwell.vis import plot_singularity_comparison

        fig, ax = plot_singularity_comparison(resolution=50)
        self._save_and_validate(fig)
