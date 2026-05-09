"""maxwell.vortex_engine — Molecular vortex theory (Arts. 822-831).

Maxwell's mechanical model of the ether: molecular vortices
whose rotation produces magnetic phenomena and whose
disturbances explain Faraday rotation and light propagation.
"""

from __future__ import annotations

from maxwell.vortex_engine.equations_of_motion import (
    VortexEquations,
    calc_vortex_circular_velocity,
)
from maxwell.vortex_engine.helmholtz_law import (
    apply_helmholtz_vortex_law,
    calc_vortex_stretching,
)
from maxwell.vortex_engine.kinetic_energy import (
    calc_disturbed_vortex_energy,
    calc_plane_wave_vortex_energy,
    express_vortex_current_velocity,
)
from maxwell.vortex_engine.magnetic_rotation import (
    compare_verdet_data,
    derive_magnetic_rotation,
)
from maxwell.vortex_engine.vortex_lattice import (
    MolecularVortex,
    VortexLattice,
    append_mechanical_theory_notes,
)

__all__ = [
    # Vortex lattice (Arts. 822-824, 831)
    "MolecularVortex",
    "VortexLattice",
    "append_mechanical_theory_notes",
    # Helmholtz law (Art. 823)
    "apply_helmholtz_vortex_law",
    "calc_vortex_stretching",
    # Kinetic energy (Arts. 824-826)
    "calc_disturbed_vortex_energy",
    "express_vortex_current_velocity",
    "calc_plane_wave_vortex_energy",
    # Equations of motion (Arts. 827-828)
    "VortexEquations",
    "calc_vortex_circular_velocity",
    # Magnetic rotation (Arts. 829-831)
    "derive_magnetic_rotation",
    "compare_verdet_data",
]
