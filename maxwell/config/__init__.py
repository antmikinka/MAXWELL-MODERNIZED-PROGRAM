"""maxwell.config — Physical constants, conventions, and configuration."""

from __future__ import annotations

from maxwell.config.constants import (
    C_APPROX,
    CONST,
    C,
    UniversalConstants,
    cgs_unit_of,
)
from maxwell.config.conventions import (
    ForceDirectionConvention,
    MagneticDirection,
    PolarityConvention,
    apply_force_direction,
    convert_pole_naming,
    magnetic_convention_summary,
    right_hand_rule_direction,
    verify_austral_positive,
)

__all__ = [
    # Constants
    "UniversalConstants",
    "CONST",
    "C",
    "C_APPROX",
    "cgs_unit_of",
    # Conventions
    "PolarityConvention",
    "ForceDirectionConvention",
    "MagneticDirection",
    "verify_austral_positive",
    "apply_force_direction",
    "magnetic_convention_summary",
    "convert_pole_naming",
    "right_hand_rule_direction",
]
