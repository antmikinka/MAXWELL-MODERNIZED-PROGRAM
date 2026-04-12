"""maxwell.instruments.suspended_coil — Suspended coil instruments (Arts. 721-724, 728-729).

Thomson's sensitive suspended coil, mode of suspension,
and determination of magnetic force by suspended coil method.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class SuspendedCoil:
    """Base suspended coil instrument (Arts. 721-722).

    A coil suspended by a fine wire or fiber, free to rotate
    in a magnetic field. The torque on the coil is proportional
    to the current and the field strength.

    Attributes:
        n_turns: Number of turns in suspended coil.
        area: Area of the coil (cm^2).
        torsion_constant: Torsional constant of suspension fiber.
        horizontal_field: External horizontal magnetic field.
    """

    n_turns: int
    area: float  # cm^2
    torsion_constant: float
    horizontal_field: float

    @maxwell_cite(721, part=4, theory_class="standard_math")
    def magnetic_moment(self, current: float) -> float:
        """Calculate magnetic moment of the suspended coil.

        mu = n * I * A

        Args:
            current: Current through coil (abamperes).

        Returns:
            Magnetic moment (emu).
        """
        return self.n_turns * current * self.area

    @maxwell_cite(721, part=4, theory_class="standard_math")
    def torque(self, current: float, theta: float) -> float:
        """Calculate torque on suspended coil.

        tau = n*I*A*H*sin(theta) - k*theta

        Args:
            current: Current through coil (abamperes).
            theta: Angular deflection (radians).

        Returns:
            Net torque (dyne-cm).
        """
        magnetic = self.magnetic_moment(current) * self.horizontal_field * np.sin(theta)
        restoring = -self.torsion_constant * theta
        return magnetic + restoring

    @maxwell_cite(721, part=4, theory_class="standard_math")
    def equilibrium_deflection(self, current: float) -> float:
        """Find equilibrium deflection angle for given current.

        At equilibrium: n*I*A*H*sin(theta) = k*theta
        For small angles: theta = n*I*A*H / k

        Args:
            current: Current through coil (abamperes).

        Returns:
            Equilibrium angle in radians.
        """
        mu = self.magnetic_moment(current)
        # Small angle approximation: sin(theta) ~ theta
        return mu * self.horizontal_field / self.torsion_constant


@dataclass
class ThomsonSensitiveCoil:
    """Thomson's sensitive suspended coil (Art. 722).

    Thomson's design uses a long, narrow coil suspended in
    a strong magnetic field for maximum sensitivity to
    small currents.

    Attributes:
        n_turns: Number of turns.
        coil_length: Length of the coil (cm).
        coil_width: Width of the coil (cm).
        field_strength: Magnetic field strength (oersted).
        torsion_constant: Torsional constant of suspension.
    """

    n_turns: int
    coil_length: float
    coil_width: float
    field_strength: float
    torsion_constant: float

    @property
    def area(self) -> float:
        """Coil area in cm^2."""
        return self.coil_length * self.coil_width

    @maxwell_cite(722, part=4, theory_class="standard_math")
    def sensitivity(self) -> float:
        """Current sensitivity (radians per abampere).

        d(theta)/dI = n*A*H / k  (small angle)
        """
        return self.n_turns * self.area * self.field_strength / self.torsion_constant

    @maxwell_cite(722, part=4, theory_class="standard_math")
    def measure_current(self, theta: float) -> float:
        """Determine current from measured deflection.

        Args:
            theta: Measured deflection (radians).

        Returns:
            Current in abamperes.
        """
        return theta * self.torsion_constant / (self.n_turns * self.area * self.field_strength)


@dataclass
class ThomsonCombinedInstrument:
    """Thomson's combined suspended coil and galvanometer (Art. 724).

    A hybrid instrument combining the suspended coil method
    with a standard galvanometer for absolute current measurement.
    """

    galvanometer_constant: float
    suspended_coil_sensitivity: float
    horizontal_field: float

    @maxwell_cite(724, part=4, theory_class="standard_math")
    def measure_current_both_methods(
        self,
        galvanometer_theta: float,
        coil_theta: float,
    ) -> dict[str, float]:
        """Measure current by both galvanometer and suspended coil.

        Args:
            galvanometer_theta: Galvanometer deflection (radians).
            coil_theta: Suspended coil deflection (radians).

        Returns:
            Dictionary with both current measurements.
        """
        I_galv = self.horizontal_field / self.galvanometer_constant * np.tan(galvanometer_theta)
        I_coil = coil_theta / self.suspended_coil_sensitivity
        return {
            "from_galvanometer": I_galv,
            "from_suspended_coil": I_coil,
            "mean": (I_galv + I_coil) / 2,
        }


@maxwell_cite(723, part=4, theory_class="standard_math")
def determine_magnetic_force(
    coil_deflection: float,
    coil_constant: float,
    torsion_constant: float,
) -> float:
    """Determine magnetic force from suspended coil deflection.

    F = k * theta / (n * A)

    Args:
        coil_deflection: Angular deflection (radians).
        coil_constant: n*A product of the coil.
        torsion_constant: Torsional constant of suspension.

    Returns:
        Magnetic force field H in oersted.
    """
    return torsion_constant * coil_deflection / coil_constant


@maxwell_cite(728, part=4, theory_class="standard_math")
def calc_uniform_normal_force(
    current: float,
    n_turns: int,
    area: float,
    field: float,
) -> float:
    """Calculate uniform normal force on suspended coil.

    When the field is uniform and normal to the coil plane,
    the torque is simply tau = n*I*A*H.

    Args:
        current: Current (abamperes).
        n_turns: Number of turns.
        area: Coil area (cm^2).
        field: Magnetic field (oersted).

    Returns:
        Torque in dyne-cm.
    """
    return n_turns * current * area * field
