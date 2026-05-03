"""
JAX-compatible magnetic vector potential — Part III (Arts. 405-406).

Provides VectorPotentialJAX: a JAX-pytree version of maxwell.calculus.vector_potential.VectorPotential,
enabling JIT compilation, automatic differentiation, and vectorized evaluation of the
magnetic vector potential A and its derived B field.

Key capabilities:
- A = (m x r) / r^3 for magnetic dipoles
- A = Idl / r for current elements (CGS-EMU)
- B = curl(A) via numerical finite differences
- B = curl(A) via JAX auto-diff (exact)
- Full pytree registration for jax.jit, jax.grad, jax.vmap

Category: B (user_original) — JAX adapter for Maxwell's vector potential theory.

References:
    Part III, Arts. 405-406: Magnetic vector potential A where B = curl(A).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import jax
import jax.numpy as jnp
from jax import jit, vmap, jacfwd

from maxwell.jax._compat import jax_tree, safe_div, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "VectorPotentialJAX",
    "curl_jax",
    "curl_autodiff_jax",
    "dipole_vector_potential_jax",
    "B_from_dipole_autodiff_jax",
    "verify_vector_potential_curl_jax",
    "current_element_potential_jax",
]


# ── VectorPotentialJAX ──────────────────────────────────────────


@jax_tree
@dataclass
class VectorPotentialJAX:
    """Magnetic vector potential A (JAX-compatible pytree).

    Art. 405-406: The magnetic vector potential A is defined such that:

        B = curl(A)

    This definition automatically satisfies div(B) = 0.

    Attributes:
        A_field: Vector potential A (gauss*cm), shape (3,).
        position: Position where A is evaluated (cm), shape (3,).
    """

    A_field: jax.Array
    position: jax.Array

    def __post_init__(self):
        self.A_field = jnp.asarray(self.A_field, dtype=jnp.float64)
        self.position = jnp.asarray(self.position, dtype=jnp.float64)

    # ── Properties ──────────────────────────────────────────────

    @property
    def magnitude(self) -> jax.Array:
        """|A| — magnitude of vector potential."""
        return safe_norm(self.A_field[None, :], axis=-1)[0]

    @property
    def direction(self) -> jax.Array:
        """Unit vector in direction of A (zero if A is zero)."""
        mag = self.magnitude
        return jnp.where(mag > 1e-30, self.A_field / mag, jnp.zeros(3))

    # ── B field from A ──────────────────────────────────────────

    def compute_B_field(self, A_func: Callable, dx: float = 0.01) -> jax.Array:
        """B = curl(A) via numerical finite differences.

        Art. 405: B = nabla x A

        Args:
            A_func: Callable that takes position (3,) and returns A (3,).
            dx: Step size for finite differences.

        Returns:
            B field vector (gauss), shape (3,).
        """
        return curl_jax(A_func, self.position, dx=dx)

    def compute_B_field_autodiff(self, A_func: Callable) -> jax.Array:
        """B = curl(A) via JAX auto-diff (exact curl).

        Uses jax.jacfwd to compute the Jacobian of A, then extracts
        the curl components analytically.

        Args:
            A_func: Callable that takes position (3,) and returns A (3,).

        Returns:
            B field vector (gauss), shape (3,).
        """
        return curl_autodiff_jax(A_func, self.position)


# ── Standalone curl functions ───────────────────────────────────


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="standard_math",
    description="Numerical curl via finite differences in JAX",
)
def curl_jax(
    field_func: Callable[[jax.Array], jax.Array],
    point: jax.Array,
    dx: float = 0.01,
) -> jax.Array:
    """Compute curl of a vector field via numerical finite differences.

    Art. 405: (curl A)_i = epsilon_ijk * partial_j A_k

    In components:
        (curl A)_x = dA_z/dy - dA_y/dz
        (curl A)_y = dA_x/dz - dA_z/dx
        (curl A)_z = dA_y/dx - dA_x/dy

    Args:
        field_func: Function mapping position (3,) -> field (3,).
        point: Position where curl is evaluated, shape (3,).
        dx: Step size for central differences.

    Returns:
        Curl vector, shape (3,).
    """
    point = jnp.asarray(point, dtype=jnp.float64)

    def component(i: int) -> jax.Array:
        j = (i + 1) % 3
        k = (i + 2) % 3

        # partial_j A_k
        delta_j = jnp.zeros(3, dtype=jnp.float64).at[j].set(dx)
        A_plus_j = field_func(point + delta_j)[k]
        A_minus_j = field_func(point - delta_j)[k]
        dA_k_dj = (A_plus_j - A_minus_j) / (2.0 * dx)

        # partial_k A_j
        delta_k = jnp.zeros(3, dtype=jnp.float64).at[k].set(dx)
        A_plus_k = field_func(point + delta_k)[j]
        A_minus_k = field_func(point - delta_k)[j]
        dA_j_dk = (A_plus_k - A_minus_k) / (2.0 * dx)

        return dA_k_dj - dA_j_dk

    return jnp.array([component(i) for i in range(3)], dtype=jnp.float64)


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="standard_math",
    description="Exact curl via JAX auto-diff (jacfwd)",
)
def curl_autodiff_jax(
    field_func: Callable[[jax.Array], jax.Array],
    point: jax.Array,
) -> jax.Array:
    """Compute exact curl of a vector field via JAX auto-differentiation.

    Uses jax.jacfwd to compute the Jacobian J_ij = dA_i/dx_j, then:
        (curl A)_x = J[2,1] - J[1,2]
        (curl A)_y = J[0,2] - J[2,0]
        (curl A)_z = J[1,0] - J[0,1]

    Args:
        field_func: Function mapping position (3,) -> field (3,).
        point: Position where curl is evaluated, shape (3,).

    Returns:
        Curl vector, shape (3,).
    """
    point = jnp.asarray(point, dtype=jnp.float64)
    J = jacfwd(field_func)(point)  # shape (3, 3): J[i,j] = dA_i/dx_j

    return jnp.array([
        J[2, 1] - J[1, 2],  # x component
        J[0, 2] - J[2, 0],  # y component
        J[1, 0] - J[0, 1],  # z component
    ], dtype=jnp.float64)


# ── Dipole vector potential ─────────────────────────────────────


@maxwell_cite(
    406,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Magnetic vector potential from a dipole: A = (m x r) / r^3",
)
def dipole_vector_potential_jax(
    magnetic_moment: jax.Array,
    observation_point: jax.Array,
    dipole_position: jax.Array | None = None,
) -> jax.Array:
    """Vector potential A from a magnetic dipole.

    Art. 406: For a magnetic dipole m at position r_0, the vector
    potential at r is:

        A(r) = (m x (r - r_0)) / |r - r_0|^3

    Args:
        magnetic_moment: Dipole moment m (emu), shape (3,).
        observation_point: Position where A is evaluated (cm), shape (3,).
        dipole_position: Position of dipole (cm), shape (3,). Defaults to origin.

    Returns:
        Vector potential A (gauss*cm), shape (3,).
    """
    magnetic_moment = jnp.asarray(magnetic_moment, dtype=jnp.float64)
    observation_point = jnp.asarray(observation_point, dtype=jnp.float64)
    if dipole_position is None:
        dipole_position = jnp.zeros(3, dtype=jnp.float64)
    else:
        dipole_position = jnp.asarray(dipole_position, dtype=jnp.float64)

    r_vec = observation_point - dipole_position
    r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
    r_mag_safe = jnp.maximum(r_mag, 1e-30)

    A = jnp.cross(magnetic_moment, r_vec) / (r_mag_safe ** 3)
    return jnp.where(r_mag < 1e-30, jnp.zeros(3), A)


@maxwell_cite(
    405, 406,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="B field from dipole via auto-diff curl of A",
)
def B_from_dipole_autodiff_jax(
    magnetic_moment: jax.Array,
    observation_point: jax.Array,
    dipole_position: jax.Array | None = None,
) -> jax.Array:
    """B field from magnetic dipole via auto-diff curl of vector potential.

    Computes B = curl(A) where A is the dipole vector potential,
    using JAX auto-diff for exact derivatives.

    The analytical dipole B field is:
        B = (3*(m . r_hat)*r_hat - m) / r^3

    This verifies that curl(A_dipole) = B_dipole.

    Args:
        magnetic_moment: Dipole moment m (emu), shape (3,).
        observation_point: Position where B is evaluated (cm), shape (3,).
        dipole_position: Position of dipole (cm), shape (3,). Defaults to origin.

    Returns:
        B field (gauss), shape (3,).
    """
    magnetic_moment = jnp.asarray(magnetic_moment, dtype=jnp.float64)
    observation_point = jnp.asarray(observation_point, dtype=jnp.float64)
    if dipole_position is None:
        dipole_position = jnp.zeros(3, dtype=jnp.float64)
    else:
        dipole_position = jnp.asarray(dipole_position, dtype=jnp.float64)

    def A_at(pos: jax.Array) -> jax.Array:
        return dipole_vector_potential_jax(magnetic_moment, pos, dipole_position)

    return curl_autodiff_jax(A_at, observation_point)


@maxwell_cite(
    405, 406,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Verify curl(A) = B for magnetic dipole",
)
def verify_vector_potential_curl_jax(
    magnetic_moment: jax.Array,
    observation_point: jax.Array,
    dipole_position: jax.Array | None = None,
) -> dict[str, jax.Array | float]:
    """Verify that curl(A) = B for a magnetic dipole.

    Art. 405: B = curl(A) must hold for any valid vector potential.

    For a dipole:
        A = (m x r) / r^3
        B_analytical = (3*(m.r_hat)*r_hat - m) / r^3

    This function computes B via auto-diff curl of A and compares
    with the analytical dipole B field.

    Args:
        magnetic_moment: Dipole moment m (emu), shape (3,).
        observation_point: Position where B is evaluated (cm), shape (3,).
        dipole_position: Position of dipole (cm), shape (3,). Defaults to origin.

    Returns:
        Dictionary with:
        - A: Vector potential at observation point, shape (3,)
        - B_from_curl: curl(A) via auto-diff, shape (3,)
        - B_analytical: Analytical dipole B field, shape (3,)
        - residual: |B_from_curl - B_analytical|, scalar
        - verified: True if residual < tolerance
    """
    magnetic_moment = jnp.asarray(magnetic_moment, dtype=jnp.float64)
    observation_point = jnp.asarray(observation_point, dtype=jnp.float64)
    if dipole_position is None:
        dipole_position = jnp.zeros(3, dtype=jnp.float64)
    else:
        dipole_position = jnp.asarray(dipole_position, dtype=jnp.float64)

    # Compute A
    A = dipole_vector_potential_jax(magnetic_moment, observation_point, dipole_position)

    # Compute B via auto-diff curl
    def A_at(pos: jax.Array) -> jax.Array:
        return dipole_vector_potential_jax(magnetic_moment, pos, dipole_position)

    B_from_curl = curl_autodiff_jax(A_at, observation_point)

    # Analytical dipole B field
    r_vec = observation_point - dipole_position
    r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
    r_mag_safe = jnp.maximum(r_mag, 1e-30)
    r_hat = jnp.where(r_mag > 1e-30, r_vec / r_mag_safe, jnp.zeros(3))
    m_dot_r = jnp.dot(magnetic_moment, r_hat)
    B_analytical = (3.0 * m_dot_r * r_hat - magnetic_moment) / (r_mag_safe ** 3)
    B_analytical = jnp.where(r_mag < 1e-30, jnp.zeros(3), B_analytical)

    residual = safe_norm((B_from_curl - B_analytical)[None, :], axis=-1)[0]
    tolerance = 1e-6

    return {
        "A": A,
        "B_from_curl": B_from_curl,
        "B_analytical": B_analytical,
        "residual": residual,
        "verified": residual < tolerance,
    }


# ── Current element vector potential ────────────────────────────


@maxwell_cite(
    405,
    part=3, chapter="Vector Potential",
    theory_class="maxwell_original",
    description="Vector potential from current element: A = Idl / r (CGS-EMU)",
)
def current_element_potential_jax(
    Idl: jax.Array,
    source_pos: jax.Array,
    observation_pos: jax.Array,
) -> jax.Array:
    """Vector potential from a current element.

    Art. 405: For a current element I*dl at position r', the vector
    potential at r is (CGS-EMU):

        A(r) = I * dl / |r - r'|

    Args:
        Idl: Current element I*dl (abampere*cm), shape (3,).
        source_pos: Position of current element (cm), shape (3,).
        observation_pos: Position where A is evaluated (cm), shape (3,).

    Returns:
        Vector potential A (gauss*cm), shape (3,).
    """
    Idl = jnp.asarray(Idl, dtype=jnp.float64)
    source_pos = jnp.asarray(source_pos, dtype=jnp.float64)
    observation_pos = jnp.asarray(observation_pos, dtype=jnp.float64)

    r_vec = observation_pos - source_pos
    r_mag = safe_norm(r_vec[None, :], axis=-1)[0]
    r_mag_safe = jnp.maximum(r_mag, 1e-30)

    A = Idl / r_mag_safe
    return jnp.where(r_mag < 1e-30, jnp.zeros(3), A)
