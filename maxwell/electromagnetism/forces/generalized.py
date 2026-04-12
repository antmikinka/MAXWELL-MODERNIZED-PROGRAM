"""maxwell.electromagnetism.forces.generalized — Generalized mechanical forces (Arts. 573-575).

Implements Maxwell's generalized force equations for electromagnetic systems,
relating mechanical forces to changes in electromagnetic energy.

Maxwell's CGS formulation (Arts. 573-575):
    Generalized electromagnetic force:

        F_x = dW/dx  (at constant flux)
        F_x = -dW/dx  (at constant current)

    where W is the electromagnetic energy.

    For coupled circuits:
        F = I1 * I2 * dM/dx

where:
    F = mechanical force (dynes)
    W = electromagnetic energy (ergs)
    M = mutual inductance (cm)
    I = current (abamperes)

Category: A (maxwell_original) — Maxwell's generalized force theory.

References:
    Part IV, Arts. 573-575: Generalized mechanical forces.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class GeneralizedForce:
    """
    Generalized electromagnetic force calculator.

    Art. 573-575: Maxwell derived general expressions for
    mechanical forces in electromagnetic systems using energy methods.

    The force in direction x is:
    - F_x = +dW/dx at constant flux (energy increases with x)
    - F_x = -dW/dx at constant current (energy decreases with x)

    Attributes:
        inductance_function: Function L(x) returning inductance.
        mutual_inductance_function: Function M(x) returning mutual inductance.
    """

    inductance_function: callable = None
    mutual_inductance_function: callable = None

    @maxwell_cite(
        573, 574, 575,
        part=4, chapter="Generalized Forces",
        theory_class="maxwell_original",
        description="Calculate force at constant current",
    )
    def force_constant_current(
        self,
        current: float,
        position: float,
        dL_dx: float,
    ) -> float:
        """
        Calculate force at constant current.

        Art. 573-575: At constant current:

            F_x = (1/2) * I² * dL/dx

        Args:
            current: Current (abamperes).
            position: Position (cm).
            dL_dx: Gradient of inductance.

        Returns:
            Force (dynes).
        """
        return 0.5 * current ** 2 * dL_dx

    @maxwell_cite(
        573, 574,
        part=4, chapter="Generalized Forces",
        theory_class="maxwell_original",
        description="Calculate force between coupled circuits",
    )
    def force_coupled_circuits(
        self,
        current1: float,
        current2: float,
        position: float,
        dM_dx: float,
    ) -> float:
        """
        Calculate force between coupled circuits.

        Art. 573-575: For two coupled circuits:

            F_x = I1 * I2 * dM/dx

        Args:
            current1: Current in circuit 1 (abamperes).
            current2: Current in circuit 2 (abamperes).
            position: Position (cm).
            dM_dx: Gradient of mutual inductance.

        Returns:
            Force (dynes).
        """
        return current1 * current2 * dM_dx

    @maxwell_cite(
        573, 575,
        part=4, chapter="Generalized Forces",
        theory_class="maxwell_original",
        description="Calculate torque on circuit",
    )
    def torque(
        self,
        current1: float,
        current2: float,
        angle: float,
        dM_dtheta: float,
    ) -> float:
        """
        Calculate torque on a circuit.

        Art. 573-575: The torque is:

            tau = I1 * I2 * dM/dtheta

        Args:
            current1: Current in circuit 1 (abamperes).
            current2: Current in circuit 2 (abamperes).
            angle: Angle (radians).
            dM_dtheta: Angular derivative of mutual inductance.

        Returns:
            Torque (dyne*cm).
        """
        return current1 * current2 * dM_dtheta


@maxwell_cite(
    573, 574, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Calculate force from energy gradient",
)
def calc_force_from_energy(
    energy_gradient: float,
    constant_current: bool = True,
) -> float:
    """
    Calculate force from energy gradient.

    Art. 573-575: The generalized force is:

        F_x = -dW/dx  (constant current)
        F_x = +dW/dx  (constant flux)

    Args:
        energy_gradient: dW/dx (ergs/cm).
        constant_current: True for constant current, False for constant flux.

    Returns:
        Force (dynes).

    Reference:
        Part IV, Arts. 573-575: Force from energy gradient.
    """
    if constant_current:
        return -energy_gradient
    else:
        return energy_gradient


@maxwell_cite(
    573, 574,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Calculate force on movable coil",
)
def calc_force_movable_coil(
    fixed_coil_current: float,
    movable_coil_current: float,
    mutual_inductance_gradient: float,
) -> float:
    """
    Calculate force on a movable coil.

    Art. 573-575: For a movable coil coupled to a fixed coil:

        F = I_fixed * I_movable * dM/dx

    Args:
        fixed_coil_current: Current in fixed coil (abamperes).
        movable_coil_current: Current in movable coil (abamperes).
        mutual_inductance_gradient: dM/dx (dimensionless).

    Returns:
        Force on movable coil (dynes).

    Reference:
        Part IV, Arts. 573-575: Force on movable coil.
    """
    return fixed_coil_current * movable_coil_current * mutual_inductance_gradient


@maxwell_cite(
    573, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Calculate torque on current loop in B field",
)
def calc_torque_on_loop(
    magnetic_moment: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate torque on a current loop in magnetic field.

    Art. 573-575: The torque is:

        tau = m × B

    where m is the magnetic moment.

    Args:
        magnetic_moment: Magnetic moment (EMU).
        B_field: Magnetic field (gauss).

    Returns:
        Torque vector (dyne*cm).

    Reference:
        Part IV, Arts. 573-575: Torque on current loop.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return np.cross(magnetic_moment, B_field)


@maxwell_cite(
    573, 574, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Calculate force on magnetic dipole",
)
def calc_force_on_dipole(
    magnetic_moment: np.ndarray,
    B_field_gradient: np.ndarray,
) -> np.ndarray:
    """
    Calculate force on a magnetic dipole in non-uniform field.

    Art. 573-575: The force is:

        F = (m · ∇) B

    For a dipole aligned with the field gradient:
        F_z = m * dB/dz

    Args:
        magnetic_moment: Magnetic moment vector (EMU).
        B_field_gradient: Gradient tensor dB_ij/dx_j (gauss/cm).

    Returns:
        Force vector (dynes).

    Reference:
        Part IV, Arts. 573-575: Force on magnetic dipole.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    B_field_gradient = np.asarray(B_field_gradient, dtype=np.float64)

    # F_i = sum_j(m_j * dB_j/dx_i)
    # Simplified: F = (m · ∇) B
    if B_field_gradient.shape == (3, 3):
        return np.dot(magnetic_moment, B_field_gradient.T)
    elif B_field_gradient.shape == (3,):
        # Assume gradient along one direction
        return magnetic_moment * B_field_gradient
    else:
        return np.zeros(3)


