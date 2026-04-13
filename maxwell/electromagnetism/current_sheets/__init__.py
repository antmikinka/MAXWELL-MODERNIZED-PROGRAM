"""Current-Sheets — electromagnetic theory of surface current distributions.

Maxwell's theory of current-sheets (Ch XII, Arts. 647-674) provides
the mathematical framework for analyzing surface currents and their
electromagnetic fields. This is essential for understanding:

- Current distributions on conducting surfaces
- Magnetic shells and equivalent current sheets
- Surface impedance and boundary conditions
- Electromagnetic shielding

Category: A (maxwell_original) — Maxwell's theory of current-sheets.
"""

from __future__ import annotations

from maxwell.electromagnetism.current_sheets.sheet_theory import (
    CurrentSheet,
    MagneticShell,
    calc_sheet_field_discontinuity,
    calc_magnetic_shell_potential,
    calc_sheet_vector_potential,
    calc_sheet_inductance,
    verify_shell_equivalence,
    calc_sheet_interaction,
    CurrentSheetCalculator,
)

from maxwell.electromagnetism.current_sheets.surface_currents import (
    SurfaceCurrentDensity,
    calc_surface_current,
    calc_field_from_surface_current,
    calc_sheet_boundary_condition,
    analyze_surface_current_distribution,
    calc_surface_impedance,
    SurfaceCurrentAnalyzer,
)

from maxwell.electromagnetism.current_sheets.boundary_conditions import (
    ElectromagneticBoundary,
    calc_tangential_E_discontinuity,
    calc_normal_B_continuity,
    calc_normal_D_discontinuity,
    calc_tangential_H_discontinuity,
    verify_boundary_conditions,
    calc_moving_boundary_conditions,
    calc_boundary_energy_flux,
    BoundaryConditionAnalyzer,
)

__all__ = [
    # Current Sheet Theory (Arts. 647-655)
    "CurrentSheet",
    "MagneticShell",
    "calc_sheet_field_discontinuity",
    "calc_magnetic_shell_potential",
    "calc_sheet_vector_potential",
    "calc_sheet_inductance",
    "verify_shell_equivalence",
    "calc_sheet_interaction",
    "CurrentSheetCalculator",
    # Surface Currents (Arts. 656-662)
    "SurfaceCurrentDensity",
    "calc_surface_current",
    "calc_field_from_surface_current",
    "calc_sheet_boundary_condition",
    "analyze_surface_current_distribution",
    "calc_surface_impedance",
    "SurfaceCurrentAnalyzer",
    # Boundary Conditions (Arts. 663-674)
    "ElectromagneticBoundary",
    "calc_tangential_E_discontinuity",
    "calc_normal_B_continuity",
    "calc_normal_D_discontinuity",
    "calc_tangential_H_discontinuity",
    "verify_boundary_conditions",
    "calc_moving_boundary_conditions",
    "calc_boundary_energy_flux",
    "BoundaryConditionAnalyzer",
]
