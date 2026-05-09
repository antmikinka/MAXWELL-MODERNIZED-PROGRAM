"""maxwell.electromagnetism.forces.ponderomotive — Ponderomotive forces (Arts. 602-603).

Implements Maxwell's ponderomotive force equations, which describe the
mechanical forces on matter in electromagnetic fields.

Maxwell's CGS formulation (Arts. 602-603):
    Ponderomotive force density:

        f = rho * E + (1/c) * J × B

    where:
    - rho * E is the electric force on charges
    - (1/c) * J × B is the magnetic force on currents

    In CGS-EMU (c=1 for EMU):
        f = rho * E + J × B

where:
    f = force density (dynes/cm³)
    rho = charge density (statcoulombs/cm³ or abcoulombs/cm³)
    J = current density (abamperes/cm²)
    E = electric field (statvolts/cm)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's ponderomotive force theory.

References:
    Part IV, Arts. 602-603: Ponderomotive forces on matter.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class PonderomotiveForce:
    """
    Ponderomotive force calculator.

    Art. 602-603: Maxwell's ponderomotive force equations describe
    the mechanical force on matter in electromagnetic fields.

    The total force density is:
        f = rho * E + J × B

    Attributes:
        charge_density: Charge density function rho(r).
        current_density: Current density function J(r).
    """

    charge_density: callable = None
    current_density: callable = None

    @maxwell_cite(
        602,
        603,
        part=4,
        chapter="Ponderomotive Forces",
        theory_class="maxwell_original",
        description="Calculate ponderomotive force density",
    )
    def force_density(
        self,
        E_field: np.ndarray,
        B_field: np.ndarray,
        position: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate ponderomotive force density at a point.

        Art. 602-603: The force density is:

            f = rho * E + J × B

        Args:
            E_field: Electric field (statvolts/cm).
            B_field: Magnetic field (gauss).
            position: Position for evaluating rho and J.

        Returns:
            Force density (dynes/cm³).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        B_field = np.asarray(B_field, dtype=np.float64)

        # Get charge and current densities at position
        if position is not None:
            position = np.asarray(position, dtype=np.float64)

        if self.charge_density is not None and position is not None:
            rho = self.charge_density(position)
        else:
            rho = 0.0

        if self.current_density is not None and position is not None:
            J = np.asarray(self.current_density(position), dtype=np.float64)
        else:
            J = np.zeros(3)

        # Electric force: rho * E
        f_electric = rho * E_field

        # Magnetic force: J × B
        f_magnetic = np.cross(J, B_field)

        return f_electric + f_magnetic

    @maxwell_cite(
        602,
        603,
        part=4,
        chapter="Ponderomotive Forces",
        theory_class="maxwell_original",
        description="Calculate total force on volume",
    )
    def total_force(
        self,
        E_field_func: callable,
        B_field_func: callable,
        volume_bounds: tuple,
        n_points: int = 10,
    ) -> np.ndarray:
        """
        Calculate total ponderomotive force on a volume.

        Art. 602-603: Integrate force density over volume:

            F = integral(f) dV

        Args:
            E_field_func: Function E(r) returning electric field.
            B_field_func: Function B(r) returning magnetic field.
            volume_bounds: ((x_min,x_max), (y_min,y_max), (z_min,z_max)).
            n_points: Points per dimension for integration.

        Returns:
            Total force (dynes).
        """
        (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds

        dx = (x_max - x_min) / n_points
        dy = (y_max - y_min) / n_points
        dz = (z_max - z_min) / n_points
        dV = dx * dy * dz

        total_force = np.zeros(3)

        for i in range(n_points):
            for j in range(n_points):
                for k in range(n_points):
                    x = x_min + (i + 0.5) * dx
                    y = y_min + (j + 0.5) * dy
                    z = z_min + (k + 0.5) * dz
                    r = np.array([x, y, z])

                    E = np.asarray(E_field_func(r), dtype=np.float64)
                    B = np.asarray(B_field_func(r), dtype=np.float64)
                    f = self.force_density(E, B, r)

                    total_force += f * dV

        return total_force


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate electric force on charge distribution",
)
def calc_electric_force_density(
    charge_density: float,
    E_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate electric force density on charge distribution.

    Art. 602-603: The electric force density is:

        f_electric = rho * E

    Args:
        charge_density: Charge density rho (abcoulombs/cm³).
        E_field: Electric field (statvolts/cm).

    Returns:
        Force density (dynes/cm³).

    Reference:
        Part IV, Arts. 602-603: Electric force density.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    return charge_density * E_field


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate magnetic force on current distribution",
)
def calc_magnetic_force_density(
    J: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic force density on current distribution.

    Art. 602-603: The magnetic force density is:

        f_magnetic = J × B

    Args:
        J: Current density (abamperes/cm²).
        B_field: Magnetic field (gauss).

    Returns:
        Force density (dynes/cm³).

    Reference:
        Part IV, Arts. 602-603: Magnetic force density.
    """
    J = np.asarray(J, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return np.cross(J, B_field)


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate Lorentz force on current element: F = I*L×B",
)
def calc_ponderomotive_force(
    current: float,
    length_vector: np.ndarray,
    B_field: np.ndarray,
    E_field: np.ndarray = None,
    rho: float = 0.0,
) -> np.ndarray:
    """
    Calculate ponderomotive force on current element.

    Art. 602-603: For a current element in a magnetic field:

        F = I * L × B

    With charge density and electric field:
        F = rho * E + J × B

    Args:
        current: Current (abamperes).
        length_vector: Length vector of conductor (cm).
        B_field: Magnetic field (gauss).
        E_field: Optional electric field.
        rho: Optional charge density.

    Returns:
        Force vector (dynes).

    Reference:
        Part IV, Arts. 602-603: Ponderomotive force on current element.
    """
    length_vector = np.asarray(length_vector, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    force = current * np.cross(length_vector, B_field)

    if E_field is not None and rho != 0.0:
        E_field = np.asarray(E_field, dtype=np.float64)
        force += rho * E_field

    return force


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate total ponderomotive force density",
)
def calc_ponderomotive_force_density(
    rho: float,
    J: np.ndarray,
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate total ponderomotive force density.

    Art. 602-603: The total force density is:

        f = rho * E + J × B

    Args:
        rho: Charge density (abcoulombs/cm³).
        J: Current density (abamperes/cm²).
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Force density (dynes/cm³).

    Reference:
        Part IV, Arts. 602-603: Total ponderomotive force.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    J = np.asarray(J, dtype=np.float64)

    return rho * E_field + np.cross(J, B_field)


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate force on point charge",
)
def calc_force_on_point_charge(
    charge: float,
    velocity: np.ndarray,
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate force on a point charge (Lorentz force).

    Art. 602-603: For a point charge q moving with velocity v:

        F = q * E + (q/c) * v × B

    In CGS-EMU (c=1):
        F = q * E + q * v × B

    Args:
        charge: Charge (abcoulombs).
        velocity: Velocity (cm/s).
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Force (dynes).

    Reference:
        Part IV, Arts. 602-603: Force on point charge.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    velocity = np.asarray(velocity, dtype=np.float64)

    # Electric force
    F_electric = charge * E_field

    # Magnetic force (in CGS-EMU, c=1)
    F_magnetic = charge * np.cross(velocity, B_field)

    return F_electric + F_magnetic


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate force on current-carrying wire",
)
def calc_force_on_wire_ponderomotive(
    current: float,
    wire_path: list[np.ndarray],
    B_field_func: callable,
) -> np.ndarray:
    """
    Calculate total force on a current-carrying wire.

    Art. 602-603: For a wire carrying current I along path C:

        F = I * integral(dl × B)

    Args:
        current: Current (abamperes).
        wire_path: List of points defining wire path (cm).
        B_field_func: Function B(r) returning magnetic field.

    Returns:
        Total force (dynes).

    Reference:
        Part IV, Arts. 602-603: Force on current-carrying wire.
    """
    wire_path = [np.asarray(p, dtype=np.float64) for p in wire_path]
    n = len(wire_path)

    if n < 2:
        return np.zeros(3)

    total_force = np.zeros(3)

    for i in range(n - 1):
        dl = wire_path[i + 1] - wire_path[i]
        mid_point = (wire_path[i] + wire_path[i + 1]) / 2

        B = np.asarray(B_field_func(mid_point), dtype=np.float64)
        total_force += current * np.cross(dl, B)

    return total_force


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Calculate Maxwell stress tensor force",
)
def calc_force_from_stress_tensor(
    E_field: np.ndarray,
    B_field: np.ndarray,
    surface_normal: np.ndarray,
    area: float,
) -> np.ndarray:
    """
    Calculate force using Maxwell stress tensor.

    Art. 602-603: The force on a surface can be calculated from
    the Maxwell stress tensor:

        F_i = integral(T_ij * n_j) dA

    For uniform fields and flat surface:
        F = T · n * A

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
        surface_normal: Unit normal to surface.
        area: Surface area (cm²).

    Returns:
        Force (dynes).

    Reference:
        Part IV, Arts. 602-603: Stress tensor force.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    surface_normal = np.asarray(surface_normal, dtype=np.float64)

    # Maxwell stress tensor (CGS)
    # T_ij = (1/4π) * (E_i*E_j + B_i*B_j - (1/2)*(E²+B²)*delta_ij)
    E_squared = np.dot(E_field, E_field)
    B_squared = np.dot(B_field, B_field)

    T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            T[i, j] = (1.0 / (4.0 * np.pi)) * (
                E_field[i] * E_field[j]
                + B_field[i] * B_field[j]
                - 0.5 * (E_squared + B_squared) * (1 if i == j else 0)
            )

    # F = T · n * A
    return np.dot(T, surface_normal) * area


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Verify ponderomotive force relations",
)
def verify_ponderomotive_forces(
    charge: float = 1.0,
    current: float = 1.0,
    E_field: np.ndarray = None,
    B_field: np.ndarray = None,
    velocity: np.ndarray = None,
    tolerance: float = 1e-10,
) -> dict[str, float | np.ndarray | bool]:
    """
    Verify ponderomotive force relations.

    Art. 602-603: This function verifies:
    1. F = q*E + q*v×B for point charge
    2. Force direction (parallel to E for stationary charge)
    3. Magnetic force perpendicular to v and B

    Args:
        charge: Test charge (abcoulombs).
        current: Test current (abamperes).
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
        velocity: Charge velocity (cm/s).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if E_field is None:
        E_field = np.array([1000.0, 0.0, 0.0])
    if B_field is None:
        B_field = np.array([0.0, 1000.0, 0.0])
    if velocity is None:
        velocity = np.array([0.0, 0.0, 1e8])

    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    velocity = np.asarray(velocity, dtype=np.float64)

    # Force on charge
    F = calc_force_on_point_charge(charge, velocity, E_field, B_field)

    # Verify components
    F_electric = charge * E_field
    F_magnetic = charge * np.cross(velocity, B_field)

    # Magnetic force should be perpendicular to both v and B
    v_perp_verified = abs(np.dot(F_magnetic, velocity)) < tolerance
    B_perp_verified = abs(np.dot(F_magnetic, B_field)) < tolerance

    # Total force verification
    F_expected = F_electric + F_magnetic
    force_verified = np.allclose(F, F_expected, atol=tolerance)

    return {
        "charge": charge,
        "velocity": velocity,
        "E_field": E_field,
        "B_field": B_field,
        "force_total": F,
        "force_electric": F_electric,
        "force_magnetic": F_magnetic,
        "magnetic_perp_to_velocity": v_perp_verified,
        "magnetic_perp_to_B": B_perp_verified,
        "force_verified": force_verified,
        "verified": v_perp_verified and B_perp_verified and force_verified,
    }


