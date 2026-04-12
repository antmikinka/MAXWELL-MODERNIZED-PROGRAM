"""
Optics — Electromagnetic Wave Theory and Light Propagation.

This module implements Maxwell's electromagnetic theory of light,
proving that light is an electromagnetic wave phenomenon.

Part IV, Chapter XX: Electromagnetic Theory of Light (Arts. 781-808)

Key components:
- wave_equation: Derivation of EM wave equation from Maxwell's equations
- velocity: EM wave velocity and refractive index (Arts. 786-787)
- constants: Optical constants and material properties (Arts. 788-790)
- radiation_pressure: Mechanical action of light (Arts. 791-794)
- metals: Reflection/refraction in metallic media (Arts. 795-800)
- plane_waves: Advanced polarization and interference (Arts. 801-803)
- crystals: Birefringence and crystalline optics (Arts. 804-805)
- diffusion: Light diffusion through turbid media (Arts. 806-808)

Maxwell's greatest achievement was recognizing that the wave speed derived from
electromagnetic theory equals the measured speed of light, proving that light
itself is an electromagnetic phenomenon.
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

from maxwell.optics.velocity import (
    WaveVelocity,
    calc_wave_velocity,
    calc_refractive_index,
    calc_permittivity_from_refractive_index,
    calc_wavelength_in_medium,
    calc_wave_number,
    calc_E_B_ratio,
    verify_maxwell_velocity,
    analyze_wave_velocity,
)

from maxwell.optics.constants import (
    OpticalConstants,
    OPTICAL_CONSTANTS,
    WAVELENGTH_RANGES,
    get_optical_constants,
    calc_refractive_index_from_EM,
    calc_frequency_from_wavelength,
    calc_wavelength_from_frequency,
    calc_optical_path_difference,
    classify_spectral_region,
    verify_optical_constants,
    analyze_optical_constants,
)

from maxwell.optics.radiation_pressure import (
    RadiationPressure,
    calc_radiation_pressure,
    calc_radiation_pressure_oblique,
    calc_radiation_force,
    calc_energy_density_from_intensity,
    calc_radiation_momentum,
    calc_radiation_pressure_from_E,
    verify_radiation_pressure,
    analyze_radiation_pressure,
)

from maxwell.optics.metals import (
    MetallicReflection,
    METAL_OPTICAL_CONSTANTS,
    get_metal_constants,
    calc_fresnel_reflection_metal,
    calc_metal_reflectance_normal,
    calc_skin_depth,
    calc_absorption_coefficient,
    verify_metallic_reflection,
    analyze_metallic_reflection,
)

from maxwell.optics.plane_waves import (
    PolarizationState,
    calc_polarized_wave_intensity,
    calc_wave_interference,
    calc_polarization_ellipse,
    calc_fringe_visibility,
    verify_polarization_relations,
    analyze_plane_wave_polarization,
)

from maxwell.optics.crystals import (
    CrystalOptics,
    CRYSTAL_OPTICAL_CONSTANTS,
    get_crystal_constants,
    calc_birefringence,
    calc_velocity_difference,
    calc_retardation_waves,
    verify_crystal_optics,
    analyze_crystal_optics,
)

from maxwell.optics.diffusion import (
    LightDiffusion,
    calc_beer_lambert_transmission,
    calc_transmitted_intensity,
    calc_absorbance,
    calc_scattering_albedo,
    calc_mean_free_path,
    calc_optical_depth,
    verify_light_diffusion,
    analyze_light_diffusion,
)

__all__ = [
    # Wave equation (Arts. 781-791)
    "ElectromagneticWave",
    "PlaneWave",
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
    "WaveEquationCalculator",

    # Velocity (Arts. 786-787)
    "WaveVelocity",
    "calc_wave_velocity",
    "calc_refractive_index",
    "calc_permittivity_from_refractive_index",
    "calc_wavelength_in_medium",
    "calc_wave_number",
    "calc_E_B_ratio",
    "verify_maxwell_velocity",
    "analyze_wave_velocity",

    # Constants (Arts. 788-790)
    "OpticalConstants",
    "OPTICAL_CONSTANTS",
    "WAVELENGTH_RANGES",
    "get_optical_constants",
    "calc_refractive_index_from_EM",
    "calc_frequency_from_wavelength",
    "calc_wavelength_from_frequency",
    "calc_optical_path_difference",
    "classify_spectral_region",
    "verify_optical_constants",
    "analyze_optical_constants",

    # Radiation pressure (Arts. 791-794)
    "RadiationPressure",
    "calc_radiation_pressure",
    "calc_radiation_pressure_oblique",
    "calc_radiation_force",
    "calc_energy_density_from_intensity",
    "calc_radiation_momentum",
    "calc_radiation_pressure_from_E",
    "verify_radiation_pressure",
    "analyze_radiation_pressure",

    # Metals (Arts. 795-800)
    "MetallicReflection",
    "METAL_OPTICAL_CONSTANTS",
    "get_metal_constants",
    "calc_fresnel_reflection_metal",
    "calc_metal_reflectance_normal",
    "calc_skin_depth",
    "calc_absorption_coefficient",
    "verify_metallic_reflection",
    "analyze_metallic_reflection",

    # Plane waves (Arts. 801-803)
    "PolarizationState",
    "calc_polarized_wave_intensity",
    "calc_wave_interference",
    "calc_polarization_ellipse",
    "calc_fringe_visibility",
    "verify_polarization_relations",
    "analyze_plane_wave_polarization",

    # Crystals (Arts. 804-805)
    "CrystalOptics",
    "CRYSTAL_OPTICAL_CONSTANTS",
    "get_crystal_constants",
    "calc_birefringence",
    "calc_velocity_difference",
    "calc_retardation_waves",
    "verify_crystal_optics",
    "analyze_crystal_optics",

    # Diffusion (Arts. 806-808)
    "LightDiffusion",
    "calc_beer_lambert_transmission",
    "calc_transmitted_intensity",
    "calc_absorbance",
    "calc_scattering_albedo",
    "calc_mean_free_path",
    "calc_optical_depth",
    "verify_light_diffusion",
    "analyze_light_diffusion",
]
