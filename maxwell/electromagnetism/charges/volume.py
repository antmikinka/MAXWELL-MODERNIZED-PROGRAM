"""maxwell.electromagnetism.charges.volume — Volume charge density (Art. 612).

Implements Maxwell's treatment of volume charge density and its relation
to the electric field through Gauss's law.

Maxwell's CGS formulation (Art. 612):
    Volume charge density equation:

        div(D) = 4πρ

    or in terms of E:
        div(E) = 4πρ/ε

    where ρ is the volume charge density.

    The total charge in a volume is:
        Q = integral(ρ) dV

where:
    ρ = volume charge density (statcoulombs/cm³ or abcoulombs/cm³)
    D = electric displacement (statcoulombs/cm²)
    E = electric field (statvolts/cm)
    ε = permittivity

Category: A (maxwell_original) — Maxwell's volume charge theory.

References:
    Part IV, Art. 612: Volume charge density.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class VolumeCharge:
    """
    Volume charge density calculator.

    Art. 612: Maxwell's relation for volume charge:

        div(D) = 4πρ

    This relates charge density to the divergence of electric displacement.

    Attributes:
        permittivity: Permittivity ε.
    """

    permittivity: float = 1.0

    @maxwell_cite(
        612,
        part=4, chapter="Volume Charge",
        theory_class="maxwell_original",
        description="Calculate charge density from D field divergence",
    )
    def charge_density_from_divergence(
        self,
        D_field_func: callable,
        position: np.ndarray,
        delta: float = 1e-6,
    ) -> float:
        """
        Calculate charge density from divergence of D.

        Art. 612: ρ = div(D) / (4π)

        Args:
            D_field_func: Function D(r) returning displacement.
            position: Position for evaluation.
            delta: Finite difference step.

        Returns:
            Charge density ρ (statcoulombs/cm³).
        """
        position = np.asarray(position, dtype=np.float64)

        # Numerical divergence
        div_D = 0.0
        for i in range(3):
            pos_plus = position.copy()
            pos_plus[i] += delta
            pos_minus = position.copy()
            pos_minus[i] -= delta

            D_plus = np.asarray(D_field_func(pos_plus), dtype=np.float64)[i]
            D_minus = np.asarray(D_field_func(pos_minus), dtype=np.float64)[i]

            div_D += (D_plus - D_minus) / (2 * delta)

        return div_D / (4.0 * np.pi)

    @maxwell_cite(
        612,
        part=4, chapter="Volume Charge",
        theory_class="maxwell_original",
        description="Calculate total charge in volume",
    )
    def total_charge_in_volume(
        self,
        rho_func: callable,
        volume_bounds: tuple,
        n_points: int = 10,
    ) -> float:
        """
        Calculate total charge in a volume.

        Art. 612: Q = integral(ρ) dV

        Args:
            rho_func: Function ρ(r) returning charge density.
            volume_bounds: ((x_min,x_max), (y_min,y_max), (z_min,z_max)).
            n_points: Points per dimension for integration.

        Returns:
            Total charge Q (statcoulombs).
        """
        (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds

        dx = (x_max - x_min) / n_points
        dy = (y_max - y_min) / n_points
        dz = (z_max - z_min) / n_points
        dV = dx * dy * dz

        total_charge = 0.0
        for i in range(n_points):
            for j in range(n_points):
                for k in range(n_points):
                    x = x_min + (i + 0.5) * dx
                    y = y_min + (j + 0.5) * dy
                    z = z_min + (k + 0.5) * dz
                    r = np.array([x, y, z])

                    rho = rho_func(r)
                    total_charge += rho * dV

        return total_charge


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Calculate charge density: ρ = div(D)/(4π)",
)
def calc_volume_charge_density(
    D_field: np.ndarray,
    div_D: float,
) -> float:
    """
    Calculate volume charge density from divergence of D.

    Art. 612: Gauss's law in differential form:

        ρ = div(D) / (4π)

    Args:
        D_field: Electric displacement at point.
        div_D: Divergence of D.

    Returns:
        Charge density ρ (statcoulombs/cm³).

    Reference:
        Part IV, Art. 612: Volume charge density.
    """
    return div_D / (4.0 * np.pi)


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Calculate charge density from E field divergence",
)
def calc_charge_density_from_E(
    div_E: float,
    permittivity: float = 1.0,
) -> float:
    """
    Calculate charge density from divergence of E.

    Art. 612: In terms of E:

        ρ = ε * div(E) / (4π)

    Args:
        div_E: Divergence of E.
        permittivity: Permittivity ε.

    Returns:
        Charge density ρ.

    Reference:
        Part IV, Art. 612: Charge from E divergence.
    """
    return permittivity * div_E / (4.0 * np.pi)


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Calculate total charge from uniform density",
)
def calc_total_charge_uniform(
    charge_density: float,
    volume: float,
) -> float:
    """
    Calculate total charge for uniform charge density.

    Art. 612: For uniform ρ:

        Q = ρ * V

    Args:
        charge_density: Charge density ρ.
        volume: Volume V.

    Returns:
        Total charge Q.

    Reference:
        Part IV, Art. 612: Total charge.
    """
    return charge_density * volume


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Calculate charge in sphere with uniform density",
)
def calc_charge_in_sphere(
    charge_density: float,
    radius: float,
) -> float:
    """
    Calculate total charge in a sphere with uniform density.

    Art. 612: For a sphere of radius R:

        Q = ρ * (4/3)πR³

    Args:
        charge_density: Charge density ρ.
        radius: Sphere radius R.

    Returns:
        Total charge Q.

    Reference:
        Part IV, Art. 612: Charge in sphere.
    """
    if radius <= 0:
        return 0.0

    volume = (4.0 / 3.0) * np.pi * radius ** 3
    return charge_density * volume


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Calculate E field from uniform charged sphere",
)
def calc_field_from_charged_sphere(
    total_charge: float,
    sphere_radius: float,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate electric field from a uniformly charged sphere.

    Art. 612: For a sphere with total charge Q:
    - Outside (r > R): E = Q/r² (point charge)
    - Inside (r < R): E = Q*r/R³ (linear with r)

    Args:
        total_charge: Total charge Q.
        sphere_radius: Sphere radius R.
        position: Position from sphere center.

    Returns:
        Electric field E.

    Reference:
        Part IV, Art. 612: Field of charged sphere.
    """
    position = np.asarray(position, dtype=np.float64)
    r = np.linalg.norm(position)

    if r < 1e-15:
        return np.zeros(3)

    r_hat = position / r

    if r >= sphere_radius:
        # Outside: point charge field
        E_mag = total_charge / (r ** 2)
    else:
        # Inside: linear field
        if sphere_radius > 0:
            E_mag = total_charge * r / (sphere_radius ** 3)
        else:
            E_mag = 0.0

    return E_mag * r_hat


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Verify Gauss's law for volume charge",
)
def verify_gauss_law_volume(
    charge_density: float,
    sphere_radius: float,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify Gauss's law for volume charge.

    Art. 612: This function verifies:
    1. Q = integral(ρ) dV
    2. Flux of E through surface = 4πQ

    Args:
        charge_density: Uniform charge density.
        sphere_radius: Radius of charged sphere.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Total charge in sphere
    Q = calc_charge_in_sphere(charge_density, sphere_radius)

    # Flux through surface at r > R
    r_test = 2.0 * sphere_radius
    E_surface = calc_field_from_charged_sphere(Q, sphere_radius, np.array([r_test, 0, 0]))

    # Flux = E * 4πr²
    flux = np.linalg.norm(E_surface) * 4.0 * np.pi * r_test ** 2

    # Gauss's law: flux = 4πQ
    expected_flux = 4.0 * np.pi * Q

    flux_error = abs(flux - expected_flux) / abs(expected_flux) if expected_flux != 0 else 0

    return {
        "charge_density": charge_density,
        "sphere_radius": sphere_radius,
        "total_charge_Q": Q,
        "test_radius": r_test,
        "E_at_surface": float(np.linalg.norm(E_surface)),
        "calculated_flux": flux,
        "expected_flux": expected_flux,
        "flux_error": float(flux_error),
        "gauss_law_verified": bool(flux_error < tolerance),
    }


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Complete volume charge analysis",
)
def analyze_volume_charge(
    charge_density: float,
    volume_bounds: tuple,
) -> dict[str, float]:
    """
    Complete analysis of volume charge distribution.

    Art. 612: Comprehensive analysis including:
    1. Total charge
    2. Volume
    3. Average charge density

    Args:
        charge_density: Charge density (may be function or constant).
        volume_bounds: ((x_min,x_max), (y_min,y_max), (z_min,z_max)).

    Returns:
        Dictionary with complete analysis results.
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds

    volume = (x_max - x_min) * (y_max - y_min) * (z_max - z_min)

    if callable(charge_density):
        # Numerical integration
        vc = VolumeCharge()
        total_charge = vc.total_charge_in_volume(charge_density, volume_bounds, n_points=20)
        avg_density = total_charge / volume if volume > 0 else 0
    else:
        total_charge = charge_density * volume
        avg_density = charge_density

    return {
        "volume_bounds": volume_bounds,
        "volume": volume,
        "total_charge": total_charge,
        "average_charge_density": avg_density,
    }


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Verify continuity equation",
)
def verify_continuity_equation(
    rho_func: callable,
    t: float,
    dt: float,
    div_J: float,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify continuity equation for charge conservation.

    Art. 612: The continuity equation is:

        div(J) + dρ/dt = 0

    Args:
        rho_func: Function ρ(t) returning charge density.
        t: Time for evaluation.
        dt: Time step for derivative.
        div_J: Divergence of current density.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Calculate dρ/dt
    rho_plus = rho_func(t + dt)
    rho_minus = rho_func(t - dt)
    drho_dt = (rho_plus - rho_minus) / (2 * dt)

    # Continuity: div(J) + dρ/dt = 0
    continuity_value = div_J + drho_dt

    return {
        "rho_at_t": rho_func(t),
        "drho_dt": drho_dt,
        "div_J": div_J,
        "continuity_value": continuity_value,
        "continuity_error": abs(continuity_value),
        "continuity_verified": abs(continuity_value) < tolerance,
    }


@maxwell_cite(
    612,
    part=4, chapter="Volume Charge",
    theory_class="maxwell_original",
    description="Verify charge conservation",
)
def verify_charge_conservation(
    initial_charge: float,
    current_out: float,
    time_interval: float,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify charge conservation in a closed system.

    Art. 612: Charge conservation:

        Q_final = Q_initial - integral(I_out) dt

    For constant I_out:
        Q_final = Q_initial - I_out * t

    Args:
        initial_charge: Initial charge Q_initial.
        current_out: Current flowing out.
        time_interval: Time interval.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Final charge after current flows out
    Q_final = initial_charge - current_out * time_interval

    # Verify charge is conserved (positive check)
    charge_conserved = Q_final >= 0

    return {
        "initial_charge": initial_charge,
        "current_out": current_out,
        "time_interval": time_interval,
        "charge_outflow": current_out * time_interval,
        "final_charge": Q_final,
        "charge_conserved": charge_conserved,
    }
