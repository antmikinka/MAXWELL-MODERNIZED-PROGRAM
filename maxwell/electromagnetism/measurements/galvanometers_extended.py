"""maxwell.electromagnetism.measurements.galvanometers_extended — Galvanometer designs and analysis (Arts. 736-754).

Implements Maxwell's detailed treatment of galvanometers and electrical
measurement instruments from Part IV:

- Tangent galvanometer (Arts. 736-738)
- Sine galvanometer (Art. 739)
- Helmholtz galvanometer (Arts. 741-743)
- Wattmeter (Arts. 744, 746)
- Electrodynamometer (Arts. 747-749)
- Current weigher (Arts. 751-754)
- Joule balance (Q = I^2 R t; standard_math, no article numbers —
  D-17 re-map 2026-08-21: the Joule-balance instrument post-dates the
  1873 Treatise and Arts. 755-757 belong to Ch XVII "Comparison of
  Coils", not to Joule heating)

Galvanometers measure electric current by the magnetic force produced
by the current. Maxwell's analysis (CGS units):

Tangent galvanometer:
    I = (c * H * r / (2 * pi * n)) * tan(theta)

where:
    H = horizontal component of Earth's field (gauss)
    r = coil radius (cm)
    n = number of turns
    theta = deflection angle

Sine galvanometer:
    I = (c * H * r / (2 * pi * n)) * sin(theta)

Helmholtz galvanometer (two coils):
    More uniform field, improved accuracy

CGS Units (explicit-c Gaussian convention, D-16 class):
    Coil fields are computed as B = (2 pi n I)/(c r) and related forms,
    i.e. the current value is read as statamperes (equivalently I/c with
    I in abamperes, since 1 abampere = CONST.C statamperes).  Labels in
    method docstrings that say "abamperes" should be read through this
    convention; the numeric convention is pinned by the Ch XVI qualifying
    tests against an independent Biot-Savart quadrature.
    I = current (statamperes in the explicit-c forms)
    H = magnetic field (gauss = oersted in air)
    r = distance (cm)
    theta = angle (radians or degrees)

Category: A (maxwell_original) — Maxwell's galvanometer theory
(arts. 736-754); the Joule balance is Category B (standard_math) per the
D-17 re-map.

References:
    Part IV, Ch XVI: Observations (Arts. 736-751 head) and Ch XVII head
    (Arts. 752-754, current weigher mapping as adjudicated by this
    program; Arts. 755-757 NOT claimed — see joule_balance D-17 note).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np

from maxwell.config.constants import CONST
from maxwell.math.elliptic_integrals import (
    calc_complete_elliptic_integral_first_kind,
    calc_complete_elliptic_integral_second_kind,
)
from maxwell.meta.citation import maxwell_cite

#: Standard gravity (cm/s^2) for force -> equivalent-mass conversion.
#: Sourced from ``maxwell.config.constants.CONST.G_STANDARD`` (Wave-6
#: constant hygiene; Stage-3 D-33).
_G_STANDARD: float = CONST.G_STANDARD


@dataclass
class TangentGalvanometer:
    """
    Tangent galvanometer for current measurement.

    Arts. 736-738: The tangent galvanometer consists of a vertical
    circular coil with a magnetic needle at the center. The coil
    is aligned with the magnetic meridian, and the current produces
    a field perpendicular to Earth's horizontal field.

    The deflection theta satisfies:
        tan(theta) = B_coil / H_earth

    where:
        B_coil = (2 * pi * n * I) / (c * r)  (coil field at center)
        H_earth = horizontal component of Earth's field

    Solving for current:
        I = (c * r * H_earth / (2 * pi * n)) * tan(theta)

    The galvanometer constant K is:
        K = (c * r * H_earth) / (2 * pi * n)

    so that:
        I = K * tan(theta)

    Attributes:
        coil_radius: r (cm).
        num_turns: Number of turns n.
        earth_field: H_earth (gauss).
    """

    coil_radius: float
    num_turns: int = 1
    earth_field: float = 0.25  # Typical Earth field ~0.25 gauss

    @property
    def galvanometer_constant(self) -> float:
        """
        Calculate the galvanometer constant K.

        K = (c * r * H) / (2 * pi * n)

        Returns:
            K (abamperes).
        """
        return (CONST.C * self.coil_radius * self.earth_field) / (
            2.0 * np.pi * self.num_turns
        )

    @maxwell_cite(
        736,
        737,
        part=4,
        chapter="Tangent Galvanometer",
        theory_class="maxwell_original",
        description="Calculate current from deflection",
    )
    def current_from_deflection(self, deflection_angle_deg: float) -> float:
        """
        Calculate current from observed deflection.

        Art. 736-737: For a tangent galvanometer:
            I = K * tan(theta)

        Args:
            deflection_angle_deg: Observed deflection theta (degrees).

        Returns:
            Current I (abamperes).

        Reference:
            Part IV, Arts. 736-737: Tangent galvanometer.
        """
        theta_rad = np.radians(deflection_angle_deg)
        return self.galvanometer_constant * np.tan(theta_rad)

    @maxwell_cite(
        736,
        737,
        part=4,
        chapter="Tangent Galvanometer",
        theory_class="maxwell_original",
        description="Calculate deflection from current",
    )
    def deflection_from_current(self, current: float) -> float:
        """
        Calculate deflection angle for a given current.

        Art. 736-737: Rearranging the tangent formula:
            theta = arctan(I / K)

        Args:
            current: Current I (abamperes).

        Returns:
            Deflection angle (degrees).

        Reference:
            Part IV, Arts. 736-737: Tangent galvanometer.
        """
        if self.galvanometer_constant == 0:
            return 0.0
        theta_rad = np.arctan(current / self.galvanometer_constant)
        return np.degrees(theta_rad)

    @maxwell_cite(
        736,
        737,
        738,
        part=4,
        chapter="Tangent Galvanometer",
        theory_class="maxwell_original",
        description="Calculate coil magnetic field",
    )
    def coil_field_at_center(self, current: float) -> float:
        """
        Calculate magnetic field at coil center.

        Art. 736-738: The field at the center of a circular coil:
            B = (2 * pi * n * I) / (c * r)

        Args:
            current: Current I (abamperes).

        Returns:
            Magnetic field B (gauss).

        Reference:
            Part IV, Arts. 736-738: Coil field calculation.
        """
        return (2.0 * np.pi * self.num_turns * current) / (CONST.C * self.coil_radius)


@maxwell_cite(
    736,
    737,
    738,
    part=4,
    chapter="Tangent Galvanometer",
    theory_class="maxwell_original",
    description="Create and analyze tangent galvanometer",
)
def tangent_galvanometer(
    coil_radius: float,
    num_turns: int,
    earth_field: float = 0.25,
    current: float = None,
    deflection_angle: float = None,
) -> dict[str, float]:
    """
    Calculate tangent galvanometer properties.

    Arts. 736-738: Complete analysis of a tangent galvanometer:

    The tangent galvanometer measures current by balancing:
    - Earth's horizontal magnetic field H (north-south)
    - Coil's magnetic field B (east-west, perpendicular to coil plane)

    The needle deflects by angle theta where:
        tan(theta) = B / H

    This gives:
        I = (c * r * H / (2 * pi * n)) * tan(theta)

    The galvanometer is most accurate for deflections between
    30 and 60 degrees (tan is well-behaved, needle response is linear).

    Args:
        coil_radius: Coil radius r (cm).
        num_turns: Number of turns n.
        earth_field: Horizontal Earth field H (gauss, default 0.25).
        current: Current I (abamperes), optional.
        deflection_angle: Deflection theta (degrees), optional.

    Returns:
        Dictionary with:
        - galvanometer_constant: K = c*r*H/(2*pi*n)
        - coil_field: B at center for given current
        - current: Calculated from deflection (if provided)
        - deflection: Calculated from current (if provided)
        - sensitivity: d(theta)/dI at small angles

    Reference:
        Part IV, Arts. 736-738: Tangent galvanometer.

    Example:
        >>> result = tangent_galvanometer(
        ...     coil_radius=15.0,  # 15 cm
        ...     num_turns=10,
        ...     earth_field=0.25,
        ...     deflection_angle=45.0
        ... )
        >>> print(f"Current = {result['current']:.6f} abamperes")
    """
    galvo = TangentGalvanometer(coil_radius, num_turns, earth_field)

    result = {
        "galvanometer_constant": galvo.galvanometer_constant,
        "coil_radius": coil_radius,
        "num_turns": num_turns,
        "earth_field": earth_field,
    }

    # Coil field at center (if current given)
    if current is not None:
        result["coil_field"] = galvo.coil_field_at_center(current)
        result["calculated_deflection"] = galvo.deflection_from_current(current)

    # Current from deflection (if deflection given)
    if deflection_angle is not None:
        result["current"] = galvo.current_from_deflection(deflection_angle)

    # Sensitivity (d theta / d I at I=0)
    # theta = arctan(I/K), so d theta/dI = 1/(K*(1+(I/K)^2))
    # At I=0: sensitivity = 1/K (radians per abampere)
    sensitivity = 1.0 / galvo.galvanometer_constant  # rad/abA
    result["sensitivity_rad_per_abA"] = sensitivity
    result["sensitivity_deg_per_abA"] = np.degrees(sensitivity)

    return result


@dataclass
class SineGalvanometer:
    """
    Sine galvanometer for current measurement.

    Art. 739: The sine galvanometer differs from the tangent
    galvanometer in that the coil is rotated to follow the needle,
    keeping the coil field perpendicular to the needle.

    The deflection theta satisfies:
        sin(theta) = B_coil / H_earth

    Solving for current:
        I = (c * r * H_earth / (2 * pi * n)) * sin(theta)

    The sine galvanometer has advantages:
    - More uniform scale
    - Better for larger deflections
    - Easier to read accurately

    Attributes:
        coil_radius: r (cm).
        num_turns: Number of turns n.
        earth_field: H_earth (gauss).
    """

    coil_radius: float
    num_turns: int = 1
    earth_field: float = 0.25

    @property
    def galvanometer_constant(self) -> float:
        """
        Calculate the galvanometer constant K.

        Same as tangent galvanometer:
            K = (c * r * H) / (2 * pi * n)

        Returns:
            K (abamperes).
        """
        return (CONST.C * self.coil_radius * self.earth_field) / (
            2.0 * np.pi * self.num_turns
        )

    @maxwell_cite(
        739,
        part=4,
        chapter="Sine Galvanometer",
        theory_class="maxwell_original",
        description="Calculate current from deflection",
    )
    def current_from_deflection(self, deflection_angle_deg: float) -> float:
        """
        Calculate current from observed deflection.

        Art. 739: For a sine galvanometer:
            I = K * sin(theta)

        Args:
            deflection_angle_deg: Observed deflection theta (degrees).

        Returns:
            Current I (abamperes).
        """
        theta_rad = np.radians(deflection_angle_deg)
        return self.galvanometer_constant * np.sin(theta_rad)

    @maxwell_cite(
        739,
        part=4,
        chapter="Sine Galvanometer",
        theory_class="maxwell_original",
        description="Calculate deflection from current",
    )
    def deflection_from_current(self, current: float) -> float:
        """
        Calculate deflection angle for a given current.

        Art. 739: Rearranging the sine formula:
            theta = arcsin(I / K)

        Note: This is only valid for |I| <= K (|sin(theta)| <= 1).

        Args:
            current: Current I (abamperes).

        Returns:
            Deflection angle (degrees), or None if current too large.
        """
        if self.galvanometer_constant == 0:
            return 0.0
        ratio = current / self.galvanometer_constant
        if abs(ratio) > 1.0:
            return None  # Beyond range
        theta_rad = np.arcsin(ratio)
        return np.degrees(theta_rad)


@maxwell_cite(
    739,
    part=4,
    chapter="Sine Galvanometer",
    theory_class="maxwell_original",
    description="Create and analyze sine galvanometer",
)
def sine_galvanometer(
    coil_radius: float,
    num_turns: int,
    earth_field: float = 0.25,
    current: float = None,
    deflection_angle: float = None,
) -> dict[str, float]:
    """
    Calculate sine galvanometer properties.

    Art. 739: Complete analysis of a sine galvanometer:

    The coil is rotated to keep its field perpendicular to the
    magnetic needle. The rotation angle theta satisfies:
        sin(theta) = B_coil / H_earth

    This gives:
        I = (c * r * H / (2 * pi * n)) * sin(theta)

    The sine galvanometer has a more uniform scale than the
    tangent type and is better for larger deflections.

    Args:
        coil_radius: Coil radius r (cm).
        num_turns: Number of turns n.
        earth_field: Horizontal Earth field H (gauss).
        current: Current I (abamperes), optional.
        deflection_angle: Deflection theta (degrees), optional.

    Returns:
        Dictionary with galvanometer analysis.

    Reference:
        Part IV, Art. 739: Sine galvanometer.
    """
    galvo = SineGalvanometer(coil_radius, num_turns, earth_field)

    result = {
        "galvanometer_constant": galvo.galvanometer_constant,
        "coil_radius": coil_radius,
        "num_turns": num_turns,
        "earth_field": earth_field,
        "type": "sine",
    }

    if current is not None:
        result["deflection"] = galvo.deflection_from_current(current)
        result["max_current"] = galvo.galvanometer_constant  # When sin(theta)=1

    if deflection_angle is not None:
        result["current"] = galvo.current_from_deflection(deflection_angle)

    return result


@dataclass
class HelmholtzGalvanometer:
    """
    Helmholtz galvanometer with two coils.

    Arts. 741-743: The Helmholtz arrangement uses two identical
    circular coils separated by a distance equal to their radius.
    This produces a highly uniform magnetic field in the region
    between the coils.

    For two coils of radius r, separated by distance r:
        B_center = (32 * pi * n * I) / (5 * sqrt(5) * c * r)
                 = 2 * (4/5)^(3/2) * (2 * pi * n * I) / (c * r)
                 ≈ 1.4311 * (single-coil center field)

    (Each coil contributes 2 pi n I r^2 / (c (r^2 + (r/2)^2)^(3/2));
    the earlier 8/(5 sqrt(5)) prefactor was short by a factor of 4 —
    repaired 2026-08-21 against an independent Biot-Savart quadrature
    in tests/test_articles_ch16_observations_730_750.py and the
    adjudicated EMU form 32 pi n I / (5 sqrt(5) a) of
    maxwell.instruments.helmholtz.HelmholtzCoil.field_at_center.)

    The field uniformity is much better than a single coil:
        - Single coil: B varies as 1/r^3 away from center
        - Helmholtz: B uniform to 1% over ~r/10 region

    Attributes:
        coil_radius: r (cm).
        num_turns_per_coil: Turns n per coil.
        coil_separation: Distance between coils (default = r).
        earth_field: H_earth (gauss).
    """

    coil_radius: float
    num_turns_per_coil: int = 1
    coil_separation: float = None  # Default = radius for Helmholtz
    earth_field: float = 0.25

    def __post_init__(self):
        """Set coil separation to radius if not specified."""
        if self.coil_separation is None:
            self.coil_separation = self.coil_radius

    @property
    def helmholtz_factor(self) -> float:
        """
        Helmholtz field factor (pair midpoint field / single-coil center
        field).

        For ideal Helmholtz (separation = radius):
            factor = 2 * (4/5)^(3/2) = 16 / (5 * sqrt(5)) ≈ 1.4311

        (Greater than 1: two coils at half-radius separation produce a
        STRONGER midpoint field than one coil at its centre.  Repaired
        2026-08-21: the former special-case value 8/(5 sqrt(5)) = 0.7155
        was the (4/5)^(3/2) coefficient alone and contradicted both the
        general-separation branch below — which yields 1.4311 at d = r —
        and Biot-Savart quadrature.)

        Returns:
            Field factor relative to a single coil.
        """
        if self.coil_separation == self.coil_radius:
            return 16.0 / (5.0 * np.sqrt(5.0))
        # General formula for arbitrary separation
        r = self.coil_radius
        d = self.coil_separation
        return (r**3) * (
            1 / (r**2 + (d / 2) ** 2) ** (3 / 2) + 1 / (r**2 + (d / 2) ** 2) ** (3 / 2)
        )

    @property
    def galvanometer_constant(self) -> float:
        """
        Calculate the Helmholtz galvanometer constant.

        K = (c * r * H / (2 * pi * n)) * helmholtz_factor

        Returns:
            K (abamperes).
        """
        single_coil_K = (CONST.C * self.coil_radius * self.earth_field) / (
            2.0 * np.pi * self.num_turns_per_coil
        )
        return single_coil_K / self.helmholtz_factor

    @maxwell_cite(
        741,
        742,
        743,
        part=4,
        chapter="Helmholtz Galvanometer",
        theory_class="maxwell_original",
        description="Calculate field at center",
    )
    def field_at_center(self, current: float) -> float:
        """
        Calculate magnetic field at the Helmholtz-pair midpoint.

        Arts. 741-743: For ideal Helmholtz coils (separation = radius),
        each coil contributes 2 pi n I r^2 / (c (r^2 + (r/2)^2)^(3/2)),
        hence

            B = (32 * pi * n * I) / (5 * sqrt(5) * c * r)

        (explicit-c convention: the numeric current reads as statamperes;
        see module docstring.  Prefactor repaired 2026-08-21 — the former
        8/(5 sqrt(5)) form was short by a factor of 4.)

        Args:
            current: Current I (statamperes in the explicit-c form).

        Returns:
            Magnetic field B (gauss).
        """
        return (32.0 * np.pi * self.num_turns_per_coil * current) / (
            5.0 * np.sqrt(5.0) * CONST.C * self.coil_radius
        )

    @maxwell_cite(
        741,
        742,
        743,
        part=4,
        chapter="Helmholtz Galvanometer",
        theory_class="maxwell_original",
        description="Calculate current from deflection",
    )
    def current_from_deflection(self, deflection_angle_deg: float) -> float:
        """
        Calculate current from observed deflection.

        Arts. 741-743: Same tangent formula as single coil,
        but with different constant.

            I = K * tan(theta)

        Args:
            deflection_angle_deg: Deflection theta (degrees).

        Returns:
            Current I (abamperes).
        """
        theta_rad = np.radians(deflection_angle_deg)
        return self.galvanometer_constant * np.tan(theta_rad)


@maxwell_cite(
    741,
    742,
    743,
    part=4,
    chapter="Helmholtz Galvanometer",
    theory_class="maxwell_original",
    description="Create and analyze Helmholtz galvanometer",
)
def helmholtz_galvanometer(
    coil_radius: float,
    num_turns_per_coil: int,
    coil_separation: float = None,
    earth_field: float = 0.25,
    current: float = None,
    deflection_angle: float = None,
) -> dict[str, float]:
    """
    Calculate Helmholtz galvanometer properties.

    Arts. 741-743: Complete analysis of a Helmholtz galvanometer:

    The Helmholtz arrangement provides a highly uniform magnetic field
    by using two identical coils separated by their radius. This gives:

        B_center = (32 * pi * n * I) / (5 * sqrt(5) * c * r)
                 = (16 / (5 * sqrt(5))) * (single-coil center field)

    The field uniformity is excellent near the center, making this
    ideal for precision measurements.

    Advantages over single coil:
    - Uniform field over larger region
    - Reduced sensitivity to needle position
    - Better accuracy for precision work

    Args:
        coil_radius: Coil radius r (cm).
        num_turns_per_coil: Turns n per coil.
        coil_separation: Distance between coils (default = r).
        earth_field: Horizontal Earth field H (gauss).
        current: Current I (abamperes), optional.
        deflection_angle: Deflection theta (degrees), optional.

    Returns:
        Dictionary with Helmholtz galvanometer analysis.

    Reference:
        Part IV, Arts. 741-743: Helmholtz galvanometer.
    """
    galvo = HelmholtzGalvanometer(
        coil_radius, num_turns_per_coil, coil_separation, earth_field
    )

    result = {
        "galvanometer_constant": galvo.galvanometer_constant,
        "helmholtz_factor": galvo.helmholtz_factor,
        "coil_radius": coil_radius,
        "num_turns_per_coil": num_turns_per_coil,
        "coil_separation": galvo.coil_separation,
        "earth_field": earth_field,
        "is_ideal_helmholtz": coil_separation is None or coil_separation == coil_radius,
    }

    if current is not None:
        result["field_at_center"] = galvo.field_at_center(current)
        result["calculated_deflection"] = np.degrees(
            np.arctan(current / galvo.galvanometer_constant)
        )

    if deflection_angle is not None:
        result["current"] = galvo.current_from_deflection(deflection_angle)

    return result


@dataclass
class Electrodynamometer:
    """
    Electrodynamometer for current and power measurement.

    Arts. 747-749: An electrodynamometer uses the force between
    two current-carrying coils to measure current or power.

    Construction:
    - Fixed coil (field coil): Produces magnetic field
    - Movable coil: Experiences torque in the field
    - Spring or torsion fiber: Provides restoring torque

    For current measurement:
        Torque = k * I1 * I2 * sin(theta)

    For wattmeter (power measurement):
        - Fixed coil carries load current I
        - Movable coil carries current proportional to voltage V
        - Torque is proportional to V * I = power

    The deflection theta at equilibrium:
        theta = (k / spring_constant) * I1 * I2

    Attributes:
        mutual_inductance_gradient: dM/dtheta (abhenry/radian)
        spring_constant: Restoring torque per radian
        fixed_coil_turns: N1
        movable_coil_turns: N2
        coil_area: Area of movable coil (cm^2)
    """

    mutual_inductance_gradient: float = 1e-6  # abhenry/radian
    spring_constant: float = 1.0  # dyne*cm/radian
    fixed_coil_turns: int = 100
    movable_coil_turns: int = 50
    coil_area: float = 1.0  # cm^2

    @maxwell_cite(
        747,
        748,
        749,
        part=4,
        chapter="Electrodynamometer",
        theory_class="maxwell_original",
        description="Calculate torque on movable coil",
    )
    def torque(self, current1: float, current2: float, angle_rad: float) -> float:
        """
        Calculate electromagnetic torque on movable coil.

        Arts. 747-749: The torque on the movable coil is:
            T = I1 * I2 * (dM/dtheta) * sin(theta)

        where M is the mutual inductance between coils.

        Args:
            current1: Current in fixed coil (abamperes).
            current2: Current in movable coil (abamperes).
            angle_rad: Angle between coil planes (radians).

        Returns:
            Torque T (dyne*cm).
        """
        return current1 * current2 * self.mutual_inductance_gradient * np.sin(angle_rad)

    @maxwell_cite(
        747,
        748,
        749,
        part=4,
        chapter="Electrodynamometer",
        theory_class="maxwell_original",
        description="Calculate equilibrium deflection",
    )
    def equilibrium_deflection(self, current1: float, current2: float) -> float:
        """
        Calculate equilibrium deflection angle.

        Arts. 747-749: At equilibrium, electromagnetic torque
        equals restoring torque:
            I1 * I2 * (dM/dtheta) * sin(theta) = k * theta

        For small angles (sin(theta) ~ theta):
            theta = (I1 * I2 / k) * (dM/dtheta)

        Args:
            current1: Fixed coil current (abamperes).
            current2: Movable coil current (abamperes).

        Returns:
            Deflection angle (radians).
        """
        # Small angle approximation
        return (
            current1 * current2 * self.mutual_inductance_gradient
        ) / self.spring_constant


@maxwell_cite(
    744,
    746,
    part=4,
    chapter="Wattmeter",
    theory_class="maxwell_original",
    description="Calculate power using electrodynamometer wattmeter",
)
def wattmeter(
    voltage: float,
    current: float,
    wattmeter_constant: float = 1.0,
    power_factor: float = 1.0,
) -> dict[str, float]:
    """
    Calculate power measurement using an electrodynamometer wattmeter.

    Arts. 744, 746: A wattmeter measures electrical power using an
    electrodynamometer where:
    - Fixed coil carries the load current I
    - Movable coil carries a current proportional to voltage V
    - Deflection is proportional to V * I = power

    For AC circuits:
        P = V * I * cos(phi) = V * I * power_factor

    The wattmeter reading:
        Reading = wattmeter_constant * deflection

    Args:
        voltage: Voltage V (volts).
        current: Current I (amperes).
        wattmeter_constant: Calibration constant.
        power_factor: cos(phi) for AC (default 1.0 for DC).

    Returns:
        Dictionary with:
        - power: True power (watts)
        - apparent_power: V * I (volt-amperes)
        - deflection: Instrument deflection
        - power_factor: cos(phi)

    Reference:
        Part IV, Arts. 744, 746: Wattmeter.

    Example:
        >>> result = wattmeter(voltage=120.0, current=10.0)
        >>> print(f"Power = {result['power']} watts")
    """
    # True power
    power = voltage * current * power_factor

    # Apparent power
    apparent_power = voltage * current

    # Wattmeter deflection (proportional to power)
    deflection = power / wattmeter_constant if wattmeter_constant > 0 else 0

    return {
        "power": power,
        "apparent_power": apparent_power,
        "reactive_power": apparent_power * np.sqrt(1 - power_factor**2),
        "power_factor": power_factor,
        "phase_angle": np.degrees(np.arccos(power_factor)),
        "deflection": deflection,
        "wattmeter_constant": wattmeter_constant,
    }


@maxwell_cite(
    747,
    748,
    749,
    part=4,
    chapter="Electrodynamometer",
    theory_class="maxwell_original",
    description="Create and analyze electrodynamometer",
)
def electrodynamometer(
    current1: float,
    current2: float,
    mutual_inductance_gradient: float = 1e-6,
    spring_constant: float = 1.0,
) -> dict[str, float]:
    """
    Analyze electrodynamometer operation.

    Arts. 747-749: Complete analysis of an electrodynamometer:

    The torque on the movable coil:
        T = I1 * I2 * (dM/dtheta) * sin(theta)

    At equilibrium with restoring spring:
        T_electromagnetic = T_spring
        I1 * I2 * (dM/dtheta) * sin(theta) = k * theta

    For small angles:
        theta = (I1 * I2 / k) * (dM/dtheta)

    The electrodynamometer can measure:
    - Current (with coils in series)
    - Power (wattmeter configuration)
    - Mutual inductance

    Args:
        current1: Fixed coil current (abamperes).
        current2: Movable coil current (abamperes).
        mutual_inductance_gradient: dM/dtheta (abhenry/radian).
        spring_constant: k (dyne*cm/radian).

    Returns:
        Dictionary with:
        - torque: Electromagnetic torque at 90 degrees
        - equilibrium_deflection: Small angle deflection
        - sensitivity: d(theta)/dI

    Reference:
        Part IV, Arts. 747-749: Electrodynamometer.
    """
    # Maximum torque (at 90 degrees)
    max_torque = current1 * current2 * mutual_inductance_gradient

    # Equilibrium deflection (small angle approximation)
    theta_eq = (current1 * current2 * mutual_inductance_gradient) / spring_constant

    # Sensitivity (radians per abampere^2)
    sensitivity = mutual_inductance_gradient / spring_constant

    return {
        "current1": current1,
        "current2": current2,
        "max_torque": max_torque,
        "equilibrium_deflection_rad": theta_eq,
        "equilibrium_deflection_deg": np.degrees(theta_eq),
        "sensitivity": sensitivity,
        "mutual_inductance_gradient": mutual_inductance_gradient,
        "spring_constant": spring_constant,
    }


def _coaxial_mutual_inductance_emu(a: float, b: float, z: float) -> float:
    """
    Mutual inductance (EMU, centimetres) of two coaxial circular filaments.

    Maxwell's elliptic-integral formula (Treatise, the Arts. 703-704
    methods as applied to the current weigher, Arts. 751-754):

        M = 4 pi sqrt(a b) [ (2/k - k) K(k^2) - (2/k) E(k^2) ]
        k^2 = 4 a b / [ (a + b)^2 + z^2 ]

    Pure EMU convention: inductance has dimensions of length (mu_0 = 4 pi
    is absorbed into the definition), no factor of c appears. K and E are
    evaluated by the scipy-backed complete elliptic integrals of
    ``maxwell.math.elliptic_integrals`` (machine precision for all
    0 <= k^2 < 1; the k^2 -> 1 limit is the filament-coincident
    divergence of the Neumann integral and is clamped).

    Args:
        a: Radius of first loop (cm).
        b: Radius of second loop (cm).
        z: Axial separation of the loop planes (cm).

    Returns:
        Mutual inductance M (cm, EMU).
    """
    if a <= 0.0 or b <= 0.0:
        return 0.0
    s_sq = (a + b) ** 2 + z * z
    k_sq = 4.0 * a * b / s_sq
    # k^2 = 1 only for coincident filaments (self-inductance divergence);
    # clamp to keep K finite for numerically degenerate inputs.
    k_sq = min(k_sq, 1.0 - 1e-15)
    k = np.sqrt(k_sq)
    K = calc_complete_elliptic_integral_first_kind(k)
    E = calc_complete_elliptic_integral_second_kind(k)
    return 4.0 * np.pi * np.sqrt(a * b) * ((2.0 / k - k) * K - (2.0 / k) * E)


def _coaxial_mutual_gradient_emu(a: float, b: float, z: float) -> float:
    """
    Axial gradient dM/dz (dimensionless, EMU) of the coaxial-filament
    mutual inductance — analytic derivative of Maxwell's elliptic formula.

    With s^2 = (a + b)^2 + z^2, m = k^2 = 4 a b / s^2, one has
    dk/dz = -k z / s^2 and d/dk [(2/k - k) K - (2/k) E]
    = [ (2 - k^2) E / (1 - k^2) - 2 K ] / k^2, hence

        dM/dz = (4 pi sqrt(a b) z / (k s^2))
                * [ 2 K(m) - (2 - m) E(m) / (1 - m) ] .

    Checks: odd in z (attraction symmetry), exactly 0 at z = 0, and for
    z >> a + b reduces to -6 pi^2 a^2 b^2 / z^4, the derivative of the
    dipole-limit mutual inductance M -> 2 pi^2 a^2 b^2 / z^3.

    Args:
        a: Radius of first loop (cm).
        b: Radius of second loop (cm).
        z: Axial separation of the loop planes (cm).

    Returns:
        dM/dz (dimensionless in EMU).
    """
    if a <= 0.0 or b <= 0.0 or z == 0.0:
        return 0.0  # gradient vanishes by symmetry at z = 0
    s_sq = (a + b) ** 2 + z * z
    m = 4.0 * a * b / s_sq
    m = min(m, 1.0 - 1e-15)
    k = np.sqrt(m)
    K = calc_complete_elliptic_integral_first_kind(k)
    E = calc_complete_elliptic_integral_second_kind(k)
    bracket = 2.0 * K - (2.0 - m) * E / (1.0 - m)
    return 4.0 * np.pi * np.sqrt(a * b) * z / (k * s_sq) * bracket


@maxwell_cite(
    751,
    752,
    753,
    754,
    part=4,
    chapter="Current Weigher",
    theory_class="maxwell_original",
    description="Calculate force in current weigher",
)
def current_weigher(
    current: float,
    coil_radius: float,
    num_turns_fixed: int,
    num_turns_movable: int,
    coil_separation: float,
) -> dict[str, float]:
    """
    Calculate force in a current weigher (ampere balance).

    Arts. 751-754: A current weigher measures current by weighing
    the axial magnetic force between two coaxial coils. This is an
    absolute method: the force is fixed by the geometry through the
    mutual inductance, with no empirical calibration factor.

    Pure EMU formulation (no mu_0, no factor of c): the generalized
    electromagnetic force conjugate to a coordinate x is

        F_x = I1 * I2 * dM/dx

    and when a circuit is weighed against itself (I1 = I2 = I, the
    weigher configuration)

        F = I^2 * dM/dx ,

    with M the mutual inductance in centimetres, I in abamperes and
    F in dynes. For N1 fixed and N2 movable turns of common radius r,
    M_total = N1 * N2 * M_loop, where the mutual inductance of two
    coaxial circular filaments is Maxwell's elliptic-integral formula

        M_loop = 4 pi r [ (2/k - k) K(k^2) - (2/k) E(k^2) ] ,
        k^2 = 4 r^2 / (4 r^2 + x^2) ,

    and dM_loop/dx is its analytic derivative (see
    ``_coaxial_mutual_gradient_emu``). The current is read from the
    weighed force by

        I = sqrt(F / (N1 * N2 * dM_loop/dx)) .

    Args:
        current: Current I (abamperes), identical in both coils.
        coil_radius: Radius of both coils (cm, assumed equal).
        num_turns_fixed: N1 turns in the fixed coil.
        num_turns_movable: N2 turns in the movable coil.
        coil_separation: Axial distance x between coil planes (cm).

    Returns:
        Dictionary with:
        - force: Axial force on the movable coil in the direction of
          increasing separation (dynes); negative = attraction for
          currents in the same sense
        - equivalent_mass: force / g_standard (grams)
        - dM_dx: Total gradient N1 * N2 * dM_loop/dx (dimensionless)
        - mutual_inductance: Total M at this separation (cm, EMU)

    Reference:
        Part IV, Arts. 751-754: Current weigher.

    Example:
        >>> result = current_weigher(
        ...     current=1.0,
        ...     coil_radius=10.0,
        ...     num_turns_fixed=100,
        ...     num_turns_movable=50,
        ...     coil_separation=15.0
        ... )
        >>> print(f"Force = {result['force']:.4e} dynes")
    """
    r = coil_radius
    d = coil_separation
    N1 = num_turns_fixed
    N2 = num_turns_movable

    # Mutual inductance of one coaxial filament pair (cm, EMU) and its
    # exact axial gradient — no c^2, no invented geometry factor.
    M_loop = _coaxial_mutual_inductance_emu(r, r, d)
    dM_loop_dx = _coaxial_mutual_gradient_emu(r, r, d)

    # N1 * N2 turn pairs act in series: M_total = N1 * N2 * M_loop.
    dM_dx = N1 * N2 * dM_loop_dx

    # Arts. 751-754 (EMU): F = I^2 dM/dx, force in dynes for I in
    # abamperes and M in centimetres.
    force = current**2 * dM_dx

    # Equivalent mass that balances the force (F = m g)
    equivalent_mass = force / _G_STANDARD

    return {
        "force": force,
        "equivalent_mass": equivalent_mass,
        "dM_dx": dM_dx,
        "mutual_inductance": N1 * N2 * M_loop,
        "current": current,
        "coil_radius": coil_radius,
        "num_turns_fixed": N1,
        "num_turns_movable": N2,
        "coil_separation": d,
    }


# D-17 re-map (2026-08-21, Stage-3 defect register S2): the former
# citation of Treatise Arts. 755-757 was anachronistic on two counts —
# (1) Ch XVII (Arts. 752-757) of Part IV is "Comparison of Coils", not
# Joule heating; (2) the Joule-balance instrument (weighing a current by
# its resistive heat) was developed in the 1880s, after the 1873
# Treatise.  Q = I^2 R t itself is Joule's 1841 law — established
# physics, hence standard_math with NO article numbers.  Genuine Ch XVII
# coil-comparison methods are a separate work package (not faked here):
# they are implemented, article by article (Arts. 752-757), in
# maxwell/electromagnetism/coil_comparison/ (CIRCUITUS, Wave 7).
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Joule heating Q = I^2 R t (Joule 1841; anachronistic as a Treatise instrument)",
)
def joule_balance(
    current: float,
    resistance: float,
    time: float,
    heat_capacity: float = None,
) -> dict[str, float]:
    """
    Calculate heat production using Joule's law (Joule balance).

    D-17 re-map (2026-08-21): this function implements the generic Joule
    heating law (Joule, 1841), NOT any Treatise article:

        Q = I^2 * R * t

    where:
        Q = heat energy (ergs in CGS, joules in SI)
        I = current
        R = resistance
        t = time

    Anachronism note: the Joule-balance instrument post-dates the 1873
    Treatise, and Arts. 755-757 belong to Ch XVII "Comparison of Coils".
    No article numbers are claimed (see decorator comment).

    The mechanical equivalent of heat:
        1 calorie = 4.184e7 ergs = 4.184 joules

    As a modern extension, a Joule balance measures current by the heat
    produced, providing an absolute current standard.

    Temperature rise (if heat capacity known):
        Delta_T = Q / C

    Args:
        current: Current I (amperes).
        resistance: Resistance R (ohms).
        time: Duration t (seconds).
        heat_capacity: C (ergs/degree), optional.

    Returns:
        Dictionary with:
        - heat_energy: Q (ergs)
        - heat_calories: Q in calories
        - temperature_rise: Delta_T (if C given)
        - power: I^2 * R (watts)

    Example:
        >>> result = joule_balance(current=1.0, resistance=1.0, time=1.0)
        >>> print(f"Heat = {result['heat_calories']:.4f} calories")
    """
    # Convert to CGS if needed (assuming SI input for convenience)
    # I (A) -> abA: 1 A = 0.1 abA
    # R (ohm) -> abohm: 1 ohm = 1e9 abohm
    # But we'll compute in SI and convert final result

    # Power in watts (SI): P = I^2 * R
    power_si = current**2 * resistance

    # Energy in joules
    energy_joules = power_si * time

    # Convert to ergs (1 J = 1e7 erg)
    heat_energy = energy_joules * 1e7

    # Convert to calories (1 cal = 4.184e7 erg)
    heat_calories = heat_energy / 4.184e7

    result = {
        "heat_energy": heat_energy,
        "heat_calories": heat_calories,
        "heat_joules": energy_joules,
        "power_watts": power_si,
        "current": current,
        "resistance": resistance,
        "time": time,
    }

    if heat_capacity is not None:
        result["temperature_rise"] = heat_energy / heat_capacity

    return result


# Range justification (lint rule 6): this aggregator reports one result
# block per instrument article-cluster implemented in this module; each
# listed article has an article-specific computation elsewhere in this
# file (tangent 736-738, sine 739, Helmholtz 741-743, wattmeter 744/746,
# electrodynamometer 747-749, current weigher 751-754).  Arts. 755-757
# were removed by the D-17 re-map (2026-08-21): the Joule balance is
# standard_math and post-dates the Treatise.  Chapter field names Ch XVI
# (Observations, 730-751), which holds the bulk of the range; 752-754
# sit at the head of Ch XVII (Comparison of Coils) per the PARTS table
# and are carried by the current-weigher mapping adjudicated with D-05.
# Article-specific computations for Ch XVII's own subject matter
# (Comparison of Coils, Arts. 752-757) additionally live in
# maxwell/electromagnetism/coil_comparison/.
@maxwell_cite(
    736,
    737,
    738,
    739,
    741,
    742,
    743,
    744,
    746,
    747,
    748,
    749,
    751,
    752,
    753,
    754,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Complete galvanometer and measurement analysis",
)
def analyze_galvanometers() -> dict[str, dict]:
    """
    Complete analysis of galvanometers and electrical measurements.

    Arts. 736-754: Comprehensive analysis including all types of
    galvanometers and measurement instruments described by Maxwell.
    The Joule-balance block is a standard_math extension (D-17 re-map;
    no Treatise articles claimed for it).

    Returns:
        Dictionary with complete analysis of:
        - Tangent galvanometer
        - Sine galvanometer
        - Helmholtz galvanometer
        - Wattmeter
        - Electrodynamometer
        - Current weigher
        - Joule balance (standard_math extension, D-17)

    Reference:
        Part IV, Arts. 736-754: Complete measurement analysis.
    """
    results = {}

    # 1. Tangent galvanometer
    results["tangent_galvanometer"] = tangent_galvanometer(
        coil_radius=15.0, num_turns=10, earth_field=0.25, deflection_angle=45.0
    )

    # 2. Sine galvanometer
    results["sine_galvanometer"] = sine_galvanometer(
        coil_radius=15.0, num_turns=10, earth_field=0.25, deflection_angle=45.0
    )

    # 3. Helmholtz galvanometer
    results["helmholtz_galvanometer"] = helmholtz_galvanometer(
        coil_radius=10.0, num_turns_per_coil=50, earth_field=0.25, deflection_angle=45.0
    )

    # 4. Wattmeter
    results["wattmeter"] = wattmeter(voltage=120.0, current=10.0, power_factor=0.8)

    # 5. Electrodynamometer
    results["electrodynamometer"] = electrodynamometer(
        current1=1.0, current2=0.5, mutual_inductance_gradient=1e-6, spring_constant=1.0
    )

    # 6. Current weigher
    results["current_weigher"] = current_weigher(
        current=1.0,
        coil_radius=10.0,
        num_turns_fixed=100,
        num_turns_movable=50,
        coil_separation=15.0,
    )

    # 7. Joule balance
    results["joule_balance"] = joule_balance(
        current=1.0, resistance=1.0, time=60.0, heat_capacity=100.0  # erg/degree
    )

    return results


__all__ = [
    "TangentGalvanometer",
    "SineGalvanometer",
    "HelmholtzGalvanometer",
    "Electrodynamometer",
    "tangent_galvanometer",
    "sine_galvanometer",
    "helmholtz_galvanometer",
    "wattmeter",
    "electrodynamometer",
    "current_weigher",
    "joule_balance",
    "analyze_galvanometers",
]
