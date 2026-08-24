"""maxwell.experiments.ratio_v.combined — Combined methods (Arts. 773, 775-779).

Maxwell's combined method and related techniques for determining the
ratio v of electrostatic to electromagnetic units:

* Maxwell's combined resistance/capacitance comparison (Art. 773)
* Intermittent-current method (Art. 775)
* Condenser and wippe in a Wheatstone bridge (Art. 776)
* Rapid-action correction (Art. 777)
* Capacity compared with self-induction (Art. 778)
* Coil and condenser combined (Art. 779)

Dimensional bookkeeping (explicit)
==================================

Readings are numeric values in the two CGS systems; the dimensions are

* resistance:  R_ESU = s/cm = L^-1 T,     R_EMU = cm/s = L T^-1
* capacitance: C_ESU = cm   = L,           C_EMU = s^2/cm = L^-1 T^2
* inductance:  L_ESU = s^2/cm = L^-1 T^2, L_EMU = cm = L

and the numeric readings for one and the same apparatus obey
``R_ESU/R_EMU = 1/v^2``, ``C_ESU/C_EMU = v^2``, ``L_ESU/L_EMU = 1/v^2``.
Consequences used below:

* ``R_EMU C_EMU = R_ESU C_ESU`` — the RC time constant is a *pure time*
  in either system (invariant), which is the internal consistency of
  Art. 773.
* ``sqrt(L_EMU C_EMU) = sqrt(L_EMU C_ESU)/v`` — mixing an EMU inductance
  with an ESU capacitance introduces exactly one power of v, which Arts.
  778-779 exploit through the LC period.

Every reduction returns v in cm/s.
"""

from __future__ import annotations

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi

#: Speed of light in CGS (cm/s) — single source of truth (D-33 guardrail).
C_CGS = CONST.C


@maxwell_cite(
    773,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="maxwell_original",
    description="Maxwell's combined resistance and capacitance comparison",
)
def method_maxwell_combined(
    resistance_esu: float,
    resistance_emu: float,
    capacity_esu: float,
    capacity_emu: float,
) -> dict[str, float]:
    """Maxwell's combined method.

    Art. 773: the ratio is obtained from two independent comparisons of
    the *same* apparatus in the two systems, which must agree:

    * resistance readings obey ``n_esu/n_emu = 1/v^2`` (p = -2), so
      ``v = sqrt(R_EMU / R_ESU)``;
    * capacitance readings obey ``n_esu/n_emu = v^2`` (p = +2), so
      ``v = sqrt(C_ESU / C_EMU)``.

    Internal consistency (pure-time invariant): since R has power -2 and
    C power +2, the product is system-independent,

        R_EMU C_EMU = R_ESU C_ESU = tau   (seconds)

    which this reduction reports as a diagnostic.

    Args:
        resistance_esu: Resistance in statohms (s/cm).
        resistance_emu: Same resistance in abohms (cm/s).
        capacity_esu: Capacitance in ESU (cm).
        capacity_emu: Same capacitance in EMU (s^2/cm).

    Returns:
        Dictionary with v from resistance, v from capacitance, their
        mean, the disagreement percentage, the two RC time constants
        (which must coincide) and the deviation of the mean from the
        accepted speed of light.

    Raises:
        ValueError: If any reading is not positive.
    """
    if min(resistance_esu, resistance_emu, capacity_esu, capacity_emu) <= 0:
        raise ValueError(
            "all readings must be positive, got "
            f"R_esu={resistance_esu}, R_emu={resistance_emu}, "
            f"C_esu={capacity_esu}, C_emu={capacity_emu}"
        )
    v_from_resistance = float(np.sqrt(resistance_emu / resistance_esu))
    v_from_capacitance = float(np.sqrt(capacity_esu / capacity_emu))
    mean_v = 0.5 * (v_from_resistance + v_from_capacitance)
    rc_emu = resistance_emu * capacity_emu
    rc_esu = resistance_esu * capacity_esu
    return {
        "v_from_resistance": v_from_resistance,
        "v_from_capacitance": v_from_capacitance,
        "mean_v": mean_v,
        "disagreement_pct": abs(v_from_resistance - v_from_capacitance) / mean_v * 100,
        "rc_time_constant_emu_s": rc_emu,
        "rc_time_constant_esu_s": rc_esu,
        "rc_invariance_rel_diff": abs(rc_emu - rc_esu) / rc_esu,
        "deviation_from_c_pct": abs(mean_v - C_CGS) / C_CGS * 100,
    }


