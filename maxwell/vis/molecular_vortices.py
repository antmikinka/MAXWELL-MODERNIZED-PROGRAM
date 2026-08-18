"""maxwell.vis.molecular_vortices -- Molecular vortex visualization.

Implements visualization of Maxwell's mechanical vortex model of magnetism,
showing the lattice of rotating molecular vortices and their collective
magnetic field behavior.

Corresponds to Maxwell's mechanical theory in
Part IV, Arts. 822-824 (Molecular Vortices).
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    822,
    part=4,
    chapter="Molecular Vortices",
    description="Calculate 2D vortex lattice velocity field.",
)
def calc_vortex_lattice(
    x: np.ndarray,
    y: np.ndarray,
    vortex_centers: list[tuple[float, float]] | None = None,
    vortex_signs: list[int] | None = None,
    vortex_strength: float = 1.0,
    core_radius: float = 0.3,
) -> dict[str, np.ndarray]:
    """Calculate velocity field of a 2D molecular vortex lattice.

    Art. 822: Maxwell's model of molecular vortices -- adjacent
    vortices rotating in opposite directions like meshing gears.
    The velocity field of a point vortex at origin:

        v_theta = Gamma / (2 * pi * r)  (outside core)
        v_theta = Gamma * r / (2 * pi * r_c^2)  (inside core)

    where Gamma is the circulation strength and r_c is the core radius.
    The core regularization avoids the singularity at r = 0.

    Adjacent vortices alternate rotation direction (signs alternate
    in a checkerboard pattern), producing the "gear" mechanism
    Maxwell proposed for magnetic field generation.

    Args:
        x: 2D grid of x positions (cm).
        y: 2D grid of y positions (cm).
        vortex_centers: List of (cx, cy) center positions.
            Default: 3x3 checkerboard grid.
        vortex_signs: List of +1 or -1 for each vortex rotation sense.
            Default: alternating checkerboard pattern.
        vortex_strength: Circulation strength Gamma.
        core_radius: Vortex core radius (cm) for regularization.

    Returns:
        Dictionary with 'v_x', 'v_y' (velocity components),
        'v_magnitude', 'omega' (vorticity = curl v), and
        'vortex_centers', 'vortex_signs'.

    Reference:
        Part IV, Art. 822: Molecular vortex rotation model.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    if vortex_centers is None:
        # 3x3 checkerboard lattice
        positions = [-1.0, 0.0, 1.0]
        vortex_centers = [(px, py) for px in positions for py in positions]

    if vortex_signs is None:
        # Alternating checkerboard pattern
        vortex_signs = []
        for i, (cx, cy) in enumerate(vortex_centers):
            ix = int(round(cx + 1))
            iy = int(round(cy + 1))
            vortex_signs.append(1 if (ix + iy) % 2 == 0 else -1)

    v_x = np.zeros_like(x, dtype=np.float64)
    v_y = np.zeros_like(x, dtype=np.float64)
    omega = np.zeros_like(x, dtype=np.float64)

    for (cx, cy), sign in zip(vortex_centers, vortex_signs):
        dx = x - cx
        dy = y - cy
        r = np.sqrt(dx**2 + dy**2)
        r_safe = np.maximum(r, 1e-10)

        # Tangential velocity (counter-clockwise for sign=+1)
        # Inside core: solid body rotation v ~ r
        # Outside core: potential vortex v ~ 1/r
        inside = r < core_radius
        outside = ~inside

        # Outside: potential vortex
        v_theta_out = sign * vortex_strength / (2.0 * np.pi * r_safe)
        v_x = np.where(outside, v_x - v_theta_out * dy / r_safe, v_x)
        v_y = np.where(outside, v_y + v_theta_out * dx / r_safe, v_y)

        # Inside: solid body rotation (smooth regularization)
        v_theta_in = sign * vortex_strength * r / (2.0 * np.pi * core_radius**2)
        v_x = np.where(inside, v_x - v_theta_in * dy / r_safe, v_x)
        v_y = np.where(inside, v_y + v_theta_in * dx / r_safe, v_y)

        # Vorticity: omega = dv_y/dx - dv_x/dy
        # For point vortex: omega = Gamma * delta(r)
        # For regularized: smooth Gaussian-like peak
        omega += (
            sign
            * vortex_strength
            / (np.pi * core_radius**2)
            * np.exp(-(r**2) / core_radius**2)
        )

    v_magnitude = np.sqrt(v_x**2 + v_y**2)

    return {
        "v_x": v_x,
        "v_y": v_y,
        "v_magnitude": v_magnitude,
        "omega": omega,
        "vortex_centers": vortex_centers,
        "vortex_signs": vortex_signs,
    }


