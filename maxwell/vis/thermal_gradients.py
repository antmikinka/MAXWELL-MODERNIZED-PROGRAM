"""maxwell.vis.thermal_gradients -- Thermal gradients and Joule heating visualization.

Implements 2D visualization of heat conduction with Joule heating sources,
spatial power dissipation maps, and thermoelectric Peltier effects at junctions.

Corresponds to Maxwell's treatment of heat generation by current and
thermoelectric phenomena in
Part II, Art. 242 (Generation of Heat by Current) and Art. 249 (Peltier's Phenomenon).
"""

from __future__ import annotations

import numpy as np

from maxwell.vis._compat import require_matplotlib, plt, Figure, Axes
from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@maxwell_cite(
    242,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Calculate spatial Joule heating power density distribution.",
)
def calc_joule_heat_distribution(
    E_x: np.ndarray,
    E_y: np.ndarray,
    sigma: float = 5.8e17,
) -> np.ndarray:
    """Calculate spatial Joule heating power density: p = sigma * |E|^2.

    Art. 242: The volumetric rate of heat generation in a conductor is
    proportional to the square of the electric field and the conductivity:

        p(x,y) = sigma * (E_x^2 + E_y^2)  [erg/(cm^3 s)]

    This is the field-theoretic form of Joule's law P = I^2 * R.

    Args:
        E_x: Electric field x-component (statvolt/cm).
        E_y: Electric field y-component (statvolt/cm).
        sigma: Electrical conductivity (esu/s = cm/s in CGS).
               Default: copper ~5.8e17 esu/s.

    Returns:
        Power density p(x,y) in erg/(cm^3 s), same shape as inputs.

    Reference:
        Part II, Art. 242: Joule's law for heat generation.
    """
    E_x = np.asarray(E_x, dtype=np.float64)
    E_y = np.asarray(E_y, dtype=np.float64)
    return sigma * (E_x**2 + E_y**2)


