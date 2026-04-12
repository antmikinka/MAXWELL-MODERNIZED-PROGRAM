"""maxwell.instruments.helmholtz — Helmholtz's double coil (Art. 713).

Helmholtz's arrangement of two identical coils separated by a
distance equal to their radius, producing an extremely uniform
magnetic field in the central region.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class HelmholtzCoil:
    """Helmholtz double coil arrangement (Art. 713).

    Two identical circular coils of radius R, separated by
    distance R, carrying current in the same direction.
    This arrangement cancels the second derivative of the
    field at the center, maximizing uniformity.

    Attributes:
        radius: Coil radius (cm).
        n_turns: Number of turns per coil.
        current: Current through coils (abamperes).
    """

    radius: float
    n_turns: int
    current: float

    @maxwell_cite(713, part=4, theory_class="standard_math")
    def field_at_center(self) -> float:
        """Calculate field at the center point.

        H = (8/5^(3/2)) * n*I / R
          = 0.7155 * n*I / R

        This is the famous Helmholtz formula: two coils
        each contributing (4/5^(3/2)) * n*I/R.

        Returns:
            Field H in oersted.
        """
        factor = (8.0 / (5.0**1.5))
        return factor * self.n_turns * self.current / self.radius

    @maxwell_cite(713, part=4, theory_class="standard_math")
    def field_on_axis(self, z: float) -> float:
        """Calculate field along the axis at position z from center.

        H(z) = (n*I*R^2/2) * [1/(R^2+(z-R/2)^2)^(3/2) + 1/(R^2+(z+R/2)^2)^(3/2)]

        Args:
            z: Position along axis from center (cm).

        Returns:
            Field H in oersted.
        """
        R = self.radius
        R2 = R**2
        term1 = 1.0 / (R2 + (z - R / 2.0) ** 2) ** 1.5
        term2 = 1.0 / (R2 + (z + R / 2.0) ** 2) ** 1.5
        return 0.5 * self.n_turns * self.current * R2 * (term1 + term2)

    @maxwell_cite(713, part=4, theory_class="standard_math")
    def uniformity_region(self, tolerance: float = 0.01) -> float:
        """Calculate the radius of the uniform field region.

        Returns the distance from center where the field
        deviates by less than the given tolerance.

        Args:
            tolerance: Maximum fractional deviation (default 1%).

        Returns:
            Radius of uniform region in cm.
        """
        H0 = self.field_at_center()
        # Search along axis for where |H(z) - H0| / H0 > tolerance
        z = 0.0
        step = 0.01 * self.radius
        while z < self.radius:
            Hz = self.field_on_axis(z)
            if abs(Hz - H0) / H0 > tolerance:
                return z
            z += step
        return z
