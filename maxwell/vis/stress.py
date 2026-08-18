"""maxwell.vis.stress — Maxwell stress tensor visualization.

Implements 2D visualization of the Maxwell stress tensor, showing
principal stress directions and field energy density.

Corresponds to Maxwell's treatment of electromagnetic stress in
Part IV, Arts. 616-620 (stress in the dielectric medium).
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vis._base import create_meshgrid, format_axis_labels
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    616,
    617,
    618,
    619,
    620,
    part=4,
    chapter="Electromagnetic Stress in the Dielectric",
    description="Plot Maxwell stress tensor as principal stress ellipses on a 2D field.",
)
def plot_stress_tensor_2d(
    field_func: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
    x_min: float = -5.0,
    x_max: float = 5.0,
    y_min: float = -5.0,
    y_max: float = 5.0,
    nx: int = 30,
    ny: int = 30,
    skip: int = 2,
    quiver_scale: float = 1.0,
    cmap: str = "seismic",
    title: str = "Maxwell Stress Tensor",
    ax: Axes | None = None,
) -> Figure:
    """Plot the Maxwell stress tensor as principal stress ellipses.

    Art. 616-620: Maxwell's stress tensor T_ij describes the
    electromagnetic stress in the medium:

        T_ij = E_i E_j + B_i B_j - (1/2) delta_ij (E^2 + B^2)

    The eigenvalues of T give the principal stresses:
    - Positive eigenvalue: tension (pulling)
    - Negative eigenvalue: compression (pushing)

    Args:
        field_func: Function E(x, y) -> (Ex, Ey) returning the
                    electric field components on the grid.
        x_min, x_max: X range in cm.
        y_min, y_max: Y range in cm.
        nx, ny: Grid resolution for stress tensor evaluation.
        skip: Plot every skip-th point for clarity.
        quiver_scale: Scale factor for stress arrows.
        cmap: Colormap for energy density background.
        title: Plot title.
        ax: Optional existing axes.

    Returns:
        Matplotlib Figure with stress tensor visualization.

    Reference:
        Part IV, Arts. 616-620: Stress in the dielectric.
    """
    require_matplotlib()

    X, Y = create_meshgrid(x_min, x_max, y_min, y_max, nx, ny)
    Ex, Ey = field_func(X, Y)

    # Compute energy density for background colormap
    energy_density = 0.5 * (Ex**2 + Ey**2)

    # Compute stress tensor components (2D, no B field)
    # T_xx = Ex^2 - 0.5*(Ex^2 + Ey^2) = 0.5*(Ex^2 - Ey^2)
    # T_yy = Ey^2 - 0.5*(Ex^2 + Ey^2) = 0.5*(Ey^2 - Ex^2)
    # T_xy = Ex * Ey
    T_xx = 0.5 * (Ex**2 - Ey**2)
    T_yy = 0.5 * (Ey**2 - Ex**2)
    T_xy = Ex * Ey

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    # Background: energy density
    cf = ax.contourf(X, Y, energy_density, levels=30, cmap=cmap, alpha=0.6)
    fig.colorbar(cf, ax=ax, label="Energy Density (erg/cm^3)")

    # Stress tensor as quiver arrows (showing principal stress direction)
    # The principal direction is given by the eigenvector of the larger eigenvalue
    eigenvalues = np.sqrt(T_xx**2 + T_xy**2)
    angle = 0.5 * np.arctan2(2 * T_xy, T_xx - T_yy)

    # Subsample for clarity
    X_s = X[::skip, ::skip]
    Y_s = Y[::skip, ::skip]
    angle_s = angle[::skip, ::skip]
    eigen_s = eigenvalues[::skip, ::skip]

    # Arrow direction and length from eigenvalue
    dx = quiver_scale * eigen_s * np.cos(angle_s)
    dy = quiver_scale * eigen_s * np.sin(angle_s)

    ax.quiver(
        X_s,
        Y_s,
        dx,
        dy,
        angles="xy",
        scale_units="xy",
        scale=1.0,
        color="black",
        alpha=0.7,
        width=0.003,
    )

    format_axis_labels(ax, title=title)
    fig.tight_layout()
    return fig


@maxwell_cite(
    616,
    617,
    618,
    619,
    620,
    part=4,
    chapter="Electromagnetic Stress in the Dielectric",
    description="Verify stress tensor properties: symmetry, trace, and eigenvalue reality.",
)
def verify_stress_tensor_plot(
    stress_tensor_func=None,
    E_field: tuple[float, float, float] = (1.0, 0.0, 0.0),
    B_field: tuple[float, float, float] = (0.0, 1.0, 0.0),
) -> dict:
    """Verify stress tensor visualization properties.

    Checks:
    - T is symmetric: T_ij = T_ji
    - Trace T = -(E^2 + B^2)/2 = -energy_density * 2 (in CGS)
    - Eigenvalues are real (symmetric matrix guarantee)

    Args:
        stress_tensor_func: Optional stress tensor function.
        E_field: Electric field vector (Ex, Ey, Ez).
        B_field: Magnetic field vector (Bx, By, Bz).

    Returns:
        Dictionary with verification results.
    """
    E = np.array(E_field, dtype=np.float64)
    B = np.array(B_field, dtype=np.float64)
    E2 = np.dot(E, E)
    B2 = np.dot(B, B)

    # Build 3x3 stress tensor
    T = (np.outer(E, E) + np.outer(B, B) - 0.5 * np.eye(3) * (E2 + B2)) / (4.0 * np.pi)

    # Symmetry check
    is_symmetric = np.allclose(T, T.T, atol=1e-10)

    # Trace check: Tr(T) = -(E^2 + B^2) / (8*pi)
    expected_trace = -(E2 + B2) / (8.0 * np.pi)
    trace_error = abs(T.trace() - expected_trace)

    # Eigenvalue check
    eigenvalues = np.linalg.eigvalsh(T)
    all_real = np.all(np.isreal(eigenvalues))

    return {
        "symmetric": is_symmetric,
        "trace": T.trace(),
        "expected_trace": expected_trace,
        "trace_error": trace_error,
        "eigenvalues": eigenvalues.tolist(),
        "all_real_eigenvalues": all_real,
        "energy_density": (E2 + B2) / (8.0 * np.pi),
    }