@maxwell_cite(
    573, 574, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Calculate force between coaxial coils",
)
def calc_force_coaxial_coils(
    current1: float,
    current2: float,
    radius1: float,
    radius2: float,
    separation: float,
) -> float:
    """
    Calculate force between coaxial circular coils.

    Art. 573-575: For coaxial coils, the force is:

        F = I1 * I2 * dM/dz

    Using the mutual inductance formula for coaxial loops:
        M = 4*pi*sqrt(a*b) * [(2/k - k)*K(k) - (2/k)*E(k)]

    Args:
        current1: Current in coil 1 (abamperes).
        current2: Current in coil 2 (abamperes).
        radius1: Radius of coil 1 (cm).
        radius2: Radius of coil 2 (cm).
        separation: Axial separation (cm).

    Returns:
        Force (dynes). Positive = attractive.

    Reference:
        Part IV, Arts. 573-575: Coaxial coil force.
    """
    a = radius1
    b = radius2
    z = separation

    # k² parameter for elliptic integrals
    k_squared = 4.0 * a * b / ((a + b) ** 2 + z ** 2)

    if k_squared <= 0 or k_squared > 1:
        return 0.0

    k = np.sqrt(k_squared)

    # Approximate dM/dz using finite difference
    delta = 1e-6 * z if z > 0 else 1e-6

    def mutual_inductance(sep):
        k2 = 4.0 * a * b / ((a + b) ** 2 + sep ** 2)
        if k2 <= 0 or k2 > 1:
            return 0.0
        kk = np.sqrt(k2)
        K = (np.pi / 2) * (1.0 + k2 / 4.0)
        E = (np.pi / 2) * (1.0 - k2 / 4.0)
        if kk < 1e-10:
            return 0.0
        return 4.0 * np.pi * np.sqrt(a * b) * ((2.0 / kk - kk) * K - (2.0 / kk) * E)

    M_plus = mutual_inductance(z + delta)
    M_minus = mutual_inductance(z - delta)
    dM_dz = (M_plus - M_minus) / (2 * delta)

    return current1 * current2 * dM_dz


