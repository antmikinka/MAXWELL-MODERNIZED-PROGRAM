"""maxwell.instruments.helmholtz — Helmholtz's double coil (Art. 713).

Two identical coaxial circular coils separated by a distance equal to
their radius, carrying current in the same direction, produce an
extremely uniform magnetic field in the central region.

Unit convention — CGS-EMU (repo default for Part IV instruments):
currents in abamperes, fields in gauss; the EMU Biot-Savart law
dB = I dl x r_hat / r^2 carries no factor of c, so the on-axis field of
one coil is B(z) = 2.pi.n.I.a^2 / (a^2 + z^2)^(3/2).

Note (Stage-3 defect D-16 reconciliation): the Gaussian-flavoured module
``maxwell.electromagnetism.components.circular_coils`` carries an explicit
``CONST.C`` in the same Biot-Savart expression and therefore reads its
current argument as statamperes; both descriptions agree once
1 abampere = c statamperes is applied (pinned by
``tests/test_articles_instruments_707_729.py``).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class HelmholtzCoil:
    """Helmholtz double coil arrangement (Art. 713).

    Two identical circular coils of radius ``radius``, separated by a
    distance equal to ``radius`` (the Helmholtz condition,
    :meth:`optimal_spacing`), carrying current in the same direction.
    At this spacing the second derivative of the axial field at the
    centre vanishes, maximising the uniform region.

    Attributes:
        radius: Coil radius (cm).
        n_turns: Number of turns per coil.
        current: Current through coils (abamperes).
    """

    radius: float
    n_turns: int
    current: float

    @staticmethod
    def optimal_spacing(radius: float) -> float:
        """Helmholtz condition: spacing equal to the radius (Art. 713).

        The axial field of two identical coils at separation s is
        B(z) = 2.pi.n.I.a^2 [g(z - s/2) + g(z + s/2)] with
        g(u) = (a^2 + u^2)^(-3/2). Its second derivative at the centre is

            B''(0) = 2.pi.n.I.a^2 * 2 * (12(s/2)^2 - 3a^2)
                     * (a^2 + s^2/4)^(-7/2)
                   ∝ 3(s^2 - a^2),

        which vanishes if and only if s = a: the Helmholtz uniformity
        condition.

        Args:
            radius: Coil radius (cm).

        Returns:
            Coil separation for maximum field uniformity (cm).
        """
        return radius

    @maxwell_cite(
        713,
        part=4,
        theory_class="standard_math",
        description="Field at the midpoint of a Helmholtz pair (EMU)",
    )
    def field_at_center(self, spacing: float | None = None) -> float:
        """Calculate field at the midpoint between the coils.

        Each coil contributes 2.pi.n.I.a^2 / (a^2 + (s/2)^2)^(3/2), so

            B = 4.pi.n.I.a^2 / (a^2 + s^2/4)^(3/2)

        which at the Helmholtz spacing s = a reduces to

            B = 4.pi.n.I/a * (4/5)^(3/2) = 32.pi.n.I / (5*sqrt(5)*a)
              ≈ 8.99176 * n.I/a   (gauss, EMU).

        (In SI the same geometry gives mu0.n.I/a * (4/5)^(3/2); the EMU
        form replaces mu0 by 4.pi.)

        Args:
            spacing: Coil separation (cm); defaults to the Helmholtz
                spacing (the radius).

        Returns:
            Field B in gauss.
        """
        a = self.radius
        s = a if spacing is None else spacing
        return (
            4.0
            * PI
            * self.n_turns
            * self.current
            * a**2
            / (a**2 + (0.5 * s) ** 2) ** 1.5
        )

    @maxwell_cite(
        713,
        part=4,
        theory_class="standard_math",
        description="Axial field profile of a Helmholtz pair (EMU)",
    )
    def field_on_axis(self, z: float, spacing: float | None = None) -> float:
        """Calculate field along the axis at position z from the midpoint.

        B(z) = 2.pi.n.I.a^2 * [ (a^2 + (z - s/2)^2)^(-3/2)
                                + (a^2 + (z + s/2)^2)^(-3/2) ]

        Args:
            z: Position along axis from the midpoint (cm).
            spacing: Coil separation (cm); defaults to the Helmholtz
                spacing (the radius).

        Returns:
            Field B in gauss.
        """
        a = self.radius
        s = a if spacing is None else spacing
        a2 = a**2
        term1 = 1.0 / (a2 + (z - 0.5 * s) ** 2) ** 1.5
        term2 = 1.0 / (a2 + (z + 0.5 * s) ** 2) ** 1.5
        return 2.0 * PI * self.n_turns * self.current * a2 * (term1 + term2)

    @maxwell_cite(
        713,
        part=4,
        theory_class="standard_math",
        description="Extent of the uniform-field region along the axis",
    )
    def uniformity_region(self, tolerance: float = 0.01) -> float:
        """Calculate the half-length of the uniform field region.

        Returns the axial distance from the centre at which the field
        first deviates from the centre value by more than ``tolerance``
        (relative), scanning outward in steps of radius/200.

        Args:
            tolerance: Maximum fractional deviation (default 1%).

        Returns:
            Half-length of the uniform region along the axis (cm).
        """
        b0 = self.field_at_center()
        z = 0.0
        step = 0.005 * self.radius
        while z < self.radius:
            bz = self.field_on_axis(z)
            if abs(bz - b0) / b0 > tolerance:
                return z
            z += step
        return z
