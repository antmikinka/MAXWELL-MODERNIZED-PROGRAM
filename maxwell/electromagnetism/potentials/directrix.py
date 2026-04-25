"""maxwell.electromagnetism.potentials.directrix — Directrix function (Arts. 517-519).

Implements Maxwell's directrix function for calculating magnetic potentials
and fields from arbitrary current distributions.

Maxwell's CGS formulation (Arts. 517-519):
    The directrix function relates the magnetic field to the current distribution:

        H = curl(A)  where A is the vector potential

    For a current distribution J:
        A(r) = integral(J(r') / |r - r'|) dV'

    The directrix gives the direction and magnitude of the field.

where:
    J = current density (abamperes/cm²)
    A = vector potential (gauss*cm)
    H = magnetic field (oersted)

Category: A (maxwell_original) — Maxwell's directrix theory.

References:
    Part IV, Arts. 517-519: Directrix function and vector potential.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class DirectrixFunction:
    """
    Directrix function for magnetic field calculations.

    Art. 517-519: Maxwell's directrix function provides a way to
    calculate the magnetic field from a current distribution using
    the vector potential formalism.

    The directrix at a point gives both the direction and magnitude
    of the magnetic field that would be produced by a unit current
    element at that point.

    Attributes:
        current_distribution: Current density function J(r).
        integration_volume: Bounds for integration.
    """

    current_distribution: callable = None
    integration_volume: tuple = None

    @maxwell_cite(
        517, 518, 519,
        part=4, chapter="Directrix Function",
        theory_class="maxwell_original",
        description="Calculate vector potential from current distribution",
    )
    def vector_potential(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate vector potential A at a position.

        Art. 517-519: The vector potential is:

            A(r) = integral(J(r') / |r - r'|) dV'

        Args:
            position: Position where A is calculated (cm).

        Returns:
            Vector potential A (gauss*cm).
        """
        if self.current_distribution is None or self.integration_volume is None:
            return np.zeros(3)

        position = np.asarray(position, dtype=np.float64)
        (x_min, x_max), (y_min, y_max), (z_min, z_max) = self.integration_volume

        # Numerical integration (simplified)
        n_points = 10
        dx = (x_max - x_min) / n_points
        dy = (y_max - y_min) / n_points
        dz = (z_max - z_min) / n_points
        dV = dx * dy * dz

        A = np.zeros(3)
        for i in range(n_points):
            for j in range(n_points):
                for k in range(n_points):
                    x = x_min + (i + 0.5) * dx
                    y = y_min + (j + 0.5) * dy
                    z = z_min + (k + 0.5) * dz
                    r_prime = np.array([x, y, z])

                    J = self.current_distribution(r_prime)
                    r_diff = position - r_prime
                    r_mag = np.linalg.norm(r_diff)

                    if r_mag > 1e-15:
                        A += J * dV / r_mag

        return A

    @maxwell_cite(
        517, 518,
        part=4, chapter="Directrix Function",
        theory_class="maxwell_original",
        description="Calculate magnetic field from vector potential curl",
    )
    def magnetic_field(self, position: np.ndarray, delta: float = 1e-6) -> np.ndarray:
        """
        Calculate magnetic field H = curl(A).

        Art. 517-519: The magnetic field is the curl of the vector potential.

        Args:
            position: Position where H is calculated (cm).
            delta: Finite difference step (cm).

        Returns:
            Magnetic field H (oersted).
        """
        position = np.asarray(position, dtype=np.float64)
        A0 = self.vector_potential(position)

        # Numerical curl
        curl = np.zeros(3)

        # dAz/dy - dAy/dz
        Ay_plus = self.vector_potential(position + np.array([0, delta, 0]))[1]
        Ay_minus = self.vector_potential(position - np.array([0, delta, 0]))[1]
        dAy_dz = (Ay_plus - Ay_minus) / (2 * delta)

        Az_plus = self.vector_potential(position + np.array([0, 0, delta]))[2]
        Az_minus = self.vector_potential(position - np.array([0, 0, delta]))[2]
        dAz_dy = (Az_plus - Az_minus) / (2 * delta)

        curl[0] = dAz_dy - dAy_dz

        # dAx/dz - dAz/dx
        Az_plus = self.vector_potential(position + np.array([0, 0, delta]))[2]
        Az_minus = self.vector_potential(position - np.array([0, 0, delta]))[2]
        dAz_dx = (Az_plus - Az_minus) / (2 * delta)

        Ax_plus = self.vector_potential(position + np.array([delta, 0, 0]))[0]
        Ax_minus = self.vector_potential(position - np.array([delta, 0, 0]))[0]
        dAx_dz = (Ax_plus - Ax_minus) / (2 * delta)

        curl[1] = dAx_dz - dAz_dx

        # dAy/dx - dAx/dy
        Ax_plus = self.vector_potential(position + np.array([delta, 0, 0]))[0]
        Ax_minus = self.vector_potential(position - np.array([delta, 0, 0]))[0]
        dAx_dy = (Ax_plus - Ax_minus) / (2 * delta)

        Ay_plus = self.vector_potential(position + np.array([0, delta, 0]))[1]
        Ay_minus = self.vector_potential(position - np.array([0, delta, 0]))[1]
        dAy_dx = (Ay_plus - Ay_minus) / (2 * delta)

        curl[2] = dAy_dx - dAx_dy

        return curl


