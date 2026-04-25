"""
maxwell.engineering — Engineering applications of magnetic theory.

This subpackage implements engineering applications from Maxwell's Treatise:
- Naval magnetism and compass deviation (naval.py, Art. 441)
- Magnetic shielding
- Industrial magnetic applications

Category: A (maxwell_original) — Maxwell's engineering applications.
"""

from __future__ import annotations

from maxwell.engineering.naval import (
    ShipMagnetism,
    MagneticCompass,
    flinders_bar_correction,
    quadrantal_correctors,
    simulate_compass_swinging,
    verify_naval_magnetism,
)

__all__ = [
    # Naval Magnetism (Art. 441)
    "ShipMagnetism",
    "MagneticCompass",
    "flinders_bar_correction",
    "quadrantal_correctors",
    "simulate_compass_swinging",
    "verify_naval_magnetism",
]
