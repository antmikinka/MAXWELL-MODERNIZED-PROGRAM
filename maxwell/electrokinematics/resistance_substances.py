"""
Resistance of Substances — Maxwell's Part II, Chapter XII (Arts. 359-370).

This module implements Maxwell's theory of resistance properties of different
substances:

1. **Metal Resistance** (Arts. 359-362): Pure metal resistivity and temperature dependence
   - Metallic conduction theory
   - Temperature coefficient of resistance
   - Matthiessen's rule for pure metals

2. **Alloy Resistance** (Arts. 363-364): Alloy resistivity
   - Matthiessen's rule for alloys
   - Composition dependence

3. **Electrolyte Resistance** (Arts. 365-366): Ionic conduction
   - Electrolyte resistivity
   - Concentration dependence

4. **Dielectric Resistance** (Arts. 367-368): Insulator resistance
   - Leakage through insulators
   - Volume and surface resistivity

5. **Semiconductor Resistance** (Arts. 369-370): Early semiconductor observations
   - Temperature dependence (negative coefficient)
   - Photoconductivity (Maxwell's observations)

Maxwell's key insight: Resistance depends on material composition, temperature,
and physical state. His systematic measurements established the foundations
of materials science.

CGS-EMU units are used throughout:
    - Resistance: abohms
    - Resistivity: abohm·cm
    - Conductivity: siemens/cm
    - Temperature: Kelvin

Category: A (maxwell_original) — Maxwell's theory of substance resistance.

References:
    Part II, Chapter XII: Resistance of Substances (Arts. 359-370).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Dict, List, Optional, Union

import numpy as np

from maxwell.config.constants import C_APPROX, CONST, C
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# MATERIAL DATABASE
# =============================================================================


@dataclass
class MaterialResistance:
    """
    Material resistance property database.

    This class contains reference data for resistivity and temperature
    coefficients of common materials, based on Maxwell's measurements
    and modern values.

    Attributes:
        name: Material name.
        resistivity_20c: Resistivity at 20°C (abohm·cm).
        temperature_coefficient: Alpha at 20°C (1/K).
        conductivity_20c: Calculated conductivity (siemens/cm).
    """

    name: str
    resistivity_20c: float  # abohm·cm
    temperature_coefficient: float  # 1/K
    material_type: str  # "metal", "alloy", "electrolyte", "dielectric", "semiconductor"

    def __post_init__(self):
        """Calculate conductivity from resistivity."""
        if self.resistivity_20c > 0:
            self.conductivity_20c = 1.0 / self.resistivity_20c
        else:
            self.conductivity_20c = 0.0

    @property
    def resistivity(self) -> float:
        """Return resistivity at 20°C."""
        return self.resistivity_20c

    @property
    def conductivity(self) -> float:
        """Return conductivity at 20°C."""
        return self.conductivity_20c


# Material database (CGS-EMU units: abohm·cm for resistivity)
# 1 ohm·cm = 1e9 abohm·cm

MATERIAL_DATABASE: Dict[str, MaterialResistance] = {
    # Pure Metals (Arts. 359-362)
    "silver": MaterialResistance(
        name="Silver",
        resistivity_20c=1.59e-8 * 1e9,  # 1.59e-8 ohm·cm → abohm·cm
        temperature_coefficient=0.0038,
        material_type="metal",
    ),
    "copper": MaterialResistance(
        name="Copper",
        resistivity_20c=1.68e-8 * 1e9,
        temperature_coefficient=0.00393,
        material_type="metal",
    ),
    "gold": MaterialResistance(
        name="Gold",
        resistivity_20c=2.44e-8 * 1e9,
        temperature_coefficient=0.0034,
        material_type="metal",
    ),
    "aluminum": MaterialResistance(
        name="Aluminum",
        resistivity_20c=2.82e-8 * 1e9,
        temperature_coefficient=0.0039,
        material_type="metal",
    ),
    "iron": MaterialResistance(
        name="Iron",
        resistivity_20c=9.71e-8 * 1e9,
        temperature_coefficient=0.0050,
        material_type="metal",
    ),
    "nickel": MaterialResistance(
        name="Nickel",
        resistivity_20c=6.99e-8 * 1e9,
        temperature_coefficient=0.0060,
        material_type="metal",
    ),
    "platinum": MaterialResistance(
        name="Platinum",
        resistivity_20c=10.6e-8 * 1e9,
        temperature_coefficient=0.00392,
        material_type="metal",
    ),
    "tungsten": MaterialResistance(
        name="Tungsten",
        resistivity_20c=5.6e-8 * 1e9,
        temperature_coefficient=0.0045,
        material_type="metal",
    ),
    "zinc": MaterialResistance(
        name="Zinc",
        resistivity_20c=5.9e-8 * 1e9,
        temperature_coefficient=0.0037,
        material_type="metal",
    ),
    "tin": MaterialResistance(
        name="Tin",
        resistivity_20c=11.5e-8 * 1e9,
        temperature_coefficient=0.0042,
        material_type="metal",
    ),
    "lead": MaterialResistance(
        name="Lead",
        resistivity_20c=22.0e-8 * 1e9,
        temperature_coefficient=0.0039,
        material_type="metal",
    ),
    "mercury": MaterialResistance(
        name="Mercury",
        resistivity_20c=98.0e-8 * 1e9,
        temperature_coefficient=0.0009,
        material_type="metal",
    ),
    # Alloys (Arts. 363-364)
    "brass": MaterialResistance(
        name="Brass (Cu-Zn)",
        resistivity_20c=6.0e-8 * 1e9,
        temperature_coefficient=0.0015,
        material_type="alloy",
    ),
    "bronze": MaterialResistance(
        name="Bronze (Cu-Sn)",
        resistivity_20c=10.0e-8 * 1e9,
        temperature_coefficient=0.0010,
        material_type="alloy",
    ),
    "constantan": MaterialResistance(
        name="Constantan (Cu-Ni)",
        resistivity_20c=49.0e-8 * 1e9,
        temperature_coefficient=0.00001,  # Very low TCR
        material_type="alloy",
    ),
    "manganin": MaterialResistance(
        name="Manganin (Cu-Mn-Ni)",
        resistivity_20c=48.0e-8 * 1e9,
        temperature_coefficient=0.00002,
        material_type="alloy",
    ),
    "nichrome": MaterialResistance(
        name="Nichrome (Ni-Cr)",
        resistivity_20c=110.0e-8 * 1e9,
        temperature_coefficient=0.0004,
        material_type="alloy",
    ),
    "steel": MaterialResistance(
        name="Steel (carbon)",
        resistivity_20c=15.0e-8 * 1e9,
        temperature_coefficient=0.003,
        material_type="alloy",
    ),
    # Electrolytes (Arts. 365-366)
    "seawater": MaterialResistance(
        name="Seawater",
        resistivity_20c=20.0,  # ~20 abohm·cm (0.2 ohm·m)
        temperature_coefficient=-0.02,  # Negative TCR
        material_type="electrolyte",
    ),
    "copper_sulfate": MaterialResistance(
        name="CuSO4 solution (saturated)",
        resistivity_20c=25.0,
        temperature_coefficient=-0.015,
        material_type="electrolyte",
    ),
    "sulfuric_acid": MaterialResistance(
        name="H2SO4 (30%)",
        resistivity_20c=1.5,
        temperature_coefficient=-0.012,
        material_type="electrolyte",
    ),
    "sodium_chloride": MaterialResistance(
        name="NaCl solution (1M)",
        resistivity_20c=7.5,
        temperature_coefficient=-0.02,
        material_type="electrolyte",
    ),
    # Dielectrics/Insulators (Arts. 367-368)
    "glass": MaterialResistance(
        name="Glass (Pyrex)",
        resistivity_20c=1e13,  # Very high resistivity
        temperature_coefficient=-0.05,
        material_type="dielectric",
    ),
    "mica": MaterialResistance(
        name="Mica",
        resistivity_20c=1e15,
        temperature_coefficient=-0.03,
        material_type="dielectric",
    ),
    "quartz": MaterialResistance(
        name="Quartz (fused)",
        resistivity_20c=1e17,
        temperature_coefficient=-0.02,
        material_type="dielectric",
    ),
    "rubber": MaterialResistance(
        name="Rubber",
        resistivity_20c=1e14,
        temperature_coefficient=-0.05,
        material_type="dielectric",
    ),
    "ebonite": MaterialResistance(
        name="Ebonite (hard rubber)",
        resistivity_20c=1e15,
        temperature_coefficient=-0.04,
        material_type="dielectric",
    ),
    "gutta_percha": MaterialResistance(
        name="Gutta-percha",
        resistivity_20c=1e14,
        temperature_coefficient=-0.03,
        material_type="dielectric",
    ),
    "paraffin": MaterialResistance(
        name="Paraffin wax",
        resistivity_20c=1e16,
        temperature_coefficient=-0.02,
        material_type="dielectric",
    ),
    "shellac": MaterialResistance(
        name="Shellac",
        resistivity_20c=1e14,
        temperature_coefficient=-0.04,
        material_type="dielectric",
    ),
    "air": MaterialResistance(
        name="Air (dry)",
        resistivity_20c=1e18,  # Extremely high
        temperature_coefficient=0.0,
        material_type="dielectric",
    ),
    # Semiconductors (Arts. 369-370)
    "silicon": MaterialResistance(
        name="Silicon (intrinsic)",
        resistivity_20c=2.3e5,  # High resistivity for intrinsic Si
        temperature_coefficient=-0.07,  # Negative TCR
        material_type="semiconductor",
    ),
    "germanium": MaterialResistance(
        name="Germanium (intrinsic)",
        resistivity_20c=47.0,
        temperature_coefficient=-0.05,
        material_type="semiconductor",
    ),
    "carbon": MaterialResistance(
        name="Carbon (graphite)",
        resistivity_20c=1.38e-5 * 1e9,
        temperature_coefficient=-0.0005,  # Slightly negative
        material_type="semiconductor",
    ),
    "selenium": MaterialResistance(
        name="Selenium",
        resistivity_20c=1e5,
        temperature_coefficient=-0.03,
        material_type="semiconductor",
    ),
}


def get_material_data(material_name: str) -> Optional[MaterialResistance]:
    """
    Get material resistance data from the database.

    Args:
        material_name: Name of the material.

    Returns:
        MaterialResistance object or None if not found.

    Example:
        >>> mat = get_material_data("copper")
        >>> print(f"Resistivity: {mat.resistivity} abohm·cm")
    """
    return MATERIAL_DATABASE.get(material_name.lower())


# =============================================================================
# METAL RESISTANCE (Arts. 359-362)
# =============================================================================


@maxwell_cite(
    359,
    360,
    361,
    362,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate resistivity of pure metal at given temperature",
)
def metal_resistance(
    material: str,
    temperature: float,
    reference_temperature: float = 293.15,
) -> dict[str, float]:
    """
    Calculate the resistivity of a pure metal at a given temperature.

    Arts. 359-362: Maxwell established that the resistance of pure metals
    increases linearly with temperature over a wide range:

        rho(T) = rho_0 * [1 + alpha * (T - T_0)]

    where:
        - rho_0 = resistivity at reference temperature T_0
        - alpha = temperature coefficient of resistance (TCR)
        - T = operating temperature

    For copper at 20°C: rho_0 ≈ 1.68e-8 ohm·cm, alpha ≈ 0.00393 K^-1

    Maxwell noted that the temperature coefficient is approximately the
    same for all pure metals (~0.4%/K), suggesting a universal mechanism.

    Args:
        material: Name of the metal (e.g., "copper", "silver", "gold").
        temperature: Operating temperature T (Kelvin).
        reference_temperature: Reference temperature T_0 (default: 293.15 K).

    Returns:
        Dictionary with:
        - resistivity: rho at temperature T (abohm·cm)
        - conductivity: sigma = 1/rho (siemens/cm)
        - resistivity_at_20c: rho_0 (abohm·cm)
        - temperature_coefficient: alpha (1/K)
        - temperature: T (K)
        - temperature_change: T - T_0 (K)

    Raises:
        ValueError: If material not found in database.

    References:
        Part II, Arts. 359-362: Metal resistance and temperature dependence.

    Example:
        >>> # Copper at 100°C (373.15 K)
        >>> result = metal_resistance("copper", 373.15)
        >>> print(f"rho(100°C) = {result['resistivity']:.2e} abohm·cm")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    if material_data.material_type not in ["metal"]:
        # Allow some flexibility for close materials
        if material_data.material_type == "alloy":
            pass  # Can use this function for alloys too
        else:
            raise ValueError(f"Material '{material}' is not a pure metal")

    rho_0 = material_data.resistivity_20c
    alpha = material_data.temperature_coefficient

    # Linear temperature dependence
    delta_T = temperature - reference_temperature
    resistivity = rho_0 * (1 + alpha * delta_T)
    conductivity = 1.0 / resistivity if resistivity > 0 else float("inf")

    return {
        "resistivity": resistivity,
        "conductivity": conductivity,
        "resistivity_at_20c": rho_0,
        "conductivity_at_20c": 1.0 / rho_0 if rho_0 > 0 else float("inf"),
        "temperature_coefficient": alpha,
        "temperature": temperature,
        "reference_temperature": reference_temperature,
        "temperature_change": delta_T,
        "material": material_data.name,
        "material_type": material_data.material_type,
    }


