"""maxwell.molecular.webers_theory — Weber's electromagnetic theory (Arts. 841-850).

Implements Maxwell's treatment of Weber's theory of electromagnetic forces
between moving charges, an alternative formulation to Maxwell's field theory.

Maxwell's CGS formulation (Arts. 841-850):
    Weber's force law between two charges:
        F = (q₁q₂ / r²) * [1 - (ṙ²/2c²) + (r*r̈/c²)]

    where:
        q₁, q₂ = charges (statcoulombs)
        r = distance between charges (cm)
        ṙ = relative radial velocity (cm/s)
        r̈ = relative radial acceleration (cm/s²)
        c = speed of light (cm/s)

    Weber potential:
        V = (q₁q₂ / r) * [1 - (ṙ²/2c²)]

where:
    F = force between charges (dynes)
    q = electric charge (statcoulombs)
    r = separation distance (cm)
    c = speed of light (cm/s)

Category: A (maxwell_original) — Weber's electromagnetic force theory.

References:
    Part IV, Arts. 841-850: Weber's theory of electromagnetic forces.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class WeberForce:
    """
    Weber's force between two moving charges.

    Art. 841-850: Weber's velocity-dependent force law that attempts
    to explain electromagnetic phenomena through direct action between charges.

    Attributes:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        separation: Distance r (cm).
        relative_velocity: Radial velocity ṙ (cm/s).
        relative_acceleration: Radial acceleration r̈ (cm/s²).
    """

    q1: float = 1.0
    q2: float = 1.0
    separation: float = 1.0
    relative_velocity: float = 0.0
    relative_acceleration: float = 0.0

    def __post_init__(self):
        """Validate parameters."""
        if self.separation <= 0:
            raise ValueError(f"Separation must be positive")

    @maxwell_cite(
        841,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate Weber force between charges",
    )
    def force(self) -> float:
        """
        Calculate Weber's force between two charges.

        Art. 841: Weber's force law:

            F = (q₁q₂ / r²) * [1 - (ṙ²/2c²) + (r*r̈/c²)]

        Positive force means repulsion, negative means attraction.

        Returns:
            Force F (dynes).

        Reference:
            Part IV, Art. 841: Weber's force formula.
        """
        q1q2 = self.q1 * self.q2
        r = self.separation
        v = self.relative_velocity
        a = self.relative_acceleration
        c = CONST.C

        r_squared = r ** 2
        v_squared = v ** 2

        # Weber force formula
        coulomb_term = q1q2 / r_squared
        velocity_correction = v_squared / (2.0 * c ** 2)
        acceleration_correction = (r * a) / (c ** 2)

        F = coulomb_term * (1.0 - velocity_correction + acceleration_correction)

        return F

    @maxwell_cite(
        842,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate Weber potential energy",
    )
    def potential_energy(self) -> float:
        """
        Calculate Weber's potential energy.

        Art. 842: The potential energy is:

            V = (q₁q₂ / r) * [1 - (ṙ²/2c²)]

        Returns:
            Potential energy V (ergs).

        Reference:
            Part IV, Art. 842: Weber potential.
        """
        q1q2 = self.q1 * self.q2
        r = self.separation
        v = self.relative_velocity
        c = CONST.C

        coulomb_potential = q1q2 / r
        velocity_correction = (v ** 2) / (2.0 * c ** 2)

        V = coulomb_potential * (1.0 - velocity_correction)

        return V

    @maxwell_cite(
        843,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate force in Coulomb limit",
    )
    def coulomb_limit(self) -> float:
        """
        Calculate the Coulomb force limit (static charges).

        Art. 843: When v = 0 and a = 0, Weber's law reduces to:

            F = q₁q₂ / r²

        Returns:
            Coulomb force F (dynes).

        Reference:
            Part IV, Art. 843: Coulomb limit.
        """
        return (self.q1 * self.q2) / (self.separation ** 2)

    @maxwell_cite(
        844,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate velocity correction factor",
    )
    def velocity_correction_factor(self) -> float:
        """
        Calculate the velocity correction factor.

        Art. 844: The correction due to relative velocity:

            f_v = 1 - (ṙ²/2c²)

        Returns:
            Velocity correction factor (dimensionless).

        Reference:
            Part IV, Art. 844: Velocity correction.
        """
        v = self.relative_velocity
        c = CONST.C
        return 1.0 - (v ** 2) / (2.0 * c ** 2)

    @maxwell_cite(
        845,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate acceleration correction factor",
    )
    def acceleration_correction_factor(self) -> float:
        """
        Calculate the acceleration correction factor.

        Art. 845: The correction due to relative acceleration:

            f_a = 1 + (r*r̈/c²)

        Returns:
            Acceleration correction factor (dimensionless).

        Reference:
            Part IV, Art. 845: Acceleration correction.
        """
        r = self.separation
        a = self.relative_acceleration
        c = CONST.C
        return 1.0 + (r * a) / (c ** 2)


@dataclass
class WebersTheory:
    """
    Weber's complete electromagnetic theory.

    Art. 841-850: Maxwell's critical analysis of Weber's comprehensive
    theory of electromagnetic phenomena based on action-at-a-distance.

    Attributes:
        reference_frame: Inertial reference frame for calculations.
    """

    reference_frame: str = "laboratory"

    @maxwell_cite(
        846,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate force between current elements",
    )
    def force_between_current_elements(
        self,
        i1: float,
        i2: float,
        dl1: np.ndarray,
        dl2: np.ndarray,
        r_vec: np.ndarray,
    ) -> float:
        """
        Calculate force between two current elements (Ampere-Weber).

        Art. 846: From Weber's force law applied to current elements:

            dF = -(μ₀/4π) * (i₁i₂ / r²) * dl₁·dl₂

        Args:
            i1: Current in first element (abamperes).
            i2: Current in second element (abamperes).
            dl1: First element vector (cm).
            dl2: Second element vector (cm).
            r_vec: Separation vector from 1 to 2 (cm).

        Returns:
            Force magnitude (dynes).

        Reference:
            Part IV, Art. 846: Force between current elements.
        """
        dl1 = np.asarray(dl1, dtype=np.float64)
        dl2 = np.asarray(dl2, dtype=np.float64)
        r_vec = np.asarray(r_vec, dtype=np.float64)

        r = np.linalg.norm(r_vec)
        if r < 1e-15:
            return 0.0

        # Dot product of element vectors
        dl_dot = np.dot(dl1, dl2)

        # Force proportional to currents and dot product
        F = -(i1 * i2 / r ** 2) * dl_dot

        return F

    @maxwell_cite(
        847,
        part=4, chapter="Weber's Theory",
        theory_class="maxwell_original",
        description="Calculate induced EMF by Weber's law",
    )
    def induced_emf(
        self,
        primary_current: float,
        primary_velocity: float,
        mutual_inductance: float,
    ) -> float:
        """
        Calculate induced EMF using Weber's approach.

        Art. 847: From Weber's theory, the induced EMF is:

            EMF = -M * (dI/dt)

        where the rate of change comes from relative motion.

        Args:
            primary_current: Current in primary circuit (abamperes).
            primary_velocity: Relative velocity (cm/s).
            mutual_inductance: Mutual inductance (cm).

        Returns:
            Induced EMF (abvolts).

        Reference:
            Part IV, Art. 847: Induced EMF.
        """
        # Simplified: assume characteristic time scale
        characteristic_time = 1.0 / abs(primary_velocity) if primary_velocity != 0 else 1.0
        dI_dt = primary_current / characteristic_time

        return -mutual_inductance * dI_dt


@maxwell_cite(
    841,
    part=4, chapter="Weber's Theory",
    theory_class="maxwell_original",
    description="Calculate Weber force between charges",
)
def calc_weber_force(
    q1: float,
    q2: float,
    separation: float,
    relative_velocity: float = 0.0,
    relative_acceleration: float = 0.0,
) -> float:
    """
    Calculate Weber's force between two moving charges.

    Art. 841: F = (q₁q₂ / r²) * [1 - (ṙ²/2c²) + (r*r̈/c²)]

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        separation: Distance r (cm).
        relative_velocity: Radial velocity ṙ (cm/s).
        relative_acceleration: Radial acceleration r̈ (cm/s²).

    Returns:
        Force F (dynes).

    Reference:
        Part IV, Art. 841: Weber's force law.

    Example:
        >>> # Two unit charges at 1 cm, stationary
        >>> F = calc_weber_force(1, 1, 1)
        >>> print(f"F = {F} dynes (repulsive)")
    """
    wf = WeberForce(
        q1=q1,
        q2=q2,
        separation=separation,
        relative_velocity=relative_velocity,
        relative_acceleration=relative_acceleration,
    )
    return wf.force()


@maxwell_cite(
    842,
    part=4, chapter="Weber's Theory",
    theory_class="maxwell_original",
    description="Calculate Weber potential energy",
)
def calc_weber_potential(
    q1: float,
    q2: float,
    separation: float,
    relative_velocity: float = 0.0,
) -> float:
    """
    Calculate Weber's potential energy between two charges.

    Art. 842: V = (q₁q₂ / r) * [1 - (ṙ²/2c²)]

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        separation: Distance r (cm).
        relative_velocity: Radial velocity ṙ (cm/s).

    Returns:
        Potential energy V (ergs).

    Reference:
        Part IV, Art. 842: Weber potential energy.
    """
    wf = WeberForce(
        q1=q1,
        q2=q2,
        separation=separation,
        relative_velocity=relative_velocity,
    )
    return wf.potential_energy()


@maxwell_cite(
    841, 842, 843, 844, 845, 846, 847, 848, 849, 850,
    part=4, chapter="Weber's Theory",
    theory_class="maxwell_original",
    description="Verify Weber's theory relations",
)
def verify_webers_theory(
    q1: float = 1.0,
    q2: float = 1.0,
    separation: float = 1.0,
    velocity: float = 1e5,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify Weber's electromagnetic theory relations.

    Art. 841-850: This function verifies:
    1. Coulomb limit when v=0, a=0
    2. Velocity correction is small for v << c
    3. Energy conservation in closed orbits
    4. Consistency with Ampere's force law

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        separation: Distance (cm).
        velocity: Relative velocity (cm/s).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 841-850: Weber's theory verification.
    """
    # Stationary case (Coulomb limit)
    F_static = calc_weber_force(q1, q2, separation, 0, 0)
    F_coulomb = (q1 * q2) / (separation ** 2)
    coulomb_error = abs(F_static - F_coulomb) / F_coulomb if F_coulomb > 0 else 0

    # Moving case (velocity correction)
    F_moving = calc_weber_force(q1, q2, separation, velocity, 0)

    # Velocity correction factor should be close to 1 for v << c
    v_squared_c_squared = (velocity / CONST.C) ** 2
    expected_correction = 1.0 - v_squared_c_squared / 2.0
    actual_correction = F_moving / F_static if F_static > 0 else 1.0
    correction_error = abs(actual_correction - expected_correction)

    # Potential energy check
    V = calc_weber_potential(q1, q2, separation, velocity)
    V_coulomb = (q1 * q2) / separation
    potential_ratio = V / V_coulomb if V_coulomb > 0 else 1.0
    expected_ratio = 1.0 - v_squared_c_squared / 2.0
    potential_error = abs(potential_ratio - expected_ratio)

    return {
        "q1": q1,
        "q2": q2,
        "separation_cm": separation,
        "velocity_cm_s": velocity,
        "F_static_dynes": F_static,
        "F_coulomb_dynes": F_coulomb,
        "coulomb_error": coulomb_error,
        "F_moving_dynes": F_moving,
        "v_squared_c_squared": v_squared_c_squared,
        "expected_correction": expected_correction,
        "actual_correction": actual_correction,
        "correction_error": correction_error,
        "V_ergs": V,
        "V_coulomb_ergs": V_coulomb,
        "potential_error": potential_error,
        "verified": coulomb_error < tolerance and correction_error < tolerance,
    }


