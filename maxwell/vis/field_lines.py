"""maxwell.vis.field_lines — Electric and magnetic field line plotting.

Implements 2D field line visualization using matplotlib streamplot,
supporting point charges, dipoles, and arbitrary field functions.

All functions trace to Maxwell's treatment of field lines in
Part I (electrostatics) and Part IV (electromagnetism).
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple

import numpy as np

from maxwell.vis._compat import require_matplotlib, plt, Figure, Axes
from maxwell.vis._base import create_meshgrid, format_axis_labels


def plot_field_lines_2d(
    field_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_min: float = -5.0,
    x_max: float = 5.0,
    y_min: float = -5.0,
    y_max: float = 5.0,
    nx: int = 50,
    ny: int = 50,
    density: float = 1.5,
    linewidth: Optional[np.ndarray] = None,
    cmap: str = "autumn",
    charge_positions: Optional[list[Tuple[float, float]]] = None,
    charge_signs: Optional[list[int]] = None,
    title: str = "Electric Field Lines",
    ax: Optional[Axes] = None,
) -> Figure:
    """Plot 2D electric field lines using streamplot.

    Art. 52-61: Maxwell's treatment of field lines (lines of force)
    as visual representations of the electric field direction.

    Args:
        field_func: Function E(x, y) -> (Ex, Ey) where x, y are 2D arrays
                    and the return is a tuple of two 2D arrays for the
                    x and y components of the field.
        x_min, x_max: X range in cm.
        y_min, y_max: Y range in cm.
        nx, ny: Grid resolution.
        density: Streamline density (lines per unit area).
        linewidth: Optional array of line widths, shape (ny, nx).
                   Defaults to field magnitude.
        cmap: Colormap for streamlines.
        charge_positions: Optional list of (x, y) charge positions
                          to mark on the plot.
        charge_signs: Optional list of +1/-1 for charge polarity.
        title: Plot title.
        ax: Optional existing axes to plot on.

    Returns:
        Matplotlib Figure containing the field line plot.

    Reference:
        Part I, Arts. 52-61: Lines of force.
    """
    require_matplotlib()

    X, Y = create_meshgrid(x_min, x_max, y_min, y_max, nx, ny)
    Ex, Ey = field_func(X, Y)

    # Compute field magnitude for linewidth
    magnitude = np.sqrt(Ex**2 + Ey**2)
    if linewidth is None:
        linewidth = magnitude

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    strm = ax.streamplot(
        X, Y, Ex, Ey,
        density=density,
        linewidth=linewidth,
        cmap=cmap,
        arrowsize=1.2,
        arrowstyle="-|>",
    )

    # Mark charge positions if provided
    if charge_positions and charge_signs:
        for (cx, cy), sign in zip(charge_positions, charge_signs):
            color = "red" if sign > 0 else "blue"
            ax.plot(cx, cy, "o", color=color, markersize=12,
                    label="+" if sign > 0 else "-")
            ax.text(cx + 0.3, cy, "+" if sign > 0 else "-",
                    fontsize=14, fontweight="bold", color="white",
                    ha="center", va="center")

    fig.colorbar(strm.lines, ax=ax, label="|E| (statvolt/cm)")
    format_axis_labels(ax, title=title)

    if charge_positions:
        ax.legend(loc="upper right")

    fig.tight_layout()
    return fig


def plot_dipole_field_lines(
    charge_magnitude: float = 1.0,
    separation: float = 2.0,
    **kwargs,
) -> Figure:
    """Plot field lines for an electric dipole.

    Convenience wrapper around plot_field_lines_2d for the canonical
    dipole configuration.

    Args:
        charge_magnitude: Absolute charge value (esu).
        separation: Distance between charges (cm).
        **kwargs: Additional arguments passed to plot_field_lines_2d.

    Returns:
        Matplotlib Figure with dipole field lines.
    """
    half_sep = separation / 2.0

    def dipole_field(x, y):
        """Compute E field from a dipole at (±separation/2, 0)."""
        eps = 1e-10  # Avoid singularity at charge positions

        # Positive charge at (+half_sep, 0)
        dx_p = x - half_sep
        dy_p = y - 0
        r_p2 = dx_p**2 + dy_p**2 + eps
        r_p = np.sqrt(r_p2)
        Ex_p = charge_magnitude * dx_p / r_p2
        Ey_p = charge_magnitude * dy_p / r_p2

        # Negative charge at (-half_sep, 0)
        dx_n = x + half_sep
        dy_n = y - 0
        r_n2 = dx_n**2 + dy_n**2 + eps
        r_n = np.sqrt(r_n2)
        Ex_n = -charge_magnitude * dx_n / r_n2
        Ey_n = -charge_magnitude * dy_n / r_n2

        return Ex_p + Ex_n, Ey_p + Ey_n

    kwargs.setdefault("charge_positions", [(half_sep, 0), (-half_sep, 0)])
    kwargs.setdefault("charge_signs", [1, -1])
    kwargs.setdefault("title", "Electric Dipole Field Lines")

    return plot_field_lines_2d(dipole_field, **kwargs)
