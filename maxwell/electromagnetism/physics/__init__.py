"""Physics module — Maxwell stress tensor and field stress analysis.

References:
    Part IV, Art. 501: Electromagnetic stress and field tension.
"""

from maxwell.electromagnetism.physics.stress import (
    MaxwellStress,
    analyze_stress,
    calc_force_from_stress,
    calc_stress_on_plane,
    calc_stress_tensor,
    verify_electric_stress,
    verify_stress_tensor,
)

__all__ = [
    "MaxwellStress",
    "calc_stress_tensor",
    "calc_force_from_stress",
    "calc_stress_on_plane",
    "verify_stress_tensor",
    "verify_electric_stress",
    "analyze_stress",
]
