"""maxwell.electromagnetism.theory.comparisons — Force law comparisons (Arts. 526-527).

Implements Maxwell's comparative analysis of different electromagnetic force
formulations, including Ampere's, Grassmann's, and Weber's force laws.

Maxwell's CGS formulation (Arts. 526-527):
    Maxwell compared several force laws for current elements:

    1. Ampere's law (1823):
       d²F = (I1*I2/r²) * [2(dl1·r)(dl2·r)/r² - (dl1·dl2)] * r_hat

    2. Grassmann's law (1845):
       dF = (I1*I2/r²) * dl2 × (dl1 × r_hat)

    3. Weber's law (1846):
       Based on velocity-dependent forces between charges

    Maxwell showed these are equivalent for closed circuits but differ
    for open circuits and individual elements.

Category: A (maxwell_original) — Maxwell's comparative analysis.

References:
    Part IV, Arts. 526-527: Comparison of force laws.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ForceLawComparison:
    """
    Comparative analysis of electromagnetic force laws.

    Art. 526-527: Maxwell analyzed the different formulations of
    electromagnetic force laws and their properties:

    - Ampere's law: Satisfies action-reaction for elements
    - Grassmann's law: Derived from field concept, equivalent for closed circuits
    - Weber's law: Based on direct charge interactions

    This class provides calculations using each formulation.

    Attributes:
        law_type: Type of force law ('ampere', 'grassmann', 'weber').
    """

    law_type: str = "ampere"

    def __post_init__(self):
        """Validate law type."""
        valid_types = {"ampere", "grassmann", "weber"}
        if self.law_type not in valid_types:
            raise ValueError(f"law_type must be one of {valid_types}")

    @maxwell_cite(
        526,
        527,
        part=4,
        chapter="Force Law Comparisons",
        theory_class="maxwell_original",
        description="Calculate force using selected law",
    )
    def calculate_force(
        self,
        current1: float,
        dl1: np.ndarray,
        current2: float,
        dl2: np.ndarray,
        r_vector: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate force using the selected force law.

        Art. 526-527: Different force laws give different results for
        individual elements but agree for closed circuits.

        Args:
            current1: Current in first element (abamperes).
            dl1: First element vector (cm).
            current2: Current in second element (abamperes).
            dl2: Second element vector (cm).
            r_vector: Vector from element 1 to 2 (cm).

        Returns:
            Force on element 2 (dynes).
        """
        if self.law_type == "ampere":
            return _ampere_force(current1, dl1, current2, dl2, r_vector)
        elif self.law_type == "grassmann":
            return _grassmann_force(current1, dl1, current2, dl2, r_vector)
        else:  # weber
            return _weber_force(current1, dl1, current2, dl2, r_vector)


def _ampere_force(
    I1: float,
    dl1: np.ndarray,
    I2: float,
    dl2: np.ndarray,
    r_vec: np.ndarray,
) -> np.ndarray:
    """Ampere's original force law."""
    r_mag = np.linalg.norm(r_vec)
    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r_vec / r_mag
    dl1_dot_dl2 = np.dot(dl1, dl2)
    dl1_dot_r = np.dot(dl1, r_hat)
    dl2_dot_r = np.dot(dl2, r_hat)

    factor = (I1 * I2) / (r_mag**2)
    bracket = 2.0 * (dl1_dot_r * dl2_dot_r) / (r_mag**2) - dl1_dot_dl2

    return factor * bracket * r_hat


def _grassmann_force(
    I1: float,
    dl1: np.ndarray,
    I2: float,
    dl2: np.ndarray,
    r_vec: np.ndarray,
) -> np.ndarray:
    """Grassmann's force law (field-based)."""
    r_mag = np.linalg.norm(r_vec)
    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r_vec / r_mag
    cross1 = np.cross(dl1, r_hat)
    cross2 = np.cross(dl2, cross1)

    return (I1 * I2 / (r_mag**2)) * cross2


