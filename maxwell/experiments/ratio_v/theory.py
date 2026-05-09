"""maxwell.experiments.ratio_v.theory — Unit ratio theory (Arts. 768-770, 780).

Theoretical foundation: the ratio of electrostatic to
electromagnetic units is a velocity, experimentally
determined to equal the speed of light.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi

# Speed of light in CGS (cm/s)
C_CGS = 2.99792458e10


@maxwell_cite(768, part=4, theory_class="maxwell_original")
def motivate_ratio_investigation() -> dict[str, str]:
    """State the nature and importance of the ratio investigation.

    Art. 768: The ratio between electrostatic and electromagnetic
    units is one of the most important investigations in physics,
    as it connects the two systems of electrical measurement and
    reveals the fundamental nature of electricity.

    Returns:
        Motivation dictionary.
    """
    return {
        "significance": "The ratio v between ESU and EMU units is "
        "found to be a velocity of the same order as "
        "the speed of light",
        "implication": "This suggests that light itself may be an "
        "electromagnetic phenomenon",
        "method": "Compare the same physical quantity (charge, "
        "current, resistance) measured in both systems",
        "expected_result": "v = c = 2.998 x 10^10 cm/s",
    }


@maxwell_cite(769, part=4, theory_class="maxwell_original")
def prove_ratio_is_velocity() -> float:
    """Prove that the ratio of units is a velocity.

    Art. 769: Dimensional analysis shows that the ratio of
    the ESU unit to the EMU unit of any electrical quantity
    has dimensions of velocity:

    [ESU charge] / [EMU charge] = [L T^{-1}] = velocity

    Returns:
        Theoretical ratio (speed of light in CGS).
    """
    # Dimensional analysis:
    # ESU: [q] = M^{1/2} L^{3/2} T^{-1}
    # EMU: [q] = M^{1/2} L^{1/2}
    # Ratio: L/T = velocity
    return C_CGS


@maxwell_cite(770, part=4, theory_class="standard_math")
def calc_convection_current(
    charge: float,
    velocity: float,
) -> float:
    """Calculate current produced by a moving charge (convection current).

    Art. 770: A moving charged body constitutes an electric
    current. This convection current produces a magnetic field
    proportional to the charge and its velocity.

    In ESU: current_ESU = q_ESU / t
    In EMU: current_EMU = q_EMU / t

    The magnetic field of the convection current provides
    a way to measure the ratio v.

    Args:
        charge: Electric charge (ESU units).
        velocity: Velocity of the charge (cm/s).

    Returns:
        Convection current in EMU (abamperes).
    """
    # I_EMU = q_ESU * v / c (since 1 ESU of charge = c EMU)
    return charge * velocity / C_CGS


@maxwell_cite(780, part=4, theory_class="standard_math")
def compare_resistance_systems(
    resistance_esu: float,
    resistance_emu: float,
) -> dict[str, float]:
    """Compare ESU and EMU resistance values.

    Art. 780: The resistance of the same conductor measured
    in ESU vs EMU units differs by a factor of v^2:

    R_ESU / R_EMU = v^2 = c^2

    Args:
        resistance_esu: Resistance in ESU (statohms).
        resistance_emu: Resistance in EMU (abohms).

    Returns:
        Ratio and velocity calculation.
    """
    ratio = resistance_esu / resistance_emu if resistance_emu != 0 else float("inf")
    calculated_v = np.sqrt(ratio)

    return {
        "resistance_esu": resistance_esu,
        "resistance_emu": resistance_emu,
        "ratio_esu_emu": ratio,
        "calculated_v": calculated_v,
        "speed_of_light": C_CGS,
        "deviation_pct": abs(calculated_v - C_CGS) / C_CGS * 100,
    }


@dataclass
class UnitRatioExperiment:
    """Framework for measuring the ESU/EMU ratio.

    Base class for all experimental methods (Weber-Kohlrausch,
    Thomson, Maxwell's combined method, etc.).
    """

    measured_quantity_esu: float
    measured_quantity_emu: float
    quantity_name: str

    @maxwell_cite(769, part=4, theory_class="standard_math")
    def calculate_ratio(self) -> float:
        """Calculate the ratio v = ESU/EMU."""
        if self.measured_quantity_emu == 0:
            return float("inf")
        return abs(self.measured_quantity_esu / self.measured_quantity_emu)

    @maxwell_cite(769, part=4, theory_class="standard_math")
    def verify_equals_c(self, tolerance: float = 0.05) -> bool:
        """Verify that the ratio equals the speed of light.

        Args:
            tolerance: Acceptable fractional deviation (default 5%).

        Returns:
            True if ratio is within tolerance of c.
        """
        v = self.calculate_ratio()
        return abs(v - C_CGS) / C_CGS < tolerance