@maxwell_cite(
    359,
    360,
    361,
    362,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate temperature coefficient dR/dT for metals",
)
def temperature_coefficient(
    material: str,
    temperature: float = 293.15,
) -> dict[str, float]:
    """
    Calculate the temperature coefficient of resistance (dR/dT) for a metal.

    Arts. 359-362: Maxwell measured the temperature coefficient alpha = (1/R) * dR/dT
    for various metals. This coefficient represents the fractional change in
    resistance per degree of temperature change.

    For pure metals, alpha is approximately:

        alpha ≈ 0.004 K^-1 = 0.4% per Kelvin

    at room temperature. This corresponds to a resistance increase of about
    4% for every 10°C rise.

    The temperature coefficient itself varies with temperature:

        alpha(T) = alpha_0 / [1 + alpha_0 * (T - T_0)]

    Args:
        material: Name of the metal.
        temperature: Temperature at which to evaluate alpha (K).

    Returns:
        Dictionary with:
        - alpha: Temperature coefficient at T (1/K)
        - alpha_20c: Reference value at 20°C
        - d_rho_dT: Absolute rate of change d(rho)/dT (abohm·cm/K)
        - percent_change_per_K: alpha * 100 (%/K)
        - percent_change_per_10C: alpha * 10 * 100 (% per 10°C)

    Raises:
        ValueError: If material not found.

    References:
        Part II, Arts. 359-362: Temperature coefficient measurements.

    Example:
        >>> # Copper temperature coefficient
        >>> result = temperature_coefficient("copper")
        >>> print(f"alpha = {result['alpha']:.5f} 1/K")
        >>> print(f"Change per 10°C = {result['percent_change_per_10C']:.2f}%")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    alpha_0 = material_data.temperature_coefficient
    rho_0 = material_data.resistivity_20c
    T_0 = 293.15  # 20°C

    # Temperature dependence of alpha
    delta_T = temperature - T_0
    alpha = (
        alpha_0 / (1 + alpha_0 * delta_T) if (1 + alpha_0 * delta_T) > 0 else alpha_0
    )

    # Absolute rate of change: d(rho)/dT = alpha * rho
    rho_at_T = rho_0 * (1 + alpha_0 * delta_T)
    d_rho_dT = alpha * rho_at_T

    return {
        "alpha": alpha,
        "alpha_20c": alpha_0,
        "d_rho_dT": d_rho_dT,
        "percent_change_per_K": alpha * 100,
        "percent_change_per_10C": alpha * 10 * 100,
        "temperature": temperature,
        "material": material_data.name,
    }


# =============================================================================
# ALLOY RESISTANCE (Arts. 363-364)
# =============================================================================


@maxwell_cite(
    363,
    364,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate resistivity of alloy at given temperature",
)
def alloy_resistance(
    material: str,
    temperature: float,
    reference_temperature: float = 293.15,
) -> dict[str, float]:
    """
    Calculate the resistivity of an alloy at a given temperature.

    Arts. 363-364: Maxwell observed that alloys generally have:
    1. Higher resistivity than their constituent pure metals
    2. Lower temperature coefficients than pure metals
    3. More complex composition dependence

    Matthiessen's rule for alloys states that the total resistivity is:

        rho_total = rho_thermal + rho_residual

    where:
        - rho_thermal = temperature-dependent part (phonon scattering)
        - rho_residual = temperature-independent part (impurity scattering)

    For alloys, rho_residual dominates, giving:
        - Higher overall resistivity
        - Lower temperature coefficient

    Some alloys (constantan, manganin) have nearly zero TCR, making them
    ideal for precision resistors.

    Args:
        material: Name of the alloy (e.g., "brass", "constantan", "nichrome").
        temperature: Operating temperature (K).
        reference_temperature: Reference temperature (default: 293.15 K).

    Returns:
        Dictionary with:
        - resistivity: rho at temperature T (abohm·cm)
        - conductivity: sigma = 1/rho (siemens/cm)
        - temperature_coefficient: alpha (1/K)
        - temperature: T (K)

    Raises:
        ValueError: If material not found or not an alloy.

    References:
        Part II, Arts. 363-364: Alloy resistance and Matthiessen's rule.

    Example:
        >>> # Constantan at 100°C
        >>> result = alloy_resistance("constantan", 373.15)
        >>> print(f"rho = {result['resistivity']:.2e} abohm·cm")
        >>> print(f"alpha = {result['temperature_coefficient']:.5f} 1/K")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    if material_data.material_type not in ["alloy", "metal"]:
        raise ValueError(f"Material '{material}' is not an alloy")

    rho_0 = material_data.resistivity_20c
    alpha = material_data.temperature_coefficient

    # Temperature dependence (linear approximation)
    delta_T = temperature - reference_temperature
    resistivity = rho_0 * (1 + alpha * delta_T)
    conductivity = 1.0 / resistivity if resistivity > 0 else float("inf")

    return {
        "resistivity": resistivity,
        "conductivity": conductivity,
        "resistivity_at_20c": rho_0,
        "temperature_coefficient": alpha,
        "temperature": temperature,
        "reference_temperature": reference_temperature,
        "temperature_change": delta_T,
        "material": material_data.name,
        "material_type": material_data.material_type,
    }


