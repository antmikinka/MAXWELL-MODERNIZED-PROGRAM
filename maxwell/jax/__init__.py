"""
maxwell.jax — JAX adapter for GPU/TPU acceleration and auto-differentiation.

Provides JAX-compatible implementations of Maxwell's 1873 Treatise computations,
enabling JIT compilation, automatic differentiation, and vectorized evaluation
across thousands of field points simultaneously.

Package Structure
-----------------
_core        : JAX compatibility utilities (pytree registration, safe ops)
_scipy_special: Pure JAX wrappers for scipy.special functions (lpmv, legendre, ellipj)
_elliptic    : AGM-based elliptic integrals (pure JAX, no scipy dependency)
core         : JAX-compatible domain classes (PointChargeJAX, etc.)

Usage
-----
>>> import jax
>>> from maxwell.jax.core.charge import PointChargeJAX
>>>
>>> charge = PointChargeJAX(q=1.0, position=jax.numpy.array([0.0, 0.0, 0.0]))
>>> E = charge.field_at(jax.numpy.array([[5.0, 0.0, 0.0], [0.0, 5.0, 0.0]]))
>>> # E.shape = (2, 3) — batched evaluation via jax.vmap
"""

from __future__ import annotations

import jax

# Enable float64 for CGS precision — Maxwell's unit ratios require ~15 digits
jax.config.update("jax_enable_x64", True)

__all__ = [
    "enable_x64",
    "disable_x64",
    # Subpackages
    "core",
    # Compatibility utilities
    "_compat",
    # Pure JAX special functions
    "_scipy_special",
    # Pure JAX elliptic integrals
    "_elliptic",
]


def enable_x64() -> None:
    """Enable 64-bit floats for CGS-EMU precision. Call before any JAX computation."""
    jax.config.update("jax_enable_x64", True)


def disable_x64() -> None:
    """Disable 64-bit floats (use for GPU memory-constrained scenarios)."""
    jax.config.update("jax_enable_x64", False)
