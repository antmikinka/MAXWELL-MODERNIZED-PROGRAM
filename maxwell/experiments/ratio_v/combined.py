"""maxwell.experiments.ratio_v.combined — Combined methods (Arts. 775-779).

Maxwell's combined method and related techniques:
- Intermittent current method
- Condenser and wippe in Wheatstone bridge
- Rapid action correction
- Capacity compared with self-induction
- Coil and condenser combined
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi
C_CGS = 2.99792458e10


@maxwell_cite(773, part=4, theory_class="maxwell_original")
def method_maxwell_combined(
    resistance_esu: float,
    resistance_emu: float,
    capacity_esu: float,
    capacity_emu: float,
) -> dict[str, float]:
    """Maxwell's combined method.

    Art. 773: Maxwell used both resistance and capacitance
    measurements to cross-check the ratio determination.

    From resistance: v^2 = R_ESU / R_EMU
    From capacitance: v^2 = C_ESU / C_EMU

    The two methods should give the same result.

    Args:
        resistance_esu: Resistance in ESU (statohms).
        resistance_emu: Resistance in EMU (abohms).
        capacity_esu: Capacitance in ESU (cm).
        capacity_emu: Capacitance in EMU.

    Returns:
        Velocity calculations from both methods.
    """
    v_from_resistance = np.sqrt(resistance_esu / resistance_emu)
    v_from_capacitance = np.sqrt(capacity_esu / capacity_emu)

    return {
        "v_from_resistance": v_from_resistance,
        "v_from_capacitance": v_from_capacitance,
        "mean_v": (v_from_resistance + v_from_capacitance) / 2,
        "disagreement_pct": abs(v_from_resistance - v_from_capacitance)
                            / ((v_from_resistance + v_from_capacitance) / 2) * 100,
        "deviation_from_c_pct": abs((v_from_resistance + v_from_capacitance) / 2 - C_CGS)
                                / C_CGS * 100,
    }


@maxwell_cite(775, part=4, theory_class="standard_math")
def method_intermittent_current(
    capacity: float,
    voltage: float,
    frequency: float,
    measured_current: float,
) -> float:
    """Method by intermittent current.

    Art. 775: A condenser is charged and discharged at a
    known frequency, producing an intermittent current.
    The ratio v is determined from the relationship
    between the charge (ESU) and the measured current (EMU).

    Args:
        capacity: Condenser capacity (ESU, cm).
        voltage: Charging voltage (ESU, statvolts).
        frequency: Charge/discharge frequency.
        measured_current: Average current (EMU, abamperes).

    Returns:
        Calculated velocity v.
    """
    # Charge per cycle: q = C * V (in ESU)
    # Average current: I = q * f (in ESU/s)
    # In EMU: I_EMU = I_ESU / v
    # So v = I_ESU / I_EMU = C * V * f / I_EMU
    charge_per_cycle = capacity * voltage
    current_esu = charge_per_cycle * frequency
    return current_esu / measured_current


@maxwell_cite(776, part=4, theory_class="standard_math")
def method_condenser_wippe(
    bridge_ratio: float,
    condenser_capacity: float,
    known_resistance: float,
    frequency: float,
) -> float:
    """Condenser and wippe in Wheatstone bridge.

    Art. 776: A condenser is placed in one arm of a
    Wheatstone bridge. The wippe (changeover switch)
    alternately charges and discharges the condenser.
    Balance conditions yield the ratio v.

    Args:
        bridge_ratio: Ratio of the bridge arms at balance.
        condenser_capacity: Capacity of the condenser.
        known_resistance: Known resistance in the bridge.
        frequency: Switching frequency.

    Returns:
        Calculated velocity v.
    """
    # At balance: R = 1 / (C * f * v^2)
    # So v = 1 / sqrt(R * C * f)
    return 1.0 / np.sqrt(known_resistance * condenser_capacity * frequency)


@maxwell_cite(777, part=4, theory_class="standard_math")
def apply_rapid_action_correction(
    measured_v: float,
    switching_frequency: float,
    circuit_time_constant: float,
) -> float:
    """Correction when action is too rapid.

    Art. 777: When the charging/discharging is too rapid
    compared to the circuit time constant, the condenser
    does not fully charge or discharge, requiring a correction.

    Args:
        measured_v: Uncorrected velocity measurement.
        switching_frequency: Switching frequency.
        circuit_time_constant: RC time constant of the circuit.

    Returns:
        Corrected velocity.
    """
    # Correction factor: the condenser charges to
    # V * (1 - exp(-t/RC)) instead of V
    # For t = 1/(2f) (half-period):
    half_period = 1.0 / (2.0 * switching_frequency)
    charge_fraction = 1.0 - np.exp(-half_period / circuit_time_constant)

    return measured_v / charge_fraction


@maxwell_cite(778, part=4, theory_class="standard_math")
def compare_capacity_inductance(
    capacity: float,
    inductance: float,
    resonant_frequency: float,
) -> float:
    """Compare capacity with self-induction.

    Art. 778: The resonance frequency of an LC circuit:
    omega = 1 / sqrt(L * C)

    If L is measured in EMU and C in ESU, the resonance
    frequency involves the ratio v.

    Args:
        capacity: Capacitance (ESU).
        inductance: Inductance (EMU).
        resonant_frequency: Measured resonance frequency.

    Returns:
        Calculated velocity v.
    """
    # omega = v / sqrt(L_EMU * C_ESU)
    # So v = omega * sqrt(L_EMU * C_ESU)
    return resonant_frequency * np.sqrt(inductance * capacity)


@maxwell_cite(779, part=4, theory_class="standard_math")
def combine_coil_condenser(
    coil_inductance: float,
    condenser_capacity: float,
    measured_period: float,
) -> float:
    """Coil and condenser combined.

    Art. 779: Combining a coil of known inductance (EMU)
    with a condenser of known capacity (ESU) to determine
    the ratio v from the oscillation period.

    T = 2*pi * sqrt(L_EMU * C_ESU) / v

    Args:
        coil_inductance: Inductance of coil (EMU, cm).
        condenser_capacity: Capacity (ESU, cm).
        measured_period: Oscillation period.

    Returns:
        Calculated velocity v.
    """
    # v = 2*pi * sqrt(L * C) / T
    return 2.0 * PI * np.sqrt(coil_inductance * condenser_capacity) / measured_period
