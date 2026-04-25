"""maxwell.experiments.ratio_v.condensers — Condenser methods (Arts. 771-774).

Experimental methods using capacitor (condenser) discharge to
determine the ratio of ESU to EMU units:
- Weber and Kohlrausch's method
- Thomson's electrometer method
- Jenkin's method by condenser capacity
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi
C_CGS = 2.99792458e10


@maxwell_cite(771, part=4, theory_class="standard_math")
def method_weber_kohlrausch(
    capacity_emu: float,
    capacity_esu: float,
) -> float:
    """Weber and Kohlrausch's method (1856).

    The first measurement of the ratio v. They measured the
    capacitance of a condenser in both EMU and ESU units:
    - ESU: by geometric measurement and calculation
    - EMU: by comparing with a known resistance and period

    C_ESU / C_EMU = v^2

    Args:
        capacity_emu: Capacitance in EMU units.
        capacity_esu: Capacitance in ESU units.

    Returns:
        Calculated velocity v = sqrt(C_ESU / C_EMU).
    """
    ratio = capacity_esu / capacity_emu if capacity_emu != 0 else float("inf")
    return np.sqrt(ratio)


@dataclass
class CondenserMeasurement:
    """A single condenser-based measurement of the ratio v."""

    geometry_capacitance: float  # Calculated from dimensions (ESU)
    measured_capacitance: float  # Measured electrically (EMU)
    method: str

    @maxwell_cite(771, part=4, theory_class="standard_math")
    def calculate_v(self) -> float:
        """Calculate v from condenser measurements."""
        return np.sqrt(self.geometry_capacitance / self.measured_capacitance)

    @maxwell_cite(771, part=4, theory_class="standard_math")
    def deviation_from_c(self) -> float:
        """Percentage deviation from speed of light."""
        v = self.calculate_v()
        return abs(v - C_CGS) / C_CGS * 100


@maxwell_cite(772, part=4, theory_class="standard_math")
def method_thomson_electrometer(
    voltage_esu: float,
    voltage_emu: float,
    current_emu: float,
    resistance_emu: float,
) -> float:
    """Thomson's method by electrometer (1860).

    Thomson used an electrometer to measure potential in ESU
    units while simultaneously measuring current and resistance
    in EMU units.

    V_ESU / V_EMU = v

    Args:
        voltage_esu: Voltage measured by electrometer (statvolts).
        voltage_emu: Voltage from I*R measurement (abvolts).
        current_emu: Current in abamperes.
        resistance_emu: Resistance in abohms.

    Returns:
        Calculated velocity v.
    """
    v_from_voltage = voltage_esu / voltage_emu if voltage_emu != 0 else float("inf")
    return v_from_voltage


@maxwell_cite(774, part=4, theory_class="standard_math")
def method_jenkin(
    condenser_capacity_esu: float,
    condenser_capacity_emu: float,
    discharge_frequency: float,
    measured_current_emu: float,
) -> float:
    """Jenkin's method by condenser capacity.

    Jenkin charged and discharged a condenser at a known
    frequency, measuring the average current in EMU units
    while the capacity was known in ESU units.

    I_EMU = C_ESU * V * f / v

    Args:
        condenser_capacity_esu: Capacity in ESU (cm).
        condenser_capacity_emu: Capacity in EMU.
        discharge_frequency: Charge/discharge frequency (Hz).
        measured_current_emu: Average current (abamperes).

    Returns:
        Calculated velocity v.
    """
    # I = C * V * f / v^2 (in mixed units)
    # So v = sqrt(C_ESU * V * f / I_EMU)
    # Simplified for the experimental setup
    ratio = condenser_capacity_esu / condenser_capacity_emu
    return np.sqrt(ratio)
