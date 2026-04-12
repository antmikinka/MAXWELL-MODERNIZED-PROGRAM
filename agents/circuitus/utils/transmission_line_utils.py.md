# Utility: transmission_line_utils

## Purpose

Python utility module for transmission line analysis in CGS units.

## Location

`agents/circuitus/utils/transmission_line_utils.py`

---

## Module Contents

```python
"""
CIRCUITUS Transmission Line Utilities

CGS unit computations for transmission line analysis in the Maxwell Treatise Modernization Project.

Supported Line Types:
- Coaxial Line
- Two-Wire Line
- Stripline
- Microstrip

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Art. 604-619, Art. 781-797
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class LineType(Enum):
    """Transmission line types."""
    COAXIAL = "coaxial"
    TWO_WIRE = "two_wire"
    STRIPLINE = "stripline"
    MICROSTRIP = "microstrip"


@dataclass
class LineParameters:
    """Distributed line parameters (per unit length)."""
    r: float  # Resistance (statohm/cm)
    l: float  # Inductance (cm/cm, dimensionless in CGS)
    g: float  # Conductance (s⁻¹/cm)
    c: float  # Capacitance (statfarad/cm)
    maxwell_articles: List[str]


@dataclass
class PropagationResults:
    """Propagation constant and related quantities."""
    gamma: complex  # Propagation constant (cm⁻¹)
    alpha: float  # Attenuation constant (Np/cm)
    beta: float  # Phase constant (rad/cm)
    z0: complex  # Characteristic impedance (statohm)
    v_p: float  # Phase velocity (cm/s)
    wavelength: float  # Wavelength (cm)


@dataclass
class LineResults:
    """Complete transmission line analysis results."""
    z_in: complex  # Input impedance (statohm)
    gamma_l: complex  # Electrical length
    reflection_coefficient: complex
    vswr: float
    power_delivered: float  # erg/s
    efficiency: float  # fraction


# ============================================================================
# PHYSICAL CONSTANTS (CGS)
# ============================================================================

# Speed of light in vacuum (cm/s)
C_CGS = 2.99792458e10

# Permeability of free space (dimensionless in CGS)
MU_0_CGS = 1.0

# Permittivity of free space (dimensionless in CGS)
EPS_0_CGS = 1.0

# Intrinsic impedance of free space (statohm)
ETA_0 = 4 * np.pi / C_CGS  # ≈ 377 ohms in SI, different in CGS


# ============================================================================
# COAXIAL LINE PARAMETERS
# ============================================================================

def coaxial_inductance(a: float, b: float, mu_r: float = 1.0) -> float:
    """
    Calculate inductance per unit length of coaxial line.
    
    L = (μ/2π) × ln(b/a)  (CGS, dimensionless)
    
    Args:
        a: Inner conductor radius (cm)
        b: Outer conductor radius (cm)
        mu_r: Relative permeability of dielectric
    
    Returns:
        Inductance per unit length (cm/cm, dimensionless)
    """
    if a <= 0 or b <= a:
        raise ValueError("Invalid geometry: require 0 < a < b")
    return (mu_r / (2 * np.pi)) * np.log(b / a)


def coaxial_capacitance(a: float, b: float, K: float = 1.0) -> float:
    """
    Calculate capacitance per unit length of coaxial line.
    
    C = K / (2 × ln(b/a))  (CGS, statfarad/cm)
    
    Args:
        a: Inner conductor radius (cm)
        b: Outer conductor radius (cm)
        K: Dielectric constant (dimensionless)
    
    Returns:
        Capacitance per unit length (statfarad/cm)
    """
    if a <= 0 or b <= a:
        raise ValueError("Invalid geometry: require 0 < a < b")
    return K / (2 * np.log(b / a))


def coaxial_resistance(a: float, b: float, sigma: float, 
                       freq: float) -> float:
    """
    Calculate resistance per unit length including skin effect.
    
    R = 1/(2πσδ) × (1/a + 1/b)  (CGS, statohm/cm)
    
    Args:
        a: Inner conductor radius (cm)
        b: Outer conductor radius (cm)
        sigma: Conductor conductivity (s⁻¹, CGS)
        freq: Frequency (Hz)
    
    Returns:
        Resistance per unit length (statohm/cm)
    """
    omega = 2 * np.pi * freq
    
    # Skin depth in CGS: δ = √(2/(ωμσ))
    # For CGS: μ = mu_r (dimensionless), σ in s⁻¹
    delta = np.sqrt(2 / (omega * mu_r * sigma))
    
    r = (1 / (2 * np.pi * sigma * delta)) * (1/a + 1/b)
    return r


def coaxial_conductance(a: float, b: float, K: float, 
                        sigma_d: float) -> float:
    """
    Calculate conductance per unit length for lossy dielectric.
    
    G = 4πσ_d / K  (CGS, s⁻¹/cm)
    
    Args:
        a: Inner conductor radius (cm)
        b: Outer conductor radius (cm)
        K: Dielectric constant
        sigma_d: Dielectric conductivity (s⁻¹)
    
    Returns:
        Conductance per unit length (s⁻¹/cm)
    """
    return 4 * np.pi * sigma_d / K


def coaxial_characteristic_impedance(a: float, b: float, K: float,
                                      mu_r: float = 1.0) -> float:
    """
    Calculate characteristic impedance of coaxial line (lossless).
    
    Z0 = (1/2π) × √(μ/K) × ln(b/a)  (CGS, statohm)
    
    Args:
        a: Inner conductor radius (cm)
        b: Outer conductor radius (cm)
        K: Dielectric constant
        mu_r: Relative permeability
    
    Returns:
        Characteristic impedance (statohm)
    """
    return (1 / (2 * np.pi)) * np.sqrt(mu_r / K) * np.log(b / a)


# ============================================================================
# TWO-WIRE LINE PARAMETERS
# ============================================================================

def two_wire_inductance(a: float, d: float, mu_r: float = 1.0) -> float:
    """
    Calculate inductance per unit length of two-wire line.
    
    L = (μ/π) × arccosh(d/2a)  (CGS, dimensionless)
    
    For d >> a: arccosh(d/2a) ≈ ln(d/a)
    
    Args:
        a: Wire radius (cm)
        d: Wire separation (cm)
        mu_r: Relative permeability
    
    Returns:
        Inductance per unit length (cm/cm)
    """
    if a <= 0 or d <= 2*a:
        raise ValueError("Invalid geometry: require d > 2a")
    return (mu_r / np.pi) * np.arccosh(d / (2*a))


def two_wire_capacitance(a: float, d: float, K: float = 1.0) -> float:
    """
    Calculate capacitance per unit length of two-wire line.
    
    C = K / (2 × arccosh(d/2a))  (CGS, statfarad/cm)
    
    Args:
        a: Wire radius (cm)
        d: Wire separation (cm)
        K: Dielectric constant
    
    Returns:
        Capacitance per unit length (statfarad/cm)
    """
    if a <= 0 or d <= 2*a:
        raise ValueError("Invalid geometry: require d > 2a")
    return K / (2 * np.arccosh(d / (2*a)))


def two_wire_characteristic_impedance(a: float, d: float, K: float,
                                       mu_r: float = 1.0) -> float:
    """
    Calculate characteristic impedance of two-wire line (lossless).
    
    Z0 = (1/π) × √(μ/K) × arccosh(d/2a)  (CGS, statohm)
    
    For d >> a: Z0 ≈ (1/π) × √(μ/K) × ln(d/a)
    
    Args:
        a: Wire radius (cm)
        d: Wire separation (cm)
        K: Dielectric constant
        mu_r: Relative permeability
    
    Returns:
        Characteristic impedance (statohm)
    """
    return (1 / np.pi) * np.sqrt(mu_r / K) * np.arccosh(d / (2*a))


# ============================================================================
# MICROSTRIP PARAMETERS
# ============================================================================

def microstrip_effective_dielectric(w: float, h: float, K: float) -> float:
    """
    Calculate effective dielectric constant for microstrip.
    
    K_eff = (K+1)/2 + (K-1)/2 × (1 + 10h/w)^(-0.5)
    
    Args:
        w: Trace width (cm)
        h: Substrate height (cm)
        K: Substrate dielectric constant
    
    Returns:
        Effective dielectric constant (dimensionless)
    """
    if w <= 0 or h <= 0:
        raise ValueError("Invalid geometry")
    
    term = (1 + 10*h/w)**(-0.5)
    return (K + 1)/2 + (K - 1)/2 * term


def microstrip_characteristic_impedance(w: float, h: float, K: float,
                                         t: float = 0) -> float:
    """
    Calculate characteristic impedance of microstrip.
    
    For w/h ≤ 1:
    Z0 ≈ (60/√K_eff) × ln(8h/w + w/4h)
    
    For w/h > 1:
    Z0 ≈ (120π/√K_eff) / (w/h + 1.393 + 0.667×ln(w/h + 1.444))
    
    Args:
        w: Trace width (cm)
        h: Substrate height (cm)
        K: Substrate dielectric constant
        t: Trace thickness (cm, optional)
    
    Returns:
        Characteristic impedance (statohm)
    """
    K_eff = microstrip_effective_dielectric(w, h, K)
    sqrt_K = np.sqrt(K_eff)
    
    ratio = w / h
    
    if ratio <= 1:
        z0 = (60 / sqrt_K) * np.log(8*h/w + w/(4*h))
    else:
        denom = ratio + 1.393 + 0.667 * np.log(ratio + 1.444)
        z0 = (120 * np.pi / sqrt_K) / denom
    
    return z0


# ============================================================================
# PROPAGATION CONSTANTS
# ============================================================================

def propagation_constant(r: float, l: float, g: float, c: float,
                         omega: float) -> complex:
    """
    Calculate propagation constant.
    
    γ = α + jβ = √((R + jωL)(G + jωC))
    
    Args:
        r: Resistance per unit length (statohm/cm)
        l: Inductance per unit length (cm/cm)
        g: Conductance per unit length (s⁻¹/cm)
        c: Capacitance per unit length (statfarad/cm)
        omega: Angular frequency (rad/s)
    
    Returns:
        Propagation constant γ (cm⁻¹)
    """
    z_prime = complex(r, omega * l)  # Series impedance
    y_prime = complex(g, omega * c)  # Shunt admittance
    
    gamma = np.sqrt(z_prime * y_prime)
    return gamma


def characteristic_impedance(r: float, l: float, g: float, c: float,
                              omega: float) -> complex:
    """
    Calculate characteristic impedance.
    
    Z0 = √((R + jωL)/(G + jωC))
    
    Args:
        r: Resistance per unit length (statohm/cm)
        l: Inductance per unit length (cm/cm)
        g: Conductance per unit length (s⁻¹/cm)
        c: Capacitance per unit length (statfarad/cm)
        omega: Angular frequency (rad/s)
    
    Returns:
        Characteristic impedance (statohm)
    """
    z_prime = complex(r, omega * l)
    y_prime = complex(g, omega * c)
    
    z0 = np.sqrt(z_prime / y_prime)
    return z0


def attenuation_constant_low_loss(r: float, l: float, g: float, c: float,
                                   z0: float) -> float:
    """
    Calculate attenuation constant for low-loss line.
    
    α ≈ R/(2Z0) + G×Z0/2  (Np/cm)
    
    Args:
        r: Resistance per unit length (statohm/cm)
        l: Inductance per unit length (cm/cm)
        g: Conductance per unit length (s⁻¹/cm)
        c: Capacitance per unit length (statfarad/cm)
        z0: Characteristic impedance magnitude (statohm)
    
    Returns:
        Attenuation constant (Np/cm)
    """
    alpha_c = r / (2 * z0)  # Conductor loss
    alpha_d = g * z0 / 2  # Dielectric loss
    return alpha_c + alpha_d


def phase_constant_lossless(l: float, c: float, omega: float) -> float:
    """
    Calculate phase constant for lossless line.
    
    β = ω√(LC)
    
    Args:
        l: Inductance per unit length (cm/cm)
        c: Capacitance per unit length (statfarad/cm)
        omega: Angular frequency (rad/s)
    
    Returns:
        Phase constant (rad/cm)
    """
    return omega * np.sqrt(l * c)


def phase_velocity(l: float, c: float) -> float:
    """
    Calculate phase velocity for lossless line.
    
    v_p = 1/√(LC)
    
    Args:
        l: Inductance per unit length (cm/cm)
        c: Capacitance per unit length (statfarad/cm)
    
    Returns:
        Phase velocity (cm/s)
    """
    return 1 / np.sqrt(l * c)


def wavelength(beta: float) -> float:
    """
    Calculate wavelength from phase constant.
    
    λ = 2π/β
    
    Args:
        beta: Phase constant (rad/cm)
    
    Returns:
        Wavelength (cm)
    """
    return 2 * np.pi / beta


# ============================================================================
# INPUT IMPEDANCE
# ============================================================================

def input_impedance(z0: complex, z_l: complex, gamma: complex, 
                    length: float) -> complex:
    """
    Calculate input impedance of terminated line.
    
    Z_in = Z0 × (ZL + Z0×tanh(γl)) / (Z0 + ZL×tanh(γl))
    
    Args:
        z0: Characteristic impedance (statohm)
        z_l: Load impedance (statohm)
        gamma: Propagation constant (cm⁻¹)
        length: Line length (cm)
    
    Returns:
        Input impedance (statohm)
    """
    gamma_l = gamma * length
    tanh_gamma_l = np.tanh(gamma_l)
    
    z_in = z0 * (z_l + z0 * tanh_gamma_l) / (z0 + z_l * tanh_gamma_l)
    return z_in


def input_impedance_lossless(z0: float, z_l: complex, beta: float,
                              length: float) -> complex:
    """
    Calculate input impedance for lossless line.
    
    Z_in = Z0 × (ZL + j×Z0×tan(βl)) / (Z0 + j×ZL×tan(βl))
    
    Args:
        z0: Characteristic impedance (statohm)
        z_l: Load impedance (statohm)
        beta: Phase constant (rad/cm)
        length: Line length (cm)
    
    Returns:
        Input impedance (statohm)
    """
    beta_l = beta * length
    tan_beta_l = np.tan(beta_l)
    
    numerator = z_l + complex(0, z0 * tan_beta_l)
    denominator = z0 + complex(0, z_l * tan_beta_l)
    
    return z0 * numerator / denominator


def input_impedance_special(z0: float, z_l: complex, beta: float,
                            length: float, case: str) -> complex:
    """
    Calculate input impedance for special line lengths.
    
    Args:
        z0: Characteristic impedance (statohm)
        z_l: Load impedance (statohm)
        beta: Phase constant (rad/cm)
        length: Line length (cm)
        case: 'matched', 'short', 'open', 'quarter_wave', 'half_wave'
    
    Returns:
        Input impedance (statohm)
    """
    if case == 'matched':
        return z0
    
    elif case == 'short':
        # Z_L = 0
        return complex(0, z0 * np.tan(beta * length))
    
    elif case == 'open':
        # Z_L = ∞
        return complex(0, -z0 / np.tan(beta * length))
    
    elif case == 'quarter_wave':
        # l = λ/4, βl = π/2
        return (z0 ** 2) / z_l
    
    elif case == 'half_wave':
        # l = λ/2, βl = π
        return z_l
    
    else:
        raise ValueError(f"Unknown case: {case}")


# ============================================================================
# REFLECTION AND VSWR
# ============================================================================

def reflection_coefficient(z_l: complex, z0: complex) -> complex:
    """
    Calculate voltage reflection coefficient.
    
    Γ = (ZL - Z0) / (ZL + Z0)
    
    Args:
        z_l: Load impedance (statohm)
        z0: Characteristic impedance (statohm)
    
    Returns:
        Reflection coefficient (complex, |Γ| ≤ 1 for passive loads)
    """
    return (z_l - z0) / (z_l + z0)


def vswr(gamma: complex) -> float:
    """
    Calculate Voltage Standing Wave Ratio.
    
    VSWR = (1 + |Γ|) / (1 - |Γ|)
    
    Args:
        gamma: Reflection coefficient
    
    Returns:
        VSWR (≥ 1)
    """
    gamma_mag = abs(gamma)
    if gamma_mag >= 1:
        return float('inf')
    return (1 + gamma_mag) / (1 - gamma_mag)


def return_loss(gamma: complex) -> float:
    """
    Calculate return loss in dB.
    
    RL = -20 × log₁₀(|Γ|)
    
    Args:
        gamma: Reflection coefficient
    
    Returns:
        Return loss (dB, positive for passive loads)
    """
    gamma_mag = abs(gamma)
    if gamma_mag == 0:
        return float('inf')
    return -20 * np.log10(gamma_mag)


# ============================================================================
# POWER ANALYSIS
# ============================================================================

def incident_power(v_plus: float, z0: float) -> float:
    """
    Calculate incident power.
    
    P_inc = |V⁺|² / (2×Z0)
    
    Args:
        v_plus: Forward wave voltage amplitude (statvolt)
        z0: Characteristic impedance (statohm)
    
    Returns:
        Incident power (erg/s)
    """
    return (v_plus ** 2) / (2 * z0)


def reflected_power(v_plus: float, z0: float, gamma: complex) -> float:
    """
    Calculate reflected power.
    
    P_ref = |Γ|² × P_inc
    
    Args:
        v_plus: Forward wave voltage amplitude (statvolt)
        z0: Characteristic impedance (statohm)
        gamma: Reflection coefficient
    
    Returns:
        Reflected power (erg/s)
    """
    p_inc = incident_power(v_plus, z0)
    return (abs(gamma) ** 2) * p_inc


def delivered_power(v_plus: float, z0: float, gamma: complex) -> float:
    """
    Calculate power delivered to load.
    
    P_del = (1 - |Γ|²) × P_inc
    
    Args:
        v_plus: Forward wave voltage amplitude (statvolt)
        z0: Characteristic impedance (statohm)
        gamma: Reflection coefficient
    
    Returns:
        Delivered power (erg/s)
    """
    p_inc = incident_power(v_plus, z0)
    return (1 - abs(gamma) ** 2) * p_inc


def transmission_efficiency(gamma: complex, alpha: float, 
                            length: float) -> float:
    """
    Calculate overall transmission efficiency.
    
    η = (1 - |Γ|²) × exp(-2αl)
    
    Args:
        gamma: Reflection coefficient at load
        alpha: Attenuation constant (Np/cm)
        length: Line length (cm)
    
    Returns:
        Efficiency (0 to 1)
    """
    mismatch_loss = 1 - abs(gamma) ** 2
    attenuation_loss = np.exp(-2 * alpha * length)
    return mismatch_loss * attenuation_loss


# ============================================================================
# SKIN DEPTH
# ============================================================================

def skin_depth(sigma: float, mu_r: float, freq: float) -> float:
    """
    Calculate skin depth in CGS.
    
    δ = √(2/(ωμσ))
    
    Args:
        sigma: Conductivity (s⁻¹, CGS)
        mu_r: Relative permeability
        freq: Frequency (Hz)
    
    Returns:
        Skin depth (cm)
    """
    omega = 2 * np.pi * freq
    delta = np.sqrt(2 / (omega * mu_r * sigma))
    return delta


# ============================================================================
# MAXWELL ARTICLE REFERENCES
# ============================================================================

def get_maxwell_articles(topic: str) -> List[str]:
    """
    Get Maxwell article references for transmission line topic.
    
    Args:
        topic: Topic string
    
    Returns:
        List of article references
    """
    article_map = {
        'field_equations': ['Art. 604-619'],
        'wave_propagation': ['Art. 781-797'],
        'conduction_loss': ['Art. 287-300'],
        'energy_transport': ['Art. 56-57', 'Art. 424-430'],
        'speed_of_light': ['Art. 781-797'],
    }
    
    return article_map.get(topic, ['Art. 604-619', 'Art. 781-797'])


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Coaxial line
    a = 0.05  # cm (inner radius)
    b = 0.15  # cm (outer radius)
    K = 2.1   # dielectric constant
    
    z0 = coaxial_characteristic_impedance(a, b, K)
    l = coaxial_inductance(a, b)
    c = coaxial_capacitance(a, b, K)
    
    print(f"Coaxial Line (a={a} cm, b={b} cm, K={K})")
    print(f"  Z0 = {z0:.2f} statohm")
    print(f"  L = {l:.2e} cm/cm")
    print(f"  C = {c:.2e} statfarad/cm")
    
    # Propagation at 1 GHz
    freq = 1e9
    omega = 2 * np.pi * freq
    
    gamma = propagation_constant(0, l, 0, c, omega)
    v_p = phase_velocity(l, c)
    
    print(f"  At f = {freq/1e9} GHz:")
    print(f"    β = {gamma.imag:.2e} rad/cm")
    print(f"    v_p = {v_p:.2e} cm/s ({v_p/C_CGS*100:.1f}% of c)")
    
    # Example: Quarter-wave transformer
    z_l = 100  # statohm
    length = np.pi / (2 * gamma.imag)  # λ/4
    
    z_in = input_impedance_lossless(z0, z_l, gamma.imag, length)
    print(f"  Quarter-wave with ZL={z_l} statohm:")
    print(f"    Zin = {abs(z_in):.2f} statohm")
```

