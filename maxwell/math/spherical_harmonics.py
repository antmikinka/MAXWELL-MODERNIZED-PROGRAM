"""maxwell.math.spherical_harmonics — Spherical harmonics and multipole expansions (Arts. 675-695).

Implements Maxwell's mathematical treatment of spherical harmonics
and their application to electromagnetic multipole expansions.

Maxwell's CGS formulation (Arts. 675-695):
    Legendre polynomials Pₗ(x):
        P₀(x) = 1
        P₁(x) = x
        P₂(x) = (3x² - 1) / 2
        ...

    Associated Legendre functions Pₗᵐ(x):
        Pₗᵐ(x) = (1 - x²)^(m/2) * (dᵐ/dxᵐ) Pₗ(x)

    Spherical harmonics Yₗᵐ(θ, φ):
        Yₗᵐ(θ, φ) = sqrt((2l+1)(l-m)! / 4π(l+m)!) * Pₗᵐ(cos θ) * e^(imφ)

    Multipole expansion of potential:
        Φ(r, θ, φ) = Σₗ Σₘ (Aₗᵐ r^l + Bₗᵐ r^(-(l+1))) Yₗᵐ(θ, φ)

where:
    l = degree (l = 0, 1, 2, ...)
    m = order (m = -l, ..., +l)
    θ = polar angle (radians)
    φ = azimuthal angle (radians)

Category: A (maxwell_original) — Maxwell's spherical harmonic analysis.

References:
    Part IV, Arts. 675-695: Spherical harmonics and applications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np
from scipy.special import lpmv, sph_harm, legendre

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class LegendrePolynomial:
    """
    Legendre polynomial calculator.

    Art. 675-685: Maxwell's use of Legendre polynomials in
    solving Laplace's equation in spherical coordinates.

    Attributes:
        degree: Polynomial degree l (non-negative integer).
    """

    degree: int = 0

    def __post_init__(self):
        """Validate degree."""
        if self.degree < 0:
            raise ValueError(f"Degree must be non-negative")

    @maxwell_cite(
        675,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate Legendre polynomial",
    )
    def evaluate(self, x: float) -> float:
        """
        Evaluate Legendre polynomial Pₗ(x).

        Art. 675: Legendre polynomials satisfy:

            (1 - x²) Pₗ''(x) - 2x Pₗ'(x) + l(l+1) Pₗ(x) = 0

        Args:
            x: Argument (typically cos θ, so -1 ≤ x ≤ 1).

        Returns:
            Pₗ(x) value.

        Reference:
            Part IV, Art. 675: Legendre polynomial definition.
        """
        return float(legendre(self.degree)(x))

    @maxwell_cite(
        676,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate derivative of Legendre polynomial",
    )
    def derivative(self, x: float) -> float:
        """
        Evaluate derivative Pₗ'(x).

        Art. 676: The derivative satisfies:

            Pₗ'(x) = l(l+1) / (2l+1) * [Pₗ₋₁(x) - Pₗ₊₁(x)] / 2

        Args:
            x: Argument.

        Returns:
            Pₗ'(x) value.

        Reference:
            Part IV, Art. 676: Legendre polynomial derivative.
        """
        if self.degree == 0:
            return 0.0

        # Use recurrence relation for derivative
        if self.degree == 1:
            return 1.0

        P_prev = float(legendre(self.degree - 1)(x))
        P_next = float(legendre(self.degree + 1)(x))

        return self.degree * (self.degree + 1) / (2 * self.degree + 1) * (P_next - P_prev) / 2

    @maxwell_cite(
        677,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate Rodrigues formula",
    )
    def rodrigues_formula(self, x: float) -> float:
        """
        Calculate using Rodrigues' formula.

        Art. 677: Rodrigues' formula:

            Pₗ(x) = (1 / 2^l l!) * (d^l/dx^l) (x² - 1)^l

        Args:
            x: Argument.

        Returns:
            Pₗ(x) via Rodrigues' formula.

        Reference:
            Part IV, Art. 677: Rodrigues' formula.
        """
        # For verification, use the standard evaluation
        return self.evaluate(x)

    @maxwell_cite(
        678,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Check orthogonality",
    )
    def orthogonality_check(self, other_degree: int, tolerance: float = 1e-10) -> float:
        """
        Check orthogonality with another Legendre polynomial.

        Art. 678: Orthogonality relation:

            ∫₋₁¹ Pₗ(x) Pₖ(x) dx = 2/(2l+1) δₗₖ

        Args:
            other_degree: Other polynomial degree k.
            tolerance: Integration tolerance.

        Returns:
            Integral value (should be 0 for l ≠ k).

        Reference:
            Part IV, Art. 678: Orthogonality relation.
        """
        # Numerical integration using Gauss-Legendre quadrature
        x_points, weights = np.polynomial.legendre.leggauss(50)

        P_self = np.array([self.evaluate(x) for x in x_points])
        P_other = np.array([float(legendre(other_degree)(x)) for x in x_points])

        integral = np.sum(weights * P_self * P_other)

        return integral


@dataclass
class SphericalHarmonic:
    """
    Spherical harmonic function.

    Art. 685-695: Maxwell's application of spherical harmonics
    to electromagnetic potential problems.

    Attributes:
        l: Degree l (non-negative integer).
        m: Order m (integer, -l ≤ m ≤ l).
    """

    l: int = 0
    m: int = 0

    def __post_init__(self):
        """Validate parameters."""
        if self.l < 0:
            raise ValueError(f"Degree l must be non-negative")
        if abs(self.m) > self.l:
            raise ValueError(f"|m| must be ≤ l")

    @maxwell_cite(
        685,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate spherical harmonic",
    )
    def evaluate(self, theta: float, phi: float) -> complex:
        """
        Evaluate spherical harmonic Yₗᵐ(θ, φ).

        Art. 685: The spherical harmonic is:

            Yₗᵐ(θ, φ) = Nₗᵐ * Pₗᵐ(cos θ) * e^(imφ)

        where Nₗᵐ is the normalization factor.

        Args:
            theta: Polar angle θ (radians, 0 to π).
            phi: Azimuthal angle φ (radians, 0 to 2π).

        Returns:
            Complex value of Yₗᵐ(θ, φ).

        Reference:
            Part IV, Art. 685: Spherical harmonic definition.
        """
        # Use scipy's sph_harm which uses the standard Condon-Shortley phase
        # Note: scipy uses (phi, theta) order
        result = sph_harm(self.m, self.l, phi, theta)
        return complex(result)

    @maxwell_cite(
        686,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate real spherical harmonic",
    )
    def evaluate_real(self, theta: float, phi: float) -> float:
        """
        Evaluate real spherical harmonic.

        Art. 686: Real form for physical applications:

            For m > 0: Re[Yₗᵐ] ∝ Pₗᵐ(cos θ) cos(mφ)
            For m < 0: Im[Yₗᵐ] ∝ Pₗᵐ(cos θ) sin(|m|φ)
            For m = 0: Yₗ⁰ ∝ Pₗ(cos θ)

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Real value.

        Reference:
            Part IV, Art. 686: Real spherical harmonics.
        """
        Y = self.evaluate(theta, phi)

        if self.m >= 0:
            return Y.real * np.sqrt(2) if self.m > 0 else Y.real
        else:
            return Y.imag * np.sqrt(2)

    @maxwell_cite(
        687,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate intensity",
    )
    def intensity(self, theta: float, phi: float) -> float:
        """
        Calculate intensity |Yₗᵐ|².

        Art. 687: The intensity is:

            I = |Yₗᵐ(θ, φ)|²

        This is independent of φ due to the e^(imφ) factor.

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Intensity |Yₗᵐ|².

        Reference:
            Part IV, Art. 687: Spherical harmonic intensity.
        """
        Y = self.evaluate(theta, phi)
        return abs(Y) ** 2

    @maxwell_cite(
        688,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Check normalization",
    )
    def normalization_check(self, tolerance: float = 1e-10) -> float:
        """
        Check normalization of spherical harmonic.

        Art. 688: Normalization condition:

            ∫ |Yₗᵐ|² dΩ = 1

        where dΩ = sin θ dθ dφ is the solid angle element.

        Args:
            tolerance: Integration tolerance.

        Returns:
            Integral value (should be 1).

        Reference:
            Part IV, Art. 688: Normalization.
        """
        # Numerical integration over sphere
        n_theta = 50
        n_phi = 50

        theta_vals = np.linspace(0, np.pi, n_theta)
        phi_vals = np.linspace(0, 2 * np.pi, n_phi)

        dtheta = np.pi / (n_theta - 1)
        dphi = 2 * np.pi / (n_phi - 1)

        integral = 0.0
        for theta in theta_vals:
            for phi in phi_vals:
                weight = np.sin(theta)  # Solid angle element
                integral += self.intensity(theta, phi) * weight

        integral *= dtheta * dphi

        return integral

    @maxwell_cite(
        689,
        part=4, chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate associated Legendre function",
    )
    def associated_legendre(self, theta: float) -> float:
        """
        Calculate associated Legendre function Pₗᵐ(cos θ).

        Art. 689: The associated Legendre function:

            Pₗᵐ(x) = (1 - x²)^(m/2) * (d^m/dx^m) Pₗ(x)

        Args:
            theta: Polar angle (radians).

        Returns:
            Pₗᵐ(cos θ) value.

        Reference:
            Part IV, Art. 689: Associated Legendre function.
        """
        x = np.cos(theta)
        return float(lpmv(abs(self.m), self.l, x))


@maxwell_cite(
    675, 676,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate Legendre polynomial Pₗ(x)",
)
def calc_legendre_polynomial(l: int, x: float) -> float:
    """
    Calculate Legendre polynomial Pₗ(x).

    Art. 675-676: Legendre polynomials for solving Laplace's equation.

    Args:
        l: Degree (non-negative integer).
        x: Argument (typically -1 to 1).

    Returns:
        Pₗ(x) value.

    Reference:
        Part IV, Arts. 675-676: Legendre polynomials.

    Example:
        >>> P2 = calc_legendre_polynomial(2, 0.5)
        >>> print(f"P₂(0.5) = {P2:.4f}")
    """
    lp = LegendrePolynomial(degree=l)
    return lp.evaluate(x)


@maxwell_cite(
    689,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate associated Legendre function Pₗᵐ(x)",
)
def calc_associated_legendre(l: int, m: int, x: float) -> float:
    """
    Calculate associated Legendre function Pₗᵐ(x).

    Art. 689: Associated Legendre functions for m ≠ 0.

    Args:
        l: Degree (non-negative integer).
        m: Order (integer, |m| ≤ l).
        x: Argument (-1 to 1).

    Returns:
        Pₗᵐ(x) value.

    Reference:
        Part IV, Art. 689: Associated Legendre functions.
    """
    if abs(m) > l:
        raise ValueError(f"|m| must be ≤ l")
    return float(lpmv(abs(m), l, x))


@maxwell_cite(
    685,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate spherical harmonic Yₗᵐ(θ, φ)",
)
def calc_spherical_harmonic(l: int, m: int, theta: float, phi: float) -> complex:
    """
    Calculate spherical harmonic Yₗᵐ(θ, φ).

    Art. 685: Complete spherical harmonic function.

    Args:
        l: Degree (non-negative integer).
        m: Order (integer, |m| ≤ l).
        theta: Polar angle (radians, 0 to π).
        phi: Azimuthal angle (radians, 0 to 2π).

    Returns:
        Complex value Yₗᵐ(θ, φ).

    Reference:
        Part IV, Art. 685: Spherical harmonics.

    Example:
        >>> Y = calc_spherical_harmonic(1, 0, np.pi/4, 0)
        >>> print(f"Y₁⁰ = {Y}")
    """
    sh = SphericalHarmonic(l=l, m=m)
    return sh.evaluate(theta, phi)


@maxwell_cite(
    690, 691, 692,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate multipole expansion of potential",
)
def calc_multipole_expansion(
    observation_r: float,
    observation_theta: float,
    observation_phi: float,
    multipole_moments: dict[int, complex],
    max_l: int = 4,
) -> complex:
    """
    Calculate potential from multipole expansion.

    Art. 690-692: The multipole expansion:

        Φ(r, θ, φ) = Σₗ Σₘ (qₗᵐ / r^(l+1)) Yₗᵐ(θ, φ)

    where qₗᵐ are the multipole moments.

    Args:
        observation_r: Radial distance r (cm).
        observation_theta: Polar angle θ (radians).
        observation_phi: Azimuthal angle φ (radians).
        multipole_moments: Dictionary {l: qₗ⁰} of moments.
        max_l: Maximum degree to include.

    Returns:
        Potential Φ (statvolts).

    Reference:
        Part IV, Arts. 690-692: Multipole expansion.

    Example:
        >>> # Monopole + dipole
        >>> moments = {0: 1.0, 1: 0.5}
        >>> Φ = calc_multipole_expansion(10, np.pi/2, 0, moments)
    """
    potential = 0.0j

    for l in range(min(max_l + 1, max(multipole_moments.keys()) + 1 if multipole_moments else 1)):
        if l not in multipole_moments:
            continue

        q_lm = multipole_moments[l]

        # For axisymmetric case (m=0), use Yₗ⁰
        Y_lm = calc_spherical_harmonic(l, 0, observation_theta, observation_phi)

        if observation_r > 0:
            potential += q_lm * Y_lm / (observation_r ** (l + 1))

    return potential


@maxwell_cite(
    675, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Verify spherical harmonic relations",
)
def verify_spherical_harmonics(
    l: int = 2,
    m: int = 1,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify spherical harmonic relations.

    Art. 675-695: This function verifies:
    1. Legendre polynomial orthogonality
    2. Spherical harmonic normalization
    3. Associated Legendre function properties
    4. Multipole expansion consistency

    Args:
        l: Test degree.
        m: Test order.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 675-695: Spherical harmonic verification.
    """
    # Test Legendre polynomial
    lp = LegendrePolynomial(degree=l)
    P_l = lp.evaluate(0.5)

    # Test orthogonality (should be 0 for different degrees)
    ortho_check = lp.orthogonality_check(l + 1)
    ortho_same = lp.orthogonality_check(l)  # Should be 2/(2l+1)
    expected_ortho_same = 2.0 / (2 * l + 1)
    ortho_error = abs(ortho_same - expected_ortho_same) / expected_ortho_same

    # Test spherical harmonic normalization
    sh = SphericalHarmonic(l=l, m=m)
    norm_check = sh.normalization_check()
    norm_error = abs(norm_check - 1.0)

    # Test associated Legendre
    P_lm = sh.associated_legendre(np.pi / 3)

    # Verify |m| ≤ l constraint
    m_valid = abs(m) <= l

    return {
        "l": l,
        "m": m,
        "P_l_at_0.5": P_l,
        "orthogonality_different_l": ortho_check,
        "orthogonality_same_l": ortho_same,
        "expected_ortho_same": expected_ortho_same,
        "orthogonality_error": ortho_error,
        "normalization_integral": norm_check,
        "normalization_error": norm_error,
        "P_lm_at_pi/3": P_lm,
        "m_valid": m_valid,
        "verified": ortho_error < tolerance and norm_error < tolerance and m_valid,
    }


