"""
maxwell.jax.electromagnetism — JAX-compatible Maxwell electromagnetism.

JAX-pytree versions of Maxwell's electromagnetic computations,
enabling JIT compilation, automatic differentiation, and vectorized evaluation.

Implemented:
- FaradayInductionJAX: Faraday's law with safe operations and pytree support
- analyze_faraday_induction_jax: Complete multi-turn coil induction analysis
- ElectromagneticFieldJAX: Complete EM field state (E, B, H, D, J, rho)
- MaxwellEquationsJAX: Gauss's laws, Faraday's law, Ampere-Maxwell law
- verify_maxwell_equations_jax: Numerical verification suite
- LorentzForceJAX, MaxwellStressTensorJAX: EM forces and stress
- DisplacementCurrentJAX, AmpereMaxwellLawJAX: Displacement current, Ampere-Maxwell
- ElectricFieldJAX: Electric field definition, flux, Gauss's law, EMF

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from maxwell.jax.electromagnetism.ampere_maxwell import (
    AmpereMaxwellLawJAX,
    DisplacementCurrentJAX,
    capacitor_paradox_jax,
    curl_H_jax,
    displacement_current_jax,
    magnetic_field_from_current_jax,
    total_current_jax,
)
from maxwell.jax.electromagnetism.equations import (
    ElectromagneticFieldJAX,
    MaxwellEquationsJAX,
    verify_maxwell_equations_jax,
)
from maxwell.jax.electromagnetism.field import (
    ElectricFieldJAX,
    electric_flux_jax,
    electric_tension_jax,
    electromotive_force_jax,
    field_from_potential_jax,
    gauss_law_closed_surface_jax,
    superposition_field_jax,
)
from maxwell.jax.electromagnetism.forces import (
    LorentzForceJAX,
    MaxwellStressTensorJAX,
)
from maxwell.jax.electromagnetism.induction import (
    FaradayInductionJAX,
    analyze_faraday_induction_jax,
)

__all__ = [
    # Ampere-Maxwell
    "AmpereMaxwellLawJAX",
    "DisplacementCurrentJAX",
    "capacitor_paradox_jax",
    "curl_H_jax",
    "displacement_current_jax",
    "magnetic_field_from_current_jax",
    "total_current_jax",
    # Maxwell equations
    "ElectromagneticFieldJAX",
    "MaxwellEquationsJAX",
    "verify_maxwell_equations_jax",
    # Electric field
    "ElectricFieldJAX",
    "electric_flux_jax",
    "electric_tension_jax",
    "electromotive_force_jax",
    "field_from_potential_jax",
    "gauss_law_closed_surface_jax",
    "superposition_field_jax",
    # Forces
    "LorentzForceJAX",
    "MaxwellStressTensorJAX",
    # Faraday
    "FaradayInductionJAX",
    "analyze_faraday_induction_jax",
]
