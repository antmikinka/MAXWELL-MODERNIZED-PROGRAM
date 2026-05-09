"""
Maxwell's Treatise Part III: Magnetism (Arts. 371-474).

Magnetic measurements, terrestrial magnetism, and related theory.
"""

from maxwell.magnetism.magnetic_measurements import (  # Classes; Functions
    BalanceMagnetometer,
    BifilarSuspension,
    DeflectionMagnetometer,
    DipCircle,
    KewMagnetometer,
    MagneticSurvey,
    UnifilarSuspension,
    dip_correction,
    magnetic_declination,
    magnetometer_gauss_method,
    magnetometer_sine_position,
    magnetometer_tan_position,
    torsion_constant,
    vertical_intensity,
    vibration_magnetometer,
)
from maxwell.magnetism.terrestrial_magnetism import (  # Classes; Functions
    GeomagneticElements,
    diurnal_variation,
    earth_field_components,
    earth_magnetic_potential,
    gauss_coefficients,
    gauss_spherical_analysis,
    isoclinal_lines,
    isodynamic_lines,
    isogonal_lines,
    magnetic_elements,
    magnetic_observatory_protocol,
    magnetic_storm,
    magnetic_survey_method,
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
