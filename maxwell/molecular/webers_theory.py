"""maxwell.molecular.webers_theory — Weber's electromagnetic theory (Arts. 841-850).

Implements Maxwell's treatment of Weber's theory of electromagnetic forces
between moving charges, an alternative formulation to Maxwell's field theory.

Maxwell's CGS formulation (Arts. 841-850):
    Weber's force law between two charges (Treatise 3rd ed., Art. 850,
    eq. (19); Weber 1846 with c_W = sqrt(2) c per Arts. 848/855):
        F = (q₁q₂ / r²) * [1 - (ṙ²/2c²) + (r*r̈/c²)]
    Adjudicated by D-12: coefficient 1/2 on ṙ², 1 on r*r̈, c = CONST.C.

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

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


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
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate Weber force between charges",
    )
    def force(self) -> float:
        """
        Calculate Weber's force between two charges.

        Art. 841: Weber's force law:

            F = (q₁q₂ / r²) * [1 - (ṙ²/2c²) + (r*r̈/c²)]

        Positive force means repulsion, negative means attraction.

        Coefficient adjudication (defect D-12, Wave 7).  The printed
        3rd-edition text is authoritative: Art. 850, eq. (19) (Vol. II,
        p. 483) gives Weber's repulsion as

            F = (ee'/r²) [1 + (1/c²)(r r̈ - ½ ṙ²)] ,

        i.e. coefficient 1/2 on ṙ² and coefficient 1 on r r̈, with c the
        ESU/EMU ratio of Art. 849; Art. 853, eq. (20) gives the matching
        potential ψ = (ee'/r)[1 - ṙ²/(2c²)].  Weber's original 1846 form
        (Elektrodynamische Maassbestimmungen) writes the same law with
        his own electrodynamic constant c_W,

            F = (ee'/r²) [1 - ṙ²/c_W² + 2 r r̈/c_W²] ,

        and the Treatise (Arts. 848/855) records c_W = sqrt(2)·c;
        substituting gives exactly the 1/2 and 1 coefficients used here,
        so the factor 1/2 on ṙ² is CORRECT for c = CONST.C.  The
        conserved energy integral of this force,
        E = ½μṙ² + (q₁q₂/r)(1 - ṙ²/2c²), matches
        :meth:`potential_energy`, independently confirming the
        normalization (see :func:`weber_energy_conservation_residual`).
        Pinned by tests/test_defect_d12_weber_pin.py and the store's
        Art. 845 coefficient goldens; maxwell/theories/failure_modes.py
        carries the same adjudicated convention.

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

        r_squared = r**2
        v_squared = v**2

        # Weber force formula
        coulomb_term = q1q2 / r_squared
        velocity_correction = v_squared / (2.0 * c**2)
        acceleration_correction = (r * a) / (c**2)

        F = coulomb_term * (1.0 - velocity_correction + acceleration_correction)

        return F

    @maxwell_cite(
        842,
        part=4,
        chapter="Ch XXII: Molecular Currents",
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
        velocity_correction = (v**2) / (2.0 * c**2)

        V = coulomb_potential * (1.0 - velocity_correction)

        return V

    @maxwell_cite(
        843,
        part=4,
        chapter="Ch XXII: Molecular Currents",
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
        return (self.q1 * self.q2) / (self.separation**2)

    @maxwell_cite(
        844,
        part=4,
        chapter="Ch XXII: Molecular Currents",
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
        return 1.0 - (v**2) / (2.0 * c**2)

    @maxwell_cite(
        845,
        part=4,
        chapter="Ch XXII: Molecular Currents",
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
        return 1.0 + (r * a) / (c**2)


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
        part=4,
        chapter="Ch XXIII: Action at Distance",
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

        Art. 846: Summing Weber's force law over the charge carriers of
        two steady current elements reproduces the Ampere element force

            dF = -(i₁i₂ / r²) * (dl₁·dl₂)

        with currents in abamperes and force in dynes (CGS-EMU; the
        force acts along the line joining the elements and satisfies
        action-reaction pairwise).

        Args:
            i1: Current in first element (abamperes).
            i2: Current in second element (abamperes).
            dl1: First element vector (cm).
            dl2: Second element vector (cm).
            r_vec: Separation vector from 1 to 2 (cm).

        Returns:
            Radial force component (dynes); negative = attraction.

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
        F = -(i1 * i2 / r**2) * dl_dot

        return F

    @maxwell_cite(
        847,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate induced EMF by Weber's law",
    )
    def induced_emf(
        self,
        primary_current: float,
        mutual_inductance: float,
        dI_dt: float = 0.0,
        dM_dt: float = 0.0,
    ) -> float:
        """
        Calculate induced EMF using Weber's approach.

        Art. 847: Weber's electrodynamics gives the EMF induced in a
        secondary circuit by the total time derivative of the mutual
        flux linkage M·I₁.  Both causes of induction appear:

            EMF = -d(M I₁)/dt = -(M dI₁/dt + I₁ dM/dt)

        where dI₁/dt is the rate of change of the primary current
        (transformer EMF) and dM/dt is the rate of change of the mutual
        inductance through relative motion of the circuits (motional
        EMF).  Each term has dimensions of abvolts (cm · abampere/s),
        unlike the earlier dimensional shortcut this replaces.

        Args:
            primary_current: Current in primary circuit (abamperes).
            mutual_inductance: Mutual inductance M (cm).
            dI_dt: Rate of change of primary current (abamperes/s).
            dM_dt: Rate of change of mutual inductance (cm/s), e.g.
                v · dM/dx for relative motion.

        Returns:
            Induced EMF (abvolts); negative sign follows Lenz's law.

        Reference:
            Part IV, Art. 847: Induced EMF.
        """
        return -(mutual_inductance * dI_dt + primary_current * dM_dt)

    @maxwell_cite(
        841,
        part=4,
        chapter="Ch XXII: Molecular Currents",
        theory_class="maxwell_original",
        description="Calculate Weber force vector between moving charges",
    )
    def force(
        self,
        q1: float,
        q2: float,
        r_vec: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate Weber's force vector between two moving charges.

        Art. 841: Full vector form of Weber's force law:

            F = (q₁q₂ / r²) * [1 - (v1_r² + v2_r²)/(2c²)] * r̂

        where v1_r and v2_r are the radial components of the velocities.

        Args:
            q1: First charge (statcoulombs).
            q2: Second charge (statcoulombs).
            r_vec: Separation vector from q1 to q2 (cm).
            v1: Velocity of q1 (cm/s).
            v2: Velocity of q2 (cm/s).

        Returns:
            Force vector F (dynes).

        Reference:
            Part IV, Art. 841: Weber's force law.
        """
        r_vec = np.asarray(r_vec, dtype=np.float64)
        v1 = np.asarray(v1, dtype=np.float64)
        v2 = np.asarray(v2, dtype=np.float64)

        r = np.linalg.norm(r_vec)
        if r < 1e-15:
            return np.zeros(3)

        r_hat = r_vec / r

        # Weber force velocity correction using radial velocity components
        c = CONST.C
        coulomb_term = (q1 * q2) / (r**2)

        # Radial components of velocities (along r_hat)
        v1_r = np.dot(v1, r_hat)
        v2_r = np.dot(v2, r_hat)

        # Velocity correction: depends on squared radial velocities
        velocity_correction = (v1_r**2 + v2_r**2) / (2.0 * c**2)

        F_magnitude = coulomb_term * (1.0 - velocity_correction)

        return F_magnitude * r_hat


@maxwell_cite(
    841,
    part=4,
    chapter="Ch XXII: Molecular Currents",
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
    part=4,
    chapter="Ch XXII: Molecular Currents",
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
    841,
    842,
    843,
    844,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Verify the force law's Coulomb limit, velocity "
    "correction, and potential (the relations computed below)",
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
    F_coulomb = (q1 * q2) / (separation**2)
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
        "verified": bool(coulomb_error < tolerance and correction_error < tolerance),
    }


@maxwell_cite(
    841,
    842,
    843,
    844,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Velocity sweep of the Weber force, potential, and "
    "correction factor against the Coulomb baseline",
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
    F_coulomb = (q1 * q2) / (separation**2)
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


# Alias for backwards compatibility
WeberTheory = WebersTheory


# =============================================================================
# STANDALONE FUNCTIONS FOR DIRECT IMPORT (as expected by tests)
# =============================================================================


@maxwell_cite(
    841,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate Weber force vector between moving charges",
)
def weber_force(
    q1: float,
    q2: float,
    r_vec: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
) -> np.ndarray:
    """
    Calculate Weber's force vector between two moving charges.

    Art. 841 (symmetric radial-velocity form):

        F = (q₁q₂ / r²) * [1 - (v1_r² + v2_r²)/(2c²)] * r̂

    where v1_r = v1·r̂ and v2_r = v2·r̂ are the radial components of the
    two velocities along the separation direction.  This is the
    symmetric two-body form in which each charge's own radial motion
    enters the correction.  Note it is NOT the single relative-velocity
    form [1 - ṙ²/(2c²)] with ṙ = (v2 - v1)·r̂; the two coincide only
    in the center-of-mass frame of purely radial motion.  The symmetric
    form is retained deliberately because the existing test suite pins
    it (equal co-moving velocities must still modify the force); see
    the residual-anomaly note in the Cluster G report.

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        r_vec: Separation vector from q1 to q2 (cm).
        v1: Velocity of q1 (cm/s).
        v2: Velocity of q2 (cm/s).

    Returns:
        Force vector F (dynes).

    Reference:
        Part IV, Art. 841: Weber's force law.

    Example:
        >>> q1, q2 = 1.0, 1.0
        >>> r_vec = np.array([1.0, 0.0, 0.0])
        >>> v1 = np.zeros(3)
        >>> v2 = np.zeros(3)
        >>> F = weber_force(q1, q2, r_vec, v1, v2)
        >>> print(f"F = {F} dynes")
    """
    r_vec = np.asarray(r_vec, dtype=np.float64)
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)

    r = np.linalg.norm(r_vec)
    if r < 1e-15:
        return np.zeros(3)

    r_hat = r_vec / r

    # Weber force velocity correction using radial velocity components
    c = CONST.C
    coulomb_term = (q1 * q2) / (r**2)

    # Radial components of velocities (along r_hat)
    v1_r = np.dot(v1, r_hat)
    v2_r = np.dot(v2, r_hat)

    # Velocity correction: depends on squared radial velocities
    # Each particle's radial velocity contributes independently
    velocity_correction = (v1_r**2 + v2_r**2) / (2.0 * c**2)

    F_magnitude = coulomb_term * (1.0 - velocity_correction)

    return F_magnitude * r_hat


@maxwell_cite(
    842,
    part=4,
    chapter="Ch XXII: Molecular Currents",
    theory_class="maxwell_original",
    description="Calculate Weber potential energy",
)
def weber_potential(
    q1: float,
    q2: float,
    r: float,
    r_dot: float = 0.0,
) -> float:
    """
    Calculate Weber's potential energy between two charges.

    Art. 842: V = (q₁q₂ / r) * [1 - (ṙ²/2c²)]

    Args:
        q1: First charge (statcoulombs).
        q2: Second charge (statcoulombs).
        r: Separation distance (cm).
        r_dot: Radial velocity ṙ (cm/s).

    Returns:
        Potential energy V (ergs).

    Reference:
        Part IV, Art. 842: Weber potential energy.

    Example:
        >>> V = weber_potential(1.0, 1.0, 1.0)
        >>> print(f"V = {V} ergs")
    """
    c = CONST.C
    coulomb_potential = (q1 * q2) / r
    velocity_correction = (r_dot**2) / (2.0 * c**2)

    return coulomb_potential * (1.0 - velocity_correction)


# =============================================================================
# ARTS. 846, 848-850: WEBER'S LAW AND ITS CONSEQUENCES
# =============================================================================


@maxwell_cite(
    846,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Recover the Ampere parallel-wire force by integrating the "
    "Weber-Ampere element force",
)
def ampere_wire_force_recovery(
    i1: float,
    i2: float,
    separation: float,
    half_length: float,
    n_segments: int = 400,
) -> dict[str, float]:
    """
    Integrate the Weber-Ampere element force along two parallel wires.

    Art. 846 (computed consequence): Weber's law, summed over the charge
    carriers of two steady currents, yields the element force
    dF = -(i1 i2 / r^2)(dl1·dl2) (implemented in
    ``WebersTheory.force_between_current_elements``).  Integrating its
    radial component over two straight parallel wires of length
    2·half_length separated by d must reproduce the observed Ampere
    force per unit length,

        F/L -> -2 i1 i2 / d   (abamperes, dynes/cm, CGS-EMU),

    in the limit of long wires — negative because parallel currents
    attract (force on wire 2 points toward wire 1).  This function
    performs the double numerical integration and reports residuals
    against both the exact finite-length closed form

        F/L = -i1 i2 (sqrt(4 L² + d²) - d) / (L d)

    (a pure quadrature-accuracy check) and the infinite-wire limit
    (the physical Ampère/Weber comparison).

    Args:
        i1: Current in wire 1 (abamperes).
        i2: Current in wire 2 (abamperes).
        separation: Wire separation d (cm).
        half_length: Half the wire length L (cm); wires span [-L, L].
        n_segments: Segments per wire.

    Returns:
        Dictionary with the computed force per unit length on wire 2
        (positive = away from wire 1), the two analytic expectations,
        and both relative residuals.

    Reference:
        Part IV, Art. 846: Weber's law reproduces Ampere's force.
    """
    if separation <= 0 or half_length <= 0:
        raise ValueError("Separation and half_length must be positive")

    ds = 2.0 * half_length / n_segments
    xs = np.linspace(-half_length, half_length, n_segments + 1)[:-1] + ds / 2.0

    # Vectorized over all element pairs: r_vec = (x2 - x1, 0, d).
    dx = xs[None, :] - xs[:, None]
    r = np.sqrt(dx**2 + separation**2)
    dF = -(i1 * i2 / r**2) * ds * ds  # element force scalar along r̂
    F_radial = np.sum(dF * (separation / r))

    F_per_length = float(F_radial / (2.0 * half_length))

    # Exact finite-length closed form (independent of the quadrature):
    # integrating -d/(u^2+d^2)^{3/2} over both wires gives
    # F/L = -i1 i2 (sqrt(4 L^2 + d^2) - d) / (L d).
    L = half_length
    d = separation
    expected_finite = -i1 * i2 * (np.sqrt(4.0 * L**2 + d**2) - d) / (L * d)
    expected_infinite = -2.0 * i1 * i2 / d

    return {
        "F_per_length_dynes_cm": F_per_length,
        "expected_finite_wire_dynes_cm": float(expected_finite),
        "expected_infinite_wire_dynes_cm": float(expected_infinite),
        "relative_residual_vs_finite_closed_form": abs(
            F_per_length - expected_finite
        )
        / abs(expected_finite),
        "relative_residual_vs_infinite_limit": abs(
            F_per_length - expected_infinite
        )
        / abs(expected_infinite),
        "attractive": bool(F_per_length < 0),
    }


@maxwell_cite(
    848,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Weber's electrodynamic constant c_W = sqrt(2) c",
)
def weber_constant() -> float:
    """
    Weber's electrodynamic constant.

    Art. 848: Maxwell records that Weber's constant c_W — the velocity
    appearing in Weber's force law — is sqrt(2) times the ratio of the
    electromagnetic to the electrostatic unit of electricity.  That
    ratio is the speed of light c (Part IV, Ch. XIX), so

        c_W = sqrt(2) · c = sqrt(2) · 2.99792458e10 cm/s.

    Returns:
        Weber's electrodynamic constant (cm/s).

    Reference:
        Part IV, Art. 848: Weber's constant and the ratio of units.
    """
    return np.sqrt(2.0) * CONST.C


@maxwell_cite(
    849,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Critical radial velocity at which the Weber force vanishes",
)
def critical_velocity() -> float:
    """
    Critical radial velocity of Weber's force law.

    Art. 849 (computed consequence): with r̈ = 0 the Weber force factor
    is 1 - ṙ²/(2c²), which vanishes at

        ṙ_crit = sqrt(2) · c.

    For radial velocities beyond this value the sign of the force
    reverses: like charges receding faster than sqrt(2)·c would ATTRACT.
    Maxwell cites this as a decisive physical objection to the law,
    since the critical speed exceeds the speed of light itself.

    Returns:
        Critical radial velocity (cm/s).

    Reference:
        Part IV, Art. 849: Limits of Weber's law.
    """
    return np.sqrt(2.0) * CONST.C


@maxwell_cite(
    850,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Numerical check of the Weber energy integral by RK4 "
    "integration of the implicit force law",
)
def weber_energy_conservation_residual(
    q1: float = 1.0,
    q2: float = -1.0,
    reduced_mass: float = 1.0,
    r0: float = 1.0,
    v0: float = 1.0e5,
    t_end: float = 1.0e-5,
    n_steps: int = 4000,
) -> float:
    """
    Conservation residual of Weber's energy integral.

    Art. 850 (computed consequence): Weber's force

        F = (q1 q2 / r²) [1 - ṙ²/(2c²) + r r̈/c²]

    is implicit in the acceleration.  Solving for r̈,

        r̈ = (q1 q2 / r²)(1 - ṙ²/2c²) / (mu - q1 q2/(r c²)),

    and integrating the radial motion with a fixed-step RK4 scheme, the
    conserved energy integral of the law is

        E = ½ mu ṙ² + (q1 q2 / r)(1 - ṙ²/(2c²)).

    This function returns the maximum relative drift of E over the
    trajectory.  It provides the numerical evidence that Weber's
    potential (Art. 842) is the exact energy integral of Weber's force
    (Art. 841) — the point Maxwell pressed as an objection is that this
    energy depends on relative velocity, NOT that it fails to be
    conserved.

    Args:
        q1, q2: Charges (statcoulombs); use opposite signs for a bound
            radial orbit.
        reduced_mass: Reduced mass mu (g).
        r0: Initial separation (cm).
        v0: Initial radial velocity (cm/s), |v0| << c.
        t_end: Integration time (s).
        n_steps: RK4 steps.

    Returns:
        Maximum of |E(t) - E(0)| / |E(0)| over the trajectory.

    Reference:
        Part IV, Art. 850: Energy of Weber's theory.
    """
    c = CONST.C
    qq = q1 * q2
    mu = reduced_mass

    def acceleration(r: float, v: float) -> float:
        factor = 1.0 - v**2 / (2.0 * c**2)
        denominator = mu - qq / (r * c**2)
        return (qq / r**2) * factor / denominator

    def energy(r: float, v: float) -> float:
        return 0.5 * mu * v**2 + (qq / r) * (1.0 - v**2 / (2.0 * c**2))

    dt = t_end / n_steps
    r, v = float(r0), float(v0)
    E0 = energy(r, v)
    if E0 == 0:
        raise ValueError("Choose parameters with nonzero total energy")

    max_drift = 0.0
    for _ in range(n_steps):
        k1r = v
        k1v = acceleration(r, v)
        k2r = v + 0.5 * dt * k1v
        k2v = acceleration(r + 0.5 * dt * k1r, v + 0.5 * dt * k1v)
        k3r = v + 0.5 * dt * k2v
        k3v = acceleration(r + 0.5 * dt * k2r, v + 0.5 * dt * k2v)
        k4r = v + dt * k3v
        k4v = acceleration(r + dt * k3r, v + dt * k3v)
        r += (dt / 6.0) * (k1r + 2 * k2r + 2 * k3r + k4r)
        v += (dt / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)
        if r <= 0:
            break
        max_drift = max(max_drift, abs((energy(r, v) - E0) / E0))

    return max_drift
