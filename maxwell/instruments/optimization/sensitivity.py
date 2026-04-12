"""maxwell.instruments.optimization.sensitivity — Sensitivity optimization (Arts. 716-720).

Optimization of galvanometer wire thickness, sensitivity,
and the law of thickness for maximum sensitivity.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@maxwell_cite(716, part=4, theory_class="standard_math")
def optimize_galvanometer_wire(
    external_resistance: float,
    wire_resistivity: float,
    available_volume: float,
    coil_inner_radius: float,
    coil_outer_radius: float,
) -> dict[str, float]:
    """Optimize wire dimensions for galvanometer sensitivity.

    Art. 716: The proper thickness of the wire depends on the
    external resistance. For maximum sensitivity, the coil
    resistance should equal the external resistance.

    Args:
        external_resistance: External circuit resistance (cm/s in CGS).
        wire_resistivity: Resistivity of wire material.
        available_volume: Total volume of wire available.
        coil_inner_radius: Inner radius of winding space.
        coil_outer_radius: Outer radius of winding space.

    Returns:
        Optimized wire radius, length, and number of turns.
    """
    # For max sensitivity: R_coil = R_external
    # R = rho * L / (pi * r_wire^2)
    # Volume = L * pi * r_wire^2
    # So R = rho * L^2 / Volume => L = sqrt(R * Volume / rho)

    optimal_length = np.sqrt(external_resistance * available_volume / wire_resistivity)
    wire_area = available_volume / optimal_length
    wire_radius = np.sqrt(wire_area / PI)

    # Estimate turns from mean circumference
    mean_radius = (coil_inner_radius + coil_outer_radius) / 2.0
    mean_circumference = 2.0 * PI * mean_radius
    n_turns = int(optimal_length / mean_circumference)

    return {
        "wire_radius": wire_radius,
        "wire_length": optimal_length,
        "n_turns": n_turns,
        "coil_resistance": external_resistance,
    }


@maxwell_cite(718, part=4, theory_class="standard_math")
def optimize_galvanometer_sensitivity(
    n_turns: int,
    radius: float,
    wire_radius: float,
    wire_resistivity: float,
    external_resistance: float,
) -> dict[str, float]:
    """Theory of greatest sensibility (Art. 718).

    Maximum sensitivity is achieved when:
    1. The coil resistance equals the external resistance
    2. The wire is as thick as possible (maximizing n for given R)
    3. The coil radius is as small as practical

    Args:
        n_turns: Current number of turns.
        radius: Mean coil radius.
        wire_radius: Wire radius.
        wire_resistivity: Wire material resistivity.
        external_resistance: External circuit resistance.

    Returns:
        Sensitivity metrics and optimal parameters.
    """
    # Current coil resistance
    wire_length = 2.0 * PI * radius * n_turns
    wire_area = PI * wire_radius**2
    coil_resistance = wire_resistivity * wire_length / wire_area

    # Sensitivity = G / H = 2*pi*n / (R_coil * H)
    # For optimal: R_coil = R_external
    optimal_n = int(n_turns * np.sqrt(external_resistance / coil_resistance))
    optimal_G = 2.0 * PI * optimal_n / radius

    return {
        "current_resistance": coil_resistance,
        "optimal_resistance": external_resistance,
        "optimal_turns": optimal_n,
        "optimal_G": optimal_G,
        "sensitivity_ratio": optimal_G / coil_resistance if coil_resistance > 0 else 0,
    }


@maxwell_cite(719, part=4, theory_class="standard_math")
def apply_sensitivity_wire_law(
    position_in_coil: float,
    external_resistance: float,
    wire_resistivity: float,
    coil_dimensions: dict[str, float],
) -> float:
    """Apply the law of wire thickness for sensitivity (Art. 719).

    When the coil has multiple layers, the optimal wire thickness
    varies with position: outer layers should use thicker wire
    because each turn contributes less to the field at the center.

    Args:
        position_in_coil: Radial position within coil winding (cm from center).
        external_resistance: External circuit resistance.
        wire_resistivity: Wire material resistivity.
        coil_dimensions: Dict with inner_radius, outer_radius, depth.

    Returns:
        Optimal wire radius at the given position.
    """
    inner_r = coil_dimensions["inner_radius"]
    outer_r = coil_dimensions["outer_radius"]

    # The field contribution per turn decreases with radius
    # so optimal wire thickness should increase
    # Maxwell's law: wire cross-section proportional to r
    fractional_position = (position_in_coil - inner_r) / (outer_r - inner_r)
    base_radius = np.sqrt(external_resistance * (inner_r) / (wire_resistivity * 2.0 * PI))

    # Scale wire radius with position
    return base_radius * (1.0 + fractional_position)
