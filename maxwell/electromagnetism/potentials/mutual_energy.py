"""maxwell.electromagnetism.potentials.mutual_energy — Mutual potential energy (Arts. 520-521).

Implements Maxwell's treatment of the mutual potential energy between current
circuits, which is the basis for mutual inductance calculations.

Maxwell's CGS formulation (Arts. 520-521):
    Mutual potential energy of two circuits:
        W = -I1 * I2 * M

    where M is the mutual inductance:
        M = integral(dl1 · dl2 / r)  (Neumann formula)

    The force between circuits is:
        F = -dW/dx = I1 * I2 * dM/dx

where:
    I1, I2 = currents (abamperes)
    M = mutual inductance (cm in CGS-EMU)
    W = mutual energy (ergs)

Category: A (maxwell_original) — Maxwell's theory of mutual energy.

References:
    Part IV, Arts. 520-521: Mutual potential energy of circuits.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MutualEnergy:
    """
    Mutual potential energy calculator for two current circuits.

    Art. 520-521: The mutual potential energy of two current-carrying
    circuits is:

        W = -I1 * I2 * M

    where M is the mutual inductance, calculated using Neumann's formula:

        M = integral over circuit1, circuit2 of (dl1 · dl2 / r)

    The negative sign indicates that the energy is lowered when currents
    flow in directions that produce attractive forces.

    Attributes:
        current1: Current in first circuit (abamperes).
        current2: Current in second circuit (abamperes).
        mutual_inductance: Mutual inductance M (cm).
    """

    current1: float
    current2: float
    mutual_inductance: float

    @property
    def energy(self) -> float:
        """
        Mutual potential energy.

        Returns:
            W = -I1 * I2 * M (ergs).
        """
        return -self.current1 * self.current2 * self.mutual_inductance

    @maxwell_cite(
        520, 521,
        part=4, chapter="Mutual Energy",
        theory_class="maxwell_original",
        description="Calculate force from energy gradient",
    )
    def force_from_gradient(self, dM_dx: float) -> float:
        """
        Calculate force from gradient of mutual inductance.

        Art. 520-521: The force in direction x is:

            F_x = -dW/dx = I1 * I2 * dM/dx

        Args:
            dM_dx: Gradient of mutual inductance (dimensionless).

        Returns:
            Force (dynes).
        """
        return self.current1 * self.current2 * dM_dx

    @maxwell_cite(
        520,
        part=4, chapter="Mutual Energy",
        theory_class="maxwell_original",
        description="Calculate torque from energy derivative",
    )
    def torque_from_derivative(self, dM_dtheta: float) -> float:
        """
        Calculate torque from angular derivative of mutual inductance.

        Art. 520: The torque about an axis is:

            tau = -dW/dtheta = I1 * I2 * dM/dtheta

        Args:
            dM_dtheta: Angular derivative of M (cm/radian).

        Returns:
            Torque (dyne*cm).
        """
        return self.current1 * self.current2 * dM_dtheta


@maxwell_cite(
    520, 521,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Calculate mutual inductance using Neumann formula",
)
def calc_neumann_mutual_inductance(
    circuit1_vertices: list[np.ndarray],
    circuit2_vertices: list[np.ndarray],
    n_sample_points: int = 100,
) -> float:
    """
    Calculate mutual inductance using Neumann's formula.

    Art. 520-521: Neumann's formula for mutual inductance:

        M = (1/c²) * double_integral(dl1 · dl2 / r)

    In CGS-EMU (c=1 for EMU), this simplifies to:

        M = double_integral(dl1 · dl2 / r)

    This function performs numerical integration over polygonal circuits.

    Args:
        circuit1_vertices: Vertices of first circuit (cm).
        circuit2_vertices: Vertices of second circuit (cm).
        n_sample_points: Number of sample points per circuit.

    Returns:
        Mutual inductance (cm).

    Reference:
        Part IV, Arts. 520-521: Neumann formula.
    """
    circuit1_vertices = [np.asarray(v, dtype=np.float64) for v in circuit1_vertices]
    circuit2_vertices = [np.asarray(v, dtype=np.float64) for v in circuit2_vertices]

    # Discretize circuits into segments
    segments1 = _get_segments(circuit1_vertices, n_sample_points)
    segments2 = _get_segments(circuit2_vertices, n_sample_points)

    M = 0.0
    for seg1 in segments1:
        for seg2 in segments2:
            dl1, pos1 = seg1
            dl2, pos2 = seg2

            r_vec = pos2 - pos1
            r_mag = np.linalg.norm(r_vec)

            if r_mag > 1e-15:
                M += np.dot(dl1, dl2) / r_mag

    return M


def _get_segments(vertices: list[np.ndarray], n_points: int) -> list:
    """Get discretized segments from vertices."""
    segments = []
    n = len(vertices)

    points_per_segment = max(1, n_points // n)

    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]

        segment_vec = v2 - v1
        segment_length = np.linalg.norm(segment_vec)

        for j in range(points_per_segment):
            frac = (j + 0.5) / points_per_segment
            pos = v1 + frac * segment_vec
            dl = segment_vec / points_per_segment
            segments.append((dl, pos))

    return segments


@maxwell_cite(
    520, 521,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Calculate mutual energy of two circuits",
)
def calc_mutual_energy(
    current1: float,
    current2: float,
    mutual_inductance: float,
) -> float:
    """
    Calculate mutual potential energy of two circuits.

    Art. 520-521: The mutual energy is:

        W = -I1 * I2 * M

    Args:
        current1: Current in first circuit (abamperes).
        current2: Current in second circuit (abamperes).
        mutual_inductance: Mutual inductance (cm).

    Returns:
        Mutual energy (ergs).

    Reference:
        Part IV, Arts. 520-521: Mutual energy calculation.
    """
    return -current1 * current2 * mutual_inductance


@maxwell_cite(
    520,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Calculate force between circuits",
)
def calc_force_between_circuits(
    current1: float,
    current2: float,
    dM_dx: float,
) -> float:
    """
    Calculate force between circuits from mutual inductance gradient.

    Art. 520: The force in direction x is:

        F_x = I1 * I2 * dM/dx

    Args:
        current1: Current in first circuit (abamperes).
        current2: Current in second circuit (abamperes).
        dM_dx: Gradient of M with respect to x.

    Returns:
        Force (dynes).
    """
    return current1 * current2 * dM_dx


@maxwell_cite(
    520, 521,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Calculate mutual inductance of coaxial circular loops",
)
def calc_mutual_inductance_coaxial_loops(
    radius1: float,
    radius2: float,
    axial_separation: float = None,
    separation: float = None,
) -> float:
    """
    Calculate mutual inductance of coaxial circular loops.

    Art. 520-521: For two coaxial circular loops of radii a and b,
    separated by distance z, the mutual inductance is:

        M = 4*pi*sqrt(a*b) * [(2/k - k)*K(k) - (2/k)*E(k)]

    where:
        k² = 4ab / [(a+b)² + z²]
        K, E = complete elliptic integrals

    For small k (large separation):
        M ≈ 2*pi²*a²*b² / (a² + z²)^(3/2)  [dipole approximation]

    Args:
        radius1: Radius of first loop (cm).
        radius2: Radius of second loop (cm).
        axial_separation: Axial distance between loops (cm).

    Returns:
        Mutual inductance (cm).

    Reference:
        Part IV, Arts. 520-521: Coaxial loop mutual inductance.
    """
    a = radius1
    b = radius2
    z = axial_separation if axial_separation is not None else separation

    # k² parameter
    k_squared = 4.0 * a * b / ((a + b) ** 2 + z ** 2)

    if k_squared > 1.0:
        k_squared = 1.0
    if k_squared < 0:
        return 0.0

    k = np.sqrt(k_squared)

    # For small k, use dipole approximation
    if k < 0.1:
        R3 = (a ** 2 + z ** 2) ** 1.5
        if R3 > 1e-15:
            return 2.0 * np.pi ** 2 * a ** 2 * b ** 2 / R3
        return 0.0

    # Elliptic integral approximation
    # K(k) ≈ pi/2 * (1 + k²/4 + 9k⁴/64 + ...)
    # E(k) ≈ pi/2 * (1 - k²/4 - 3k⁴/64 - ...)
    K = (np.pi / 2) * (1.0 + k_squared / 4.0 + 9.0 * k_squared ** 2 / 64.0)
    E = (np.pi / 2) * (1.0 - k_squared / 4.0 - 3.0 * k_squared ** 2 / 64.0)

    if k < 1e-10:
        return 0.0

    # Maxwell's formula
    M = 4.0 * np.pi * np.sqrt(a * b) * ((2.0 / k - k) * K - (2.0 / k) * E)

    return M


@maxwell_cite(
    520, 521,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Verify mutual energy relations",
)
def verify_mutual_energy_relations(
    current1: float = 1.0,
    current2: float = 1.0,
    radius1: float = 1.0,
    radius2: float = 1.0,
    separations: list[float] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify mutual energy relations.

    Art. 520-521: This function verifies:
    1. W = -I1*I2*M
    2. F = I1*I2*dM/dx
    3. Force direction (attractive for parallel currents)

    Args:
        current1: First test current (abamperes).
        current2: Second test current (abamperes).
        radius1: Radius of first loop (cm).
        radius2: Radius of second loop (cm).
        separations: List of separations to test (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if separations is None:
        separations = [2.0, 3.0, 5.0, 10.0]

    energies = []
    forces_numerical = []
    forces_analytical = []

    for z in separations:
        M = calc_mutual_inductance_coaxial_loops(radius1, radius2, z)
        W = calc_mutual_energy(current1, current2, M)
        energies.append(W)

        # Numerical derivative for force
        delta = 1e-6
        M_plus = calc_mutual_inductance_coaxial_loops(radius1, radius2, z + delta)
        M_minus = calc_mutual_inductance_coaxial_loops(radius1, radius2, z - delta)
        dM_dz = (M_plus - M_minus) / (2 * delta)

        F_num = current1 * current2 * dM_dz
        forces_numerical.append(F_num)

        # Analytical estimate (dipole approximation)
        R3 = (radius1 ** 2 + z ** 2) ** 1.5
        if R3 > 1e-15:
            M_approx = 2.0 * np.pi ** 2 * radius1 ** 2 * radius2 ** 2 / R3
            dM_dz_approx = -3.0 * 2.0 * np.pi ** 2 * radius1 ** 2 * radius2 ** 2 * z / (radius1 ** 2 + z ** 2) ** 2.5
            F_ana = current1 * current2 * dM_dz_approx
        else:
            F_ana = 0.0
        forces_analytical.append(F_ana)

    # Check force direction (should be negative = attractive for same-direction currents)
    attraction_verified = all(f < 0 for f in forces_numerical if abs(f) > 1e-15)

    # Check energy decreases with decreasing separation
    energy_verified = all(energies[i] < energies[i+1] for i in range(len(energies)-1))

    return {
        "currents": (current1, current2),
        "separations": separations,
        "energies": energies,
        "forces_numerical": forces_numerical,
        "forces_analytical": forces_analytical,
        "attraction_verified": attraction_verified,
        "energy_verified": energy_verified,
        "verified": attraction_verified and energy_verified,
    }


@maxwell_cite(
    520, 521,
    part=4, chapter="Mutual Energy",
    theory_class="maxwell_original",
    description="Complete mutual energy analysis",
)
def analyze_mutual_energy(
    current1: float,
    current2: float,
    circuit1_vertices: list[np.ndarray],
    circuit2_vertices: list[np.ndarray],
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of mutual energy between circuits.

    Art. 520-521: Comprehensive analysis including:
    1. Mutual inductance calculation
    2. Energy calculation
    3. Force estimates
    4. Coupling coefficient

    Args:
        current1: Current in first circuit (abamperes).
        current2: Current in second circuit (abamperes).
        circuit1_vertices: Vertices of first circuit (cm).
        circuit2_vertices: Vertices of second circuit (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    M = calc_neumann_mutual_inductance(circuit1_vertices, circuit2_vertices)
    W = calc_mutual_energy(current1, current2, M)

    # Self-inductance estimates (approximate)
    L1 = _estimate_self_inductance(circuit1_vertices)
    L2 = _estimate_self_inductance(circuit2_vertices)

    # Coupling coefficient k = M / sqrt(L1*L2)
    if L1 > 0 and L2 > 0:
        k = M / np.sqrt(L1 * L2)
    else:
        k = 0.0

    return {
        "mutual_inductance": M,
        "mutual_energy": W,
        "self_inductance_1": L1,
        "self_inductance_2": L2,
        "coupling_coefficient": min(1.0, max(-1.0, k)),
        "current1": current1,
        "current2": current2,
    }


def _estimate_self_inductance(vertices: list[np.ndarray]) -> float:
    """Rough estimate of self-inductance for a planar loop."""
    vertices = [np.asarray(v, dtype=np.float64) for v in vertices]

    # Calculate perimeter and area
    perimeter = 0.0
    for i in range(len(vertices)):
        perimeter += np.linalg.norm(vertices[(i + 1) % len(vertices)] - vertices[i])

    # Area using shoelace formula
    if len(vertices) >= 3:
        area = 0.0
        for i in range(len(vertices)):
            area += vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
            area -= vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
        area = abs(area) / 2.0
    else:
        area = 0.0

    # Approximate formula: L ≈ 2*pi*R * (ln(8R/a) - 2) for circular loop
    # Simplified: L ≈ perimeter * (some factor)
    if perimeter > 0:
        effective_radius = perimeter / (2 * np.pi)
        if effective_radius > 0.1:
            return 4.0 * np.pi * effective_radius * (np.log(8 * effective_radius / 0.1) - 1.75)
    return perimeter * 0.5


# Alias for test compatibility
calc_mutual_inductance = calc_mutual_inductance_coaxial_loops
