"""maxwell.vis.hysteresis_loops -- Magnetic hysteresis loop visualization.

Implements B-H hysteresis loop plotting with labeled coercivity and retentivity,
material comparison, and loop area shading.

Corresponds to Maxwell's treatment of magnetic hysteresis in
Part III, Arts. 442-446 (Magnetic Hysteresis).
"""

from __future__ import annotations

import numpy as np

from maxwell.materials.hysteresis import (
    generate_theoretical_hysteresis_loop,
)
from maxwell.meta.citation import maxwell_cite
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    442,
    part=3,
    chapter="Magnetic Hysteresis",
    description="Generate B-H hysteresis loop from physical parameters.",
)
def calc_hysteresis_loop(
    H_max: float,
    mu_r: float,
    alpha: float,
    n_points: int = 500,
) -> dict[str, np.ndarray]:
    """Generate B-H loop using a Jiles-Atherton inspired model.

    Art. 442-446: Maxwell theory of magnetic hysteresis describes
    the lag of magnetization behind the applied field, creating a
    closed loop with retentivity and coercivity.

    This wraps generate_theoretical_hysteresis_loop with physically
    intuitive parameters.

    Args:
        H_max: Maximum applied field (gauss).
        mu_r: Relative permeability (dimensionless).
        alpha: Hysteresis coupling parameter (dimensionless, ~0.001).
        n_points: Number of points per branch.

    Returns:
        Dictionary with H_values, B_values, H_branch1, B_branch1, H_branch2, B_branch2.

    Reference:
        Part III, Arts. 442-446: Magnetic hysteresis theory.
    """
    I_s = mu_r * H_max * 0.1
    H_c = alpha * H_max
    kappa_initial = mu_r * 0.01

    raw = generate_theoretical_hysteresis_loop(
        I_s=max(I_s, 1.0),
        H_c=max(H_c, 0.1),
        kappa_initial=max(kappa_initial, 0.001),
        n_points=n_points,
    )

    H_branch1 = raw["H_branch1"]
    I_branch1 = raw["I_branch1"]
    H_branch2 = raw["H_branch2"]
    I_branch2 = raw["I_branch2"]
    H_full = raw["H_full"]
    I_full = raw["I_full"]

    mu0 = 1.0
    B_branch1 = mu0 * (H_branch1 + I_branch1)
    B_branch2 = mu0 * (H_branch2 + I_branch2)
    B_full = mu0 * (H_full + I_full)

    return {
        "H_values": H_full,
        "B_values": B_full,
        "H_branch1": H_branch1,
        "B_branch1": B_branch1,
        "H_branch2": H_branch2,
        "B_branch2": B_branch2,
        "H_max_input": H_max,
    }


