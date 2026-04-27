"""
Pure JAX wrappers for scipy.special functions used in Maxwell's Treatise.

Provides JIT-compatible implementations of:
- Associated Legendre functions (lpmv) via jax.lax recurrence
- Legendre polynomials (legendre) via recurrence relation
- Spherical harmonics (via lpmv_jax + normalization, matching scipy)
- Jacobi elliptic functions (ellipj) — delegated to _elliptic module

These wrappers bridge the scipy.special API gap in JAX, enabling the
spherical harmonics module (Arts. 128-146, 675-695) to run under jit/grad/vmap.

Category: B (user_original) — JAX compatibility layer.
"""

from __future__ import annotations

import math

import jax
import jax.numpy as jnp
from jax import lax

__all__ = [
    "lpmv_jax",
    "legendre_jax",
    "roots_legendre_jax",
    "sph_harm_y_jax",
]


# ── Associated Legendre Functions ───────────────────────────────

def lpmv_jax(m: int, n: int, x: jax.Array) -> jax.Array:
    """Associated Legendre function P_m^n(x) for |m| <= n.

    Uses the standard recurrence relation for numerical stability.
    Pure JAX implementation — fully JIT and grad compatible.

    Args:
        m: Order (can be negative).
        n: Degree (n >= 0).
        x: Argument array in [-1, 1].

    Returns:
        P_m^n(x) array, same shape as x.

    Reference:
        Part I, Arts. 128-134: Spherical harmonics theory.
        Abramowitz & Stegun 8.5.3 (recurrence).
    """
    x = jnp.asarray(x, dtype=jnp.float64)
    m_abs = abs(m)

    # For |m| > n, the function is zero
    if m_abs > n:
        return jnp.zeros_like(x)

    # Handle negative m: P_{-m}^n = (-1)^m * (n-m)!/(n+m)! * P_m^n
    sign = 1.0
    if m < 0:
        sign = (-1.0) ** m_abs
        ratio = 1.0
        for k in range(n - m_abs + 1, n + m_abs + 1):
            ratio = ratio / k
        for k in range(1, m_abs + 1):
            ratio = ratio * k

    # P_n^0(x) = P_n(x) — use the Legendre polynomial directly
    if m_abs == 0:
        return sign * legendre_jax(n, x)

    # ── Compute P_m^m(x) and P_{m+1}^m(x) ──────────────────────
    # P_m^m(x) = (-1)^m · (2m-1)!! · (1-x²)^(m/2)
    # P_{m+1}^m(x) = x · (2m+1) · P_m^m(x)
    sin_theta = jnp.sqrt(jnp.maximum(1.0 - x ** 2, 0.0))

    # (2m-1)!! for m >= 1
    double_fact = 1.0
    for k in range(1, 2 * m_abs, 2):
        double_fact *= k

    p_mm = (-1.0) ** m_abs * double_fact * sin_theta ** m_abs

    # P_{m+1}^m = x * (2m+1) * P_m^m
    if m_abs + 1 > n:
        return sign * p_mm
    p_mp1m = x * (2 * m_abs + 1) * p_mm

    if n == m_abs + 1:
        return sign * p_mp1m

    # ── Recurrence: P_{k+1}^m = ((2k+1)*x*P_k^m - (k+m)*P_{k-1}^m) / (k-m+1) ──
    # Starting from k = m+1, iterate up to k = n-1
    def recurrence_body(k: int, state: tuple) -> tuple:
        p_km1, p_k = state
        p_kp1 = ((2 * k + 1) * x * p_k - (k + m_abs) * p_km1) / (k - m_abs + 1)
        return p_k, p_kp1

    _, result = lax.fori_loop(m_abs + 1, n, recurrence_body, (p_mm, p_mp1m))
    return sign * result


def legendre_jax(n: int, x: jax.Array) -> jax.Array:
    """Legendre polynomial P_n(x) via Bonnet's recurrence.

    P_0(x) = 1
    P_1(x) = x
    (n+1)*P_{n+1}(x) = (2n+1)*x*P_n(x) - n*P_{n-1}(x)

    Pure JAX — fully JIT and grad compatible.

    Args:
        n: Degree (n >= 0).
        x: Argument array.

    Returns:
        P_n(x) array, same shape as x.

    Reference:
        Part I, Art. 128: Legendre polynomials.
    """
    x = jnp.asarray(x, dtype=jnp.float64)

    if n == 0:
        return jnp.ones_like(x)
    if n == 1:
        return x

    def step(k: int, state: tuple) -> tuple:
        p_km1, p_k = state
        p_kp1 = ((2 * k + 1) * x * p_k - k * p_km1) / (k + 1)
        return p_k, p_kp1

    _, result = lax.fori_loop(1, n, step, (jnp.ones_like(x), x))
    return result


