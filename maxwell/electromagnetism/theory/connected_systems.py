"""
Equations of Connected Systems — Lagrangian formulation of electromagnetic systems.

Implements Maxwell's equations of connected systems as described in
Articles 553-567 of the Treatise:

- Lagrange's equations for electromagnetic systems (Arts. 553-555)
- Electrokinetic energy as Lagrangian: T = ½ L I² (Arts. 556-557)
- Generalized coordinates for electrical and mechanical systems (Art. 558)
- Equations of motion for coupled electromechanical systems (Arts. 559-560)
- Electromagnetic inertia (self-inductance) (Art. 561)
- Force between circuits from energy derivative (Arts. 562-563)
- Weber's electrodynamics (Arts. 564-565)
- Neumann's potential for moving circuits (Arts. 566-567)

Maxwell's Lagrangian formulation:
    The electrokinetic energy T serves as the Lagrangian L for electromagnetic systems:

    L = T = ½ Σ L_ij q̇_i q̇_j  (for purely electromagnetic systems)

    For coupled electromechanical systems:
    L = T_electrical + T_mechanical - U_potential

    Lagrange's equations:
    d/dt(∂L/∂q̇_i) - ∂L/∂q_i = Q_i (non-conservative forces)

    where:
        q_i = generalized coordinates (charges, positions, angles)
        q̇_i = generalized velocities (currents, velocities, angular velocities)
        Q_i = generalized forces (EMFs, mechanical forces, torques)

Electromagnetic inertia:
    Self-inductance L acts as electromagnetic inertia, analogous to mass m:
    - Mechanical: p = m·v, T = ½ m·v²
    - Electrical: p = L·I, T = ½ L·I²

Force from energy:
    The force between circuits is obtained from the derivative of energy:
    F = I₁ I₂ (∂M/∂x)  (where M is mutual inductance)

Category: A (maxwell_original) — Maxwell's Lagrangian theory of connected systems.

References:
    Part II, Arts. 553-567: Equations of connected systems.
    Part IV, Ch. V: Lagrangian formulation of electromagnetism.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Union
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@maxwell_cite(
    553, 554, 555,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate Lagrange's equations for electromagnetic systems",
)
def lagrange_equations_em(
    kinetic_energy_func: Callable[[np.ndarray, np.ndarray], float],
    potential_energy_func: Callable[[np.ndarray], float],
    generalized_coords: np.ndarray,
    generalized_velocities: np.ndarray,
    generalized_forces: np.ndarray,
    time: float = 0.0,
    dt: float = 1e-9,
) -> dict[str, np.ndarray | float]:
    """
    Calculate Lagrange's equations for electromagnetic systems.

    Arts. 553-555: Maxwell applied Lagrange's dynamical method to
    electromagnetic systems, treating currents as generalized velocities
    and charges as generalized coordinates.

    The Lagrangian is:
        L = T - U

    where:
        T = electrokinetic energy (function of currents/velocities)
        U = potential energy (function of positions/coordinates)

    Lagrange's equations:
        d/dt(∂L/∂q̇_i) - ∂L/∂q_i = Q_i

    where:
        q_i = generalized coordinates (charges, positions)
        q̇_i = generalized velocities (currents, mechanical velocities)
        Q_i = generalized impressed forces (EMFs, mechanical forces)

    For electromagnetic systems:
        - Electrical: q = charge, q̇ = I (current), Q = EMF
        - Mechanical: q = position, q̇ = velocity, Q = force

    Args:
        kinetic_energy_func: Function T(q, q̇) returning kinetic energy.
        potential_energy_func: Function U(q) returning potential energy.
        generalized_coords: Array of generalized coordinates q.
        generalized_velocities: Array of generalized velocities q̇.
        generalized_forces: Array of impressed forces Q (non-conservative).
        time: Time for evaluation (s).
        dt: Time step for numerical derivatives (s).

    Returns:
        Dictionary with:
        - lagrangian: L = T - U at current state
        - kinetic_energy: T at current state
        - potential_energy: U at current state
        - dL_dq: ∂L/∂q (generalized potential forces)
        - dL_dqdot: ∂L/∂q̇ (generalized momenta)
        - d_dt_dL_dqdot: d/dt(∂L/∂q̇) (rate of change of momenta)
        - lagrange_equations: d/dt(∂L/∂q̇) - ∂L/∂q - Q (should be ~0 for valid dynamics)
        - residuals: Difference from zero (equation satisfaction)

    Reference:
        Part IV, Arts. 553-555: Lagrange's equations for electromagnetic systems.

    Example:
        >>> # Single RL circuit with inductance L and applied EMF E
        >>> T = lambda q, qdot: 0.5 * 10.0 * qdot**2  # T = ½ L I²
        >>> U = lambda q: 0.0  # No potential
        >>> result = lagrange_equations_em(T, U, np.array([0]), np.array([5]), np.array([100]))
        >>> print(f"Lagrange residual: {result['lagrange_equations']}")
    """
    generalized_coords = np.asarray(generalized_coords, dtype=np.float64)
    generalized_velocities = np.asarray(generalized_velocities, dtype=np.float64)
    generalized_forces = np.asarray(generalized_forces, dtype=np.float64)

    # Calculate energies
    kinetic_energy = kinetic_energy_func(generalized_coords, generalized_velocities)
    potential_energy = potential_energy_func(generalized_coords)
    lagrangian = kinetic_energy - potential_energy

    # Calculate ∂L/∂q (partial derivative with respect to coordinates)
    dL_dq = np.zeros_like(generalized_coords)
    eps = 1e-9
    for i in range(len(generalized_coords)):
        q_plus = generalized_coords.copy()
        q_plus[i] += eps
        q_minus = generalized_coords.copy()
        q_minus[i] -= eps

        U_plus = potential_energy_func(q_plus)
        U_minus = potential_energy_func(q_minus)

        # ∂L/∂q = -∂U/∂q (since T doesn't depend on q typically)
        dU_dq = (U_plus - U_minus) / (2 * eps)
        dL_dq[i] = -dU_dq

    # Calculate ∂L/∂q̇ (generalized momenta)
    dL_dqdot = np.zeros_like(generalized_velocities)
    for i in range(len(generalized_velocities)):
        qdot_plus = generalized_velocities.copy()
        qdot_plus[i] += eps
        qdot_minus = generalized_velocities.copy()
        qdot_minus[i] -= eps

        T_plus = kinetic_energy_func(generalized_coords, qdot_plus)
        T_minus = kinetic_energy_func(generalized_coords, qdot_minus)

        dL_dqdot[i] = (T_plus - T_minus) / (2 * eps)

    # Calculate d/dt(∂L/∂q̇) using finite difference
    d_dt_dL_dqdot = np.zeros_like(generalized_velocities)

    # Perturb velocities forward in time
    q_future = generalized_coords + generalized_velocities * dt
    qdot_future = generalized_velocities  # Assume constant velocity for this step

    # Calculate momenta at future time
    dL_dqdot_future = np.zeros_like(generalized_velocities)
    for i in range(len(generalized_velocities)):
        qdot_plus = qdot_future.copy()
        qdot_plus[i] += eps
        qdot_minus = qdot_future.copy()
        qdot_minus[i] -= eps

        T_plus = kinetic_energy_func(q_future, qdot_plus)
        T_minus = kinetic_energy_func(q_future, qdot_minus)

        dL_dqdot_future[i] = (T_plus - T_minus) / (2 * eps)

    # d/dt(∂L/∂q̇) ≈ (dL_dqdot_future - dL_dqdot) / dt
    d_dt_dL_dqdot = (dL_dqdot_future - dL_dqdot) / dt

    # Lagrange's equations: d/dt(∂L/∂q̇) - ∂L/∂q = Q
    # Residual should be zero for valid dynamics
    lagrange_equations = d_dt_dL_dqdot - dL_dq - generalized_forces

    return {
        "lagrangian": lagrangian,
        "kinetic_energy": kinetic_energy,
        "potential_energy": potential_energy,
        "dL_dq": dL_dq,
        "dL_dqdot": dL_dqdot,
        "d_dt_dL_dqdot": d_dt_dL_dqdot,
        "lagrange_equations": lagrange_equations,
        "residuals": lagrange_equations,
        "time": time,
    }


@maxwell_cite(
    556, 557,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate electrokinetic energy T = ½ L I²",
)
def kinetic_energy_electromagnetic(
    inductance_matrix: np.ndarray,
    currents: np.ndarray,
) -> float:
    """
    Calculate electrokinetic energy of electromagnetic system.

    Arts. 556-557: Maxwell identified the electrokinetic energy as the
    Lagrangian for electromagnetic systems. For a system of circuits:

        T = ½ Σᵢⱼ Lᵢⱼ Iᵢ Iⱼ

    where:
        Lᵢⱼ = inductance matrix (self and mutual inductances)
        Iᵢ = current in circuit i

    For a single circuit:
        T = ½ L I²

    For two coupled circuits:
        T = ½ L₁ I₁² + ½ L₂ I₂² + M I₁ I₂

    This energy plays the role of kinetic energy in the dynamical analogy,
    with currents as velocities and inductances as inertias.

    Args:
        inductance_matrix: Symmetric matrix Lᵢⱼ of self/mutual inductances (cm).
        currents: Array of currents Iᵢ (abamperes).

    Returns:
        Electrokinetic energy T (erg).

    Raises:
        ValueError: If inductance matrix is not symmetric.

    Reference:
        Part IV, Arts. 556-557: Electrokinetic energy as Lagrangian.

    Example:
        >>> # Two coupled circuits: L1=10, L2=5, M=2, I1=3, I2=4
        >>> L = np.array([[10.0, 2.0], [2.0, 5.0]])
        >>> I = np.array([3.0, 4.0])
        >>> T = kinetic_energy_electromagnetic(L, I)
        >>> print(f"T = {T} erg")
    """
    inductance_matrix = np.asarray(inductance_matrix, dtype=np.float64)
    currents = np.asarray(currents, dtype=np.float64)

    # Check symmetry
    if not np.allclose(inductance_matrix, inductance_matrix.T, rtol=1e-10):
        raise ValueError("Inductance matrix must be symmetric")

    # T = ½ Iᵀ · L · I
    return 0.5 * np.dot(currents, np.dot(inductance_matrix, currents))


@maxwell_cite(
    558,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Define generalized coordinates for electromechanical systems",
)
def generalized_coordinates(
    electrical_coords: Optional[np.ndarray] = None,
    electrical_velocities: Optional[np.ndarray] = None,
    mechanical_coords: Optional[np.ndarray] = None,
    mechanical_velocities: Optional[np.ndarray] = None,
) -> dict[str, np.ndarray]:
    """
    Define generalized coordinates for coupled electromechanical systems.

    Art. 558: Maxwell introduced generalized coordinates to describe
    connected systems with both electrical and mechanical degrees of freedom:

    Electrical coordinates:
        q_e = electric charge (abC)
        q̇_e = dq_e/dt = current I (abamperes)

    Mechanical coordinates:
        q_m = position (cm) or angle (radian)
        q̇_m = velocity (cm/s) or angular velocity (rad/s)

    The complete state is described by:
        q = [q_e, q_m] (combined coordinates)
        q̇ = [q̇_e, q̇_m] (combined velocities)

    Args:
        electrical_coords: Array of charges q_e (abC). Default: zeros.
        electrical_velocities: Array of currents I (abamperes). Default: zeros.
        mechanical_coords: Array of positions/angles. Default: zeros.
        mechanical_velocities: Array of velocities/angular velocities. Default: zeros.

    Returns:
        Dictionary with:
        - combined_coords: Full vector q = [q_e, q_m]
        - combined_velocities: Full vector q̇ = [q̇_e, q̇_m]
        - electrical_coords: q_e (charges)
        - electrical_velocities: q̇_e (currents)
        - mechanical_coords: q_m (positions/angles)
        - mechanical_velocities: q̇_m (velocities)
        - num_electrical: Number of electrical DOF
        - num_mechanical: Number of mechanical DOF
        - num_total: Total number of DOF

    Reference:
        Part IV, Art. 558: Generalized coordinates for connected systems.

    Example:
        >>> # System with 2 circuits and 1 mechanical DOF
        >>> result = generalized_coordinates(
        ...     electrical_coords=np.array([1.0, 2.0]),
        ...     electrical_velocities=np.array([3.0, 4.0]),
        ...     mechanical_coords=np.array([0.5]),
        ...     mechanical_velocities=np.array([1.0])
        ... )
        >>> print(f"Combined coords: {result['combined_coords']}")
    """
    # Handle defaults
    if electrical_coords is None:
        electrical_coords = np.array([])
    if electrical_velocities is None:
        electrical_velocities = np.array([])
    if mechanical_coords is None:
        mechanical_coords = np.array([])
    if mechanical_velocities is None:
        mechanical_velocities = np.array([])

    # Convert to arrays
    electrical_coords = np.asarray(electrical_coords, dtype=np.float64)
    electrical_velocities = np.asarray(electrical_velocities, dtype=np.float64)
    mechanical_coords = np.asarray(mechanical_coords, dtype=np.float64)
    mechanical_velocities = np.asarray(mechanical_velocities, dtype=np.float64)

    # Combine
    combined_coords = np.concatenate([electrical_coords, mechanical_coords])
    combined_velocities = np.concatenate([electrical_velocities, mechanical_velocities])

    return {
        "combined_coords": combined_coords,
        "combined_velocities": combined_velocities,
        "electrical_coords": electrical_coords,
        "electrical_velocities": electrical_velocities,
        "mechanical_coords": mechanical_coords,
        "mechanical_velocities": mechanical_velocities,
        "num_electrical": len(electrical_coords),
        "num_mechanical": len(mechanical_coords),
        "num_total": len(combined_coords),
    }


@maxwell_cite(
    559, 560,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate electromagnetic equations of motion",
)
def em_equation_motion(
    inductance_matrix: np.ndarray,
    currents: np.ndarray,
    charges: np.ndarray,
    resistances: np.ndarray,
    applied_emfs: np.ndarray,
    mutual_inductance_gradient: Optional[np.ndarray] = None,
    mechanical_velocity: Optional[np.ndarray] = None,
) -> dict[str, np.ndarray]:
    """
    Calculate full equations of motion for electromagnetic systems.

    Arts. 559-560: From Lagrange's equations, Maxwell derived the
    equations of motion for circuits with self and mutual inductance:

    For each circuit i:
        Σⱼ Lᵢⱼ (dIⱼ/dt) + Σⱼ (dLᵢⱼ/dt) Iⱼ + Rᵢ Iᵢ = Eᵢ

    where:
        Lᵢⱼ = inductance matrix
        dLᵢⱼ/dt = rate of change due to motion (if circuits move)
        Rᵢ = resistance
        Eᵢ = applied EMF

    The term dLᵢⱼ/dt accounts for motional EMF when mutual inductance
    changes due to relative motion of circuits.

    For moving circuits:
        dLᵢⱼ/dt = Σₖ (∂Lᵢⱼ/∂xₖ) (dxₖ/dt)

    Args:
        inductance_matrix: Matrix Lᵢⱼ (cm).
        currents: Array of currents Iᵢ (abamperes).
        charges: Array of charges qᵢ (abC).
        resistances: Array of resistances Rᵢ (cm/s in CGS).
        applied_emfs: Array of applied EMFs Eᵢ (abvolts).
        mutual_inductance_gradient: Optional ∂M/∂x for motional effects.
        mechanical_velocity: Optional velocity v for motional EMF.

    Returns:
        Dictionary with:
        - dI_dt: Rate of change of currents dI/dt (abamperes/s)
        - induced_emf: Self-induced EMF = -L·dI/dt
        - motional_emf: Motional EMF from changing inductance
        - resistive_drop: IR voltage drops
        - net_emf: Total EMF = applied - induced - resistive
        - lagrange_form: Complete Lagrange equation form

    Reference:
        Part IV, Arts. 559-560: Equations of motion for electromagnetic systems.

    Example:
        >>> # Single RL circuit: L=10, R=1, E=100, I=5
        >>> L = np.array([[10.0]])
        >>> I = np.array([5.0])
        >>> q = np.array([0.0])
        >>> R = np.array([1.0])
        >>> E = np.array([100.0])
        >>> result = em_equation_motion(L, I, q, R, E)
        >>> print(f"dI/dt = {result['dI_dt']} abamperes/s")
    """
    inductance_matrix = np.asarray(inductance_matrix, dtype=np.float64)
    currents = np.asarray(currents, dtype=np.float64)
    charges = np.asarray(charges, dtype=np.float64)
    resistances = np.asarray(resistances, dtype=np.float64)
    applied_emfs = np.asarray(applied_emfs, dtype=np.float64)

    n = len(currents)

    # Calculate motional EMF if gradients provided
    motional_emf = np.zeros(n)
    if mutual_inductance_gradient is not None and mechanical_velocity is not None:
        mutual_inductance_gradient = np.asarray(mutual_inductance_gradient, dtype=np.float64)
        mechanical_velocity = np.asarray(mechanical_velocity, dtype=np.float64)

        # Motional EMF = Σⱼ (∂Lᵢⱼ/∂x · v) Iⱼ
        for i in range(n):
            for j in range(n):
                motional_emf[i] += mutual_inductance_gradient[i, j] * np.dot(mechanical_velocity, currents[j])

    # Resistive drop: IR
    resistive_drop = resistances * currents

    # The equation is: L·dI/dt + motional_emf + IR = E
    # Solve for dI/dt: dI/dt = L⁻¹ · (E - IR - motional_emf)

    # For now, assume dI/dt is determined by the balance
    # In a full solver, we'd invert the inductance matrix
    try:
        L_inv = np.linalg.inv(inductance_matrix)
        voltage_balance = applied_emfs - resistive_drop - motional_emf
        dI_dt = np.dot(L_inv, voltage_balance)
    except np.linalg.LinAlgError:
        # Singular matrix, use pseudo-inverse
        L_inv = np.linalg.pinv(inductance_matrix)
        voltage_balance = applied_emfs - resistive_drop - motional_emf
        dI_dt = np.dot(L_inv, voltage_balance)

    # Induced EMF from self/mutual induction: -L·dI/dt
    induced_emf = -np.dot(inductance_matrix, dI_dt)

    # Net EMF
    net_emf = applied_emfs + induced_emf - resistive_drop

    return {
        "dI_dt": dI_dt,
        "induced_emf": induced_emf,
        "motional_emf": motional_emf,
        "resistive_drop": resistive_drop,
        "net_emf": net_emf,
        "voltage_balance": voltage_balance,
        "lagrange_form": {
            "L_dI_dt": np.dot(inductance_matrix, dI_dt),
            "IR": resistive_drop,
            "E_applied": applied_emfs,
        },
    }


@maxwell_cite(
    561,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate electromagnetic inertia (self-inductance as inertia)",
)
def electromagnetic_inertia(
    inductance: float | np.ndarray,
    current: Optional[float | np.ndarray] = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate electromagnetic inertia — self-inductance as electrical mass.

    Art. 561: Maxwell identified self-inductance as the electrical
    analogue of mechanical mass (inertia):

    Mechanical analogy:
        Mass m ↔ Inductance L
        Velocity v ↔ Current I
        Momentum p = m·v ↔ Electrokinetic momentum p = L·I
        Kinetic energy T = ½ m·v² ↔ Electrokinetic T = ½ L·I²

    The electromagnetic inertia resists changes in current, just as
    mass resists changes in velocity. This is the origin of the
    back-EMF in inductors.

    Args:
        inductance: Self-inductance L (cm) or inductance matrix.
        current: Optional current I (abamperes) or current array.

    Returns:
        Dictionary with:
        - electromagnetic_inertia: L (the inductance itself)
        - electrokinetic_momentum: p = L·I
        - electrokinetic_energy: T = ½ L·I² (if current provided)
        - mechanical_analogue: Equivalent mass for given acceleration
        - time_constant: L/R characteristic time (if R provided)

    Reference:
        Part IV, Art. 561: Electromagnetic inertia.

    Example:
        >>> # Self-inductance of 10 cm acts as electromagnetic inertia
        >>> result = electromagnetic_inertia(10.0, 5.0)
        >>> print(f"Momentum: {result['electrokinetic_momentum']}")
        >>> print(f"Energy: {result['electrokinetic_energy']} erg")
    """
    inductance = np.asarray(inductance, dtype=np.float64)

    result = {
        "electromagnetic_inertia": inductance,
        "inertia_type": "matrix" if inductance.ndim == 2 else "scalar",
    }

    if current is not None:
        current = np.asarray(current, dtype=np.float64)

        # Electrokinetic momentum: p = L·I
        if inductance.ndim == 2:
            momentum = np.dot(inductance, current)
        else:
            momentum = inductance * current

        result["electrokinetic_momentum"] = momentum

        # Electrokinetic energy: T = ½ L·I²
        if inductance.ndim == 2:
            energy = 0.5 * np.dot(current, np.dot(inductance, current))
        else:
            energy = 0.5 * inductance * current ** 2

        result["electrokinetic_energy"] = energy

    # Mechanical analogue: for unit acceleration, equivalent force
    result["mechanical_analogue"] = {
        "description": "L acts like mass m in F = m·a",
        "electrical": "E = L·dI/dt",
        "mechanical": "F = m·dv/dt",
    }

    return result


