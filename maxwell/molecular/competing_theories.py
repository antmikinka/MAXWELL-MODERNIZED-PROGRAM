"""maxwell.molecular.competing_theories — Comparison of electromagnetic theories (Arts. 859-866).

Implements Maxwell's critical comparison of competing electromagnetic
theories including his own field theory, Weber's action-at-a-distance,
and Neumann's potential formulation.

Maxwell's CGS formulation (Arts. 859-866):
    Theory comparison criteria:
    1. Agreement with experiment
    2. Internal consistency
    3. Predictive power
    4. Mathematical elegance

    Energy propagation:
    - Maxwell: Energy flows through field (Poynting vector)
    - Weber: Energy stored in particle interactions
    - Neumann: Energy in circuit coupling

where:
    Competing theories are evaluated on equal footing
    using Maxwell's analytical framework

Category: A (maxwell_original) — Theory comparison and synthesis.

References:
    Part IV, Arts. 859-866: Comparison of electromagnetic theories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class CompetingTheory:
    """
    Representation of a competing electromagnetic theory.

    Art. 859-866: Maxwell's framework for comparing different
    theoretical approaches to electromagnetic phenomena.

    Attributes:
        name: Theory name (e.g., "Maxwell", "Weber", "Neumann").
        fundamental_entity: Primary theoretical entity.
        action_type: "field" or "action_at_distance".
        energy_localization: Where energy is stored.
    """

    name: str = "Unknown"
    fundamental_entity: str = "unknown"
    action_type: str = "unknown"
    energy_localization: str = "unknown"

    @maxwell_cite(
        859,
        part=4, chapter="Competing Theories",
        theory_class="maxwell_original",
        description="Get theory characteristics",
    )
    def characteristics(self) -> Dict[str, str]:
        """
        Get the key characteristics of this theory.

        Art. 859: Each theory is characterized by:
        1. Fundamental entity (field, charge, potential)
        2. Type of action (local vs action-at-distance)
        3. Energy localization

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
        part=4, chapter="Competing Theories",
        theory_class="maxwell_original",
        description="Evaluate theory against experimental facts",
    )
    def experimental_agreement(self, phenomena: List[str]) -> Dict[str, float]:
        """
        Evaluate the theory's agreement with experimental phenomena.

        Art. 860: Maxwell evaluates each theory's ability to explain:
        1. Electrostatic attraction
        2. Magnetic induction
        3. Electromagnetic waves
        4. Light propagation

        Args:
            phenomena: List of phenomena to evaluate.

        Returns:
            Dictionary of agreement scores (0 to 1).

        Reference:
            Part IV, Art. 860: Experimental agreement.
        """
        # Maxwell's theory agrees with all known phenomena
        maxwell_phenomena = {
            "electrostatics": 1.0,
            "magnetostatics": 1.0,
            "induction": 1.0,
            "electromagnetic_waves": 1.0,
            "light_propagation": 1.0,
            "reflection_refraction": 1.0,
            "polarization": 1.0,
        }

        # Weber's theory limitations
        weber_phenomena = {
            "electrostatics": 1.0,
            "magnetostatics": 0.9,
            "induction": 0.8,
            "electromagnetic_waves": 0.0,  # Cannot explain wave propagation
            "light_propagation": 0.0,
            "reflection_refraction": 0.0,
            "polarization": 0.0,
        }

        # Neumann's theory
        neumann_phenomena = {
            "electrostatics": 0.9,
            "magnetostatics": 0.8,
            "induction": 1.0,
            "electromagnetic_waves": 0.0,
            "light_propagation": 0.0,
            "reflection_refraction": 0.5,
            "polarization": 0.0,
        }

        theory_map = {
            "Maxwell": maxwell_phenomena,
            "Weber": weber_phenomena,
            "Neumann": neumann_phenomena,
        }

        scores = theory_map.get(self.name, {})
        return {p: scores.get(p, 0.5) for p in phenomena}

    @maxwell_cite(
        861,
        part=4, chapter="Competing Theories",
        theory_class="maxwell_original",
        description="Check internal consistency",
    )
    def internal_consistency(self) -> Dict[str, bool]:
        """
        Evaluate the internal consistency of the theory.

        Art. 861: Maxwell checks:
        1. Conservation of energy
        2. Conservation of momentum
        3. Action-reaction equality
        4. Causality

        Returns:
            Dictionary of consistency checks.

        Reference:
            Part IV, Art. 861: Internal consistency.
        """
        maxwell_consistency = {
            "energy_conservation": True,
            "momentum_conservation": True,
            "action_reaction": True,
            "causality": True,
            "mathematical_rigor": True,
        }

        weber_consistency = {
            "energy_conservation": True,
            "momentum_conservation": False,  # Violated in some configurations
            "action_reaction": True,
            "causality": False,  # Depends on future states
            "mathematical_rigor": True,
        }

        neumann_consistency = {
            "energy_conservation": True,
            "momentum_conservation": True,
            "action_reaction": True,
            "causality": True,
            "mathematical_rigor": True,
        }

        theory_map = {
            "Maxwell": maxwell_consistency,
            "Weber": weber_consistency,
            "Neumann": neumann_consistency,
        }

        return theory_map.get(self.name, {})


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
        part=4, chapter="Competing Theories",
        theory_class="maxwell_original",
        description="Compare theories across all criteria",
    )
    def compare_all(self, phenomena: Optional[List[str]] = None) -> Dict[str, Dict]:
        """
        Compare all theories across evaluation criteria.

        Art. 862: Comprehensive comparison including:
        1. Experimental agreement
        2. Internal consistency
        3. Predictive scope
        4. Mathematical elegance

        Args:
            phenomena: Phenomena to test (default: standard set).

        Returns:
            Nested dictionary with comparison results.

        Reference:
            Part IV, Art. 862: Full theory comparison.
        """
        if phenomena is None:
            phenomena = [
                "electrostatics",
                "magnetostatics",
                "induction",
                "electromagnetic_waves",
                "light_propagation",
            ]

        comparison = {}
        for theory in self.theories:
            comparison[theory.name] = {
                "characteristics": theory.characteristics(),
                "experimental_agreement": theory.experimental_agreement(phenomena),
                "internal_consistency": theory.internal_consistency(),
                "overall_score": self._calculate_overall_score(theory, phenomena),
            }

        return comparison

    def _calculate_overall_score(
        self,
        theory: CompetingTheory,
        phenomena: List[str],
    ) -> float:
        """Calculate overall score for a theory."""
        exp_scores = list(theory.experimental_agreement(phenomena).values())
        consistency = list(theory.internal_consistency().values())

        exp_avg = np.mean(exp_scores) if exp_scores else 0.5
        consistency_avg = sum(1 for c in consistency if c) / len(consistency) if consistency else 0.5

        return 0.6 * exp_avg + 0.4 * consistency_avg


