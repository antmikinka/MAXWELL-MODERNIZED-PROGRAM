# Utility: bridge_analysis_utils

## Purpose

Python utility module for bridge circuit analysis in CGS units.

## Location

`agents/circuitus/utils/bridge_analysis_utils.py`

---

## Module Contents

```python
"""
CIRCUITUS Bridge Analysis Utilities

CGS unit computations for bridge circuit analysis in the Maxwell Treatise Modernization Project.

Supported Bridge Types:
- Wheatstone Bridge (DC resistance)
- Kelvin Double Bridge (low resistance)
- Maxwell Bridge (inductance)
- Hay Bridge (high-Q inductance)
- Schering Bridge (capacitance)
- Wien Bridge (frequency)

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Art. 343-348, Art. 287-300, Art. 541-570
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class BridgeType(Enum):
    """Bridge circuit types."""
    WHEATSTONE = "wheatstone"
    KELVIN = "kelvin"
    MAXWELL = "maxwell"
    HAY = "hay"
    SCHERING = "schering"
    WIEN = "wien"
    ANDERSON = "anderson"


@dataclass
class BridgeResult:
    """Bridge measurement results."""
    bridge_type: BridgeType
    unknown_value: float
    unknown_unit: str
    balance_achieved: bool
    sensitivity: float
    uncertainty: float
    maxwell_articles: List[str]


@dataclass
class BridgeError:
    """Bridge measurement error analysis."""
    systematic_errors: Dict[str, float]
    random_errors: Dict[str, float]
    combined_uncertainty: float
    expanded_uncertainty: float  # k=2


# ============================================================================
# WHEATSTONE BRIDGE
# ============================================================================

def wheatstone_balance(r1: float, r2: float, r3: float, r4: float) -> bool:
    """
    Check if Wheatstone bridge is balanced.
    
    Balance condition: R1/R2 = R3/R4  or  R1×R4 = R2×R3
    
    Args:
        r1, r2, r3, r4: Arm resistances in statohm
    
    Returns:
        True if balanced (within numerical tolerance)
    """
    lhs = r1 * r4
    rhs = r2 * r3
    return np.isclose(lhs, rhs, rtol=1e-10)


def wheatstone_unknown(r1: float, r2: float, r3: float) -> float:
    """
    Calculate unknown resistance in Wheatstone bridge.
    
    R4 = R3 × (R2/R1)
    
    Args:
        r1, r2: Ratio arms in statohm
        r3: Variable standard in statohm
    
    Returns:
        R4 (unknown) in statohm
    
    Maxwell Reference: Art. 343-348
    """
    return r3 * (r2 / r1)


def wheatstone_sensitivity(r1: float, r2: float, r3: float, r4: float,
                           v_source: float, r_galvanometer: float) -> float:
    """
    Calculate Wheatstone bridge sensitivity.
    
    S = dV_out / (ΔR/R)  (output voltage change per unit fractional resistance change)
    
    Args:
        r1, r2, r3, r4: Arm resistances in statohm
        v_source: Source voltage in statvolt
        r_galvanometer: Galvanometer resistance in statohm
    
    Returns:
        Sensitivity in statvolt per unit fractional change
    
    Maximum sensitivity when R1 = R2 = R3 = R4
    """
    # Thevenin equivalent resistance seen by galvanometer
    r_th = (r1 * r2) / (r1 + r2) + (r3 * r4) / (r3 + r4)
    
    # Open-circuit voltage for small unbalance ΔR
    # dV_out ≈ V_s × (r2/(r1+r2)²) × ΔR1 (for change in R1)
    
    # Sensitivity at balance point
    if wheatstone_balance(r1, r2, r3, r4):
        # For equal arms (maximum sensitivity)
        if np.isclose(r1, r2) and np.isclose(r2, r3) and np.isclose(r3, r4):
            s = v_source / (4 * (r_th + r_galvanometer))
        else:
            s = v_source * r2 / ((r1 + r2)**2) / (r_th + r_galvanometer)
    else:
        s = 0  # Not at balance
    
    return s


def wheatstone_unbalance_voltage(r1: float, r2: float, r3: float, r4: float,
                                  v_source: float) -> float:
    """
    Calculate output voltage for unbalanced Wheatstone bridge.
    
    V_out = V_s × [R2/(R1+R2) - R4/(R3+R4)]
    
    Args:
        r1, r2, r3, r4: Arm resistances in statohm
        v_source: Source voltage in statvolt
    
    Returns:
        Output voltage in statvolt
    """
    v_b = v_source * r2 / (r1 + r2)  # Voltage at node B
    v_d = v_source * r4 / (r3 + r4)  # Voltage at node D
    return v_b - v_d


# ============================================================================
# KELVIN DOUBLE BRIDGE
# ============================================================================

def kelvin_balance(m: float, n: float, m_aux: float, n_aux: float,
                   r_s: float, r: float = 0) -> float:
    """
    Calculate unknown resistance in Kelvin double bridge.
    
    Balance condition: Rx/Rs = M/N = m/n (auxiliary ratio equals main ratio)
    
    Rx = Rs × (M/N) + correction term (if r ≠ 0 and ratios don't match exactly)
    
    Args:
        m, n: Main ratio arms in statohm
        m_aux, n_aux: Auxiliary ratio arms in statohm
        r_s: Standard resistance in statohm
        r: Link resistance in statohm (default 0 for ideal)
    
    Returns:
        Rx (unknown) in statohm
    """
    main_ratio = m / n
    aux_ratio = m_aux / n_aux
    
    # Ideal case (ratios match exactly)
    rx = r_s * main_ratio
    
    # Correction for link resistance if ratios don't match
    if r > 0 and not np.isclose(main_ratio, aux_ratio):
        correction = r * (main_ratio - aux_ratio) / (1 + aux_ratio)
        rx += correction
    
    return rx


def kelvin_minimum_measurable(r_std: float, ratio_accuracy: float) -> float:
    """
    Estimate minimum measurable resistance with Kelvin bridge.
    
    Args:
        r_std: Standard resistance in statohm
        ratio_accuracy: Ratio accuracy (fractional)
    
    Returns:
        Minimum measurable resistance in statohm
    """
    # Typically can measure down to about 0.001 × standard
    return r_std * 0.001


# ============================================================================
# MAXWELL BRIDGE
# ============================================================================

def maxwell_bridge_balance(r1: float, r2: float, r3: float, c1: float) -> Tuple[float, float]:
    """
    Calculate unknown inductance and resistance in Maxwell bridge.
    
    Balance conditions:
    Lx = R2 × R3 × C1
    Rx = (R2 × R3) / R1
    
    Args:
        r1: Resistance in arm 1 (in statohm)
        r2, r3: Standard resistances in statohm
        c1: Standard capacitance in statfarad
    
    Returns:
        (Lx, Rx) - unknown inductance in cm, unknown resistance in statohm
    
    Maxwell Reference: Art. 541-570
    """
    lx = r2 * r3 * c1  # cm (CGS inductance)
    rx = (r2 * r3) / r1  # statohm
    return lx, rx


def maxwell_bridge_q(lx: float, rx: float, omega: float) -> float:
    """
    Calculate Q factor of measured coil in Maxwell bridge.
    
    Q = ωL/R
    
    Args:
        lx: Inductance in cm
        rx: Resistance in statohm
        omega: Angular frequency in rad/s
    
    Returns:
        Q factor (dimensionless)
    """
    return omega * lx / rx


def maxwell_bridge_frequency_dependent() -> bool:
    """
    Check if Maxwell bridge balance is frequency dependent.
    
    Returns:
        False - Maxwell bridge balance is independent of frequency
    """
    return False  # Balance equations don't contain ω


# ============================================================================
# HAY BRIDGE
# ============================================================================

def hay_bridge_balance(r1: float, r2: float, r3: float, c1: float, 
                       omega: float) -> Tuple[float, float]:
    """
    Calculate unknown inductance and resistance in Hay bridge.
    
    Balance conditions:
    Lx = (R2 × R3 × C1) / (1 + ω²×R1²×C1²)
    Rx = (ω²×R1×R2×R3×C1²) / (1 + ω²×R1²×C1²)
    
    Args:
        r1: Resistance in series with C1 (statohm)
        r2, r3: Standard resistances (statohm)
        c1: Standard capacitance (statfarad)
        omega: Angular frequency (rad/s)
    
    Returns:
        (Lx, Rx) - unknown inductance in cm, unknown resistance in statohm
    
    Hay bridge is suitable for high-Q coils (Q > 10)
    """
    denom = 1 + (omega**2) * (r1**2) * (c1**2)
    
    lx = (r2 * r3 * c1) / denom
    rx = ((omega**2) * r1 * r2 * r3 * (c1**2)) / denom
    
    return lx, rx


def hay_bridge_q(r1: float, c1: float, omega: float) -> float:
    """
    Calculate Q factor for Hay bridge measurement.
    
    Q = 1 / (ω×R1×C1)
    
    Args:
        r1: Series resistance in statohm
        c1: Series capacitance in statfarad
        omega: Angular frequency in rad/s
    
    Returns:
        Q factor (dimensionless)
    """
    return 1 / (omega * r1 * c1)


def hay_bridge_suitable_for_high_q() -> bool:
    """
    Check if Hay bridge is suitable for high-Q measurements.
    
    Returns:
        True - Hay bridge is designed for high-Q coils (Q > 10)
    """
    return True


# ============================================================================
# SCHERING BRIDGE
# ============================================================================

def schering_bridge_balance(c1: float, r3: float, r4: float, 
                            c4: float = 0) -> Tuple[float, float]:
    """
    Calculate unknown capacitance and loss resistance in Schering bridge.
    
    Balance conditions:
    Cx = C1 × (R4/R3)
    tan(δ) = ω×C4×R4 (if C4 present for loss measurement)
    
    Args:
        c1: Standard capacitance in statfarad
        r3, r4: Standard resistances in statohm
        c4: Variable capacitance for loss measurement (optional)
    
    Returns:
        (Cx, tan_delta) - unknown capacitance in statfarad, loss tangent
    """
    cx = c1 * (r4 / r3)
    tan_delta = 0  # Would need ω and C4 to calculate
    
    return cx, tan_delta


def schering_loss_angle(omega: float, c4: float, r4: float) -> float:
    """
    Calculate loss tangent (dissipation factor) in Schering bridge.
    
    tan(δ) = ω × C4 × R4
    
    Args:
        omega: Angular frequency in rad/s
        c4: Parallel capacitance in statfarad
        r4: Parallel resistance in statohm
    
    Returns:
        Loss tangent (dimensionless)
    """
    return omega * c4 * r4


def schering_phase_defect_angle(tan_delta: float) -> float:
    """
    Calculate phase defect angle from loss tangent.
    
    δ = arctan(tan δ)
    Phase defect = 90° - δ (for ideal capacitor)
    
    Args:
        tan_delta: Loss tangent
    
    Returns:
        Phase defect angle in degrees
    """
    delta = np.arctan(tan_delta)
    return 90 - np.degrees(delta)


# ============================================================================
# WIEN BRIDGE
# ============================================================================

def wien_bridge_frequency(r1: float, r2: float, c1: float, c2: float) -> float:
    """
    Calculate balance frequency for Wien bridge.
    
    ω² = 1 / (R1×R2×C1×C2)
    
    Args:
        r1, r2: Resistances in statohm
        c1, c2: Capacitances in statfarad
    
    Returns:
        Angular frequency in rad/s
    """
    return 1 / np.sqrt(r1 * r2 * c1 * c2)


def wien_bridge_amplitude_balance(r3: float, r4: float, r1: float, r2: float,
                                   c1: float, c2: float) -> bool:
    """
    Check amplitude balance condition for Wien bridge.
    
    R3/R4 = C1/C2 + R2/R1
    
    Args:
        r1, r2, r3, r4: Bridge resistances in statohm
        c1, c2: Bridge capacitances in statfarad
    
    Returns:
        True if amplitude balance condition is satisfied
    """
    lhs = r3 / r4
    rhs = c1 / c2 + r2 / r1
    return np.isclose(lhs, rhs, rtol=1e-6)


def wien_bridge_equal_components(r: float, c: float) -> Tuple[float, float, float]:
    """
    Wien bridge with equal components (R1=R2=R, C1=C2=C).
    
    Frequency: f = 1/(2πRC)
    Amplitude balance: R3/R4 = 2
    
    Args:
        r: Resistance in statohm
        c: Capacitance in statfarad
    
    Returns:
        (omega, frequency_hz, r3_r4_ratio)
    """
    omega = 1 / (r * c)
    freq_hz = omega / (2 * np.pi)
    r3_r4_ratio = 2
    
    return omega, freq_hz, r3_r4_ratio


# ============================================================================
# BRIDGE COMPARISON
# ============================================================================

def get_bridge_recommendation(measurand: str, value_range: Tuple[float, float],
                               accuracy_required: float) -> BridgeType:
    """
    Recommend bridge type based on measurement requirements.
    
    Args:
        measurand: What to measure ('resistance', 'inductance', 'capacitance', 'frequency')
        value_range: (min, max) expected value
        accuracy_required: Required accuracy (fractional, e.g., 0.001 for 0.1%)
    
    Returns:
        Recommended BridgeType
    """
    if measurand == 'resistance':
        if value_range[1] < 1:  # Low resistance (< 1 statohm)
            return BridgeType.KELVIN
        else:
            return BridgeType.WHEATSTONE
    
    elif measurand == 'inductance':
        # Estimate Q from value range (simplified)
        q_estimate = 5  # Default assumption
        if q_estimate > 10:
            return BridgeType.HAY
        else:
            return BridgeType.MAXWELL
    
    elif measurand == 'capacitance':
        return BridgeType.SCHERING
    
    elif measurand == 'frequency':
        return BridgeType.WIEN
    
    else:
        return BridgeType.WHEATSTONE  # Default


def get_maxwell_articles_for_bridge(bridge_type: BridgeType) -> List[str]:
    """
    Get Maxwell article references for bridge type.
    
    Args:
        bridge_type: Type of bridge
    
    Returns:
        List of article references
    """
    article_map = {
        BridgeType.WHEATSTONE: ['Art. 343-348', 'Art. 287-300'],
        BridgeType.KELVIN: ['Art. 343-348', 'Art. 287-300'],
        BridgeType.MAXWELL: ['Art. 541-570', 'Art. 343-348'],
        BridgeType.HAY: ['Art. 541-570', 'Art. 343-348'],
        BridgeType.SCHERING: ['Art. 75-76', 'Art. 343-348'],
        BridgeType.WIEN: ['Art. 343-348', 'Art. 75-76'],
        BridgeType.ANDERSON: ['Art. 541-570', 'Art. 343-348'],
    }
    
    return article_map.get(bridge_type, ['Art. 343-348'])


# ============================================================================
# ERROR ANALYSIS
# ============================================================================

def bridge_uncertainty(r_unknown: float, 
                       relative_uncertainties: Dict[str, float],
                       confidence_level: float = 0.95) -> Tuple[float, float]:
    """
    Calculate combined and expanded uncertainty for bridge measurement.
    
    Args:
        r_unknown: Measured unknown value
        relative_uncertainties: Dictionary of {source: relative_uncertainty}
        confidence_level: Desired confidence level (default 95%)
    
    Returns:
        (combined_uncertainty, expanded_uncertainty)
    """
    # Combine relative uncertainties in quadrature
    u_rel_squared = sum(u**2 for u in relative_uncertainties.values())
    u_rel = np.sqrt(u_rel_squared)
    
    # Combined uncertainty
    u_c = r_unknown * u_rel
    
    # Expanded uncertainty (k factor for confidence level)
    k_factors = {0.90: 1.645, 0.95: 2.0, 0.99: 2.576}
    k = k_factors.get(confidence_level, 2.0)
    u_expanded = k * u_c
    
    return u_c, u_expanded


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Wheatstone bridge
    r1, r2, r3 = 1000, 1000, 1500  # statohm
    r4 = wheatstone_unknown(r1, r2, r3)
    print(f"Wheatstone bridge: R4 = {r4} statohm")
    
    # Example: Maxwell bridge
    r1, r2, r3, c1 = 1000, 500, 1000, 1e-12  # CGS units
    lx, rx = maxwell_bridge_balance(r1, r2, r3, c1)
    print(f"Maxwell bridge: Lx = {lx} cm, Rx = {rx} statohm")
    
    # Example: Wien bridge frequency
    r, c = 1000, 1e-12  # CGS units
    omega, freq, ratio = wien_bridge_equal_components(r, c)
    print(f"Wien bridge: f = {freq/1e6:.2f} MHz, R3/R4 = {ratio}")
```

---

## Usage Examples

```python
from bridge_analysis_utils import *

# Example 1: Wheatstone bridge measurement
r1, r2, r3 = 1000, 1000, 1500  # statohm
r4 = wheatstone_unknown(r1, r2, r3)
print(f"Unknown resistance: {r4} statohm")

# Example 2: Maxwell bridge for inductance
lx, rx = maxwell_bridge_balance(1000, 500, 1000, 1e-12)
print(f"Inductance: {lx} cm, Resistance: {rx} statohm")

# Example 3: Hay bridge Q factor
q = hay_bridge_q(1000, 1e-12, 2 * np.pi * 1e6)
print(f"Q factor: {q:.2f}")

# Example 4: Bridge recommendation
bridge = get_bridge_recommendation('resistance', (0.001, 0.1), 0.001)
print(f"Recommended bridge: {bridge.value}")
```

---

## Quality Criteria

- [ ] All computations in CGS units
- [ ] Maxwell article references included
- [ ] Bridge balance conditions correct
- [ ] Error analysis implemented
- [ ] Documentation complete
