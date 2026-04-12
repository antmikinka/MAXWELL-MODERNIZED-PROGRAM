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

Category: A (maxwell_original) — Maxwell's elliptic integral methods.

References:
    Part IV, Arts. 696-705: Elliptic integrals in electromagnetism.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.special import ellipk, ellipe, ellipj

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


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
        part=4, chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate first kind elliptic integral",
    )
    def first_kind(self, amplitude: float = np.pi/2) -> float:
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
            # Complete elliptic integral
            return float(ellipk(k ** 2))

        # Incomplete integral via numerical integration
        def integrand(theta):
            denom = np.sqrt(1 - k ** 2 * np.sin(theta) ** 2)
            return 1.0 / denom if denom > 1e-15 else 1e15

        # Numerical integration using Simpson's rule
        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = np.trapz([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        697,
        part=4, chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate second kind elliptic integral",
    )
    def second_kind(self, amplitude: float = np.pi/2) -> float:
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
            # Complete elliptic integral
            return float(ellipe(k ** 2))

        # Incomplete integral via numerical integration
        def integrand(theta):
            return np.sqrt(1 - k ** 2 * np.sin(theta) ** 2)

        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = np.trapz([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        698,
        part=4, chapter="Elliptic Integrals",
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
            denom2 = np.sqrt(1 - k ** 2 * np.sin(theta) ** 2)
            denom = denom1 * denom2
            return 1.0 / denom if denom > 1e-15 else 1e15

        n_points = 100
        theta_vals = np.linspace(0, amplitude, n_points)
        integral = np.trapz([integrand(t) for t in theta_vals], theta_vals)

        return integral

    @maxwell_cite(
        699,
        part=4, chapter="Elliptic Integrals",
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
        sn, cn, dn, ph = ellipj(u, k ** 2)

        return (float(sn), float(cn), float(dn))

    @maxwell_cite(
        700,
        part=4, chapter="Elliptic Integrals",
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
        k_prime = np.sqrt(1 - k ** 2)  # Complementary modulus

        # Descending Landen transformation
        k1 = (1 - k_prime) / (1 + k_prime) if (1 + k_prime) > 0 else 0

        # The complete integral transforms as:
        # K(k) = (1 + k₁) K(k₁)
        K1 = float(ellipk(k1 ** 2)) if k1 > 0 else np.pi / 2

        return (k1, K1)

    @maxwell_cite(
        701,
        part=4, chapter="Elliptic Integrals",
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
        return np.sqrt(1 - k ** 2)

    @maxwell_cite(
        702,
        part=4, chapter="Elliptic Integrals",
        theory_class="maxwell_original",
        description="Calculate parameter m = k²",
    )
    def parameter(self) -> float:
        """
        Calculate the parameter m = k².

        Art. 702: Many formulas use m = k² instead of k directly.

        Returns:
            Parameter m.

        Reference:
            Part IV, Art. 702: Parameter definition.
        """
        return self.modulus ** 2


@maxwell_cite(
    696,
    part=4, chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate complete elliptic integral of first kind K(k)",
)
def calc_complete_elliptic_integral_first_kind(modulus: float) -> float:
    """
    Calculate complete elliptic integral of the first kind.

    Art. 696: K(k) = ∫₀^(π/2) dθ / sqrt(1 - k² sin² θ)

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).

    Returns:
        K(k) value.

    Reference:
        Part IV, Art. 696: Complete first kind integral.

    Example:
        >>> K = calc_complete_elliptic_integral_first_kind(0.5)
        >>> print(f"K(0.5) = {K:.4f}")
    """
    if not 0 <= modulus <= 1:
        raise ValueError(f"Modulus must be in [0, 1]")
    return float(ellipk(modulus ** 2))


@maxwell_cite(
    697,
    part=4, chapter="Elliptic Integrals",
    theory_class="maxwell_original",
    description="Calculate complete elliptic integral of second kind E(k)",
)
def calc_complete_elliptic_integral_second_kind(modulus: float) -> float:
    """
    Calculate complete elliptic integral of the second kind.

    Art. 697: E(k) = ∫₀^(π/2) sqrt(1 - k² sin² θ) dθ

    Args:
        modulus: Modulus k (0 ≤ k ≤ 1).

    Returns:
        E(k) value.

    Reference:
        Part IV, Art. 697: Complete second kind integral.
    """
    if not 0 <= modulus <= 1:
        raise ValueError(f"Modulus must be in [0, 1]")
    return float(ellipe(modulus ** 2))


@maxwell_cite(
    696,
    part=4, chapter="Elliptic Integrals",
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
    part=4, chapter="Elliptic Integrals",
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
    part=4, chapter="Elliptic Integrals",
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
    696, 697, 698, 699, 700, 701, 702, 703, 704, 705,
    part=4, chapter="Elliptic Integrals",
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
    K = ei.first_kind(np.pi/2)
    E = ei.second_kind(np.pi/2)

    # Complementary modulus and integrals
    k_prime = ei.complementary_modulus()
    ei_prime = EllipticIntegral(modulus=k_prime)
    K_prime = ei_prime.first_kind(np.pi/2)
    E_prime = ei_prime.second_kind(np.pi/2)

    # Legendre relation: E K' + E' K - K K' = π/2
    legendre_lhs = E * K_prime + E_prime * K - K * K_prime
    legendre_error = abs(legendre_lhs - np.pi / 2) / (np.pi / 2)

    # Jacobian identity: sn² + cn² = 1
    u_test = 1.0
    sn, cn, dn = ei.jacobian_functions(u_test)
    jacobi_error = abs(sn ** 2 + cn ** 2 - 1.0)

    # dn² + k² sn² = 1
    dn_error = abs(dn ** 2 + k ** 2 * sn ** 2 - 1.0)

    # Limiting case: K(0) = π/2
    ei_zero = EllipticIntegral(modulus=0.0)
    K_zero = ei_zero.first_kind(np.pi/2)
    K_zero_error = abs(K_zero - np.pi / 2) / (np.pi / 2)

    # Limiting case: E(0) = π/2
    E_zero = ei_zero.second_kind(np.pi/2)
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
    696, 697, 698, 699, 700, 701, 702, 703, 704, 705,
    part=4, chapter="Elliptic Integrals",
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
        K_values.append(ei.first_kind(np.pi/2))
        E_values.append(ei.second_kind(np.pi/2))

        k_prime = ei.complementary_modulus()
        ei_prime = EllipticIntegral(modulus=k_prime)
        K_prime_values.append(ei_prime.first_kind(np.pi/2))
        E_prime_values.append(ei_prime.second_kind(np.pi/2))

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
        "K_diverges_as_k->1": K_values[-1] if k_max < 1 else float('inf'),
        "E_approaches_1_as_k->1": E_values[-1] if k_max < 1 else 1.0,
        "landen_k_original": k_mid,
        "landen_k_transformed": k1,
        "landen_K_transformed": K1,
        "jacobian_sn_at_1": sn,
        "jacobian_cn_at_1": cn,
        "jacobian_dn_at_1": dn,
        "CGS_units": "Dimensionless integrals and functions",
    }
