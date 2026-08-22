"""maxwell.magneto_optics.circular_polarization — Circular rays (Arts. 811-817).

Kinematical analysis of circularly polarized light: the resolution of a
linearly polarized ray into right- and left-circular components, the
velocity splitting which produces Faraday rotation, and the vector
description of the luminiferous disturbance (Maxwell 1873, Part IV,
Ch. XXI "Magnetic Action on Light", Arts. 811-817).

Unit and sign conventions
-------------------------
* All angles are returned in radians; velocities in cm/s.
* ``perform_kinematic_analysis`` uses the convention
  ``rotation_per_length = (k_right - k_left) / 2``: the rotation of the
  plane of polarization equals HALF the phase difference accumulated by
  the two circular components (Art. 811).  This convention is pinned by
  the regression spec ``tests/test_defects_s1.py`` R2 (defect D-04).
* Art. 817 parametrisation (used by :func:`derive_circular_kinematics`):
  ``xi = r cos(theta)``, ``eta = r sin(theta)``, ``theta = n t - q z + a``
  with ``n`` the angular frequency and ``q`` the wave number; the ray is
  right- or left-handed according as ``q`` is negative or positive, and
  is propagated in the positive direction of ``z`` when ``n`` and ``q``
  have the same sign.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi


@maxwell_cite(811, part=4, theory_class="standard_math")
def perform_kinematic_analysis(
    omega: float,
    k_right: float,
    k_left: float,
) -> dict[str, float]:
    """Kinematical analysis of the two circular components (Art. 811).

    A linearly polarized wave is the sum of a right- and a left-circular
    component.  In a rotatory or magnetic medium the two components
    travel with different velocities: after a distance L their phases
    differ by (k_right - k_left) L, and the resultant plane of
    polarization has turned through HALF that phase difference.

    Args:
        omega: Angular frequency of the wave.
        k_right: Wave number for right circular polarization.
        k_left: Wave number for left circular polarization.

    Returns:
        Dictionary with entries:
            v_right, v_left: Phase velocities omega/k (cm/s).
            velocity_split: v_right - v_left.
            phase_diff_per_length: k_right - k_left.
            rotation_per_length: (k_right - k_left) / 2 — rotation of the
                plane of polarization per unit path (rad/cm).
    """
    v_right = omega / k_right
    v_left = omega / k_left

    # After traveling distance L, the phase difference
    # between the two components causes rotation equal to HALF of it.
    phase_diff_per_unit_length = k_right - k_left
    rotation_per_unit_length = phase_diff_per_unit_length / 2.0

    return {
        "v_right": v_right,
        "v_left": v_left,
        "velocity_split": v_right - v_left,
        "phase_diff_per_length": phase_diff_per_unit_length,
        "rotation_per_length": rotation_per_unit_length,
    }


@maxwell_cite(812, part=4, theory_class="standard_math")
def calc_circular_velocity_split(
    refractive_index: float,
    magnetic_field: float,
    verdet_constant: float,
    wavelength: float,
) -> float:
    """Velocity difference of the circular components (Art. 812).

    From Faraday's law theta = V B L (Art. 808) and the kinematic
    identity theta = (k_R - k_L) L / 2 (Art. 811) one obtains
    Delta k = 2 V B.  With n = c k / omega and omega = 2 pi c / lambda
    this gives the refractive-index difference

        n_R - n_L = V B lambda / pi         (NO factor 2 — D-04),

    and with v = c/n, to first order in the small split,

        Delta v = c Delta n / n^2.

    Args:
        refractive_index: Base refractive index of the medium.
        magnetic_field: Magnetic force along the ray (gauss).
        verdet_constant: Verdet constant in rad/(gauss cm).
        wavelength: Wavelength of the light (cm).

    Returns:
        Difference of propagation velocity of the two circular
        components (cm/s).
    """
    c = CONST.C
    # Delta n = V * B * lambda / pi  (Stage-3 defect D-04: the factor 2
    # present in the pre-fix code was removed; see tests/test_defects_s1.py R2).
    delta_n = verdet_constant * wavelength * magnetic_field / PI
    # Delta v = c * delta_n / n^2
    return c * delta_n / refractive_index**2


@dataclass
class CircularlyPolarizedRay:
    """Right or left-handed circularly polarized ray (Art. 813).

    Represents a single circularly polarized component propagating
    through a medium, with its electric field vector rotating about the
    propagation axis at constant magnitude (Art. 813: the tip of the
    vector describes a circle).

    Attributes:
        amplitude: Electric field amplitude vector (its norm is the
            radius r of the circle described by the disturbance).
        omega: Angular frequency.
        k: Wave number (signed: sign carries the handedness/propagation
            sense in the Art. 817 convention).
        handedness: 'right' or 'left'.
        propagation_axis: Direction of propagation (need not be unit).
    """

    amplitude: np.ndarray
    omega: float
    k: float
    handedness: str
    propagation_axis: np.ndarray

    @maxwell_cite(813, part=4, theory_class="standard_math")
    def electric_field(self, z: float, t: float) -> np.ndarray:
        """Electric field vector at position z and time t.

        For circular polarization the vector rotates at constant
        magnitude, so the tip describes a circle:
        E = A * [cos(kz - wt) * ex + sin(kz - wt) * ey]  (right-handed)
        E = A * [cos(kz - wt) * ex - sin(kz - wt) * ey]  (left-handed)

        Args:
            z: Position along the propagation axis.
            t: Time.

        Returns:
            Electric field vector (transverse to the propagation axis,
            magnitude equal to the amplitude A).
        """
        phase = self.k * z - self.omega * t
        sign = 1 if self.handedness == "right" else -1

        # Build orthonormal basis perpendicular to propagation
        # For simplicity, assume propagation along z
        if np.allclose(self.propagation_axis, [0, 0, 1]):
            ex = np.array([1.0, 0.0, 0.0])
            ey = np.array([0.0, 1.0, 0.0])
        else:
            # General case: construct perpendicular basis
            ez = self.propagation_axis / np.linalg.norm(self.propagation_axis)
            ex = np.array([1.0, 0.0, 0.0])
            if np.abs(np.dot(ex, ez)) > 0.9:
                ex = np.array([0.0, 1.0, 0.0])
            ex = ex - np.dot(ex, ez) * ez
            ex = ex / np.linalg.norm(ex)
            ey = np.cross(ez, ex)

        A = np.linalg.norm(self.amplitude)
        return A * (np.cos(phase) * ex + sign * np.sin(phase) * ey)

    @maxwell_cite(813, part=4, theory_class="standard_math")
    def velocity(self) -> float:
        """Phase velocity of this circular component.

        v = omega / k

        Returns:
            Phase velocity in cm/s.
        """
        return self.omega / self.k


@maxwell_cite(814, part=4, theory_class="standard_math")
def calc_natural_velocity_split(
    refractive_index: float,
    rotatory_power: float,
    wavelength: float,
) -> dict[str, float]:
    """Velocity split in a naturally rotatory medium (Art. 814).

    In quartz, turpentine, &c. the two circular components travel at
    different velocities on account of the structure of the medium,
    without any applied magnetic force.  With rotation per unit length
    rho = (k_R - k_L)/2 and v = omega/k, first order gives

        Delta v = 2 v^2 rho / omega.

    Args:
        refractive_index: Average refractive index.
        rotatory_power: Rotatory power rho (rad/cm).
        wavelength: Wavelength (cm).

    Returns:
        Dictionary with v_right, v_left (cm/s) and delta_v = v_right -
        v_left.
    """
    c = CONST.C
    v_avg = c / refractive_index
    # Delta v = 2 * v^2 * rotatory_power / omega
    omega = 2.0 * PI * c / wavelength
    delta_v = 2.0 * v_avg**2 * rotatory_power / omega

    return {
        "v_right": v_avg + delta_v / 2,
        "v_left": v_avg - delta_v / 2,
        "delta_v": delta_v,
    }


@maxwell_cite(815, part=4, theory_class="standard_math")
def calc_magnetic_velocity_split(
    refractive_index: float,
    magnetic_field: float,
    verdet_constant: float,
    wavelength: float,
) -> dict[str, float]:
    """Velocity split induced by a magnetic force along the ray (Art. 815).

    Maxwell 1873, Art. 815: the helix which represents a given ray has
    the same configuration whether the ray goes one way or the other,
    but "in the first instance the ray travels faster... Hence greater
    forces are called into play when the helix is going round one way
    than when it is going round the other way."  The magnetic-force-
    induced split is computed from rotation per unit length V B =
    (k_R - k_L)/2, i.e. Delta k = 2 V B, so that

        Delta v = v^2 Delta k / omega.

    This is consistent with :func:`calc_circular_velocity_split` (Art.
    812): both give Delta v = c V B lambda / (pi n^2).

    Args:
        refractive_index: Average refractive index.
        magnetic_field: Applied magnetic force along the ray (gauss).
        verdet_constant: Verdet constant in rad/(gauss cm).
        wavelength: Wavelength (cm).

    Returns:
        Dictionary with v_right, v_left (cm/s) and delta_v.
    """
    c = CONST.C
    v_avg = c / refractive_index
    # Rotation per unit length = V * B = (k_R - k_L) / 2
    # So delta_k = 2 * V * B
    # delta_v = v^2 * delta_k / omega
    omega = 2.0 * PI * c / wavelength
    delta_k = 2.0 * verdet_constant * magnetic_field
    delta_v = v_avg**2 * delta_k / omega

    return {
        "v_right": v_avg + delta_v / 2,
        "v_left": v_avg - delta_v / 2,
        "delta_v": delta_v,
    }


@maxwell_cite(
    816,
    part=4,
    theory_class="maxwell_original",
    description="The luminiferous disturbance is a vector perpendicular to "
    "the direction of the ray; its longitudinal part is zero.",
)
def define_light_vector(
    disturbance: np.ndarray,
    ray_direction: np.ndarray,
) -> np.ndarray:
    """Transverse vector disturbance of light (Art. 816).

    Maxwell 1873, Art. 816: "The disturbance which constitutes light,
    whatever its physical nature may be, is of the nature of a vector,
    perpendicular to the direction of the ray."  This is proved from the
    interference of two rays, combined with the non-interference of two
    rays polarized in perpendicular planes: the disturbance must be a
    directed quantity, and it must be perpendicular to the ray.  Light is
    therefore a TRANSVERSE VECTOR wave, not a longitudinal scalar
    (compression) wave.

    Computed result: the component of the disturbance vector transverse
    to the ray direction, i.e. the disturbance with its (unphysical)
    longitudinal projection removed:

        light_vector = d - (d . r_hat) r_hat.

    For a physically admissible light wave the longitudinal part is zero
    and the returned vector equals the input exactly; in either case the
    result is perpendicular to the ray to machine precision.

    Args:
        disturbance: Disturbance vector, shape (3,).
        ray_direction: Direction of the ray (need not be unit), shape (3,).

    Returns:
        Transverse part of the disturbance, shape (3,).
    """
    d = np.asarray(disturbance, dtype=float)
    ray = np.asarray(ray_direction, dtype=float)
    r_hat = ray / np.linalg.norm(ray)
    return d - np.dot(d, r_hat) * r_hat


@maxwell_cite(
    817,
    part=4,
    theory_class="maxwell_original",
    description="Equations of a circularly-polarized ray: xi = r cos(theta), "
    "eta = r sin(theta), theta = n t - q z + a; n tau = 2 pi, q lambda = 2 pi, "
    "velocity = n/q; handedness by the sign of q, propagation sense by the "
    "relative signs of n and q.",
)
def derive_circular_kinematics(
    n_freq: float,
    q_wavenumber: float,
    amplitude: float,
    phase: float = 0.0,
    z: float = 0.0,
    t: float = 0.0,
) -> dict[str, float | str]:
    """Kinematic equations of a circularly polarized ray (Art. 817).

    Maxwell 1873, Art. 817, equations (1)-(4):

        xi    = r cos(theta),   eta = r sin(theta)     (1)
        theta = n t - q z + a                          (2)
        n tau = 2 pi            (periodic time tau)    (3)
        q lambda = 2 pi         (wave-length lambda)   (4)

    "The velocity of propagation is n/q.  The phase of the disturbance
    when t and z are both zero is a.  The circularly-polarized light is
    right-handed or left-handed according as q is negative or positive.
    ...  The light is propagated in the positive or the negative
    direction of the axis of z, according as n and q are of the same or
    of opposite signs."

    Args:
        n_freq: Angular frequency n (rad/s).  Must be nonzero.
        q_wavenumber: Wave number q (rad/cm); its sign carries the
            handedness.  Must be nonzero.
        amplitude: Magnitude r of the vector disturbance.
        phase: Initial phase a (radians).
        z: Position at which to evaluate the disturbance (cm).
        t: Time at which to evaluate the disturbance (s).

    Returns:
        Dictionary with computed entries:
            xi, eta: Components of the disturbance at (z, t) — eq. (1).
            theta: Phase angle n t - q z + a at (z, t) — eq. (2).
            radius: The amplitude r (check: xi^2 + eta^2 = r^2).
            velocity: n/q (cm/s).
            wavelength: 2 pi/|q| (cm) — eq. (4).
            period: 2 pi/|n| (s) — eq. (3).
            handedness: 'right' if q < 0 else 'left'.
            propagation_direction: +1 if sign(n) == sign(q) (positive z),
                else -1.

    Raises:
        ValueError: If n_freq or q_wavenumber is zero (the period or the
            velocity/lambda would be undefined).
    """
    if n_freq == 0:
        raise ValueError("n_freq must be nonzero (period 2*pi/|n| undefined)")
    if q_wavenumber == 0:
        raise ValueError(
            "q_wavenumber must be nonzero (velocity n/q and wavelength "
            "2*pi/|q| undefined)"
        )

    theta = n_freq * t - q_wavenumber * z + phase
    xi = amplitude * float(np.cos(theta))
    eta = amplitude * float(np.sin(theta))

    return {
        "xi": xi,
        "eta": eta,
        "theta": theta,
        "radius": amplitude,
        "velocity": n_freq / q_wavenumber,
        "wavelength": 2.0 * float(PI) / abs(q_wavenumber),
        "period": 2.0 * float(PI) / abs(n_freq),
        "handedness": "right" if q_wavenumber < 0 else "left",
        "propagation_direction": 1 if (n_freq * q_wavenumber > 0) else -1,
    }
