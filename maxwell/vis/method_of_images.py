"""maxwell.vis.method_of_images — Method of Images visualization.

Implements 2D visualization of the Method of Images for a point charge
above an infinite conducting plane, using the image charge technique.

Corresponds to Maxwell's treatment of electric images in
Part II, Art. 155 (Theory of Electric Images).
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._base import create_meshgrid, format_axis_labels
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    155,
    part=2,
    chapter="Theory of Electric Images",
    description="Calculate potential and field for a point charge above a conducting plane using the method of images.",
)
def calc_method_of_images(
    q: float,
    d: float,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate potential and field for charge + image charge.

    Art. 155: A point charge +q at distance d from an infinite
    conducting plane. The image charge -q at -d produces V=0 on
    the plane (x=0), satisfying the boundary condition.

    The potential at point (x, y) is:
        V = q / r_real - q / r_image
    where:
        r_real  = sqrt((x - d)^2 + y^2)   (distance to real charge)
        r_image = sqrt((x + d)^2 + y^2)   (distance to image charge)

    The electric field components:
        Ex = -dV/dx, Ey = -dV/dy

    Args:
        q: Charge magnitude (CGS-ESU statcoulombs).
        d: Distance from conducting plane (cm).
        x_grid: 2D x-coordinate mesh grid.
        y_grid: 2D y-coordinate mesh grid.

    Returns:
        Tuple of (V, Ex, Ey) 2D arrays.
    """
    eps = 1e-10  # Avoid singularity at charge positions

    # Real charge at (d, 0), image charge at (-d, 0)
    dx_real = x_grid - d
    dy_real = y_grid
    r_real_sq = dx_real**2 + dy_real**2 + eps
    r_real = np.sqrt(r_real_sq)

    dx_image = x_grid + d
    dy_image = y_grid
    r_image_sq = dx_image**2 + dy_image**2 + eps
    r_image = np.sqrt(r_image_sq)

    # Potential: superposition of real (+q) and image (-q) charges
    V = q / r_real - q / r_image

    # Electric field: E = -grad(V)
    # dV/dx = -q * dx_real / r_real^3 + q * dx_image / r_image^3
    # dV/dy = -q * dy_real / r_real^3 + q * dy_image / r_image^3
    Ex = q * dx_real / r_real_sq**1.5 - q * dx_image / r_image_sq**1.5
    Ey = q * dy_real / r_real_sq**1.5 - q * dy_image / r_image_sq**1.5

    return V, Ex, Ey


@maxwell_cite(
    155,
    part=2,
    chapter="Theory of Electric Images",
    description="Plot equipotential contours and field lines for a charge above a conducting plane.",
)
def plot_method_of_images(
    q: float = 1.0,
    d: float = 1.0,
    x_range: Tuple[float, float] = (-3.0, 3.0),
    y_range: Tuple[float, float] = (-3.0, 3.0),
    resolution: int = 100,
    ax: Optional[Axes] = None,
    show_image_charges: bool = True,
) -> Tuple[Figure, Axes]:
    """Plot Method of Images visualization for Art. 155.

    Shows equipotential contours and field lines for a charge above
    a conducting plane, with real and image charges marked.

    The conducting plane is at x=0 (shown as a vertical dashed line).
    The real charge +q is at (d, 0) and the image charge -q is at
    (-d, 0).

    Args:
        q: Charge magnitude (statcoulombs).
        d: Distance from conducting plane (cm).
        x_range: X plot domain (min, max).
        y_range: Y plot domain (min, max).
        resolution: Grid resolution (points per axis).
        ax: Optional existing matplotlib axes (creates new if None).
        show_image_charges: Whether to mark charge positions.

    Returns:
        Tuple of (fig, ax) matplotlib figure and axes.

    Reference:
        Part II, Art. 155: Theory of Electric Images.
    """
    require_matplotlib()

    X, Y = create_meshgrid(
        x_range[0],
        x_range[1],
        y_range[0],
        y_range[1],
        resolution,
        resolution,
    )

    V, Ex, Ey = calc_method_of_images(q, d, X, Y)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    # Background: potential filled contour
    vmin, vmax = np.nanmin(V), np.nanmax(V)
    vmax_abs = max(abs(vmin), abs(vmax))
    cf = ax.contourf(
        X,
        Y,
        V,
        levels=30,
        cmap="RdBu_r",
        vmin=-vmax_abs,
        vmax=vmax_abs,
        alpha=0.8,
    )
    fig.colorbar(cf, ax=ax, label="V (statvolt)")

    # Equipotential contour lines
    ax.contour(X, Y, V, levels=15, colors="black", linewidths=0.5, alpha=0.4)

    # Field lines (streamplot)
    magnitude = np.sqrt(Ex**2 + Ey**2)
    strm = ax.streamplot(
        X,
        Y,
        Ex,
        Ey,
        density=1.2,
        linewidth=magnitude / np.nanmax(magnitude) * 2,
        cmap="autumn",
        arrowsize=1.0,
        arrowstyle="-|>",
    )

    # Conducting plane (x=0)
    ax.axvline(
        x=0, color="gray", linestyle="--", linewidth=2, label="Conducting Plane (V=0)"
    )

    # Mark charge positions
    if show_image_charges:
        # Real charge
        ax.plot(d, 0, "o", color="red", markersize=14, zorder=5)
        ax.text(
            d + 0.2, 0.2, f"+q", fontsize=12, fontweight="bold", color="red", ha="left"
        )

        # Image charge (dashed to indicate it's virtual)
        ax.plot(
            -d,
            0,
            "o",
            color="blue",
            markersize=14,
            zorder=5,
            markerfacecolor="none",
            markeredgewidth=2,
        )
        ax.text(
            -d - 0.2,
            0.2,
            f"-q (image)",
            fontsize=12,
            fontweight="bold",
            color="blue",
            ha="right",
        )

    format_axis_labels(
        ax, title="Method of Images: Charge Above Conducting Plane (Art. 155)"
    )
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig, ax
