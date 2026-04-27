"""
maxwell.jax.core — JAX-compatible implementations of core domain objects.

JAX-pytree versions of Maxwell's electrostatic and magnetic primitives,
enabling JIT compilation, automatic differentiation, and vectorized evaluation.

Implemented:
- PointChargeJAX: Coulomb's law with safe division and batched evaluation
- charge_system_field/potential: Superposition for multi-charge systems
- field_gradient: Auto-differentiation demo
- MagneticPoleJAX: Magnetic pole field calculation (Art. 371)
- MagnetJAX: Permanent magnet with force/torque/energy (Arts. 372-376)
- pole_force_jax: Coulomb's law for magnetic poles (Art. 376)
- mutual_action_jax: Mutual action between two magnets (Art. 392)
- torque_on_magnet_jax: Torque on magnet in uniform field (Art. 373)

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from maxwell.jax.core.charge import (
    PointChargeJAX,
    charge_system_field,
    charge_system_potential,
    field_gradient,
)
from maxwell.jax.core.magnet import (
    MagneticPoleJAX,
    MagnetJAX,
    pole_force_jax,
    mutual_action_jax,
    torque_on_magnet_jax,
    pole_force_gradient,
)

__all__ = [
    "PointChargeJAX",
    "charge_system_field",
    "charge_system_potential",
    "field_gradient",
    "MagneticPoleJAX",
    "MagnetJAX",
    "pole_force_jax",
    "mutual_action_jax",
    "torque_on_magnet_jax",
    "pole_force_gradient",
]