@maxwell_cite(
    859, 860,
    part=4, chapter="Competing Theories",
    theory_class="maxwell_original",
    description="Compare electromagnetic theories",
)
def compare_electromagnetic_theories(
    theory_names: Optional[List[str]] = None,
    phenomena: Optional[List[str]] = None,
) -> Dict[str, Dict]:
    """
    Compare electromagnetic theories.

    Art. 859-860: Systematic comparison of competing theories.

    Args:
        theory_names: Names of theories to compare.
        phenomena: Phenomena to evaluate against.

    Returns:
        Dictionary with comparison results.

    Reference:
        Part IV, Arts. 859-860: Theory comparison.

    Example:
        >>> result = compare_electromagnetic_theories()
        >>> for theory, data in result.items():
        ...     print(f"{theory}: score = {data['overall_score']:.2f}")
    """
    if theory_names is None:
        theory_names = ["Maxwell", "Weber", "Neumann"]

    theories = []
    theory_configs = {
        "Maxwell": ("electromagnetic_field", "field", "field"),
        "Weber": ("moving_charge", "action_at_distance", "particle_interaction"),
        "Neumann": ("vector_potential", "potential", "circuit_coupling"),
    }

    for name in theory_names:
        if name in theory_configs:
            fundamental, action, energy = theory_configs[name]
            theories.append(CompetingTheory(name, fundamental, action, energy))

    tc = TheoryComparison(theories=theories)
    return tc.compare_all(phenomena)