@maxwell_cite(
    363,
    364,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Apply Matthiessen's rule for alloy resistivity",
)
def matthiessen_rule(
    base_metal_resistivity: float,
    impurity_concentration: float,
    residual_resistivity_factor: float = 1.0,
) -> dict[str, float]:
    """
    Apply Matthiessen's rule to estimate alloy resistivity from composition.

    Arts. 363-364: Matthiessen's rule states that the resistivity of an
    alloy is the sum of:

        rho_alloy = rho_thermal(T) + rho_residual(c)

    where:
        - rho_thermal(T) = resistivity of pure metal at temperature T
        - rho_residual(c) = residual resistivity from impurities

    For dilute alloys, the residual resistivity is proportional to
    impurity concentration:

        rho_residual = C * c

    where c is the atomic fraction of impurity and C is a constant
    depending on the impurity type.

    Args:
        base_metal_resistivity: Resistivity of the pure base metal (abohm·cm).
        impurity_concentration: Atomic fraction c of impurity (0 to 1).
        residual_resistivity_factor: C factor (typical: 1-100 for common impurities).

    Returns:
        Dictionary with:
        - residual_resistivity: rho_residual from impurities
        - total_resistivity: rho_total = rho_metal + rho_residual
        - impurity_concentration: Input concentration
        - resistivity_increase_factor: rho_total / rho_metal

    References:
        Part II, Arts. 363-364: Matthiessen's rule.

    Example:
        >>> # Copper with 1% impurity
        >>> result = matthiessen_rule(1.68, 0.01, residual_resistivity_factor=50)
        >>> print(f"rho_alloy = {result['total_resistivity']:.2f} abohm·cm")
    """
    if base_metal_resistivity <= 0:
        raise ValueError(f"base_metal_resistivity must be positive")
    if not 0 <= impurity_concentration <= 1:
        raise ValueError(f"impurity_concentration must be between 0 and 1")
    if residual_resistivity_factor < 0:
        raise ValueError(f"residual_resistivity_factor must be non-negative")

    # Residual resistivity from impurities
    residual_resistivity = residual_resistivity_factor * impurity_concentration

    # Total resistivity
    total_resistivity = base_metal_resistivity + residual_resistivity

    # Increase factor
    increase_factor = total_resistivity / base_metal_resistivity

    return {
        "residual_resistivity": residual_resistivity,
        "total_resistivity": total_resistivity,
        "base_metal_resistivity": base_metal_resistivity,
        "impurity_concentration": impurity_concentration,
        "residual_resistivity_factor": residual_resistivity_factor,
        "resistivity_increase_factor": increase_factor,
    }


