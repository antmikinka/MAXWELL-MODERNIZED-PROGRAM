"""maxwell.electromagnetism.currents.emf_relation — EMF-current relation (Art. 611).

Implements Maxwell's equation relating electromotive force to current,
including resistance and inductance effects.

Maxwell's CGS formulation (Art. 611):
    EMF-current equation (Eq. I):

        EMF = R*I + L*dI/dt

    This is the circuit equation including both resistive voltage drop
    and inductive EMF.

    In terms of fields:
        integral(E·dl) = R*I + L*dI/dt

where:
    EMF = electromotive force (abvolts)
    R = resistance (abohms)
    I = current (abamperes)
    L = inductance (cm in CGS)

Category: A (maxwell_original) — Maxwell's EMF-current theory.

References:
    Part IV, Art. 611: EMF-current equation (Eq. I).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class EMFCurrentRelation:
    """
    EMF-current relation calculator.

    Art. 611: Maxwell's equation for circuits:

        EMF = R*I + L*dI/dt

    Attributes:
        resistance: Circuit resistance R (abohms).
        inductance: Circuit inductance L (cm).
    """

    resistance: float
    inductance: float = 0.0

    def __post_init__(self):
        """Validate parameters."""
        if self.resistance < 0:
            raise ValueError(f"Resistance must be non-negative")
        if self.inductance < 0:
            raise ValueError(f"Inductance must be non-negative")

    @maxwell_cite(
        611,
        part=4,
        chapter="EMF-Current Relation",
        theory_class="maxwell_original",
        description="Calculate EMF from current and dI/dt",
    )
    def emf(self, current: float, dI_dt: float) -> float:
        """
        Calculate EMF from current and its rate of change.

        Art. 611: EMF = R*I + L*dI/dt

        Args:
            current: Current (abamperes).
            dI_dt: Rate of change of current (abamperes/s).

        Returns:
            EMF (abvolts).
        """
        return self.resistance * current + self.inductance * dI_dt

    @maxwell_cite(
        611,
        part=4,
        chapter="EMF-Current Relation",
        theory_class="maxwell_original",
        description="Calculate current from EMF",
    )
    def steady_current(self, emf: float) -> float:
        """
        Calculate steady-state current (dI/dt = 0).

        Art. 611: For steady state:

            I = EMF / R

        Args:
            emf: Applied EMF (abvolts).

        Returns:
            Steady current (abamperes).
        """
        if self.resistance <= 0:
            return float("inf")
        return emf / self.resistance


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate EMF: EMF = R*I + L*dI/dt",
)
def calc_emf_current_relation(
    resistance: float,
    current: float,
    inductance: float,
    dI_dt: float,
) -> float:
    """
    Calculate EMF from current and its rate of change.

    Art. 611: The complete circuit equation:

        EMF = R*I + L*dI/dt

    Args:
        resistance: Resistance R (abohms).
        current: Current I (abamperes).
        inductance: Inductance L (cm).
        dI_dt: Rate of change of current (abamperes/s).

    Returns:
        EMF (abvolts).

    Reference:
        Part IV, Art. 611: EMF-current equation (Eq. I).
    """
    return resistance * current + inductance * dI_dt


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate resistive voltage drop",
)
def calc_resistive_drop(
    resistance: float,
    current: float,
) -> float:
    """
    Calculate resistive voltage drop (Ohm's law).

    Art. 611: V = R*I

    Args:
        resistance: Resistance (abohms).
        current: Current (abamperes).

    Returns:
        Voltage drop (abvolts).

    Reference:
        Part IV, Art. 611: Resistive drop.
    """
    return resistance * current


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate inductive EMF",
)
def calc_inductive_emf(
    inductance: float,
    dI_dt: float,
) -> float:
    """
    Calculate inductive EMF.

    Art. 611: EMF_inductive = L*dI/dt

    The sign depends on whether current is increasing or decreasing.

    Args:
        inductance: Inductance L (cm).
        dI_dt: Rate of change of current (abamperes/s).

    Returns:
        Inductive EMF (abvolts).

    Reference:
        Part IV, Art. 611: Inductive EMF.
    """
    return inductance * dI_dt


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate current in RL circuit",
)
def calc_rl_circuit_current(
    emf: float,
    resistance: float,
    inductance: float,
    time: float,
    initial_current: float = 0.0,
) -> float:
    """
    Calculate current in an RL circuit with constant EMF.

    Art. 611: The solution to R*I + L*dI/dt = EMF is:

        I(t) = (EMF/R) * (1 - exp(-Rt/L)) + I0*exp(-Rt/L)

    Args:
        emf: Applied EMF (abvolts).
        resistance: Resistance (abohms).
        inductance: Inductance (cm).
        time: Time (s).
        initial_current: Initial current (abamperes).

    Returns:
        Current at time t (abamperes).

    Reference:
        Part IV, Art. 611: RL circuit response.
    """
    if resistance <= 0:
        # Pure inductor
        if inductance > 0:
            return initial_current + (emf / inductance) * time
        return initial_current

    tau = inductance / resistance if inductance > 0 else 0
    I_final = emf / resistance

    if tau > 0:
        return I_final * (1.0 - np.exp(-time / tau)) + initial_current * np.exp(
            -time / tau
        )
    else:
        return I_final


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate line integral of E around circuit",
)
def calc_line_integral_E(
    E_field_func: callable,
    circuit_path: list[np.ndarray],
) -> float:
    """
    Calculate line integral of E around a circuit.

    Art. 611: The EMF is:

        EMF = integral(E · dl)

    Args:
        E_field_func: Function E(r) returning electric field.
        circuit_path: List of points defining circuit path.

    Returns:
        EMF (abvolts).

    Reference:
        Part IV, Art. 611: Line integral of E.
    """
    circuit_path = [np.asarray(p, dtype=np.float64) for p in circuit_path]
    n = len(circuit_path)

    if n < 2:
        return 0.0

    emf = 0.0
    for i in range(n):
        dl = circuit_path[(i + 1) % n] - circuit_path[i]
        mid_point = (circuit_path[i] + circuit_path[(i + 1) % n]) / 2

        E = np.asarray(E_field_func(mid_point), dtype=np.float64)
        emf += np.dot(E, dl)

    return emf


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Verify EMF-current relation",
)
def verify_emf_current_relation(
    resistance: float = 1.0,
    inductance: float = 100.0,
    emf: float = 1.0,
    test_times: list[float] = None,
    tolerance: float = 1e-10,
) -> dict[str, float | bool | list]:
    """
    Verify EMF-current relation.

    Art. 611: This function verifies:
    1. EMF = R*I + L*dI/dt at all times
    2. Steady state: I = EMF/R

    Args:
        resistance: Resistance (abohms).
        inductance: Inductance (cm).
        emf: Applied EMF (abvolts).
        test_times: Times to evaluate.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_times is None:
        tau = inductance / resistance if resistance > 0 else 1.0
        test_times = [0.01 * tau, 0.1 * tau, 0.5 * tau, tau, 2 * tau, 5 * tau]

    verified_at_all_times = True
    results = []

    for t in test_times:
        I = calc_rl_circuit_current(emf, resistance, inductance, t)

        # Calculate dI/dt
        dt = 1e-12
        I_plus = calc_rl_circuit_current(emf, resistance, inductance, t + dt)
        I_minus = calc_rl_circuit_current(emf, resistance, inductance, t - dt)
        dI_dt = (I_plus - I_minus) / (2 * dt)

        # Check EMF = R*I + L*dI/dt
        emf_calculated = resistance * I + inductance * dI_dt
        emf_error = (
            abs(emf_calculated - emf) / abs(emf)
            if abs(emf) > 0
            else abs(emf_calculated)
        )

        verified = emf_error < tolerance
        verified_at_all_times = verified_at_all_times and verified

        results.append(
            {
                "time": t,
                "current": I,
                "dI_dt": dI_dt,
                "emf_calculated": emf_calculated,
                "emf_error": emf_error,
                "verified": verified,
            }
        )

    # Steady state check
    I_steady = calc_rl_circuit_current(
        emf,
        resistance,
        inductance,
        10.0 * (inductance / resistance if resistance > 0 else 1.0),
    )
    I_expected = emf / resistance if resistance > 0 else float("inf")
    steady_error = (
        abs(I_steady - I_expected) / I_expected
        if I_expected < float("inf") and I_expected > 0
        else 0
    )

    return {
        "resistance": resistance,
        "inductance": inductance,
        "emf": emf,
        "test_times": test_times,
        "results_by_time": results,
        "steady_state_current": I_steady,
        "expected_steady_current": I_expected,
        "steady_state_error": steady_error,
        "verified_at_all_times": verified_at_all_times,
        "relation_verified": verified_at_all_times and steady_error < tolerance,
    }


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Complete EMF-current analysis",
)
def analyze_emf_current(
    resistance: float,
    inductance: float,
    emf: float,
    time_range: tuple[float, float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of EMF-current relation.

    Art. 611: Comprehensive analysis including:
    1. Current vs time
    2. Resistive and inductive voltage drops
    3. Power analysis

    Args:
        resistance: Resistance (abohms).
        inductance: Inductance (cm).
        emf: Applied EMF (abvolts).
        time_range: (t_min, t_max) in seconds.

    Returns:
        Dictionary with complete analysis results.
    """
    tau = inductance / resistance if resistance > 0 else 1.0

    if time_range is None:
        time_range = (0.0, 5.0 * tau)

    n_points = 50
    times = np.linspace(time_range[0], time_range[1], n_points)

    currents = []
    resistive_drops = []
    inductive_emfs = []
    powers = []

    for t in times:
        I = calc_rl_circuit_current(emf, resistance, inductance, t, 0.0)

        # Numerical dI/dt
        dt = 1e-12
        I_plus = calc_rl_circuit_current(emf, resistance, inductance, t + dt, 0.0)
        I_minus = calc_rl_circuit_current(emf, resistance, inductance, t - dt, 0.0)
        dI_dt = (I_plus - I_minus) / (2 * dt)

        V_R = resistance * I
        V_L = inductance * dI_dt

        currents.append(I)
        resistive_drops.append(V_R)
        inductive_emfs.append(V_L)
        powers.append(emf * I)

    I_final = emf / resistance if resistance > 0 else 0

    return {
        "resistance": resistance,
        "inductance": inductance,
        "emf": emf,
        "time_constant": tau,
        "time_range": time_range,
        "times": times,
        "currents": currents,
        "resistive_drops": resistive_drops,
        "inductive_emfs": inductive_emfs,
        "powers": powers,
        "final_current": currents[-1] if currents else 0,
        "expected_final_current": I_final,
    }


# =============================================================================
# ALIASES AND ADDITIONAL FUNCTIONS FOR TEST COMPATIBILITY
# =============================================================================


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate current from EMF (Ohm's law)",
)
def calc_current_from_emf(emf: float, resistance: float) -> float:
    """
    Calculate current from EMF using Ohm's law.

    Art. 611: I = EMF / R

    Args:
        emf: Electromotive force (abvolts).
        resistance: Resistance (abohms).

    Returns:
        Current I (abamperes).

    Reference:
        Part IV, Art. 611: Ohm's law.
    """
    if resistance <= 0:
        return float("inf")
    return emf / resistance


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate EMF from current",
)
def calc_emf_from_current(current: float, resistance: float) -> float:
    """
    Calculate EMF from current using Ohm's law.

    Art. 611: EMF = I * R

    Args:
        current: Current (abamperes).
        resistance: Resistance (abohms).

    Returns:
        EMF (abvolts).

    Reference:
        Part IV, Art. 611: Ohm's law.
    """
    return current * resistance


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate power from EMF",
)
def calc_power_from_emf(emf: float, current: float) -> float:
    """
    Calculate power from EMF and current.

    Art. 611: P = EMF * I

    Args:
        emf: Electromotive force (abvolts).
        current: Current (abamperes).

    Returns:
        Power P (ergs/s).

    Reference:
        Part IV, Art. 611: Power.
    """
    return emf * current


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate series resistance",
)
def calc_series_resistance(resistances: list[float]) -> float:
    """
    Calculate total resistance for series combination.

    Art. 611: R_series = R1 + R2 + ...

    Args:
        resistances: List of resistances.

    Returns:
        Total series resistance.

    Reference:
        Part IV, Art. 611: Series resistance.
    """
    return sum(resistances)


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate parallel resistance",
)
def calc_parallel_resistance(resistances: list[float]) -> float:
    """
    Calculate total resistance for parallel combination.

    Art. 611: 1/R_parallel = 1/R1 + 1/R2 + ...

    Args:
        resistances: List of resistances.

    Returns:
        Total parallel resistance.

    Reference:
        Part IV, Art. 611: Parallel resistance.
    """
    if not resistances:
        return float("inf")
    inv_sum = sum(1.0 / r for r in resistances if r > 0)
    if inv_sum <= 0:
        return float("inf")
    return 1.0 / inv_sum


# Alias for test compatibility
EMFRelation = EMFCurrentRelation


# Add methods to EMFRelation class for test compatibility
@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate current from EMF",
)
def _emf_current_from_emf(self, emf: float) -> float:
    """Calculate current from EMF: I = EMF / R."""
    return emf / self.resistance if self.resistance > 0 else float("inf")


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate EMF from current",
)
def _emf_emf_from_current(self, current: float) -> float:
    """Calculate EMF from current: EMF = I * R."""
    return current * self.resistance


@maxwell_cite(
    611,
    part=4,
    chapter="EMF-Current Relation",
    theory_class="maxwell_original",
    description="Calculate power",
)
def _emf_power(self, emf: float, current: float) -> float:
    """Calculate power: P = EMF * I."""
    return emf * current


# Add methods to class
EMFCurrentRelation.current_from_emf = _emf_current_from_emf
EMFCurrentRelation.emf_from_current = _emf_emf_from_current
EMFCurrentRelation.power = _emf_power
