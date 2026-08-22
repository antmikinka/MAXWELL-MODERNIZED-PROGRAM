"""maxwell.instruments.suspended_coil — Suspended coil instruments (Arts. 721-724, 728).

Thomson's sensitive suspended coil, the mode of suspension, the
determination of magnetic force by the suspended-coil method, and the
uniform-field torque.

Unit convention — CGS-EMU (repo default for Part IV instruments):
    currents : abampere (abA)
    fields   : gauss
    torques  : dyne.cm
    magnetic moment of a coil: n.I.A (emu = erg/gauss), since a turn of
    area A carrying I abampere is a magnetic shell of moment I.A.

Sign convention: theta is the deflection of the coil from its
zero-current position, in which the plane of the coil is parallel to the
controlling field. The torque of the field on the coil is then
n.I.A.H.cos(theta) (maximum at theta = 0), opposed by the controlling
(torsion) torque k.theta.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


def _bisect_root(f, lo: float, hi: float, iterations: int = 100) -> float:
    """Bisection root of a continuous ``f`` with ``f(lo)*f(hi) <= 0``."""
    flo = f(lo)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if flo * fmid <= 0.0:
            hi = mid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)


@dataclass
class SuspendedCoil:
    """Base suspended coil instrument (Arts. 721-722).

    A coil suspended by a fine fiber, free to rotate in a magnetic field.
    The magnetic torque on the coil is balanced by the controlling torque
    of the suspension (equilibrium solved exactly, not only at small
    angles).

    Attributes:
        n_turns: Number of turns in suspended coil.
        area: Area of the coil (cm^2).
        torsion_constant: Controlling torque per radian of the suspension
            fiber k (dyne.cm/rad).
        horizontal_field: External field H (gauss).
    """

    n_turns: int
    area: float  # cm^2
    torsion_constant: float
    horizontal_field: float

    @maxwell_cite(
        721,
        part=4,
        theory_class="standard_math",
        description="Magnetic moment of a current coil, mu = n.I.A",
    )
    def magnetic_moment(self, current: float) -> float:
        """Calculate magnetic moment of the suspended coil.

        mu = n.I.A

        Args:
            current: Current through coil (abamperes).

        Returns:
            Magnetic moment (emu = erg/gauss).
        """
        return self.n_turns * current * self.area

    @maxwell_cite(
        721,
        part=4,
        theory_class="standard_math",
        description="Net torque n.I.A.H.cos(theta) - k.theta",
    )
    def torque(self, current: float, theta: float) -> float:
        """Calculate net torque on suspended coil.

        tau = n.I.A.H.cos(theta) - k.theta

        with theta measured from the zero-current position (coil plane
        parallel to the field), where the magnetic torque is maximal.

        Args:
            current: Current through coil (abamperes).
            theta: Angular deflection (radians).

        Returns:
            Net torque (dyne.cm), positive in the direction of increasing
            theta.
        """
        magnetic = self.magnetic_moment(current) * self.horizontal_field * np.cos(theta)
        restoring = -self.torsion_constant * theta
        return magnetic + restoring

    @maxwell_cite(
        721,
        part=4,
        theory_class="standard_math",
        description="Exact controlling-vs-magnetic torque equilibrium",
    )
    def equilibrium_deflection(self, current: float) -> float:
        """Find the equilibrium deflection angle for a given current.

        Solves the controlling-torque / magnetic-torque balance

            k.theta = n.I.A.H.cos(theta)

        exactly by bisection on (0, pi/2), where the root is unique
        (k.theta increases from 0 while n.I.A.H.cos(theta) decreases to
        0). The small-angle limit is theta ≈ n.I.A.H/k.

        Args:
            current: Current through coil (abamperes).

        Returns:
            Equilibrium angle in radians (sign follows the current).
        """
        if current == 0.0:
            return 0.0
        mu = self.magnetic_moment(abs(current))

        def balance(theta: float) -> float:
            return self.torsion_constant * theta - mu * self.horizontal_field * np.cos(theta)

        # balance(0) = -mu.H <= 0 and balance(pi/2) = k.pi/2 > 0, with a
        # strictly increasing balance function, so the root is unique.
        theta = _bisect_root(balance, 0.0, 0.5 * PI)
        return theta if current > 0.0 else -theta


@dataclass
class ThomsonSensitiveCoil:
    """Thomson's sensitive suspended coil (Art. 722).

    Thomson's design uses a long, narrow coil of many turns suspended in
    a strong field, so that the deflection per unit current
    n.A.H/k is large.

    Attributes:
        n_turns: Number of turns.
        coil_length: Length of the coil (cm).
        coil_width: Width of the coil (cm).
        field_strength: Field strength (gauss).
        torsion_constant: Controlling torque per radian (dyne.cm/rad).
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

    @maxwell_cite(
        722,
        part=4,
        theory_class="standard_math",
        description="Current sensitivity d(theta)/dI at zero deflection = n.A.H/k",
    )
    def sensitivity(self) -> float:
        """Current sensitivity (radians per abampere).

        Differentiating k.theta = n.I.A.H.cos(theta) at theta = 0 gives
        d(theta)/dI = n.A.H/k.
        """
        return self.n_turns * self.area * self.field_strength / self.torsion_constant

    @maxwell_cite(
        722,
        part=4,
        theory_class="standard_math",
        description="Exact inversion I = k.theta/(n.A.H.cos(theta))",
    )
    def measure_current(self, theta: float) -> float:
        """Determine current from measured deflection.

        Exact inversion of the equilibrium balance
        k.theta = n.I.A.H.cos(theta):

            I = k.theta / (n.A.H.cos(theta))

        (reduces to theta/sensitivity at small deflection).

        Args:
            theta: Measured deflection (radians), |theta| < pi/2.

        Returns:
            Current in abamperes.
        """
        return (
            theta
            * self.torsion_constant
            / (
                self.n_turns
                * self.area
                * self.field_strength
                * np.cos(theta)
            )
        )


