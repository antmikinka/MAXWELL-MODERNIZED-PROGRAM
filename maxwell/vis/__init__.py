"""maxwell.vis — Visualization for Maxwell's electromagnetic computations.

Provides publication-quality plotting for electrostatic fields, equipotential
surfaces, magnetic field lines, and Maxwell stress tensor visualization.

All modules gracefully degrade when matplotlib is not installed.
Install with: pip install maxwell[viz]

Submodules:
    _compat      — Safe matplotlib import with graceful degradation
    _base        — Shared grid and axis utilities
    field_lines  — Electric and magnetic field line plotting
    equipotential — Equipotential contour plotting
    stress       — Maxwell stress tensor visualization
"""

from __future__ import annotations

from maxwell.vis._compat import HAS_MATPLOTLIB

__all__ = [
    "HAS_MATPLOTLIB",
]

if HAS_MATPLOTLIB:
    from maxwell.vis._base import create_meshgrid, evaluate_on_grid
    from maxwell.vis.field_lines import plot_field_lines_2d
    from maxwell.vis.equipotential import plot_equipotentials_2d
    from maxwell.vis.stress import plot_stress_tensor_2d

    __all__ += [
        "create_meshgrid",
        "evaluate_on_grid",
        "plot_field_lines_2d",
        "plot_equipotentials_2d",
        "plot_stress_tensor_2d",
    ]
