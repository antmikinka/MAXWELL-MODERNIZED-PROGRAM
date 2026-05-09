"""maxwell.signal_processing — Signal transmission and telegraphy (Arts. 730-757).

Package for Maxwell's theory of electromagnetic signal transmission,
including telegraphy and signal propagation along transmission lines.
"""

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
    # Telegraph line (Arts. 730-757)
    "TelegraphLine",
    "SignalTransmission",
    "calc_signal_velocity",
    "calc_characteristic_impedance",
    "calc_propagation_constant",
    "calc_signal_delay",
    "verify_telegraph_line",
    "analyze_telegraph_line",
]