@dataclass
class ThomsonCombinedInstrument:
    """Thomson's combined suspended coil and galvanometer (Art. 724).

    A hybrid instrument combining the suspended-coil method with a
    standard (tangent) galvanometer, so the same current can be read two
    independent ways and cross-checked.

    Attributes:
        galvanometer_constant: G of the galvanometer coil (cm^-1).
        suspended_coil_sensitivity: Suspended-coil sensitivity S =
            n.A.H/k (radians per abampere, small-deflection).
        horizontal_field: Terrestrial horizontal field H (gauss).
    """

    galvanometer_constant: float
    suspended_coil_sensitivity: float
    horizontal_field: float

    @maxwell_cite(
        724,
        part=4,
        theory_class="standard_math",
        description="Same current read by tangent galvanometer and suspended coil",
    )
    def measure_current_both_methods(
        self,
        galvanometer_theta: float,
        coil_theta: float,
    ) -> dict[str, float]:
        """Measure current by both galvanometer and suspended coil.

        The galvanometer reading uses the tangent law I = (H/G) tan(theta)
        (exact); the suspended-coil reading uses the small-deflection
        sensitivity I = theta/S (leading order in theta).

        Args:
            galvanometer_theta: Galvanometer deflection (radians).
            coil_theta: Suspended coil deflection (radians).

        Returns:
            Dictionary with both current measurements and their mean.
        """
        i_galv = (
            self.horizontal_field
            / self.galvanometer_constant
            * np.tan(galvanometer_theta)
        )
        i_coil = coil_theta / self.suspended_coil_sensitivity
        return {
            "from_galvanometer": i_galv,
            "from_suspended_coil": i_coil,
            "mean": (i_galv + i_coil) / 2,
        }


@maxwell_cite(
    723,
    part=4,
    theory_class="standard_math",
    description="Determination of an unknown field from coil deflection, "
    "H = k.theta/(n.A.I)",
)
def determine_magnetic_force(
    coil_deflection: float,
    coil_constant: float,
    torsion_constant: float,
    current: float,
) -> float:
    """Determine magnetic force (field) from suspended coil deflection.

    Inverting the small-deflection equilibrium k.theta = n.I.A.H:

        H = k.theta / (n.A.I)

    where ``coil_constant`` is the n.A product of the coil. This is the
    suspended-coil method of measuring an unknown field with a known
    current.

    Args:
        coil_deflection: Angular deflection (radians).
        coil_constant: n.A product of the coil (cm^2 turns).
        torsion_constant: Controlling torque per radian (dyne.cm/rad).
        current: Current through the coil (abamperes).

    Returns:
        Field H in gauss.

    Raises:
        ValueError: if current or coil_constant is not positive.
    """
    if current <= 0.0:
        raise ValueError("current must be positive")
    if coil_constant <= 0.0:
        raise ValueError("coil_constant must be positive")
    return torsion_constant * coil_deflection / (coil_constant * current)


@maxwell_cite(
    728,
    part=4,
    theory_class="standard_math",
    description="Maximum torque n.I.A.H of a uniform field lying in the coil plane",
)
def calc_uniform_normal_force(
    current: float,
    n_turns: int,
    area: float,
    field: float,
) -> float:
    """Calculate the torque of a uniform field on the suspended coil.

    When the uniform field lies in the plane of the coil — i.e. normal to
    the coil's magnetic moment — the torque attains its maximum value

        tau = n.I.A.H   (dyne.cm).

    (A field perpendicular to the coil plane is parallel to the magnetic
    moment and exerts no torque.)

    Args:
        current: Current (abamperes).
        n_turns: Number of turns.
        area: Coil area (cm^2).
        field: Magnetic field (gauss).

    Returns:
        Torque in dyne.cm.
    """
    return n_turns * current * area * field