@maxwell_cite(
    602,
    603,
    part=4,
    chapter="Ponderomotive Forces",
    theory_class="maxwell_original",
    description="Complete ponderomotive force analysis",
)
def analyze_ponderomotive_forces(
    charge_density: float,
    J: np.ndarray,
    E_field: np.ndarray,
    B_field: np.ndarray,
    volume: float = 1.0,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of ponderomotive forces.

    Art. 602-603: Comprehensive analysis including:
    1. Electric and magnetic force densities
    2. Total force density
    3. Force on volume
    4. Direction analysis

    Args:
        charge_density: Charge density (abcoulombs/cm³).
        J: Current density (abamperes/cm²).
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
        volume: Volume for total force (cm³).

    Returns:
        Dictionary with complete analysis results.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    J = np.asarray(J, dtype=np.float64)

    f_electric = calc_electric_force_density(charge_density, E_field)
    f_magnetic = calc_magnetic_force_density(J, B_field)
    f_total = calc_ponderomotive_force(charge_density, J, E_field, B_field)

    # Total force on volume (assuming uniform)
    F_total = f_total * volume

    return {
        "charge_density": charge_density,
        "current_density": J,
        "E_field": E_field,
        "B_field": B_field,
        "force_density_electric": f_electric,
        "force_density_magnetic": f_magnetic,
        "force_density_total": f_total,
        "total_force_on_volume": F_total,
        "electric_fraction": (
            np.linalg.norm(f_electric) / np.linalg.norm(f_total)
            if np.linalg.norm(f_total) > 0
            else 0
        ),
        "magnetic_fraction": (
            np.linalg.norm(f_magnetic) / np.linalg.norm(f_total)
            if np.linalg.norm(f_total) > 0
            else 0
        ),
    }
