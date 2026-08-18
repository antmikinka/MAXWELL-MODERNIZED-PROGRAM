"""maxwell.vis -- Visualization for Maxwell's electromagnetic computations.

Provides publication-quality plotting for electrostatic fields, equipotential
surfaces, magnetic field lines, Maxwell stress tensor visualization, method
of images, edge singularity analysis, dielectric soakage, hysteresis loops,
electromagnetic wave propagation, magnetic shells, and spherical harmonics.

All modules gracefully degrade when matplotlib is not installed.
Install with: pip install maxwell[viz]

Submodules:
    _compat               -- Safe matplotlib import with graceful degradation
    _base                 -- Shared grid and axis utilities
    field_lines           -- Electric and magnetic field line plotting
    equipotential         -- Equipotential contour plotting
    stress                -- Maxwell stress tensor visualization
    method_of_images      -- Method of Images (Art. 155) visualization
    edge_singularities    -- Conducting edge field singularities (Art. 191)
    dielectric_soakage    -- Dielectric absorption current decay (Art. 329)
    hysteresis_loops      -- Magnetic hysteresis B-H loops (Arts. 442-446)
    em_wave_propagation   -- EM wave propagation and polarization (Art. 791)
    magnetic_shell        -- Magnetic shell and solid angle (Art. 409)
    spherical_harmonics   -- Spherical harmonic globes (Art. 467)
    flow_tubes            -- Unit tubes of flow (Art. 290)
    thermal_gradients     -- Joule heating and thermoelectric effects (Arts. 242, 249)
    molecular_vortices    -- Molecular vortex lattice (Arts. 822-824)
    helicoidal_potentials -- Helicoidal potential surfaces (Arts. 486-487)
    electrotonic_state    -- Electrotonic state / vector potential (Arts. 540, 617)
"""

from __future__ import annotations

from maxwell.vis._compat import HAS_MATPLOTLIB

__all__ = [
    "HAS_MATPLOTLIB",
]

if HAS_MATPLOTLIB:
    from maxwell.vis._base import create_meshgrid, evaluate_on_grid
    from maxwell.vis.dielectric_soakage import (
        calc_dielectric_absorption,
        plot_dielectric_soakage,
    )
    from maxwell.vis.edge_singularities import (
        calc_edge_singularity,
        calc_wedge_field,
        plot_edge_singularity,
        plot_singularity_comparison,
    )
    from maxwell.vis.electrotonic_state import (
        calc_B_from_electrotonic,
        calc_electrotonic_straight_wire,
        calc_electrotonic_transient,
        plot_A_and_B_fields,
        plot_A_transient,
        plot_electrotonic_3d_surface,
        plot_electrotonic_state_2d,
    )
    from maxwell.vis.em_wave_propagation import (
        calc_em_wave,
        plot_em_wave_propagation,
        plot_wave_snapshot_3d,
    )
    from maxwell.vis.equipotential import (
        plot_dipole_equipotentials,
        plot_equipotentials_2d,
    )
    from maxwell.vis.field_lines import (
        plot_dipole_field_lines,
        plot_field_lines_2d,
    )
    from maxwell.vis.flow_tubes import (
        calc_unit_tubes,
        plot_unit_tubes_3d,
        plot_unit_tubes_of_flow,
    )
    from maxwell.vis.helicoidal_potentials import (
        calc_solid_angle_loop,
        plot_helicoidal_potentials,
        plot_loop_field_lines,
        plot_loop_potential_3d,
    )
    from maxwell.vis.hysteresis_loops import (
        calc_hysteresis_loop,
        plot_hysteresis_loops,
        plot_material_comparison,
    )
    from maxwell.vis.magnetic_shell import (
        calc_shell_potential,
        calc_solid_angle,
        plot_magnetic_shell,
        plot_shell_potential,
    )
    from maxwell.vis.method_of_images import (
        calc_method_of_images,
        plot_method_of_images,
    )
    from maxwell.vis.molecular_vortices import (
        calc_magnetic_field_from_vortices,
        calc_vortex_lattice,
        plot_molecular_vortices,
        plot_vortex_3d_surface,
    )
    from maxwell.vis.spherical_harmonics import (
        calc_field_intensity,
        calc_gauss_harmonics,
        plot_harmonic_contour,
        plot_harmonic_globe,
        plot_harmonic_modes,
    )
    from maxwell.vis.stress import (
        plot_stress_tensor_2d,
        verify_stress_tensor_plot,
    )
    from maxwell.vis.thermal_gradients import (
        calc_joule_heat_distribution,
        calc_peltier_junction,
        calc_thermal_gradients,
        plot_joule_heat_distribution,
        plot_thermal_gradients,
        plot_thermoelectric_effects,
    )

    __all__ += [
        "create_meshgrid",
        "evaluate_on_grid",
        "plot_field_lines_2d",
        "plot_dipole_field_lines",
        "plot_equipotentials_2d",
        "plot_dipole_equipotentials",
        "plot_stress_tensor_2d",
        "verify_stress_tensor_plot",
        "calc_method_of_images",
        "plot_method_of_images",
        "calc_wedge_field",
        "calc_edge_singularity",
        "plot_edge_singularity",
        "plot_singularity_comparison",
        "calc_dielectric_absorption",
        "plot_dielectric_soakage",
        "calc_hysteresis_loop",
        "plot_hysteresis_loops",
        "plot_material_comparison",
        "calc_em_wave",
        "plot_em_wave_propagation",
        "plot_wave_snapshot_3d",
        "calc_solid_angle",
        "calc_shell_potential",
        "plot_magnetic_shell",
        "plot_shell_potential",
        "calc_gauss_harmonics",
        "calc_field_intensity",
        "plot_harmonic_globe",
        "plot_harmonic_modes",
        "plot_harmonic_contour",
        "calc_unit_tubes",
        "plot_unit_tubes_of_flow",
        "plot_unit_tubes_3d",
        "calc_joule_heat_distribution",
        "calc_thermal_gradients",
        "calc_peltier_junction",
        "plot_thermal_gradients",
        "plot_joule_heat_distribution",
        "plot_thermoelectric_effects",
        "calc_vortex_lattice",
        "calc_magnetic_field_from_vortices",
        "plot_molecular_vortices",
        "plot_vortex_3d_surface",
        "calc_solid_angle_loop",
        "plot_helicoidal_potentials",
        "plot_loop_potential_3d",
        "plot_loop_field_lines",
        "calc_electrotonic_straight_wire",
        "calc_electrotonic_transient",
        "calc_B_from_electrotonic",
        "plot_electrotonic_state_2d",
        "plot_A_and_B_fields",
        "plot_A_transient",
        "plot_electrotonic_3d_surface",
    ]