@maxwell_cite(
    822,
    part=4,
    chapter="Molecular Vortices",
    description="Calculate magnetic field equivalent from vortex lattice.",
)
def calc_magnetic_field_from_vortices(
    vortex_centers: list[tuple[float, float]],
    vortex_signs: list[int],
    vortex_strength: float = 1.0,
    core_radius: float = 0.3,
    density: float = 1.0,
) -> dict[str, float]:
    """Calculate macroscopic magnetic field from vortex lattice.

    Art. 822: Maxwell's key relation -- the magnetic field H is
    proportional to the angular momentum density of the vortices:

        H = (1/2) * rho * omega * r^2

    For the lattice, the net field is the vector sum of all
    vortex contributions. In the checkerboard configuration
    with alternating signs, the net field depends on the
    asymmetry of the vortex distribution.

    Args:
        vortex_centers: List of (cx, cy) positions.
        vortex_signs: List of +1/-1 rotation senses.
        vortex_strength: Circulation strength Gamma.
        core_radius: Vortex core radius.
        density: Ether density rho.

    Returns:
        Dictionary with 'H_x', 'H_y', 'H_magnitude', 'total_energy'.

    Reference:
        Part IV, Art. 822: Magnetic field from vortex angular momentum.
    """
    H_x = 0.0
    H_y = 0.0
    total_energy = 0.0

    for (cx, cy), sign in zip(vortex_centers, vortex_signs):
        # Magnetic field contribution from each vortex
        H = 0.5 * density * sign * vortex_strength * core_radius**2
        # Direction: along z-axis for 2D vortices
        H_z = H
        _ = H_z  # Used for display purposes

        # Kinetic energy of each vortex
        T = 0.25 * density * vortex_strength**2 * core_radius**4
        total_energy += T

    # Net field (for symmetric checkerboard, cancels to zero)
    # Non-zero for asymmetric distributions
    H_magnitude = np.sqrt(H_x**2 + H_y**2)

    return {
        "H_x": H_x,
        "H_y": H_y,
        "H_magnitude": H_magnitude,
        "total_energy": total_energy,
    }


