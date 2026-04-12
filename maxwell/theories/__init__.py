"""Competing theory failure analysis.

References:
    Part IV, Arts. 857-859: Comparison with alternative theories.
"""

from maxwell.theories.failure_modes import (
    analyze_action_at_distance_failure,
    analyze_weber_failure,
    analyze_mechanical_ether_failure,
    verify_maxwell_supremacy,
    analyze_failure_modes,
    TheoryResult,
)

__all__ = [
    "analyze_action_at_distance_failure",
    "analyze_weber_failure",
    "analyze_mechanical_ether_failure",
    "verify_maxwell_supremacy",
    "analyze_failure_modes",
    "TheoryResult",
]
