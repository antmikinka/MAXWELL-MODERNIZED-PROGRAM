"""
Magnetic Measurement Instruments — Maxwell's Part III, Chapter VII.

This module implements Maxwell's theory of magnetic measurement instruments
from Part III, Chapter VII (Arts. 449-464):

1. **Deflection Magnetometer** (Arts. 449-452):
   - Measurement of magnetic moment by deflection
   - Tan-A and Sin-A position measurements
   - Gauss's method for H and M determination

2. **Suspension Systems** (Arts. 453-456):
   - Unifilar suspension (single fiber torsion)
   - Bifilar suspension (two-fiber magnetometer)
   - Torsion constant determination
   - Magnetic declination measurement

3. **Kew Magnetometer** (Arts. 457-459):
   - Absolute measurement of horizontal force H
   - Vibration/oscillation period method

4. **Dip Circle** (Arts. 460-462):
   - Measurement of magnetic inclination/dip angle
   - Dip corrections and error analysis

5. **Balance Magnetometer** (Arts. 463-464):
   - Vertical force balance measurement
   - Vertical intensity Z determination

Category: A (maxwell_original) — Maxwell's theory of magnetic measurements.

References:
    Part III, Chapter VII: Magnetic Measurements (Arts. 449-464).
    Part IV, Arts. 707-729: Galvanometer measurements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# DEFLECTION MAGNETOMETER (Arts. 449-452)
# =============================================================================


@dataclass
class DeflectionMagnetometer:
    """
    Deflection magnetometer for measuring magnetic moments.

    Arts. 449-450: Maxwell described the deflection magnetometer,
    which measures the magnetic moment of a magnet by observing
    the deflection it produces on a compass needle.

    The magnetometer consists of:
        - A small compass needle at the center of a graduated circle
        - A long arm (alidade) for positioning the test magnet
        - The magnet is placed at a known distance r from the needle

    When a magnet with moment M is placed at distance r, the
    deflection theta of the needle is given by:
        tan(theta) = (2 * M) / (H * r^3)  [End-on position]
        tan(theta) = (M) / (H * r^3)      [Broadside position]

    where H is the horizontal component of Earth's field.

    Attributes:
        earth_field_H: H - horizontal Earth field (gauss).
        needle_distance: r - distance from magnet to needle (cm).
        position: "end_on" or "broadside" configuration.

    References:
        Part III, Art. 449: Deflection magnetometer principle.
        Part III, Art. 450: Theory of operation.
    """

    earth_field_H: float = 0.18  # gauss (typical mid-latitude)
    needle_distance: float = 20.0  # cm
    position: str = "end_on"
    needle_moment: float = 1.0  # emu (magnetic moment of compass needle)

    @maxwell_cite(
        449,
        450,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Deflection magnetometer measurement",
    )
    def measure_magnetic_moment(
        self,
        measured_deflection: float,
    ) -> dict[str, float]:
        """
        Measure the magnetic moment of a test magnet.

        Arts. 449-450: From the deflection theta, the magnetic moment M is:

        End-on position (magnet axis points at needle):
            M = (H * r^3 / 2) * tan(theta)

        Broadside position (magnet perpendicular to needle):
            M = (H * r^3) * tan(theta)

        Args:
            measured_deflection: theta - observed deflection (radians).

        Returns:
            Dictionary with:
            - magnetic_moment: M (emu)
            - field_at_needle: B from magnet at needle position (gauss)
            - deflection_degrees: theta in degrees
            - position: Configuration used

        References:
            Part III, Art. 449: Measurement method.
            Part III, Art. 450: Moment calculation.

        Example:
            >>> dm = DeflectionMagnetometer(earth_field_H=0.18, needle_distance=20.0)
            >>> result = dm.measure_magnetic_moment(np.radians(30))
            >>> print(f"Magnetic moment: {result['magnetic_moment']:.2f} emu")
        """
        theta = measured_deflection
        r = self.needle_distance
        H = self.earth_field_H

        if self.position == "end_on":
            # M = (H * r^3 / 2) * tan(theta)
            magnetic_moment = (H * r**3 / 2) * np.tan(theta)
            field_factor = 2  # Field is 2M/r^3
        elif self.position == "broadside":
            # M = (H * r^3) * tan(theta)
            magnetic_moment = (H * r**3) * np.tan(theta)
            field_factor = 1  # Field is M/r^3
        else:
            raise ValueError(f"Unknown position: {self.position}")

        # Field produced by magnet at needle position
        field_at_needle = field_factor * magnetic_moment / r**3

        return {
            "magnetic_moment": magnetic_moment,
            "field_at_needle": field_at_needle,
            "deflection_degrees": np.degrees(theta),
            "deflection_radians": theta,
            "position": self.position,
            "earth_field_H": H,
            "needle_distance": r,
        }

    @maxwell_cite(
        449,
        450,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Predict deflection from known magnetic moment",
    )
    def predict_deflection(
        self,
        magnetic_moment: float,
    ) -> dict[str, float]:
        """
        Predict the deflection for a magnet of known moment.

        Arts. 449-450: Given a magnet with moment M, the expected
        deflection is:

        End-on position:
            theta = arctan(2 * M / (H * r^3))

        Broadside position:
            theta = arctan(M / (H * r^3))

        Args:
            magnetic_moment: M - magnetic moment of test magnet (emu).

        Returns:
            Dictionary with:
            - deflection_radians: theta (radians)
            - deflection_degrees: theta (degrees)
            - tan_theta: tan(theta) value
            - field_ratio: B_magnet / H ratio

        References:
            Part III, Art. 449: Deflection theory.
            Part III, Art. 450: Prediction formula.
        """
        r = self.needle_distance
        H = self.earth_field_H

        if self.position == "end_on":
            tan_theta = 2 * magnetic_moment / (H * r**3)
        elif self.position == "broadside":
            tan_theta = magnetic_moment / (H * r**3)
        else:
            raise ValueError(f"Unknown position: {self.position}")

        theta = np.arctan(tan_theta)
        field_ratio = tan_theta  # B_magnet / H = tan(theta)

        return {
            "deflection_radians": theta,
            "deflection_degrees": np.degrees(theta),
            "tan_theta": tan_theta,
            "field_ratio": field_ratio,
            "magnetic_moment": magnetic_moment,
            "earth_field_H": H,
            "needle_distance": r,
            "position": self.position,
        }


@maxwell_cite(
    451,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Magnetometer Tan-A position (Gauss method)",
)
def magnetometer_tan_position(
    magnetic_moment: float,
    earth_field_H: float,
    distance: float,
    deflection: float,
) -> dict[str, float]:
    """
    Magnetometer measurement in Tan-A (Gauss) position.

    Art. 451: Maxwell described Gauss's method using the tangent
    law for absolute measurement of magnetic moment and Earth's field.

    In the Tan-A position:
        - The magnet is placed with its axis perpendicular to the
          magnetic meridian (East-West orientation)
        - The compass needle aligns with the resultant of Earth's
          field H and the magnet's field B
        - tan(theta) = B / H = (2 * M) / (H * r^3)

    This gives: M/H = (r^3 / 2) * tan(theta)

    By combining with vibration experiments (period T), both M and H
    can be determined absolutely.

    Args:
        magnetic_moment: M - magnetic moment (emu).
        earth_field_H: H - horizontal Earth field (gauss).
        distance: r - distance from magnet to needle (cm).
        deflection: theta - measured deflection (radians).

    Returns:
        Dictionary with:
        - M_over_H: Ratio M/H from deflection
        - computed_M: M calculated from H and deflection
        - field_from_magnet: B at needle position (gauss)
        - tan_deflection: tan(theta)
        - gauss_constant: k = r^3/2 for this setup

    References:
        Part III, Art. 451: Gauss's tangent method.

    Example:
        >>> result = magnetometer_tan_position(
        ...     magnetic_moment=100, earth_field_H=0.18,
        ...     distance=20.0, deflection=np.radians(30)
        ... )
        >>> print(f"M/H ratio: {result['M_over_H']:.2f}")
    """
    tan_theta = np.tan(deflection)

    # Gauss's constant for Tan-A position
    gauss_constant = distance**3 / 2

    # M/H ratio from deflection
    M_over_H = gauss_constant * tan_theta

    # M calculated from known H
    computed_M = earth_field_H * M_over_H

    # Field from magnet at needle
    field_from_magnet = 2 * magnetic_moment / distance**3

    return {
        "M_over_H": M_over_H,
        "computed_M": computed_M,
        "input_M": magnetic_moment,
        "field_from_magnet": field_from_magnet,
        "tan_deflection": tan_theta,
        "gauss_constant": gauss_constant,
        "earth_field_H": earth_field_H,
        "distance": distance,
        "deflection_degrees": np.degrees(deflection),
    }


@maxwell_cite(
    452,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Magnetometer Sin-A position measurement",
)
def magnetometer_sine_position(
    magnetic_moment: float,
    earth_field_H: float,
    distance: float,
    deflection: float,
) -> dict[str, float]:
    """
    Magnetometer measurement in Sin-A position.

    Art. 452: Maxwell described an alternative to the tangent method
    using the sine law, which can be more accurate for large deflections.

    In the Sin-A position (using a sine galvanometer):
        - The entire instrument is rotated until the needle returns
          to its original (zero) position
        - The angle of rotation alpha satisfies:
          sin(alpha) = B / H_res = (2 * M) / (r^3 * H_res)
        - For small angles, sin(alpha) ≈ tan(alpha)

    The sine method avoids the nonlinearity of tan(theta) for large
    deflections and provides better accuracy.

    Args:
        magnetic_moment: M - magnetic moment (emu).
        earth_field_H: H - horizontal Earth field (gauss).
        distance: r - distance from magnet to needle (cm).
        deflection: alpha - rotation angle (radians).

    Returns:
        Dictionary with:
        - M_over_H: Ratio M/H from sine measurement
        - computed_M: M calculated from H and deflection
        - field_from_magnet: B at needle position (gauss)
        - sin_deflection: sin(alpha)
        - comparison_tan: What tan(alpha) would give

    References:
        Part III, Art. 452: Sine method.

    Example:
        >>> result = magnetometer_sine_position(
        ...     magnetic_moment=100, earth_field_H=0.18,
        ...     distance=20.0, deflection=np.radians(30)
        ... )
        >>> print(f"sin(alpha) = {result['sin_deflection']:.4f}")
    """
    sin_alpha = np.sin(deflection)
    tan_alpha = np.tan(deflection)

    # M/H ratio from sine measurement
    gauss_constant = distance**3 / 2
    M_over_H = gauss_constant * sin_alpha

    # M calculated from known H
    computed_M = earth_field_H * M_over_H

    # Field from magnet at needle
    field_from_magnet = 2 * magnetic_moment / distance**3

    # Comparison: error if tangent method were used
    tan_error = (tan_alpha - sin_alpha) / sin_alpha if sin_alpha != 0 else 0

    return {
        "M_over_H": M_over_H,
        "computed_M": computed_M,
        "input_M": magnetic_moment,
        "field_from_magnet": field_from_magnet,
        "sin_deflection": sin_alpha,
        "tan_deflection": tan_alpha,
        "tan_sin_difference": tan_alpha - sin_alpha,
        "tan_error_fraction": tan_error,
        "earth_field_H": earth_field_H,
        "distance": distance,
        "deflection_degrees": np.degrees(deflection),
    }


@maxwell_cite(
    451,
    452,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Gauss's method for absolute H and M determination",
)
def magnetometer_gauss_method(
    tan_deflection: float,
    vibration_period: float,
    distance: float,
    moment_of_inertia: float,
    position: str = "tan_a",
) -> dict[str, float]:
    """
    Gauss's method for absolute determination of H and M.

    Arts. 451-452: Gauss developed a complete method for determining
    both the magnetic moment M of a magnet and the Earth's horizontal
    field H absolutely, using two experiments:

    1. Deflection experiment (this function):
       M/H = (r^3 / 2) * tan(theta)  [Tan-A position]
       M/H = r^3 * tan(theta)        [Tan-B position]

    2. Vibration experiment:
       T = 2*pi * sqrt(I / (M * H))
       M*H = 4*pi^2 * I / T^2

    Combining these:
       H = (2*pi / T) * sqrt(2 * I / (r^3 * tan(theta)))  [Tan-A]
       M = (r^3 * tan(theta) / 2) * H  [Tan-A]

    Args:
        tan_deflection: tan(theta) from deflection experiment.
        vibration_period: T - oscillation period (seconds).
        distance: r - distance in deflection experiment (cm).
        moment_of_inertia: I - moment of inertia of magnet (g*cm^2).
        position: "tan_a" or "tan_b" configuration.

    Returns:
        Dictionary with:
        - earth_field_H: H (gauss)
        - magnetic_moment: M (emu)
        - MH_product: M*H from vibration
        - M_over_H: M/H from deflection
        - position: Configuration used

    References:
        Part III, Arts. 451-452: Gauss's absolute method.

    Example:
        >>> result = magnetometer_gauss_method(
        ...     tan_deflection=0.577,  # tan(30 degrees)
        ...     vibration_period=10.0,
        ...     distance=20.0,
        ...     moment_of_inertia=100.0
        ... )
        >>> print(f"H = {result['earth_field_H']:.4f} gauss")
        >>> print(f"M = {result['magnetic_moment']:.2f} emu")
    """
    # Geometric factor
    if position == "tan_a":
        geo_factor = distance**3 / 2
    elif position == "tan_b":
        geo_factor = distance**3
    else:
        raise ValueError(f"Unknown position: {position}")

    # M/H from deflection
    M_over_H = geo_factor * tan_deflection

    # M*H from vibration: M*H = 4*pi^2 * I / T^2
    MH_product = 4 * np.pi**2 * moment_of_inertia / vibration_period**2

    # Solve for H and M
    # H^2 = (M*H) / (M/H)
    earth_field_H = np.sqrt(MH_product / M_over_H) if M_over_H > 0 else 0
    magnetic_moment = M_over_H * earth_field_H

    return {
        "earth_field_H": earth_field_H,
        "magnetic_moment": magnetic_moment,
        "MH_product": MH_product,
        "M_over_H": M_over_H,
        "position": position,
        "tan_deflection": tan_deflection,
        "deflection_degrees": np.degrees(np.arctan(tan_deflection)),
        "vibration_period": vibration_period,
        "distance": distance,
        "moment_of_inertia": moment_of_inertia,
    }


# =============================================================================
# SUSPENSION SYSTEMS (Arts. 453-456)
# =============================================================================


@dataclass
class UnifilarSuspension:
    """
    Unifilar (single-fiber) suspension system.

    Arts. 453-454: Maxwell described the unifilar suspension, where
    a magnet is suspended by a single torsion fiber. This is the
    basis for many magnetometers.

    The torsion fiber provides a restoring torque:
        tau = -kappa * theta

    where kappa is the torsion constant and theta is the twist angle.

    The equation of motion for a magnet with moment of inertia I:
        I * d^2theta/dt^2 + gamma * dtheta/dt + kappa * theta = M * B * sin(theta)

    For small oscillations:
        omega_0 = sqrt(kappa / I)  [natural frequency without field]
        omega = sqrt((kappa + M*B) / I)  [with aligning field]

    Attributes:
        fiber_length: l - fiber length (cm).
        fiber_radius: r - fiber radius (cm).
        shear_modulus: G - shear modulus of fiber material (dyne/cm^2).
        suspended_mass: m - mass of suspended magnet (g).
        moment_of_inertia: I - moment of inertia (g*cm^2).

    References:
        Part III, Arts. 453-454: Unifilar suspension theory.
    """

    fiber_length: float = 30.0  # cm
    fiber_radius: float = 0.005  # cm
    shear_modulus: float = 3e11  # dyne/cm^2 (quartz)
    suspended_mass: float = 10.0  # g
    moment_of_inertia: float = 100.0  # g*cm^2

    def __post_init__(self):
        """Compute torsion constant from fiber properties."""
        # kappa = (pi * G * r^4) / (2 * l)
        self.torsion_constant = (
            np.pi * self.shear_modulus * self.fiber_radius**4
        ) / (2 * self.fiber_length)

    @maxwell_cite(
        453,
        454,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Unifilar suspension oscillation",
    )
    def oscillation_period(
        self,
        magnetic_moment: float = 0,
        earth_field_H: float = 0.18,
    ) -> dict[str, float]:
        """
        Calculate oscillation period of unifilar suspension.

        Arts. 453-454: The period depends on whether Earth's field
        provides additional restoring torque.

        Without magnetic field (or magnet perpendicular to field):
            T_0 = 2*pi * sqrt(I / kappa)

        With aligning field (magnet parallel to field):
            T = 2*pi * sqrt(I / (kappa + M*H))

        Args:
            magnetic_moment: M - magnetic moment of suspended magnet (emu).
            earth_field_H: H - horizontal Earth field (gauss).

        Returns:
            Dictionary with:
            - period: T (seconds)
            - natural_frequency: omega_0 (rad/s)
            - torsion_constant: kappa
            - MH_contribution: M*H term

        References:
            Part III, Art. 453: Torsion suspension.
            Part III, Art. 454: Oscillation theory.
        """
        kappa = self.torsion_constant
        I = self.moment_of_inertia

        # Natural frequency without field
        omega_0 = np.sqrt(kappa / I) if I > 0 and kappa > 0 else 0
        T_0 = 2 * np.pi / omega_0 if omega_0 > 0 else float("inf")

        # With magnetic field
        MH_term = magnetic_moment * earth_field_H
        omega_with_field = np.sqrt((kappa + MH_term) / I) if I > 0 else 0
        T_with_field = (
            2 * np.pi / omega_with_field if omega_with_field > 0 else float("inf")
        )

        return {
            "period": T_with_field,
            "period_zero_field": T_0,
            "natural_frequency": omega_with_field,
            "natural_frequency_zero_field": omega_0,
            "torsion_constant": kappa,
            "MH_contribution": MH_term,
            "moment_of_inertia": I,
            "magnetic_moment": magnetic_moment,
            "earth_field_H": earth_field_H,
        }


@maxwell_cite(
    453,
    454,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Determine torsion constant of suspension fiber",
)
def torsion_constant(
    fiber_length: float,
    fiber_radius: float,
    shear_modulus: float,
    measured_period: float = None,
    suspended_inertia: float = None,
) -> dict[str, float]:
    """
    Determine the torsion constant of a suspension fiber.

    Arts. 453-454: Maxwell described two methods for determining
    the torsion constant kappa:

    1. Theoretical calculation from fiber properties:
       kappa = (pi * G * r^4) / (2 * l)
       where G is shear modulus, r is radius, l is length.

    2. Experimental determination from oscillation period:
       kappa = 4*pi^2 * I / T^2
       where I is moment of inertia and T is period.

    Args:
        fiber_length: l - fiber length (cm).
        fiber_radius: r - fiber radius (cm).
        shear_modulus: G - shear modulus (dyne/cm^2).
        measured_period: T - measured oscillation period (s). Optional.
        suspended_inertia: I - moment of inertia (g*cm^2). Optional.

    Returns:
        Dictionary with:
        - torsion_constant: kappa (theoretical) dyne*cm/rad
        - experimental_kappa: kappa from period (if measured)
        - discrepancy: Difference between methods
        - fiber_properties: Input parameters

    References:
        Part III, Arts. 453-454: Torsion constant determination.

    Example:
        >>> result = torsion_constant(
        ...     fiber_length=30.0, fiber_radius=0.005,
        ...     shear_modulus=3e11
        ... )
        >>> print(f"Torsion constant: {result['torsion_constant']:.4f} dyne*cm/rad")
    """
    # Theoretical torsion constant
    kappa_theoretical = (np.pi * shear_modulus * fiber_radius**4) / (2 * fiber_length)

    result = {
        "torsion_constant": kappa_theoretical,
        "fiber_length": fiber_length,
        "fiber_radius": fiber_radius,
        "shear_modulus": shear_modulus,
    }

    # Experimental determination if period is provided
    if measured_period is not None and suspended_inertia is not None:
        kappa_experimental = 4 * np.pi**2 * suspended_inertia / measured_period**2
        discrepancy = (
            (kappa_theoretical - kappa_experimental) / kappa_theoretical
            if kappa_theoretical > 0
            else 0
        )

        result.update(
            {
                "experimental_kappa": kappa_experimental,
                "measured_period": measured_period,
                "suspended_inertia": suspended_inertia,
                "discrepancy": discrepancy,
                "discrepancy_percent": discrepancy * 100,
            }
        )

    return result


@dataclass
class BifilarSuspension:
    """
    Bifilar (two-fiber) suspension system.

    Arts. 455-456: Maxwell described the bifilar suspension, where
    a magnet is suspended by two parallel fibers. This configuration
    is used for measuring the horizontal component of Earth's field.

    The bifilar suspension has advantages:
        - No torsion in the fibers (they remain parallel)
        - Restoring torque comes from gravity acting on raised center of mass
        - More stable than unifilar for precise measurements

    When the magnet rotates by angle theta, the fibers twist and the
    magnet rises slightly. The restoring torque is:
        tau = -D * sin(theta)

    where D is the bifilar constant:
        D = (m * g * a * b) / l

    m = suspended mass, g = gravity, a = fiber separation at top,
    b = fiber separation at bottom, l = fiber length.

    Attributes:
        fiber_length: l - fiber length (cm).
        top_separation: a - separation at suspension point (cm).
        bottom_separation: b - separation at magnet (cm).
        suspended_mass: m - mass of magnet (g).

    References:
        Part III, Arts. 455-456: Bifilar suspension theory.
    """

    fiber_length: float = 30.0  # cm
    top_separation: float = 2.0  # cm
    bottom_separation: float = 2.0  # cm
    suspended_mass: float = 50.0  # g

    def __post_init__(self):
        """Compute bifilar constant."""
        g = 980  # cm/s^2
        # D = (m * g * a * b) / l
        self.bifilar_constant = (
            self.suspended_mass * g * self.top_separation * self.bottom_separation
        ) / self.fiber_length

    @maxwell_cite(
        455,
        456,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Bifilar suspension for horizontal force measurement",
    )
    def measure_horizontal_force(
        self,
        equilibrium_angle: float,
        magnetic_moment: float,
    ) -> dict[str, float]:
        """
        Measure Earth's horizontal magnetic force using bifilar suspension.

        Arts. 455-456: In equilibrium, the magnetic torque equals the
        gravitational restoring torque:

            M * H * sin(alpha) = D * sin(theta)

        where alpha is the angle between magnet and meridian, and theta
        is the twist angle of the suspension.

        For the standard configuration (magnet perpendicular to meridian):
            H = D / M  (when in equilibrium at 90 degrees)

        More generally:
            H = (D * sin(theta)) / (M * sin(alpha))

        Args:
            equilibrium_angle: theta - equilibrium deflection (radians).
            magnetic_moment: M - magnetic moment of suspended magnet (emu).

        Returns:
            Dictionary with:
            - earth_field_H: H (gauss)
            - magnetic_torque: M*H (dyne*cm)
            - restoring_torque: D*sin(theta) (dyne*cm)
            - bifilar_constant: D

        References:
            Part III, Art. 455: Bifilar magnetometer.
            Part III, Art. 456: Horizontal force measurement.

        Example:
            >>> bf = BifilarSuspension(fiber_length=30, suspended_mass=50)
            >>> result = bf.measure_horizontal_force(np.radians(30), 100)
            >>> print(f"H = {result['earth_field_H']:.4f} gauss")
        """
        D = self.bifilar_constant
        theta = equilibrium_angle

        # Restoring torque from gravity
        restoring_torque = D * np.sin(theta)

        # In equilibrium: M * H = restoring_torque (for perpendicular orientation)
        # H = D * sin(theta) / M
        earth_field_H = restoring_torque / magnetic_moment if magnetic_moment > 0 else 0

        # Magnetic torque
        magnetic_torque = magnetic_moment * earth_field_H

        return {
            "earth_field_H": earth_field_H,
            "magnetic_torque": magnetic_torque,
            "restoring_torque": restoring_torque,
            "bifilar_constant": D,
            "equilibrium_angle": theta,
            "equilibrium_degrees": np.degrees(theta),
            "magnetic_moment": magnetic_moment,
            "suspended_mass": self.suspended_mass,
            "fiber_length": self.fiber_length,
        }


@maxwell_cite(
    455,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Measure magnetic declination",
)
def magnetic_declination(
    astronomical_azimuth: float,
    magnetic_azimuth: float,
    observatory_latitude: float = None,
    observatory_longitude: float = None,
) -> dict[str, float]:
    """
    Measure magnetic declination (variation).

    Art. 455: Maxwell described the measurement of magnetic declination,
    which is the angle between magnetic north and true (astronomical) north.

    Declination D = astronomical_azimuth - magnetic_azimuth

    Positive declination means magnetic north is east of true north.
    Negative declination means magnetic north is west of true north.

    The measurement requires:
        1. Astronomical observation to determine true north
        2. Magnetic observation using a declinometer or theodolite

    Args:
        astronomical_azimuth: True north reference (radians, from North clockwise).
        magnetic_azimuth: Magnetic north reading (radians, from North clockwise).
        observatory_latitude: Optional latitude for record.
        observatory_longitude: Optional longitude for record.

    Returns:
        Dictionary with:
        - declination: D (radians)
        - declination_degrees: D in degrees
        - declination_minutes: D in arcminutes
        - east_positive: True if declination is east (positive)
        - location: Observatory coordinates if provided

    References:
        Part III, Art. 455: Declination measurement.

    Example:
        >>> result = magnetic_declination(0, np.radians(5))  # Magnetic north 5 deg East
        >>> print(f"Declination: {result['declination_degrees']:.2f} deg East")
    """
    # Declination: angle from true north to magnetic north
    declination = magnetic_azimuth - astronomical_azimuth

    # Normalize to [-pi, pi]
    while declination > np.pi:
        declination -= 2 * np.pi
    while declination < -np.pi:
        declination += 2 * np.pi

    declination_degrees = np.degrees(declination)
    declination_minutes = abs(declination_degrees) * 60

    return {
        "declination": declination,
        "declination_degrees": declination_degrees,
        "declination_minutes": declination_minutes,
        "east_positive": declination > 0,
        "astronomical_azimuth": astronomical_azimuth,
        "magnetic_azimuth": magnetic_azimuth,
        "observatory_latitude": observatory_latitude,
        "observatory_longitude": observatory_longitude,
    }


# =============================================================================
# KEW MAGNETOMETER (Arts. 457-459)
# =============================================================================


@dataclass
class KewMagnetometer:
    """
    Kew Observatory magnetometer for absolute measurements.

    Arts. 457-458: Maxwell described the Kew pattern magnetometer,
    an absolute instrument for measuring Earth's horizontal field H.

    The Kew magnetometer combines:
        1. A unifilar suspension with a permanent magnet
        2. A theodolite for precise angular measurement
        3. A vibration apparatus for period measurement

    The measurement procedure:
        1. Deflection: Place a deflecting magnet at known distance,
           measure deflection angle theta
        2. Vibration: Suspend magnet alone, measure oscillation period T

    From these: H = (2*pi/T) * sqrt(2*I / (r^3 * tan(theta)))

    Attributes:
        fiber_length: Suspension fiber length (cm).
        magnet_length: Length of suspended magnet (cm).
        magnet_mass: Mass of suspended magnet (g).
        telescope_distance: Distance to scale (cm).

    References:
        Part III, Arts. 457-458: Kew magnetometer design.
    """

    fiber_length: float = 60.0  # cm
    magnet_length: float = 10.0  # cm
    magnet_mass: float = 50.0  # g
    telescope_distance: float = 200.0  # cm

    def __post_init__(self):
        """Estimate moment of inertia."""
        # Approximate as thin rod: I = (1/12) * m * L^2
        self.moment_of_inertia = (1 / 12) * self.magnet_mass * self.magnet_length**2

    @maxwell_cite(
        457,
        458,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Kew magnetometer absolute measurement",
    )
    def measure_absolute_H(
        self,
        deflection_angle: float,
        vibration_period: float,
        deflecting_moment: float,
        deflection_distance: float,
    ) -> dict[str, float]:
        """
        Measure Earth's horizontal field H absolutely.

        Arts. 457-458: The Kew method combines deflection and vibration
        measurements for absolute determination of H.

        Deflection experiment:
            M/H = (r^3 / 2) * tan(theta)

        Vibration experiment:
            M*H = 4*pi^2 * I / T^2

        Combined (eliminating M):
            H^2 = (4*pi^2 * I / T^2) / ((r^3 / 2) * tan(theta))
            H = (2*pi / T) * sqrt(2 * I / (r^3 * tan(theta)))

        Args:
            deflection_angle: theta - measured deflection (radians).
            vibration_period: T - oscillation period (seconds).
            deflecting_moment: M - moment of deflecting magnet (emu).
            deflection_distance: r - distance to deflecting magnet (cm).

        Returns:
            Dictionary with:
            - earth_field_H: H (gauss)
            - magnet_moment: M (emu) derived from H
            - MH_product: From vibration
            - M_over_H: From deflection
            - measurement_quality: Consistency check

        References:
            Part III, Arts. 457-458: Absolute measurement method.

        Example:
            >>> km = KewMagnetometer()
            >>> result = km.measure_absolute_H(
            ...     deflection_angle=np.radians(30),
            ...     vibration_period=10.0,
            ...     deflecting_moment=100,
            ...     deflection_distance=30.0
            ... )
            >>> print(f"H = {result['earth_field_H']:.4f} gauss")
        """
        r = deflection_distance
        theta = deflection_angle
        T = vibration_period
        I = self.moment_of_inertia

        tan_theta = np.tan(theta)

        # M/H from deflection
        M_over_H = (r**3 / 2) * tan_theta

        # M*H from vibration
        MH_product = 4 * np.pi**2 * I / T**2

        # H from combined equations
        H_squared = MH_product / M_over_H if M_over_H > 0 else 0
        earth_field_H = np.sqrt(H_squared)

        # M derived from H
        magnetic_moment = M_over_H * earth_field_H

        # Consistency check: M should match deflecting_moment approximately
        # (they may differ due to experimental conditions)
        measurement_quality = (
            1 - abs(magnetic_moment - deflecting_moment) / deflecting_moment
            if deflecting_moment > 0
            else 0
        )

        return {
            "earth_field_H": earth_field_H,
            "magnet_moment": magnetic_moment,
            "deflecting_moment": deflecting_moment,
            "MH_product": MH_product,
            "M_over_H": M_over_H,
            "measurement_quality": measurement_quality,
            "deflection_angle": theta,
            "deflection_degrees": np.degrees(theta),
            "vibration_period": T,
            "deflection_distance": r,
            "moment_of_inertia": I,
        }


@maxwell_cite(
    459,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Vibration magnetometer method",
)
def vibration_magnetometer(
    vibration_period: float,
    moment_of_inertia: float,
    magnetic_moment: float = None,
    earth_field_H: float = None,
) -> dict[str, float]:
    """
    Vibration magnetometer method.

    Art. 459: Maxwell described the vibration method, where a magnet
    suspended by a fiber oscillates in Earth's magnetic field.

    The period of oscillation is:
        T = 2*pi * sqrt(I / (M * H))

    This gives: M*H = 4*pi^2 * I / T^2

    If either M or H is known, the other can be determined.

    Corrections:
        - Torsion of fiber: T_corrected = T * sqrt(1 + tau/MH)
        - Amplitude decay: damping correction
        - Temperature: magnet strength varies with temperature

    Args:
        vibration_period: T - measured period (seconds).
        moment_of_inertia: I - moment of inertia (g*cm^2).
        magnetic_moment: M - magnetic moment (emu). Optional.
        earth_field_H: H - horizontal field (gauss). Optional.

    Returns:
        Dictionary with:
        - MH_product: M*H from vibration
        - derived_M: M if H provided
        - derived_H: H if M provided
        - natural_frequency: omega (rad/s)
        - torsion_correction: Estimate if fiber properties known

    References:
        Part III, Art. 459: Vibration method.

    Example:
        >>> result = vibration_magnetometer(
        ...     vibration_period=10.0,
        ...     moment_of_inertia=100.0,
        ...     earth_field_H=0.18
        ... )
        >>> print(f"M = {result['derived_M']:.2f} emu")
    """
    # M*H = 4*pi^2 * I / T^2
    MH_product = 4 * np.pi**2 * moment_of_inertia / vibration_period**2

    # Natural frequency
    omega = 2 * np.pi / vibration_period

    # Derived quantities
    derived_M = MH_product / earth_field_H if earth_field_H else None
    derived_H = MH_product / magnetic_moment if magnetic_moment else None

    return {
        "MH_product": MH_product,
        "derived_M": derived_M,
        "derived_H": derived_H,
        "natural_frequency": omega,
        "vibration_period": vibration_period,
        "moment_of_inertia": moment_of_inertia,
        "input_magnetic_moment": magnetic_moment,
        "input_earth_field_H": earth_field_H,
    }


# =============================================================================
# DIP CIRCLE (Arts. 460-462)
# =============================================================================


@dataclass
class DipCircle:
    """
    Dip circle for measuring magnetic inclination.

    Arts. 460-461: Maxwell described the dip circle (inclinometer),
    which measures the angle of magnetic dip (inclination).

    The dip circle consists of:
        - A magnetic needle free to rotate in the vertical plane
        - A vertical graduated circle
        - The needle aligns with the total Earth field vector

    The dip angle I is given by:
        tan(I) = Z / H

    where Z is the vertical component and H is the horizontal component.

    Total field: F = sqrt(H^2 + Z^2)

    Attributes:
        needle_length: Length of dip needle (cm).
        needle_mass: Mass of dip needle (g).
        pivot_friction: Estimated friction torque (dyne*cm).
        reading_microscope: Resolution of angle reading (degrees).

    References:
        Part III, Arts. 460-461: Dip circle design and theory.
    """

    needle_length: float = 15.0  # cm
    needle_mass: float = 5.0  # g
    pivot_friction: float = 0.01  # dyne*cm
    reading_microscope: float = 0.1  # degrees

    @maxwell_cite(
        460,
        461,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Dip circle measurement of inclination",
    )
    def measure_dip(
        self,
        observed_dip: float,
        azimuth_from_meridian: float = 0,
    ) -> dict[str, float]:
        """
        Measure magnetic dip (inclination).

        Arts. 460-461: The dip circle measures the angle I between
        the total Earth field and the horizontal plane.

        True dip (needle in magnetic meridian):
            tan(I) = Z / H

        When the dip circle is rotated by azimuth angle alpha from
        the meridian, the apparent dip I' is:
            tan(I') = tan(I) / cos(alpha)

        At alpha = 90 (prime vertical): I' = 90 (needle points straight down)

        Args:
            observed_dip: I or I' - measured dip angle (radians).
            azimuth_from_meridian: alpha - rotation from meridian (radians).

        Returns:
            Dictionary with:
            - observed_dip: I' (radians)
            - true_dip: I corrected for azimuth (radians)
            - vertical_component: Z (gauss) assuming H
            - total_field: F (gauss)
            - dip_components: H, Z, F breakdown

        References:
            Part III, Arts. 460-461: Dip measurement.

        Example:
            >>> dc = DipCircle()
            >>> result = dc.measure_dip(np.radians(60))
            >>> print(f"Dip: {result['observed_dip_degrees']:.1f} degrees")
        """
        I_observed = observed_dip
        alpha = azimuth_from_meridian

        # Correct for azimuth to get true dip
        # tan(I) = tan(I') * cos(alpha)
        tan_I_observed = np.tan(I_observed)
        tan_I_true = tan_I_observed * np.cos(alpha)
        I_true = np.arctan(tan_I_true)

        # Assume typical H to compute Z and F
        H = 0.18  # gauss (typical)
        Z = H * tan_I_true  # Vertical component
        F = np.sqrt(H**2 + Z**2)  # Total field

        return {
            "observed_dip": I_observed,
            "observed_dip_degrees": np.degrees(I_observed),
            "true_dip": I_true,
            "true_dip_degrees": np.degrees(I_true),
            "vertical_component_Z": Z,
            "horizontal_component_H": H,
            "total_field_F": F,
            "azimuth_from_meridian": alpha,
            "azimuth_degrees": np.degrees(alpha),
        }


@maxwell_cite(
    462,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Dip measurement corrections",
)
def dip_correction(
    observed_dip: float,
    needle_reversed_dip: float = None,
    azimuth_error: float = 0,
    eccentricity_error: float = 0,
    temperature: float = 293.15,
    temperature_coefficient: float = -0.0002,
) -> dict[str, float]:
    """
    Apply corrections to dip measurements.

    Art. 462: Maxwell described various corrections needed for
    accurate dip measurement:

    1. Reversal correction: Reading with needle reversed eliminates
       errors from center of gravity offset.
       I = (I_1 + I_2) / 2  [if truly 180 reversal]

    2. Azimuth correction: If dip circle not exactly in meridian:
       tan(I_true) = tan(I_observed) * cos(azimuth_error)

    3. Eccentricity correction: Error from axis not at center:
       delta_I = e * sin(2*I) / (2*R)

    4. Temperature correction: Magnet strength varies with T:
       M(T) = M_0 * (1 + alpha * (T - T_0))

    Args:
        observed_dip: I_obs - measured dip (radians).
        needle_reversed_dip: I_rev - reading with needle reversed. Optional.
        azimuth_error: delta_alpha - azimuth misalignment (radians).
        eccentricity_error: e - eccentricity (cm).
        temperature: T - observation temperature (K).
        temperature_coefficient: alpha - temp coefficient of magnet.

    Returns:
        Dictionary with:
        - corrected_dip: I after all corrections
        - reversal_correction: Correction from reversal
        - azimuth_correction: Correction from azimuth
        - eccentricity_correction: Correction from eccentricity
        - temperature_correction: Correction from temperature

    References:
        Part III, Art. 462: Dip corrections.

    Example:
        >>> result = dip_correction(
        ...     observed_dip=np.radians(60),
        ...     needle_reversed_dip=np.radians(59.5),
        ...     azimuth_error=np.radians(2)
        ... )
        >>> print(f"Corrected dip: {result['corrected_dip_degrees']:.2f} deg")
    """
    corrections = []
    dip = observed_dip

    # 1. Reversal correction
    if needle_reversed_dip is not None:
        dip_reversal = (observed_dip + needle_reversed_dip) / 2
        reversal_correction = dip_reversal - observed_dip
        dip = dip_reversal
    else:
        reversal_correction = 0

    # 2. Azimuth correction
    # tan(I_true) = tan(I) * cos(delta_alpha)
    if azimuth_error != 0:
        tan_I = np.tan(dip)
        tan_I_corrected = tan_I * np.cos(azimuth_error)
        dip_azimuth = np.arctan(tan_I_corrected)
        azimuth_correction = dip_azimuth - dip
        dip = dip_azimuth
    else:
        azimuth_correction = 0

    # 3. Eccentricity correction
    # delta_I = e * sin(2I) / (2R) where R is circle radius
    # Assume R = 10 cm for typical dip circle
    R = 10.0
    if eccentricity_error != 0:
        eccentricity_correction = eccentricity_error * np.sin(2 * dip) / (2 * R)
        dip += eccentricity_correction
    else:
        eccentricity_correction = 0

    # 4. Temperature correction (affects needle magnetism)
    # Small effect on dip, usually neglected
    delta_T = temperature - 293.15
    temperature_correction = temperature_coefficient * delta_T * np.tan(dip)
    # This is a small correction to the effective field ratio

    # Final corrected dip
    corrected_dip = dip

    return {
        "corrected_dip": corrected_dip,
        "corrected_dip_degrees": np.degrees(corrected_dip),
        "observed_dip": observed_dip,
        "observed_dip_degrees": np.degrees(observed_dip),
        "reversal_correction": reversal_correction,
        "reversal_correction_degrees": np.degrees(reversal_correction),
        "azimuth_correction": azimuth_correction,
        "azimuth_correction_degrees": np.degrees(azimuth_correction),
        "eccentricity_correction": eccentricity_correction,
        "eccentricity_correction_degrees": np.degrees(eccentricity_correction),
        "temperature_correction": temperature_correction,
        "temperature": temperature,
        "needle_reversed_dip": needle_reversed_dip,
    }


# =============================================================================
# BALANCE MAGNETOMETER (Arts. 463-464)
# =============================================================================


@dataclass
class BalanceMagnetometer:
    """
    Balance magnetometer for vertical force measurement.

    Arts. 463-464: Maxwell described the balance magnetometer,
    which measures the vertical component Z of Earth's field.

    The balance magnetometer consists of:
        - A horizontal beam with a magnetic needle at one end
        - A counterweight to balance the beam
        - The magnetic torque from Z tilts the beam

    In equilibrium:
        M * Z * cos(theta) = m * g * d * sin(theta)

    where m is the counterweight mass, d is the lever arm,
    and theta is the tilt angle.

    For small angles:
        Z = (m * g * d) / M

    Attributes:
        beam_length: Length of balance beam (cm).
        magnetic_moment: M - moment of needle (emu).
        counterweight_mass: m - counterweight (g).
        counterweight_arm: d - counterweight lever arm (cm).

    References:
        Part III, Arts. 463-464: Balance magnetometer theory.
    """

    beam_length: float = 20.0  # cm
    magnetic_moment: float = 100.0  # emu
    counterweight_mass: float = 1.0  # g
    counterweight_arm: float = 10.0  # cm

    @maxwell_cite(
        463,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Balance magnetometer for vertical force",
    )
    def measure_vertical_force(
        self,
        tilt_angle: float,
    ) -> dict[str, float]:
        """
        Measure vertical component Z using balance magnetometer.

        Art. 463: The equilibrium condition is:

            M * Z * cos(theta) = m * g * d * sin(theta)

        Solving for Z:
            Z = (m * g * d / M) * tan(theta)

        For the null method (theta = 0 with additional weight w):
            Z = (w * g * L) / M

        Args:
            tilt_angle: theta - measured tilt (radians).

        Returns:
            Dictionary with:
            - vertical_component_Z: Z (gauss)
            - magnetic_torque: M*Z*cos(theta)
            - gravitational_torque: m*g*d*sin(theta)
            - tilt_degrees: theta in degrees

        References:
            Part III, Art. 463: Balance magnetometer.

        Example:
            >>> bm = BalanceMagnetometer()
            >>> result = bm.measure_vertical_force(np.radians(5))
            >>> print(f"Z = {result['vertical_component_Z']:.4f} gauss")
        """
        g = 980  # cm/s^2
        theta = tilt_angle
        M = self.magnetic_moment
        m = self.counterweight_mass
        d = self.counterweight_arm

        # Gravitational torque
        tau_gravity = m * g * d * np.sin(theta)

        # Magnetic torque (assuming Z acts on horizontal component of M)
        # tau_magnetic = M * Z * cos(theta)

        # Equilibrium: tau_magnetic = tau_gravity
        # M * Z * cos(theta) = m * g * d * sin(theta)
        # Z = (m * g * d / M) * tan(theta)

        vertical_component_Z = (m * g * d / M) * np.tan(theta)

        magnetic_torque = M * vertical_component_Z * np.cos(theta)

        return {
            "vertical_component_Z": vertical_component_Z,
            "magnetic_torque": magnetic_torque,
            "gravitational_torque": tau_gravity,
            "tilt_angle": theta,
            "tilt_degrees": np.degrees(theta),
            "magnetic_moment": M,
            "counterweight_mass": m,
            "counterweight_arm": d,
            "beam_length": self.beam_length,
        }


@maxwell_cite(
    464,
    part=3,
    chapter="Magnetic Measurements",
    theory_class="maxwell_original",
    description="Measure vertical intensity Z",
)
def vertical_intensity(
    balance_reading: float,
    calibration_constant: float,
    temperature: float = 293.15,
    temperature_coefficient: float = -0.0002,
) -> dict[str, float]:
    """
    Measure vertical intensity Z of Earth's field.

    Art. 464: Maxwell described the final determination of Z using
    the balance magnetometer with proper calibrations.

    The vertical intensity is related to the horizontal intensity H
    and the dip I by:
        Z = H * tan(I)

    The balance magnetometer provides a direct measurement:
        Z = K * reading

    where K is the calibration constant determined from known Z
    or from comparison with H and dip measurements.

    Temperature correction:
        Z(T) = Z_0 * (1 + alpha * (T - T_0))

    Args:
        balance_reading: Scale reading from balance magnetometer.
        calibration_constant: K - instrument constant (gauss/reading).
        temperature: T - observation temperature (K).
        temperature_coefficient: alpha - temp coefficient.

    Returns:
        Dictionary with:
        - vertical_intensity_Z: Z (gauss)
        - temperature_corrected_Z: Z at standard temperature
        - total_field: F if H assumed
        - dip_from_ZH: Dip angle if H assumed
        - measurement_conditions: Temperature, etc.

    References:
        Part III, Art. 464: Vertical intensity determination.

    Example:
        >>> result = vertical_intensity(
        ...     balance_reading=0.42,
        ...     calibration_constant=1.0
        ... )
        >>> print(f"Z = {result['vertical_intensity_Z']:.4f} gauss")
    """
    g = 980  # cm/s^2 (reference)

    # Z from balance reading
    vertical_intensity_Z = calibration_constant * balance_reading

    # Temperature correction to standard (293.15 K)
    delta_T = temperature - 293.15
    temperature_correction = 1 + temperature_coefficient * delta_T
    temperature_corrected_Z = vertical_intensity_Z / temperature_correction

    # Derived quantities (assuming typical H = 0.18 gauss)
    H = 0.18
    total_field = np.sqrt(H**2 + vertical_intensity_Z**2)
    dip = np.arctan(vertical_intensity_Z / H)

    return {
        "vertical_intensity_Z": vertical_intensity_Z,
        "temperature_corrected_Z": temperature_corrected_Z,
        "total_field_F": total_field,
        "dip_angle": dip,
        "dip_degrees": np.degrees(dip),
        "assumed_horizontal_H": H,
        "balance_reading": balance_reading,
        "calibration_constant": calibration_constant,
        "temperature": temperature,
        "temperature_coefficient": temperature_coefficient,
        "temperature_correction_factor": temperature_correction,
    }


# =============================================================================
# COMPREHENSIVE MAGNETIC SURVEY (All Articles 449-464)
# =============================================================================


@dataclass
class MagneticSurvey:
    """
    Complete magnetic survey station using Maxwell's methods.

    This class combines all measurement techniques from
    Arts. 449-464 for a complete determination of Earth's
    magnetic field elements.

    The seven elements determined are:
        1. H - Horizontal intensity
        2. Z - Vertical intensity
        3. F - Total intensity
        4. I - Inclination (dip)
        5. D - Declination (variation)
        6. X - North component
        7. Y - East component

    References:
        Part III, Chapter VII: Complete magnetic measurement system.
    """

    observatory_name: str = "Unknown"
    latitude: float = None
    longitude: float = None
    date: str = None

    @maxwell_cite(
        449,
        450,
        451,
        452,
        453,
        454,
        455,
        456,
        457,
        458,
        459,
        460,
        461,
        462,
        463,
        464,
        part=3,
        chapter="Magnetic Measurements",
        theory_class="maxwell_original",
        description="Complete magnetic survey",
    )
    def complete_survey(
        self,
        # Deflection magnetometer data
        deflection_angle: float,
        deflection_distance: float,
        vibration_period: float,
        magnet_inertia: float,
        # Dip circle data
        observed_dip: float,
        # Declination data
        astronomical_azimuth: float,
        magnetic_azimuth: float,
        # Balance magnetometer data
        balance_reading: float,
        balance_constant: float,
        # Optional dip circle data
        dip_reversed: float = None,
    ) -> dict[str, float]:
        """
        Perform complete magnetic survey using Maxwell's methods.

        This combines all measurements from Arts. 449-464:
            1. H from deflection + vibration (Gauss method)
            2. I from dip circle
            3. D from declination measurement
            4. Z from balance magnetometer
            5. F, X, Y computed from H, Z, D

        Args:
            deflection_angle: From deflection magnetometer.
            deflection_distance: r for deflection.
            vibration_period: T for vibration.
            magnet_inertia: I for suspended magnet.
            observed_dip: From dip circle.
            dip_reversed: Reversed dip reading (optional).
            astronomical_azimuth: True north reference.
            magnetic_azimuth: Magnetic north reading.
            balance_reading: From balance magnetometer.
            balance_constant: Calibration constant.

        Returns:
            Dictionary with all seven magnetic elements and metadata.

        References:
            Part III, Arts. 449-464: Complete survey method.
        """
        # 1. H from Gauss's method (Arts. 451-452, 457-459)
        tan_theta = np.tan(deflection_angle)
        M_over_H = (deflection_distance**3 / 2) * tan_theta
        MH_product = 4 * np.pi**2 * magnet_inertia / vibration_period**2
        H = np.sqrt(MH_product / M_over_H) if M_over_H > 0 else 0
        M = M_over_H * H

        # 2. I from dip circle (Arts. 460-462)
        if dip_reversed is not None:
            dip = (observed_dip + dip_reversed) / 2
        else:
            dip = observed_dip
        dip_corrections = dip_correction(observed_dip, dip_reversed)

        # 3. D from declination (Art. 455)
        decl_data = magnetic_declination(astronomical_azimuth, magnetic_azimuth)

        # 4. Z from balance magnetometer (Arts. 463-464)
        Z_data = vertical_intensity(balance_reading, balance_constant)
        Z = Z_data["vertical_intensity_Z"]

        # 5. Compute remaining elements
        F = np.sqrt(H**2 + Z**2)  # Total intensity
        X = H * np.cos(decl_data["declination"])  # North component
        Y = H * np.sin(decl_data["declination"])  # East component

        # Consistency check: Z should equal H * tan(I)
        Z_from_dip = H * np.tan(dip)
        Z_consistency = 1 - abs(Z - Z_from_dip) / Z if Z > 0 else 0

        return {
            # Horizontal components
            "H": H,
            "X": X,
            "Y": Y,
            # Vertical component
            "Z": Z,
            # Total field
            "F": F,
            # Angles
            "dip_I": dip,
            "dip_degrees": np.degrees(dip),
            "declination_D": decl_data["declination"],
            "declination_degrees": decl_data["declination_degrees"],
            # Derived from magnetometer
            "magnetic_moment_M": M,
            "M_over_H": M_over_H,
            "MH_product": MH_product,
            # Consistency
            "Z_from_dip": Z_from_dip,
            "Z_consistency": Z_consistency,
            # Observatory info
            "observatory": self.observatory_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "date": self.date,
        }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Deflection Magnetometer
    "DeflectionMagnetometer",
    "magnetometer_tan_position",
    "magnetometer_sine_position",
    "magnetometer_gauss_method",
    # Suspension Systems
    "UnifilarSuspension",
    "torsion_constant",
    "BifilarSuspension",
    "magnetic_declination",
    # Kew Magnetometer
    "KewMagnetometer",
    "vibration_magnetometer",
    # Dip Circle
    "DipCircle",
    "dip_correction",
    # Balance Magnetometer
    "BalanceMagnetometer",
    "vertical_intensity",
    # Comprehensive
    "MagneticSurvey",
]
