"""maxwell.electromagnetism.forces.sliding — Motional EMF and sliding conductors (Arts. 594-597).

Implements Maxwell's treatment of motional electromotive force, including
the classic sliding conductor problem.

Maxwell's CGS formulation (Arts. 594-597):
    Motional EMF for conductor moving in magnetic field:

        EMF = integral((v × B) · dl)

    For a straight conductor of length L moving perpendicular to B:
        EMF = B * v * L

    The induced current creates a magnetic force opposing the motion
    (Lenz's law).

where:
    EMF = electromotive force (abvolts)
    v = velocity (cm/s)
    B = magnetic field (gauss)
    L = conductor length (cm)

Category: A (maxwell_original) — Maxwell's motional EMF theory.

References:
    Part IV, Arts. 594-597: Motional electromotive force.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class SlidingConductor:
    """
    Sliding conductor motional EMF calculator.

    Art. 594-597: The classic problem of a conductor sliding on
    conducting rails in a magnetic field, which demonstrates
    motional EMF and electromagnetic braking.

    Attributes:
        conductor_length: Length of sliding conductor (cm).
        magnetic_field: Magnetic field strength (gauss).
        circuit_resistance: Total circuit resistance (abohms).
    """

    conductor_length: float
    magnetic_field: float
    circuit_resistance: float = 1.0

    def __post_init__(self):
        """Validate parameters."""
        if self.conductor_length <= 0:
            raise ValueError(f"Length must be positive")
        if self.magnetic_field < 0:
            raise ValueError(f"B field must be non-negative")
        if self.circuit_resistance <= 0:
            raise ValueError(f"Resistance must be positive")

    @maxwell_cite(
        594, 595,
        part=4, chapter="Motional EMF",
        theory_class="maxwell_original",
        description="Calculate motional EMF",
    )
    def motional_emf(self, velocity: float) -> float:
        """
        Calculate motional EMF for sliding conductor.

        Art. 594-595: For a conductor moving perpendicular to B:

            EMF = B * v * L

        Args:
            velocity: Velocity of conductor (cm/s).

        Returns:
            Motional EMF (abvolts).
        """
        return self.magnetic_field * velocity * self.conductor_length

    @maxwell_cite(
        594, 596,
        part=4, chapter="Motional EMF",
        theory_class="maxwell_original",
        description="Calculate induced current",
    )
    def induced_current(self, velocity: float) -> float:
        """
        Calculate induced current in sliding conductor circuit.

        Art. 594-596: From Ohm's law:

            I = EMF / R = B * v * L / R

        Args:
            velocity: Velocity of conductor (cm/s).

        Returns:
            Induced current (abamperes).
        """
        emf = self.motional_emf(velocity)
        return emf / self.circuit_resistance

    @maxwell_cite(
        596, 597,
        part=4, chapter="Motional EMF",
        theory_class="maxwell_original",
        description="Calculate magnetic braking force",
    )
    def braking_force(self, velocity: float) -> float:
        """
        Calculate magnetic braking force opposing motion.

        Art. 596-597: The induced current creates a magnetic force:

            F_brake = I * L * B = (B² * L² / R) * v

        This force opposes the motion (Lenz's law).

        Args:
            velocity: Velocity of conductor (cm/s).

        Returns:
            Braking force (dynes). Negative = opposing motion.
        """
        I = self.induced_current(velocity)
        return -I * self.conductor_length * self.magnetic_field

    @maxwell_cite(
        594, 597,
        part=4, chapter="Motional EMF",
        theory_class="maxwell_original",
        description="Calculate terminal velocity",
    )
    def terminal_velocity(self, applied_force: float) -> float:
        """
        Calculate terminal velocity under constant applied force.

        Art. 594-597: At terminal velocity, applied force equals
        braking force:

            F_applied = B² * L² * v_terminal / R

            v_terminal = F_applied * R / (B² * L²)

        Args:
            applied_force: Constant applied force (dynes).

        Returns:
            Terminal velocity (cm/s).
        """
        B = self.magnetic_field
        L = self.conductor_length
        R = self.circuit_resistance

        denominator = B ** 2 * L ** 2
        if denominator < 1e-15:
            return float('inf')

        return applied_force * R / denominator

    @maxwell_cite(
        594, 597,
        part=4, chapter="Motional EMF",
        theory_class="maxwell_original",
        description="Calculate velocity vs time under constant force",
    )
    def velocity_vs_time(self, applied_force: float, mass: float, time: float) -> float:
        """
        Calculate velocity as function of time under constant force.

        Art. 594-597: The equation of motion is:

            m * dv/dt = F_applied - (B²L²/R) * v

        Solution:
            v(t) = v_terminal * (1 - exp(-t/tau))

        where tau = m * R / (B² * L²)

        Args:
            applied_force: Applied force (dynes).
            mass: Mass of conductor (g).
            time: Time (s).

        Returns:
            Velocity at time t (cm/s).
        """
        v_terminal = self.terminal_velocity(applied_force)

        B = self.magnetic_field
        L = self.conductor_length
        R = self.circuit_resistance

        tau = mass * R / (B ** 2 * L ** 2) if B > 0 else float('inf')

        if tau == float('inf') or tau < 1e-15:
            return v_terminal

        return v_terminal * (1.0 - np.exp(-time / tau))


@maxwell_cite(
    594, 595,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Calculate motional EMF: EMF = |v×B|*L",
)
def calc_motional_emf(
    velocity: np.ndarray,
    B_field: np.ndarray,
    conductor_length: float,
) -> float:
    """
    Calculate motional EMF for conductor moving in magnetic field.

    Art. 594-595: For a conductor moving in a magnetic field:

        EMF = |v × B| * L

    Args:
        velocity: Velocity vector (cm/s).
        B_field: Magnetic field vector (gauss).
        conductor_length: Conductor length (cm).

    Returns:
        Motional EMF (abvolts).

    Reference:
        Part IV, Arts. 594-595: Motional EMF.
    """
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return np.linalg.norm(np.cross(velocity, B_field)) * conductor_length


@maxwell_cite(
    594, 595,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Calculate motional EMF: EMF = B*v*L",
)
def calc_motional_emf_sliding(
    B_field: float,
    velocity: float,
    conductor_length: float,
) -> float:
    """
    Calculate motional EMF for sliding conductor.

    Art. 594-595: For a conductor moving perpendicular to magnetic field:

        EMF = B * v * L

    Args:
        B_field: Magnetic field (gauss).
        velocity: Velocity (cm/s).
        conductor_length: Conductor length (cm).

    Returns:
        Motional EMF (abvolts).

    Reference:
        Part IV, Arts. 594-595: Sliding conductor EMF.
    """
    return B_field * velocity * conductor_length


@maxwell_cite(
    596, 597,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Calculate magnetic braking force",
)
def calc_magnetic_braking_force(
    B_field: float,
    velocity: float,
    conductor_length: float,
    resistance: float,
) -> float:
    """
    Calculate magnetic braking force on sliding conductor.

    Art. 596-597: The braking force is:

        F_brake = -B² * L² * v / R

    The negative sign indicates opposition to motion.

    Args:
        B_field: Magnetic field (gauss).
        velocity: Velocity (cm/s).
        conductor_length: Conductor length (cm).
        resistance: Circuit resistance (abohms).

    Returns:
        Braking force (dynes). Negative = opposing motion.

    Reference:
        Part IV, Arts. 596-597: Magnetic braking.
    """
    if resistance <= 0:
        return 0.0

    return -(B_field ** 2) * (conductor_length ** 2) * velocity / resistance


@maxwell_cite(
    594, 595, 596, 597,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Calculate power dissipation in sliding conductor",
)
def calc_power_dissipation(
    B_field: float,
    velocity: float,
    conductor_length: float,
    resistance: float,
) -> float:
    """
    Calculate power dissipated as heat in sliding conductor.

    Art. 594-597: The power dissipated is:

        P = I² * R = (B * v * L)² / R

    This equals the mechanical power removed by braking:
        P = |F_brake * v|

    Args:
        B_field: Magnetic field (gauss).
        velocity: Velocity (cm/s).
        conductor_length: Conductor length (cm).
        resistance: Circuit resistance (abohms).

    Returns:
        Power dissipated (ergs/s).

    Reference:
        Part IV, Arts. 594-597: Power dissipation.
    """
    if resistance <= 0:
        return 0.0

    emf = B_field * velocity * conductor_length
    return emf ** 2 / resistance


@maxwell_cite(
    594, 597,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Calculate motional EMF for arbitrary motion",
)
def calc_motional_emf_arbitrary(
    velocity: np.ndarray,
    B_field: np.ndarray,
    conductor_vector: np.ndarray,
) -> float:
    """
    Calculate motional EMF for arbitrary conductor motion.

    Art. 594-597: For arbitrary orientation:

        EMF = (v × B) · L

    Args:
        velocity: Velocity vector (cm/s).
        B_field: Magnetic field vector (gauss).
        conductor_vector: Conductor length vector (cm).

    Returns:
        Motional EMF (abvolts).

    Reference:
        Part IV, Arts. 594-597: Arbitrary motion EMF.
    """
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    conductor_vector = np.asarray(conductor_vector, dtype=np.float64)

    return np.dot(np.cross(velocity, B_field), conductor_vector)


@maxwell_cite(
    594, 595, 596, 597,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Verify motional EMF and braking relations",
)
def verify_motional_emf(
    B_field: float = 1000.0,
    velocity: float = 100.0,
    conductor_length: float = 10.0,
    resistance: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify motional EMF and magnetic braking relations.

    Art. 594-597: This function verifies:
    1. EMF = B*v*L
    2. I = EMF/R
    3. F_brake = I*L*B
    4. Power balance: mechanical power = electrical power

    Args:
        B_field: Magnetic field (gauss).
        velocity: Velocity (cm/s).
        conductor_length: Conductor length (cm).
        resistance: Circuit resistance (abohms).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Calculate quantities
    emf = calc_motional_emf_sliding(B_field, velocity, conductor_length)
    current = emf / resistance
    braking_force = calc_magnetic_braking_force(B_field, velocity, conductor_length, resistance)
    power_electrical = calc_power_dissipation(B_field, velocity, conductor_length, resistance)

    # Mechanical power (force * velocity)
    power_mechanical = abs(braking_force * velocity)

    # Verify power balance
    power_error = abs(power_electrical - power_mechanical) / max(power_electrical, 1e-15)

    # Verify force relation
    expected_force = -current * conductor_length * B_field
    force_error = abs(braking_force - expected_force) / max(abs(expected_force), 1e-15)

    # Verify EMF relation
    expected_emf = B_field * velocity * conductor_length
    emf_error = abs(emf - expected_emf) / max(abs(expected_emf), 1e-15)

    return {
        "B_field": B_field,
        "velocity": velocity,
        "conductor_length": conductor_length,
        "resistance": resistance,
        "emf": emf,
        "expected_emf": expected_emf,
        "current": current,
        "braking_force": braking_force,
        "power_electrical": power_electrical,
        "power_mechanical": power_mechanical,
        "emf_error": emf_error,
        "force_error": force_error,
        "power_error": power_error,
        "verified": emf_error < tolerance and force_error < tolerance and power_error < tolerance,
    }


@maxwell_cite(
    594, 595, 596, 597,
    part=4, chapter="Motional EMF",
    theory_class="maxwell_original",
    description="Complete sliding conductor analysis",
)
def analyze_sliding_conductor(
    B_field: float,
    conductor_length: float,
    resistance: float,
    applied_force: float = 0.0,
    mass: float = None,
    time_range: tuple[float, float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of sliding conductor dynamics.

    Art. 594-597: Comprehensive analysis including:
    1. Motional EMF
    2. Induced current
    3. Braking force
    4. Velocity vs time (if force and mass provided)
    5. Power dissipation

    Args:
        B_field: Magnetic field (gauss).
        conductor_length: Conductor length (cm).
        resistance: Circuit resistance (abohms).
        applied_force: Applied force (dynes).
        mass: Conductor mass (g).
        time_range: (t_min, t_max) in seconds.

    Returns:
        Dictionary with complete analysis results.
    """
    slider = SlidingConductor(
        conductor_length=conductor_length,
        magnetic_field=B_field,
        circuit_resistance=resistance
    )

    result = {
        "B_field": B_field,
        "conductor_length": conductor_length,
        "resistance": resistance,
        "terminal_velocity": slider.terminal_velocity(applied_force) if applied_force > 0 else 0,
    }

    if applied_force > 0 and mass is not None and time_range is not None:
        n_points = 50
        times = np.linspace(time_range[0], time_range[1], n_points)

        velocities = [slider.velocity_vs_time(applied_force, mass, t) for t in times]
        emfs = [slider.motional_emf(v) for v in velocities]
        currents = [slider.induced_current(v) for v in velocities]
        braking_forces = [slider.braking_force(v) for v in velocities]

        result["time_range"] = time_range
        result["times"] = times
        result["velocities"] = velocities
        result["emfs"] = emfs
        result["currents"] = currents
        result["braking_forces"] = braking_forces
        result["mass"] = mass
        result["applied_force"] = applied_force

    return result
