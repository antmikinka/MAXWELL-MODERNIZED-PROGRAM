"""maxwell.instruments.optimization.sensitivity — Sensitivity optimization.

Part IV, Chapter XV "Electromagnetic Instruments", Arts. 716, 718, 719
(the uniform-wire instrument of Art. 720 lives in
``maxwell.instruments.galvanometers``).

Unit convention — CGS-EMU (repo default for Part IV instruments):
currents in abamperes, resistances in abohm (dimensions of velocity,
cm/s), resistivities in abohm.cm, lengths in cm.

Article correspondence:
    716  wire dimensions for a coil whose resistance is prescribed
    718  theory of greatest sensibility: R_coil = R_external
    719  law of wire thickness across the layers of the coil
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@maxwell_cite(
    716,
    part=4,
    theory_class="standard_math",
    description="Wire dimensions giving a prescribed coil resistance from a fixed "
    "wire volume",
)
def optimize_galvanometer_wire(
    external_resistance: float,
    wire_resistivity: float,
    available_volume: float,
    coil_inner_radius: float,
    coil_outer_radius: float,
) -> dict[str, float]:
    """Optimize wire dimensions for galvanometer sensitivity (Art. 716).

    The proper thickness of the wire depends on the external resistance:
    for maximum sensibility the coil resistance must equal the external
    resistance (the Art.-718 theorem). Given a fixed wire volume V and
    resistivity rho, the length L and cross-section A = V/L of wire that
    realize R_coil = R_ext follow from R = rho.L/A = rho.L^2/V:

        L = sqrt(R_ext * V / rho),   A = V / L,   y = sqrt(A / pi).

    The returned turn count uses the mean winding radius
    (coil_inner_radius + coil_outer_radius)/2.

    Identities (verified by tests): rho*L/A == R_ext exactly and
    L*A == V exactly.

    Args:
        external_resistance: External circuit resistance (abohm).
        wire_resistivity: Resistivity of wire material (abohm.cm).
        available_volume: Total volume of wire available (cm^3).
        coil_inner_radius: Inner radius of winding space (cm).
        coil_outer_radius: Outer radius of winding space (cm).

    Returns:
        Optimized wire_radius, wire_length, wire_area, n_turns and
        coil_resistance.

    Raises:
        ValueError: for non-positive inputs.
    """
    if min(external_resistance, wire_resistivity, available_volume,
           coil_inner_radius, coil_outer_radius) <= 0.0:
        raise ValueError("all inputs must be positive")

    optimal_length = np.sqrt(
        external_resistance * available_volume / wire_resistivity
    )
    wire_area = available_volume / optimal_length
    wire_radius = np.sqrt(wire_area / PI)

    mean_radius = (coil_inner_radius + coil_outer_radius) / 2.0
    n_turns = int(optimal_length / (2.0 * PI * mean_radius))

    return {
        "wire_radius": wire_radius,
        "wire_area": wire_area,
        "wire_length": optimal_length,
        "n_turns": n_turns,
        "coil_resistance": wire_resistivity * optimal_length / wire_area,
    }


def sensitivity_figure_of_merit(
    coil_resistance: float, external_resistance: float
) -> float:
    """Sensibility figure of merit g(R) = sqrt(R)/(R + R_ext) (Art. 718).

    With a fixed wire volume V the winding can be drawn out: using wire
    length L gives G ∝ n ∝ L and R_coil = rho.L^2/V, hence G ∝
    sqrt(R_coil). The deflection per unit EMF is proportional to

        g(R_coil) = G / (R_coil + R_ext) ∝ sqrt(R_coil) / (R_coil + R_ext),

    whose derivative vanishes exactly at R_coil = R_ext (the theorem of
    greatest sensibility). The common geometric factor cancels in g.

    Args:
        coil_resistance: Coil resistance (abohm), must be positive.
        external_resistance: External circuit resistance (abohm).

    Returns:
        Dimensionless merit value (proportional to deflection per unit
        EMF at fixed wire volume and coil form).
    """
    return np.sqrt(coil_resistance) / (coil_resistance + external_resistance)


@maxwell_cite(
    718,
    part=4,
    theory_class="standard_math",
    description="Theory of greatest sensibility: optimum re-winding at fixed wire "
    "volume, R_coil = R_ext",
)
def optimize_galvanometer_sensitivity(
    wire_length: float,
    wire_radius: float,
    wire_resistivity: float,
    external_resistance: float,
    coil_radius: float,
) -> dict[str, float]:
    """Theory of greatest sensibility (Art. 718).

    A winding of fixed wire volume V = pi.y^2.L0 may be drawn to a new
    length L (cross-section V/L): the coil constant scales as
    G = L/R_c^2-groove-form (fixed coil radius) and the resistance as
    R_coil = rho.L^2/V. The deflection per unit EMF,

        merit(L) ∝ L / (R_ext + rho.L^2 / V),

    is stationary where d/dL [L/(R_ext + rho.L^2/V)] = 0, i.e. where

        R_coil(L*) = rho.L*^2/V = R_ext,   L* = sqrt(R_ext.V/rho):

    the coil resistance must equal the external resistance. This function
    returns the optimum together with the sensibility gain over the
    winding as given.

    Args:
        wire_length: Length of wire as currently wound (cm).
        wire_radius: Wire radius as currently wound (cm).
        wire_resistivity: Wire material resistivity (abohm.cm).
        external_resistance: External circuit resistance (abohm).
        coil_radius: Mean coil radius, unchanged by re-winding (cm).

    Returns:
        Dictionary with the as-wound resistance, the optimal wire length,
        optimal resistance (== external_resistance), optimal turns and
        coil constant at the optimum, and the sensitivity_gain
        merit(L*)/merit(L0).

    Raises:
        ValueError: for non-positive inputs.
    """
    if min(wire_length, wire_radius, wire_resistivity, external_resistance,
           coil_radius) <= 0.0:
        raise ValueError("all inputs must be positive")

    volume = PI * wire_radius**2 * wire_length
    current_resistance = wire_resistivity * wire_length / (PI * wire_radius**2)

    optimal_length = np.sqrt(external_resistance * volume / wire_resistivity)
    optimal_resistance = wire_resistivity * optimal_length**2 / volume
    optimal_turns = int(optimal_length / (2.0 * PI * coil_radius))
    optimal_g = 2.0 * PI * optimal_turns / coil_radius

    def merit(length: float) -> float:
        return length / (external_resistance + wire_resistivity * length**2 / volume)

    gain = merit(optimal_length) / merit(wire_length)

    return {
        "current_resistance": current_resistance,
        "optimal_wire_length": optimal_length,
        "optimal_resistance": optimal_resistance,
        "optimal_turns": optimal_turns,
        "optimal_G": optimal_g,
        "sensitivity_gain": gain,
    }


@maxwell_cite(
    719,
    part=4,
    theory_class="standard_math",
    description="Law of wire thickness across the coil layers: section proportional "
    "to the square of the distance from the axis",
)
def apply_sensitivity_wire_law(
    position_in_coil: float,
    external_resistance: float,
    wire_resistivity: float,
    coil_dimensions: dict[str, float],
) -> float:
    """Apply the law of wire thickness for sensibility (Art. 719).

    When the coil space (inner radius r1, outer radius r2, axial depth d)
    is to be filled with wire for maximum sensibility under the
    Art.-718 resistance constraint, the optimal wire cross-section varies
    with the radius of the layer. Variation of
    G = ∫ (2.pi/r) dn subject to R = ∫ rho.(2.pi.r/A) dn = R_ext and the
    winding-space filling dn = d.dr/A(r) gives, by the Euler equation of
    the resulting Lagrange problem,

        A(r) = kappa.r^2,   i.e. wire radius y(r) = r.sqrt(kappa/pi),

    with kappa fixed by the resistance constraint:

        kappa = sqrt( pi.rho.d.(r1^-2 - r2^-2) / R_ext ).

    The wire is therefore proportionally thicker in the outer layers,
    where each turn contributes less to the field at the centre.

    Args:
        position_in_coil: Radial position of the layer, r1 <= r <= r2 (cm).
        external_resistance: External circuit resistance (abohm).
        wire_resistivity: Wire material resistivity (abohm.cm).
        coil_dimensions: Dict with inner_radius, outer_radius, depth (cm).

    Returns:
        Optimal wire radius at the given position (cm).

    Raises:
        ValueError: for non-positive inputs or a position outside the
            winding space.
    """
    inner_r = coil_dimensions["inner_radius"]
    outer_r = coil_dimensions["outer_radius"]
    depth = coil_dimensions["depth"]
    if min(inner_r, outer_r, depth, external_resistance, wire_resistivity) <= 0.0:
        raise ValueError("all inputs must be positive")
    if not (inner_r <= position_in_coil <= outer_r):
        raise ValueError("position_in_coil must lie within the winding space")

    kappa = np.sqrt(
        PI * wire_resistivity * depth
        * (inner_r**-2 - outer_r**-2) / external_resistance
    )
    return position_in_coil * np.sqrt(kappa / PI)