@maxwell_cite(
    242,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Calculate 2D steady-state temperature field with Joule heating source.",
)
def calc_thermal_gradients(
    x: np.ndarray,
    y: np.ndarray,
    sigma: float = 5.8e17,
    k_thermal: float = 4.01e7,
    E0: float = 1e-8,
    T_boundary: float = 300.0,
    geometry: str = "rectangular",
) -> dict[str, np.ndarray]:
    """Calculate 2D steady-state temperature field with Joule heating.

    Art. 242 & 243: Solves the Poisson equation for steady-state heat
    conduction with internal heat generation from Joule heating:

        k_thermal * nabla^2 T + sigma * |E|^2 = 0

    For a rectangular conductor with uniform E field:
        T(x,y) = T_boundary + (sigma * E0^2 / (2 * k_thermal)) * (L^2/4 - x^2 + W^2/4 - y^2)

    The temperature profile is parabolic, maximum at the center.

    Args:
        x: 2D grid of x positions (cm).
        y: 2D grid of y positions (cm).
        sigma: Electrical conductivity (esu/s). Default: copper.
        k_thermal: Thermal conductivity (erg/(cm s K)). Default: copper ~4.01e7.
        E0: Applied electric field magnitude (statvolt/cm).
        T_boundary: Boundary temperature (K).
        geometry: 'rectangular' or 'circular' cross-section.

    Returns:
        Dictionary with 'T' (temperature field), 'T_max', 'dT' (temperature rise),
        'q_x', 'q_y' (heat flux components), 'p' (power density).

    Reference:
        Part II, Arts. 242-243: Heat conduction analogy with electricity.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    L = 2.0  # Half-width (cm)
    W = 1.0  # Half-height (cm)

    # Joule heating power density (uniform for uniform E field)
    p = sigma * E0**2

    if geometry == "rectangular":
        # Parabolic temperature profile for rectangular cross-section
        # T = T_boundary + (p / (2*k)) * (L^2 - x^2 + W^2 - y^2) / 2
        dT = (p / (2.0 * k_thermal)) * ((L**2 - x**2) + (W**2 - y**2)) / 2.0
    elif geometry == "circular":
        # Parabolic profile for circular cross-section (radius R)
        R = 1.0
        r2 = x**2 + y**2
        mask = r2 <= R**2
        dT = np.zeros_like(x)
        dT[mask] = (p / (4.0 * k_thermal)) * (R**2 - r2[mask])
    else:
        raise ValueError("geometry must be 'rectangular' or 'circular'")

    T = T_boundary + dT
    T_max = np.max(T)

    # Heat flux: q = -k_thermal * grad(T)
    dx = x[0, 1] - x[0, 0] if x.shape[1] > 1 else 1.0
    dy = y[1, 0] - y[0, 0] if y.shape[0] > 1 else 1.0
    q_x = -k_thermal * np.gradient(T, dx, axis=1)
    q_y = -k_thermal * np.gradient(T, dy, axis=0)

    return {
        "T": T,
        "T_max": T_max,
        "dT": dT,
        "q_x": q_x,
        "q_y": q_y,
        "p": p,
    }


@maxwell_cite(
    249,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Calculate Peltier thermoelectric EMF at a metal junction.",
)
def calc_peltier_junction(
    dT: np.ndarray,
    material_A: str = "copper",
    material_B: str = "iron",
) -> dict[str, np.ndarray]:
    """Calculate Peltier thermoelectric EMF at a junction of two metals.

    Art. 249: When two dissimilar metals are joined and their junctions
    are held at different temperatures, an electromotive force is generated:

        EMF = Pi_AB * delta_T / T_junction

    where Pi_AB is the Peltier coefficient for the A-B junction.
    The Peltier coefficient relates to the Seebeck coefficient: Pi_AB = S_AB * T.

    Materials and their approximate Seebeck coefficients (statvolt/K):
        copper:  +1.8e-6 V/K = 6.0e-15 statvolt/K
        iron:    +15.0e-6 V/K = 5.0e-14 statvolt/K
        constantan: -35.0e-6 V/K = -1.17e-13 statvolt/K
        chromel:  +22.0e-6 V/K = 7.3e-14 statvolt/K

    Args:
        dT: Temperature difference across junction (K).
        material_A: First material name.
        material_B: Second material name.

    Returns:
        Dictionary with 'EMF' (thermoelectric EMF in statvolts),
        'Pi_AB' (Peltier coefficient in erg/esu), 'S_A', 'S_B' (Seebeck coeffs).

    Reference:
        Part II, Art. 249: Peltier's phenomenon and thermoelectric EMF.
    """
    # Seebeck coefficients in statvolt/K (1 V = 1/299.792458 statvolt)
    c_light = CONST.C / 1e8  # Speed of light factor for V -> statvolt conversion
    seebeck_coeffs = {
        "copper": 1.8e-6 / c_light,
        "iron": 15.0e-6 / c_light,
        "constantan": -35.0e-6 / c_light,
        "chromel": 22.0e-6 / c_light,
        "aluminum": 1.5e-6 / c_light,
        "gold": 1.5e-6 / c_light,
    }

    if material_A not in seebeck_coeffs:
        raise ValueError(f"Unknown material: {material_A}")
    if material_B not in seebeck_coeffs:
        raise ValueError(f"Unknown material: {material_B}")

    S_A = seebeck_coeffs[material_A]
    S_B = seebeck_coeffs[material_B]
    S_AB = S_B - S_A

    # Peltier coefficient: Pi_AB = S_AB * T (at reference T = 300 K)
    T_ref = 300.0
    Pi_AB = S_AB * T_ref

    dT = np.asarray(dT, dtype=np.float64)
    EMF = S_AB * dT

    return {
        "EMF": EMF,
        "Pi_AB": Pi_AB,
        "S_A": S_A,
        "S_B": S_B,
        "S_AB": S_AB,
    }


@maxwell_cite(
    242,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Plot 2D temperature field with heat flux vectors and Joule heating.",
)
def plot_thermal_gradients(
    sigma: float = 5.8e17,
    k_thermal: float = 4.01e7,
    E0: float = 1e-8,
    T_boundary: float = 300.0,
    geometry: str = "rectangular",
    resolution: int = 50,
    show_flux: bool = True,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot 2D temperature field with heat flux vectors and Joule heating.

    Art. 242 & 243: Visualizes the steady-state temperature distribution
    in a conductor with Joule heating. Shows:
    - Temperature contour map (color-filled)
    - Heat flux vectors (arrows showing direction of heat flow)
    - Hot spot location (typically center for symmetric geometries)
    - Boundary conditions (fixed temperature at edges)

    Args:
        sigma: Electrical conductivity (esu/s). Default: copper.
        k_thermal: Thermal conductivity (erg/(cm s K)). Default: copper.
        E0: Applied electric field (statvolt/cm).
        T_boundary: Boundary temperature (K).
        geometry: 'rectangular' or 'circular'.
        resolution: Grid resolution.
        show_flux: Whether to overlay heat flux arrows.
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part II, Arts. 242-243: Heat conduction with Joule heating.
    """
    require_matplotlib()

    x = np.linspace(-1.5, 1.5, resolution)
    y = np.linspace(-0.75, 0.75, resolution)
    X, Y = np.meshgrid(x, y)

    result = calc_thermal_gradients(
        X, Y, sigma=sigma, k_thermal=k_thermal,
        E0=E0, T_boundary=T_boundary, geometry=geometry,
    )

    T = result["T"]
    dT = result["dT"]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    # Temperature contour fill
    cf = ax.contourf(
        X, Y, T,
        levels=30,
        cmap="hot",
        vmin=T_boundary,
        vmax=result["T_max"],
    )
    fig.colorbar(cf, ax=ax, label="Temperature T (K)")

    # Temperature contour lines
    contours = ax.contour(
        X, Y, T,
        levels=10,
        colors="white",
        linewidths=0.5,
        alpha=0.5,
    )
    ax.clabel(contours, inline=True, fontsize=7, fmt="%.1f")

    # Heat flux vectors (downsampled for clarity)
    if show_flux:
        skip = max(1, resolution // 15)
        q_x = result["q_x"]
        q_y = result["q_y"]
        q_mag = np.sqrt(q_x**2 + q_y**2)
        q_mag_max = np.max(q_mag)
        if q_mag_max > 0:
            q_x_norm = q_x / q_mag_max
            q_y_norm = q_y / q_mag_max
            ax.quiver(
                X[::skip, ::skip], Y[::skip, ::skip],
                q_x_norm[::skip, ::skip], q_y_norm[::skip, ::skip],
                color="cyan", alpha=0.6, scale=20, width=0.003,
                label="Heat flux direction",
            )

    # Mark hot spot
    hot_idx = np.unravel_index(np.argmax(T), T.shape)
    ax.plot(X[hot_idx], Y[hot_idx], "w*", markersize=15, label=f"Hot spot: {T[hot_idx]:.1f} K")

    # Geometry outline
    if geometry == "rectangular":
        rect = plt.Rectangle((-1.5, -0.75), 3.0, 1.5, fill=False,
                            edgecolor="white", linewidth=2, linestyle="--")
        ax.add_patch(rect)
    elif geometry == "circular":
        circle = plt.Circle((0, 0), 1.0, fill=False,
                          edgecolor="white", linewidth=2, linestyle="--")
        ax.add_patch(circle)

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title(
        f"Thermal Gradients with Joule Heating (Art. 242, {geometry.capitalize()})"
    )
    if show_flux:
        ax.legend(loc="best", fontsize=8)
    ax.set_aspect("equal")

    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    242,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Plot spatial Joule heating power density distribution.",
)
def plot_joule_heat_distribution(
    sigma: float = 5.8e17,
    E0: float = 1e-8,
    geometry: str = "nonuniform",
    resolution: int = 50,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot spatial Joule heating power density distribution.

    Art. 242: Visualizes how heat generation varies spatially in a
    conductor. For a non-uniform cross-section (e.g., a wire with a
    constriction), the E field concentrates at the narrow point,
    causing localized heating hot spots:

        p(x,y) = sigma * |E(x,y)|^2

    This explains why fuses blow at their narrowest point and why
    PCB traces heat up most at sharp corners.

    Args:
        sigma: Electrical conductivity (esu/s). Default: copper.
        E0: Base electric field magnitude (statvolt/cm).
        geometry: 'uniform' or 'nonuniform' (constriction).
        resolution: Grid resolution.
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part II, Art. 242: Joule's law, heat generation by current.
    """
    require_matplotlib()

    x = np.linspace(-2.0, 2.0, resolution)
    y = np.linspace(-1.0, 1.0, resolution)
    X, Y = np.meshgrid(x, y)

    if geometry == "uniform":
        # Uniform E field
        E_x = np.full_like(X, E0)
        E_y = np.zeros_like(Y)
    elif geometry == "nonuniform":
        # Constriction: E field enhanced at center narrow region
        # Model: current crowding at a constriction point
        r = np.sqrt(X**2 + Y**2)
        # Base field plus constriction enhancement
        E_x = E0 * (1.0 + 3.0 * np.exp(-r**2 / 0.5))
        E_y = E0 * 0.5 * (X / (r + 0.1)) * np.exp(-r**2 / 0.5)
    else:
        raise ValueError("geometry must be 'uniform' or 'nonuniform'")

    p = calc_joule_heat_distribution(E_x, E_y, sigma=sigma)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    vmax = np.max(p)
    cf = ax.contourf(
        X, Y, p,
        levels=30,
        cmap="YlOrRd",
        vmin=0,
        vmax=vmax,
    )
    fig.colorbar(cf, ax=ax, label="Power Density p (erg/(cm^3 s))")

    # Contour lines
    ax.contour(X, Y, p, levels=10, colors="black", linewidths=0.5, alpha=0.3)

    # Constriction outline for non-uniform case
    if geometry == "nonuniform":
        # Draw conductor shape with constriction
        x_edge = np.linspace(-2.0, 2.0, 100)
        y_top = 0.5 + 0.3 * np.exp(-x_edge**2 / 0.5)
        y_bottom = -y_top
        ax.plot(x_edge, y_top, "k-", linewidth=2, label="Conductor boundary")
        ax.plot(x_edge, y_bottom, "k-", linewidth=2)

    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title(
        f"Joule Heat Distribution (Art. 242, {geometry.capitalize()})"
    )
    ax.set_aspect("equal")

    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    249,
    part=2,
    chapter="Conduction in Linear Conductors",
    description="Plot thermoelectric EMF and Peltier effect visualization.",
)
def plot_thermoelectric_effects(
    dT_range: tuple[float, float] = (0.0, 100.0),
    resolution: int = 100,
    material_pairs: list[tuple[str, str]] | None = None,
    fig: Figure | None = None,
) -> tuple[Figure, list[Axes]]:
    """Plot thermoelectric EMF and Peltier effect visualization.

    Art. 249: Two-panel visualization of thermoelectric phenomena:

    Panel 1: Thermoelectric EMF vs temperature difference for various
    material pairs (Seebeck effect). The linear relationship
    EMF = S_AB * delta_T demonstrates the direct conversion of
    thermal gradients to electrical potential.

    Panel 2: Peltier coefficient comparison across material pairs.
    Shows which combinations produce the strongest heating/cooling
    at junctions when current flows.

    Common thermocouple types:
        Type J: Iron-Constantan (high sensitivity)
        Type K: Chromel-Aluminum (widely used)
        Type T: Copper-Constantan (low temperature)

    Args:
        dT_range: (dT_min, dT_max) temperature difference range (K).
        resolution: Number of dT points.
        material_pairs: List of (material_A, material_B) pairs.
            Default: common thermocouple combinations.
        fig: Existing figure to use (optional).

    Returns:
        Tuple of (Figure, list[Axes]).

    Reference:
        Part II, Art. 249: Peltier's phenomenon and thermoelectric EMF.
    """
    require_matplotlib()

    if material_pairs is None:
        material_pairs = [
            ("copper", "iron"),
            ("copper", "constantan"),
            ("iron", "constantan"),
            ("chromel", "aluminum"),
        ]

    dT = np.linspace(dT_range[0], dT_range[1], resolution)

    pair_colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ff7f00", "#984ea3", "#a65628"]

    if fig is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    else:
        axes = fig.axes
        ax1, ax2 = axes[0], axes[1]

    # Panel 1: EMF vs dT (Seebeck effect)
    for idx, (mat_A, mat_B) in enumerate(material_pairs):
        result = calc_peltier_junction(dT, mat_A, mat_B)
        color = pair_colors[idx % len(pair_colors)]
        ax1.plot(dT, result["EMF"], color=color, linewidth=2,
                label=f"{mat_A.title()}-{mat_B.title()}")

    ax1.set_xlabel("Temperature Difference dT (K)")
    ax1.set_ylabel("Thermoelectric EMF (statvolts)")
    ax1.set_title("Seebeck Effect: EMF vs Temperature Difference (Art. 249)")
    ax1.legend(loc="best", fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color="k", linestyle="-", linewidth=0.5)

    # Panel 2: Peltier coefficient bar chart
    pair_names = []
    pi_values = []
    for mat_A, mat_B in material_pairs:
        result = calc_peltier_junction(np.array([1.0]), mat_A, mat_B)
        pair_names.append(f"{mat_A[:3]}-{mat_B[:3]}")
        pi_values.append(result["Pi_AB"])

    colors_bar = [pair_colors[i % len(pair_colors)] for i in range(len(pi_values))]
    bars = ax2.barh(pair_names, pi_values, color=colors_bar, alpha=0.7)

    for bar, val in zip(bars, pi_values):
        ax2.text(val, bar.get_y() + bar.get_height() / 2,
                f"{val:.2e}", va="center", ha="left" if val > 0 else "right",
                fontsize=8)

    ax2.set_xlabel("Peltier Coefficient Pi_AB (erg/esu)")
    ax2.set_title("Peltier Coefficients at 300 K (Art. 249)")
    ax2.axvline(x=0, color="k", linestyle="-", linewidth=0.5)
    ax2.grid(True, alpha=0.3, axis="x")

    fig.suptitle("Thermoelectric Effects (Arts. 242, 249)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig, [ax1, ax2]