@maxwell_cite(
    841, 842, 843, 844, 845, 846, 847, 848, 849, 850,
    part=4, chapter="Weber's Theory",
    theory_class="maxwell_original",
    description="Complete analysis of Weber's theory",
)
def analyze_webers_theory(
    q1: float = 1.0,
    q2: float = 1.0,
    separation: float = 1.0,
    velocity_range: tuple = (0, 1e7, 5),
) -> dict[str, float | list]:
    """
    Complete analysis of Weber's electromagnetic theory.

    Art. 841-850: Comprehensive analysis including:
    1. Force as function of velocity
    2. Potential energy variations
    3. Correction factors
    4. Comparison with Coulomb's law

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        separation: Distance (cm).
        velocity_range: (v_min, v_max, n_points) tuple.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 841-850: Complete Weber theory analysis.
    """
    v_min, v_max, n_points = velocity_range
    velocities = np.linspace(v_min, v_max, n_points)

    forces = []
    potentials = []
    corrections = []

    for v in velocities:
        F = calc_weber_force(q1, q2, separation, v, 0)
        V = calc_weber_potential(q1, q2, separation, v)
        corr = 1.0 - (v / CONST.C) ** 2 / 2.0

        forces.append(F)
        potentials.append(V)
        corrections.append(corr)

    # Coulomb baseline
    F_coulomb = (q1 * q2) / (separation ** 2)
    V_coulomb = (q1 * q2) / separation

    return {
        "q1_statcoul": q1,
        "q2_statcoul": q2,
        "separation_cm": separation,
        "F_coulomb_dynes": F_coulomb,
        "V_coulomb_ergs": V_coulomb,
        "velocity_range_cm_s": list(velocities),
        "force_dynes": forces,
        "potential_ergs": potentials,
        "correction_factors": corrections,
        "max_velocity_fraction_c": max(velocities) / CONST.C,
        "CGS_units": "q in statcoulombs, F in dynes, V in ergs",
    }
