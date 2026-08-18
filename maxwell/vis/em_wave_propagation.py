"""maxwell.vis.em_wave_propagation -- Electromagnetic wave propagation visualization.

Implements 2D and 3D visualization of plane electromagnetic wave propagation,
showing orthogonal E/B fields and polarization states.

Corresponds to Maxwell's electromagnetic theory of light in
Part IV, Art. 791 (Electromagnetic Theory of Light).
"""

from __future__ import annotations

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    791,
    part=4,
    chapter="Electromagnetic Theory of Light",
    description="Calculate E and B fields for plane wave propagation.",
)
def calc_em_wave(
    x: np.ndarray,
    t: float,
    omega: float,
    k: float,
    E0: float,
    polarization: str = "linear",
) -> dict[str, np.ndarray]:
    """Calculate E and B fields for plane wave propagation.

    Art. 791: For a plane electromagnetic wave propagating in +z direction:

        E_x(z,t) = E0 * cos(k*z - omega*t)          (linear)
        E_y(z,t) = E0 * cos(k*z - omega*t + delta)   (polarization-dependent)
        B = (1/c) * k_hat x E

    Polarization states:
    - linear: E oscillates along x-axis only
    - circular_right: E_x = E_y with +90-degree phase difference
    - circular_left: E_x = E_y with -90-degree phase difference
    - elliptical: General case with arbitrary amplitude ratio and phase

    Args:
        x: Spatial positions along propagation axis (cm).
        t: Time instant (s).
        omega: Angular frequency (rad/s).
        k: Wave number (cm^-1).
        E0: Electric field amplitude (statvolts/cm).
        polarization: 'linear', 'circular_right', 'circular_left', or 'elliptical'.

    Returns:
        Dictionary with:
        - E_x, E_y, E_z: Electric field components
        - B_x, B_y, B_z: Magnetic field components
        - E_magnitude, B_magnitude: Field magnitudes

    Reference:
        Part IV, Art. 791: Electromagnetic wave theory.
    """
    x = np.asarray(x, dtype=np.float64)
    phase = k * x - omega * t

    if polarization == "linear":
        E_x = E0 * np.cos(phase)
        E_y = np.zeros_like(x)
    elif polarization == "circular_right":
        E_x = E0 * np.cos(phase)
        E_y = E0 * np.sin(phase)
    elif polarization == "circular_left":
        E_x = E0 * np.cos(phase)
        E_y = -E0 * np.sin(phase)
    elif polarization == "elliptical":
        E_x = E0 * np.cos(phase)
        E_y = E0 * 0.5 * np.sin(phase)
    else:
        raise ValueError(
            "polarization must be linear, circular_right, circular_left, or elliptical"
        )

    E_z = np.zeros_like(x)

    c = CONST.C
    B_x = -E_y / c
    B_y = E_x / c
    B_z = np.zeros_like(x)

    E_magnitude = np.sqrt(E_x**2 + E_y**2 + E_z**2)
    B_magnitude = np.sqrt(B_x**2 + B_y**2 + B_z**2)

    return {
        "E_x": E_x,
        "E_y": E_y,
        "E_z": E_z,
        "B_x": B_x,
        "B_y": B_y,
        "B_z": B_z,
        "E_magnitude": E_magnitude,
        "B_magnitude": B_magnitude,
    }


