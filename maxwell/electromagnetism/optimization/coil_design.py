"""maxwell.electromagnetism.optimization.coil_design — Coil optimization (Art. 706).

Implements Maxwell's analysis of optimal coil design for maximum
field uniformity and strength.

Maxwell's CGS formulation (Art. 706):
    For a coil of given wire length and radius, the design parameters are:
    - Coil radius a
    - Number of turns n
    - Coil length L (for solenoids)

    Optimal designs maximize:
    - Field at center: B = 2*pi*n*I/(c*a)
    - Field uniformity: minimize dB/dz
    - Efficiency: B per unit power

    Maxwell showed that the Helmholtz configuration (separation = radius)
    gives the most uniform field for two identical coils.

where:
    a = coil radius (cm)
    n = number of turns
    I = current (abamperes)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's coil optimization theory.

References:
    Part IV, Art. 706: Coil design optimization.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import (
    calc_coil_on_axis,
    calc_double_coil_field,
)
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Calculate coil field efficiency",
)
def calc_coil_efficiency(
    current: float,
    coil_radius: float,
    wire_length: float,
    wire_radius: float,
) -> dict[str, float]:
    """
    Calculate coil field efficiency.

    Art. 706: For a given wire length and gauge, the efficiency is:

        eta = B_center / (I * sqrt(R))

    where R is the resistance proportional to wire_length / wire_area.

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        wire_length: Total wire length (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with efficiency parameters.
    """
    # Number of turns
    n = int(wire_length / (2 * np.pi * coil_radius))
    n = max(n, 1)

    # Center field
    B = calc_coil_on_axis(current, coil_radius, 0, n)

    # Wire cross-section area
    A_wire = np.pi * wire_radius**2

    # Resistance proportional (in arbitrary units)
    R_proportional = wire_length / A_wire

    # Efficiency
    efficiency = B / (current * np.sqrt(max(R_proportional, 1e-15)))

    return {
        "n_turns": n,
        "center_field": B,
        "wire_length": wire_length,
        "wire_cross_section": A_wire,
        "resistance_proportional": R_proportional,
        "efficiency": efficiency,
    }


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Calculate optimal coil radius for given wire",
)
def calc_optimal_coil_radius(
    wire_length: float,
    wire_radius: float,
    target_position: float = 0.0,
) -> float:
    """
    Calculate optimal coil radius for maximum field at target position.

    Art. 706: For a given wire length, the optimal radius balances
    the number of turns (favors small radius) against field strength
    per turn (favors large radius).

    Args:
        wire_length: Total wire length (cm).
        wire_radius: Wire radius (cm).
        target_position: Axial position for max field (cm).

    Returns:
        Optimal coil radius (cm).
    """

    def negative_field(a):
        if a < wire_radius * 2:
            return 1e30
        n = max(int(wire_length / (2 * np.pi * a)), 1)
        B = calc_coil_on_axis(1.0, a, target_position, n)
        return -B

    result = minimize_scalar(
        negative_field,
        bounds=(wire_radius * 2, wire_length / (2 * np.pi)),
        method="bounded",
    )
    return result.x


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Calculate optimal Helmholtz configuration",
)
def calc_optimal_helmholtz(
    wire_length: float,
    wire_radius: float,
) -> dict[str, float]:
    """
    Calculate optimal Helmholtz coil configuration.

    Art. 706: For a given wire length split equally between two coils,
    find the radius that maximizes uniform field at center.

    Args:
        wire_length: Total wire length for both coils (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with optimal configuration parameters.
    """
    wire_per_coil = wire_length / 2

    def negative_helmholtz_field(a):
        if a < wire_radius * 2:
            return 1e30
        n = max(int(wire_per_coil / (2 * np.pi * a)), 1)
        B = calc_double_coil_field(
            1.0, a, np.array([0, 0, 0]), coil_separation=a, n_turns=n
        )
        return -np.linalg.norm(B)

    result = minimize_scalar(
        negative_helmholtz_field,
        bounds=(wire_radius * 2, wire_per_coil / (2 * np.pi)),
        method="bounded",
    )

    optimal_radius = result.x
    n = max(int(wire_per_coil / (2 * np.pi * optimal_radius)), 1)
    B = calc_double_coil_field(
        1.0,
        optimal_radius,
        np.array([0, 0, 0]),
        coil_separation=optimal_radius,
        n_turns=n,
    )

    return {
        "optimal_radius": optimal_radius,
        "n_turns_per_coil": n,
        "separation": optimal_radius,
        "center_field_per_ampere": np.linalg.norm(B),
        "wire_per_coil": wire_per_coil,
    }


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Calculate coil uniformity figure of merit",
)
def calc_uniformity_fom(
    coil_radius: float,
    n_turns: int = 1,
    coil_separation: float = None,
    evaluation_radius: float = None,
) -> dict[str, float]:
    """
    Calculate coil configuration uniformity figure of merit.

    Art. 706: The uniformity is measured by the field variation
    over a spherical region of interest.

    Args:
        coil_radius: Coil radius (cm).
        n_turns: Turns per coil.
        coil_separation: Separation (cm, default = radius for Helmholtz).
        evaluation_radius: Radius of evaluation sphere (cm, default 0.1*coil_radius).

    Returns:
        Dictionary with uniformity figure of merit.
    """
    if coil_separation is None:
        coil_separation = coil_radius
    if evaluation_radius is None:
        evaluation_radius = 0.1 * coil_radius

    # Field at center
    B_center = calc_double_coil_field(
        1.0,
        coil_radius,
        np.array([0, 0, 0]),
        coil_separation=coil_separation,
        n_turns=n_turns,
    )
    B_center_mag = np.linalg.norm(B_center)

    # Field at various points within evaluation sphere
    n_points = 20
    max_variation = 0.0

    np.random.seed(42)
    for _ in range(n_points):
        # Random point within sphere
        r = evaluation_radius * np.random.uniform(0, 1)
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)

        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        B = calc_double_coil_field(
            1.0,
            coil_radius,
            np.array([x, y, z]),
            coil_separation=coil_separation,
            n_turns=n_turns,
        )
        B_mag = np.linalg.norm(B)
        variation = (
            abs(B_mag - B_center_mag) / B_center_mag if B_center_mag > 1e-15 else 0
        )
        max_variation = max(max_variation, variation)

    return {
        "coil_radius": coil_radius,
        "coil_separation": coil_separation,
        "evaluation_radius": evaluation_radius,
        "center_field_per_ampere": B_center_mag,
        "max_variation": max_variation,
        "uniformity_score": 1.0 - max_variation,
    }


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Verify optimal coil design",
)
def verify_coil_design(
    wire_length: float = 100.0,
    wire_radius: float = 0.05,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify coil design optimization.

    Art. 706: This function verifies:
    1. Optimal radius produces higher field than arbitrary choices
    2. Helmholtz configuration has better uniformity than other separations

    Args:
        wire_length: Test wire length (cm).
        wire_radius: Test wire radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Optimal radius
    a_opt = calc_optimal_coil_radius(wire_length, wire_radius)
    n_opt = max(int(wire_length / (2 * np.pi * a_opt)), 1)
    B_opt = calc_coil_on_axis(1.0, a_opt, 0, n_opt)

    # Compare with arbitrary radii
    a_small = wire_radius * 10
    n_small = max(int(wire_length / (2 * np.pi * a_small)), 1)
    B_small = calc_coil_on_axis(1.0, a_small, 0, n_small)

    a_large = wire_length / (4 * np.pi)
    n_large = max(int(wire_length / (2 * np.pi * a_large)), 1)
    B_large = calc_coil_on_axis(1.0, a_large, 0, n_large)

    optimal_wins = B_opt >= B_small and B_opt >= B_large

    # Helmholtz uniformity vs other separations
    helmholtz_fom = calc_uniformity_fom(
        a_opt, n_opt, coil_separation=a_opt, evaluation_radius=0.1 * a_opt
    )
    tight_fom = calc_uniformity_fom(
        a_opt, n_opt, coil_separation=0.5 * a_opt, evaluation_radius=0.1 * a_opt
    )

    helmholtz_more_uniform = (
        helmholtz_fom["uniformity_score"] >= tight_fom["uniformity_score"]
    )

    return {
        "optimal_radius": a_opt,
        "B_optimal": B_opt,
        "B_small_radius": B_small,
        "B_large_radius": B_large,
        "optimal_wins": bool(optimal_wins),
        "helmholtz_uniformity": helmholtz_fom["uniformity_score"],
        "tight_uniformity": tight_fom["uniformity_score"],
        "helmholtz_more_uniform": bool(helmholtz_more_uniform),
        "verified": bool(optimal_wins and helmholtz_more_uniform),
    }


@maxwell_cite(
    706,
    part=4,
    chapter="Coil Design",
    theory_class="maxwell_original",
    description="Complete coil design analysis",
)
def analyze_coil_design(
    wire_length: float,
    wire_radius: float,
) -> dict[str, float | dict]:
    """
    Complete coil design optimization analysis.

    Art. 706: Comprehensive analysis including:
    1. Optimal single coil
    2. Optimal Helmholtz pair
    3. Uniformity comparison
    4. Efficiency analysis

    Args:
        wire_length: Available wire length (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    # Single coil optimization
    a_single = calc_optimal_coil_radius(wire_length, wire_radius)
    n_single = max(int(wire_length / (2 * np.pi * a_single)), 1)
    B_single = calc_coil_on_axis(1.0, a_single, 0, n_single)

    # Helmholtz optimization
    helmholtz = calc_optimal_helmholtz(wire_length, wire_radius)

    # Efficiency
    efficiency = calc_coil_efficiency(1.0, a_single, wire_length, wire_radius)

    return {
        "wire_length": wire_length,
        "wire_radius": wire_radius,
        "single_coil": {
            "radius": a_single,
            "n_turns": n_single,
            "center_field_per_ampere": B_single,
        },
        "helmholtz": helmholtz,
        "efficiency": efficiency,
    }
