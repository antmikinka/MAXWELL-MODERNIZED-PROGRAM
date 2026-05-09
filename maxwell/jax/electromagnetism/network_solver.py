"""JAX network solver -- Part II Electrokinematics (Arts. 273-284).

Kirchhoff's laws, conductance matrix networks, Wheatstone bridge,
and reciprocity theorem implemented with JAX pytree support for
JIT compilation, automatic differentiation, and vectorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree, safe_div

__all__ = [
    "NetworkSolverJAX",
    "KirchhoffJAX",
    "WheatstoneBridgeJAX",
    "ReciprocityVerifierJAX",
    "kirchhoff_junction_rule_jax",
    "kirchhoff_loop_rule_jax",
    "solve_network_jax",
    "wheatstone_bridge_balance_jax",
    "wheatstone_bridge_sensitivity_jax",
    "reciprocity_theorem_jax",
    "verify_network_solution_jax",
    "analyze_network_jax",
]


# -- Data classes -------------------------------------------------------------------


@jax_tree(static_fields=("reference_node",))
@dataclass
class NetworkSolverJAX:
    """Resistor network solver via conductance matrix (JAX-compatible pytree).

    Arts. 276-280: For a network of linear conductors, node potentials are
    found by solving G @ V = I, where G is the conductance (admittance) matrix.

    Fields:
        conductance_matrix: (N, N) symmetric adjacency matrix. G[i,j] = conductance
            between nodes i and j (negative off-diagonal), G[i,i] = sum of
            conductances at node i.
        current_vector: (N,) injected currents at each node.
        reference_node: Index of ground node (held at V=0).
    """

    conductance_matrix: jax.Array
    current_vector: jax.Array
    reference_node: int = 0

    def __post_init__(self) -> None:
        self.conductance_matrix = jnp.asarray(
            self.conductance_matrix, dtype=jnp.float64
        )
        self.current_vector = jnp.asarray(self.current_vector, dtype=jnp.float64)

    @property
    def node_potentials(self) -> jax.Array:
        """Solve G_reduced @ V_reduced = I_reduced, with V_ref=0."""
        return self._solve_potentials(
            self.conductance_matrix, self.current_vector, self.reference_node
        )

    @classmethod
    def from_edges(
        cls,
        n_nodes: int,
        edges: List[Tuple[int, int, float]],
        current_sources: List[Tuple[int, float]],
        reference_node: int = 0,
    ) -> "NetworkSolverJAX":
        """Build from edge list.

        Args:
            n_nodes: Total number of nodes.
            edges: List of (i, j, g) tuples where g is conductance between nodes i and j.
            current_sources: List of (node, I) tuples for current injection.
            reference_node: Ground node index.
        """
        G = jnp.zeros((n_nodes, n_nodes), dtype=jnp.float64)
        I = jnp.zeros(n_nodes, dtype=jnp.float64)
        for i, j, g in edges:
            G = G.at[i, i].add(g).at[j, j].add(g).at[i, j].add(-g).at[j, i].add(-g)
        for node, current in current_sources:
            I = I.at[node].add(current)
        return cls(
            conductance_matrix=G, current_vector=I, reference_node=reference_node
        )

    @staticmethod
    def _solve_potentials(G: jax.Array, I: jax.Array, ref_node: int) -> jax.Array:
        """Solve reduced system, return full potentials with V_ref=0."""
        n = G.shape[0]
        idx = jnp.array([i for i in range(n) if i != ref_node], dtype=jnp.int32)
        G_red = G[idx[:, None], idx[None, :]]
        I_red = I[idx]
        V_red = jnp.linalg.solve(G_red, I_red)
        V = jnp.zeros(n, dtype=jnp.float64)
        V = V.at[idx].set(V_red)
        return V

    @staticmethod
    def _branch_current(G: jax.Array, V: jax.Array, i: int, j: int) -> jax.Array:
        """Branch current from i to j: I = -G[i,j] * (V[i] - V[j])."""
        return -G[i, j] * (V[i] - V[j])

    @property
    def branch_currents(self) -> jax.Array:
        """NxN branch current matrix. I[i,j] = -G[i,j] * (V[i] - V[j])."""
        V = self.node_potentials
        G = self.conductance_matrix
        return -G * (V[:, None] - V[None, :])

    @property
    def branch_power(self) -> jax.Array:
        """NxN branch power matrix: P[i,j] = I[i,j]^2 / |G[i,j]| for connected nodes."""
        I_branch = self.branch_currents
        G = self.conductance_matrix
        # Off-diagonal entries are negative conductances; diagonal is self-conductance
        abs_G = jnp.abs(G)
        safe_G = jnp.where(abs_G > 0, abs_G, 1.0)
        return jnp.where(abs_G > 0, I_branch**2 / safe_G, 0.0)

    @property
    def total_power(self) -> jax.Array:
        """Total power dissipated (each branch counted once)."""
        return jnp.sum(self.branch_power) / 2.0

    def effective_resistance(self, node_a: int, node_b: int) -> jax.Array:
        """Effective resistance between two nodes.

        Inject 1A at node_a, extract at node_b, measure voltage difference.
        """
        n = self.conductance_matrix.shape[0]
        I_test = (
            jnp.zeros(n, dtype=jnp.float64).at[node_a].set(1.0).at[node_b].set(-1.0)
        )
        V = self._solve_potentials(self.conductance_matrix, I_test, self.reference_node)
        return safe_div(V[node_a] - V[node_b], 1.0, safe_default=0.0)

    def verify_kirchhoff(self, tol: float = 1e-10) -> Dict[str, Any]:
        """Verify KCL: G @ V == I for non-reference nodes."""
        V = self.node_potentials
        I_computed = jnp.dot(self.conductance_matrix, V)
        residual = jnp.abs(I_computed - self.current_vector)
        # Only check non-reference nodes
        n = self.conductance_matrix.shape[0]
        idx = jnp.array(
            [i for i in range(n) if i != self.reference_node], dtype=jnp.int32
        )
        non_ref_residual = residual[idx]
        return {
            "max_residual": jnp.max(non_ref_residual),
            "kcl_satisfied": bool(jnp.all(non_ref_residual < tol)),
        }


@jax_tree(static_fields=("reference_node",))
@dataclass
class KirchhoffJAX:
    """KCL/KVL verification (JAX-compatible pytree).

    Arts. 273-275: Kirchhoff's current law (junction rule) and
    voltage law (loop rule) verification for network solutions.

    Fields:
        node_potentials: (N,) node voltage vector.
        conductance_matrix: (N, N) conductance matrix.
        current_vector: (N,) injected current vector.
        reference_node: Ground node index (excluded from KCL check).
    """

    node_potentials: jax.Array
    conductance_matrix: jax.Array
    current_vector: jax.Array
    reference_node: int = 0

    def __post_init__(self) -> None:
        self.node_potentials = jnp.asarray(self.node_potentials, dtype=jnp.float64)
        self.conductance_matrix = jnp.asarray(
            self.conductance_matrix, dtype=jnp.float64
        )
        self.current_vector = jnp.asarray(self.current_vector, dtype=jnp.float64)

    @property
    def kcl_residuals(self) -> jax.Array:
        """I_injected - G @ V for non-reference nodes. Should be ~0."""
        n = self.conductance_matrix.shape[0]
        idx = jnp.array(
            [i for i in range(n) if i != self.reference_node], dtype=jnp.int32
        )
        full_residual = self.current_vector - jnp.dot(
            self.conductance_matrix, self.node_potentials
        )
        return full_residual[idx]

    @property
    def kcl_max_residual(self) -> jax.Array:
        """Maximum absolute KCL residual (non-reference nodes)."""
        return jnp.max(jnp.abs(self.kcl_residuals))

    @property
    def kcl_satisfied(self) -> bool:
        """Whether KCL is satisfied within tolerance."""
        return bool(self.kcl_max_residual < 1e-10)

    @property
    def power_balance(self) -> jax.Array:
        """Source power minus dissipated power. Should be ~0.

        P_source = I . V
        P_dissipated = sum over branches of I_ij * (V_i - V_j)
        """
        V = self.node_potentials
        P_source = jnp.dot(self.current_vector, V)
        G = self.conductance_matrix
        n = G.shape[0]
        total = jnp.array(0.0, dtype=jnp.float64)

        def outer_body(i, val):
            def inner_body(j, val2):
                I_ij = -G[i, j] * (V[i] - V[j])
                return val2 + I_ij * (V[i] - V[j])

            return val + jax.lax.fori_loop(
                i + 1, n, inner_body, jnp.array(0.0, dtype=jnp.float64)
            )

        P_dissipated = jax.lax.fori_loop(
            0, n - 1, outer_body, jnp.array(0.0, dtype=jnp.float64)
        )
        return P_source - P_dissipated


@jax_tree
@dataclass
class WheatstoneBridgeJAX:
    """Wheatstone bridge analysis (JAX-compatible pytree).

    Arts. 281-284: Four-resistor bridge for precision resistance measurement.
    Balance condition: R1 * R4 = R2 * R3.

    Standard configuration:
        Node A --R1-- Node B --R2-- Node C
          |              |              |
          +---- R3 ------+---- R4 ------+

    Fields:
        R1: First arm resistance.
        R2: Second arm resistance.
        R3: Third arm resistance.
        R4: Fourth arm resistance.
    """

    R1: float
    R2: float
    R3: float
    R4: float

    def __post_init__(self) -> None:
        self.R1 = jnp.asarray(self.R1, dtype=jnp.float64)
        self.R2 = jnp.asarray(self.R2, dtype=jnp.float64)
        self.R3 = jnp.asarray(self.R3, dtype=jnp.float64)
        self.R4 = jnp.asarray(self.R4, dtype=jnp.float64)

    @property
    def balance_error(self) -> jax.Array:
        """R1*R4 - R2*R3 (zero when balanced)."""
        return self.R1 * self.R4 - self.R2 * self.R3

    @property
    def is_balanced(self) -> bool:
        """Whether bridge is balanced within tolerance."""
        return bool(jnp.abs(self.balance_error) < 1e-10)

    @property
    def balance_point_R4(self) -> jax.Array:
        """R4 value for exact balance: R2*R3/R1."""
        return safe_div(self.R2 * self.R3, self.R1, safe_default=0.0)

    def thevenin_voltage(self, V_battery: float) -> jax.Array:
        """Open-circuit voltage across galvanometer terminals."""
        V = jnp.asarray(V_battery, dtype=jnp.float64)
        V_left = V * safe_div(self.R3, self.R1 + self.R3, safe_default=0.0)
        V_right = V * safe_div(self.R4, self.R2 + self.R4, safe_default=0.0)
        return V_left - V_right

    def thevenin_resistance(self) -> jax.Array:
        """Thevenin resistance seen by galvanometer: R1||R3 + R2||R4."""
        R13 = safe_div(self.R1 * self.R3, self.R1 + self.R3, safe_default=0.0)
        R24 = safe_div(self.R2 * self.R4, self.R2 + self.R4, safe_default=0.0)
        return R13 + R24

    def galvanometer_current(
        self, V_battery: float, R_galvanometer: float
    ) -> jax.Array:
        """Current through galvanometer: V_th / (R_th + R_g)."""
        Vth = self.thevenin_voltage(V_battery)
        Rth = self.thevenin_resistance()
        Rg = jnp.asarray(R_galvanometer, dtype=jnp.float64)
        return safe_div(Vth, Rth + Rg, safe_default=0.0)

    @staticmethod
    @jax.jit
    def _balance_error_jit(R1: float, R2: float, R3: float, R4: float) -> jax.Array:
        R1, R2, R3, R4 = [jnp.asarray(r, dtype=jnp.float64) for r in (R1, R2, R3, R4)]
        return R1 * R4 - R2 * R3

    @staticmethod
    @jax.jit
    def _thevenin_voltage_jit(
        R1: float, R2: float, R3: float, R4: float, V: float
    ) -> jax.Array:
        V = jnp.asarray(V, dtype=jnp.float64)
        R1, R2, R3, R4 = [jnp.asarray(r, dtype=jnp.float64) for r in (R1, R2, R3, R4)]
        Vl = V * safe_div(R3, R1 + R3, safe_default=0.0)
        Vr = V * safe_div(R4, R2 + R4, safe_default=0.0)
        return Vl - Vr

    @staticmethod
    @jax.jit
    def _galvanometer_current_jit(R1, R2, R3, R4, V, Rg):
        V, Rg = [jnp.asarray(x, dtype=jnp.float64) for x in (V, Rg)]
        R1, R2, R3, R4 = [jnp.asarray(r, dtype=jnp.float64) for r in (R1, R2, R3, R4)]
        R13 = safe_div(R1 * R3, R1 + R3, safe_default=0.0)
        R24 = safe_div(R2 * R4, R2 + R4, safe_default=0.0)
        Vth = V * (
            safe_div(R3, R1 + R3, safe_default=0.0)
            - safe_div(R4, R2 + R4, safe_default=0.0)
        )
        return safe_div(Vth, R13 + R24 + Rg, safe_default=0.0)


@jax_tree(static_fields=("reference_node",))
@dataclass
class ReciprocityVerifierJAX:
    """Reciprocity theorem verifier (JAX-compatible pytree).

    Arts. 277-278: Maxwell's reciprocity theorem -- for any linear
    passive network, the transfer resistance between two port pairs
    is symmetric.

    Fields:
        conductance_matrix: (N, N) conductance matrix.
        reference_node: Ground node index.
    """

    conductance_matrix: jax.Array
    reference_node: int = 0

    def __post_init__(self) -> None:
        self.conductance_matrix = jnp.asarray(
            self.conductance_matrix, dtype=jnp.float64
        )

    def transfer_resistance(self, port_a: int, port_b: int) -> jax.Array:
        """Transfer resistance: V_port_b / I_applied at port_a (with -I at reference)."""
        n = self.conductance_matrix.shape[0]
        I = (
            jnp.zeros(n, dtype=jnp.float64)
            .at[port_a]
            .set(1.0)
            .at[self.reference_node]
            .set(-1.0)
        )
        V = NetworkSolverJAX._solve_potentials(
            self.conductance_matrix, I, self.reference_node
        )
        return safe_div(V[port_b] - V[self.reference_node], 1.0, safe_default=0.0)

    def verify(
        self,
        port1_a: int,
        port1_b: int,
        port2_a: int,
        port2_b: int,
        tol: float = 1e-10,
    ) -> Dict[str, Any]:
        """Verify reciprocity: R_12 == R_21."""
        R12 = self.transfer_resistance(port1_a, port2_a)
        R21 = self.transfer_resistance(port2_a, port1_a)
        error = jnp.abs(R12 - R21)
        rel_error = safe_div(error, jnp.abs(R12) + 1e-30, safe_default=0.0)
        return {
            "R_12": R12,
            "R_21": R21,
            "error": error,
            "relative_error": rel_error,
            "is_reciprocal": bool(rel_error < tol),
        }


# -- Standalone functions -------------------------------------------------------------


@maxwell_cite(
    273,
    274,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Kirchhoff's junction rule (current conservation)",
)
def kirchhoff_junction_rule_jax(currents: jax.Array) -> Dict[str, Any]:
    """Verify Kirchhoff's current law. Arts. 273-274.

    sum(I_k) = 0 at any junction.

    Args:
        currents: Array of currents at the node (positive = entering).

    Returns:
        Dictionary with 'sum', 'satisfied' boolean.
    """
    currents = jnp.asarray(currents, dtype=jnp.float64)
    total = jnp.sum(currents)
    satisfied = jnp.abs(total) < 1e-10 * jnp.maximum(1.0, jnp.max(jnp.abs(currents)))
    return {"sum": total, "satisfied": bool(satisfied)}


@maxwell_cite(
    275,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Kirchhoff's loop rule (voltage conservation)",
)
def kirchhoff_loop_rule_jax(voltage_drops: jax.Array) -> Dict[str, Any]:
    """Verify Kirchhoff's voltage law. Art. 275.

    sum(V_k) = 0 around any closed loop.

    Args:
        voltage_drops: Array of voltage drops around the loop.

    Returns:
        Dictionary with 'sum', 'satisfied' boolean.
    """
    voltage_drops = jnp.asarray(voltage_drops, dtype=jnp.float64)
    total = jnp.sum(voltage_drops)
    satisfied = jnp.abs(total) < 1e-10 * jnp.maximum(
        1.0, jnp.max(jnp.abs(voltage_drops))
    )
    return {"sum": total, "satisfied": bool(satisfied)}


@maxwell_cite(
    279,
    280,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Solve resistor network via conductance matrix",
)
def solve_network_jax(
    conductance_matrix: jax.Array,
    current_vector: jax.Array,
    reference_node: int = 0,
) -> Dict[str, Any]:
    """Solve linear resistor network. Arts. 279-280.

    Args:
        conductance_matrix: (N, N) conductance matrix.
        current_vector: (N,) injected currents.
        reference_node: Ground node index.

    Returns:
        Dictionary with 'node_potentials', 'branch_currents', 'total_power'.
    """
    solver = NetworkSolverJAX(
        conductance_matrix=conductance_matrix,
        current_vector=current_vector,
        reference_node=reference_node,
    )
    V = solver.node_potentials
    I_branch = solver.branch_currents
    return {
        "node_potentials": V,
        "branch_currents": I_branch,
        "total_power": solver.total_power,
    }


@maxwell_cite(
    281,
    282,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Wheatstone bridge balance analysis",
)
def wheatstone_bridge_balance_jax(
    R1: float, R2: float, R3: float, R4: float
) -> Dict[str, Any]:
    """Analyze Wheatstone bridge balance. Arts. 281-282.

    Balance condition: R1 * R4 = R2 * R3.

    Returns:
        Dictionary with balance_error, is_balanced, ratio_1_2, ratio_3_4, balance_point_R4.
    """
    bridge = WheatstoneBridgeJAX(R1=R1, R2=R2, R3=R3, R4=R4)
    ratio_1_2 = safe_div(bridge.R1, bridge.R2, safe_default=0.0)
    ratio_3_4 = safe_div(bridge.R3, bridge.R4, safe_default=0.0)
    return {
        "balance_error": bridge.balance_error,
        "is_balanced": bridge.is_balanced,
        "ratio_1_2": ratio_1_2,
        "ratio_3_4": ratio_3_4,
        "balance_point_R4": bridge.balance_point_R4,
    }


@maxwell_cite(
    283,
    284,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Wheatstone bridge sensitivity analysis",
)
def wheatstone_bridge_sensitivity_jax(
    R1: float,
    R2: float,
    R3: float,
    R4: float,
    V_battery: float,
    R_galvanometer: float,
) -> Dict[str, Any]:
    """Analyze Wheatstone bridge sensitivity. Arts. 283-284.

    Returns:
        Dictionary with thevenin_voltage, thevenin_resistance,
        galvanometer_current, balance_error, is_balanced.
    """
    bridge = WheatstoneBridgeJAX(R1=R1, R2=R2, R3=R3, R4=R4)
    Vth = bridge.thevenin_voltage(V_battery)
    Rth = bridge.thevenin_resistance()
    Ig = bridge.galvanometer_current(V_battery, R_galvanometer)
    return {
        "thevenin_voltage": Vth,
        "thevenin_resistance": Rth,
        "galvanometer_current": Ig,
        "balance_error": bridge.balance_error,
        "is_balanced": bridge.is_balanced,
    }


@maxwell_cite(
    277,
    278,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Reciprocity theorem verification",
)
def reciprocity_theorem_jax(
    conductance_matrix: jax.Array,
    port1: Tuple[int, int],
    port2: Tuple[int, int],
    reference_node: int = 0,
) -> Dict[str, Any]:
    """Verify reciprocity theorem. Arts. 277-278.

    For linear passive networks, transfer resistance is symmetric.

    Args:
        conductance_matrix: (N, N) conductance matrix.
        port1: (node_a, node_b) for port 1.
        port2: (node_c, node_d) for port 2.
        reference_node: Ground node index.

    Returns:
        Dictionary with R_12, R_21, error, relative_error, is_reciprocal.
    """
    verifier = ReciprocityVerifierJAX(
        conductance_matrix=conductance_matrix,
        reference_node=reference_node,
    )
    return verifier.verify(port1[0], port1[1], port2[0], port2[1])


@maxwell_cite(
    273,
    274,
    275,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Verify network solution satisfies Kirchhoff's laws",
)
def verify_network_solution_jax(
    G: jax.Array,
    V: jax.Array,
    I_injected: jax.Array,
    tol: float = 1e-10,
    reference_node: int = 0,
) -> Dict[str, Any]:
    """Verify network solution satisfies KCL. Arts. 273-275.

    Args:
        G: Conductance matrix.
        V: Node potentials.
        I_injected: Injected currents.
        tol: Tolerance for verification.
        reference_node: Ground node index.

    Returns:
        Dictionary with max_residual, kcl_satisfied, power_source, power_dissipated.
    """
    G = jnp.asarray(G, dtype=jnp.float64)
    V = jnp.asarray(V, dtype=jnp.float64)
    I_injected = jnp.asarray(I_injected, dtype=jnp.float64)

    # KCL verification: only check non-reference nodes
    n = G.shape[0]
    idx = jnp.array([i for i in range(n) if i != reference_node], dtype=jnp.int32)
    I_computed = jnp.dot(G, V)
    residual = jnp.abs(I_computed - I_injected)
    non_ref_residual = residual[idx]
    max_residual = jnp.max(non_ref_residual)

    # Source power: only non-reference nodes (ref node V=0)
    P_source = jnp.dot(I_injected[idx], V[idx])

    # Dissipated power from branches (off-diagonal entries, counted once)
    I_branch = -G * (V[:, None] - V[None, :])
    abs_G = jnp.abs(G)
    safe_G = jnp.where(abs_G > 0, abs_G, 1.0)
    P_branch = jnp.where(abs_G > 0, I_branch**2 / safe_G, 0.0)
    P_dissipated = jnp.sum(P_branch) / 2.0

    return {
        "max_residual": max_residual,
        "kcl_satisfied": bool(jnp.all(non_ref_residual < tol)),
        "power_source": P_source,
        "power_dissipated": P_dissipated,
    }


@maxwell_cite(
    273,
    274,
    275,
    276,
    277,
    278,
    279,
    280,
    part=2,
    chapter="Theory of Linear Systems of Conductors",
    description="Comprehensive network analysis",
)
def analyze_network_jax(
    edges: List[Tuple[int, int, float]],
    current_sources: List[Tuple[int, float]],
    reference_node: int = 0,
) -> Dict[str, Any]:
    """Comprehensive network analysis. Arts. 273-280.

    Args:
        edges: List of (i, j, g) tuples defining network topology.
        current_sources: List of (node, I) tuples.
        reference_node: Ground node index.

    Returns:
        Dictionary with node_potentials, branch_currents, total_power,
        kirchhoff_verification, and effective_resistances between adjacent nodes.
    """
    node_set = set()
    for i, j, _ in edges:
        node_set.add(i)
        node_set.add(j)
    for node, _ in current_sources:
        node_set.add(node)
    n_nodes = max(node_set) + 1

    solver = NetworkSolverJAX.from_edges(
        n_nodes=n_nodes,
        edges=edges,
        current_sources=current_sources,
        reference_node=reference_node,
    )

    V = solver.node_potentials
    I_branch = solver.branch_currents
    P_total = solver.total_power
    kirchhoff = solver.verify_kirchhoff()

    # Effective resistances for each edge
    eff_resistances = {}
    for i, j, g in edges:
        eff_resistances[(i, j)] = solver.effective_resistance(i, j)

    return {
        "node_potentials": V,
        "branch_currents": I_branch,
        "total_power": P_total,
        "kirchhoff_verification": kirchhoff,
        "effective_resistances": eff_resistances,
        "n_nodes": n_nodes,
    }
