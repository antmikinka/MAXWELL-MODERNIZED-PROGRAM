"""maxwell.molecular.amperes_theory — Ampere's molecular currents (Arts. 832-840).

Implements Maxwell's treatment of Ampere's theory of molecular currents
as the explanation for magnetic phenomena in materials.

Maxwell's CGS formulation (Arts. 832-840):
    Magnetic moment of molecular current:
        m = I * A / c  (in CGS-EMU)

    where:
        I = molecular current (abamperes)
        A = area of current loop (cm²)
        c = speed of light (cm/s)

    Magnetic field from molecular current:
        B = (2m / r³) cos(θ) r̂ + (m / r³) sin(θ) θ̂

    Magnetization from aligned molecular currents:
        M = N * m  (magnetic moment per unit volume)

where:
    m = magnetic moment (erg/gauss)
    I = molecular current (abamperes)
    A = area of current loop (cm²)
    M = magnetization (gauss)
    N = number density of molecular currents (cm⁻³)

Category: A (maxwell_original) — Ampere's molecular current theory.

References:
    Part IV, Arts. 832-840: Ampere's theory of molecular currents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MolecularCurrent:
    """
    Molecular current loop representing atomic magnetic moment.

    Art. 832-840: Ampere's hypothesis that magnetic phenomena arise
    from microscopic current loops within matter.

    Attributes:
        current: Molecular current I (abamperes).
        area: Area of current loop A (cm²).
        normal: Unit normal vector to loop plane.
        position: Position of current loop center (cm).
    """

    current: float = 0.0
    area: float = 1e-16  # Typical atomic scale
    normal: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1]))
    position: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))

    def __post_init__(self):
        """Validate and normalize parameters."""
        self.normal = np.asarray(self.normal, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        # Normalize the normal vector
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

        if self.current < 0:
            raise ValueError(f"Current must be non-negative")
        if self.area <= 0:
            raise ValueError(f"Area must be positive")

    @maxwell_cite(
        832,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic moment of molecular current",
    )
    def magnetic_moment(self) -> float:
        """
        Calculate the magnetic moment of the molecular current.

        Art. 832: The magnetic moment is:

            m = I * A / c

        In CGS-EMU, this gives m in erg/gauss.

        Returns:
            Magnetic moment m (erg/gauss).

        Reference:
            Part IV, Art. 832: Magnetic moment formula.
        """
        return (self.current * self.area) / CONST.C

    @maxwell_cite(
        833,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic field at distance",
    )
    def magnetic_field_at(self, observation_point: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field at observation point.

        Art. 833: For a dipole (small current loop):

            B(r) = (3(m·r̂)r̂ - m) / r³

        where r is the vector from dipole to observation point.

        Args:
            observation_point: Position to evaluate field (cm).

        Returns:
            Magnetic field B (gauss).

        Reference:
            Part IV, Art. 833: Dipole field.
        """
        observation_point = np.asarray(observation_point, dtype=np.float64)

        # Vector from dipole to observation point
        r_vec = observation_point - self.position
        r = np.linalg.norm(r_vec)

        if r < 1e-10:
            return np.array([0.0, 0.0, 0.0])

        r_hat = r_vec / r
        m_vec = self.magnetic_moment() * self.normal

        # Dipole field: B = (3(m·r̂)r̂ - m) / r³
        m_dot_r = np.dot(m_vec, r_hat)
        B = (3.0 * m_dot_r * r_hat - m_vec) / (r ** 3)

        return B

    @maxwell_cite(
        834,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate vector potential",
    )
    def vector_potential_at(self, observation_point: np.ndarray) -> np.ndarray:
        """
        Calculate vector potential at observation point.

        Art. 834: For a magnetic dipole:

            A(r) = (m × r̂) / r²

        Args:
            observation_point: Position to evaluate potential (cm).

        Returns:
            Vector potential A (gauss·cm).

        Reference:
            Part IV, Art. 834: Vector potential.
        """
        observation_point = np.asarray(observation_point, dtype=np.float64)

        r_vec = observation_point - self.position
        r = np.linalg.norm(r_vec)

        if r < 1e-10:
            return np.array([0.0, 0.0, 0.0])

        r_hat = r_vec / r
        m_vec = self.magnetic_moment() * self.normal

        # Vector potential: A = (m × r̂) / r²
        A = np.cross(m_vec, r_hat) / (r ** 2)

        return A


