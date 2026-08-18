"""maxwell.electromagnetism.experiments.ampere_balance — Ampere's current balance (Arts. 579-584).

Simulates Ampere's classic experiment measuring forces between
current-carrying conductors using a current balance.

Maxwell's CGS formulation (Arts. 579-584):
    The force between two parallel wires of length L, separation d:

        F = 2 * I1 * I2 * L / (c^2 * d)

    where c is the speed of light in CGS units.

    The current balance measures this force by balancing it
    against a known weight:

        F = m * g

    From the equilibrium condition:

        I = sqrt(m * g * c^2 * d / (2 * L))

    Ampere showed that the force law has the form:

        dF = (I1 * I2 / r^2) * [2*(ds1·ds2) - 3*(ds1·r)(ds2·r)/r^2]

where:
    I1, I2 = currents (abamperes)
    L = wire length (cm)
    d = separation (cm)
    F = force (dynes)
    c = speed of light (cm/s)

Category: A (maxwell_original) — Ampere's force law experiment.

References:
    Part IV, Arts. 579-584: Ampere's current balance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class BalanceReading:
    """Result from a current balance measurement.

    Attributes:
        current1: Current in fixed wire (abamperes).
        current2: Current in movable wire (abamperes).
        separation: Wire separation (cm).
        wire_length: Length of parallel section (cm).
        measured_force: Measured force (dynes).
        theoretical_force: Theoretical force (dynes).
        error: Fractional error.
    """

    current1: float
    current2: float
    separation: float
    wire_length: float
    measured_force: float
    theoretical_force: float
    error: float


def _parallel_wire_force(
    current1: float,
    current2: float,
    wire_length: float,
    separation: float,
) -> float:
    """Force between two parallel straight wires (CGS-EMU).

    F = 2 * I1 * I2 * L / (c^2 * d)
    """
    if separation < 1e-15:
        return 0.0
    return 2.0 * current1 * current2 * wire_length / (CONST.C**2 * separation)


@maxwell_cite(
    579,
    580,
    part=4,
    chapter="Current Balance",
    theory_class="maxwell_original",
    description="Simulate Ampere's current balance experiment",
)
def simulate_ampere_balance(
    current1: float,
    current2: float,
    wire_length: float,
    separation: float,
    mass_precision: float = 1e-6,
) -> BalanceReading:
    """Simulate a current balance measurement.

    Art. 579-580: The balance measures the force between two
    parallel current-carrying wires.

    Args:
        current1: Current in fixed wire (abamperes).
        current2: Current in movable wire (abamperes).
        wire_length: Length of parallel section (cm).
        separation: Center-to-center separation (cm).
        mass_precision: Measurement precision (grams).

    Returns:
        BalanceReading with measured and theoretical values.
    """
    # Theoretical force
    F_theory = _parallel_wire_force(current1, current2, wire_length, separation)

    # Simulate measurement with finite precision
    g = CONST.G  # gravitational acceleration in CGS
    equivalent_mass = F_theory / g  # mass in grams

    # Add quantization from measurement precision
    quantized_mass = round(equivalent_mass / mass_precision) * mass_precision
    F_measured = quantized_mass * g

    error = abs(F_measured - F_theory) / abs(F_theory) if abs(F_theory) > 1e-15 else 0

    return BalanceReading(
        current1=current1,
        current2=current2,
        separation=separation,
        wire_length=wire_length,
        measured_force=F_measured,
        theoretical_force=F_theory,
        error=error,
    )


@maxwell_cite(
    581,
    582,
    part=4,
    chapter="Current Balance",
    theory_class="maxwell_original",
    description="Calculate force vs separation curve",
)
def force_vs_separation(
    current: float,
    wire_length: float,
    separations: list[float] | None = None,
) -> tuple[list[float], list[float]]:
    """Calculate force as function of wire separation.

    Art. 581-582: The force decreases as 1/d with separation.

    Args:
        current: Current in both wires (abamperes).
        wire_length: Wire length (cm).
        separations: List of separations (cm).

    Returns:
        Tuple of (separations, forces).
    """
    if separations is None:
        separations = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]

    forces = [
        _parallel_wire_force(current, current, wire_length, d) for d in separations
    ]
    return list(separations), forces


@maxwell_cite(
    582,
    583,
    part=4,
    chapter="Current Balance",
    theory_class="maxwell_original",
    description="Calculate force vs current curve",
)
def force_vs_current(
    wire_length: float,
    separation: float,
    currents: list[float] | None = None,
) -> tuple[list[float], list[float]]:
    """Calculate force as function of current.

    Art. 582-583: The force increases as I^2 for equal currents.

    Args:
        wire_length: Wire length (cm).
        separation: Wire separation (cm).
        currents: List of currents (abamperes).

    Returns:
        Tuple of (currents, forces).
    """
    if currents is None:
        currents = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

    forces = [_parallel_wire_force(I, I, wire_length, separation) for I in currents]
    return list(currents), forces


@maxwell_cite(
    579,
    580,
    581,
    582,
    583,
    584,
    part=4,
    chapter="Current Balance",
    theory_class="maxwell_original",
    description="Verify Ampere's force law",
)
def verify_ampere_balance(
    current: float = 1.0,
    wire_length: float = 100.0,
    separation: float = 1.0,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """Verify Ampere's force law.

    Art. 579-584: Verifies:
    1. Force proportional to I1*I2
    2. Force proportional to L
    3. Force inversely proportional to d
    4. Doubling current quadruples force (I^2 dependence)

    Args:
        current: Test current (abamperes).
        wire_length: Test wire length (cm).
        separation: Test separation (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Baseline
    F0 = _parallel_wire_force(current, current, wire_length, separation)

    # Double current -> 4x force
    F_2I = _parallel_wire_force(2 * current, 2 * current, wire_length, separation)
    current_squared = abs(F_2I / F0 - 4.0) < tolerance if abs(F0) > 1e-15 else True

    # Double length -> 2x force
    F_2L = _parallel_wire_force(current, current, 2 * wire_length, separation)
    length_linear = abs(F_2L / F0 - 2.0) < tolerance if abs(F0) > 1e-15 else True

    # Double separation -> 1/2 force
    F_2d = _parallel_wire_force(current, current, wire_length, 2 * separation)
    inverse_distance = abs(F_2d / F0 - 0.5) < tolerance if abs(F0) > 1e-15 else True

    # Opposite currents -> repulsive (sign check)
    F_opp = _parallel_wire_force(current, -current, wire_length, separation)
    opposite_sign = F_opp < 0 and F0 > 0

    return {
        "force_baseline": F0,
        "force_double_current": F_2I,
        "force_double_length": F_2L,
        "force_double_separation": F_2d,
        "current_squared_law": bool(current_squared),
        "length_linear": bool(length_linear),
        "inverse_distance": bool(inverse_distance),
        "opposite_currents_repel": bool(opposite_sign),
        "verified": bool(
            current_squared and length_linear and inverse_distance and opposite_sign
        ),
    }


@maxwell_cite(
    579,
    580,
    581,
    582,
    583,
    584,
    part=4,
    chapter="Current Balance",
    theory_class="maxwell_original",
    description="Complete current balance analysis",
)
def analyze_ampere_balance(
    current: float = 1.0,
    wire_length: float = 100.0,
    separation: float = 1.0,
) -> dict[str, float | list | BalanceReading]:
    """Complete analysis of Ampere's current balance experiment.

    Art. 579-584: Comprehensive analysis including:
    1. Single measurement simulation
    2. Force vs separation curve
    3. Force vs current curve
    4. Verification of force law

    Args:
        current: Current (abamperes).
        wire_length: Wire length (cm).
        separation: Wire separation (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    # Single measurement
    reading = simulate_ampere_balance(current, current, wire_length, separation)

    # Curves
    seps, forces_sep = force_vs_separation(current, wire_length)
    currs, forces_curr = force_vs_current(wire_length, separation)

    # Verification
    verification = verify_ampere_balance(current, wire_length, separation)

    return {
        "reading": reading,
        "separations": seps,
        "forces_vs_separation": forces_sep,
        "currents": currs,
        "forces_vs_current": forces_curr,
        "verification": verification,
        "force_law_valid": verification["verified"],
    }
