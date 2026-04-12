"""maxwell.electromagnetism.theory — General equations of the electromagnetic field.

Maxwell's general equations (Arts. 594-603) — the complete mathematical
description of classical electromagnetism.

Equation (A): Faraday's Law — ∇ × E = -(1/c)·∂B/∂t
Equation (B): General EMF — E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ
Equation (C): Ponderomotive Force — F = ρE + (1/c)(J × B)
Equation (D): Magnetic Induction — B = H + 4πM
Equation (E): Ampere-Maxwell — ∇ × H = (4π/c)·J + (1/c)·∂D/∂t
Equation (F): Electric Displacement — D = εE
Equation (G): Conduction Current — J = σE
Gauss's Law (Electric): ∇ · D = 4πρ
Gauss's Law (Magnetic): ∇ · B = 0
"""

from __future__ import annotations

from maxwell.electromagnetism.theory.general_equations import (
    # Data classes
    ElectromagneticField,
    MaxwellEquations,
    GeneralEquationsCalculator,
    # Core equation functions
    calc_faradays_law,
    calc_general_emf,
    calc_ponderomotive_force,
    calc_magnetic_induction,
    calc_ampere_maxwell,
    calc_electric_displacement,
    calc_conduction_current,
    calc_gauss_law_electric,
    calc_gauss_law_magnetic,
    # Vector calculus utilities
    numerical_divergence,
    numerical_curl,
    # Verification and analysis
    verify_maxwell_equations,
    analyze_complete_field,
)

__all__ = [
    # Data classes
    "ElectromagneticField",
    "MaxwellEquations",
    "GeneralEquationsCalculator",
    # Core equation functions (A-G + Gauss)
    "calc_faradays_law",        # Equation (A)
    "calc_general_emf",         # Equation (B)
    "calc_ponderomotive_force", # Equation (C)
    "calc_magnetic_induction",  # Equation (D)
    "calc_ampere_maxwell",      # Equation (E)
    "calc_electric_displacement",  # Equation (F)
    "calc_conduction_current",  # Equation (G)
    "calc_gauss_law_electric",  # Gauss Electric
    "calc_gauss_law_magnetic",  # Gauss Magnetic
    # Vector calculus utilities
    "numerical_divergence",
    "numerical_curl",
    # Verification and analysis
    "verify_maxwell_equations",
    "analyze_complete_field",
]
