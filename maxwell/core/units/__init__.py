"""
Unit systems and dimensional analysis for Maxwell's Treatise.

This subpackage provides:
- Dimensional analysis of electromagnetic quantities (Arts. 620-628)
- Conversion between ESU (electrostatic) and EMU (electromagnetic) units
- Verification of the speed of light relationship (Arts. 771-781)
- CGS unit conversion utilities
- Magnetic dimensions and unit definitions
"""

from __future__ import annotations

# Import from local modules
from maxwell.core.units.dimensions import (
    Dimension,
    ElectromagneticUnit,
    EMUDimensions,
    ESUDimensions,
    calc_unit_ratio,
    convert_emu_to_esu,
    convert_esu_to_emu,
    get_emu_dimensions,
    get_esu_dimensions,
    get_practical_unit_conversions,
    verify_dimensional_consistency,
    verify_speed_of_light_relationship,
)
from maxwell.core.units.units import (
    CONVERTER,
    CGSUnitConverter,
    MagneticDimensions,
)

__all__ = [
    # Dimensional analysis
    "Dimension",
    "ElectromagneticUnit",
    "ESUDimensions",
    "EMUDimensions",
    "get_esu_dimensions",
    "get_emu_dimensions",
    "calc_unit_ratio",
    "verify_speed_of_light_relationship",
    "convert_esu_to_emu",
    "convert_emu_to_esu",
    "get_practical_unit_conversions",
    "verify_dimensional_consistency",
    # Unit conversion
    "CGSUnitConverter",
    "MagneticDimensions",
    "CONVERTER",
]
