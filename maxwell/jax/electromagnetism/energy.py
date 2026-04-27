"""
JAX-compatible electrostatic energy — Part IV (Electromagnetic Energy).

Provides ElectrostaticEnergyJAX and CapacitorEnergyJAX: JAX-pytree versions
of maxwell.electromagnetism.energy.electrostatic.ElectrostaticEnergy that
support JIT compilation, automatic differentiation, and batched evaluation
via vmap over electric field configurations simultaneously.

Implements Maxwell's electrostatic energy formulas from Articles 630-631:

- Energy density: u = (1/8*pi) * E*D = (1/8*pi) * eps * E^2  (Art. 630)
- Total energy: U = (1/8*pi) * int(E*D dV)  (Art. 630)
- Capacitor energy: U = (1/2)*C*V^2 = Q^2/(2*C) = (1/2)*Q*V  (Art. 631)

All computations use CGS-EMU units:
    E in statvolt/cm, energy density in erg/cm^3, energy in erg

Key differences from the NumPy version:
- Uses jax.numpy exclusively (no np.* calls)
- Safe norm via jnp.where (no Python if/else on array values)
- Pytree-registered for jax.jit, jax.grad, jax.vmap compatibility
- Batch-aware: vmap works over (N, 3) E-field arrays

Category: B (user_original) -- JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 630-631: Electrostatic energy and energy density.
    Part IV, Ch. XXI: Energy stored in electrified systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree, safe_div, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "ElectrostaticEnergyJAX",
    "CapacitorEnergyJAX",
    "calc_electrostatic_energy_density_jax",
    "calc_energy_density_from_ED_dot_jax",
    "calc_capacitor_energy_jax",
    "calc_total_electrostatic_energy_jax",
    "verify_electrostatic_energy_density_jax",
    "analyze_electrostatic_energy_jax",
]


# ── ElectrostaticEnergyJAX ─────────────────────────────────────────


@jax_tree
@dataclass
class ElectrostaticEnergyJAX:
    """Electrostatic energy stored in an electric field (JAX-compatible).

    Art. 630-631: The energy stored in an electrostatic field is distributed
    throughout the field with energy density proportional to E*D.

    For a linear dielectric (D = eps*E):
        u = (1/8*pi) * eps * E^2  (erg/cm^3)

    Total energy:
        U = (1/8*pi) * int(E*D dV)  (erg)

    Attributes:
        E_field: Electric field vector (statvolt/cm), shape (3,).
        permittivity: Permittivity eps (default 1.0 for vacuum in CGS).
    """

    E_field: jax.Array  # shape (3,)
    permittivity: float = 1.0

    def __post_init__(self):
        self.E_field = jnp.asarray(self.E_field, dtype=jnp.float64)
        self.permittivity = jnp.asarray(self.permittivity, dtype=jnp.float64)

    # ── Properties ────────────────────────────────────────────────

    @property
    def D_field(self) -> jax.Array:
        """Electric displacement field.

        Returns:
            D = eps * E (statcoulombs/cm^2), shape (3,).
        """
        return jnp.asarray(self.permittivity, dtype=jnp.float64) * self.E_field

    @property
    def energy_density(self) -> jax.Array:
        """Electrostatic energy density at a point.

        Art. 630: u = (1/8*pi) * E*D = (1/8*pi) * eps * E^2

        Returns:
            Energy density u (erg/cm^3), scalar.
        """
        E_mag_sq = jnp.dot(self.E_field, self.E_field)
        return (jnp.asarray(self.permittivity, dtype=jnp.float64) / (8.0 * jnp.pi)) * E_mag_sq

    # ── Methods ───────────────────────────────────────────────────

    def total_energy(self, volume: jax.Array) -> jax.Array:
        """Total electrostatic energy in specified volume.

        Art. 630: U = u * V for uniform field in volume V.

        Args:
            volume: Volume in cm^3.

        Returns:
            Total energy U (erg), scalar.
        """
        volume = jnp.asarray(volume, dtype=jnp.float64)
        return self.energy_density * volume

    def energy_density_at(self, E_field: jax.Array) -> jax.Array:
        """Energy density with a custom E field override.

        Art. 630: u = (1/8*pi) * eps * E^2

        Args:
            E_field: Override electric field vector (statvolt/cm), shape (3,).

        Returns:
            Energy density u (erg/cm^3), scalar.
        """
        E_field = jnp.asarray(E_field, dtype=jnp.float64)
        E_mag_sq = jnp.dot(E_field, E_field)
        return (jnp.asarray(self.permittivity, dtype=jnp.float64) / (8.0 * jnp.pi)) * E_mag_sq

    # ── Class methods ─────────────────────────────────────────────

    @classmethod
    def from_E_and_D(
        cls,
        E: jax.Array,
        D: jax.Array,
    ) -> ElectrostaticEnergyJAX:
        """Create from E and D fields directly.

        Art. 630: The general formulation using both E and D fields,
        valid for all dielectrics including anisotropic materials.

        Args:
            E: Electric field vector (statvolt/cm), shape (3,).
            D: Electric displacement vector (statcoulombs/cm^2), shape (3,).

        Returns:
            ElectrostaticEnergyJAX instance.
        """
        E = jnp.asarray(E, dtype=jnp.float64)
        D = jnp.asarray(D, dtype=jnp.float64)
        E_mag_sq = jnp.dot(E, E)
        E_mag = safe_norm(E[None, :], axis=-1)[0]
        # For linear D = eps*E: eps = |D|/|E| when E != 0
        D_mag = safe_norm(D[None, :], axis=-1)[0]
        permittivity = jnp.where(E_mag > 1e-30, D_mag / E_mag, 1.0)
        return cls(E_field=E, permittivity=permittivity)

    # ── JIT-compiled static helpers ───────────────────────────────

    @staticmethod
    @jit
    def _density_jit(E_field: jax.Array, permittivity: float) -> jax.Array:
        """JIT-compiled energy density calculation."""
        E_field = jnp.asarray(E_field, dtype=jnp.float64)
        eps = jnp.asarray(permittivity, dtype=jnp.float64)
        E_mag_sq = jnp.dot(E_field, E_field)
        return (eps / (8.0 * jnp.pi)) * E_mag_sq

    @staticmethod
    @jit
    def _total_energy_jit(
        E_field: jax.Array, permittivity: float, volume: float
    ) -> jax.Array:
        """JIT-compiled total energy calculation."""
        E_field = jnp.asarray(E_field, dtype=jnp.float64)
        eps = jnp.asarray(permittivity, dtype=jnp.float64)
        vol = jnp.asarray(volume, dtype=jnp.float64)
        E_mag_sq = jnp.dot(E_field, E_field)
        return (eps / (8.0 * jnp.pi)) * E_mag_sq * vol


# ── CapacitorEnergyJAX ─────────────────────────────────────────────


@jax_tree
@dataclass
class CapacitorEnergyJAX:
    """Capacitor energy calculator (JAX-compatible pytree).

    Art. 631: The energy stored in a charged capacitor can be expressed as:

        U = (1/2) * C * V^2  (erg)  [when C and V known]
        U = Q^2 / (2*C)  (erg)      [when Q and C known]
        U = (1/2) * Q * V  (erg)    [when Q and V known]

    In CGS, capacitance has dimensions of length (cm).
    1 statfarad = 1 cm.

    Attributes:
        capacitance: Capacitance C (cm in CGS, or statfarads).
    """

    capacitance: float

    def __post_init__(self):
        self.capacitance = jnp.asarray(self.capacitance, dtype=jnp.float64)

    # ── Methods ───────────────────────────────────────────────────

    def from_voltage(self, voltage: jax.Array) -> jax.Array:
        """Energy from capacitance and voltage: U = (1/2) * C * V^2.

        Art. 631.

        Args:
            voltage: Potential difference V (statvolts).

        Returns:
            Stored energy U (erg), scalar.
        """
        V = jnp.asarray(voltage, dtype=jnp.float64)
        C = jnp.asarray(self.capacitance, dtype=jnp.float64)
        return 0.5 * C * V ** 2

    def from_charge(self, charge: jax.Array) -> jax.Array:
        """Energy from capacitance and charge: U = Q^2 / (2*C).

        Art. 631.

        Args:
            charge: Charge Q (statcoulombs).

        Returns:
            Stored energy U (erg), scalar.
        """
        Q = jnp.asarray(charge, dtype=jnp.float64)
        C = jnp.asarray(self.capacitance, dtype=jnp.float64)
        return safe_div(Q ** 2, 2.0 * C, safe_default=0.0)

    def from_QV(self, charge: jax.Array, voltage: jax.Array) -> jax.Array:
        """Energy from charge and voltage: U = (1/2) * Q * V.

        Art. 631.

        Args:
            charge: Charge Q (statcoulombs).
            voltage: Potential difference V (statvolts).

        Returns:
            Stored energy U (erg), scalar.
        """
        Q = jnp.asarray(charge, dtype=jnp.float64)
        V = jnp.asarray(voltage, dtype=jnp.float64)
        return 0.5 * Q * V

    # ── JIT-compiled static helpers ───────────────────────────────

    @staticmethod
    @jit
    def _cv2_jit(capacitance: float, voltage: float) -> jax.Array:
        """JIT-compiled (1/2)*C*V^2."""
        C = jnp.asarray(capacitance, dtype=jnp.float64)
        V = jnp.asarray(voltage, dtype=jnp.float64)
        return 0.5 * C * V ** 2

    @staticmethod
    @jit
    def _q2c_jit(charge: float, capacitance: float) -> jax.Array:
        """JIT-compiled Q^2/(2*C)."""
        Q = jnp.asarray(charge, dtype=jnp.float64)
        C = jnp.asarray(capacitance, dtype=jnp.float64)
        return safe_div(Q ** 2, 2.0 * C, safe_default=0.0)

    @staticmethod
    @jit
    def _qv_jit(charge: float, voltage: float) -> jax.Array:
        """JIT-compiled (1/2)*Q*V."""
        Q = jnp.asarray(charge, dtype=jnp.float64)
        V = jnp.asarray(voltage, dtype=jnp.float64)
        return 0.5 * Q * V


# ── Standalone functions ──────────────────────────────────────────


@maxwell_cite(
    630,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate electrostatic energy density: u = (1/8*pi) * eps * E^2 (JAX)",
)
def calc_electrostatic_energy_density_jax(
    E_field: jax.Array,
    permittivity: float = 1.0,
) -> jax.Array:
    """Calculate electrostatic energy density at a point.

    Art. 630: The energy stored per unit volume in an electrostatic field:

        u = (1/8*pi) * eps * E^2  (erg/cm^3)

    Args:
        E_field: Electric field vector (statvolt/cm), shape (3,).
        permittivity: Permittivity eps (default 1.0 for vacuum in CGS).

    Returns:
        Energy density u (erg/cm^3), scalar.
    """
    E_field = jnp.asarray(E_field, dtype=jnp.float64)
    eps = jnp.asarray(permittivity, dtype=jnp.float64)
    E_mag_sq = jnp.dot(E_field, E_field)
    return (eps / (8.0 * jnp.pi)) * E_mag_sq


@maxwell_cite(
    630,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density from E and D dot product: u = (1/8*pi) * E.D (JAX)",
)
def calc_energy_density_from_ED_dot_jax(
    E_field: jax.Array,
    D_field: jax.Array,
) -> jax.Array:
    """Calculate energy density from E and D fields directly.

    Art. 630: The most general form of electrostatic energy density:

        u = (1/8*pi) * E.D

    This applies to all dielectrics, including nonlinear and anisotropic
    materials where D may not be parallel to E.

    Args:
        E_field: Electric field (statvolt/cm), shape (3,).
        D_field: Electric displacement (statcoulombs/cm^2), shape (3,).

    Returns:
        Energy density u (erg/cm^3), scalar.
    """
    E_field = jnp.asarray(E_field, dtype=jnp.float64)
    D_field = jnp.asarray(D_field, dtype=jnp.float64)
    return jnp.dot(E_field, D_field) / (8.0 * jnp.pi)


@maxwell_cite(
    631,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate capacitor energy: U = (1/2)*C*V^2 or Q^2/(2*C) (JAX)",
)
def calc_capacitor_energy_jax(
    capacitance: float,
    voltage: float | None = None,
    charge: float | None = None,
) -> jax.Array:
    """Calculate electrostatic energy stored in a capacitor.

    Art. 631: The energy stored in a charged capacitor can be expressed as:

        U = (1/2) * C * V^2  (erg)  [when C and V known]
        U = Q^2 / (2*C)  (erg)      [when Q and C known]

    Args:
        capacitance: Capacitance C (cm in CGS).
        voltage: Potential difference V (statvolts).
        charge: Charge Q (statcoulombs).
            At least one of voltage or charge must be provided.

    Returns:
        Stored energy U (erg), scalar.

    Raises:
        ValueError: If neither voltage nor charge provided, or capacitance not positive.
    """
    if voltage is None and charge is None:
        raise ValueError("At least one of voltage or charge must be provided")

    C = jnp.asarray(capacitance, dtype=jnp.float64)

    # U = (1/2) * C * V^2
    if voltage is not None:
        V = jnp.asarray(voltage, dtype=jnp.float64)
        return 0.5 * C * V ** 2

    # U = Q^2 / (2*C)
    Q = jnp.asarray(charge, dtype=jnp.float64)
    return safe_div(Q ** 2, 2.0 * C, safe_default=0.0)


@maxwell_cite(
    630,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate total electrostatic energy: U = u * V (JAX)",
)
def calc_total_electrostatic_energy_jax(
    E_field: jax.Array,
    volume: float,
    permittivity: float = 1.0,
) -> jax.Array:
    """Calculate total electrostatic energy in a volume.

    Art. 630: For uniform field: U = (1/8*pi) * eps * E^2 * V

    Args:
        E_field: Electric field vector (statvolt/cm), shape (3,).
        volume: Volume in cm^3.
        permittivity: Permittivity eps (default 1.0).

    Returns:
        Total energy U (erg), scalar.
    """
    E_field = jnp.asarray(E_field, dtype=jnp.float64)
    eps = jnp.asarray(permittivity, dtype=jnp.float64)
    vol = jnp.asarray(volume, dtype=jnp.float64)
    E_mag_sq = jnp.dot(E_field, E_field)
    return (eps / (8.0 * jnp.pi)) * E_mag_sq * vol


@maxwell_cite(
    630,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify electrostatic energy density formula — isotropy check (JAX)",
)
def verify_electrostatic_energy_density_jax(
    E_magnitude: float = 1000.0,
    permittivity: float = 1.0,
) -> dict[str, jax.Array | bool]:
    """Verify the electrostatic energy density formula.

    Art. 630: This function verifies:

        u = (1/8*pi) * eps * E^2

    by comparing calculations in different field orientations.

    Args:
        E_magnitude: Test field magnitude (statvolt/cm).
        permittivity: Permittivity (default 1.0 for vacuum).

    Returns:
        Dictionary with:
        - energy_density_x: Energy for E along x-axis
        - energy_density_y: Energy for E along y-axis
        - energy_density_z: Energy for E along z-axis
        - expected: Expected value (1/8*pi) * eps * E^2
        - all_match: True if all orientations give same result
        - verified: True if results match expected
    """
    E_mag = jnp.asarray(E_magnitude, dtype=jnp.float64)
    eps = jnp.asarray(permittivity, dtype=jnp.float64)

    E_x = jnp.array([E_mag, 0.0, 0.0])
    E_y = jnp.array([0.0, E_mag, 0.0])
    E_z = jnp.array([0.0, 0.0, E_mag])

    u_x = calc_electrostatic_energy_density_jax(E_x, permittivity)
    u_y = calc_electrostatic_energy_density_jax(E_y, permittivity)
    u_z = calc_electrostatic_energy_density_jax(E_z, permittivity)

    expected = (eps / (8.0 * jnp.pi)) * E_mag ** 2

    tol = 1e-10
    all_match = (
        jnp.isclose(u_x, u_y, rtol=tol)
        and jnp.isclose(u_y, u_z, rtol=tol)
        and jnp.isclose(u_x, expected, rtol=tol)
    )

    return {
        "energy_density_x": u_x,
        "energy_density_y": u_y,
        "energy_density_z": u_z,
        "expected": expected,
        "all_match": bool(all_match),
        "verified": bool(all_match),
    }


@maxwell_cite(
    630, 631,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete electrostatic energy analysis (JAX)",
)
def analyze_electrostatic_energy_jax(
    E_field: jax.Array,
    permittivity: float = 1.0,
    volume: float | None = None,
    capacitance: float | None = None,
    voltage: float | None = None,
) -> dict[str, jax.Array]:
    """Perform comprehensive electrostatic energy analysis.

    Art. 630-631: Complete analysis including:
    1. Energy density from field
    2. Total energy in volume
    3. D field calculation
    4. Capacitor energy (if parameters provided)
    5. Field intensity and direction

    Args:
        E_field: Electric field vector (statvolt/cm), shape (3,).
        permittivity: Permittivity eps (default 1.0).
        volume: Optional volume for total energy (cm^3).
        capacitance: Optional capacitance for capacitor comparison (cm).
        voltage: Optional voltage for capacitor comparison (statvolts).

    Returns:
        Dictionary with:
        - E_field: Input electric field
        - E_magnitude: |E| (statvolt/cm)
        - D_field: Electric displacement (statcoulombs/cm^2)
        - energy_density: u (erg/cm^3)
        - total_energy: U (erg, if volume provided)
        - capacitor_energy: U_cap (erg, if C and V provided)
        - energy_ratio: field_energy / capacitor_energy
    """
    E_field = jnp.asarray(E_field, dtype=jnp.float64)
    eps = jnp.asarray(permittivity, dtype=jnp.float64)

    E_mag = safe_norm(E_field[None, :], axis=-1)[0]
    E_direction = jnp.where(
        E_mag > 1e-30,
        E_field / E_mag,
        jnp.zeros(3),
    )

    D_field = eps * E_field

    energy_density = calc_electrostatic_energy_density_jax(E_field, permittivity)

    result: dict[str, jax.Array] = {
        "E_field": E_field,
        "E_magnitude": E_mag,
        "E_direction": E_direction,
        "D_field": D_field,
        "permittivity": eps,
        "energy_density": energy_density,
    }

    if volume is not None:
        vol = jnp.asarray(volume, dtype=jnp.float64)
        result["volume"] = vol
        result["total_energy"] = energy_density * vol

    if capacitance is not None and voltage is not None:
        cap_energy = calc_capacitor_energy_jax(capacitance, voltage)
        result["capacitor_energy"] = cap_energy
        if volume is not None:
            field_energy = energy_density * jnp.asarray(volume, dtype=jnp.float64)
            result["energy_ratio"] = safe_div(field_energy, cap_energy, safe_default=0.0)

    return result
