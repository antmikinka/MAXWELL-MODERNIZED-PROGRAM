"""maxwell.math — Advanced mathematical methods.

Package for Maxwell's advanced mathematical techniques including
spherical harmonics, elliptic integrals, vector calculus, and
conjugate functions for 2D electrostatics.

Coverage:
    - Part I, Chapter IX (Arts. 128-146): Spherical harmonics foundations
    - Part IV (Arts. 675-695): Multipole expansions
    - Part IV (Arts. 696-705): Elliptic integrals
    - Vector operators (Arts. 71-110): Vector calculus
    - Conjugate functions (Arts. 182-206): 2D electrostatics
"""

from maxwell.math.spherical_harmonics import (
    # Part I, Chapter IX (Arts. 128-146) — Core spherical harmonics
    LaplaceSpherical,
    SurfaceHarmonic,
    SolidHarmonic,
    SphericalHarmonicExpansion,
    addition_theorem,
    angle_between_directions,
    verify_addition_theorem,
    potential_expansion_addition_theorem,
    distance_between_points,
    verify_chapter_ix,
    analyze_chapter_ix,

    # Part IV (Arts. 675-695) — Multipole expansions
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
    # Part I, Chapter IX (Arts. 128-146) — Spherical harmonics foundations
    "LaplaceSpherical",
    "SurfaceHarmonic",
    "SolidHarmonic",
    "SphericalHarmonicExpansion",
    "addition_theorem",
    "angle_between_directions",
    "verify_addition_theorem",
    "potential_expansion_addition_theorem",
    "distance_between_points",
    "verify_chapter_ix",
    "analyze_chapter_ix",

    # Part IV (Arts. 675-695) — Multipole expansions
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
