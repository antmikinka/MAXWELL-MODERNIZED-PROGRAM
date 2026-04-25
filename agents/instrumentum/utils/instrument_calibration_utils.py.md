# Utility: instrument_calibration_utils

## Purpose

Python utility module for instrument calibration procedures and traceability calculations.

## Location

`agents/instrumentum/utils/instrument_calibration_utils.py`

---

## Module Contents

```python
"""
INSTRUMENTUM Calibration Utilities

Calibration procedure automation and traceability calculations
for instruments in the Maxwell Treatise Modernization Project.

Calibration Hierarchy:
- Primary Standards: NIST, PTB, NPL (quantum standards)
- Secondary Standards: Accredited laboratory standards
- Working Standards: Laboratory reference instruments
- Field Instruments: Operating measurement devices

Theory Classification:
- maxwell_original: Maxwell's 1873 measurement principles
- user_original: User's calibration extensions (DO NOT CHANGE)
- standard_math: Standard calibration implementations

Maxwell References: Art. 287-300, Art. 343-348, Art. 730-750
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import numpy as np


class CalibrationLevel(Enum):
    """Calibration hierarchy levels."""
    PRIMARY = "primary"           # National metrology institute
    SECONDARY = "secondary"       # Accredited laboratory
    WORKING = "working"           # Laboratory reference
    FIELD = "field"              # Operating instrument


class CalibrationStatus(Enum):
    """Calibration status."""
    CALIBRATED = "calibrated"
    DUE_SOON = "due_soon"        # Within 30 days
    OVERDUE = "overdue"
    OUT_OF_TOLERANCE = "out_of_tolerance"
    NOT_CALIBRATABLE = "not_calibratable"


@dataclass
class CalibrationPoint:
    """Single calibration point."""
    nominal_value: float
    measured_value: float
    standard_value: float
    standard_uncertainty: float
    unit: str
    deviation: float
    tolerance: float
    
    @property
    def error(self) -> float:
        """Calculate error."""
        return self.measured_value - self.nominal_value
    
    @property
    def correction(self) -> float:
        """Calculate correction."""
        return -self.error
    
    @property
    def within_tolerance(self) -> bool:
        """Check if within tolerance."""
        return abs(self.error) <= self.tolerance


@dataclass
class CalibrationCertificate:
    """Complete calibration certificate."""
    instrument_id: str
    instrument_name: str
    calibration_date: datetime
    next_due_date: datetime
    calibration_level: CalibrationLevel
    status: CalibrationStatus
    points: List[CalibrationPoint]
    environmental_conditions: Dict[str, float]
    technician: str
    certificate_number: str
    traceability_chain: List[str]
    combined_uncertainty: float
    coverage_factor: float
    expanded_uncertainty: float
    confidence_level: float


# ============================================================================
# CALIBRATION HIERARCHY
# ============================================================================

def get_traceability_chain(
    instrument_level: CalibrationLevel
) -> List[str]:
    """
    Get traceability chain for calibration level.
    
    Args:
        instrument_level: Level of instrument
    
    Returns:
        List of traceability levels from primary to instrument
    """
    chains = {
        CalibrationLevel.PRIMARY: [
            "NIST Quantum Standards",
            "Primary Standard"
        ],
        CalibrationLevel.SECONDARY: [
            "NIST Quantum Standards",
            "Primary Standard",
            "Secondary Standard"
        ],
        CalibrationLevel.WORKING: [
            "NIST Quantum Standards",
            "Primary Standard",
            "Secondary Standard",
            "Working Standard"
        ],
        CalibrationLevel.FIELD: [
            "NIST Quantum Standards",
            "Primary Standard",
            "Secondary Standard",
            "Working Standard",
            "Field Instrument"
        ]
    }
    
    return chains.get(instrument_level, [])


def calculate_tur(
    tolerance: float,
    uncertainty: float
) -> float:
    """
    Calculate Test Uncertainty Ratio (TUR).
    
    Args:
        tolerance: Instrument tolerance
        uncertainty: Calibration uncertainty
    
    Returns:
        TUR value
    
    Note:
        TUR >= 4:1 is acceptable
        TUR >= 2:1 is marginal
        TUR < 2:1 is unacceptable
    """
    if uncertainty == 0:
        return float('inf')
    
    return tolerance / uncertainty


def tur_acceptance(tur: float) -> Tuple[bool, str]:
    """
    Evaluate TUR acceptance.
    
    Args:
        tur: Test Uncertainty Ratio
    
    Returns:
        (is_acceptable, recommendation)
    """
    if tur >= 4.0:
        return True, "Acceptable - TUR >= 4:1"
    elif tur >= 2.0:
        return False, "Marginal - Use with caution, TUR >= 2:1"
    else:
        return False, "Unacceptable - TUR < 2:1, improve calibration"


# ============================================================================
# CALIBRATION POINTS
# ============================================================================

def create_calibration_point(
    nominal_value: float,
    measured_value: float,
    standard_value: float,
    standard_uncertainty: float,
    tolerance: float,
    unit: str
) -> CalibrationPoint:
    """
    Create calibration point with calculated fields.
    
    Args:
        nominal_value: Nominal instrument reading
        measured_value: Actual measured value
        standard_value: Reference standard value
        standard_uncertainty: Standard uncertainty
        tolerance: Acceptable tolerance
        unit: Unit of measurement
    
    Returns:
        CalibrationPoint with all fields populated
    """
    deviation = measured_value - standard_value
    
    return CalibrationPoint(
        nominal_value=nominal_value,
        measured_value=measured_value,
        standard_value=standard_value,
        standard_uncertainty=standard_uncertainty,
        unit=unit,
        deviation=deviation,
        tolerance=tolerance
    )


def calculate_linearity_error(
    calibration_points: List[CalibrationPoint]
) -> Tuple[float, float, float]:
    """
    Calculate linearity error from calibration points.
    
    Args:
        calibration_points: List of calibration points
    
    Returns:
        (max_positive_error, max_negative_error, non_linearity)
    """
    errors = [pt.error for pt in calibration_points]
    
    max_positive = max(errors)
    max_negative = min(errors)
    non_linearity = max_positive - max_negative
    
    return max_positive, max_negative, non_linearity


def calculate_hysteresis(
    upscale_points: List[CalibrationPoint],
    downscale_points: List[CalibrationPoint]
) -> float:
    """
    Calculate hysteresis from upscale and downscale readings.
    
    Args:
        upscale_points: Calibration points going up
        downscale_points: Calibration points going down
    
    Returns:
        Maximum hysteresis (same units as measurements)
    """
    if len(upscale_points) != len(downscale_points):
        raise ValueError("Mismatched number of calibration points")
    
    hysteresis_values = []
    for up, down in zip(upscale_points, downscale_points):
        if abs(up.nominal_value - down.nominal_value) < 1e-10:
            hysteresis_values.append(abs(up.error - down.error))
    
    return max(hysteresis_values) if hysteresis_values else 0.0


# ============================================================================
# CALIBRATION STATUS
# ============================================================================

def determine_calibration_status(
    calibration_date: datetime,
    calibration_interval_months: int,
    out_of_tolerance: bool
) -> CalibrationStatus:
    """
    Determine calibration status.
    
    Args:
        calibration_date: Date of last calibration
        calibration_interval_months: Calibration interval in months
        out_of_tolerance: True if last calibration failed
    
    Returns:
        CalibrationStatus
    """
    if out_of_tolerance:
        return CalibrationStatus.OUT_OF_TOLERANCE
    
    next_due = calibration_date + timedelta(days=calibration_interval_months * 30)
    today = datetime.now()
    
    if today > next_due:
        return CalibrationStatus.OVERDUE
    elif today > next_due - timedelta(days=30):
        return CalibrationStatus.DUE_SOON
    else:
        return CalibrationStatus.CALIBRATED


def calculate_next_due_date(
    calibration_date: datetime,
    interval_months: int
) -> datetime:
    """
    Calculate next calibration due date.
    
    Args:
        calibration_date: Date of calibration
        interval_months: Calibration interval
    
    Returns:
        Next due date
    """
    # Approximate months as 30 days
    return calibration_date + timedelta(days=interval_months * 30)


# ============================================================================
# UNCERTAINTY PROPAGATION
# ============================================================================

def propagate_calibration_uncertainty(
    standard_uncertainty: float,
    resolution_uncertainty: float,
    repeatability_uncertainty: float,
    temperature_uncertainty: float,
    drift_uncertainty: float
) -> float:
    """
    Calculate combined calibration uncertainty.
    
    Args:
        standard_uncertainty: Uncertainty from reference standard
        resolution_uncertainty: Uncertainty from instrument resolution
        repeatability_uncertainty: Uncertainty from repeatability
        temperature_uncertainty: Uncertainty from temperature effects
        drift_uncertainty: Uncertainty from drift
    
    Returns:
        Combined standard uncertainty (root sum square)
    """
    u_squared = (
        standard_uncertainty ** 2 +
        resolution_uncertainty ** 2 +
        repeatability_uncertainty ** 2 +
        temperature_uncertainty ** 2 +
        drift_uncertainty ** 2
    )
    
    return np.sqrt(u_squared)


def calculate_expanded_uncertainty(
    combined_uncertainty: float,
    confidence_level: float = 0.95,
    effective_dof: Optional[float] = None
) -> Tuple[float, float]:
    """
    Calculate expanded uncertainty with coverage factor.
    
    Args:
        combined_uncertainty: Combined standard uncertainty
        confidence_level: Desired confidence level
        effective_dof: Effective degrees of freedom
    
    Returns:
        (expanded_uncertainty, coverage_factor)
    """
    from scipy import stats
    
    if effective_dof is None or effective_dof == float('inf'):
        k = stats.norm.ppf((1 + confidence_level) / 2)
    else:
        k = stats.t.ppf((1 + confidence_level) / 2, effective_dof)
    
    U = k * combined_uncertainty
    return U, k


# ============================================================================
# ENVIRONMENTAL CORRECTIONS
# ============================================================================

def temperature_correction(
    value: float,
    reference_temp: float,
    actual_temp: float,
    temperature_coefficient: float
) -> float:
    """
    Apply temperature correction.
    
    Args:
        value: Measured value
        reference_temp: Reference temperature (K)
        actual_temp: Actual temperature (K)
        temperature_coefficient: Coefficient per K
    
    Returns:
        Corrected value
    """
    delta_t = actual_temp - reference_temp
    correction = value * temperature_coefficient * delta_t
    return value + correction


def humidity_correction(
    value: float,
    reference_humidity: float,
    actual_humidity: float,
    humidity_coefficient: float
) -> float:
    """
    Apply humidity correction.
    
    Args:
        value: Measured value
        reference_humidity: Reference humidity (%RH)
        actual_humidity: Actual humidity (%RH)
        humidity_coefficient: Coefficient per %RH
    
    Returns:
        Corrected value
    """
    delta_h = actual_humidity - reference_humidity
    correction = value * humidity_coefficient * delta_h
    return value + correction


def pressure_correction(
    value: float,
    reference_pressure: float,
    actual_pressure: float,
    pressure_coefficient: float
) -> float:
    """
    Apply pressure correction.
    
    Args:
        value: Measured value
        reference_pressure: Reference pressure (atm)
        actual_pressure: Actual pressure (atm)
        pressure_coefficient: Coefficient per atm
    
    Returns:
        Corrected value
    """
    delta_p = actual_pressure - reference_pressure
    correction = value * pressure_coefficient * delta_p
    return value + correction


# ============================================================================
# CALIBRATION CERTIFICATE
# ============================================================================

def create_calibration_certificate(
    instrument_id: str,
    instrument_name: str,
    calibration_date: datetime,
    calibration_interval_months: int,
    calibration_level: CalibrationLevel,
    points: List[CalibrationPoint],
    environmental_conditions: Dict[str, float],
    technician: str,
    certificate_number: str,
    combined_uncertainty: float,
    coverage_factor: float,
    confidence_level: float = 0.95
) -> CalibrationCertificate:
    """
    Create complete calibration certificate.
    
    Args:
        instrument_id: Instrument identifier
        instrument_name: Instrument name
        calibration_date: Date of calibration
        calibration_interval_months: Calibration interval
        calibration_level: Level of calibration
        points: Calibration points
        environmental_conditions: Temperature, humidity, pressure
        technician: Technician name
        certificate_number: Certificate number
        combined_uncertainty: Combined uncertainty
        coverage_factor: Coverage factor (k)
        confidence_level: Confidence level
    
    Returns:
        Complete calibration certificate
    """
    next_due = calculate_next_due_date(calibration_date, calibration_interval_months)
    
    # Determine status
    out_of_tolerance = any(not pt.within_tolerance for pt in points)
    status = determine_calibration_status(
        calibration_date,
        calibration_interval_months,
        out_of_tolerance
    )
    
    # Build traceability chain
    traceability = get_traceability_chain(calibration_level)
    
    # Calculate expanded uncertainty
    expanded_uncertainty = combined_uncertainty * coverage_factor
    
    return CalibrationCertificate(
        instrument_id=instrument_id,
        instrument_name=instrument_name,
        calibration_date=calibration_date,
        next_due_date=next_due,
        calibration_level=calibration_level,
        status=status,
        points=points,
        environmental_conditions=environmental_conditions,
        technician=technician,
        certificate_number=certificate_number,
        traceability_chain=traceability,
        combined_uncertainty=combined_uncertainty,
        coverage_factor=coverage_factor,
        expanded_uncertainty=expanded_uncertainty,
        confidence_level=confidence_level
    )


def format_calibration_report(certificate: CalibrationCertificate) -> str:
    """
    Format calibration certificate as report.
    
    Args:
        certificate: Calibration certificate
    
    Returns:
        Formatted report string
    """
    lines = []
    lines.append("=" * 80)
    lines.append("CALIBRATION CERTIFICATE")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Certificate Number: {certificate.certificate_number}")
    lines.append(f"Instrument: {certificate.instrument_name}")
    lines.append(f"ID: {certificate.instrument_id}")
    lines.append(f"Calibration Date: {certificate.calibration_date.strftime('%Y-%m-%d')}")
    lines.append(f"Next Due Date: {certificate.next_due_date.strftime('%Y-%m-%d')}")
    lines.append(f"Status: {certificate.status.value.upper()}")
    lines.append(f"Calibration Level: {certificate.calibration_level.value}")
    lines.append("")
    lines.append("Traceability Chain:")
    for i, level in enumerate(certificate.traceability_chain, 1):
        lines.append(f"  {i}. {level}")
    lines.append("")
    lines.append("Environmental Conditions:")
    for key, value in certificate.environmental_conditions.items():
        lines.append(f"  {key}: {value}")
    lines.append("")
    lines.append("Calibration Points:")
    lines.append("-" * 80)
    lines.append(f"{'Nominal':<12} {'Measured':<12} {'Standard':<12} {'Error':<10} {'Tolerance':<10} {'Status':<8}")
    lines.append("-" * 80)
    
    for pt in certificate.points:
        status_str = "PASS" if pt.within_tolerance else "FAIL"
        lines.append(
            f"{pt.nominal_value:<12.6g} {pt.measured_value:<12.6g} "
            f"{pt.standard_value:<12.6g} {pt.error:<10.6g} "
            f"{pt.tolerance:<10.6g} {status_str:<8}"
        )
    
    lines.append("-" * 80)
    lines.append("")
    lines.append("Uncertainty:")
    lines.append(f"  Combined Uncertainty: {certificate.combined_uncertainty:.6g} {certificate.points[0].unit}")
    lines.append(f"  Coverage Factor (k): {certificate.coverage_factor:.3f}")
    lines.append(f"  Expanded Uncertainty: {certificate.expanded_uncertainty:.6g} {certificate.points[0].unit}")
    lines.append(f"  Confidence Level: {certificate.confidence_level*100:.1f}%")
    lines.append("")
    lines.append(f"Technician: {certificate.technician}")
    lines.append("=" * 80)
    
    return "\n".join(lines)


# ============================================================================
# GALVANOMETER CALIBRATION
# ============================================================================

def calibrate_galvanometer_sensitivity(
    known_currents: List[float],
    measured_deflections: List[float]
) -> Tuple[float, float, float]:
    """
    Calibrate galvanometer current sensitivity.
    
    Args:
        known_currents: List of known currents (statampere)
        measured_deflections: List of measured deflections (cm)
    
    Returns:
        (sensitivity, uncertainty, r_squared)
        Sensitivity in cm/statampere
    """
    # Linear regression: deflection = sensitivity × current
    currents = np.array(known_currents)
    deflections = np.array(measured_deflections)
    
    # Least squares fit
    slope = np.sum(currents * deflections) / np.sum(currents ** 2)
    
    # Calculate residuals
    predicted = slope * currents
    residuals = deflections - predicted
    
    # Calculate R²
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((deflections - np.mean(deflections)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    
    # Estimate uncertainty
    n = len(currents)
    if n > 2:
        std_error = np.sqrt(ss_res / (n - 2))
        uncertainty = std_error / np.sqrt(np.sum(currents ** 2))
    else:
        uncertainty = 0.0
    
    return slope, uncertainty, r_squared


# ============================================================================
# MAGNETOMETER CALIBRATION
# ============================================================================

def calibrate_magnetometer_field(
    known_fields: List[float],
    measured_deflections: List[float]
) -> Tuple[float, float, float]:
    """
    Calibrate magnetometer field sensitivity.
    
    Args:
        known_fields: List of known fields (oersted)
        measured_deflections: List of measured deflections (radians)
    
    Returns:
        (sensitivity, uncertainty, r_squared)
        Sensitivity in rad/oersted
    """
    fields = np.array(known_fields)
    deflections = np.array(measured_deflections)
    
    # Linear regression
    slope = np.sum(fields * deflections) / np.sum(fields ** 2)
    
    # Calculate R²
    predicted = slope * fields
    residuals = deflections - predicted
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((deflections - np.mean(deflections)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    
    # Estimate uncertainty
    n = len(fields)
    if n > 2:
        std_error = np.sqrt(ss_res / (n - 2))
        uncertainty = std_error / np.sqrt(np.sum(fields ** 2))
    else:
        uncertainty = 0.0
    
    return slope, uncertainty, r_squared


# ============================================================================
# ELECTROMETER CALIBRATION
# ============================================================================

def calibrate_electrometer_voltage(
    known_voltages: List[float],
    measured_deflections: List[float]
) -> Tuple[float, float, float]:
    """
    Calibrate electrometer voltage sensitivity.
    
    Args:
        known_voltages: List of known voltages (statvolt)
        measured_deflections: List of measured deflections (radians)
    
    Returns:
        (sensitivity, uncertainty, r_squared)
        Sensitivity in rad/statvolt
    """
    voltages = np.array(known_voltages)
    deflections = np.array(measured_deflections)
    
    # Linear regression
    slope = np.sum(voltages * deflections) / np.sum(voltages ** 2)
    
    # Calculate R²
    predicted = slope * voltages
    residuals = deflections - predicted
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((deflections - np.mean(deflections)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    
    # Estimate uncertainty
    n = len(voltages)
    if n > 2:
        std_error = np.sqrt(ss_res / (n - 2))
        uncertainty = std_error / np.sqrt(np.sum(voltages ** 2))
    else:
        uncertainty = 0.0
    
    return slope, uncertainty, r_squared


# ============================================================================
# MAXWELL ARTICLE REFERENCES
# ============================================================================

def get_maxwell_calibration_articles() -> List[str]:
    """
    Get Maxwell article references for calibration.
    
    Returns:
        List of article references
    """
    return [
        'Art. 287-300: Networks and conduction',
        'Art. 343-348: Wheatstone bridge',
        'Art. 730-750: Galvanometers',
        'Art. 449-474: Magnetic measurements',
        'Art. 230-235: Electrification'
    ]


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Create calibration certificate
    calibration_date = datetime(2024, 1, 15)
    
    points = [
        create_calibration_point(
            nominal_value=1.0,
            measured_value=1.002,
            standard_value=1.000,
            standard_uncertainty=0.001,
            tolerance=0.01,
            unit="statvolt"
        ),
        create_calibration_point(
            nominal_value=5.0,
            measured_value=5.008,
            standard_value=5.000,
            standard_uncertainty=0.002,
            tolerance=0.05,
            unit="statvolt"
        ),
        create_calibration_point(
            nominal_value=10.0,
            measured_value=10.015,
            standard_value=10.000,
            standard_uncertainty=0.005,
            tolerance=0.10,
            unit="statvolt"
        )
    ]
    
    # Calculate combined uncertainty
    u_combined = propagate_calibration_uncertainty(
        standard_uncertainty=0.005,
        resolution_uncertainty=0.001,
        repeatability_uncertainty=0.002,
        temperature_uncertainty=0.001,
        drift_uncertainty=0.001
    )
    
    certificate = create_calibration_certificate(
        instrument_id="ELECT-001",
        instrument_name="Quadrant Electrometer",
        calibration_date=calibration_date,
        calibration_interval_months=12,
        calibration_level=CalibrationLevel.WORKING,
        points=points,
        environmental_conditions={
            "Temperature": "293 K",
            "Humidity": "50% RH",
            "Pressure": "1 atm"
        },
        technician="J. Smith",
        certificate_number="CAL-2024-001",
        combined_uncertainty=u_combined,
        coverage_factor=2.0
    )
    
    print(format_calibration_report(certificate))
```

