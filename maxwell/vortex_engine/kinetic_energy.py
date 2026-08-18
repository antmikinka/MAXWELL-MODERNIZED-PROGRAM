"""maxwell.vortex_engine.kinetic_energy — Disturbed medium energy (Arts. 824-826).

Kinetic energy of the disturbed vortex medium, expressed in
terms of current and velocity, for plane waves.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vortex_engine.vortex_lattice import MolecularVortex, VortexLattice


@maxwell_cite(824, part=4, theory_class="maxwell_original")
def calc_disturbed_vortex_energy(
    lattice: VortexLattice,
    perturbation: np.ndarray,
) -> float:
    """Calculate energy of the disturbed vortex medium.

    When the vortex lattice is disturbed (e.g., by a passing
    electromagnetic wave), the energy changes. The disturbance
    modifies both the kinetic energy of rotation and the
    translational energy of the vortex centers.

    Args:
        lattice: The vortex lattice.
        perturbation: Displacement perturbation vector.

    Returns:
        Total energy of the disturbed medium.
    """
    # Base energy
    base_energy = lattice.total_kinetic_energy()

    # Disturbance energy: proportional to perturbation^2
    perturbation_energy = 0.5 * np.dot(perturbation, perturbation)

    return base_energy + perturbation_energy


@maxwell_cite(825, part=4, theory_class="maxwell_original")
def express_vortex_current_velocity(
    vortex: MolecularVortex,
    current_density: np.ndarray,
) -> dict[str, float]:
    """Express vortex energy in terms of current and velocity.

    Art. 825: The energy of the disturbed medium can be
    expressed in terms of the electric current (motion of
    idle-wheel particles) and the vortex velocity.

    Args:
        vortex: The vortex.
        current_density: Electric current density vector.

    Returns:
        Energy components dict.
    """
    # In Maxwell's model, J ~ rho_idle * v_idle
    # And the vortex angular velocity omega ~ H
    # The coupling energy is proportional to J . A

    H_field = vortex.magnetic_field_equivalent()

    return {
        "vortex_energy": vortex.kinetic_energy(),
        "coupling_energy": np.dot(current_density, vortex.axis) * H_field,
        "total": vortex.kinetic_energy()
        + np.dot(current_density, vortex.axis) * H_field,
    }


@maxwell_cite(826, part=4, theory_class="maxwell_original")
def calc_plane_wave_vortex_energy(
    vortex: MolecularVortex,
    wave_amplitude: float,
    wave_frequency: float,
) -> float:
    """Calculate kinetic energy for plane wave disturbance.

    Art. 826: For a plane wave passing through the vortex
    lattice, the energy oscillates between kinetic (vortex
    rotation) and potential (ether elasticity).

    Args:
        vortex: Representative vortex in the lattice.
        wave_amplitude: Amplitude of the plane wave.
        wave_frequency: Angular frequency of the wave.

    Returns:
        Average kinetic energy per vortex.
    """
    # The wave modulates the vortex angular velocity:
    # omega(t) = omega_0 + delta_omega * cos(wt)
    # Average kinetic energy = (1/4) * rho * (omega_0^2 + delta_omega^2/2) * r^4

    base_energy = vortex.kinetic_energy()
    # delta_omega proportional to wave amplitude
    delta_omega = wave_amplitude * wave_frequency
    perturbation_energy = 0.25 * vortex.density * delta_omega**2 * vortex.radius**4 / 2

    return base_energy + perturbation_energy
