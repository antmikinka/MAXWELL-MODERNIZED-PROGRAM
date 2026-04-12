# Utility: cgs_unit_converter

## Purpose

Comprehensive CGS unit conversion utility for electrostatic (ESU), electromagnetic (EMU), and Gaussian unit systems.

## Location

`agents/materia/utils/cgs_unit_converter.py`

---

## Module Contents

```python
"""
CGS Unit Converter

Comprehensive unit conversion between CGS (ESU, EMU, Gaussian) and SI units.
Supports all quantities relevant to Maxwell's Treatise on Electricity and Magnetism.

CGS Systems:
- ESU (Electrostatic): Based on statcoulomb, statvolt
- EMU (Electromagnetic): Based on abampere, abcoulomb
- Gaussian: Mixed system (ESU for electric, EMU for magnetic)

Reference: Maxwell, J.C. Treatise on Electricity and Magnetism (1873)
"""

from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class CGSSystem(Enum):
    """CGS unit system types."""
    ESU = "esu"  # Electrostatic
    EMU = "emu"  # Electromagnetic
    GAUSSIAN = "gaussian"  # Mixed


@dataclass
class UnitConversion:
    """Unit conversion factor and information."""
    factor: float
    offset: float  # For temperature
    from_unit: str
    to_unit: str
    category: str


# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

# Speed of light (cm/s)
C_CGS = 2.99792458e10

# Conversion between ESU and EMU charge units
ESU_EMU_RATIO = C_CGS  # 1 abcoulomb = c statcoulomb

# SI-CGS conversion factors
VOLT_TO_STATVOLT = 1 / 299.79  # 1 V = 1/299.79 statvolt
STATVOLT_TO_VOLT = 299.79  # 1 statvolt = 299.79 V

AMPERE_TO_STATAMPERE = 1 / 2.9979e9  # 1 A = c/10 statampere (ESU)
STATAMPERE_TO_AMPERE = 2.9979e9

AMPERE_TO_ABAMPERE = 0.1  # 1 A = 0.1 abampere (EMU)
ABAMPERE_TO_AMPERE = 10

# Magnetic field conversions
OERSTED_TO_A_PER_M = 79.577  # 1 oersted = 1000/4π A/m
GAUSS_TO_TESLA = 1e-4  # 1 gauss = 10⁻⁴ T


# ============================================================================
# ELECTRIC QUANTITIES (ESU)
# ============================================================================

ELECTRIC_POTENTIAL = {
    'statvolt_to_volt': STATVOLT_TO_VOLT,
    'volt_to_statvolt': VOLT_TO_STATVOLT,
    'abvolt_to_volt': 1e-8,  # EMU
    'volt_to_abvolt': 1e8,
}

ELECTRIC_CHARGE = {
    'statcoulomb_to_coulomb': 3.3356e-10,
    'coulomb_to_statcoulomb': 2.9979e9,
    'abcoulomb_to_coulomb': 10,  # EMU
    'coulomb_to_abcoulomb': 0.1,
}

ELECTRIC_FIELD = {
    'statvolt_per_cm_to_V_per_m': 29979,
    'V_per_m_to_statvolt_per_cm': 1 / 29979,
    'abvolt_per_cm_to_V_per_m': 1e-6,  # EMU
    'V_per_m_to_abvolt_per_cm': 1e6,
}

ELECTRIC_CURRENT = {
    'statampere_to_ampere': 3.3356e-10,
    'ampere_to_statampere': 2.9979e9,
    'abampere_to_ampere': 10,  # EMU
    'ampere_to_abampere': 0.1,
}

CAPACITANCE = {
    'statfarad_to_farad': 1.1126e-12,
    'farad_to_statfarad': 8.9876e11,
    'abfarad_to_farad': 1e9,  # EMU
    'farad_to_abfarad': 1e-9,
}

RESISTANCE = {
    'statohm_to_ohm': 8.9876e11,
    'ohm_to_statohm': 1.1126e-12,
    'abohm_to_ohm': 1e-9,  # EMU
    'ohm_to_abohm': 1e9,
}

CONDUCTIVITY = {
    'cgs_esu_to_S_per_m': 8.9876e9,  # s⁻¹ to S/m
    'S_per_m_to_cgs_esu': 1.1126e-10,
}

RESISTIVITY = {
    'statohm_cm_to_ohm_m': 8.9876e9,
    'ohm_m_to_statohm_cm': 1.1126e-10,
}


# ============================================================================
# MAGNETIC QUANTITIES (EMU)
# ============================================================================

MAGNETIC_FIELD_H = {
    'oersted_to_A_per_m': OERSTED_TO_A_PER_M,
    'A_per_m_to_oersted': 1 / OERSTED_TO_A_PER_M,
    'gilbert_to_A': 0.79577,  # EMU magnetomotive force
    'A_to_gilbert': 1.2566,
}

MAGNETIC_INDUCTION_B = {
    'gauss_to_tesla': GAUSS_TO_TESLA,
    'tesla_to_gauss': 1 / GAUSS_TO_TESLA,
    'maxwell_to_weber': 1e-8,  # EMU magnetic flux
    'weber_to_maxwell': 1e8,
}

MAGNETIZATION = {
    'emu_per_cm3_to_A_per_m': 1000,
    'A_per_m_to_emu_per_cm3': 0.001,
}

PERMEABILITY = {
    'cgss_to_si': 1.0,  # Relative permeability is dimensionless and same
    'si_to_cgs': 1.0,
}

SUSCEPTIBILITY = {
    'cgs_to_si': 4 * np.pi,  # κ_SI = 4π × κ_CGS
    'si_to_cgs': 1 / (4 * np.pi),
}

MAGNETIC_MOMENT = {
    'emu_to_A_m2': 0.001,
    'A_m2_to_emu': 1000,
}

INDUCTANCE = {
    'cm_to_henry': 1e-9,  # CGS inductance in cm
    'henry_to_cm': 1e9,
    'abhenry_to_henry': 1e-9,  # EMU
    'henry_to_abhenry': 1e9,
}


# ============================================================================
# MECHANICAL QUANTITIES (CGS)
# ============================================================================

ENERGY = {
    'erg_to_joule': 1e-7,
    'joule_to_erg': 1e7,
    'electronvolt_to_erg': 1.6022e-12,
    'erg_to_electronvolt': 6.2415e11,
}

POWER = {
    'erg_per_s_to_watt': 1e-7,
    'watt_to_erg_per_s': 1e7,
}

FORCE = {
    'dyne_to_newton': 1e-5,
    'newton_to_dyne': 1e5,
}

PRESSURE = {
    'dyne_per_cm2_to_pascal': 0.1,
    'pascal_to_dyne_per_cm2': 10,
}

STRESS = {
    'dyne_per_cm2_to_pascal': 0.1,
    'pascal_to_dyne_per_cm2': 10,
}


# ============================================================================
# MATERIAL PROPERTIES
# ============================================================================

DENSITY = {
    'g_per_cm3_to_kg_per_m3': 1000,
    'kg_per_m3_to_g_per_cm3': 0.001,
}

CONCENTRATION = {
    'mol_per_cm3_to_mol_per_m3': 1e6,
    'mol_per_m3_to_mol_per_cm3': 1e-6,
    'mol_per_L_to_mol_per_cm3': 0.001,
    'mol_per_cm3_to_mol_per_L': 1000,
}

MOBILITY_IONIC = {
    'cm2_per_statvolt_s_to_m2_per_V_s': 3.3356e-6,
    'm2_per_V_s_to_cm2_per_statvolt_s': 2.9979e5,
}

DIFFUSION = {
    'cm2_per_s_to_m2_per_s': 1e-4,
    'm2_per_s_to_cm2_per_s': 1e4,
}


# ============================================================================
# CONVERSION FUNCTIONS
# ============================================================================

def convert_potential(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert electric potential between units.
    
    Args:
        value: Value to convert
        from_unit: Source unit ('statvolt', 'volt', 'abvolt')
        to_unit: Target unit
    
    Returns:
        Converted value
    """
    # First convert to volt
    if from_unit == 'statvolt':
        value_volt = value * STATVOLT_TO_VOLT
    elif from_unit == 'abvolt':
        value_volt = value * 1e-8
    elif from_unit == 'volt':
        value_volt = value
    else:
        raise ValueError(f"Unknown unit: {from_unit}")
    
    # Then convert from volt to target
    if to_unit == 'volt':
        return value_volt
    elif to_unit == 'statvolt':
        return value_volt * VOLT_TO_STATVOLT
    elif to_unit == 'abvolt':
        return value_volt * 1e8
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


def convert_electric_field(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert electric field between units.
    """
    conversions = {
        ('statvolt_per_cm', 'V_per_m'): 29979,
        ('V_per_m', 'statvolt_per_cm'): 1 / 29979,
        ('statvolt_per_cm', 'statvolt_per_cm'): 1,
        ('V_per_m', 'V_per_m'): 1,
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return value * conversions[key]
    
    raise ValueError(f"No conversion from {from_unit} to {to_unit}")


def convert_magnetic_field(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert magnetic field H between units.
    """
    conversions = {
        ('oersted', 'A_per_m'): OERSTED_TO_A_PER_M,
        ('A_per_m', 'oersted'): 1 / OERSTED_TO_A_PER_M,
        ('oersted', 'oersted'): 1,
        ('A_per_m', 'A_per_m'): 1,
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return value * conversions[key]
    
    raise ValueError(f"No conversion from {from_unit} to {to_unit}")


def convert_magnetic_induction(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert magnetic induction B between units.
    """
    conversions = {
        ('gauss', 'tesla'): GAUSS_TO_TESLA,
        ('tesla', 'gauss'): 1 / GAUSS_TO_TESLA,
        ('gauss', 'gauss'): 1,
        ('tesla', 'tesla'): 1,
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return value * conversions[key]
    
    raise ValueError(f"No conversion from {from_unit} to {to_unit}")


def convert_energy(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert energy between units.
    """
    conversions = {
        ('erg', 'joule'): 1e-7,
        ('joule', 'erg'): 1e7,
        ('erg', 'eV'): 6.2415e11,
        ('eV', 'erg'): 1.6022e-12,
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return value * conversions[key]
    
    raise ValueError(f"No conversion from {from_unit} to {to_unit}")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert temperature between units.
    """
    if from_unit == 'K' and to_unit == 'C':
        return value - 273.15
    elif from_unit == 'C' and to_unit == 'K':
        return value + 273.15
    elif from_unit == 'F' and to_unit == 'K':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'K' and to_unit == 'F':
        return (value - 273.15) * 9/5 + 32
    elif from_unit == to_unit:
        return value
    
    raise ValueError(f"No conversion from {from_unit} to {to_unit}")


# ============================================================================
# QUICK REFERENCE TABLES
# ============================================================================

def get_conversion_table(category: str) -> Dict[str, float]:
    """
    Get conversion table for a category of quantities.
    
    Args:
        category: Quantity category
    
    Returns:
        Dictionary of conversion factors
    """
    tables = {
        'electric_potential': ELECTRIC_POTENTIAL,
        'electric_charge': ELECTRIC_CHARGE,
        'electric_field': ELECTRIC_FIELD,
        'electric_current': ELECTRIC_CURRENT,
        'capacitance': CAPACITANCE,
        'resistance': RESISTANCE,
        'conductivity': CONDUCTIVITY,
        'magnetic_field_h': MAGNETIC_FIELD_H,
        'magnetic_induction_b': MAGNETIC_INDUCTION_B,
        'magnetization': MAGNETIZATION,
        'susceptibility': SUSCEPTIBILITY,
        'energy': ENERGY,
        'power': POWER,
        'force': FORCE,
        'pressure': PRESSURE,
        'density': DENSITY,
        'concentration': CONCENTRATION,
        'diffusion': DIFFUSION,
    }
    
    if category in tables:
        return tables[category]
    
    raise ValueError(f"Unknown category: {category}")


def print_conversion_summary():
    """Print a summary of all available conversions."""
    print("=" * 70)
    print("CGS UNIT CONVERSION SUMMARY")
    print("=" * 70)
    print()
    
    print("ELECTRIC QUANTITIES (ESU):")
    print(f"  1 statvolt     = {STATVOLT_TO_VOLT:.2f} V")
    print(f"  1 statcoulomb  = {3.3356e-10:.2e} C")
    print(f"  1 statampere   = {3.3356e-10:.2e} A")
    print(f"  1 statfarad    = {1.1126e-12:.2e} F")
    print(f"  1 statohm      = {8.9876e11:.2e} Ω")
    print()
    
    print("MAGNETIC QUANTITIES (EMU):")
    print(f"  1 oersted      = {OERSTED_TO_A_PER_M:.2f} A/m")
    print(f"  1 gauss        = {GAUSS_TO_TESLA:.1e} T")
    print(f"  1 emu/cm³      = {1000:.0f} A/m")
    print(f"  1 maxwell      = {1e-8:.0e} Wb")
    print()
    
    print("MECHANICAL QUANTITIES (CGS):")
    print(f"  1 erg          = {1e-7:.0e} J")
    print(f"  1 dyne         = {1e-5:.0e} N")
    print(f"  1 dyne/cm²     = {0.1:.1f} Pa")
    print()
    
    print("KEY RELATIONS (CGS Gaussian):")
    print("  D = KE = E + 4πP  (dielectric)")
    print("  B = μH = H + 4πI  (magnetic)")
    print("  div(E) = 4πρ      (Gauss's law)")
    print()


# ============================================================================
# VALIDATION
# ============================================================================

def validate_cgs_consistency(value: float, unit: str, category: str) -> bool:
    """
    Validate that a value is within reasonable CGS ranges.
    
    Args:
        value: Value to check
        unit: Unit of the value
        category: Quantity category
    
    Returns:
        True if value is reasonable
    """
    # Define reasonable ranges for each category
    ranges = {
        'electric_potential_statvolt': (1e-6, 1e6),
        'electric_field_statvolt_per_cm': (1e-6, 1e5),
        'magnetic_field_oersted': (1e-6, 1e6),
        'magnetic_induction_gauss': (1e-9, 1e6),
        'permeability': (0.1, 1e6),
        'dielectric_constant': (1, 1e5),
        'conductivity_cgs': (1e-15, 1e20),
        'energy_erg': (1e-12, 1e14),
    }
    
    key = f"{category}_{unit}"
    if key in ranges:
        min_val, max_val = ranges[key]
        return min_val <= abs(value) <= max_val
    
    return True  # No validation defined


# ============================================================================
# MAIN (Quick Reference)
# ============================================================================

if __name__ == "__main__":
    print_conversion_summary()
```

---

## Usage Examples

```python
from cgs_unit_converter import *

# Example 1: Electric potential conversion
V = convert_potential(1, 'statvolt', 'volt')
print(f"1 statvolt = {V:.2f} V")  # 299.79 V

# Example 2: Magnetic field conversion
H_A_m = convert_magnetic_field(100, 'oersted', 'A_per_m')
print(f"100 oersted = {H_A_m:.1f} A/m")  # 7957.7 A/m

# Example 3: Energy conversion
E_erg = convert_energy(1e-6, 'joule', 'erg')
print(f"1 μJ = {E_erg:.0f} erg")  # 10 erg

# Example 4: Print conversion summary
print_conversion_summary()
```

---

## Quality Criteria

- [ ] All conversions to/from CGS units
- [ ] ESU, EMU, and Gaussian systems supported
- [ ] Comprehensive coverage of Maxwell treatise quantities
- [ ] Input validation implemented
- [ ] Documentation complete
