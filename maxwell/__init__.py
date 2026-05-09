"""
maxwell — A Modern Computational Implementation of Maxwell's Treatise
======================================================================

James Clerk Maxwell's *A Treatise on Electricity and Magnetism* (1873),
modernized into a computational physics library.

Coverage:
    Part I   — Electrostatics       (Arts. 27–229)
    Part II  — Electrokinematics    (Arts. 230–370)
    Part III — Magnetism            (Arts. 371–474)
    Part IV  — Electromagnetism     (Arts. 475–866)

Total: 866 articles, 283+ modules, 80+ subpackages.

Unit System: CGS (centimeter-gram-second) primary, SI secondary.
Citation:  Every function is traceable to a Maxwell article via @maxwell_cite.

Quick Start
-----------
>>> from maxwell import PointCharge, LorentzForce, FaradayInduction
>>> from maxwell import MaxwellEquations, ElectromagneticField
>>> from maxwell import CONST, C
>>> print(f"c = {C:.4e} cm/s")
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Maxwell Modernization Project"

# ── Constants and units ───────────────────────────────────────────────
from maxwell.config.constants import CONST, C

# ── Core primitives ───────────────────────────────────────────────────
from maxwell.core.charge import PointCharge
from maxwell.core.field import ElectricField
from maxwell.core.magnet import Magnet
from maxwell.core.moment import MagneticMoment
from maxwell.core.potential import ElectricPotential
from maxwell.core.units import CGSUnitConverter, MagneticDimensions

# ── Electrokinematics ─────────────────────────────────────────────────
from maxwell.electrokinematics.network_solver import NetworkAnalyzer
from maxwell.electromagnetism.energy.electrostatic import (
    calc_electrostatic_energy_density,
)

# ── Electromagnetism — Energy ─────────────────────────────────────────
from maxwell.electromagnetism.energy.magnetic import (
    calc_magnetic_energy_density,
    calc_total_magnetic_energy,
)

# ── Electromagnetism — Fields ─────────────────────────────────────────
from maxwell.electromagnetism.fields.ampere_maxwell import (
    AmpereMaxwellLaw,
    DisplacementCurrent,
)

# ── Electromagnetism — Forces ────────────────────────────────────────
from maxwell.electromagnetism.forces.lorentz import LorentzForce
from maxwell.electromagnetism.forces.stress_tensor import MaxwellStressTensor

# ── Electromagnetism — Induction ──────────────────────────────────────
from maxwell.electromagnetism.induction.faraday import FaradayInduction

# ── Electromagnetism — Theory ─────────────────────────────────────────
from maxwell.electromagnetism.theory.general_equations import (
    ElectromagneticField,
    MaxwellEquations,
)

# ── Electrostatics ────────────────────────────────────────────────────
from maxwell.electrostatics.dielectrics import DielectricMaterial

# ── Engineering ───────────────────────────────────────────────────────
from maxwell.engineering import MagneticCompass, ShipMagnetism

# ── Instruments ───────────────────────────────────────────────────────
from maxwell.instruments.galvanometers import TangentGalvanometer
from maxwell.instruments.helmholtz import HelmholtzCoil

# ── Magnetism ─────────────────────────────────────────────────────────
from maxwell.magnetism.terrestrial_magnetism import GeomagneticElements

# ── Materials ─────────────────────────────────────────────────────────
from maxwell.materials.constitutive import (
    Conductivity,
    ElectricDisplacement,
    Magnetization,
    Permeability,
)
from maxwell.materials.hysteresis import HysteresisLoop
from maxwell.math.elliptic_integrals import EllipticIntegral

# ── Mathematics ───────────────────────────────────────────────────────
from maxwell.math.spherical_harmonics import (
    LegendrePolynomial,
    SphericalHarmonicExpansion,
)

# ── Citation System ───────────────────────────────────────────────────
from maxwell.meta.citation import get_all_citations, get_citation

# ── Competing Theories ────────────────────────────────────────────────
from maxwell.molecular.competing_theories import CompetingTheory

# ── Optics ────────────────────────────────────────────────────────────
from maxwell.optics.wave_equation import PlaneWave

__all__ = [
    # Version
    "__version__",
    # Core primitives
    "PointCharge",
    "ElectricField",
    "ElectricPotential",
    "Magnet",
    "MagneticMoment",
    # Constants and units
    "CONST",
    "C",
    "CGSUnitConverter",
    "MagneticDimensions",
    # Forces
    "LorentzForce",
    "MaxwellStressTensor",
    # Induction
    "FaradayInduction",
    # Theory
    "MaxwellEquations",
    "ElectromagneticField",
    # Energy
    "calc_magnetic_energy_density",
    "calc_total_magnetic_energy",
    "calc_electrostatic_energy_density",
    # Fields
    "AmpereMaxwellLaw",
    "DisplacementCurrent",
    # Electrostatics
    "DielectricMaterial",
    # Electrokinematics
    "NetworkAnalyzer",
    # Magnetism
    "GeomagneticElements",
    # Optics
    "PlaneWave",
    # Mathematics
    "SphericalHarmonicExpansion",
    "LegendrePolynomial",
    "EllipticIntegral",
    # Instruments
    "TangentGalvanometer",
    "HelmholtzCoil",
    # Materials
    "Magnetization",
    "ElectricDisplacement",
    "Conductivity",
    "Permeability",
    "HysteresisLoop",
    # Engineering
    "ShipMagnetism",
    "MagneticCompass",
    # Competing Theories
    "CompetingTheory",
    # Citation
    "get_citation",
    "get_all_citations",
]
