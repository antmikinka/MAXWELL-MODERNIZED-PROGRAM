"""maxwell.math.elliptic_integrals — Elliptic integrals and functions (Arts. 696-705).

Implements Maxwell's mathematical treatment of elliptic integrals
and their application to electromagnetic problems.

Maxwell's CGS formulation (Arts. 696-705):
    Elliptic integral of the first kind:
        F(φ, k) = ∫₀^φ dθ / sqrt(1 - k² sin² θ)

    Complete elliptic integral of the first kind:
        K(k) = F(π/2, k) = ∫₀^(π/2) dθ / sqrt(1 - k² sin² θ)

    Elliptic integral of the second kind:
        E(φ, k) = ∫₀^φ sqrt(1 - k² sin² θ) dθ

    Complete elliptic integral of the second kind:
        E(k) = E(π/2, k) = ∫₀^(π/2) sqrt(1 - k² sin² θ) dθ

    Elliptic integral of the third kind:
        Π(n; φ, k) = ∫₀^φ dθ / (1 + n sin² θ) sqrt(1 - k² sin² θ)

where:
    k = modulus (0 ≤ k ≤ 1)
    φ = amplitude (radians)
    n = characteristic (for third kind)

Parameter convention (m = k²):
    Since the 2026-08-21 math-spine hardening this module also provides
    ``calc_complete_elliptic_k_parameter`` / ``calc_complete_elliptic_e_parameter``
    which evaluate K(m), E(m) on the full real domain m < 1 — including
    NEGATIVE parameter (imaginary modulus) — by the arithmetic-geometric
    mean (DLMF §19.8) combined with the imaginary-modulus transformation
    (DLMF §19.7).  The AGM iteration is the classical descending-Landen
    process of Treatise Arts. 700-701 in its quadratically convergent
    Gauss form.  Accuracy: full double precision (~1e-15 relative) for
    every m < 1; the previous scipy pass-through was restricted to
    0 ≤ m ≤ 1 by the public wrappers.

Category: A (maxwell_original) — Maxwell's elliptic integral methods.

References:
    Part IV, Arts. 696-705: Elliptic integrals in electromagnetism.
    DLMF §§19.2, 19.7, 19.8: complete elliptic integrals, Landen and
    imaginary-modulus transformations, arithmetic-geometric mean.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import trapezoid
from scipy.special import ellipj, ellipk

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class EllipticIntegral:
    """
    Elliptic integral calculator.

    Art. 696-705: Maxwell's use of elliptic integrals for
    calculating electromagnetic fields in complex geometries.

    Attributes:
        modulus: Modulus k (0 ≤ k ≤ 1).
    """

    modulus: float = 0.5

    def __post_init__(self):
        """Validate modulus."""
        if not 0 <= self.modulus <= 1:
            raise ValueError(f"Modulus k must be in [0, 1]")

    @maxwell_cite(
        696,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate first kind elliptic integral",
    )
    def first_kind(self, amplitude: float = np.pi / 2) -> float:
        """
        Calculate elliptic integral of the first kind F(φ, k).

        Art. 696: The incomplete elliptic integral:

            F(φ, k) = ∫₀^φ dθ / sqrt(1 - k² sin² θ)

        For φ = π/2, this gives the complete integral K(k).

        Args:
            amplitude: Amplitude φ (radians).

        Returns:
            F(φ, k) value.

        Reference:
            Part IV, Art. 696: First kind elliptic integral.
        """
        k = self.modulus

        if amplitude == np.pi / 2:
            # Complete elliptic integral (hardened AGM evaluation)
            return calc_complete_elliptic_k_parameter(k**2)

        # Incomplete integral via numerical integration
        def integrand(theta):
            denom = np.sqrt(1 - k**2 * np.sin(theta) ** 2)
            return 1.0 / denom if denom > 1e-15 else 1e15

        # Numerical integration using trapezoidal rule
        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = trapezoid([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        697,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate second kind elliptic integral",
    )
    def second_kind(self, amplitude: float = np.pi / 2) -> float:
        """
        Calculate elliptic integral of the second kind E(φ, k).

        Art. 697: The incomplete elliptic integral:

            E(φ, k) = ∫₀^φ sqrt(1 - k² sin² θ) dθ

        For φ = π/2, this gives the complete integral E(k).

        Args:
            amplitude: Amplitude φ (radians).

        Returns:
            E(φ, k) value.

        Reference:
            Part IV, Art. 697: Second kind elliptic integral.
        """
        k = self.modulus

        if amplitude == np.pi / 2:
            # Complete elliptic integral (hardened AGM evaluation)
            return calc_complete_elliptic_e_parameter(k**2)

        # Incomplete integral via numerical integration
        def integrand(theta):
            return np.sqrt(1 - k**2 * np.sin(theta) ** 2)

        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = trapezoid([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        698,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate third kind elliptic integral",
    )
    def third_kind(
        self,
        amplitude: float,
        characteristic: float,
    ) -> float:
        """
        Calculate elliptic integral of the third kind Π(n; φ, k).

        Art. 698: The incomplete elliptic integral:

            Π(n; φ, k) = ∫₀^φ dθ / (1 + n sin² θ) sqrt(1 - k² sin² θ)

        Args:
            amplitude: Amplitude φ (radians).
            characteristic: Characteristic n.

        Returns:
            Π(n; φ, k) value.

        Reference:
            Part IV, Art. 698: Third kind elliptic integral.
        """
        k = self.modulus

        def integrand(theta):
            denom1 = 1 + characteristic * np.sin(theta) ** 2
            denom2 = np.sqrt(1 - k**2 * np.sin(theta) ** 2)
            denom = denom1 * denom2
            return 1.0 / denom if denom > 1e-15 else 1e15

        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = trapezoid([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        699,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate Jacobian elliptic functions",
    )
    def jacobian_functions(self, u: float) -> Tuple[float, float, float]:
        """
        Calculate Jacobian elliptic functions sn, cn, dn.

        Art. 699: Jacobian elliptic functions are inverses of
        elliptic integrals:

            u = F(φ, k) → sn(u, k) = sin φ
                         cn(u, k) = cos φ
                         dn(u, k) = sqrt(1 - k² sin² φ)

        Args:
            u: Argument (the value of the elliptic integral).

        Returns:
            Tuple (sn, cn, dn).

        Reference:
            Part IV, Art. 699: Jacobian elliptic functions.
        """
        k = self.modulus

        # Use scipy's ellipj which returns (sn, cn, dn, ph)
        sn, cn, dn, ph = ellipj(u, k**2)

        return (float(sn), float(cn), float(dn))

    @maxwell_cite(
        700,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate Landen transformation",
    )
    def landen_transformation(self) -> Tuple[float, float]:
        """
        Calculate Landen transformation for modulus.

        Art. 700: The Landen transformation relates elliptic
        integrals with different moduli:

            k₁ = (1 - k') / (1 + k')

        where k' = sqrt(1 - k²) is the complementary modulus.

        Args:
            None (uses self.modulus).

        Returns:
            Tuple (k₁, K₁) of new modulus and integral.

        Reference:
            Part IV, Art. 700: Landen transformation.
        """
        k = self.modulus
        k_prime = np.sqrt(1 - k**2)  # Complementary modulus

        # Descending Landen transformation
        k1 = (1 - k_prime) / (1 + k_prime) if (1 + k_prime) > 0 else 0

        # The complete integral transforms as:
        # K(k) = (1 + k₁) K(k₁)
        K1 = float(ellipk(k1**2)) if k1 > 0 else np.pi / 2

        return (k1, K1)

    @maxwell_cite(
        701,
        part=4,
        chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate complementary modulus",
    )
    def complementary_modulus(self) -> float:
        """
        Calculate the complementary modulus k'.

        Art. 701: The complementary modulus:

            k' = sqrt(1 - k²)

        Args:
            None (uses self.modulus).

        Returns:
            Complementary modulus k'.

        Reference:
            Part IV, Art. 701: Complementary modulus.
        """
        k = self.modulus
        return np.sqrt(1 - k**2)

    def parameter(self) -> float:
        """
        Calculate the parameter m = k².

        Bare convention helper (defect D-39 remediation): the m = k²
        parameter convention itself is carried — with its Art. 702
        citation — by ``calc_complete_elliptic_k_parameter`` and
        ``calc_complete_elliptic_e_parameter`` below.  This trivial
        accessor deliberately cites no article so that it cannot
        hijack Art. 702 coverage.

        Returns:
            Parameter m.
        """
        return self.modulus**2


# ── Hardened complete integrals, parameter convention m = k² ──────────────
#
# K(m), E(m) on the FULL real domain m < 1, including negative parameter
# (imaginary modulus).  Primary algorithm: arithmetic-geometric mean
# (DLMF §19.8; Gauss), i.e. the quadratically convergent form of the
# descending Landen iteration of Treatise Arts. 700-701.  For m < 0 the
# imaginary-modulus transformation (DLMF §19.7) maps into (0, 1):
#
#     K(m) = K(m₁) / sqrt(1 - m),      E(m) = sqrt(1 - m) · E(m₁),
#     m₁ = m / (m - 1) ∈ (0, 1)        (m < 0).
#
# This is a pure-Python port of the AGM kernel in maxwell/jax/_elliptic.py
# (deliberately no JAX import in non-JAX code).  Verified against the
# Carlson-form values of scipy.special.ellipk/ellipe at ~1e-15 relative
# for m ∈ [-10, 1 - 1e-15] (see tests/test_articles_math_spine_691_706.py).


def _elliptic_agm_k_e(m: float) -> tuple[float, float]:
    """(K(m), E(m)) for 0 ≤ m < 1 by the arithmetic-geometric mean.

    DLMF §19.8(i).  With a₀ = 1, b₀ = sqrt(1 - m), c₀ = sqrt(m):

        K(m) = π / (2 M),   M = AGM(1, sqrt(1 - m)) = lim aₙ,
        E(m) = K(m) · (1 − Σₙ₌₀^∞ 2ⁿ⁻¹ cₙ²)

    where aₙ₊₁ = (aₙ + bₙ)/2, bₙ₊₁ = sqrt(aₙ bₙ), cₙ₊₁ = (aₙ − bₙ)/2.
    Convergence is quadratic: ≤ 7 iterations give full double precision
    for every 0 ≤ m < 1 (more only absurdly close to m = 1).

    Args:
        m: Parameter m = k² with 0 ≤ m < 1.

    Returns:
        Tuple (K(m), E(m)).
    """
    if m == 0.0:
        half_pi = float(np.pi / 2.0)
        return half_pi, half_pi
    a = 1.0
    b = float(np.sqrt(1.0 - m))
    # n = 0 term of the E-sum: 2^{-1} c₀² with c₀² = m.  (The public
    # wrappers map m < 0 into (0, 1) before calling this helper, so here
    # 0 ≤ m < 1 and the sum is non-negative.)
    s_sum = 0.5 * m
    eps = float(np.finfo(float).eps)
    for n in range(1, 64):
        a_next = 0.5 * (a + b)
        c = 0.5 * (a - b)
        b = float(np.sqrt(a * b))
        a = a_next
        # Terminate the moment c is indistinguishable from 0 at double
        # precision.  Do NOT keep summing after this point: the computed c
        # stalls at ~ulp(a) (rounding noise) while the weight 2^{n-1}
        # keeps doubling, which would pollute the sum.  Every genuine
        # remaining term is below the rounding level of s_sum because the
        # true c_n decays quadratically.
        if abs(c) <= 4.0 * eps * a:
            break
        s_sum += 2.0 ** (n - 1) * c * c
    K = float(np.pi / (2.0 * a))
    E = K * (1.0 - s_sum)
    return K, E


def _imaginary_modulus_map(m: float) -> float:
    """Map a negative parameter m < 0 to m₁ = m/(m−1) ∈ (0, 1).

    DLMF §19.7 (imaginary-modulus transformation): the complete
    integrals at imaginary modulus k = i·κ (parameter m = −κ²) reduce
    to complete integrals at the real parameter m₁ = m/(m − 1).
    """
    return m / (m - 1.0)


@maxwell_cite(
    696,
    702,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Hardened complete K(m), parameter convention, all m < 1",
)
def calc_complete_elliptic_k_parameter(m: float) -> float:
    """Complete elliptic integral of the first kind K(m), parameter m = k².

    Art. 696 (definition) and Art. 702 (parameter convention):

        K(m) = ∫₀^(π/2) dθ / sqrt(1 − m sin²θ),   m < 1.

    Valid on the full real domain m ∈ (−∞, 1), INCLUDING negative m:
      * m ≥ 0: arithmetic-geometric mean, K = π / (2·AGM(1, √(1−m)))
        (DLMF §19.8);
      * m < 0: imaginary-modulus transformation (DLMF §19.7)
        K(m) = K(m/(m−1)) / √(1−m).
    Special values: K(0) = π/2; K(m) → +∞ logarithmically as m → 1⁻.

    Accuracy: ~1e-15 relative across the whole domain (AGM converges
    quadratically; cross-checked against scipy's Carlson-form values).

    Args:
        m: Parameter m = k² (any real m < 1).

    Returns:
        K(m) value (float; math.inf at m = 1).

    Raises:
        ValueError: If m ≥ 1 (K is complex/undefined on the real axis,
            except for the logarithmic divergence returned at m = 1).
    """
    if m > 1.0:
        raise ValueError(f"Parameter m must be < 1 for real K(m), got {m}")
    if m == 1.0:
        return float("inf")
    if m < 0.0:
        m1 = _imaginary_modulus_map(m)
        K1, _ = _elliptic_agm_k_e(m1)
        return K1 / float(np.sqrt(1.0 - m))
    K, _ = _elliptic_agm_k_e(m)
    return K


@maxwell_cite(
    697,
    702,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Hardened complete E(m), parameter convention, all m < 1",
)
def calc_complete_elliptic_e_parameter(m: float) -> float:
    """Complete elliptic integral of the second kind E(m), parameter m = k².

    Art. 697 (definition) and Art. 702 (parameter convention):

        E(m) = ∫₀^(π/2) sqrt(1 − m sin²θ) dθ,   m < 1.

    Valid on the full real domain m ∈ (−∞, 1), INCLUDING negative m:
      * m ≥ 0: AGM evaluation E = K·(1 − Σ 2ⁿ⁻¹cₙ²) (DLMF §19.8(i));
      * m < 0: imaginary-modulus transformation (DLMF §19.7)
        E(m) = √(1−m) · E(m/(m−1)).
    Special values: E(0) = π/2; E(1) = 1.

    Accuracy: ~1e-15 relative across the whole domain.

    Args:
        m: Parameter m = k² (any real m < 1).

    Returns:
        E(m) value (float).

    Raises:
        ValueError: If m > 1 (E is complex on the real axis there).
    """
    if m > 1.0:
        raise ValueError(f"Parameter m must be ≤ 1 for real E(m), got {m}")
    if m == 1.0:
        return 1.0
    if m < 0.0:
        m1 = _imaginary_modulus_map(m)
        _, E1 = _elliptic_agm_k_e(m1)
        return float(np.sqrt(1.0 - m)) * E1
    _, E = _elliptic_agm_k_e(m)
    return E


@maxwell_cite(
    696,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate complete elliptic integral of first kind K(k)",
)
def calc_complete_elliptic_integral_first_kind(modulus: float) -> float:
    """
    Calculate complete elliptic integral of the first kind.

    Art. 696: K(k) = ∫₀^(π/2) dθ / sqrt(1 - k² sin² θ)

    Delegates to the hardened parameter-convention evaluator
    ``calc_complete_elliptic_k_parameter(k²)`` (AGM; DLMF §19.8), so the
    value is exact to double precision right up to k → 1.

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).

    Returns:
        K(k) value (math.inf at k = 1).

    Reference:
        Part IV, Art. 696: Complete first kind integral.

    Example:
        >>> K = calc_complete_elliptic_integral_first_kind(0.5)
        >>> print(f"K(0.5) = {K:.4f}")
    """
    if not 0 <= modulus <= 1:
        raise ValueError(f"Modulus must be in [0, 1]")
    return calc_complete_elliptic_k_parameter(modulus**2)


@maxwell_cite(
    697,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate complete elliptic integral of second kind E(k)",
)
def calc_complete_elliptic_integral_second_kind(modulus: float) -> float:
    """
    Calculate complete elliptic integral of the second kind.

    Art. 697: E(k) = ∫₀^(π/2) sqrt(1 - k² sin² θ) dθ

    Delegates to the hardened parameter-convention evaluator
    ``calc_complete_elliptic_e_parameter(k²)`` (AGM; DLMF §19.8(i)).

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).

    Returns:
        E(k) value.

    Reference:
        Part IV, Art. 697: Complete second kind integral.
    """
    if not 0 <= modulus <= 1:
        raise ValueError(f"Modulus must be in [0, 1]")
    return calc_complete_elliptic_e_parameter(modulus**2)


@maxwell_cite(
    696,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate incomplete elliptic integral of first kind",
)
def calc_elliptic_integral_first_kind(modulus: float, amplitude: float) -> float:
    """
    Calculate incomplete elliptic integral of the first kind.

    Art. 696: F(φ, k) = ∫₀^φ dθ / sqrt(1 - k² sin² θ)

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).
        amplitude: Amplitude φ (radians).

    Returns:
        F(φ, k) value.

    Reference:
        Part IV, Art. 696: Incomplete first kind integral.
    """
    ei = EllipticIntegral(modulus=modulus)
    return ei.first_kind(amplitude)


@maxwell_cite(
    697,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate incomplete elliptic integral of second kind",
)
def calc_elliptic_integral_second_kind(modulus: float, amplitude: float) -> float:
    """
    Calculate incomplete elliptic integral of the second kind.

    Art. 697: E(φ, k) = ∫₀^φ sqrt(1 - k² sin² θ) dθ

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).
        amplitude: Amplitude φ (radians).

    Returns:
        E(φ, k) value.

    Reference:
        Part IV, Art. 697: Incomplete second kind integral.
    """
    ei = EllipticIntegral(modulus=modulus)
    return ei.second_kind(amplitude)


@maxwell_cite(
    698,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate elliptic integral of third kind",
)
def calc_elliptic_integral_third_kind(
    modulus: float,
    amplitude: float,
    characteristic: float,
) -> float:
    """
    Calculate elliptic integral of the third kind.

    Art. 698: Π(n; φ, k) = ∫₀^φ dθ / (1 + n sin² θ) sqrt(1 - k² sin² θ)

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).
        amplitude: Amplitude φ (radians).
        characteristic: Characteristic n.

    Returns:
        Π(n; φ, k) value.

    Reference:
        Part IV, Art. 698: Third kind elliptic integral.
    """
    ei = EllipticIntegral(modulus=modulus)
    return ei.third_kind(amplitude, characteristic)


@maxwell_cite(
    696,
    697,
    698,
    699,
    700,
    701,
    702,
    703,
    704,
    705,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Verify elliptic integral relations",
)
def verify_elliptic_integrals(
    modulus: float = 0.5,
    tolerance: float = 1e-8,
) -> dict[str, float | bool]:
    """
    Verify elliptic integral relations.

    Art. 696-705: This function verifies:
    1. K(k) and E(k) values
    2. Legendre relation: E K' + E' K - K K' = π/2
    3. Jacobian function identities
    4. Limiting cases k → 0 and k → 1

    Args:
        modulus: Modulus k to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 696-705: Elliptic integral verification.
    """
    ei = EllipticIntegral(modulus=modulus)
    k = modulus

    # Complete integrals
    K = ei.first_kind(np.pi / 2)
    E = ei.second_kind(np.pi / 2)

    # Complementary modulus and integrals
    k_prime = ei.complementary_modulus()
    ei_prime = EllipticIntegral(modulus=k_prime)
    K_prime = ei_prime.first_kind(np.pi / 2)
    E_prime = ei_prime.second_kind(np.pi / 2)

    # Legendre relation: E K' + E' K - K K' = π/2
    legendre_lhs = E * K_prime + E_prime * K - K * K_prime
    legendre_error = abs(legendre_lhs - np.pi / 2) / (np.pi / 2)

    # Jacobian identity: sn² + cn² = 1
    u_test = 1.0
    sn, cn, dn = ei.jacobian_functions(u_test)
    jacobi_error = abs(sn**2 + cn**2 - 1.0)

    # dn² + k² sn² = 1
    dn_error = abs(dn**2 + k**2 * sn**2 - 1.0)

    # Limiting case: K(0) = π/2
    ei_zero = EllipticIntegral(modulus=0.0)
    K_zero = ei_zero.first_kind(np.pi / 2)
    K_zero_error = abs(K_zero - np.pi / 2) / (np.pi / 2)

    # Limiting case: E(0) = π/2
    E_zero = ei_zero.second_kind(np.pi / 2)
    E_zero_error = abs(E_zero - np.pi / 2) / (np.pi / 2)

    return {
        "modulus_k": k,
        "complementary_modulus": k_prime,
        "K_complete": K,
        "E_complete": E,
        "K_prime": K_prime,
        "E_prime": E_prime,
        "legendre_relation_LHS": legendre_lhs,
        "legendre_expected": np.pi / 2,
        "legendre_error": legendre_error,
        "sn_at_1": sn,
        "cn_at_1": cn,
        "dn_at_1": dn,
        "jacobi_identity_error": jacobi_error,
        "dn_identity_error": dn_error,
        "K_zero_limit": K_zero,
        "K_zero_error": K_zero_error,
        "E_zero_limit": E_zero,
        "E_zero_error": E_zero_error,
        "verified": legendre_error < tolerance and jacobi_error < tolerance,
    }


@maxwell_cite(
    696,
    697,
    698,
    699,
    700,
    701,
    702,
    703,
    704,
    705,
    part=4,
    chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Complete elliptic integral analysis",
)
def analyze_elliptic_integrals(
    modulus_range: tuple = (0.0, 0.9, 5),
) -> dict[str, float | list]:
    """
    Complete analysis of elliptic integrals.

    Art. 696-705: Comprehensive analysis including:
    1. K(k) and E(k) vs modulus
    2. Complementary integrals
    3. Jacobian function values
    4. Landen transformation effects

    Args:
        modulus_range: (k_min, k_max, n_points) tuple.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 696-705: Complete elliptic integral analysis.
    """
    k_min, k_max, n_points = modulus_range
    k_values = np.linspace(k_min, k_max, n_points)

    K_values = []
    E_values = []
    K_prime_values = []
    E_prime_values = []

    for k in k_values:
        ei = EllipticIntegral(modulus=k)
        K_values.append(ei.first_kind(np.pi / 2))
        E_values.append(ei.second_kind(np.pi / 2))

        k_prime = ei.complementary_modulus()
        ei_prime = EllipticIntegral(modulus=k_prime)
        K_prime_values.append(ei_prime.first_kind(np.pi / 2))
        E_prime_values.append(ei_prime.second_kind(np.pi / 2))

    # Landen transformation for mid-point
    k_mid = (k_min + k_max) / 2
    ei_mid = EllipticIntegral(modulus=k_mid)
    k1, K1 = ei_mid.landen_transformation()

    # Jacobian functions at representative point
    u_test = 1.0
    sn, cn, dn = ei_mid.jacobian_functions(u_test)

    return {
        "modulus_range": list(k_values),
        "K_values": K_values,
        "E_values": E_values,
        "K_prime_values": K_prime_values,
        "E_prime_values": E_prime_values,
        "K_diverges_as_k->1": K_values[-1] if k_max < 1 else float("inf"),
        "E_approaches_1_as_k->1": E_values[-1] if k_max < 1 else 1.0,
        "landen_k_original": k_mid,
        "landen_k_transformed": k1,
        "landen_K_transformed": K1,
        "jacobian_sn_at_1": sn,
        "jacobian_cn_at_1": cn,
        "jacobian_dn_at_1": dn,
        "CGS_units": "Dimensionless integrals and functions",
    }
