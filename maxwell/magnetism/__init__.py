"""
Maxwell's Treatise Part III: Magnetism (Arts. 371-474).

Magnetic measurements, terrestrial magnetism, and related theory.
"""

from maxwell.magnetism.magnetic_measurements import (
    # Classes
    DeflectionMagnetometer,
    UnifilarSuspension,
    BifilarSuspension,
    KewMagnetometer,
    DipCircle,
    BalanceMagnetometer,
    MagneticSurvey,
    # Functions
    magnetometer_tan_position,
    magnetometer_sine_position,
    magnetometer_gauss_method,
    torsion_constant,
    magnetic_declination,
    vibration_magnetometer,
    dip_correction,
    vertical_intensity,
)

from maxwell.magnetism.terrestrial_magnetism import (
    # Classes
    GeomagneticElements,
    # Functions
    earth_field_components,
    magnetic_elements,
    magnetic_observatory_protocol,
    magnetic_survey_method,
    gauss_spherical_analysis,
    isodynamic_lines,
    isoclinal_lines,
    isogonal_lines,
    diurnal_variation,
    magnetic_storm,
    earth_magnetic_potential,
    gauss_coefficients,
    terrestrial_analysis,
)

__all__ = [
    # Classes
    "DeflectionMagnetometer",
    "UnifilarSuspension",
    "BifilarSuspension",
    "KewMagnetometer",
    "DipCircle",
    "BalanceMagnetometer",
    "MagneticSurvey",
    "GeomagneticElements",
    # Functions
    "magnetometer_tan_position",
    "magnetometer_sine_position",
    "magnetometer_gauss_method",
    "torsion_constant",
    "magnetic_declination",
    "vibration_magnetometer",
    "dip_correction",
    "vertical_intensity",
    "earth_field_components",
    "magnetic_elements",
    "magnetic_observatory_protocol",
    "magnetic_survey_method",
    "gauss_spherical_analysis",
    "isodynamic_lines",
    "isoclinal_lines",
    "isogonal_lines",
    "diurnal_variation",
    "magnetic_storm",
    "earth_magnetic_potential",
    "gauss_coefficients",
    "terrestrial_analysis",
]
