"""maxwell.electromagnetism.potentials — Magnetic potentials (Arts. 480-487).

Package for magnetic potential calculations including multivalued potentials,
equipotential surfaces, and mutual energy.
"""

from maxwell.electromagnetism.potentials.directrix import (
    DirectrixFunction,
    analyze_directrix,
    calc_directrix_straight_wire,
    calc_field_from_potential,
    calc_vector_potential_element,
    verify_directrix_relations,
)
from maxwell.electromagnetism.potentials.multivalued import (
    CyclicPotential,
    analyze_cyclic_potential,
    calc_cyclic_potential,
    calc_potential_difference,
    calc_work_on_magnetic_pole,
    determine_branch,
    verify_cyclic_potential,
)
from maxwell.electromagnetism.potentials.mutual_energy import (
    MutualEnergy,
    analyze_mutual_energy,
    calc_force_between_circuits,
    calc_mutual_energy,
    calc_mutual_inductance_coaxial_loops,
    calc_neumann_mutual_inductance,
    verify_mutual_energy_relations,
)
from maxwell.electromagnetism.potentials.surfaces import (
    CurrentLoopPotential,
    EquipotentialSurface,
    analyze_equipotential_surfaces,
    calc_dipole_field,
    calc_dipole_potential,
    calc_magnetic_potential,
    calc_solid_angle_circular_loop,
    verify_equipotential_surfaces,
)

__all__ = [
    # Multivalued (Art. 480)
    "CyclicPotential",
    "calc_cyclic_potential",
    "calc_potential_difference",
    "verify_cyclic_potential",
    "calc_work_on_magnetic_pole",
    "determine_branch",
    "analyze_cyclic_potential",
    # Surfaces (Arts. 486-487)
    "EquipotentialSurface",
    "CurrentLoopPotential",
    "calc_solid_angle_circular_loop",
    "calc_magnetic_potential",
    "calc_dipole_potential",
    "calc_dipole_field",
    "verify_equipotential_surfaces",
    "analyze_equipotential_surfaces",
    # Mutual Energy (Arts. 520-521)
    "MutualEnergy",
    "calc_neumann_mutual_inductance",
    "calc_mutual_energy",
    "calc_force_between_circuits",
    "calc_mutual_inductance_coaxial_loops",
    "verify_mutual_energy_relations",
    "analyze_mutual_energy",
    # Directrix (Arts. 517-519)
    "DirectrixFunction",
    "calc_vector_potential_element",
    "calc_field_from_potential",
    "calc_directrix_straight_wire",
    "verify_directrix_relations",
    "analyze_directrix",
]
