"""maxwell.dynamics -- Lagrangian and Hamiltonian dynamics kernel.

Provides energy-based force derivation using JAX auto-differentiation,
implementing Maxwell's variational approach to mechanics (Layer 52).

Submodules:
    lagrangian -- Lagrangian formulation with JAX auto-diff
"""

from __future__ import annotations

__all__ = [
    "GeneralizedSystem",
]

from maxwell.dynamics.lagrangian import GeneralizedSystem
