# Utility: circuitus_computation_utils

## Purpose

Python utility module for circuit analysis computations in CGS units.

## Location

`agents/circuitus/utils/circuitus_computation_utils.py`

---

## Module Contents

```python
"""
CIRCUITUS Computation Utilities

CGS unit computations for circuit analysis in the Maxwell Treatise Modernization Project.

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations
"""

from typing import Dict, List, Tuple, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np


class CircuitElementType(Enum):
    """Circuit element types."""
    RESISTOR = "R"
    CAPACITOR = "C"
    INDUCTOR = "L"
    VOLTAGE_SOURCE = "V"
    CURRENT_SOURCE = "I"
    MUTUAL_INDUCTANCE = "M"


class AnalysisType(Enum):
    """Circuit analysis types."""
    DC = "dc"
    AC_STEADY_STATE = "ac"
    TRANSIENT = "transient"
    LAPLACE = "laplace"


@dataclass
class CircuitElement:
    """Circuit element definition."""
    element_type: CircuitElementType
    value: float
    unit: str
    node_positive: int
    node_negative: int
    maxwell_articles: List[str]
    
    @property
    def impedance(self, omega: float = 0) -> complex:
        """Calculate impedance at given frequency."""
        if self.element_type == CircuitElementType.RESISTOR:
            return complex(self.value, 0)
        elif self.element_type == CircuitElementType.INDUCTOR:
            return complex(0, omega * self.value)
        elif self.element_type == CircuitElementType.CAPACITOR:
            if omega == 0:
                return complex(0, float('inf'))
            return complex(0, -1 / (omega * self.value))
        else:
            raise ValueError(f"Impedance not defined for {self.element_type}")


@dataclass
class CircuitResult:
    """Circuit analysis results."""
    node_voltages: Dict[int, complex]
    branch_currents: Dict[str, complex]
    power_dissipated: Dict[str, float]
    total_power_supplied: float
    power_balance_verified: bool


# ============================================================================
# UNIT CONVERSIONS
# ============================================================================

def volt_to_statvolt(volt: float) -> float:
    """Convert SI volt to CGS statvolt."""
    return volt / 299.79


def statvolt_to_volt(statvolt: float) -> float:
    """Convert CGS statvolt to SI volt."""
    return statvolt * 299.79


def ampere_to_statampere(ampere: float) -> float:
    """Convert SI ampere to CGS statampere."""
    return ampere / 3.3356e-10


def statampere_to_ampere(statampere: float) -> float:
    """Convert CGS statampere to SI ampere."""
    return statampere * 3.3356e-10


def ohm_to_statohm(ohm: float) -> float:
    """Convert SI ohm to CGS statohm."""
    return ohm / 8.9876e11


def statohm_to_ohm(statohm: float) -> float:
    """Convert CGS statohm to SI ohm."""
    return statohm * 8.9876e11


def farad_to_statfarad(farad: float) -> float:
    """Convert SI farad to CGS statfarad."""
    return farad / 1.1126e-12


def statfarad_to_farad(statfarad: float) -> float:
    """Convert CGS statfarad to SI farad."""
    return statfarad * 1.1126e-12


def henry_to_cm(henry: float) -> float:
    """Convert SI henry to CGS cm (inductance)."""
    return henry / 1.1126e-12


def cm_to_henry(cm: float) -> float:
    """Convert CGS cm to SI henry."""
    return cm * 1.1126e-12


def watt_to_erg_per_s(watt: float) -> float:
    """Convert SI watt to CGS erg/s."""
    return watt / 1e-7


def erg_per_s_to_watt(erg_per_s: float) -> float:
    """Convert CGS erg/s to SI watt."""
    return erg_per_s * 1e-7


# ============================================================================
# OHM'S LAW AND POWER
# ============================================================================

def ohms_law_voltage(current: float, resistance: float) -> float:
    """
    Calculate voltage using Ohm's law (CGS).
    
    V = I × R
    
    Args:
        current: Current in statampere
        resistance: Resistance in statohm
    
    Returns:
        Voltage in statvolt
    """
    return current * resistance


def ohms_law_current(voltage: float, resistance: float) -> float:
    """
    Calculate current using Ohm's law (CGS).
    
    I = V / R
    
    Args:
        voltage: Voltage in statvolt
        resistance: Resistance in statohm
    
    Returns:
        Current in statampere
    """
    return voltage / resistance


def ohms_law_resistance(voltage: float, current: float) -> float:
    """
    Calculate resistance using Ohm's law (CGS).
    
    R = V / I
    
    Args:
        voltage: Voltage in statvolt
        current: Current in statampere
    
    Returns:
        Resistance in statohm
    """
    return voltage / current


def power_dissipated(current: float, resistance: float) -> float:
    """
    Calculate power dissipated in resistor (CGS).
    
    P = I² × R
    
    Args:
        current: Current in statampere
        resistance: Resistance in statohm
    
    Returns:
        Power in erg/s
    """
    return (current ** 2) * resistance


def power_from_voltage(voltage: float, resistance: float) -> float:
    """
    Calculate power from voltage (CGS).
    
    P = V² / R
    
    Args:
        voltage: Voltage in statvolt
        resistance: Resistance in statohm
    
    Returns:
        Power in erg/s
    """
    return (voltage ** 2) / resistance


def power_from_vi(voltage: float, current: float) -> float:
    """
    Calculate power from voltage and current (CGS).
    
    P = V × I
    
    Args:
        voltage: Voltage in statvolt
        current: Current in statampere
    
    Returns:
        Power in erg/s
    """
    return voltage * current


# ============================================================================
# SERIES AND PARALLEL COMBINATIONS
# ============================================================================

def series_resistance(resistances: List[float]) -> float:
    """
    Calculate equivalent resistance for series combination.
    
    R_eq = R1 + R2 + ... + Rn
    
    Args:
        resistances: List of resistance values in statohm
    
    Returns:
        Equivalent resistance in statohm
    """
    return sum(resistances)


def parallel_resistance(resistances: List[float]) -> float:
    """
    Calculate equivalent resistance for parallel combination.
    
    1/R_eq = 1/R1 + 1/R2 + ... + 1/Rn
    
    Args:
        resistances: List of resistance values in statohm
    
    Returns:
        Equivalent resistance in statohm
    """
    return 1 / sum(1/r for r in resistances)


def series_inductance(inductances: List[float], mutual: float = 0) -> float:
    """
    Calculate equivalent inductance for series combination.
    
    L_eq = L1 + L2 + ... + Ln ± 2M (for coupled inductors)
    
    Args:
        inductances: List of inductance values in cm
        mutual: Mutual inductance in cm (positive for aiding, negative for opposing)
    
    Returns:
        Equivalent inductance in cm
    """
    total = sum(inductances)
    if len(inductances) == 2 and mutual != 0:
        total += 2 * mutual
    return total


def parallel_inductance(inductances: List[float]) -> float:
    """
    Calculate equivalent inductance for parallel combination (no coupling).
    
    1/L_eq = 1/L1 + 1/L2 + ... + 1/Ln
    
    Args:
        inductances: List of inductance values in cm
    
    Returns:
        Equivalent inductance in cm
    """
    return 1 / sum(1/l for l in inductances)


def series_capacitance(capacitances: List[float]) -> float:
    """
    Calculate equivalent capacitance for series combination.
    
    1/C_eq = 1/C1 + 1/C2 + ... + 1/Cn
    
    Args:
        capacitances: List of capacitance values in statfarad
    
    Returns:
        Equivalent capacitance in statfarad
    """
    return 1 / sum(1/c for c in capacitances)


def parallel_capacitance(capacitances: List[float]) -> float:
    """
    Calculate equivalent capacitance for parallel combination.
    
    C_eq = C1 + C2 + ... + Cn
    
    Args:
        capacitances: List of capacitance values in statfarad
    
    Returns:
        Equivalent capacitance in statfarad
    """
    return sum(capacitances)


# ============================================================================
# AC CIRCUIT ANALYSIS
# ============================================================================

def impedance_resistor(resistance: float) -> complex:
    """Impedance of resistor (real)."""
    return complex(resistance, 0)


def impedance_inductor(inductance: float, omega: float) -> complex:
    """
    Impedance of inductor.
    
    Z = jωL
    
    Args:
        inductance: Inductance in cm
        omega: Angular frequency in rad/s
    
    Returns:
        Impedance in statohm
    """
    return complex(0, omega * inductance)


def impedance_capacitor(capacitance: float, omega: float) -> complex:
    """
    Impedance of capacitor.
    
    Z = 1/(jωC) = -j/(ωC)
    
    Args:
        capacitance: Capacitance in statfarad
        omega: Angular frequency in rad/s
    
    Returns:
        Impedance in statohm
    """
    if omega == 0:
        return complex(0, float('inf'))
    return complex(0, -1 / (omega * capacitance))


def impedance_series_rlc(resistance: float, inductance: float, 
                         capacitance: float, omega: float) -> complex:
    """
    Impedance of series RLC circuit.
    
    Z = R + j(ωL - 1/(ωC))
    
    Args:
        resistance: Resistance in statohm
        inductance: Inductance in cm
        capacitance: Capacitance in statfarad
        omega: Angular frequency in rad/s
    
    Returns:
        Impedance in statohm
    """
    z_r = impedance_resistor(resistance)
    z_l = impedance_inductor(inductance, omega)
    z_c = impedance_capacitor(capacitance, omega)
    return z_r + z_l + z_c


def impedance_parallel_rlc(resistance: float, inductance: float,
                           capacitance: float, omega: float) -> complex:
    """
    Admittance of parallel RLC circuit.
    
    Y = 1/R + 1/(jωL) + jωC = G + j(Bc - BL)
    Z = 1/Y
    
    Args:
        resistance: Resistance in statohm
        inductance: Inductance in cm
        capacitance: Capacitance in statfarad
        omega: Angular frequency in rad/s
    
    Returns:
        Impedance in statohm
    """
    y_r = 1 / resistance
    y_l = 1 / (complex(0, omega * inductance))
    y_c = 1 / impedance_capacitor(capacitance, omega)
    
    y_total = y_r + y_l + y_c
    return 1 / y_total


def resonant_frequency(inductance: float, capacitance: float) -> float:
    """
    Calculate resonant angular frequency.
    
    ω₀ = 1/√(LC)
    
    Args:
        inductance: Inductance in cm
        capacitance: Capacitance in statfarad
    
    Returns:
        Resonant angular frequency in rad/s
    """
    return 1 / np.sqrt(inductance * capacitance)


def quality_factor_series(resistance: float, inductance: float, 
                          capacitance: float) -> float:
    """
    Quality factor for series RLC circuit.
    
    Q = ω₀L/R = 1/(ω₀RC)
    
    Args:
        resistance: Resistance in statohm
        inductance: Inductance in cm
        capacitance: Capacitance in statfarad
    
    Returns:
        Quality factor (dimensionless)
    """
    omega_0 = resonant_frequency(inductance, capacitance)
    return omega_0 * inductance / resistance


def quality_factor_parallel(resistance: float, inductance: float,
                            capacitance: float) -> float:
    """
    Quality factor for parallel RLC circuit.
    
    Q = R/(ω₀L) = ω₀RC
    
    Args:
        resistance: Resistance in statohm
        inductance: Inductance in cm
        capacitance: Capacitance in statfarad
    
    Returns:
        Quality factor (dimensionless)
    """
    omega_0 = resonant_frequency(inductance, capacitance)
    return resistance / (omega_0 * inductance)


def bandwidth_series(resistance: float, inductance: float) -> float:
    """
    Bandwidth for series RLC circuit.
    
    Δω = R/L
    
    Args:
        resistance: Resistance in statohm
        inductance: Inductance in cm
    
    Returns:
        Bandwidth in rad/s
    """
    return resistance / inductance


# ============================================================================
# TIME CONSTANTS
# ============================================================================

def time_constant_rc(resistance: float, capacitance: float) -> float:
    """
    Time constant for RC circuit.
    
    τ = RC
    
    Args:
        resistance: Resistance in statohm
        capacitance: Capacitance in statfarad
    
    Returns:
        Time constant in seconds
    """
    return resistance * capacitance


def time_constant_rl(inductance: float, resistance: float) -> float:
    """
    Time constant for RL circuit.
    
    τ = L/R
    
    Args:
        inductance: Inductance in cm
        resistance: Resistance in statohm
    
    Returns:
        Time constant in seconds
    """
    return inductance / resistance


# ============================================================================
# TRANSFORMER AND MUTUAL INDUCTANCE
# ============================================================================

def mutual_inductance_coupling(l1: float, l2: float, k: float) -> float:
    """
    Calculate mutual inductance from coupling coefficient.
    
    M = k × √(L1 × L2)
    
    Args:
        l1: Self-inductance 1 in cm
        l2: Self-inductance 2 in cm
        k: Coupling coefficient (0 ≤ k ≤ 1)
    
    Returns:
        Mutual inductance in cm
    """
    if not 0 <= k <= 1:
        raise ValueError("Coupling coefficient must be between 0 and 1")
    return k * np.sqrt(l1 * l2)


def coupling_coefficient(mutual: float, l1: float, l2: float) -> float:
    """
    Calculate coupling coefficient from mutual inductance.
    
    k = M / √(L1 × L2)
    
    Args:
        mutual: Mutual inductance in cm
        l1: Self-inductance 1 in cm
        l2: Self-inductance 2 in cm
    
    Returns:
        Coupling coefficient (0 ≤ k ≤ 1)
    """
    k = mutual / np.sqrt(l1 * l2)
    return min(max(k, 0), 1)  # Clamp to [0, 1]


def transformer_impedance_reflection(z_load: float, n1: int, n2: int) -> float:
    """
    Reflect load impedance through ideal transformer.
    
    Z_in = Z_L / n²  where n = N2/N1
    
    Args:
        z_load: Load impedance in statohm
        n1: Primary turns
        n2: Secondary turns
    
    Returns:
        Reflected impedance in statohm
    """
    n = n2 / n1
    return z_load / (n ** 2)


# ============================================================================
# Y-Δ TRANSFORMATION
# ============================================================================

def delta_to_y(r_ab: float, r_bc: float, r_ca: float) -> Tuple[float, float, float]:
    """
    Convert Δ (delta) resistances to Y (star) resistances.
    
    R_a = (R_ab × R_ca) / (R_ab + R_bc + R_ca)
    
    Args:
        r_ab, r_bc, r_ca: Delta resistances in statohm
    
    Returns:
        (R_a, R_b, R_c) in statohm
    """
    sum_r = r_ab + r_bc + r_ca
    r_a = (r_ab * r_ca) / sum_r
    r_b = (r_ab * r_bc) / sum_r
    r_c = (r_bc * r_ca) / sum_r
    return r_a, r_b, r_c


def y_to_delta(r_a: float, r_b: float, r_c: float) -> Tuple[float, float, float]:
    """
    Convert Y (star) resistances to Δ (delta) resistances.
    
    R_ab = (R_a×R_b + R_b×R_c + R_c×R_a) / R_c
    
    Args:
        r_a, r_b, r_c: Star resistances in statohm
    
    Returns:
        (R_ab, R_bc, R_ca) in statohm
    """
    sum_products = r_a*r_b + r_b*r_c + r_c*r_a
    r_ab = sum_products / r_c
    r_bc = sum_products / r_a
    r_ca = sum_products / r_b
    return r_ab, r_bc, r_ca


# ============================================================================
# MAXWELL ARTICLE REFERENCES
# ============================================================================

def get_maxwell_articles(topic: str) -> List[str]:
    """
    Get relevant Maxwell article references for a circuit topic.
    
    Args:
        topic: Circuit topic
    
    Returns:
        List of article references
    """
    article_map = {
        'kcl': ['Art. 230-235'],
        'kvl': ['Art. 287-300'],
        'resistance': ['Art. 287-300', 'Art. 301-320'],
        'bridge': ['Art. 343-348', 'Art. 287-300'],
        'inductance': ['Art. 541-570'],
        'mutual_inductance': ['Art. 541-570'],
        'capacitance': ['Art. 75-76'],
        'transmission_line': ['Art. 604-619', 'Art. 781-797'],
        'network_theorems': ['Art. 287-300', 'Art. 301-320'],
    }
    
    return article_map.get(topic, [])


# ============================================================================
# MAIN (Quick Reference)
# ============================================================================

if __name__ == "__main__":
    # Example calculations
    print("CGS Circuit Analysis Examples")
    print("=" * 50)
    
    # Example 1: Ohm's law
    v = ohms_law_voltage(1e-6, 1e6)  # 1 μstatA × 1 Mstatohm
    print(f"V = I×R: {v:.3e} statvolt")
    
    # Example 2: Series RLC impedance at resonance
    r, l, c = 1000, 1e6, 1e-12  # CGS values
    omega_0 = resonant_frequency(l, c)
    z = impedance_series_rlc(r, l, c, omega_0)
    print(f"Series RLC at resonance: Z = {z} statohm")
    
    # Example 3: Q factor
    q = quality_factor_series(r, l, c)
    print(f"Quality factor: Q = {q:.2f}")
    
    # Example 4: Y-Δ transformation
    r_ab, r_bc, r_ca = 3000, 3000, 3000
    r_a, r_b, r_c = delta_to_y(r_ab, r_bc, r_ca)
    print(f"Δ→Y: {r_a}, {r_b}, {r_c} statohm")
```

---

## Usage Examples

```python
from circuitus_computation_utils import *

# Example 1: Series RLC circuit
r, l, c = 1000, 1e6, 1e-12  # CGS values
omega_0 = resonant_frequency(l, c)
q = quality_factor_series(r, l, c)
print(f"Resonant frequency: {omega_0:.3e} rad/s")
print(f"Quality factor: {q:.2f}")

# Example 2: Unit conversion
v_si = 5.0  # 5 V
v_cgs = volt_to_statvolt(v_si)
print(f"{v_si} V = {v_cgs:.3e} statvolt")

# Example 3: Mutual inductance
l1, l2 = 1e6, 1e6  # cm
k = 0.5
m = mutual_inductance_coupling(l1, l2, k)
print(f"Mutual inductance: {m:.3e} cm")

# Example 4: Y-Δ transformation
r_delta = [3000, 3000, 3000]
r_a, r_b, r_c = delta_to_y(*r_delta)
```

---

## Quality Criteria

- [ ] All computations in CGS units
- [ ] Maxwell article references included
- [ ] Theory classification enforced
- [ ] Input validation implemented
- [ ] Documentation complete