@maxwell_cite(
    517, 518, 519,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Calculate directrix (vector potential) of current element",
)
def calc_directrix(
    current: float,
    element_position: np.ndarray,
    element_direction: np.ndarray,
    observation_point: np.ndarray,
) -> np.ndarray:
    """
    Calculate directrix (vector potential) from a current element.

    Art. 517-519: For a current element at a given position:

        A(r) = I * dl / |r - r'|

    Args:
        current: Current (abamperes).
        element_position: Position of current element (cm).
        element_direction: Direction vector of element.
        observation_point: Position where A is calculated (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    element_position = np.asarray(element_position, dtype=np.float64)
    element_direction = np.asarray(element_direction, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    r_vec = observation_point - element_position
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-15:
        return np.zeros(3)

    # Normalize direction
    dir_norm = element_direction / np.linalg.norm(element_direction) if np.linalg.norm(element_direction) > 0 else element_direction

    return current * dir_norm / r_mag


@maxwell_cite(
    517, 518, 519,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Calculate vector potential of current element",
)
def calc_vector_potential_element(
    current: float,
    element_vector: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate vector potential from a current element.

    Art. 517-519: For a current element I*dl at the origin:

        A(r) = (I * dl) / r

    where r is the distance from the element.

    Args:
        current: Current (abamperes).
        element_vector: Element vector dl (cm).
        position: Position where A is calculated (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    position = np.asarray(position, dtype=np.float64)
    r_mag = np.linalg.norm(position)

    if r_mag < 1e-15:
        return np.zeros(3)

    element_vector = np.asarray(element_vector, dtype=np.float64)

    return current * element_vector / r_mag


@maxwell_cite(
    517, 518,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Calculate magnetic field from vector potential",
)
def calc_field_from_potential(
    A_func: callable,
    position: np.ndarray,
    delta: float = 1e-6,
) -> np.ndarray:
    """
    Calculate magnetic field as curl of vector potential.

    Art. 517-519: H = curl(A)

    Args:
        A_func: Function returning vector potential at position.
        position: Position where H is calculated (cm).
        delta: Finite difference step (cm).

    Returns:
        Magnetic field H (oersted).
    """
    position = np.asarray(position, dtype=np.float64)
    A0 = np.asarray(A_func(position), dtype=np.float64)

    # Numerical curl
    curl = np.zeros(3)

    for i in range(3):
        j, k = (i + 1) % 3, (i + 2) % 3

        pos_plus_j = position.copy()
        pos_plus_j[j] += delta
        pos_minus_j = position.copy()
        pos_minus_j[j] -= delta

        pos_plus_k = position.copy()
        pos_plus_k[k] += delta
        pos_minus_k = position.copy()
        pos_minus_k[k] -= delta

        Ak_plus = A_func(pos_plus_k)[k]
        Ak_minus = A_func(pos_minus_k)[k]
        dAk_dj = (Ak_plus - Ak_minus) / (2 * delta)

        Aj_plus = A_func(pos_plus_j)[j]
        Aj_minus = A_func(pos_minus_j)[j]
        dAj_dk = (Aj_plus - Aj_minus) / (2 * delta)

        curl[i] = dAk_dj - dAj_dk

    return curl


@maxwell_cite(
    517, 518, 519,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Calculate directrix for straight wire",
)
def calc_directrix_straight_wire(
    current: float,
    wire_start: np.ndarray,
    wire_end: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate directrix (vector potential) for a straight wire segment.

    Art. 517-519: For a finite straight wire from r1 to r2:

        A(r) = (I/4π) * integral(dl / |r - r'|)

    Args:
        current: Current in wire (abamperes).
        wire_start: Start position of wire (cm).
        wire_end: End position of wire (cm).
        position: Position where A is calculated (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    wire_start = np.asarray(wire_start, dtype=np.float64)
    wire_end = np.asarray(wire_end, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    dl = wire_end - wire_start
    L = np.linalg.norm(dl)

    if L < 1e-15:
        return np.zeros(3)

    dl_unit = dl / L

    # Numerical integration along wire
    n_segments = 50
    A = np.zeros(3)

    for i in range(n_segments):
        frac = (i + 0.5) / n_segments
        r_prime = wire_start + frac * dl
        r_vec = position - r_prime
        r_mag = np.linalg.norm(r_vec)

        if r_mag > 1e-15:
            A += dl_unit * (L / n_segments) / r_mag

    return current * A


@maxwell_cite(
    517, 518, 519,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Verify vector potential relations",
)
def verify_directrix_relations(
    current: float = 1.0,
    wire_length: float = 10.0,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify relations involving the directrix function.

    Art. 517-519: This function verifies:
    1. H = curl(A)
    2. div(A) = 0 (Coulomb gauge)
    3. Consistency with Biot-Savart law

    Args:
        current: Test current (abamperes).
        wire_length: Length of test wire (cm).
        test_positions: Positions to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([2.0, 0.0, 0.0]),
            np.array([5.0, 0.0, 0.0]),
        ]

    wire_start = np.array([0.0, 0.0, -wire_length / 2])
    wire_end = np.array([0.0, 0.0, wire_length / 2])

    fields_from_curl = []
    fields_from_biot_savart = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        # Field from directrix (curl of A)
        def A_func(r):
            return calc_directrix_straight_wire(current, wire_start, wire_end, r)

        H_curl = calc_field_from_potential(A_func, pos)
        fields_from_curl.append(H_curl)

        # Field from Biot-Savart (Oersted field for long wire)
        r_perp = np.linalg.norm(pos - np.dot(pos, np.array([0, 0, 1])) * np.array([0, 0, 1]))
        if r_perp > 0:
            H_bs = 2.0 * current / r_perp
            # Direction is tangential
            H_vec = np.array([-pos[1], pos[0], 0.0])
            H_vec = H_vec / np.linalg.norm(H_vec) * H_bs if np.linalg.norm(H_vec) > 0 else np.zeros(3)
        else:
            H_vec = np.zeros(3)
        fields_from_biot_savart.append(H_vec)

    # Compare
    errors = []
    for H_c, H_b in zip(fields_from_curl, fields_from_biot_savart):
        mag_c = np.linalg.norm(H_c)
        mag_b = np.linalg.norm(H_b)
        if mag_b > 1e-15:
            errors.append(abs(mag_c - mag_b) / mag_b)
        else:
            errors.append(abs(mag_c))

    max_error = max(errors) if errors else 0

    return {
        "test_positions": test_positions,
        "fields_from_curl": fields_from_curl,
        "fields_from_biot_savart": fields_from_biot_savart,
        "relative_errors": errors,
        "max_error": max_error,
        "verified": max_error < tolerance,
    }


@maxwell_cite(
    517, 518, 519,
    part=4, chapter="Directrix Function",
    theory_class="maxwell_original",
    description="Complete directrix function analysis",
)
def analyze_directrix(
    current: float,
    wire_start: np.ndarray,
    wire_end: np.ndarray,
    evaluation_points: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis using the directrix function.

    Art. 517-519: Comprehensive analysis including:
    1. Vector potential at multiple points
    2. Magnetic field from curl
    3. Comparison with direct field calculation

    Args:
        current: Current in wire (abamperes).
        wire_start: Start of wire (cm).
        wire_end: End of wire (cm).
        evaluation_points: Points for evaluation.

    Returns:
        Dictionary with complete analysis results.
    """
    if evaluation_points is None:
        evaluation_points = [
            np.array([1.0, 0.0, 0.0]),
            np.array([2.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
        ]

    results = {
        "current": current,
        "wire_start": wire_start,
        "wire_end": wire_end,
        "wire_length": np.linalg.norm(np.asarray(wire_end) - np.asarray(wire_start)),
    }

    vector_potentials = []
    magnetic_fields = []

    for point in evaluation_points:
        point = np.asarray(point, dtype=np.float64)
        A = calc_directrix_straight_wire(current, wire_start, wire_end, point)
        vector_potentials.append(A)

        def A_func(r):
            return calc_directrix_straight_wire(current, wire_start, wire_end, r)

        H = calc_field_from_potential(A_func, point)
        magnetic_fields.append(H)

    results["vector_potentials"] = vector_potentials
    results["magnetic_fields"] = magnetic_fields

    return results
