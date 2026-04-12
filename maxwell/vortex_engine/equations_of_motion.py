"""maxwell.vortex_engine.equations_of_motion — Vortex dynamics (Arts. 827-828).

Equations of motion for the vortex lattice and the velocity
of circularly polarized rays in the vortex medium.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vortex_engine.vortex_lattice import MolecularVortex, VortexLattice

PI = np.pi


@dataclass
class VortexEquations:
    """System of equations governing vortex motion (Arts. 827-828)."""

    vortex: MolecularVortex
    ether_density: float
    elastic_constant: float

    @maxwell_cite(827, part=4, theory_class="maxwell_original")
    def derive_vortex_equations_of_motion(self) -> dict[str, str]:
        """Derive equations of motion for the vortex lattice.

        The equation of motion for a vortex in the ether:
            rho * d^2(xi)/dt^2 = mu * nabla^2(xi) + F_magnetic

        where xi is the displacement, rho is ether density,
        mu is the elastic constant, and F_magnetic is the
        force due to the magnetic vortex rotation.

        Returns:
            Equations dict.
        """
        return {
            "equation_of_motion": "rho * d^2(xi)/dt^2 = mu * nabla^2(xi) + F_magnetic",
            "magnetic_force": "F_magnetic = rho * omega x (d(xi)/dt)",
            "wave_equation": "nabla^2(E) = (rho/mu) * d^2(E)/dt^2",
            "wave_speed": "v = sqrt(mu/rho)",
        }

    @maxwell_cite(827, part=4, theory_class="maxwell_original")
    def solve_plane_wave(self, k: np.ndarray, omega: float) -> np.ndarray:
        """Solve for plane wave propagation in vortex medium.

        Args:
            k: Wave vector.
            omega: Angular frequency.

        Returns:
            Dispersion relation: omega(k).
        """
        c = np.sqrt(self.elastic_constant / self.ether_density)
        return c * np.linalg.norm(k)


@maxwell_cite(828, part=4, theory_class="maxwell_original")
def calc_vortex_circular_velocity(
    vortex: MolecularVortex,
    magnetic_field: float,
    wave_frequency: float,
) -> dict[str, float]:
    """Calculate velocity of circularly polarized ray in vortex medium.

    Art. 828: The vortex model predicts that right and left
    circularly polarized rays travel at different velocities,
    in agreement with Faraday's observations.

    The velocity difference arises because the vortex rotation
    adds to one circular component and subtracts from the other.

    Args:
        vortex: Representative vortex.
        magnetic_field: External magnetic field.
        wave_frequency: Frequency of the light wave.

    Returns:
        Velocities for right and left circular polarization.
    """
    c = 2.99792458e10  # speed of light in vacuum
    base_velocity = c  # in ether, v = c

    # The vortex rotation modifies the effective velocity
    # delta_v ~ omega_vortex / omega_wave
    delta_v = vortex.angular_velocity / wave_frequency * base_velocity * 0.001

    return {
        "v_right": base_velocity + delta_v,
        "v_left": base_velocity - delta_v,
        "velocity_split": 2 * delta_v,
    }
