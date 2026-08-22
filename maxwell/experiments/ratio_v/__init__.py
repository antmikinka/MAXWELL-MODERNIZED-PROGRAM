"""maxwell.experiments.ratio_v — Ratio of ESU to EMU units (Arts. 768-780).

Experimental determination that the ratio of electrostatic to
electromagnetic units is a velocity equal (within experimental error) to
the speed of light.  Numeric-value convention (Treatise Arts. 768-770):
for one and the same physical quantity with readings n_esu, n_emu,

    n_esu / n_emu = v**p

with p = +1 (charge, current), -1 (potential), +2 (capacitance),
-2 (resistance, inductance); see ``theory.UNIT_RATIO_POWERS`` and the
``theory`` module docstring for the dimensional bookkeeping.
"""

from __future__ import annotations

from maxwell.experiments.ratio_v.combined import (
    apply_rapid_action_correction,
    combine_coil_condenser,
    compare_capacity_inductance,
    method_condenser_wippe,
    method_intermittent_current,
    method_maxwell_combined,
    rapid_action_charge_fraction,
)
from maxwell.experiments.ratio_v.condensers import (
    CondenserMeasurement,
    capacity_parallel,
    capacity_series,
    convert_capacity,
    method_jenkin,
    method_thomson_electrometer,
    method_weber_kohlrausch,
    sphere_capacity_esu,
)
from maxwell.experiments.ratio_v.theory import (
    UNIT_RATIO_POWERS,
    V_HISTORICAL,
    V_HISTORICAL_TOL,
    UnitRatioExperiment,
    calc_convection_current,
    compare_resistance_systems,
    derive_unit_ratio_dimension,
    historical_v_anchor,
    motivate_ratio_investigation,
    prove_ratio_is_velocity,
    v_from_convection_field,
)

__all__ = [
    # Theory (Arts. 768-770, 780)
    "UNIT_RATIO_POWERS",
    "V_HISTORICAL",
    "V_HISTORICAL_TOL",
    "UnitRatioExperiment",
    "motivate_ratio_investigation",
    "derive_unit_ratio_dimension",
    "prove_ratio_is_velocity",
    "historical_v_anchor",
    "calc_convection_current",
    "v_from_convection_field",
    "compare_resistance_systems",
    # Condenser methods (Arts. 771-774)
    "CondenserMeasurement",
    "sphere_capacity_esu",
    "method_weber_kohlrausch",
    "method_thomson_electrometer",
    "method_jenkin",
    "convert_capacity",
    "capacity_parallel",
    "capacity_series",
    # Combined methods (Arts. 773, 775-779)
    "method_maxwell_combined",
    "method_intermittent_current",
    "method_condenser_wippe",
    "rapid_action_charge_fraction",
    "apply_rapid_action_correction",
    "compare_capacity_inductance",
    "combine_coil_condenser",
]
