"""maxwell.materials.constitutive — Constitutive relations (Arts. 605, 608, 609, 614).

Package for Maxwell's constitutive relations describing material properties:
- Magnetization (Art. 605): B = H + 4πI = μH
- Electric displacement (Art. 608): D = εE = E + 4πP
- Conductivity (Art. 609): J = σE
- Permeability (Art. 614): B = μH
"""

from maxwell.materials.constitutive.magnetization import (
    Magnetization,
    calc_magnetic_induction,
    calc_magnetization_intensity,
    calc_permeability,
    calc_susceptibility,
    calc_magnetic_moment,
    verify_magnetization,
    analyze_magnetization,
)

from maxwell.materials.constitutive.displacement import (
    ElectricDisplacement,
    calc_electric_displacement,
    calc_displacement,  # Alias for test compatibility
    calc_polarization,
    calc_permittivity_from_susceptibility,
    calc_dielectric_constant,
    calc_bound_charge_density,
    verify_displacement_relations,
    analyze_displacement,
)

from maxwell.materials.constitutive.conductivity import (
    Conductivity,
    calc_conduction_current,
    calc_current_density,  # Alias for test compatibility
    calc_wire_current,
    calc_resistance,
    calc_conductance,
    calc_power_dissipation_conduction,
    calc_conductivity_from_resistivity,
    verify_conduction_relations,
    analyze_conduction,
)

from maxwell.materials.constitutive.permeability import (
    Permeability,
    calc_magnetic_induction_permeability,
    calc_B_from_H,  # Alias for test compatibility
    calc_permeability_from_k,
    calc_k_from_permeability,
    calc_magnetic_energy_density,
    classify_material_by_permeability,
    calc_magnetic_flux,
    verify_permeability_relations,
    analyze_permeability,
    VACUUM_PERMEABILITY,  # Constant for test compatibility
)

__all__ = [
    # Magnetization (Art. 605)
    "Magnetization",
    "calc_magnetic_induction",
    "calc_magnetization_intensity",
    "calc_permeability",
    "calc_susceptibility",
    "calc_magnetic_moment",
    "verify_magnetization",
    "analyze_magnetization",
    # Electric displacement (Art. 608)
    "ElectricDisplacement",
    "calc_electric_displacement",
    "calc_displacement",  # Alias for test compatibility
    "calc_polarization",
    "calc_permittivity_from_susceptibility",
    "calc_dielectric_constant",
    "calc_bound_charge_density",
    "verify_displacement_relations",
    "analyze_displacement",
    # Conductivity (Art. 609)
    "Conductivity",
    "calc_conduction_current",
    "calc_current_density",  # Alias for test compatibility
    "calc_wire_current",
    "calc_resistance",
    "calc_conductance",
    "calc_power_dissipation_conduction",
    "calc_conductivity_from_resistivity",
    "verify_conduction_relations",
    "analyze_conduction",
    # Permeability (Art. 614)
    "Permeability",
    "calc_magnetic_induction_permeability",
    "calc_B_from_H",  # Alias for test compatibility
    "calc_permeability_from_k",
    "calc_k_from_permeability",
    "calc_magnetic_energy_density",
    "classify_material_by_permeability",
    "calc_magnetic_flux",
    "verify_permeability_relations",
    "analyze_permeability",
    "VACUUM_PERMEABILITY",  # Constant for test compatibility
]
