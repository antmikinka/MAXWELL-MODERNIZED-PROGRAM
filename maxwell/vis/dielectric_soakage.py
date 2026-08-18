"""maxwell.vis.dielectric_soakage -- Dielectric absorption (soakage) visualization.

Implements time-domain visualization of dielectric absorption current decay,
showing the multi-exponential behavior Maxwell described as "electric soakage."

Corresponds to Maxwell's treatment of dielectric absorption in
Part II, Art. 329 (Absorption and Soakage).
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    329,
    part=2,
    chapter="Conduction in Dielectric Media",
    description="Calculate dielectric absorption current as multi-exponential decay.",
)
def calc_dielectric_absorption(
    t: np.ndarray,
    tau: list[float] | None = None,
    A: list[float] | None = None,
) -> np.ndarray:
    """Calculate dielectric absorption current: I(t) = sum(Ai * exp(-t/tau_i)).

    Art. 329: Maxwell's "electric soakage" -- current decays as a sum of
    exponentials with distinct time constants representing slow polarization
    mechanisms within the dielectric.

    Args:
        t: Time array (seconds).
        tau: List of time constants tau_i (seconds). Default: [1.0, 10.0, 100.0].
        A: List of amplitude coefficients A_i (abamperes). Default: [1.0, 0.3, 0.1].

    Returns:
        Absorption current I(t) at each time point, shape same as t.

    Reference:
        Part II, Art. 329: Dielectric absorption theory.
    """
    if tau is None:
        tau = [1.0, 10.0, 100.0]
    if A is None:
        A = [1.0, 0.3, 0.1]

    if len(tau) != len(A):
        raise ValueError("tau and A must have the same length")

    t = np.asarray(t, dtype=np.float64)
    result = np.zeros_like(t, dtype=np.float64)

    for ai, taui in zip(A, tau):
        result += ai * np.exp(-t / taui)

    return result


@maxwell_cite(
    329,
    part=2,
    chapter="Conduction in Dielectric Media",
    description="Plot time-domain absorption current decay with multiple time constants.",
)
def plot_dielectric_soakage(
    tau: list[float] | None = None,
    A: list[float] | None = None,
    t_range: tuple[float, float] = (0.01, 1000.0),
    resolution: int = 500,
    ax: Axes | None = None,
    log_scale: bool = True,
) -> tuple[Figure, Axes]:
    """Plot time-domain absorption current decay with multiple time constants.

    Art. 329: Visualizes dielectric soakage showing the characteristic
    multi-exponential decay. The log-scale view reveals individual
    time constant contributions.

    Args:
        tau: Time constants (seconds). Default: [1.0, 10.0, 100.0].
        A: Amplitude coefficients (abamperes). Default: [1.0, 0.3, 0.1].
        t_range: (t_min, t_max) in seconds.
        resolution: Number of time points.
        ax: Existing axes to plot on (optional).
        log_scale: Use log-log scale (default True, reveals time constants).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part II, Art. 329: Dielectric absorption (electric soakage).
    """
    require_matplotlib()

    if tau is None:
        tau = [1.0, 10.0, 100.0]
    if A is None:
        A = [1.0, 0.3, 0.1]

    t = np.linspace(t_range[0], t_range[1], resolution)
    I_total = calc_dielectric_absorption(t, tau, A)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]

    for i, (taui, ai) in enumerate(zip(tau, A)):
        I_component = ai * np.exp(-t / taui)
        color = colors[i % len(colors)]
        ax.plot(
            t,
            I_component,
            "--",
            color=color,
            linewidth=1.5,
            alpha=0.6,
            label=f"tau={taui:.1f}s (A={ai:.2f})",
        )

    ax.plot(t, I_total, "k-", linewidth=2.5, label="Total current")

    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")

    ax.set_xlabel("Time t (s)")
    ax.set_ylabel("Absorption Current I(t) (abamperes)")
    ax.set_title("Dielectric Soakage -- Absorption Current Decay (Art. 329)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3, which="both")

    for i, taui in enumerate(tau):
        color = colors[i % len(colors)]
        ax.axvline(x=taui, color=color, linestyle=":", alpha=0.4)

    fig.tight_layout()
    return fig, ax
