"""
Ohm's Law — the fundamental relation between current, EMF, and resistance.

Art. 241: The current is equal to the electromotive force divided by the resistance.

Maxwell's notation: C = E / R  (current = EMF / resistance)
Modern notation:     I = V / R

Category: C (standard_math) — Ohm's law is well-established physics.

References:
    Part II, Art. 241: Ohm's Law.
    Part II, Art. 274: Ohm's Law (mathematical theory).
"""

from __future__ import annotations

from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    241,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="standard_math",
    description="Ohm's Law: current = EMF / resistance",
)
def solve_ohm_law(emf: float, resistance: float) -> float:
    """Solve Ohm's Law for current.

    Args:
        emf: Electromotive force (statvolt in CGS-ESU).
        resistance: Resistance (statohm in CGS-ESU).

    Returns:
        Current (statampere in CGS-ESU).

    Reference:
        Part II, Art. 241.
    """
    if resistance <= 0:
        raise ValueError(f"Resistance must be positive, got {resistance}")
    return emf / resistance


@maxwell_cite(
    241,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="standard_math",
    description="Ohm's Law: EMF = current * resistance",
)
def calc_emf(current: float, resistance: float) -> float:
    """Calculate EMF from current and resistance.

    E = C * R  (Maxwell's notation)

    Args:
        current: Current (statampere).
        resistance: Resistance (statohm).

    Returns:
        Electromotive force (statvolt).
    """
    if resistance < 0:
        raise ValueError(f"Resistance must be non-negative, got {resistance}")
    return current * resistance


@maxwell_cite(
    241,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="standard_math",
    description="Ohm's Law: resistance = EMF / current",
)
def calc_resistance(emf: float, current: float) -> float:
    """Calculate resistance from EMF and current.

    R = E / C

    Args:
        emf: Electromotive force (statvolt).
        current: Current (statampere).

    Returns:
        Resistance (statohm).
    """
    if current == 0:
        raise ValueError("Current cannot be zero")
    return emf / current


@maxwell_cite(
    277,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="standard_math",
    description="Resistance of uniform wire: R = rho * L / A",
)
def uniform_wire_resistance(
    specific_resistance: float, length: float, cross_section: float
) -> float:
    """Calculate resistance of a wire of uniform cross-section.

    R = rho * L / A

    Args:
        specific_resistance: Specific resistance rho (statohm·cm).
        length: Wire length (cm).
        cross_section: Cross-sectional area (cm^2).

    Returns:
        Total resistance (statohm).

    Reference:
        Part II, Art. 277.
    """
    if cross_section <= 0:
        raise ValueError(f"Cross-section must be positive, got {cross_section}")
    if length < 0:
        raise ValueError(f"Length must be non-negative, got {length}")
    return specific_resistance * length / cross_section


@maxwell_cite(
    279,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="standard_math",
    description="Specific resistance in electromagnetic measure",
)
def specific_resistance_emu(
    resistance_emu: float, length: float, cross_section: float
) -> float:
    """Calculate specific resistance in electromagnetic measure.

    rho = R * A / L

    Args:
        resistance_emu: Resistance in EMU (abohm).
        length: Length (cm).
        cross_section: Cross-section (cm^2).

    Returns:
        Specific resistance rho (abohm·cm).

    Reference:
        Part II, Art. 279.
    """
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    return resistance_emu * cross_section / length
