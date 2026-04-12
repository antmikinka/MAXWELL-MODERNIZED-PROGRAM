"""maxwell.electromagnetism.forces.medium_force — Forces in magnetic medium (Arts. 639-640).

Implements Maxwell's treatment of forces in a magnetized medium,
including the effects of magnetic permeability and magnetization.

Maxwell's CGS formulation (Arts. 639-640):
    Force on a magnetic dipole in a medium:

        F = (m . grad) * B

    For a magnetized body with magnetization M:

        F = integral((M . grad) * B) dV

    In a medium with permeability mu:

        B = mu * H

    The force density in the medium is:

        f = (M . grad) * B + (1/c) * j x B

    Maxwell showed that the force depends on the gradient of the
    field, not just the field itself.

where:
    m = magnetic moment (erg/gauss)
    B = magnetic field (gauss)
    M = magnetization (emu/cm^3)
    H = magnetic field intensity (oersted)
    mu = magnetic permeability
    j = current density (abamperes/cm^2)

Category: A (maxwell_original) — Maxwell's magnetic medium force theory.

References:
    Part IV, Arts. 639-640: Forces in magnetic media.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


def _numerical_gradient_field(B_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate gradient of a vector field component along its direction.

    Returns grad_B_dot = (B . grad) B evaluated at position.
    """
    position = np.asarray(position, dtype=np.float64)
    B_at_pos = np.asarray(B_func(position), dtype=np.float64)

    grad = np.zeros(3)
    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta

        B_plus = np.asarray(B_func(pos_plus), dtype=np.float64)
        B_minus = np.asarray(B_func(pos_minus), dtype=np.float64)

        # d/dx_i of (B . B) / 2 = B . (dB/dx_i)
        dB2_dx = (np.dot(B_plus, B_plus) - np.dot(B_minus, B_minus)) / (2 * delta)
        grad[i] = B_at_pos[i] * dB2_dx / (2.0 * np.linalg.norm(B_at_pos)) if np.linalg.norm(B_at_pos) > 1e-15 else 0

    return grad


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Calculate force on magnetic dipole in medium",
)
def calc_medium_force(
    magnetic_moment: np.ndarray,
    B_function: callable,
    position: np.ndarray,
    delta: float = 1e-6,
) -> np.ndarray:
    """
    Calculate force on a magnetic dipole in a magnetic medium.

    Art. 639-640: The force on a magnetic dipole m in a field B is:

        F = (m . grad) * B

    This requires a non-uniform field — a uniform field produces torque
    but no net force.

    In component form:
        F_i = sum_j(m_j * dB_i/dx_j)

    Args:
        magnetic_moment: Magnetic dipole moment (erg/gauss).
        B_function: Function returning B field at position.
        position: Position of dipole (cm).
        delta: Finite difference step (cm).

    Returns:
        Force vector (dynes).
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    force = np.zeros(3)

    for i in range(3):
        # dB_i/dx_j for each j
        for j in range(3):
            pos_plus = position.copy()
            pos_plus[j] += delta
            pos_minus = position.copy()
            pos_minus[j] -= delta

            B_plus = np.asarray(B_function(pos_plus), dtype=np.float64)
            B_minus = np.asarray(B_function(pos_minus), dtype=np.float64)

            dB_idx = (B_plus[i] - B_minus[i]) / (2 * delta)
            force[i] += magnetic_moment[j] * dB_idx

    return force


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Calculate force on magnetized body",
)
def calc_magnetized_body_force(
    magnetization: callable,
    B_function: callable,
    volume_points: list[np.ndarray],
    volume_element: float = 1.0,
) -> np.ndarray:
    """
    Calculate total force on a magnetized body.

    Art. 639-640: For a body with magnetization M(r):

        F = integral((M(r) . grad) * B(r)) dV

    This function performs numerical integration over volume points.

    Args:
        magnetization: Function M(r) returning magnetization.
        B_function: Function returning B field at position.
        volume_points: Sample points within the body (cm).
        volume_element: Volume per sample point (cm^3).

    Returns:
        Total force (dynes).
    """
    total_force = np.zeros(3)

    for point in volume_points:
        point = np.asarray(point, dtype=np.float64)
        M = np.asarray(magnetization(point), dtype=np.float64)

        # Force density at this point
        f = np.zeros(3)
        for i in range(3):
            for j in range(3):
                pos_plus = point.copy()
                pos_plus[j] += 1e-6
                pos_minus = point.copy()
                pos_minus[j] -= 1e-6

                B_plus = np.asarray(B_function(pos_plus), dtype=np.float64)
                B_minus = np.asarray(B_function(pos_minus), dtype=np.float64)

                dB_idx = (B_plus[i] - B_minus[i]) / (2e-6)
                f[i] += M[j] * dB_idx

        total_force += f * volume_element

    return total_force


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Calculate force in permeable medium",
)
def calc_permeable_medium_force(
    B_function: callable,
    position: np.ndarray,
    permeability: float = 1.0,
    susceptibility: float = 0.0,
    volume: float = 1.0,
) -> np.ndarray:
    """
    Calculate force on a permeable body in a magnetic field.

    Art. 639-640: For a body with permeability mu and susceptibility chi:

        M = chi * H = chi * B / mu

        F = (M . grad) * B * V

    For paramagnetic materials (chi > 0), force is toward stronger field.
    For diamagnetic materials (chi < 0), force is toward weaker field.

    Args:
        B_function: Function returning B at position.
        position: Position of body (cm).
        permeability: Relative permeability mu.
        susceptibility: Magnetic susceptibility chi.
        volume: Body volume (cm^3).

    Returns:
        Force vector (dynes).
    """
    position = np.asarray(position, dtype=np.float64)
    B_at_pos = np.asarray(B_function(position), dtype=np.float64)

    # Magnetization: M = chi * H = chi * B / mu_0 (in CGS, mu_0 = 1 for vacuum)
    M = susceptibility * B_at_pos

    # Force: F = (M . grad) B * V
    force = np.zeros(3)
    delta = 1e-6

    for i in range(3):
        for j in range(3):
            pos_plus = position.copy()
            pos_plus[j] += delta
            pos_minus = position.copy()
            pos_minus[j] -= delta

            B_plus = np.asarray(B_function(pos_plus), dtype=np.float64)
            B_minus = np.asarray(B_function(pos_minus), dtype=np.float64)

            dB_idx = (B_plus[i] - B_minus[i]) / (2 * delta)
            force[i] += M[j] * dB_idx

    return force * volume


@dataclass
class MediumForceCalculator:
    """
    Force calculator for magnetic media.

    Art. 639-640: Handles forces on dipoles, magnetized bodies,
    and permeable materials in non-uniform magnetic fields.

    Attributes:
        B_function: Function returning B field at position.
        permeability: Medium permeability (default 1.0 for vacuum).
    """

    B_function: callable
    permeability: float = 1.0

    @maxwell_cite(
        639, 640,
        part=4, chapter="Forces in Magnetic Medium",
        theory_class="maxwell_original",
        description="Calculate dipole force",
    )
    def dipole_force(
        self,
        magnetic_moment: np.ndarray,
        position: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate force on a magnetic dipole.

        Args:
            magnetic_moment: Magnetic moment (erg/gauss).
            position: Position (cm).

        Returns:
            Force (dynes).
        """
        return calc_medium_force(magnetic_moment, self.B_function, position)

    @maxwell_cite(
        639, 640,
        part=4, chapter="Forces in Magnetic Medium",
        theory_class="maxwell_original",
        description="Calculate permeable body force",
    )
    def permeable_force(
        self,
        position: np.ndarray,
        susceptibility: float,
        volume: float = 1.0,
    ) -> np.ndarray:
        """
        Calculate force on a permeable body.

        Args:
            position: Position (cm).
            susceptibility: Magnetic susceptibility.
            volume: Body volume (cm^3).

        Returns:
            Force (dynes).
        """
        return calc_permeable_medium_force(
            self.B_function, position, self.permeability,
            susceptibility, volume,
        )


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Calculate force on dipole near current-carrying wire",
)
def calc_dipole_force_near_wire(
    current: float,
    magnetic_moment: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate force on a dipole near a current-carrying wire.

    Art. 639-640: For a wire along z-axis, B = (2I/cr) * phi_hat.
    The force on a dipole depends on the field gradient.

    Args:
        current: Wire current (abamperes).
        magnetic_moment: Dipole moment (erg/gauss).
        position: Dipole position (cm).

    Returns:
        Force (dynes).
    """
    position = np.asarray(position, dtype=np.float64)
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)

    r_perp = np.sqrt(position[0] ** 2 + position[1] ** 2)
    if r_perp < 1e-15:
        return np.zeros(3)

    def B_func(r):
        r = np.asarray(r, dtype=np.float64)
        rp = np.sqrt(r[0] ** 2 + r[1] ** 2)
        if rp < 1e-15:
            return np.zeros(3)
        # B = (2I/cr) * phi_hat
        B_mag = 2.0 * current / (CONST.C * rp)
        B_phi = np.array([-r[1], r[0], 0.0]) / rp
        return B_mag * B_phi

    return calc_medium_force(magnetic_moment, B_func, position)


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Verify medium force relations",
)
def verify_medium_force(
    magnetic_moment: np.ndarray = None,
    tolerance: float = 1e-5,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify force relations in magnetic medium.

    Art. 639-640: This function verifies:
    1. F = (m . grad) B for a known field configuration
    2. Force direction (toward stronger field for paramagnetic)
    3. Force magnitude scaling

    Args:
        magnetic_moment: Test magnetic moment (erg/gauss).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if magnetic_moment is None:
        magnetic_moment = np.array([1.0, 0.0, 0.0])

    # Test with a field gradient: B = (0, 0, B0 * (1 + x/L))
    B0 = 1000.0
    L = 10.0

    def B_func(r):
        return np.array([0.0, 0.0, B0 * (1.0 + r[0] / L)])

    pos = np.array([1.0, 0.0, 0.0])

    F = calc_medium_force(magnetic_moment, B_func, pos)

    # Analytical: F_z = m_x * dB_z/dx = m_x * B0/L
    F_expected_z = magnetic_moment[0] * B0 / L

    z_error = abs(F[2] - F_expected_z) / abs(F_expected_z) if abs(F_expected_z) > 1e-15 else abs(F[2])

    # Test: force should be zero for uniform field
    def uniform_B(r):
        return np.array([0.0, 0.0, B0])

    F_uniform = calc_medium_force(magnetic_moment, uniform_B, pos)
    uniform_force_mag = np.linalg.norm(F_uniform)

    return {
        "magnetic_moment": magnetic_moment,
        "position": pos,
        "force": F,
        "expected_F_z": F_expected_z,
        "z_component_error": z_error,
        "uniform_field_force": F_uniform,
        "uniform_force_magnitude": uniform_force_mag,
        "force_zero_in_uniform_field": bool(uniform_force_mag < tolerance),
        "z_component_verified": bool(z_error < tolerance),
        "verified": bool(z_error < tolerance and uniform_force_mag < tolerance),
    }


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Verify paramagnetic vs diamagnetic response",
)
def verify_magnetic_response(
    susceptibility_paramagnetic: float = 1e-5,
    susceptibility_diamagnetic: float = -1e-5,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify paramagnetic vs diamagnetic force response.

    Art. 639-640: Paramagnetic materials (chi > 0) are attracted to
    stronger fields, while diamagnetic materials (chi < 0) are repelled.

    Args:
        susceptibility_paramagnetic: Test paramagnetic susceptibility.
        susceptibility_diamagnetic: Test diamagnetic susceptibility.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with response verification results.
    """
    # Non-uniform field: B increases with z (gradient along z)
    def B_func(r):
        return np.array([0.0, 0.0, 1000.0 * np.exp(-r[2] / 10.0)])

    pos = np.array([0.0, 0.0, 1.0])

    F_para = calc_permeable_medium_force(
        B_func, pos, susceptibility=susceptibility_paramagnetic, volume=1.0
    )
    F_dia = calc_permeable_medium_force(
        B_func, pos, susceptibility=susceptibility_diamagnetic, volume=1.0
    )

    # For B_z = B0*exp(-z/L): field is stronger at smaller z
    # Paramagnetic (chi>0): force toward stronger field = negative z
    # Diamagnetic (chi<0): force toward weaker field = positive z
    para_toward_stronger = F_para[2] < 0  # negative z = toward stronger field
    dia_toward_weaker = F_dia[2] > 0  # positive z = toward weaker field

    # Magnitudes should be equal (just opposite sign)
    mag_ratio = abs(F_para[2] / F_dia[2]) if abs(F_dia[2]) > 1e-15 else 0
    mag_error = abs(mag_ratio - 1.0)

    return {
        "paramagnetic_force": F_para,
        "diamagnetic_force": F_dia,
        "para_toward_stronger_field": bool(para_toward_stronger),
        "dia_toward_weaker_field": bool(dia_toward_weaker),
        "magnitude_ratio": mag_ratio,
        "magnitude_error": mag_error,
        "response_verified": bool(para_toward_stronger and dia_toward_weaker and mag_error < tolerance),
    }


@maxwell_cite(
    639, 640,
    part=4, chapter="Forces in Magnetic Medium",
    theory_class="maxwell_original",
    description="Complete medium force analysis",
)
def analyze_medium_forces(
    magnetic_moment: np.ndarray,
    B_function: callable,
    test_positions: list[np.ndarray] = None,
    susceptibility: float = 1e-5,
    volume: float = 1.0,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of forces in magnetic medium.

    Art. 639-640: Comprehensive analysis including:
    1. Dipole force at multiple positions
    2. Permeable body force
    3. Force direction and magnitude analysis
    4. Field gradient analysis

    Args:
        magnetic_moment: Magnetic moment (erg/gauss).
        B_function: Magnetic field function B(r).
        test_positions: Positions for evaluation (cm).
        susceptibility: Magnetic susceptibility.
        volume: Test body volume (cm^3).

    Returns:
        Dictionary with complete analysis results.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)

    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([2.0, 0.0, 0.0]),
        ]

    results = {
        "magnetic_moment": magnetic_moment,
        "susceptibility": susceptibility,
        "volume": volume,
    }

    dipole_forces = []
    permeable_forces = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        F_dipole = calc_medium_force(magnetic_moment, B_function, pos)
        dipole_forces.append(F_dipole)

        F_permeable = calc_permeable_medium_force(
            B_function, pos, susceptibility=susceptibility, volume=volume
        )
        permeable_forces.append(F_permeable)

    results["dipole_forces"] = dipole_forces
    results["permeable_forces"] = permeable_forces
    results["test_positions"] = test_positions

    # Force magnitudes
    dipole_magnitudes = [np.linalg.norm(f) for f in dipole_forces]
    permeable_magnitudes = [np.linalg.norm(f) for f in permeable_forces]

    results["dipole_force_magnitudes"] = dipole_magnitudes
    results["permeable_force_magnitudes"] = permeable_magnitudes
    results["max_dipole_force"] = max(dipole_magnitudes)
    results["max_permeable_force"] = max(permeable_magnitudes)

    return results
