"""maxwell.electromagnetism.measurements.galvanometers_extended — Galvanometer designs and analysis (Arts. 736-757).

Implements Maxwell's detailed treatment of galvanometers and electrical
measurement instruments from Part IV:

- Tangent galvanometer (Arts. 736-738)
- Sine galvanometer (Art. 739)
- Helmholtz galvanometer (Arts. 741-743)
- Wattmeter (Arts. 744, 746)
- Electrodynamometer (Arts. 747-749)
- Current weigher (Arts. 751-754)
- Joule balance (Arts. 755-757)

Galvanometers measure electric current by the magnetic force produced
by the current. Maxwell's analysis (CGS units):

Tangent galvanometer:
    I = (H * r / (2 * pi * n)) * tan(theta)

where:
    H = horizontal component of Earth's field (gauss)
    r = coil radius (cm)
    n = number of turns
    theta = deflection angle

Sine galvanometer:
    I = (H * r / (2 * pi * n)) * sin(theta)

Helmholtz galvanometer (two coils):
    More uniform field, improved accuracy

CGS Units:
    I = current (abamperes)
    H = magnetic field (gauss = oersted in air)
    r = distance (cm)
    theta = angle (radians or degrees)

Category: A (maxwell_original) — Maxwell's galvanometer theory.

References:
    Part IV, Ch XVI: Electrical Measurement (Arts. 736-757).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


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
        B_center = (8 * pi * n * I) / (5 * sqrt(5) * c * r)
                 = 0.7155 * (2 * pi * n * I) / (c * r)

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
        Helmholtz field reduction factor.

        For ideal Helmholtz (separation = radius):
            factor = 8 / (5 * sqrt(5)) = 0.7155

        Returns:
            Field reduction factor relative to single coil.
        """
        if self.coil_separation == self.coil_radius:
            return 8.0 / (5.0 * np.sqrt(5.0))
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
        Calculate magnetic field at Helmholtz coil center.

        Arts. 741-743: For ideal Helmholtz coils:
            B = (8 * pi * n * I) / (5 * sqrt(5) * c * r)

        Args:
            current: Current I (abamperes).

        Returns:
            Magnetic field B (gauss).
        """
        return (8.0 * np.pi * self.num_turns_per_coil * current) / (
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

        B_center = (8 * pi * n * I) / (5 * sqrt(5) * c * r)

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
    the magnetic force between coils. This is an absolute method
    for current measurement.

    For two coaxial circular coils:
        F = (mu0 / 4pi) * (2 * pi^2 * N1 * N2 * I^2 * r1^2 * r2^2) / d^4
            [for small coils at large separation]

    More generally, the force is:
        F = I^2 * (dM/dx)

    where M is the mutual inductance and x is the separation.

    The current is determined from:
        I = sqrt(F / (dM/dx))

    In CGS units, the force between coaxial coils:
        F = (2 * pi * N1 * N2 * I^2 / c^2) * f(r1, r2, d)

    where f is a geometric factor.

    Args:
        current: Current I (abamperes).
        coil_radius: Radius of coils (cm, assumed equal).
        num_turns_fixed: N1 turns in fixed coil.
        num_turns_movable: N2 turns in movable coil.
        coil_separation: Distance between coils (cm).

    Returns:
        Dictionary with:
        - force: Magnetic force (dynes)
        - equivalent_mass: Mass that balances force (grams)
        - mutual_inductance_gradient: dM/dx

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

    # Approximate formula for coaxial coils (r << d)
    # Force ~ (2*pi*N1*N2*I^2/c^2) * (r^4/d^4) for small coils
    # More accurate: use elliptic integral formulas

    # Simplified geometric factor
    if d > 2 * r:
        # Far-field approximation
        geom_factor = (r**4) / (d**4)
    else:
        # Near-field - use empirical correction
        geom_factor = (r**2) / (d**2 + r**2)

    # Force in CGS
    force = (2.0 * np.pi * N1 * N2 * current**2 / (CONST.C**2)) * geom_factor

    # Equivalent mass (F = m*g)
    g = 980.665  # cm/s^2
    equivalent_mass = force / g

    # Mutual inductance gradient (dM/dx)
    # F = I^2 * (dM/dx), so dM/dx = F/I^2
    dM_dx = force / (current**2) if current > 0 else 0

    return {
        "force": force,
        "equivalent_mass": equivalent_mass,
        "dM_dx": dM_dx,
        "current": current,
        "coil_radius": coil_radius,
        "num_turns_fixed": N1,
        "num_turns_movable": N2,
        "coil_separation": d,
        "geometric_factor": geom_factor,
    }


@maxwell_cite(
    755,
    756,
    757,
    part=4,
    chapter="Joule Balance",
    theory_class="maxwell_original",
    description="Calculate energy in Joule balance",
)
def joule_balance(
    current: float,
    resistance: float,
    time: float,
    heat_capacity: float = None,
) -> dict[str, float]:
    """
    Calculate heat production using Joule's law (Joule balance).

    Arts. 755-757: Joule's experiments established that the heat
    produced in a resistor is:

        Q = I^2 * R * t

    where:
        Q = heat energy (ergs in CGS, joules in SI)
        I = current
        R = resistance
        t = time

    The mechanical equivalent of heat:
        1 calorie = 4.184e7 ergs = 4.184 joules

    The Joule balance measures current by the heat produced,
    providing an absolute current standard.

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

    Reference:
        Part IV, Arts. 755-757: Joule balance.

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
    755,
    756,
    757,
    part=4,
    chapter="Electrical Measurements",
    theory_class="maxwell_original",
    description="Complete galvanometer and measurement analysis",
)
def analyze_galvanometers() -> dict[str, dict]:
    """
    Complete analysis of galvanometers and electrical measurements.

    Arts. 736-757: Comprehensive analysis including all types of
    galvanometers and measurement instruments described by Maxwell.

    Returns:
        Dictionary with complete analysis of:
        - Tangent galvanometer
        - Sine galvanometer
        - Helmholtz galvanometer
        - Wattmeter
        - Electrodynamometer
        - Current weigher
        - Joule balance

    Reference:
        Part IV, Arts. 736-757: Complete measurement analysis.
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
