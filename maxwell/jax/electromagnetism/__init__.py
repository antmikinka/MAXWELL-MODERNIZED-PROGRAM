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

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from maxwell.jax.electromagnetism.equations import (
    ElectromagneticFieldJAX,
    MaxwellEquationsJAX,
    verify_maxwell_equations_jax,
)
from maxwell.jax.electromagnetism.induction import (
    FaradayInductionJAX,
    analyze_faraday_induction_jax,
)

__all__ = [
    "ElectromagneticFieldJAX",
    "FaradayInductionJAX",
    "MaxwellEquationsJAX",
    "analyze_faraday_induction_jax",
    "verify_maxwell_equations_jax",
]
