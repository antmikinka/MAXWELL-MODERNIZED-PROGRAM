"""
JAX-compatible magnetic energy -- Part IV (Electromagnetic Energy).

Provides MagneticEnergyJAX and InductorEnergyJAX: JAX-pytree versions
of maxwell.electromagnetism.energy.magnetic.MagneticEnergy that
support JIT compilation, automatic differentiation, and batched evaluation
via vmap over magnetic field configurations simultaneously.

Implements Maxwell's magnetic energy formulas from Articles 632-633:

- Energy density: u = (1/8*pi) * B*H = (1/8*pi) * mu * H^2  (Art. 632)
- Total energy: U = (1/8*pi) * int(B*H dV)  (Art. 632)
- Inductor energy: U = (1/2)*L*I^2 = Phi^2/(2*L) = (1/2)*Phi*I  (Art. 633)

All computations use CGS-EMU units:
    H in oersted, energy density in erg/cm^3, energy in erg

Key differences from the NumPy version:
- Uses jax.numpy exclusively (no np.* calls)
- Safe norm via jnp.where (no Python if/else on array values)
- Pytree-registered for jax.jit, jax.grad, jax.vmap compatibility
- Batch-aware: vmap works over (N, 3) H-field arrays

Category: B (user_original) -- JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 632-633: Magnetic energy and energy density.
    Part IV, Ch. XXI: Energy stored in magnetic systems.
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
    "MagneticEnergyJAX",
    "InductorEnergyJAX",
    "calc_magnetic_energy_density_jax",
    "calc_energy_density_from_BH_dot_jax",
    "calc_inductor_energy_jax",
    "calc_total_magnetic_energy_jax",
    "verify_magnetic_energy_density_jax",
    "analyze_magnetic_energy_jax",
]


# -- MagneticEnergyJAX --


@jax_tree
@dataclass
class MagneticEnergyJAX:
    """Magnetic energy stored in a magnetic field (JAX-compatible).

    Art. 632-633: The energy stored in a magnetic field is distributed
    throughout the field with energy density proportional to B*H.

    For a linear magnetic material (B = mu*H):
        u = (1/8*pi) * mu * H^2  (erg/cm^3)

    Total energy:
        U = (1/8*pi) * int(B*H dV)  (erg)

    Attributes:
        H_field: Magnetic field intensity vector (oersted), shape (3,).
        permeability: Permeability mu (default 1.0 for vacuum in CGS).
    """

    H_field: jax.Array  # shape (3,)
    permeability: float = 1.0

    def __post_init__(self):
        self.H_field = jnp.asarray(self.H_field, dtype=jnp.float64)
        self.permeability = jnp.asarray(self.permeability, dtype=jnp.float64)

    # -- Properties --

    @property
    def B_field(self) -> jax.Array:
        """Magnetic flux density field.

        Returns:
            B = mu * H (gauss), shape (3,).
        """
        return jnp.asarray(self.permeability, dtype=jnp.float64) * self.H_field

    @property
    def energy_density(self) -> jax.Array:
        """Magnetic energy density at a point.

        Art. 632: u = (1/8*pi) * mu * H^2

        Returns:
            Energy density u (erg/cm^3), scalar.
        """
        H_mag_sq = jnp.dot(self.H_field, self.H_field)
        return (
            jnp.asarray(self.permeability, dtype=jnp.float64) / (8.0 * jnp.pi)
        ) * H_mag_sq

    # -- Methods --

    def total_energy(self, volume: jax.Array) -> jax.Array:
        """Total magnetic energy in specified volume.

        Art. 632: U = u * V for uniform field in volume V.

        Args:
            volume: Volume in cm^3.

        Returns:
            Total energy U (erg), scalar.
        """
        volume = jnp.asarray(volume, dtype=jnp.float64)
        return self.energy_density * volume

    def energy_density_at(self, H_field: jax.Array) -> jax.Array:
        """Energy density with a custom H field override.

        Art. 632: u = (1/8*pi) * mu * H^2

        Args:
            H_field: Override magnetic field vector (oersted), shape (3,).

        Returns:
            Energy density u (erg/cm^3), scalar.
        """
        H_field = jnp.asarray(H_field, dtype=jnp.float64)
        H_mag_sq = jnp.dot(H_field, H_field)
        return (
            jnp.asarray(self.permeability, dtype=jnp.float64) / (8.0 * jnp.pi)
        ) * H_mag_sq

    # -- Class methods --

    @classmethod
    def from_B_and_H(
        cls,
        B: jax.Array,
        H: jax.Array,
    ) -> MagneticEnergyJAX:
        """Create from B and H fields directly.

        Art. 632: The general formulation using both B and H fields,
        valid for all magnetic materials including anisotropic materials.

        Args:
            B: Magnetic flux density (gauss), shape (3,).
            H: Magnetic field intensity (oersted), shape (3,).

        Returns:
            MagneticEnergyJAX instance.
        """
        B = jnp.asarray(B, dtype=jnp.float64)
        H = jnp.asarray(H, dtype=jnp.float64)
        H_mag_sq = jnp.dot(H, H)
        H_mag = safe_norm(H[None, :], axis=-1)[0]
        # For linear B = mu*H: mu = |B|/|H| when H != 0
        B_mag = safe_norm(B[None, :], axis=-1)[0]
        permeability = jnp.where(H_mag > 1e-30, B_mag / H_mag, 1.0)
        return cls(H_field=H, permeability=permeability)

    # -- JIT-compiled static helpers --

    @staticmethod
    @jit
    def _density_jit(H_field: jax.Array, permeability: float) -> jax.Array:
        """JIT-compiled energy density calculation."""
        H_field = jnp.asarray(H_field, dtype=jnp.float64)
        mu = jnp.asarray(permeability, dtype=jnp.float64)
        H_mag_sq = jnp.dot(H_field, H_field)
        return (mu / (8.0 * jnp.pi)) * H_mag_sq

    @staticmethod
    @jit
    def _total_energy_jit(
        H_field: jax.Array, permeability: float, volume: float
    ) -> jax.Array:
        """JIT-compiled total energy calculation."""
        H_field = jnp.asarray(H_field, dtype=jnp.float64)
        mu = jnp.asarray(permeability, dtype=jnp.float64)
        vol = jnp.asarray(volume, dtype=jnp.float64)
        H_mag_sq = jnp.dot(H_field, H_field)
        return (mu / (8.0 * jnp.pi)) * H_mag_sq * vol


# -- InductorEnergyJAX --


@jax_tree
@dataclass
class InductorEnergyJAX:
    """Inductor energy calculator (JAX-compatible pytree).

    Art. 633: The energy stored in an inductor can be expressed as:

        U = (1/2) * L * I^2  (erg)  [when L and I known]
        U = Phi^2 / (2*L)  (erg)      [when Phi and L known]
        U = (1/2) * Phi * I  (erg)    [when Phi and I known]

    In CGS, inductance has dimensions of length (cm).
    1 abhenry = 1 cm.

    Attributes:
        inductance: Inductance L (cm in CGS, or abhenries).
    """

    inductance: float

    def __post_init__(self):
        self.inductance = jnp.asarray(self.inductance, dtype=jnp.float64)

    # -- Methods --

    def from_current(self, current: jax.Array) -> jax.Array:
        """Energy from inductance and current: U = (1/2) * L * I^2.

        Art. 633.

        Args:
            current: Current I (abamperes).

        Returns:
            Stored energy U (erg), scalar.
        """
        I = jnp.asarray(current, dtype=jnp.float64)
        L = jnp.asarray(self.inductance, dtype=jnp.float64)
        return 0.5 * L * I**2

    def from_flux(self, flux: jax.Array) -> jax.Array:
        """Energy from flux and inductance: U = Phi^2 / (2*L).

        Art. 633.

        Args:
            flux: Magnetic flux Phi (maxwells).

        Returns:
            Stored energy U (erg), scalar.
        """
        Phi = jnp.asarray(flux, dtype=jnp.float64)
        L = jnp.asarray(self.inductance, dtype=jnp.float64)
        return safe_div(Phi**2, 2.0 * L, safe_default=0.0)

    def from_flux_current(self, flux: jax.Array, current: jax.Array) -> jax.Array:
        """Energy from flux and current: U = (1/2) * Phi * I.

        Art. 633.

        Args:
            flux: Magnetic flux Phi (maxwells).
            current: Current I (abamperes).

        Returns:
            Stored energy U (erg), scalar.
        """
        Phi = jnp.asarray(flux, dtype=jnp.float64)
        I = jnp.asarray(current, dtype=jnp.float64)
        return 0.5 * Phi * I

    # -- JIT-compiled static helpers --

    @staticmethod
    @jit
    def _li2_jit(inductance: float, current: float) -> jax.Array:
        """JIT-compiled (1/2)*L*I^2."""
        L = jnp.asarray(inductance, dtype=jnp.float64)
        I = jnp.asarray(current, dtype=jnp.float64)
        return 0.5 * L * I**2

    @staticmethod
    @jit
    def _phi2l_jit(flux: float, inductance: float) -> jax.Array:
        """JIT-compiled Phi^2/(2*L)."""
        Phi = jnp.asarray(flux, dtype=jnp.float64)
        L = jnp.asarray(inductance, dtype=jnp.float64)
        return safe_div(Phi**2, 2.0 * L, safe_default=0.0)

    @staticmethod
    @jit
    def _phi_i_jit(flux: float, current: float) -> jax.Array:
        """JIT-compiled (1/2)*Phi*I."""
        Phi = jnp.asarray(flux, dtype=jnp.float64)
        I = jnp.asarray(current, dtype=jnp.float64)
        return 0.5 * Phi * I


# -- Standalone functions --


@maxwell_cite(
    632,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate magnetic energy density: u = (1/8*pi) * mu * H^2 (JAX)",
)
def calc_magnetic_energy_density_jax(
    H_field: jax.Array,
    permeability: float = 1.0,
) -> jax.Array:
    """Calculate magnetic energy density at a point.

    Art. 632: The energy stored per unit volume in a magnetic field:

        u = (1/8*pi) * mu * H^2  (erg/cm^3)

    Args:
        H_field: Magnetic field intensity vector (oersted), shape (3,).
        permeability: Permeability mu (default 1.0 for vacuum in CGS).

    Returns:
        Energy density u (erg/cm^3), scalar.
    """
    H_field = jnp.asarray(H_field, dtype=jnp.float64)
    mu = jnp.asarray(permeability, dtype=jnp.float64)
    H_mag_sq = jnp.dot(H_field, H_field)
    return (mu / (8.0 * jnp.pi)) * H_mag_sq


@maxwell_cite(
    632,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density from B and H dot product: u = (1/8*pi) * B.H (JAX)",
)
def calc_energy_density_from_BH_dot_jax(
    B_field: jax.Array,
    H_field: jax.Array,
) -> jax.Array:
    """Calculate energy density from B and H fields directly.

    Art. 632: The most general form of magnetic energy density:

        u = (1/8*pi) * B.H

    This applies to all magnetic materials, including nonlinear and
    anisotropic materials where B may not be parallel to H.

    Args:
        B_field: Magnetic flux density (gauss), shape (3,).
        H_field: Magnetic field intensity (oersted), shape (3,).

    Returns:
        Energy density u (erg/cm^3), scalar.
    """
    B_field = jnp.asarray(B_field, dtype=jnp.float64)
    H_field = jnp.asarray(H_field, dtype=jnp.float64)
    return jnp.dot(B_field, H_field) / (8.0 * jnp.pi)


@maxwell_cite(
    633,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate inductor energy: U = (1/2)*L*I^2 or Phi^2/(2*L) (JAX)",
)
def calc_inductor_energy_jax(
    inductance: float,
    current: float | None = None,
    flux: float | None = None,
) -> jax.Array:
    """Calculate magnetic energy stored in an inductor.

    Art. 633: The energy stored in an inductor can be expressed as:

        U = (1/2) * L * I^2  (erg)  [when L and I known]
        U = Phi^2 / (2*L)  (erg)      [when Phi and L known]

    Args:
        inductance: Inductance L (cm in CGS).
        current: Current I (abamperes).
        flux: Magnetic flux Phi (maxwells).
            At least one of current or flux must be provided.

    Returns:
        Stored energy U (erg), scalar.

    Raises:
        ValueError: If neither current nor flux provided.
    """
    if current is None and flux is None:
        raise ValueError("At least one of current or flux must be provided")

    L = jnp.asarray(inductance, dtype=jnp.float64)

    # U = (1/2) * L * I^2
    if current is not None:
        I = jnp.asarray(current, dtype=jnp.float64)
        return 0.5 * L * I**2

    # U = Phi^2 / (2*L)
    Phi = jnp.asarray(flux, dtype=jnp.float64)
    return safe_div(Phi**2, 2.0 * L, safe_default=0.0)


@maxwell_cite(
    632,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate total magnetic energy: U = u * V (JAX)",
)
def calc_total_magnetic_energy_jax(
    H_field: jax.Array,
    volume: float,
    permeability: float = 1.0,
) -> jax.Array:
    """Calculate total magnetic energy in a volume.

    Art. 632: For uniform field: U = (1/8*pi) * mu * H^2 * V

    Args:
        H_field: Magnetic field intensity vector (oersted), shape (3,).
        volume: Volume in cm^3.
        permeability: Permeability mu (default 1.0).

    Returns:
        Total energy U (erg), scalar.
    """
    H_field = jnp.asarray(H_field, dtype=jnp.float64)
    mu = jnp.asarray(permeability, dtype=jnp.float64)
    vol = jnp.asarray(volume, dtype=jnp.float64)
    H_mag_sq = jnp.dot(H_field, H_field)
    return (mu / (8.0 * jnp.pi)) * H_mag_sq * vol


@maxwell_cite(
    632,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify magnetic energy density formula -- isotropy check (JAX)",
)
def verify_magnetic_energy_density_jax(
    H_magnitude: float = 1000.0,
    permeability: float = 1.0,
) -> dict[str, jax.Array | bool]:
    """Verify the magnetic energy density formula.

    Art. 632: This function verifies:

        u = (1/8*pi) * mu * H^2

    by comparing calculations in different field orientations.

    Args:
        H_magnitude: Test field magnitude (oersted).
        permeability: Permeability (default 1.0 for vacuum).

    Returns:
        Dictionary with:
        - energy_density_x: Energy for H along x-axis
        - energy_density_y: Energy for H along y-axis
        - energy_density_z: Energy for H along z-axis
        - expected: Expected value (1/8*pi) * mu * H^2
        - all_match: True if all orientations give same result
        - verified: True if results match expected
    """
    H_mag = jnp.asarray(H_magnitude, dtype=jnp.float64)
    mu = jnp.asarray(permeability, dtype=jnp.float64)

    H_x = jnp.array([H_mag, 0.0, 0.0])
    H_y = jnp.array([0.0, H_mag, 0.0])
    H_z = jnp.array([0.0, 0.0, H_mag])

    u_x = calc_magnetic_energy_density_jax(H_x, permeability)
    u_y = calc_magnetic_energy_density_jax(H_y, permeability)
    u_z = calc_magnetic_energy_density_jax(H_z, permeability)

    expected = (mu / (8.0 * jnp.pi)) * H_mag**2

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
    632,
    633,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete magnetic energy analysis (JAX)",
)
def analyze_magnetic_energy_jax(
    H_field: jax.Array,
    permeability: float = 1.0,
    volume: float | None = None,
    inductance: float | None = None,
    current: float | None = None,
) -> dict[str, jax.Array]:
    """Perform comprehensive magnetic energy analysis.

    Art. 632-633: Complete analysis including:
    1. Energy density from field
    2. Total energy in volume
    3. B field calculation
    4. Inductor energy (if parameters provided)
    5. Field intensity and direction

    Args:
        H_field: Magnetic field intensity vector (oersted), shape (3,).
        permeability: Permeability mu (default 1.0).
        volume: Optional volume for total energy (cm^3).
        inductance: Optional inductance for inductor comparison (cm).
        current: Optional current for inductor comparison (abamperes).

    Returns:
        Dictionary with:
        - H_field: Input magnetic field
        - H_magnitude: |H| (oersted)
        - B_field: Magnetic flux density (gauss)
        - energy_density: u (erg/cm^3)
        - total_energy: U (erg, if volume provided)
        - inductor_energy: U_L (erg, if L and I provided)
        - energy_ratio: field_energy / inductor_energy
    """
    H_field = jnp.asarray(H_field, dtype=jnp.float64)
    mu = jnp.asarray(permeability, dtype=jnp.float64)

    H_mag = safe_norm(H_field[None, :], axis=-1)[0]
    H_direction = jnp.where(
        H_mag > 1e-30,
        H_field / H_mag,
        jnp.zeros(3),
    )

    B_field = mu * H_field

    energy_density = calc_magnetic_energy_density_jax(H_field, permeability)

    result: dict[str, jax.Array] = {
        "H_field": H_field,
        "H_magnitude": H_mag,
        "H_direction": H_direction,
        "B_field": B_field,
        "permeability": mu,
        "energy_density": energy_density,
    }

    if volume is not None:
        vol = jnp.asarray(volume, dtype=jnp.float64)
        result["volume"] = vol
        result["total_energy"] = energy_density * vol

    if inductance is not None and current is not None:
        ind_energy = calc_inductor_energy_jax(inductance, current)
        result["inductor_energy"] = ind_energy
        if volume is not None:
            field_energy = energy_density * jnp.asarray(volume, dtype=jnp.float64)
            result["energy_ratio"] = safe_div(
                field_energy, ind_energy, safe_default=0.0
            )

    return result
