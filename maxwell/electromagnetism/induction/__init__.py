"""
Faraday Induction — Electromagnetic Induction Module.

Implements Faraday's law of electromagnetic induction (Arts. 528-531),
Lenz's law (Art. 542), self-induction (Arts. 546-551), and generalized
EMF (Arts. 576-577) from Maxwell's Treatise.

References:
    Part IV, Arts. 528-531: Faraday's law of induction.
    Part IV, Art. 542: Lenz's law.
    Part IV, Arts. 546-551: Self-induction.
    Part IV, Arts. 576-577: Generalized EMF.
"""

from maxwell.electromagnetism.induction.faraday import (
    FaradayInduction,
    InducedEMF,
    MagneticFlux,
    analyze_faraday_induction,
    calc_flux_through_loop,
    calc_induced_emf,
    calc_magnetic_flux,
    calc_motional_emf,
    calc_self_induction,
    flux_change_for_emf,
    verify_faradays_law,
    verify_lenz_law,
)
from maxwell.electromagnetism.induction.generalized import (
    GeneralizedEMF,
    analyze_generalized_emf,
    calc_generalized_emf,
    calc_motional_emf_general,
    calc_rotating_loop_emf,
    calc_sliding_conductor_emf,
    verify_generalized_emf,
)
from maxwell.electromagnetism.induction.lenz import (
    LenzLawCalculator,
    analyze_lenz_law,
    calc_induced_current,
    calc_induced_emf,
    calc_motional_emf_lenz,
    calc_rotating_coil_emf,
    verify_lenz_law_direction,
)
from maxwell.electromagnetism.induction.self import (
    SelfInductance,
    analyze_self_induction,
    calc_inductor_energy,
    calc_loop_inductance,
    calc_rl_current_decay,
    calc_rl_current_rise,
    calc_self_induced_emf,
    calc_solenoid_inductance,
    verify_self_induction,
)

__all__ = [
    # Faraday (Arts. 528-531)
    "FaradayInduction",
    "MagneticFlux",
    "InducedEMF",
    "calc_magnetic_flux",
    "calc_induced_emf",
    "calc_motional_emf",
    "calc_self_induction",
    "calc_flux_through_loop",
    "verify_lenz_law",
    "analyze_faraday_induction",
    "flux_change_for_emf",
    "verify_faradays_law",
    # Lenz (Art. 542)
    "LenzLawCalculator",
    "calc_induced_current",
    "calc_motional_emf_lenz",
    "calc_rotating_coil_emf",
    "verify_lenz_law_direction",
    "analyze_lenz_law",
    # Self-induction (Arts. 546-551)
    "SelfInductance",
    "calc_solenoid_inductance",
    "calc_loop_inductance",
    "calc_self_induced_emf",
    "calc_inductor_energy",
    "calc_rl_current_rise",
    "calc_rl_current_decay",
    "verify_self_induction",
    "analyze_self_induction",
    # Generalized EMF (Arts. 576-577)
    "GeneralizedEMF",
    "calc_generalized_emf",
    "calc_motional_emf_general",
    "calc_rotating_loop_emf",
    "calc_sliding_conductor_emf",
    "verify_generalized_emf",
    "analyze_generalized_emf",
]