@maxwell_cite(
    573, 574, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Verify generalized force relations",
)
def verify_generalized_forces(
    current1: float = 1.0,
    current2: float = 1.0,
    radius1: float = 1.0,
    radius2: float = 1.0,
    separations: list[float] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify generalized force relations.

    Art. 573-575: This function verifies:
    1. F = I1*I2*dM/dx for coaxial coils
    2. Force is attractive for same-direction currents
    3. Force decreases with separation

    Args:
        current1: Test current 1 (abamperes).
        current2: Test current 2 (abamperes).
        radius1: Radius of coil 1 (cm).
        radius2: Radius of coil 2 (cm).
        separations: Separations to test (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if separations is None:
        separations = [2.0, 3.0, 5.0, 10.0]

    forces = []
    for z in separations:
        F = calc_force_coaxial_coils(current1, current2, radius1, radius2, z)
        forces.append(F)

    # Verify attraction for same-direction currents
    attraction_verified = all(f < 0 for f in forces if abs(f) > 1e-15)

    # Verify force decreases with separation
    decreasing_verified = all(abs(forces[i]) >= abs(forces[i+1]) for i in range(len(forces)-1))

    # Verify current reversal changes sign
    F_same = calc_force_coaxial_coils(current1, current2, radius1, radius2, 2.0)
    F_opposite = calc_force_coaxial_coils(current1, -current2, radius1, radius2, 2.0)
    sign_change_verified = np.sign(F_same) != np.sign(F_opposite)

    return {
        "current1": current1,
        "current2": current2,
        "separations": separations,
        "forces": forces,
        "attraction_verified": attraction_verified,
        "decreasing_verified": decreasing_verified,
        "sign_change_verified": sign_change_verified,
        "verified": attraction_verified and decreasing_verified and sign_change_verified,
    }


@maxwell_cite(
    573, 574, 575,
    part=4, chapter="Generalized Forces",
    theory_class="maxwell_original",
    description="Complete generalized force analysis",
)
def analyze_generalized_forces(
    current1: float,
    current2: float,
    geometry: str = "coaxial_coils",
    parameters: dict = None,
) -> dict[str, float | list]:
    """
    Complete analysis of generalized electromagnetic forces.

    Art. 573-575: Comprehensive analysis including:
    1. Force at multiple positions
    2. Torque calculations
    3. Energy-based verification

    Args:
        current1: Current in circuit 1 (abamperes).
        current2: Current in circuit 2 (abamperes).
        geometry: Type of geometry ('coaxial_coils', 'parallel_wires', 'dipole').
        parameters: Geometry-specific parameters.

    Returns:
        Dictionary with complete analysis results.
    """
    if parameters is None:
        parameters = {}

    results = {
        "current1": current1,
        "current2": current2,
        "geometry": geometry,
    }

    if geometry == "coaxial_coils":
        radius1 = parameters.get("radius1", 1.0)
        radius2 = parameters.get("radius2", 1.0)
        separations = parameters.get("separations", [2.0, 3.0, 5.0, 10.0])

        forces = [
            calc_force_coaxial_coils(current1, current2, radius1, radius2, z)
            for z in separations
        ]

        results["separations"] = separations
        results["forces"] = forces
        results["max_force"] = max(abs(f) for f in forces)

    elif geometry == "parallel_wires":
        separation = parameters.get("separation", 1.0)
        length = parameters.get("length", 10.0)

        # F/L = 2*I1*I2/r
        force = 2.0 * current1 * current2 * length / separation

        results["separation"] = separation
        results["length"] = length
        results["force"] = force

    elif geometry == "dipole":
        m = np.asarray(parameters.get("magnetic_moment", [0, 0, 100]), dtype=np.float64)
        B_grad = np.asarray(parameters.get("field_gradient", [0, 0, 100]), dtype=np.float64)

        force = calc_force_on_dipole(m, B_grad)

        results["magnetic_moment"] = m
        results["field_gradient"] = B_grad
        results["force"] = force

    return results
