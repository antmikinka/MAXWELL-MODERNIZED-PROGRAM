"""
Measurement and Units — Part I, Chapters I and II (Arts. 2-11, 20-26).

This module implements Maxwell's treatment of:
- Measurement of physical quantities (Arts. 2-11)
- Units of electrical measurement (Arts. 20-26)

The approach follows Maxwell's rigorous method: every physical quantity
is defined by its measurement operation, and units are derived from
fundamental standards of length, mass, and time.

Category: B (user_original) — Measurement theory for Maxwell's Treatise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import Any

import numpy as np

from maxwell.config.constants import C_APPROX, CONST, C
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# PRELIMINARY — MEASUREMENT OF QUANTITIES (Arts. 2-11)
# =============================================================================


@maxwell_cite(
    2,
    3,
    4,
    part=1,
    chapter="Measurement of Quantities",
    theory_class="user_original",
    description="Principles of physical measurement — magnitude, ratio, standard.",
)
def measurement_of_quantities(
    quantity_value: float, standard_value: float
) -> dict[str, float]:
    """
    Perform measurement of a physical quantity by comparison with a standard.

    Maxwell's principle (Art. 2): Every measurement consists of determining
    the ratio of the quantity to a standard unit of the same kind.

    Args:
        quantity_value: The value of the quantity to be measured.
        standard_value: The value of the reference standard (unit).

    Returns:
        Dictionary containing:
            - 'numerical_value': The ratio quantity/standard
            - 'relative_error': Estimated relative error (based on precision)
            - 'magnitude_order': Order of magnitude (power of 10)

    Reference:
        Part I, Arts. 2-4: Principles of measurement, magnitude comparison,
        and the concept of physical quantity.
    """
    if standard_value == 0:
        raise ValueError("Standard value cannot be zero")

    numerical_value = quantity_value / standard_value
    magnitude_order = (
        np.floor(np.log10(abs(numerical_value))) if numerical_value != 0 else 0
    )

    # Estimate relative error based on numerical precision
    relative_error = np.finfo(float).eps ** 0.5  # ~1e-8 for double precision

    return {
        "numerical_value": float(numerical_value),
        "relative_error": float(relative_error),
        "magnitude_order": int(magnitude_order),
    }


@maxwell_cite(
    5,
    6,
    7,
    part=1,
    chapter="Numerical Value and Units",
    theory_class="user_original",
    description="Numerical value, unit definition, and the relation between them.",
)
def numerical_value_units(
    measured_value: float, unit_name: str, base_units: dict[str, float] | None = None
) -> dict[str, Any]:
    """
    Express a numerical value in terms of defined units.

    Maxwell (Art. 5): A measured quantity is expressed as:
        Quantity = Numerical Value x Unit

    When the unit is changed, the numerical value changes inversely.

    Args:
        measured_value: The numerical value of the measurement.
        unit_name: Name of the unit (e.g., 'cm', 'g', 's').
        base_units: Optional dict specifying fundamental unit values.
                   Default: {'L': 1.0, 'M': 1.0, 'T': 1.0} (CGS base).

    Returns:
        Dictionary containing:
            - 'value': The numerical value
            - 'unit': The unit name
            - 'dimensions': Dimensional exponents [L, M, T]
            - 'full_expression': String representation

    Reference:
        Part I, Arts. 5-7: Numerical value, unit definition, and their
        inverse relationship.
    """
    if base_units is None:
        base_units = {"L": 1.0, "M": 1.0, "T": 1.0}

    # Standard dimensional exponents for common units
    unit_dimensions = {
        "cm": {"L": 1, "M": 0, "T": 0},
        "g": {"L": 0, "M": 1, "T": 0},
        "s": {"L": 0, "M": 0, "T": 1},
        "dyne": {"L": 1, "M": 1, "T": -2},
        "erg": {"L": 2, "M": 1, "T": -2},
        "esu_charge": {"L": 1.5, "M": 0.5, "T": -1},
        "emu_charge": {"L": 0.5, "M": 0.5, "T": 0},
        "statvolt": {"L": 0.5, "M": 0.5, "T": -1},
        "abvolt": {"L": 1.5, "M": 0.5, "T": -2},
    }

    dimensions = unit_dimensions.get(unit_name, {"L": 0, "M": 0, "T": 0})

    return {
        "value": float(measured_value),
        "unit": unit_name,
        "dimensions": dimensions,
        "full_expression": f"{measured_value} {unit_name}",
    }


@maxwell_cite(
    8,
    9,
    part=1,
    chapter="Dimensional Analysis",
    theory_class="user_original",
    description="Dimensional formulas and the method of dimensions.",
)
def dimensional_analysis(
    quantity_type: str, dimensions: dict[str, float] | None = None
) -> dict[str, Any]:
    """
    Perform dimensional analysis using Maxwell's method of dimensions.

    Maxwell (Art. 8): Every derived unit can be expressed in terms of
    fundamental units [L], [M], [T] using dimensional formulae.

    The dimensional equation allows conversion between unit systems
    and verification of physical equations (Art. 9).

    Args:
        quantity_type: Name of the physical quantity (e.g., 'velocity', 'force').
        dimensions: Optional custom dimensional formula. If None, uses standard.

    Returns:
        Dictionary containing:
            - 'quantity': Name of the quantity
            - 'dimensional_formula': Dict with [L], [M], [T] exponents
            - 'dimensional_equation': String representation
            - 'homogeneity_check': Function to verify dimensional consistency

    Reference:
        Part I, Arts. 8-9: Dimensional formulas and their application
        to unit conversion and equation verification.
    """
    # Standard dimensional formulae (Maxwell's CGS system)
    standard_dimensions = {
        # Mechanical quantities
        "length": {"L": 1, "M": 0, "T": 0},
        "mass": {"L": 0, "M": 1, "T": 0},
        "time": {"L": 0, "M": 0, "T": 1},
        "velocity": {"L": 1, "M": 0, "T": -1},
        "acceleration": {"L": 1, "M": 0, "T": -2},
        "force": {"L": 1, "M": 1, "T": -2},
        "energy": {"L": 2, "M": 1, "T": -2},
        "power": {"L": 2, "M": 1, "T": -3},
        "density": {"L": -3, "M": 1, "T": 0},
        "pressure": {"L": -1, "M": 1, "T": -2},
        # Electrical quantities (ESU)
        "esu_charge": {"L": 1.5, "M": 0.5, "T": -1},
        "esu_potential": {"L": 0.5, "M": 0.5, "T": -1},
        "esu_current": {"L": 1.5, "M": 0.5, "T": -2},
        "esu_resistance": {"L": -1, "M": 1, "T": 1},
        "esu_capacitance": {"L": 1, "M": 0, "T": 0},
        # Electrical quantities (EMU)
        "emu_charge": {"L": 0.5, "M": 0.5, "T": 0},
        "emu_potential": {"L": 1.5, "M": 0.5, "T": -2},
        "emu_current": {"L": 0.5, "M": 0.5, "T": -1},
        "emu_resistance": {"L": 1, "M": 1, "T": -1},
        "emu_capacitance": {"L": -2, "M": -1, "T": 2},
        # Magnetic quantities
        "magnetic_pole": {"L": 1.5, "M": 0.5, "T": -1},
        "magnetic_field": {"L": -0.5, "M": 0.5, "T": -1},
        "magnetic_moment": {"L": 2.5, "M": 0.5, "T": -1},
        "magnetization": {"L": -0.5, "M": 0.5, "T": -1},
    }

    if dimensions is None:
        if quantity_type not in standard_dimensions:
            raise KeyError(
                f"Unknown quantity type: {quantity_type!r}. "
                f"Available: {list(standard_dimensions.keys())}"
            )
        dimensions = standard_dimensions[quantity_type]

    def dimensional_equation() -> str:
        parts = []
        for base, exp in [
            ("L", dimensions.get("L", 0)),
            ("M", dimensions.get("M", 0)),
            ("T", dimensions.get("T", 0)),
        ]:
            if exp != 0:
                if exp == 1:
                    parts.append(f"[{base}]")
                else:
                    parts.append(f"[{base}]^{exp}")
        return " ".join(parts) if parts else "[dimensionless]"

    def homogeneity_check(equation_terms: list[dict[str, float]]) -> bool:
        """
        Verify dimensional homogeneity of an equation.

        All terms must have identical dimensions for the equation
        to be physically meaningful (Art. 9).

        Args:
            equation_terms: List of dimensional formulas for each term.

        Returns:
            True if all terms are dimensionally consistent.
        """
        if not equation_terms:
            return True
        reference = equation_terms[0]
        return all(
            abs(term.get("L", 0) - reference.get("L", 0)) < 1e-10
            and abs(term.get("M", 0) - reference.get("M", 0)) < 1e-10
            and abs(term.get("T", 0) - reference.get("T", 0)) < 1e-10
            for term in equation_terms
        )

    return {
        "quantity": quantity_type,
        "dimensional_formula": dict(dimensions),
        "dimensional_equation": dimensional_equation(),
        "homogeneity_check": homogeneity_check,
    }


@maxwell_cite(
    10,
    part=1,
    chapter="Derived Units",
    theory_class="user_original",
    description="Derivation of units from fundamental standards.",
)
def derived_units(
    derived_quantity: str, fundamental_units: dict[str, float] | None = None
) -> dict[str, Any]:
    """
    Express derived units in terms of fundamental units.

    Maxwell (Art. 10): All derived units are defined by their relation
    to fundamental units through physical laws or definitions.

    Args:
        derived_quantity: Name of the derived quantity.
        fundamental_units: Optional dict of fundamental unit values.
                          Default: CGS base (cm, g, s).

    Returns:
        Dictionary containing:
            - 'quantity': Name of the derived quantity
            - 'derivation': Expression in fundamental units
            - 'dimensional_formula': [L], [M], [T] exponents
            - 'coherent_value': Value in coherent derived unit

    Reference:
        Part I, Art. 10: Derived units from fundamental standards.
    """
    if fundamental_units is None:
        fundamental_units = {"length": 1.0, "mass": 1.0, "time": 1.0}

    # Derivation rules for common quantities
    derivations = {
        "velocity": {"formula": "length / time", "dims": {"L": 1, "M": 0, "T": -1}},
        "acceleration": {
            "formula": "length / time^2",
            "dims": {"L": 1, "M": 0, "T": -2},
        },
        "force": {
            "formula": "mass * length / time^2",
            "dims": {"L": 1, "M": 1, "T": -2},
        },
        "energy": {
            "formula": "mass * length^2 / time^2",
            "dims": {"L": 2, "M": 1, "T": -2},
        },
        "power": {
            "formula": "mass * length^2 / time^3",
            "dims": {"L": 2, "M": 1, "T": -3},
        },
        "pressure": {
            "formula": "mass / (length * time^2)",
            "dims": {"L": -1, "M": 1, "T": -2},
        },
        "density": {"formula": "mass / length^3", "dims": {"L": -3, "M": 1, "T": 0}},
        "esu_charge": {
            "formula": "mass^0.5 * length^1.5 / time",
            "dims": {"L": 1.5, "M": 0.5, "T": -1},
        },
        "emu_charge": {
            "formula": "mass^0.5 * length^0.5",
            "dims": {"L": 0.5, "M": 0.5, "T": 0},
        },
        "esu_resistance": {
            "formula": "time * mass / length",
            "dims": {"L": -1, "M": 1, "T": 1},
        },
        "emu_resistance": {
            "formula": "length / time",
            "dims": {"L": 1, "M": 1, "T": -1},
        },
        "esu_capacitance": {"formula": "length", "dims": {"L": 1, "M": 0, "T": 0}},
        "emu_capacitance": {
            "formula": "time^2 / (mass * length^2)",
            "dims": {"L": -2, "M": -1, "T": 2},
        },
    }

    if derived_quantity not in derivations:
        raise KeyError(
            f"Unknown derived quantity: {derived_quantity!r}. "
            f"Available: {list(derivations.keys())}"
        )

    derivation = derivations[derived_quantity]

    return {
        "quantity": derived_quantity,
        "derivation": derivation["formula"],
        "dimensional_formula": derivation["dims"],
        "fundamental_units": fundamental_units,
    }


@maxwell_cite(
    11,
    part=1,
    chapter="Unit Conversion",
    theory_class="user_original",
    description="Conversion between different unit systems.",
)
def unit_conversion(
    value: float, from_system: str, to_system: str, quantity_type: str
) -> dict[str, float]:
    """
    Convert a value between different unit systems.

    Maxwell (Art. 11): The numerical value of a quantity changes when
    the unit is changed, inversely proportional to the unit size.

    This function handles conversions between:
    - CGS-ESU (Electrostatic Units)
    - CGS-EMU (Electromagnetic Units)
    - SI (International System)

    Args:
        value: The numerical value to convert.
        from_system: Source unit system ('esu', 'emu', 'si').
        to_system: Target unit system ('esu', 'emu', 'si').
        quantity_type: Type of quantity ('charge', 'potential', 'current',
                       'resistance', 'capacitance').

    Returns:
        Dictionary containing:
            - 'original_value': Input value
            - 'converted_value': Result of conversion
            - 'conversion_factor': Factor used
            - 'from_unit': Source unit name
            - 'to_unit': Target unit name

    Reference:
        Part I, Art. 11: Conversion between unit systems.
        Part IV, Arts. 771-781: Ratio of units (c factor).
    """
    # Unit names for each system
    unit_names = {
        "charge": {"esu": "statcoulomb", "emu": "abcoulomb", "si": "coulomb"},
        "potential": {"esu": "statvolt", "emu": "abvolt", "si": "volt"},
        "current": {"esu": "statampere", "emu": "abampere", "si": "ampere"},
        "resistance": {"esu": "statohm", "emu": "abohm", "si": "ohm"},
        "capacitance": {"esu": "cm (ESU)", "emu": "abfarad", "si": "farad"},
    }

    # Conversion factors (all relative to ESU as base)
    # The key relationship: ESU/EMU = c^n where n depends on quantity
    conversion_factors = {
        "charge": {
            "esu_to_emu": 1 / C,
            "emu_to_esu": C,
            "esu_to_si": 1 / (10 * C),
            "si_to_esu": 10 * C,
        },
        "potential": {
            "esu_to_emu": C,
            "emu_to_esu": 1 / C,
            "esu_to_si": 1 / 300,
            "si_to_esu": 300,
        },
        "current": {
            "esu_to_emu": 1 / C,
            "emu_to_esu": C,
            "esu_to_si": 1 / (10 * C),
            "si_to_esu": 10 * C,
        },
        "resistance": {
            "esu_to_emu": 1 / (C**2),
            "emu_to_esu": C**2,
            "esu_to_si": 1 / (9e11),
            "si_to_esu": 9e11,
        },
        "capacitance": {
            "esu_to_emu": 1 / (C**2),
            "emu_to_esu": C**2,
            "esu_to_si": 1 / (9e11),
            "si_to_esu": 9e11,
        },
    }

    if quantity_type not in conversion_factors:
        raise KeyError(f"Unknown quantity type: {quantity_type!r}")
    if from_system not in ["esu", "emu", "si"]:
        raise ValueError(f"Unknown source system: {from_system!r}")
    if to_system not in ["esu", "emu", "si"]:
        raise ValueError(f"Unknown target system: {to_system!r}")

    # Direct conversion
    if from_system == to_system:
        converted_value = value
        conversion_factor = 1.0
    else:
        # Convert via ESU as intermediate if needed
        key_from = f"{from_system}_to_esu" if from_system != "esu" else None
        key_to = f"esu_to_{to_system}" if to_system != "esu" else None

        if from_system == "esu":
            conversion_factor = conversion_factors[quantity_type][key_to]
            converted_value = value * conversion_factor
        elif to_system == "esu":
            conversion_factor = conversion_factors[quantity_type][key_from]
            converted_value = value * conversion_factor
        else:
            # Both non-ESU: convert source to ESU, then ESU to target
            factor_to_esu = conversion_factors[quantity_type][f"{from_system}_to_esu"]
            factor_from_esu = conversion_factors[quantity_type][f"esu_to_{to_system}"]
            conversion_factor = factor_to_esu * factor_from_esu
            converted_value = value * conversion_factor

    return {
        "original_value": float(value),
        "converted_value": float(converted_value),
        "conversion_factor": float(conversion_factor),
        "from_unit": unit_names[quantity_type][from_system],
        "to_unit": unit_names[quantity_type][to_system],
        "from_system": from_system,
        "to_system": to_system,
    }


# =============================================================================
# ELEMENTARY MATHEMATICAL THEORY — UNITS (Arts. 20-26)
# =============================================================================


@maxwell_cite(
    20,
    21,
    part=1,
    chapter="Unit of Resistance",
    theory_class="user_original",
    description="Definition and measurement of electrical resistance in CGS.",
)
def resistance_unit(resistance_value: float, system: str = "cgs") -> dict[str, Any]:
    """
    Define and convert the unit of electrical resistance.

    Maxwell (Arts. 20-21): Resistance is defined by Ohm's law as the ratio
    of electromotive force to current. In CGS-EMU, the unit resistance
    has dimensions [L][T]^-1 (velocity).

    The practical unit (Ohm) is defined as 10^9 CGS-EMU units.

    Args:
        resistance_value: Resistance value in CGS-EMU units.
        system: Target system ('cgs', 'practical', 'si').

    Returns:
        Dictionary containing:
            - 'cgs_emu_value': Value in CGS-EMU (abohm)
            - 'practical_value': Value in Ohms
            - 'cgs_esu_value': Value in CGS-ESU (statohm)
            - 'dimensions': Dimensional formula

    Reference:
        Part I, Arts. 20-21: Unit of resistance.
        Part II, Arts. 335-340: Measurement of resistance.
    """
    cgs_emu_value = resistance_value

    # 1 Ohm = 10^9 abohm (CGS-EMU)
    practical_value = resistance_value / 1e9

    # CGS-ESU: resistance has dimensions [T][L]^-1
    # Conversion: 1 statohm = c^2 abohm
    cgs_esu_value = resistance_value / (C**2)

    return {
        "cgs_emu_value": float(cgs_emu_value),
        "cgs_emu_unit": "abohm",
        "practical_value": float(practical_value),
        "practical_unit": "ohm",
        "cgs_esu_value": float(cgs_esu_value),
        "cgs_esu_unit": "statohm",
        "dimensions": {"L": 1, "M": 1, "T": -1},
        "dimensional_equation": "[L][T]^-1 (EMU) or [T][L]^-1 (ESU)",
    }


@maxwell_cite(
    22,
    23,
    part=1,
    chapter="Unit of Potential",
    theory_class="user_original",
    description="Definition of potential and electromotive force units.",
)
def potential_unit(potential_value: float, system: str = "cgs") -> dict[str, Any]:
    """
    Define and convert the unit of electric potential.

    Maxwell (Arts. 22-23): Electric potential is defined as the work
    required to move a unit charge from infinity to a point.
    Electromotive force (EMF) is measured in the same units.

    In CGS-ESU, the unit potential has dimensions [L]^[1/2][M]^[1/2][T]^-1.
    In CGS-EMU, dimensions are [L]^[3/2][M]^[1/2][T]^-2.

    Args:
        potential_value: Potential value (default: CGS-EMU abvolts).
        system: Source system ('cgs_emu', 'cgs_esu', 'practical').

    Returns:
        Dictionary containing values in all unit systems:
            - 'cgs_esu_value': Value in statvolts
            - 'cgs_emu_value': Value in abvolts
            - 'practical_value': Value in Volts
            - 'dimensions_esu': ESU dimensional formula
            - 'dimensions_emu': EMU dimensional formula

    Reference:
        Part I, Arts. 22-23: Unit of potential and electromotive force.
        Part II, Arts. 228-236: Electromotive force.
    """
    # Convert input to CGS-EMU (abvolts)
    if system == "cgs_emu":
        cgs_emu_value = potential_value
    elif system == "cgs_esu":
        # 1 statvolt = c abvolts
        cgs_emu_value = potential_value * C
    elif system == "practical":
        # 1 Volt = 10^8 abvolts
        cgs_emu_value = potential_value * 1e8
    else:
        raise ValueError(f"Unknown system: {system!r}")

    # CGS-ESU: 1 statvolt = c abvolts, so abvolts/c = statvolts
    cgs_esu_value = cgs_emu_value / C

    # Practical: 1 Volt = 10^8 abvolts
    practical_value = cgs_emu_value / 1e8

    return {
        "cgs_esu_value": float(cgs_esu_value),
        "cgs_esu_unit": "statvolt",
        "cgs_emu_value": float(cgs_emu_value),
        "cgs_emu_unit": "abvolt",
        "practical_value": float(practical_value),
        "practical_unit": "volt",
        "dimensions_esu": {"L": 0.5, "M": 0.5, "T": -1},
        "dimensions_emu": {"L": 1.5, "M": 0.5, "T": -2},
        "dimensional_equation_esu": "[L]^{1/2}[M]^{1/2}[T]^{-1}",
        "dimensional_equation_emu": "[L]^{3/2}[M]^{1/2}[T]^{-2}",
    }


@maxwell_cite(
    24,
    part=1,
    chapter="Unit of Current",
    theory_class="user_original",
    description="Definition of electrical current unit.",
)
def current_unit(current_value: float, system: str = "cgs") -> dict[str, Any]:
    """
    Define and convert the unit of electric current.

    Maxwell (Art. 24): Current strength is measured by the quantity
    of electricity passing through a section per unit time.

    The unit current produces unit magnetic effect at unit distance
    (electromagnetic definition) or transfers unit charge per unit time
    (electrostatic definition).

    Args:
        current_value: Current value (default: CGS-EMU abamperes).
        system: Source system ('cgs_emu', 'cgs_esu', 'practical').

    Returns:
        Dictionary containing:
            - 'cgs_emu_value': Value in abamperes
            - 'cgs_esu_value': Value in statamperes
            - 'practical_value': Value in Amperes
            - 'dimensions': Dimensional formula for each system

    Reference:
        Part I, Art. 24: Unit of current.
        Part II, Arts. 282-283: Current and quantity of electricity.
    """
    # Convert input to CGS-EMU (abamperes)
    if system == "cgs_emu":
        cgs_emu_value = current_value
    elif system == "cgs_esu":
        # 1 statampere = c abamperes
        cgs_emu_value = current_value * C
    elif system == "practical":
        # 1 Ampere = 0.1 abampere
        cgs_emu_value = current_value / 0.1
    else:
        raise ValueError(f"Unknown system: {system!r}")

    # CGS-ESU: 1 statampere = c abamperes
    cgs_esu_value = cgs_emu_value / C

    # Practical: 1 Ampere = 0.1 abampere
    practical_value = cgs_emu_value * 0.1

    return {
        "cgs_emu_value": float(cgs_emu_value),
        "cgs_emu_unit": "abampere",
        "cgs_esu_value": float(cgs_esu_value),
        "cgs_esu_unit": "statampere",
        "practical_value": float(practical_value),
        "practical_unit": "ampere",
        "dimensions_emu": {"L": 0.5, "M": 0.5, "T": -1},
        "dimensions_esu": {"L": 1.5, "M": 0.5, "T": -2},
        "dimensional_equation_emu": "[L]^{1/2}[M]^{1/2}[T]^{-1}",
        "dimensional_equation_esu": "[L]^{3/2}[M]^{1/2}[T]^{-2}",
    }


@maxwell_cite(
    25,
    part=1,
    chapter="Unit of Quantity",
    theory_class="user_original",
    description="Definition of quantity of electricity (charge) unit.",
)
def quantity_unit(quantity_value: float, system: str = "cgs") -> dict[str, Any]:
    """
    Define and convert the unit of quantity of electricity (charge).

    Maxwell (Art. 25): Quantity of electricity is defined as the product
    of current strength and time through which it flows.

    Q = I * t

    The unit quantity is that which passes in unit time with unit current.

    Args:
        quantity_value: Charge value (default: CGS-EMU abcoulombs).
        system: Source system ('cgs_emu', 'cgs_esu', 'practical').

    Returns:
        Dictionary containing:
            - 'cgs_emu_value': Value in abcoulombs
            - 'cgs_esu_value': Value in statcoulombs
            - 'practical_value': Value in Coulombs
            - 'dimensions': Dimensional formula

    Reference:
        Part I, Art. 25: Unit of quantity of electricity.
        Part II, Arts. 278-283: Quantity and current.
    """
    # Convert input to CGS-EMU (abcoulombs)
    if system == "cgs_emu":
        cgs_emu_value = quantity_value
    elif system == "cgs_esu":
        # 1 statcoulomb = c abcoulombs / c^2 = abcoulomb / c...
        # Actually: q_esu = c * q_emu, so q_emu = q_esu / c
        cgs_emu_value = quantity_value / C
    elif system == "practical":
        # 1 Coulomb = 0.1 abcoulomb
        cgs_emu_value = quantity_value / 0.1
    else:
        raise ValueError(f"Unknown system: {system!r}")

    # CGS-ESU: q_esu = c * q_emu
    cgs_esu_value = cgs_emu_value * C

    # Practical: 1 Coulomb = 0.1 abcoulomb
    practical_value = cgs_emu_value * 0.1

    return {
        "cgs_emu_value": float(cgs_emu_value),
        "cgs_emu_unit": "abcoulomb",
        "cgs_esu_value": float(cgs_esu_value),
        "cgs_esu_unit": "statcoulomb",
        "practical_value": float(practical_value),
        "practical_unit": "coulomb",
        "dimensions_emu": {"L": 0.5, "M": 0.5, "T": 0},
        "dimensions_esu": {"L": 1.5, "M": 0.5, "T": -1},
        "dimensional_equation_emu": "[L]^{1/2}[M]^{1/2}",
        "dimensional_equation_esu": "[L]^{3/2}[M]^{1/2}[T]^{-1}",
    }


@maxwell_cite(
    26,
    part=1,
    chapter="Unit of Capacity",
    theory_class="user_original",
    description="Definition of electrical capacity (capacitance) unit.",
)
def capacity_unit(capacity_value: float, system: str = "cgs") -> dict[str, Any]:
    """
    Define and convert the unit of electrical capacity (capacitance).

    Maxwell (Art. 26): The capacity of a conductor is the quantity
    of electricity required to raise its potential by one unit.

    C = Q / V

    In CGS-ESU, capacity has dimensions of length [L] — a conducting
    sphere of radius r has capacity r (in cm).

    Args:
        capacity_value: Capacitance value (default: CGS-ESU cm).
        system: Source system ('cgs_esu', 'cgs_emu', 'practical').

    Returns:
        Dictionary containing:
            - 'cgs_esu_value': Value in cm (ESU capacitance)
            - 'cgs_emu_value': Value in abfarads
            - 'practical_value': Value in Farads
            - 'dimensions': Dimensional formula

    Reference:
        Part I, Art. 26: Unit of capacity.
        Part II, Arts. 83-116: Capacity and induction.
    """
    # Convert input to CGS-ESU (cm)
    if system == "cgs_esu":
        cgs_esu_value = capacity_value
    elif system == "cgs_emu":
        # C_emu = C_esu / c^2, so C_esu = c^2 * C_emu
        cgs_esu_value = capacity_value * (C**2)
    elif system == "practical":
        # 1 Farad = 9e11 cm (ESU)
        cgs_esu_value = capacity_value * 9e11
    else:
        raise ValueError(f"Unknown system: {system!r}")

    # CGS-EMU: C_emu = C_esu / c^2
    cgs_emu_value = cgs_esu_value / (C**2)

    # Practical: 1 Farad = 9e11 cm (ESU) ≈ 1/(9e11) statfarads
    practical_value = cgs_esu_value / 9e11

    return {
        "cgs_esu_value": float(cgs_esu_value),
        "cgs_esu_unit": "cm (ESU capacitance)",
        "cgs_emu_value": float(cgs_emu_value),
        "cgs_emu_unit": "abfarad",
        "practical_value": float(practical_value),
        "practical_unit": "farad",
        "dimensions_esu": {"L": 1, "M": 0, "T": 0},
        "dimensions_emu": {"L": -2, "M": -1, "T": 2},
        "dimensional_equation_esu": "[L]",
        "dimensional_equation_emu": "[L]^{-2}[M]^{-1}[T]^{2}",
        "note": "In ESU, capacitance has dimensions of length — a sphere of radius r cm has capacity r cm.",
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_all_dimensional_formulae() -> dict[str, dict[str, float]]:
    """
    Get a comprehensive table of dimensional formulae.

    Returns:
        Dictionary mapping quantity names to their dimensional formulas [L], [M], [T].
    """
    return {
        # Mechanical
        "length": {"L": 1, "M": 0, "T": 0},
        "mass": {"L": 0, "M": 1, "T": 0},
        "time": {"L": 0, "M": 0, "T": 1},
        "velocity": {"L": 1, "M": 0, "T": -1},
        "acceleration": {"L": 1, "M": 0, "T": -2},
        "force": {"L": 1, "M": 1, "T": -2},
        "energy": {"L": 2, "M": 1, "T": -2},
        "power": {"L": 2, "M": 1, "T": -3},
        # Electrical ESU
        "esu_charge": {"L": 1.5, "M": 0.5, "T": -1},
        "esu_potential": {"L": 0.5, "M": 0.5, "T": -1},
        "esu_current": {"L": 1.5, "M": 0.5, "T": -2},
        "esu_resistance": {"L": -1, "M": 1, "T": 1},
        "esu_capacitance": {"L": 1, "M": 0, "T": 0},
        # Electrical EMU
        "emu_charge": {"L": 0.5, "M": 0.5, "T": 0},
        "emu_potential": {"L": 1.5, "M": 0.5, "T": -2},
        "emu_current": {"L": 0.5, "M": 0.5, "T": -1},
        "emu_resistance": {"L": 1, "M": 1, "T": -1},
        "emu_capacitance": {"L": -2, "M": -1, "T": 2},
        # Magnetic
        "magnetic_pole": {"L": 1.5, "M": 0.5, "T": -1},
        "magnetic_field": {"L": -0.5, "M": 0.5, "T": -1},
        "magnetic_moment": {"L": 2.5, "M": 0.5, "T": -1},
        "magnetization": {"L": -0.5, "M": 0.5, "T": -1},
    }


def verify_dimensional_homogeneity(terms: list[dict[str, float]]) -> tuple[bool, str]:
    """
    Verify that all terms in an equation have the same dimensions.

    Maxwell's principle (Art. 9): A physical equation must be
    dimensionally homogeneous — all terms added or equated must
    have identical dimensional formulas.

    Args:
        terms: List of dimensional formulas for each term.

    Returns:
        Tuple of (is_homogeneous, message).
    """
    if len(terms) < 2:
        return True, "Single term — trivially homogeneous"

    reference = terms[0]
    for i, term in enumerate(terms[1:], 1):
        for dim in ["L", "M", "T"]:
            if abs(term.get(dim, 0) - reference.get(dim, 0)) > 1e-10:
                return (
                    False,
                    f"Term {i} differs in [{dim}]: expected {reference.get(dim, 0)}, got {term.get(dim, 0)}",
                )

    return True, "All terms are dimensionally consistent"