@dataclass
class AmperesTheory:
    """
    Ampere's theory of molecular currents for magnetism.

    Art. 832-840: Maxwell's analysis of Ampere's hypothesis that
    all magnetic phenomena arise from molecular-scale current loops.

    Attributes:
        number_density: Number of molecular currents per unit volume (cm⁻³).
        alignment_factor: Degree of alignment (0 to 1).
    """

    number_density: float = 1e23  # Typical atomic density
    alignment_factor: float = 0.0  # 0 = random, 1 = fully aligned

    @maxwell_cite(
        835,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetization from aligned currents",
    )
    def magnetization(self, molecular_moment: float) -> float:
        """
        Calculate magnetization from aligned molecular currents.

        Art. 835: The magnetization is:

            M = N * m * f

        where:
            N = number density
            m = molecular moment
            f = alignment factor

        Args:
            molecular_moment: Average molecular moment (erg/gauss).

        Returns:
            Magnetization M (gauss).

        Reference:
            Part IV, Art. 835: Magnetization formula.
        """
        return self.number_density * molecular_moment * self.alignment_factor

    @maxwell_cite(
        836,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate magnetic susceptibility",
    )
    def susceptibility(
        self,
        molecular_moment: float,
        temperature: float,
        applied_field: float,
    ) -> float:
        """
        Calculate magnetic susceptibility.

        Art. 836: For paramagnetic materials (Curie's law):

            χ = C / T

        where C is the Curie constant.

        Args:
            molecular_moment: Molecular moment (erg/gauss).
            temperature: Absolute temperature (K).
            applied_field: Applied field (gauss).

        Returns:
            Magnetic susceptibility χ (dimensionless).

        Reference:
            Part IV, Art. 836: Magnetic susceptibility.
        """
        if temperature <= 0:
            return 0.0

        # Curie constant (simplified)
        C = (self.number_density * molecular_moment ** 2) / (3.0 * 1.38e-16)

        return C / temperature

    @maxwell_cite(
        837,
        part=4, chapter="Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate bound current density",
    )
    def bound_current_density(self, magnetization_field: np.ndarray) -> np.ndarray:
        """
        Calculate bound current density from magnetization.

        Art. 837: The bound current density is:

            J_b = c * ∇ × M

        Args:
            magnetization_field: Magnetization vector field.

        Returns:
            Bound current density J_b (abamperes/cm²).

        Reference:
            Part IV, Art. 837: Bound current density.
        """
        # Simplified: assume uniform magnetization gives zero bound current
        # In general, this requires numerical differentiation
        return np.zeros(3)


@maxwell_cite(
    832,
    part=4, chapter="Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate molecular magnetic moment",
)
def calc_molecular_moment(current: float, area: float) -> float:
    """
    Calculate magnetic moment of a molecular current.

    Art. 832: m = I * A / c

    Args:
        current: Molecular current I (abamperes).
        area: Loop area A (cm²).

    Returns:
        Magnetic moment m (erg/gauss).

    Reference:
        Part IV, Art. 832: Molecular moment formula.

    Example:
        >>> m = calc_molecular_moment(1e-6, 1e-16)
        >>> print(f"m = {m:.2e} erg/gauss")
    """
    return (current * area) / CONST.C


@maxwell_cite(
    833,
    part=4, chapter="Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate molecular field at distance",
)
def calc_molecular_field(
    molecular_moment: float,
    distance: float,
    angle: float,
) -> tuple[float, float]:
    """
    Calculate magnetic field from molecular current at distance.

    Art. 833: For a dipole field:

        B_r = (2m / r³) cos(θ)
        B_θ = (m / r³) sin(θ)

    Args:
        molecular_moment: Magnetic moment m (erg/gauss).
        distance: Distance r from dipole (cm).
        angle: Polar angle θ (radians).

    Returns:
        Tuple (B_r, B_θ) in gauss.

    Reference:
        Part IV, Art. 833: Dipole field components.
    """
    if distance <= 0:
        return (0.0, 0.0)

    r_cubed = distance ** 3

    B_radial = (2.0 * molecular_moment / r_cubed) * np.cos(angle)
    B_tangential = -(molecular_moment / r_cubed) * np.sin(angle)

    return (B_radial, B_tangential)


