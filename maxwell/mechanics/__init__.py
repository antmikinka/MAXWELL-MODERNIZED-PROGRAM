"""
maxwell.mechanics — Magnetic energy, forces, and torques.

This subpackage implements the mechanics of magnetic systems:
- Dipole potential energy W = -m·B (potential_energy.py, Art. 389)
- Shell energy and work in external fields (shell_energy.py, Art. 423)

Category: A (maxwell_original) — Maxwell's magnetic mechanics.
"""

from __future__ import annotations

from maxwell.mechanics.potential_energy import (
    MagneticPotentialEnergy,
    calc_dipole_potential_energy,
    energy_of_magnetized_body,
    force_on_dipole,
    stable_equilibrium_orientation,
    torque_on_dipole,
    work_rotating_dipole,
)
from maxwell.mechanics.shell_energy import (
    ShellEnergy,
    calc_shell_potential_energy,
    compute_shell_flux,
    force_on_shell,
    shell_equilibrium_orientation,
    torque_on_shell,
    work_moving_shell,
)

__all__ = [
    # Dipole Energy (Art. 389)
    "MagneticPotentialEnergy",
    "calc_dipole_potential_energy",
    "work_rotating_dipole",
    "torque_on_dipole",
    "force_on_dipole",
    "stable_equilibrium_orientation",
    "energy_of_magnetized_body",
    # Shell Energy (Art. 423)
    "ShellEnergy",
    "calc_shell_potential_energy",
    "compute_shell_flux",
    "work_moving_shell",
    "force_on_shell",
    "torque_on_shell",
    "shell_equilibrium_orientation",
]
