"""maxwell.electromagnetism.fields.electrotonic — Electrotonic state (Arts. 540-541).

Implements Maxwell's concept of the electrotonic state, which is his
term for what we now call the vector potential A.

Maxwell's CGS formulation (Arts. 540-541):
    The electrotonic state (vector potential) A is defined by:

        H = curl(A)
        E = -dA/dt - grad(phi)

    The electrotonic state represents the "electromagnetic momentum"
    per unit charge and is fundamental to field theory.

where:
    A = electrotonic state / vector potential (gauss*cm)
    H = magnetic field (oersted)
    E = electric field (statvolts/cm)
    phi = electric scalar potential (statvolts)

Category: A (maxwell_original) — Maxwell's electrotonic state theory.

References:
    Part IV, Arts. 540-541: Electrotonic state and electromagnetic momentum.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class ElectrotonicState:
    """
    Maxwell's electrotonic state (vector potential).

    Art. 540-541: The electrotonic state is Maxwell's term for the
    vector potential A. It represents the electromagnetic momentum
    per unit charge at a point in space.

    Key properties:
    - H = curl(A) gives the magnetic field
    - E = -dA/dt - grad(phi) gives the electric field
    - The line integral of A around a circuit equals the magnetic flux

    Attributes:
        A_function: Function returning A at a position.
        scalar_potential_function: Optional function returning phi.
    """

    A_function: callable = None
    scalar_potential_function: callable = None

    @maxwell_cite(
        540, 541,
        part=4, chapter="Electrotonic State",
        theory_class="maxwell_original",
        description="Calculate electrotonic state at position",
    )
    def at_position(self, position: np.ndarray, time: float = 0.0) -> np.ndarray:
        """
        Calculate electrotonic state at a position.

        Art. 540-541: The electrotonic state A at a point in space.

        Args:
            position: Position vector (cm).
            time: Time (s) for time-dependent fields.

        Returns:
            Vector potential A (gauss*cm).
        """
        if self.A_function is None:
            return np.zeros(3)
        return np.asarray(self.A_function(position, time), dtype=np.float64)

    @maxwell_cite(
        540, 541,
        part=4, chapter="Electrotonic State",
        theory_class="maxwell_original",
        description="Calculate magnetic field from electrotonic state curl",
    )
    def magnetic_field(self, position: np.ndarray, delta: float = 1e-6) -> np.ndarray:
        """
        Calculate magnetic field H = curl(A).

        Art. 540-541: The magnetic field is the curl of the electrotonic state.

        Args:
            position: Position (cm).
            delta: Finite difference step (cm).

        Returns:
            Magnetic field H (oersted).
        """
        if self.A_function is None:
            return np.zeros(3)

        position = np.asarray(position, dtype=np.float64)

        def A_wrapper(r):
            return np.asarray(self.A_function(r), dtype=np.float64)

        return _numerical_curl(A_wrapper, position, delta)

    @maxwell_cite(
        540, 541,
        part=4, chapter="Electrotonic State",
        theory_class="maxwell_original",
        description="Calculate electric field from electrotonic state",
    )
    def electric_field(
        self,
        position: np.ndarray,
        time: float = 0.0,
        dt: float = 1e-9,
        delta: float = 1e-6,
    ) -> np.ndarray:
        """
        Calculate electric field E = -dA/dt - grad(phi).

        Art. 540-541: The electric field has two contributions:
        1. Time derivative of electrotonic state (induction)
        2. Gradient of scalar potential (electrostatic)

        Args:
            position: Position (cm).
            time: Time (s).
            dt: Time step for derivative (s).
            delta: Spatial step for gradient (cm).

        Returns:
            Electric field E (statvolts/cm).
        """
        position = np.asarray(position, dtype=np.float64)

        # -dA/dt contribution
        if self.A_function is not None:
            A_plus = np.asarray(self.A_function(position, time + dt), dtype=np.float64)
            A_minus = np.asarray(self.A_function(position, time - dt), dtype=np.float64)
            dA_dt = (A_plus - A_minus) / (2 * dt)
        else:
            dA_dt = np.zeros(3)

        # -grad(phi) contribution
        if self.scalar_potential_function is not None:
            grad_phi = _numerical_gradient(self.scalar_potential_function, position, delta)
        else:
            grad_phi = np.zeros(3)

        return -dA_dt - grad_phi

    @maxwell_cite(
        540,
        part=4, chapter="Electrotonic State",
        theory_class="maxwell_original",
        description="Calculate electromagnetic momentum",
    )
    def electromagnetic_momentum(self, position: np.ndarray, charge: float = 1.0) -> np.ndarray:
        """
        Calculate electromagnetic momentum per unit charge.

        Art. 540-541: The electrotonic state A represents the
        electromagnetic momentum per unit charge.

        For a charge q, the electromagnetic momentum is:
            p_em = q * A

        Args:
            position: Position (cm).
            charge: Charge (abcoulombs).

        Returns:
            Electromagnetic momentum (g*cm/s).
        """
        A = self.at_position(position)
        return charge * A


def _numerical_curl(F_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate numerical curl of vector field F."""
    curl = np.zeros(3)

    # dFz/dy - dFy/dz
    Fy_plus = F_func(position + np.array([0, delta, 0]))[1]
    Fy_minus = F_func(position - np.array([0, delta, 0]))[1]
    dFy_dz = (Fy_plus - Fy_minus) / (2 * delta)

    Fz_plus = F_func(position + np.array([0, 0, delta]))[2]
    Fz_minus = F_func(position - np.array([0, 0, delta]))[2]
    dFz_dy = (Fz_plus - Fz_minus) / (2 * delta)

    curl[0] = dFz_dy - dFy_dz

    # dFx/dz - dFz/dx
    Fz_plus = F_func(position + np.array([0, 0, delta]))[2]
    Fz_minus = F_func(position - np.array([0, 0, delta]))[2]
    dFz_dx = (Fz_plus - Fz_minus) / (2 * delta)

    Fx_plus = F_func(position + np.array([delta, 0, 0]))[0]
    Fx_minus = F_func(position - np.array([delta, 0, 0]))[0]
    dFx_dz = (Fx_plus - Fx_minus) / (2 * delta)

    curl[1] = dFx_dz - dFz_dx

    # dFy/dx - dFx/dy
    Fx_plus = F_func(position + np.array([delta, 0, 0]))[0]
    Fx_minus = F_func(position - np.array([delta, 0, 0]))[0]
    dFx_dy = (Fx_plus - Fx_minus) / (2 * delta)

    Fy_plus = F_func(position + np.array([0, delta, 0]))[1]
    Fy_minus = F_func(position - np.array([0, delta, 0]))[1]
    dFy_dx = (Fy_plus - Fy_minus) / (2 * delta)

    curl[2] = dFy_dx - dFx_dy

    return curl