# =============================================================================
# ELECTROLYTE RESISTANCE (Arts. 365-366)
# =============================================================================


@maxwell_cite(
    365,
    366,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate resistivity of electrolyte solution",
)
def electrolyte_resistance(
    concentration: float,
    temperature: float,
    electrolyte_type: str = "generic",
    reference_concentration: float = 1.0,
) -> dict[str, float]:
    """
    Calculate the resistivity of an electrolyte solution.

    Arts. 365-366: Maxwell analyzed the resistance of electrolyte solutions,
    noting that:

    1. Resistivity decreases with increasing concentration (up to a limit)
    2. Resistivity decreases with increasing temperature (negative TCR)
    3. Different ions have different mobilities

    The specific conductivity is related to concentration by:

        kappa = Lambda_m * c

    where:
        - kappa = conductivity (S/cm)
        - Lambda_m = molar conductivity (S·cm²/mol)
        - c = concentration (mol/cm³)

    For dilute solutions, Kohlrausch's law applies:

        Lambda_m = Lambda_m^0 - K * sqrt(c)

    The temperature dependence is approximately:

        kappa(T) = kappa_25 * [1 + alpha * (T - 298)]

    with alpha ≈ 0.02 K^-1 for many electrolytes.

    Args:
        concentration: Concentration c (mol/cm³ or mol/L if > 0.1).
        temperature: Temperature T (K).
        electrolyte_type: Type of electrolyte for lookup.
        reference_concentration: Reference concentration for scaling.

    Returns:
        Dictionary with:
        - resistivity: rho (abohm·cm)
        - conductivity: kappa (siemens/cm)
        - molar_conductivity: Lambda_m (S·cm²/mol)
        - temperature_coefficient: alpha (1/K)
        - temperature: T (K)

    References:
        Part II, Arts. 365-366: Electrolyte resistance.

    Example:
        >>> # NaCl solution at 0.1 M, 25°C
        >>> result = electrolyte_resistance(0.1, 298.15, "nacl")
        >>> print(f"kappa = {result['conductivity']:.4f} S/cm")
    """
    # Reference molar conductivities at infinite dilution (S·cm²/mol)
    # Converted to CGS-EMU: 1 S·cm²/mol = 1e8 abS·cm²/mol
    molar_conductivities = {
        "kcl": 149.9 * 1e8,  # KCl
        "nacl": 126.4 * 1e8,  # NaCl
        "hcl": 426.2 * 1e8,  # HCl
        "cuso4": 133.0 * 1e8,  # CuSO4
        "h2so4": 859.0 * 1e8,  # H2SO4 (diprotic)
        "generic": 100.0 * 1e8,  # Generic
    }

    # Temperature coefficients
    temp_coeffs = {
        "kcl": 0.019,
        "nacl": 0.020,
        "hcl": 0.015,
        "cuso4": 0.018,
        "h2so4": 0.012,
        "generic": 0.02,
    }

    # Get parameters
    electrolyte_key = electrolyte_type.lower() if electrolyte_type else "generic"
    Lambda_0 = molar_conductivities.get(
        electrolyte_key, molar_conductivities["generic"]
    )
    alpha = temp_coeffs.get(electrolyte_key, 0.02)

    # Adjust concentration units (assume mol/L if > 0.1)
    if concentration > 0.1:
        concentration = concentration / 1000  # Convert to mol/cm³

    # Kohlrausch correction for concentration (simplified)
    # Lambda_m = Lambda_0 * (1 - k * sqrt(c))
    kohlrausch_k = 0.1  # Approximate constant
    Lambda_m = Lambda_0 * (1 - kohlrausch_k * np.sqrt(concentration))

    # Conductivity
    kappa = Lambda_m * concentration

    # Temperature correction
    T_ref = 298.15
    delta_T = temperature - T_ref
    kappa_T = kappa * (1 + alpha * delta_T)

    # Resistivity
    resistivity = 1.0 / kappa_T if kappa_T > 0 else float("inf")

    return {
        "resistivity": resistivity,
        "conductivity": kappa_T,
        "molar_conductivity": Lambda_m,
        "concentration": concentration,
        "temperature": temperature,
        "temperature_coefficient": alpha,
        "electrolyte_type": electrolyte_type,
        "delta_T_from_25C": delta_T,
    }