@maxwell_cite(
    775,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Intermittent-current determination of v",
)
def method_intermittent_current(
    capacity: float,
    voltage: float,
    frequency: float,
    measured_current: float,
) -> float:
    """Method by intermittent current.

    Art. 775: a condenser is charged and discharged ``frequency`` times
    per second.  The charge per cycle ``Q = C V`` is known in ESU
    (statcoulombs, with C in cm and V in statvolts); the average current
    is measured in EMU (abamperes):

        I_ESU = C_ESU V_ESU f,      I_EMU = I_ESU / v

    hence

        v = C_ESU V_ESU f / I_EMU        (cm/s)

    Dimensional check: the quotient is a ratio of currents; current unit
    sizes differ by one power of velocity, so the result carries L T^-1.

    Args:
        capacity: Condenser capacity (ESU, cm).
        voltage: Charging voltage (ESU, statvolts).
        frequency: Charge/discharge frequency (Hz).
        measured_current: Average current (EMU, abamperes).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If any input is not positive.
    """
    if min(capacity, voltage, frequency, measured_current) <= 0:
        raise ValueError(
            "all inputs must be positive, got "
            f"C={capacity}, V={voltage}, f={frequency}, I={measured_current}"
        )
    charge_per_cycle = capacity * voltage
    current_esu = charge_per_cycle * frequency
    return float(current_esu / measured_current)


@maxwell_cite(
    776,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Condenser and wippe in a Wheatstone bridge",
)
def method_condenser_wippe(
    bridge_ratio: float,
    condenser_capacity: float,
    known_resistance: float,
    frequency: float,
) -> float:
    """Condenser and wippe in a Wheatstone bridge.

    Art. 776: a condenser in a bridge arm is charged and discharged
    ``frequency`` times per second by the wippe (changeover switch).  At
    each cycle it carries the charge ``C V``, so its average current is
    ``C V f`` and it behaves as an effective resistance

        R_eff = V / (C V f) = 1 / (C_ESU f)        (ESU: s/cm)

    Converted to electromagnetic measure (``R_EMU = R_ESU v^2`` since
    resistance has power -2), balance of the bridge against the known
    EMU resistance ``R`` with arm ratio ``bridge_ratio = rho`` gives

        R = rho v^2 / (C_ESU f)   =>   v = sqrt(R C_ESU f / rho)

    Dimensional check: ``[R C_ESU f] = (L T^-1)(L)(T^-1) = L^2 T^-2``,
    whose square root is a velocity (cm/s).

    Args:
        bridge_ratio: Wheatstone arm ratio rho at balance (dimensionless,
            as defined above).
        condenser_capacity: Capacity of the condenser (ESU, cm).
        known_resistance: Known resistance in the bridge (EMU, abohms).
        frequency: Switching frequency (Hz).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If any input is not positive.
    """
    if min(bridge_ratio, condenser_capacity, known_resistance, frequency) <= 0:
        raise ValueError(
            "all inputs must be positive, got "
            f"rho={bridge_ratio}, C={condenser_capacity}, "
            f"R={known_resistance}, f={frequency}"
        )
    return float(
        np.sqrt(known_resistance * condenser_capacity * frequency / bridge_ratio)
    )


@maxwell_cite(
    777,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Charge fraction when the switching is too rapid for the time constant",
)
def rapid_action_charge_fraction(
    switching_frequency: float,
    circuit_time_constant: float,
) -> float:
    """Fraction of full charge reached when action is too rapid.

    Art. 777: with half-period ``t = 1/(2f)`` and circuit time constant
    ``RC``, the condenser charges only to

        charge_fraction = 1 - exp(-t / RC)

    of its full value.

    Args:
        switching_frequency: Switching frequency (Hz).
        circuit_time_constant: RC time constant of the circuit (s).

    Returns:
        Charge fraction in (0, 1).

    Raises:
        ValueError: If either input is not positive.
    """
    if switching_frequency <= 0 or circuit_time_constant <= 0:
        raise ValueError(
            f"inputs must be positive, got f={switching_frequency}, "
            f"RC={circuit_time_constant}"
        )
    half_period = 1.0 / (2.0 * switching_frequency)
    return float(1.0 - np.exp(-half_period / circuit_time_constant))


