"""
Electric current — the foundation of electrokinematics.

Implements the theory of electric current from Part II of Maxwell's Treatise:
- Current density and its relation to total current (Arts. 150-160)
- The continuity equation for charge conservation
- Surface integrals of current density
- Current as a vector quantity

Maxwell's formulation (CGS-EMU):
    Current density: J = I / A (abampere/cm^2)
    Total current: I = integral_S (J . dA)
    Continuity: div J = -∂ρ/∂t

Category: A (maxwell_original) — Maxwell's theory of electric current.

References:
    Part II, Arts. 150-160: Electric current and current density.
    Part II, Art. 177: Continuity equation.
    Part IV, Art. 629: Current as a vector quantity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectricCurrent:
    """Electric current flowing through a conductor.

    Art. 150-160: Electric current is the rate of flow of electric charge
    through a surface. In CGS-EMU, current is measured in abamperes.

    The current density J is a vector field describing current per unit
    area at each point in space.

    Attributes:
        total_current: Total current (abampere in CGS-EMU, statampere in CGS-ESU).
        current_density: Current density vector field J (abampere/cm^2).
        cross_section: Cross-sectional area (cm^2).
        direction: Unit vector in direction of current flow.

    Note:
        Maxwell primarily uses electromagnetic measure (EMU) for current.
        In CGS-ESU: 1 statampere = 1 esu/s = c/10 abampere
        In CGS-EMU: 1 abampere = 1 emu/s = 10 statampere / c
    """

    total_current: float
    cross_section: float
    direction: np.ndarray = field(default_factory=lambda: np.array([1.0, 0.0, 0.0]))
    current_density: np.ndarray | None = None

    def __post_init__(self):
        self.direction = np.asarray(self.direction, dtype=np.float64)
        if self.direction.shape != (3,):
            raise ValueError(f"Direction must be 3D, got shape {self.direction.shape}")
        if self.cross_section <= 0:
            raise ValueError(
                f"Cross-section must be positive, got {self.cross_section}"
            )

        # Compute current density if not provided
        if self.current_density is None:
            J_magnitude = self.total_current / self.cross_section
            self.current_density = J_magnitude * self.direction

    @property
    def current_density_magnitude(self) -> float:
        """Magnitude of current density.

        Art. 150: The current density is the current per unit area.

        Returns:
            Current density magnitude (abampere/cm^2).

        Reference:
            Part II, Art. 150: Current density definition.
        """
        return np.linalg.norm(self.current_density)

    @property
    def verify_total_current(self) -> float:
        """Verify total current from current density.

        Returns:
            Total current computed from J · A (abampere).

        Reference:
            Part II, Art. 150: Current density and total current relation.
        """
        return self.current_density_magnitude * self.cross_section


@maxwell_cite(
    150,
    part=2,
    chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Current density: J = I / A",
)
def calc_current_density(
    current: float,
    cross_section: float,
    direction: np.ndarray | None = None,
) -> np.ndarray:
    """Calculate current density from total current and cross-section.

    Art. 150: The current density J is the current per unit area
    passing through a surface perpendicular to the flow direction.

    J = I / A

    In vector form:
        J = (I / A) * n_hat

    where n_hat is the unit vector in the direction of current flow.

    Args:
        current: Total current (abampere in CGS-EMU).
        cross_section: Cross-sectional area perpendicular to flow (cm^2).
        direction: Unit vector in current direction (default: x-axis).

    Returns:
        Current density vector J (abampere/cm^2).

    Reference:
        Part II, Art. 150: Current density definition.

    Example:
        >>> J = calc_current_density(10.0, 0.5)  # 10 abA through 0.5 cm^2
        >>> print(f"Current density: {np.linalg.norm(J):.2f} abampere/cm^2")
    """
    if cross_section <= 0:
        raise ValueError(f"Cross-section must be positive, got {cross_section}")

    if direction is None:
        direction = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    else:
        direction = np.asarray(direction, dtype=np.float64)
        direction = direction / np.linalg.norm(direction)  # Normalize

    J_magnitude = current / cross_section
    return J_magnitude * direction


@maxwell_cite(
    177,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Continuity equation: ∇·J = -∂ρ/∂t",
)
def continuity_equation(
    current_density_func: Callable[[np.ndarray, float], np.ndarray],
    charge_density_func: Callable[[np.ndarray, float], float],
    point: np.ndarray,
    time: float,
    dt: float = 1e-9,
    h: float = 1e-6,
) -> dict[str, float]:
    """Verify the continuity equation at a point in space and time.

    Art. 177: The continuity equation expresses conservation of charge:
        ∇ · J = -∂ρ/∂t

    This states that the divergence of current density equals the
    negative rate of change of charge density. Physically, charge
    flowing out of a volume must decrease the charge within.

    The equation is verified numerically by computing:
        - Divergence of J using central differences
        - Time derivative of ρ using finite differences

    Args:
        current_density_func: Function J(r, t) returning current density vector.
        charge_density_func: Function ρ(r, t) returning charge density.
        point: Position vector (cm) where continuity is checked.
        time: Time (s) at which to check continuity.
        dt: Time step for ∂ρ/∂t calculation.
        h: Spatial step for divergence calculation.

    Returns:
        Dictionary with:
            - divergence_J: ∇ · J at (point, time)
            - minus_drho_dt: -∂ρ/∂t at (point, time)
            - difference: |∇ · J - (-∂ρ/∂t)|
            - verified: True if continuity equation holds within tolerance

    Reference:
        Part II, Art. 177: The continuity equation.

    Note:
        The continuity equation is a fundamental law of electromagnetism,
        expressing local conservation of electric charge.
    """
    point = np.asarray(point, dtype=np.float64)

    # Compute divergence of J using central differences
    def divergence(
        J_func: Callable[[np.ndarray], np.ndarray], p: np.ndarray, h: float
    ) -> float:
        """Numerical divergence using central differences."""
        div = 0.0
        for i in range(3):
            delta_plus = np.zeros(3)
            delta_minus = np.zeros(3)
            delta_plus[i] = h
            delta_minus[i] = -h

            J_plus = J_func(p + delta_plus)
            J_minus = J_func(p + delta_minus)

            div += (J_plus[i] - J_minus[i]) / (2 * h)
        return div

    # Divergence at current time
    J_at_time = lambda r: current_density_func(r, time)
    div_J = divergence(J_at_time, point, h)

    # Time derivative of charge density: ∂ρ/∂t
    rho_plus = charge_density_func(point, time + dt)
    rho_minus = charge_density_func(point, time - dt)
    drho_dt = (rho_plus - rho_minus) / (2 * dt)

    # Verify continuity: ∇ · J = -∂ρ/∂t
    minus_drho_dt = -drho_dt
    difference = abs(div_J - minus_drho_dt)

    # Relative error (avoid division by zero)
    scale = max(abs(div_J), abs(minus_drho_dt), 1e-15)
    relative_error = difference / scale

    return {
        "divergence_J": div_J,
        "minus_drho_dt": minus_drho_dt,
        "difference": difference,
        "relative_error": relative_error,
        "verified": relative_error < 0.01,  # 1% tolerance for numerical differentiation
    }


@maxwell_cite(
    150,
    part=2,
    chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Total current as surface integral of current density",
)
def calc_total_current(
    current_density_func: Callable[[np.ndarray], np.ndarray],
    surface_param: Callable[[float, float], tuple[np.ndarray, np.ndarray]],
    u_range: tuple[float, float],
    v_range: tuple[float, float],
    nu: int = 50,
    nv: int = 50,
) -> float:
    """Calculate total current through a surface.

    Art. 150: The total current through a surface is the surface integral
    of the current density:

        I = integral_S (J · dA)

    where dA is the vector area element (normal to surface).

    For a parametric surface r(u, v):
        dA = (∂r/∂u × ∂r/∂v) du dv

    Args:
        current_density_func: Function returning J at a position.
        surface_param: Parametric surface function returning (point, dA_vector).
        u_range: (u_min, u_max) parameter range.
        v_range: (v_min, v_max) parameter range.
        nu: Number of subdivisions in u direction.
        nv: Number of subdivisions in v direction.

    Returns:
        Total current through surface (abampere).

    Reference:
        Part II, Art. 150: Current as surface integral.

    Example:
        >>> # Current through a circular disk of radius R
        >>> def disk_param(u, v):
        ...     # u = radius (0 to R), v = angle (0 to 2π)
        ...     x = u * np.cos(v)
        ...     y = u * np.sin(v)
        ...     z = 0.0
        ...     point = np.array([x, y, z])
        ...     dA = np.array([0, 0, u])  # dA = r dr dθ in z-direction
        ...     return point, dA
        >>> I = calc_total_current(J_func, disk_param, (0, R), (0, 2*np.pi))
    """
    u_min, u_max = u_range
    v_min, v_max = v_range

    du = (u_max - u_min) / nu
    dv = (v_max - v_min) / nv

    total_current = 0.0

    for i in range(nu):
        for j in range(nv):
            # Midpoint of each element
            u = u_min + (i + 0.5) * du
            v = v_min + (j + 0.5) * dv

            # Get position and area element
            point, dA = surface_param(u, v)
            point = np.asarray(point, dtype=np.float64)
            dA = np.asarray(dA, dtype=np.float64)

            # Evaluate current density and compute flux through element
            J = current_density_func(point)
            total_current += np.dot(J, dA)

    return total_current


@maxwell_cite(
    64,
    part=2,
    chapter="Electric Currents",
    theory_class="maxwell_original",
    description="Current as a vector quantity with direction",
)
def current_vector(
    magnitude: float,
    direction: np.ndarray,
) -> np.ndarray:
    """Create a current vector with magnitude and direction.

    Art. 64: Electric current, when considered as flowing through
    a conductor, has both magnitude and direction, making it a
    vector quantity.

    Args:
        magnitude: Current magnitude (abampere).
        direction: Unit vector in direction of current flow.

    Returns:
        Current vector I (abampere in direction of flow).

    Reference:
        Part II, Art. 64: Current as a vector.
    """
    direction = np.asarray(direction, dtype=np.float64)
    norm = np.linalg.norm(direction)
    if norm == 0:
        raise ValueError("Direction vector cannot be zero")
    direction = direction / norm
    return magnitude * direction


@maxwell_cite(
    150,
    part=2,
    chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Current through surface at arbitrary angle",
)
def current_through_tilted_surface(
    current: float,
    cross_section: float,
    angle_degrees: float,
) -> float:
    """Calculate current through a surface tilted relative to flow.

    When a surface is tilted at an angle θ to the current direction,
    the effective area perpendicular to flow is A·cos(θ).

    The current through the tilted surface is:
        I_effective = J · A · cos(θ) = I · cos(θ)

    Args:
        current: Total current (abampere).
        cross_section: Cross-sectional area (cm^2).
        angle_degrees: Angle between current direction and surface normal.

    Returns:
        Current through the tilted surface (abampere).

    Reference:
        Part II, Art. 150: Current density and surface orientation.
    """
    theta_rad = np.deg2rad(angle_degrees)
    return current * np.cos(theta_rad)


@maxwell_cite(
    177,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Steady current condition: ∇·J = 0",
)
def verify_steady_current(
    current_density_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    grid_resolution: tuple[int, int, int],
) -> dict[str, float]:
    """Verify that a current distribution is steady (time-independent).

    For steady currents (∂ρ/∂t = 0), the continuity equation reduces to:
        ∇ · J = 0

    This function numerically verifies that the divergence of J is
    approximately zero throughout a volume.

    Args:
        current_density_func: Function returning J at a position.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        grid_resolution: (nx, ny, nz) for numerical grid.

    Returns:
        Dictionary with:
            - max_divergence: Maximum |∇ · J| in volume
            - mean_divergence: Mean |∇ · J| in volume
            - std_divergence: Standard deviation of ∇ · J
            - verified: True if divergence is approximately zero

    Reference:
        Part II, Art. 177: Steady current condition.
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds
    nx, ny, nz = grid_resolution

    dx = (x_max - x_min) / nx
    dy = (y_max - y_min) / ny
    dz = (z_max - z_min) / nz
    h = min(dx, dy, dz) * 0.5  # Smaller step for central differences

    def divergence_at(point: np.ndarray) -> float:
        """Compute divergence at a point."""
        div = 0.0
        for i in range(3):
            delta_plus = np.zeros(3)
            delta_minus = np.zeros(3)
            delta_plus[i] = h
            delta_minus[i] = -h

            J_plus = current_density_func(point + delta_plus)
            J_minus = current_density_func(point + delta_minus)

            div += (J_plus[i] - J_minus[i]) / (2 * h)
        return div

    divergences = []
    for i in range(1, nx - 1):  # Avoid boundaries
        for j in range(1, ny - 1):
            for k in range(1, nz - 1):
                x = x_min + i * dx
                y = y_min + j * dy
                z = z_min + k * dz
                point = np.array([x, y, z])
                div = divergence_at(point)
                divergences.append(abs(div))

    if not divergences:
        return {
            "max_divergence": 0.0,
            "mean_divergence": 0.0,
            "std_divergence": 0.0,
            "verified": True,
        }

    max_div = max(divergences)
    mean_div = np.mean(divergences)
    std_div = np.std(divergences)

    return {
        "max_divergence": max_div,
        "mean_divergence": mean_div,
        "std_divergence": std_div,
        "verified": max_div < 1e-6,  # Divergence should be essentially zero
        "grid_points": len(divergences),
    }


