"""Philosophical analysis of Maxwell's theory.

References:
    Part IV, Arts. 865-866: Completeness of electromagnetic theory of light.
"""

from maxwell.philosophy.medium_check import (
    calc_wave_properties,
    calc_reflection_coefficient,
    verify_maxwell_relation,
    verify_wave_speed,
    analyze_theory_completeness,
    MediumProperties,
    WaveProperties,
)

__all__ = [
    "calc_wave_properties",
    "calc_reflection_coefficient",
    "verify_maxwell_relation",
    "verify_wave_speed",
    "analyze_theory_completeness",
    "MediumProperties",
    "WaveProperties",
]