@maxwell_cite(
    777,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Correction of a v measurement when action is too rapid",
)
def apply_rapid_action_correction(
    measured_v: float,
    switching_frequency: float,
    circuit_time_constant: float,
) -> float:
    """Correction when action is too rapid.

    Art. 777: when the charging/discharging is too rapid compared with
    the circuit time constant, the condenser reaches only the charge
    fraction ``1 - exp(-t/RC)`` of its full value, so the uncorrected
    measurement comes out too LARGE:

        measured_v = v_true / charge_fraction

    Recovering the true velocity therefore MULTIPLIES by the charge
    fraction (e.g. charge_fraction = 0.5 halves the corrected value).
    The correction always shrinks the measured value (Stage 3 defect
    D-03 regression guard: the inverted, amplifying form is wrong).

    Args:
        measured_v: Uncorrected velocity measurement (cm/s).
        switching_frequency: Switching frequency (Hz).
        circuit_time_constant: RC time constant of the circuit (s).

    Returns:
        Corrected velocity (cm/s), never larger than ``measured_v``.
    """
    charge_fraction = rapid_action_charge_fraction(
        switching_frequency, circuit_time_constant
    )
    return measured_v * charge_fraction


@maxwell_cite(
    778,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Capacity compared with self-induction via LC resonance",
)
def compare_capacity_inductance(
    capacity: float,
    inductance: float,
    resonant_angular_frequency: float,
) -> float:
    """Compare capacity with self-induction.

    Art. 778: an LC circuit oscillates with ``omega = 1/sqrt(L C)`` when
    L and C are expressed in *one consistent* system.  With the
    inductance read in EMU (cm) and the capacitance in ESU (cm), the
    conversion ``C_EMU = C_ESU / v^2`` gives

        omega = 1 / sqrt(L_EMU C_EMU) = v / sqrt(L_EMU C_ESU)

    hence

        v = omega sqrt(L_EMU C_ESU)        (cm/s)

    Dimensional check: ``sqrt(cm * cm) * s^-1 = cm/s``.

    Args:
        capacity: Capacitance (ESU, cm).
        inductance: Inductance (EMU, cm).
        resonant_angular_frequency: Measured angular resonance frequency
            omega (rad/s).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If any input is not positive.
    """
    if min(capacity, inductance, resonant_angular_frequency) <= 0:
        raise ValueError(
            "all inputs must be positive, got "
            f"C={capacity}, L={inductance}, omega={resonant_angular_frequency}"
        )
    return float(resonant_angular_frequency * np.sqrt(inductance * capacity))


@maxwell_cite(
    779,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Coil and condenser combined: v from the oscillation period",
)
def combine_coil_condenser(
    coil_inductance: float,
    condenser_capacity: float,
    measured_period: float,
) -> float:
    """Coil and condenser combined.

    Art. 779: a coil of known EMU inductance ``L`` (cm) and a condenser
    of known ESU capacity ``C`` (cm) form an oscillator whose period,
    with ``C_EMU = C_ESU / v^2``, is

        T = 2 pi sqrt(L_EMU C_EMU) = 2 pi sqrt(L_EMU C_ESU) / v

    hence

        v = 2 pi sqrt(L_EMU C_ESU) / T        (cm/s)

    Dimensional check: ``sqrt(cm * cm) / s = cm/s``.

    Args:
        coil_inductance: Inductance of the coil (EMU, cm).
        condenser_capacity: Capacity of the condenser (ESU, cm).
        measured_period: Oscillation period (s).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If any input is not positive.
    """
    if min(coil_inductance, condenser_capacity, measured_period) <= 0:
        raise ValueError(
            "all inputs must be positive, got "
            f"L={coil_inductance}, C={condenser_capacity}, T={measured_period}"
        )
    return float(
        2.0 * PI * np.sqrt(coil_inductance * condenser_capacity) / measured_period
    )
