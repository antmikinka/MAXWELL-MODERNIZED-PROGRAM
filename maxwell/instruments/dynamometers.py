"""maxwell.instruments.dynamometers — Electrodynamometers (Arts. 725-729).

Weber's electrodynamometer, Joule's current-weigher, solenoid suction,
and torsion dynamometers.

Unit convention — CGS-EMU (repo default for Part IV instruments):
    currents : abampere (abA)
    torques  : dyne.cm
    forces   : dyne
    mutual inductance: cm (EMU inductance has the dimension of length;
        mu0 -> 4*pi is dimensionless), so the generalized force between
        two circuits carrying the same current is I^2.dM/dx with no
        factor of c^2 (cf. the Stage-3 D-05 repair of the extended
        current weigher).

Common physics: the mechanical force/torque between two circuits equals
the derivative of their mutual energy M.I1.I2 with respect to the
generalized coordinate; with the coils in series (I1 = I2 = I) every
instrument in this module reads I^2, which is what makes these
instruments usable for alternating currents (reading the mean square).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class WeberDynamometer:
    """Weber's electrodynamometer (Art. 725).

    Measures the square of the current by the torque between a fixed
    and a moving coil. Since the torque is I1.I2.dM/dtheta and both
    coils carry the same current, torque ∝ I^2; the instrument therefore
    reads mean-square current and serves for AC as well as DC.

    The constant ``mutual_coefficient`` idealizes dM/dtheta as
    independent of theta (the instrument is used over the small angular
    range where this holds).

    Attributes:
        fixed_turns: Number of turns in fixed coil.
        moving_turns: Number of turns in moving coil.
        mutual_coefficient: dM/dtheta (cm/rad), constant-gradient
            approximation.
        torsion_constant: Torsion constant of suspension (dyne.cm/rad).
    """

    fixed_turns: int
    moving_turns: int
    mutual_coefficient: float  # dM/dtheta
    torsion_constant: float

    @maxwell_cite(
        725,
        part=4,
        theory_class="standard_math",
        description="Dynamometer torque tau = I^2 dM/dtheta",
    )
    def torque(self, current: float) -> float:
        """Calculate torque on moving coil.

        tau = I^2 * dM/dtheta

        Args:
            current: Current through both coils (abamperes).

        Returns:
            Torque in dyne.cm.
        """
        return current**2 * self.mutual_coefficient

    @maxwell_cite(
        725,
        part=4,
        theory_class="standard_math",
        description="Equilibrium I^2 dM/dtheta = k.theta (constant gradient)",
    )
    def equilibrium_deflection(self, current: float) -> float:
        """Find equilibrium deflection.

        At equilibrium: I^2 * dM/dtheta = k * theta, hence
        theta = I^2 (dM/dtheta) / k under the constant-gradient
        approximation of ``mutual_coefficient``.

        Args:
            current: Current (abamperes).

        Returns:
            Deflection angle in radians.
        """
        return current**2 * self.mutual_coefficient / self.torsion_constant

    @maxwell_cite(
        725,
        part=4,
        theory_class="standard_math",
        description="Inversion I = sqrt(k.theta/(dM/dtheta))",
    )
    def measure_current(self, theta: float) -> float:
        """Measure current from deflection (works for AC RMS too).

        I = sqrt(k * theta / (dM/dtheta))

        Args:
            theta: Deflection angle (radians), theta >= 0.

        Returns:
            Current (abamperes). For AC, this is the RMS value.
        """
        return np.sqrt(theta * self.torsion_constant / self.mutual_coefficient)

    @maxwell_cite(
        725,
        part=4,
        theory_class="standard_math",
        description="Computed check that the torque scales as I^2",
    )
    def verify_force_proportional_to_I_squared(self) -> bool:
        """Verify computationally that the instrument torque ∝ I^2.

        Evaluates the actual torque law at two currents and extracts the
        power-law exponent log(tau(2I)/tau(I))/log(2); returns True only
        if the exponent equals 2 within 1e-9. This is the fundamental
        property that makes the electrodynamometer suitable for AC
        measurement (the verdict is computed from the torque function,
        never returned as a literal).

        Returns:
            True if the computed scaling exponent is 2 within tolerance.
        """
        tau_1 = self.torque(1.0)
        tau_2 = self.torque(2.0)
        if tau_1 == 0.0:
            return False
        exponent = np.log(tau_2 / tau_1) / np.log(2.0)
        return bool(abs(exponent - 2.0) < 1e-9)


@dataclass
class JouleCurrentWeigher:
    """Current-weigher (Art. 726).

    Measures current by the mechanical weight required to balance the
    magnetic attraction between two coaxial coils; the current is
    determined from a force measurement, F = I^2.dM/dx.

    Attributes:
        fixed_coil_turns: Turns in the fixed coil.
        moving_coil_turns: Turns in the moving coil.
        coil_separation: Distance between coil centers (cm).
        force_constant: dM/dx (dimensionless in EMU, mutual inductance
            gradient with respect to separation).
    """

    fixed_coil_turns: int
    moving_coil_turns: int
    coil_separation: float
    force_constant: float  # dM/dx

    @maxwell_cite(
        726,
        part=4,
        theory_class="standard_math",
        description="Weigher force F = I^2 dM/dx (EMU, no c^2)",
    )
    def force(self, current: float) -> float:
        """Calculate force between coils.

        F = I^2 * dM/dx

        Args:
            current: Current through both coils (abamperes).

        Returns:
            Force in dynes.
        """
        return current**2 * self.force_constant

    @maxwell_cite(
        726,
        part=4,
        theory_class="standard_math",
        description="Inversion I = sqrt(F/(dM/dx))",
    )
    def measure_current(self, force: float) -> float:
        """Determine current from measured balancing force.

        I = sqrt(F / (dM/dx))

        Args:
            force: Measured balancing force (dynes), force >= 0.

        Returns:
            Current in abamperes.
        """
        return np.sqrt(force / self.force_constant)

    @maxwell_cite(
        726,
        part=4,
        theory_class="standard_math",
        description="Balancing mass m = F/g for the weigher",
    )
    def balancing_mass(self, current: float, g: float = CONST.G_STANDARD) -> float:
        """Calculate the mass needed to balance the magnetic force.

        Args:
            current: Current (abamperes).
            g: Gravitational acceleration (cm/s^2). Default is standard
                gravity g0 = 980.665 cm/s^2 from
                ``maxwell.config.constants.CONST.G_STANDARD``
                (Stage-3 D-33 constant hygiene; closed Wave 6).

        Returns:
            Balancing mass in grams.
        """
        return self.force(current) / g


@maxwell_cite(
    727,
    part=4,
    theory_class="standard_math",
    description="Suction force of a solenoid on a coaxial core coil, "
    "F = 4.pi.n1.n2.A.I^2",
)
def calc_solenoid_suction(
    solenoid_turns: int,
    core_turns: int,
    current: float,
    solenoid_length: float,
    core_length: float,
    core_area: float,
) -> float:
    """Calculate the 'suction' force of a solenoid on its core coil.

    Two coaxial solenoids (outer: N1 turns over length L1; core coil:
    N2 turns over length L2, cross-section A) carrying the same current
    have mutual inductance M = 4.pi.n1.n2.A.x in the long-solenoid
    approximation, where x is the overlap length and n_i = N_i/L_i are
    turns per unit length (EMU: M in cm). The generalized force is

        F = I^2.dM/dx = 4.pi.n1.n2.A.I^2   (dynes).

    Consistency (checked by test): the work of drawing the core fully in
    is F.L2 = 4.pi.n1.N2.A.I^2 = M_total.I^2, the mutual energy of the
    fully-inserted position.

    Args:
        solenoid_turns: Number of turns in the outer solenoid.
        core_turns: Number of turns of the core coil.
        current: Current (abamperes), same in both windings.
        solenoid_length: Length of the outer solenoid (cm).
        core_length: Axial length of the core coil (cm).
        core_area: Cross-section of the core coil (cm^2).

    Returns:
        Suction force in dynes.

    Raises:
        ValueError: for non-positive lengths, area, or turn counts.
    """
    if min(solenoid_length, core_length, core_area) <= 0.0:
        raise ValueError("lengths and area must be positive")
    if solenoid_turns <= 0 or core_turns <= 0:
        raise ValueError("turn counts must be positive")

    n1 = solenoid_turns / solenoid_length  # turns per cm
    n2 = core_turns / core_length
    return 4.0 * PI * n1 * n2 * core_area * current**2


@dataclass
class TorsionDynamometer:
    """Electrodynamometer with torsion arm (Art. 729).

    Measures the torque between the coils by the torsion angle a fiber
    must supply to restore the moving coil to its zero position,
    combining dynamometer and torsion-balance principles.

    Attributes:
        fixed_turns: Turns in fixed coil.
        moving_turns: Turns in moving coil.
        mutual_coefficient: dM/dtheta (cm/rad), constant-gradient
            approximation.
        torsion_constant: Torsion constant (dyne.cm/rad).
    """

    fixed_turns: int
    moving_turns: int
    mutual_coefficient: float
    torsion_constant: float

    @maxwell_cite(
        729,
        part=4,
        theory_class="standard_math",
        description="Torsion balance condition theta = I^2 (dM/dtheta)/k",
    )
    def torsion_angle(self, current: float) -> float:
        """Calculate torsion angle for given current.

        theta = I^2 * (dM/dtheta) / k

        Args:
            current: Current (abamperes).

        Returns:
            Torsion angle in radians.
        """
        return current**2 * self.mutual_coefficient / self.torsion_constant


@maxwell_cite(
    729,
    part=4,
    theory_class="standard_math",
    description="Inversion I = sqrt(k.theta/(dM/dtheta))",
)
def measure_current_from_torsion(
    torsion_angle: float,
    mutual_coefficient: float,
    torsion_constant: float,
) -> float:
    """Determine current from torsion dynamometer reading.

    I = sqrt(k * theta / (dM/dtheta))

    Args:
        torsion_angle: Measured torsion angle (radians), >= 0.
        mutual_coefficient: dM/dtheta value (cm/rad).
        torsion_constant: Torsion constant (dyne.cm/rad).

    Returns:
        Current in abamperes.
    """
    return np.sqrt(torsion_angle * torsion_constant / mutual_coefficient)
