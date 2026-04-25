"""
maxwell — A Modern Computational Implementation of Maxwell's Treatise
======================================================================

James Clerk Maxwell's *A Treatise on Electricity and Magnetism* (1873),
modernized into a computational physics library.

Coverage:
    Part I   — Electrostatics       (Arts. 27–229,   Layers 0–12)
    Part II  — Electrokinematics    (Arts. 230–370,  Layers 13–30)
    Part III — Magnetism            (Arts. 371–474,  Layers 30b–42)
    Part IV  — Electromagnetism     (Arts. 475–866,  Layers 43–86)
    Part V   — System Core          (Meta-layer,     Layers 90–94)
    Part VI  — Scalar Physics       (Extension,      Layers 95–97)

Total: 885+ articles, 80+ layers, 200+ modules.

Unit System: CGS (centimeter-gram-second) primary, SI secondary.
Citation:  Every function is traceable to a Maxwell article via @maxwell_cite.

Examples
--------
>>> from maxwell.core.units import MagneticDimensions
>>> from maxwell.config.constants import C
>>> from maxwell.fields.force import MagneticForce
"""

__version__ = "0.1.0"
__author__ = "Maxwell Modernization Project"
__all__ = ["__version__"]
