"""Tests for NetworkSolverJAX -- Part II Electrokinematics (Arts. 273-284)."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from maxwell.jax.electromagnetism.network_solver import (
    NetworkSolverJAX,
    KirchhoffJAX,
    WheatstoneBridgeJAX,
    ReciprocityVerifierJAX,
    kirchhoff_junction_rule_jax,
    kirchhoff_loop_rule_jax,
    solve_network_jax,
    wheatstone_bridge_balance_jax,
    wheatstone_bridge_sensitivity_jax,
    reciprocity_theorem_jax,
    verify_network_solution_jax,
    analyze_network_jax,
)

TOL = 1e-10


# -- TestNetworkSolverJAXPytree ----------------------------------------------------

class TestNetworkSolverJAXPytree:
    """Flatten/unflatten, jit, vmap, grad."""

    def test_flatten_unflatten(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        obj = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        # conductance_matrix, current_vector (reference_node is static)
        assert len(leaves) == 2
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(reconstructed.conductance_matrix, G)
        assert jnp.allclose(reconstructed.current_vector, I)
        assert reconstructed.reference_node == 0

    def test_jit_compatible(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        obj = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        jit_fn = jax.jit(lambda o: o.node_potentials)
        result = jit_fn(obj)
        assert result.shape == (2,)

    def test_tree_map(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        obj = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2 if hasattr(x, 'dtype') else x, obj)
        assert jnp.allclose(doubled.conductance_matrix, G * 2)
        assert jnp.allclose(doubled.current_vector, I * 2)

    def test_vmap_over_current(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        currents = jnp.array([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])

        def solve_with_current(I):
            return NetworkSolverJAX(
                conductance_matrix=G, current_vector=I, reference_node=0
            ).node_potentials

        results = jax.vmap(solve_with_current)(currents)
        assert results.shape == (3, 2)


# -- TestNetworkSolverJAXSimpleNetwork ----------------------------------------------

class TestNetworkSolverJAXSimpleNetwork:
    """Single R, series, parallel, triangle, bridge networks."""

    def test_single_resistor(self):
        """Two nodes, one resistor between them."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        assert float(V[0]) == pytest.approx(0.0, abs=1e-8)
        assert float(V[1]) == pytest.approx(1.0, abs=1e-8)

    def test_series_resistors(self):
        """Three nodes in series: 0--1ohm--1--2ohm--2, 1A injected at node 2."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=3,
            edges=[(0, 1, 1.0), (1, 2, 0.5)],
            current_sources=[(2, 1.0)],
            reference_node=0,
        )
        V = solver.node_potentials
        assert float(V[0]) == pytest.approx(0.0, abs=1e-8)
        assert float(V[1]) == pytest.approx(1.0, abs=1e-8)
        assert float(V[2]) == pytest.approx(3.0, abs=1e-8)

    def test_parallel_resistors(self):
        """Two parallel 1-ohm resistors between node 0 and node 1, 2A injected at node 1."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0), (0, 1, 1.0)], current_sources=[(1, 2.0)], reference_node=0
        )
        V = solver.node_potentials
        # Equivalent conductance = 2 S, V = I/G = 2/2 = 1V
        assert float(V[1]) == pytest.approx(1.0, abs=1e-8)

    def test_triangle_network(self):
        """3-node triangle: all edges 1S, 1A injected at node 0, ref=2."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=3,
            edges=[(0, 1, 1.0), (1, 2, 1.0), (0, 2, 1.0)],
            current_sources=[(0, 1.0)],
            reference_node=2,
        )
        V = solver.node_potentials
        assert float(V[2]) == pytest.approx(0.0, abs=1e-8)
        # V[0] = 2/3, V[1] = 1/3 (current flows from 0 to ref both directly and via node 1)
        assert float(V[0]) == pytest.approx(2.0 / 3.0, abs=1e-8)
        assert float(V[1]) == pytest.approx(1.0 / 3.0, abs=1e-8)

    def test_bridge_network(self):
        """Bridge network: 4 nodes, 4 outer edges + 1 cross edge."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=4,
            edges=[(0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (2, 3, 1.0), (1, 2, 0.5)],
            current_sources=[(0, 1.0), (3, -1.0)],
            reference_node=3,
        )
        V = solver.node_potentials
        assert float(V[3]) == pytest.approx(0.0, abs=1e-8)
        assert float(V[0]) > 0.0
        # By symmetry V[1] == V[2]
        assert float(V[1]) == pytest.approx(float(V[2]), abs=1e-8)