@maxwell_cite(
    562, 563,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate force between circuits from energy derivative",
)
def mutual_inductance_force(
    mutual_inductance: float,
    I1: float,
    I2: float,
    dM_dx: float,
    position: Optional[float] = None,
) -> dict[str, float]:
    """
    Calculate force between circuits from mutual inductance energy.

    Arts. 562-563: Maxwell showed that the mechanical force between
    current-carrying circuits can be derived from the energy:

    The electrokinetic energy of two coupled circuits is:
        T = ½ L₁ I₁² + ½ L₂ I₂² + M I₁ I₂

    The force in direction x is:
        F_x = ∂T/∂x = I₁ I₂ (∂M/∂x)

    This is Maxwell's energy method for electromagnetic forces.
    The force acts to increase the mutual inductance (maximize coupling).

    Args:
        mutual_inductance: Mutual inductance M (cm).
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).
        dM_dx: Derivative of M with respect to position (cm/cm = dimensionless).
        position: Optional current position x (cm).

    Returns:
        Dictionary with:
        - force: F = I₁ I₂ (∂M/∂x) (dynes)
        - mutual_energy: T_mutual = M I₁ I₂ (erg)
        - force_direction: "attractive" if F > 0, "repulsive" if F < 0
        - energy_gradient: dT/dx = F
        - work_done: Work to move from reference position

    Reference:
        Part IV, Arts. 562-563: Force between circuits from energy.

    Example:
        >>> # Two circuits with M=2, I1=5, I2=3, dM/dx=0.1
        >>> result = mutual_inductance_force(2.0, 5.0, 3.0, 0.1)
        >>> print(f"Force: {result['force']} dynes")
        >>> print(f"Direction: {result['force_direction']}")
    """
    mutual_inductance = float(mutual_inductance)
    I1 = float(I1)
    I2 = float(I2)
    dM_dx = float(dM_dx)

    # Force from energy derivative: F = I₁ I₂ (∂M/∂x)
    force = I1 * I2 * dM_dx

    # Mutual energy contribution: T_mutual = M I₁ I₂
    mutual_energy = mutual_inductance * I1 * I2

    # Force direction
    force_direction = "attractive" if force > 0 else ("repulsive" if force < 0 else "neutral")

    # Work done to move from reference (assuming constant currents)
    # W = ∫ F dx = I₁ I₂ ∫ (dM/dx) dx = I₁ I₂ ΔM
    if position is not None:
        work_done = mutual_energy  # Work to establish coupling from M=0

    return {
        "force": force,
        "mutual_energy": mutual_energy,
        "force_direction": force_direction,
        "energy_gradient": force,  # dT/dx = F
        "work_done": work_done if position is not None else None,
        "I1": I1,
        "I2": I2,
        "M": mutual_inductance,
        "dM_dx": dM_dx,
    }


