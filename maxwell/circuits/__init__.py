"""
Circuit Dynamics and Mutual Induction — Maxwell's theory of interacting circuits.

This module implements the dynamics of electromagnetism, self and mutual induction
as described in Maxwell's Treatise, Part IV, Articles 578-584:

- Self-inductance and magnetic energy (Arts. 578-580)
- Mutual inductance and coupled circuits (Arts. 581-582)
- Mutual induction EMF (Art. 583)
- Force and torque between circuits (Art. 584)

Classes:
    Circuit: Single circuit with self-inductance and resistance.
    CoupledCircuits: Two magnetically coupled circuits.

Functions:
    calc_solenoid_inductance: L = 4πn²A/l for solenoid.
    calc_self_inductance: Self-inductance from geometry.
    calc_mutual_inductance: Mutual inductance between circuits.
    calc_coupling_coefficient: k = M/√(L₁L₂).
    calc_emf_from_mutual_inductance: EMF = -M·dI/dt.
    calc_force_between_circuits: F = I₁I₂ ∂M/∂x.
    calc_torque_between_circuits: τ = I₁I₂ ∂M/∂θ.
    analyze_circuit_system: Complete system analysis.
    verify_energy_conservation: Verify T = (1/2)ΣL_ij I_i I_j.
    verify_circuit_dynamics: Complete theory verification.

References:
    Maxwell, Treatise on Electricity and Magnetism, Part IV, Arts. 578-584.
"""

from maxwell.circuits.dynamics import (
    Circuit,
    CoupledCircuits,
    calc_solenoid_inductance,
    calc_self_inductance,
    calc_mutual_inductance,
    calc_coupling_coefficient,
    calc_emf_from_mutual_inductance,
    calc_force_between_circuits,
    calc_torque_between_circuits,
    analyze_circuit_system,
    verify_energy_conservation,
    verify_circuit_dynamics,
)

__all__ = [
    # Classes
    "Circuit",
    "CoupledCircuits",
    # Functions
    "calc_solenoid_inductance",
    "calc_self_inductance",
    "calc_mutual_inductance",
    "calc_coupling_coefficient",
    "calc_emf_from_mutual_inductance",
    "calc_force_between_circuits",
    "calc_torque_between_circuits",
    "analyze_circuit_system",
    "verify_energy_conservation",
    "verify_circuit_dynamics",
]
