"""maxwell.magneto_optics.circular_polarization — Circular rays (Arts. 811-817).

Kinematical analysis of circularly polarized light, velocity
splitting in rotatory and magnetic media, and the vector
nature of the luminiferous disturbance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@maxwell_cite(811, part=4, theory_class="standard_math")
def perform_kinematic_analysis(
    omega: float,
    k_right: float,
    k_left: float,
) -> dict[str, float]:
    """Kinematical analysis of circular polarization components.

    A linearly polarized wave can be decomposed into right and
    left circularly polarized components. In a magnetized medium,
    these components travel at different velocities.

    Args:
        omega: Angular frequency of the wave.
        k_right: Wave number for right circular polarization.
        k_left: Wave number for left circular polarization.

    Returns:
        Dictionary with velocities, phase difference, and rotation.
    """
    v_right = omega / k_right
    v_left = omega / k_left

    # After traveling distance L, the phase difference
    # between the two components causes rotation
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
    """Calculate velocity difference between circular polarizations.

    In a magnetic medium, the refractive indices for right and
    left circularly polarized light differ:
        n_R - n_L = 2 * V * lambda * B / pi

    Args:
        refractive_index: Base refractive index of medium.
        magnetic_field: Magnetic field strength.
        verdet_constant: Verdet constant.
        wavelength: Wavelength of light.

    Returns:
        Difference in propagation velocity (cm/s).
    """
    c = 2.99792458e10  # speed of light in CGS
    # Delta n = 2 * V * lambda * B / pi (approximately)
    delta_n = 2.0 * verdet_constant * wavelength * magnetic_field / PI
    # Delta v = c * delta_n / n^2
    return c * delta_n / refractive_index**2


@dataclass
class CircularlyPolarizedRay:
    """Right or left-handed circularly polarized ray (Art. 813).

    Represents a single circularly polarized component propagating
    through a medium, with its electric and magnetic field vectors
    rotating about the propagation axis.

    Attributes:
        amplitude: Electric field amplitude.
        omega: Angular frequency.
        k: Wave number.
        handedness: 'right' or 'left'.
        propagation_axis: Unit vector in propagation direction.
    """

    amplitude: np.ndarray
    omega: float
    k: float
    handedness: str
    propagation_axis: np.ndarray

    @maxwell_cite(813, part=4, theory_class="standard_math")
    def electric_field(self, z: float, t: float) -> np.ndarray:
        """Calculate electric field vector at position z and time t.

        For circular polarization, the E-field rotates:
        E = A * [cos(kz - wt) * ex + sin(kz - wt) * ey]  (right-handed)
        E = A * [cos(kz - wt) * ex - sin(kz - wt) * ey]  (left-handed)

        Args:
            z: Position along propagation axis.
            t: Time.

        Returns:
            Electric field vector.
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
    """Calculate velocity split in naturally rotatory media.

    In quartz, turpentine, etc., the velocities of right and
    left circularly polarized light differ due to the intrinsic
    structure of the medium (not an applied field).

    Args:
        refractive_index: Average refractive index.
        rotatory_power: Rotatory power (radians/cm).
        wavelength: Wavelength.

    Returns:
        Velocities for right and left circular components.
    """
    c = 2.99792458e10
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
    """Calculate velocity split in magnetized media.

    The magnetic-field-induced velocity difference between
    circular polarizations, causing Faraday rotation.

    Args:
        refractive_index: Average refractive index.
        magnetic_field: Applied magnetic field.
        verdet_constant: Verdet constant.
        wavelength: Wavelength.

    Returns:
        Velocities for right and left circular components.
    """
    c = 2.99792458e10
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


@maxwell_cite(816, part=4, theory_class="standard_math")
def define_light_vector(
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """Define the luminiferous disturbance as a vector.

    Art. 816: The luminiferous disturbance in a circularly
    polarized ray is a vector quantity - the electric field
    vector rotates in a plane perpendicular to propagation.

    This proves that light is a transverse vector wave,
    not a scalar compression wave.

    Args:
        E_field: Electric field vector of the light wave.
        B_field: Magnetic field vector of the light wave.

    Returns:
        The Poynting vector (direction of energy flow).
    """
    # S = (c/4pi) E x B
    return (2.99792458e10 / (4.0 * PI)) * np.cross(E_field, B_field)


@maxwell_cite(817, part=4, theory_class="standard_math")
def derive_circular_kinematics(
    omega: float,
    k_right: float,
    k_left: float,
    amplitude: float,
) -> dict[str, Any]:
    """Derive kinematic equations of circularly polarized light.

    Full kinematical description: the electric field components,
    intensity, and polarization state as functions of position
    and time.

    Args:
        omega: Angular frequency.
        k_right: Wave number for right circular.
        k_left: Wave number for left circular.
        amplitude: Electric field amplitude.

    Returns:
        Kinematic parameters dict.
    """
    from typing import Any

    v_r = omega / k_right
    v_l = omega / k_left

    # Rotation of polarization plane after distance L
    rotation_per_cm = (k_right - k_left) / 2.0

    # Ellipticity: for pure circular, the amplitudes are equal
    # Linear polarization is recovered when delta_phi = pi
    beat_length = 2.0 * PI / abs(k_right - k_left)

    return {
        "omega": omega,
        "k_right": k_right,
        "k_left": k_left,
        "v_right": v_r,
        "v_left": v_l,
        "rotation_per_cm": rotation_per_cm,
        "beat_length": beat_length,
        "amplitude": amplitude,
        "intensity": amplitude**2,  # Proportional to E^2
    }
