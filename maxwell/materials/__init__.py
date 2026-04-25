"""
maxwell.materials — Induced magnetization, saturation, and hysteresis.

This subpackage implements the magnetic properties of materials:
- Induced magnetization I = κH (induction.py, Arts. 424-426)
- Magnetic saturation and Weber model (saturation.py, Arts. 442-443)
- Hysteresis phenomena and energy loss (hysteresis.py, Arts. 444-446)

Category: A (maxwell_original) — Maxwell's theory of magnetic materials.
"""

from __future__ import annotations

from maxwell.materials.induction import (
    SubstanceInduction,
    MagneticSusceptibility,
    InducedMagnetization,
    calc_induced_magnetization,
    calc_B_in_material,
    determine_susceptibility,
    force_on_induced_magnet,
    typical_susceptibility_values,
)

from maxwell.materials.saturation import (
    WeberModel,
    observe_saturation,
    fit_weber_model,
    approach_to_saturation,
    molecular_alignment_fraction,
)

from maxwell.materials.hysteresis import (
    HysteresisLoop,
    WeberModelWithHysteresis,
    explain_hysteresis_phenomena,
    analyze_hysteresis_loop,
    hysteresis_loss_steinmetz,
    generate_theoretical_hysteresis_loop,
    typical_hysteresis_parameters,
)

__all__ = [
    # Induced Magnetization (Arts. 424-426)
    "SubstanceInduction",
    "MagneticSusceptibility",
    "InducedMagnetization",
    "calc_induced_magnetization",
    "calc_B_in_material",
    "determine_susceptibility",
    "force_on_induced_magnet",
    "typical_susceptibility_values",
    # Magnetic Saturation (Arts. 442-443)
    "WeberModel",
    "observe_saturation",
    "fit_weber_model",
    "approach_to_saturation",
    "molecular_alignment_fraction",
    # Magnetic Hysteresis (Arts. 444-446)
    "HysteresisLoop",
    "WeberModelWithHysteresis",
    "explain_hysteresis_phenomena",
    "analyze_hysteresis_loop",
    "hysteresis_loss_steinmetz",
    "generate_theoretical_hysteresis_loop",
    "typical_hysteresis_parameters",
]
