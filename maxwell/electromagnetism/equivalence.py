"""maxwell.electromagnetism.equivalence — Circuit-to-shell equivalence (Arts. 482-485).

Implements Maxwell's equivalence theorem between a current-carrying circuit
and a magnetic shell, which was crucial for his unified theory of electromagnetism.

Maxwell's CGS formulation (Arts. 482-485):
    A closed current circuit is magnetically equivalent to a magnetic shell
    (double layer of magnetic poles) bounded by the circuit, where:

    Shell strength = current (in appropriate units)

    The potential at any point is:
        Omega = I * omega  (where omega is solid angle subtended by circuit)

    This equivalence allows treating current circuits using magnetic shell theory.

where:
    I = current in abamperes (EMU)
    omega = solid angle (steradians)
    Omega = magnetic scalar potential (oersted*cm)

Category: A (maxwell_original) — Maxwell's equivalence theorem.

References:
    Part IV, Arts. 482-485: Circuit-shell equivalence theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticShell:
    """
    Magnetic shell equivalent to a current-carrying circuit.

    Art. 482-485: Maxwell's equivalence theorem states that any closed
    current circuit can be replaced (for magnetic field calculations) by
    a magnetic shell bounded by the circuit. The shell has:

    - Strength sigma = I (current per unit length along edge)
    - Magnetic moment per unit area = I (in CGS-EMU)
    - Same external field as the original circuit

    The shell is a "double layer" of magnetic poles: positive on one face,
    negative on the other, with surface density proportional to current.

    Attributes:
        current: Equivalent current (abamperes).
        boundary_curve: Points defining the circuit boundary (cm).
        shell_normal: Unit vector normal to shell (direction of + face).
    """

    current: float
    boundary_curve: list[np.ndarray] = None
    shell_normal: np.ndarray = None

    def __post_init__(self):
        """Validate and set defaults."""
        if self.boundary_curve is None:
            self.boundary_curve = [
                np.array([1.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([-1.0, 0.0, 0.0]),
                np.array([0.0, -1.0, 0.0]),
            ]
        else:
            self.boundary_curve = [
                np.asarray(p, dtype=np.float64) for p in self.boundary_curve
            ]

        self.shell_normal = (
            np.asarray(self.shell_normal, dtype=np.float64)
            if self.shell_normal is not None
            else np.array([0.0, 0.0, 1.0])
        )
        norm = np.linalg.norm(self.shell_normal)
        if norm > 0:
            self.shell_normal = self.shell_normal / norm

    @property
    def shell_strength(self) -> float:
        """
        Strength of the magnetic shell.

        Returns:
            sigma = I (abamperes, equivalent current).
        """
        return self.current

    @maxwell_cite(
        482,
        483,
        part=4,
        chapter="Circuit-Shell Equivalence",
        theory_class="maxwell_original",
        description="Calculate potential from magnetic shell",
    )
    def potential_at(self, position: np.ndarray) -> float:
        """
        Calculate magnetic potential from the equivalent shell.

        Art. 482-485: The potential at point P is:

            Omega = I * omega

        where omega is the solid angle subtended by the shell (circuit)
        at point P. The sign depends on which face of the shell faces P.

        Args:
            position: Position vector (cm).

        Returns:
            Magnetic potential (oersted*cm).

        Reference:
            Part IV, Arts. 482-485: Shell potential.
        """
        position = np.asarray(position, dtype=np.float64)

        # Calculate solid angle using boundary curve
        omega = self._calculate_solid_angle(position)

        return self.current * omega

    def _calculate_solid_angle(self, position: np.ndarray) -> float:
        """
        Calculate solid angle subtended by boundary curve at position.

        Uses the formula: omega = sum of spherical excess angles for
        triangles formed by position and each edge segment.

        Args:
            position: Observation point (cm).

        Returns:
            Solid angle (steradians).
        """
        n = len(self.boundary_curve)
        if n < 3:
            return 0.0

        total_omega = 0.0

        for i in range(n):
            p1 = self.boundary_curve[i] - position
            p2 = self.boundary_curve[(i + 1) % n] - position

            r1 = np.linalg.norm(p1)
            r2 = np.linalg.norm(p2)

            if r1 < 1e-15 or r2 < 1e-15:
                continue  # At boundary (singularity)

            # Normalize
            u1 = p1 / r1
            u2 = p2 / r2

            # Angle between edges as seen from position
            cos_theta = np.clip(np.dot(u1, u2), -1.0, 1.0)
            theta = np.arccos(cos_theta)

            # Area contribution (simplified - exact requires more complex formula)
            # This is an approximation; exact calculation requires spherical trigonometry
            cross = np.cross(u1, u2)
            sign = np.sign(np.dot(cross, self.shell_normal))

            total_omega += sign * theta

        return total_omega

    @maxwell_cite(
        484,
        485,
        part=4,
        chapter="Circuit-Shell Equivalence",
        theory_class="maxwell_original",
        description="Calculate field from shell (equivalent to circuit field)",
    )
    def field_at(self, position: np.ndarray, delta: float = 1e-6) -> np.ndarray:
        """
        Calculate magnetic field from shell (equivalent to circuit field).

        Art. 484-485: H = -grad(Omega), computed numerically.

        Args:
            position: Position vector (cm).
            delta: Finite difference step (cm).

        Returns:
            Magnetic field vector (oersted).

        Reference:
            Part IV, Arts. 484-485: Field from shell.
        """
        position = np.asarray(position, dtype=np.float64)
        omega_0 = self.potential_at(position)

        grad = np.zeros(3)
        for i in range(3):
            pos_plus = position.copy()
            pos_plus[i] += delta
            grad[i] = (self.potential_at(pos_plus) - omega_0) / delta

        return -grad


@dataclass
class CurrentCircuit:
    """
    Current-carrying circuit with magnetic field calculation.

    Art. 482-485: A closed current circuit can be analyzed either directly
    (using Biot-Savart) or via the equivalent magnetic shell. Both methods
    must give identical results (the equivalence theorem).

    Attributes:
        current: Current in circuit (abamperes).
        vertices: Vertices of the circuit path (cm).
    """

    current: float
    vertices: list[np.ndarray] = None

    def __post_init__(self):
        """Validate and set defaults."""
        if self.vertices is None:
            self.vertices = [
                np.array([1.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([-1.0, 0.0, 0.0]),
                np.array([0.0, -1.0, 0.0]),
            ]
        else:
            self.vertices = [np.asarray(v, dtype=np.float64) for v in self.vertices]

    @maxwell_cite(
        482,
        part=4,
        chapter="Circuit-Shell Equivalence",
        theory_class="maxwell_original",
        description="Calculate field from circuit using Biot-Savart",
    )
    def field_at_biot_savart(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field using Biot-Savart law.

        Art. 482: Direct calculation from current elements:

            H = I * integral(dl × r) / r³

        For a polygonal circuit, this is summed over each segment.

        Args:
            position: Position vector (cm).

        Returns:
            Magnetic field vector (oersted).

        Reference:
            Part IV, Art. 482: Biot-Savart for circuits.
        """
        position = np.asarray(position, dtype=np.float64)
        total_field = np.zeros(3)

        n = len(self.vertices)
        for i in range(n):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % n]

            # Segment vector
            dl = p2 - p1
            segment_mid = (p1 + p2) / 2

            # Vector from segment to observation point
            r_vec = position - segment_mid
            r_mag = np.linalg.norm(r_vec)

            if r_mag < 1e-15:
                continue  # Too close to wire

            # Biot-Savart: dH = I * (dl × r) / (4*pi*r³)
            # In CGS-EMU with our conventions: dH = I * (dl × r_hat) / r²
            r_hat = r_vec / r_mag
            dH = self.current * np.cross(dl, r_hat) / (r_mag**2)

            # Factor for finite segment (approximate)
            segment_factor = np.linalg.norm(dl) / (4.0 * np.pi * r_mag)
            total_field += dH * segment_factor

        return total_field

    def get_equivalent_shell(self, normal: np.ndarray = None) -> MagneticShell:
        """
        Get the equivalent magnetic shell for this circuit.

        Art. 482-485: The circuit is equivalent to a magnetic shell bounded
        by the circuit, with strength equal to the current.

        Args:
            normal: Optional shell normal direction.

        Returns:
            MagneticShell equivalent to this circuit.

        Reference:
            Part IV, Arts. 482-485: Circuit-shell equivalence.
        """
        return MagneticShell(
            current=self.current, boundary_curve=self.vertices, shell_normal=normal
        )


