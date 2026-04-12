"""
Faraday Induction — Electromagnetic Induction Module.

Implements Faraday's law of electromagnetic induction (Arts. 528-531)
and Lenz's law (Art. 542) from Maxwell's Treatise.

Exports:
    - FaradayInduction: Main class for induction calculations
    - MagneticFlux: Magnetic flux dataclass
    - InducedEMF: Induced EMF dataclass
    - calc_magnetic_flux: Calculate Φ = B · A
    - calc_induced_emf: Calculate EMF = -dΦ/dt
    - calc_motional_emf: Calculate EMF from motion
    - calc_self_induction: Calculate EMF = -L·dI/dt
    - calc_flux_through_loop: Calculate flux through circular loop
    - verify_lenz_law: Verify Lenz's law direction
    - analyze_faraday_induction: Complete induction analysis
    - flux_change_for_emf: Required flux change for target EMF
    - verify_faradays_law: Numerical verification of Faraday's law

References:
    Part IV, Arts. 528-531: Faraday's law of induction.
    Part IV, Art. 542: Lenz's law.
"""

from maxwell.electromagnetism.induction.faraday import (
    FaradayInduction,
    MagneticFlux,
    InducedEMF,
    calc_magnetic_flux,
    calc_induced_emf,
    calc_motional_emf,
    calc_self_induction,
    calc_flux_through_loop,
    verify_lenz_law,
    analyze_faraday_induction,
    flux_change_for_emf,
    verify_faradays_law,
)

__all__ = [
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
]