---

## Usage Examples

```python
from transmission_line_utils import *

# Example 1: Coaxial cable parameters
a, b, K = 0.05, 0.15, 2.1  # CGS units
z0 = coaxial_characteristic_impedance(a, b, K)
print(f"Coaxial Z0 = {z0:.2f} statohm")

# Example 2: Microstrip impedance
w, h, K = 0.1, 0.05, 4.5  # CGS units
z0 = microstrip_characteristic_impedance(w, h, K)
K_eff = microstrip_effective_dielectric(w, h, K)
print(f"Microstrip Z0 = {z0:.2f} statohm, K_eff = {K_eff:.2f}")

# Example 3: Reflection and VSWR
z_l = 150 + 50j  # statohm
z0 = 50  # statohm
gamma = reflection_coefficient(z_l, z0)
vswr_val = vswr(gamma)
print(f"Gamma = {gamma:.3f}, VSWR = {vswr_val:.2f}")

# Example 4: Quarter-wave transformer
z0_line = 75  # statohm
z_load = 100  # statohm
z_in = input_impedance_special(z0_line, z_load, 0, 0, 'quarter_wave')
print(f"Quarter-wave Zin = {z_in:.2f} statohm")
```

---

## Quality Criteria

- [ ] All computations in CGS units
- [ ] Maxwell article references included
- [ ] Multiple line types supported
- [ ] Loss and lossless cases handled
- [ ] Documentation complete