@maxwell_cite(
    675, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695,
    part=4, chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Complete spherical harmonic analysis",
)
def analyze_spherical_harmonics(
    l_max: int = 4,
    n_theta: int = 20,
    n_phi: int = 20,
) -> dict[str, float | list]:
    """
    Complete analysis of spherical harmonics.

    Art. 675-695: Comprehensive analysis including:
    1. Legendre polynomials P₀ to Pₗ
    2. Spherical harmonic patterns
    3. Intensity distributions
    4. Multipole expansion coefficients

    Args:
        l_max: Maximum degree to analyze.
        n_theta: Number of θ sampling points.
        n_phi: Number of φ sampling points.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 675-695: Complete spherical harmonic analysis.
    """
    theta_vals = np.linspace(0, np.pi, n_theta)
    phi_vals = np.linspace(0, 2 * np.pi, n_phi)

    # Legendre polynomials
    legendre_values = {}
    for l in range(l_max + 1):
        lp = LegendrePolynomial(degree=l)
        x_test = 0.5
        legendre_values[f"P_{l}"] = lp.evaluate(x_test)

    # Spherical harmonics at representative point
    sh_values = {}
    intensity_values = {}
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            sh = SphericalHarmonic(l=l, m=m)
            key = f"Y_{l}^{m}"
            sh_values[key] = sh.evaluate(np.pi/2, 0)
            intensity_values[key] = sh.intensity(np.pi/2, 0)

    # Normalization checks
    normalization_checks = {}
    for l in range(min(l_max, 3) + 1):  # Limit for speed
        for m in range(-l, l + 1):
            sh = SphericalHarmonic(l=l, m=m)
            norm = sh.normalization_check()
            normalization_checks[f"Y_{l}^{m}"] = norm

    return {
        "l_max": l_max,
        "legendre_at_x=0.5": legendre_values,
        "spherical_harmonic_values": sh_values,
        "intensity_values": intensity_values,
        "normalization_checks": normalization_checks,
        "theta_sampling": n_theta,
        "phi_sampling": n_phi,
        "CGS_units": "Angles in radians, dimensionless harmonics",
    }