@dataclass
class CircuitEquivalence:
    """
    Circuit-shell equivalence calculator.

    Art. 482-485: Maxwell's equivalence theorem between a current-carrying
    circuit and a magnetic shell.

    Attributes:
        current: Current in circuit (abamperes).
        area: Area of circuit (cm²).
    """

    current: float = 0.0
    area: float = 1.0

    @maxwell_cite(
        482,
        483,
        part=4,
        chapter="Circuit-Shell Equivalence",
        theory_class="maxwell_original",
        description="Calculate magnetic moment from circuit area and current",
    )
    def magnetic_moment(self, current: float = None, area: float = None) -> float:
        """
        Calculate magnetic moment: m = I * A / c.

        Art. 482-483: For a current loop:

            m = I * A / c

        Args:
            current: Current (abamperes, uses self.current if None).
            area: Area (cm², uses self.area if None).

        Returns:
            Magnetic moment (EMU).
        """
        I = current if current is not None else self.current
        A = area if area is not None else self.area
        return I * A / CONST.C


@maxwell_cite(
    482,
    483,
    part=4,
    chapter="Circuit-Shell Equivalence",
    theory_class="maxwell_original",
    description="Calculate solid angle of circular loop on axis",
)
def calc_solid_angle(
    radius: float,
    distance: float,
) -> float:
    """
    Calculate solid angle subtended by a circular loop on its axis.

    Art. 482-485: For a circular loop of radius R at distance z:

        Omega = 2*pi * (1 - z / sqrt(R² + z²))

    Args:
        radius: Loop radius (cm).
        distance: Axial distance from loop (cm).

    Returns:
        Solid angle (steradians).

    Reference:
        Part IV, Arts. 482-485: Solid angle of circular loop.
    """
    R = radius
    z = abs(distance)
    r = np.sqrt(R**2 + z**2)
    if r < 1e-15:
        return 2.0 * np.pi
    return 2.0 * np.pi * (1.0 - z / r)