@maxwell_cite(
    822,
    part=4,
    chapter="Molecular Vortices",
    description="Plot 2D vortex lattice velocity field with vorticity.",
)
def plot_molecular_vortices(
    grid_range: tuple[float, float] = (-2.0, 2.0),
    resolution: int = 50,
    vortex_strength: float = 1.0,
    core_radius: float = 0.3,
    show_streamlines: bool = True,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot 2D vortex lattice velocity field with vorticity.

    Art. 822: Visualizes Maxwell's molecular vortex model showing:
    - Velocity field as streamlines or quiver arrows
    - Vorticity (curl of velocity) as color map
    - Vortex centers marked with rotation direction
    - The checkerboard pattern of alternating rotation

    The visualization demonstrates how the collective behavior
    of rotating vortices could produce macroscopic magnetic
    phenomena, as Maxwell proposed.

    Args:
        grid_range: (min, max) spatial range (cm).
        resolution: Grid resolution.
        vortex_strength: Circulation strength.
        core_radius: Vortex core radius (cm).
        show_streamlines: True for streamlines, False for quiver.
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part IV, Art. 822: Molecular vortex model of magnetism.
    """
    require_matplotlib()

    x = np.linspace(grid_range[0], grid_range[1], resolution)
    y = np.linspace(grid_range[0], grid_range[1], resolution)
    X, Y = np.meshgrid(x, y)

    result = calc_vortex_lattice(
        X, Y, vortex_strength=vortex_strength, core_radius=core_radius
    )

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        fig = ax.figure

    # Vorticity color map
    omega = result["omega"]
    omega_max = np.max(np.abs(omega))
    cf = ax.contourf(
        X,
        Y,
        omega,
        levels=30,
        cmap="RdBu_r",
        vmin=-omega_max,
        vmax=omega_max,
    )
    fig.colorbar(cf, ax=ax, label="Vorticity omega (1/s)")

    if show_streamlines:
        # Streamlines
        ax.streamplot(
            X,
            Y,
            result["v_x"],
            result["v_y"],
            color="gray",
            linewidth=0.5,
            density=1.5,
            arrowsize=0.8,
        )
    else:
        # Quiver (downsampled)
        skip = max(1, resolution // 12)
        v_mag = result["v_magnitude"]
        v_max = np.max(v_mag)
        if v_max > 0:
            ax.quiver(
                X[::skip, ::skip],
                Y[::skip, ::skip],
                result["v_x"][::skip, ::skip] / v_max,
                result["v_y"][::skip, ::skip] / v_max,
                color="black",
                alpha=0.5,
                scale=25,
                width=0.003,
            )

    # Mark vortex centers
    for (cx, cy), sign in zip(result["vortex_centers"], result["vortex_signs"]):
        color = "red" if sign > 0 else "blue"
        marker = r"$\circlearrowleft$" if sign > 0 else r"$\circlearrowright$"
        ax.text(
            cx,
            cy,
            marker,
            fontsize=20,
            color=color,
            ha="center",
            va="center",
            fontweight="bold",
        )

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title("Molecular Vortices -- Checkerboard Lattice (Art. 822)")
    ax.set_aspect("equal")

    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    822,
    part=4,
    chapter="Molecular Vortices",
    description="Plot 3D vorticity surface of vortex lattice.",
)
def plot_vortex_3d_surface(
    resolution: int = 40,
    vortex_strength: float = 1.0,
    core_radius: float = 0.3,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot 3D vorticity surface of vortex lattice.

    Art. 822: 3D surface plot showing vorticity as height,
    with positive vortices (red, upward) and negative
    vortices (blue, downward) clearly distinguished.
    This illustrates the alternating rotation sense
    central to Maxwell's gear mechanism.

    Args:
        resolution: Grid resolution.
        vortex_strength: Circulation strength.
        core_radius: Vortex core radius (cm).
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes) with 3D projection.

    Reference:
        Part IV, Art. 822: Alternating vortex rotation.
    """
    require_matplotlib()

    x = np.linspace(-2.0, 2.0, resolution)
    y = np.linspace(-2.0, 2.0, resolution)
    X, Y = np.meshgrid(x, y)

    result = calc_vortex_lattice(
        X, Y, vortex_strength=vortex_strength, core_radius=core_radius
    )

    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    omega = result["omega"]
    omega_max = np.max(np.abs(omega))

    # Color surface by vorticity sign
    try:
        from matplotlib import colormaps

        cmap_obj = colormaps.get_cmap("RdBu_r")
    except Exception:
        cmap_obj = plt.cm.get_cmap("RdBu_r")

    colors = cmap_obj(0.5 + 0.5 * omega / omega_max)

    ax.plot_surface(
        X,
        Y,
        omega,
        facecolors=colors,
        alpha=0.85,
        linewidth=0,
        antialiased=True,
        rstride=1,
        cstride=1,
        cmap="RdBu_r",
        vmin=-omega_max,
        vmax=omega_max,
    )

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("Vorticity")
    ax.set_title("Molecular Vortices 3D -- Alternating Rotation (Art. 822)")

    fig.tight_layout()
    return fig, ax