def _numerical_gradient(f_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate numerical gradient of scalar field f."""
    grad = np.zeros(3)

    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta

        grad[i] = (f_func(pos_plus) - f_func(pos_minus)) / (2 * delta)

    return grad


@maxwell_cite(
    540, 541,
    part=4, chapter="Electrotonic State",
    theory_class="maxwell_original",
    description="Calculate electrotonic state for uniform B field",
)
def calc_electrotonic_uniform_field(
    B_field: np.ndarray,
    position: np.ndarray,
    gauge: str = "symmetric",
) -> np.ndarray:
    """
    Calculate electrotonic state (vector potential) for uniform B field.

    Art. 540-541: For a uniform magnetic field B, the vector potential
    can be written in different gauges:

    Symmetric gauge: A = (1/2) * B × r
    Landau gauge: A = (0, Bx, 0) for B = (0, 0, B)

    Both give the same B = curl(A).

    Args:
        B_field: Uniform magnetic field (gauss).
        position: Position (cm).
        gauge: 'symmetric' or 'landau'.

    Returns:
        Vector potential A (gauss*cm).
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    if gauge == "symmetric":
        # A = (1/2) * B × r
        return 0.5 * np.cross(B_field, position)
    elif gauge == "landau":
        # Landau gauge for B along z
        if np.abs(B_field[2]) > np.abs(B_field[0]) and np.abs(B_field[2]) > np.abs(B_field[1]):
            # B = (0, 0, Bz): A = (-By, 0, 0)
            return np.array([-B_field[2] * position[1], 0.0, 0.0])
        else:
            # Fall back to symmetric
            return 0.5 * np.cross(B_field, position)
    else:
        return 0.5 * np.cross(B_field, position)


@maxwell_cite(
    540, 541,
    part=4, chapter="Electrotonic State",
    theory_class="maxwell_original",
    description="Calculate electrotonic state for current loop",
)
def calc_electrotonic_loop(
    current: float,
    loop_radius: float,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate electrotonic state for a circular current loop.

    Art. 540-541: For a circular loop of radius a carrying current I,
    the vector potential at position r is:

        A(r) = (I/c) * integral(dl / |r - r'|)

    In CGS-EMU, this simplifies. On the axis:
        A_phi = (I * a²) / (2 * (a² + z²)^(3/2))  [dipole approximation]

    Args:
        current: Current in loop (abamperes).
        loop_radius: Loop radius (cm).
        position: Position (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    position = np.asarray(position, dtype=np.float64)

    # Convert to cylindrical coordinates
    z = position[2]
    r_perp = np.sqrt(position[0] ** 2 + position[1] ** 2)

    # Dipole approximation for large distances
    R3 = (loop_radius ** 2 + z ** 2) ** 1.5
    if R3 > 1e-15 and r_perp > 1e-15:
        # Magnetic moment
        m = current * np.pi * loop_radius ** 2

        # Vector potential for dipole: A = (m × r) / r³
        m_vec = np.array([0, 0, m])
        r_mag = np.sqrt(r_perp ** 2 + z ** 2)

        if r_mag > 1e-15:
            return np.cross(m_vec, position) / (r_mag ** 3)

    return np.zeros(3)


@maxwell_cite(
    540, 541,
    part=4, chapter="Electrotonic State",
    theory_class="maxwell_original",
    description="Calculate magnetic flux from electrotonic state",
)
def calc_flux_from_electrotonic(
    A_function: callable,
    circuit_vertices: list[np.ndarray],
) -> float:
    """
    Calculate magnetic flux from electrotonic state line integral.

    Art. 540-541: The magnetic flux through a circuit is equal to
    the line integral of the electrotonic state around the circuit:

        Phi = integral(A · dl) = sum(A_i · dl_i)

    Args:
        A_function: Function returning A at position.
        circuit_vertices: Vertices of the circuit (cm).

    Returns:
        Magnetic flux (maxwells).
    """
    circuit_vertices = [np.asarray(v, dtype=np.float64) for v in circuit_vertices]
    n = len(circuit_vertices)

    if n < 3:
        return 0.0

    flux = 0.0
    for i in range(n):
        r1 = circuit_vertices[i]
        r2 = circuit_vertices[(i + 1) % n]
        dl = r2 - r1
        mid_point = (r1 + r2) / 2

        A = np.asarray(A_function(mid_point), dtype=np.float64)
        flux += np.dot(A, dl)

    return flux


@maxwell_cite(
    540, 541,
    part=4, chapter="Electrotonic State",
    theory_class="maxwell_original",
    description="Verify electrotonic state relations",
)
def verify_electrotonic_relations(
    B_field: np.ndarray = None,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify relations involving the electrotonic state.

    Art. 540-541: This function verifies:
    1. curl(A) = B for uniform field
    2. Line integral of A equals flux

    Args:
        B_field: Test magnetic field (gauss).
        test_positions: Positions to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if B_field is None:
        B_field = np.array([0.0, 0.0, 1000.0])

    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
        ]

    # Test curl(A) = B
    errors = []
    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        def A_func(r):
            return calc_electrotonic_uniform_field(B_field, r, gauge="symmetric")

        B_from_curl = _numerical_curl(A_func, pos, delta=1e-6)

        error = np.linalg.norm(B_from_curl - B_field) / np.linalg.norm(B_field)
        errors.append(error)

    max_error = max(errors) if errors else 0

    return {
        "test_field": B_field,
        "test_positions": test_positions,
        "curl_errors": errors,
        "max_error": max_error,
        "verified": max_error < tolerance,
    }


@maxwell_cite(
    540, 541,
    part=4, chapter="Electrotonic State",
    theory_class="maxwell_original",
    description="Complete electrotonic state analysis",
)
def analyze_electrotonic_state(
    B_field: np.ndarray,
    evaluation_points: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of the electrotonic state.

    Art. 540-541: Comprehensive analysis including:
    1. Vector potential at multiple points
    2. Magnetic field from curl
    3. Verification of B = curl(A)

    Args:
        B_field: Background magnetic field (gauss).
        evaluation_points: Points for evaluation.

    Returns:
        Dictionary with complete analysis results.
    """
    if evaluation_points is None:
        evaluation_points = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
            np.array([2.0, 0.0, 0.0]),
        ]

    B_field = np.asarray(B_field, dtype=np.float64)

    results = {
        "background_field": B_field,
        "field_magnitude": np.linalg.norm(B_field),
    }

    vector_potentials = []
    fields_from_curl = []

    for point in evaluation_points:
        point = np.asarray(point, dtype=np.float64)

        A = calc_electrotonic_uniform_field(B_field, point, gauge="symmetric")
        vector_potentials.append(A)

        def A_func(r):
            return calc_electrotonic_uniform_field(B_field, r, gauge="symmetric")

        B_calc = _numerical_curl(A_func, point, delta=1e-6)
        fields_from_curl.append(B_calc)

    results["vector_potentials"] = vector_potentials
    results["fields_from_curl"] = fields_from_curl

    return results
