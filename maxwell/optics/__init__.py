"""
Optics — Electromagnetic Wave Theory.

This module implements Maxwell's electromagnetic theory of light,
proving that light is an electromagnetic wave phenomenon.

Part IV, Chapter XX: Electromagnetic Theory of Light (Arts. 781-791)

Key achievements:
- Derivation of the electromagnetic wave equation from Maxwell's equations
- Proof that EM wave speed equals the measured speed of light
- Plane wave solutions and their properties
- Energy and momentum in electromagnetic waves
- Poynting vector and energy flux
"""

from maxwell.optics.wave_equation import (
    # Dataclasses
    ElectromagneticWave,
    PlaneWave,

    # Core functions
    derive_wave_equation_from_maxwell,
    calc_wave_speed,
    calc_wavelength,
    calc_plane_wave_E,
    calc_plane_wave_B_from_E,
    calc_poynting_vector,
    calc_energy_density,
    calc_wave_intensity,
    verify_transversality,
    verify_speed_equals_c,
    analyze_wave,

    # Calculator class
    WaveEquationCalculator,
)

__all__ = [
    # Dataclasses
    "ElectromagneticWave",
    "PlaneWave",

    # Core functions
    "derive_wave_equation_from_maxwell",
    "calc_wave_speed",
    "calc_wavelength",
    "calc_plane_wave_E",
    "calc_plane_wave_B_from_E",
    "calc_poynting_vector",
    "calc_energy_density",
    "calc_wave_intensity",
    "verify_transversality",
    "verify_speed_equals_c",
    "analyze_wave",

    # Calculator class
    "WaveEquationCalculator",
]
