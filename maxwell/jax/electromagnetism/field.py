"""
JAX-compatible electric field and electric intensity.

Provides ElectricFieldJAX: a JAX-pytree version of maxwell.core.field.ElectricField
that supports JIT compilation, automatic differentiation, and batched evaluation.

Implements the theory of the electric field from Part I:
- Electric field definition (Art. 44)
- Electromotive force and potential (Art. 45)
- Equipotential surfaces (Art. 46)
- Lines of force (Art. 47)
- Electric tension (Art. 48)
- Electromotive force calculation (Art. 49)
- Electric flux and Gauss's law (Art. 76)
- Field from potential gradient (Art. 71)

Category: B (user_original) — JAX adapter for Maxwell's theory.

References:
    Part I, Chapter I, Arts. 44-49: Electric field fundamentals.
    Part I, Chapter II, Arts. 66-68: Field intensity from charges.
    Part I, Chapter II, Art. 76: Induction through a closed surface.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree, safe_norm
from maxwell.jax.core.charge import PointChargeJAX
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "ElectricFieldJAX",
    "electric_flux_jax",
    "gauss_law_closed_surface_jax",
    "field_from_potential_jax",
    "electromotive_force_jax",
    "electric_tension_jax",
    "superposition_field_jax",
]


@jax_tree
@dataclass
class ElectricFieldJAX:
    """The electric field at a point in space (JAX-compatible).

    Art. 44: The electric field is the region in which electric forces act.
    Art. 47: Lines of force represent the direction of the field.

    The electric field E is defined as the force per unit charge:
        E = F / q  (dyne/esu = statvolt/cm)

    In CGS-ESU, for a point charge:
        E = q * r_hat / r^2

    Attributes:
        value: Field vector (Ex, Ey, Ez) in statvolt/cm, shape (3,).
        position: Position vector (x, y, z) in cm where field is evaluated.
    """

    value: jax.Array  # shape (3,)
    position: jax.Array  # shape (3,)

    def __post_init__(self):
        self.value = jnp.asarray(self.value, dtype=jnp.float64)
        self.position = jnp.asarray(self.position, dtype=jnp.float64)

    @property
    def magnitude(self) -> jax.Array:
        """Magnitude of the electric field |E|."""
        return safe_norm(self.value[None, :], axis=-1)[0]

    @property
    def direction(self) -> jax.Array:
        """Unit vector in the direction of the field."""
        mag = self.magnitude
        return jnp.where(mag > 1e-30, self.value / mag, jnp.zeros(3))

    # ── Factory methods ───────────────────────────────────────────

    @classmethod
    @maxwell_cite(
        44,
        47,
        part=1,
        chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Create electric field from a point charge (JAX)",
    )
    def from_point_charge(
        cls, charge: PointChargeJAX, point: jax.Array
    ) -> ElectricFieldJAX:
        """Create electric field due to a point charge at a given position.

        E = q * r_hat / r^2  (Art. 44, Art. 66)

        Args:
            charge: PointChargeJAX object with charge q and position.
            point: Position vector (cm) where field is evaluated.

        Returns:
            ElectricFieldJAX object at the specified point.
        """
        point = jnp.asarray(point, dtype=jnp.float64)
        field_value = charge.field_at(point)
        return cls(value=field_value, position=point)

    @classmethod
    @maxwell_cite(
        44,
        84,
        part=1,
        chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Superposition of electric fields from multiple charges (JAX)",
    )
    def superposition(
        cls, charges: list[PointChargeJAX], point: jax.Array
    ) -> ElectricFieldJAX:
        """Calculate resultant electric field from multiple point charges.

        Art. 84: The principle of superposition — the resultant field is
        the vector sum of individual fields.

        Args:
            charges: List of PointChargeJAX objects.
            point: Position vector (cm) where field is evaluated.

        Returns:
            Resultant ElectricFieldJAX at the specified point.
        """
        point = jnp.asarray(point, dtype=jnp.float64)
        total_field = jnp.zeros(3)
        for charge in charges:
            total_field = total_field + charge.field_at(point)
        return cls(value=total_field, position=point)

    # ── Field properties ──────────────────────────────────────────

    @maxwell_cite(
        68,
        part=1,
        chapter="Mathematical Definitions",
        theory_class="maxwell_original",
        description="Resultant electric intensity at a point (JAX)",
    )
    def intensity(self) -> jax.Array:
        """Calculate the resultant electric intensity at the point.

        Art. 68: The resultant intensity is the magnitude of the
        resultant force on a unit positive charge.

        Returns:
            Electric intensity (statvolt/cm).
        """
        return self.magnitude

    @maxwell_cite(
        49,
        part=1,
        chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Electromotive force along a path (JAX)",
    )
    def electromotive_force(
        self,
        path_end: jax.Array,
        num_steps: int = 100,
    ) -> jax.Array:
        """Calculate electromotive force (EMF) along a path from current position.

        Art. 49: The electromotive force is the line integral of
        the electric intensity along a path.

        For electrostatic fields, this equals the potential difference:
            EMF = integral(E . dl) = V(start) - V(end)

        Args:
            path_end: End position vector (cm), shape (3,).
            num_steps: Number of steps for numerical integration.

        Returns:
            Electromotive force (statvolt).
        """
        path_end = jnp.asarray(path_end, dtype=jnp.float64)
        path_vector = path_end - self.position
        dl = path_vector / num_steps

        # Use jax.lax.fori_loop for JIT traceability
        def step(i, emf):
            t = (i + 0.5) / num_steps
            emf = emf + jnp.dot(self.value, dl)
            return emf

        return jax.lax.fori_loop(0, num_steps, step, jnp.array(0.0))

    # ── Batched evaluation ────────────────────────────────────────

    def field_at_batched(self, positions: jax.Array) -> jax.Array:
        """Evaluate field at many positions (assumes uniform field).

        For a uniform field, this broadcasts the same value.
        For non-uniform fields, use with a field function.

        Args:
            positions: Array of position vectors, shape (N, 3).

        Returns:
            Field vectors at each position, shape (N, 3).
        """
        return jnp.broadcast_to(self.value[None, :], (positions.shape[0], 3))


# ── Standalone functions ───────────────────────────────────────────


@maxwell_cite(
    48,
    part=1,
    chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Electric tension along a line of force (JAX)",
)
def electric_tension_jax(field_value: jax.Array) -> jax.Array:
    """Calculate electric tension along a line of force.

    Art. 48: Electric tension is the integral of the electric intensity
    along a line of force. It represents the work done per unit charge.

    For a uniform field: Tension = |E| * length

    Args:
        field_value: Electric field vector, shape (3,).

    Returns:
        Electric tension (statvolt/cm along the line).
    """
    return safe_norm(field_value[None, :], axis=-1)[0]


@maxwell_cite(
    76,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Electric flux through a surface (JAX)",
)
def electric_flux_jax(
    field_value: jax.Array,
    surface_normal: jax.Array,
    area: float,
) -> jax.Array:
    """Calculate electric flux through a surface.

    Art. 76: The induction through a closed surface equals 4*pi times
    the total charge enclosed (Gauss's law in CGS).

    Flux = integral(E . dA) ≈ E . n * Area  (for uniform field over planar surface)

    Args:
        field_value: Electric field vector, shape (3,).
        surface_normal: Unit normal vector to the surface, shape (3,).
        area: Surface area in cm^2.

    Returns:
        Electric flux through the surface.
    """
    surface_normal = jnp.asarray(surface_normal, dtype=jnp.float64)
    n_mag = safe_norm(surface_normal[None, :], axis=-1)[0]
    n_hat = jnp.where(n_mag > 1e-30, surface_normal / n_mag, jnp.zeros(3))
    return jnp.dot(field_value, n_hat) * area


@maxwell_cite(
    76,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Gauss's law — flux through closed surface (JAX)",
)
def gauss_law_closed_surface_jax(
    total_charge: jax.Array,
) -> jax.Array:
    """Compute the expected electric flux through a closed surface via Gauss's law.

    Art. 76: The total induction through any closed surface is equal to
    4*pi times the total quantity of electricity enclosed.

    In CGS-ESU:
        Flux = 4 * pi * Q_enclosed

    Args:
        total_charge: Total enclosed charge in esu.

    Returns:
        Expected electric flux through the closed surface.
    """
    return 4.0 * jnp.pi * total_charge


@maxwell_cite(
    71,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Electric field as gradient of potential (JAX)",
)
def field_from_potential_jax(
    potential_func,
    point: jax.Array,
) -> jax.Array:
    """Calculate electric field from potential using automatic differentiation.

    Art. 71: The resultant intensity is the gradient of the potential:
        E = -grad(V)

    In components:
        Ex = -dV/dx, Ey = -dV/dy, Ez = -dV/dz

    Uses JAX automatic differentiation for exact gradients.

    Args:
        potential_func: Function returning V at a position (shape (3,) -> scalar).
        point: Position vector (cm) where field is calculated, shape (3,).

    Returns:
        Electric field vector at the specified point, shape (3,).
    """
    point = jnp.asarray(point, dtype=jnp.float64)
    grad_V = grad(potential_func)(point)
    return -grad_V


@maxwell_cite(
    69,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Line integral of electric intensity (JAX)",
)
def electromotive_force_jax(
    field_func,
    start: jax.Array,
    end: jax.Array,
    num_steps: int = 1000,
) -> jax.Array:
    """Calculate line integral of electric intensity along a path.

    Art. 69: The line integral of the electric intensity along a path
    is the electromotive force between the endpoints.

    EMF = integral(E . dl) from start to end

    For electrostatic fields, this is path-independent and equals
    the potential difference.

    Uses jax.lax.fori_loop for JIT traceability.

    Args:
        field_func: Function returning E at a position (shape (3,) -> shape (3,)).
        start: Starting position vector (cm), shape (3,).
        end: Ending position vector (cm), shape (3,).
        num_steps: Number of steps for numerical integration.

    Returns:
        Line integral (electromotive force in statvolt).
    """
    start = jnp.asarray(start, dtype=jnp.float64)
    end = jnp.asarray(end, dtype=jnp.float64)
    path_vector = end - start
    dl = path_vector / num_steps

    def step(i, integral):
        t = (i + 0.5) / num_steps
        current_pos = start + t * path_vector
        E = field_func(current_pos)
        integral = integral + jnp.dot(E, dl)
        return integral

    return jax.lax.fori_loop(0, num_steps, step, jnp.array(0.0))


@maxwell_cite(
    84,
    part=1,
    chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Superposition of electric fields from multiple charges (JAX standalone)",
)
def superposition_field_jax(
    charges: list[PointChargeJAX],
    points: jax.Array,
) -> jax.Array:
    """Total electric field from multiple point charges at many points.

    Art. 84: The principle of superposition — the resultant field is
    the vector sum of individual fields.

    Args:
        charges: List of PointChargeJAX objects.
        points: Evaluation points, shape (N, 3).

    Returns:
        Total electric field, shape (N, 3).
    """
    total = jnp.zeros_like(points)
    for charge in charges:
        total = total + charge.field_at_batched(points)
    return total