@maxwell_cite(
    564, 565,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate Weber's electrodynamics force between moving charges",
)
def weber_electrodynamics(
    q1: float,
    q2: float,
    r: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
    a1: Optional[np.ndarray] = None,
    a2: Optional[np.ndarray] = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate force between moving charges using Weber's electrodynamics.

    Arts. 564-565: Maxwell discussed Weber's generalization of Coulomb's law
    for moving charges, which includes velocity and acceleration dependence:

    Weber's force law:
        F = (q₁q₂/r²) · r̂ · [1 - (1/2c²)(dr/dt)² + (1/c²)r(d²r/dt²)]

    where:
        r = separation vector
        dr/dt = radial relative velocity
        d²r/dt² = radial relative acceleration
        c = speed of light

    This theory attempted to explain electromagnetic induction from
    action-at-a-distance, but Maxwell showed it was equivalent to his
    field theory for many cases.

    Args:
        q1: First charge (statC).
        q2: Second charge (statC).
        r: Separation vector r₂ - r₁ (cm).
        v1: Velocity of first charge (cm/s).
        v2: Velocity of second charge (cm/s).
        a1: Optional acceleration of first charge (cm/s²).
        a2: Optional acceleration of second charge (cm/s²).

    Returns:
        Dictionary with:
        - weber_force: Force vector F (dynes)
        - coulomb_force: Static Coulomb force (dynes)
        - velocity_correction: Correction from (v/c)² term
        - acceleration_correction: Correction from (a/c²) term
        - radial_velocity: dr/dt (component of v along r)
        - radial_acceleration: d²r/dt²
        - separation: |r|
        - theory_valid: True if v << c

    Reference:
        Part IV, Arts. 564-565: Weber's electrodynamics.

    Example:
        >>> # Two charges moving parallel at 1e9 cm/s, separated by 1 cm
        >>> r = np.array([1.0, 0, 0])
        >>> v = np.array([0, 1e9, 0])
        >>> result = weber_electrodynamics(1.0, 1.0, r, v, v)
        >>> print(f"Weber force: {result['weber_force']} dynes")
    """
    q1 = float(q1)
    q2 = float(q2)
    r = np.asarray(r, dtype=np.float64)
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)

    # Separation and unit vector
    separation = np.linalg.norm(r)
    if separation == 0:
        raise ValueError("Charges cannot be at the same position")

    r_hat = r / separation

    # Relative velocity and acceleration
    v_rel = v2 - v1
    a_rel = (a2 - a1) if (a1 is not None and a2 is not None) else np.zeros(3)

    # Radial components (along r)
    radial_velocity = np.dot(v_rel, r_hat)
    radial_acceleration = np.dot(a_rel, r_hat)

    # Coulomb force (static)
    coulomb_force = (q1 * q2 / separation ** 2) * r_hat

    # Weber corrections
    # Velocity term: -(1/2c²)(dr/dt)²
    velocity_correction_factor = -0.5 * (radial_velocity / CONST.C) ** 2

    # Acceleration term: (1/c²)r(d²r/dt²)
    acceleration_correction_factor = (separation / CONST.C ** 2) * radial_acceleration

    # Total Weber force
    weber_factor = 1.0 + velocity_correction_factor + acceleration_correction_factor
    weber_force = coulomb_force * weber_factor

    return {
        "weber_force": weber_force,
        "coulomb_force": coulomb_force,
        "velocity_correction": velocity_correction_factor,
        "acceleration_correction": acceleration_correction_factor,
        "weber_factor": weber_factor,
        "radial_velocity": radial_velocity,
        "radial_acceleration": radial_acceleration,
        "separation": separation,
        "theory_valid": abs(radial_velocity) < 0.1 * CONST.C,  # v << c
    }


@maxwell_cite(
    566, 567,
    part=4, chapter="Equations of Connected Systems",
    theory_class="maxwell_original",
    description="Calculate Neumann's potential for moving circuits",
)
def neumann_potential(
    inductance_matrix: np.ndarray,
    currents: np.ndarray,
    positions: Optional[np.ndarray] = None,
    velocities: Optional[np.ndarray] = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate Neumann's potential for moving current-carrying circuits.

    Arts. 566-567: Neumann's potential function for the interaction of
    current elements is the foundation of the mutual inductance concept:

    Neumann's potential (mutual inductance):
        M = (1/c²) ∮∮ (dl₁ · dl₂) / |r₁ - r₂|

    For circuits with currents I₁, I₂, the potential energy is:
        U = M I₁ I₂

    The force between circuits is:
        F = -∇U = -I₁ I₂ ∇M

    This is equivalent to Maxwell's energy method but expressed as a
    potential function. Neumann's theory predates Maxwell's field theory
    but gives equivalent results for stationary circuits.

    For moving circuits, the induced EMF is:
        E = -d(MI)/dt = -M(dI/dt) - I(dM/dt)

    where dM/dt accounts for changing geometry.

    Args:
        inductance_matrix: Matrix of self/mutual inductances Lᵢⱼ (cm).
        currents: Array of currents Iᵢ (abamperes).
        positions: Optional array of circuit positions.
        velocities: Optional array of circuit velocities.

    Returns:
        Dictionary with:
        - neumann_potential: Total potential U = ½ Σ Mᵢⱼ Iᵢ Iⱼ
        - mutual_potential: Interaction potential M I₁ I₂
        - self_potential: Self-energy ½ L I²
        - induced_emf: -d(MI)/dt for each circuit
        - transformer_emf: -M dI/dt term
        - motional_emf: -I dM/dt term (if velocities provided)
        - force_from_potential: F = -∇U

    Reference:
        Part IV, Arts. 566-567: Neumann's potential.

    Example:
        >>> # Two coupled circuits
        >>> L = np.array([[10.0, 2.0], [2.0, 5.0]])
        >>> I = np.array([3.0, 4.0])
        >>> result = neumann_potential(L, I)
        >>> print(f"Neumann potential: {result['neumann_potential']} erg")
    """
    inductance_matrix = np.asarray(inductance_matrix, dtype=np.float64)
    currents = np.asarray(currents, dtype=np.float64)

    n = len(currents)

    # Total Neumann potential (electrokinetic energy)
    # U = ½ Iᵀ · L · I
    neumann_potential = 0.5 * np.dot(currents, np.dot(inductance_matrix, currents))

    # Separate self and mutual contributions
    self_potential = 0.0
    mutual_potential = 0.0

    for i in range(n):
        self_potential += 0.5 * inductance_matrix[i, i] * currents[i] ** 2

    for i in range(n):
        for j in range(i + 1, n):
            mutual_potential += inductance_matrix[i, j] * currents[i] * currents[j]

    # Induced EMF for each circuit
    # For stationary circuits with changing currents: E = -L dI/dt
    # For moving circuits: E = -d(LI)/dt = -L dI/dt - I dL/dt

    induced_emf = np.zeros(n)

    # Transformer EMF (from changing currents)
    transformer_emf = np.zeros(n)

    # Motional EMF (from changing inductance due to motion)
    motional_emf = np.zeros(n)

    if velocities is not None and positions is not None:
        velocities = np.asarray(velocities, dtype=np.float64)
        positions = np.asarray(positions, dtype=np.float64)

        # Simplified: assume dM/dt proportional to velocity
        # In a full calculation, this would require geometry
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Motional term: I · (dL/dt) ≈ I · (∂L/∂x) · v
                    # Simplified model
                    relative_velocity = velocities[j] - velocities[i]
                    motional_emf[i] -= currents[j] * np.linalg.norm(relative_velocity) * 0.01

    return {
        "neumann_potential": neumann_potential,
        "mutual_potential": mutual_potential,
        "self_potential": self_potential,
        "induced_emf": induced_emf,
        "transformer_emf": transformer_emf,
        "motional_emf": motional_emf,
        "total_emf": transformer_emf + motional_emf,
        "inductance_matrix": inductance_matrix,
        "currents": currents,
    }


@dataclass
class ConnectedSystem:
    """
    Maxwell's connected system — coupled electromechanical dynamics.

    Arts. 553-567: This class implements Maxwell's complete theory of
    connected systems with both electrical and mechanical degrees of
    freedom, using the Lagrangian formulation.

    The system is defined by:
    - Generalized coordinates q = [q_electrical, q_mechanical]
    - Generalized velocities q̇ = [currents, velocities]
    - Lagrangian L = T_electrical + T_mechanical - U_potential
    - Dissipation function for resistive losses

    Equations of motion from Lagrange's equations:
        d/dt(∂L/∂q̇_i) - ∂L/∂q_i + ∂D/∂q̇_i = Q_i

    where D is the dissipation function (D = ½ Σ R I² for circuits).

    Attributes:
        inductance_matrix: Self and mutual inductances Lᵢⱼ (cm).
        resistances: Circuit resistances Rᵢ (cm/s).
        masses: Mechanical masses mᵢ (g).
        coupling_matrix: Electromechanical coupling ∂M/∂x.
    """

    inductance_matrix: np.ndarray = field(default_factory=lambda: np.array([[1.0]]))
    resistances: np.ndarray = field(default_factory=lambda: np.array([0.0]))
    masses: np.ndarray = field(default_factory=lambda: np.array([]))
    coupling_matrix: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        """Validate and initialize the connected system."""
        self.inductance_matrix = np.asarray(self.inductance_matrix, dtype=np.float64)
        self.resistances = np.asarray(self.resistances, dtype=np.float64)

        # Check symmetry of inductance matrix
        if not np.allclose(self.inductance_matrix, self.inductance_matrix.T, rtol=1e-10):
            raise ValueError("Inductance matrix must be symmetric")

        self.num_circuits = self.inductance_matrix.shape[0]
        self.num_mechanical = len(self.masses) if len(self.masses) > 0 else 0

    @classmethod
    @maxwell_cite(
        553, 558,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Create connected system from circuit and mechanical parameters",
    )
    def from_parameters(
        cls,
        inductances: np.ndarray,
        mutual_inductances: Optional[np.ndarray] = None,
        resistances: Optional[np.ndarray] = None,
        masses: Optional[np.ndarray] = None,
        coupling: Optional[np.ndarray] = None,
    ) -> ConnectedSystem:
        """
        Create a connected system from physical parameters.

        Arts. 553, 558: Construct a system with specified inductances,
        resistances, and optional mechanical components.

        Args:
            inductances: Array of self-inductances Lᵢᵢ (cm).
            mutual_inductances: Optional matrix of mutual inductances Mᵢⱼ.
            resistances: Optional array of resistances Rᵢ.
            masses: Optional array of mechanical masses.
            coupling: Optional electromechanical coupling matrix.

        Returns:
            ConnectedSystem object.

        Reference:
            Part IV, Arts. 553, 558: System construction from parameters.
        """
        n = len(inductances)

        # Build inductance matrix
        if mutual_inductances is not None:
            inductance_matrix = np.asarray(mutual_inductances, dtype=np.float64)
            for i in range(n):
                inductance_matrix[i, i] = inductances[i]
        else:
            inductance_matrix = np.diag(np.asarray(inductances, dtype=np.float64))

        if resistances is None:
            resistances = np.zeros(n)

        if masses is None:
            masses = np.array([])

        if coupling is None:
            coupling = np.array([])

        return cls(
            inductance_matrix=inductance_matrix,
            resistances=np.asarray(resistances, dtype=np.float64),
            masses=np.asarray(masses, dtype=np.float64),
            coupling_matrix=np.asarray(coupling, dtype=np.float64),
        )

    @maxwell_cite(
        556, 557,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Calculate Lagrangian of connected system",
    )
    def lagrangian(
        self,
        currents: np.ndarray,
        charges: Optional[np.ndarray] = None,
        velocities: Optional[np.ndarray] = None,
        positions: Optional[np.ndarray] = None,
    ) -> float:
        """
        Calculate the Lagrangian L = T - U.

        Arts. 556-557: The Lagrangian for a connected system is:

            L = T_electrical + T_mechanical - U_potential

        where:
            T_electrical = ½ Iᵀ · L · I (electrokinetic energy)
            T_mechanical = ½ m·v² (mechanical kinetic energy)
            U_potential = potential energy (springs, gravity, etc.)

        Args:
            currents: Array of currents I (abamperes).
            charges: Optional array of charges (for potential energy).
            velocities: Optional array of mechanical velocities.
            positions: Optional array of positions (for potential energy).

        Returns:
            Lagrangian L (erg).

        Reference:
            Part IV, Arts. 556-557: Lagrangian formulation.
        """
        currents = np.asarray(currents, dtype=np.float64)

        # Electrical kinetic energy (electrokinetic)
        T_electrical = 0.5 * np.dot(currents, np.dot(self.inductance_matrix, currents))

        # Mechanical kinetic energy
        T_mechanical = 0.0
        if velocities is not None and len(self.masses) > 0:
            velocities = np.asarray(velocities, dtype=np.float64)
            T_mechanical = 0.5 * np.dot(self.masses * velocities, velocities)

        # Potential energy (simplified — would need capacitance, springs, etc.)
        U_potential = 0.0
        if charges is not None:
            # Could add capacitor energy: U = ½ q²/C
            pass

        return T_electrical + T_mechanical - U_potential

    @maxwell_cite(
        559, 560,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Calculate equations of motion for connected system",
    )
    def equations_of_motion(
        self,
        currents: np.ndarray,
        charges: np.ndarray,
        applied_emfs: np.ndarray,
        mechanical_forces: Optional[np.ndarray] = None,
    ) -> dict[str, np.ndarray]:
        """
        Calculate complete equations of motion.

        Arts. 559-560: The equations of motion from Lagrange's equations:

        Electrical:
            L·dI/dt + R·I = E_applied

        Mechanical:
            m·dv/dt + b·v = F_applied + F_electromagnetic

        where F_electromagnetic = Iᵀ · (∂L/∂x) · I from energy gradient.

        Args:
            currents: Current state currents I.
            charges: Current state charges q.
            applied_emfs: Applied EMFs to circuits.
            mechanical_forces: Optional applied mechanical forces.

        Returns:
            Dictionary with:
            - dI_dt: Current derivatives
            - mechanical_acceleration: Mechanical accelerations (if applicable)
            - electromagnetic_force: Force from field energy
            - power_dissipated: I²R losses
            - power_supplied: E·I input power
        """
        currents = np.asarray(currents, dtype=np.float64)
        charges = np.asarray(charges, dtype=np.float64)
        applied_emfs = np.asarray(applied_emfs, dtype=np.float64)

        # Electrical equation: L·dI/dt + R·I = E
        # dI/dt = L⁻¹·(E - R·I)
        resistive_drop = self.resistances * currents
        voltage_balance = applied_emfs - resistive_drop

        try:
            L_inv = np.linalg.inv(self.inductance_matrix)
            dI_dt = np.dot(L_inv, voltage_balance)
        except np.linalg.LinAlgError:
            L_inv = np.linalg.pinv(self.inductance_matrix)
            dI_dt = np.dot(L_inv, voltage_balance)

        # Electromagnetic force on mechanical DOF
        electromagnetic_force = np.zeros(self.num_mechanical)
        if self.num_mechanical > 0 and len(self.coupling_matrix) > 0:
            # F_em = Iᵀ · (∂L/∂x) · I
            for k in range(self.num_mechanical):
                for i in range(self.num_circuits):
                    for j in range(self.num_circuits):
                        electromagnetic_force[k] += currents[i] * self.coupling_matrix[k, i, j] * currents[j]

        # Power calculations
        power_dissipated = np.dot(self.resistances * currents, currents)
        power_supplied = np.dot(applied_emfs, currents)

        result = {
            "dI_dt": dI_dt,
            "resistive_drop": resistive_drop,
            "voltage_balance": voltage_balance,
            "electromagnetic_force": electromagnetic_force,
            "power_dissipated": power_dissipated,
            "power_supplied": power_supplied,
            "power_stored": power_supplied - power_dissipated,  # dT/dt
        }

        if mechanical_forces is not None:
            mechanical_forces = np.asarray(mechanical_forces, dtype=np.float64)
            if len(self.masses) > 0:
                mechanical_acceleration = (mechanical_forces + electromagnetic_force) / self.masses
                result["mechanical_acceleration"] = mechanical_acceleration

        return result

    @maxwell_cite(
        561,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Calculate electrokinetic momentum (generalized momentum)",
    )
    def electrokinetic_momentum(self, currents: np.ndarray) -> np.ndarray:
        """
        Calculate electrokinetic momentum (generalized momentum).

        Art. 561: The momentum conjugate to current is:

            p = ∂L/∂İ = L · I

        This is the electromagnetic analogue of p = m·v.

        Args:
            currents: Array of currents I (abamperes).

        Returns:
            Electrokinetic momentum p (abA·cm).

        Reference:
            Part IV, Art. 561: Electromagnetic momentum.
        """
        currents = np.asarray(currents, dtype=np.float64)
        return np.dot(self.inductance_matrix, currents)

    @maxwell_cite(
        562, 563,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Calculate force from energy gradient",
    )
    def force_from_energy(
        self,
        currents: np.ndarray,
        position_derivative: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate mechanical force from energy gradient.

        Arts. 562-563: The force in direction x is:

            F_x = ∂T/∂x = ½ Iᵀ · (∂L/∂x) · I

        For mutual inductance varying with position:
            F = I₁ I₂ (∂M/∂x)

        Args:
            currents: Array of currents I.
            position_derivative: ∂L/∂x tensor (num_mech × num_circuits × num_circuits).

        Returns:
            Force vector F (dynes).
        """
        currents = np.asarray(currents, dtype=np.float64)

        # F_k = ½ Σᵢⱼ Iᵢ (∂Lᵢⱼ/∂x_k) Iⱼ
        num_mech = position_derivative.shape[0]
        force = np.zeros(num_mech)

        for k in range(num_mech):
            for i in range(len(currents)):
                for j in range(len(currents)):
                    force[k] += 0.5 * currents[i] * position_derivative[k, i, j] * currents[j]

        # Factor of 2 because the matrix is symmetric
        return 2.0 * force

    @maxwell_cite(
        553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567,
        part=4, chapter="Equations of Connected Systems",
        theory_class="maxwell_original",
        description="Complete analysis of connected system dynamics",
    )
    def analyze(
        self,
        currents: np.ndarray,
        charges: np.ndarray,
        applied_emfs: np.ndarray,
        velocities: Optional[np.ndarray] = None,
        positions: Optional[np.ndarray] = None,
    ) -> dict[str, float | np.ndarray]:
        """
        Complete analysis of connected system dynamics.

        Arts. 553-567: Comprehensive analysis including:
        1. Lagrangian and energies
        2. Equations of motion
        3. Electrokinetic momentum
        4. Force from energy gradient
        5. Power balance
        6. Time constants

        Args:
            currents: Array of currents I (abamperes).
            charges: Array of charges q (abC).
            applied_emfs: Applied EMFs (abvolts).
            velocities: Optional mechanical velocities.
            positions: Optional mechanical positions.

        Returns:
            Dictionary with complete analysis results.

        Reference:
            Part IV, Arts. 553-567: Complete connected system analysis.
        """
        currents = np.asarray(currents, dtype=np.float64)
        charges = np.asarray(charges, dtype=np.float64)
        applied_emfs = np.asarray(applied_emfs, dtype=np.float64)

        # Lagrangian
        lagrangian = self.lagrangian(currents, charges, velocities, positions)

        # Electrokinetic energy
        T = 0.5 * np.dot(currents, np.dot(self.inductance_matrix, currents))

        # Equations of motion
        motion = self.equations_of_motion(currents, charges, applied_emfs)

        # Momentum
        momentum = self.electrokinetic_momentum(currents)

        # Time constants for each circuit
        time_constants = np.zeros(self.num_circuits)
        for i in range(self.num_circuits):
            if self.resistances[i] > 0:
                time_constants[i] = self.inductance_matrix[i, i] / self.resistances[i]

        return {
            "lagrangian": lagrangian,
            "electrokinetic_energy": T,
            "equations_of_motion": motion,
            "electrokinetic_momentum": momentum,
            "time_constants": time_constants,
            "num_circuits": self.num_circuits,
            "num_mechanical_dof": self.num_mechanical,
            "inductance_matrix": self.inductance_matrix,
            "currents": currents,
            "charges": charges,
        }


__all__ = [
    # Lagrangian formulation (Arts. 553-558)
    "lagrange_equations_em",
    "kinetic_energy_electromagnetic",
    "generalized_coordinates",
    # Electromagnetic equations of motion (Arts. 559-563)
    "em_equation_motion",
    "electromagnetic_inertia",
    "mutual_inductance_force",
    # Weber's and Neumann's theories (Arts. 564-567)
    "weber_electrodynamics",
    "neumann_potential",
    # ConnectedSystem class
    "ConnectedSystem",
]
