"""
Universal constants for Maxwell's Treatise implementation.

All constants are defined in CGS (centimeter-gram-second) units as primary,
with SI equivalents provided for reference. This module is the single source
of truth for all numerical constants used across Parts I–VI.

Category: C (standard_math) — Well-established physical constants.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class UniversalConstants:
    """
    Universal physical constants in CGS units.

    References:
        - Speed of light: Part IV, Ch. XX (EM theory of light), Art. 782
        - Unit ratio: Part IV, Ch. XIX (Ratio of units), Arts. 771–781
    """

    # ── Fundamental ──────────────────────────────────────────────
    #: Speed of light in vacuum (cm/s) — Art. 782
    C: float = 2.99792458e10

    #: Speed of light in vacuum, approximate (cm/s) — Maxwell's value ~3e10
    C_APPROX: float = 3.0e10

    # ── CGS electromagnetic units ────────────────────────────────
    #: Vacuum permeability (EMU, dimensionless in CGS-EMU)
    MU0_EMU: float = 1.0

    #: Vacuum permittivity (EMU) = 1/c^2
    EPS0_EMU: float = 1.0 / C ** 2

    #: Vacuum permittivity (ESU, dimensionless in CGS-ESU)
    EPS0_ESU: float = 1.0

    #: Vacuum permeability (ESU) = c^2
    MU0_ESU: float = C ** 2

    # ── Electron (CGS) ──────────────────────────────────────────
    #: Elementary charge (esu, statcoulombs)
    E_CHARGE_ESU: float = 4.8032047e-10

    #: Elementary charge (emu, abCoulombs)
    E_CHARGE_EMU: float = 1.602176634e-20

    #: Electron mass (g)
    ELECTRON_MASS: float = 9.1093837e-28

    # ── Conversion factors ───────────────────────────────────────
    #: 1 volt = 10^8 abV = 10^8 / c statV
    VOLT_TO_STATVOLT: float = 1.0 / 299.792458

    #: 1 ampere = 0.1 abA = c / 10^9 statA
    AMPERE_TO_STATAMPERE: float = 2.99792458e9

    #: 1 ohm = 10^9 / c^2 statohm ≈ 1.11e-12
    OHM_TO_STATOHM: float = 1.0e9 / C ** 2

    #: 1 Tesla = 10^4 Gauss
    TESLA_TO_GAUSS: float = 1.0e4

    # ── SI reference (not used internally, for output only) ──────
    #: Vacuum permeability SI (H/m)
    MU0_SI: float = 1.25663706212e-6

    #: Vacuum permittivity SI (F/m)
    EPS0_SI: float = 8.8541878128e-12

    #: Boltzmann constant (erg/K) — for thermoelectric calculations
    K_BOLTZMANN: float = 1.380649e-16


# Module-level convenience
C = UniversalConstants.C
"""Speed of light in vacuum (cm/s)."""

C_APPROX = UniversalConstants.C_APPROX
"""Approximate speed of light (3e10 cm/s)."""

CONST = UniversalConstants()
"""Global constants instance."""


def cgs_unit_of(quantity: str) -> str:
    """Return the CGS unit name for a physical quantity.

    Args:
        quantity: Name of the physical quantity.

    Returns:
        The CGS unit name.

    Reference:
        Part II, Ch. XI (Measurement of Resistance), Arts. 335–340.
        Part IV, Ch. XIX (Ratio of Units), Arts. 771–781.
    """
    _units = {
        "length": "cm",
        "mass": "g",
        "time": "s",
        "force": "dyne",
        "energy": "erg",
        "charge_esu": "statcoulomb (esu)",
        "charge_emu": "abcoulomb (emu)",
        "potential_esu": "statvolt",
        "potential_emu": "abvolt",
        "resistance_esu": "statohm",
        "resistance_emu": "abohm",
        "current_esu": "statampere",
        "current_emu": "abampere",
        "magnetic_field": "gauss",
        "magnetic_flux": "maxwell",
        "capacitance_esu": "centimeter",
        "capacitance_emu": "abfarad",
        "magnetic_moment": "emu (erg/gauss)",
    }
    if quantity not in _units:
        raise KeyError(f"Unknown quantity: {quantity!r}. Available: {list(_units)}")
    return _units[quantity]
