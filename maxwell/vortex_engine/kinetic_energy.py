"""maxwell.vortex_engine.kinetic_energy — Disturbed medium energy (Arts. 824-826).

Kinetic energy of the disturbed vortex medium: the angular velocity of a
displaced element (Art. 824), the coupling of that motion with the
molecular rotations, its expression in terms of current and velocity
(Art. 825), and its reduced form for plane waves (Art. 826).

Maxwell 1873, Part IV, Ch. XXI, Arts. 824-826.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@maxwell_cite(
    824,
    part=4,
    theory_class="maxwell_original",
    description="Equation (2): the angular velocity of an element of the "
    "medium is half the curl of its velocity.",
)
def calc_vortex_angular_velocity(velocity_gradient: np.ndarray) -> np.ndarray:
    """Angular velocity of a displaced element of the medium (Art. 824).

    Maxwell 1873, Art. 824, equation (2): the components of the angular
    velocity of an element of the medium are

        omega_1 = (1/2) d/dt (d zeta/dy - d eta/dz)
        omega_2 = (1/2) d/dt (d xi/dz  - d zeta/dx)
        omega_3 = (1/2) d/dt (d eta/dx - d xi/dy)

    which is one half of the curl of the velocity (xi-dot, eta-dot,
    zeta-dot): omega = (1/2) curl v.

    Args:
        velocity_gradient: Velocity-gradient tensor L with
            L[i, j] = dv_i/dx_j, shape (3, 3).

    Returns:
        Angular velocity vector omega = (1/2) curl v, shape (3,).
    """
    L = np.asarray(velocity_gradient, dtype=float)
    return 0.5 * np.array(
        [
            L[2, 1] - L[1, 2],  # dv_z/dy - dv_y/dz
            L[0, 2] - L[2, 0],  # dv_x/dz - dv_z/dx
            L[1, 0] - L[0, 1],  # dv_y/dx - dv_x/dy
        ]
    )


@maxwell_cite(
    824,
    part=4,
    theory_class="maxwell_original",
    description="Equation (3): the kinetic energy of the medium contains a "
    "term 2 C (alpha omega_1 + beta omega_2 + gamma omega_3) coupling the "
    "angular velocity acquired during the propagation of light with the "
    "motion by which magnetic phenomena are explained.",
)
def calc_disturbed_vortex_energy(
    magnetic_force: np.ndarray,
    angular_velocity: np.ndarray,
    coupling_constant: float,
) -> float:
    """Coupling energy of the disturbed medium (Art. 824, eq. 3).

    Maxwell 1873, Art. 824: "The next step in our hypothesis is the
    assumption that the kinetic energy of the medium contains a term of
    the form

        2 C (alpha omega_1 + beta omega_2 + gamma omega_3)         (3)

    This is equivalent to supposing that the angular velocity acquired by
    the element of the medium during the propagation of light is a
    quantity which may enter into combination with that motion by which
    magnetic phenomena are explained."  Here (alpha, beta, gamma) are
    the components of the magnetic force and (omega_1, omega_2, omega_3)
    those of the angular velocity of the element.

    Args:
        magnetic_force: Magnetic force vector (alpha, beta, gamma).
        angular_velocity: Angular velocity vector of the disturbed
            element (from :func:`calc_vortex_angular_velocity`).
        coupling_constant: The constant C of the hypothesis.

    Returns:
        Coupling term 2 C (H . omega) of the kinetic energy density.
    """
    H = np.asarray(magnetic_force, dtype=float)
    omega = np.asarray(angular_velocity, dtype=float)
    return 2.0 * coupling_constant * float(np.dot(H, omega))


@maxwell_cite(
    825,
    part=4,
    theory_class="maxwell_original",
    description="Equation (5): the coupling term becomes 4 pi C "
    "(xi-dot u + eta-dot v + zeta-dot w) in terms of the electric current "
    "components u, v, w of Art. 607.",
)
def express_vortex_current_velocity(
    particle_velocity: np.ndarray,
    current_density: np.ndarray,
    coupling_constant: float,
) -> float:
    """Coupling energy in terms of current and velocity (Art. 825, eq. 5).

    Maxwell 1873, Art. 825: integrating by parts, the coupling part of
    the kinetic energy in unit of volume "may be written

        4 pi C (xi-dot u + eta-dot v + zeta-dot w)                 (5)

    where u, v, w are the components of the electric current as given in
    equations (E), Art. 607."  The hypothesis is therefore equivalent to
    the assumption that the velocity of a particle of the medium may
    enter into combination with the electric current.

    Args:
        particle_velocity: Particle velocity vector (xi-dot, eta-dot,
            zeta-dot).
        current_density: Electric current vector (u, v, w).
        coupling_constant: The constant C.

    Returns:
        Coupling energy density 4 pi C (v . J).
    """
    v = np.asarray(particle_velocity, dtype=float)
    J = np.asarray(current_density, dtype=float)
    return 4.0 * PI * coupling_constant * float(np.dot(v, J))


@maxwell_cite(
    826,
    part=4,
    theory_class="maxwell_original",
    description="Equation (9): for waves in planes normal to the magnetic "
    "force gamma along z, T = (1/2) rho (xi-dot^2 + eta-dot^2 + zeta-dot^2) "
    "+ C gamma (xi'' eta-dot - eta'' xi-dot).",
)
def calc_plane_wave_vortex_energy(
    density: float,
    coupling_constant: float,
    magnetic_force_gamma: float,
    velocity: np.ndarray,
    curvature: np.ndarray,
) -> float:
    """Kinetic energy density for a plane wave (Art. 826, eq. 9).

    Maxwell 1873, Art. 826: for waves in planes normal to the axis of z
    (the magnetic force gamma along z), the displacements are functions
    of z and t only, and the kinetic energy per unit volume becomes

        T = (1/2) rho (xi-dot^2 + eta-dot^2 + zeta-dot^2)
            + C gamma (xi'' eta-dot - eta'' xi-dot)                 (9)

    where primes denote d^2/dz^2.  For a circularly-polarized ray this
    expression reduces exactly to Art. 828 eq. (15),
    T = (1/2) rho r^2 n^2 - C gamma r^2 q^2 n.

    Args:
        density: Density rho of the medium.
        coupling_constant: The constant C.
        magnetic_force_gamma: Magnetic force gamma resolved along z.
        velocity: Velocity vector (xi-dot, eta-dot, zeta-dot).
        curvature: Curvature vector (xi'', eta'', zeta''); only the
            x and y components enter eq. (9).

    Returns:
        Kinetic energy density T per unit volume.
    """
    v = np.asarray(velocity, dtype=float)
    curv = np.asarray(curvature, dtype=float)
    translational = 0.5 * density * float(np.dot(v, v))
    coupling = (
        coupling_constant * magnetic_force_gamma * (curv[0] * v[1] - curv[1] * v[0])
    )
    return translational + coupling
