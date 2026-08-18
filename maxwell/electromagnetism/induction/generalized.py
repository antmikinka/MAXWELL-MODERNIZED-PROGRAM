"""maxwell.electromagnetism.induction.generalized — Generalized EMF (Arts. 576-577).

Implements Maxwell's generalized formulation of electromotive force,
including both transformer and motional EMF.

Maxwell's CGS formulation (Arts. 576-577):
    Generalized EMF in a circuit:

        EMF = -d(Phi)/dt = -d/dt(integral(B·dA))

    This includes:
    - Transformer EMF: -integral(dB/dt · dA)  (changing B field)
    - Motional EMF: integral((v × B) · dl)  (moving conductor)

    In terms of vector potential:
        EMF = -d/dt(integral(A · dl))

where:
    EMF = electromotive force (abvolts)
    Phi = magnetic flux (maxwells)
    B = magnetic field (gauss)
    A = vector potential (gauss*cm)
    v = velocity (cm/s)

Category: A (maxwell_original) — Maxwell's generalized EMF theory.

References:
    Part IV, Arts. 576-577: Generalized electromotive force.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class GeneralizedEMF:
    """
    Generalized EMF calculator for arbitrary circuits.

    Art. 576-577: Maxwell's generalized formulation includes all
    sources of EMF:
    - Time-varying magnetic fields (transformer EMF)
    - Moving conductors in magnetic fields (motional EMF)
    - Both effects combined

    Attributes:
        circuit_vertices: Vertices defining the circuit (cm).
        velocity_function: Optional function v(r, t) for moving circuits.
    """

    circuit_vertices: list[np.ndarray]
    velocity_function: callable = None

    def __post_init__(self):
        """Validate vertices."""
        self.circuit_vertices = [
            np.asarray(v, dtype=np.float64) for v in self.circuit_vertices
        ]
        if len(self.circuit_vertices) < 3:
            raise ValueError("Circuit must have at least 3 vertices")

    @maxwell_cite(
        576,
        577,
        part=4,
        chapter="Generalized EMF",
        theory_class="maxwell_original",
        description="Calculate transformer EMF from changing B field",
    )
    def transformer_emf(
        self,
        dB_dt_function: callable,
        time: float = 0.0,
    ) -> float:
        """
        Calculate transformer EMF from time-varying magnetic field.

        Art. 576-577: Transformer EMF is:

            EMF = -integral(dB/dt · dA)

        Args:
            dB_dt_function: Function dB/dt(r, t) returning field rate.
            time: Time for evaluation (s).

        Returns:
            Transformer EMF (abvolts).
        """
        # Numerical integration over circuit area
        area_vector = self._calculate_area_vector()
        area_mag = np.linalg.norm(area_vector)

        if area_mag < 1e-15:
            return 0.0

        area_normal = area_vector / area_mag
        centroid = self._calculate_centroid()

        dB_dt = np.asarray(dB_dt_function(centroid, time), dtype=np.float64)

        return -np.dot(dB_dt, area_normal) * area_mag

    @maxwell_cite(
        576,
        577,
        part=4,
        chapter="Generalized EMF",
        theory_class="maxwell_original",
        description="Calculate motional EMF from moving conductor",
    )
    def motional_emf(
        self,
        B_field_function: callable,
        time: float = 0.0,
    ) -> float:
        """
        Calculate motional EMF from conductor motion.

        Art. 576-577: Motional EMF is:

            EMF = integral((v × B) · dl)

        Args:
            B_field_function: Function B(r, t) returning magnetic field.
            time: Time for evaluation (s).

        Returns:
            Motional EMF (abvolts).
        """
        if self.velocity_function is None:
            return 0.0

        emf = 0.0
        n = len(self.circuit_vertices)

        for i in range(n):
            r1 = self.circuit_vertices[i]
            r2 = self.circuit_vertices[(i + 1) % n]
            dl = r2 - r1
            mid_point = (r1 + r2) / 2

            v = np.asarray(self.velocity_function(mid_point, time), dtype=np.float64)
            B = np.asarray(B_field_function(mid_point, time), dtype=np.float64)

            # (v × B) · dl
            emf += np.dot(np.cross(v, B), dl)

        return emf

    @maxwell_cite(
        576,
        577,
        part=4,
        chapter="Generalized EMF",
        theory_class="maxwell_original",
        description="Calculate total generalized EMF",
    )
    def total_emf(
        self,
        B_field_function: callable,
        dB_dt_function: callable = None,
        time: float = 0.0,
    ) -> float:
        """
        Calculate total EMF (transformer + motional).

        Art. 576-577: The total EMF is:

            EMF_total = EMF_transformer + EMF_motional

        Args:
            B_field_function: Function B(r, t) returning magnetic field.
            dB_dt_function: Function dB/dt(r, t) (optional, uses numerical derivative).
            time: Time for evaluation (s).

        Returns:
            Total EMF (abvolts).
        """
        # Transformer EMF
        if dB_dt_function is not None:
            emf_transformer = self.transformer_emf(dB_dt_function, time)
        else:
            # Numerical derivative
            dt = 1e-9

            def numerical_dB_dt(r, t):
                B_plus = np.asarray(B_field_function(r, t + dt), dtype=np.float64)
                B_minus = np.asarray(B_field_function(r, t - dt), dtype=np.float64)
                return (B_plus - B_minus) / (2 * dt)

            emf_transformer = self.transformer_emf(numerical_dB_dt, time)

        # Motional EMF
        emf_motional = self.motional_emf(B_field_function, time)

        return emf_transformer + emf_motional

    def _calculate_area_vector(self) -> np.ndarray:
        """Calculate area vector of planar circuit."""
        n = len(self.circuit_vertices)
        if n < 3:
            return np.zeros(3)

        # Centroid
        centroid = sum(self.circuit_vertices) / n

        area_vector = np.zeros(3)
        for i in range(n):
            r1 = self.circuit_vertices[i] - centroid
            r2 = self.circuit_vertices[(i + 1) % n] - centroid
            area_vector += np.cross(r1, r2)

        return area_vector / 2.0

    def _calculate_centroid(self) -> np.ndarray:
        """Calculate centroid of circuit."""
        return sum(self.circuit_vertices) / len(self.circuit_vertices)


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Calculate EMF from changing flux: EMF = -d(Phi)/dt",
)
def calc_generalized_emf(
    dPhi_dt: float,
) -> float:
    """
    Calculate generalized EMF from rate of change of flux.

    Art. 576-577: Faraday's law in its general form:

        EMF = -d(Phi)/dt

    This includes both transformer and motional contributions.

    Args:
        dPhi_dt: Rate of change of flux (maxwells/s).

    Returns:
        EMF (abvolts).

    Reference:
        Part IV, Arts. 576-577: Generalized EMF.
    """
    return -dPhi_dt


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Calculate motional EMF: EMF = integral((v × B) · dl)",
)
def calc_motional_emf_general(
    velocity: np.ndarray,
    B_field: np.ndarray,
    conductor_length: np.ndarray,
) -> float:
    """
    Calculate motional EMF for a straight conductor.

    Art. 576-577: For a straight conductor moving in a magnetic field:

        EMF = (v × B) · L

    Args:
        velocity: Velocity of conductor (cm/s).
        B_field: Magnetic field (gauss).
        conductor_length: Length vector of conductor (cm).

    Returns:
        Motional EMF (abvolts).

    Reference:
        Part IV, Arts. 576-577: Motional EMF.
    """
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    conductor_length = np.asarray(conductor_length, dtype=np.float64)

    return np.dot(np.cross(velocity, B_field), conductor_length)


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Calculate EMF from rotating loop",
)
def calc_rotating_loop_emf(
    B_field: float,
    loop_area: float,
    n_turns: int,
    angular_velocity: float,
    time: float,
    initial_angle: float = 0.0,
) -> float:
    """
    Calculate EMF from a loop rotating in a magnetic field.

    Art. 576-577: For a loop rotating with angular velocity omega:

        Phi(t) = N * B * A * cos(omega*t + phi_0)
        EMF = N * B * A * omega * sin(omega*t + phi_0)

    Args:
        B_field: Magnetic field strength (gauss).
        loop_area: Area of loop (cm²).
        n_turns: Number of turns.
        angular_velocity: Angular velocity (rad/s).
        time: Time (s).
        initial_angle: Initial angle (radians).

    Returns:
        Induced EMF (abvolts).

    Reference:
        Part IV, Arts. 576-577: Rotating loop EMF.
    """
    phase = angular_velocity * time + initial_angle

    return n_turns * B_field * loop_area * angular_velocity * np.sin(phase)


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Calculate EMF from sliding conductor",
)
def calc_sliding_conductor_emf(
    B_field: float,
    velocity: float,
    conductor_length: float,
) -> float:
    """
    Calculate EMF from a conductor sliding on rails.

    Art. 576-577: For a conductor of length L sliding with velocity v
    perpendicular to magnetic field B:

        EMF = B * v * L

    Args:
        B_field: Magnetic field (gauss).
        velocity: Velocity of conductor (cm/s).
        conductor_length: Length of conductor (cm).

    Returns:
        Induced EMF (abvolts).

    Reference:
        Part IV, Arts. 576-577: Sliding conductor EMF.
    """
    return B_field * velocity * conductor_length


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Verify generalized EMF relations",
)
def verify_generalized_emf(
    B_field: float = 1000.0,
    loop_area: float = 100.0,
    n_turns: int = 1,
    angular_velocity: float = 10.0,
    test_times: list[float] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify generalized EMF relations.

    Art. 576-577: This function verifies:
    1. EMF = -d(Phi)/dt for rotating loop
    2. Maximum EMF = N*B*A*omega
    3. EMF is sinusoidal

    Args:
        B_field: Magnetic field (gauss).
        loop_area: Loop area (cm²).
        n_turns: Number of turns.
        angular_velocity: Angular velocity (rad/s).
        test_times: Times to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_times is None:
        period = 2 * np.pi / angular_velocity
        test_times = np.linspace(0, period, 10)

    emf_values = []
    for t in test_times:
        emf = calc_rotating_loop_emf(B_field, loop_area, n_turns, angular_velocity, t)
        emf_values.append(emf)

    # Expected maximum
    emf_max_expected = n_turns * B_field * loop_area * angular_velocity
    emf_max_actual = max(abs(e) for e in emf_values)

    max_error = (
        abs(emf_max_actual - emf_max_expected) / emf_max_expected
        if emf_max_expected > 0
        else 0
    )

    # Verify sinusoidal (zero crossings at expected times)
    period = 2 * np.pi / angular_velocity
    emf_at_zero = calc_rotating_loop_emf(
        B_field, loop_area, n_turns, angular_velocity, 0
    )
    emf_at_half_period = calc_rotating_loop_emf(
        B_field, loop_area, n_turns, angular_velocity, period / 2
    )

    zero_crossing_verified = abs(emf_at_zero) < tolerance * emf_max_expected
    half_period_verified = abs(emf_at_half_period) < tolerance * emf_max_expected

    max_verified = max_error < tolerance

    return {
        "B_field": B_field,
        "loop_area": loop_area,
        "n_turns": n_turns,
        "angular_velocity": angular_velocity,
        "test_times": test_times,
        "emf_values": emf_values,
        "emf_max_expected": emf_max_expected,
        "emf_max_actual": emf_max_actual,
        "max_error": max_error,
        "zero_crossing_verified": zero_crossing_verified,
        "half_period_verified": half_period_verified,
        "max_verified": max_verified,
        "verified": max_verified and zero_crossing_verified and half_period_verified,
    }


@maxwell_cite(
    576,
    577,
    part=4,
    chapter="Generalized EMF",
    theory_class="maxwell_original",
    description="Complete generalized EMF analysis",
)
def analyze_generalized_emf(
    circuit_vertices: list[np.ndarray],
    B_field_function: callable,
    velocity_function: callable = None,
    time_range: tuple[float, float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of generalized EMF.

    Art. 576-577: Comprehensive analysis including:
    1. Transformer EMF
    2. Motional EMF
    3. Total EMF
    4. Time dependence

    Args:
        circuit_vertices: Vertices of circuit (cm).
        B_field_function: Function B(r, t) returning magnetic field.
        velocity_function: Optional function v(r, t) for motion.
        time_range: (t_min, t_max) in seconds.

    Returns:
        Dictionary with complete analysis results.
    """
    if time_range is None:
        time_range = (0.0, 1.0)

    n_points = 50
    times = np.linspace(time_range[0], time_range[1], n_points)

    emf_calculator = GeneralizedEMF(
        circuit_vertices=circuit_vertices, velocity_function=velocity_function
    )

    emf_transformer = []
    emf_motional = []
    emf_total = []

    for t in times:
        # Numerical dB/dt
        dt = 1e-9

        def numerical_dB_dt(r, time):
            B_plus = np.asarray(B_field_function(r, time + dt), dtype=np.float64)
            B_minus = np.asarray(B_field_function(r, time - dt), dtype=np.float64)
            return (B_plus - B_minus) / (2 * dt)

        emf_t = emf_calculator.transformer_emf(numerical_dB_dt, t)
        emf_m = (
            emf_calculator.motional_emf(B_field_function, t)
            if velocity_function
            else 0.0
        )

        emf_transformer.append(emf_t)
        emf_motional.append(emf_m)
        emf_total.append(emf_t + emf_m)

    return {
        "circuit_vertices": circuit_vertices,
        "time_range": time_range,
        "times": times,
        "emf_transformer": emf_transformer,
        "emf_motional": emf_motional,
        "emf_total": emf_total,
        "max_emf": max(abs(e) for e in emf_total),
        "has_motion": velocity_function is not None,
    }
