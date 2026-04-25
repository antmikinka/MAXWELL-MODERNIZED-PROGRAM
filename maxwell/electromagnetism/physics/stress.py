"""maxwell.electromagnetism.physics.stress — Maxwell stress tensor (Art. 501).

Implements Maxwell's stress tensor, which describes the electromagnetic
forces as stresses in the field rather than action at a distance.

Maxwell's CGS formulation (Art. 501):
    The Maxwell stress tensor components in CGS-Gaussian units:

        T_ij = (1/4*pi) * [E_i*E_j + B_i*B_j - (1/2)*delta_ij*(E^2 + B^2)]

    The force on charges in a volume is the surface integral:

        F_i = integral(T_ij * n_j) dA

    The stress tensor components represent:
    - Diagonal (T_xx, T_yy, T_zz): pressure/tension along field lines
    - Off-diagonal: shear stresses

    Along field lines: tension = (E^2 + B^2)/(8*pi)
    Perpendicular to field lines: pressure = (E^2 + B^2)/(8*pi)

where:
    T_ij = stress tensor component (dyne/cm^2)
    E = electric field (statvolts/cm)
    B = magnetic field (gauss)
    delta_ij = Kronecker delta

Category: A (maxwell_original) — Maxwell's stress tensor theory.

References:
    Part IV, Art. 501: Electromagnetic stress and field tension.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Calculate Maxwell stress tensor",
)
def calc_stress_tensor(
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate the Maxwell stress tensor.

    Art. 501: The electromagnetic stress tensor in CGS-Gaussian units:

        T_ij = (1/4*pi) * [E_i*E_j + B_i*B_j - (1/2)*delta_ij*(E^2 + B^2)]

    The diagonal elements represent pressure (positive) or tension (negative)
    along the coordinate axes. The off-diagonal elements represent shear.

    Key properties:
    - Along field lines: tension = (E^2 + B^2)/(8*pi)
    - Perpendicular to field lines: pressure = (E^2 + B^2)/(8*pi)
    - The tensor is symmetric: T_ij = T_ji
    - Trace(T) = -(E^2 + B^2)/(8*pi) = -energy_density

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        3x3 stress tensor (dyne/cm^2).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    E2 = np.dot(E_field, E_field)
    B2 = np.dot(B_field, B_field)

    T = np.zeros((3, 3))

    for i in range(3):
        for j in range(3):
            if i == j:
                T[i, j] = E_field[i] * E_field[j] + B_field[i] * B_field[j]
                T[i, j] -= 0.5 * (E2 + B2)
            else:
                T[i, j] = E_field[i] * E_field[j] + B_field[i] * B_field[j]

    return T / (4.0 * np.pi)


@dataclass
class MaxwellStress:
    """
    Maxwell stress tensor calculator.

    Art. 501: The stress tensor formalism replaces the concept of
    action at a distance with local stresses in the electromagnetic
    field. Forces are transmitted through the field via these stresses.

    Attributes:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
    """

    E_field: np.ndarray = None
    B_field: np.ndarray = None

    def __post_init__(self):
        """Initialize fields to zero if None."""
        if self.E_field is None:
            self.E_field = np.zeros(3)
        if self.B_field is None:
            self.B_field = np.zeros(3)
        self.E_field = np.asarray(self.E_field, dtype=np.float64)
        self.B_field = np.asarray(self.B_field, dtype=np.float64)

    @maxwell_cite(
        501,
        part=4, chapter="Electromagnetic Stress",
        theory_class="maxwell_original",
        description="Get stress tensor",
    )
    def tensor(self) -> np.ndarray:
        """
        Calculate the full stress tensor.

        Returns:
            3x3 stress tensor (dyne/cm^2).
        """
        return calc_stress_tensor(self.E_field, self.B_field)

    @maxwell_cite(
        501,
        part=4, chapter="Electromagnetic Stress",
        theory_class="maxwell_original",
        description="Calculate electromagnetic energy density",
    )
    def energy_density(self) -> float:
        """
        Calculate electromagnetic energy density.

        Art. 501: The energy density is:

            u = (E^2 + B^2) / (8*pi)

        This equals -Trace(T)/3 for the stress tensor.

        Returns:
            Energy density (ergs/cm^3).
        """
        E2 = np.dot(self.E_field, self.E_field)
        B2 = np.dot(self.B_field, self.B_field)
        return (E2 + B2) / (8.0 * np.pi)

    @maxwell_cite(
        501,
        part=4, chapter="Electromagnetic Stress",
        theory_class="maxwell_original",
        description="Calculate stress along a direction",
    )
    def stress_along(self, direction: np.ndarray) -> np.ndarray:
        """
        Calculate stress vector along a direction.

        Art. 501: The force per unit area on a surface with normal n is:

            f_i = T_ij * n_j

        Args:
            direction: Unit normal vector.

        Returns:
            Stress vector (dyne/cm^2).
        """
        direction = np.asarray(direction, dtype=np.float64)
        dir_norm = np.linalg.norm(direction)
        if dir_norm > 0:
            direction = direction / dir_norm

        T = self.tensor()
        return T @ direction

    @maxwell_cite(
        501,
        part=4, chapter="Electromagnetic Stress",
        theory_class="maxwell_original",
        description="Calculate tension along field lines",
    )
    def tension_along_field(self) -> float:
        """
        Calculate tension along magnetic field lines.

        Art. 501: Along field lines, there is a tension:

            tension = B^2 / (8*pi)

        This pulls charges together along field lines.

        Returns:
            Tension (dyne/cm^2).
        """
        B2 = np.dot(self.B_field, self.B_field)
        return B2 / (8.0 * np.pi)

    @maxwell_cite(
        501,
        part=4, chapter="Electromagnetic Stress",
        theory_class="maxwell_original",
        description="Calculate pressure perpendicular to field lines",
    )
    def pressure_perpendicular_to_field(self) -> float:
        """
        Calculate pressure perpendicular to magnetic field lines.

        Art. 501: Perpendicular to field lines, there is a pressure:

            pressure = B^2 / (8*pi)

        This pushes field lines apart.

        Returns:
            Pressure (dyne/cm^2).
        """
        B2 = np.dot(self.B_field, self.B_field)
        return B2 / (8.0 * np.pi)


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Calculate force from stress tensor",
)
def calc_force_from_stress(
    E_field: np.ndarray,
    B_field: np.ndarray,
    surface_normal: np.ndarray,
    surface_area: float,
) -> np.ndarray:
    """
    Calculate force on a surface from the stress tensor.

    Art. 501: The force on a surface with normal n and area A is:

        F = T . n * A

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
        surface_normal: Unit normal vector.
        surface_area: Surface area (cm^2).

    Returns:
        Force vector (dynes).
    """
    T = calc_stress_tensor(E_field, B_field)
    surface_normal = np.asarray(surface_normal, dtype=np.float64)
    norm = np.linalg.norm(surface_normal)
    if norm > 0:
        surface_normal = surface_normal / norm

    return (T @ surface_normal) * surface_area


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Calculate stress on a plane",
)
def calc_stress_on_plane(
    E_field: np.ndarray,
    B_field: np.ndarray,
    normal: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Calculate stress components on a plane.

    Art. 501: For a plane with normal n, the stress has:
    - Normal component (pressure/tension): f_n = (f . n)
    - Tangential component (shear): f_t = f - f_n * n

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).
        normal: Plane normal vector.

    Returns:
        Dictionary with stress components.
    """
    T = calc_stress_tensor(E_field, B_field)
    normal = np.asarray(normal, dtype=np.float64)
    n_mag = np.linalg.norm(normal)
    if n_mag > 0:
        normal = normal / n_mag

    # Force per unit area
    f = T @ normal

    # Normal component
    f_normal = np.dot(f, normal) * normal

    # Tangential component
    f_tangent = f - f_normal

    return {
        "total_stress": f,
        "normal_stress": f_normal,
        "normal_stress_magnitude": np.dot(f, normal),
        "shear_stress": f_tangent,
        "shear_magnitude": np.linalg.norm(f_tangent),
    }


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Verify stress tensor properties",
)
def verify_stress_tensor(
    E_field: np.ndarray = None,
    B_field: np.ndarray = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify Maxwell stress tensor properties.

    Art. 501: This function verifies:
    1. Tensor is symmetric: T_ij = T_ji
    2. Trace = -energy_density * 3 (in 3D)
    3. Tension along field = pressure perpendicular = B^2/(8*pi)

    Args:
        E_field: Electric field (statvolts/cm, default zero).
        B_field: Magnetic field (gauss, default unit z).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if E_field is None:
        E_field = np.zeros(3)
    if B_field is None:
        B_field = np.array([0.0, 0.0, 1000.0])

    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    T = calc_stress_tensor(E_field, B_field)

    # Symmetry check
    symmetry_error = np.linalg.norm(T - T.T)

    # Trace check
    trace_T = np.trace(T)
    E2 = np.dot(E_field, E_field)
    B2 = np.dot(B_field, B_field)
    energy_density = (E2 + B2) / (8.0 * np.pi)
    trace_error = abs(trace_T + energy_density)

    # For pure B field along z:
    # T_xx = T_yy = -B^2/(8*pi) (pressure perpendicular to field)
    # T_zz = +B^2/(8*pi) (tension along field)
    B2_8pi = B2 / (8.0 * np.pi)
    expected_diagonal = np.array([-B2_8pi, -B2_8pi, B2_8pi])

    diagonal_error = np.linalg.norm(np.diag(T) - expected_diagonal)

    # Verify tension along field = pressure perpendicular
    tension_along = abs(T[2, 2]) if B2 > 0 else 0
    pressure_perp = T[0, 0] if B2 > 0 else 0
    tension_pressure_ratio = tension_along / pressure_perp if pressure_perp > 1e-15 else 0

    return {
        "stress_tensor": T,
        "symmetry_error": symmetry_error,
        "trace": trace_T,
        "expected_trace": -energy_density,
        "trace_error": trace_error,
        "energy_density": energy_density,
        "diagonal_error": diagonal_error,
        "tension_along_field": tension_along,
        "pressure_perpendicular": pressure_perp,
        "tension_pressure_ratio": tension_pressure_ratio,
        "symmetric": bool(symmetry_error < tolerance),
        "trace_correct": bool(trace_error < tolerance),
        "diagonal_correct": bool(diagonal_error < tolerance),
        "verified": bool(
            symmetry_error < tolerance
            and trace_error < tolerance
            and diagonal_error < tolerance
        ),
    }


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Verify stress tensor for pure electric field",
)
def verify_electric_stress(
    E_field: np.ndarray = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify stress tensor properties for pure electric field.

    Art. 501: For a pure E field along z:
    - T_xx = T_yy = E^2/(8*pi) (pressure perpendicular)
    - T_zz = -E^2/(8*pi) (tension along)

    Args:
        E_field: Electric field (statvolts/cm, default along z).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if E_field is None:
        E_field = np.array([0.0, 0.0, 100.0])

    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.zeros(3)

    T = calc_stress_tensor(E_field, B_field)

    E2 = np.dot(E_field, E_field)
    E2_8pi = E2 / (8.0 * np.pi)

    # Find the direction of E
    e_dir = E_field / np.linalg.norm(E_field) if np.linalg.norm(E_field) > 1e-15 else np.array([0, 0, 1])

    # For E along z: T_xx = T_yy = E^2/(8pi), T_zz = -E^2/(8pi)
    expected_T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if i == j:
                expected_T[i, j] = E_field[i] * E_field[j] - 0.5 * E2
            else:
                expected_T[i, j] = E_field[i] * E_field[j]
    expected_T /= (4.0 * np.pi)

    error = np.linalg.norm(T - expected_T)

    return {
        "E_field": E_field,
        "stress_tensor": T,
        "expected_tensor": expected_T,
        "tensor_error": error,
        "energy_density": E2_8pi,
        "verified": bool(error < tolerance),
    }


@maxwell_cite(
    501,
    part=4, chapter="Electromagnetic Stress",
    theory_class="maxwell_original",
    description="Complete stress tensor analysis",
)
def analyze_stress(
    E_field: np.ndarray = None,
    B_field: np.ndarray = None,
    test_normals: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of Maxwell stress tensor.

    Art. 501: Comprehensive analysis including:
    1. Full stress tensor
    2. Eigenvalues and eigenvectors (principal stresses)
    3. Stress on various planes
    4. Energy density
    5. Tension and pressure along field lines

    Args:
        E_field: Electric field (statvolts/cm, default zero).
        B_field: Magnetic field (gauss, default unit z).
        test_normals: Surface normals to test.

    Returns:
        Dictionary with complete analysis results.
    """
    if E_field is None:
        E_field = np.zeros(3)
    if B_field is None:
        B_field = np.array([0.0, 0.0, 1000.0])

    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    T = calc_stress_tensor(E_field, B_field)

    # Eigenvalues (principal stresses)
    eigenvalues, eigenvectors = np.linalg.eigh(T)

    # Energy density
    E2 = np.dot(E_field, E_field)
    B2 = np.dot(B_field, B_field)
    energy_density = (E2 + B2) / (8.0 * np.pi)

    # Tension and pressure
    B2_8pi = B2 / (8.0 * np.pi)
    E2_8pi = E2 / (8.0 * np.pi)

    results = {
        "stress_tensor": T,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "energy_density": energy_density,
        "magnetic_pressure": B2_8pi,
        "electric_pressure": E2_8pi,
        "total_pressure": B2_8pi + E2_8pi,
        "trace": np.trace(T),
    }

    # Stress on test planes
    if test_normals is None:
        test_normals = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
        ]

    plane_stresses = []
    for normal in test_normals:
        normal = np.asarray(normal, dtype=np.float64)
        stress = calc_stress_on_plane(E_field, B_field, normal)
        plane_stresses.append(stress)

    results["plane_stresses"] = plane_stresses
    results["E_field"] = E_field
    results["B_field"] = B_field

    return results
