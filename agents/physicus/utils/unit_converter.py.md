# Unit Converter Utilities

## Purpose

Comprehensive unit conversion utilities for CGS and SI systems. All conversions preserve exact values where possible.

## Module: unit_converter.py

```python
"""
Unit Converter Utilities

Comprehensive unit conversions between CGS and SI systems.
All physics implementations use CGS by default.

Maxwell Articles: 41-42 (Dimensions and units)
"""

import numpy as np
from typing import Union, Dict, Tuple
from enum import Enum


class UnitSystem(Enum):
    """Supported unit systems."""
    CGS_ESU = "cgs_esu"       # Electrostatic units
    CGS_EMU = "cgs_emu"       # Electromagnetic units
    CGS_GAUSSIAN = "cgs_gaussian"  # Gaussian (mixed)
    SI = "si"                 # SI (MKSA)


# =============================================================================
# Fundamental Conversion Factors
# =============================================================================

# Speed of light (exact)
C_CGS = 29979245800  # cm/s

# CGS to SI length/mass/time
LENGTH_CM_TO_M = 0.01
MASS_G_TO_KG = 0.001
TIME_S_TO_S = 1.0

# Force and energy
DYNE_TO_NEWTON = 1e-5
ERG_TO_JOULE = 1e-7

# =============================================================================
# Electrostatic Conversions (ESU)
# =============================================================================

# Charge
STATCOULOMB_TO_COULOMB = 3.335640951981520e-10  # exact via ε₀
COULOMB_TO_STATCOULOMB = 1 / STATCOULOMB_TO_COULOMB

# Current
STATAMPERE_TO_AMPERE = STATCOULOMB_TO_COULOMB  # statC/s
AMPERE_TO_STATAMPERE = 1 / STATAMPERE_TO_AMPERE

# Electric field
STATVOLT_PER_CM_TO_VOLT_PER_M = 29979.2458
VOLT_PER_M_TO_STATVOLT_PER_CM = 1 / STATVOLT_PER_CM_TO_VOLT_PER_M

# Potential
STATVOLT_TO_VOLT = 299.792458
VOLT_TO_STATVOLT = 1 / STATVOLT_TO_VOLT

# Capacitance
STATFARAD_TO_FARAD = 1.112650056053618e-12
FARAD_TO_STATFARAD = 1 / STATFARAD_TO_FARAD

# Resistance
STATOHM_TO_OHM = 8.987551787368176e11
OHM_TO_STATOHM = 1 / STATOHM_TO_OHM

# =============================================================================
# Electromagnetic Conversions (EMU)
# =============================================================================

# Current
ABAMPERE_TO_AMPERE = 10.0
AMPERE_TO_ABAMPERE = 0.1

# Charge
ABCOULOMB_TO_COULOMB = 10.0
COULOMB_TO_ABCOULOMB = 0.1

# Voltage
ABVOLT_TO_VOLT = 1e-8
VOLT_TO_ABVOLT = 1e8

# Resistance
ABOHM_TO_OHM = 1e-9
OHM_TO_ABOHM = 1e9

# Inductance
ABHENRY_TO_HENRY = 1e-9
HENRY_TO_ABHENRY = 1e9
CM_TO_HENRY = 1e-9  # CGS EMU inductance is in cm

# =============================================================================
# Magnetic Conversions
# =============================================================================

# Magnetic field B
GAUSS_TO_TESLA = 1e-4
TESLA_TO_GAUSS = 1e4

# Magnetic field H
OERSTED_TO_A_PER_M = 79.57747154594767
A_PER_M_TO_OERSTED = 1 / OERSTED_TO_A_PER_M

# Magnetic flux
MAXWELL_TO_WEBER = 1e-8
WEBER_TO_MAXWELL = 1e8

# Magnetic moment
ERG_PER_GAUSS_TO_A_M2 = 1e-3
A_M2_TO_ERG_PER_GAUSS = 1e3

# Magnetization
ERG_PER_GAUSS_CM3_TO_A_PER_M = 1000
A_PER_M_TO_ERG_PER_GAUSS_CM3 = 0.001

# =============================================================================
# Material Property Conversions
# =============================================================================

# Conductivity
CGS_CONDUCTIVITY_TO_SI = 1.112650056e-12  # s⁻¹ to S/m
SI_CONDUCTIVITY_TO_CGS = 1 / CGS_CONDUCTIVITY_TO_SI

# Permittivity (relative - same in both systems)
# ε_r is dimensionless and identical in CGS and SI

# Permeability (relative - same in both systems)
# μ_r is dimensionless and identical in CGS and SI

# Absolute permittivity
# CGS: ε = ε_r (dimensionless, since ε₀ = 1)
# SI: ε = ε₀ε_r where ε₀ = 8.854×10⁻¹² F/m
EPSILON_0_SI = 8.854187817e-12  # F/m

# Absolute permeability
# CGS: μ = μ_r (dimensionless, since μ₀ = 1 in some conventions)
# SI: μ = μ₀μ_r where μ₀ = 4π×10⁻⁷ H/m
MU_0_SI = 4 * np.pi * 1e-7  # H/m


class UnitConverter:
    """
    Comprehensive unit converter for electromagnetic quantities.
    
    Examples
    --------
    >>> converter = UnitConverter()
    >>> converter.convert(1.0, 'charge', 'statcoulomb', 'coulomb')
    3.336e-10
    >>> converter.convert(1000, 'magnetic_field', 'gauss', 'tesla')
    0.1
    """
    
    def __init__(self):
        self.c = C_CGS
        
    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert length between units.
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('cm', 'm', 'mm', 'um', 'nm', 'angstrom')
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        # Convert to meters first
        to_meter = {
            'cm': 0.01, 'm': 1.0, 'mm': 0.001,
            'um': 1e-6, 'nm': 1e-9, 'angstrom': 1e-10,
            'km': 1000, 'inch': 0.0254, 'foot': 0.3048
        }
        
        value_in_m = value * to_meter[from_unit]
        return value_in_m / to_meter[to_unit]
    
    def convert_charge(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert electric charge between units.
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('statcoulomb', 'coulomb', 'abcoulomb', 'e')
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        # Elementary charge
        E_CHARGE_C = 1.602176634e-19  # C
        E_CHARGE_STATC = 4.80320471e-10  # statC
        
        conversions = {
            ('statcoulomb', 'coulomb'): STATCOULOMB_TO_COULOMB,
            ('coulomb', 'statcoulomb'): COULOMB_TO_STATCOULOMB,
            ('abcoulomb', 'coulomb'): ABCOULOMB_TO_COULOMB,
            ('coulomb', 'abcoulomb'): COULOMB_TO_ABCOULOMB,
            ('statcoulomb', 'abcoulomb'): STATCOULOMB_TO_COULOMB * ABCOULOMB_TO_COULOMB,
            ('abcoulomb', 'statcoulomb'): COULOMB_TO_ABCOULOMB * COULOMB_TO_STATCOULOMB,
            ('e', 'coulomb'): E_CHARGE_C,
            ('e', 'statcoulomb'): E_CHARGE_STATC,
        }
        
        if (from_unit, to_unit) in conversions:
            return value * conversions[(from_unit, to_unit)]
        
        if from_unit == to_unit:
            return value
        
        raise ValueError(f"Unknown conversion: {from_unit} to {to_unit}")
    
    def convert_field(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert electric or magnetic field between units.
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('statvolt/cm', 'V/m', 'gauss', 'tesla', 'oersted', 'A/m')
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        conversions = {
            ('statvolt/cm', 'V/m'): STATVOLT_PER_CM_TO_VOLT_PER_M,
            ('V/m', 'statvolt/cm'): VOLT_PER_M_TO_STATVOLT_PER_CM,
            ('gauss', 'tesla'): GAUSS_TO_TESLA,
            ('tesla', 'gauss'): TESLA_TO_GAUSS,
            ('oersted', 'A/m'): OERSTED_TO_A_PER_M,
            ('A/m', 'oersted'): A_PER_M_TO_OERSTED,
        }
        
        if (from_unit, to_unit) in conversions:
            return value * conversions[(from_unit, to_unit)]
        
        if from_unit == to_unit:
            return value
        
        raise ValueError(f"Unknown conversion: {from_unit} to {to_unit}")
    
    def convert_potential(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert electric potential between units.
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('statvolt', 'volt', 'abvolt')
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        conversions = {
            ('statvolt', 'volt'): STATVOLT_TO_VOLT,
            ('volt', 'statvolt'): VOLT_TO_STATVOLT,
            ('abvolt', 'volt'): ABVOLT_TO_VOLT,
            ('volt', 'abvolt'): VOLT_TO_ABVOLT,
            ('statvolt', 'abvolt'): STATVOLT_TO_VOLT * VOLT_TO_ABVOLT,
            ('abvolt', 'statvolt'): ABVOLT_TO_VOLT * VOLT_TO_STATVOLT,
        }
        
        if (from_unit, to_unit) in conversions:
            return value * conversions[(from_unit, to_unit)]
        
        if from_unit == to_unit:
            return value
        
        raise ValueError(f"Unknown conversion: {from_unit} to {to_unit}")
    
    def convert_conductivity(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert electrical conductivity between CGS and SI.
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('s^-1' for CGS, 'S/m' for SI)
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        if from_unit == 's^-1' and to_unit == 'S/m':
            return value * CGS_CONDUCTIVITY_TO_SI
        elif from_unit == 'S/m' and to_unit == 's^-1':
            return value * SI_CONDUCTIVITY_TO_CGS
        elif from_unit == to_unit:
            return value
        else:
            raise ValueError(f"Unknown conversion: {from_unit} to {to_unit}")
    
    def convert_inductance(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert inductance between CGS (cm) and SI (henry).
        
        Parameters
        ----------
        value : float
            Value to convert
        from_unit : str
            Source unit ('cm', 'henry', 'nH', 'uH', 'mH')
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        
        Notes
        -----
        In CGS EMU, inductance has dimensions of length (centimeters).
        1 cm inductance = 10⁻⁹ H = 1 nH
        """
        to_henry = {
            'cm': 1e-9, 'henry': 1.0, 'nH': 1e-9, 'uH': 1e-6, 'mH': 1e-3
        }
        
        value_in_henry = value * to_henry[from_unit]
        return value_in_henry / to_henry[to_unit]
    
    def convert(self, value: float, quantity: str, from_unit: str, to_unit: str) -> float:
        """
        General conversion method.
        
        Parameters
        ----------
        value : float
            Value to convert
        quantity : str
            Physical quantity ('length', 'charge', 'field', 'potential', 
                             'conductivity', 'inductance')
        from_unit : str
            Source unit
        to_unit : str
            Target unit
            
        Returns
        -------
        converted : float
            Converted value
        """
        converters = {
            'length': self.convert_length,
            'charge': self.convert_charge,
            'field': self.convert_field,
            'potential': self.convert_potential,
            'conductivity': self.convert_conductivity,
            'inductance': self.convert_inductance,
        }
        
        if quantity not in converters:
            raise ValueError(f"Unknown quantity: {quantity}")
        
        return converters[quantity](value, from_unit, to_unit)


# =============================================================================
# Convenience Functions
# =============================================================================

def cgs_to_si(value: float, quantity: str) -> float:
    """
    Convert from CGS to SI units.
    
    Parameters
    ----------
    value : float
        Value in CGS units
    quantity : str
        Physical quantity type
        
    Returns
    -------
    si_value : float
        Value in SI units
    """
    converter = UnitConverter()
    
    si_units = {
        'charge': ('statcoulomb', 'coulomb'),
        'field_e': ('statvolt/cm', 'V/m'),
        'field_b': ('gauss', 'tesla'),
        'potential': ('statvolt', 'volt'),
        'conductivity': ('s^-1', 'S/m'),
        'inductance': ('cm', 'henry'),
        'energy': ('erg', 'joule'),
        'force': ('dyne', 'newton'),
    }
    
    if quantity not in si_units:
        raise ValueError(f"Unknown quantity: {quantity}")
    
    from_unit, to_unit = si_units[quantity]
    return converter.convert(value, quantity.split('_')[0], from_unit, to_unit)


def si_to_cgs(value: float, quantity: str) -> float:
    """
    Convert from SI to CGS units.
    
    Parameters
    ----------
    value : float
        Value in SI units
    quantity : str
        Physical quantity type
        
    Returns
    -------
    cgs_value : float
        Value in CGS units
    """
    converter = UnitConverter()
    
    cgs_units = {
        'charge': ('coulomb', 'statcoulomb'),
        'field_e': ('V/m', 'statvolt/cm'),
        'field_b': ('tesla', 'gauss'),
        'potential': ('volt', 'statvolt'),
        'conductivity': ('S/m', 's^-1'),
        'inductance': ('henry', 'cm'),
        'energy': ('joule', 'erg'),
        'force': ('newton', 'dyne'),
    }
    
    if quantity not in cgs_units:
        raise ValueError(f"Unknown quantity: {quantity}")
    
    from_unit, to_unit = cgs_units[quantity]
    return converter.convert(value, quantity.split('_')[0], from_unit, to_unit)
```

## Usage Examples

```python
from maxwell.utils.unit_converter import (
    UnitConverter, cgs_to_si, si_to_cgs
)

# Create converter
converter = UnitConverter()

# Convert charge
q_cgs = 1.0  # statcoulomb
q_si = converter.convert(q_cgs, 'charge', 'statcoulomb', 'coulomb')
print(f"1 statcoulomb = {q_si} coulomb")

# Convert magnetic field
B_gauss = 10000  # gauss
B_tesla = converter.convert_field(B_gauss, 'gauss', 'tesla')
print(f"10000 gauss = {B_tesla} tesla")

# Convert conductivity
sigma_cgs = 5.96e17  # copper in CGS (s⁻¹)
sigma_si = cgs_to_si(sigma_cgs, 'conductivity')
print(f"Copper conductivity: {sigma_si} S/m")

# Convenience functions
q_statc = si_to_cgs(1e-9, 'charge')  # 1 nC to statcoulomb
print(f"1 nC = {q_statc} statcoulomb")
```

## Related Utilities

- `field_computation_helper.py` - Field calculations
- `validation_helper.py` - Physics validation
