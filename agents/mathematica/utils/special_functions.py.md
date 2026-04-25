# Utility: Special Functions Helper

## Description

Utility for computing special functions used throughout Maxwell's Treatise: Legendre polynomials, Bessel functions, elliptic integrals, etc.

## Purpose

Provide a unified interface to SciPy's special functions with CGS unit conventions and Maxwell article citations.

## Implementation

```python
"""
Special Functions Helper for Maxwell's Treatise

Provides Legendre polynomials, Bessel functions, elliptic integrals,
and other special functions used throughout the Treatise.

Maxwell Articles: 125-133 (spherical harmonics), 261-270 (Bessel)
"""

import numpy as np
from scipy import special
from typing import Tuple, Union
from maxwell.core.citation import cite_article


@cite_article([125, 126, 127, 128, 129, 130, 131, 132, 133])
class LegendreFunctions:
    """
    Legendre polynomials and associated Legendre functions.
    
    Used for spherical harmonic expansions in electrostatics
    and magnetostatics.
    """
    
    @staticmethod
    def P(n: int, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Legendre polynomial P_n(x).
        
        Parameters
        ----------
        n : int
            Degree (n >= 0)
        x : float or np.ndarray
            Argument (typically cos θ, so -1 <= x <= 1)
        
        Returns
        -------
        P_n : float or np.ndarray
            Value of Legendre polynomial
        
        Examples
        --------
        >>> LegendreFunctions.P(0, x)  # P_0(x) = 1
        >>> LegendreFunctions.P(1, x)  # P_1(x) = x
        >>> LegendreFunctions.P(2, x)  # P_2(x) = (3x² - 1)/2
        """
        return special.legendre(n)(x)
    
    @staticmethod
    def Pn_array(n_max: int, x: Union[float, np.ndarray]) -> np.ndarray:
        """
        Compute all Legendre polynomials P_0 to P_n at x.
        
        Returns
        -------
        P : np.ndarray
            Array of P_0(x), P_1(x), ..., P_n(x)
        """
        return special.lpmn(0, n_max, x)[0][0, :]
    
    @staticmethod
    def P_associated(
        n: int,
        m: int,
        x: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Associated Legendre function P_n^m(x).
        
        Parameters
        ----------
        n : int
            Degree (n >= 0)
        m : int
            Order (|m| <= n)
        x : float or np.ndarray
            Argument (-1 <= x <= 1)
        
        Returns
        -------
        P_n^m : float or np.ndarray
            Associated Legendre function value
        
        Notes
        -----
        Uses Condon-Shortley phase convention.
        """
        if abs(m) > n:
            return np.zeros_like(x) if hasattr(x, '__len__') else 0.0
        
        # special.lpmn returns array for all m up to m_max
        Pnm, _ = special.lpmn(n, n, x)
        return Pnm[m, n]
    
    @staticmethod
    def Pnm_array(
        n_max: int,
        m_max: int,
        x: Union[float, np.ndarray]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute associated Legendre functions up to degree n_max and order m_max.
        
        Returns
        -------
        Pnm : np.ndarray
            Pnm[m, n] for 0 <= m <= m_max, 0 <= n <= n_max
        dPnm : np.ndarray
            Derivatives dPnm[m, n]/dx
        """
        return special.lpmn(m_max, n_max, x)
    
    @staticmethod
    def Y_lm(
        l: int,
        m: int,
        theta: Union[float, np.ndarray],
        phi: Union[float, np.ndarray]
    ) -> Union[complex, np.ndarray]:
        """
        Spherical harmonic Y_l^m(θ, φ).
        
        Parameters
        ----------
        l : int
            Degree (l >= 0)
        m : int
            Order (|m| <= l)
        theta : float or np.ndarray
            Polar angle (0 <= θ <= π)
        phi : float or np.ndarray
            Azimuthal angle (-π <= φ <= π)
        
        Returns
        -------
        Y_l^m : complex
            Spherical harmonic value
        
        Notes
        -----
        Normalization: ∫|Y_l^m|² dΩ = 1
        Includes Condon-Shortley phase.
        """
        return special.sph_harm(m, l, phi, theta)  # Note: phi, theta order
    
    @staticmethod
    def addition_theorem(
        n: int,
        gamma: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Legendre addition theorem: P_n(cos γ) in terms of angles.
        
        P_n(cos γ) = P_n(cos θ)P_n(cos θ') 
                   + 2 Σ_{m=1}^n [(n-m)!/(n+m)!] P_n^m(cos θ)P_n^m(cos θ') cos(m(φ-φ'))
        
        Parameters
        ----------
        n : int
            Degree
        gamma : float or np.ndarray
            Angle between two directions
        
        Returns
        -------
        P_n(cos γ) : float or np.ndarray
        """
        return LegendreFunctions.P(n, np.cos(gamma))


@cite_article([261, 262, 263, 264, 265, 266, 267, 268, 269, 270])
class BesselFunctions:
    """
    Bessel functions for cylindrical problems.
    
    Used for problems with cylindrical symmetry,
    particularly in electromagnetic wave theory.
    """
    
    @staticmethod
    def J(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Bessel function of the first kind J_n(x).
        
        Parameters
        ----------
        n : float or int
            Order (can be non-integer)
        x : float or np.ndarray
            Argument (x >= 0)
        
        Returns
        -------
        J_n : float or np.ndarray
            Bessel function value
        """
        return special.jv(n, x)
    
    @staticmethod
    def Y(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Bessel function of the second kind Y_n(x) (Neumann function).
        
        Parameters
        ----------
        n : float or int
            Order
        x : float or np.ndarray
            Argument (x > 0)
        
        Returns
        -------
        Y_n : float or np.ndarray
            Bessel function of second kind
        
        Notes
        -----
        Singular at x = 0.
        """
        return special.yv(n, x)
    
    @staticmethod
    def H1(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[complex, np.ndarray]:
        """
        Hankel function of the first kind H_n^(1)(x) = J_n(x) + iY_n(x).
        
        Used for outgoing cylindrical waves.
        """
        return special.hankel1(n, x)
    
    @staticmethod
    def H2(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[complex, np.ndarray]:
        """
        Hankel function of the second kind H_n^(2)(x) = J_n(x) - iY_n(x).
        
        Used for incoming cylindrical waves.
        """
        return special.hankel2(n, x)
    
    @staticmethod
    def I(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Modified Bessel function of the first kind I_n(x).
        
        Used for problems with exponential behavior.
        """
        return special.iv(n, x)
    
    @staticmethod
    def K(n: Union[float, int], x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Modified Bessel function of the second kind K_n(x).
        
        Singular at x = 0.
        """
        return special.kv(n, x)
    
    @staticmethod
    def zeros_J(n: int, count: int = 1) -> np.ndarray:
        """
        Compute zeros of J_n(x).
        
        Parameters
        ----------
        n : int
            Order
        count : int
            Number of zeros to return
        
        Returns
        -------
        zeros : np.ndarray
            First 'count' positive zeros of J_n(x)
        """
        return special.jn_zeros(n, count)


@cite_article([413, 414, 415, 416, 417])
class EllipticIntegrals:
    """
    Elliptic integrals for magnetic field calculations.
    
    Used for off-axis field of current loops and disks.
    """
    
    @staticmethod
    def K(k: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Complete elliptic integral of the first kind K(k).
        
        K(k) = ∫_0^(π/2) dθ / √(1 - k² sin²θ)
        
        Parameters
        ----------
        k : float or np.ndarray
            Modulus (0 <= k <= 1)
        
        Returns
        -------
        K : float or np.ndarray
            Complete elliptic integral of first kind
        """
        return special.ellipk(k**2)  # SciPy uses m = k²
    
    @staticmethod
    def E(k: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Complete elliptic integral of the second kind E(k).
        
        E(k) = ∫_0^(π/2) √(1 - k² sin²θ) dθ
        
        Parameters
        ----------
        k : float or np.ndarray
            Modulus (0 <= k <= 1)
        
        Returns
        -------
        E : float or np.ndarray
            Complete elliptic integral of second kind
        """
        return special.ellipe(k**2)
    
    @staticmethod
    def F(phi: Union[float, np.ndarray], k: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Incomplete elliptic integral of the first kind F(φ, k).
        
        F(φ, k) = ∫_0^φ dθ / √(1 - k² sin²θ)
        """
        return special.ellipkinc(phi, k**2)
    
    @staticmethod
    def E_incomplete(phi: Union[float, np.ndarray], k: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Incomplete elliptic integral of the second kind E(φ, k).
        
        E(φ, k) = ∫_0^φ √(1 - k² sin²θ) dθ
        """
        return special.ellipeinc(phi, k**2)


# === Convenience Functions ===

@cite_article([125, 126, 127])
def legendre_expansion_coefficients(
    f: callable,
    n_max: int,
    n_points: int = 100
) -> np.ndarray:
    """
    Compute Legendre expansion coefficients for a function.
    
    f(x) = Σ a_n P_n(x)
    
    a_n = (2n+1)/2 ∫_{-1}^{1} f(x) P_n(x) dx
    
    Parameters
    ----------
    f : callable
        Function to expand, f(x)
    n_max : int
        Maximum degree
    n_points : int
        Number of quadrature points
    
    Returns
    -------
    a : np.ndarray
        Expansion coefficients a_0, a_1, ..., a_{n_max}
    """
    from scipy.integrate import quad
    
    coefficients = []
    for n in range(n_max + 1):
        integrand = lambda x: f(x) * LegendreFunctions.P(n, x)
        integral, _ = quad(integrand, -1, 1)
        a_n = (2 * n + 1) / 2 * integral
        coefficients.append(a_n)
    
    return np.array(coefficients)
```

## Usage Examples

```python
from maxwell.mathematics.special import LegendreFunctions, BesselFunctions

# Legendre polynomials
P2 = LegendreFunctions.P(2, x=0.5)
P_all = LegendreFunctions.Pn_array(5, x=np.linspace(-1, 1, 100))

# Spherical harmonics
Y_2_1 = LegendreFunctions.Y_lm(l=2, m=1, theta=np.pi/3, phi=np.pi/4)

# Bessel function zeros
J1_zeros = BesselFunctions.zeros_J(n=1, count=5)
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 125-133 | Spherical harmonics, Legendre polynomials |
| 261-270 | Bessel functions for cylindrical conductors |
| 413-417 | Elliptic integrals for magnetic shells |
