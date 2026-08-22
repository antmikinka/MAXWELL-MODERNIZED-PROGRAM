"""maxwell.vortex_engine.magnetic_rotation — Verdet's research (Arts. 829-830).

The expression for the rotation of the plane of polarization deduced
from the vortex theory (Art. 829, equations (21)-(26)) and its
comparison with Verdet's measurements on bisulphide of carbon
(Art. 830).

Maxwell 1873, Part IV, Ch. XXI, Arts. 829-830.
"""

from __future__ import annotations

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi

#: Verdet's measurements on bisulphide of carbon at 24.9 C (Art. 830).
#:
#: Provenance: Maxwell 1873, Vol. II, p. 468, table "Magnetic Rotation of
#: the Plane of Polarization (from Verdet)".  Rotations are Verdet's own
#: numbers normalized so that the ray E reads 1000; the absolute rotation
#: of the ray E was 25 deg 28 min.  "observed" are Verdet's measurements,
#: "formula_1" the values calculated by formula (I) of Art. 830 — which is
#: exactly Art. 829 eq. (26).  Fraunhofer wavelengths in cm: C (red)
#: 6.563e-5, D (sodium) 5.893e-5, E 5.270e-5, F (H beta) 4.861e-5,
#: G (H gamma) 4.308e-5.  EMPIRICAL class (historical determinations).
VERDET_CS2_DATA: dict = {
    "medium": "bisulphide_of_carbon",
    "temperature_c": 24.9,
    "rotation_of_E": 25.0 + 28.0 / 60.0,  # degrees: 25 deg 28 min
    "wavelengths_cm": {
        "C": 6.563e-5,
        "D": 5.893e-5,
        "E": 5.270e-5,
        "F": 4.861e-5,
        "G": 4.308e-5,
    },
    "observed_rotation": {"C": 592, "D": 768, "E": 1000, "F": 1234, "G": 1704},
    "calculated_formula_1": {"C": 589, "D": 760, "E": 1000, "F": 1234, "G": 1713},
}


@maxwell_cite(
    829,
    part=4,
    theory_class="maxwell_original",
    description="Equation (25): m = 4 pi^2 C / (v rho) is the coefficient "
    "of magnetic rotation for the medium, to be determined by observation.",
)
def rotation_coefficient(
    coupling_constant: float,
    density: float,
    velocity: float | None = None,
) -> float:
    """Coefficient of magnetic rotation of the medium (Art. 829, eq. 25).

    Maxwell 1873, Art. 829: "Writing 4 pi^2 C / (v rho) = m (25) we may
    call m the coefficient of magnetic rotation for the medium, a
    quantity whose value must be determined by observation."  Here v is
    the velocity of light in air and rho the density of the medium.

    Args:
        coupling_constant: Coupling constant C of Art. 824 eq. (3).
        density: Density rho of the medium.
        velocity: Velocity of light in air (cm/s); defaults to CONST.C.

    Returns:
        m = 4 pi^2 C / (v rho).
    """
    v = CONST.C if velocity is None else velocity
    return 4.0 * PI**2 * coupling_constant / (v * density)


@maxwell_cite(
    829,
    part=4,
    theory_class="maxwell_original",
    description="Equations (23)-(24) and the final result (26): "
    "theta = m c gamma (i^2/lambda^2) (i - lambda di/dlambda), with the "
    "exact denominator of eq. (24) available as a correction.",
)
def derive_magnetic_rotation(
    coupling_constant: float,
    density: float,
    path_length: float,
    magnetic_force: float,
    refractive_index: float,
    wavelength: float,
    dispersion_slope: float = 0.0,
    velocity: float | None = None,
    include_denominator_correction: bool = False,
) -> float:
    """Rotation of the plane of polarization from the vortex theory.

    Maxwell 1873, Art. 829.  With lambda the wave-length in air, v the
    velocity in air, and i the index of refraction in the medium,
    q lambda = 2 pi i and n lambda = 2 pi v (eq. 21), and the rotation
    through a thickness c of the medium is (eqs. 23-24)

        theta = [4 pi^2 C / (v rho)] c gamma (i^2 / lambda^2)
                x (i - lambda di/dlambda)
                x 1 / (1 - 2 pi C gamma i^2 / (v rho lambda)),

    where the last factor is "in all actual cases a quantity which we may
    neglect in comparison with unity".  Writing m = 4 pi^2 C / (v rho)
    (eq. 25), the final result of the theory is (eq. 26)

        theta = m c gamma (i^2 / lambda^2) (i - lambda di/dlambda),

    "where theta is the angular rotation of the plane of polarization,
    m a constant determined by observation of the medium, gamma the
    intensity of the magnetic force resolved in the direction of the ray,
    c the length of the ray within the medium, lambda the wave-length of
    the light in air, and i its index of refraction in the medium."

    Args:
        coupling_constant: Coupling constant C.
        density: Density rho of the medium.
        path_length: Length c of the ray within the medium (cm).
        magnetic_force: Magnetic force gamma resolved along the ray.
        refractive_index: Index of refraction i in the medium.
        wavelength: Wave-length lambda of the light in air (cm).
        dispersion_slope: di/dlambda; lambda di/dlambda vanishes when 0.
        velocity: Velocity of light in air (cm/s); defaults to CONST.C.
        include_denominator_correction: If True, include the exact
            denominator of eq. (24); default False reproduces eq. (26).

    Returns:
        Rotation angle theta in radians.
    """
    v = CONST.C if velocity is None else velocity
    m = rotation_coefficient(coupling_constant, density, velocity=v)
    theta = (
        m
        * path_length
        * magnetic_force
        * (refractive_index**2 / wavelength**2)
        * (refractive_index - wavelength * dispersion_slope)
    )
    if include_denominator_correction:
        denominator = 1.0 - (
            2.0 * PI * coupling_constant * magnetic_force * refractive_index**2
        ) / (v * density * wavelength)
        theta = theta / denominator
    return theta