@maxwell_cite(
    365,
    366,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate concentration dependence of electrolyte conductivity",
)
def electrolyte_conductivity_vs_concentration(
    concentrations: list[float],
    electrolyte_type: str = "generic",
    temperature: float = 298.15,
) -> dict[str, list[float]]:
    """
    Calculate conductivity as a function of concentration for an electrolyte.

    Arts. 365-366: Maxwell measured the conductivity of electrolytes at
    various concentrations, establishing that:

    1. At low concentrations: conductivity increases linearly with c
    2. At high concentrations: conductivity reaches a maximum then decreases
       (due to ion-ion interactions)

    This function computes the full concentration dependence.

    Args:
        concentrations: List of concentrations to evaluate.
        electrolyte_type: Type of electrolyte.
        temperature: Temperature (K).

    Returns:
        Dictionary with:
        - concentrations: Input concentrations
        - conductivities: Computed conductivities
        - resistivities: Computed resistivities

    References:
        Part II, Arts. 365-366: Concentration dependence.

    Example:
        >>> # NaCl conductivity from 0.001 to 1 M
        >>> concs = np.logspace(-3, 0, 10)
        >>> result = electrolyte_conductivity_vs_concentration(concs, "nacl")
    """
    conductivities = []
    resistivities = []

    for c in concentrations:
        result = electrolyte_resistance(c, temperature, electrolyte_type)
        conductivities.append(result["conductivity"])
        resistivities.append(result["resistivity"])

    return {
        "concentrations": list(concentrations),
        "conductivities": conductivities,
        "resistivities": resistivities,
        "electrolyte_type": electrolyte_type,
        "temperature": temperature,
    }


# =============================================================================
# DIELECTRIC RESISTANCE (Arts. 367-368)
# =============================================================================