# -- TestNetworkSolverJAXProperties -------------------------------------------------

class TestNetworkSolverJAXProperties:
    """branch_currents, branch_power, total_power, verify_kirchhoff."""

    def test_branch_currents_shape(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        bc = solver.branch_currents
        assert bc.shape == (2, 2)

    def test_branch_currents_skew_symmetric(self):
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        I = jnp.array([1.0, 0.0, 0.0])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        bc = solver.branch_currents
        # I[i,j] = -I[j,i] for off-diagonal
        assert float(bc[1, 2]) == pytest.approx(-float(bc[2, 1]), abs=1e-8)

    def test_branch_power_non_negative(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        bp = solver.branch_power
        assert jnp.all(bp >= 0)

    def test_total_power_positive(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        P = solver.total_power
        assert float(P) == pytest.approx(1.0, abs=1e-8)

    def test_verify_kirchhoff_passes(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        result = solver.verify_kirchhoff()
        assert result["kcl_satisfied"] is True
        assert float(result["max_residual"]) < 1e-8

    def test_verify_kirchhoff_all_keys(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        result = solver.verify_kirchhoff()
        assert "max_residual" in result
        assert "kcl_satisfied" in result


# -- TestNetworkSolverJAXEdgeCases --------------------------------------------------

class TestNetworkSolverJAXEdgeCases:
    """Zero conductance entries, single source, large networks."""

    def test_zero_conductance_row_col(self):
        """Reference node should have zeros in its row/col effect."""
        G = jnp.array([[0.0, 0.0, 0.0], [0.0, 1.0, -1.0], [0.0, -1.0, 1.0]])
        I = jnp.array([0.0, 1.0, -1.0])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        V = solver.node_potentials
        assert float(V[0]) == pytest.approx(0.0, abs=1e-8)

    def test_single_current_source(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 2.0)], current_sources=[(1, 3.0)], reference_node=0
        )
        V = solver.node_potentials
        # R = 1/2, V = I * R = 3 * 0.5 = 1.5
        assert float(V[1]) == pytest.approx(1.5, abs=1e-8)

    def test_effective_resistance_symmetric(self):
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        I = jnp.zeros(3, dtype=jnp.float64)
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        R_ab = solver.effective_resistance(1, 2)
        R_ba = solver.effective_resistance(2, 1)
        assert float(R_ab) == pytest.approx(float(R_ba), abs=1e-8)

    def test_power_balance_with_single_resistor(self):
        """P_dissipated should equal V * I for single resistor."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 0.5)], current_sources=[(1, 2.0)], reference_node=0
        )
        V = solver.node_potentials
        P_total = solver.total_power
        # R = 2 ohm, V = I * R = 2 * 2 = 4V, P = V * I = 4 * 2 = 8W
        assert float(P_total) == pytest.approx(8.0, abs=1e-8)


# -- TestKirchhoffJAXPytree ---------------------------------------------------------

class TestKirchhoffJAXPytree:
    """Flatten/unflatten, jit."""

    def test_flatten_unflatten(self):
        V = jnp.array([0.0, 1.0, 2.0])
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        I = jnp.array([1.0, 0.0, 0.0])
        obj = KirchhoffJAX(node_potentials=V, conductance_matrix=G, current_vector=I, reference_node=0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 3
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert jnp.allclose(reconstructed.node_potentials, V)

    def test_jit_compatible(self):
        V = jnp.array([0.0, 1.0, 2.0])
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        I = jnp.array([1.0, 0.0, 0.0])
        obj = KirchhoffJAX(node_potentials=V, conductance_matrix=G, current_vector=I, reference_node=0)
        jit_fn = jax.jit(lambda o: o.kcl_max_residual)
        result = jit_fn(obj)
        assert float(result) >= 0

    def test_tree_map(self):
        V = jnp.array([0.0, 1.0, 2.0])
        G = jnp.array([[1.0, 0.0], [0.0, 1.0]])
        I = jnp.array([0.0, 0.0])
        obj = KirchhoffJAX(node_potentials=V, conductance_matrix=G, current_vector=I, reference_node=0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2 if hasattr(x, 'dtype') else x, obj)
        assert jnp.allclose(doubled.node_potentials, V * 2)


# -- TestKirchhoffJAXVerification ---------------------------------------------------

class TestKirchhoffJAXVerification:
    """KCL residuals, power balance, satisfied checks."""

    def test_kcl_satisfied_for_valid_solution(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=3,
            edges=[(0, 1, 1.0), (1, 2, 2.0)],
            current_sources=[(1, 1.0)],
            reference_node=0,
        )
        V = solver.node_potentials
        k = KirchhoffJAX(node_potentials=V, conductance_matrix=solver.conductance_matrix,
                         current_vector=solver.current_vector, reference_node=0)
        assert k.kcl_satisfied

    def test_kcl_max_residual_small(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        k = KirchhoffJAX(node_potentials=V, conductance_matrix=solver.conductance_matrix,
                         current_vector=solver.current_vector, reference_node=0)
        assert float(k.kcl_max_residual) < 1e-8

    def test_kcl_residuals_shape(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        V = solver.node_potentials
        k = KirchhoffJAX(node_potentials=V, conductance_matrix=G, current_vector=I, reference_node=0)
        # N-1 non-reference nodes
        assert k.kcl_residuals.shape == (1,)

    def test_power_balance_small(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 0.5)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        k = KirchhoffJAX(node_potentials=V, conductance_matrix=solver.conductance_matrix,
                         current_vector=solver.current_vector, reference_node=0)
        pb = k.power_balance
        assert float(jnp.abs(pb)) < 1e-6

    def test_kcl_residuals_non_ref_near_zero(self):
        """For a valid solution, non-reference KCL residuals should be ~0."""
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        I = jnp.array([1.0, 0.5, -1.5])
        solver = NetworkSolverJAX(conductance_matrix=G, current_vector=I, reference_node=0)
        V = solver.node_potentials
        k = KirchhoffJAX(node_potentials=V, conductance_matrix=G, current_vector=I, reference_node=0)
        assert float(jnp.max(jnp.abs(k.kcl_residuals))) < 1e-8


# -- TestWheatstoneBridgeJAXPytree --------------------------------------------------

class TestWheatstoneBridgeJAXPytree:
    """Flatten/unflatten, jit, tree_map."""

    def test_flatten_unflatten(self):
        obj = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)
        leaves, treedef = jax.tree_util.tree_flatten(obj)
        assert len(leaves) == 4
        reconstructed = jax.tree_util.tree_unflatten(treedef, leaves)
        assert float(reconstructed.R1) == pytest.approx(100.0)

    def test_jit_compatible(self):
        obj = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=100.0)
        jit_fn = jax.jit(lambda o: o.balance_error)
        result = jit_fn(obj)
        assert float(result) == pytest.approx(0.0)

    def test_tree_map(self):
        obj = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=400.0)
        doubled = jax.tree_util.tree_map(lambda x: x * 2, obj)
        assert float(doubled.R1) == pytest.approx(200.0)
        assert float(doubled.R4) == pytest.approx(800.0)


# -- TestWheatstoneBridgeJAXBalance -------------------------------------------------

class TestWheatstoneBridgeJAXBalance:
    """Balanced, unbalanced, balance_point."""

    def test_balanced_bridge(self):
        """100/200 = 300/600."""
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)
        assert bridge.is_balanced
        assert float(bridge.balance_error) == pytest.approx(0.0)

    def test_balanced_equal_arms(self):
        """100/100 = 100/100."""
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=100.0)
        assert bridge.is_balanced

    def test_unbalanced_bridge(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=101.0)
        assert not bridge.is_balanced
        # R1*R4 - R2*R3 = 100*101 - 100*100 = 100
        assert float(bridge.balance_error) == pytest.approx(100.0)

    def test_balance_point_R4(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=500.0)
        # Balance point: R2*R3/R1 = 200*300/100 = 600
        assert float(bridge.balance_point_R4) == pytest.approx(600.0)

    def test_balance_error_sign(self):
        """R1*R4 - R2*R3: positive if R4 > balance point."""
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=200.0)
        assert float(bridge.balance_error) > 0


# -- TestWheatstoneBridgeJAXThevenin ------------------------------------------------

class TestWheatstoneBridgeJAXThevenin:
    """Thevenin voltage, resistance, galvanometer current."""

    def test_thevenin_voltage_balanced(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)
        Vth = bridge.thevenin_voltage(10.0)
        assert float(Vth) == pytest.approx(0.0, abs=1e-10)

    def test_thevenin_voltage_unbalanced(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=101.0)
        Vth = bridge.thevenin_voltage(10.0)
        # Left divider: V * R3/(R1+R3) = 10 * 100/200 = 5
        # Right divider: V * R4/(R2+R4) = 10 * 101/201 ~ 5.025
        assert float(jnp.abs(Vth)) > 0

    def test_thevenin_resistance(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=100.0)
        Rth = bridge.thevenin_resistance()
        # R1||R3 + R2||R4 = 50 + 50 = 100
        assert float(Rth) == pytest.approx(100.0)

    def test_galvanometer_current_balanced(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)
        Ig = bridge.galvanometer_current(10.0, 10.0)
        assert float(Ig) == pytest.approx(0.0, abs=1e-10)


# -- TestWheatstoneBridgeJAXSensitivity ---------------------------------------------

class TestWheatstoneBridgeJAXSensitivity:
    """Galvanometer current for small imbalance."""

    def test_small_imbalance_current(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=100.1)
        Ig = bridge.galvanometer_current(1.0, 10.0)
        assert float(jnp.abs(Ig)) > 0

    def test_current_increases_with_voltage(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=101.0)
        Ig1 = bridge.galvanometer_current(1.0, 10.0)
        Ig2 = bridge.galvanometer_current(2.0, 10.0)
        assert float(jnp.abs(Ig2)) == pytest.approx(float(jnp.abs(Ig1)) * 2, rel=1e-6)

    def test_current_decreases_with_galvanometer_resistance(self):
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=100.0, R3=100.0, R4=101.0)
        Ig_low = bridge.galvanometer_current(1.0, 1.0)
        Ig_high = bridge.galvanometer_current(1.0, 100.0)
        assert float(jnp.abs(Ig_high)) < float(jnp.abs(Ig_low))


# -- TestReciprocityVerifierJAX -----------------------------------------------------

class TestReciprocityVerifierJAX:
    """Transfer resistance symmetry, verify method."""

    def test_transfer_resistance_symmetric(self):
        G = jnp.array([
            [3.0, -1.0, -1.0, -1.0],
            [-1.0, 3.0, -1.0, -1.0],
            [-1.0, -1.0, 3.0, -1.0],
            [-1.0, -1.0, -1.0, 3.0],
        ])
        verifier = ReciprocityVerifierJAX(conductance_matrix=G, reference_node=0)
        R12 = verifier.transfer_resistance(1, 2)
        R21 = verifier.transfer_resistance(2, 1)
        assert float(R12) == pytest.approx(float(R21), abs=1e-8)

    def test_verify_reciprocity_passes(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        verifier = ReciprocityVerifierJAX(conductance_matrix=G, reference_node=0)
        result = verifier.verify(1, 0, 0, 1)
        # Port2_a = 0 which is the reference node, so R = V[0]/1 = 0
        # This is a degenerate case but should still be reciprocal
        assert bool(result["is_reciprocal"])

    def test_verify_t_network(self):
        """T-network: 0-1: 1S, 1-2: 2S, 1-3: 3S."""
        G = jnp.array([
            [1.0, -1.0, 0.0, 0.0],
            [-1.0, 6.0, -2.0, -3.0],
            [0.0, -2.0, 2.0, 0.0],
            [0.0, -3.0, 0.0, 3.0],
        ])
        verifier = ReciprocityVerifierJAX(conductance_matrix=G, reference_node=0)
        result = verifier.verify(1, 2, 1, 3)
        assert bool(result["is_reciprocal"])

    def test_verify_all_keys(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        verifier = ReciprocityVerifierJAX(conductance_matrix=G, reference_node=0)
        result = verifier.verify(1, 0, 0, 1)
        expected_keys = {"R_12", "R_21", "error", "relative_error", "is_reciprocal"}
        assert set(result.keys()) == expected_keys

    def test_verify_returns_floats(self):
        G = jnp.array([[3.0, -1.0, -2.0], [-1.0, 3.0, -2.0], [-2.0, -2.0, 4.0]])
        verifier = ReciprocityVerifierJAX(conductance_matrix=G, reference_node=0)
        result = verifier.verify(1, 2, 2, 1)
        assert float(result["error"]) < 1e-8


# -- TestStandaloneNetworkFunctions -------------------------------------------------

class TestStandaloneNetworkFunctions:
    """All 8 standalone functions."""

    def test_kirchhoff_junction_satisfied(self):
        result = kirchhoff_junction_rule_jax(jnp.array([5.0, -3.0, -2.0]))
        assert result["satisfied"]
        assert float(result["sum"]) == pytest.approx(0.0)

    def test_kirchhoff_junction_unsatisfied(self):
        result = kirchhoff_junction_rule_jax(jnp.array([5.0, -3.0, -1.0]))
        assert not result["satisfied"]

    def test_kirchhoff_loop_satisfied(self):
        result = kirchhoff_loop_rule_jax(jnp.array([-10.0, 3.0, 7.0]))
        assert result["satisfied"]

    def test_kirchhoff_loop_unsatisfied(self):
        result = kirchhoff_loop_rule_jax(jnp.array([10.0, 3.0, 7.0]))
        assert not result["satisfied"]

    def test_solve_network_jax(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        result = solve_network_jax(solver.conductance_matrix, solver.current_vector, reference_node=0)
        assert "node_potentials" in result
        assert "branch_currents" in result
        assert "total_power" in result
        assert float(result["node_potentials"][1]) == pytest.approx(1.0, abs=1e-8)

    def test_wheatstone_bridge_balance_jax(self):
        result = wheatstone_bridge_balance_jax(100, 200, 300, 600)
        assert result["is_balanced"]
        assert float(result["balance_error"]) == pytest.approx(0.0)

    def test_wheatstone_bridge_sensitivity_jax(self):
        result = wheatstone_bridge_sensitivity_jax(100, 100, 100, 101, 1.0, 10.0)
        assert "thevenin_voltage" in result
        assert "thevenin_resistance" in result
        assert "galvanometer_current" in result

    def test_reciprocity_theorem_jax(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        result = reciprocity_theorem_jax(G, port1=(1, 0), port2=(0, 1), reference_node=0)
        assert bool(result["is_reciprocal"])


# -- TestJITNetworkSolver -----------------------------------------------------------

class TestJITNetworkSolver:
    """JIT compilation for network solver functions."""

    def test_jit_solve_potentials(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])

        @jax.jit
        def solve(G, I):
            return NetworkSolverJAX(G, I, 0).node_potentials

        result = solve(G, I)
        assert result.shape == (2,)

    def test_jit_wheatstone_balance_error(self):
        @jax.jit
        def balance_error(R1, R2, R3, R4):
            return WheatstoneBridgeJAX._balance_error_jit(R1, R2, R3, R4)

        result = balance_error(100.0, 100.0, 100.0, 100.0)
        assert float(result) == pytest.approx(0.0)

    def test_jit_wheatstone_thevenin(self):
        @jax.jit
        def vth(R1, R2, R3, R4, V):
            return WheatstoneBridgeJAX._thevenin_voltage_jit(R1, R2, R3, R4, V)

        result = vth(100.0, 100.0, 100.0, 100.0, 10.0)
        assert float(result) == pytest.approx(0.0)

    def test_jit_wheatstone_galvanometer(self):
        @jax.jit
        def ig(R1, R2, R3, R4, V, Rg):
            return WheatstoneBridgeJAX._galvanometer_current_jit(R1, R2, R3, R4, V, Rg)

        result = ig(100.0, 100.0, 100.0, 100.0, 10.0, 10.0)
        assert float(result) == pytest.approx(0.0, abs=1e-10)

    def test_jit_branch_currents(self):
        @jax.jit
        def compute_bc(G, I):
            return NetworkSolverJAX(G, I, 0).branch_currents

        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        I = jnp.array([1.0, 0.0])
        result = compute_bc(G, I)
        assert result.shape == (2, 2)


# -- TestAutoDiffNetwork ------------------------------------------------------------

class TestAutoDiffNetwork:
    """Gradients through network solver functions."""

    def test_grad_through_effective_resistance(self):
        def eff_R(G_val):
            G = jnp.array([[2.0, -1.0], [-1.0, G_val]])
            I = jnp.zeros(2, dtype=jnp.float64)
            solver = NetworkSolverJAX(G, I, reference_node=0)
            return solver.effective_resistance(0, 1)

        grad_fn = jax.grad(eff_R)
        g = grad_fn(2.0)
        assert jnp.isfinite(g)

    def test_grad_through_bridge_thevenin(self):
        def vth_of_R4(R4):
            return WheatstoneBridgeJAX(100.0, 100.0, 100.0, R4).thevenin_voltage(10.0)

        grad_fn = jax.grad(vth_of_R4)
        g = grad_fn(100.0)
        assert jnp.isfinite(g)

    def test_grad_through_galvanometer_current(self):
        def ig_of_R4(R4):
            return WheatstoneBridgeJAX(100.0, 100.0, 100.0, R4).galvanometer_current(10.0, 10.0)

        grad_fn = jax.grad(ig_of_R4)
        g = grad_fn(101.0)
        assert jnp.isfinite(g)

    def test_grad_through_total_power(self):
        def power(G_val):
            G = jnp.array([[G_val, -1.0], [-1.0, G_val]])
            I = jnp.array([1.0, 0.0])
            solver = NetworkSolverJAX(G, I, reference_node=0)
            return solver.total_power

        grad_fn = jax.grad(power)
        g = grad_fn(2.0)
        assert jnp.isfinite(g)

    def test_grad_through_kirchhoff_residual(self):
        def max_resid(V_val):
            V = jnp.array([0.0, V_val, 0.0])
            G = jnp.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
            I = V  # For identity G, I = V
            k = KirchhoffJAX(V, G, I, reference_node=0)
            return k.kcl_max_residual

        grad_fn = jax.grad(max_resid)
        g = grad_fn(1.0)
        assert jnp.isfinite(g)


# -- TestVmapNetwork ----------------------------------------------------------------

class TestVmapNetwork:
    """Vmap over network inputs."""

    def test_vmap_over_current_sources(self):
        G = jnp.array([[2.0, -1.0], [-1.0, 2.0]])
        currents = jnp.array([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])

        def solve_with_I(I):
            return NetworkSolverJAX(G, I, 0).node_potentials

        results = jax.vmap(solve_with_I)(currents)
        assert results.shape == (3, 2)

    def test_vmap_over_bridge_R4(self):
        R4s = jnp.array([98.0, 99.0, 100.0, 101.0, 102.0])

        def balance_error(R4):
            return WheatstoneBridgeJAX(100.0, 100.0, 100.0, R4).balance_error

        results = jax.vmap(balance_error)(R4s)
        assert results.shape == (5,)
        assert float(results[2]) == pytest.approx(0.0)

    def test_vmap_over_bridge_voltage(self):
        voltages = jnp.array([1.0, 5.0, 10.0])

        def thevenin(V):
            return WheatstoneBridgeJAX(100.0, 100.0, 100.0, 101.0).thevenin_voltage(V)

        results = jax.vmap(thevenin)(voltages)
        assert results.shape == (3,)
        # Should scale linearly with voltage
        assert jnp.allclose(results[1] / results[0], jnp.array(5.0), rtol=1e-6)

    def test_vmap_transfer_resistance(self):
        """Vmap over different conductance values."""
        G_vals = jnp.array([1.0, 2.0, 3.0])

        def transfer_R(g):
            G = jnp.array([[g * 2, -g], [-g, g * 2]])
            verifier = ReciprocityVerifierJAX(G, reference_node=0)
            return verifier.transfer_resistance(1, 0)

        results = jax.vmap(transfer_R)(G_vals)
        assert results.shape == (3,)

    def test_vmap_kirchhoff_check(self):
        """Vmap over different voltage values."""
        V_vals = jnp.array([0.5, 1.0, 1.5])

        def check_vcl(V_val):
            V = jnp.array([0.0, V_val, 0.0])
            G = jnp.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
            I = V  # For identity G, I = V
            k = KirchhoffJAX(V, G, I, reference_node=0)
            return k.kcl_max_residual

        results = jax.vmap(check_vcl)(V_vals)
        assert results.shape == (3,)
        assert jnp.all(results < 1e-10)


# -- TestNumPyNetworkComparison -----------------------------------------------------

class TestNumPyNetworkComparison:
    """JAX vs NumPy comparison."""

    def test_single_resistor_numpy_equiv(self):
        """JAX: 2 nodes, 1 ohm, 1A -> V=1V."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V_jax = solver.node_potentials
        # NumPy: G = [[1, -1], [-1, 1]], reduced: [1], I_reduced = [1], V = 1
        assert float(V_jax[1]) == pytest.approx(1.0, abs=1e-8)

    def test_series_resistors_numpy_equiv(self):
        """JAX vs manual calculation for series resistors."""
        solver = NetworkSolverJAX.from_edges(
            n_nodes=3,
            edges=[(0, 1, 1.0), (1, 2, 0.5)],
            current_sources=[(2, 1.0)],
            reference_node=0,
        )
        V_jax = solver.node_potentials
        # NumPy: R_total from node 2 to ref = 1 + 2 = 3 ohms
        assert float(V_jax[2]) == pytest.approx(3.0, abs=1e-8)

    def test_wheatstone_balance_numpy_equiv(self):
        """JAX Wheatstone balance matches analytical result."""
        bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)
        assert float(bridge.balance_error) == pytest.approx(0.0)
        # Analytical: R1*R4 = 60000, R2*R3 = 60000
        assert float(bridge.balance_point_R4) == pytest.approx(600.0)


# -- TestVerifyNetworkSolutionJAX ---------------------------------------------------

class TestVerifyNetworkSolutionJAX:
    """verify_network_solution_jax function."""

    def test_valid_solution(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        result = verify_network_solution_jax(
            solver.conductance_matrix, V, solver.current_vector, reference_node=0
        )
        # Non-reference node (node 1) should have small residual
        assert float(result["max_residual"]) < 1e-8
        assert result["kcl_satisfied"]

    def test_power_conservation(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0), (0, -1.0)], reference_node=0
        )
        V = solver.node_potentials
        result = verify_network_solution_jax(
            solver.conductance_matrix, V, solver.current_vector, reference_node=0
        )
        # Source power should equal dissipated power
        assert float(result["power_source"]) == pytest.approx(float(result["power_dissipated"]), rel=1e-6)

    def test_all_keys_present(self):
        solver = NetworkSolverJAX.from_edges(
            n_nodes=2, edges=[(0, 1, 1.0)], current_sources=[(1, 1.0)], reference_node=0
        )
        V = solver.node_potentials
        result = verify_network_solution_jax(
            solver.conductance_matrix, V, solver.current_vector, reference_node=0
        )
        expected_keys = {"max_residual", "kcl_satisfied", "power_source", "power_dissipated"}
        assert set(result.keys()) == expected_keys


# -- TestAnalyzeNetworkJAX ----------------------------------------------------------

class TestAnalyzeNetworkJAX:
    """analyze_network_jax function."""

    def test_simple_network(self):
        edges = [(0, 1, 1.0), (1, 2, 2.0)]
        sources = [(1, 1.0)]
        result = analyze_network_jax(edges, sources, reference_node=0)
        assert "node_potentials" in result
        assert "branch_currents" in result
        assert "total_power" in result
        assert "kirchhoff_verification" in result
        assert "effective_resistances" in result

    def test_kirchhoff_verified(self):
        edges = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, 0.5)]
        sources = [(0, 1.0)]
        result = analyze_network_jax(edges, sources, reference_node=2)
        assert result["kirchhoff_verification"]["kcl_satisfied"]

    def test_bridge_network_analysis(self):
        """Full bridge network analysis."""
        edges = [(0, 1, 0.01), (0, 2, 0.01), (1, 3, 0.01), (2, 3, 0.01), (1, 2, 0.001)]
        sources = [(0, 1.0), (3, -1.0)]
        result = analyze_network_jax(edges, sources, reference_node=3)
        assert float(result["node_potentials"][0]) > 0
        assert result["kirchhoff_verification"]["kcl_satisfied"]
