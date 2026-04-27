"""
maxwell.jax.math — Spherical harmonics and special-function math for JAX.

Provides JAX-compatible versions of Maxwell's Treatise spherical-harmonic
expansions (Part I, Arts. 128-146; Part IV, Arts. 675-695), enabling
JIT compilation, automatic differentiation, and batched evaluation
over thousands of angular grid points simultaneously.

Implemented:
- SphericalHarmonicExpansionJAX : axisymmetric expansion on theta grids
- legendre_batched              : Bonnet recurrence via jax.lax.fori_loop
- addition_theorem_jax          : pure-JAX addition theorem using sph_harm_y_jax

Category: B (user_original) — JAX adapter layer.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jax import lax

from maxwell.jax._compat import jax_tree
from maxwell.jax._scipy_special import sph_harm_y_jax
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "SphericalHarmonicExpansionJAX",
    "legendre_batched",
    "addition_theorem_jax",
]


# =============================================================================
# LEGENDRE POLYNOMIALS
# =============================================================================


@maxwell_cite(
    128, 129, 130,
    part=1, chapter="Spherical Harmonics",
    theory_class="standard_math",
    description="Batched Legendre polynomial evaluation via Bonnet recurrence (JAX)",
)
def legendre_batched(n: int, x: jax.Array) -> jax.Array:
    """Batched Legendre polynomial evaluation via Bonnet's recurrence.

    Computes Pₙ(x) for a vector of x-values simultaneously.
    Uses ``jax.lax.fori_loop`` so the recurrence is JIT-traceable.

    Recurrence (Bonnet's formula):
        P₀(x) = 1
        P₁(x) = x
        (k+1)·Pₖ₊₁(x) = (2k+1)·x·Pₖ(x) − k·Pₖ₋₁(x)

    Args:
        n: Degree (non-negative integer).
        x: Array of arguments in [-1, 1], any shape.

    Returns:
        Pₙ(x) array, same shape as *x*.
    """
    x = jnp.asarray(x, dtype=jnp.float64)

    # Base cases: P₀ = 1, P₁ = x, then iterate via fori_loop.
    # Uses lax.cond for n==0 to stay JIT-traceable when n is an
    # abstract integer (e.g. inside a jitted function).
    result = lax.cond(
        n == 0,
        lambda _: jnp.ones_like(x),
        lambda _: lax.cond(
            n == 1,
            lambda _: x,
            lambda _: _legendre_fori(n, x),
            None,
        ),
        None,
    )
    return result


def _legendre_fori(n: int, x: jax.Array) -> jax.Array:
    """Internal helper: Bonnet recurrence for n >= 2."""

    def step(k: int, state: tuple) -> tuple:
        p_km1, p_k = state
        p_kp1 = ((2 * k + 1) * x * p_k - k * p_km1) / (k + 1)
        return (p_k, p_kp1)

    _, result = lax.fori_loop(1, n, step, (jnp.ones_like(x), x))
    return result


# =============================================================================
# ADDITION THEOREM
# =============================================================================


@maxwell_cite(
    134, 135,
    part=1, chapter="Spherical Harmonics",
    theory_class="standard_math",
    description="Spherical-harmonic addition theorem (pure JAX)",
)
def addition_theorem_jax(
    l: int,
    theta1: jax.Array,
    phi1: jax.Array,
    theta2: jax.Array,
    phi2: jax.Array,
) -> jax.Array:
    """Spherical-harmonic addition theorem (pure JAX).

    Computes
        Pₗ(cos γ) = (4π / (2l+1)) · Σₘ Yₗₘ(θ₁,φ₁) · Yₗₘ*(θ₂,φ₂)

    where γ is the angle between two directions on the unit sphere:
        cos γ = cos θ₁ cos θ₂ + sin θ₁ sin θ₂ cos(φ₁ − φ₂)

    The function also returns the direct Legendre evaluation for
    verification purposes (the two should agree to machine precision).

    Args:
        l: Degree (non-negative integer).
        theta1: Polar angle of first direction (radians).
        phi1: Azimuthal angle of first direction (radians).
        theta2: Polar angle of second direction (radians).
        phi2: Azimuthal angle of second direction (radians).

    Returns:
        Tuple ``(P_l_addition, P_l_direct)`` — both real-valued,
        same broadcast shape as the inputs.
    """
    theta1 = jnp.asarray(theta1, dtype=jnp.float64)
    phi1 = jnp.asarray(phi1, dtype=jnp.float64)
    theta2 = jnp.asarray(theta2, dtype=jnp.float64)
    phi2 = jnp.asarray(phi2, dtype=jnp.float64)

    # Cosine of angle between directions
    cos_gamma = (
        jnp.cos(theta1) * jnp.cos(theta2)
        + jnp.sin(theta1) * jnp.sin(theta2) * jnp.cos(phi1 - phi2)
    )
    cos_gamma = jnp.clip(cos_gamma, -1.0, 1.0)

    # Direct Legendre evaluation
    P_l_direct = legendre_batched(l, cos_gamma)

    # Sum over m via spherical harmonics
    m_sum = jnp.sum(
        jnp.stack([
            sph_harm_y_jax(m, l, phi1, theta1)
            * jnp.conj(sph_harm_y_jax(m, l, phi2, theta2))
            for m in range(-l, l + 1)
        ]),
        axis=0,
    )

    P_l_addition = (4.0 * jnp.pi / (2 * l + 1)) * m_sum.real

    return P_l_addition, P_l_direct


# =============================================================================
# SPHERICAL HARMONIC EXPANSION (JAX PYTREE)
# =============================================================================


@jax_tree
@dataclass
class SphericalHarmonicExpansionJAX:
    """Axisymmetric spherical-harmonic expansion (JAX-compatible pytree).

    Expands a function *f(θ)* defined on the sphere in terms of zonal
    (m = 0) spherical harmonics:

        f(θ) ≈ Σₗ₌₀ᴸ  aₗ · Yₗ⁰(θ, φ)

    where the coefficients are obtained by quadrature:

        aₗ = ∫₀ᵖⁱ f(θ) · Yₗ⁰(θ) · sin θ · dθ · (2π)

    The class stores the full complex coefficient matrix
    ``coefficients[l, m + max_l]`` so that the same object can also
    represent non-axisymmetric expansions if desired.

    Attributes:
        max_l: Maximum harmonic degree.
        coefficients: Complex array of shape ``(max_l + 1, 2·max_l + 1)``
            with entry ``(l, m)`` accessible via index
            ``coefficients[l, m + max_l]``.

    Example::

        >>> expansion = SphericalHarmonicExpansionJAX(max_l=8)
        >>> theta_grid = jnp.linspace(0, jnp.pi, 200)
        >>> coeffs = expansion.compute_coefficients(
        ...     lambda th: jnp.cos(th) ** 2, theta_grid
        ... )
        >>> recon = expansion.reconstruct(theta_grid, 0.0)

    References:
        Part I, Arts. 139-142: Spherical harmonic expansion theory.
    """

    max_l: int = 0
    coefficients: jax.Array | None = None

    def __post_init__(self):
        if self.coefficients is None:
            self.coefficients = jnp.zeros(
                (self.max_l + 1, 2 * self.max_l + 1), dtype=jnp.complex128
            )

    # ── Coefficient computation ─────────────────────────────────

    def compute_coefficients(
        self,
        f_theta: callable,
        theta_grid: jax.Array,
    ) -> jax.Array:
        """Compute zonal expansion coefficients by numerical quadrature.

        For each ``(l, m)`` with ``|m| ≤ l ≤ max_l``:

            aₗₘ = ∫∫ f(θ) Yₗₘ*(θ, φ) sin θ dθ dφ

        For an axisymmetric input *f(θ)* the φ-integral evaluates to
        ``2π`` and only the ``m = 0`` column is non-zero.

        Args:
            f_theta: Callable ``f(theta)`` returning function values
                on the grid.  Must accept and return a 1-D float64 array.
            theta_grid: 1-D array of polar angles in ``[0, π]``.

        Returns:
            Coefficient array of shape ``(max_l + 1, 2·max_l + 1)``.
        """
        theta_grid = jnp.asarray(theta_grid, dtype=jnp.float64)
        n = theta_grid.shape[0]

        # Trapezoidal quadrature weights (sin θ is the solid-angle Jacobian)
        dtheta = jnp.pi / (n - 1)
        sin_theta = jnp.sin(theta_grid)
        weights = sin_theta * dtheta
        weights = weights.at[0].multiply(0.5)
        weights = weights.at[-1].multiply(0.5)

        f_vals = f_theta(theta_grid)

        # Fill coefficients.  Python for-loop over static max_l range is
        # fully JIT-compatible because max_l is a fixed dataclass attribute
        # (not a traced value).
        #
        # For axisymmetric f(θ), the phi-integral gives:
        #   ∫ e^{-imφ} dφ = 2π  for m=0
        #   ∫ e^{-imφ} dφ = 0   for m≠0
        # So only m=0 coefficients are non-zero.
        coeffs = jnp.zeros_like(self.coefficients)
        for l in range(self.max_l + 1):
            Y_l0 = sph_harm_y_jax(0, l, 0.0, theta_grid)
            a_l0 = jnp.sum(f_vals * jnp.conj(Y_l0) * weights) * 2.0 * jnp.pi
            coeffs = coeffs.at[l, self.max_l].set(a_l0)
        self.coefficients = coeffs
        return coeffs

    # ── Reconstruction ──────────────────────────────────────────

    def reconstruct(
        self,
        theta: jax.Array,
        phi: jax.Array,
    ) -> jax.Array:
        """Reconstruct *f(θ, φ)* from expansion coefficients.

        Evaluates
            f(θ, φ) ≈ Σₗ₌₀ᴸ Σₘ₌₋ₗˡ  aₗₘ · Yₗₘ(θ, φ)

        Args:
            theta: Polar angle(s) in radians.
            phi: Azimuthal angle(s) in radians.

        Returns:
            Reconstructed value(s), real part, same shape as *theta*.
        """
        theta = jnp.atleast_1d(jnp.asarray(theta, dtype=jnp.float64))
        phi = jnp.atleast_1d(jnp.asarray(phi, dtype=jnp.float64))

        # Python for-loops over static max_l range.  All loop variables
        # (l, idx) are concrete Python ints so sph_harm_y_jax receives
        # static m / n parameters — fully JIT-compatible.
        result = jnp.zeros(theta.shape, dtype=jnp.complex128)
        for l in range(self.max_l + 1):
            for idx in range(2 * self.max_l + 1):
                m_val = idx - self.max_l
                if abs(m_val) <= l:
                    result = (
                        result
                        + self.coefficients[l, idx]
                        * sph_harm_y_jax(m_val, l, phi, theta)
                    )

        if theta.shape == (1,):
            return result.real.squeeze()
        return result.real

    # ── Convergence analysis ────────────────────────────────────

    def convergence_analysis(
        self,
        f_theta: callable,
        theta_grid: jax.Array,
        phi_grid: jax.Array | None = None,
    ) -> jax.Array:
        """Convergence analysis: mean absolute error at each l_max.

        Computes
            error(l') = mean | f(θᵢ) − f_{l'}(θᵢ) |
        for ``l' = 0, 1, …, max_l`` where ``f_{l'}`` is the truncated
        expansion keeping only terms with ``l ≤ l'``.

        Args:
            f_theta: Callable returning function values on the grid.
            theta_grid: 1-D array of polar angles in ``[0, π]``.
            phi_grid: 1-D array of azimuthal angles (default all zero).

        Returns:
            Array of length ``max_l + 1`` with errors at each truncation.
        """
        theta_grid = jnp.asarray(theta_grid, dtype=jnp.float64)
        if phi_grid is None:
            phi_grid = jnp.zeros_like(theta_grid)
        else:
            phi_grid = jnp.asarray(phi_grid, dtype=jnp.float64)

        exact = f_theta(theta_grid)
        n_pts = theta_grid.shape[0]

        errors = jnp.zeros(self.max_l + 1, dtype=jnp.float64)

        for l_prime in range(self.max_l + 1):
            recon = jnp.zeros(theta_grid.shape, dtype=jnp.complex128)
            for l in range(l_prime + 1):
                for idx in range(2 * self.max_l + 1):
                    m_val = idx - self.max_l
                    if abs(m_val) <= l:
                        recon = (
                            recon
                            + self.coefficients[l, idx]
                            * sph_harm_y_jax(m_val, l, phi_grid, theta_grid)
                        )
            err = jnp.mean(jnp.abs(exact - recon.real))
            errors = errors.at[l_prime].set(err)

        return errors