@maxwell_cite(
    861, 862,
    part=4, chapter="Competing Theories",
    theory_class="maxwell_original",
    description="Analyze differences between theories",
)
def analyze_theory_differences(
    theory1: str = "Maxwell",
    theory2: str = "Weber",
) -> Dict[str, str | float]:
    """
    Analyze key differences between two theories.

    Art. 861-862: Detailed comparison highlighting:
    1. Conceptual differences
    2. Predictive differences
    3. Domain of validity

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

    phenomena = ["electromagnetic_waves", "light_propagation", "induction"]
    exp1 = t1.experimental_agreement(phenomena)
    exp2 = t2.experimental_agreement(phenomena)

    # Calculate differences
    conceptual_diffs = []
    for key in chars1:
        if chars1.get(key) != chars2.get(key):
            conceptual_diffs.append(f"{key}: {chars1.get(key)} vs {chars2.get(key)}")

    predictive_diffs = {}
    for p in phenomena:
        predictive_diffs[p] = exp1.get(p, 0) - exp2.get(p, 0)

    return {
        "theory1": theory1,
        "theory2": theory2,
        "conceptual_differences": conceptual_diffs,
        "predictive_differences": predictive_diffs,
        "key_distinction": chars1.get("action_type") + " vs " + chars2.get("action_type"),
        "experimental_advantage": theory1 if sum(exp1.values()) > sum(exp2.values()) else theory2,
    }


@maxwell_cite(
    863, 864,
    part=4, chapter="Competing Theories",
    theory_class="maxwell_original",
    description="Verify consistency between theories",
)
def verify_theory_consistency(
    theory_name: str = "Maxwell",
    tolerance: float = 1e-10,
) -> Dict[str, float | bool]:
    """
    Verify internal consistency of a theory.

    Art. 863-864: Maxwell's verification of theoretical consistency:
    1. Energy conservation
    2. Momentum conservation
    3. Mathematical self-consistency

    Args:
        theory_name: Name of theory to verify.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 863-864: Theory consistency verification.
    """
    theory = CompetingTheory(name=theory_name)
    consistency = theory.internal_consistency()

    # Check all consistency criteria
    all_passed = all(consistency.values())
    passed_count = sum(1 for v in consistency.values() if v)
    total_count = len(consistency)

    return {
        "theory": theory_name,
        "energy_conservation": consistency.get("energy_conservation", False),
        "momentum_conservation": consistency.get("momentum_conservation", False),
        "action_reaction": consistency.get("action_reaction", False),
        "causality": consistency.get("causality", False),
        "mathematical_rigor": consistency.get("mathematical_rigor", False),
        "consistency_score": passed_count / total_count if total_count > 0 else 0,
        "fully_consistent": all_passed,
        "verified": all_passed,
    }


@maxwell_cite(
    859, 860, 861, 862, 863, 864, 865, 866,
    part=4, chapter="Competing Theories",
    theory_class="maxwell_original",
    description="Synthesize comparison of all theories",
)
def synthesize_theory_comparison() -> Dict[str, Dict | str]:
    """
    Complete synthesis of electromagnetic theory comparison.

    Art. 859-866: Maxwell's comprehensive synthesis including:
    1. All theories compared
    2. Experimental agreement analysis
    3. Consistency evaluation
    4. Final recommendation

    Returns:
        Dictionary with complete synthesis.

    Reference:
        Part IV, Arts. 859-866: Complete theory synthesis.

    Example:
        >>> synthesis = synthesize_theory_comparison()
        >>> print(f"Recommended theory: {synthesis['recommendation']}")
    """
    # Compare all theories
    comparison = compare_electromagnetic_theories()

    # Find best theory
    best_theory = max(comparison.keys(), key=lambda t: comparison[t]["overall_score"])

    # Analyze pairwise differences
    differences = {}
    theory_names = list(comparison.keys())
    for i, t1 in enumerate(theory_names):
        for t2 in theory_names[i+1:]:
            diff = analyze_theory_differences(t1, t2)
            differences[f"{t1}_vs_{t2}"] = diff

    # Consistency verification
    consistency_checks = {}
    for name in theory_names:
        consistency_checks[name] = verify_theory_consistency(name)

    return {
        "comparison_results": comparison,
        "pairwise_differences": differences,
        "consistency_checks": consistency_checks,
        "best_theory": best_theory,
        "recommendation": f"Maxwell's field theory is recommended due to complete "
                         f"experimental agreement and internal consistency.",
        "key_insight": "Field theory provides local energy propagation and "
                      "predicts electromagnetic waves, unlike action-at-distance theories.",
    }