def _weber_force(
    I1: float,
    dl1: np.ndarray,
    I2: float,
    dl2: np.ndarray,
    r_vec: np.ndarray,
) -> np.ndarray:
    """
    Weber's force law (velocity-dependent).

    Weber's law is based on direct charge interactions with
    velocity and acceleration dependence. For steady currents,
    it reduces to a form similar to Ampere's but with differences
    in the coefficients.
    """
    # Simplified Weber form for steady currents
    # This gives same result as Ampere for closed circuits
    return _ampere_force(I1, dl1, I2, dl2, r_vec)


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Compare force laws for specific geometry",
)
def compare_force_laws(
    current1: float = 1.0,
    current2: float = 1.0,
    dl1: np.ndarray = None,
    dl2: np.ndarray = None,
    r_vector: np.ndarray = None,
) -> dict[str, np.ndarray | float]:
    """
    Compare different force laws for a specific geometry.

    Art. 526-527: This function calculates the force using Ampere's,
    Grassmann's, and Weber's laws and compares the results.

    Args:
        current1: Current in first element (abamperes).
        current2: Current in second element (abamperes).
        dl1: First element vector (cm, default: [1,0,0]).
        dl2: Second element vector (cm, default: [1,0,0]).
        r_vector: Separation vector (cm, default: [0,1,0]).

    Returns:
        Dictionary with forces from each law and comparison metrics.

    Reference:
        Part IV, Arts. 526-527: Force law comparison.
    """
    dl1 = (
        np.asarray(dl1, dtype=np.float64)
        if dl1 is not None
        else np.array([1.0, 0.0, 0.0])
    )
    dl2 = (
        np.asarray(dl2, dtype=np.float64)
        if dl2 is not None
        else np.array([1.0, 0.0, 0.0])
    )
    r_vector = (
        np.asarray(r_vector, dtype=np.float64)
        if r_vector is not None
        else np.array([0.0, 1.0, 0.0])
    )

    F_ampere = _ampere_force(current1, dl1, current2, dl2, r_vector)
    F_grassmann = _grassmann_force(current1, dl1, current2, dl2, r_vector)
    F_weber = _weber_force(current1, dl1, current2, dl2, r_vector)

    # Differences
    diff_AG = np.linalg.norm(F_ampere - F_grassmann)
    diff_AW = np.linalg.norm(F_ampere - F_weber)
    diff_GW = np.linalg.norm(F_grassmann - F_weber)

    # Magnitudes
    mag_ampere = np.linalg.norm(F_ampere)
    mag_grassmann = np.linalg.norm(F_grassmann)

    return {
        "force_ampere": F_ampere,
        "force_grassmann": F_grassmann,
        "force_weber": F_weber,
        "magnitude_ampere": mag_ampere,
        "magnitude_grassmann": mag_grassmann,
        "difference_ampere_grassmann": diff_AG,
        "difference_ampere_weber": diff_AW,
        "difference_grassmann_weber": diff_GW,
        "relative_difference": diff_AG / mag_ampere if mag_ampere > 1e-15 else 0.0,
    }


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Verify action-reaction for force laws",
)
def verify_action_reaction(
    current1: float = 1.0,
    current2: float = 1.0,
    dl1: np.ndarray = None,
    dl2: np.ndarray = None,
    separation: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, bool | np.ndarray]:
    """
    Verify Newton's third law (action-reaction) for force laws.

    Art. 526-527: Ampere's law satisfies action-reaction for individual
    elements (F_12 = -F_21), while Grassmann's law does not (but gives
    correct results for closed circuits).

    Args:
        current1: Current in first element (abamperes).
        current2: Current in second element (abamperes).
        dl1: First element vector (cm).
        dl2: Second element vector (cm).
        separation: Distance between elements (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results for each force law.
    """
    dl1 = (
        np.asarray(dl1, dtype=np.float64)
        if dl1 is not None
        else np.array([1.0, 0.0, 0.0])
    )
    dl2 = (
        np.asarray(dl2, dtype=np.float64)
        if dl2 is not None
        else np.array([0.0, 1.0, 0.0])
    )

    r_vec = np.array([0.0, separation, 0.0])
    r_rev = -r_vec

    # Ampere's law
    F_12_ampere = _ampere_force(current1, dl1, current2, dl2, r_vec)
    F_21_ampere = _ampere_force(current2, dl2, current1, dl1, r_rev)
    ampere_satisfies = np.allclose(F_12_ampere, -F_21_ampere, atol=tolerance)

    # Grassmann's law
    F_12_grassmann = _grassmann_force(current1, dl1, current2, dl2, r_vec)
    F_21_grassmann = _grassmann_force(current2, dl2, current1, dl1, r_rev)
    grassmann_satisfies = np.allclose(F_12_grassmann, -F_21_grassmann, atol=tolerance)

    return {
        "force_12_ampere": F_12_ampere,
        "force_21_ampere": F_21_ampere,
        "ampere_action_reaction": ampere_satisfies,
        "force_12_grassmann": F_12_grassmann,
        "force_21_grassmann": F_21_grassmann,
        "grassmann_action_reaction": grassmann_satisfies,
        "summary": "Ampere satisfies action-reaction; Grassmann does not (but agrees for closed circuits)",
    }


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Compare force laws for parallel elements",
)
def compare_parallel_elements(
    current1: float = 1.0,
    current2: float = 1.0,
    element_length: float = 1e-6,
    separation: float = 1.0,
) -> dict[str, float | np.ndarray]:
    """
    Compare force laws for parallel current elements.

    Art. 526-527: For parallel elements perpendicular to their separation,
    the different force laws give:
    - Ampere: Attractive force proportional to I1*I2*dl1*dl2/r²
    - Grassmann: Same magnitude and direction
    - Weber: Similar to Ampere

    Args:
        current1: Current in first element (abamperes).
        current2: Current in second element (abamperes).
        element_length: Length of elements (cm).
        separation: Distance between elements (cm).

    Returns:
        Dictionary with comparison results.
    """
    dl1 = np.array([element_length, 0.0, 0.0])
    dl2 = np.array([element_length, 0.0, 0.0])
    r_vec = np.array([0.0, separation, 0.0])

    F_ampere = _ampere_force(current1, dl1, current2, dl2, r_vec)
    F_grassmann = _grassmann_force(current1, dl1, current2, dl2, r_vec)
    F_weber = _weber_force(current1, dl1, current2, dl2, r_vec)

    return {
        "geometry": "parallel_elements_perpendicular_to_separation",
        "force_ampere": F_ampere,
        "force_grassmann": F_grassmann,
        "force_weber": F_weber,
        "all_attractive": F_ampere[1] < 0 and F_grassmann[1] < 0 and F_weber[1] < 0,
        "magnitude_ratio_AG": (
            np.linalg.norm(F_ampere) / np.linalg.norm(F_grassmann)
            if np.linalg.norm(F_grassmann) > 0
            else float("inf")
        ),
    }


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Complete force law comparison analysis",
)
def analyze_force_laws(
    current1: float = 1.0,
    current2: float = 1.0,
    test_geometries: list[dict] = None,
) -> dict[str, list | dict]:
    """
    Complete comparative analysis of force laws.

    Art. 526-527: Comprehensive analysis across multiple geometries:
    1. Parallel elements
    2. Perpendicular elements
    3. Collinear elements
    4. Various orientations

    Args:
        current1: Current in first element (abamperes).
        current2: Current in second element (abamperes).
        test_geometries: List of geometry dictionaries with dl1, dl2, r_vector.

    Returns:
        Dictionary with complete comparison results.
    """
    if test_geometries is None:
        test_geometries = [
            {
                "name": "parallel_perp_to_r",
                "dl1": [1, 0, 0],
                "dl2": [1, 0, 0],
                "r": [0, 1, 0],
            },
            {
                "name": "parallel_along_r",
                "dl1": [0, 1, 0],
                "dl2": [0, 1, 0],
                "r": [0, 1, 0],
            },
            {
                "name": "perpendicular_elements",
                "dl1": [1, 0, 0],
                "dl2": [0, 0, 1],
                "r": [0, 1, 0],
            },
            {
                "name": "perpendicular_r",
                "dl1": [1, 0, 0],
                "dl2": [0, 0, 1],
                "r": [0, 1, 0],
            },
        ]

    results = []
    for geom in test_geometries:
        dl1 = np.array(geom["dl1"], dtype=np.float64) * 1e-6
        dl2 = np.array(geom["dl2"], dtype=np.float64) * 1e-6
        r_vec = np.array(geom["r"], dtype=np.float64)

        comparison = compare_force_laws(current1, current2, dl1, dl2, r_vec)
        comparison["geometry"] = geom["name"]
        results.append(comparison)

    return {
        "current1": current1,
        "current2": current2,
        "geometries_tested": len(results),
        "results_by_geometry": results,
        "summary": "Force laws agree for closed circuits, differ for open circuits",
    }


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Ampere force law for parallel wires: F/L = 2*I1*I2/r",
)
def ampere_force_law(I1: float, I2: float, r: float) -> float:
    """
    Calculate force per unit length between parallel wires (Ampere's law).

    Art. 526-527: For two parallel wires separated by distance r:

        F/L = 2 * I1 * I2 / r  (dynes/cm in CGS)

    Args:
        I1: Current in wire 1 (abamperes).
        I2: Current in wire 2 (abamperes).
        r: Separation distance (cm).

    Returns:
        Force per unit length (dynes/cm). Positive = attractive.
    """
    return 2.0 * I1 * I2 / r


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Grassmann force law: F = I * dl × B",
)
def grassmann_force_law(
    current: float,
    dl: np.ndarray,
    B: np.ndarray,
) -> np.ndarray:
    """
    Calculate Grassmann force: F = I * dl × B.

    Art. 526-527: The force on a current element in a magnetic field:

        F = I * dl × B

    Args:
        current: Current (abamperes).
        dl: Current element vector (cm).
        B: Magnetic field (gauss).

    Returns:
        Force vector (dynes).
    """
    dl = np.asarray(dl, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    return current * np.cross(dl, B)


@maxwell_cite(
    526,
    527,
    part=4,
    chapter="Force Law Comparisons",
    theory_class="maxwell_original",
    description="Weber force law for moving charges",
)
def weber_force_law(
    q1: float,
    q2: float,
    r: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
) -> np.ndarray:
    """
    Calculate Weber force between moving charges.

    Art. 526-527: Weber's velocity-dependent force law:

        F = (q1*q2/r²) * [r_hat + (v1·v2)/c² * r_hat - ...]

    Simplified form for comparison purposes.

    Args:
        q1: Charge 1 (abcoulombs).
        q2: Charge 2 (abcoulombs).
        r: Separation vector (cm).
        v1: Velocity of charge 1 (cm/s).
        v2: Velocity of charge 2 (cm/s).

    Returns:
        Force vector (dynes).
    """
    r = np.asarray(r, dtype=np.float64)
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)
    r_mag = np.linalg.norm(r)

    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r / r_mag

    # Coulomb term
    F_coulomb = q1 * q2 / (r_mag**2) * r_hat

    # Velocity-dependent correction (simplified Weber form)
    v1_dot_v2 = np.dot(v1, v2)
    v1_dot_r = np.dot(v1, r_hat)
    v2_dot_r = np.dot(v2, r_hat)

    correction = (3.0 * v1_dot_r * v2_dot_r - 2.0 * v1_dot_v2) / (CONST.C**2)

    return F_coulomb * (1.0 + correction)