@maxwell_cite(
    152,
    part=2,
    chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Current density from multiple parallel conductors",
)
def current_density_parallel(
    currents: list[float],
    areas: list[float],
) -> np.ndarray:
    """Calculate total current density from parallel conductors.

    When multiple conductors carry current in parallel, the total
    current density is the sum of individual current densities.

    J_total = sum_i (I_i / A_i)

    Args:
        currents: List of currents in each conductor (abampere).
        areas: List of cross-sectional areas (cm^2).

    Returns:
        Total current density magnitude (abampere/cm^2).

    Reference:
        Part II, Art. 152: Current density in composite conductors.
    """
    if len(currents) != len(areas):
        raise ValueError("Currents and areas must have same length")

    J_total = 0.0
    for I, A in zip(currents, areas):
        if A <= 0:
            raise ValueError(f"Area must be positive, got {A}")
        J_total += I / A

    return J_total


@maxwell_cite(
    150,
    part=2,
    chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Verify current conservation in a junction",
)
def verify_current_conservation(
    incoming_currents: list[float],
    outgoing_currents: list[float],
    tolerance: float = 1e-10,
) -> dict[str, float]:
    """Verify Kirchhoff's current law (conservation of charge at a junction).

    The sum of currents entering a junction must equal the sum leaving:
        sum(I_incoming) = sum(I_outgoing)

    This is a direct consequence of the continuity equation for steady
    currents.

    Args:
        incoming_currents: List of currents entering junction (abampere).
        outgoing_currents: List of currents leaving junction (abampere).
        tolerance: Numerical tolerance for comparison.

    Returns:
        Dictionary with:
            - total_incoming: Sum of incoming currents
            - total_outgoing: Sum of outgoing currents
            - difference: |incoming - outgoing|
            - verified: True if conserved within tolerance

    Reference:
        Part II, Art. 150: Current conservation (Kirchhoff's law).
    """
    total_in = sum(incoming_currents)
    total_out = sum(outgoing_currents)
    difference = abs(total_in - total_out)

    return {
        "total_incoming": total_in,
        "total_outgoing": total_out,
        "difference": difference,
        "verified": difference <= tolerance,
    }
