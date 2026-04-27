"""
maxwell.jax.math — JAX-compatible spherical harmonics math.

Exports the JAX pytree expansion class, batched Legendre polynomial
evaluation, and the pure-JAX addition theorem utility.

Usage::

    >>> from maxwell.jax.math import (
    ...     SphericalHarmonicExpansionJAX,
    ...     legendre_batched,
    ...     addition_theorem_jax,
    ... )
    >>> expansion = SphericalHarmonicExpansionJAX(max_l=10)
    >>> theta = jnp.linspace(0, jnp.pi, 200)
    >>> expansion.compute_coefficients(lambda th: jnp.cos(th), theta)
    >>> recon = expansion.reconstruct(theta, 0.0)
"""

from __future__ import annotations

from maxwell.jax.math.spherical_harmonics import (
    SphericalHarmonicExpansionJAX,
    addition_theorem_jax,
    legendre_batched,
)

__all__ = [
    "SphericalHarmonicExpansionJAX",
    "legendre_batched",
    "addition_theorem_jax",
]