@maxwell_cite(
    482,
    483,
    484,
    485,
    part=4,
    chapter="Circuit-Shell Equivalence",
    theory_class="maxwell_original",
    description="Verify circuit-shell equivalence theorem",
)
def verify_circuit_shell_equivalence(
    current: float = 1.0,
    circuit_radius: float = 1.0,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-5,
) -> dict[str, float | bool | list]:
    """
    Verify Maxwell's circuit-shell equivalence theorem.

    Art. 482-485: This function verifies that a current circuit and its
    equivalent magnetic shell produce the same magnetic field at all points.

    Args:
        current: Test current (abamperes).
        circuit_radius: Radius of circular test circuit (cm).
        test_positions: Positions to test (default: various points on axis).
        tolerance: Numerical tolerance for equivalence.

    Returns:
        Dictionary with verification results:
        - circuit_fields: Field from circuit at each position
        - shell_fields: Field from shell at each position
        - max_relative_error: Maximum relative difference
        - equivalence_verified: True if fields match within tolerance

    Reference:
        Part IV, Arts. 482-485: Equivalence theorem verification.
    """
    # Create circular circuit approximation
    n_segments = 16
    angles = np.linspace(0, 2 * np.pi, n_segments, endpoint=False)
    vertices = [
        np.array([circuit_radius * np.cos(a), circuit_radius * np.sin(a), 0])
        for a in angles
    ]

    circuit = CurrentCircuit(current=current, vertices=vertices)
    shell = circuit.get_equivalent_shell(normal=np.array([0.0, 0.0, 1.0]))

    if test_positions is None:
        test_positions = [
            np.array([0, 0, 0.5]),
            np.array([0, 0, 1.0]),
            np.array([0, 0, 2.0]),
            np.array([0, 0, 5.0]),
        ]

    circuit_fields = []
    shell_fields = []
    relative_errors = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)
        H_circuit = circuit.field_at_biot_savart(pos)
        H_shell = shell.field_at(pos)

        circuit_fields.append(H_circuit)
        shell_fields.append(H_shell)

        # Relative error
        H_c_mag = np.linalg.norm(H_circuit)
        H_s_mag = np.linalg.norm(H_shell)

        if H_c_mag > 1e-15:
            rel_error = np.linalg.norm(H_circuit - H_shell) / H_c_mag
        else:
            rel_error = np.linalg.norm(H_circuit - H_shell)

        relative_errors.append(rel_error)

    max_error = max(relative_errors)
    equivalence_verified = max_error < tolerance

    return {
        "current": current,
        "circuit_radius": circuit_radius,
        "test_positions": [p.tolist() for p in test_positions],
        "circuit_fields": [f.tolist() for f in circuit_fields],
        "shell_fields": [f.tolist() for f in shell_fields],
        "relative_errors": relative_errors,
        "max_relative_error": max_error,
        "equivalence_verified": equivalence_verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    482,
    483,
    part=4,
    chapter="Circuit-Shell Equivalence",
    theory_class="maxwell_original",
    description="Calculate solid angle of arbitrary planar loop",
)
def calc_solid_angle_loop(
    vertices: list[np.ndarray],
    position: np.ndarray,
) -> float:
    """
    Calculate solid angle subtended by a planar current loop.

    Art. 482-485: For an arbitrary planar loop defined by vertices,
    the solid angle at point P can be calculated by summing the
    contributions from each edge.

    Args:
        vertices: List of vertices defining the loop (cm).
        position: Position where solid angle is calculated (cm).

    Returns:
        Solid angle (steradians).

    Reference:
        Part IV, Arts. 482-485: Solid angle calculation.
    """
    vertices = [np.asarray(v, dtype=np.float64) for v in vertices]
    position = np.asarray(position, dtype=np.float64)

    n = len(vertices)
    if n < 3:
        return 0.0

    # Calculate normal to loop plane
    v0 = vertices[1] - vertices[0]
    v1 = vertices[2] - vertices[0]
    normal = np.cross(v0, v1)
    normal = (
        normal / np.linalg.norm(normal)
        if np.linalg.norm(normal) > 0
        else np.array([0, 0, 1])
    )

    total_omega = 0.0

    for i in range(n):
        r1 = vertices[i] - position
        r2 = vertices[(i + 1) % n] - position

        r1_mag = np.linalg.norm(r1)
        r2_mag = np.linalg.norm(r2)

        if r1_mag < 1e-15 or r2_mag < 1e-15:
            continue

        u1 = r1 / r1_mag
        u2 = r2 / r2_mag

        # Spherical angle
        cos_theta = np.clip(np.dot(u1, u2), -1.0, 1.0)
        theta = np.arccos(cos_theta)

        # Sign from cross product
        cross = np.cross(u1, u2)
        sign = np.sign(np.dot(cross, normal))

        total_omega += sign * theta

    return total_omega