@maxwell_cite(
    830,
    part=4,
    theory_class="maxwell_original",
    description="Verdet's two laws: the rotations follow approximately the "
    "inverse square of the wave-length, while the product theta lambda^2 "
    "increases from the least refrangible to the most refrangible end of "
    "the spectrum.",
)
def verdet_inverse_square_analysis(
    wavelengths: np.ndarray,
    rotations: np.ndarray,
    threshold: float = 0.15,
) -> dict:
    """Analyse a rotation spectrum against Verdet's laws (Art. 830).

    Maxwell 1873, Art. 830, Verdet's results:
    (1) "The magnetic rotations of the planes of polarization of the rays
    of different colours follow approximately the law of the inverse
    square of the wave-length."
    (2) "The exact law of the phenomena is always such that the product
    of the rotation by the square of the wave-length increases from the
    least refrangible to the most refrangible end of the spectrum."

    Computed checks, both from the data alone:
    * law (2): theta lambda^2 is strictly increasing when the rays are
      ordered from longest to shortest wavelength;
    * law (1): least-squares fit theta = k / lambda^2
      (k = sum(theta x)/sum(x^2) with x = 1/lambda^2), with the RMS
      fractional residual reported and compared to the threshold.

    Args:
        wavelengths: Wave-lengths (any consistent unit), array-like.
        rotations: Corresponding measured rotations, array-like.
        threshold: RMS fractional residual below which the inverse-square
            law is deemed to hold approximately.

    Returns:
        Dictionary with entries:
            wavelength_order: wavelengths sorted longest-first (the
                order "from the least refrangible to the most
                refrangible end of the spectrum").
            theta_lambda_squared: theta lambda^2 in that order.
            monotonic_increase: True when theta lambda^2 increases
                strictly along that order (law 2).
            best_fit_k: Least-squares coefficient of theta = k/lambda^2.
            rms_fractional_residual: RMS of (theta_fit - theta)/theta.
            obeys_inverse_square_within_threshold: True when the RMS
                fractional residual is below the threshold (law 1).
    """
    lam = np.asarray(wavelengths, dtype=float)
    theta = np.asarray(rotations, dtype=float)
    order = np.argsort(lam)[::-1]  # longest wavelength first
    lam_sorted = lam[order]
    theta_sorted = theta[order]
    theta_lambda_squared = theta_sorted * lam_sorted**2
    monotonic = bool(np.all(np.diff(theta_lambda_squared) > 0))
    x = 1.0 / lam**2
    best_fit_k = float(np.dot(theta, x) / np.dot(x, x))
    residual = (best_fit_k * x - theta) / theta
    rms = float(np.sqrt(np.mean(residual**2)))
    return {
        "wavelength_order": lam_sorted,
        "theta_lambda_squared": theta_lambda_squared,
        "monotonic_increase": monotonic,
        "best_fit_k": best_fit_k,
        "rms_fractional_residual": rms,
        "obeys_inverse_square_within_threshold": bool(rms < threshold),
    }


@maxwell_cite(830, part=4, theory_class="standard_math")
def compare_verdet_data(
    calculated_rotation: float,
    measured_rotation: float,
    tolerance: float = 0.1,
) -> dict[str, float]:
    """Compare a calculated rotation with Verdet's measurement (Art. 830).

    Art. 830: "The only test to which this theory has hitherto been
    subjected is that of comparing the values of theta for different
    kinds of light passing through the same medium and acted on by the
    same magnetic force."

    Args:
        calculated_rotation: Rotation predicted by the theory.
        measured_rotation: Rotation measured by Verdet.
        tolerance: Acceptable fractional difference.

    Returns:
        Dictionary with calculated, measured, discrepancy,
        fractional_error, and agrees (fractional_error < tolerance).
    """
    discrepancy = abs(calculated_rotation - measured_rotation)
    fractional_error = (
        discrepancy / measured_rotation if measured_rotation != 0 else float("inf")
    )

    return {
        "calculated": calculated_rotation,
        "measured": measured_rotation,
        "discrepancy": discrepancy,
        "fractional_error": fractional_error,
        "agrees": fractional_error < tolerance,
    }