---

## Usage Examples

```python
from instrument_calibration_utils import *

# Example 1: Calculate TUR
tur = calculate_tur(tolerance=0.01, uncertainty=0.002)
print(f"TUR: {tur:.1f}:1")
acceptance, recommendation = tur_acceptance(tur)
print(f"Status: {recommendation}")

# Example 2: Create calibration points
pt = create_calibration_point(
    nominal_value=10.0,
    measured_value=10.015,
    standard_value=10.000,
    standard_uncertainty=0.005,
    tolerance=0.10,
    unit="statvolt"
)
print(f"Error: {pt.error:.6f}, Within tolerance: {pt.within_tolerance}")

# Example 3: Galvanometer calibration
currents = [0.1, 0.2, 0.5, 1.0, 2.0]
deflections = [0.52, 1.01, 2.55, 5.10, 10.15]
sensitivity, uncertainty, r2 = calibrate_galvanometer_sensitivity(currents, deflections)
print(f"Sensitivity: {sensitivity:.4f} cm/statampere, R²: {r2:.4f}")

# Example 4: Complete certificate
cert = create_calibration_certificate(...)
print(format_calibration_report(cert))
```

---

## Quality Criteria

- [ ] Calibration hierarchy correctly implemented
- [ ] TUR calculation with acceptance criteria
- [ ] Uncertainty propagation (root sum square)
- [ ] Environmental corrections included
- [ ] Instrument-specific calibration functions
- [ ] Maxwell article references provided