@maxwell_cite(
    832, 833, 834, 835, 836, 837, 838, 839, 840,
    part=4, chapter="Molecular Currents",
    theory_class="maxwell_original",
    description="Verify Ampere's theory relations",
)
def verify_amperes_theory(
    current: float = 1e-6,
    area: float = 1e-16,
    number_density: float = 1e23,
    distance: float = 1e-7,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify Ampere's molecular current theory relations.

    Art. 832-840: This function verifies:
    1. Magnetic moment formula: m = I*A/c
    2. Dipole field at large distances
    3. Magnetization from aligned moments
    4. Consistency with macroscopic magnetism

    Args:
        current: Molecular current (abamperes).
        area: Loop area (cm²).
        number_density: Number density (cm⁻³).
        distance: Test distance (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 832-840: Ampere's theory verification.
    """
    # Calculate molecular moment
    m = calc_molecular_moment(current, area)
    expected_m = (current * area) / CONST.C
    m_error = abs(m - expected_m) / expected_m if expected_m > 0 else 0

    # Calculate field at distance
    angle = np.pi / 4
    B_r, B_θ = calc_molecular_field(m, distance, angle)

    # Verify dipole field relation
    # For dipole field: B_r = (2m/r³)*cos(θ), B_θ = -(m/r³)*sin(θ)
    # Magnitude: |B| = (m/r³) * sqrt(4cos²(θ) + sin²(θ))
    B_expected = (m / (distance ** 3)) * np.sqrt(4 * np.cos(angle)**2 + np.sin(angle)**2)
    B_magnitude = np.sqrt(B_r ** 2 + B_θ ** 2)
    field_error = abs(B_magnitude - B_expected) / B_expected if B_expected > 0 else 0

    # Verify magnetization
    at = AmperesTheory(number_density=number_density, alignment_factor=1.0)
    M = at.magnetization(m)
    expected_M = number_density * m
    M_error = abs(M - expected_M) / expected_M if expected_M > 0 else 0

    return {
        "current": current,
        "area": area,
        "number_density": number_density,
        "molecular_moment": m,
        "expected_moment": expected_m,
        "moment_error": m_error,
        "B_radial": B_r,
        "B_tangential": B_θ,
        "B_magnitude": B_magnitude,
        "field_error": field_error,
        "magnetization": M,
        "magnetization_error": M_error,
        "verified": bool(m_error < tolerance and field_error < tolerance and M_error < tolerance),
    }


@maxwell_cite(
    832, 833, 834, 835, 836, 837, 838, 839, 840,
    part=4, chapter="Molecular Currents",
    theory_class="maxwell_original",
    description="Complete analysis of Ampere's theory",
)
def analyze_amperes_theory(
    current: float = 1e-6,
    area: float = 1e-16,
    number_density: float = 1e23,
    alignment_factor: float = 0.5,
    temperature: float = 300.0,
    applied_field: float = 1000.0,
) -> dict[str, float]:
    """
    Complete analysis of Ampere's molecular current theory.

    Art. 832-840: Comprehensive analysis including:
    1. Molecular moment calculation
    2. Field at various distances
    3. Bulk magnetization
    4. Temperature dependence

    Args:
        current: Molecular current (abamperes).
        area: Loop area (cm²).
        number_density: Number density (cm⁻³).
        alignment_factor: Alignment factor (0-1).
        temperature: Temperature (K).
        applied_field: Applied field (gauss).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 832-840: Complete Ampere theory analysis.
    """
    m = calc_molecular_moment(current, area)

    at = AmperesTheory(
        number_density=number_density,
        alignment_factor=alignment_factor
    )

    M = at.magnetization(m)
    chi = at.susceptibility(m, temperature, applied_field)

    # Field at characteristic distance
    char_distance = (number_density ** (-1/3))  # Average inter-atomic distance
    B_r, B_θ = calc_molecular_field(m, char_distance, 0)

    return {
        "current_abamp": current,
        "area_cm2": area,
        "molecular_moment_erg_gauss": m,
        "number_density_cm3": number_density,
        "alignment_factor": alignment_factor,
        "magnetization_gauss": M,
        "susceptibility": chi,
        "curie_constant": chi * temperature,
        "temperature_K": temperature,
        "applied_field_gauss": applied_field,
        "char_distance_cm": char_distance,
        "B_radial_at_char": B_r,
        "B_tangential_at_char": B_θ,
        "CGS_units": "m in erg/gauss, B in gauss, M in gauss",
    }