@maxwell_cite(
    791,
    part=4,
    chapter="Electromagnetic Theory of Light",
    description="Plot E and B field propagation showing orthogonal wave nature.",
)
def plot_em_wave_propagation(
    omega: float = 2 * np.pi,
    E0: float = 1.0,
    polarization: str = "linear",
    x_range: tuple[float, float] = (0.0, 4 * np.pi),
    resolution: int = 200,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot E and B field propagation showing orthogonal wave nature.

    Art. 791: Visualizes the propagating electromagnetic wave with:
    - E field (red) and B field (blue) on separate subplots
    - Orthogonal relationship: E perpendicular to B, both perpendicular to propagation
    - Wave speed c = omega/k verification
    - Polarization state visualization

    Args:
        omega: Angular frequency (rad/s). Default: 2*pi (1 Hz).
        E0: Electric field amplitude (statvolts/cm).
        polarization: 'linear', 'circular_right', 'circular_left', 'elliptical'.
        x_range: (x_min, x_max) propagation distance (cm).
        resolution: Number of spatial points.
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes) or (Figure, list[Axes]) for multi-panel.

    Reference:
        Part IV, Art. 791: Electromagnetic wave propagation.
    """
    require_matplotlib()

    k = omega / CONST.C
    x = np.linspace(x_range[0], x_range[1], resolution)
    fields = calc_em_wave(x, t=0.0, omega=omega, k=k, E0=E0, polarization=polarization)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(x, fields["E_x"], "r-", linewidth=1.5, label="E_x")
    if np.max(np.abs(fields["E_y"])) > 1e-15:
        ax1.plot(x, fields["E_y"], "g--", linewidth=1.5, label="E_y")
    ax1.set_ylabel("Electric Field E (statvolt/cm)")
    ax1.set_title("EM Wave Propagation -- E Field (Art. 791)")
    ax1.legend(loc="best", fontsize=9)
    ax1.grid(True, alpha=0.3)

    wavelength = 2 * np.pi / k if k > 0 else 1.0
    ax1.annotate(
        "lambda = {:.2f} cm".format(wavelength),
        xy=(x_range[0] + wavelength, E0 * 0.5),
        fontsize=9,
        color="gray",
        arrowprops=dict(arrowstyle="<->", color="gray"),
    )

    ax2.plot(x, fields["B_y"], "b-", linewidth=1.5, label="B_y")
    if np.max(np.abs(fields["B_x"])) > 1e-15:
        ax2.plot(x, fields["B_x"], "m--", linewidth=1.5, label="B_x")
    ax2.set_xlabel("Position z (cm)")
    ax2.set_ylabel("Magnetic Field B (gauss)")
    ax2.set_title("EM Wave Propagation -- B Field (Art. 791)")
    ax2.legend(loc="best", fontsize=9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle(
        "Electromagnetic Wave Propagation: {} Polarization (Art. 791)".format(
            polarization.replace("_", " ").title()
        ),
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig, [ax1, ax2]


@maxwell_cite(
    791,
    part=4,
    chapter="Electromagnetic Theory of Light",
    description="3D visualization of E and B vectors along propagation axis.",
)
def plot_wave_snapshot_3d(
    E0: float = 1.0,
    wavelength: float = 1.0,
    resolution: int = 200,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """3D visualization of E and B vectors along propagation axis.

    Art. 791: Three-dimensional view showing E vectors (red arrows)
    and B vectors (blue arrows) perpendicular to the propagation
    direction (z-axis), illustrating the transverse nature of
    electromagnetic waves.

    Args:
        E0: Electric field amplitude (statvolts/cm).
        wavelength: Wavelength lambda (cm).
        resolution: Number of sample points.
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes) with 3D projection.

    Reference:
        Part IV, Art. 791: Transverse electromagnetic waves.
    """
    require_matplotlib()

    omega = 2 * np.pi * CONST.C / wavelength
    k = 2 * np.pi / wavelength
    z = np.linspace(0, 2 * wavelength, resolution)
    t = 0.0
    phase = k * z - omega * t

    E_x = E0 * np.cos(phase)
    B_y = E0 / CONST.C * np.cos(phase)

    if ax is None:
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    zeros = np.zeros_like(z)
    scale_e = 0.2
    scale_b = 0.2 * CONST.C

    ax.quiver(
        z,
        zeros,
        zeros,
        zeros,
        E_x * scale_e,
        zeros,
        color="red",
        alpha=0.7,
        arrow_length_ratio=0.03,
        label="E field",
    )
    ax.quiver(
        z,
        zeros,
        zeros,
        zeros,
        zeros,
        B_y * scale_b,
        color="blue",
        alpha=0.7,
        arrow_length_ratio=0.03,
        label="B field",
    )

    ax.plot(z, E_x * scale_e, zeros, "r-", linewidth=1.5, alpha=0.5)
    ax.plot(z, zeros, B_y * scale_b, "b-", linewidth=1.5, alpha=0.5)

    ax.plot([0, 2.5 * wavelength], [0, 0], [0, 0], "k-", linewidth=1, alpha=0.3)
    ax.plot(
        [0, 0],
        [-E0 * scale_e * 1.2, E0 * scale_e * 1.2],
        [0, 0],
        "r-",
        linewidth=0.8,
        alpha=0.3,
    )
    ax.plot(
        [0, 0],
        [0, 0],
        [-E0 * scale_e * 1.2, E0 * scale_e * 1.2],
        "b-",
        linewidth=0.8,
        alpha=0.3,
    )

    ax.set_xlabel("Propagation (z)")
    ax.set_ylabel("E field (x)")
    ax.set_zlabel("B field (y)")
    ax.set_title("3D EM Wave Snapshot (Art. 791)")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig, ax
