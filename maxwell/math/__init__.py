"""maxwell.math — Advanced mathematical methods (Arts. 675-705).

Package for Maxwell's advanced mathematical techniques including
spherical harmonics, elliptic integrals, and special functions.
"""

from maxwell.math.spherical_harmonics import (
    SphericalHarmonic,
    LegendrePolynomial,
    calc_legendre_polynomial,
    calc_associated_legendre,
    calc_spherical_harmonic,
    calc_multipole_expansion,
    verify_spherical_harmonics,
    analyze_spherical_harmonics,
)

from maxwell.math.elliptic_integrals import (
    EllipticIntegral,
    calc_elliptic_integral_first_kind,
    calc_elliptic_integral_second_kind,
    calc_elliptic_integral_third_kind,
    calc_complete_elliptic_integral_first_kind,
    calc_complete_elliptic_integral_second_kind,
    verify_elliptic_integrals,
    analyze_elliptic_integrals,
)

__all__ = [
    # Spherical harmonics (Arts. 675-695)
    "SphericalHarmonic",
    "LegendrePolynomial",
    "calc_legendre_polynomial",
    "calc_associated_legendre",
    "calc_spherical_harmonic",
    "calc_multipole_expansion",
    "verify_spherical_harmonics",
    "analyze_spherical_harmonics",

    # Elliptic integrals (Arts. 696-705)
    "EllipticIntegral",
    "calc_elliptic_integral_first_kind",
    "calc_elliptic_integral_second_kind",
    "calc_elliptic_integral_third_kind",
    "calc_complete_elliptic_integral_first_kind",
    "calc_complete_elliptic_integral_second_kind",
    "verify_elliptic_integrals",
    "analyze_elliptic_integrals",
]