@maxwell_cite(
    442,
    part=3,
    chapter="Magnetic Hysteresis",
    description="Plot B-H hysteresis loop with labeled retentivity/coercivity.",
)
def plot_hysteresis_loops(
    H_max: float = 1000.0,
    mu_r: float = 1000.0,
    alpha: float = 0.001,
    ax: Axes | None = None,
    show_coercivity: bool = True,
    show_retentivity: bool = True,
) -> tuple[Figure, Axes]:
    """Plot B-H hysteresis loop with labeled retentivity/coercivity.

    Art. 442-446: Visualizes the complete hysteresis loop with B-H curve,
    labeled coercive field H_c, labeled retentivity B_r, and shaded loop
    area representing energy loss per cycle.

    Args:
        H_max: Maximum applied field (gauss).
        mu_r: Relative permeability.
        alpha: Hysteresis coupling parameter.
        ax: Existing axes to plot on (optional).
        show_coercivity: Annotate coercive force point.
        show_retentivity: Annotate retentivity point.

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part III, Arts. 442-446: Magnetic hysteresis.
    """
    require_matplotlib()

    loop_data = calc_hysteresis_loop(H_max, mu_r, alpha)
    H = loop_data["H_values"]
    B = loop_data["B_values"]
    H_asc = loop_data["H_branch1"]
    B_asc = loop_data["B_branch1"]
    H_desc = loop_data["H_branch2"]
    B_desc = loop_data["B_branch2"]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 7))
    else:
        fig = ax.figure

    ax.plot(H_asc, B_asc, "b-", linewidth=2, label="Ascending branch")
    ax.plot(H_desc, B_desc, "r-", linewidth=2, label="Descending branch")

    H_min, H_max_val = H.min(), H.max()
    B_max_val = max(abs(B.min()), abs(B.max()))

    upper = np.maximum(B_asc, B_desc)
    lower = np.minimum(B_asc, B_desc)

    H_common = np.linspace(H_min, H_max_val, 200)
    upper_interp = np.interp(H_common, H_asc, upper)
    lower_interp = np.interp(H_common, H_desc, lower)
    ax.fill_between(
        H_common,
        lower_interp,
        upper_interp,
        alpha=0.2,
        color="gray",
        label="Energy loss area",
    )

    idx_B_zero_asc = np.argmin(np.abs(B_asc))
    H_c_est = H_asc[idx_B_zero_asc]
    idx_H_zero_asc = np.argmin(np.abs(H_asc))
    B_r_est = B_asc[idx_H_zero_asc]

    if show_coercivity:
        ax.plot(H_c_est, 0, "ro", markersize=10, zorder=5)
        ax.annotate(
            "H_c = {:.1f} G".format(H_c_est),
            xy=(H_c_est, 0),
            xytext=(H_c_est, -B_max_val * 0.15),
            ha="center",
            fontsize=10,
            color="red",
            arrowprops=dict(arrowstyle="->", color="red"),
        )

    if show_retentivity:
        ax.plot(0, B_r_est, "go", markersize=10, zorder=5)
        ax.annotate(
            "B_r = {:.1f}".format(B_r_est),
            xy=(0, B_r_est),
            xytext=(H_max_val * 0.15, B_r_est),
            va="center",
            fontsize=10,
            color="green",
            arrowprops=dict(arrowstyle="->", color="green"),
        )

    ax.axhline(y=0, color="black", linewidth=0.5, alpha=0.5)
    ax.axvline(x=0, color="black", linewidth=0.5, alpha=0.5)

    ax.set_xlabel("Applied Field H (gauss)")
    ax.set_ylabel("Flux Density B")
    ax.set_title("Magnetic Hysteresis Loop -- B-H Curve (Arts. 442-446)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    444,
    part=3,
    chapter="Magnetic Hysteresis",
    description="Compare hysteresis loops for soft iron, steel, and permanent magnet materials.",
)
def plot_material_comparison(
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Compare hysteresis loops for soft iron, steel, and permanent magnet materials.

    Art. 444-446: Maxwell cataloged magnetic properties of various substances.
    This plot overlays loops for representative materials to show the range
    from soft magnetic (narrow loop) to hard magnetic (wide loop).

    Materials compared:
    - Electrical steel (medium coercivity)
    - Iron pure (soft, narrow loop)
    - Alnico 5 (hard, wide loop)

    Args:
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part III, Arts. 444-446: Material magnetic properties.
    """
    require_matplotlib()

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    else:
        fig = ax.figure

    materials = {
        "Electrical Steel (soft)": {
            "H_max": 100,
            "mu_r": 4000,
            "alpha": 0.005,
            "color": "#377eb8",
        },
        "Iron Pure (soft)": {
            "H_max": 50,
            "mu_r": 5000,
            "alpha": 0.002,
            "color": "#4daf4a",
        },
        "Alnico 5 (hard)": {
            "H_max": 1000,
            "mu_r": 20,
            "alpha": 0.6,
            "color": "#e41a1c",
        },
    }

    for name, params in materials.items():
        loop_data = calc_hysteresis_loop(
            H_max=params["H_max"],
            mu_r=params["mu_r"],
            alpha=params["alpha"],
            n_points=300,
        )
        H = loop_data["H_values"]
        B = loop_data["B_values"]

        B_norm = B / np.max(np.abs(B)) if np.max(np.abs(B)) > 0 else B
        H_norm = H / params["H_max"] if params["H_max"] > 0 else H

        ax.plot(H_norm, B_norm, "-", color=params["color"], linewidth=2, label=name)

    ax.axhline(y=0, color="black", linewidth=0.5, alpha=0.5)
    ax.axvline(x=0, color="black", linewidth=0.5, alpha=0.5)

    ax.set_xlabel("Normalized Applied Field H/H_max")
    ax.set_ylabel("Normalized Flux Density B/B_max")
    ax.set_title("Hysteresis Loop Material Comparison (Arts. 444-446)")
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig, ax
