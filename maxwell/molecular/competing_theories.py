"""maxwell.molecular.competing_theories — Comparison of electromagnetic
theories (Arts. 841-866).

Implements Maxwell's critical comparison of the competing
electromagnetic theories — Ampere's molecular currents, Weber's
action-at-a-distance force law, Neumann's potential formulation —
against Maxwell's own field theory.

COMPUTE-OR-DELETE REMEDIATION (Stage 3 defects D-09 / D-11):
    The previous version of this module carried invented "agreement
    scores" (0.95, 0.9, 0.85, ...) and hardcoded consistency booleans
    that were not computed from anything.  Every such literal has been
    deleted.  All quantitative entries now returned by this module are
    RESIDUALS computed from the theories' own formulas as implemented
    in ``maxwell.molecular.amperes_theory``, ``webers_theory``, and
    ``neumanns_theory``:

        residual = |computed_value - reference_value| / |reference|

    where the reference is an independent analytic result (elliptic
    closed form, far-field dipole limit, Ampere's wire force, energy
    integral, ...).  A residual of 0 means exact agreement; larger
    means worse.  Qualitative strengths/limitations are retained ONLY
    as labeled commentary (dict entries under keys marked
    ``*_commentary`` or inside ``critiques`` lists), never as numbers.

    Residual keys deliberately avoid the words "agreement", "score",
    and "confidence" so that anti-theater lint can verify no literal
    verdicts remain.

Categories:
    A (maxwell_original) — the comparison framework of Arts. 859-866.
    C (standard_math) — the numerical residual computations.

References:
    Part IV, Ch. XXII (Arts. 832-845), Ch. XXIII (Arts. 846-866).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite
from maxwell.molecular.amperes_theory import (
    AmperesTheory,
    calc_molecular_field,
    calc_molecular_moment,
    sphere_center_field_rings,
)
from maxwell.molecular.neumanns_theory import (
    maxwell_mutual_inductance_closed_form,
    motional_emf_coaxial,
    neumann_far_field_residual,
    neumann_mutual_inductance,
    neumann_reciprocity_residual,
)
from maxwell.molecular.webers_theory import (
    WebersTheory,
    ampere_wire_force_recovery,
    calc_weber_force,
    critical_velocity,
    weber_energy_conservation_residual,
)

# =============================================================================
# COMPUTED RESIDUALS PER THEORY (all values are computations, not literals)
# =============================================================================


def _ampere_computed_residuals() -> Dict[str, float]:
    """Residuals computed from Ampere's molecular-current formulas.

    References used (independent analytic results):
      * dipole field on axis:        B = +2m/r^3        (Art. 833)
      * dipole field at equator:     B = -m/r^3         (Art. 833)
      * magnetization:               M = N m f          (Art. 835)
      * sphere interior field:       B = (8 pi/3) M     (Art. 840)
    """
    m = calc_molecular_moment(1e-6, 1e-16)
    r = 1e-6

    B_axis, _ = calc_molecular_field(m, r, 0.0)
    axis_residual = abs(B_axis - 2.0 * m / r**3) / abs(2.0 * m / r**3)

    _, B_eq = calc_molecular_field(m, r, np.pi / 2)
    equator_residual = abs(B_eq + m / r**3) / abs(m / r**3)

    at = AmperesTheory(number_density=1e23, alignment_factor=0.5)
    M = at.magnetization(m)
    magnetization_residual = abs(M - 1e23 * m * 0.5) / abs(1e23 * m * 0.5)

    M_vec = np.array([0.0, 0.0, 50.0])
    B_sphere = sphere_center_field_rings(M_vec, 1.0)
    expected_sphere = (8.0 * np.pi / 3.0) * M_vec
    sphere_residual = float(
        np.linalg.norm(B_sphere - expected_sphere) / np.linalg.norm(expected_sphere)
    )

    return {
        "dipole_axis_residual": float(axis_residual),
        "dipole_equator_residual": float(equator_residual),
        "magnetization_residual": float(magnetization_residual),
        "sphere_interior_field_residual": sphere_residual,
    }


def _weber_computed_residuals() -> Dict[str, float]:
    """Residuals computed from Weber's force law.

    References used:
      * Coulomb limit (v = a = 0): F = q1 q2 / r^2           (Art. 843)
      * wire-force closed form for finite wires               (Art. 846)
      * conservation of the Weber energy integral             (Art. 850)
      * action-reaction pairwise equality of element forces   (Art. 846)
    """
    # 1. Coulomb limit of the force law (identity at v = a = 0).
    q1 = q2 = 1.0
    r_sep = 2.0
    F_static = calc_weber_force(q1, q2, r_sep, 0.0, 0.0)
    F_coulomb = q1 * q2 / r_sep**2
    coulomb_residual = abs(F_static - F_coulomb) / abs(F_coulomb)

    # 2. Recovery of the Ampere parallel-wire force (finite-length
    #    closed form isolates quadrature error from truncation).
    wire = ampere_wire_force_recovery(1.0, 1.0, 1.0, 50.0, n_segments=400)
    wire_residual = wire["relative_residual_vs_finite_closed_form"]
    wire_infinite_residual = wire["relative_residual_vs_infinite_limit"]

    # 3. Conservation of the Weber energy integral along an RK4
    #    trajectory of the implicit force law.
    energy_residual = weber_energy_conservation_residual(n_steps=2000)

    # 4. Action-reaction: element force on (1,2) plus the force on
    #    (2,1) with reversed separation must cancel.
    wt = WebersTheory()
    dl1 = np.array([0.1, 0.0, 0.0])
    dl2 = np.array([0.0, 0.05, 0.1])
    r_vec = np.array([0.3, 0.2, 0.5])
    F12 = wt.force_between_current_elements(1.0, 2.0, dl1, dl2, r_vec)
    F21 = wt.force_between_current_elements(2.0, 1.0, dl2, dl1, -r_vec)
    action_reaction_residual = abs(F12 + F21) / max(abs(F12), 1e-30)

    return {
        "coulomb_limit_residual": float(coulomb_residual),
        "ampere_wire_recovery_residual": float(wire_residual),
        "ampere_wire_infinite_limit_residual": float(wire_infinite_residual),
        "energy_integral_residual": float(energy_residual),
        "action_reaction_residual": float(action_reaction_residual),
    }


def _neumann_computed_residuals() -> Dict[str, float]:
    """Residuals computed from Neumann's mutual-inductance formula.

    References used:
      * reciprocity M12 = M21                            (Art. 856)
      * Maxwell's elliptic closed form for coaxial loops (Art. 853)
      * far-field dipole limit M -> 2 pi^2 R1^2 R2^2/d^3 (Art. 857)
      * Lenz sign of the motional EMF                    (Art. 858)
    """
    reciprocity = neumann_reciprocity_residual(
        R1=1.0, R2=2.0, d=3.0, n_segments_12=160, n_segments_21=120
    )

    M_quad = neumann_mutual_inductance(1.0, 2.0, 3.0, n_segments=240)
    M_closed = maxwell_mutual_inductance_closed_form(1.0, 2.0, 3.0)
    closed_form_residual = abs(M_quad - M_closed) / abs(M_closed)

    far_field = neumann_far_field_residual(R1=1.0, R2=1.0, d=20.0)

    # Lenz sign: pulling the loops apart (v > 0) with I > 0 must induce
    # an EMF whose sign drives a current supporting the decreasing flux,
    # i.e. EMF has the sign of I * v because dM/dd < 0.
    emf = motional_emf_coaxial(1.0, 1.0, 5.0, current=1.0, velocity=10.0)
    lenz_sign_residual = 0.0 if emf > 0 else 1.0

    return {
        "reciprocity_residual": float(reciprocity),
        "elliptic_closed_form_residual": float(closed_form_residual),
        "far_field_dipole_residual": float(far_field),
        "motional_emf_lenz_sign_residual": float(lenz_sign_residual),
    }


def _maxwell_computed_residuals() -> Dict[str, float]:
    """Residual computed for Maxwell's own theory.

    Reference: the ratio of the electromagnetic unit velocity
    (Weber-Kohlrausch, 3.1e10 cm/s) to Fizeau's measured speed of light
    (3.15e10 cm/s) as recorded by Maxwell — the numerical anchor of the
    electromagnetic theory of light.
    """
    c_em = 3.1e10
    c_light = 3.15e10
    return {
        "historical_wave_speed_residual": float(abs(c_em - c_light) / c_light),
    }


_RESIDUAL_BUILDERS: Dict[str, Callable[[], Dict[str, float]]] = {
    "Ampere": _ampere_computed_residuals,
    "Weber": _weber_computed_residuals,
    "Neumann": _neumann_computed_residuals,
    "Maxwell": _maxwell_computed_residuals,
}


def _computed_checks(theory_name: str) -> Dict[str, bool]:
    """Boolean consistency checks derived from the computed residuals.

    Every value below is thresholded numerical evidence, not assertion.
    """
    if theory_name == "Weber":
        res = _weber_computed_residuals()
        v_crit = critical_velocity()
        return {
            "energy_conservation": bool(res["energy_integral_residual"] < 1e-8),
            "action_reaction": bool(res["action_reaction_residual"] < 1e-10),
            "coulomb_limit_exact": bool(res["coulomb_limit_residual"] < 1e-12),
            "critical_velocity_exceeds_light": bool(v_crit > CONST.C),
        }
    if theory_name == "Neumann":
        res = _neumann_computed_residuals()
        return {
            "reciprocity": bool(res["reciprocity_residual"] < 1e-6),
            "matches_elliptic_closed_form": bool(
                res["elliptic_closed_form_residual"] < 1e-2
            ),
            "correct_far_field_limit": bool(res["far_field_dipole_residual"] < 5e-2),
            "lenz_sign": bool(res["motional_emf_lenz_sign_residual"] == 0.0),
        }
    if theory_name == "Ampere":
        res = _ampere_computed_residuals()
        return {
            "dipole_field_axis": bool(res["dipole_axis_residual"] < 1e-10),
            "dipole_field_equator": bool(res["dipole_equator_residual"] < 1e-10),
            "sphere_interior_field": bool(res["sphere_interior_field_residual"] < 1e-6),
        }
    if theory_name == "Maxwell":
        res = _maxwell_computed_residuals()
        return {
            "wave_speed_matches_light": bool(
                res["historical_wave_speed_residual"] < 0.1
            ),
        }
    return {}


# =============================================================================
# THEORY DATA MODEL
# =============================================================================


@dataclass
class CompetingTheory:
    """
    Representation of a competing electromagnetic theory.

    Art. 859-866: Maxwell's framework for comparing different
    theoretical approaches to electromagnetic phenomena.

    Attributes:
        name: Theory name (e.g., "Maxwell", "Weber", "Neumann").
        fundamental_entity: Primary theoretical entity (descriptive).
        action_type: "field" or "action_at_distance" (descriptive).
        energy_localization: Where energy is stored (descriptive).
    """

    name: str = "Unknown"
    fundamental_entity: str = "unknown"
    action_type: str = "unknown"
    energy_localization: str = "unknown"

    @maxwell_cite(
        859,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Get theory characteristics",
    )
    def characteristics(self) -> Dict[str, str]:
        """
        Get the key characteristics of this theory.

        Art. 859: Each theory is characterized by its fundamental
        entity, type of action, and energy localization.  These are
        descriptive classifications, not scores.

        Returns:
            Dictionary of theory characteristics.

        Reference:
            Part IV, Art. 859: Theory characteristics.
        """
        return {
            "name": self.name,
            "fundamental_entity": self.fundamental_entity,
            "action_type": self.action_type,
            "energy_localization": self.energy_localization,
        }

    @maxwell_cite(
        860,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="standard_math",
        description="Compute theory residuals against analytic references",
    )
    def computed_residuals(self) -> Dict[str, float]:
        """
        Compute the theory's residuals against analytic references.

        Art. 860 (compute-or-delete): replaces the former literal
        "agreement scores".  Each entry is

            |computed - reference| / |reference|

        evaluated from the theory's own formulas (see the per-theory
        builders at module level).  0 = exact agreement.  Theories with
        no registered computable checks yield an empty dict — an honest
        admission that nothing was computed.

        Returns:
            Dictionary of residual magnitudes (dimensionless).

        Reference:
            Part IV, Art. 860: Comparison with the facts.
        """
        builder = _RESIDUAL_BUILDERS.get(self.name)
        return builder() if builder is not None else {}

    @maxwell_cite(
        861,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="standard_math",
        description="Computed consistency checks (thresholded residuals)",
    )
    def computed_checks(self) -> Dict[str, bool]:
        """
        Computed consistency checks for the theory.

        Art. 861 (compute-or-delete): replaces hardcoded consistency
        booleans.  Each check is a thresholded residual computed from
        the theory's own formulas.  Checks that are not numerically
        decidable (e.g. historical objections about causality) are NOT
        listed here; they appear as labeled commentary in
        :func:`maxwell_critiques`.

        Returns:
            Dictionary of computed boolean checks.

        Reference:
            Part IV, Art. 861: Internal consistency.
        """
        return _computed_checks(self.name)

    @maxwell_cite(
        862,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="standard_math",
        description="Full computed comparison entry for one theory",
    )
    def compare_all(self, phenomena: Optional[List[str]] = None) -> Dict[str, Dict]:
        """
        Compare this theory across all computable criteria.

        Art. 862: the returned entry contains characteristics
        (descriptive), computed residuals, computed checks, and the
        summary statistics max_residual / n_residuals — all derived
        from actual computations.

        Args:
            phenomena: Unused (retained for API compatibility); kept
                so older callers do not break.

        Returns:
            Nested dictionary with the computed comparison entry.

        Reference:
            Part IV, Art. 862: Full theory comparison.
        """
        residuals = self.computed_residuals()
        checks = self.computed_checks()
        return {
            self.name: {
                "characteristics": self.characteristics(),
                "computed_residuals": residuals,
                "computed_checks": checks,
                "max_residual": (
                    float(max(residuals.values())) if residuals else float("inf")
                ),
                "n_residuals": len(residuals),
                "n_checks_passed": int(sum(checks.values())),
            }
        }


@dataclass
class TheoryComparison:
    """
    Comparative analysis of electromagnetic theories.

    Art. 859-866: Maxwell's systematic comparison of all
    competing electromagnetic theories.

    Attributes:
        theories: List of theories to compare.
    """

    theories: List[CompetingTheory] = field(default_factory=list)

    def __post_init__(self):
        """Initialize with standard theories if empty."""
        if not self.theories:
            self.theories = [
                CompetingTheory(
                    name="Maxwell",
                    fundamental_entity="electromagnetic_field",
                    action_type="field",
                    energy_localization="field",
                ),
                CompetingTheory(
                    name="Weber",
                    fundamental_entity="moving_charge",
                    action_type="action_at_distance",
                    energy_localization="particle_interaction",
                ),
                CompetingTheory(
                    name="Neumann",
                    fundamental_entity="vector_potential",
                    action_type="potential",
                    energy_localization="circuit_coupling",
                ),
            ]

    @maxwell_cite(
        862,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="standard_math",
        description="Compare all theories across computed criteria",
    )
    def compare_all(self, phenomena: Optional[List[str]] = None) -> Dict[str, Dict]:
        """
        Compare all theories across the computable criteria.

        Art. 862: each entry contains characteristics, computed
        residuals, computed checks, and summary statistics.  No literal
        scores remain: every number is computed from a theory formula.

        Args:
            phenomena: Unused (retained for API compatibility).

        Returns:
            Nested dictionary with computed comparison results.

        Reference:
            Part IV, Art. 862: Full theory comparison.
        """
        comparison = {}
        for theory in self.theories:
            entry = theory.compare_all(phenomena)[theory.name]
            comparison[theory.name] = entry
        return comparison


# =============================================================================
# HISTORICAL COMMENTARY (clearly labeled, never scored)
# =============================================================================


def maxwell_critiques() -> Dict[str, List[str]]:
    """
    Maxwell's recorded objections, as labeled commentary.

    These are historical statements from the Treatise, preserved as
    strings with attribution.  They are deliberately NOT converted into
    numbers: causality and interpretive objections are not computable
    from the force law.  Where a critique has a computable counterpart
    (e.g. the critical velocity of Art. 849), the computation lives in
    ``webers_theory`` and is surfaced via the computed checks.

    This function carries no ``@maxwell_cite`` decorator on purpose: it
    records commentary rather than implementing an article's computation,
    so citing the articles here would overstate what the code does.
    Provenance is kept in the reference below instead.

    Returns:
        Dictionary mapping theory name to a list of recorded critiques.

    Reference:
        Part IV, Arts. 848-850: Maxwell's objections to Weber's theory.
    """
    return {
        "Weber": [
            "Art. 849: the force changes sign at the critical velocity "
            "sqrt(2) c, which exceeds the speed of light (computed in "
            "webers_theory.critical_velocity).",
            "Art. 850: the potential energy of two particles depends on "
            "their relative velocity, contrary to the ordinary notion of "
            "potential energy (the energy integral is nevertheless "
            "conserved; see weber_energy_conservation_residual).",
            "Weber's law contains the acceleration of the particles, so "
            "the force is not determined by the instantaneous state of "
            "position and velocity alone.",
        ],
        "Neumann": [
            "Neumann's potential is confined to closed circuits and does "
            "not provide a local account of the field between them.",
            "The theory gives no mechanism for the propagation of "
            "disturbances at finite speed.",
        ],
        "Ampere": [
            "Ampere's molecular currents describe the statics of "
            "magnetized bodies but not the propagation of electromagnetic "
            "disturbances.",
        ],
    }


# =============================================================================
# MODULE-LEVEL COMPARISON FUNCTIONS
# =============================================================================


@maxwell_cite(
    859,
    860,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Compare electromagnetic theories via computed residuals",
)
def compare_electromagnetic_theories(
    theory_names: Optional[List[str]] = None,
    phenomena: Optional[List[str]] = None,
) -> Dict[str, Dict]:
    """
    Compare electromagnetic theories.

    Art. 859-860: Systematic comparison of competing theories through
    computed residuals against analytic references.

    Args:
        theory_names: Names of theories to compare.
        phenomena: Unused (retained for API compatibility).

    Returns:
        Dictionary with computed comparison results.

    Reference:
        Part IV, Arts. 859-860: Theory comparison.

    Example:
        >>> result = compare_electromagnetic_theories()
        >>> for theory, data in result.items():
        ...     print(f"{theory}: max residual = {data['max_residual']:.2e}")
    """
    if theory_names is None:
        theory_names = ["Maxwell", "Weber", "Neumann"]

    theories = []
    theory_configs = {
        "Maxwell": ("electromagnetic_field", "field", "field"),
        "Weber": ("moving_charge", "action_at_distance", "particle_interaction"),
        "Neumann": ("vector_potential", "potential", "circuit_coupling"),
        "Ampere": ("molecular_current", "near_action", "molecular_currents"),
    }

    for name in theory_names:
        if name in theory_configs:
            fundamental, action, energy = theory_configs[name]
            theories.append(CompetingTheory(name, fundamental, action, energy))

    tc = TheoryComparison(theories=theories)
    return tc.compare_all(phenomena)


@maxwell_cite(
    861,
    862,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Analyze computed differences between two theories",
)
def analyze_theory_differences(
    theory1: str = "Maxwell",
    theory2: str = "Weber",
) -> Dict[str, object]:
    """
    Analyze key differences between two theories.

    Art. 861-862: conceptual differences (descriptive characteristics),
    residual differences on shared computed checks, and a computed
    verdict on which theory has the smaller total residual.

    Args:
        theory1: First theory name.
        theory2: Second theory name.

    Returns:
        Dictionary with difference analysis.

    Reference:
        Part IV, Arts. 861-862: Theory differences.
    """
    t1 = CompetingTheory(name=theory1)
    t2 = CompetingTheory(name=theory2)

    chars1 = t1.characteristics()
    chars2 = t2.characteristics()

    conceptual_diffs = []
    for key in chars1:
        if chars1.get(key) != chars2.get(key):
            conceptual_diffs.append(f"{key}: {chars1.get(key)} vs {chars2.get(key)}")

    res1 = t1.computed_residuals()
    res2 = t2.computed_residuals()
    shared = sorted(set(res1) & set(res2))
    residual_differences = {k: res1[k] - res2[k] for k in shared}

    total1 = float(sum(res1.values())) if res1 else float("inf")
    total2 = float(sum(res2.values())) if res2 else float("inf")
    if not res1 and not res2:
        verdict = "inconclusive (no computed residuals on either side)"
    elif total1 < total2:
        verdict = theory1
    elif total2 < total1:
        verdict = theory2
    else:
        verdict = "tie"

    return {
        "theory1": theory1,
        "theory2": theory2,
        "conceptual_differences": conceptual_diffs,
        "shared_residual_differences": residual_differences,
        "total_residual_theory1": total1,
        "total_residual_theory2": total2,
        "key_distinction": chars1.get("action_type")
        + " vs "
        + chars2.get("action_type"),
        "computed_lower_residual_theory": verdict,
    }


@maxwell_cite(
    863,
    864,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Verify computed consistency of a theory",
)
def verify_theory_consistency(
    theory_name: str = "Maxwell",
    tolerance: float = 1e-10,
) -> Dict[str, object]:
    """
    Verify internal consistency of a theory from computed checks.

    Art. 863-864: every boolean below is derived by thresholding a
    residual computed from the theory's own formulas.  The tolerance
    parameter is retained for API compatibility; the thresholds used
    are documented in :func:`_computed_checks`.

    Args:
        theory_name: Name of theory to verify.
        tolerance: Retained for API compatibility (unused).

    Returns:
        Dictionary with computed verification results.

    Reference:
        Part IV, Arts. 863-864: Theory consistency verification.
    """
    theory = CompetingTheory(name=theory_name)
    checks = theory.computed_checks()

    passed_count = sum(1 for v in checks.values() if v)
    total_count = len(checks)
    all_passed = total_count > 0 and passed_count == total_count

    return {
        "theory": theory_name,
        "computed_checks": checks,
        "consistency_fraction": passed_count / total_count if total_count else 0.0,
        "fully_consistent": bool(all_passed),
        "verified": bool(all_passed),
    }


@maxwell_cite(
    862,
    866,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Synthesize the computed comparison of all theories",
)
def synthesize_theory_comparison() -> Dict[str, object]:
    """
    Complete synthesis of electromagnetic theory comparison.

    Art. 859-866: all theories compared on computed residuals, with the
    best-supported theory selected by smallest maximum residual (a
    computed verdict, not an assertion).

    Returns:
        Dictionary with complete synthesis.

    Reference:
        Part IV, Arts. 859-866: Complete theory synthesis.

    Example:
        >>> synthesis = synthesize_theory_comparison()
        >>> print(f"Lowest-residual theory: {synthesis['best_theory']}")
    """
    comparison = compare_electromagnetic_theories()

    finite_entries = {
        name: data
        for name, data in comparison.items()
        if np.isfinite(data["max_residual"])
    }
    best_theory = (
        min(finite_entries, key=lambda t: finite_entries[t]["max_residual"])
        if finite_entries
        else "none"
    )

    differences = {}
    theory_names = list(comparison.keys())
    for i, t1 in enumerate(theory_names):
        for t2 in theory_names[i + 1 :]:
            differences[f"{t1}_vs_{t2}"] = analyze_theory_differences(t1, t2)

    consistency_checks = {
        name: verify_theory_consistency(name) for name in theory_names
    }

    return {
        "comparison_results": comparison,
        "pairwise_differences": differences,
        "consistency_checks": consistency_checks,
        "best_theory": best_theory,
        "selection_rule": "smallest maximum computed residual",
        "maxwell_critiques": maxwell_critiques(),
        "key_insight_commentary": (
            "Commentary (Maxwell 1873, Arts. 865-866): the field theory "
            "localizes energy and propagates disturbances at finite "
            "speed; action-at-distance theories reproduce the same "
            "circuit-level facts but offer no local mechanism."
        ),
    }


# =============================================================================
# STANDALONE FUNCTIONS FOR DIRECT IMPORT (as expected by tests)
# =============================================================================


@maxwell_cite(
    859,
    860,
    861,
    862,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Compare all electromagnetic theories via computed " "residuals",
)
def compare_theories() -> Dict[str, Dict]:
    """
    Compare all electromagnetic theories.

    Art. 859-862 (compute-or-delete): entries for Ampere's, Weber's,
    and Neumann's theories, each populated with residuals computed from
    that theory's own formulas (no literal scores anywhere).

    Returns:
        Dictionary with computed comparison results for each theory.

    Reference:
        Part IV, Arts. 859-862: Theory comparison.

    Example:
        >>> result = compare_theories()
        >>> for name, data in result.items():
        ...     print(f"{name}: max residual = {data['max_residual']:.2e}")
    """
    comparison = compare_electromagnetic_theories(
        theory_names=["Ampere", "Weber", "Neumann"]
    )

    return {
        "amperes_theory": comparison.get("Ampere", {}),
        "webers_theory": comparison.get("Weber", {}),
        "neumanns_theory": comparison.get("Neumann", {}),
    }


@maxwell_cite(
    859,
    860,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Ampere's theory: descriptive commentary plus computed " "checks",
)
def analyze_amperes_theory() -> Dict[str, object]:
    """
    Analyze Ampere's molecular current theory.

    Art. 859-860: descriptive commentary (strings and labeled lists)
    together with residuals computed from the amperes_theory module.
    The former invented agreement scores have been deleted.

    Returns:
        Dictionary with analysis of Ampere's theory.

    Reference:
        Part IV, Arts. 859-860: Ampere's theory analysis.
    """
    return {
        "molecular_currents": "Magnetic phenomena arise from molecular current loops",
        "fundamental_entity": "Current loop",
        "action_type": "Near action through medium",
        "strengths_commentary": [
            "Explains magnetism through known electrical phenomena",
            "Provides mechanical model for magnetic moments",
        ],
        "limitations": [
            "Describes static and quasi-static magnetism only",
            "Contains no displacement current and no wave propagation",
        ],
        "computed_checks": _ampere_computed_residuals(),
    }


@maxwell_cite(
    843,
    846,
    849,
    850,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Weber's theory: descriptive commentary plus computed "
    "checks from the force law itself",
)
def analyze_webers_theory() -> Dict[str, object]:
    """
    Analyze Weber's velocity-dependent force theory.

    Art. 841-850: descriptive commentary together with residuals
    computed from Weber's own force law: Coulomb limit, recovery of the
    Ampere wire force, energy-integral conservation, and the critical
    velocity sign reversal (Maxwell's objection, now a computation).
    The former invented agreement scores have been deleted.

    Returns:
        Dictionary with analysis of Weber's theory.

    Reference:
        Part IV, Arts. 841-850: Weber's theory analysis.
    """
    weber_res = _weber_computed_residuals()
    v_crit = critical_velocity()
    below = calc_weber_force(1.0, 1.0, 1.0, 0.9 * v_crit, 0.0)
    above = calc_weber_force(1.0, 1.0, 1.0, 1.1 * v_crit, 0.0)
    weber_res["critical_velocity_sign_flip"] = float(
        1.0 if (below > 0 and above < 0) else 0.0
    )

    return {
        "velocity_dependent": "Force depends on relative velocity of charges",
        "action_at_distance": "Direct interaction without intermediary field",
        "fundamental_entity": "Moving charge",
        "strengths_commentary": [
            "Unifies electrostatic and electromagnetic phenomena",
            "Derives Ampere's force law from charge interactions",
        ],
        "limitations": [
            "Force reverses sign beyond the critical velocity sqrt(2) c "
            "(computed below)",
            "Energy integral depends on relative velocity",
            "No field concept for local energy storage",
        ],
        "computed_checks": weber_res,
        "maxwell_critiques": maxwell_critiques()["Weber"],
    }


@maxwell_cite(
    853,
    856,
    857,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Neumann's theory: descriptive commentary plus computed "
    "checks from the Neumann integral",
)
def analyze_neumanns_theory() -> Dict[str, object]:
    """
    Analyze Neumann's potential-based theory.

    Art. 851-858: descriptive commentary together with residuals
    computed from Neumann's formula: reciprocity, comparison with
    Maxwell's elliptic closed form, far-field dipole limit, and the
    Lenz sign of the motional EMF.  The former invented agreement
    scores have been deleted.

    Returns:
        Dictionary with analysis of Neumann's theory.

    Reference:
        Part IV, Arts. 851-858: Neumann's theory analysis.
    """
    return {
        "potential_based": "Uses vector potential as fundamental quantity",
        "induction_focus": "Primary focus on electromagnetic induction",
        "fundamental_entity": "Vector potential",
        "strengths_commentary": [
            "Elegant mathematical formulation of induction",
            "Reciprocity and energy expressions follow directly",
        ],
        "limitations": [
            "Limited to closed-circuit phenomena",
            "No wave propagation or displacement current",
            "No local energy transport mechanism",
        ],
        "computed_checks": _neumann_computed_residuals(),
    }


@maxwell_cite(
    865,
    866,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Maxwell's field theory: commentary plus the computed "
    "wave-speed check",
)
def maxwell_advantages() -> Dict[str, object]:
    """
    Describe Maxwell's field theory relative to competing theories.

    Art. 865-866: descriptive commentary together with the one
    quantitative anchor Maxwell himself used — the agreement of the
    electromagnetic unit velocity with the measured speed of light,
    computed here from the historical numbers (3.1e10 vs 3.15e10 cm/s).
    The former all-1.0 "agreement" dict has been deleted.

    Returns:
        Dictionary with Maxwell's theory description.

    Reference:
        Part IV, Arts. 865-866: Maxwell's theory assessment.
    """
    return {
        "field_concept": "Electromagnetic field as physical entity",
        "displacement_current": "Time-varying electric field produces magnetic field",
        "fundamental_entity": "Electromagnetic field",
        "strengths_commentary": [
            "Local energy conservation via the Poynting vector",
            "Causal propagation at finite speed",
            "Predicts electromagnetic waves",
        ],
        "advantages_over_competitors_commentary": {
            "vs_weber": [
                "No superluminal critical velocity",
                "Local energy storage in the field",
            ],
            "vs_neumann": [
                "Generalizes beyond closed circuits",
                "Displacement current completes the dynamics",
            ],
            "vs_ampere": [
                "Includes time-varying phenomena and wave propagation",
            ],
        },
        "computed_checks": _maxwell_computed_residuals(),
    }


@maxwell_cite(
    859,
    860,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Induced magnetization of a diamagnetic body",
)
def diamagnetic_response(
    applied_field: float,
    material_constant: float = -1e-5,
) -> float:
    """
    Calculate the induced magnetization of a diamagnetic body.

    Art. 859-860 (compute-or-delete, defect D-18): the former version
    returned the input ``material_constant`` unchanged.  The function
    now COMPUTES the induced magnetization

        M_ind = chi · H

    from the susceptibility chi (``material_constant``) and the applied
    field H.  Diamagnetic susceptibilities are negative because the
    induced molecular currents oppose the applied field (Lenz's law),
    so M_ind is negative for positive applied field.

    Args:
        applied_field: Applied magnetic field H (gauss).
        material_constant: Susceptibility chi (dimensionless, negative
            for diamagnets; default is the order of magnitude of
            bismuth-free weak diamagnets).

    Returns:
        Induced magnetization M_ind = chi H (gauss).

    Reference:
        Part IV, Arts. 859-860: Diamagnetic response.
    """
    return material_constant * applied_field


# Alias for backwards compatibility
maxwells_theory_advantages = maxwell_advantages
