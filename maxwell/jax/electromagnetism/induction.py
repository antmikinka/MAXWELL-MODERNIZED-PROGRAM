"""
JAX-compatible Faraday electromagnetic induction.

Provides FaradayInductionJAX: a JAX-pytree version of
maxwell.electromagnetism.induction.faraday.FaradayInduction
that supports JIT compilation, automatic differentiation, and batched evaluation
via vmap over magnetic field configurations simultaneously.

Implements Michael Faraday's 1831 discovery of electromagnetic induction,
as described by Maxwell in Articles 528-531 and 542:

- Electromagnetic induction phenomenon (Art. 528)
- Faraday's law: EMF = -N * dΦ/dt (Art. 529)
- Magnetic flux: Φ = B · n̂ * A (Art. 530)
- Motional EMF: EMF = |v × B| * ℓ (Art. 529-530)
- Lenz's Law: induced current opposes the change (Art. 542)

All computations use CGS-EMU units:
    B in gauss, area in cm², flux in maxwells
    EMF in abvolts, current in abamperes

Key differences from the NumPy version:
- Uses jax.numpy exclusively (no np.* calls)
- Safe division via jnp.where (no Python if/else on array values)
- Pytree-registered for jax.jit, jax.grad, jax.vmap compatibility
- Batch-aware: vmap works over (N, 3) B-field arrays

Category: B (user_original) — JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 528-531: Faraday's law of induction.
    Part IV, Art. 542: Lenz's law and direction of induced currents.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree, safe_div, safe_norm
from maxwell.meta.citation import maxwell_cite

__all__ = [
    "FaradayInductionJAX",
    "analyze_faraday_induction_jax",
]

# Default normal vector (z-axis) — used when normal is not specified.
_Z_AXIS = jnp.array([0.0, 0.0, 1.0])


# ── FaradayInductionJAX ─────────────────────────────────────────


@jax_tree
@dataclass
class FaradayInductionJAX:
    """Faraday electromagnetic induction calculator (JAX-compatible).

    Art. 528-531, 542: Unified interface for computing magnetic flux,
    induced EMF (Faraday's law), motional EMF, and Lenz's law direction
    verification — all differentiable and JIT-compileable.

    Attributes:
        num_turns: Number of turns in the coil (integer, traced).
        resistance: Circuit resistance for current calculations (abohms in EMU).
            Use None if resistance is not needed.

    Example:
        >>> import jax.numpy as jnp
        >>> from maxwell.jax.electromagnetism.induction import FaradayInductionJAX
        >>> coil = FaradayInductionJAX(num_turns=100, resistance=50.0)
        >>> flux = coil.magnetic_flux(
        ...     B_field=jnp.array([0.0, 0.0, 1000.0]),
        ...     area=10.0,
        ...     normal=jnp.array([0.0, 0.0, 1.0]),
        ... )
        >>> emf = coil.induced_emf(flux_change_rate=10000.0)
    """

    num_turns: int
    resistance: float | None = None

    def __post_init__(self):
        # Ensure resistance is a JAX array when present for tracing.
        if self.resistance is not None:
            self.resistance = float(self.resistance)

    # ── Magnetic flux ───────────────────────────────────────────

    def magnetic_flux(
        self,
        B_field: jax.Array,
        area: float,
        normal: jax.Array | None = None,
    ) -> jax.Array:
        """Magnetic flux through a surface: Φ = (B · n̂) * A, total for N turns.

        Art. 528-530: For a coil with N turns, the total flux linkage is
        N times the flux per turn.  The normal is normalized if supplied,
        defaulting to the z-axis.

        Args:
            B_field: Magnetic flux density vector (gauss), shape (3,).
            area: Surface area (cm²).
            normal: Optional unit normal vector (default: z-axis), shape (3,).

        Returns:
            Total magnetic flux for all N turns (maxwells), scalar.
        """
        B_field = jnp.asarray(B_field, dtype=jnp.float64)
        if normal is None:
            n = _Z_AXIS
        else:
            n = jnp.asarray(normal, dtype=jnp.float64)
            n_mag = safe_norm(n[None, :], axis=-1)[0]
            n = jnp.where(n_mag > 1e-30, n / n_mag, _Z_AXIS)

        flux_per_turn = area * jnp.dot(B_field, n)
        return jnp.asarray(self.num_turns, dtype=jnp.float64) * flux_per_turn

    # ── Induced EMF (Faraday's law) ─────────────────────────────

    def induced_emf(self, flux_change_rate: jax.Array) -> jax.Array:
        """Induced electromotive force: EMF = -N * dΦ/dt.

        Art. 529-531: Faraday's law for N turns.  The negative sign
        encodes Lenz's law (Art. 542).

        Args:
            flux_change_rate: Rate of flux change per turn dΦ/dt (maxwells/s).

        Returns:
            Induced EMF (abvolts in EMU), scalar.
        """
        rate = jnp.asarray(flux_change_rate, dtype=jnp.float64)
        total_rate = jnp.asarray(self.num_turns, dtype=jnp.float64) * rate
        return -total_rate

    # ── Motional EMF ────────────────────────────────────────────

    def motional_emf(
        self,
        velocity: jax.Array,
        B_field: jax.Array,
        length: jax.Array,
    ) -> jax.Array:
        """Motional EMF for a conductor moving in a magnetic field.

        Art. 529-530: EMF = ∮(v × B)·dl.  For a straight conductor of
        length ℓ the magnitude is |v × B| * ℓ, scaled by N turns.

        Args:
            velocity: Velocity vector (cm/s), shape (3,).
            B_field: Magnetic flux density (gauss), shape (3,).
            length: Conductor length in the field (cm).

        Returns:
            Total motional EMF (abvolts), scalar.
        """
        B_field = jnp.asarray(B_field, dtype=jnp.float64)
        velocity = jnp.asarray(velocity, dtype=jnp.float64)
        length = jnp.asarray(length, dtype=jnp.float64)

        v_cross_B = jnp.cross(velocity, B_field)
        emf_per_conductor = safe_norm(v_cross_B[None, :], axis=-1)[0] * length
        return jnp.asarray(self.num_turns, dtype=jnp.float64) * emf_per_conductor

    # ── Lenz's law check ────────────────────────────────────────

    def lenz_law_check(
        self,
        applied_flux_change: jax.Array,
        induced_current: jax.Array,
    ) -> jax.Array:
        """Verify that the induced current opposes the flux change.

        Art. 542: Lenz's law states the induced current creates a magnetic
        field that opposes the change in flux that produced it.  Equivalently,
        EMF and dΦ/dt must have opposite signs, i.e.  EMF * dΦ/dt <= 0.

        Here we use the sign of (applied_flux_change * induced_current):
        if the current correctly opposes, the product is negative (or zero).

        Args:
            applied_flux_change: ΔΦ through one turn (maxwells).
            induced_current: Induced current (abamperes).

        Returns:
            Boolean scalar — True if the induced current opposes the change.
        """
        dphi = jnp.asarray(applied_flux_change, dtype=jnp.float64)
        curr = jnp.asarray(induced_current, dtype=jnp.float64)
        # Opposes change when product is <= 0 (EMF opposes dΦ/dt).
        return dphi * curr <= 0.0

    # ── JIT-compiled static helpers ─────────────────────────────

    @staticmethod
    @jit
    def _flux_jit(
        num_turns: int,
        B_field: jax.Array,
        area: float,
        normal: jax.Array,
    ) -> jax.Array:
        """JIT-compiled magnetic flux (static helper for scan / control flow)."""
        n_mag = safe_norm(normal[None, :], axis=-1)[0]
        n = jnp.where(n_mag > 1e-30, normal / n_mag, _Z_AXIS)
        flux_per_turn = area * jnp.dot(B_field, n)
        return jnp.asarray(num_turns, dtype=jnp.float64) * flux_per_turn

    @staticmethod
    @jit
    def _emf_jit(num_turns: int, flux_change_rate: jax.Array) -> jax.Array:
        """JIT-compiled Faraday EMF."""
        return -jnp.asarray(num_turns, dtype=jnp.float64) * jnp.asarray(
            flux_change_rate, dtype=jnp.float64
        )

    @staticmethod
    @jit
    def _motional_emf_jit(
        num_turns: int,
        B_field: jax.Array,
        length: jax.Array,
        velocity: jax.Array,
    ) -> jax.Array:
        """JIT-compiled motional EMF."""
        v_cross_B = jnp.cross(velocity, B_field)
        emf_per = safe_norm(v_cross_B[None, :], axis=-1)[0] * length
        return jnp.asarray(num_turns, dtype=jnp.float64) * emf_per


# ── Batched evaluation helpers ───────────────────────────────────


@maxwell_cite(
    528,
    529,
    530,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Magnetic flux over a batch of B-field configurations via vmap",
)
def flux_over_batch(
    coil: FaradayInductionJAX,
    B_fields: jax.Array,
    area: float,
    normal: jax.Array,
) -> jax.Array:
    """Magnetic flux computed over a batch of B-field vectors.

    Args:
        coil: FaradayInductionJAX instance.
        B_fields: Array of B-field vectors, shape (N, 3) (gauss).
        area: Surface area (cm²).
        normal: Unit normal vector, shape (3,).

    Returns:
        Flux per configuration (maxwells), shape (N,).
    """
    return vmap(lambda B: coil.magnetic_flux(B, area, normal))(B_fields)


@maxwell_cite(
    529,
    531,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Induced EMF over a batch of flux change rates via vmap",
)
def emf_over_batch(
    coil: FaradayInductionJAX,
    flux_rates: jax.Array,
) -> jax.Array:
    """Induced EMF computed over a batch of flux change rates.

    Args:
        coil: FaradayInductionJAX instance.
        flux_rates: Array of dΦ/dt values (maxwells/s), shape (N,).

    Returns:
        Induced EMF per configuration (abvolts), shape (N,).
    """
    return vmap(coil.induced_emf)(flux_rates)


# ── Complete Faraday induction analysis ─────────────────────────


@maxwell_cite(
    528,
    529,
    530,
    531,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Complete Faraday induction analysis for a multi-turn coil (JAX)",
)
def analyze_faraday_induction_jax(
    B_initial: jax.Array,
    B_final: jax.Array,
    loop_area: float,
    loop_normal: jax.Array,
    time_interval: jax.Array,
    resistance: jax.Array,
    num_turns: int = 1,
) -> dict[str, jax.Array]:
    """Complete Faraday induction analysis for a multi-turn coil.

    Art. 528-531: Computes initial/final flux, flux change, induced EMF,
    induced current, and total charge transferred for a coil whose
    magnetic field changes from B_initial to B_final over time_interval.

    All outputs are JAX arrays in CGS-EMU units and are JIT / grad / vmap
    compatible.

    Args:
        B_initial: Initial magnetic field vector (gauss), shape (3,).
        B_final: Final magnetic field vector (gauss), shape (3,).
        loop_area: Area of each turn (cm²).
        loop_normal: Normal vector to loop plane, shape (3,).
            Will be normalized internally.
        time_interval: Time for the field change (seconds).
        resistance: Total circuit resistance (abohms in EMU).
        num_turns: Number of turns in the coil (default: 1).

    Returns:
        Dictionary with keys:
            flux_initial       – Initial flux per turn (maxwells)
            flux_final         – Final flux per turn (maxwells)
            flux_change        – ΔΦ per turn (maxwells)
            total_flux_change  – N * ΔΦ (maxwells)
            flux_change_rate   – Average dΦ/dt (maxwells/s)
            average_emf        – Induced EMF (abvolts)
            average_current    – Induced current (abamperes)
            charge_transferred – Total charge that flowed (abcoulombs)

    Reference:
        Part IV, Arts. 528-531: Complete Faraday induction analysis.

    Example:
        >>> B0 = jnp.array([0.0, 0.0, 0.0])
        >>> B1 = jnp.array([0.0, 0.0, 1000.0])
        >>> result = analyze_faraday_induction_jax(
        ...     B_initial=B0,
        ...     B_final=B1,
        ...     loop_area=10.0,
        ...     loop_normal=jnp.array([0.0, 0.0, 1.0]),
        ...     time_interval=0.5,
        ...     resistance=100.0,
        ...     num_turns=100,
        ... )
        >>> print(f"EMF = {result['average_emf']} abvolts")
    """
    B_initial = jnp.asarray(B_initial, dtype=jnp.float64)
    B_final = jnp.asarray(B_final, dtype=jnp.float64)
    loop_normal = jnp.asarray(loop_normal, dtype=jnp.float64)
    time_interval = jnp.asarray(time_interval, dtype=jnp.float64)
    resistance = jnp.asarray(resistance, dtype=jnp.float64)
    N = jnp.asarray(num_turns, dtype=jnp.float64)

    # Normalize the loop normal — safe against zero vectors.
    normal_mag = safe_norm(loop_normal[None, :], axis=-1)[0]
    n = jnp.where(normal_mag > 1e-30, loop_normal / normal_mag, _Z_AXIS)

    # Flux per turn: Φ = A * (B · n̂)
    flux_initial = loop_area * jnp.dot(B_initial, n)
    flux_final = loop_area * jnp.dot(B_final, n)
    flux_change = flux_final - flux_initial

    # Total flux change for N turns
    total_flux_change = N * flux_change

    # Average rate of flux change — safe division.
    flux_change_rate = safe_div(total_flux_change, time_interval, safe_default=0.0)

    # Faraday's law: EMF = -N * dΦ/dt
    average_emf = -N * flux_change_rate

    # Ohm's law: I = EMF / R — safe division.
    average_current = safe_div(average_emf, resistance, safe_default=0.0)

    # Total charge transferred: Q = -N * ΔΦ / R
    charge_transferred = safe_div(-total_flux_change, resistance, safe_default=0.0)

    return {
        "flux_initial": flux_initial,
        "flux_final": flux_final,
        "flux_change": flux_change,
        "total_flux_change": total_flux_change,
        "flux_change_rate": flux_change_rate,
        "average_emf": average_emf,
        "average_current": average_current,
        "charge_transferred": charge_transferred,
        "num_turns": num_turns,
    }


# ── Gradient helpers (demonstrate auto-differentiation) ──────────


@maxwell_cite(
    529,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Gradient of induced EMF w.r.t. flux_change_rate via jax.grad",
)
def emf_wrt_flux_rate(
    num_turns: int,
    flux_change_rate: jax.Array,
) -> jax.Array:
    """Gradient of induced EMF with respect to flux_change_rate.

    Should always return -N, demonstrating that JAX auto-differentiates
    Faraday's law correctly.

    Args:
        num_turns: Number of coil turns.
        flux_change_rate: dΦ/dt value (maxwells/s).

    Returns:
        d(EMF)/d(dΦ/dt), scalar (should equal -N).
    """
    N = jnp.asarray(num_turns, dtype=jnp.float64)

    def emf_fn(rate):
        return -N * rate

    return grad(emf_fn)(jnp.asarray(flux_change_rate, dtype=jnp.float64))


@maxwell_cite(
    528,
    529,
    530,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Gradient of magnetic flux w.r.t. B-field vector via jax.grad",
)
def flux_wrt_bfield(
    num_turns: int,
    B_field: jax.Array,
    area: float,
    normal: jax.Array,
) -> jax.Array:
    """Gradient of magnetic flux with respect to the B-field vector.

    Should return N * area * n̂, demonstrating vector-valued gradients.

    Args:
        num_turns: Number of coil turns.
        B_field: Magnetic field vector (gauss), shape (3,).
        area: Surface area (cm²).
        normal: Unit normal vector, shape (3,).

    Returns:
        ∇_B Φ, shape (3,).
    """
    N = jnp.asarray(num_turns, dtype=jnp.float64)
    n = jnp.asarray(normal, dtype=jnp.float64)
    B = jnp.asarray(B_field, dtype=jnp.float64)

    def flux_fn(B_vec):
        return N * area * jnp.dot(B_vec, n)

    return grad(flux_fn)(B)
