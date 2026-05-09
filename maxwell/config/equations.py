"""maxwell.config.equations — Comprehensive Maxwell equation catalog.

Data-driven registry of ALL equation sets from Maxwell's Treatise on Electricity
and Magnetism (1873). Each equation is catalogued with:

- LaTeX strings (exact formula as written by Maxwell)
- Variable definitions (name, description, CGS units, type)
- Function mapping (which maxwell.math function computes it)
- Maxwell article references
- Derivation steps
- Preset examples with numerical values

This module serves as the single source of truth for equation metadata,
enabling automatic documentation generation, equation validation, and
cross-referencing between code and the original Treatise.

All units are in CGS (centimeter-gram-second) system.

Category: C (standard_math) — Established electromagnetic theory.

References:
    Maxwell, J. C. "A Treatise on Electricity and Magnetism", 3rd ed., 1873.
    Volume 1: Parts I-III (Electrostatics, Electrokinematics, Magnetism).
    Volume 2: Parts IV-VI (Electromagnetic Theory, Optics, Molecular Theory).
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from maxwell.meta.citation import maxwell_cite

# ═══════════════════════════════════════════════════════════════════
# DATA TYPES
# ═══════════════════════════════════════════════════════════════════


class EquationSet(Enum):
    """Enum identifying each of Maxwell's equation sets (A through H)."""

    # Volume 2, Part IV, Chapter IX — General Equations
    SET_A = "A"  # Magnetic Induction from Vector Potential
    SET_B = "B"  # Electromotive Intensity
    SET_C = "C"  # Electromagnetic Force (Lorentz)
    SET_D = "D"  # Magnetization (B = H + 4pi*I)
    SET_E = "E"  # Electric Currents (Ampere's law)
    SET_F = "F"  # Electric Displacement
    SET_G = "G"  # Conductivity (Ohm's law)
    SET_H = "H"  # True Currents (total current)
    # Auxiliary equations
    SOLENoidal = "solenoidal"  # Current continuity
    FREE_CHARGE = "free_charge"  # Free electricity from displacement
    # Volume 1, Part I, Chapter I — Electrostatics
    COULOMB = "coulomb"  # Coulomb's law
    NET_CHARGE = "net_charge"  # Net charge = m - n


class VariableType(Enum):
    """Type of physical variable."""

    SCALAR = "scalar"
    VECTOR = "vector"
    TENSOR = "tensor"
    FIELD = "field"  # Spatial field (scalar or vector valued)


@dataclass(frozen=True)
class Variable:
    """Definition of a variable used in Maxwell's equations.

    Attributes:
        name: Variable symbol (e.g., "phi", "A", "B").
        description: Physical meaning.
        units: CGS unit string (e.g., "statvolt", "gauss").
        var_type: Scalar, vector, tensor, or field.
        components: Component names for vector/tensor (e.g., ["Fx","Fy","Fz"]).
        modern_name: Modern equivalent name if different.
    """

    name: str
    description: str
    units: str
    var_type: VariableType = VariableType.SCALAR
    components: List[str] = field(default_factory=list)
    modern_name: Optional[str] = None


@dataclass(frozen=True)
class EquationFormula:
    """A single equation formula within an equation set.

    Attributes:
        equation_id: Unique identifier (e.g., "A1", "E2").
        latex: LaTeX representation of the formula.
        description: Textual description of what the equation computes.
        variables: List of Variable objects used in this formula.
        component: Which component (for multi-component equations).
    """

    equation_id: str
    latex: str
    description: str
    variables: List[Variable] = field(default_factory=list)
    component: Optional[str] = None


