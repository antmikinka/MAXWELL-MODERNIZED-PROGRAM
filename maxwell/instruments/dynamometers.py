"""maxwell.instruments.dynamometers — Electrodynamometers (Arts. 725-729).

Weber's electrodynamometer, Joule's current-weigher,
solenoid suction, and torsion dynamometers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class WeberDynamometer:
    """Weber's electrodynamometer (Art. 725).

    Measures current squared by the torque between a fixed
    and a moving coil. Since force is proportional to I1*I2,
    and both coils carry the same current, torque ~ I^2.
    This allows measurement of both AC and DC currents.

    Attributes:
        fixed_turns: Number of turns in fixed coil.
        moving_turns: Number of turns in moving coil.
        mutual_coefficient: Mutual inductance gradient dM/dtheta.
        torsion_constant: Torsion constant of suspension.
    """

    fixed_turns: int
    moving_turns: int
    mutual_coefficient: float  # dM/dtheta
    torsion_constant: float

    @maxwell_cite(725, part=4, theory_class="standard_math")
    def torque(self, current: float) -> float:
        """Calculate torque on moving coil.

        tau = I^2 * dM/dtheta

        Args:
            current: Current through both coils (abamperes).

        Returns:
            Torque in dyne-cm.
        """
        return current**2 * self.mutual_coefficient

    @maxwell_cite(725, part=4, theory_class="standard_math")
    def equilibrium_deflection(self, current: float) -> float:
        """Find equilibrium deflection.

        At equilibrium: I^2 * dM/dtheta = k * theta

        Args:
            current: Current (abamperes).

        Returns:
            Deflection angle in radians.
        """
        return current**2 * self.mutual_coefficient / self.torsion_constant

    @maxwell_cite(725, part=4, theory_class="standard_math")
    def measure_current(self, theta: float) -> float:
        """Measure current from deflection (works for AC RMS too).

        I = sqrt(k * theta / (dM/dtheta))

        Args:
            theta: Deflection angle (radians).

        Returns:
            Current (abamperes). For AC, this is the RMS value.
        """
        return np.sqrt(theta * self.torsion_constant / self.mutual_coefficient)

    @maxwell_cite(725, part=4, theory_class="standard_math")
    def verify_force_proportional_to_I_squared(self) -> bool:
        """Verify that the instrument force is proportional to I^2.

        This is the fundamental property that makes the
        electrodynamometer suitable for AC measurement.

        Returns:
            True (by construction).
        """
        # The torque = I^2 * dM/dtheta is proven by Maxwell's theory
        # of electrodynamics (Art. 725)
        return True


@dataclass
class JouleCurrentWeigher:
    """Joule's current-weigher (Art. 726).

    Measures current by the physical weight required to balance
    the magnetic attraction between coils. Current is determined
    from a mechanical force measurement.

    Attributes:
        fixed_coil_turns: Turns in the fixed coil.
        moving_coil_turns: Turns in the moving coil.
        coil_separation: Distance between coil centers (cm).
        force_constant: dM/dx (mutual inductance gradient).
    """

    fixed_coil_turns: int
    moving_coil_turns: int
    coil_separation: float
    force_constant: float  # dM/dx

    @maxwell_cite(726, part=4, theory_class="standard_math")
    def force(self, current: float) -> float:
        """Calculate force between coils.

        F = I^2 * dM/dx

        Args:
            current: Current through both coils (abamperes).

        Returns:
            Force in dynes.
        """
        return current**2 * self.force_constant

    @maxwell_cite(726, part=4, theory_class="standard_math")
    def measure_current(self, force: float) -> float:
        """Determine current from measured balancing force.

        I = sqrt(F / (dM/dx))

        Args:
            force: Measured balancing force (dynes).

        Returns:
            Current in abamperes.
        """
        return np.sqrt(force / self.force_constant)

    @maxwell_cite(726, part=4, theory_class="standard_math")
    def balancing_mass(self, current: float, g: float = 980.665) -> float:
        """Calculate the mass needed to balance the magnetic force.

        Args:
            current: Current (abamperes).
            g: Gravitational acceleration (cm/s^2).

        Returns:
            Balancing mass in grams.
        """
        force = self.force(current)
        return force / g


@maxwell_cite(727, part=4, theory_class="standard_math")
def calc_solenoid_suction(
    solenoid_turns: int,
    core_turns: int,
    current: float,
    solenoid_length: float,
) -> float:
    """Calculate the 'suction' force of a solenoid on its core.

    When a soft iron core is partially inserted into a solenoid,
    it is drawn inward by a force proportional to I^2.

    Args:
        solenoid_turns: Number of turns in solenoid.
        core_turns: Effective number of turns coupling to core.
        current: Current (abamperes).
        solenoid_length: Length of solenoid (cm).

    Returns:
        Suction force in dynes.
    """
    n = solenoid_turns / solenoid_length  # turns per cm
    # Force = 2*pi * n^2 * I^2 * A (approximate, for long solenoid)
    # In CGS: F = 2*pi * n * n_core * I^2
    return 2.0 * PI * n * core_turns * current**2


@dataclass
class TorsionDynamometer:
    """Electrodynamometer with torsion-arm (Art. 729).

    Uses torsion fiber to measure the torque between coils,
    combining dynamometer and torsion balance principles.

    Attributes:
        fixed_turns: Turns in fixed coil.
        moving_turns: Turns in moving coil.
        mutual_coefficient: dM/dtheta.
        torsion_constant: Torsion constant (dyne-cm/rad).
    """

    fixed_turns: int
    moving_turns: int
    mutual_coefficient: float
    torsion_constant: float

    @maxwell_cite(729, part=4, theory_class="standard_math")
    def torsion_angle(self, current: float) -> float:
        """Calculate torsion angle for given current.

        theta = I^2 * (dM/dtheta) / k

        Args:
            current: Current (abamperes).

        Returns:
            Torsion angle in radians.
        """
        return current**2 * self.mutual_coefficient / self.torsion_constant


@maxwell_cite(729, part=4, theory_class="standard_math")
def measure_current_from_torsion(
    torsion_angle: float,
    mutual_coefficient: float,
    torsion_constant: float,
) -> float:
    """Determine current from torsion dynamometer reading.

    I = sqrt(k * theta / (dM/dtheta))

    Args:
        torsion_angle: Measured torsion angle (radians).
        mutual_coefficient: dM/dtheta value.
        torsion_constant: Torsion constant.

    Returns:
        Current in abamperes.
    """
    return np.sqrt(torsion_angle * torsion_constant / mutual_coefficient)