@maxwell_cite(
    367,
    368,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate resistivity of dielectric/insulating material",
)
def dielectric_resistance(
    material: str,
    temperature: float = 293.15,
    humidity_factor: float = 1.0,
) -> dict[str, float]:
    """
    Calculate the resistivity of a dielectric (insulating) material.

    Arts. 367-368: Maxwell recognized that even the best insulators have
    finite (though very high) resistivity. Key characteristics:

    1. Resistivity is typically 10^10 to 10^18 abohm·cm
    2. Temperature coefficient is NEGATIVE (resistivity decreases with T)
    3. Moisture dramatically reduces resistivity
    4. Surface contamination affects measurements

    The temperature dependence for dielectrics is:

        rho(T) = rho_0 * exp[E_a / (k_B * (1/T - 1/T_0))]

    where E_a is the activation energy for conduction.

    For practical purposes over limited ranges:

        rho(T) = rho_0 * exp[-beta * (T - T_0)]

    where beta ≈ 0.03-0.05 K^-1.

    Args:
        material: Name of the dielectric material.
        temperature: Temperature T (K).
        humidity_factor: Factor for moisture effect (1.0 = dry, <1.0 = humid).

    Returns:
        Dictionary with:
        - resistivity: rho at temperature T (abohm·cm)
        - conductivity: sigma = 1/rho (siemens/cm)
        - resistivity_20c: Reference value at 20°C
        - temperature: T (K)
        - humidity_factor: Input humidity factor

    Raises:
        ValueError: If material not found.

    References:
        Part II, Arts. 367-368: Dielectric resistance.

    Example:
        >>> # Glass at 50°C
        >>> result = dielectric_resistance("glass", 323.15)
        >>> print(f"rho = {result['resistivity']:.2e} abohm·cm")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    if material_data.material_type not in ["dielectric"]:
        raise ValueError(f"Material '{material}' is not a dielectric")

    rho_0 = material_data.resistivity_20c
    beta = abs(material_data.temperature_coefficient)  # Negative TCR -> positive beta

    # Exponential temperature dependence
    delta_T = temperature - 293.15
    resistivity = rho_0 * np.exp(-beta * delta_T)

    # Humidity effect (moisture reduces resistivity)
    if humidity_factor < 1.0 and humidity_factor > 0:
        resistivity = resistivity * humidity_factor

    conductivity = 1.0 / resistivity if resistivity > 0 else float("inf")

    return {
        "resistivity": resistivity,
        "conductivity": conductivity,
        "resistivity_20c": rho_0,
        "temperature": temperature,
        "humidity_factor": humidity_factor,
        "material": material_data.name,
        "material_type": material_data.material_type,
        "temperature_coefficient": material_data.temperature_coefficient,
    }


@maxwell_cite(
    367,
    368,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate surface resistivity of insulator",
)
def surface_resistivity(
    material: str,
    surface_condition: str = "clean",
    humidity: float = 0.5,
) -> dict[str, float]:
    """
    Calculate surface resistivity of a dielectric material.

    Arts. 367-368: Maxwell distinguished between VOLUME resistivity
    (through the bulk) and SURFACE resistivity (along the surface).

    Surface resistivity is typically much lower than volume resistivity
    due to:
    - Surface contamination
    - Moisture adsorption
    - Dust and dirt

    For a clean, dry surface:

        rho_surface ≈ rho_volume / (characteristic_length)

    For humid/contaminated surfaces, empirical factors apply.

    Surface resistivity is measured in ohms (or abohms) per square.

    Args:
        material: Name of the dielectric.
        surface_condition: "clean", "contaminated", or "wet".
        humidity: Relative humidity (0 to 1).

    Returns:
        Dictionary with:
        - surface_resistivity: rho_s (abohms per square)
        - volume_resistivity: rho_v for comparison
        - reduction_factor: rho_s / rho_v

    References:
        Part II, Arts. 367-368: Surface vs. volume resistance.

    Example:
        >>> # Glass surface at 50% humidity
        >>> result = surface_resistivity("glass", surface_condition="clean", humidity=0.5)
        >>> print(f"rho_surface = {result['surface_resistivity']:.2e} abohm/sq")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    rho_volume = material_data.resistivity_20c

    # Surface condition factors
    condition_factors = {
        "clean": 0.1,  # Surface resistivity ~10% of volume
        "contaminated": 0.001,  # 1000x reduction
        "wet": 0.0001,  # 10000x reduction
    }

    base_factor = condition_factors.get(surface_condition, 0.1)

    # Humidity effect
    humidity_factor = 1.0 - 0.9 * humidity  # At 100% humidity, factor = 0.1

    # Surface resistivity
    reduction_factor = base_factor * humidity_factor
    surface_resistivity = rho_volume * reduction_factor

    return {
        "surface_resistivity": surface_resistivity,
        "volume_resistivity": rho_volume,
        "reduction_factor": reduction_factor,
        "surface_condition": surface_condition,
        "humidity": humidity,
        "material": material_data.name,
    }


# =============================================================================
# SEMICONDUCTOR RESISTANCE (Arts. 369-370)
# =============================================================================


