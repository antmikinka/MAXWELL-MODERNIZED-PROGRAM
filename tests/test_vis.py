"""Tests for maxwell.vis visualization package."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.vis._compat import HAS_MATPLOTLIB, plt

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
        from maxwell.vis._base import evaluate_on_grid, create_meshgrid

        def vec_field(x, y):
            return np.stack([x, y], axis=-1)

        X, Y = create_meshgrid(-1, 1, -1, 1, 5, 5)
        result = evaluate_on_grid(vec_field, X, Y, component=0)
        assert result.shape == (5, 5)
        assert np.allclose(result, X)

    def test_evaluate_on_grid_scalar(self):
        from maxwell.vis._base import evaluate_on_grid, create_meshgrid

        def scalar_field(x, y):
            return x**2 + y**2

        X, Y = create_meshgrid(-1, 1, -1, 1, 5, 5)
        result = evaluate_on_grid(scalar_field, X, Y)
        assert result.shape == (5, 5)
        assert np.allclose(result, X**2 + Y**2)

    def test_format_axis_labels(self):
        from maxwell.vis._base import format_axis_labels
        import matplotlib.pyplot as mplt

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
            field, nx=10, ny=10,
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
        from maxwell.vis.stress import verify_stress_tensor_plot
        import numpy as np
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
            create_meshgrid,
            evaluate_on_grid,
            plot_field_lines_2d,
            plot_equipotentials_2d,
            plot_stress_tensor_2d,
        )
        assert callable(create_meshgrid)
        assert callable(evaluate_on_grid)
        assert callable(plot_field_lines_2d)
        assert callable(plot_equipotentials_2d)
        assert callable(plot_stress_tensor_2d)
