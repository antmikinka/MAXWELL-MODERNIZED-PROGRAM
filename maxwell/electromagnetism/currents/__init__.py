"""maxwell.electromagnetism.currents — Current equations (Arts. 610-611).

Package for Maxwell's current equations including total current and
the EMF-current relation.
"""

from maxwell.electromagnetism.currents.total import (
    TotalCurrent,
    calc_total_current_density,
    calc_displacement_current_from_dEdt,
    calc_total_current_through_surface,
    calc_curl_H_from_total_current,
    verify_continuity_with_total_current,
    verify_capacitor_total_current,
    analyze_total_current,
)

from maxwell.electromagnetism.currents.emf_relation import (
    EMFCurrentRelation,
    calc_emf_current_relation,
    calc_resistive_drop,
    calc_inductive_emf,
    calc_rl_circuit_current,
    calc_line_integral_E,
    verify_emf_current_relation,
    analyze_emf_current,
)

__all__ = [
    # Total current (Art. 610)
    "TotalCurrent",
    "calc_total_current_density",
    "calc_displacement_current_from_dEdt",
    "calc_total_current_through_surface",
    "calc_curl_H_from_total_current",
    "verify_continuity_with_total_current",
    "verify_capacitor_total_current",
    "analyze_total_current",
    # EMF-Current relation (Art. 611)
    "EMFCurrentRelation",
    "calc_emf_current_relation",
    "calc_resistive_drop",
    "calc_inductive_emf",
    "calc_rl_circuit_current",
    "calc_line_integral_E",
    "verify_emf_current_relation",
    "analyze_emf_current",
]