@maxwell_cite(
    369,
    370,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate resistivity of semiconductor material",
)
def semiconductor_resistance(
    material: str,
    temperature: float,
    doping_concentration: float = None,
) -> dict[str, float]:
    """
    Calculate the resistivity of a semiconductor material.

    Arts. 369-370: Maxwell made early observations of semiconductor-like
    behavior in materials such as selenium and carbon. Key characteristics:

    1. NEGATIVE temperature coefficient (resistivity decreases with T)
    2. Strong temperature dependence (exponential)
    3. Photoconductivity (Maxwell observed this in selenium)
    4. Sensitivity to impurities (doping)

    For intrinsic (pure) semiconductors:

        rho(T) = rho_0 * exp[E_g / (2 * k_B * T)]

    where E_g is the bandgap energy.

    For extrinsic (doped) semiconductors:

        rho = 1 / (q * n * mu_n + q * p * mu_p)

    where n, p are carrier concentrations and mu are mobilities.

    Args:
        material: Name of the semiconductor.
        temperature: Temperature T (K).
        doping_concentration: Optional doping level (carriers/cm³).

    Returns:
        Dictionary with:
        - resistivity: rho at temperature T (abohm·cm)
        - conductivity: sigma = 1/rho (siemens/cm)
        - temperature: T (K)
        - temperature_coefficient: alpha (negative for semiconductors)
        - material_type: "intrinsic" or "extrinsic"

    Raises:
        ValueError: If material not found.

    References:
        Part II, Arts. 369-370: Semiconductor observations.

    Example:
        >>> # Silicon at 50°C
        >>> result = semiconductor_resistance("silicon", 323.15)
        >>> print(f"rho = {result['resistivity']:.2e} abohm·cm")
    """
    material_data = get_material_data(material)

    if material_data is None:
        raise ValueError(f"Material '{material}' not found in database")

    rho_0 = material_data.resistivity_20c
    T_0 = 293.15

    # Semiconductor parameters (approximate)
    bandgaps = {
        "silicon": 1.12,  # eV
        "germanium": 0.67,
        "selenium": 1.8,
        "carbon": 0.0,  # Semimetal
    }

    E_g = bandgaps.get(material.lower(), 1.0)  # Default 1 eV

    # Convert to CGS: 1 eV = 1.602e-12 erg
    # k_B = 1.38e-16 erg/K
    # E_g / (2*k_B) has units of K
    E_g_erg = E_g * 1.602e-12
    k_B = 1.380649e-16
    characteristic_temp = E_g_erg / (2 * k_B)

    # Intrinsic semiconductor: rho ~ exp(E_g / 2kT)
    if doping_concentration is None:
        # Intrinsic behavior
        resistivity = rho_0 * np.exp(characteristic_temp * (1 / temperature - 1 / T_0))
        material_type = "intrinsic"
    else:
        # Extrinsic (doped) - simplified model
        # rho = 1 / (q * n * mu)
        q = 4.803e-10  # Elementary charge in esu ≈ 1.602e-20 abC
        n = doping_concentration  # Assume n-type for simplicity
        mu = 1000  # Approximate mobility cm²/(V·s)

        conductivity_extrinsic = q * n * mu * 1e8  # Convert to CGS-EMU
        resistivity = 1.0 / conductivity_extrinsic
        material_type = "extrinsic"

    conductivity = 1.0 / resistivity if resistivity > 0 else float("inf")

    # Temperature coefficient (negative!)
    alpha = -characteristic_temp / (temperature**2)

    return {
        "resistivity": resistivity,
        "conductivity": conductivity,
        "temperature": temperature,
        "temperature_coefficient": alpha,
        "material": material_data.name,
        "material_type": material_type,
        "bandgap_ev": E_g,
        "doping_concentration": doping_concentration,
    }


@maxwell_cite(
    369,
    370,
    part=2,
    chapter="Resistance of Substances",
    theory_class="maxwell_original",
    description="Calculate photoconductivity effect in selenium",
)
def photoconductivity(
    material: str,
    dark_resistivity: float,
    illumination: float,
    wavelength: float = 550,
) -> dict[str, float]:
    """
    Calculate the change in resistivity due to illumination (photoconductivity).

    Arts. 369-370: Maxwell observed that selenium becomes more conductive
    when exposed to light - the phenomenon of photoconductivity. This was
    one of the first observations of semiconductor optoelectronic behavior.

    The photoconductivity is:

        delta_sigma = eta * q * G * tau

    where:
        - eta = quantum efficiency
        - G = photon flux (photons/cm²/s)
        - tau = carrier lifetime

    For moderate illumination:

        rho_light = rho_dark / (1 + beta * I)

    where I is the light intensity and beta is the photoconductive gain.

    Args:
        material: Name of the photoconductive material.
        dark_resistivity: Resistivity in the dark (abohm·cm).
        illumination: Light intensity (arbitrary units, 0-1 for normalization).
        wavelength: Wavelength of light (nm, default: 550 nm green).

    Returns:
        Dictionary with:
        - resistivity_light: rho under illumination
        - resistivity_dark: rho in dark
        - photoconductivity: delta_sigma
        - reduction_factor: rho_light / rho_dark

    References:
        Part II, Arts. 369-370: Photoconductivity of selenium.

    Example:
        >>> # Selenium under illumination
        >>> result = photoconductivity("selenium", 1e5, illumination=0.5)
        >>> print(f"rho_light = {result['resistivity_light']:.2e} abohm·cm")
    """
    if dark_resistivity <= 0:
        raise ValueError(f"dark_resistivity must be positive")
    if illumination < 0:
        raise ValueError(f"illumination must be non-negative")

    # Photoconductive gain factor (material dependent)
    gains = {
        "selenium": 0.8,  # High photoconductive response
        "silicon": 0.5,
        "germanium": 0.6,
    }

    beta = gains.get(material.lower(), 0.5)

    # Wavelength dependence (peak response)
    peak_wavelengths = {
        "selenium": 500,  # Green
        "silicon": 800,  # Near IR
        "germanium": 1500,  # IR
    }

    peak = peak_wavelengths.get(material.lower(), 550)
    wavelength_factor = np.exp(-(((wavelength - peak) / 100) ** 2))

    # Photoconductivity
    effective_illumination = illumination * wavelength_factor
    reduction_factor = 1.0 / (1 + beta * effective_illumination)

    resistivity_light = dark_resistivity * reduction_factor
    photoconductivity = 1.0 / resistivity_light - 1.0 / dark_resistivity

    return {
        "resistivity_light": resistivity_light,
        "resistivity_dark": dark_resistivity,
        "photoconductivity": photoconductivity,
        "reduction_factor": reduction_factor,
        "illumination": illumination,
        "wavelength": wavelength,
        "material": material,
    }


# =============================================================================
# RESISTANCE SUBSTANCES ANALYZER CLASS
# =============================================================================


