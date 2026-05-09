"""maxwell.vis.edge_singularities — Conducting edge field singularity visualization.

Implements 2D visualization of field enhancement near sharp conducting edges
and wedges, showing the power-law singularity behavior.

Corresponds to Maxwell's treatment of singular points and edges in
Part II, Art. 191 (Singular Points and Lines of Force).
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._base import create_meshgrid, format_axis_labels
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    191,
    part=2,
    chapter="Singular Points and Lines of Force",
    description="Calculate field magnitude near a conducting wedge of given angle.",
)
def calc_wedge_field(
    r: np.ndarray,
    theta: np.ndarray,
    alpha: float,
    E0: float = 1.0,
) -> np.ndarray:
    """Calculate field near a conducting wedge.

    Art. 191: Near a conducting wedge of angle alpha, the electric
    field behaves as a power law in the distance from the edge:

        E(r, theta) ~ E0 * r^(pi/alpha - 1) * sin(pi * theta / alpha)

    The exponent n = pi/alpha - 1 determines the singularity strength:
    - alpha = pi/2 (90-degree wedge): n = 1, E ~ r (vanishes at edge)
    - alpha = pi  (flat plane):       n = 0, E = constant
    - alpha -> 0  (sharp edge):       n -> inf, E diverges

    Args:
        r: Radial distance from edge (must be > 0).
        theta: Angular position from wedge face (radians).
        alpha: Wedge opening angle (radians).
        E0: Reference field strength.

    Returns:
        E_magnitude: Field strength array.
    """
    exponent = np.pi / alpha - 1.0
    # Avoid issues at r=0
    r_safe = np.where(r < 1e-15, 1e-15, r)
    E = E0 * r_safe**exponent * np.abs(np.sin(np.pi * theta / alpha))
    return E


@maxwell_cite(
    191,
    part=2,
    chapter="Singular Points and Lines of Force",
    description="Calculate field on 2D grid near a conducting edge.",
)
def calc_edge_singularity(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float = np.pi / 2,
) -> np.ndarray:
    """Calculate field on 2D grid near conducting edge.

    Maps Cartesian (x, y) to polar (r, theta) coordinates centered
    at the wedge tip, then applies the wedge field solution.

    The wedge edge is placed at the origin (0, 0). The wedge faces
    lie along theta=0 and theta=alpha.

    Args:
        x: 2D x-coordinate mesh grid.
        y: 2D y-coordinate mesh grid.
        alpha: Wedge opening angle (radians). Default pi/2 (90 degrees).

    Returns:
        E: 2D field magnitude array.
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(np.abs(y), x)
    # Clamp theta to [0, alpha] range for the wedge geometry
    theta = np.clip(theta, 0, alpha)

    return calc_wedge_field(r, theta, alpha)


@maxwell_cite(
    191,
    part=2,
    chapter="Singular Points and Lines of Force",
    description="Plot field enhancement near conducting edge with logarithmic colormap.",
)
def plot_edge_singularity(
    alpha: float = np.pi / 2,
    x_range: Tuple[float, float] = (0.01, 3.0),
    y_range: Tuple[float, float] = (-3.0, 3.0),
    resolution: int = 100,
    ax: Optional[Axes] = None,
    log_scale: bool = True,
) -> Tuple[Figure, Axes]:
    """Plot field enhancement near conducting edge for Art. 191.

    Visualizes the power-law field singularity near a conducting wedge
    edge. The field magnitude is shown with optional logarithmic color
    scale to highlight the singularity structure.

    Args:
        alpha: Wedge angle in radians (default pi/2 = 90 degrees).
        x_range: X plot domain (min, max), must start > 0.
        y_range: Y plot domain (min, max).
        resolution: Grid resolution (points per axis).
        ax: Optional existing matplotlib axes (creates new if None).
        log_scale: Use logarithmic color scale for field magnitude.

    Returns:
        Tuple of (fig, ax) matplotlib figure and axes.

    Reference:
        Part II, Art. 191: Singular Points and Lines of Force.
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

    E = calc_edge_singularity(X, Y, alpha)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    if log_scale:
        # Log scale to show wide dynamic range
        E_log = np.log10(E + 1e-15)
        cf = ax.contourf(X, Y, E_log, levels=30, cmap="plasma", alpha=0.8)
        fig.colorbar(cf, ax=ax, label="log10(|E|)")
    else:
        cf = ax.contourf(X, Y, E, levels=30, cmap="plasma", alpha=0.8)
        fig.colorbar(cf, ax=ax, label="|E|")

    # Wedge boundary lines
    ax.axhline(y=0, color="white", linestyle="-", linewidth=1.5, alpha=0.5)

    # Contour lines
    ax.contour(X, Y, E, levels=10, colors="white", linewidths=0.3, alpha=0.3)

    # Mark edge position
    ax.plot(0, 0, "w*", markersize=15, zorder=5, label="Edge")

    alpha_deg = np.degrees(alpha)
    format_axis_labels(
        ax,
        title=f"Field Singularity Near {alpha_deg:.0f} Degree Conducting Edge (Art. 191)",
    )
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    191,
    part=2,
    chapter="Singular Points and Lines of Force",
    description="Compare singularity strength for different wedge angles.",
)
def plot_singularity_comparison(
    x_range: Tuple[float, float] = (0.01, 3.0),
    resolution: int = 100,
    ax: Optional[Axes] = None,
) -> Tuple[Figure, Axes]:
    """Compare singularity strength for different wedge angles.

    Shows field magnitude vs. distance from edge for alpha = pi/4
    (sharp), pi/2 (90 degrees), and 3*pi/4 (obtuse), illustrating
    how the singularity strengthens as the wedge angle decreases.

    Args:
        x_range: Radial distance range (min, max).
        resolution: Number of evaluation points.
        ax: Optional existing matplotlib axes (creates new if None).

    Returns:
        Tuple of (fig, ax) matplotlib figure and axes.

    Reference:
        Part II, Art. 191: Singular Points and Lines of Force.
    """
    require_matplotlib()

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    angles = [np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    labels = [
        r"$\alpha = \pi/4$ (sharp)",
        r"$\alpha = \pi/2$ (90 deg)",
        r"$\alpha = 3\pi/4$ (obtuse)",
    ]
    colors = ["red", "green", "blue"]

    r_vals = np.linspace(x_range[0], x_range[1], resolution)
    theta_fixed = np.pi / 4  # Fixed observation angle

    for angle, label, color in zip(angles, labels, colors):
        E_vals = calc_wedge_field(r_vals, np.full_like(r_vals, theta_fixed), angle)
        ax.loglog(r_vals, E_vals, color=color, linewidth=2, label=label)

    ax.set_xlabel("Distance from Edge r (cm)")
    ax.set_ylabel("|E| (statvolt/cm)")
    ax.set_title("Field Singularity Strength vs. Wedge Angle (Art. 191)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    return fig, ax
