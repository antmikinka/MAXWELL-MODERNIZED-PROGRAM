"""
maxwell.geometry — Magnetic solenoids and shells.

This subpackage implements the geometry of magnetic distributions:
- Solenoids: tubular magnetic distributions (solenoids.py, Arts. 407-408, 414)
- Shells: surface distributions of dipoles (shells.py, Arts. 409-411)

Category: A (maxwell_original) — Maxwell's magnetic geometry.
"""

from __future__ import annotations

from maxwell.geometry.solenoids import (
    Solenoid,
    ComplexSolenoid,
    solenoid_potential,
)

from maxwell.geometry.shells import (
    MagneticShell,
    shell_potential,
    shell_potential_alternative_proof,
    shell_potential_discontinuity,
    shell_current_equivalence,
    work_moving_shell_in_field,
)

__all__ = [
    # Solenoids (Arts. 407-408, 414)
    "Solenoid",
    "ComplexSolenoid",
    "solenoid_potential",
    # Shells (Arts. 409-411)
    "MagneticShell",
    "shell_potential",
    "shell_potential_alternative_proof",
    "shell_potential_discontinuity",
    "shell_current_equivalence",
    "work_moving_shell_in_field",
]
