"""
JAX-compatible Ampere-Maxwell law and displacement current.

Provides JAX-pytree versions of:
- maxwell.electromagnetism.fields.ampere_maxwell.DisplacementCurrent
- maxwell.electromagnetism.fields.ampere_maxwell.AmpereMaxwellLaw

Enabling JIT compilation, automatic differentiation, and vectorized
evaluation of displacement current and Ampere-Maxwell law in CGS units.

Implemented (Arts. 606-607):
    - DisplacementCurrentJAX: J_d = (epsilon/4pi) * dE/dt, D = epsilon*E
    - AmpereMaxwellLawJAX: curl(H) = 4pi*J_cond + dD/dt
    - Standalone functions: displacement_current_jax, total_current_jax,
      curl_H_jax, magnetic_field_from_current_jax, capacitor_paradox_jax

Category: B (user_original) -- JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 606-607: Ampere-Maxwell law and displacement current.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit, vmap

from maxwell.jax._compat import jax_tree, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "DisplacementCurrentJAX",
    "AmpereMaxwellLawJAX",
    "displacement_current_jax",
    "total_current_jax",
    "curl_H_jax",
    "magnetic_field_from_current_jax",
    "capacitor_paradox_jax",
]


# ── DisplacementCurrentJAX ──────────────────────────────────────


@jax_tree
@dataclass
class DisplacementCurrentJAX:
    """Displacement current density (JAX-compatible pytree).

    Art. 606-607: Maxwell's displacement current arises from the
    time-varying electric field:

        J_d = (epsilon / 4pi) * dE/dt

    Attributes:
        E_field: Electric field vector (statvolts/cm), shape (3,).
        dE_dt: Time derivative of E (statvolts/cm/s), shape (3,).
        permittivity: Permittivity epsilon (dimensionless).
    """

    E_field: jax.Array = None  # type: ignore[assignment]
    dE_dt: jax.Array = None  # type: ignore[assignment]
    permittivity: float = 1.0

    def __post_init__(self):
        zero3 = jnp.zeros(3, dtype=jnp.float64)
        object.__setattr__(
            self,
            "E_field",
            jnp.asarray(
                self.E_field if self.E_field is not None else zero3,
                dtype=jnp.float64,
            ),
        )
        object.__setattr__(
            self,
            "dE_dt",
            jnp.asarray(
                self.dE_dt if self.dE_dt is not None else zero3,
                dtype=jnp.float64,
            ),
        )

    @property
    def D_field(self) -> jax.Array:
        """D = epsilon * E."""
        return jnp.asarray(self.permittivity, dtype=jnp.float64) * self.E_field

    @property
    def dD_dt(self) -> jax.Array:
        """dD/dt = epsilon * dE/dt."""
        return jnp.asarray(self.permittivity, dtype=jnp.float64) * self.dE_dt

    @property
    def J_displacement(self) -> jax.Array:
        """J_d = (1/4pi) * dD/dt."""
        return self.dD_dt / (4.0 * jnp.pi)

    @property
    def magnitude(self) -> jax.Array:
        """|J_d|."""
        return safe_norm(self.J_displacement[None, :], axis=-1)[0]


# ── AmpereMaxwellLawJAX ─────────────────────────────────────────


@jax_tree
@dataclass
class AmpereMaxwellLawJAX:
    """Ampere-Maxwell law calculator (JAX-compatible pytree).

    Art. 606-607: Maxwell's completion of Ampere's law:

        curl(H) = 4pi * (J_cond + J_disp)
        J_disp = (epsilon / 4pi) * dE/dt

    Attributes:
        J_conduction: Conduction current density (abamperes/cm^2), shape (3,).
        dE_dt: Time derivative of E (statvolts/cm/s), shape (3,).
        permittivity: Permittivity epsilon (dimensionless).
    """

    J_conduction: jax.Array = None  # type: ignore[assignment]
    dE_dt: jax.Array = None  # type: ignore[assignment]
    permittivity: float = 1.0

    def __post_init__(self):
        zero3 = jnp.zeros(3, dtype=jnp.float64)
        object.__setattr__(
            self,
            "J_conduction",
            jnp.asarray(
                self.J_conduction if self.J_conduction is not None else zero3,
                dtype=jnp.float64,
            ),
        )
        object.__setattr__(
            self,
            "dE_dt",
            jnp.asarray(
                self.dE_dt if self.dE_dt is not None else zero3,
                dtype=jnp.float64,
            ),
        )

    @property
    def J_displacement(self) -> jax.Array:
        """J_d = (epsilon / 4pi) * dE/dt."""
        return (
            jnp.asarray(self.permittivity, dtype=jnp.float64)
            * self.dE_dt
            / (4.0 * jnp.pi)
        )

    @property
    def J_total(self) -> jax.Array:
        """J_total = J_cond + J_disp."""
        return self.J_conduction + self.J_displacement

    @property
    def curl_H(self) -> jax.Array:
        """curl(H) = 4pi * J_total."""
        return 4.0 * jnp.pi * self.J_total

    def compute_curl_H(
        self,
        J_conduction: jax.Array = None,
        dE_dt: jax.Array = None,
    ) -> jax.Array:
        """Compute curl(H) with optional overrides."""
        J_c = J_conduction if J_conduction is not None else self.J_conduction
        dE = dE_dt if dE_dt is not None else self.dE_dt
        J_d = jnp.asarray(self.permittivity, dtype=jnp.float64) * dE / (4.0 * jnp.pi)
        return 4.0 * jnp.pi * (J_c + J_d)


# ── Standalone JAX functions ────────────────────────────────────


@maxwell_cite(
    606,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Displacement current density in CGS-Gaussian units",
)
def displacement_current_jax(
    dE_dt: jax.Array,
    permittivity: jax.Array = 1.0,
) -> jax.Array:
    """J_d = (epsilon / 4pi) * dE/dt.

    Art. 606.

    Args:
        dE_dt: Time derivative of E (statvolts/cm/s), shape (3,).
        permittivity: Permittivity epsilon (dimensionless).

    Returns:
        Displacement current density (abamperes/cm^2), shape (3,).
    """
    dE_dt = jnp.asarray(dE_dt, dtype=jnp.float64)
    permittivity = jnp.asarray(permittivity, dtype=jnp.float64)
    return (permittivity / (4.0 * jnp.pi)) * dE_dt


@maxwell_cite(
    606,
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Total current density including displacement",
)
def total_current_jax(
    J_conduction: jax.Array,
    dE_dt: jax.Array,
    permittivity: jax.Array = 1.0,
) -> jax.Array:
    """J_total = J_cond + (epsilon/4pi) * dE/dt.

    Art. 606-607.

    Args:
        J_conduction: Conduction current density (abamperes/cm^2), shape (3,).
        dE_dt: Time derivative of E (statvolts/cm/s), shape (3,).
        permittivity: Permittivity epsilon (dimensionless).

    Returns:
        Total current density (abamperes/cm^2), shape (3,).
    """
    J_conduction = jnp.asarray(J_conduction, dtype=jnp.float64)
    dE_dt = jnp.asarray(dE_dt, dtype=jnp.float64)
    permittivity = jnp.asarray(permittivity, dtype=jnp.float64)
    J_disp = (permittivity / (4.0 * jnp.pi)) * dE_dt
    return J_conduction + J_disp


@maxwell_cite(
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Curl of H field from total current",
)
def curl_H_jax(
    J_conduction: jax.Array,
    dE_dt: jax.Array,
    permittivity: jax.Array = 1.0,
) -> jax.Array:
    """curl(H) = 4pi * J_total.

    Art. 607.

    Args:
        J_conduction: Conduction current density (abamperes/cm^2), shape (3,).
        dE_dt: Time derivative of E (statvolts/cm/s), shape (3,).
        permittivity: Permittivity epsilon (dimensionless).

    Returns:
        Curl of H (oersted/cm), shape (3,).
    """
    J_total = total_current_jax(J_conduction, dE_dt, permittivity)
    return 4.0 * jnp.pi * J_total


@maxwell_cite(
    606,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Magnetic field from current element via Biot-Savart",
)
def magnetic_field_from_current_jax(
    current_element: jax.Array,
    position: jax.Array,
) -> jax.Array:
    """dH = (1/4pi) * (I*dl x r) / r^3.

    Art. 606. Biot-Savart law for a current element.

    Args:
        current_element: Current element I*dl (abampere*cm), shape (3,).
        position: Position relative to current element (cm), shape (3,).

    Returns:
        Magnetic field H (oersted), shape (3,).
    """
    current_element = jnp.asarray(current_element, dtype=jnp.float64)
    position = jnp.asarray(position, dtype=jnp.float64)
    r_mag = safe_norm(position[None, :], axis=-1)[0]
    # Safe computation: zero field at zero distance
    r_mag_safe = jnp.where(r_mag > 1e-30, r_mag, 1.0)
    r_hat = jnp.where(r_mag > 1e-30, position / r_mag_safe, jnp.zeros(3))
    cross = jnp.cross(current_element, r_hat)
    dH_mag = jnp.where(r_mag > 1e-30, 1.0 / (r_mag_safe**2), 0.0)
    dH = (1.0 / (4.0 * jnp.pi)) * cross * dH_mag
    return dH


@maxwell_cite(
    606,
    607,
    part=4,
    chapter="Ampere-Maxwell Law",
    theory_class="maxwell_original",
    description="Capacitor paradox verification in CGS units",
)
def capacitor_paradox_jax(
    charging_current: jax.Array,
    plate_area: jax.Array,
) -> dict[str, jax.Array]:
    """Verify displacement current resolves the capacitor paradox.

    Art. 606-607: For a charging capacitor, displacement current
    between plates equals conduction current in wires.

    Args:
        charging_current: Charging current (abamperes).
        plate_area: Capacitor plate area (cm^2).

    Returns:
        Dictionary with conduction_current, displacement_current,
        dE_dt, and paradox_resolved flag.
    """
    charging_current = jnp.asarray(charging_current, dtype=jnp.float64)
    plate_area = jnp.asarray(plate_area, dtype=jnp.float64)

    # dE/dt = 4pi * I / A
    dE_dt = (4.0 * jnp.pi / plate_area) * charging_current

    # J_d = (1/4pi) * dE/dt = I / A
    J_d = dE_dt / (4.0 * jnp.pi)

    # I_d = J_d * A = I
    I_displacement = J_d * plate_area

    return {
        "conduction_current": charging_current,
        "displacement_current": I_displacement,
        "dE_dt": dE_dt,
        "paradox_resolved": jnp.isclose(I_displacement, charging_current, rtol=1e-10),
    }