@maxwell_cite(
    484,
    485,
    part=4,
    chapter="Circuit-Shell Equivalence",
    theory_class="maxwell_original",
    description="Calculate magnetic moment of current loop",
)
def calc_magnetic_moment(
    current: float,
    vertices: list[np.ndarray],
) -> np.ndarray:
    """
    Calculate magnetic moment of a planar current loop.

    Art. 484-485: The magnetic moment of a current loop is:

        m = I * A * n

    where A is the area and n is the unit normal (right-hand rule).

    For a polygon, area can be calculated from vertices.

    In CGS-EMU:
        I = current (abamperes)
        A = area (cm²)
        m = magnetic moment (EMU, erg/gauss)

    Args:
        current: Current in loop (abamperes).
        vertices: Vertices of the loop (cm).

    Returns:
        Magnetic moment vector (EMU).

    Reference:
        Part IV, Arts. 484-485: Magnetic moment of circuits.
    """
    vertices = [np.asarray(v, dtype=np.float64) for v in vertices]
    n = len(vertices)

    if n < 3:
        return np.zeros(3)

    # Calculate area vector using shoelace formula in 3D
    area_vector = np.zeros(3)
    centroid = sum(vertices) / n

    for i in range(n):
        v1 = vertices[i] - centroid
        v2 = vertices[(i + 1) % n] - centroid
        area_vector += np.cross(v1, v2)

    area_vector = area_vector / 2.0

    # m = I * A (area vector already includes direction)
    return current * area_vector


@maxwell_cite(
    482,
    483,
    484,
    485,
    part=4,
    chapter="Circuit-Shell Equivalence",
    theory_class="maxwell_original",
    description="Complete circuit-shell equivalence analysis",
)
def analyze_circuit_shell_equivalence(
    current: float,
    vertices: list[np.ndarray],
    evaluation_points: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of circuit-shell equivalence.

    Art. 482-485: Comprehensive analysis including:
    1. Circuit magnetic moment
    2. Equivalent shell parameters
    3. Field comparison at multiple points
    4. Solid angle calculations

    Args:
        current: Current in circuit (abamperes).
        vertices: Circuit vertices (cm).
        evaluation_points: Points for field evaluation.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 482-485: Complete equivalence analysis.
    """
    circuit = CurrentCircuit(current=current, vertices=vertices)
    shell = circuit.get_equivalent_shell()

    # Magnetic moment
    m = calc_magnetic_moment(current, vertices)

    result = {
        "current": current,
        "num_vertices": len(vertices),
        "magnetic_moment": m,
        "shell_strength": shell.shell_strength,
    }

    if evaluation_points is not None:
        circuit_fields = []
        shell_fields = []
        potentials = []

        for point in evaluation_points:
            point = np.asarray(point, dtype=np.float64)
            circuit_fields.append(circuit.field_at_biot_savart(point))
            shell_fields.append(shell.field_at(point))
            potentials.append(shell.potential_at(point))

        result["evaluation_points"] = evaluation_points
        result["circuit_fields"] = circuit_fields
        result["shell_fields"] = shell_fields
        result["potentials"] = potentials

    return result
