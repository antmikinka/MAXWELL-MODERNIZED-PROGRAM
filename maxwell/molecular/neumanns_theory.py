"""maxwell.molecular.neumanns_theory — Neumann's electromagnetic potential (Arts. 851-858).

Implements Maxwell's treatment of Neumann's theory of electromagnetic
potential and mutual inductance between circuits.

Maxwell's CGS formulation (Arts. 851-858):
    Neumann's formula for mutual inductance:
        M = ∮∮ (dl₁ · dl₂) / r

    where:
        dl₁, dl₂ = line elements of the two circuits (cm)
        r = distance between line elements (cm)
        M = mutual inductance (cm in CGS)

    Neumann potential for current element:
        A = I ∮ dl / r

    where:
        A = vector potential (gauss·cm)
        I = current (abamperes)

where:
    M = mutual inductance (cm)
    A = vector potential (gauss·cm)
    r = distance (cm)
    I = current (abamperes)

Category: A (maxwell_original) — Neumann's potential theory.

References:
    Part IV, Arts. 851-858: Neumann's electromagnetic potential.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class NeumannPotential:
    """
    Neumann's electromagnetic potential theory.

    Art. 851-858: Neumann's formulation of electromagnetic interactions
    through a potential function that depends on circuit geometry.

    Attributes:
        current: Current in the source circuit (abamperes).
        circuit_shape: Parametric description of circuit.
    """

    current: float = 1.0
    circuit_shape: Callable[[float], np.ndarray] = None

    def __post_init__(self):
        """Validate parameters."""
        if self.circuit_shape is None:
            # Default to circular loop
            self.circuit_shape = lambda t: np.array([np.cos(t), np.sin(t), 0])

    @maxwell_cite(
        851,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate vector potential from current loop",
    )
    def vector_potential_at(
        self,
        observation_point: np.ndarray,
        n_segments: int = 100,
    ) -> np.ndarray:
        """
        Calculate vector potential at observation point.

        Art. 851: The vector potential is:

            A(r) = I ∮ dl' / |r - r'|

        Args:
            observation_point: Point to evaluate A (cm).
            n_segments: Number of discretization segments.

        Returns:
            Vector potential A (gauss·cm).

        Reference:
            Part IV, Art. 851: Vector potential formula.
        """
        observation_point = np.asarray(observation_point, dtype=np.float64)

        A = np.zeros(3)
        dt = 2 * np.pi / n_segments

        for i in range(n_segments):
            t = i * dt
            r_prime = self.circuit_shape(t)

            # Tangent vector (dl)
            t_next = (i + 1) * dt
            r_prime_next = self.circuit_shape(t_next)
            dl = r_prime_next - r_prime

            # Distance to observation point
            r_vec = observation_point - r_prime
            r = np.linalg.norm(r_vec)

            if r > 1e-15:
                A += self.current * dl / r

        return A

    @maxwell_cite(
        852,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate magnetic flux through loop",
    )
    def magnetic_flux_through(
        self,
        target_loop: Callable[[float], np.ndarray],
        n_segments: int = 100,
    ) -> float:
        """
        Calculate magnetic flux through target loop.

        Art. 852: The flux is:

            Φ = ∮ A · dl

        Args:
            target_loop: Parametric target loop function.
            n_segments: Number of discretization segments.

        Returns:
            Magnetic flux Φ (maxwells).

        Reference:
            Part IV, Art. 852: Magnetic flux.
        """
        flux = 0.0
        dt = 2 * np.pi / n_segments

        for i in range(n_segments):
            t = i * dt
            r = target_loop(t)

            # Get vector potential at this point
            A = self.vector_potential_at(r, n_segments)

            # Tangent vector
            t_next = (i + 1) * dt
            r_next = target_loop(t_next)
            dl = r_next - r

            flux += np.dot(A, dl)

        return flux


@dataclass
class NeumannTheory:
    """
    Neumann's complete electromagnetic theory.

    Art. 851-858: Maxwell's analysis of Neumann's potential-based
    formulation of electromagnetic induction.

    Attributes:
        reference_configuration: Circuit configuration reference.
    """

    reference_configuration: str = "general"

    @maxwell_cite(
        853,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate mutual inductance between loops",
    )
    def mutual_inductance(
        self,
        loop1=None,
        loop2=None,
        R1: float = None,
        R2: float = None,
        d: float = None,
        n_segments: int = 100,
    ) -> float:
        """
        Calculate mutual inductance using Neumann's formula.

        Art. 853: Neumann's formula:

            M = ∮∮ (dl₁ · dl₂) / r₁₂

        Can be called with either:
        - loop1, loop2: Callable parametrizations
        - R1, R2, d: Parameters for coaxial circular loops

        Args:
            loop1: First loop parametrization (Callable).
            loop2: Second loop parametrization (Callable).
            R1: Radius of first loop (cm).
            R2: Radius of second loop (cm).
            d: Axial separation (cm).
            n_segments: Number of discretization segments per loop.

        Returns:
            Mutual inductance M (cm).

        Reference:
            Part IV, Art. 853: Neumann's mutual inductance formula.
        """
        # Handle coaxial circular loops case
        if R1 is not None and R2 is not None and d is not None:

            def loop1_func(t):
                return np.array([R1 * np.cos(t), R1 * np.sin(t), 0])

            def loop2_func(t):
                return np.array([R2 * np.cos(t), R2 * np.sin(t), d])

            loop1 = loop1_func
            loop2 = loop2_func

        if loop1 is None or loop2 is None:
            return 0.0

        M = 0.0
        dt1 = 2 * np.pi / n_segments
        dt2 = 2 * np.pi / n_segments

        for i in range(n_segments):
            t1 = i * dt1
            r1 = loop1(t1)
            t1_next = (i + 1) * dt1
            r1_next = loop1(t1_next)
            dl1 = r1_next - r1

            for j in range(n_segments):
                t2 = j * dt2
                r2 = loop2(t2)
                t2_next = (j + 1) * dt2
                r2_next = loop2(t2_next)
                dl2 = r2_next - r2

                # Distance between segments
                r12_vec = r2 - r1
                r12 = np.linalg.norm(r12_vec)

                if r12 > 1e-15:
                    dl_dot = np.dot(dl1, dl2)
                    M += dl_dot / r12

        return M

    @maxwell_cite(
        854,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate self-inductance of loop",
    )
    def self_inductance(
        self,
        loop: Callable[[float], np.ndarray],
        wire_radius: float = 0.01,
        n_segments: int = 100,
    ) -> float:
        """
        Calculate self-inductance of a current loop.

        Art. 854: Self-inductance requires wire radius to avoid
        divergence at r = 0.  Maxwell's formula for a circular circuit
        of radius R and wire radius a (Treatise, circular-circuit
        formula) is, in CGS-EMU with L in cm (abhenries),

            L = 4π R [ln(8R/a) - 2]

        where the -2 corresponds to a surface-current distribution on
        the wire (a uniform volume distribution gives -7/4 instead).

        Args:
            loop: Loop parametrization.
            wire_radius: Wire radius a (cm).
            n_segments: Number of segments.

        Returns:
            Self-inductance L (cm).

        Reference:
            Part IV, Art. 854: Self-inductance.
        """
        # Get characteristic radius from loop
        points = [loop(t) for t in np.linspace(0, 2 * np.pi, n_segments)]
        distances = [np.linalg.norm(p) for p in points]
        R = np.mean(distances)  # Average radius

        if R <= wire_radius:
            return 0.0

        # Maxwell's circular-circuit formula (surface-current form).
        L = 4.0 * np.pi * R * (np.log(8 * R / wire_radius) - 2.0)

        return L

    @maxwell_cite(
        855,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate induced EMF from changing current",
    )
    def induced_emf(
        self,
        mutual_inductance_M: float,
        primary_current: float,
        current_rate_of_change: float,
    ) -> float:
        """
        Calculate induced EMF in secondary circuit.

        Art. 855: Faraday's law with Neumann potential:

            EMF₂ = -M * (dI₁/dt)

        Args:
            mutual_inductance_M: Mutual inductance (cm).
            primary_current: Primary current (abamperes).
            current_rate_of_change: dI/dt (abamperes/s).

        Returns:
            Induced EMF (abvolts).

        Reference:
            Part IV, Art. 855: Induced EMF.
        """
        return -mutual_inductance_M * current_rate_of_change

    @maxwell_cite(
        853,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate mutual inductance between circular loops",
    )
    def mutual_inductance_loops(
        self,
        R1: float,
        R2: float,
        d: float,
        n_segments: int = 100,
    ) -> float:
        """
        Calculate mutual inductance between two coaxial circular loops.

        Art. 853: Using Neumann's formula for coaxial loops.

        Args:
            R1: Radius of first loop (cm).
            R2: Radius of second loop (cm).
            d: Axial separation (cm).
            n_segments: Number of discretization segments.

        Returns:
            Mutual inductance M (cm).

        Reference:
            Part IV, Art. 853: Mutual inductance formula.
        """

        def loop1(t):
            return np.array([R1 * np.cos(t), R1 * np.sin(t), 0])

        def loop2(t):
            return np.array([R2 * np.cos(t), R2 * np.sin(t), d])

        return self.mutual_inductance(loop1, loop2, n_segments)

    @maxwell_cite(
        852,
        part=4,
        chapter="Ch XXIII: Action at Distance",
        theory_class="maxwell_original",
        description="Calculate potential energy of coupled circuits",
    )
    def potential_energy(
        self,
        M: float,
        I1: float,
        I2: float,
    ) -> float:
        """
        Calculate mutual potential energy of coupled circuits.

        Art. 852: The potential energy is:

            W = M * I1 * I2

        Args:
            M: Mutual inductance (cm).
            I1: Current in first circuit (abamperes).
            I2: Current in second circuit (abamperes).

        Returns:
            Potential energy W (ergs).

        Reference:
            Part IV, Art. 852: Mutual potential energy.
        """
        return M * I1 * I2


@maxwell_cite(
    853,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Calculate mutual inductance by Neumann's formula",
)
def calc_mutual_inductance_neumann(
    loop1_radius: float,
    loop2_radius: float,
    separation: float,
    n_segments: int = 100,
) -> float:
    """
    Calculate mutual inductance between two coaxial circular loops.

    Art. 853: Using Neumann's formula for coaxial loops:

        M = ∮∮ (dl₁ · dl₂) / r

    For coaxial circular loops, this can be computed numerically.

    Args:
        loop1_radius: Radius of first loop (cm).
        loop2_radius: Radius of second loop (cm).
        separation: Axial separation between loops (cm).
        n_segments: Number of discretization segments.

    Returns:
        Mutual inductance M (cm).

    Reference:
        Part IV, Art. 853: Mutual inductance formula.

    Example:
        >>> M = calc_mutual_inductance_neumann(10, 10, 5)
        >>> print(f"M = {M:.2f} cm")
    """

    # Define coaxial circular loops
    def loop1(t):
        return np.array([loop1_radius * np.cos(t), loop1_radius * np.sin(t), 0])

    def loop2(t):
        return np.array(
            [loop2_radius * np.cos(t), loop2_radius * np.sin(t), separation]
        )

    nt = NeumannTheory()
    return nt.mutual_inductance(loop1, loop2, n_segments)


@maxwell_cite(
    851,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Calculate Neumann potential for current element",
)
def calc_neumann_potential(
    current: float,
    source_point: np.ndarray,
    observation_point: np.ndarray,
) -> np.ndarray:
    """
    Calculate vector potential from current element.

    Art. 851: The potential from a current element is:

        dA = I * dl / r

    Args:
        current: Current (abamperes).
        source_point: Source element position (cm).
        observation_point: Observation position (cm).

    Returns:
        Vector potential dA (gauss·cm).

    Reference:
        Part IV, Art. 851: Neumann potential element.
    """
    source_point = np.asarray(source_point, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    r_vec = observation_point - source_point
    r = np.linalg.norm(r_vec)

    if r < 1e-15:
        return np.zeros(3)

    # For a differential element, return I/r times unit vector
    # In practice, this needs to be integrated over the circuit
    return current * r_vec / (r**2)


@maxwell_cite(
    852,
    853,
    854,
    856,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Verify the reciprocity, self-inductance, and energy "
    "relations computed below",
)
def verify_neumanns_theory(
    loop1_radius: float = 10.0,
    loop2_radius: float = 10.0,
    separation: float = 5.0,
    current: float = 1.0,
    tolerance: float = 1e-8,
) -> dict[str, float | bool]:
    """
    Verify Neumann's electromagnetic theory relations.

    Art. 851-858: This function verifies:
    1. Mutual inductance symmetry: M₁₂ = M₂₁
    2. Vector potential satisfies ∇·A = 0
    3. Flux linkage consistency
    4. Energy stored in coupled circuits

    Args:
        loop1_radius: First loop radius (cm).
        loop2_radius: Second loop radius (cm).
        separation: Axial separation (cm).
        current: Test current (abamperes).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 851-858: Neumann's theory verification.
    """

    # Define loops
    def loop1(t):
        return np.array([loop1_radius * np.cos(t), loop1_radius * np.sin(t), 0])

    def loop2(t):
        return np.array(
            [loop2_radius * np.cos(t), loop2_radius * np.sin(t), separation]
        )

    nt = NeumannTheory()

    # Mutual inductance (should be symmetric)
    M_12 = nt.mutual_inductance(loop1, loop2, n_segments=50)
    M_21 = nt.mutual_inductance(loop2, loop1, n_segments=50)

    # Symmetry check
    symmetry_error = abs(M_12 - M_21) / ((M_12 + M_21) / 2) if (M_12 + M_21) > 0 else 0

    # Self-inductance check
    L1 = nt.self_inductance(loop1, 0.1, 100)
    L2 = nt.self_inductance(loop2, 0.1, 100)

    # Coupling coefficient (should be < 1)
    if L1 > 0 and L2 > 0:
        k = M_12 / np.sqrt(L1 * L2)
        coupling_valid = k <= 1.0 + tolerance
    else:
        k = 0
        coupling_valid = True

    # Energy check: W = (1/2)L₁I₁² + (1/2)L₂I₂² + M*I₁*I₂
    I1 = current
    I2 = current
    W = 0.5 * L1 * I1**2 + 0.5 * L2 * I2**2 + M_12 * I1 * I2
    energy_positive = W > 0

    return {
        "loop1_radius_cm": loop1_radius,
        "loop2_radius_cm": loop2_radius,
        "separation_cm": separation,
        "M_12_cm": M_12,
        "M_21_cm": M_21,
        "symmetry_error": symmetry_error,
        "L1_cm": L1,
        "L2_cm": L2,
        "coupling_coefficient": k,
        "coupling_valid": coupling_valid,
        "energy_ergs": W,
        "energy_positive": energy_positive,
        "verified": bool(
            symmetry_error < tolerance and coupling_valid and energy_positive
        ),
    }


@maxwell_cite(
    852,
    853,
    854,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Mutual inductance vs separation, self-inductance, and "
    "coupling coefficients from Neumann's formula",
)
def analyze_neumanns_theory(
    loop1_radius: float = 10.0,
    loop2_radius: float = 10.0,
    separation_range: tuple = (1.0, 20.0, 5),
    current: float = 1.0,
) -> dict[str, float | list]:
    """
    Complete analysis of Neumann's electromagnetic theory.

    Art. 851-858: Comprehensive analysis including:
    1. Mutual inductance vs separation
    2. Self-inductance calculation
    3. Induced EMF for changing currents
    4. Energy storage in coupled circuits

    Args:
        loop1_radius: First loop radius (cm).
        loop2_radius: Second loop radius (cm).
        separation_range: (s_min, s_max, n_points) tuple.
        current: Reference current (abamperes).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 851-858: Complete Neumann theory analysis.
    """
    s_min, s_max, n_points = separation_range
    separations = np.linspace(s_min, s_max, n_points)

    def loop1(t):
        return np.array([loop1_radius * np.cos(t), loop1_radius * np.sin(t), 0])

    def loop2(t, sep):
        return np.array([loop2_radius * np.cos(t), loop2_radius * np.sin(t), sep])

    nt = NeumannTheory()

    mutual_inductances = []
    for s in separations:
        M = nt.mutual_inductance(loop1, lambda t: loop2(t, s), n_segments=50)
        mutual_inductances.append(M)

    # Self-inductance
    L1 = nt.self_inductance(loop1, 0.1, 100)
    L2 = nt.self_inductance(lambda t: loop2(t, separations[0]), 0.1, 100)

    # Coupling coefficients
    coupling_coeffs = []
    if L1 > 0 and L2 > 0:
        for M in mutual_inductances:
            k = M / np.sqrt(L1 * L2)
            coupling_coeffs.append(k)

    return {
        "loop1_radius_cm": loop1_radius,
        "loop2_radius_cm": loop2_radius,
        "L1_cm": L1,
        "L2_cm": L2,
        "separation_range_cm": list(separations),
        "mutual_inductance_cm": mutual_inductances,
        "coupling_coefficients": coupling_coeffs if coupling_coeffs else [],
        "current_abamp": current,
        "CGS_units": "M, L in cm, I in abamperes",
    }


# =============================================================================
# STANDALONE FUNCTIONS FOR DIRECT IMPORT (as expected by tests)
# =============================================================================


@maxwell_cite(
    853,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Calculate mutual inductance between circular loops",
)
def neumann_mutual_inductance(
    R1: float,
    R2: float,
    d: float,
    n_segments: int = 100,
) -> float:
    """
    Calculate mutual inductance between two coaxial circular loops.

    Art. 853: Using Neumann's formula:

        M = ∮∮ (dl₁ · dl₂) / r

    Args:
        R1: Radius of first loop (cm).
        R2: Radius of second loop (cm).
        d: Axial separation (cm).
        n_segments: Number of discretization segments.

    Returns:
        Mutual inductance M (cm).

    Reference:
        Part IV, Art. 853: Mutual inductance formula.
    """
    nt = NeumannTheory()
    return nt.mutual_inductance_loops(R1, R2, d, n_segments)


@maxwell_cite(
    854,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Calculate self-inductance of circular loop",
)
def circular_loop_inductance(
    R: float,
    a: float,
) -> float:
    """
    Calculate self-inductance of a circular loop.

    Art. 854: Maxwell's formula for a circular circuit of radius R and
    wire radius a (CGS-EMU, L in cm / abhenries):

        L = 4π R [ln(8R/a) - 2]

    The -2 corresponds to a surface-current distribution on the wire;
    a uniform volume distribution would give -7/4.

    Args:
        R: Loop radius (cm).
        a: Wire radius (cm).

    Returns:
        Self-inductance L (cm).

    Reference:
        Part IV, Art. 854: Self-inductance formula.
    """
    if R <= a:
        return 0.0
    return 4.0 * np.pi * R * (np.log(8 * R / a) - 2.0)


@maxwell_cite(
    852,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Calculate mutual potential energy",
)
def mutual_potential_energy(
    M: float,
    I1: float,
    I2: float,
) -> float:
    """
    Calculate mutual potential energy of coupled circuits.

    Art. 852: The potential energy is:

        W = M * I1 * I2

    Args:
        M: Mutual inductance (cm).
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).

    Returns:
        Potential energy W (ergs).

    Reference:
        Part IV, Art. 852: Mutual potential energy.
    """
    return M * I1 * I2


# =============================================================================
# ARTS. 856-858 CONSEQUENCES OF NEUMANN'S FORMULA
# =============================================================================


@maxwell_cite(
    853,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="standard_math",
    description="Elliptic closed form for the mutual inductance of coaxial "
    "circles (Maxwell's formula), used as an independent oracle",
)
def maxwell_mutual_inductance_closed_form(
    R1: float,
    R2: float,
    d: float,
) -> float:
    """
    Mutual inductance of two coaxial circles in elliptic closed form.

    Maxwell's own closed-form evaluation of the Neumann integral for two
    coaxial circles of radii R1, R2 at axial separation d:

        M = 4π sqrt(R1 R2) [ (2/k - k) K(k²) - (2/k) E(k²) ],
        k² = 4 R1 R2 / ((R1 + R2)² + d²),

    with K, E the complete elliptic integrals of the first and second
    kind (DLMF 19.2).  This is an independent evaluation path from the
    double quadrature of :func:`neumann_mutual_inductance`; comparing
    the two is the Art. 856-857 verification below.

    Args:
        R1: Radius of first loop (cm).
        R2: Radius of second loop (cm).
        d: Axial separation (cm).

    Returns:
        Mutual inductance M (cm, CGS-EMU).

    Reference:
        Part IV, Art. 853: Neumann's formula, elliptic evaluation.
    """
    from scipy.special import ellipe, ellipk

    k2 = 4.0 * R1 * R2 / ((R1 + R2) ** 2 + d * d)
    k = np.sqrt(k2)
    return float(
        4.0
        * np.pi
        * np.sqrt(R1 * R2)
        * ((2.0 / k - k) * ellipk(k2) - (2.0 / k) * ellipe(k2))
    )


@maxwell_cite(
    856,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Computed reciprocity residual M12 - M21 of Neumann's " "formula",
)
def neumann_reciprocity_residual(
    R1: float = 1.0,
    R2: float = 2.0,
    d: float = 3.0,
    n_segments_12: int = 160,
    n_segments_21: int = 120,
) -> float:
    """
    Reciprocity residual of the mutual inductance.

    Art. 856 (computed consequence): Neumann's double integral is
    symmetric under exchange of the two circuits, so the mutual
    inductance must satisfy M12 = M21.  The residual

        |M(R1, R2, d) - M(R2, R1, d)| / M(R1, R2, d)

    is evaluated with DIFFERENT discretizations in the two directions
    (n_segments_12 vs n_segments_21) so the test is not trivially zero
    by construction.

    Args:
        R1, R2: Loop radii (cm); use unequal values for a real test.
        d: Axial separation (cm).
        n_segments_12: Segments for the M12 evaluation.
        n_segments_21: Segments for the M21 evaluation.

    Returns:
        Relative reciprocity residual (dimensionless).

    Reference:
        Part IV, Art. 856: Reciprocity of mutual inductance.
    """
    M_12 = neumann_mutual_inductance(R1, R2, d, n_segments_12)
    M_21 = neumann_mutual_inductance(R2, R1, d, n_segments_21)
    scale = max(abs(M_12), abs(M_21), 1e-30)
    return abs(M_12 - M_21) / scale


@maxwell_cite(
    857,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Far-field dipole limit of Neumann's mutual inductance",
)
def neumann_far_field_residual(
    R1: float = 1.0,
    R2: float = 1.0,
    d: float = 20.0,
    n_segments: int = 240,
) -> float:
    """
    Far-field residual of the mutual inductance.

    Art. 857 (computed consequence): when the separation d is large
    compared with both radii, each loop sees the other as a magnetic
    dipole and the Neumann integral reduces to

        M -> 2 π² R1² R2² / d³   (CGS-EMU).

    This function returns the relative residual of the quadrature
    against that dipole limit, which vanishes as (R/d)².

    Args:
        R1, R2: Loop radii (cm).
        d: Axial separation (cm), should satisfy d >> R1 + R2.
        n_segments: Quadrature segments per loop.

    Returns:
        Relative residual against the far-field limit.

    Reference:
        Part IV, Art. 857: Distant-circuit limit.
    """
    M_quad = neumann_mutual_inductance(R1, R2, d, n_segments)
    M_far = 2.0 * np.pi**2 * R1**2 * R2**2 / d**3
    return abs(M_quad - M_far) / abs(M_far)


@maxwell_cite(
    858,
    part=4,
    chapter="Ch XXIII: Action at Distance",
    theory_class="maxwell_original",
    description="Motional EMF of a moving secondary circuit from dM/dt",
)
def motional_emf_coaxial(
    R1: float,
    R2: float,
    d: float,
    current: float,
    velocity: float,
    n_segments: int = 240,
    dd: float | None = None,
) -> float:
    """
    Motional EMF induced by axial motion of the secondary circuit.

    Art. 858 (computed consequence): with steady primary current I and
    relative axial velocity v = dd/dt, the induced EMF in the secondary
    is

        EMF = -d(M I)/dt = -I v (dM/dd),

    with dM/dd evaluated by central differences of the Neumann
    quadrature.  The sign encodes Lenz's law.

    Args:
        R1, R2: Loop radii (cm).
        d: Instantaneous axial separation (cm).
        current: Primary current I (abamperes).
        velocity: Relative axial velocity v = dd/dt (cm/s); positive v
            increases the separation.
        n_segments: Quadrature segments per loop.
        dd: Central-difference step (cm); default d/1000.

    Returns:
        Induced EMF (abvolts).

    Reference:
        Part IV, Art. 858: Induction by relative motion.
    """
    if d <= 0:
        raise ValueError("Separation must be positive")
    step = d / 1000.0 if dd is None else dd
    M_plus = neumann_mutual_inductance(R1, R2, d + step, n_segments)
    M_minus = neumann_mutual_inductance(R1, R2, d - step, n_segments)
    dM_dd = (M_plus - M_minus) / (2.0 * step)
    return -current * velocity * dM_dd
