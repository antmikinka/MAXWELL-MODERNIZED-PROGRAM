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

    In CGS-EMU units, for a wire along the z-axis:

        A_z = -(2 * I / c) * ln(r/r0)

    We use r0 = 1 cm as the reference distance (gauge choice).
    The constant factor 2/c in CGS-EMU gives A_z = -2*I*ln(r).

    Args:
        x: x positions (cm).
        y: y positions (cm).
        z: z positions (cm).
        current: Current in wire (abamperes, CGS-EMU).
        wire_axis: Wire orientation ('x', 'y', or 'z').

    Returns:
        Dictionary with 'A_x', 'A_y', 'A_z' (components),
        'A_magnitude', 'r_cyl' (cylindrical radius).

    Reference:
        Part IV, Art. 540: Electrotonic state for straight conductors.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    # Cylindrical radius (perpendicular distance from wire)
    if wire_axis == "z":
        r_cyl = np.sqrt(x**2 + y**2)
        # A points along z-axis
        A_z = -2.0 * current * np.log(np.maximum(r_cyl, 1e-10))
        A_x = np.zeros_like(x)
        A_y = np.zeros_like(y)
    elif wire_axis == "x":
        r_cyl = np.sqrt(y**2 + z**2)
        A_x = -2.0 * current * np.log(np.maximum(r_cyl, 1e-10))
        A_y = np.zeros_like(y)
        A_z = np.zeros_like(z)
    elif wire_axis == "y":
        r_cyl = np.sqrt(x**2 + z**2)
        A_y = -2.0 * current * np.log(np.maximum(r_cyl, 1e-10))
        A_x = np.zeros_like(x)
        A_z = np.zeros_like(z)
    else:
        raise ValueError("wire_axis must be 'x', 'y', or 'z'")

    A_magnitude = np.sqrt(A_x**2 + A_y**2 + A_z**2)

    return {
        "A_x": A_x,
        "A_y": A_y,
        "A_z": A_z,
        "A_magnitude": A_magnitude,
        "r_cyl": r_cyl,
    }


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

        I(t) = I_f + (I_0 - I_f) * exp(-t/tau)
        A(t) = -(2 * I(t)) * ln(r) * z_hat

    This describes the "extra current" phenomenon Maxwell observed
    during circuit switching -- the induced EMF from changing A.

    Args:
        x: x positions (cm).
        y: y positions (cm).
        current_initial: Initial current (abamperes).
        current_final: Final current (abamperes).
        time_constant: Transient time constant tau (seconds).
        time: Observation time (seconds).

    Returns:
        Dictionary with 'A_z', 'A_magnitude', 'time', 'I_t' (current at time t).

    Reference:
        Part IV, Art. 617: Transient electrotonic state and extra current.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    # Current at time t (exponential rise/decay)
    I_t = current_final + (current_initial - current_final) * np.exp(-time / time_constant)

    r_cyl = np.sqrt(x**2 + y**2)
    A_z = -2.0 * I_t * np.log(np.maximum(r_cyl, 1e-10))
    A_magnitude = np.abs(A_z)

    return {
        "A_z": A_z,
        "A_magnitude": A_magnitude,
        "time": time,
        "I_t": I_t,
    }


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

    For the straight wire case, B should match the Biot-Savart result:
        B_theta = 2*I/r (CGS-EMU)

    Uses central finite differences for numerical curl:
        B_x = dA_z/dy - dA_y/dz
        B_y = dA_x/dz - dA_z/dx
        B_z = dA_y/dx - dA_x/dy

    Args:
        A_func: Function returning (A_x, A_y, A_z) at positions.
        x: 2D or 3D grid of x positions.
        y: 2D or 3D grid of y positions.
        z: 2D or 3D grid of z positions.
        h: Step size for numerical curl.

    Returns:
        Dictionary with 'B_x', 'B_y', 'B_z', 'B_magnitude'.

    Reference:
        Part IV, Art. 540: B = curl(A) relationship.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    # Central differences for curl
    # B_x = dA_z/dy - dA_y/dz
    A_z_plus_y = A_func(x, y + h, z)[2]
    A_z_minus_y = A_func(x, y - h, z)[2]
    A_y_plus_z = A_func(x, y, z + h)[1]
    A_y_minus_z = A_func(x, y, z - h)[1]

    B_x = (A_z_plus_y - A_z_minus_y) / (2 * h) - (A_y_plus_z - A_y_minus_z) / (2 * h)

    # B_y = dA_x/dz - dA_z/dx
    A_x_plus_z = A_func(x, y, z + h)[0]
    A_x_minus_z = A_func(x, y, z - h)[0]
    A_z_plus_x = A_func(x + h, y, z)[2]
    A_z_minus_x = A_func(x - h, y, z)[2]

    B_y = (A_x_plus_z - A_x_minus_z) / (2 * h) - (A_z_plus_x - A_z_minus_x) / (2 * h)

    # B_z = dA_y/dx - dA_x/dy
    A_y_plus_x = A_func(x + h, y, z)[1]
    A_y_minus_x = A_func(x - h, y, z)[1]
    A_x_plus_y = A_func(x, y + h, z)[0]
    A_x_minus_y = A_func(x, y - h, z)[0]

    B_z = (A_y_plus_x - A_y_minus_x) / (2 * h) - (A_x_plus_y - A_x_minus_y) / (2 * h)

    B_magnitude = np.sqrt(B_x**2 + B_y**2 + B_z**2)

    return {
        "B_x": B_x,
        "B_y": B_y,
        "B_z": B_z,
        "B_magnitude": B_magnitude,
    }


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

    For a wire along z-axis, A points along z and its magnitude
    depends only on the perpendicular distance r = sqrt(x^2 + y^2).
    The ln(r) dependence produces the characteristic "funnel" shape.

    Args:
        current: Current in wire (abamperes).
        grid_range: (min, max) spatial range (cm).
        resolution: Grid resolution.
        wire_axis: Wire orientation ('x', 'y', or 'z').
        show_magnitude: Whether to show magnitude contour.
        ax: Existing axes (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part IV, Art. 540: Electrotonic state visualization.
    """
    require_matplotlib()

    x = np.linspace(grid_range[0], grid_range[1], resolution)
    y = np.linspace(grid_range[0], grid_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)  # z = 0 cross-section

    result = calc_electrotonic_straight_wire(X, Y, Z, current=current, wire_axis=wire_axis)

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        fig = ax.figure

    if show_magnitude:
        # Magnitude contour fill
        A_mag = result["A_magnitude"]
        # Clip for visualization (avoid extreme values near wire)
        A_mag_clip = np.clip(A_mag, 0, np.percentile(A_mag, 95))
        cf = ax.contourf(
            X, Y, A_mag_clip,
            levels=30,
            cmap="plasma",
        )
        fig.colorbar(cf, ax=ax, label="|A| (electrotonic state)")

    # A-field contour lines
    A_z = result["A_z"]
    A_z_clip = np.clip(A_z, -np.percentile(np.abs(A_z), 95), np.percentile(np.abs(A_z), 95))
    ax.contour(
        X, Y, A_z_clip,
        levels=15,
        colors="white",
        linewidths=0.5,
        alpha=0.4,
    )

    # Mark wire position
    if wire_axis == "z":
        ax.plot(0, 0, "wo", markersize=12, label="Wire (cross-section)")
    elif wire_axis == "x":
        ax.plot(0, 0, "wo", markersize=12, label="Wire (cross-section)")
    else:
        ax.plot(0, 0, "wo", markersize=12, label="Wire (cross-section)")

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title(
        f"Electrotonic State -- Straight Wire (Art. 540, I={current:.1f})"
    )
    ax.legend(loc="best", fontsize=9)
    ax.set_aspect("equal")

    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    540,
    part=4,
    chapter="Electrotonic State",
    description="Plot A and B vector fields side by side.",
)
def plot_A_and_B_fields(
    current: float = 1.0,
    grid_range: tuple[float, float] = (-2.0, 2.0),
    resolution: int = 30,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot A and B vector fields side by side.

    Art. 540: Demonstrates the relationship between the electrotonic
    state (A-field) and the magnetic induction (B-field) by showing
    both as quiver plots. The curl relationship B = curl(A) is
    visually apparent -- A circulates around the wire while B
    forms closed loops.

    Args:
        current: Current in wire (abamperes).
        grid_range: (min, max) spatial range (cm).
        resolution: Grid resolution.
        ax: Existing axes (optional). If None, creates 1x2 figure.

    Returns:
        Tuple of (Figure, Axes). For the 1x2 case, returns the
        second axes.

    Reference:
        Part IV, Art. 540: B = curl(A) visualization.
    """
    require_matplotlib()

    x = np.linspace(grid_range[0], grid_range[1], resolution)
    y = np.linspace(grid_range[0], grid_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    result = calc_electrotonic_straight_wire(X, Y, Z, current=current)

    # B field from Biot-Savart for straight wire:
    # B_theta = 2*I/r in the azimuthal direction
    r = np.sqrt(X**2 + Y**2)
    r_safe = np.maximum(r, 1e-10)
    B_x = -2.0 * current * Y / r_safe**2  # azimuthal
    B_y = 2.0 * current * X / r_safe**2
    B_mag = np.sqrt(B_x**2 + B_y**2)

    if ax is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig = ax.figure
        ax1 = ax
        ax2 = fig.add_subplot(122) if len(fig.axes) < 2 else fig.axes[1]

    # A-field quiver (A points along z, so show A_z as color + quiver of grad A_z)
    A_z = result["A_z"]
    A_z_clip = np.clip(A_z, -np.percentile(np.abs(A_z), 95), np.percentile(np.abs(A_z), 95))
    cf1 = ax1.contourf(X, Y, A_z_clip, levels=20, cmap="coolwarm")
    fig.colorbar(cf1, ax=ax1, label="A_z")

    # Gradient of A_z (direction of A variation)
    dA_dx, dA_dy = np.gradient(A_z_clip)
    skip = max(1, resolution // 10)
    ax1.quiver(
        X[::skip, ::skip], Y[::skip, ::skip],
        dA_dx[::skip, ::skip], dA_dy[::skip, ::skip],
        color="white", alpha=0.6, scale=30, width=0.003,
    )
    ax1.set_title("A-Field (Electrotonic State)")
    ax1.set_xlabel("x (cm)")
    ax1.set_ylabel("y (cm)")
    ax1.set_aspect("equal")

    # B-field quiver
    B_mag_clip = np.clip(B_mag, 0, np.percentile(B_mag, 95))
    cf2 = ax2.contourf(X, Y, B_mag_clip, levels=20, cmap="viridis")
    fig.colorbar(cf2, ax=ax2, label="|B|")

    B_x_norm = B_x / np.maximum(B_mag, 1e-10)
    B_y_norm = B_y / np.maximum(B_mag, 1e-10)
    ax2.quiver(
        X[::skip, ::skip], Y[::skip, ::skip],
        B_x_norm[::skip, ::skip], B_y_norm[::skip, ::skip],
        color="white", alpha=0.6, scale=25, width=0.003,
    )
    ax2.set_title("B-Field (Magnetic Induction)")
    ax2.set_xlabel("x (cm)")
    ax2.set_ylabel("y (cm)")
    ax2.set_aspect("equal")

    fig.suptitle("A and B Fields -- Electrotonic State (Art. 540)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig, ax2


@maxwell_cite(
    617,
    part=4,
    chapter="Electrotonic State",
    description="Plot time evolution of electrotonic state during transient.",
)
def plot_A_transient(
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

    The "extra current" effect -- the induced EMF from dA/dt --
    is what Maxwell observed when opening/closing circuits.

    Args:
        current_initial: Initial current (abamperes).
        current_final: Final current (abamperes).
        time_constant: Transient time constant tau (seconds).
        time_range: (t_min, t_max) in seconds.
        observation_points: List of (x, y) observation positions.
            Default: [(0.5, 0), (1.0, 0), (2.0, 0)].
        fig: Existing figure (optional).

    Returns:
        Tuple of (Figure, list[Axes]).

    Reference:
        Part IV, Art. 617: Transient electrotonic state.
    """
    require_matplotlib()

    if observation_points is None:
        observation_points = [(0.5, 0.0), (1.0, 0.0), (2.0, 0.0)]

    t = np.linspace(time_range[0], time_range[1], 200)

    colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ff7f00", "#984ea3"]

    if fig is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    else:
        axes = fig.axes
        ax1, ax2 = axes[0], axes[1]

    # Panel 1: A(t) at observation points
    for idx, (px, py) in enumerate(observation_points):
        A_t = []
        for ti in t:
            result = calc_electrotonic_transient(
                np.array([px]), np.array([py]),
                current_initial=current_initial,
                current_final=current_final,
                time_constant=time_constant,
                time=ti,
            )
            A_t.append(result["A_magnitude"][0])
        A_t = np.array(A_t)

        color = colors[idx % len(colors)]
        r_str = f"r={np.sqrt(px**2+py**2):.1f}"
        ax1.plot(t, A_t, color=color, linewidth=2, label=r_str)

    ax1.set_xlabel("Time t (s)")
    ax1.set_ylabel("|A| (electrotonic state)")
    ax1.set_title("Electrotonic State vs Time (Art. 617)")
    ax1.legend(loc="best", fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Current I(t)
    I_t = current_final + (current_initial - current_final) * np.exp(-t / time_constant)
    ax2.plot(t, I_t, color="#e41a1c", linewidth=2, label="I(t)")
    ax2.axhline(y=current_final, color="gray", linestyle="--", linewidth=1,
                label=f"Final: {current_final}")
    ax2.axhline(y=current_initial, color="gray", linestyle=":", linewidth=1,
                label=f"Initial: {current_initial}")

    # Mark time constant
    I_at_tau = current_final + (current_initial - current_final) * np.exp(-1)
    ax2.plot(time_constant, I_at_tau, "ko", markersize=8, label=f"tau={time_constant}s")

    ax2.set_xlabel("Time t (s)")
    ax2.set_ylabel("Current I (abamperes)")
    ax2.set_title("Current Transient (Art. 617)")
    ax2.legend(loc="best", fontsize=9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Electrotonic State Transient (Art. 617)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig, [ax1, ax2]


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
        current: Current in wire (abamperes).
        resolution: Grid resolution.
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes) with 3D projection.

    Reference:
        Part IV, Art. 540: Electrotonic state 3D structure.
    """
    require_matplotlib()

    x = np.linspace(-2.0, 2.0, resolution)
    y = np.linspace(-2.0, 2.0, resolution)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    result = calc_electrotonic_straight_wire(X, Y, Z, current=current)
    A_mag = result["A_magnitude"]

    # Clip for visualization
    A_mag_clip = np.clip(A_mag, 0, np.percentile(A_mag, 98))

    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    try:
        from matplotlib import colormaps
        cmap_obj = colormaps.get_cmap("plasma")
    except Exception:
        cmap_obj = plt.cm.get_cmap("plasma")

    A_max = np.max(A_mag_clip)
    colors = cmap_obj(0.5 * A_mag_clip / np.maximum(A_max, 1e-10))

    ax.plot_surface(
        X, Y, A_mag_clip,
        facecolors=colors,
        alpha=0.85,
        linewidth=0,
        antialiased=True,
        rstride=1,
        cstride=1,
        cmap="plasma",
        vmin=0,
        vmax=A_max,
    )

    # Mark wire position
    ax.plot([0], [0], [0], "ko", markersize=8, label="Wire")

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_zlabel("|A| (electrotonic state)")
    ax.set_title(f"3D Electrotonic State (Art. 540, I={current:.1f})")
    ax.legend(loc="best")

    fig.tight_layout()
    return fig, ax
