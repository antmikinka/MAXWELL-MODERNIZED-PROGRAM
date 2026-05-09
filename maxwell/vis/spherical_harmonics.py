"""maxwell.vis.spherical_harmonics -- Spherical harmonic globe visualization.

Implements 3D globe visualization of spherical harmonic decomposition for
Earth's magnetic field using Gauss coefficients, following Maxwell's treatment
of terrestrial magnetism and spherical harmonic analysis.

Corresponds to Maxwell's treatment of spherical harmonics in
Part I, Arts. 128-146 and Part III, Art. 467 (Terrestrial Magnetism).
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from scipy.special import lpmv

from maxwell.math.spherical_harmonics import (
    calc_legendre_polynomial,
    calc_spherical_harmonic,
)
from maxwell.meta.citation import maxwell_cite
from maxwell.vis._compat import Axes, Figure, plt, require_matplotlib


@maxwell_cite(
    467,
    part=3,
    chapter="Terrestrial Magnetism",
    description="Calculate spherical harmonic field on a sphere using Gauss coefficients.",
)
def calc_gauss_harmonics(
    n: int,
    m: int,
    coeffs: dict[tuple[int, int], tuple[float, float]],
    theta: np.ndarray,
    phi: np.ndarray,
) -> np.ndarray:
    """Calculate spherical harmonic field on a sphere using Gauss coefficients.

    Art. 467: Gauss's method for representing Earth's magnetic field as a
    spherical harmonic expansion. The magnetic potential at the Earth's surface is:

        V(R, theta, phi) = R * sum_{n=1}^{N} sum_{m=0}^{n}
            [g_n^m * cos(m*phi) + h_n^m * sin(m*phi)] * P_n^m(cos(theta))

    where g_n^m and h_n^m are the Gauss coefficients, P_n^m are the associated
    Legendre functions, and R is the Earth's radius.

    Args:
        n: Maximum degree of the expansion.
        m: Maximum order of the expansion (m <= n).
        coeffs: Dictionary {(n, m): (g_nm, h_nm)} of Gauss coefficients.
                g_nm and h_nm are the cosine and sine coefficients.
        theta: Polar angle array (colatitude, radians, 0 to pi).
        phi: Azimuthal angle array (longitude, radians, 0 to 2*pi).

    Returns:
        Magnetic potential V at each (theta, phi) point, same shape as inputs.

    Reference:
        Part III, Art. 467: Gauss coefficients for terrestrial magnetism.
    """
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)

    result = np.zeros_like(theta, dtype=np.float64)

    for (nn, mm), (g_nm, h_nm) in coeffs.items():
        if nn > n or mm > m:
            continue

        # Compute associated Legendre function P_n^m(cos(theta))
        cos_theta = np.cos(theta)
        P_nm = lpmv(mm, nn, cos_theta)

        # Azimuthal dependence
        cos_mphi = np.cos(mm * phi)
        sin_mphi = np.sin(mm * phi)

        # Contribution: (g * cos + h * sin) * P_nm
        result += (g_nm * cos_mphi + h_nm * sin_mphi) * P_nm

    return result


@maxwell_cite(
    467,
    part=3,
    chapter="Terrestrial Magnetism",
    description="Calculate field intensity from Gauss harmonic coefficients.",
)
def calc_field_intensity(
    n: int,
    m: int,
    coeffs: dict[tuple[int, int], tuple[float, float]],
    theta: np.ndarray,
    phi: np.ndarray,
    radius: float = 1.0,
) -> dict[str, np.ndarray]:
    """Calculate magnetic field intensity components from Gauss coefficients.

    Art. 467: The magnetic field components are derived from the gradient
    of the magnetic potential:

        B_r = -dV/dr
        B_theta = -(1/r) * dV/dtheta
        B_phi = -(1/(r*sin(theta))) * dV/dphi

    Args:
        n: Maximum degree.
        m: Maximum order.
        coeffs: Gauss coefficients {(n, m): (g, h)}.
        theta: Colatitude (radians).
        phi: Longitude (radians).
        radius: Sphere radius (default: 1.0 for unit sphere).

    Returns:
        Dictionary with 'B_r', 'B_theta', 'B_phi', and 'B_total' arrays.

    Reference:
        Part III, Art. 467: Field intensity from Gauss expansion.
    """
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    sin_theta = np.sin(theta)
    sin_theta = np.where(sin_theta < 1e-10, 1e-10, sin_theta)

    # Calculate potential
    V = calc_gauss_harmonics(n, m, coeffs, theta, phi)

    # Numerical derivatives for field components
    dtheta = 1e-6
    dphi = 1e-6

    V_th_plus = calc_gauss_harmonics(n, m, coeffs, theta + dtheta, phi)
    V_th_minus = calc_gauss_harmonics(n, m, coeffs, theta - dtheta, phi)
    B_theta = -(1.0 / radius) * (V_th_plus - V_th_minus) / (2 * dtheta)

    V_ph_plus = calc_gauss_harmonics(n, m, coeffs, theta, phi + dphi)
    V_ph_minus = calc_gauss_harmonics(n, m, coeffs, theta, phi - dphi)
    B_phi = -(1.0 / (radius * sin_theta)) * (V_ph_plus - V_ph_minus) / (2 * dphi)

    # Radial component (simplified: B_r ~ -V/r for unit sphere)
    B_r = -V / radius

    B_total = np.sqrt(B_r**2 + B_theta**2 + B_phi**2)

    return {
        "B_r": B_r,
        "B_theta": B_theta,
        "B_phi": B_phi,
        "B_total": B_total,
        "V": V,
    }


@maxwell_cite(
    467,
    part=3,
    chapter="Terrestrial Magnetism",
    description="Plot 3D globe with Gauss coefficient spherical harmonic visualization.",
)
def plot_harmonic_globe(
    n: int = 3,
    m: int = 3,
    coeffs: dict[tuple[int, int], tuple[float, float]] = None,
    resolution: int = 50,
    cmap: str = "RdBu_r",
    ax: Optional[Axes] = None,
) -> Tuple[Figure, Axes]:
    """Plot 3D globe with Gauss coefficient spherical harmonic visualization.

    Art. 467: Renders a 3D sphere with the magnetic potential from Gauss
    coefficients mapped onto its surface. The globe shows the Earth's magnetic
    field structure as a spherical harmonic expansion.

    Default coefficients use simplified dipole + quadrupole terms:
        g_1^0 = 1.0 (axial dipole -- dominant term)
        g_1^1 = 0.1, h_1^1 = 0.05 (tilted dipole)
        g_2^0 = 0.1 (quadrupole)

    Args:
        n: Maximum degree. Default: 3.
        m: Maximum order. Default: 3.
        coeffs: Gauss coefficients {(n, m): (g, h)}. Uses defaults if None.
        resolution: Grid resolution for sphere surface. Default: 50.
        cmap: Colormap name. Default: "RdBu_r".
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part III, Art. 467: Gauss coefficient globe visualization.
    """
    require_matplotlib()

    if coeffs is None:
        coeffs = {
            (1, 0): (1.0, 0.0),  # Axial dipole
            (1, 1): (0.1, 0.05),  # Tilted dipole
            (2, 0): (0.1, 0.0),  # Quadrupole
            (2, 1): (0.05, 0.02),  # Quadrupole tilt
            (2, 2): (0.03, 0.01),  # Sectorial quadrupole
        }

    # Create sphere surface
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Calculate potential on sphere
    V = calc_gauss_harmonics(n, m, coeffs, theta_grid, phi_grid)

    # Normalize for coloring
    vmax_abs = np.nanmax(np.abs(V))
    if vmax_abs < 1e-15:
        vmax_abs = 1.0
    norm_V = V / vmax_abs

    # Convert to Cartesian for 3D plotting
    X = np.sin(theta_grid) * np.cos(phi_grid)
    Y = np.sin(theta_grid) * np.sin(phi_grid)
    Z = np.cos(theta_grid)

    if ax is None:
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    # Get colormap for surface coloring
    try:
        from matplotlib import colormaps

        cmap_obj = colormaps.get_cmap(cmap)
    except Exception:
        cmap_obj = plt.cm.get_cmap(cmap)

    colors = cmap_obj(0.5 + 0.5 * norm_V)

    # Plot sphere surface with potential coloring
    ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=colors,
        alpha=0.85,
        linewidth=0,
        antialiased=True,
        rstride=1,
        cstride=1,
    )

    # Draw latitude lines
    for lat in [-60, -30, 0, 30, 60]:
        lat_rad = np.radians(90 - lat)  # Convert to colatitude
        theta_lat = np.full(100, lat_rad)
        phi_lat = np.linspace(0, 2 * np.pi, 100)
        x_lat = np.sin(theta_lat) * np.cos(phi_lat)
        y_lat = np.sin(theta_lat) * np.sin(phi_lat)
        z_lat = np.cos(theta_lat)
        ax.plot(x_lat, y_lat, z_lat, "k-", linewidth=0.5, alpha=0.3)

    # Draw longitude lines
    for lon in range(0, 360, 30):
        lon_rad = np.radians(lon)
        theta_lon = np.linspace(0, np.pi, 100)
        phi_lon = np.full(100, lon_rad)
        x_lon = np.sin(theta_lon) * np.cos(phi_lon)
        y_lon = np.sin(theta_lon) * np.sin(phi_lon)
        z_lon = np.cos(theta_lon)
        ax.plot(x_lon, y_lon, z_lon, "k-", linewidth=0.5, alpha=0.3)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Spherical Harmonic Globe: Gauss Coefficients (Art. 467, n_max={n})")
    ax.set_box_aspect([1, 1, 1])

    # Add coefficient summary text
    coeff_text = "Gauss coefficients:\n"
    for (nn, mm), (g, h) in sorted(coeffs.items()):
        coeff_text += f"  g_{nn}^{mm}={g:.3f}, h_{nn}^{mm}={h:.3f}\n"
    ax.text2D(
        0.02,
        0.02,
        coeff_text,
        transform=ax.transAxes,
        fontsize=8,
        verticalalignment="bottom",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
    )

    fig.tight_layout()
    return fig, ax


@maxwell_cite(
    467,
    part=3,
    chapter="Terrestrial Magnetism",
    description="Plot individual spherical harmonic modes on sphere surface.",
)
def plot_harmonic_modes(
    max_n: int = 4,
    resolution: int = 40,
    cmap: str = "RdBu_r",
    fig: Optional[Figure] = None,
) -> Tuple[Figure, np.ndarray]:
    """Plot individual spherical harmonic modes on sphere surface.

    Art. 467: Creates a grid of subplots showing individual Y_l^m modes
    on the sphere surface. Each subplot shows one (l, m) combination,
    allowing visual comparison of the different harmonic patterns.

    The modes are classified as:
        - Zonal (m=0): bands parallel to equator
        - Tesseral (0 < m < l): checkerboard pattern
        - Sectorial (m=l): wedge-shaped sectors

    Args:
        max_n: Maximum degree to show. Default: 4.
        resolution: Grid resolution per subplot. Default: 40.
        cmap: Colormap name. Default: "RdBu_r".
        fig: Existing figure to use (optional, creates new if None).

    Returns:
        Tuple of (Figure, axes_array).

    Reference:
        Part III, Art. 467: Harmonic mode visualization.
    """
    require_matplotlib()

    # Create grid of subplots
    n_rows = max_n + 1  # l = 0 to max_n
    n_cols = max_n + 1  # m = 0 to max_n

    if fig is None:
        fig, axes = plt.subplots(
            n_rows,
            n_cols,
            figsize=(4 * (max_n + 1), 4 * (max_n + 1)),
            subplot_kw={"projection": "3d"},
        )
    else:
        axes = np.array(fig.axes).reshape(n_rows, n_cols)

    # Ensure axes is 2D
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)

    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Cartesian coordinates
    X = np.sin(theta_grid) * np.cos(phi_grid)
    Y = np.sin(theta_grid) * np.sin(phi_grid)
    Z = np.cos(theta_grid)

    try:
        from matplotlib import colormaps

        cmap_obj = colormaps.get_cmap(cmap)
    except Exception:
        cmap_obj = plt.cm.get_cmap(cmap)

    for l in range(max_n + 1):
        for m_idx in range(max_n + 1):
            m = m_idx  # m = 0, 1, 2, ..., max_n
            ax = axes[l, m_idx]

            if m > l:
                # Invalid mode (m > l): hide subplot
                ax.set_visible(False)
                continue

            # Calculate real part of Y_l^m
            Y_lm = np.zeros_like(theta_grid, dtype=np.float64)
            cos_theta = np.cos(theta_grid)
            P_lm = lpmv(m, l, cos_theta)

            # Real spherical harmonic
            if m == 0:
                Y_lm = P_lm
            else:
                Y_lm = P_lm * np.cos(m * phi_grid)

            # Normalize
            vmax_abs = np.nanmax(np.abs(Y_lm))
            if vmax_abs < 1e-15:
                vmax_abs = 1.0
            norm_Y = Y_lm / vmax_abs

            colors = cmap_obj(0.5 + 0.5 * norm_Y)

            ax.plot_surface(
                X,
                Y,
                Z,
                facecolors=colors,
                alpha=0.8,
                linewidth=0,
                antialiased=True,
                rstride=2,
                cstride=2,
            )

            # Harmonic type label
            if m == 0:
                mode_type = "zonal"
            elif m == l:
                mode_type = "sectorial"
            else:
                mode_type = "tesseral"

            ax.set_title(f"Y_{l}^{m} ({mode_type})", fontsize=9)
            ax.set_axis_off()
            ax.set_box_aspect([1, 1, 1])

    fig.suptitle(
        f"Spherical Harmonic Modes Y_l^m on Sphere (Art. 467, max_l={max_n})",
        fontsize=14,
        y=1.0,
    )
    fig.tight_layout()
    return fig, axes


@maxwell_cite(
    467,
    part=3,
    chapter="Terrestrial Magnetism",
    description="Plot 2D contour of spherical harmonic field on a sphere.",
)
def plot_harmonic_contour(
    n: int = 3,
    m: int = 3,
    coeffs: dict[tuple[int, int], tuple[float, float]] = None,
    resolution: int = 100,
    ax: Optional[Axes] = None,
) -> Tuple[Figure, Axes]:
    """Plot 2D contour (Mollweide projection) of spherical harmonic field.

    Art. 467: Creates a 2D map projection showing the magnetic potential
    as filled contours. This is the standard way to visualize global
    magnetic field data from Gauss coefficient expansions.

    Args:
        n: Maximum degree. Default: 3.
        m: Maximum order. Default: 3.
        coeffs: Gauss coefficients {(n, m): (g, h)}. Uses defaults if None.
        resolution: Grid resolution. Default: 100.
        ax: Existing matplotlib axes (optional).

    Returns:
        Tuple of (Figure, Axes).

    Reference:
        Part III, Art. 467: Harmonic contour map.
    """
    require_matplotlib()

    if coeffs is None:
        coeffs = {
            (1, 0): (1.0, 0.0),
            (1, 1): (0.1, 0.05),
            (2, 0): (0.1, 0.0),
        }

    # Create grid in (colatitude, longitude)
    theta = np.linspace(0, np.pi, resolution)
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    V = calc_gauss_harmonics(n, m, coeffs, theta_grid, phi_grid)

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))
    else:
        fig = ax.figure

    # Convert to latitude for display (latitude = 90 - colatitude in degrees)
    lat = 90.0 - np.degrees(theta_grid)
    lon = np.degrees(phi_grid)

    # Wrap longitude to [-180, 180]
    lon = np.where(lon > 180, lon - 360, lon)

    vmax_abs = np.nanmax(np.abs(V))

    cf = ax.contourf(
        lon,
        lat,
        V,
        levels=40,
        cmap="RdBu_r",
        vmin=-vmax_abs,
        vmax=vmax_abs,
    )
    fig.colorbar(cf, ax=ax, label="Magnetic Potential V")

    # Draw grid lines
    for lat_line in [-60, -30, 0, 30, 60]:
        ax.axhline(y=lat_line, color="gray", linestyle="--", linewidth=0.5, alpha=0.3)
    for lon_line in [-120, -60, 0, 60, 120]:
        ax.axvline(x=lon_line, color="gray", linestyle="--", linewidth=0.5, alpha=0.3)

    ax.set_xlabel("Longitude (degrees)")
    ax.set_ylabel("Latitude (degrees)")
    ax.set_title(f"Spherical Harmonic Field Contours (Art. 467, n_max={n})")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)

    fig.tight_layout()
    return fig, ax
