"""Electrokinetic energy -- JAX implementations for Arts. 634-638.

Energy stored in the magnetic field produced by electric currents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree

__all__ = [
    "ElectrokineticEnergyJAX",
    "CoupledCircuitEnergyJAX",
    "calc_electrokinetic_energy_jax",
    "calc_single_circuit_energy_jax",
    "calc_coupled_circuits_energy_jax",
    "calc_mutual_inductance_energy_jax",
    "calc_two_circuit_energy_jax",
    "calc_coupling_coefficient_jax",
    "verify_coupled_circuits_energy_jax",
    "analyze_electrokinetic_energy_jax",
]


# -- Data classes -------------------------------------------------------------------

@jax_tree
@dataclass
class ElectrokineticEnergyJAX:
    """Electrokinetic energy of current-carrying circuits (JAX-compatible).

    Art. 634-638: Energy stored in the magnetic field produced by electric currents.

    Field formulation:  T = (1/2) integral(A . J dV)
    Circuit formulation: T = (1/2) sum(L_ij I_i I_j)
    """

    inductance: Optional[float] = None
    current: Optional[float] = None
    inductance_matrix: Optional[jax.Array] = None
    currents: Optional[jax.Array] = None

    @property
    def energy(self) -> jax.Array:
        """Calculate total electrokinetic energy in erg."""
        if self.inductance is not None and self.current is not None:
            return self._single_energy_jit(self.inductance, self.current)
        if self.inductance_matrix is not None and self.currents is not None:
            return self._coupled_energy_jit(self.inductance_matrix, self.currents)
        return jnp.array(0.0)

    @classmethod
    def from_single_circuit(cls, inductance: float, current: float) -> "ElectrokineticEnergyJAX":
        """Single circuit energy T = (1/2) * L * I^2. Art. 635."""
        return cls(inductance=inductance, current=current)

    @classmethod
    def from_coupled_circuits(cls, inductance_matrix: jax.Array, currents: jax.Array) -> "ElectrokineticEnergyJAX":
        """Coupled circuits energy T = (1/2) * I^T . L . I. Arts. 636-637."""
        return cls(inductance_matrix=inductance_matrix, currents=currents)

    def energy_from_fields(self, A_potential: jax.Array, J_current: jax.Array, volume: float) -> jax.Array:
        """Field formulation: T = (1/2) * A . J * V. Art. 634."""
        return self._fields_energy_jit(A_potential, J_current, volume)

    def energy_from_two_circuits(self, L1: float, L2: float, M: float, I1: float, I2: float) -> jax.Array:
        """Two coupled circuits energy. Arts. 636-637."""
        return self._two_circuit_energy_jit(L1, L2, M, I1, I2)

    def coupling_coefficient(self, L1: float, L2: float, M: float) -> jax.Array:
        """Coupling coefficient k = M / sqrt(L1 * L2). Art. 638."""
        return self._coupling_coefficient_jit(M, L1, L2)

    @staticmethod
    def _single_energy_jit(inductance: float, current: float) -> jax.Array:
        """T = (1/2) * L * I^2."""
        return 0.5 * inductance * current ** 2

    @staticmethod
    def _coupled_energy_jit(inductance_matrix: jax.Array, currents: jax.Array) -> jax.Array:
        """T = (1/2) * I^T . L . I."""
        Li = jnp.dot(inductance_matrix, currents)
        return 0.5 * jnp.dot(currents, Li)

    @staticmethod
    def _fields_energy_jit(A_potential: jax.Array, J_current: jax.Array, volume: float) -> jax.Array:
        """T = (1/2) * (A . J) * V."""
        dot_product = jnp.dot(A_potential, J_current)
        return 0.5 * dot_product * volume

    @staticmethod
    def _two_circuit_energy_jit(L1: float, L2: float, M: float, I1: float, I2: float) -> jax.Array:
        """T = (1/2)*L1*I1^2 + (1/2)*L2*I2^2 + M*I1*I2."""
        return 0.5 * L1 * I1 ** 2 + 0.5 * L2 * I2 ** 2 + M * I1 * I2

    @staticmethod
    def _coupling_coefficient_jit(M: float, L1: float, L2: float) -> jax.Array:
        """k = M / sqrt(L1 * L2)."""
        denom = jnp.sqrt(jnp.abs(L1 * L2))
        return jnp.where(denom > 0, M / denom, 0.0)


@jax_tree
@dataclass
class CoupledCircuitEnergyJAX:
    """Coupled circuit energy calculator (JAX-compatible pytree).

    Art. 636-637: For multiple coupled circuits with inductance matrix L_ij:
        T = (1/2) * I^T . L . I
    """

    inductance_matrix: jax.Array

    def from_currents(self, currents: jax.Array) -> jax.Array:
        """Total energy T = (1/2) * currents^T . L . currents."""
        return self._total_jit(self.inductance_matrix, currents)

    def from_currents_at(self, currents: jax.Array, inductance_matrix: jax.Array) -> jax.Array:
        """Energy with a custom inductance matrix override."""
        return self._total_jit(inductance_matrix, currents)

    def self_energies(self, currents: jax.Array) -> jax.Array:
        """Per-circuit self energy: (1/2) * L_ii * I_i^2."""
        return self._self_jit(jnp.diag(self.inductance_matrix), currents)

    def mutual_energy(self, currents: jax.Array) -> jax.Array:
        """Mutual energy: sum over i<j of L_ij * I_i * I_j."""
        return self._mutual_jit(self.inductance_matrix, currents)

    def coupling_matrix(self, currents: jax.Array) -> jax.Array:
        """Pairwise coupling coefficients k_ij = L_ij / sqrt(L_ii * L_jj)."""
        L = self.inductance_matrix
        diag = jnp.diag(L)
        sqrt_diag = jnp.sqrt(jnp.abs(diag))
        outer = jnp.outer(sqrt_diag, sqrt_diag)
        safe_outer = jnp.where(outer > 0, outer, 1.0)
        return jnp.where(outer > 0, L / safe_outer, 0.0)

    @staticmethod
    def _total_jit(inductance_matrix: jax.Array, currents: jax.Array) -> jax.Array:
        Li = jnp.dot(inductance_matrix, currents)
        return 0.5 * jnp.dot(currents, Li)

    @staticmethod
    def _self_jit(L_diag: jax.Array, currents: jax.Array) -> jax.Array:
        return 0.5 * L_diag * currents ** 2

    @staticmethod
    def _mutual_jit(inductance_matrix: jax.Array, currents: jax.Array) -> jax.Array:
        N = inductance_matrix.shape[0]
        total = jnp.array(0.0)
        def outer_body(i, val):
            def inner_body(j, val2):
                term = inductance_matrix[i, j] * currents[i] * currents[j]
                return val2 + jnp.where(i < j, term, 0.0)
            return val + jax.lax.fori_loop(0, N, inner_body, 0.0)
        return jax.lax.fori_loop(0, N, outer_body, total)


# -- Standalone functions -------------------------------------------------------------

@maxwell_cite(634, part=4, chapter="Electrokinetic Energy", description="Field formulation of electrokinetic energy")
def calc_electrokinetic_energy_jax(A_potential: jax.Array, J_current: jax.Array, volume: float) -> jax.Array:
    """Calculate electrokinetic energy from vector potential and current density.

    Art. 634: T = (1/2) * (A . J) * V
    """
    return ElectrokineticEnergyJAX._fields_energy_jit(A_potential, J_current, volume)


@maxwell_cite(635, part=4, chapter="Electrokinetic Energy", description="Single circuit energy")
def calc_single_circuit_energy_jax(inductance: float, current: float) -> jax.Array:
    """Single circuit energy T = (1/2) * L * I^2. Art. 635."""
    return ElectrokineticEnergyJAX._single_energy_jit(inductance, current)


@maxwell_cite(636, 637, part=4, chapter="Electrokinetic Energy", description="Coupled circuits energy")
def calc_coupled_circuits_energy_jax(inductance_matrix: jax.Array, currents: jax.Array) -> jax.Array:
    """Coupled circuits energy T = (1/2) * I^T . L . I. Arts. 636-637."""
    return ElectrokineticEnergyJAX._coupled_energy_jit(inductance_matrix, currents)


@maxwell_cite(638, part=4, chapter="Electrokinetic Energy", description="Mutual inductance energy")
def calc_mutual_inductance_energy_jax(mutual_inductance: float, I1: float, I2: float) -> jax.Array:
    """Mutual inductance energy T_mutual = M * I1 * I2. Art. 638."""
    return mutual_inductance * I1 * I2


@maxwell_cite(636, 637, part=4, chapter="Electrokinetic Energy", description="Two coupled circuit energy")
def calc_two_circuit_energy_jax(L1: float, L2: float, M: float, I1: float, I2: float) -> jax.Array:
    """Two coupled circuit energy. Arts. 636-637.

    T = (1/2)*L1*I1^2 + (1/2)*L2*I2^2 + M*I1*I2
    """
    return ElectrokineticEnergyJAX._two_circuit_energy_jit(L1, L2, M, I1, I2)


@maxwell_cite(638, part=4, chapter="Electrokinetic Energy", description="Coupling coefficient")
def calc_coupling_coefficient_jax(M: float, L1: float, L2: float) -> jax.Array:
    """Coupling coefficient k = M / sqrt(L1 * L2). Art. 638."""
    return ElectrokineticEnergyJAX._coupling_coefficient_jit(M, L1, L2)


@maxwell_cite(636, 637, part=4, chapter="Electrokinetic Energy", description="Verify coupled circuits energy consistency")
def verify_coupled_circuits_energy_jax(
    L1: float, L2: float, M: float, I1: float, I2: float, tolerance: float = 1e-10
) -> Dict[str, jax.Array]:
    """Verify coupled circuits energy consistency. Arts. 636-637."""
    # Scalar approach
    scalar_total = calc_two_circuit_energy_jax(L1, L2, M, I1, I2)

    # Matrix approach
    L_matrix = jnp.array([[L1, M], [M, L2]])
    I_vec = jnp.array([I1, I2])
    matrix_total = calc_coupled_circuits_energy_jax(L_matrix, I_vec)

    # Components
    self_energy_1 = calc_single_circuit_energy_jax(L1, I1)
    self_energy_2 = calc_single_circuit_energy_jax(L2, I2)
    mutual_energy = calc_mutual_inductance_energy_jax(M, I1, I2)
    component_sum = self_energy_1 + self_energy_2 + mutual_energy

    diff = jnp.abs(scalar_total - matrix_total)

    return {
        "scalar_total": scalar_total,
        "matrix_total": matrix_total,
        "self_energy_1": self_energy_1,
        "self_energy_2": self_energy_2,
        "mutual_energy": mutual_energy,
        "component_sum": component_sum,
        "difference": diff,
        "verified": diff < tolerance,
    }


@maxwell_cite(635, 636, 637, 638, part=4, chapter="Electrokinetic Energy", description="Comprehensive electrokinetic energy analysis")
def analyze_electrokinetic_energy_jax(
    inductance: Optional[float] = None,
    current: Optional[float] = None,
    L1: Optional[float] = None,
    L2: Optional[float] = None,
    M: Optional[float] = None,
    I1: Optional[float] = None,
    I2: Optional[float] = None,
    inductance_matrix: Optional[jax.Array] = None,
    currents: Optional[jax.Array] = None,
) -> Dict[str, jax.Array]:
    """Comprehensive electrokinetic energy analysis. Arts. 635-638."""
    result: Dict[str, jax.Array] = {}

    # Single circuit
    if inductance is not None and current is not None:
        result["single_energy"] = calc_single_circuit_energy_jax(inductance, current)

    # Two circuit
    if all(v is not None for v in [L1, L2, M, I1, I2]):
        result["two_circuit_energy"] = calc_two_circuit_energy_jax(L1, L2, M, I1, I2)
        result["coupling_coefficient"] = calc_coupling_coefficient_jax(M, L1, L2)
        result["self_energy_1"] = calc_single_circuit_energy_jax(L1, I1)
        result["self_energy_2"] = calc_single_circuit_energy_jax(L2, I2)
        result["mutual_energy"] = calc_mutual_inductance_energy_jax(M, I1, I2)

    # Matrix
    if inductance_matrix is not None and currents is not None:
        result["matrix_energy"] = calc_coupled_circuits_energy_jax(inductance_matrix, currents)
        result["verification"] = verify_coupled_circuits_energy_jax(
            float(inductance_matrix[0, 0]), float(inductance_matrix[1, 1]),
            float(inductance_matrix[0, 1]), float(currents[0]), float(currents[1])
        )["verified"]

    return result
