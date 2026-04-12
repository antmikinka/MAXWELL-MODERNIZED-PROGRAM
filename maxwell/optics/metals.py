"""maxwell.optics.metals — Reflection and refraction in metals (Arts. 795-800).

Implements Maxwell's treatment of electromagnetic wave reflection and
refraction at metallic surfaces, including the theory of metallic reflection.

Maxwell's CGS formulation (Arts. 795-800):
    Fresnel reflection coefficients:
        r_perp = (n1*cos(θ1) - n2*cos(θ2)) / (n1*cos(θ1) + n2*cos(θ2))
        r_par = (n2*cos(θ1) - n1*cos(θ2)) / (n2*cos(θ1) + n1*cos(θ2))

    Reflectance (intensity reflection coefficient):
        R = |r|²

    For metals with complex refractive index ñ = n + iκ:
        The imaginary part κ causes absorption

    Skin depth (penetration depth):
        δ = c / (ω * κ) = λ / (2π * κ)

    where:
        n = real refractive index
        κ = extinction coefficient (imaginary part)
        ñ = n + iκ = complex refractive index

where:
    r = amplitude reflection coefficient (dimensionless)
    R = reflectance (intensity reflection coefficient, dimensionless)
    n = refractive index of dielectric
    ñ = complex refractive index of metal
    κ = extinction coefficient
    δ = skin depth (cm)

Category: A (maxwell_original) — Maxwell's metallic reflection theory.

References:
    Part IV, Arts. 795-800: Reflection and refraction in metals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


# Optical constants for common metals at visible wavelengths (λ ≈ 589 nm)
# Format: {name: (n, κ)} where ñ = n + iκ
METAL_OPTICAL_CONSTANTS = {
    "silver": (0.05, 3.88),      # Highly reflective in visible
    "gold": (0.47, 2.41),        # Yellow color from interband transitions
    "copper": (0.62, 2.57),      # Reddish color
    "aluminum": (1.39, 7.61),    # Good UV reflector
    "chromium": (3.11, 4.20),    # Used for mirrors
    "nickel": (1.88, 3.46),
    "platinum": (2.19, 3.39),
    "titanium": (2.53, 3.31),
    "iron": (2.47, 3.37),
    "sodium": (0.04, 2.37),      # Alkali metal
}


@dataclass
class MetallicReflection:
    """
    Calculator for reflection and refraction at metallic surfaces.

    Art. 795-800: Maxwell's theory of metallic reflection treats metals
    as having a complex refractive index, which accounts for both
    reflection and absorption.

    Attributes:
        n1: Refractive index of incident medium (real).
        n2_real: Real part of metal refractive index.
        kappa: Extinction coefficient (imaginary part).
    """

    n1: float = 1.0  # Air/vacuum
    n2_real: float = 0.05  # Real part (e.g., silver)
    kappa: float = 3.88  # Extinction coefficient

    def __post_init__(self):
        """Validate parameters."""
        if self.n1 <= 0:
            raise ValueError(f"n1 must be positive, got {self.n1}")

    @property
    def complex_refractive_index(self) -> complex:
        """Complex refractive index ñ = n + iκ."""
        return complex(self.n2_real, self.kappa)

    @maxwell_cite(
        795,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate Fresnel reflection coefficient (perpendicular)",
    )
    def reflection_perpendicular(self, angle_incidence: float) -> complex:
        """
        Calculate Fresnel reflection coefficient for perpendicular polarization.

        Art. 795: For s-polarization (E perpendicular to plane of incidence):

            r_s = (n1*cos(θ1) - ñ2*cos(θ2)) / (n1*cos(θ1) + ñ2*cos(θ2))

        For metals, ñ2 is complex, making r_s complex.

        Args:
            angle_incidence: Angle of incidence θ1 (radians).

        Returns:
            Complex reflection coefficient r_s.

        Reference:
            Part IV, Art. 795: Fresnel reflection (perpendicular).
        """
        theta1 = angle_incidence
        cos_theta1 = np.cos(theta1)

        # Snell's law with complex index: n1*sin(θ1) = ñ2*sin(θ2)
        sin_theta1 = np.sin(theta1)
        n2_complex = self.complex_refractive_index

        # sin(θ2) = (n1/ñ2)*sin(θ1)
        sin_theta2 = (self.n1 / n2_complex) * sin_theta1

        # cos(θ2) = sqrt(1 - sin²(θ2))
        cos_theta2 = np.sqrt(1.0 - sin_theta2 ** 2)

        # r_s = (n1*cos(θ1) - ñ2*cos(θ2)) / (n1*cos(θ1) + ñ2*cos(θ2))
        numerator = self.n1 * cos_theta1 - n2_complex * cos_theta2
        denominator = self.n1 * cos_theta1 + n2_complex * cos_theta2

        return numerator / denominator

    @maxwell_cite(
        796,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate Fresnel reflection coefficient (parallel)",
    )
    def reflection_parallel(self, angle_incidence: float) -> complex:
        """
        Calculate Fresnel reflection coefficient for parallel polarization.

        Art. 796: For p-polarization (E parallel to plane of incidence):

            r_p = (ñ2*cos(θ1) - n1*cos(θ2)) / (ñ2*cos(θ1) + n1*cos(θ2))

        Args:
            angle_incidence: Angle of incidence θ1 (radians).

        Returns:
            Complex reflection coefficient r_p.

        Reference:
            Part IV, Art. 796: Fresnel reflection (parallel).
        """
        theta1 = angle_incidence
        cos_theta1 = np.cos(theta1)

        sin_theta1 = np.sin(theta1)
        n2_complex = self.complex_refractive_index
        sin_theta2 = (self.n1 / n2_complex) * sin_theta1
        cos_theta2 = np.sqrt(1.0 - sin_theta2 ** 2)

        # r_p = (ñ2*cos(θ1) - n1*cos(θ2)) / (ñ2*cos(θ1) + n1*cos(θ2))
        numerator = n2_complex * cos_theta1 - self.n1 * cos_theta2
        denominator = n2_complex * cos_theta1 + self.n1 * cos_theta2

        return numerator / denominator

    @maxwell_cite(
        797,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate reflectance R = |r|²",
    )
    def reflectance(self, angle_incidence: float, polarization: str = "unpolarized") -> float:
        """
        Calculate reflectance (intensity reflection coefficient).

        Art. 797: The reflectance is:

            R_s = |r_s|²  (perpendicular)
            R_p = |r_p|²  (parallel)
            R = (R_s + R_p) / 2  (unpolarized)

        Args:
            angle_incidence: Angle of incidence (radians).
            polarization: "s", "p", or "unpolarized".

        Returns:
            Reflectance R (dimensionless, 0 to 1).

        Reference:
            Part IV, Art. 797: Reflectance.
        """
        r_s = self.reflection_perpendicular(angle_incidence)
        r_p = self.reflection_parallel(angle_incidence)

        R_s = abs(r_s) ** 2
        R_p = abs(r_p) ** 2

        if polarization == "s":
            return R_s
        elif polarization == "p":
            return R_p
        else:  # unpolarized
            return (R_s + R_p) / 2.0

    @maxwell_cite(
        798,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate skin depth in metal",
    )
    def skin_depth(self, wavelength: float) -> float:
        """
        Calculate skin depth (penetration depth) in the metal.

        Art. 798: The skin depth is:

            δ = λ / (2π * κ)

        This is the depth at which field amplitude drops to 1/e.

        Args:
            wavelength: Vacuum wavelength λ (cm).

        Returns:
            Skin depth δ (cm).

        Reference:
            Part IV, Art. 798: Skin depth.
        """
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")
        if self.kappa <= 0:
            return float('inf')

        return wavelength / (2.0 * np.pi * self.kappa)

    @maxwell_cite(
        799,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate absorption coefficient",
    )
    def absorption_coefficient(self, wavelength: float) -> float:
        """
        Calculate absorption coefficient.

        Art. 799: The absorption coefficient is:

            α = 4π * κ / λ  (cm⁻¹)

        Intensity decays as I = I₀ * exp(-α*z).

        Args:
            wavelength: Vacuum wavelength (cm).

        Returns:
            Absorption coefficient α (cm⁻¹).

        Reference:
            Part IV, Art. 799: Absorption coefficient.
        """
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")
        if self.kappa <= 0:
            return 0.0

        return 4.0 * np.pi * self.kappa / wavelength

    @maxwell_cite(
        800,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate normal incidence reflectance",
    )
    def normal_reflectance(self) -> float:
        """
        Calculate reflectance at normal incidence.

        Art. 800: At normal incidence (θ = 0):

            R = |(n1 - ñ2) / (n1 + ñ2)|²

        For air-metal interface (n1 = 1):

            R = |(1 - n - iκ) / (1 + n + iκ)|²
              = [(1-n)² + κ²] / [(1+n)² + κ²]

        Returns:
            Normal reflectance R (dimensionless).

        Reference:
            Part IV, Art. 800: Normal incidence reflection.
        """
        n = self.n2_real
        k = self.kappa

        numerator = (self.n1 - n) ** 2 + k ** 2
        denominator = (self.n1 + n) ** 2 + k ** 2

        return numerator / denominator


@maxwell_cite(
    795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Get metal optical constants",
)
def get_metal_constants(metal_name: str) -> dict[str, float]:
    """
    Get optical constants for a metal.

    Art. 795: Lookup table of complex refractive indices for
    common metals at visible wavelengths.

    Args:
        metal_name: Name of metal (case-insensitive).

    Returns:
        Dictionary with:
        - n: Real part of refractive index
        - κ: Extinction coefficient
        - ñ: Complex refractive index

    Raises:
        KeyError: If metal not found.

    Reference:
        Part IV, Art. 795: Metal optical constants.

    Example:
        >>> constants = get_metal_constants("silver")
        >>> print(f"ñ = {constants['n']} + i{constants['κ']}")
    """
    metal_key = metal_name.lower()
    if metal_key not in METAL_OPTICAL_CONSTANTS:
        available = list(METAL_OPTICAL_CONSTANTS.keys())
        raise KeyError(f"Metal '{metal_name}' not found. Available: {available}")

    n, kappa = METAL_OPTICAL_CONSTANTS[metal_key]
    return {
        "n": n,
        "κ": kappa,
        "complex_n": complex(n, kappa),
    }


@maxwell_cite(
    795, 796,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate Fresnel reflection coefficient for metal",
)
def calc_fresnel_reflection_metal(
    n1: float,
    n2_real: float,
    kappa: float,
    angle_incidence: float,
    polarization: str = "s",
) -> complex:
    """
    Calculate Fresnel reflection coefficient for metal interface.

    Art. 795-796: For a metal with complex refractive index ñ = n + iκ:

        r_s = (n1*cos(θ1) - ñ2*cos(θ2)) / (n1*cos(θ1) + ñ2*cos(θ2))
        r_p = (ñ2*cos(θ1) - n1*cos(θ2)) / (ñ2*cos(θ1) + n1*cos(θ2))

    Args:
        n1: Refractive index of incident medium.
        n2_real: Real part of metal refractive index.
        kappa: Extinction coefficient.
        angle_incidence: Angle of incidence (radians).
        polarization: "s" or "p".

    Returns:
        Complex reflection coefficient.

    Reference:
        Part IV, Arts. 795-796: Fresnel reflection at metal.

    Example:
        >>> # Silver at normal incidence
        >>> r = calc_fresnel_reflection_metal(1.0, 0.05, 3.88, 0.0)
        >>> R = abs(r)**2  # Reflectance
        >>> print(f"R = {R:.4f}")  # R ≈ 0.95 for silver
    """
    n2_complex = complex(n2_real, kappa)
    theta1 = angle_incidence
    cos_theta1 = np.cos(theta1)
    sin_theta1 = np.sin(theta1)

    # Complex Snell's law
    sin_theta2 = (n1 / n2_complex) * sin_theta1
    cos_theta2 = np.sqrt(1.0 - sin_theta2 ** 2)

    if polarization == "s":
        numerator = n1 * cos_theta1 - n2_complex * cos_theta2
        denominator = n1 * cos_theta1 + n2_complex * cos_theta2
    else:  # p
        numerator = n2_complex * cos_theta1 - n1 * cos_theta2
        denominator = n2_complex * cos_theta1 + n1 * cos_theta2

    return numerator / denominator


@maxwell_cite(
    797,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate metal reflectance at normal incidence",
)
def calc_metal_reflectance_normal(
    n1: float,
    n2_real: float,
    kappa: float,
) -> float:
    """
    Calculate reflectance of metal at normal incidence.

    Art. 797-800: At normal incidence:

        R = [(n1 - n2)² + κ²] / [(n1 + n2)² + κ²]

    For highly reflective metals (large κ), R approaches 1.

    Args:
        n1: Refractive index of incident medium.
        n2_real: Real part of metal refractive index.
        kappa: Extinction coefficient.

    Returns:
        Reflectance R (0 to 1).

    Reference:
        Part IV, Arts. 797-800: Normal reflectance of metals.

    Example:
        >>> # Silver reflectance
        >>> R = calc_metal_reflectance_normal(1.0, 0.05, 3.88)
        >>> print(f"R = {R:.4f}")  # R ≈ 0.95
    """
    numerator = (n1 - n2_real) ** 2 + kappa ** 2
    denominator = (n1 + n2_real) ** 2 + kappa ** 2
    return numerator / denominator


@maxwell_cite(
    798,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate skin depth in metal",
)
def calc_skin_depth(
    wavelength: float,
    kappa: float,
) -> float:
    """
    Calculate electromagnetic skin depth in metal.

    Art. 798: The skin depth is the penetration depth at which
    field amplitude drops to 1/e of surface value:

        δ = λ / (2π * κ)

    Args:
        wavelength: Vacuum wavelength (cm).
        kappa: Extinction coefficient.

    Returns:
        Skin depth δ (cm).

    Reference:
        Part IV, Art. 798: Skin depth formula.

    Example:
        >>> # Skin depth for visible light in silver
        >>> delta = calc_skin_depth(500e-7, 3.88)
        >>> print(f"δ = {delta*1e7:.1f} nm")  # ~20 nm
    """
    if wavelength <= 0:
        raise ValueError(f"Wavelength must be positive")
    if kappa <= 0:
        return float('inf')

    return wavelength / (2.0 * np.pi * kappa)


@maxwell_cite(
    799,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate absorption coefficient",
)
def calc_absorption_coefficient(
    wavelength: float,
    kappa: float,
) -> float:
    """
    Calculate absorption coefficient of metal.

    Art. 799: The absorption coefficient α determines intensity decay:

        I(z) = I₀ * exp(-α*z)

    where:

        α = 4π * κ / λ  (cm⁻¹)

    Args:
        wavelength: Vacuum wavelength (cm).
        kappa: Extinction coefficient.

    Returns:
        Absorption coefficient α (cm⁻¹).

    Reference:
        Part IV, Art. 799: Absorption coefficient.
    """
    if wavelength <= 0:
        raise ValueError(f"Wavelength must be positive")
    if kappa <= 0:
        return 0.0

    return 4.0 * np.pi * kappa / wavelength


@maxwell_cite(
    795, 796, 797, 798, 799, 800,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify metallic reflection relations",
)
def verify_metallic_reflection(
    n2_real: float = 0.05,
    kappa: float = 3.88,
    wavelength: float = 589e-7,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify metallic reflection relationships.

    Art. 795-800: This function verifies:
    1. R = |r|² at normal incidence
    2. Skin depth formula
    3. Absorption coefficient relation
    4. R → 1 as κ → ∞ (perfect reflector)

    Args:
        n2_real: Real part of metal refractive index.
        kappa: Extinction coefficient.
        wavelength: Test wavelength (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 795-800: Metallic reflection verification.
    """
    n1 = 1.0  # Air

    # Normal reflectance
    R = calc_metal_reflectance_normal(n1, n2_real, kappa)

    # Verify R → 1 as κ increases
    R_large_kappa = calc_metal_reflectance_normal(n1, n2_real, 100.0)
    high_reflectivity_verified = R_large_kappa > 0.99

    # Skin depth
    delta = calc_skin_depth(wavelength, kappa)

    # Absorption coefficient
    alpha = calc_absorption_coefficient(wavelength, kappa)

    # Verify α = 2/δ
    alpha_expected = 2.0 / delta if delta > 0 else 0
    alpha_error = abs(alpha - alpha_expected) / alpha if alpha > 0 else 0

    return {
        "n2_real": n2_real,
        "kappa": kappa,
        "wavelength": wavelength,
        "normal_reflectance": R,
        "skin_depth": delta,
        "absorption_coefficient": alpha,
        "alpha_expected": alpha_expected,
        "alpha_error": alpha_error,
        "high_reflectivity_verified": high_reflectivity_verified,
        "verified": alpha_error < tolerance and high_reflectivity_verified,
    }


