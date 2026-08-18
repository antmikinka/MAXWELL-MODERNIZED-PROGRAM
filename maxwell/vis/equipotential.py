"""maxwell.vis.equipotential — Equipotential contour plotting.

Implements 2D equipotential line visualization using matplotlib contour,
supporting point charges, dipoles, and arbitrary potential functions.

Corresponds to Maxwell's treatment of equipotential surfaces in
Part I, Arts. 16-19 (equipotential surfaces and lines of force).
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._base import create_meshgrid, format_axis_labels
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    16,
    17,
    18,
    19,
    part=1,
    chapter="On Equipotential Surfaces and Lines of Force",
    description="Plot 2D equipotential contours for arbitrary potential functions.",
)
def plot_equipotentials_2d(
    potential_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_min: float = -5.0,
    x_max: float = 5.0,
    y_min: float = -5.0,
    y_max: float = 5.0,
    nx: int = 200,
    ny: int = 200,
    n_levels: int = 20,
    levels: np.ndarray | None = None,
    cmap: str = "RdBu_r",
    filled: bool = True,
    charge_positions: list[tuple[float, float]] | None = None,
    charge_signs: list[int] | None = None,
    title: str = "Equipotential Lines",
    ax: Axes | None = None,
) -> Figure:
    """Plot 2D equipotential contours.

    Art. 16-19: Maxwell's treatment of equipotential surfaces —
    surfaces where the potential V is constant. The electric field
    is everywhere perpendicular to these surfaces.

    Args:
        potential_func: Function V(x, y) returning potential values
                        on the grid.
        x_min, x_max: X range in cm.
        y_min, y_max: Y range in cm.
        nx, ny: Grid resolution.
        n_levels: Number of contour levels (if levels not specified).
        levels: Explicit contour levels (overrides n_levels).
        cmap: Colormap for filled contours.
        filled: Whether to use filled contours (contourf) or lines (contour).
        charge_positions: Optional list of (x, y) charge positions.
        charge_signs: Optional list of +1/-1 for charge polarity.
        title: Plot title.
        ax: Optional existing axes.

    Returns:
        Matplotlib Figure with equipotential plot.

    Reference:
        Part I, Arts. 16-19: Equipotential surfaces.
    """
    require_matplotlib()

    X, Y = create_meshgrid(x_min, x_max, y_min, y_max, nx, ny)
    V = potential_func(X, Y)

    if levels is None:
        levels = n_levels

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    if filled:
        cf = ax.contourf(X, Y, V, levels=levels, cmap=cmap, alpha=0.8)
        fig.colorbar(cf, ax=ax, label="V (statvolt)")
    else:
        cs = ax.contour(X, Y, V, levels=levels, cmap=cmap, linewidths=1.0)
        fig.colorbar(cs, ax=ax, label="V (statvolt)")

    # Mark charge positions
    if charge_positions and charge_signs:
        for (cx, cy), sign in zip(charge_positions, charge_signs):
            color = "red" if sign > 0 else "blue"
            ax.plot(
                cx, cy, "o", color=color, markersize=10, label="+" if sign > 0 else "-"
            )

    format_axis_labels(ax, title=title)

    if charge_positions:
        ax.legend(loc="upper right")

    fig.tight_layout()
    return fig


@maxwell_cite(
    16,
    17,
    18,
    19,
    part=1,
    chapter="On Equipotential Surfaces and Lines of Force",
    description="Plot equipotential lines for an electric dipole (convenience wrapper).",
)
def plot_dipole_equipotentials(
    charge_magnitude: float = 1.0,
    separation: float = 2.0,
    **kwargs,
) -> Figure:
    """Plot equipotential lines for an electric dipole.

    Convenience wrapper for the canonical dipole configuration.

    Args:
        charge_magnitude: Absolute charge value (esu).
        separation: Distance between charges (cm).
        **kwargs: Additional arguments to plot_equipotentials_2d.

    Returns:
        Matplotlib Figure with dipole equipotentials.
    """
    half_sep = separation / 2.0

    def dipole_potential(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Compute V from a dipole at (±separation/2, 0)."""
        eps = 1e-10
        dx_p = x - half_sep
        dy_p = y
        r_p = np.sqrt(dx_p**2 + dy_p**2 + eps)
        dx_n = x + half_sep
        dy_n = y
        r_n = np.sqrt(dx_n**2 + dy_n**2 + eps)
        return charge_magnitude / r_p - charge_magnitude / r_n

    kwargs.setdefault("charge_positions", [(half_sep, 0), (-half_sep, 0)])
    kwargs.setdefault("charge_signs", [1, -1])
    kwargs.setdefault("title", "Dipole Equipotential Lines")

    return plot_equipotentials_2d(dipole_potential, **kwargs)
