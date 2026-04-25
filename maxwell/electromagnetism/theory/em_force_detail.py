"""maxwell.electromagnetism.theory.em_force_detail — Ampere's detailed force investigations (Arts. 481-509).

Implements Maxwell's detailed analysis of Ampere's electromagnetic force experiments
and theoretical derivations from Part IV:

- Ampere's force experiment (Arts. 488-489)
- Interaction of current elements (Arts. 493-495)
- Integrated force between circuits (Arts. 498-500)
- Ampere's four equilibrium cases (Arts. 501-509)

Maxwell's CGS formulation (Arts. 488-509):
    Ampere's force law between current elements:

    dF = (I1*I2/r^2) * [2*(dl1·r)(dl2·r)/r^2 - (dl1·dl2)] * r_hat

    Alternative Grassmann form (equivalent for closed circuits):
    dF = (I1*I2/r^2) * dl2 × (dl1 × r_hat)

where:
    I1, I2 = currents (abamperes)
    dl1, dl2 = current element vectors (cm)
    r = separation vector (cm)
    dF = force (dynes)

Category: A (maxwell_original) — Maxwell's analysis of Ampere's force law.

References:
    Part IV, Arts. 481-509: Ampere's investigation of electromagnetic force.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from typing import Optional, Tuple, List

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class CurrentElement:
    """
    A current element for force calculations.

    Art. 493-495: A current element is an infinitesimal segment of a
    current-carrying wire, characterized by:
    - Position in space
    - Direction and length (dl vector)
    - Current magnitude

    The force between elements is the basis for calculating forces
    between complete circuits.

    Attributes:
        current: Current magnitude (abamperes).
        position: Position vector (cm).
        direction: Unit vector in current direction.
        length: Element length (cm).
    """

    current: float
    position: np.ndarray
    direction: np.ndarray
    length: float = 1e-6  # Small but finite for numerical work

    def __post_init__(self):
        """Validate and normalize."""
        self.position = np.asarray(self.position, dtype=np.float64)
        self.direction = np.asarray(self.direction, dtype=np.float64)

        dir_norm = np.linalg.norm(self.direction)
        if dir_norm > 0:
            self.direction = self.direction / dir_norm
        else:
            raise ValueError("Direction vector cannot be zero")

        if self.length <= 0:
            raise ValueError("Element length must be positive")

    @property
    def element_vector(self) -> np.ndarray:
        """
        Current element vector I*dl.

        Returns:
            I * dl vector (abampere*cm).
        """
        return self.current * self.length * self.direction

    @property
    def Idl(self) -> np.ndarray:
        """Alias for element_vector."""
        return self.element_vector


@maxwell_cite(
    488, 489,
    part=4, chapter="Ampere's Force Experiment",
    theory_class="maxwell_original",
    description="Calculate force in Ampere's force experiment",
)
def ampere_force_experiment(
    wire_length: float,
    separation: float,
    current1: float,
    current2: float,
    wire_radius: float = 0.1,
) -> dict[str, float]:
    """
    Calculate the force in Ampere's classic force experiment.

    Art. 488-489: Ampere's experiment measured the force between two
    parallel current-carrying wires. The force per unit length is:

        dF/dL = 2 * I1 * I2 / (c^2 * d)

    where d is the separation and c is the speed of light.

    For finite-length wires of length L:

        F = 2 * I1 * I2 * L / (c^2 * d) * correction_factor

    The correction factor accounts for end effects when the wire
    length is not much greater than the separation.

    Args:
        wire_length: Length of parallel wires (cm).
        separation: Center-to-center separation (cm).
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        wire_radius: Radius of wires (cm, for finite-size correction).

    Returns:
        Dictionary with:
        - force: Total force (dynes)
        - force_per_unit_length: Force density (dynes/cm)
        - infinite_wire_force: Force for infinitely long wires
        - end_effect_correction: Correction factor for finite length

    Reference:
        Part IV, Arts. 488-489: Ampere's force experiment.

    Example:
        >>> result = ampere_force_experiment(
        ...     wire_length=100.0,
        ...     separation=1.0,
        ...     current1=1.0,
        ...     current2=1.0
        ... )
        >>> print(f"Force = {result['force']:.6e} dynes")
    """
    if separation <= 0 or wire_length <= 0:
        return {
            "force": 0.0,
            "force_per_unit_length": 0.0,
            "infinite_wire_force": 0.0,
            "end_effect_correction": 0.0,
        }

    # Force per unit length for infinite wires
    f_per_length = 2.0 * current1 * current2 / (CONST.C ** 2 * separation)

    # Infinite wire force
    F_infinite = f_per_length * wire_length

    # End effect correction for finite wires
    # The exact formula involves elliptic integrals, but for L >> d:
    # correction ≈ 1 - d/L * ln(4L/d)
    L = wire_length
    d = separation
    if L > d:
        correction = 1.0 - (d / L) * np.log(4 * L / d)
    else:
        correction = 0.5  # Rough estimate for short wires

    # Total force with end correction
    F_total = F_infinite * correction

    return {
        "force": F_total,
        "force_per_unit_length": f_per_length,
        "infinite_wire_force": F_infinite,
        "end_effect_correction": correction,
        "wire_length": wire_length,
        "separation": separation,
        "current1": current1,
        "current2": current2,
    }


@maxwell_cite(
    493, 494, 495,
    part=4, chapter="Current Element Interaction",
    theory_class="maxwell_original",
    description="Calculate Ampere force between current elements",
)
def ampere_current_element(
    element1: CurrentElement,
    element2: CurrentElement,
) -> np.ndarray:
    """
    Calculate force between current elements using Ampere's formula.

    Art. 493-495: Ampere's force law between two current elements:

        dF = (I1*I2/r^2) * [2*(dl1·r)(dl2·r)/r^2 - (dl1·dl2)] * r_hat

    where r is the vector from element 1 to element 2.

    This is the fundamental law from which all electromagnetic
    forces between circuits can be derived.

    The force is along the line joining the elements (central force),
    satisfying Newton's third law (action = reaction).

    Args:
        element1: First current element.
        element2: Second current element.

    Returns:
        Force on element 2 due to element 1 (dynes).

    Reference:
        Part IV, Arts. 493-495: Current element interaction.

    Example:
        >>> elem1 = CurrentElement(1.0, np.array([0, 0, 0]), np.array([1, 0, 0]))
        >>> elem2 = CurrentElement(1.0, np.array([0, 1, 0]), np.array([1, 0, 0]))
        >>> F = ampere_current_element(elem1, elem2)
    """
    r_vec = element2.position - element1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r_vec / r_mag

    # Use geometric element vectors (without current)
    dl1 = element1.length * element1.direction
    dl2 = element2.length * element2.direction

    # Dot products
    dl1_dot_dl2 = np.dot(dl1, dl2)
    dl1_dot_r = np.dot(dl1, r_hat)
    dl2_dot_r = np.dot(dl2, r_hat)

    # Ampere's formula
    factor = (element1.current * element2.current / (r_mag ** 2))
    bracket = 2.0 * (dl1_dot_r * dl2_dot_r / (r_mag ** 2)) - dl1_dot_dl2

    return factor * bracket * r_hat


@maxwell_cite(
    493, 494, 495,
    part=4, chapter="Current Element Interaction",
    theory_class="maxwell_original",
    description="Calculate Grassmann form of force between elements",
)
def grassmann_current_element(
    element1: CurrentElement,
    element2: CurrentElement,
) -> np.ndarray:
    """
    Calculate force using Grassmann's formulation.

    Art. 493-495: The Grassmann form (equivalent for closed circuits):

        dF = (I1*I2/r^2) * dl2 × (dl1 × r_hat)

    This form does not satisfy action-reaction for individual elements,
    but gives the same total force for closed circuits.

    The Grassmann form is related to the Lorentz force law:
    dF = I2 * dl2 × B1

    where B1 is the magnetic field produced by element 1.

    Args:
        element1: First current element.
        element2: Second current element.

    Returns:
        Force on element 2 (dynes).

    Reference:
        Part IV, Arts. 493-495: Grassmann formulation.
    """
    r_vec = element2.position - element1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r_vec / r_mag

    # Use geometric element vectors (without current)
    dl1 = element1.length * element1.direction
    dl2 = element2.length * element2.direction

    # Grassmann formula: dF = (I1*I2/r^2) * dl2 × (dl1 × r_hat)
    cross1 = np.cross(dl1, r_hat)
    cross2 = np.cross(dl2, cross1)

    return (element1.current * element2.current / (r_mag ** 2)) * cross2


@maxwell_cite(
    498, 499, 500,
    part=4, chapter="Integrated Force Between Circuits",
    theory_class="maxwell_original",
    description="Integrate Ampere force over closed circuits",
)
def ampere_force_integration(
    circuit1: List[CurrentElement],
    circuit2: List[CurrentElement],
    method: str = "ampere",
) -> dict[str, np.ndarray | float]:
    """
    Calculate total force between closed circuits by integration.

    Art. 498-500: The total force between two closed current-carrying
    circuits is obtained by integrating the elemental force law over
    both circuits:

        F = ∮∮ dF(element1, element2)

    For closed circuits, Ampere's and Grassmann's formulations
    give identical results (though they differ for individual elements).

    The double line integral can be evaluated numerically by
    discretizing each circuit into segments.

    Args:
        circuit1: List of current elements forming first circuit.
        circuit2: List of current elements forming second circuit.
        method: 'ampere' or 'grassmann' force law.

    Returns:
        Dictionary with:
        - total_force: Net force vector (dynes)
        - force_magnitude: |F| (dynes)
        - method: Force law used

    Reference:
        Part IV, Arts. 498-500: Integrated force between circuits.

    Example:
        >>> # Create two circular loops
        >>> loop1 = create_circular_loop(1.0, 1.0, 32)  # R=1cm, I=1abA, 32 segments
        >>> loop2 = create_circular_loop(1.0, 1.0, 32, center=np.array([0, 0, 2]))
        >>> result = ampere_force_integration(loop1, loop2)
        >>> print(f"Force = {result['total_force']} dynes")
    """
    total_force = np.zeros(3)

    for e1 in circuit1:
        for e2 in circuit2:
            if method == "ampere":
                dF = ampere_current_element(e1, e2)
            elif method == "grassmann":
                dF = grassmann_current_element(e1, e2)
            else:
                raise ValueError(f"Unknown method: {method}")
            total_force += dF

    return {
        "total_force": total_force,
        "force_magnitude": np.linalg.norm(total_force),
        "method": method,
        "circuit1_elements": len(circuit1),
        "circuit2_elements": len(circuit2),
    }


@maxwell_cite(
    501, 502, 503, 504, 505, 506, 507, 508, 509,
    part=4, chapter="Ampere's Four Equilibrium Cases",
    theory_class="maxwell_original",
    description="Calculate force for Ampere's four equilibrium cases",
)
def ampere_four_cases(
    case_number: int,
    current: float = 1.0,
    separation: float = 1.0,
    length: float = 1.0,
) -> dict[str, float | np.ndarray | str]:
    """
    Calculate forces for Ampere's four equilibrium cases.

    Art. 501-509: Ampere established four fundamental equilibrium cases
    that any force law between current elements must satisfy:

    Case 1 (Art. 502-503): Two elements in line, current flowing in same
    direction repel; opposite direction attract.

    Case 2 (Art. 504): Two parallel elements side by side, currents in
    same direction attract; opposite directions repel.

    Case 3 (Art. 505): Two perpendicular elements in the same plane
    have zero force between them.

    Case 4 (Art. 506-509): An element and a closed circuit have forces
    that sum to zero when integrated over the circuit.

    Args:
        case_number: 1, 2, 3, or 4 for the equilibrium case.
        current: Current in elements (abamperes).
        separation: Separation distance (cm).
        length: Element length (cm).

    Returns:
        Dictionary with force results for the specified case.

    Reference:
        Part IV, Arts. 501-509: Ampere's four equilibrium cases.
    """
    if case_number == 1:
        # Two elements end-to-end along the line joining them
        # dl1 || dl2 || r_hat
        elem1 = CurrentElement(
            current=current,
            position=np.zeros(3),
            direction=np.array([0, 0, 1]),
            length=length
        )
        elem2 = CurrentElement(
            current=current,
            position=np.array([0, 0, separation]),
            direction=np.array([0, 0, 1]),
            length=length
        )

        F_ampere = ampere_current_element(elem1, elem2)

        # For this configuration:
        # Ampere: F = (I1*I2*dl1*dl2/r^2) * [2*(1)(1) - 1] = I1*I2*dl1*dl2/r^2
        # Positive = repulsive (along +z)

        return {
            "case": 1,
            "description": "Elements end-to-end, parallel currents",
            "configuration": "dl1 || dl2 || r_hat",
            "force_ampere": F_ampere,
            "force_magnitude": np.linalg.norm(F_ampere),
            "expected": "repulsive",
            "analytical": (current ** 2 * length ** 2) / (separation ** 2),
        }

    elif case_number == 2:
        # Two parallel elements side by side
        # dl1 || dl2, both perpendicular to r_hat
        elem1 = CurrentElement(
            current=current,
            position=np.zeros(3),
            direction=np.array([1, 0, 0]),
            length=length
        )
        elem2 = CurrentElement(
            current=current,
            position=np.array([0, separation, 0]),
            direction=np.array([1, 0, 0]),
            length=length
        )

        F_ampere = ampere_current_element(elem1, elem2)
        F_grassmann = grassmann_current_element(elem1, elem2)

        # For this configuration:
        # Ampere: dl1·r_hat = 0, dl2·r_hat = 0, so bracket = -dl1·dl2 = -dl^2
        # F = -(I1*I2*dl^2/r^2) * r_hat (attractive)

        return {
            "case": 2,
            "description": "Elements side-by-side, parallel currents",
            "configuration": "dl1 || dl2, both perpendicular to r_hat",
            "force_ampere": F_ampere,
            "force_grassmann": F_grassmann,
            "force_magnitude": np.linalg.norm(F_ampere),
            "expected": "attractive",
            "analytical": -(current ** 2 * length ** 2) / (separation ** 2),
        }

    elif case_number == 3:
        # Two perpendicular elements in same plane
        # dl1 perpendicular to dl2, one parallel to r_hat
        elem1 = CurrentElement(
            current=current,
            position=np.zeros(3),
            direction=np.array([1, 0, 0]),
            length=length
        )
        elem2 = CurrentElement(
            current=current,
            position=np.array([0, separation, 0]),
            direction=np.array([0, 0, 1]),
            length=length
        )

        F_ampere = ampere_current_element(elem1, elem2)
        F_grassmann = grassmann_current_element(elem1, elem2)

        # For this configuration:
        # dl1·r_hat = 0, dl2·dl1 = 0, dl2·r_hat = 0
        # Ampere: bracket = 0, so F = 0

        return {
            "case": 3,
            "description": "Elements perpendicular in same plane",
            "configuration": "dl1 perpendicular to dl2, dl1 perpendicular to r_hat",
            "force_ampere": F_ampere,
            "force_grassmann": F_grassmann,
            "force_magnitude": np.linalg.norm(F_ampere),
            "expected": "zero force",
            "analytical": 0.0,
        }

    elif case_number == 4:
        # Element and circular loop - integrated force
        # Create a circular loop and compute force on a central element
        n_segments = 32
        angles = np.linspace(0, 2 * np.pi, n_segments, endpoint=False)
        dtheta = 2 * np.pi / n_segments
        loop_radius = separation

        circuit = []
        for theta in angles:
            pos = np.array([loop_radius * np.cos(theta),
                           loop_radius * np.sin(theta), 0])
            direction = np.array([-np.sin(theta), np.cos(theta), 0])
            elem = CurrentElement(
                current=current,
                position=pos,
                direction=direction,
                length=loop_radius * dtheta
            )
            circuit.append(elem)

        # Central element at origin, pointing in z direction
        central_elem = CurrentElement(
            current=current,
            position=np.array([0, 0, 0]),
            direction=np.array([0, 0, 1]),
            length=length
        )

        # Compute total force
        total_force = np.zeros(3)
        for elem in circuit:
            dF = ampere_current_element(central_elem, elem)
            total_force += dF

        # By symmetry, the net force should be zero (or very small)
        return {
            "case": 4,
            "description": "Element at center of circular loop",
            "configuration": "Central element perpendicular to loop plane",
            "force_ampere": total_force,
            "force_magnitude": np.linalg.norm(total_force),
            "expected": "zero by symmetry",
            "loop_radius": loop_radius,
            "n_segments": n_segments,
        }

    else:
        raise ValueError(f"Case number must be 1, 2, 3, or 4, got {case_number}")


@maxwell_cite(
    501, 502, 503, 504, 505, 506, 507, 508, 509,
    part=4, chapter="Ampere's Four Equilibrium Cases",
    theory_class="maxwell_original",
    description="Verify all four equilibrium cases",
)
def verify_ampere_equilibrium(
    current: float = 1.0,
    separation: float = 1.0,
    length: float = 1.0,
    tolerance: float = 1e-6,
) -> dict[str, bool | dict]:
    """
    Verify all four of Ampere's equilibrium cases.

    Art. 501-509: This function verifies that Ampere's force law
    satisfies all four equilibrium conditions:

    1. End-to-end elements: Repulsive for parallel currents
    2. Side-by-side elements: Attractive for parallel currents
    3. Perpendicular elements: Zero force
    4. Element and closed circuit: Net force zero by symmetry

    Args:
        current: Test current (abamperes).
        separation: Test separation (cm).
        length: Element length (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results for each case.

    Reference:
        Part IV, Arts. 501-509: Equilibrium verification.
    """
    results = {}
    all_passed = True

    # Case 1: End-to-end (should be repulsive, Fz > 0)
    case1 = ampere_four_cases(1, current, separation, length)
    case1_pass = case1["force_magnitude"] > 0 and case1["force_ampere"][2] > 0
    results["case_1"] = case1_pass
    all_passed = all_passed and case1_pass

    # Case 2: Side-by-side (should be attractive, Fy < 0)
    case2 = ampere_four_cases(2, current, separation, length)
    case2_pass = case2["force_magnitude"] > 0 and case2["force_ampere"][1] < 0
    results["case_2"] = case2_pass
    all_passed = all_passed and case2_pass

    # Case 3: Perpendicular (should be zero)
    case3 = ampere_four_cases(3, current, separation, length)
    case3_pass = case3["force_magnitude"] < tolerance
    results["case_3"] = case3_pass
    all_passed = all_passed and case3_pass

    # Case 4: Element and loop (should be zero by symmetry)
    case4 = ampere_four_cases(4, current, separation, length)
    case4_pass = case4["force_magnitude"] < tolerance
    results["case_4"] = case4_pass
    all_passed = all_passed and case4_pass

    return {
        "case_1_verified": results["case_1"],
        "case_2_verified": results["case_2"],
        "case_3_verified": results["case_3"],
        "case_4_verified": results["case_4"],
        "all_verified": all_passed,
        "details": results,
    }


@maxwell_cite(
    481, 488, 489, 493, 494, 495, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509,
    part=4, chapter="Ampere's Force Investigations",
    theory_class="maxwell_original",
    description="Complete analysis of Ampere's force law",
)
def analyze_ampere_force_law(
    current: float = 1.0,
    separation: float = 1.0,
    wire_length: float = 100.0,
    element_length: float = 1e-3,
) -> dict[str, float | np.ndarray | dict]:
    """
    Complete analysis of Ampere's electromagnetic force law.

    Art. 481-509: Comprehensive analysis including:
    1. Force experiment with parallel wires
    2. Elemental force calculations (Ampere and Grassmann forms)
    3. Integrated force between circuits
    4. Verification of four equilibrium cases

    Args:
        current: Current in wires (abamperes).
        separation: Separation distance (cm).
        wire_length: Length of parallel wires (cm).
        element_length: Length of current elements (cm).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 481-509: Complete Ampere force analysis.
    """
    results = {}

    # 1. Parallel wire experiment
    wire_result = ampere_force_experiment(
        wire_length=wire_length,
        separation=separation,
        current1=current,
        current2=current
    )
    results["parallel_wire_experiment"] = wire_result

    # 2. Elemental forces
    elem1 = CurrentElement(
        current=current,
        position=np.zeros(3),
        direction=np.array([1, 0, 0]),
        length=element_length
    )
    elem2 = CurrentElement(
        current=current,
        position=np.array([0, separation, 0]),
        direction=np.array([1, 0, 0]),
        length=element_length
    )

    F_ampere = ampere_current_element(elem1, elem2)
    F_grassmann = grassmann_current_element(elem1, elem2)

    results["elemental_forces"] = {
        "ampere_force": F_ampere,
        "grassmann_force": F_grassmann,
        "difference": F_ampere - F_grassmann,
        "ampere_magnitude": np.linalg.norm(F_ampere),
        "grassmann_magnitude": np.linalg.norm(F_grassmann),
    }

    # 3. Two circular loops
    n_segments = 16
    angles = np.linspace(0, 2 * np.pi, n_segments, endpoint=False)
    dtheta = 2 * np.pi / n_segments

    loop1 = []
    loop2 = []
    for theta in angles:
        # Loop 1 at z=0
        pos1 = np.array([separation * np.cos(theta),
                        separation * np.sin(theta), 0])
        dir1 = np.array([-np.sin(theta), np.cos(theta), 0])
        loop1.append(CurrentElement(current, pos1, dir1, separation * dtheta))

        # Loop 2 at z=separation
        pos2 = np.array([separation * np.cos(theta),
                        separation * np.sin(theta), separation])
        dir2 = np.array([-np.sin(theta), np.cos(theta), 0])
        loop2.append(CurrentElement(current, pos2, dir2, separation * dtheta))

    force_result = ampere_force_integration(loop1, loop2)
    results["loop_integration"] = force_result

    # 4. Equilibrium cases verification
    equilibrium = verify_ampere_equilibrium(current, separation, element_length)
    results["equilibrium_cases"] = equilibrium

    return results


__all__ = [
    "CurrentElement",
    "ampere_force_experiment",
    "ampere_current_element",
    "grassmann_current_element",
    "ampere_force_integration",
    "ampere_four_cases",
    "verify_ampere_equilibrium",
    "analyze_ampere_force_law",
]
