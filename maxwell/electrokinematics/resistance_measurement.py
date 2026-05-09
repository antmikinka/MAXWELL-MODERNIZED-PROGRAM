"""
Measurement of Resistance — Maxwell's Treatise Part II, Chapter XI (Arts. 335-358).

This module implements Maxwell's methods for measuring electrical resistance,
covering the full range from very low resistances (fractions of an ohm) to
very high resistances (megohms and beyond).

Methods implemented:
- Substitution Method (Arts. 335-340): Comparing unknown to known resistance
- Differential Galvanometer (Arts. 341-345): Using differential instruments
- Wheatstone Bridge Methods (Arts. 346-350): Practical bridge measurements
- Low Resistance Measurement (Arts. 351-354): Kelvin double bridge, four-terminal
- High Resistance Measurement (Arts. 355-358): Leakage methods, capacitor discharge

All calculations use CGS-EMU units by default:
    - Resistance: abohms (abΩ)
    - Current: abamperes (abA)
    - Potential: abvolts (abV)
    - Conductance: siemens (abΩ^-1)

Category: A (maxwell_original) — Maxwell's resistance measurement methods.

References:
    Part II, Chapter XI: Measurement of Resistance (Arts. 335-358).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST, C
from maxwell.electrokinematics.network_solver import (
    wheatstone_bridge_balance,
    wheatstone_bridge_sensitivity,
)
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# DECORATOR WRAPPER FOR MAXWELL CITATION WITH ARTICLE METADATA
# =============================================================================

# Alias for compatibility — all functions use @maxwell_cite directly
maxwell_cite_resistance = maxwell_cite


# =============================================================================
# MEASUREMENT ERROR CLASS
# =============================================================================


@dataclass
class MeasurementError:
    """
    Error analysis for resistance measurements (GUM-compliant).

    Maxwell recognized that all measurements have uncertainties, and he
    developed methods to minimize and quantify errors (Arts. 346-350).

    This class implements modern uncertainty analysis following the
    Guide to the Expression of Uncertainty in Measurement (GUM), while
    preserving Maxwell's error classification scheme.

    Error types (Maxwell's classification):
    - Systematic errors: Instrument calibration, temperature drift
    - Random errors: Reading uncertainty, noise
    - Environmental errors: Temperature, humidity, magnetic fields

    Attributes:
        resistance_value: Measured resistance value (abΩ).
        systematic_uncertainty: Systematic uncertainty component (abΩ).
        random_uncertainty: Random uncertainty component (abΩ).
        confidence_level: Coverage factor k (default k=2 for ~95% confidence).
        temperature: Measurement temperature (Celsius) for corrections.
        temperature_coefficient: Temperature coefficient of resistance (/°C).
    """

    resistance_value: float
    systematic_uncertainty: float = 0.0
    random_uncertainty: float = 0.0
    confidence_level: float = 2.0  # k=2 for ~95% confidence
    temperature: float = 20.0  # Reference temperature 20°C
    temperature_coefficient: float = 0.0  # /°C
    calibration_factor: float = 1.0
    calibration_uncertainty: float = 0.0
    resolution_uncertainty: float = 0.0
    method: str = "unknown"
    notes: str = ""

    @property
    def combined_standard_uncertainty(self) -> float:
        """
        Calculate combined standard uncertainty (GUM Eq. 10).

        u_c = sqrt(u_sys^2 + u_rand^2 + u_cal^2 + u_res^2)

        Returns:
            Combined standard uncertainty (abΩ).
        """
        u_squared = (
            self.systematic_uncertainty**2
            + self.random_uncertainty**2
            + self.calibration_uncertainty**2
            + self.resolution_uncertainty**2
        )
        return math.sqrt(u_squared)

    @property
    def relative_uncertainty(self) -> float:
        """
        Calculate relative uncertainty (fractional).

        u_rel = u_c / R

        Returns:
            Relative uncertainty (dimensionless).
        """
        if abs(self.resistance_value) < 1e-15:
            return float("inf")
        return self.combined_standard_uncertainty / abs(self.resistance_value)

    @property
    def expanded_uncertainty(self) -> float:
        """
        Calculate expanded uncertainty for reporting.

        U = k * u_c

        where k is the coverage factor (typically k=2 for 95% confidence).

        Returns:
            Expanded uncertainty (abΩ).
        """
        return self.confidence_level * self.combined_standard_uncertainty

    @property
    def corrected_value(self) -> float:
        """
        Apply calibration correction to measured value.

        Returns:
            Calibrated resistance value (abΩ).
        """
        return self.resistance_value * self.calibration_factor

    def temperature_correction(self, reference_temp: float = 20.0) -> float:
        """
        Correct resistance for temperature deviation from reference.

        R_corrected = R_measured / [1 + α * (T - T_ref)]

        Args:
            reference_temp: Reference temperature (default 20°C).

        Returns:
            Temperature-corrected resistance (abΩ).
        """
        if self.temperature_coefficient == 0:
            return self.resistance_value

        delta_t = self.temperature - reference_temp
        correction_factor = 1.0 + self.temperature_coefficient * delta_t

        if abs(correction_factor) < 1e-15:
            raise ValueError("Invalid temperature correction factor")

        return self.resistance_value / correction_factor

    def report(self, significant_figures: int = 6) -> str:
        """
        Generate GUM-compliant uncertainty report.

        Args:
            significant_figures: Number of significant figures to report.

        Returns:
            Formatted uncertainty report string.
        """
        value = self.corrected_value
        u_c = self.combined_standard_uncertainty
        U = self.expanded_uncertainty

        # Format values with appropriate precision
        fmt = f"{{:.{max(0, significant_figures - 1 - int(math.floor(math.log10(abs(value)))))}e}}"

        report_lines = [
            f"Resistance Measurement Report",
            f"{'=' * 50}",
            f"Method: {self.method}",
            f"",
            f"Measured Value: {self.resistance_value:.{significant_figures}e} abohm",
            f"Corrected Value: {value:.{significant_figures}e} abohm",
            f"",
            f"Uncertainty Components (k={self.confidence_level}):",
            f"  Systematic:      {self.systematic_uncertainty:.{significant_figures}e} abohm",
            f"  Random:          {self.random_uncertainty:.{significant_figures}e} abohm",
            f"  Calibration:     {self.calibration_uncertainty:.{significant_figures}e} abohm",
            f"  Resolution:      {self.resolution_uncertainty:.{significant_figures}e} abohm",
            f"",
            f"Combined Standard Uncertainty: u_c = {u_c:.{significant_figures}e} abohm",
            f"Relative Uncertainty:          {self.relative_uncertainty:.{significant_figures}e} ({self.relative_uncertainty * 100:.4f}%)",
            f"Expanded Uncertainty (k={self.confidence_level}): U = {U:.{significant_figures}e} abohm",
            f"",
            f"Result: R = ({value:.{significant_figures}e} +/- {U:.{significant_figures}e}) abohm",
            f"        (k={self.confidence_level}, ~{95 if self.confidence_level == 2 else 99}% confidence)",
        ]

        if self.notes:
            report_lines.append(f"\nNotes: {self.notes}")

        return "\n".join(report_lines)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "resistance_value": self.resistance_value,
            "corrected_value": self.corrected_value,
            "systematic_uncertainty": self.systematic_uncertainty,
            "random_uncertainty": self.random_uncertainty,
            "calibration_uncertainty": self.calibration_uncertainty,
            "resolution_uncertainty": self.resolution_uncertainty,
            "combined_standard_uncertainty": self.combined_standard_uncertainty,
            "relative_uncertainty": self.relative_uncertainty,
            "expanded_uncertainty": self.expanded_uncertainty,
            "confidence_level": self.confidence_level,
            "method": self.method,
        }


# =============================================================================
# SUBSTITUTION METHOD (Arts. 335-340)
# =============================================================================


@maxwell_cite(
    335,
    336,
    337,
    theory_class="maxwell_original",
    description="Compare unknown resistance to standard using substitution method",
)
def substitution_method(
    unknown_current: float,
    standard_current: float,
    standard_resistance: float,
    emf_voltage: float = None,
    galvanometer_resistance: float = None,
) -> dict[str, float]:
    """
    Measure resistance using Maxwell's substitution method (Arts. 335-337).

    The substitution method compares an unknown resistance to a known standard
    by observing the current change when each is connected to the same circuit.

    Principle (Art. 335):
    - Connect unknown resistance R_x and measure current I_x
    - Replace with standard resistance R_s and measure current I_s
    - If the same EMF is applied: R_x / R_s = I_s / I_x

    Maxwell's refinement (Arts. 336-337):
    - Account for galvanometer resistance if significant
    - Use a battery with stable EMF
    - Make observations quickly to avoid battery drift

    Configuration:

        Battery (+) --- [R] --- [Galvanometer] --- Battery (-)

        where R is either R_x (unknown) or R_s (standard)

    Args:
        unknown_current: Current measured with unknown resistance (abA).
        standard_current: Current measured with standard resistance (abA).
        standard_resistance: Value of standard resistance (abΩ).
        emf_voltage: Battery EMF (abvolts). If None, assumed constant.
        galvanometer_resistance: Galvanometer resistance (abΩ).

    Returns:
        Dictionary with:
        - unknown_resistance: Calculated R_x (abΩ)
        - ratio_currents: I_s / I_x
        - relative_error: Estimated fractional error
        - method_sensitivity: dI/dR at operating point

    Raises:
        ValueError: If currents are zero or negative, or standard_resistance <= 0.

    References:
        Part II, Art. 335: Principle of substitution method.
        Part II, Art. 336: Practical procedure.
        Part II, Art. 337: Error considerations.

    Example:
        >>> # Unknown gives 3.5 abA, standard (100 abΩ) gives 4.2 abA
        >>> result = substitution_method(
        ...     unknown_current=3.5,
        ...     standard_current=4.2,
        ...     standard_resistance=100.0
        ... )
        >>> print(f"Unknown resistance: {result['unknown_resistance']:.2f} abΩ")
        120.0 abΩ
    """
    # Validate inputs
    if unknown_current <= 0:
        raise ValueError(f"unknown_current must be positive, got {unknown_current}")
    if standard_current <= 0:
        raise ValueError(f"standard_current must be positive, got {standard_current}")
    if standard_resistance <= 0:
        raise ValueError(
            f"standard_resistance must be positive, got {standard_resistance}"
        )

    # Current ratio: R_x = R_s * (I_s / I_x)
    current_ratio = standard_current / unknown_current
    unknown_resistance = standard_resistance * current_ratio

    # Estimate sensitivity: dI/dR ≈ -I/R (from Ohm's law)
    # For small changes: ΔR/R ≈ -ΔI/I
    method_sensitivity = (
        -unknown_current / unknown_resistance if unknown_resistance != 0 else 0
    )

    # Estimate relative error from current measurement precision
    # Assuming ~1% current reading uncertainty
    relative_error = math.sqrt(
        (0.01) ** 2 + (0.01) ** 2
    )  # RSS of both current measurements

    return {
        "unknown_resistance": unknown_resistance,
        "ratio_currents": current_ratio,
        "relative_error": relative_error,
        "method_sensitivity": method_sensitivity,
        "standard_resistance": standard_resistance,
        "unknown_current": unknown_current,
        "standard_current": standard_current,
    }


@maxwell_cite(
    338,
    339,
    340,
    theory_class="maxwell_original",
    description="Calculate resistance from voltage and current measurements",
)
def calculate_resistance_from_voltage(
    voltage: float,
    current: float,
    voltmeter_resistance: float = None,
    ammeter_resistance: float = None,
    connection_type: str = "standard",
) -> dict[str, float]:
    """
    Calculate resistance using Ohm's law with instrument corrections (Arts. 338-340).

    R = V / I

    Maxwell discussed corrections for instrument loading effects (Art. 338-340):
    - Voltmeter draws current, affecting measurement
    - Ammeter has internal resistance, causing voltage drop

    Two connection types:
    - "standard" (ammeter before voltmeter): Measures R + R_ammeter
    - "reversed" (voltmeter before ammeter): Measures R || R_voltmeter

    Args:
        voltage: Measured voltage (abvolts).
        current: Measured current (abA).
        voltmeter_resistance: Internal resistance of voltmeter (abΩ).
        ammeter_resistance: Internal resistance of ammeter (abΩ).
        connection_type: "standard" or "reversed" configuration.

    Returns:
        Dictionary with:
        - resistance_raw: V/I without corrections (abΩ)
        - resistance_corrected: Corrected for instrument effects (abΩ)
        - correction_factor: Multiplicative correction applied
        - loading_error: Estimated error from instrument loading

    Raises:
        ValueError: If current is zero or voltage/current have wrong signs.

    References:
        Part II, Art. 338: Voltmeter-ammeter method.
        Part II, Art. 339: Instrument corrections.
        Part II, Art. 340: Error analysis.

    Example:
        >>> # Standard connection: 100 abV, 2 abA, ammeter R = 0.5 abΩ
        >>> result = calculate_resistance_from_voltage(
        ...     voltage=100.0,
        ...     current=2.0,
        ...     ammeter_resistance=0.5,
        ...     connection_type="standard"
        ... )
        >>> print(f"Corrected resistance: {result['resistance_corrected']:.2f} abΩ")
        49.5 abΩ (raw 50 abΩ, minus ammeter resistance)
    """
    # Validate inputs
    if current == 0:
        raise ValueError("Current cannot be zero")
    if voltage == 0:
        raise ValueError("Voltage cannot be zero")
    if voltage * current < 0:
        raise ValueError(
            "Voltage and current must have same sign for passive resistance"
        )

    # Raw resistance from Ohm's law
    resistance_raw = voltage / current

    # Apply corrections based on connection type
    correction_factor = 1.0
    loading_error = 0.0

    if connection_type == "standard":
        # Ammeter is in series with R, voltmeter measures both
        # R_measured = R_true + R_ammeter
        if ammeter_resistance is not None and ammeter_resistance > 0:
            resistance_corrected = resistance_raw - ammeter_resistance
            correction_factor = (
                resistance_corrected / resistance_raw if resistance_raw != 0 else 1.0
            )
            loading_error = (
                ammeter_resistance / resistance_raw if resistance_raw != 0 else 0.0
            )
        else:
            resistance_corrected = resistance_raw

    elif connection_type == "reversed":
        # Voltmeter is across R only, but ammeter measures total current
        # I_measured = I_R + I_voltmeter
        # R_measured = V / (I_R + I_voltmeter) = R_true || R_voltmeter
        if voltmeter_resistance is not None and voltmeter_resistance > 0:
            # 1/R_measured = 1/R_true + 1/R_voltmeter
            # R_true = 1 / (1/R_measured - 1/R_voltmeter)
            if resistance_raw < voltmeter_resistance:
                # Can correct
                inverse_r = 1.0 / resistance_raw - 1.0 / voltmeter_resistance
                if abs(inverse_r) > 1e-15:
                    resistance_corrected = 1.0 / inverse_r
                else:
                    resistance_corrected = (
                        resistance_raw  # Can't correct, R ≈ R_voltmeter
                    )
            else:
                resistance_corrected = resistance_raw
            correction_factor = (
                resistance_corrected / resistance_raw if resistance_raw != 0 else 1.0
            )
            loading_error = 1.0 - correction_factor
        else:
            resistance_corrected = resistance_raw
    else:
        raise ValueError(f"Unknown connection_type: {connection_type}")

    # Ensure corrected resistance is positive
    if resistance_corrected <= 0:
        resistance_corrected = resistance_raw
        correction_factor = 1.0

    return {
        "resistance_raw": resistance_raw,
        "resistance_corrected": resistance_corrected,
        "correction_factor": correction_factor,
        "loading_error": loading_error,
        "voltage": voltage,
        "current": current,
    }


# =============================================================================
# DIFFERENTIAL GALVANOMETER METHOD (Arts. 341-345)
# =============================================================================


@maxwell_cite(
    341,
    342,
    343,
    344,
    345,
    theory_class="maxwell_original",
    description="Measure resistance using differential galvanometer",
)
def differential_galvanometer_method(
    coil1_current: float,
    coil2_current: float,
    known_resistance: float,
    coil1_turns: int = None,
    coil2_turns: int = None,
    coil1_resistance: float = None,
    coil2_resistance: float = None,
    null_deflection: float = 0.0,
) -> dict[str, float]:
    """
    Measure resistance using a differential galvanometer (Arts. 341-345).

    Maxwell's differential galvanometer has two coils wound on the same
    bobbin, producing opposing torques. When balanced (null deflection),
    the currents in the two coils are in a known ratio.

    Configuration (Art. 341):

        Unknown R_x --- Coil 1 --- Battery
                              |
        Known R_s   --- Coil 2 --- Battery

    Balance condition (Art. 342):
        n1 * I1 = n2 * I2  (equal and opposite torques)

    where n1, n2 are the number of turns in each coil.

    For equal coils (n1 = n2):
        I1 = I2 when R_x = R_s

    General case:
        R_x = R_s * (n1/n2) * (I2/I1)

    Args:
        coil1_current: Current through coil 1 with unknown resistance (abA).
        coil2_current: Current through coil 2 with known resistance (abA).
        known_resistance: Standard resistance in coil 2 circuit (abΩ).
        coil1_turns: Number of turns in coil 1 (default: equal to coil2).
        coil2_turns: Number of turns in coil 2 (default: same as coil1).
        coil1_resistance: Internal resistance of coil 1 (abΩ).
        coil2_resistance: Internal resistance of coil 2 (abΩ).
        null_deflection: Residual deflection at balance (default 0).

    Returns:
        Dictionary with:
        - unknown_resistance: Calculated R_x (abΩ)
        - turns_ratio: n1/n2
        - current_ratio: I2/I1
        - balance_error: Deviation from perfect null
        - sensitivity: d(deflection)/dR near balance

    Raises:
        ValueError: If currents are zero or known_resistance <= 0.

    References:
        Part II, Art. 341: Differential galvanometer principle.
        Part II, Art. 342: Balance condition derivation.
        Part II, Art. 343: Sensitivity analysis.
        Part II, Art. 344: Practical use.
        Part II, Art. 345: Error considerations.

    Example:
        >>> # Equal coils, balanced: I1 = 2 abA, I2 = 2 abA, R_s = 100 abΩ
        >>> result = differential_galvanometer_method(
        ...     coil1_current=2.0,
        ...     coil2_current=2.0,
        ...     known_resistance=100.0,
        ...     coil1_turns=100,
        ...     coil2_turns=100
        ... )
        >>> print(f"Unknown resistance: {result['unknown_resistance']:.2f} abΩ")
        100.0 abΩ
    """
    # Validate inputs
    if coil1_current == 0:
        raise ValueError(f"coil1_current cannot be zero")
    if coil2_current == 0:
        raise ValueError(f"coil2_current cannot be zero")
    if known_resistance <= 0:
        raise ValueError(f"known_resistance must be positive, got {known_resistance}")

    # Default to equal coils
    n1 = coil1_turns if coil1_turns is not None else 100
    n2 = coil2_turns if coil2_turns is not None else 100

    # Turns ratio
    turns_ratio = n1 / n2

    # Current ratio
    current_ratio = coil2_current / coil1_current

    # Calculate unknown resistance
    # From balance: n1 * I1 * (R_x + r1) = n2 * I2 * (R_s + r2)
    # Assuming coil resistances are small or compensated

    if coil1_resistance is not None and coil2_resistance is not None:
        # Include coil resistance corrections
        total_r2 = known_resistance + coil2_resistance
        # n1 * I1 * (R_x + r1) = n2 * I2 * (R_s + r2)
        # R_x = (n2/n1) * (I2/I1) * (R_s + r2) - r1
        unknown_resistance = (n2 / n1) * current_ratio * total_r2 - coil1_resistance
    else:
        # Simple case: R_x = R_s * (n2/n1) * (I2/I1)
        unknown_resistance = known_resistance * (n2 / n1) * current_ratio

    # Ensure positive resistance
    if unknown_resistance <= 0:
        unknown_resistance = known_resistance * current_ratio * (n2 / n1)

    # Balance error (deviation from perfect null)
    # At perfect balance: n1 * I1 = n2 * I2
    balance_condition = n1 * coil1_current - n2 * coil2_current
    balance_error = abs(balance_condition) / max(n1 * coil1_current, n2 * coil2_current)

    # Sensitivity: change in deflection per unit change in R_x
    # Near balance: deflection ∝ (n1*I1 - n2*I2)
    # d(deflection)/dR ≈ (n2 * I2 / R_s) * galvanometer_constant
    sensitivity = (n2 * coil2_current / known_resistance) * 0.01  # Approximate

    return {
        "unknown_resistance": unknown_resistance,
        "turns_ratio": turns_ratio,
        "current_ratio": current_ratio,
        "balance_error": balance_error,
        "sensitivity": sensitivity,
        "coil1_turns": n1,
        "coil2_turns": n2,
        "null_deflection": null_deflection,
    }


# =============================================================================
# WHEATSTONE BRIDGE MEASUREMENT (Arts. 346-350)
# =============================================================================


@maxwell_cite(
    346,
    347,
    348,
    349,
    350,
    theory_class="maxwell_original",
    description="Practical Wheatstone bridge measurement with error analysis",
)
def wheatstone_bridge_measurement(
    ratio_arm_p: float,
    ratio_arm_q: float,
    standard_resistance: float,
    galvanometer_deflection: float = None,
    battery_voltage: float = None,
    galvanometer_sensitivity: float = None,
) -> dict[str, float]:
    """
    Measure resistance using practical Wheatstone bridge (Arts. 346-350).

    Maxwell's practical bridge configuration (Art. 346):

             P              Q
        A ----/vvvvv---- B ----/vvvvv---- C
        |               |               |
       (+)             [G]             (-)
        |               |               |
        D ----/vvvvv---- E ----/vvvvv---- F
             R_x            R_s

    Balance condition (Art. 347):
        P / Q = R_x / R_s

    Therefore:
        R_x = R_s * (P / Q)

    Maxwell's improvements (Arts. 348-350):
    - Use ratio arms P, Q in decade steps (1, 10, 100, 1000)
    - Choose battery position for maximum sensitivity
    - Account for galvanometer sensitivity in uncertainty

    Args:
        ratio_arm_p: Resistance of first ratio arm P (abΩ).
        ratio_arm_q: Resistance of second ratio arm Q (abΩ).
        standard_resistance: Variable standard resistance R_s (abΩ).
        galvanometer_deflection: Observed deflection from null (divisions).
        battery_voltage: Applied voltage (abvolts).
        galvanometer_sensitivity: Current sensitivity (abA/division).

    Returns:
        Dictionary with:
        - unknown_resistance: Calculated R_x (abΩ)
        - ratio_setting: P/Q ratio
        - balance_tolerance: Uncertainty from galvanometer resolution
        - sensitivity: Bridge sensitivity at operating point
        - optimal_ratio: Recommended P/Q for best accuracy

    Raises:
        ValueError: If ratio arms or standard are non-positive.

    References:
        Part II, Art. 346: Practical bridge configuration.
        Part II, Art. 347: Balance equation.
        Part II, Art. 348: Ratio arm selection.
        Part II, Art. 349: Sensitivity optimization.
        Part II, Art. 350: Error minimization.

    Example:
        >>> # Bridge with ratio 1:10, standard = 1234 abΩ
        >>> result = wheatstone_bridge_measurement(
        ...     ratio_arm_p=100.0,
        ...     ratio_arm_q=1000.0,
        ...     standard_resistance=1234.0
        ... )
        >>> print(f"Unknown resistance: {result['unknown_resistance']:.2f} abΩ")
        123.4 abΩ
    """
    # Validate inputs
    if ratio_arm_p <= 0:
        raise ValueError(f"ratio_arm_p must be positive, got {ratio_arm_p}")
    if ratio_arm_q <= 0:
        raise ValueError(f"ratio_arm_q must be positive, got {ratio_arm_q}")
    if standard_resistance <= 0:
        raise ValueError(
            f"standard_resistance must be positive, got {standard_resistance}"
        )

    # Ratio setting
    ratio_setting = ratio_arm_p / ratio_arm_q

    # Calculate unknown resistance
    # R_x = R_s * (P / Q)
    unknown_resistance = standard_resistance * ratio_setting

    # Estimate measurement uncertainty
    # Dominated by: standard accuracy, ratio accuracy, galvanometer resolution

    # Standard resistance uncertainty (assume 0.1% typical)
    u_standard = 0.001 * standard_resistance

    # Ratio arm uncertainty (assume 0.1% each)
    u_ratio = math.sqrt(0.001**2 + 0.001**2) * ratio_setting

    # Galvanometer resolution contribution
    if (
        galvanometer_deflection is not None
        and galvanometer_sensitivity is not None
        and battery_voltage is not None
    ):
        # Smallest detectable change in R_x
        # ΔR_x ≈ (galvanometer_current * total_resistance^2) / V
        total_r = ratio_arm_p + ratio_arm_q + standard_resistance + unknown_resistance
        min_detectable_i = galvanometer_sensitivity  # Current for 1 division
        u_galvanometer = (
            abs(galvanometer_deflection) * min_detectable_i * total_r / battery_voltage
            if battery_voltage > 0
            else 0
        )
    else:
        # Default estimate: 0.1% of reading
        u_galvanometer = 0.001 * unknown_resistance

    # Combined uncertainty (RSS)
    u_combined = math.sqrt(
        u_standard**2 * ratio_setting**2
        + u_ratio**2 * standard_resistance**2
        + u_galvanometer**2
    )

    # Balance tolerance
    balance_tolerance = u_combined

    # Sensitivity (relative change per division)
    sensitivity = u_combined / unknown_resistance if unknown_resistance > 0 else 0

    # Optimal ratio (for best sensitivity, P ≈ Q when R_x ≈ R_s)
    optimal_ratio = 1.0
    if unknown_resistance > 0:
        # Best when ratio arms bracket the unknown
        optimal_ratio = (
            math.sqrt(standard_resistance / unknown_resistance)
            if unknown_resistance > 0
            else 1.0
        )

    return {
        "unknown_resistance": unknown_resistance,
        "ratio_setting": ratio_setting,
        "balance_tolerance": balance_tolerance,
        "sensitivity": sensitivity,
        "optimal_ratio": optimal_ratio,
        "ratio_arm_p": ratio_arm_p,
        "ratio_arm_q": ratio_arm_q,
        "standard_resistance": standard_resistance,
    }


# =============================================================================
# LOW RESISTANCE MEASUREMENT (Arts. 351-354)
# =============================================================================


@maxwell_cite(
    351,
    352,
    353,
    theory_class="maxwell_original",
    description="Kelvin double bridge for low resistance measurement",
)
def kelvin_double_bridge(
    outer_ratio_p: float,
    outer_ratio_q: float,
    inner_ratio_p_prime: float,
    inner_ratio_q_prime: float,
    standard_resistance: float,
    link_resistance: float = None,
) -> dict[str, float]:
    """
    Measure very low resistances using Kelvin double bridge (Arts. 351-353).

    The Kelvin double bridge (Thomson bridge) eliminates the effect of
    lead and contact resistances when measuring very low resistances
    (typically < 1 ohm).

    Configuration (Art. 351):

                  P              Q
        C1 ----/vvvvv---- B1 ----/vvvvv---- C2
        |                |                |
       (+)              [G]              (-)
        |                |                |
        C3 ----/vvvvv---- B2 ----/vvvvv---- C4
                 P'             Q'

        R_x between C1-C3 (unknown, 4-terminal)
        R_s between C2-C4 (standard, 4-terminal)
        Link resistance between C1-C2 and C3-C4

    Balance condition (Art. 352):
        R_x / R_s = P / Q = P' / Q'

    The double bridge requires TWO ratio conditions:
        1. Outer ratio: P / Q
        2. Inner ratio: P' / Q'

    When P/Q = P'/Q', the link resistance has NO effect on the measurement.

    Args:
        outer_ratio_p: Outer ratio arm P (abΩ).
        outer_ratio_q: Outer ratio arm Q (abΩ).
        inner_ratio_p_prime: Inner ratio arm P' (abΩ).
        inner_ratio_q_prime: Inner ratio arm Q' (abΩ).
        standard_resistance: Low-value standard resistance (abΩ).
        link_resistance: Resistance of connecting link (abΩ).

    Returns:
        Dictionary with:
        - unknown_resistance: Calculated R_x (abΩ)
        - outer_ratio: P/Q
        - inner_ratio: P'/Q'
        - ratio_match_error: |P/Q - P'/Q'| (should be ~0)
        - link_error_correction: Correction due to link resistance
        - measurement_valid: True if bridge properly balanced

    Raises:
        ValueError: If any ratio arm is non-positive.

    References:
        Part II, Art. 351: Kelvin double bridge principle.
        Part II, Art. 352: Balance conditions.
        Part II, Art. 353: Error analysis and corrections.

    Example:
        >>> # Measure 0.001 abΩ using equal ratios
        >>> result = kelvin_double_bridge(
        ...     outer_ratio_p=1000.0,
        ...     outer_ratio_q=1000.0,
        ...     inner_ratio_p_prime=1000.0,
        ...     inner_ratio_q_prime=1000.0,
        ...     standard_resistance=0.001
        ... )
        >>> print(f"Unknown resistance: {result['unknown_resistance']:.6f} abΩ")
        0.001000 abΩ
    """
    # Validate inputs
    for val, name in [
        (outer_ratio_p, "outer_ratio_p"),
        (outer_ratio_q, "outer_ratio_q"),
        (inner_ratio_p_prime, "inner_ratio_p_prime"),
        (inner_ratio_q_prime, "inner_ratio_q_prime"),
        (standard_resistance, "standard_resistance"),
    ]:
        if val <= 0:
            raise ValueError(f"{name} must be positive, got {val}")

    # Calculate ratios
    outer_ratio = outer_ratio_p / outer_ratio_q
    inner_ratio = inner_ratio_p_prime / inner_ratio_q_prime

    # Ratio match error (should be zero for ideal Kelvin bridge)
    ratio_match_error = abs(outer_ratio - inner_ratio)

    # Calculate unknown resistance
    # Primary: R_x = R_s * (P / Q)
    unknown_resistance_primary = standard_resistance * outer_ratio

    # Correction for link resistance (if ratios don't perfectly match)
    # ΔR_x = r_link * (P/Q - P'/Q') * Q' / (P' + Q')
    if link_resistance is not None and ratio_match_error > 1e-10:
        correction = (
            link_resistance
            * ratio_match_error
            * inner_ratio_q_prime
            / (inner_ratio_p_prime + inner_ratio_q_prime)
        )
        link_error_correction = correction
    else:
        link_error_correction = 0.0

    # Final resistance with correction
    unknown_resistance = unknown_resistance_primary + link_error_correction

    # Validity check: ratios should match within 0.1% for accurate measurement
    measurement_valid = ratio_match_error < 0.001 * outer_ratio

    return {
        "unknown_resistance": unknown_resistance,
        "outer_ratio": outer_ratio,
        "inner_ratio": inner_ratio,
        "ratio_match_error": ratio_match_error,
        "link_error_correction": link_error_correction,
        "measurement_valid": measurement_valid,
        "standard_resistance": standard_resistance,
    }


@maxwell_cite(
    354,
    theory_class="maxwell_original",
    description="Four-terminal (Kelvin) resistance measurement",
)
def four_terminal_measurement(
    voltage_sense: float,
    current_force: float,
    lead_resistance_estimate: float = None,
    contact_resistance_estimate: float = None,
) -> dict[str, float]:
    """
    Measure low resistance using four-terminal (Kelvin) method (Art. 354).

    The four-terminal method separates current-carrying leads from
    voltage-sensing leads, eliminating the effect of lead and contact
    resistances.

    Configuration (Art. 354):

        Current Source (+) ----[Lead]---- C1 ---- R_x ---- C2 ----[Lead]---- Current Source (-)
                                          |                    |
                                          |                    |
                                    V sense (+)          V sense (-)

    The voltmeter draws negligible current, so lead/contact resistances
    in the sense circuit don't affect the measurement.

    R_x = V_sense / I_force

    This is the basis for precision low-resistance measurement and is
    used in modern digital multimeters for ohms ranges below 100 ohms.

    Args:
        voltage_sense: Measured voltage between sense terminals (abvolts).
        current_force: Applied current through force terminals (abA).
        lead_resistance_estimate: Estimated lead resistance for uncertainty (abΩ).
        contact_resistance_estimate: Estimated contact resistance (abΩ).

    Returns:
        Dictionary with:
        - resistance: Calculated R_x (abΩ)
        - measurement_uncertainty: Estimated uncertainty (abΩ)
        - relative_uncertainty: Fractional uncertainty
        - min_detectable_resistance: Lower limit of measurement

    Raises:
        ValueError: If current_force is zero.

    References:
        Part II, Art. 354: Four-terminal measurement principle.

    Example:
        >>> # Measure low resistance: 0.01 abV drop at 10 abA
        >>> result = four_terminal_measurement(
        ...     voltage_sense=0.01,
        ...     current_force=10.0
        ... )
        >>> print(f"Resistance: {result['resistance']:.6f} abΩ")
        0.001000 abΩ
    """
    # Validate inputs
    if current_force == 0:
        raise ValueError("current_force cannot be zero")

    # Calculate resistance
    resistance = voltage_sense / current_force

    # Ensure positive resistance (passive element)
    if resistance < 0:
        resistance = abs(resistance)

    # Estimate uncertainty
    # Dominated by: voltmeter resolution, current source stability

    # Voltmeter resolution (assume 1 μV typical for precision DMM)
    u_voltage = 1e-6  # abV (1 μV)

    # Current source stability (assume 0.01% typical)
    u_current = 0.0001 * abs(current_force)

    # Lead/contact resistance uncertainty (if estimates provided)
    if lead_resistance_estimate is not None:
        u_lead = 0.1 * lead_resistance_estimate  # 10% uncertainty
    else:
        u_lead = 0

    if contact_resistance_estimate is not None:
        u_contact = 0.1 * contact_resistance_estimate
    else:
        u_contact = 0

    # Combined uncertainty using error propagation
    # u_R = R * sqrt((u_V/V)^2 + (u_I/I)^2)
    rel_u_voltage = u_voltage / abs(voltage_sense) if voltage_sense != 0 else 0
    rel_u_current = u_current / abs(current_force) if current_force != 0 else 0

    rel_uncertainty = math.sqrt(rel_u_voltage**2 + rel_u_current**2)
    measurement_uncertainty = resistance * rel_uncertainty

    # Add lead/contact uncertainties in quadrature
    total_uncertainty = math.sqrt(measurement_uncertainty**2 + u_lead**2 + u_contact**2)

    # Relative uncertainty
    relative_uncertainty = (
        total_uncertainty / resistance if resistance > 0 else float("inf")
    )

    # Minimum detectable resistance (when V_sense = u_voltage)
    min_detectable = u_voltage / abs(current_force)

    return {
        "resistance": resistance,
        "measurement_uncertainty": total_uncertainty,
        "relative_uncertainty": relative_uncertainty,
        "min_detectable_resistance": min_detectable,
        "voltage_sense": voltage_sense,
        "current_force": current_force,
    }


# =============================================================================
# HIGH RESISTANCE MEASUREMENT (Arts. 355-358)
# =============================================================================


@maxwell_cite(
    355,
    356,
    theory_class="maxwell_original",
    description="High resistance measurement using leakage method",
)
def leakage_method(
    capacitor_capacitance: float,
    initial_voltage: float,
    final_voltage: float,
    discharge_time: float,
    insulation_resistance_estimate: float = None,
) -> dict[str, float]:
    """
    Measure high resistance (insulation) using capacitor leakage (Arts. 355-356).

    Maxwell's leakage method measures very high resistances by observing
    the discharge of a capacitor through the unknown resistance.

    Principle (Art. 355):
    - Charge a capacitor to voltage V0
    - Connect unknown resistance R across capacitor
    - Measure voltage V after time t
    - Calculate R from exponential decay

    V(t) = V0 * exp(-t / (R * C))

    Solving for R:
    R = -t / (C * ln(V / V0)) = t / (C * ln(V0 / V))

    This method can measure resistances up to 10^12 ohms or higher,
    limited only by capacitor leakage and electrometer input impedance.

    Args:
        capacitor_capacitance: Capacitance of test capacitor (abF).
        initial_voltage: Initial capacitor voltage V0 (abvolts).
        final_voltage: Voltage after discharge time t (abvolts).
        discharge_time: Time interval for discharge (seconds).
        insulation_resistance_estimate: Expected range for sanity check (abΩ).

    Returns:
        Dictionary with:
        - insulation_resistance: Calculated R (abΩ)
        - time_constant: τ = R*C (seconds)
        - voltage_ratio: V0/V
        - decay_fraction: (V0 - V) / V0
        - measurement_validity: True if measurement is within valid range

    Raises:
        ValueError: If voltages are invalid or V_final >= V_initial.

    References:
        Part II, Art. 355: Leakage method principle.
        Part II, Art. 356: Insulation resistance measurement.

    Example:
        >>> # 1 μF capacitor discharges from 100V to 50V in 100s
        >>> result = leakage_method(
        ...     capacitor_capacitance=1e-6,
        ...     initial_voltage=100.0,
        ...     final_voltage=50.0,
        ...     discharge_time=100.0
        ... )
        >>> print(f"Insulation resistance: {result['insulation_resistance']:.2e} abΩ")
        ~1.44e8 abΩ
    """
    # Validate inputs
    if capacitor_capacitance <= 0:
        raise ValueError(
            f"capacitor_capacitance must be positive, got {capacitor_capacitance}"
        )
    if initial_voltage <= 0:
        raise ValueError(f"initial_voltage must be positive, got {initial_voltage}")
    if final_voltage <= 0:
        raise ValueError(f"final_voltage must be positive, got {final_voltage}")
    if final_voltage >= initial_voltage:
        raise ValueError(
            f"final_voltage ({final_voltage}) must be less than initial_voltage ({initial_voltage})"
        )
    if discharge_time <= 0:
        raise ValueError(f"discharge_time must be positive, got {discharge_time}")

    # Voltage ratio
    voltage_ratio = initial_voltage / final_voltage

    # Calculate resistance
    # R = t / (C * ln(V0 / V))
    ln_ratio = math.log(voltage_ratio)
    insulation_resistance = discharge_time / (capacitor_capacitance * ln_ratio)

    # Time constant
    time_constant = insulation_resistance * capacitor_capacitance

    # Decay fraction
    decay_fraction = (initial_voltage - final_voltage) / initial_voltage

    # Validity check
    # Good measurement when: 0.1 < V/V0 < 0.9 (10% to 90% discharge)
    v_ratio_normalized = final_voltage / initial_voltage
    measurement_validity = 0.1 < v_ratio_normalized < 0.9

    # Estimate uncertainty
    # Dominated by: voltage measurement accuracy, timing accuracy, capacitor tolerance

    u_voltage_ratio = 0.01 * voltage_ratio  # 1% voltage measurement
    u_time = 0.001 * discharge_time  # 0.1% timing
    u_capacitance = 0.05 * capacitor_capacitance  # 5% capacitor tolerance

    # Error propagation
    rel_uncertainty = math.sqrt(
        (u_voltage_ratio / voltage_ratio) ** 2
        + (u_time / discharge_time) ** 2
        + (u_capacitance / capacitor_capacitance) ** 2
    )

    uncertainty = insulation_resistance * rel_uncertainty

    return {
        "insulation_resistance": insulation_resistance,
        "time_constant": time_constant,
        "voltage_ratio": voltage_ratio,
        "decay_fraction": decay_fraction,
        "measurement_validity": measurement_validity,
        "uncertainty": uncertainty,
        "capacitor_capacitance": capacitor_capacitance,
        "initial_voltage": initial_voltage,
        "final_voltage": final_voltage,
        "discharge_time": discharge_time,
    }


@maxwell_cite(
    357,
    358,
    theory_class="maxwell_original",
    description="Capacitor discharge method for very high resistance",
)
def capacitor_discharge_method(
    capacitance: float,
    voltage_measurements: list[tuple[float, float]],
    electrometer_leakage: float = None,
) -> dict[str, float]:
    """
    Measure very high resistance using capacitor discharge curve fitting (Arts. 357-358).

    Maxwell's refinement (Arts. 357-358) uses multiple voltage measurements
    over time to fit the exponential decay curve, improving accuracy and
    allowing estimation of systematic errors.

    Method:
    - Collect voltage vs. time data: (t_i, V_i)
    - Fit to model: V(t) = V0 * exp(-t / (R * C))
    - Extract R from time constant τ = R * C

    Using linear regression on ln(V) vs t:
    ln(V) = ln(V0) - t / (R * C)

    Slope m = -1 / (R * C)
    Therefore: R = -1 / (m * C)

    This method can measure resistances up to 10^15 ohms with proper
    shielding and guarding techniques.

    Args:
        capacitance: Capacitance (abF).
        voltage_measurements: List of (time_seconds, voltage_abvolts) tuples.
        electrometer_leakage: Electrometer input leakage current (abA).

    Returns:
        Dictionary with:
        - resistance: Fitted resistance value (abΩ)
        - initial_voltage: Fitted V0 (abvolts)
        - time_constant: τ = R*C (seconds)
        - fit_quality: R-squared value of the fit
        - resistance_uncertainty: Standard error of fitted R

    Raises:
        ValueError: If fewer than 2 measurements or invalid data.

    References:
        Part II, Art. 357: Multi-point discharge method.
        Part II, Art. 358: Error analysis and corrections.

    Example:
        >>> # Discharge curve: 1 μF, measurements every 10 seconds
        >>> data = [(0, 100), (10, 82), (20, 67), (30, 55), (40, 45)]
        >>> result = capacitor_discharge_method(
        ...     capacitance=1e-6,
        ...     voltage_measurements=data
        ... )
        >>> print(f"Resistance: {result['resistance']:.2e} abΩ")
    """
    # Validate inputs
    if len(voltage_measurements) < 2:
        raise ValueError(
            f"At least 2 voltage measurements required, got {len(voltage_measurements)}"
        )
    if capacitance <= 0:
        raise ValueError(f"capacitance must be positive, got {capacitance}")

    # Extract data
    times = np.array([t for t, v in voltage_measurements], dtype=np.float64)
    voltages = np.array([v for t, v in voltage_measurements], dtype=np.float64)

    # Validate voltages
    if np.any(voltages <= 0):
        raise ValueError("All voltages must be positive for logarithmic analysis")
    if np.any(np.diff(times) <= 0):
        raise ValueError("Times must be strictly increasing")

    # Linear regression on ln(V) vs t
    # ln(V) = ln(V0) - t / (R * C)
    ln_voltages = np.log(voltages)

    # Linear fit: y = a + b * x
    # where y = ln(V), x = t, b = -1/(R*C), a = ln(V0)
    n = len(times)
    sum_t = np.sum(times)
    sum_ln_v = np.sum(ln_voltages)
    sum_t_sq = np.sum(times**2)
    sum_t_ln_v = np.sum(times * ln_voltages)

    # Least squares fit
    denom = n * sum_t_sq - sum_t**2
    if abs(denom) < 1e-15:
        raise ValueError("Time values too close together for reliable fit")

    slope = (n * sum_t_ln_v - sum_t * sum_ln_v) / denom
    intercept = (sum_ln_v - slope * sum_t) / n

    # Calculate resistance from slope
    # slope = -1 / (R * C)
    # R = -1 / (slope * C)
    if slope >= 0:
        raise ValueError("Slope must be negative for exponential decay")

    resistance = -1.0 / (slope * capacitance)

    # Initial voltage from intercept
    initial_voltage = math.exp(intercept)

    # Time constant
    time_constant = resistance * capacitance

    # Calculate R-squared for fit quality
    ln_v_predicted = intercept + slope * times
    ss_res = np.sum((ln_voltages - ln_v_predicted) ** 2)
    ss_tot = np.sum((ln_voltages - np.mean(ln_voltages)) ** 2)
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Standard error of slope
    if n > 2:
        se_slope = math.sqrt(ss_res / (n - 2)) / math.sqrt(sum_t_sq - sum_t**2 / n)
        # Propagate to resistance uncertainty
        # R = -1 / (slope * C)
        # dR = |dR/dslope| * dslope = (1 / (slope^2 * C)) * dslope = R * (dslope / |slope|)
        resistance_uncertainty = abs(resistance * se_slope / slope)
    else:
        resistance_uncertainty = resistance * 0.1  # Default 10% for n=2

    # Correction for electrometer leakage (if known)
    # The measured R is actually R_insulation || R_electrometer
    # 1/R_measured = 1/R_insulation + 1/R_electrometer
    corrected_resistance = resistance
    if electrometer_leakage is not None and electrometer_leakage > 0:
        # Estimate electrometer resistance from typical leakage
        # R_electrometer ≈ V_max / I_leakage
        v_max = max(voltages)
        r_electrometer = v_max / electrometer_leakage
        # Correct: 1/R_insulation = 1/R_measured - 1/R_electrometer
        inverse_r_insulation = 1.0 / resistance - 1.0 / r_electrometer
        if inverse_r_insulation > 0:
            corrected_resistance = 1.0 / inverse_r_insulation

    return {
        "resistance": resistance,
        "corrected_resistance": corrected_resistance,
        "initial_voltage": initial_voltage,
        "time_constant": time_constant,
        "fit_quality": r_squared,
        "resistance_uncertainty": resistance_uncertainty,
        "slope": slope,
        "intercept": intercept,
        "num_measurements": n,
    }


# =============================================================================
# COMPREHENSIVE RESISTANCE MEASUREMENT ANALYZER
# =============================================================================


@dataclass
class ResistanceMeasurementAnalyzer:
    """
    Comprehensive analyzer for resistance measurements.

    This class provides a unified interface for all resistance measurement
    methods implemented by Maxwell, with automatic method selection based
    on resistance range and automatic uncertainty analysis.

    Attributes:
        method: Selected measurement method.
        calibration_data: Calibration coefficients.
        reference_temperature: Reference temperature for corrections.
    """

    method: str = "auto"
    calibration_data: dict = field(default_factory=dict)
    reference_temperature: float = 20.0

    @staticmethod
    def select_method(estimated_resistance: float) -> str:
        """
        Select appropriate measurement method based on resistance range.

        Maxwell's guidance (Arts. 346-358):
        - < 1 ohm: Kelvin double bridge or four-terminal
        - 1 ohm to 1 Mohm: Wheatstone bridge
        - > 1 Mohm: Leakage or capacitor discharge

        Args:
            estimated_resistance: Approximate resistance value (abΩ).

        Returns:
            Recommended method name.
        """
        if estimated_resistance < 1.0:
            return "kelvin_double_bridge"
        elif estimated_resistance < 1e6:
            return "wheatstone_bridge"
        elif estimated_resistance < 1e10:
            return "leakage_method"
        else:
            return "capacitor_discharge"

    def analyze(
        self,
        method: str,
        measurement_data: dict,
        uncertainty_budget: dict = None,
    ) -> MeasurementError:
        """
        Perform comprehensive analysis of resistance measurement.

        Args:
            method: Measurement method used.
            measurement_data: Raw measurement data.
            uncertainty_budget: Optional uncertainty components.

        Returns:
            MeasurementError object with full uncertainty analysis.
        """
        # Extract resistance value based on method
        if method == "substitution":
            r_value = measurement_data.get("unknown_resistance", 0)
        elif method == "differential_galvanometer":
            r_value = measurement_data.get("unknown_resistance", 0)
        elif method == "wheatstone_bridge":
            r_value = measurement_data.get("unknown_resistance", 0)
        elif method == "kelvin_double_bridge":
            r_value = measurement_data.get("unknown_resistance", 0)
        elif method == "four_terminal":
            r_value = measurement_data.get("resistance", 0)
        elif method == "leakage_method":
            r_value = measurement_data.get("insulation_resistance", 0)
        elif method == "capacitor_discharge":
            r_value = measurement_data.get("resistance", 0)
        else:
            r_value = 0

        # Build uncertainty budget
        if uncertainty_budget:
            sys_unc = uncertainty_budget.get("systematic", 0)
            rand_unc = uncertainty_budget.get("random", 0)
            cal_unc = uncertainty_budget.get("calibration", 0)
            res_unc = uncertainty_budget.get("resolution", 0)
        else:
            # Default estimates based on method
            sys_unc = 0.001 * r_value  # 0.1% systematic
            rand_unc = 0.0005 * r_value  # 0.05% random
            cal_unc = 0.001 * r_value  # 0.1% calibration
            res_unc = 0.0

        return MeasurementError(
            resistance_value=r_value,
            systematic_uncertainty=sys_unc,
            random_uncertainty=rand_unc,
            calibration_uncertainty=cal_unc,
            resolution_uncertainty=res_unc,
            method=method,
        )


# =============================================================================
# MAIN: Module verification and examples
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RESISTANCE MEASUREMENT")
    print("Maxwell's Treatise, Part II, Chapter XI (Arts. 335-358)")
    print("=" * 70)

    # Test substitution method
    print("\n--- Substitution Method (Arts. 335-340) ---")
    result = substitution_method(
        unknown_current=3.5, standard_current=4.2, standard_resistance=100.0
    )
    print(f"  Unknown resistance: {result['unknown_resistance']:.2f} abohm")
    print(f"  Current ratio: {result['ratio_currents']:.4f}")

    # Test V-I method
    print("\n--- Voltage-Current Method (Arts. 338-340) ---")
    result = calculate_resistance_from_voltage(
        voltage=100.0, current=2.0, ammeter_resistance=0.5, connection_type="standard"
    )
    print(f"  Raw resistance: {result['resistance_raw']:.2f} abohm")
    print(f"  Corrected resistance: {result['resistance_corrected']:.2f} abohm")

    # Test differential galvanometer
    print("\n--- Differential Galvanometer (Arts. 341-345) ---")
    result = differential_galvanometer_method(
        coil1_current=2.0,
        coil2_current=2.0,
        known_resistance=100.0,
        coil1_turns=100,
        coil2_turns=100,
    )
    print(f"  Unknown resistance: {result['unknown_resistance']:.2f} abohm")
    print(f"  Balance error: {result['balance_error']:.6f}")

    # Test Wheatstone bridge
    print("\n--- Wheatstone Bridge (Arts. 346-350) ---")
    result = wheatstone_bridge_measurement(
        ratio_arm_p=100.0, ratio_arm_q=1000.0, standard_resistance=1234.0
    )
    print(f"  Unknown resistance: {result['unknown_resistance']:.2f} abohm")
    print(f"  Ratio setting: {result['ratio_setting']:.4f}")

    # Test Kelvin double bridge
    print("\n--- Kelvin Double Bridge (Arts. 351-354) ---")
    result = kelvin_double_bridge(
        outer_ratio_p=1000.0,
        outer_ratio_q=1000.0,
        inner_ratio_p_prime=1000.0,
        inner_ratio_q_prime=1000.0,
        standard_resistance=0.001,
    )
    print(f"  Unknown resistance: {result['unknown_resistance']:.6f} abohm")
    print(f"  Measurement valid: {result['measurement_valid']}")

    # Test four-terminal measurement
    print("\n--- Four-Terminal Measurement (Art. 354) ---")
    result = four_terminal_measurement(voltage_sense=0.01, current_force=10.0)
    print(f"  Resistance: {result['resistance']:.6f} abohm")
    print(f"  Relative uncertainty: {result['relative_uncertainty']:.6f}")

    # Test leakage method
    print("\n--- Leakage Method (Arts. 355-356) ---")
    result = leakage_method(
        capacitor_capacitance=1e-6,
        initial_voltage=100.0,
        final_voltage=50.0,
        discharge_time=100.0,
    )
    print(f"  Insulation resistance: {result['insulation_resistance']:.2e} abohm")
    print(f"  Time constant: {result['time_constant']:.2f} s")

    # Test capacitor discharge
    print("\n--- Capacitor Discharge Method (Arts. 357-358) ---")
    data = [(0, 100), (10, 82), (20, 67), (30, 55), (40, 45)]
    result = capacitor_discharge_method(capacitance=1e-6, voltage_measurements=data)
    print(f"  Resistance: {result['resistance']:.2e} abohm")
    print(f"  Fit quality (R2): {result['fit_quality']:.6f}")

    # Test MeasurementError class
    print("\n--- Measurement Error Analysis ---")
    error = MeasurementError(
        resistance_value=100.0,
        systematic_uncertainty=0.1,
        random_uncertainty=0.05,
        calibration_uncertainty=0.1,
        method="wheatstone_bridge",
    )
    print(f"  Combined uncertainty: {error.combined_standard_uncertainty:.4f} abohm")
    print(f"  Relative uncertainty: {error.relative_uncertainty:.6f}")
    print(f"  Expanded uncertainty (k=2): {error.expanded_uncertainty:.4f} abohm")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)
