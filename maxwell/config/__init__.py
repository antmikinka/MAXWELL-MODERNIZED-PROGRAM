"""maxwell.config — Physical constants, conventions, and configuration."""

from __future__ import annotations

from maxwell.config.constants import (
    UniversalConstants,
    CONST,
    C,
    C_APPROX,
    cgs_unit_of,
)

from maxwell.config.conventions import (
    PolarityConvention,
    ForceDirectionConvention,
    MagneticDirection,
    verify_austral_positive,
    apply_force_direction,
    magnetic_convention_summary,
    convert_pole_naming,
    right_hand_rule_direction,
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