@dataclass
class ResistanceSubstancesAnalyzer:
    """
    Comprehensive analyzer for resistance of substances.

    This class provides methods for analyzing:
    - Metal and alloy resistance
    - Electrolyte conductivity
    - Dielectric insulation
    - Semiconductor behavior

    Attributes:
        reference_temperature: Reference temperature for calculations (K).
    """

    reference_temperature: float = 293.15

    @maxwell_cite(
        359,
        360,
        361,
        362,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Analyze metal resistance at temperature",
    )
    def analyze_metal(self, material: str, temperature: float) -> dict:
        """Analyze metal resistance."""
        return metal_resistance(material, temperature, self.reference_temperature)

    @maxwell_cite(
        363,
        364,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Analyze alloy resistance",
    )
    def analyze_alloy(self, material: str, temperature: float) -> dict:
        """Analyze alloy resistance."""
        return alloy_resistance(material, temperature, self.reference_temperature)

    @maxwell_cite(
        365,
        366,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Analyze electrolyte resistance",
    )
    def analyze_electrolyte(
        self,
        concentration: float,
        temperature: float,
        electrolyte_type: str = "generic",
    ) -> dict:
        """Analyze electrolyte resistance."""
        return electrolyte_resistance(concentration, temperature, electrolyte_type)

    @maxwell_cite(
        367,
        368,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Analyze dielectric resistance",
    )
    def analyze_dielectric(
        self,
        material: str,
        temperature: float,
        humidity_factor: float = 1.0,
    ) -> dict:
        """Analyze dielectric resistance."""
        return dielectric_resistance(material, temperature, humidity_factor)

    @maxwell_cite(
        369,
        370,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Analyze semiconductor resistance",
    )
    def analyze_semiconductor(
        self,
        material: str,
        temperature: float,
        doping_concentration: float = None,
    ) -> dict:
        """Analyze semiconductor resistance."""
        return semiconductor_resistance(material, temperature, doping_concentration)

    @maxwell_cite(
        359,
        360,
        361,
        362,
        part=2,
        chapter="Resistance of Substances",
        theory_class="maxwell_original",
        description="Get material data from database",
    )
    def get_material(self, material_name: str) -> Optional[MaterialResistance]:
        """Get material data from database."""
        return get_material_data(material_name)


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RESISTANCE OF SUBSTANCES")
    print("Maxwell's Treatise, Part II, Chapter XII (Arts. 359-370)")
    print("=" * 70)

    # Test metal resistance
    print("\n--- Metal Resistance (Arts. 359-362) ---")
    result = metal_resistance("copper", 373.15)
    print(f"  Copper at 100°C:")
    print(f"    rho = {result['resistivity']:.2e} abohm·cm")
    print(f"    sigma = {result['conductivity']:.2e} S/cm")
    print(f"    Change from 20°C = {result['temperature_change']:.1f} K")

    # Test temperature coefficient
    print("\n--- Temperature Coefficient (Arts. 359-362) ---")
    result = temperature_coefficient("copper")
    print(f"  Copper at 20°C:")
    print(f"    alpha = {result['alpha']:.5f} 1/K")
    print(f"    % change per 10°C = {result['percent_change_per_10C']:.2f}%")

    # Test alloy resistance
    print("\n--- Alloy Resistance (Arts. 363-364) ---")
    result = alloy_resistance("constantan", 373.15)
    print(f"  Constantan at 100°C:")
    print(f"    rho = {result['resistivity']:.2e} abohm·cm")
    print(f"    alpha = {result['temperature_coefficient']:.5f} 1/K")

    # Test Matthiessen's rule
    print("\n--- Matthiessen's Rule (Arts. 363-364) ---")
    result = matthiessen_rule(1.68, 0.01, residual_resistivity_factor=50)
    print(f"  Copper with 1% impurity:")
    print(f"    rho_alloy = {result['total_resistivity']:.2f} abohm·cm")
    print(f"    Increase factor = {result['resistivity_increase_factor']:.2f}x")

    # Test electrolyte resistance
    print("\n--- Electrolyte Resistance (Arts. 365-366) ---")
    result = electrolyte_resistance(0.1, 298.15, "nacl")
    print(f"  NaCl 0.1M at 25°C:")
    print(f"    kappa = {result['conductivity']:.4f} S/cm")
    print(f"    rho = {result['resistivity']:.2f} abohm·cm")

    # Test dielectric resistance
    print("\n--- Dielectric Resistance (Arts. 367-368) ---")
    result = dielectric_resistance("glass", 323.15)
    print(f"  Glass at 50°C:")
    print(f"    rho = {result['resistivity']:.2e} abohm·cm")

    # Test surface resistivity
    print("\n--- Surface Resistivity (Arts. 367-368) ---")
    result = surface_resistivity("glass", surface_condition="clean", humidity=0.5)
    print(f"  Glass surface (clean, 50% RH):")
    print(f"    rho_surface = {result['surface_resistivity']:.2e} abohm/sq")

    # Test semiconductor resistance
    print("\n--- Semiconductor Resistance (Arts. 369-370) ---")
    result = semiconductor_resistance("silicon", 323.15)
    print(f"  Silicon at 50°C:")
    print(f"    rho = {result['resistivity']:.2e} abohm·cm")
    print(f"    alpha = {result['temperature_coefficient']:.4f} 1/K")

    # Test photoconductivity
    print("\n--- Photoconductivity (Arts. 369-370) ---")
    result = photoconductivity("selenium", 1e5, illumination=0.5)
    print(f"  Selenium under illumination:")
    print(f"    rho_dark = {result['resistivity_dark']:.2e} abohm·cm")
    print(f"    rho_light = {result['resistivity_light']:.2e} abohm·cm")
    print(f"    Reduction factor = {result['reduction_factor']:.3f}")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)
