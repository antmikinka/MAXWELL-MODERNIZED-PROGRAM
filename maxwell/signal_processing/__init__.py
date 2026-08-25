"""maxwell.signal_processing — Telegraphy and observation methods (Ch. XVI).

Package for the code of Part IV, Chapter XVI of the Treatise: telegraph
line relations (Arts. 730-735, ``telegraphy.py``) and the methods of
observation (Arts. 740, 745, 750, ``observation_methods.py`` —
amplitude correction of the vibration time, first-swing correction, and
Weber's method of recoil).

Treatise attributions cover Arts. 730-735 and 740/745/750; the
``SignalTransmission`` signal-integrity heuristics are standard_math
with no article numbers (D-24 adjudication, 2026-08-21).
"""

from maxwell.signal_processing.observation_methods import (
    KAPPA_MAGNETIC_NEEDLE,
    calc_elongation_ratio,
    calc_first_swing_deflection,
    calc_recoil_charge_product,
    calc_recoil_coefficient,
    calc_recoil_damping,
    calc_recoil_elongations,
    calc_small_arc_vibration_time,
    calc_vibration_time_at_amplitude,
)
from maxwell.signal_processing.telegraphy import (
    SignalTransmission,
    TelegraphLine,
    analyze_telegraph_line,
    calc_characteristic_impedance,
    calc_propagation_constant,
    calc_signal_delay,
    calc_signal_velocity,
    verify_telegraph_line,
)

__all__ = [
    # Telegraph line relations (Arts. 730-735)
    "TelegraphLine",
    "calc_signal_velocity",
    "calc_characteristic_impedance",
    "calc_propagation_constant",
    "calc_signal_delay",
    "verify_telegraph_line",
    "analyze_telegraph_line",
    # Signal-integrity heuristics (standard_math, no articles — D-24)
    "SignalTransmission",
    # Methods of observation (Arts. 740, 745, 750)
    "KAPPA_MAGNETIC_NEEDLE",
    "calc_vibration_time_at_amplitude",
    "calc_elongation_ratio",
    "calc_small_arc_vibration_time",
    "calc_first_swing_deflection",
    "calc_recoil_coefficient",
    "calc_recoil_elongations",
    "calc_recoil_damping",
    "calc_recoil_charge_product",
]
