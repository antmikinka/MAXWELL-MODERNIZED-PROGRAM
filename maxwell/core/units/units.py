"""
Unit systems and dimensional analysis for Maxwell's Treatise.

Implements the conversion between Electrostatic Units (ESU) and
Electromagnetic Units (EMU), following Maxwell's treatment in
Part II, Chapter XI (Arts. 335–340) and Part IV, Chapter XIX (Arts. 771–781).

The fundamental relationship: the ratio of ESU to EMU units equals c,
the speed of light — the key discovery that led to the electromagnetic
theory of light (Part IV, Chapter XX).

Category: C (standard_math) — CGS unit conventions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from maxwell.config.constants import C_APPROX, CONST, C


@dataclass(frozen=True)
class CGSUnitConverter:
    """
    Converter between CGS-ESU and CGS-EMU unit systems.

    Maxwell's notation:
        ESU quantities use Greek letters (E, D, rho)
        EMU quantities use Gothic letters (mathfrak{E}, mathfrak{B}, mathfrak{C})

    The ratio ESU/EMU = c for each dimensional quantity.

    References:
        Part II, Art. 337: Electromagnetic system of units.
        Part IV, Arts. 771–781: Ratio of units (v = c).
    """

    c: float = field(default=C, repr=False)

    # ── Charge ───────────────────────────────────────────────────
    def esu_to_emu_charge(self, q_esu: float) -> float:
        """Convert charge from ESU (statcoulomb) to EMU (abcoulomb).

        q_emu = q_esu / c

        Art. 773: The ratio of the electromagnetic to the electrostatic
        unit of quantity is equal to the velocity of light.
        """
        return q_esu / self.c

    def emu_to_esu_charge(self, q_emu: float) -> float:
        """Convert charge from EMU to ESU.

        q_esu = q_emu * c
        """
        return q_emu * self.c

    # ── Potential ────────────────────────────────────────────────
    def esu_to_emu_potential(self, v_esu: float) -> float:
        """Convert potential from ESU (statvolt) to EMU (abvolt).

        v_emu = v_esu * c
        """
        return v_esu * self.c

    def emu_to_esu_potential(self, v_emu: float) -> float:
        """Convert potential from EMU to ESU.

        v_esu = v_emu / c
        """
        return v_emu / self.c

    # ── Resistance ───────────────────────────────────────────────
    def esu_to_emu_resistance(self, r_esu: float) -> float:
        """Convert resistance from ESU (statohm) to EMU (abohm).

        r_emu = r_esu / c^2
        """
        return r_esu / self.c**2

    def emu_to_esu_resistance(self, r_emu: float) -> float:
        """Convert resistance from EMU to ESU.

        r_esu = r_emu * c^2
        """
        return r_emu * self.c**2

    # ── Current ──────────────────────────────────────────────────
    def esu_to_emu_current(self, i_esu: float) -> float:
        """Convert current from ESU to EMU.

        i_emu = i_esu / c
        """
        return i_esu / self.c

    def emu_to_esu_current(self, i_emu: float) -> float:
        """Convert current from EMU to ESU.

        i_esu = i_emu * c
        """
        return i_emu * self.c

    # ── Capacitance ──────────────────────────────────────────────
    def esu_to_emu_capacitance(self, c_esu: float) -> float:
        """Convert capacitance. ESU unit is cm; EMU unit is abfarad.

        c_emu = c_esu / c^2
        """
        return c_esu / self.c**2

    # ── Magnetic field ───────────────────────────────────────────
    def magnetic_field_to_induction(
        self, H: float, magnetization: float = 0.0
    ) -> float:
        """Convert magnetic force H to magnetic induction B.

        B = H + 4*pi*I  (Art. 400)

        Args:
            H: Magnetic force (oersted).
            magnetization: Intensity of magnetization I.

        Returns:
            Magnetic induction B (gauss).

        Reference:
            Part III, Art. 400: Relation between magnetic force,
            magnetic induction, and magnetization.
        """
        import math

        return H + 4.0 * math.pi * magnetization


@dataclass
class MagneticDimensions:
    """
    Dimensional formulae for magnetic quantities.

    Art. 374: Definition of magnetic units and their dimensions.

    The unit magnetic pole is defined such that two unit poles
    at unit distance repel with unit force: f = m1*m2/r^2.

    Therefore: [m] = [L^{3/2} M^{1/2} T^{-1}]

    References:
        Part III, Art. 374: Definition of magnetic units and dimensions.
        Part II, Art. 278: Dimensions of quantities in Ohm's law.
    """

    #: Dimensions of magnetic pole strength: [L^{3/2} M^{1/2} T^{-1}]
    POLE_STRENGTH: ClassVar[dict[str, float]] = {"L": 1.5, "M": 0.5, "T": -1.0}

    #: Dimensions of magnetic force H: [L^{-1/2} M^{1/2} T^{-1}]
    MAGNETIC_FORCE: ClassVar[dict[str, float]] = {"L": -0.5, "M": 0.5, "T": -1.0}

    #: Dimensions of magnetic induction B: same as H in CGS
    MAGNETIC_INDUCTION: ClassVar[dict[str, float]] = {"L": -0.5, "M": 0.5, "T": -1.0}

    #: Dimensions of magnetic moment: [L^{5/2} M^{1/2} T^{-1}]
    MAGNETIC_MOMENT: ClassVar[dict[str, float]] = {"L": 2.5, "M": 0.5, "T": -1.0}

    #: Dimensions of magnetization I: [L^{-1/2} M^{1/2} T^{-1}]
    MAGNETIZATION: ClassVar[dict[str, float]] = {"L": -0.5, "M": 0.5, "T": -1.0}

    @classmethod
    def verify_dimensions(cls, quantity: str, dims: dict[str, float]) -> bool:
        """Verify dimensional formula against standard.

        Args:
            quantity: Name of the magnetic quantity.
            dims: Dimensional formula to verify.

        Returns:
            True if dimensions match the standard.
        """
        standard = {
            "pole_strength": cls.POLE_STRENGTH,
            "magnetic_force": cls.MAGNETIC_FORCE,
            "magnetic_induction": cls.MAGNETIC_INDUCTION,
            "magnetic_moment": cls.MAGNETIC_MOMENT,
            "magnetization": cls.MAGNETIZATION,
        }
        if quantity not in standard:
            raise KeyError(f"Unknown quantity: {quantity!r}")
        return all(
            abs(dims.get(d, 0.0) - v) < 1e-10 for d, v in standard[quantity].items()
        )


CONVERTER = CGSUnitConverter()
"""Global unit converter instance."""