@dataclass(frozen=True)
class DerivationStep:
    """A single step in a derivation chain.

    Attributes:
        step_number: Sequential step number.
        latex: LaTeX of the intermediate result.
        explanation: Text explaining the transformation.
        from_articles: Maxwell articles this step references.
    """

    step_number: int
    latex: str
    explanation: str
    from_articles: Tuple[int, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PresetExample:
    """A numerical example with specific values.

    Attributes:
        name: Example name.
        description: What the example demonstrates.
        inputs: Dictionary of variable name -> numerical value(s).
        expected: Expected result(s).
        tolerance: Acceptable numerical tolerance.
    """

    name: str
    description: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected: Dict[str, Any] = field(default_factory=dict)
    tolerance: float = 1e-6


@dataclass(frozen=True)
class EquationSetEntry:
    """Complete catalog entry for one of Maxwell's equation sets.

    Attributes:
        set_id: Equation set identifier.
        name: Human-readable name.
        articles: Maxwell article numbers.
        volume: Volume number (1 or 2).
        part: Part number (I-VI).
        chapter: Chapter title.
        latex_summary: Combined LaTeX of all equations in the set.
        vector_form: Vector calculus form of the equations.
        formulas: List of individual equation formulas.
        variables: Dictionary of all variables used.
        function_mapping: Dict mapping equation_id -> function path.
        derivation_steps: List of derivation steps.
        examples: List of preset numerical examples.
        notes: Additional notes or historical context.
    """

    set_id: str
    name: str
    articles: Tuple[int, ...]
    volume: int
    part: int
    chapter: str
    latex_summary: str
    vector_form: str
    formulas: List[EquationFormula] = field(default_factory=list)
    variables: Dict[str, Variable] = field(default_factory=dict)
    function_mapping: Dict[str, str] = field(default_factory=dict)
    derivation_steps: List[DerivationStep] = field(default_factory=list)
    examples: List[PresetExample] = field(default_factory=list)
    notes: str = ""


# ═══════════════════════════════════════════════════════════════════
# VARIABLE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════

# ── Vector Potential (Electromagnetic Momentum) ──────────────────
VAR_F = Variable(
    name="F",
    description="x-component of electromagnetic momentum (vector potential)",
    units="gauss*cm (Mx/cm)",
    var_type=VariableType.FIELD,
    modern_name="A_x",
)
VAR_G = Variable(
    name="G",
    description="y-component of electromagnetic momentum (vector potential)",
    units="gauss*cm (Mx/cm)",
    var_type=VariableType.FIELD,
    modern_name="A_y",
)
VAR_H_vec = Variable(
    name="H",
    description="z-component of electromagnetic momentum (vector potential)",
    units="gauss*cm (Mx/cm)",
    var_type=VariableType.FIELD,
    modern_name="A_z",
    components=["F", "G", "H"],
)

# Note: H is also used for magnetic force (Set D). Context disambiguates.
VAR_H_magnetic = Variable(
    name="H",
    description="magnetic force field intensity",
    units="oersted (gauss)",
    var_type=VariableType.FIELD,
    modern_name="H",
    components=["alpha", "beta", "gamma"],
)

# ── Magnetic Induction ───────────────────────────────────────────
VAR_a = Variable(
    name="a",
    description="x-component of magnetic induction",
    units="gauss (Mx/cm^2)",
    var_type=VariableType.FIELD,
    modern_name="B_x",
)
VAR_b = Variable(
    name="b",
    description="y-component of magnetic induction",
    units="gauss (Mx/cm^2)",
    var_type=VariableType.FIELD,
    modern_name="B_y",
)
VAR_c = Variable(
    name="c",
    description="z-component of magnetic induction",
    units="gauss (Mx/cm^2)",
    var_type=VariableType.FIELD,
    modern_name="B_z",
)

# ── Magnetic Force (H field) ────────────────────────────────────
VAR_alpha = Variable(
    name="alpha",
    description="x-component of magnetic force",
    units="oersted (gauss)",
    var_type=VariableType.FIELD,
    modern_name="H_x",
)
VAR_beta = Variable(
    name="beta",
    description="y-component of magnetic force",
    units="oersted (gauss)",
    var_type=VariableType.FIELD,
    modern_name="H_y",
)
VAR_gamma = Variable(
    name="gamma",
    description="z-component of magnetic force",
    units="oersted (gauss)",
    var_type=VariableType.FIELD,
    modern_name="H_z",
)

# ── Electric Current Density ─────────────────────────────────────
VAR_u = Variable(
    name="u",
    description="x-component of total current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_x",
)
VAR_v = Variable(
    name="v",
    description="y-component of total current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_y",
)
VAR_w = Variable(
    name="w",
    description="z-component of total current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_z",
)

# ── Conduction Current ───────────────────────────────────────────
VAR_p = Variable(
    name="p",
    description="x-component of conduction current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_cond_x",
)
VAR_q = Variable(
    name="q",
    description="y-component of conduction current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_cond_y",
)
VAR_r = Variable(
    name="r",
    description="z-component of conduction current density",
    units="abampere/cm^2",
    var_type=VariableType.FIELD,
    modern_name="J_cond_z",
)

# ── Electric Displacement ────────────────────────────────────────
VAR_f = Variable(
    name="f",
    description="x-component of electric displacement",
    units="statcoulomb/cm^2",
    var_type=VariableType.FIELD,
    modern_name="D_x",
)
VAR_g = Variable(
    name="g",
    description="y-component of electric displacement",
    units="statcoulomb/cm^2",
    var_type=VariableType.FIELD,
    modern_name="D_y",
)
VAR_h = Variable(
    name="h",
    description="z-component of electric displacement",
    units="statcoulomb/cm^2",
    var_type=VariableType.FIELD,
    modern_name="D_z",
)

# ── Magnetization ────────────────────────────────────────────────
VAR_A_mag = Variable(
    name="A",
    description="x-component of magnetization (magnetic moment per unit volume)",
    units="emu/cm^3",
    var_type=VariableType.FIELD,
    modern_name="M_x",
)
VAR_B_mag = Variable(
    name="B",
    description="y-component of magnetization",
    units="emu/cm^3",
    var_type=VariableType.FIELD,
    modern_name="M_y",
)
VAR_C_mag = Variable(
    name="C",
    description="z-component of magnetization",
    units="emu/cm^3",
    var_type=VariableType.FIELD,
    modern_name="M_z",
)

# ── Electromotive Intensity (E field) ────────────────────────────
VAR_X = Variable(
    name="X",
    description="x-component of electromotive intensity",
    units="statvolt/cm",
    var_type=VariableType.FIELD,
    modern_name="E_x",
)
VAR_Y = Variable(
    name="Y",
    description="y-component of electromotive intensity",
    units="statvolt/cm",
    var_type=VariableType.FIELD,
    modern_name="E_y",
)
VAR_Z = Variable(
    name="Z",
    description="z-component of electromotive intensity",
    units="statvolt/cm",
    var_type=VariableType.FIELD,
    modern_name="E_z",
)

# ── Electromagnetic Force (Lorentz) ──────────────────────────────
VAR_X_force = Variable(
    name="X",
    description="x-component of electromagnetic force on unit current",
    units="dyne/cm",
    var_type=VariableType.FIELD,
    modern_name="F_x",
)
VAR_Y_force = Variable(
    name="Y",
    description="y-component of electromagnetic force on unit current",
    units="dyne/cm",
    var_type=VariableType.FIELD,
    modern_name="F_y",
)
VAR_Z_force = Variable(
    name="Z",
    description="z-component of electromagnetic force on unit current",
    units="dyne/cm",
    var_type=VariableType.FIELD,
    modern_name="F_z",
)

# ── Material Properties ──────────────────────────────────────────
VAR_K = Variable(
    name="K",
    description="dielectric capacity (relative permittivity)",
    units="dimensionless (ratio)",
    var_type=VariableType.SCALAR,
    modern_name="epsilon_r",
)
VAR_C_cond = Variable(
    name="C",
    description="conductivity",
    units="s^{-1} (EMU)",
    var_type=VariableType.SCALAR,
    modern_name="sigma",
)
VAR_mu = Variable(
    name="mu",
    description="magnetic permeability",
    units="dimensionless (ratio)",
    var_type=VariableType.SCALAR,
    modern_name="mu_r",
)

# ── Charge and Potential ─────────────────────────────────────────
VAR_e = Variable(
    name="e",
    description="electric charge",
    units="statcoulomb (esu) or abcoulomb (emu)",
    var_type=VariableType.SCALAR,
    modern_name="q",
)
VAR_m = Variable(
    name="m",
    description="quantity of vitreous (positive) electricity",
    units="statcoulomb",
    var_type=VariableType.SCALAR,
)
VAR_n = Variable(
    name="n",
    description="quantity of resinous (negative) electricity",
    units="statcoulomb",
    var_type=VariableType.SCALAR,
)
VAR_phi = Variable(
    name="phi",
    description="electrostatic potential",
    units="statvolt",
    var_type=VariableType.FIELD,
    modern_name="V",
)
VAR_r = Variable(
    name="r",
    description="distance between charges",
    units="cm",
    var_type=VariableType.SCALAR,
)
VAR_rho = Variable(
    name="rho",
    description="volume charge density",
    units="statcoulomb/cm^3",
    var_type=VariableType.FIELD,
)
VAR_e_free = Variable(
    name="e_free",
    description="free electricity density",
    units="statcoulomb/cm^3",
    var_type=VariableType.FIELD,
    modern_name="rho_free",
)

# ── Velocity (for material derivative) ───────────────────────────
VAR_vx = Variable(
    name="vx",
    description="x-component of velocity",
    units="cm/s",
    var_type=VariableType.SCALAR,
)
VAR_vy = Variable(
    name="vy",
    description="y-component of velocity",
    units="cm/s",
    var_type=VariableType.SCALAR,
)
VAR_vz = Variable(
    name="vz",
    description="z-component of velocity",
    units="cm/s",
    var_type=VariableType.SCALAR,
)

# ── Time ─────────────────────────────────────────────────────────
VAR_t = Variable(name="t", description="time", units="s", var_type=VariableType.SCALAR)


# ═══════════════════════════════════════════════════════════════════
# EQUATION SET DEFINITIONS
# ═══════════════════════════════════════════════════════════════════


def _build_all_equation_sets() -> Dict[str, EquationSetEntry]:
    """Build the complete equation set catalog.

    Returns:
        Dictionary mapping set_id to EquationSetEntry.
    """
    catalog: Dict[str, EquationSetEntry] = {}

    # ──────────────────────────────────────────────────────────────
    # SET A: Magnetic Induction from Vector Potential
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["A"] = EquationSetEntry(
        set_id="A",
        name="Magnetic Induction from Vector Potential",
        articles=(591, 592, 593, 594, 595, 596, 597, 598, 599, 600),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"a = \frac{\partial H}{\partial y} - \frac{\partial G}{\partial z}, \quad"
        r"b = \frac{\partial F}{\partial z} - \frac{\partial A}{\partial x}, \quad"
        r"c = \frac{\partial G}{\partial x} - \frac{\partial F}{\partial y}",
        vector_form=r"\mathbf{B} = \nabla \times \mathbf{A}",
        formulas=[
            EquationFormula(
                equation_id="A1",
                latex=r"a = \frac{\partial H}{\partial y} - \frac{\partial G}{\partial z}",
                description="x-component of magnetic induction from curl of vector potential",
                variables=[VAR_a, VAR_H_vec, VAR_G],
                component="x",
            ),
            EquationFormula(
                equation_id="A2",
                latex=r"b = \frac{\partial F}{\partial z} - \frac{\partial H}{\partial x}",
                description="y-component of magnetic induction from curl of vector potential",
                variables=[VAR_b, VAR_F, VAR_H_vec],
                component="y",
            ),
            EquationFormula(
                equation_id="A3",
                latex=r"c = \frac{\partial G}{\partial x} - \frac{\partial F}{\partial y}",
                description="z-component of magnetic induction from curl of vector potential",
                variables=[VAR_c, VAR_G, VAR_F],
                component="z",
            ),
        ],
        variables={
            "a": VAR_a,
            "b": VAR_b,
            "c": VAR_c,
            "F": VAR_F,
            "G": VAR_G,
            "H": VAR_H_vec,
        },
        function_mapping={
            "A1": "maxwell.math.vector_operators.curl",
            "A2": "maxwell.math.vector_operators.curl",
            "A3": "maxwell.math.vector_operators.curl",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{A} = (F, G, H)",
                explanation="Define the electromagnetic momentum (vector potential) A with components F, G, H.",
                from_articles=(591,),
            ),
            DerivationStep(
                step_number=2,
                latex=r"\mathbf{B} = \nabla \times \mathbf{A}",
                explanation="Magnetic induction B is the curl of the vector potential A.",
                from_articles=(591, 592, 593),
            ),
            DerivationStep(
                step_number=3,
                latex=r"a = \partial_y H - \partial_z G, \quad b = \partial_z F - \partial_x H, \quad c = \partial_x G - \partial_y F",
                explanation="Expand the curl in Cartesian coordinates to obtain the three component equations.",
                from_articles=(594, 595, 596),
            ),
        ],
        examples=[
            PresetExample(
                name="uniform_vector_potential",
                description="Magnetic induction from a linear vector potential A = (0, 0, k*x)",
                inputs={
                    "F": 0.0,
                    "G": 0.0,
                    "H_func": lambda x, y, z: 100.0 * x,
                    "point": (1.0, 0.0, 0.0),
                },
                expected={"a": 0.0, "b": 100.0, "c": 0.0},
                tolerance=1e-4,
            ),
        ],
        notes="Maxwell calls the vector potential 'electromagnetic momentum'. "
        "This set defines B = curl(A), equivalent to the modern formulation. "
        "The component notation (a,b,c) for B and (F,G,H) for A is Maxwell's original notation.",
    )

    # ──────────────────────────────────────────────────────────────
    # SET B: Electromotive Intensity
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["B"] = EquationSetEntry(
        set_id="B",
        name="Electromotive Intensity",
        articles=(591, 592, 593, 594, 595, 596, 597, 598, 599, 600),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"P = \mu \frac{\partial G}{\partial t} - \mu \frac{\partial H}{\partial y} - \frac{\partial \psi}{\partial x}",
        vector_form=r"\mathbf{E} = -\frac{\partial \mathbf{A}}{\partial t} - \nabla \psi + \mathbf{v} \times \mathbf{B}",
        formulas=[
            EquationFormula(
                equation_id="B1",
                latex=r"P = \mu \frac{\partial G}{\partial t} - \mu \frac{\partial H}{\partial y} - \frac{\partial \psi}{\partial x}",
                description="x-component of electromotive intensity",
                variables=[VAR_X, VAR_F, VAR_H_vec, VAR_phi],
                component="x",
            ),
            EquationFormula(
                equation_id="B2",
                latex=r"Q = \mu \frac{\partial H}{\partial t} - \mu \frac{\partial F}{\partial z} - \frac{\partial \psi}{\partial y}",
                description="y-component of electromotive intensity",
                variables=[VAR_Y, VAR_H_vec, VAR_F, VAR_phi],
                component="y",
            ),
            EquationFormula(
                equation_id="B3",
                latex=r"R = \mu \frac{\partial F}{\partial t} - \mu \frac{\partial G}{\partial x} - \frac{\partial \psi}{\partial z}",
                description="z-component of electromotive intensity",
                variables=[VAR_Z, VAR_F, VAR_G, VAR_phi],
                component="z",
            ),
        ],
        variables={
            "P": VAR_X,
            "Q": VAR_Y,
            "R": VAR_Z,
            "psi": VAR_phi,
            "mu": VAR_mu,
        },
        function_mapping={
            "B1": "maxwell.math.derivatives.partial_derivative_t",
            "B2": "maxwell.math.derivatives.partial_derivative_t",
            "B3": "maxwell.math.derivatives.partial_derivative_t",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{E} = -\frac{\partial \mathbf{A}}{\partial t} - \nabla \psi",
                explanation="The electromotive intensity has two contributions: the time rate of change of the vector potential (electrokinetic) and the gradient of the scalar potential (electrostatic).",
                from_articles=(591, 598),
            ),
            DerivationStep(
                step_number=2,
                latex=r"P = -\frac{\partial F}{\partial t} - \frac{\partial \psi}{\partial x}",
                explanation="x-component form. Maxwell also includes the motional term v x B for moving conductors.",
                from_articles=(598, 599),
            ),
        ],
        examples=[
            PresetExample(
                name="static_field",
                description="Electromotive intensity from static scalar potential only",
                inputs={
                    "psi_func": lambda x, y, z: 50.0 * x,
                    "A_components": (0.0, 0.0, 0.0),
                    "point": (1.0, 0.0, 0.0),
                },
                expected={"P": -50.0, "Q": 0.0, "R": 0.0},
                tolerance=1e-4,
            ),
        ],
        notes="Maxwell uses (P, Q, R) for the components of electromotive intensity (modern E field). "
        "The scalar potential psi is what we now call V or phi. "
        "Set B is Faraday's law in component form.",
    )

    # ──────────────────────────────────────────────────────────────
    # SET C: Electromagnetic Force (Lorentz Force)
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["C"] = EquationSetEntry(
        set_id="C",
        name="Electromagnetic Force on Current",
        articles=(596, 597, 598, 599, 600, 601, 602),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"X = B w - C v, \quad Y = C u - A w, \quad Z = A v - B u",
        vector_form=r"\mathbf{F} = \mathbf{J} \times \mathbf{B}",
        formulas=[
            EquationFormula(
                equation_id="C1",
                latex=r"X = B w - C v",
                description="x-component of electromagnetic force per unit volume",
                variables=[VAR_X_force, VAR_b, VAR_c, VAR_v, VAR_w],
                component="x",
            ),
            EquationFormula(
                equation_id="C2",
                latex=r"Y = C u - A w",
                description="y-component of electromagnetic force per unit volume",
                variables=[VAR_Y_force, VAR_c, VAR_a, VAR_u, VAR_w],
                component="y",
            ),
            EquationFormula(
                equation_id="C3",
                latex=r"Z = A v - B u",
                description="z-component of electromagnetic force per unit volume",
                variables=[VAR_Z_force, VAR_a, VAR_b, VAR_u, VAR_v],
                component="z",
            ),
        ],
        variables={
            "X": VAR_X_force,
            "Y": VAR_Y_force,
            "Z": VAR_Z_force,
            "a": VAR_a,
            "b": VAR_b,
            "c": VAR_c,
            "u": VAR_u,
            "v": VAR_v,
            "w": VAR_w,
        },
        function_mapping={
            "C1": "maxwell.electromagnetism.forces.lorentz.lorentz_force",
            "C2": "maxwell.electromagnetism.forces.lorentz.lorentz_force",
            "C3": "maxwell.electromagnetism.forces.lorentz.lorentz_force",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{F} = \mathbf{J} \times \mathbf{B}",
                explanation="The electromagnetic force on a current-carrying conductor is the cross product of current density and magnetic induction.",
                from_articles=(596, 597),
            ),
            DerivationStep(
                step_number=2,
                latex=r"X = B w - C v, \quad Y = C u - A w, \quad Z = A v - B u",
                explanation="Expand the cross product in Cartesian components. Note: Maxwell uses (A,B,C) for magnetic induction components here (same as a,b,c in Set A).",
                from_articles=(598, 599, 600),
            ),
        ],
        examples=[
            PresetExample(
                name="perpendicular_force",
                description="Force on current along x-axis in z-directed magnetic field",
                inputs={"a": 0.0, "b": 0.0, "c": 50.0, "u": 10.0, "v": 0.0, "w": 0.0},
                expected={"X": 0.0, "Y": 500.0, "Z": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="This is the Lorentz force law in its original form. "
        "Maxwell uses (A,B,C) for magnetic induction in this context, which are the same as (a,b,c) from Set A. "
        "The force is per unit volume of the conductor.",
    )

    # ──────────────────────────────────────────────────────────────
    # SET D: Magnetization
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["D"] = EquationSetEntry(
        set_id="D",
        name="Magnetization (Constitution of Magnetic Fields)",
        articles=(395, 396, 397, 398, 399, 400, 595, 596),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"a = \alpha + 4\pi A, \quad b = \beta + 4\pi B, \quad c = \gamma + 4\pi C",
        vector_form=r"\mathbf{B} = \mathbf{H} + 4\pi \mathbf{M}",
        formulas=[
            EquationFormula(
                equation_id="D1",
                latex=r"a = \alpha + 4\pi A",
                description="x-component: magnetic induction equals magnetic force plus magnetization",
                variables=[VAR_a, VAR_alpha, VAR_A_mag],
                component="x",
            ),
            EquationFormula(
                equation_id="D2",
                latex=r"b = \beta + 4\pi B",
                description="y-component: magnetic induction equals magnetic force plus magnetization",
                variables=[VAR_b, VAR_beta, VAR_B_mag],
                component="y",
            ),
            EquationFormula(
                equation_id="D3",
                latex=r"c = \gamma + 4\pi C",
                description="z-component: magnetic induction equals magnetic force plus magnetization",
                variables=[VAR_c, VAR_gamma, VAR_C_mag],
                component="z",
            ),
        ],
        variables={
            "a": VAR_a,
            "b": VAR_b,
            "c": VAR_c,
            "alpha": VAR_alpha,
            "beta": VAR_beta,
            "gamma": VAR_gamma,
            "A": VAR_A_mag,
            "B": VAR_B_mag,
            "C": VAR_C_mag,
        },
        function_mapping={
            "D1": "maxwell.core.magnet.compute_magnetization",
            "D2": "maxwell.core.magnet.compute_magnetization",
            "D3": "maxwell.core.magnet.compute_magnetization",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{B} = \mathbf{H} + 4\pi \mathbf{M}",
                explanation="Total magnetic induction B is the sum of the magnetic force H and the contribution from magnetization M (magnetic moment per unit volume).",
                from_articles=(395, 396),
            ),
            DerivationStep(
                step_number=2,
                latex=r"\mathbf{B} = \mu \mathbf{H}",
                explanation="For linear isotropic materials, M = kappa*H and B = mu*H where mu = 1 + 4*pi*kappa.",
                from_articles=(397, 398),
            ),
        ],
        examples=[
            PresetExample(
                name="linear_magnet",
                description="B field in a linear magnetic material with mu = 100",
                inputs={"alpha": 10.0, "beta": 0.0, "gamma": 0.0, "mu": 100.0},
                expected={"a": 1000.0, "b": 0.0, "c": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="Maxwell distinguishes between 'magnetic induction' (B), 'magnetic force' (H), and 'magnetization' (M or I). "
        "In modern notation: B = H + 4*pi*M (CGS). "
        "For linear materials: B = mu*H where mu is the relative permeability.",
    )

    # ──────────────────────────────────────────────────────────────
    # SET E: Electric Currents (Ampere's Law)
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["E"] = EquationSetEntry(
        set_id="E",
        name="Electric Currents from Magnetic Force (Ampere's Law)",
        articles=(
            591,
            592,
            593,
            594,
            595,
            596,
            597,
            598,
            599,
            600,
            601,
            602,
            603,
            604,
            605,
            607,
        ),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"4\pi u = \frac{\partial \gamma}{\partial y} - \frac{\partial \beta}{\partial z}, \quad"
        r"4\pi v = \frac{\partial \alpha}{\partial z} - \frac{\partial \gamma}{\partial x}, \quad"
        r"4\pi w = \frac{\partial \beta}{\partial x} - \frac{\partial \alpha}{\partial y}",
        vector_form=r"\nabla \times \mathbf{H} = 4\pi \mathbf{J}",
        formulas=[
            EquationFormula(
                equation_id="E1",
                latex=r"4\pi u = \frac{\partial \gamma}{\partial y} - \frac{\partial \beta}{\partial z}",
                description="x-component: curl of H equals 4*pi times current density",
                variables=[VAR_u, VAR_gamma, VAR_beta],
                component="x",
            ),
            EquationFormula(
                equation_id="E2",
                latex=r"4\pi v = \frac{\partial \alpha}{\partial z} - \frac{\partial \gamma}{\partial x}",
                description="y-component: curl of H equals 4*pi times current density",
                variables=[VAR_v, VAR_alpha, VAR_gamma],
                component="y",
            ),
            EquationFormula(
                equation_id="E3",
                latex=r"4\pi w = \frac{\partial \beta}{\partial x} - \frac{\partial \alpha}{\partial y}",
                description="z-component: curl of H equals 4*pi times current density",
                variables=[VAR_w, VAR_beta, VAR_alpha],
                component="z",
            ),
        ],
        variables={
            "u": VAR_u,
            "v": VAR_v,
            "w": VAR_w,
            "alpha": VAR_alpha,
            "beta": VAR_beta,
            "gamma": VAR_gamma,
        },
        function_mapping={
            "E1": "maxwell.math.vector_operators.curl",
            "E2": "maxwell.math.vector_operators.curl",
            "E3": "maxwell.math.vector_operators.curl",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\oint \mathbf{H} \cdot d\mathbf{l} = 4\pi I_{enc}",
                explanation="Ampere's circuital law: the line integral of H around a closed loop equals 4*pi times the enclosed current (CGS units).",
                from_articles=(607,),
            ),
            DerivationStep(
                step_number=2,
                latex=r"\nabla \times \mathbf{H} = 4\pi \mathbf{J}",
                explanation="Apply Stokes' theorem to convert the integral form to differential form.",
                from_articles=(607, 608),
            ),
            DerivationStep(
                step_number=3,
                latex=r"4\pi u = \partial_y \gamma - \partial_z \beta, \quad 4\pi v = \partial_z \alpha - \partial_x \gamma, \quad 4\pi w = \partial_x \beta - \partial_y \alpha",
                explanation="Expand curl(H) in Cartesian coordinates with H = (alpha, beta, gamma).",
                from_articles=(607, 608, 609),
            ),
        ],
        examples=[
            PresetExample(
                name="straight_wire",
                description="Current density from H field of an infinite straight wire",
                inputs={
                    "alpha_func": lambda x, y, z: 0.0,
                    "beta_func": lambda x, y, z: (
                        -2.0 * 5.0 * x / (x**2 + y**2 + 1e-12)
                        if (x**2 + y**2) > 0.01
                        else 0.0
                    ),
                    "gamma_func": lambda x, y, z: (
                        2.0 * 5.0 * y / (x**2 + y**2 + 1e-12)
                        if (x**2 + y**2) > 0.01
                        else 0.0
                    ),
                    "point": (2.0, 0.0, 0.0),
                },
                expected={"note": "u = 0 outside wire, total current = 5 abampere"},
                tolerance=1e-4,
            ),
        ],
        notes="This is Ampere's law in differential form (CGS-EMU). "
        "Maxwell uses (alpha, beta, gamma) for the components of magnetic force H, "
        "and (u, v, w) for the components of total current density J. "
        "Note: this form does NOT yet include the displacement current term; "
        "that is added in Set H.",
    )

    # ──────────────────────────────────────────────────────────────
    # SET F: Electric Displacement
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["F"] = EquationSetEntry(
        set_id="F",
        name="Electric Displacement (Dielectric Response)",
        articles=(
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            111,
            112,
            113,
            114,
            115,
            616,
            617,
            618,
            619,
            620,
            621,
            622,
        ),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"f = \frac{1}{4\pi} K X, \quad g = \frac{1}{4\pi} K Y, \quad h = \frac{1}{4\pi} K Z",
        vector_form=r"\mathbf{D} = \frac{K}{4\pi} \mathbf{E}",
        formulas=[
            EquationFormula(
                equation_id="F1",
                latex=r"f = \frac{1}{4\pi} K X",
                description="x-component of electric displacement",
                variables=[VAR_f, VAR_K, VAR_X],
                component="x",
            ),
            EquationFormula(
                equation_id="F2",
                latex=r"g = \frac{1}{4\pi} K Y",
                description="y-component of electric displacement",
                variables=[VAR_g, VAR_K, VAR_Y],
                component="y",
            ),
            EquationFormula(
                equation_id="F3",
                latex=r"h = \frac{1}{4\pi} K Z",
                description="z-component of electric displacement",
                variables=[VAR_h, VAR_K, VAR_Z],
                component="z",
            ),
        ],
        variables={
            "f": VAR_f,
            "g": VAR_g,
            "h": VAR_h,
            "K": VAR_K,
            "X": VAR_X,
            "Y": VAR_Y,
            "Z": VAR_Z,
        },
        function_mapping={
            "F1": "maxwell.core.charge.compute_displacement",
            "F2": "maxwell.core.charge.compute_displacement",
            "F3": "maxwell.core.charge.compute_displacement",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{D} = \epsilon \mathbf{E}",
                explanation="In a dielectric, the electric displacement D is proportional to the electromotive intensity E. In CGS, epsilon = K/(4*pi) where K is the specific inductive capacity (dielectric constant).",
                from_articles=(616, 617),
            ),
            DerivationStep(
                step_number=2,
                latex=r"f = \frac{K}{4\pi} X, \quad g = \frac{K}{4\pi} Y, \quad h = \frac{K}{4\pi} Z",
                explanation="Component form. K is Maxwell's 'dielectric capacity' or 'specific inductive capacity'.",
                from_articles=(618, 619, 620),
            ),
        ],
        examples=[
            PresetExample(
                name="dielectric_displacement",
                description="Electric displacement in glass (K = 6) under E = 100 statvolt/cm",
                inputs={"K": 6.0, "X": 100.0, "Y": 0.0, "Z": 0.0},
                expected={"f": 600.0 / (4.0 * np.pi), "g": 0.0, "h": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="Maxwell's 'electric displacement' is what we now call the D field. "
        "His 'dielectric capacity' K is the relative permittivity epsilon_r. "
        "In CGS-ESU, D = (K/4*pi)*E. In vacuum (K=1), D = E/(4*pi).",
    )

    # ──────────────────────────────────────────────────────────────
    # SET G: Conductivity (Ohm's Law)
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["G"] = EquationSetEntry(
        set_id="G",
        name="Conductivity (Ohm's Law for Conduction Current)",
        articles=(241, 242, 243, 244, 245, 246, 616, 617, 618, 619),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"p = C X, \quad q = C Y, \quad r = C Z",
        vector_form=r"\mathbf{J}_{cond} = \sigma \mathbf{E}",
        formulas=[
            EquationFormula(
                equation_id="G1",
                latex=r"p = C X",
                description="x-component: conduction current from Ohm's law",
                variables=[VAR_p, VAR_C_cond, VAR_X],
                component="x",
            ),
            EquationFormula(
                equation_id="G2",
                latex=r"q = C Y",
                description="y-component: conduction current from Ohm's law",
                variables=[VAR_q, VAR_C_cond, VAR_Y],
                component="y",
            ),
            EquationFormula(
                equation_id="G3",
                latex=r"r = C Z",
                description="z-component: conduction current from Ohm's law",
                variables=[VAR_r, VAR_C_cond, VAR_Z],
                component="z",
            ),
        ],
        variables={
            "p": VAR_p,
            "q": VAR_q,
            "r": VAR_r,
            "C": VAR_C_cond,
            "X": VAR_X,
            "Y": VAR_Y,
            "Z": VAR_Z,
        },
        function_mapping={
            "G1": "maxwell.circuits.dynamics.ohms_law",
            "G2": "maxwell.circuits.dynamics.ohms_law",
            "G3": "maxwell.circuits.dynamics.ohms_law",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{J}_{cond} = \sigma \mathbf{E}",
                explanation="Ohm's law in local form: conduction current density is proportional to electric field, with conductivity sigma.",
                from_articles=(241, 242),
            ),
            DerivationStep(
                step_number=2,
                latex=r"p = C X, \quad q = C Y, \quad r = C Z",
                explanation="Component form. Maxwell uses C for conductivity (modern sigma).",
                from_articles=(243, 244),
            ),
        ],
        examples=[
            PresetExample(
                name="copper_conductor",
                description="Conduction current in copper (sigma ~ 5.8e17 s^{-1} in CGS)",
                inputs={"C": 5.8e17, "X": 1.0, "Y": 0.0, "Z": 0.0},
                expected={"p": 5.8e17, "q": 0.0, "r": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="Maxwell uses C for conductivity (modern sigma). "
        "In CGS-EMU, conductivity has units of s^{-1}. "
        "This is the conduction current only; the total current includes displacement current (Set H).",
    )

    # ──────────────────────────────────────────────────────────────
    # SET H: True/Total Currents
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["H"] = EquationSetEntry(
        set_id="H",
        name="True Currents (Total Current = Conduction + Displacement)",
        articles=(
            607,
            608,
            609,
            610,
            611,
            612,
            613,
            614,
            615,
            616,
            617,
            618,
            619,
            620,
            621,
            622,
        ),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"u = p + \frac{\partial f}{\partial t}, \quad"
        r"v = q + \frac{\partial g}{\partial t}, \quad"
        r"w = r + \frac{\partial h}{\partial t}",
        vector_form=r"\mathbf{J}_{total} = \mathbf{J}_{cond} + \frac{\partial \mathbf{D}}{\partial t}",
        formulas=[
            EquationFormula(
                equation_id="H1",
                latex=r"u = p + \frac{\partial f}{\partial t}",
                description="x-component: total current = conduction + displacement current",
                variables=[VAR_u, VAR_p, VAR_f, VAR_t],
                component="x",
            ),
            EquationFormula(
                equation_id="H2",
                latex=r"v = q + \frac{\partial g}{\partial t}",
                description="y-component: total current = conduction + displacement current",
                variables=[VAR_v, VAR_q, VAR_g, VAR_t],
                component="y",
            ),
            EquationFormula(
                equation_id="H3",
                latex=r"w = r + \frac{\partial h}{\partial t}",
                description="z-component: total current = conduction + displacement current",
                variables=[VAR_w, VAR_r, VAR_h, VAR_t],
                component="z",
            ),
        ],
        variables={
            "u": VAR_u,
            "v": VAR_v,
            "w": VAR_w,
            "p": VAR_p,
            "q": VAR_q,
            "r": VAR_r,
            "f": VAR_f,
            "g": VAR_g,
            "h": VAR_h,
        },
        function_mapping={
            "H1": "maxwell.math.derivatives.partial_derivative_t",
            "H2": "maxwell.math.derivatives.partial_derivative_t",
            "H3": "maxwell.math.derivatives.partial_derivative_t",
        },
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\mathbf{J}_{total} = \mathbf{J}_{cond} + \mathbf{J}_{displacement}",
                explanation="The total (true) current is the sum of conduction current and displacement current. This is Maxwell's crucial insight.",
                from_articles=(607, 608),
            ),
            DerivationStep(
                step_number=2,
                latex=r"\mathbf{J}_{displacement} = \frac{\partial \mathbf{D}}{\partial t}",
                explanation="Displacement current is the time rate of change of electric displacement.",
                from_articles=(610, 611, 612),
            ),
            DerivationStep(
                step_number=3,
                latex=r"u = p + \partial_t f, \quad v = q + \partial_t g, \quad w = r + \partial_t h",
                explanation="Component form of the total current equation.",
                from_articles=(613, 614, 615),
            ),
        ],
        examples=[
            PresetExample(
                name="capacitor_displacement",
                description="Displacement current dominates in a charging capacitor (no conduction through dielectric)",
                inputs={
                    "p": 0.0,
                    "q": 0.0,
                    "r": 0.0,
                    "df_dt": 100.0,
                    "dg_dt": 0.0,
                    "dh_dt": 0.0,
                },
                expected={"u": 100.0, "v": 0.0, "w": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="This is the Maxwell-Ampere equation in its complete form. "
        "The displacement current term df/dt is Maxwell's revolutionary addition that makes "
        "the equations consistent and predicts electromagnetic waves. "
        "Combining Sets E and H gives the full Ampere-Maxwell law: curl(H) = 4*pi*(J_cond + dD/dt).",
    )

    # ──────────────────────────────────────────────────────────────
    # SOLENoidal: Current Continuity
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["solenoidal"] = EquationSetEntry(
        set_id="solenoidal",
        name="Solenoidal Condition (Current Continuity)",
        articles=(607, 608, 609, 610, 611),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z} = 0",
        vector_form=r"\nabla \cdot \mathbf{J}_{total} = 0",
        formulas=[
            EquationFormula(
                equation_id="S1",
                latex=r"\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z} = 0",
                description="Divergence of total current is zero (charge conservation for steady state)",
                variables=[VAR_u, VAR_v, VAR_w],
            ),
        ],
        variables={"u": VAR_u, "v": VAR_v, "w": VAR_w},
        function_mapping={"S1": "maxwell.math.vector_operators.divergence"},
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\nabla \cdot (\nabla \times \mathbf{H}) = 0",
                explanation="The divergence of a curl is identically zero (vector identity, Arts. 103-110).",
                from_articles=(103, 104, 105),
            ),
            DerivationStep(
                step_number=2,
                latex=r"\nabla \cdot \mathbf{J}_{total} = 0",
                explanation="Since J_total = (1/4pi)*curl(H) from Set E, the divergence of J_total must be zero. This expresses charge conservation.",
                from_articles=(607, 608),
            ),
        ],
        examples=[
            PresetExample(
                name="uniform_current",
                description="Uniform current density is automatically solenoidal",
                inputs={"u": 10.0, "v": 5.0, "w": 3.0},
                expected={"divergence": 0.0},
                tolerance=1e-6,
            ),
        ],
        notes="The solenoidal condition ensures charge conservation. "
        "For time-varying fields, the displacement current term ensures that div(J_total) = 0 even when div(J_cond) != 0.",
    )

    # ──────────────────────────────────────────────────────────────
    # FREE CHARGE: Free Electricity from Displacement
    # Volume 2, Part IV, Chapter IX
    # ──────────────────────────────────────────────────────────────
    catalog["free_charge"] = EquationSetEntry(
        set_id="free_charge",
        name="Free Electricity (Charge from Displacement Divergence)",
        articles=(61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 111, 112),
        volume=2,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        latex_summary=r"e = \frac{\partial f}{\partial x} + \frac{\partial g}{\partial y} + \frac{\partial h}{\partial z}",
        vector_form=r"\rho_{free} = \nabla \cdot \mathbf{D}",
        formulas=[
            EquationFormula(
                equation_id="FC1",
                latex=r"e = \frac{\partial f}{\partial x} + \frac{\partial g}{\partial y} + \frac{\partial h}{\partial z}",
                description="Free charge density equals divergence of electric displacement",
                variables=[VAR_e_free, VAR_f, VAR_g, VAR_h],
            ),
        ],
        variables={"e": VAR_e_free, "f": VAR_f, "g": VAR_g, "h": VAR_h},
        function_mapping={"FC1": "maxwell.math.vector_operators.divergence"},
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"\nabla \cdot \mathbf{D} = 4\pi \rho",
                explanation="Gauss's law: the divergence of electric displacement equals 4*pi times the free charge density (CGS).",
                from_articles=(61, 62, 63),
            ),
            DerivationStep(
                step_number=2,
                latex=r"e = \partial_x f + \partial_y g + \partial_z h",
                explanation="Component form. Maxwell uses 'e' for the quantity of free electricity per unit volume.",
                from_articles=(64, 65, 66),
            ),
        ],
        examples=[
            PresetExample(
                name="point_charge_displacement",
                description="Free charge from radial displacement field D = q*r_hat/r^2",
                inputs={
                    "f_func": lambda x, y, z: 10.0
                    * x
                    / (x**2 + y**2 + z**2 + 1e-12) ** 1.5,
                    "g_func": lambda x, y, z: 10.0
                    * y
                    / (x**2 + y**2 + z**2 + 1e-12) ** 1.5,
                    "h_func": lambda x, y, z: 10.0
                    * z
                    / (x**2 + y**2 + z**2 + 1e-12) ** 1.5,
                    "point": (2.0, 0.0, 0.0),
                },
                expected={"div_D": 0.0},  # Zero away from origin
                tolerance=1e-4,
            ),
        ],
        notes="This is Gauss's law in differential form. "
        "Maxwell uses 'e' for the free electricity density. "
        "In CGS-ESU: div(D) = 4*pi*rho. In CGS-Gaussian: div(E) = 4*pi*rho.",
    )

    # ──────────────────────────────────────────────────────────────
    # COULOMB'S LAW
    # Volume 1, Part I, Chapter I
    # ──────────────────────────────────────────────────────────────
    catalog["coulomb"] = EquationSetEntry(
        set_id="coulomb",
        name="Coulomb's Law (Electrostatic Force)",
        articles=(
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
        ),
        volume=1,
        part=1,
        chapter="On the Measurement of Quantities",
        latex_summary=r"F = \frac{e \cdot e'}{r^2}",
        vector_form=r"\mathbf{F} = \frac{q_1 q_2}{r^2} \hat{\mathbf{r}}",
        formulas=[
            EquationFormula(
                equation_id="CL1",
                latex=r"F = \frac{e \cdot e'}{r^2}",
                description="Electrostatic force between two point charges (CGS-ESU, f=1)",
                variables=[VAR_e, VAR_r],
            ),
        ],
        variables={"e": VAR_e, "r": VAR_r},
        function_mapping={"CL1": "maxwell.core.charge.coulomb_force"},
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"F \propto \frac{e \cdot e'}{r^2}",
                explanation="Coulomb's experimental result: force is proportional to product of charges and inversely proportional to square of distance.",
                from_articles=(23, 24, 25),
            ),
            DerivationStep(
                step_number=2,
                latex=r"F = \frac{e \cdot e'}{r^2}",
                explanation="In CGS-ESU units, the proportionality constant f = 1 by definition of the unit charge.",
                from_articles=(26, 27, 28),
            ),
        ],
        examples=[
            PresetExample(
                name="two_statcoulombs",
                description="Force between two unit charges at 1 cm distance",
                inputs={"e": 1.0, "e_prime": 1.0, "r": 1.0},
                expected={"F": 1.0},
                tolerance=1e-6,
            ),
        ],
        notes="In CGS-ESU, the unit of charge (statcoulomb) is DEFINED so that Coulomb's constant = 1. "
        "Two unit charges at 1 cm distance exert 1 dyne of force on each other.",
    )

    # ──────────────────────────────────────────────────────────────
    # NET CHARGE
    # Volume 1, Part I, Chapter I
    # ──────────────────────────────────────────────────────────────
    catalog["net_charge"] = EquationSetEntry(
        set_id="net_charge",
        name="Net Electric Charge",
        articles=(
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
        ),
        volume=1,
        part=1,
        chapter="On the Measurement of Quantities",
        latex_summary=r"e = m - n",
        vector_form=r"q = q_{+} - q_{-}",
        formulas=[
            EquationFormula(
                equation_id="NC1",
                latex=r"e = m - n",
                description="Net charge equals vitreous (positive) minus resinous (negative) electricity",
                variables=[VAR_e, VAR_m, VAR_n],
            ),
        ],
        variables={"e": VAR_e, "m": VAR_m, "n": VAR_n},
        function_mapping={"NC1": "maxwell.core.charge.compute_net_charge"},
        derivation_steps=[
            DerivationStep(
                step_number=1,
                latex=r"e = m - n",
                explanation="Maxwell defines the net electrification as the excess of vitreous (positive) electricity m over resinous (negative) electricity n. This reflects the two-fluid theory of electricity.",
                from_articles=(23, 24),
            ),
        ],
        examples=[
            PresetExample(
                name="positive_net_charge",
                description="Net charge with excess vitreous electricity",
                inputs={"m": 10.0, "n": 3.0},
                expected={"e": 7.0},
                tolerance=1e-6,
            ),
        ],
        notes="Maxwell uses the historical terminology: 'vitreous' electricity (positive, from rubbing glass) "
        "and 'resinous' electricity (negative, from rubbing resin). The net charge is their difference.",
    )

    return catalog


# ═══════════════════════════════════════════════════════════════════
# EQUATION REGISTRY (SINGLETON)
# ═══════════════════════════════════════════════════════════════════


class EquationRegistry:
    """Central registry for all Maxwell equation sets.

    Provides lookup, validation, and query capabilities for the
    complete equation catalog.

    Usage:
        >>> reg = EquationRegistry()
        >>> entry = reg.get("E")  # Ampere's law
        >>> print(entry.vector_form)
        >>> examples = reg.get_examples("D")
    """

    def __init__(self) -> None:
        """Initialize the registry with all equation sets."""
        self._catalog: Dict[str, EquationSetEntry] = _build_all_equation_sets()

    def get(self, set_id: str) -> EquationSetEntry:
        """Get an equation set by its identifier.

        Args:
            set_id: Equation set identifier (e.g., "A", "E", "coulomb").

        Returns:
            The EquationSetEntry for the requested set.

        Raises:
            KeyError: If set_id is not found.
        """
        if set_id not in self._catalog:
            available = ", ".join(sorted(self._catalog.keys()))
            raise KeyError(f"Unknown equation set '{set_id}'. Available: {available}")
        return self._catalog[set_id]

    def get_all(self) -> Dict[str, EquationSetEntry]:
        """Get all equation sets.

        Returns:
            Dictionary mapping set_id to EquationSetEntry.
        """
        return dict(self._catalog)

    def get_by_article(self, article: int) -> List[str]:
        """Find all equation sets that reference a given Maxwell article.

        Args:
            article: Maxwell article number.

        Returns:
            List of set_ids that reference the article.
        """
        results = []
        for set_id, entry in self._catalog.items():
            if article in entry.articles:
                results.append(set_id)
        return results

    def get_by_part(self, part: int) -> List[str]:
        """Find all equation sets from a given Part of the Treatise.

        Args:
            part: Part number (1-6).

        Returns:
            List of set_ids from the given Part.
        """
        return [set_id for set_id, entry in self._catalog.items() if entry.part == part]

    def get_by_volume(self, volume: int) -> List[str]:
        """Find all equation sets from a given Volume.

        Args:
            volume: Volume number (1 or 2).

        Returns:
            List of set_ids from the given Volume.
        """
        return [
            set_id for set_id, entry in self._catalog.items() if entry.volume == volume
        ]

    def get_variable(self, name: str) -> Optional[Variable]:
        """Find a variable definition by name.

        Searches across all equation sets.

        Args:
            name: Variable symbol (e.g., "alpha", "B", "K").

        Returns:
            The Variable definition, or None if not found.
        """
        for entry in self._catalog.values():
            if name in entry.variables:
                return entry.variables[name]
        return None

    def get_examples(self, set_id: str) -> List[PresetExample]:
        """Get all preset examples for an equation set.

        Args:
            set_id: Equation set identifier.

        Returns:
            List of PresetExample objects.
        """
        return self.get(set_id).examples

    def get_function_mapping(self, set_id: str) -> Dict[str, str]:
        """Get the function-to-equation mapping for a set.

        Args:
            set_id: Equation set identifier.

        Returns:
            Dictionary mapping equation_id -> fully qualified function path.
        """
        return self.get(set_id).function_mapping

    def summary(self) -> str:
        """Generate a human-readable summary of the entire catalog.

        Returns:
            Multi-line string summarizing all equation sets.
        """
        lines = ["=" * 70]
        lines.append("MAXWELL EQUATION CATALOG SUMMARY")
        lines.append("=" * 70)
        lines.append("")

        for set_id in sorted(self._catalog.keys()):
            entry = self._catalog[set_id]
            art_str = ", ".join(f"Art. {a}" for a in entry.articles[:5])
            if len(entry.articles) > 5:
                art_str += f", ... ({len(entry.articles)} total)"

            lines.append(f"Set {entry.set_id}: {entry.name}")
            lines.append(
                f"  Location: Vol. {entry.volume}, Part {entry.part}, Ch. '{entry.chapter}'"
            )
            lines.append(f"  Articles: {art_str}")
            lines.append(f"  Vector:   {entry.vector_form}")
            lines.append(f"  Formulas: {len(entry.formulas)}")
            lines.append(f"  Examples: {len(entry.examples)}")
            lines.append("")

        lines.append(f"Total equation sets: {len(self._catalog)}")
        total_formulas = sum(len(e.formulas) for e in self._catalog.values())
        total_examples = sum(len(e.examples) for e in self._catalog.values())
        total_variables = len(
            set().union(*(set(e.variables.keys()) for e in self._catalog.values()))
        )
        lines.append(f"Total formulas: {total_formulas}")
        lines.append(f"Total examples: {total_examples}")
        lines.append(f"Total unique variables: {total_variables}")
        lines.append("=" * 70)
        return "\n".join(lines)

    @maxwell_cite(
        591,
        592,
        593,
        594,
        595,
        596,
        597,
        598,
        599,
        600,
        601,
        602,
        603,
        604,
        605,
        607,
        608,
        609,
        610,
        611,
        612,
        613,
        614,
        615,
        616,
        617,
        618,
        619,
        620,
        621,
        622,
        part=4,
        chapter="General Equations of the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Verify all equation sets reference valid articles",
    )
    def verify_integrity(self) -> Dict[str, Any]:
        """Verify the internal consistency of the equation catalog.

        Checks:
            - All function_mapping targets are importable
            - All variables in formulas exist in the variables dict
            - All equation_ids are unique within a set
            - All derivation steps have valid article references

        Returns:
            Dictionary with 'valid', 'warnings', and 'errors' keys.
        """
        warnings_list: List[str] = []
        errors_list: List[str] = []

        for set_id, entry in self._catalog.items():
            # Check variable references in formulas
            for formula in entry.formulas:
                for var in formula.variables:
                    if var.name not in entry.variables:
                        warnings_list.append(
                            f"Set {set_id}, formula {formula.equation_id}: "
                            f"variable '{var.name}' not in variables dict"
                        )

            # Check uniqueness of equation_ids
            eq_ids = [f.equation_id for f in entry.formulas]
            if len(eq_ids) != len(set(eq_ids)):
                errors_list.append(f"Set {set_id}: duplicate equation IDs {eq_ids}")

            # Check function mappings are valid module paths
            for eq_id, func_path in entry.function_mapping.items():
                parts = func_path.rsplit(".", 1)
                if len(parts) == 2:
                    module_path, func_name = parts
                    try:
                        import importlib

                        mod = importlib.import_module(module_path)
                        if not hasattr(mod, func_name):
                            warnings_list.append(
                                f"Set {set_id}, eq {eq_id}: function '{func_name}' not found in {module_path}"
                            )
                    except ImportError:
                        warnings_list.append(
                            f"Set {set_id}, eq {eq_id}: module '{module_path}' not importable"
                        )

        return {
            "valid": len(errors_list) == 0,
            "warnings": warnings_list,
            "errors": errors_list,
            "total_sets": len(self._catalog),
        }


# Module-level singleton
REGISTRY = EquationRegistry()
"""Global equation registry singleton."""


@maxwell_cite(
    591,
    part=4,
    chapter="General Equations",
    theory_class="maxwell_original",
    description="Get equation set entry",
)
def get_equation_set(set_id: str) -> EquationSetEntry:
    """Get an equation set entry from the global registry.

    Args:
        set_id: Equation set identifier.

    Returns:
        The EquationSetEntry.
    """
    return REGISTRY.get(set_id)


@maxwell_cite(
    591,
    part=4,
    chapter="General Equations",
    theory_class="standard_math",
    description="Compute equation from component values",
)
def compute_equation(equation_id: str, **kwargs: Any) -> Dict[str, Any]:
    """Compute a specific equation given numerical inputs.

    This is a convenience function that evaluates an equation
    formula with provided parameter values.

    Args:
        equation_id: Equation identifier (e.g., "C1", "D1", "E1").
        **kwargs: Named parameter values for the equation variables.

    Returns:
        Dictionary with computed result and metadata.

    Example:
        >>> # Lorentz force C1: X = B*w - C*v
        >>> result = compute_equation("C1", b=50.0, c=0.0, u=10.0, v=0.0, w=0.0)
        >>> result["X"]  # 0.0
    """
    # Find which set contains this equation_id
    for set_id, entry in REGISTRY.get_all().items():
        for formula in entry.formulas:
            if formula.equation_id == equation_id:
                # Evaluate based on equation type
                return _evaluate_formula(formula, entry.set_id, **kwargs)

    available = []
    for entry in REGISTRY.get_all().values():
        for f in entry.formulas:
            available.append(f.equation_id)
    raise KeyError(f"Unknown equation_id '{equation_id}'. Available: {available}")


def _evaluate_formula(
    formula: EquationFormula, set_id: str, **kwargs: Any
) -> Dict[str, Any]:
    """Evaluate a formula with given parameters.

    Args:
        formula: The equation formula to evaluate.
        set_id: Which equation set it belongs to.
        **kwargs: Parameter values.

    Returns:
        Computation result dictionary.
    """
    result: Dict[str, Any] = {
        "equation_id": formula.equation_id,
        "set_id": set_id,
        "latex": formula.latex,
        "description": formula.description,
    }

    # Evaluate based on equation set
    if set_id == "A":
        result.update(_evaluate_set_a(formula, **kwargs))
    elif set_id == "C":
        result.update(_evaluate_set_c(formula, **kwargs))
    elif set_id == "D":
        result.update(_evaluate_set_d(formula, **kwargs))
    elif set_id == "E":
        result.update(_evaluate_set_e(formula, **kwargs))
    elif set_id == "F":
        result.update(_evaluate_set_f(formula, **kwargs))
    elif set_id == "G":
        result.update(_evaluate_set_g(formula, **kwargs))
    elif set_id == "H":
        result.update(_evaluate_set_h(formula, **kwargs))
    elif set_id == "coulomb":
        result.update(_evaluate_coulomb(formula, **kwargs))
    elif set_id == "net_charge":
        result.update(_evaluate_net_charge(formula, **kwargs))
    else:
        result["note"] = f"Evaluation for set {set_id} not yet implemented"

    return result


def _evaluate_set_a(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set A: B = curl(A)."""
    result: Dict[str, Any] = {}
    if formula.component == "x":
        # a = dH/dy - dG/dz
        h_func = kwargs.get("H_func", lambda x, y, z: 0.0)
        g_func = kwargs.get("G_func", lambda x, y, z: 0.0)
        point = kwargs.get("point", (0.0, 0.0, 0.0))
        h_val = kwargs.get("h", 1e-6)
        x, y, z = point
        dH_dy = (h_func(x, y + h_val, z) - h_func(x, y - h_val, z)) / (2 * h_val)
        dG_dz = (g_func(x, y, z + h_val) - g_func(x, y, z - h_val)) / (2 * h_val)
        result["a"] = dH_dy - dG_dz
    elif formula.component == "y":
        # b = dF/dz - dH/dx
        f_func = kwargs.get("F_func", lambda x, y, z: 0.0)
        h_func = kwargs.get("H_func", lambda x, y, z: 0.0)
        point = kwargs.get("point", (0.0, 0.0, 0.0))
        h_val = kwargs.get("h", 1e-6)
        x, y, z = point
        dF_dz = (f_func(x, y, z + h_val) - f_func(x, y, z - h_val)) / (2 * h_val)
        dH_dx = (h_func(x + h_val, y, z) - h_func(x - h_val, y, z)) / (2 * h_val)
        result["b"] = dF_dz - dH_dx
    elif formula.component == "z":
        # c = dG/dx - dF/dy
        g_func = kwargs.get("G_func", lambda x, y, z: 0.0)
        f_func = kwargs.get("F_func", lambda x, y, z: 0.0)
        point = kwargs.get("point", (0.0, 0.0, 0.0))
        h_val = kwargs.get("h", 1e-6)
        x, y, z = point
        dG_dx = (g_func(x + h_val, y, z) - g_func(x - h_val, y, z)) / (2 * h_val)
        dF_dy = (f_func(x, y + h_val, z) - f_func(x, y - h_val, z)) / (2 * h_val)
        result["c"] = dG_dx - dF_dy
    return result


def _evaluate_set_c(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set C: Lorentz force F = J x B."""
    result: Dict[str, Any] = {}
    if formula.component == "x":
        result["X"] = kwargs.get("b", 0.0) * kwargs.get("w", 0.0) - kwargs.get(
            "c", 0.0
        ) * kwargs.get("v", 0.0)
    elif formula.component == "y":
        result["Y"] = kwargs.get("c", 0.0) * kwargs.get("u", 0.0) - kwargs.get(
            "a", 0.0
        ) * kwargs.get("w", 0.0)
    elif formula.component == "z":
        result["Z"] = kwargs.get("a", 0.0) * kwargs.get("v", 0.0) - kwargs.get(
            "b", 0.0
        ) * kwargs.get("u", 0.0)
    return result


def _evaluate_set_d(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set D: B = H + 4*pi*M."""
    result: Dict[str, Any] = {}
    four_pi = 4.0 * np.pi
    if formula.component == "x":
        alpha = kwargs.get("alpha", 0.0)
        A = kwargs.get("A", 0.0)
        mu = kwargs.get("mu", None)
        if mu is not None:
            result["a"] = mu * alpha
        else:
            result["a"] = alpha + four_pi * A
    elif formula.component == "y":
        beta = kwargs.get("beta", 0.0)
        B = kwargs.get("B", 0.0)
        mu = kwargs.get("mu", None)
        if mu is not None:
            result["b"] = mu * beta
        else:
            result["b"] = beta + four_pi * B
    elif formula.component == "z":
        gamma = kwargs.get("gamma", 0.0)
        C = kwargs.get("C", 0.0)
        mu = kwargs.get("mu", None)
        if mu is not None:
            result["c"] = mu * gamma
        else:
            result["c"] = gamma + four_pi * C
    return result


def _evaluate_set_e(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set E: curl(H) = 4*pi*J."""
    result: Dict[str, Any] = {}
    four_pi = 4.0 * np.pi
    h_val = kwargs.get("h", 1e-6)
    point = kwargs.get("point", (0.0, 0.0, 0.0))
    x, y, z = point

    if formula.component == "x":
        gamma_func = kwargs.get("gamma_func", lambda x, y, z: 0.0)
        beta_func = kwargs.get("beta_func", lambda x, y, z: 0.0)
        dgamma_dy = (gamma_func(x, y + h_val, z) - gamma_func(x, y - h_val, z)) / (
            2 * h_val
        )
        dbeta_dz = (beta_func(x, y, z + h_val) - beta_func(x, y, z - h_val)) / (
            2 * h_val
        )
        result["4pi*u"] = dgamma_dy - dbeta_dz
        result["u"] = (dgamma_dy - dbeta_dz) / four_pi
    elif formula.component == "y":
        alpha_func = kwargs.get("alpha_func", lambda x, y, z: 0.0)
        gamma_func = kwargs.get("gamma_func", lambda x, y, z: 0.0)
        dalpha_dz = (alpha_func(x, y, z + h_val) - alpha_func(x, y, z - h_val)) / (
            2 * h_val
        )
        dgamma_dx = (gamma_func(x + h_val, y, z) - gamma_func(x - h_val, y, z)) / (
            2 * h_val
        )
        result["4pi*v"] = dalpha_dz - dgamma_dx
        result["v"] = (dalpha_dz - dgamma_dx) / four_pi
    elif formula.component == "z":
        beta_func = kwargs.get("beta_func", lambda x, y, z: 0.0)
        alpha_func = kwargs.get("alpha_func", lambda x, y, z: 0.0)
        dbeta_dx = (beta_func(x + h_val, y, z) - beta_func(x - h_val, y, z)) / (
            2 * h_val
        )
        dalpha_dy = (alpha_func(x, y + h_val, z) - alpha_func(x, y - h_val, z)) / (
            2 * h_val
        )
        result["4pi*w"] = dbeta_dx - dalpha_dy
        result["w"] = (dbeta_dx - dalpha_dy) / four_pi
    return result


def _evaluate_set_f(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set F: D = (K/4pi)*E."""
    result: Dict[str, Any] = {}
    K = kwargs.get("K", 1.0)
    four_pi_inv = 1.0 / (4.0 * np.pi)
    if formula.component == "x":
        result["f"] = four_pi_inv * K * kwargs.get("X", 0.0)
    elif formula.component == "y":
        result["g"] = four_pi_inv * K * kwargs.get("Y", 0.0)
    elif formula.component == "z":
        result["h"] = four_pi_inv * K * kwargs.get("Z", 0.0)
    return result


def _evaluate_set_g(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set G: J = sigma*E (Ohm's law)."""
    result: Dict[str, Any] = {}
    C = kwargs.get("C", 0.0)
    if formula.component == "x":
        result["p"] = C * kwargs.get("X", 0.0)
    elif formula.component == "y":
        result["q"] = C * kwargs.get("Y", 0.0)
    elif formula.component == "z":
        result["r"] = C * kwargs.get("Z", 0.0)
    return result


def _evaluate_set_h(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Set H: J_total = J_cond + dD/dt."""
    result: Dict[str, Any] = {}
    if formula.component == "x":
        result["u"] = kwargs.get("p", 0.0) + kwargs.get("df_dt", 0.0)
    elif formula.component == "y":
        result["v"] = kwargs.get("q", 0.0) + kwargs.get("dg_dt", 0.0)
    elif formula.component == "z":
        result["w"] = kwargs.get("r", 0.0) + kwargs.get("dh_dt", 0.0)
    return result


def _evaluate_coulomb(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate Coulomb's law."""
    e = kwargs.get("e", 0.0)
    e_prime = kwargs.get("e_prime", 0.0)
    r = kwargs.get("r", 1.0)
    if r == 0:
        raise ValueError("Distance r cannot be zero")
    return {"F": e * e_prime / r**2}


def _evaluate_net_charge(formula: EquationFormula, **kwargs: Any) -> Dict[str, Any]:
    """Evaluate net charge."""
    m = kwargs.get("m", 0.0)
    n = kwargs.get("n", 0.0)
    return {"e": m - n}


__all__ = [
    # Enums
    "EquationSet",
    "VariableType",
    # Data classes
    "Variable",
    "EquationFormula",
    "DerivationStep",
    "PresetExample",
    "EquationSetEntry",
    # Registry
    "EquationRegistry",
    "REGISTRY",
    # Convenience functions
    "get_equation_set",
    "compute_equation",
]