def roots_legendre_jax(n: int) -> tuple[jax.Array, jax.Array]:
    """Gauss-Legendre quadrature nodes and weights.

    Uses the Newton-Raphson method to find roots of P_n(x).
    Pure JAX implementation for JIT compatibility.

    Args:
        n: Number of quadrature points.

    Returns:
        (nodes, weights) — arrays of length n.

    Reference:
        Part I, Arts. 128-130: Integration via spherical harmonics.
    """
    # Initial guesses using Chebyshev nodes
    k = jnp.arange(1, n + 1, dtype=jnp.float64)
    x = jnp.cos(jnp.pi * (k - 0.25) / (n + 0.5))

    def newton_step(i: int, x_nodes: jax.Array) -> jax.Array:
        p_n = legendre_jax(n, x_nodes)
        p_nm1 = legendre_jax(n - 1, x_nodes)
        dp_n = n * (x_nodes * p_n - p_nm1) / (x_nodes ** 2 - 1.0)
        return x_nodes - p_n / dp_n

    x = lax.fori_loop(0, 20, newton_step, x)

    # Weights: w_i = 2 / [(1 - x_i^2) * P_n'(x_i)^2]
    p_nm1 = legendre_jax(n - 1, x)
    weights = 2.0 / ((1.0 - x ** 2) * (n * (x * legendre_jax(n, x) - p_nm1) / (x ** 2 - 1.0)) ** 2)

    return x, weights


# ── Spherical Harmonics ─────────────────────────────────────────

def sph_harm_y_jax(m: int, n: int, phi: jax.Array, theta: jax.Array) -> jax.Array:
    """Spherical harmonic Y_n^m(theta, phi) using pure JAX.

    Computes Yₙᵐ(θ, φ) via the associated Legendre function
    ``lpmv_jax``, matching ``scipy.special.sph_harm_y`` exactly.

    For ``m >= 0``:
        Yₙᵐ = Nₙᵐ · Pₙ^{|m|}(cos θ) · e^{imφ}

    For ``m < 0``:
        Yₙ^{-|m|} = (-1)^|m| · conj(Yₙ^|m|)

    where ``Nₙᵐ = √((2n+1)/(4π) · (n-|m|)!/(n+|m|)!)``.

    This convention (no Condon-Shortley phase) matches scipy's
    ``sph_harm_y`` exactly.

    Args:
        m: Order (-n <= m <= n).
        n: Degree (n >= 0).
        phi: Azimuthal angle (radians).
        theta: Polar angle (radians, 0 at north pole).

    Returns:
        Complex spherical harmonic value, same shape as phi/theta.

    Reference:
        Part I, Arts. 135-146: Spherical harmonics theory.
    """
    phi = jnp.atleast_1d(jnp.asarray(phi, dtype=jnp.float64))
    theta = jnp.atleast_1d(jnp.asarray(theta, dtype=jnp.float64))
    shape = jnp.broadcast_shapes(phi.shape, theta.shape)
    m_abs = abs(m)

    x = jnp.broadcast_to(jnp.cos(theta), shape)
    phase = jnp.broadcast_to(jnp.exp(1.0j * m * phi), shape)

    P_lm = lpmv_jax(m_abs, n, x)

    # Normalization: sqrt((2n+1)/(4pi) * (n-m)!/(n+m)!)
    norm_val = math.sqrt(
        (2 * n + 1) / (4.0 * math.pi)
        * math.factorial(n - m_abs)
        / math.factorial(n + m_abs)
    )

    result = norm_val * P_lm * phase

    # Negative m: Y_{n,-|m|} = (-1)^{|m|} * conj(Y_{n,|m|})
    # scipy does NOT include Condon-Shortley phase for m >= 0
    if m < 0:
        result = ((-1.0) ** m_abs) * jnp.conj(result)

    return result.squeeze()
