"""maxwell.calibration — Electrical measurement and calibration (Arts. 758-767).

Package for Maxwell's treatment of absolute electrical measurements,
including resistance calibration and electromagnetic measurement methods.

Maxwell's methods (Arts. 758-767):
- Absolute resistance measurement using induced currents
- Calibration of galvanometers and electrometers
- Bridge methods for precise measurements
- Standard resistance coils and their calibration
"""

from maxwell.calibration.absolute_resistance import (
    AbsoluteResistance,
    StandardResistanceCoil,
    analyze_absolute_resistance,
    calc_absolute_resistance_joule,
    calc_absolute_resistance_lenz,
    calc_absolute_resistance_recoil,
    calc_absolute_resistance_rotating_coil,
    calc_temperature_corrected_resistance,
    verify_absolute_resistance,
)

__all__ = [
    # Absolute resistance (Arts. 758-767)
    "AbsoluteResistance",
    "StandardResistanceCoil",
    "calc_absolute_resistance_recoil",
    "calc_absolute_resistance_lenz",
    "calc_absolute_resistance_rotating_coil",
    "calc_absolute_resistance_joule",
    "calc_temperature_corrected_resistance",
    "verify_absolute_resistance",
    "analyze_absolute_resistance",
]
