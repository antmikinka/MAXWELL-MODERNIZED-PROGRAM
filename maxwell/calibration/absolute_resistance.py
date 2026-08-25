"""maxwell.calibration.absolute_resistance — Absolute resistance measurement (Arts. 758-767).

Implements Maxwell's methods for absolute measurement of electrical resistance
using electromagnetic induction principles.

Maxwell's CGS formulation (Arts. 758-767):
    Absolute resistance has dimensions of velocity in CGS:
        [R] = LT⁻¹ (cm/s)

    Method of recoil for resistance measurement:
        R = (2M/T) * (θ₁/θ₂)

    where:
        M = mutual inductance between coils
        T = oscillation period
        θ₁, θ₂ = successive deflections

    Lenz's law method:
        R = EMF / I = (dΦ/dt) / I

    Rotating coil method (Lorenz method):
        R = (μ₀ * N² * A * ω) / (2 * δ)

    where:
        N = number of turns
        A = coil area
        ω = angular velocity
        δ = deflection angle

    Capacitor-discharge (leak) method (Art. 765):
        R = t / (C ln(V₀ / V))
        (purely electrostatic standards; C in EMU = s²/cm)

    Recoil damping correction (Art. 766):
        λ = ln(θ₁ / θ₂),   θ₁* = θ₁ e^(λ/2)
        (logarithmic decrement and corrected first throw)

where:
    R = resistance (abohms in CGS, which equals cm/s)
    M = mutual inductance (cm)
    Φ = magnetic flux (maxwells)
    I = current (abamperes)
    EMF = electromotive force (abvolts)

Category: A (maxwell_original) — Maxwell's absolute resistance measurement.

References:
    Part IV, Arts. 758-767: Absolute measurement of resistance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class AbsoluteResistance:
    """
    Absolute resistance measurement calculator.

    Art. 758-767: Maxwell's methods for determining resistance
    in absolute electromagnetic units without reference to material
    standards.

    Attributes:
        method: Measurement method ('recoil', 'lenz', 'rotating').
    """

    method: str = "recoil"

    @maxwell_cite(
        758,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate resistance by recoil method",
    )
    def recoil_method(
        self,
        mutual_inductance: float,
        period: float,
        first_deflection: float,
        second_deflection: float,
    ) -> float:
        """
        Calculate resistance using the recoil method.

        Art. 758: Maxwell's recoil method:

            R = (2M / T) * (θ₁ / θ₂)

        where the ratio of successive deflections gives the damping.

        Args:
            mutual_inductance: M (cm).
            period: Oscillation period T (s).
            first_deflection: θ₁ (radians).
            second_deflection: θ₂ (radians).

        Returns:
            Resistance R (abohms = cm/s in CGS).

        Reference:
            Part IV, Art. 758: Recoil method.
        """
        if period <= 0:
            raise ValueError(f"Period must be positive")
        if second_deflection <= 0:
            raise ValueError(f"Second deflection must be positive")

        return (2.0 * mutual_inductance / period) * (
            first_deflection / second_deflection
        )

    @maxwell_cite(
        759,
        760,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate resistance by Lenz's law method",
    )
    def lenz_method(
        self,
        induced_emf: float,
        induced_current: float,
    ) -> float:
        """
        Calculate resistance using Lenz's law method.

        Art. 759-760: From the induced EMF and current:

            R = EMF / I

        Args:
            induced_emf: Induced EMF (abvolts).
            induced_current: Induced current (abamperes).

        Returns:
            Resistance R (abohms).

        Reference:
            Part IV, Arts. 759-760: Lenz's law method.
        """
        if induced_current == 0:
            return float("inf")
        return induced_emf / induced_current

    @maxwell_cite(
        761,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate resistance by rotating coil method",
    )
    def rotating_coil_method(
        self,
        n_turns: int,
        coil_area: float,
        angular_velocity: float,
        magnetic_field: float,
        induced_current: float,
        circuit_resistance_known: float,
    ) -> float:
        """
        Calculate resistance using rotating coil method.

        Art. 761: Lorenz's rotating coil method:

            EMF = N * B * A * ω

            R = EMF / I - R_known

        Args:
            n_turns: Number of turns N.
            coil_area: Coil area A (cm²).
            angular_velocity: Angular velocity ω (s⁻¹).
            magnetic_field: Magnetic field B (gauss).
            induced_current: Measured current I (abamperes).
            circuit_resistance_known: Known series resistance (abohms).

        Returns:
            Unknown resistance R (abohms).

        Reference:
            Part IV, Art. 761: Rotating coil method.
        """
        if induced_current <= 0:
            return float("inf")

        emf = n_turns * magnetic_field * coil_area * angular_velocity
        total_resistance = emf / induced_current
        return total_resistance - circuit_resistance_known

    @maxwell_cite(
        762,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate resistance from energy dissipation",
    )
    def energy_dissipation_method(
        self,
        current: float,
        time: float,
        heat_generated: float,
    ) -> float:
        """
        Calculate resistance from energy dissipation.

        Art. 762: From Joule heating:

            Heat = I² * R * t

            R = Heat / (I² * t)

        Args:
            current: Current I (abamperes).
            time: Time t (s).
            heat_generated: Heat energy (ergs).

        Returns:
            Resistance R (abohms).

        Reference:
            Part IV, Art. 762: Energy dissipation method.
        """
        if current == 0 or time <= 0:
            return float("inf")

        return heat_generated / (current**2 * time)


@dataclass
class StandardResistanceCoil:
    """
    Standard resistance coil for calibration.

    Art. 763-767: Maxwell's treatment of standard resistance coils
    and their calibration against absolute measurements.

    Attributes:
        nominal_resistance: Nominal resistance value (abohms).
        material: Coil material ('german_silver', 'platinoid', 'manganin').
        temperature_coefficient: Temperature coefficient (per °C).
    """

    nominal_resistance: float
    material: str = "german_silver"
    temperature_coefficient: float = 0.0004

    # Temperature coefficients for common materials
    MATERIAL_COEFFICIENTS = {
        "german_silver": 0.0004,
        "platinoid": 0.00025,
        "manganin": 0.00002,
        "copper": 0.004,
        "silver": 0.004,
    }

    def __post_init__(self):
        """Set temperature coefficient from material."""
        if self.material.lower() in self.MATERIAL_COEFFICIENTS:
            self.temperature_coefficient = self.MATERIAL_COEFFICIENTS[
                self.material.lower()
            ]

    @maxwell_cite(
        763,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate resistance at temperature",
    )
    def resistance_at_temperature(
        self, temperature: float, reference_temp: float = 20.0
    ) -> float:
        """
        Calculate resistance at given temperature.

        Art. 763: Temperature correction:

            R(T) = R₀ * [1 + α * (T - T₀)]

        Args:
            temperature: Temperature T (°C).
            reference_temp: Reference temperature T₀ (°C).

        Returns:
            Resistance at temperature T (abohms).

        Reference:
            Part IV, Art. 763: Temperature correction.
        """
        delta_T = temperature - reference_temp
        return self.nominal_resistance * (1.0 + self.temperature_coefficient * delta_T)

    @maxwell_cite(
        764,
        part=4,
        chapter="Absolute Resistance",
        theory_class="maxwell_original",
        description="Calculate coil inductance",
    )
    def self_inductance(self, coil_radius: float, coil_length: float) -> float:
        """
        Calculate approximate self-inductance of coil.

        Art. 764: For a solenoidal coil:

            L ≈ 4π² * N² * r² / l

        This is needed for AC corrections.

        Args:
            coil_radius: Coil radius r (cm).
            coil_length: Coil length l (cm).

        Returns:
            Self-inductance L (cm).

        Reference:
            Part IV, Art. 764: Coil inductance.
        """
        if coil_length <= 0 or coil_radius <= 0:
            return 0.0

        # Estimate turns from resistance (simplified)
        wire_length = self.nominal_resistance / 0.0001  # Assume thin wire
        n_turns = int(wire_length / (2 * np.pi * coil_radius))

        return 4.0 * np.pi**2 * n_turns**2 * coil_radius**2 / coil_length


@maxwell_cite(
    758,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate absolute resistance from recoil",
)
def calc_absolute_resistance_recoil(
    mutual_inductance: float,
    period: float,
    first_deflection: float,
    second_deflection: float,
) -> float:
    """
    Calculate absolute resistance using recoil method.

    Art. 758: R = (2M / T) * (θ₁ / θ₂)

    Args:
        mutual_inductance: M (cm).
        period: Oscillation period T (s).
        first_deflection: First swing θ₁ (radians).
        second_deflection: Second swing θ₂ (radians).

    Returns:
        Resistance R (abohms).

    Reference:
        Part IV, Art. 758: Recoil method formula.

    Example:
        >>> R = calc_absolute_resistance_recoil(1000, 2.0, 0.1, 0.08)
        >>> print(f"R = {R:.2f} abohms")
    """
    ar = AbsoluteResistance()
    return ar.recoil_method(
        mutual_inductance, period, first_deflection, second_deflection
    )


@maxwell_cite(
    759,
    760,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance from induced EMF and current",
)
def calc_absolute_resistance_lenz(
    induced_emf: float,
    induced_current: float,
) -> float:
    """
    Calculate resistance using Lenz's law method.

    Art. 759-760: R = EMF / I

    Args:
        induced_emf: Induced EMF (abvolts).
        induced_current: Induced current (abamperes).

    Returns:
        Resistance R (abohms).

    Reference:
        Part IV, Arts. 759-760: Lenz's law method.
    """
    ar = AbsoluteResistance()
    return ar.lenz_method(induced_emf, induced_current)


@maxwell_cite(
    761,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance by rotating coil method",
)
def calc_absolute_resistance_rotating_coil(
    n_turns: int,
    coil_area: float,
    angular_velocity: float,
    magnetic_field: float,
    induced_current: float,
) -> float:
    """
    Calculate resistance using rotating coil (Lorenz) method.

    Art. 761: R = (N * B * A * ω) / I

    Args:
        n_turns: Number of turns.
        coil_area: Coil area (cm²).
        angular_velocity: Angular velocity (s⁻¹).
        magnetic_field: Magnetic field (gauss).
        induced_current: Induced current (abamperes).

    Returns:
        Resistance R (abohms).

    Reference:
        Part IV, Art. 761: Rotating coil method.
    """
    emf = n_turns * magnetic_field * coil_area * angular_velocity
    return calc_absolute_resistance_lenz(emf, induced_current)


@maxwell_cite(
    762,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance from heat dissipation",
)
def calc_absolute_resistance_joule(
    current: float,
    time: float,
    heat_energy: float,
) -> float:
    """
    Calculate resistance from Joule heating.

    Art. 762: R = Heat / (I² * t)

    Args:
        current: Current I (abamperes).
        time: Time t (s).
        heat_energy: Heat energy generated (ergs).

    Returns:
        Resistance R (abohms).

    Reference:
        Part IV, Art. 762: Joule heating method.
    """
    ar = AbsoluteResistance()
    return ar.energy_dissipation_method(current, time, heat_energy)


@maxwell_cite(
    763,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate temperature-corrected resistance",
)
def calc_temperature_corrected_resistance(
    nominal_resistance: float,
    temperature: float,
    temperature_coefficient: float,
    reference_temp: float = 20.0,
) -> float:
    """
    Calculate resistance corrected for temperature.

    Art. 763: R(T) = R₀ * [1 + α * (T - T₀)]

    Args:
        nominal_resistance: R₀ at reference temp (abohms).
        temperature: Actual temperature T (°C).
        temperature_coefficient: α (per °C).
        reference_temp: Reference temperature T₀ (°C).

    Returns:
        Resistance at temperature T (abohms).

    Reference:
        Part IV, Art. 763: Temperature correction.

    Example:
        >>> # Copper at 30°C (α = 0.004/°C)
        >>> R = calc_temperature_corrected_resistance(100, 30, 0.004)
        >>> print(f"R = {R:.2f} abohms")
    """
    delta_T = temperature - reference_temp
    return nominal_resistance * (1.0 + temperature_coefficient * delta_T)


@maxwell_cite(
    764,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate the approximate self-inductance of a long solenoidal "
    "standard coil from its turns, radius, and length",
)
def calc_solenoid_self_inductance(
    n_turns: int,
    coil_radius: float,
    coil_length: float,
) -> float:
    """
    Approximate self-inductance of a long solenoidal coil.

    Art. 764: For a coil of N turns uniformly wound over a length l with
    radius r (l large compared with r), the interior field is B = 4 pi n I
    with n = N/l the turns per unit length (EMU), the flux through each
    turn is B pi r^2, and the linkage of all N turns gives the working
    formula

        L = 4 pi^2 N^2 r^2 / l

    in centimetres (1 abhenry = 1 cm in CGS-EMU).  This is the leading
    term of the solenoid inductance: end effects (Nagaoka correction)
    reduce L by a relative amount of order r/l.  The inductance enters
    the absolute resistance determinations through the AC/period
    corrections that Arts. 763-764 attach to the standard coils.

    Args:
        n_turns: Number of turns N (positive integer).
        coil_radius: Coil radius r (cm).
        coil_length: Wound length l (cm).

    Returns:
        Self-inductance L (cm, i.e. abhenries in CGS-EMU).

    Raises:
        ValueError: On non-positive turns, radius, or length.

    Reference:
        Part IV, Art. 764: Coil inductance for the resistance standards.
    """
    if n_turns <= 0:
        raise ValueError("Number of turns must be positive")
    if coil_radius <= 0 or coil_length <= 0:
        raise ValueError("Coil radius and length must be positive")

    return 4.0 * np.pi**2 * n_turns**2 * coil_radius**2 / coil_length


@maxwell_cite(
    765,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance by the capacitor-discharge (leak) method",
)
def calc_absolute_resistance_capacitor_discharge(
    capacitance: float,
    voltage_initial: float,
    voltage_final: float,
    elapsed_time: float,
) -> float:
    """
    Calculate resistance by the capacitor-discharge method.

    Art. 765: A capacitor of (independently known) capacitance C is
    charged, then allowed to leak through the unknown resistance.  The
    potential decays as V(t) = V₀ e^(−t/(R C)), so measuring V₀, the
    residual V after a timed interval t gives the absolute working
    formula

        R = t / (C ln(V₀ / V))

    Unlike the induction methods (Arts. 758-762) this determination is
    purely electrostatic in its standards: in CGS-EMU the capacitance
    carries dimensions T²L⁻¹ (C in s²/cm), the elapsed time t is in
    seconds, and the result has the velocity dimensions LT⁻¹ required
    of an absolute resistance (1 abohm = 1 cm/s).

    Args:
        capacitance: Capacitance C (EMU, s²/cm; e.g. a sphere of
            radius a has C = a / CONST.C² in EMU).
        voltage_initial: Initial potential V₀ (abvolts).
        voltage_final: Residual potential V after elapsed_time
            (abvolts); must satisfy 0 < V < V₀.
        elapsed_time: Discharge interval t (s).

    Returns:
        Resistance R (abohms = cm/s in CGS-EMU).

    Raises:
        ValueError: On non-positive capacitance/time or a voltage pair
            that does not represent a genuine decay (V₀ > V > 0).

    Reference:
        Part IV, Art. 765: Capacitor-discharge determination of
        resistance in absolute measure.
    """
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive")
    if elapsed_time <= 0:
        raise ValueError("Elapsed time must be positive")
    if voltage_initial <= 0 or voltage_final <= 0:
        raise ValueError("Voltages must be positive")
    if voltage_initial <= voltage_final:
        raise ValueError("Discharge requires voltage_initial > voltage_final")

    return elapsed_time / (capacitance * math.log(voltage_initial / voltage_final))


@maxwell_cite(
    766,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Damping (logarithmic decrement) correction of recoil deflections",
)
def calc_recoil_damping_correction(
    first_deflection: float,
    second_deflection: float,
) -> tuple[float, float]:
    """
    Damping correction for the recoil/ballistic deflection pair.

    Art. 766: The recoil determination (Art. 758) reads the transient
    charge from the first throw θ₁ of the galvanometer magnet, but
    damping already attenuates that throw during the quarter period
    from the impulse to the first elongation.  From two successive
    (opposite) elongations θ₁, θ₂ the logarithmic decrement is

        λ = ln(θ₁ / θ₂)

    and the first throw corrected for damping — the value the recoil
    formula must use — is

        θ₁* = θ₁ e^(λ/2) = θ₁ sqrt(θ₁ / θ₂)

    (one half of a decrement, because θ₁ and θ₂ are separated by half
    a period while the impulse-to-elongation interval is a quarter).

    Args:
        first_deflection: First elongation θ₁ (radians), undamped side.
        second_deflection: Next opposite elongation θ₂ (radians); a
            damped swing requires 0 < θ₂ < θ₁.

    Returns:
        Tuple (λ, θ₁*): the logarithmic decrement and the damping-
        corrected first deflection (both dimensionless / radians).

    Raises:
        ValueError: On non-positive deflections or θ₂ ≥ θ₁ (no decay).

    Reference:
        Part IV, Art. 766: Corrections of the recoil method.
    """
    if first_deflection <= 0 or second_deflection <= 0:
        raise ValueError("Deflections must be positive")
    if second_deflection >= first_deflection:
        raise ValueError("Damped recoil requires second_deflection < first_deflection")

    logarithmic_decrement = math.log(first_deflection / second_deflection)
    corrected_first = first_deflection * math.exp(0.5 * logarithmic_decrement)
    return (logarithmic_decrement, corrected_first)


@maxwell_cite(
    758,
    759,
    760,
    761,
    762,
    763,
    764,
    767,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Verify absolute resistance measurements",
)
def verify_absolute_resistance(
    mutual_inductance: float = 1000.0,
    period: float = 2.0,
    deflection_ratio: float = 1.25,
    induced_emf: float = 1.0,
    induced_current: float = 0.1,
    heat_generated: float | None = None,
    dissipation_time: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify absolute resistance measurement methods.

    Art. 758-767: This function compares INDEPENDENT determinations of the
    same resistance and checks the dimensional claim of the CGS result:

    1. Recoil method (Art. 758): R from mutual inductance and damped
       deflections, inputs (M, T, θ₁/θ₂).
    2. Lenz's law method (Arts. 759-760): R = EMF/I, inputs (EMF, I).
    3. Calorimetric energy method (Art. 762): R = Q/(I²t), performed ONLY
       when an independently measured heat input ``heat_generated`` is
       supplied.  Heat is never derived from the Lenz result inside this
       function: feeding R_lenz's own heat output back into the energy
       method compares a value to itself (verification theater; Stage-3
       defect D-10).  Without a calorimetric measurement the cross-check is
       reported as not performed (NaN residual) rather than fabricated.
    4. Dimensional consistency [R] = LT⁻¹ (a velocity; 1 abohm = 1 cm/s in
       CGS-EMU), verified numerically by measuring the dimensional
       exponents of the recoil formula under unit rescaling (a velocity is
       unchanged when the length and time units are both rescaled, i.e.
       exponents (+1, -1)).

    The verdict is computed from these residuals; perturbing the Lenz
    inputs does not move the calorimetric determination.

    Args:
        mutual_inductance: M (cm).
        period: Oscillation period T (s).
        deflection_ratio: θ₁/θ₂.
        induced_emf: Test EMF (abvolts).
        induced_current: Test current (abamperes).
        heat_generated: Independently measured heat Q (ergs), optional.
        dissipation_time: Time t over which the heat was collected (s).
        tolerance: Relative tolerance for the calorimetric cross-check.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 758-767: Absolute resistance verification.
    """
    ar = AbsoluteResistance()

    # Determination 1: induction/recoil method (Art. 758).
    R_recoil = ar.recoil_method(mutual_inductance, period, deflection_ratio, 1.0)

    # Determination 2: Ohm's law on the induced EMF and current (Arts. 759-760).
    R_lenz = ar.lenz_method(induced_emf, induced_current)

    # Determination 3 (Art. 762): calorimetric.  Heat must arrive as an
    # independent measurement; it is never synthesized from R_lenz (or from
    # EMF*I, which is the same electromagnetic measurement rewritten).
    calorimetric_cross_check = heat_generated is not None
    if calorimetric_cross_check:
        R_energy = ar.energy_dissipation_method(
            induced_current, dissipation_time, heat_generated
        )
        if math.isfinite(R_lenz) and math.isfinite(R_energy) and R_lenz != 0.0:
            consistency_error = abs(R_lenz - R_energy) / abs(R_lenz)
        else:
            consistency_error = float("inf")
    else:
        R_energy = float("nan")  # not measured: no comparison is fabricated
        consistency_error = float("nan")

    # Dimensional check: in CGS-EMU, [R] = LT^-1 (a velocity).  Rescaling the
    # length unit by k scales the numeric value of M by k; rescaling the time
    # unit by k scales the numeric value of T by k.  A quantity of dimensions
    # L^a T^b then picks up k^a and k^b respectively, so measuring the two
    # scaling exponents of the recoil formula tests the velocity claim.
    scale = 2.0
    R_length = ar.recoil_method(
        scale * mutual_inductance, period, deflection_ratio, 1.0
    )
    R_time = ar.recoil_method(mutual_inductance, scale * period, deflection_ratio, 1.0)
    if R_recoil > 0.0 and R_length > 0.0 and R_time > 0.0:
        exponent_length = math.log(R_length / R_recoil) / math.log(scale)
        exponent_time = math.log(R_time / R_recoil) / math.log(scale)
        velocity_check = bool(
            abs(exponent_length - 1.0) < 1e-9 and abs(exponent_time - (-1.0)) < 1e-9
        )
    else:
        exponent_length = float("nan")
        exponent_time = float("nan")
        # Degenerate measurement: the dimensional claim is not established.
        velocity_check = False

    if calorimetric_cross_check:
        verified = bool(velocity_check and consistency_error < tolerance)
    else:
        # Only the dimensional-homogeneity result is available for the
        # supplied inputs; the calorimetric leg is honestly reported as not
        # performed via the NaN residual above.
        verified = bool(velocity_check)

    return {
        "mutual_inductance": mutual_inductance,
        "period": period,
        "deflection_ratio": deflection_ratio,
        "R_recoil": R_recoil,
        "R_lenz": R_lenz,
        "R_energy": R_energy,
        "consistency_error": consistency_error,
        "calorimetric_cross_check": calorimetric_cross_check,
        "dimension_exponents": {
            "length": exponent_length,
            "time": exponent_time,
        },
        "velocity_dimensions": velocity_check,
        "verified": verified,
    }


