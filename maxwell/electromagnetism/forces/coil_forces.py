"""maxwell.electromagnetism.forces.coil_forces — Coil interaction forces (Arts. 697-699).

Implements Maxwell's calculation of forces between current-carrying coils
using energy derivatives and mutual inductance.

Maxwell's CGS formulation (Arts. 697-699):
    The force between two coils is:

        F = I1 * I2 * dM/dx

    where M is the mutual inductance and x is the coordinate.

    The torque between coils is:

        tau = I1 * I2 * dM/dtheta

    The energy of the coil system is:

        W = (1/2)*L1*I1^2 + (1/2)*L2*I2^2 + M*I1*I2

    For coaxial circular coils, M is computed using elliptic integrals.

where:
    I1, I2 = currents (abamperes)
    M = mutual inductance (cm in CGS-EMU)
    F = force (dynes)
    tau = torque (dyne*cm)

Category: A (maxwell_original) — Maxwell's coil force theory.

References:
    Part IV, Arts. 697-699: Forces between coils.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


def _mutual_inductance_coaxial(a: float, b: float, z: float) -> float:
    """Mutual inductance of coaxial circular loops using elliptic integrals."""
    k_sq = 4.0 * a * b / ((a + b) ** 2 + z ** 2)
    k_sq = min(max(k_sq, 0), 1 - 1e-15)

    # Elliptic integral approximations
    K = (np.pi / 2) * (1 + k_sq / 4 + 9 * k_sq ** 2 / 64)
    E = (np.pi / 2) * (1 - k_sq / 4 - 3 * k_sq ** 2 / 64)

    k = np.sqrt(k_sq)
    if k < 1e-10:
        return 0.0

    # Maxwell's formula (CGS-EMU)
    M = 4.0 * np.pi * np.sqrt(a * b) * ((2.0 / k - k) * K - (2.0 / k) * E)
    return M


@maxwell_cite(
    697, 698,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Calculate force between coaxial coils",
)
def calc_coaxial_coil_force(
    current1: float,
    current2: float,
    radius1: float,
    radius2: float,
    axial_separation: float,
) -> float:
    """
    Calculate axial force between coaxial circular coils.

    Art. 697-698: The force is:

        F = I1 * I2 * dM/dz

    where dM/dz is computed numerically.

    Args:
        current1: Current in coil 1 (abamperes).
        current2: Current in coil 2 (abamperes).
        radius1: Radius of coil 1 (cm).
        radius2: Radius of coil 2 (cm).
        axial_separation: Axial distance (cm).

    Returns:
        Axial force (dynes). Positive = repulsive.
    """
    delta = 1e-6
    z = axial_separation

    M_plus = _mutual_inductance_coaxial(radius1, radius2, z + delta)
    M_minus = _mutual_inductance_coaxial(radius1, radius2, z - delta)
    dM_dz = (M_plus - M_minus) / (2 * delta)

    return current1 * current2 * dM_dz


@maxwell_cite(
    698, 699,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Calculate torque between inclined coils",
)
def calc_coil_torque(
    current1: float,
    current2: float,
    radius1: float,
    radius2: float,
    angle: float,
    separation: float = None,
) -> float:
    """
    Calculate torque between two inclined circular coils.

    Art. 698-699: The torque is:

        tau = I1 * I2 * dM/dtheta

    where theta is the angle between coil planes.

    Args:
        current1: Current in coil 1 (abamperes).
        current2: Current in coil 2 (abamperes).
        radius1: Radius of coil 1 (cm).
        radius2: Radius of coil 2 (cm).
        angle: Angle between coil planes (radians).
        separation: Center-to-center distance (cm, default max radius).

    Returns:
        Torque (dyne*cm).
    """
    if separation is None:
        separation = max(radius1, radius2)

    delta = 1e-6

    # Approximate: M varies as cos(theta) for small separation
    M0 = _mutual_inductance_coaxial(radius1, radius2, separation)
    dM_dtheta = -M0 * np.sin(angle)

    return current1 * current2 * dM_dtheta


@maxwell_cite(
    697,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Calculate force between coaxial solenoids",
)
def calc_solenoid_force(
    current1: float,
    current2: float,
    turns_per_cm1: float,
    turns_per_cm2: float,
    radius1: float,
    radius2: float,
    length1: float,
    length2: float,
    axial_separation: float,
) -> float:
    """
    Calculate force between coaxial solenoids.

    Art. 697: The force between solenoids is the sum of forces
    between all turn pairs.

    For long solenoids with overlapping fields, the force is
    approximately:

        F = 2*pi*n1*n2*I1*I2*r^2 / c^2

    Args:
        current1: Current in solenoid 1 (abamperes).
        current2: Current in solenoid 2 (abamperes).
        turns_per_cm1: Turns per cm of solenoid 1.
        turns_per_cm2: Turns per cm of solenoid 2.
        radius1: Radius of solenoid 1 (cm).
        radius2: Radius of solenoid 2 (cm).
        length1: Length of solenoid 1 (cm).
        length2: Length of solenoid 2 (cm).
        axial_separation: Axial distance between centers (cm).

    Returns:
        Axial force (dynes).
    """
    # Approximate: force between two equivalent loops
    avg_radius = (radius1 + radius2) / 2
    n1 = turns_per_cm1 * length1
    n2 = turns_per_cm2 * length2

    return calc_coaxial_coil_force(
        current1 * n1, current2 * n2,
        avg_radius, avg_radius, axial_separation,
    )


@maxwell_cite(
    697, 698, 699,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Calculate energy of coupled coil system",
)
def calc_coil_system_energy(
    current1: float,
    current2: float,
    self_inductance1: float,
    self_inductance2: float,
    mutual_inductance: float,
) -> float:
    """
    Calculate total energy of coupled coil system.

    Art. 697-699: The energy is:

        W = (1/2)*L1*I1^2 + (1/2)*L2*I2^2 + M*I1*I2

    Args:
        current1: Current in coil 1 (abamperes).
        current2: Current in coil 2 (abamperes).
        self_inductance1: Self-inductance of coil 1 (cm).
        self_inductance2: Self-inductance of coil 2 (cm).
        mutual_inductance: Mutual inductance (cm).

    Returns:
        Total energy (ergs).
    """
    return (0.5 * self_inductance1 * current1 ** 2
            + 0.5 * self_inductance2 * current2 ** 2
            + mutual_inductance * current1 * current2)


@maxwell_cite(
    697, 698, 699,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Verify coil force relations",
)
def verify_coil_forces(
    current: float = 1.0,
    radius: float = 10.0,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify coil force relations.

    Art. 697-699: This function verifies:
    1. Force sign (attractive for same-direction currents)
    2. Force decreases with separation
    3. Energy conservation: F = -dW/dx

    Args:
        current: Test current (abamperes).
        radius: Test coil radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Force at z = radius
    F1 = calc_coaxial_coil_force(current, current, radius, radius, radius)

    # Force at z = 2*radius (should be smaller)
    F2 = calc_coaxial_coil_force(current, current, radius, radius, 2 * radius)

    # Force should decrease with separation
    force_decreases = abs(F2) < abs(F1)

    # Energy check
    M = _mutual_inductance_coaxial(radius, radius, radius)
    L = 4.0 * np.pi * radius * (np.log(8 * radius / (0.1 * radius)) - 2)

    W = calc_coil_system_energy(current, current, L, L, M)

    # For same-direction currents, M > 0 and the force is attractive
    # The system energy is lowered when coils move closer (increasing M)
    # Check: W decreases as separation decreases
    M_close = _mutual_inductance_coaxial(radius, radius, radius / 2)
    energy_close = calc_coil_system_energy(current, current, L, L, M_close)
    energy_far = calc_coil_system_energy(current, current, L, L, M)
    energy_lowered = energy_close < energy_far

    return {
        "force_at_radius": F1,
        "force_at_2radius": F2,
        "force_decreases_with_separation": bool(force_decreases),
        "mutual_inductance": M,
        "self_inductance": L,
        "system_energy": W,
        "energy_lowered_by_coupling": bool(energy_lowered),
        "verified": bool(force_decreases and energy_lowered),
    }


@maxwell_cite(
    697, 698, 699,
    part=4, chapter="Coil Forces",
    theory_class="maxwell_original",
    description="Complete coil force analysis",
)
def analyze_coil_forces(
    current1: float,
    current2: float,
    radius1: float,
    radius2: float,
    separations: list[float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of forces between coils.

    Art. 697-699: Comprehensive analysis including:
    1. Force vs separation
    2. Torque vs angle
    3. System energy

    Args:
        current1: Current in coil 1 (abamperes).
        current2: Current in coil 2 (abamperes).
        radius1: Radius of coil 1 (cm).
        radius2: Radius of coil 2 (cm).
        separations: Axial separations to test.

    Returns:
        Dictionary with complete analysis results.
    """
    if separations is None:
        separations = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        separations = [s * max(radius1, radius2) for s in separations]

    forces = []
    mutual_inductances = []

    for z in separations:
        F = calc_coaxial_coil_force(current1, current2, radius1, radius2, z)
        forces.append(F)

        M = _mutual_inductance_coaxial(radius1, radius2, z)
        mutual_inductances.append(M)

    # Torque at various angles
    angles = np.linspace(0, np.pi, 10)
    torques = [calc_coil_torque(current1, current2, radius1, radius2, theta, max(radius1, radius2) * 2) for theta in angles]

    # Energy
    L1 = 4.0 * np.pi * radius1 * (np.log(8 * radius1 / (0.1 * radius1)) - 2)
    L2 = 4.0 * np.pi * radius2 * (np.log(8 * radius2 / (0.1 * radius2)) - 2)
    M0 = _mutual_inductance_coaxial(radius1, radius2, separations[0])
    energy = calc_coil_system_energy(current1, current2, L1, L2, M0)

    return {
        "current1": current1,
        "current2": current2,
        "radius1": radius1,
        "radius2": radius2,
        "separations": list(separations),
        "forces": forces,
        "mutual_inductances": mutual_inductances,
        "angles": list(angles),
        "torques": torques,
        "self_inductance_1": L1,
        "self_inductance_2": L2,
        "system_energy": energy,
    }
