"""maxwell.materials.constitutive.conductivity — Conductivity relation (Art. 609).

Implements Maxwell's constitutive relation for electrical conduction,
relating current density J to electric field E.

Maxwell's CGS formulation (Art. 609):
    Conduction current equation (Eq. G):

        J = σE

    where:
    - σ = conductivity (s⁻¹ in CGS-EMU)
    - ρ = 1/σ = resistivity

    In CGS-EMU:
        J in abamperes/cm²
        E in abvolts/cm
        σ in s⁻¹

where:
    J = conduction current density (abamperes/cm²)
    E = electric field intensity (abvolts/cm or statvolts/cm)
    σ = conductivity (s⁻¹ in CGS)
    ρ = resistivity (s in CGS)

Category: A (maxwell_original) — Maxwell's conduction theory.

References:
    Part IV, Art. 609: Conduction current equation (Eq. G).
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class Conductivity:
    """
    Conductivity calculator for conducting materials.

    Art. 609: Maxwell's relation for conduction:

        J = σE

    where σ is the conductivity (or C = 1/ρ where ρ is resistivity).

    Attributes:
        conductivity: Electrical conductivity σ (s⁻¹ in CGS).
        resistivity: Electrical resistivity ρ = 1/σ (s in CGS).
    """

    conductivity: float = 1.0
    resistivity: float = None

    def __post_init__(self):
        """Calculate resistivity from conductivity if not provided."""
        if self.resistivity is None:
            if self.conductivity > 0:
                self.resistivity = 1.0 / self.conductivity
            else:
                self.resistivity = float('inf')

    @maxwell_cite(
        609,
        part=4, chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate conduction current density J from E",
    )
    def current_density(self, E_field: np.ndarray) -> np.ndarray:
        """
        Calculate conduction current density from electric field.

        Art. 609: J = σE (Ohm's law in differential form)

        Args:
            E_field: Electric field intensity (abvolts/cm).

        Returns:
            Current density J (abamperes/cm²).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        return self.conductivity * E_field

    @maxwell_cite(
        609,
        part=4, chapter="Constitutive Relations",
        theory_class="maxwell_original",
        description="Calculate E from J",
    )
    def electric_field(self, J: np.ndarray) -> np.ndarray:
        """
        Calculate electric field from current density.

        Art. 609: E = ρJ = J/σ

        Args:
            J: Current density (abamperes/cm²).

        Returns:
            Electric field E (abvolts/cm).
        """
        J = np.asarray(J, dtype=np.float64)
        return self.resistivity * J


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate conduction current: J = σE",
)
def calc_conduction_current(
    E_field: np.ndarray,
    conductivity: float,
) -> np.ndarray:
    """
    Calculate conduction current density.

    Art. 609: Ohm's law in differential form:

        J = σE

    Args:
        E_field: Electric field (abvolts/cm).
        conductivity: Conductivity σ (s⁻¹ in CGS).

    Returns:
        Current density J (abamperes/cm²).

    Reference:
        Part IV, Art. 609: Conduction current (Eq. G).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    return conductivity * E_field


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate current in wire from E field",
)
def calc_wire_current(
    E_field: float,
    conductivity: float,
    cross_section_area: float,
) -> float:
    """
    Calculate total current in a wire from electric field.

    Art. 609: For a wire with uniform E field:

        I = J * A = σ * E * A

    Args:
        E_field: Electric field magnitude (abvolts/cm).
        conductivity: Conductivity σ (s⁻¹).
        cross_section_area: Wire cross-section (cm²).

    Returns:
        Current I (abamperes).

    Reference:
        Part IV, Art. 609: Wire current.
    """
    J = conductivity * E_field
    return J * cross_section_area


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate resistance of conductor",
)
def calc_resistance(
    resistivity: float,
    length: float,
    cross_section_area: float,
) -> float:
    """
    Calculate resistance of a uniform conductor.

    Art. 609: For a conductor of length L and area A:

        R = ρ * L / A

    Args:
        resistivity: Resistivity ρ (s in CGS).
        length: Conductor length (cm).
        cross_section_area: Cross-section area (cm²).

    Returns:
        Resistance R (abohms in CGS).

    Reference:
        Part IV, Art. 609: Resistance calculation.
    """
    if cross_section_area <= 0:
        raise ValueError("Area must be positive")
    return resistivity * length / cross_section_area


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate conductance from conductivity",
)
def calc_conductance(
    conductivity: float,
    length: float,
    cross_section_area: float,
) -> float:
    """
    Calculate conductance of a uniform conductor.

    Art. 609: For a conductor of length L and area A:

        G = σ * A / L = 1/R

    Args:
        conductivity: Conductivity σ (s⁻¹).
        length: Conductor length (cm).
        cross_section_area: Cross-section area (cm²).

    Returns:
        Conductance G (abmhos in CGS).

    Reference:
        Part IV, Art. 609: Conductance calculation.
    """
    if length <= 0:
        raise ValueError("Length must be positive")
    return conductivity * cross_section_area / length


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate power dissipation in conductor",
)
def calc_power_dissipation_conduction(
    E_field: np.ndarray,
    conductivity: float,
    volume: float,
) -> float:
    """
    Calculate power dissipated as heat in a conductor.

    Art. 609: The power density is:

        p = J · E = σE²

    Total power:
        P = integral(σE²) dV

    For uniform fields:
        P = σE²V

    Args:
        E_field: Electric field (abvolts/cm).
        conductivity: Conductivity σ (s⁻¹).
        volume: Volume of conductor (cm³).

    Returns:
        Power dissipated (ergs/s).

    Reference:
        Part IV, Art. 609: Power dissipation.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    E_squared = np.dot(E_field, E_field)

    return conductivity * E_squared * volume


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Calculate conductivity from resistivity",
)
def calc_conductivity_from_resistivity(resistivity: float) -> float:
    """
    Calculate conductivity from resistivity.

    Art. 609: σ = 1/ρ

    Args:
        resistivity: Resistivity ρ.

    Returns:
        Conductivity σ.

    Reference:
        Part IV, Art. 609: Conductivity-resistivity relation.
    """
    if resistivity <= 0:
        return float('inf') if resistivity == 0 else 0.0
    return 1.0 / resistivity


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Verify conduction relations",
)
def verify_conduction_relations(
    E_field: np.ndarray = None,
    conductivity: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | np.ndarray | bool]:
    """
    Verify conduction relations.

    Art. 609: This function verifies:
    1. J = σE
    2. E = ρJ
    3. σ = 1/ρ

    Args:
        E_field: Test electric field (abvolts/cm).
        conductivity: Test conductivity.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if E_field is None:
        E_field = np.array([1.0, 0.0, 0.0])

    E_field = np.asarray(E_field, dtype=np.float64)
    resistivity = 1.0 / conductivity if conductivity > 0 else float('inf')

    # Calculate J from E
    J = calc_conduction_current(E_field, conductivity)

    # Calculate E from J
    E_from_J = resistivity * J

    # Verify E = ρJ
    E_error = np.linalg.norm(E_field - E_from_J) / np.linalg.norm(E_field) if np.linalg.norm(E_field) > 0 else 0

    # Verify σ = 1/ρ
    sigma_check = calc_conductivity_from_resistivity(resistivity)
    sigma_error = abs(sigma_check - conductivity) / conductivity if conductivity > 0 else 0

    return {
        "E_field": E_field,
        "conductivity": conductivity,
        "resistivity": resistivity,
        "current_density_J": J,
        "E_from_J": E_from_J,
        "E_error": E_error,
        "conductivity_error": sigma_error,
        "verified": E_error < tolerance and sigma_error < tolerance,
    }


@maxwell_cite(
    609,
    part=4, chapter="Constitutive Relations",
    theory_class="maxwell_original",
    description="Complete conduction analysis",
)
def analyze_conduction(
    E_field: np.ndarray,
    conductivity: float,
    conductor_length: float = 1.0,
    cross_section_area: float = 1.0,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of electrical conduction.

    Art. 609: Comprehensive analysis including:
    1. Current density
    2. Total current
    3. Resistance
    4. Power dissipation

    Args:
        E_field: Electric field (abvolts/cm).
        conductivity: Conductivity σ (s⁻¹).
        conductor_length: Length of conductor (cm).
        cross_section_area: Cross-section area (cm²).

    Returns:
        Dictionary with complete analysis results.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    resistivity = 1.0 / conductivity if conductivity > 0 else float('inf')

    J = calc_conduction_current(E_field, conductivity)
    I = np.linalg.norm(J) * cross_section_area
    R = calc_resistance(resistivity, conductor_length, cross_section_area)
    V = np.linalg.norm(E_field) * conductor_length

    # Power
    P_Joule = I ** 2 * R if R < float('inf') else 0
    P_field = calc_power_dissipation_conduction(E_field, conductivity, conductor_length * cross_section_area)

    return {
        "E_field": E_field,
        "E_magnitude": np.linalg.norm(E_field),
        "conductivity": conductivity,
        "resistivity": resistivity,
        "current_density_J": J,
        "total_current_I": I,
        "resistance_R": R,
        "voltage_V": V,
        "power_Joule": P_Joule,
        "power_field": P_field,
        "conductor_length": conductor_length,
        "cross_section_area": cross_section_area,
    }