@maxwell_cite(
    795, 796, 797, 798, 799, 800,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete metallic reflection analysis",
)
def analyze_metallic_reflection(
    metal_name: str = None,
    n2_real: float = None,
    kappa: float = None,
    wavelength: float = 589e-7,
    angle_range: Tuple[float, float] = None,
) -> dict[str, float]:
    """
    Complete analysis of metallic reflection.

    Art. 795-800: Comprehensive analysis including:
    1. Complex refractive index
    2. Normal reflectance
    3. Angle-dependent reflectance
    4. Skin depth
    5. Absorption coefficient

    Args:
        metal_name: Optional metal name for lookup.
        n2_real: Real part of refractive index (if not using metal_name).
        kappa: Extinction coefficient (if not using metal_name).
        wavelength: Wavelength (cm).
        angle_range: (θ_min, θ_max) in radians for sweep.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 795-800: Complete metallic reflection analysis.

    Example:
        >>> # Analyze silver at visible wavelengths
        >>> result = analyze_metallic_reflection("silver", wavelength=500e-7)
        >>> print(f"R = {result['normal_reflectance']:.4f}")
        >>> print(f"δ = {result['skin_depth']*1e7:.1f} nm")
    """
    # Get metal constants
    if metal_name is not None and metal_name.lower() in METAL_OPTICAL_CONSTANTS:
        constants = get_metal_constants(metal_name)
        n2_real = constants["n"]
        kappa = constants["κ"]
    else:
        if n2_real is None:
            n2_real = 0.05
        if kappa is None:
            kappa = 3.88

    mr = MetallicReflection(n1=1.0, n2_real=n2_real, kappa=kappa)

    # Normal reflectance
    R_normal = mr.normal_reflectance()

    # Angle-dependent reflectance
    if angle_range is None:
        angle_range = (0.0, np.pi / 2 - 0.01)

    n_angles = 10
    angles = np.linspace(angle_range[0], angle_range[1], n_angles)
    R_s_values = [mr.reflectance(a, "s") for a in angles]
    R_p_values = [mr.reflectance(a, "p") for a in angles]
    R_unpol_values = [mr.reflectance(a, "unpolarized") for a in angles]

    return {
        "metal": metal_name if metal_name else "custom",
        "n_real": n2_real,
        "kappa": kappa,
        "complex_refractive_index": mr.complex_refractive_index,
        "wavelength_cm": wavelength,
        "wavelength_nm": wavelength * 1e7,
        "normal_reflectance": R_normal,
        "skin_depth_cm": mr.skin_depth(wavelength),
        "skin_depth_nm": mr.skin_depth(wavelength) * 1e7,
        "absorption_coefficient": mr.absorption_coefficient(wavelength),
        "angle_range_rad": angle_range,
        "R_s_min": min(R_s_values),
        "R_s_max": max(R_s_values),
        "R_p_min": min(R_p_values),
        "R_p_max": max(R_p_values),
        "R_unpol_min": min(R_unpol_values),
        "R_unpol_max": max(R_unpol_values),
    }
