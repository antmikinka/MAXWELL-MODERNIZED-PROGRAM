"""maxwell.vis.flow_tubes -- Unit Tubes of Flow visualization.

Implements 3D visualization of unit tubes of flow for a current density field,
as described by Maxwell in his theory of tubes of electric flow.

Corresponds to Maxwell's treatment of tubes of flow in
Part III, Art. 290 (Theory of Tubes of Flow).
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np

from maxwell.vis._compat import require_matplotlib, plt, Figure, Axes
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    290,
    part=2,
    chapter="Theory of Tubes of Flow",
    description="Calculate 3D current density field and unit tube trajectories.",
)
def calc_unit_tubes(
    charge_positions: np.ndarray,
    charge_magnitudes: np.ndarray,
    grid_range: Tuple[float, float, float, float, float, float] = (-3.0, 3.0, -3.0, 3.0, -3.0, 3.0),
    resolution: int = 20,
) -> dict:
    """Calculate 3D current density field for unit tubes of flow visualization.

    Art. 290: A tube of flow is a surface formed by drawing lines of flow
    (streamlines of the current density J) such that the tubes carry equal
    flux. The unit tube carries one unit of current between electrodes.

    For a set of point charges, the current density field J at position r is:
        J(r) = sum_i(q_i * (r - r_i) / |r - r_i|^3)

    The unit tubes are streamlines of J, each carrying unit flux.

    Args:
        charge_positions: Array of shape (N, 3) with charge positions (cm).
        charge_magnitudes: Array of shape (N,) with charge magnitudes (esu).
        grid_range: (x_min, x_max, y_min, y_max, z_min, z_max) in cm.
        resolution: Number of grid points per axis.

    Returns:
        Dictionary with:
        - Jx, Jy, Jz: 3D current density component arrays
        - J_magnitude: |J| array
        - x, y, z: 1D coordinate arrays
        - X, Y, Z: 3D meshgrid arrays
    """
    x_min, x_max, y_min, y_max, z_min, z_max = grid_range

    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    z = np.linspace(z_min, z_max, resolution)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    eps = 1e-10  # Avoid singularity at charge positions

    Jx = np.zeros_like(X)
    Jy = np.zeros_like(Y)
    Jz = np.zeros_like(Z)

    for i in range(len(charge_magnitudes)):
        dx = X - charge_positions[i, 0]
        dy = Y - charge_positions[i, 1]
        dz = Z - charge_positions[i, 2]
        r_sq = dx**2 + dy**2 + dz**2 + eps
        r = np.sqrt(r_sq)
        r_cubed = r * r_sq

        q = charge_magnitudes[i]
        Jx += q * dx / r_cubed
        Jy += q * dy / r_cubed
        Jz += q * dz / r_cubed

    J_magnitude = np.sqrt(Jx**2 + Jy**2 + Jz**2)

    return {
        "Jx": Jx,
        "Jy": Jy,
        "Jz": Jz,
        "J_magnitude": J_magnitude,
        "x": x,
        "y": y,
        "z": z,
        "X": X,
        "Y": Y,
        "Z": Z,
    }


@maxwell_cite(
    290,
    part=2,
    chapter="Theory of Tubes of Flow",
    description="Plot unit tubes of flow using matplotlib quiver/streamplot.",
)
def plot_unit_tubes_of_flow(
    charge_positions: Optional[np.ndarray] = None,
    charge_magnitudes: Optional[np.ndarray] = None,
    slice_z: float = 0.0,
    x_range: Tuple[float, float] = (-3.0, 3.0),
    y_range: Tuple[float, float] = (-3.0, 3.0),
    resolution: int = 50,
    ax: Optional[Axes] = None,
    show_charges: bool = True,
    plot_mode: str = "streamplot",
    density: float = 1.5,
) -> Tuple[Figure, Axes]:
    """Plot unit tubes of flow visualization for Art. 290.

    Shows the current density field as streamlines or quiver arrows
    on a 2D slice through the 3D field, representing cross-sections
    of unit tubes of flow.

    Art. 290: Unit tubes of flow carry equal flux between source
    and sink charges. The tube density is proportional to the
    current density magnitude.

    Args:
        charge_positions: Array of shape (N, 3) with charge positions (cm).
                         Default: dipole at (+1, 0, 0) and (-1, 0, 0).
        charge_magnitudes: Array of shape (N,) with charge magnitudes (esu).
                          Default: [+1, -1] (dipole).
        slice_z: Z-coordinate of the 2D slice plane (cm).
        x_range: X plot domain (min, max).
        y_range: Y plot domain (min, max).
        resolution: Grid resolution (points per axis).
        ax: Optional existing matplotlib axes (creates new if None).
        show_charges: Whether to mark charge positions on the slice.
        plot_mode: "streamplot" for streamlines, "quiver" for arrow field.
        density: Streamline density (streamplot mode) or arrow skip (quiver).

    Returns:
        Tuple of (fig, ax) matplotlib figure and axes.

    Reference:
        Part III, Art. 290: Theory of Tubes of Flow.
    """
    require_matplotlib()

    if charge_positions is None:
        charge_positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
    if charge_magnitudes is None:
        charge_magnitudes = np.array([1.0, -1.0])

    charge_positions = np.asarray(charge_positions, dtype=np.float64)
    charge_magnitudes = np.asarray(charge_magnitudes, dtype=np.float64)

    # Compute the 2D slice of the 3D field at slice_z
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)

    # Create a 2D field by evaluating at z = slice_z
    eps = 1e-10
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for i in range(len(charge_magnitudes)):
        dx = X - charge_positions[i, 0]
        dy = Y - charge_positions[i, 1]
        dz = slice_z - charge_positions[i, 2]
        r_sq = dx**2 + dy**2 + dz**2 + eps
        r = np.sqrt(r_sq)
        r_cubed = r * r_sq

        q = charge_magnitudes[i]
        Ex += q * dx / r_cubed
        Ey += q * dy / r_cubed

    magnitude = np.sqrt(Ex**2 + Ey**2)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    # Background: field magnitude
    vmax_abs = np.nanmax(magnitude)
    if vmax_abs > 0:
        cf = ax.contourf(
            X, Y, magnitude,
            levels=30,
            cmap="plasma",
            vmin=0,
            vmax=vmax_abs,
            alpha=0.7,
        )
        fig.colorbar(cf, ax=ax, label="|J| (current density)")

    if plot_mode == "streamplot":
        strm = ax.streamplot(
            X, Y, Ex, Ey,
            density=density,
            linewidth=magnitude / (np.nanmax(magnitude) + eps) * 2,
            cmap="autumn",
            arrowsize=1.0,
            arrowstyle="-|>",
        )
    elif plot_mode == "quiver":
        skip = max(1, int(resolution / (resolution * density / 10)))
        ax.quiver(
            X[::skip, ::skip], Y[::skip, ::skip],
            Ex[::skip, ::skip], Ey[::skip, ::skip],
            magnitude[::skip, ::skip],
            cmap="autumn",
            scale=50,
            width=0.003,
        )
    else:
        raise ValueError(f"Unknown plot_mode: {plot_mode}. Use 'streamplot' or 'quiver'.")

    # Equipotential-like contours
    ax.contour(X, Y, magnitude, levels=8, colors="white", linewidths=0.3, alpha=0.3)

    # Mark charge positions on the slice
    if show_charges:
        for i in range(len(charge_magnitudes)):
            # Only show charges that are close to the slice plane
            dz = abs(charge_positions[i, 2] - slice_z)
            if dz < 0.5:
                q = charge_magnitudes[i]
                color = "red" if q > 0 else "blue"
                marker = "o" if q > 0 else "o"
                ax.plot(
                    charge_positions[i, 0], charge_positions[i, 1],
                    marker, color=color, markersize=14, zorder=5,
                    markerfacecolor=color if q > 0 else "none",
                    markeredgewidth=2,
                )
                label = f"+q" if q > 0 else f"-q"
                ax.text(
                    charge_positions[i, 0] + 0.2, charge_positions[i, 1] + 0.2,
                    label, fontsize=12, fontweight="bold",
                    color=color, ha="left",
                )

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title(f"Unit Tubes of Flow: Current Density Field (Art. 290), z={slice_z:.1f} cm")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    290,
    part=2,
    chapter="Theory of Tubes of Flow",
    description="Plot 3D quiver visualization of unit tubes of flow.",
)
def plot_unit_tubes_3d(
    charge_positions: Optional[np.ndarray] = None,
    charge_magnitudes: Optional[np.ndarray] = None,
    grid_range: Tuple[float, float, float, float, float, float] = (-3.0, 3.0, -3.0, 3.0, -3.0, 3.0),
    resolution: int = 8,
    cmap: str = "autumn",
    skip: int = 1,
) -> Figure:
    """Plot 3D quiver visualization of unit tubes of flow.

    Art. 290: Full 3D visualization of the current density field
    using a 3D quiver plot showing the direction and magnitude
    of flow at grid points.

    Args:
        charge_positions: Array of shape (N, 3) with charge positions (cm).
        charge_magnitudes: Array of shape (N,) with charge magnitudes (esu).
        grid_range: (x_min, x_max, y_min, y_max, z_min, z_max) in cm.
        resolution: Number of grid points per axis.
        cmap: Colormap name for the quiver coloring.
        skip: Subsampling factor for the quiver plot.

    Returns:
        Matplotlib figure with 3D quiver plot.

    Reference:
        Part III, Art. 290: Theory of Tubes of Flow.
    """
    require_matplotlib()

    if charge_positions is None:
        charge_positions = np.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])
    if charge_magnitudes is None:
        charge_magnitudes = np.array([1.0, -1.0])

    charge_positions = np.asarray(charge_positions, dtype=np.float64)
    charge_magnitudes = np.asarray(charge_magnitudes, dtype=np.float64)

    field = calc_unit_tubes(charge_positions, charge_magnitudes, grid_range, resolution)

    Jx = field["Jx"]
    Jy = field["Jy"]
    Jz = field["Jz"]
    J_mag = field["J_magnitude"]
    X = field["X"]
    Y = field["Y"]
    Z = field["Z"]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Subsample for clarity
    s = max(1, skip)
    # Flatten for quiver, then reshape back
    X_s = X[::s, ::s, ::s].ravel()
    Y_s = Y[::s, ::s, ::s].ravel()
    Z_s = Z[::s, ::s, ::s].ravel()
    Jx_s = Jx[::s, ::s, ::s].ravel()
    Jy_s = Jy[::s, ::s, ::s].ravel()
    Jz_s = Jz[::s, ::s, ::s].ravel()
    J_mag_s = J_mag[::s, ::s, ::s].ravel()

    ax.quiver(
        X_s, Y_s, Z_s,
        Jx_s, Jy_s, Jz_s,
        array=J_mag_s,
        cmap=cmap,
        length=0.5,
        normalize=True,
    )

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("z (cm)")
    ax.set_title("Unit Tubes of Flow: 3D Current Density (Art. 290)")
    fig.tight_layout()
    return fig
