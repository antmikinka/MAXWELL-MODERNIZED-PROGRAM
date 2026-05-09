"""maxwell.verification -- Equation extraction and numerical verification.

Provides systematic verification of all maxwell modules against known
analytical solutions, cross-module consistency checks, and convergence
testing.

Framework:
    VerificationResult: Immutable container for a single verification test.
    VerificationSuite: Orchestrates running all registered verification tests.
    VerificationReport: Aggregated results with HTML report generation.

Module checks:
    verify_spherical_harmonics: Spherical harmonic computation checks.
    verify_electrostatics: Electrostatic module checks.
    verify_magnetism: Magnetic module checks.
    verify_electromagnetism: Electromagnetic module checks.
    verify_vector_calculus: Vector calculus operator checks.
    verify_elliptic_integrals: Elliptic integral computation checks.
    verify_units_and_dimensions: Unit system consistency checks.
    verify_optics_and_waves: Optics and wave propagation checks.

Cross-validation:
    validate_stress_energy_consistency: Stress tensor vs energy density.
    validate_faraday_self_consistency: Faraday's law sign convention.
    validate_maxwell_equations_consistency: Maxwell equation consistency.
    validate_cgs_si_roundtrip: CGS <-> SI conversion invertibility.

Convergence:
    measure_spherical_harmonic_convergence: SH expansion convergence rate.
    measure_grid_convergence: Grid resolution convergence rate.
"""

from __future__ import annotations

# Convergence
from maxwell.verification.convergence import (
    measure_grid_convergence,
    measure_spherical_harmonic_convergence,
)

# Cross-validation
from maxwell.verification.cross_validation import (
    validate_cgs_si_roundtrip,
    validate_faraday_self_consistency,
    validate_maxwell_equations_consistency,
    validate_stress_energy_consistency,
)

# Legacy exports (kept for backward compatibility)
from maxwell.verification.equation_extractor import EquationExtractor
from maxwell.verification.equation_registry import EquationRegistry

# Framework
from maxwell.verification.framework import (
    VerificationReport,
    VerificationResult,
    VerificationSuite,
)

# Module checks
from maxwell.verification.module_checks import (
    verify_electromagnetism,
    verify_electrostatics,
    verify_elliptic_integrals,
    verify_magnetism,
    verify_optics_and_waves,
    verify_spherical_harmonics,
    verify_units_and_dimensions,
    verify_vector_calculus,
)

# SymPy symbolic verification
from maxwell.verification.sympy_verify import (
    verify_ampere_law,
    verify_biot_savart,
    verify_continuity_equation,
    verify_coulomb_law_symbolic,
    verify_div_curl,
    verify_faraday_symbolic,
    verify_grad_curl,
    verify_laplace_spherical,
    verify_lorentz_force,
    verify_maxwell_correction,
    verify_stokes_theorem,
    verify_stress_tensor_properties,
    verify_wave_equation_1d,
)
from maxwell.verification.verifier import EquationVerifier

__all__ = [
    # Framework
    "VerificationResult",
    "VerificationSuite",
    "VerificationReport",
    # Module checks
    "verify_spherical_harmonics",
    "verify_electrostatics",
    "verify_magnetism",
    "verify_electromagnetism",
    "verify_vector_calculus",
    "verify_elliptic_integrals",
    "verify_units_and_dimensions",
    "verify_optics_and_waves",
    # Cross-validation
    "validate_stress_energy_consistency",
    "validate_faraday_self_consistency",
    "validate_maxwell_equations_consistency",
    "validate_cgs_si_roundtrip",
    # Convergence
    "measure_spherical_harmonic_convergence",
    "measure_grid_convergence",
    # SymPy symbolic verification
    "verify_div_curl",
    "verify_grad_curl",
    "verify_wave_equation_1d",
    "verify_laplace_spherical",
    "verify_coulomb_law_symbolic",
    "verify_biot_savart",
    "verify_faraday_symbolic",
    "verify_continuity_equation",
    "verify_maxwell_correction",
    "verify_stokes_theorem",
    "verify_lorentz_force",
    "verify_stress_tensor_properties",
    "verify_ampere_law",
    # Legacy
    "EquationExtractor",
    "EquationRegistry",
    "EquationVerifier",
]