@maxwell_cite(
    758,
    759,
    760,
    761,
    762,
    763,
    764,
    767,
    part=4,
    chapter="Absolute Resistance",
    theory_class="maxwell_original",
    description="Complete absolute resistance analysis",
)
def analyze_absolute_resistance(
    method: str = "recoil",
    mutual_inductance: float = 1000.0,
    period: float = 2.0,
    deflection_ratio: float = 1.25,
    induced_emf: float = 1.0,
    induced_current: float = 0.1,
    heat_generated: float | None = None,
    dissipation_time: float = 1.0,
    nominal_resistance: float = 10.0,
    temperature: float = 20.0,
) -> dict[str, float]:
    """
    Complete analysis of absolute resistance measurement.

    Art. 758-767: Comprehensive analysis including:
    1. Resistance by specified method
    2. Temperature corrections
    3. Method comparisons
    4. Uncertainty estimates

    The calorimetric (energy) determination is included only when an
    independently measured ``heat_generated`` is supplied; heat is never
    synthesized from the electromagnetic inputs, which would merely
    reproduce the Lenz result and fake a third method.  Without it, the
    average/spread are computed over the two determinations that exist.

    Args:
        method: Measurement method.
        mutual_inductance: M (cm).
        period: Oscillation period (s).
        deflection_ratio: θ₁/θ₂.
        induced_emf: EMF (abvolts).
        induced_current: Current (abamperes).
        heat_generated: Independently measured heat Q (ergs), optional.
        dissipation_time: Time t over which the heat was collected (s).
        nominal_resistance: Nominal coil resistance.
        temperature: Operating temperature.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 758-767: Complete absolute resistance analysis.
    """
    ar = AbsoluteResistance(method=method)

    # Calculate by each method
    R_recoil = ar.recoil_method(mutual_inductance, period, deflection_ratio, 1.0)
    R_lenz = ar.lenz_method(induced_emf, induced_current)
    if heat_generated is not None:
        R_energy = ar.energy_dissipation_method(
            induced_current, dissipation_time, heat_generated
        )
        determinations = [R_recoil, R_lenz, R_energy]
    else:
        R_energy = float("nan")  # no independent calorimetric measurement
        determinations = [R_recoil, R_lenz]

    # Temperature correction
    src = StandardResistanceCoil(nominal_resistance=nominal_resistance)
    R_corrected = src.resistance_at_temperature(temperature)

    return {
        "method": method,
        "R_recoil": R_recoil,
        "R_lenz": R_lenz,
        "R_energy": R_energy,
        "R_average": float(np.mean(determinations)),
        "R_spread": float(max(determinations) - min(determinations)),
        "nominal_resistance": nominal_resistance,
        "temperature_C": temperature,
        "R_temperature_corrected": R_corrected,
        "temperature_coefficient": src.temperature_coefficient,
        "CGS_units": "1 abohm = 1 cm/s",
    }
