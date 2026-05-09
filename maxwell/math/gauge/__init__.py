"""Gauge transformation module — Maxwell's gauge freedom.

References:
    Part IV, Arts. 616-617: Gauge transformations and potentials.
"""

from maxwell.math.gauge.manager import (
    GaugeTransformation,
    analyze_gauge_transformations,
    apply_coulomb_gauge,
    apply_lorenz_gauge,
    transform_potentials,
    verify_gauge_condition,
)

__all__ = [
    "GaugeTransformation",
    "apply_coulomb_gauge",
    "apply_lorenz_gauge",
    "verify_gauge_condition",
    "transform_potentials",
    "analyze_gauge_transformations",
]
