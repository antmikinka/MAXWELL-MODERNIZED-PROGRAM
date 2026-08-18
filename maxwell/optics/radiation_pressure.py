"""maxwell.optics.radiation_pressure — Radiation pressure (Arts. 791-794).

Implements Maxwell's theory of radiation pressure — the mechanical force
exerted by electromagnetic waves on surfaces.

Maxwell's CGS formulation (Arts. 791-794):
    Radiation pressure on absorbing surface:
        P = I / c = u  (erg/cm³ = dyne/cm²)

    Radiation pressure on reflecting surface:
        P = 2I / c = 2u  (for normal incidence)

    Energy density relation:
        u = (1/8π)(E² + B²) = I / c

    where:
        P = radiation pressure (dyne/cm²)
        I = intensity (erg/cm²/s)
        c = speed of light (cm/s)
        u = energy density (erg/cm³)

    Maxwell showed that light exerts a mechanical force, predicting
    phenomena later confirmed by Lebedev (1900) and Nichols-Hull (1901).

where:
    P = radiation pressure (dyne/cm²)
    I = wave intensity (erg/cm²/s)
    c = speed of light in vacuum (cm/s)
    u = electromagnetic energy density (erg/cm³)

Category: A (maxwell_original) — Maxwell's radiation pressure theory.

References:
    Part IV, Arts. 791-794: Radiation pressure and mechanical action of light.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    792,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate radiation pressure: P = u",
)
def calc_radiation_pressure(u: float) -> float:
    """
    Calculate radiation pressure from energy density.

    Art. 791-792: Maxwell's radiation pressure formula for absorption:

        P = u

    where u is the energy density (erg/cm³).

    For CGS units: 1 erg/cm³ = 1 dyne/cm²

    Args:
        u: Energy density (erg/cm³).

    Returns:
        Radiation pressure P (dyne/cm²).

    Raises:
        ValueError: If energy density is negative.

    Reference:
        Part IV, Arts. 791-792: Radiation pressure formula.

    Example:
        >>> P = calc_radiation_pressure(1.0)
        >>> print(f"P = {P} dyne/cm²")  # P = 1 dyne/cm²
    """
    if u < 0:
        raise ValueError(f"Energy density must be non-negative, got {u}")

    return u


@maxwell_cite(
    792,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate radiation pressure for reflection: P = 2u",
)
def calc_radiation_pressure_reflection(u: float) -> float:
    """
    Calculate radiation pressure for perfect reflection.

    Art. 792: For perfect reflection, pressure is doubled:

        P = 2u

    Args:
        u: Energy density (erg/cm³).

    Returns:
        Radiation pressure P (dyne/cm²).

    Reference:
        Part IV, Art. 792: Radiation pressure for reflection.

    Example:
        >>> P = calc_radiation_pressure_reflection(1.0)
        >>> print(f"P = {P} dyne/cm²")  # P = 2 dyne/cm²
    """
    if u < 0:
        raise ValueError(f"Energy density must be non-negative, got {u}")

    return 2.0 * u


@maxwell_cite(
    791,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate radiation pressure from intensity: P = I/c",
)
def calc_pressure_from_intensity(I: float) -> float:
    """
    Calculate radiation pressure from intensity.

    Art. 791: For absorbing surface:

        P = I / c

    Args:
        I: Intensity (erg/cm²/s).

    Returns:
        Radiation pressure P (dyne/cm²).

    Reference:
        Part IV, Art. 791: Pressure from intensity.

    Example:
        >>> P = calc_pressure_from_intensity(CONST.C)
        >>> print(f"P = {P} dyne/cm²")  # P = 1 dyne/cm²
    """
    if I < 0:
        raise ValueError(f"Intensity must be non-negative, got {I}")

    return I / CONST.C


@dataclass
class RadiationPressure:
    """
    Radiation pressure calculator.

    Art. 791-794: Maxwell predicted that electromagnetic waves exert
    mechanical pressure on surfaces they strike. This pressure arises
    from the momentum carried by the electromagnetic field.
    """

    @maxwell_cite(
        791,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate radiation pressure on absorbing surface",
    )
    def pressure_absorption(self, u: float) -> float:
        """
        Calculate radiation pressure on a perfectly absorbing surface.

        Art. 791: For absorbing surface:

            P = u

        Args:
            u: Energy density (erg/cm³).

        Returns:
            Radiation pressure (dyne/cm²).

        Reference:
            Part IV, Art. 791: Radiation pressure on absorber.
        """
        return calc_radiation_pressure(u)

    @maxwell_cite(
        792,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate radiation pressure on reflecting surface",
    )
    def pressure_reflection(self, u: float) -> float:
        """
        Calculate radiation pressure on a perfectly reflecting surface.

        Art. 792: For perfect reflection:

            P = 2u

        Args:
            u: Energy density (erg/cm³).

        Returns:
            Radiation pressure (dyne/cm²).

        Reference:
            Part IV, Art. 792: Radiation pressure on reflector.
        """
        return calc_radiation_pressure_reflection(u)

    @maxwell_cite(
        794,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate force on area from radiation pressure",
    )
    def force_on_area(self, pressure: float, area: float) -> float:
        """
        Calculate total force on area from radiation pressure.

        Art. 794: The force is:

            F = P * A

        Args:
            pressure: Radiation pressure P (dyne/cm²).
            area: Surface area A (cm²).

        Returns:
            Force (dynes).

        Reference:
            Part IV, Art. 794: Radiation force.
        """
        if area <= 0:
            raise ValueError(f"Area must be positive, got {area}")
        return pressure * area


@maxwell_cite(
    793,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate radiation pressure at oblique incidence",
)
def calc_radiation_pressure_oblique(
    intensity: float,
    angle: float,
    reflecting: bool = False,
) -> float:
    """
    Calculate radiation pressure at oblique incidence.

    Art. 793: For light incident at angle θ from normal:

        P = (I / c) * cos²(θ)  (absorbing)
        P = (2I / c) * cos²(θ)  (reflecting)

    The cos² factor accounts for:
    - Reduced projected area (cos θ)
    - Reduced momentum transfer per photon (cos θ)

    Args:
        intensity: Wave intensity (erg/cm²/s).
        angle: Angle of incidence θ (radians).
        reflecting: True for reflecting surface.

    Returns:
        Radiation pressure (dyne/cm²).

    Reference:
        Part IV, Art. 793: Oblique incidence pressure.

    Example:
        >>> # Pressure at 45° incidence
        >>> P = calc_radiation_pressure_oblique(1e6, np.pi/4)
        >>> print(f"P = {P:.2e} dyne/cm²")
    """
    if intensity < 0:
        raise ValueError(f"Intensity must be non-negative")

    cos_sq = np.cos(angle) ** 2

    base_pressure = intensity / CONST.C
    if reflecting:
        return 2.0 * base_pressure * cos_sq
    else:
        return base_pressure * cos_sq


@maxwell_cite(
    791,
    794,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate force from radiation on surface",
)
def calc_radiation_force(
    intensity: float,
    area: float,
    reflecting: bool = False,
    angle: float = 0.0,
) -> float:
    """
    Calculate total force from radiation pressure on a surface.

    Art. 791-794: The force is:

        F = P * A = (I / c) * A * cos²(θ)  (absorbing)
        F = (2I / c) * A * cos²(θ)  (reflecting)

    Args:
        intensity: Wave intensity (erg/cm²/s).
        area: Surface area (cm²).
        reflecting: True for reflecting surface.
        angle: Angle of incidence θ (radians, default: 0 for normal).

    Returns:
        Force (dynes).

    Reference:
        Part IV, Arts. 791-794: Radiation force.

    Example:
        >>> # Force on 1 m² solar sail at Earth
        >>> F = calc_radiation_force(1.4e6, 1e4, reflecting=True)
        >>> print(f"F = {F:.2e} dynes = {F/1e5:.2e} N")
    """
    if intensity < 0:
        raise ValueError(f"Intensity must be non-negative")
    if area <= 0:
        raise ValueError(f"Area must be positive, got {area}")

    cos_sq = np.cos(angle) ** 2

    if reflecting:
        return 2.0 * intensity * area * cos_sq / CONST.C
    else:
        return intensity * area * cos_sq / CONST.C


@maxwell_cite(
    791,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate energy density from intensity",
)
def calc_energy_density_from_intensity(intensity: float) -> float:
    """
    Calculate electromagnetic energy density from intensity.

    Art. 791: The energy density in a plane wave is:

        u = I / c

    This follows from the fact that energy flows at speed c.

    Args:
        intensity: Wave intensity I (erg/cm²/s).

    Returns:
        Energy density u (erg/cm³).

    Reference:
        Part IV, Art. 791: Energy density from intensity.

    Example:
        >>> # Solar radiation energy density
        >>> u = calc_energy_density_from_intensity(1.4e6)
        >>> print(f"u = {u:.2e} erg/cm³")
    """
    if intensity < 0:
        raise ValueError(f"Intensity must be non-negative")

    return intensity / CONST.C


@maxwell_cite(
    791,
    794,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate momentum carried by radiation",
)
def calc_radiation_momentum(energy: float) -> float:
    """
    Calculate momentum carried by electromagnetic radiation.

    Art. 791-794: The momentum-energy relation for radiation is:

        p = E / c

    This is a fundamental result of Maxwell's theory, later
    confirmed by special relativity.

    Args:
        energy: Electromagnetic energy (ergs).

    Returns:
        Momentum p (g·cm/s).

    Reference:
        Part IV, Arts. 791-794: Radiation momentum.

    Example:
        >>> # Momentum in 1 J of light
        >>> p = calc_radiation_momentum(1e7)  # 1 J = 1e7 erg
        >>> print(f"p = {p:.2e} g·cm/s")
    """
    if energy < 0:
        raise ValueError(f"Energy must be non-negative")

    return energy / CONST.C


@maxwell_cite(
    791,
    794,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate radiation pressure from E field amplitude",
)
def calc_radiation_pressure_from_E(
    E_amplitude: float, reflecting: bool = False
) -> float:
    """
    Calculate radiation pressure from electric field amplitude.

    Art. 791-794: Using I = (c/8π) E₀²:

        P = E₀² / (8π)  (absorbing)
        P = E₀² / (4π)  (reflecting)

    Args:
        E_amplitude: Electric field amplitude E₀ (statvolts/cm).
        reflecting: True for reflecting surface.

    Returns:
        Radiation pressure (dyne/cm²).

    Reference:
        Part IV, Arts. 791-794: Pressure from E field.

    Example:
        >>> # Pressure from E₀ = 1000 statV/cm
        >>> P = calc_radiation_pressure_from_E(1000)
        >>> print(f"P = {P:.2e} dyne/cm²")
    """
    if E_amplitude < 0:
        raise ValueError(f"Field amplitude must be non-negative")

    E_sq = E_amplitude**2
    base_pressure = E_sq / (8.0 * np.pi)

    if reflecting:
        return 2.0 * base_pressure
    else:
        return base_pressure


@maxwell_cite(
    791,
    792,
    793,
    794,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify radiation pressure relations",
)
def verify_radiation_pressure(
    intensity: float = 1.0e6,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify radiation pressure relationships.

    Art. 791-794: This function verifies:
    1. P = I / c for absorbing surface
    2. P = 2I / c for reflecting surface
    3. u = I / c (energy density)
    4. p = E / c (momentum)

    Args:
        intensity: Test intensity (erg/cm²/s).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 791-794: Radiation pressure verification.
    """
    # Calculate quantities
    P_absorb = calc_radiation_pressure(intensity, reflecting=False)
    P_reflect = calc_radiation_pressure(intensity, reflecting=True)
    u = calc_energy_density_from_intensity(intensity)

    # Verify P_absorb = I/c
    P_absorb_expected = intensity / CONST.C
    absorb_error = (
        abs(P_absorb - P_absorb_expected) / P_absorb_expected
        if P_absorb_expected > 0
        else 0
    )

    # Verify P_reflect = 2I/c
    P_reflect_expected = 2.0 * intensity / CONST.C
    reflect_error = (
        abs(P_reflect - P_reflect_expected) / P_reflect_expected
        if P_reflect_expected > 0
        else 0
    )

    # Verify u = I/c
    u_expected = intensity / CONST.C
    energy_density_error = abs(u - u_expected) / u_expected if u_expected > 0 else 0

    # Verify reflecting = 2 * absorbing
    ratio = P_reflect / P_absorb if P_absorb > 0 else 0
    ratio_error = abs(ratio - 2.0)

    return {
        "intensity": intensity,
        "P_absorbing": P_absorb,
        "P_reflecting": P_reflect,
        "energy_density": u,
        "P_absorb_expected": P_absorb_expected,
        "P_reflect_expected": P_reflect_expected,
        "absorb_error": absorb_error,
        "reflect_error": reflect_error,
        "energy_density_error": energy_density_error,
        "reflect_absorb_ratio": ratio,
        "ratio_error": ratio_error,
        "verified": all(
            [
                absorb_error < tolerance,
                reflect_error < tolerance,
                energy_density_error < tolerance,
                ratio_error < tolerance,
            ]
        ),
    }


