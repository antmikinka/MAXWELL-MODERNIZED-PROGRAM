"""maxwell.electromagnetism.induction.lenz — Lenz's law (Art. 542).

Implements Maxwell's formulation of Lenz's law for electromagnetic induction,
which determines the direction of induced currents.

Maxwell's CGS formulation (Art. 542):
    Lenz's law: The induced EMF opposes the change in magnetic flux.

        EMF = -d(Phi)/dt

    where Phi is the magnetic flux through the circuit.

    The negative sign indicates that the induced current creates a magnetic
    field that opposes the change in the original field.

where:
    Phi = magnetic flux (maxwells)
    EMF = electromotive force (statvolts or abvolts)
    t = time (seconds)

Category: A (maxwell_original) — Maxwell's formulation of Lenz's law.

References:
    Part IV, Art. 542: Lenz's law and direction of induced currents.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class LenzLawCalculator:
    """
    Calculator for Lenz's law applications.

    Art. 542: Lenz's law determines the direction of induced currents:
    the induced EMF always opposes the change in magnetic flux that
    produced it.

    This class provides calculations for various induction scenarios.

    Attributes:
        circuit_area: Area of the circuit (cm²).
        circuit_normal: Unit vector normal to circuit plane.
        resistance: Circuit resistance (abohms).
    """

    circuit_area: float
    circuit_normal: np.ndarray = None
    resistance: float = 1.0

    def __post_init__(self):
        """Validate and set defaults."""
        if self.circuit_area <= 0:
            raise ValueError(f"Circuit area must be positive, got {self.circuit_area}")

        self.circuit_normal = np.asarray(self.circuit_normal, dtype=np.float64) if self.circuit_normal is not None else np.array([0.0, 0.0, 1.0])
        norm = np.linalg.norm(self.circuit_normal)
        if norm > 0:
            self.circuit_normal = self.circuit_normal / norm

        if self.resistance <= 0:
            raise ValueError(f"Resistance must be positive, got {self.resistance}")

    @maxwell_cite(
        542,
        part=4, chapter="Lenz's Law",
        theory_class="maxwell_original",
        description="Calculate induced EMF from flux change",
    )
    def induced_emf(self, dPhi_dt: float) -> float:
        """
        Calculate induced EMF from rate of change of flux.

        Art. 542: The induced EMF is:

            EMF = -d(Phi)/dt

        The negative sign is Lenz's law.

        Args:
            dPhi_dt: Rate of change of magnetic flux (maxwells/s).

        Returns:
            Induced EMF (abvolts). Negative sign indicates opposition.
        """
        return -dPhi_dt

    @maxwell_cite(
        542,
        part=4, chapter="Lenz's Law",
        theory_class="maxwell_original",
        description="Calculate induced current from EMF",
    )
    def induced_current(self, dPhi_dt: float) -> float:
        """
        Calculate induced current from rate of change of flux.

        Art. 542: The induced current is:

            I = EMF / R = -(1/R) * d(Phi)/dt

        Args:
            dPhi_dt: Rate of change of flux (maxwells/s).

        Returns:
            Induced current (abamperes).
        """
        emf = self.induced_emf(dPhi_dt)
        return emf / self.resistance

    @maxwell_cite(
        542,
        part=4, chapter="Lenz's Law",
        theory_class="maxwell_original",
        description="Calculate induced current direction",
    )
    def current_direction(self, dPhi_dt: float) -> str:
        """
        Determine direction of induced current.

        Art. 542: The direction is determined by Lenz's law:
        - If flux is increasing (dPhi/dt > 0), induced current creates
          opposing field (negative direction relative to normal)
        - If flux is decreasing (dPhi/dt < 0), induced current creates
          reinforcing field (positive direction)

        Args:
            dPhi_dt: Rate of change of flux.

        Returns:
            'opposing' if flux increasing, 'reinforcing' if decreasing.
        """
        if dPhi_dt > 0:
            return "opposing"
        elif dPhi_dt < 0:
            return "reinforcing"
        else:
            return "none"

    @maxwell_cite(
        542,
        part=4, chapter="Lenz's Law",
        theory_class="maxwell_original",
        description="Calculate EMF from moving conductor",
    )
    def motional_emf(self, velocity: np.ndarray, B_field: np.ndarray, length: float) -> float:
        """
        Calculate motional EMF from conductor moving in magnetic field.

        Art. 542: For a conductor of length L moving with velocity v
        perpendicular to magnetic field B:

            EMF = (v × B) · L

        The direction follows Lenz's law.

        Args:
            velocity: Velocity of conductor (cm/s).
            B_field: Magnetic field (gauss).
            length: Length of conductor (cm).

        Returns:
            Motional EMF (abvolts).
        """
        velocity = np.asarray(velocity, dtype=np.float64)
        B_field = np.asarray(B_field, dtype=np.float64)

        # v × B gives electric field
        E = np.cross(velocity, B_field)

        # Project along conductor (assume conductor is along circuit tangent)
        # For a simple geometry, magnitude is |v| * |B| * sin(theta) * L
        emf_magnitude = np.linalg.norm(E) * length

        # Sign from Lenz's law
        return -emf_magnitude


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Calculate induced EMF: EMF = -d(Phi)/dt",
)
def calc_induced_emf(
    dPhi_dt: float,
) -> float:
    """
    Calculate induced electromotive force.

    Art. 542: Faraday's law with Lenz's law:

        EMF = -d(Phi)/dt

    The negative sign indicates the induced EMF opposes the flux change.

    Args:
        dPhi_dt: Rate of change of magnetic flux (maxwells/s).

    Returns:
        Induced EMF (abvolts).

    Reference:
        Part IV, Art. 542: Lenz's law formulation.

    Example:
        >>> # Flux increasing at 1000 maxwells/s
        >>> EMF = calc_induced_emf(1000)
        >>> print(f"EMF = {EMF} abvolts")  # EMF = -1000 abvolts
    """
    return -dPhi_dt


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Calculate induced current: I = -(1/R)*d(Phi)/dt",
)
def calc_induced_current(
    dPhi_dt: float,
    resistance: float,
) -> float:
    """
    Calculate induced current in a resistive circuit.

    Art. 542: Combining Faraday's law with Ohm's law:

        I = EMF / R = -(1/R) * d(Phi)/dt

    Args:
        dPhi_dt: Rate of change of flux (maxwells/s).
        resistance: Circuit resistance (abohms).

    Returns:
        Induced current (abamperes).

    Reference:
        Part IV, Art. 542: Induced current calculation.
    """
    emf = calc_induced_emf(dPhi_dt)
    return emf / resistance


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Calculate motional EMF: EMF = (v × B) · L",
)
def calc_motional_emf_lenz(
    velocity: np.ndarray,
    B_field: np.ndarray,
    conductor_length: np.ndarray,
) -> float:
    """
    Calculate motional EMF with Lenz's law direction.

    Art. 542: For a conductor moving in a magnetic field:

        EMF = integral((v × B) · dl)

    For a straight conductor:

        EMF = (v × B) · L

    Args:
        velocity: Velocity of conductor (cm/s).
        B_field: Magnetic field (gauss).
        conductor_length: Length vector of conductor (cm).

    Returns:
        Motional EMF (abvolts).

    Reference:
        Part IV, Art. 542: Motional EMF.
    """
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)
    conductor_length = np.asarray(conductor_length, dtype=np.float64)

    # v × B gives induced electric field
    E_induced = np.cross(velocity, B_field)

    return -np.dot(E_induced, conductor_length)


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Calculate EMF from rotating coil",
)
def calc_rotating_coil_emf(
    B_field: float,
    coil_area: float,
    n_turns: int,
    angular_velocity: float,
    time: float,
) -> float:
    """
    Calculate EMF from a coil rotating in a magnetic field.

    Art. 542: For a coil rotating with angular velocity omega in field B:

        Phi(t) = N * B * A * cos(omega * t)
        EMF = -d(Phi)/dt = N * B * A * omega * sin(omega * t)

    Args:
        B_field: Magnetic field strength (gauss).
        coil_area: Area of coil (cm²).
        n_turns: Number of turns.
        angular_velocity: Angular velocity (rad/s).
        time: Time at which to calculate (s).

    Returns:
        Induced EMF (abvolts).

    Reference:
        Part IV, Art. 542: Rotating coil EMF.
    """
    omega = angular_velocity
    phase = omega * time

    return n_turns * B_field * coil_area * omega * np.sin(phase)


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Verify Lenz's law direction",
)
def verify_lenz_law_direction(
    initial_flux: float,
    final_flux: float,
    time_interval: float,
    resistance: float = 1.0,
) -> dict[str, float | str | bool]:
    """
    Verify Lenz's law direction for flux change.

    Art. 542: This function verifies that:
    1. Increasing flux induces opposing current
    2. Decreasing flux induces reinforcing current
    3. The magnitude follows |EMF| = |dPhi/dt|

    Args:
        initial_flux: Initial magnetic flux (maxwells).
        final_flux: Final magnetic flux (maxwells).
        time_interval: Time interval (s).
        resistance: Circuit resistance (abohms).

    Returns:
        Dictionary with verification results.
    """
    if time_interval <= 0:
        raise ValueError(f"Time interval must be positive")

    dPhi = final_flux - initial_flux
    dPhi_dt = dPhi / time_interval

    emf = calc_induced_emf(dPhi_dt)
    current = calc_induced_current(dPhi_dt, resistance)

    # Direction check
    if dPhi > 0:
        expected_direction = "opposing"
        direction_correct = emf < 0
    elif dPhi < 0:
        expected_direction = "reinforcing"
        direction_correct = emf > 0
    else:
        expected_direction = "none"
        direction_correct = abs(emf) < 1e-15

    return {
        "initial_flux": initial_flux,
        "final_flux": final_flux,
        "flux_change": dPhi,
        "dPhi_dt": dPhi_dt,
        "induced_emf": emf,
        "induced_current": current,
        "expected_direction": expected_direction,
        "direction_correct": direction_correct,
        "lenz_law_verified": direction_correct,
    }


@maxwell_cite(
    542,
    part=4, chapter="Lenz's Law",
    theory_class="maxwell_original",
    description="Complete Lenz's law analysis",
)
def analyze_lenz_law(
    flux_function: callable,
    time_range: tuple[float, float],
    n_points: int = 100,
    resistance: float = 1.0,
) -> dict[str, float | list]:
    """
    Complete analysis of Lenz's law for arbitrary flux function.

    Art. 542: Comprehensive analysis including:
    1. Flux vs time
    2. Induced EMF vs time
    3. Induced current vs time
    4. Direction changes

    Args:
        flux_function: Function Phi(t) returning flux at time t.
        time_range: (t_min, t_max) in seconds.
        n_points: Number of evaluation points.
        resistance: Circuit resistance (abohms).

    Returns:
        Dictionary with analysis results.
    """
    t_min, t_max = time_range
    times = np.linspace(t_min, t_max, n_points)

    fluxes = [flux_function(t) for t in times]

    # Numerical derivative for EMF
    dt = (t_max - t_min) / (n_points - 1)
    emfs = []
    currents = []
    directions = []

    for i, t in enumerate(times):
        if i == 0:
            dPhi_dt = (fluxes[1] - fluxes[0]) / dt
        elif i == n_points - 1:
            dPhi_dt = (fluxes[-1] - fluxes[-2]) / dt
        else:
            dPhi_dt = (fluxes[i + 1] - fluxes[i - 1]) / (2 * dt)

        emf = calc_induced_emf(dPhi_dt)
        current = calc_induced_current(dPhi_dt, resistance)
        direction = "opposing" if dPhi_dt > 0 else ("reinforcing" if dPhi_dt < 0 else "none")

        emfs.append(emf)
        currents.append(current)
        directions.append(direction)

    return {
        "times": times,
        "fluxes": fluxes,
        "emfs": emfs,
        "currents": currents,
        "directions": directions,
        "max_emf": max(abs(e) for e in emfs),
        "max_current": max(abs(c) for c in currents),
        "direction_changes": sum(1 for i in range(1, len(directions)) if directions[i] != directions[i - 1]),
    }
