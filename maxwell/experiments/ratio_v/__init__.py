"""maxwell.experiments.ratio_v — Ratio of ESU to EMU units (Arts. 768-780).

Experimental determination that the ratio of electrostatic to
electromagnetic units equals the speed of light.
"""

from __future__ import annotations

from maxwell.experiments.ratio_v.combined import (
    apply_rapid_action_correction,
    combine_coil_condenser,
    compare_capacity_inductance,
    method_condenser_wippe,
    method_intermittent_current,
    method_maxwell_combined,
)
from maxwell.experiments.ratio_v.condensers import (
    CondenserMeasurement,
    method_jenkin,
    method_thomson_electrometer,
    method_weber_kohlrausch,
)
from maxwell.experiments.ratio_v.theory import (
    UnitRatioExperiment,
    calc_convection_current,
    compare_resistance_systems,
    motivate_ratio_investigation,
    prove_ratio_is_velocity,
)

__all__ = [
    # Theory (Arts. 768-770, 780)
    "UnitRatioExperiment",
    "motivate_ratio_investigation",
    "prove_ratio_is_velocity",
    "calc_convection_current",
    "compare_resistance_systems",
    # Condenser methods (Arts. 771-774)
    "CondenserMeasurement",
    "method_weber_kohlrausch",
    "method_thomson_electrometer",
    "method_jenkin",
    # Combined methods (Arts. 775-779)
    "method_maxwell_combined",
    "method_intermittent_current",
    "method_condenser_wippe",
    "apply_rapid_action_correction",
    "compare_capacity_inductance",
    "combine_coil_condenser",
]
