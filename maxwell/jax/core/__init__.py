"""
maxwell.jax.core — JAX-compatible implementations of core domain objects.

JAX-pytree versions of Maxwell's electrostatic and magnetic primitives,
enabling JIT compilation, automatic differentiation, and vectorized evaluation.

Implemented:
- PointChargeJAX: Coulomb's law with safe division and batched evaluation
- charge_system_field/potential: Superposition for multi-charge systems
- field_gradient: Auto-differentiation demo

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from maxwell.jax.core.charge import (
    PointChargeJAX,
    charge_system_field,
    charge_system_potential,
    field_gradient,
)

__all__ = [
    "PointChargeJAX",
    "charge_system_field",
    "charge_system_potential",
    "field_gradient",
]