@maxwell_cite(
    791,
    792,
    793,
    794,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete radiation pressure analysis",
)
def analyze_radiation_pressure(
    intensity: float,
    area: float = 1.0,
    angle: float = 0.0,
) -> dict[str, float]:
    """
    Complete analysis of radiation pressure effects.

    Art. 791-794: Comprehensive analysis including:
    1. Pressure on absorbing and reflecting surfaces
    2. Force on specified area
    3. Energy density
    4. Momentum flux
    5. Oblique incidence effects

    Args:
        intensity: Wave intensity (erg/cm²/s).
        area: Surface area for force calculation (cm²).
        angle: Angle of incidence (radians).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 791-794: Complete radiation pressure analysis.

    Example:
        >>> # Analyze solar radiation pressure
        >>> result = analyze_radiation_pressure(1.4e6, 1e4)
        >>> print(f"P = {result['pressure_absorbing']:.2e} dyne/cm²")
        >>> print(f"F = {result['force_absorbing']:.2e} dynes")
    """
    rp = RadiationPressure(intensity)

    P_absorb_normal = rp.pressure_absorbing()
    P_reflect_normal = rp.pressure_reflecting()
    P_absorb_oblique = rp.pressure_oblique(angle, reflecting=False)
    P_reflect_oblique = rp.pressure_oblique(angle, reflecting=True)

    result = {
        "intensity": intensity,
        "area": area,
        "angle_radians": angle,
        "angle_degrees": np.degrees(angle),
        "pressure_absorbing_normal": P_absorb_normal,
        "pressure_reflecting_normal": P_reflect_normal,
        "pressure_absorbing_oblique": P_absorb_oblique,
        "pressure_reflecting_oblique": P_reflect_oblique,
        "energy_density": rp.momentum_flux(),
        "momentum_flux": rp.momentum_flux(),
        "force_absorbing_normal": rp.force_on_surface(area, reflecting=False),
        "force_reflecting_normal": rp.force_on_surface(area, reflecting=True),
        "force_absorbing_oblique": calc_radiation_force(
            intensity, area, reflecting=False, angle=angle
        ),
        "force_reflecting_oblique": calc_radiation_force(
            intensity, area, reflecting=True, angle=angle
        ),
    }

    return result
