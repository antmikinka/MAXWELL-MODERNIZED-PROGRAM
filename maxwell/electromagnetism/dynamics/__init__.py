"""maxwell.electromagnetism.dynamics — Dynamics of electromagnetic systems (Arts. 496-497).

Package for dynamic interactions in electromagnetic systems, including
forces between current-carrying conductors.
"""

from maxwell.electromagnetism.dynamics.attraction import (
    ParallelConductorForce,
    calc_force_parallel_wires,
    calc_force_per_unit_length,
    calc_force_inclined_wires,
    calc_force_between_elements,
    calc_equilibrium_current,
    verify_parallel_force_law,
    calc_work_parallel_wires,
    analyze_parallel_conductor_forces,
)

__all__ = [
    # Parallel conductor forces (Arts. 496-497)
    "ParallelConductorForce",
    "calc_force_parallel_wires",
    "calc_force_per_unit_length",
    "calc_force_inclined_wires",
    "calc_force_between_elements",
    "calc_equilibrium_current",
    "verify_parallel_force_law",
    "calc_work_parallel_wires",
    "analyze_parallel_conductor_forces",
]
