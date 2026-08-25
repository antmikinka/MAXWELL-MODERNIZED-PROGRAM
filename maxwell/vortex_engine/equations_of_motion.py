"""maxwell.vortex_engine.equations_of_motion — Vortex dynamics (Arts. 827-828).

Equations of motion of the vortex medium deduced from the kinetic energy
of Art. 826 by Lagrange's equations (Art. 827), and their solution for a
circularly-polarized ray, giving the two velocities of the right- and
left-circular components (Art. 828).

Maxwell 1873, Part IV, Ch. XXI, Arts. 827-828.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class VortexEquations:
    """Equations of motion of the vortex medium (Arts. 827-828).

    Attributes:
        ether_density: Density rho of the medium.
        elastic_constant: Leading Cauchy elasticity coefficient A_0
            (eqs. (12)-(13)).
        coupling_constant: Coupling constant C of Art. 824 eq. (3).
        magnetic_force: Magnetic force gamma resolved along the ray
            (the z axis).
        elastic_higher: Higher Cauchy coefficient A_1 (q^4 term).
    """

    ether_density: float
    elastic_constant: float
    coupling_constant: float = 0.0
    magnetic_force: float = 0.0
    elastic_higher: float = 0.0

    def elastic_function(self, q: float) -> float:
        """Q(q) = A_0 q^2 - A_1 q^4 (Art. 828 eq. (16)).

        Args:
            q: Wave number.

        Returns:
            The function Q of q^2 appearing in the potential energy
            V = (1/2) r^2 Q of the circular ray.
        """
        return self.elastic_constant * q**2 - self.elastic_higher * q**4

    @maxwell_cite(
        827,
        part=4,
        theory_class="maxwell_original",
        description="Equations (10)-(13): X = rho xi-ddot - 2 C gamma "
        "d^3 eta / dz^2 dt balanced against Cauchy's form "
        "A_0 xi'' + A_1 xi'''' for a plane circular wave.",
    )
    def derive_vortex_equations_of_motion(self, n: float, q: float) -> dict[str, float]:
        """Equations of motion for a plane circular wave (Art. 827).

        Maxwell 1873, Art. 827: the components of the impressed force per
        unit volume deduced from the kinetic energy (9) by Lagrange's
        equations are

            X = rho d^2 xi/dt^2 - 2 C gamma d^3 eta / dz^2 dt      (10)
            Y = rho d^2 eta/dt^2 + 2 C gamma d^3 xi / dz^2 dt      (11)

        and for an isotropic medium these must take Cauchy's form

            X = A_0 d^2 xi/dz^2 + A_1 d^4 xi/dz^4 + &c.            (12)
            Y = A_0 d^2 eta/dz^2 + A_1 d^4 eta/dz^4 + &c.          (13)

        Substituting the circular ray xi = r cos(n t - q z),
        eta = r sin(n t - q z) and equating the coefficient of
        -r cos(n t - q z) on both sides yields the inertial coefficient
        rho n^2 - 2 C gamma q^2 n and the elastic coefficient
        Q(q) = A_0 q^2 - A_1 q^4; their residual vanishes for free
        propagation (Art. 828 eq. (18)).

        Args:
            n: Angular frequency of the ray.
            q: Wave number of the ray.

        Returns:
            Dictionary with entries:
                force_inertial_coefficient: rho n^2 - 2 C gamma q^2 n
                    (from eqs. (10)-(11)).
                force_elastic_coefficient: A_0 q^2 - A_1 q^4 = Q(q)
                    (from eqs. (12)-(13)).
                residual: inertial - elastic; zero when (n, q) satisfies
                    the free-propagation condition rho n^2 - 2 C gamma
                    q^2 n = Q.
        """
        inertial = (
            self.ether_density * n**2
            - 2.0 * self.coupling_constant * self.magnetic_force * q**2 * n
        )
        elastic = self.elastic_function(q)
        return {
            "force_inertial_coefficient": inertial,
            "force_elastic_coefficient": elastic,
            "residual": inertial - elastic,
        }

    @maxwell_cite(
        828,
        part=4,
        theory_class="maxwell_original",
        description="Equation (18): rho n^2 - 2 C gamma q^2 n = Q solved "
        "as a quadratic in n for a ray of given wave number q.",
    )
    def solve_plane_wave(self, q: float) -> dict:
        """Solve the free-propagation condition for n (Art. 828, eq. 18).

        The condition of free propagation dT/dr = dV/dr (Art. 819
        eq. (6)) gives, with T from eq. (15) and V from eq. (16),

            rho n^2 - 2 C gamma q^2 n = Q                          (18)

        "whence the value of n may be found in terms of q."

        Args:
            q: Wave number of the ray.

        Returns:
            Dictionary with entries:
                n_plus, n_minus: The two roots
                    n = (C gamma q^2 +- sqrt(C^2 gamma^2 q^4 + rho Q))
                        / rho,
                    real for non-negative discriminant, complex otherwise.
                discriminant: C^2 gamma^2 q^4 + rho Q.
                Q: The elastic function Q(q).

        Raises:
            ValueError: If ether_density is zero (no quadratic).
        """
        if self.ether_density == 0:
            raise ValueError("ether_density must be nonzero")
        Q = self.elastic_function(q)
        disc = (self.coupling_constant * self.magnetic_force * q**2) ** 2 + (
            self.ether_density * Q
        )
        if disc >= 0:
            sqrt_disc = float(np.sqrt(disc))
        else:
            sqrt_disc = complex(0.0, float(np.sqrt(-disc)))
        centre = self.coupling_constant * self.magnetic_force * q**2
        return {
            "n_plus": (centre + sqrt_disc) / self.ether_density,
            "n_minus": (centre - sqrt_disc) / self.ether_density,
            "discriminant": disc,
            "Q": Q,
        }


@maxwell_cite(
    828,
    part=4,
    theory_class="maxwell_original",
    description="The two roots of equation (18) give the angular velocities "
    "of the two circularly-polarized components; their velocities are n/q.",
)
def calc_vortex_circular_velocity(
    q: float,
    density: float,
    elastic_constant: float,
    coupling_constant: float,
    magnetic_force: float,
    elastic_higher: float = 0.0,
) -> dict:
    """Velocities of the circular components in the vortex medium (Art. 828).

    Maxwell 1873, Art. 828: the quadratic (18) has two roots n, one for
    each circular component of a ray of given wave number q; the
    corresponding phase velocities are v = n/q (Art. 817).  By Vieta's
    relations the roots satisfy

        n_plus + n_minus = 2 C gamma q^2 / rho,
        n_plus * n_minus = -Q / rho,

    so the magnetic force (gamma) splits the two velocities while their
    product is fixed by the elasticity alone.

    Args:
        q: Wave number of the ray (nonzero).
        density: Density rho of the medium (nonzero).
        elastic_constant: Cauchy coefficient A_0.
        coupling_constant: Coupling constant C.
        magnetic_force: Magnetic force gamma along the ray.
        elastic_higher: Cauchy coefficient A_1 (default 0).

    Returns:
        Dictionary with entries:
            n_plus, n_minus: Roots of rho n^2 - 2 C gamma q^2 n - Q = 0.
            v_plus, v_minus: Phase velocities n/q of the two components.
            velocity_split: v_plus - v_minus.
            sum_roots: 2 C gamma q^2 / rho (Vieta).
            product_roots: -Q / rho (Vieta).

    Raises:
        ValueError: If q or density is zero.
    """
    if q == 0:
        raise ValueError("q must be nonzero (velocity n/q undefined)")
    if density == 0:
        raise ValueError("density must be nonzero")
    Q = elastic_constant * q**2 - elastic_higher * q**4
    disc = (coupling_constant * magnetic_force * q**2) ** 2 + density * Q
    if disc >= 0:
        sqrt_disc = float(np.sqrt(disc))
    else:
        sqrt_disc = complex(0.0, float(np.sqrt(-disc)))
    centre = coupling_constant * magnetic_force * q**2
    n_plus = (centre + sqrt_disc) / density
    n_minus = (centre - sqrt_disc) / density
    return {
        "n_plus": n_plus,
        "n_minus": n_minus,
        "v_plus": n_plus / q,
        "v_minus": n_minus / q,
        "velocity_split": (n_plus - n_minus) / q,
        "sum_roots": 2.0 * coupling_constant * magnetic_force * q**2 / density,
        "product_roots": -Q / density,
    }
