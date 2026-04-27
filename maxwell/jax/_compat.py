"""
JAX compatibility utilities for the Maxwell Modernized codebase.

Provides:
- Pytree registration decorator for dataclass JAX compatibility
- Safe arithmetic operations (division, sqrt, log) with gradient handling
- Array creation helpers that dispatch to jnp when available
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Callable, Type, TypeVar
import jax
import jax.numpy as jnp
from jax.tree_util import register_pytree_node, register_pytree_node_class

T = TypeVar("T")

__all__ = [
    "jax_tree",
    "safe_div",
    "safe_sqrt",
    "safe_log",
    "safe_norm",
    "jnp",
]


# ── Pytree Registration ─────────────────────────────────────────

def jax_tree(cls: Type[T]) -> Type[T]:
    """Class decorator that registers a dataclass as a JAX pytree node.

    All dataclass fields become tree leaves (JAX-traced). Use this on any
    dataclass that should work with jax.jit, jax.grad, jax.vmap.

    Example:
        @jax_tree
        @dataclass
        class PointChargeJAX:
            q: float
            position: jax.Array
    """
    if not hasattr(cls, "__dataclass_fields__"):
        raise TypeError(f"@jax_tree requires a dataclass, got {cls.__name__}")

    field_names = tuple(f.name for f in fields(cls))

    def flatten(tree: Any) -> tuple[tuple, Any]:
        return tuple(getattr(tree, name) for name in field_names), field_names

    def unflatten(aux_data: tuple, children: tuple) -> Any:
        return cls(**dict(zip(aux_data, children)))

    register_pytree_node(cls, flatten, unflatten)
    return cls


# ── Safe Arithmetic ─────────────────────────────────────────────

def safe_div(
    numerator: jax.Array,
    denominator: jax.Array,
    safe_default: float = 0.0,
) -> jax.Array:
    """Division that returns safe_default when denominator is zero.

    Uses jnp.where for JIT traceability — no Python control flow.
    Gradient through the safe branch is zero.

    Args:
        numerator: Numerator array.
        denominator: Denominator array (same shape or broadcastable).
        safe_default: Value to return where denominator == 0.

    Returns:
        numerator / denominator where denominator != 0, else safe_default.
    """
    safe_denom = jnp.where(denominator == 0, 1.0, denominator)
    result = numerator / safe_denom
    return jnp.where(denominator == 0, safe_default, result)


def safe_sqrt(x: jax.Array, safe_default: float = 0.0) -> jax.Array:
    """Square root that returns safe_default for negative inputs.

    Args:
        x: Input array.
        safe_default: Value to return where x < 0.

    Returns:
        sqrt(x) where x >= 0, else safe_default.
    """
    return jnp.where(x < 0, safe_default, jnp.sqrt(jnp.maximum(x, 0.0)))


def safe_log(x: jax.Array, safe_default: float = 0.0) -> jax.Array:
    """Natural log that returns safe_default for non-positive inputs.

    Args:
        x: Input array.
        safe_default: Value to return where x <= 0.

    Returns:
        log(x) where x > 0, else safe_default.
    """
    safe_x = jnp.where(x <= 0, 1.0, x)
    return jnp.where(x <= 0, safe_default, jnp.log(safe_x))


def safe_norm(
    x: jax.Array,
    axis: int = -1,
    safe_default: float = 0.0,
) -> jax.Array:
    """L2 norm along an axis, safe against zero vectors.

    Uses the sqrt(sum(x^2)) formulation with a floor to avoid NaN gradients.

    Args:
        x: Input array.
        axis: Axis along which to compute the norm.
        safe_default: Minimum norm value (prevents division by zero downstream).

    Returns:
        L2 norm along axis, guaranteed >= safe_default.
    """
    sq_sum = jnp.sum(x ** 2, axis=axis)
    return jnp.sqrt(jnp.maximum(sq_sum, safe_default ** 2))
