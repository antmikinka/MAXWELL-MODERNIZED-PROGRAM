# Utility: instrumentum_computation_utils

## Purpose

Python utility module for instrument computations in CGS units.

## Location

`agents/instrumentum/utils/instrumentum_computation_utils.py`

---

## Module Contents

```python
"""
INSTRUMENTUM Computation Utilities

CGS unit computations for instrument analysis in the Maxwell Treatise Modernization Project.

Supported Instruments:
- Galvanometers (moving coil, moving magnet, mirror)
- Magnetometers (deflection, vibration)
- Electrometers (quadrant, vibrating reed)

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Art. 730-750, Art. 424-440, Art. 230-235
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class InstrumentType(Enum):
    """Instrument types."""
    GALVANOMETER = "galvanometer"
    MAGNETOMETER = "magnetometer"
    ELECTROMETER = "electrometer"


class GalvanometerType(Enum):
    """Galvanometer subtypes."""
    MOVING_COIL = "moving_coil"
    MOVING_MAGNET = "moving_magnet"
    MIRROR = "mirror"
    TANGENT = "tangent"
    ASTATIC = "astatic"


# ============================================================================
# PHYSICAL CONSTANTS (CGS)
# ============================================================================

# Boltzmann constant (erg/K)
K_B = 1.381e-16

# Elementary charge (statC)
E_CHARGE = 4.803e-10

# Speed of light (cm/s)
C_CGS = 2.99792458e10

# Room temperature (K)
T_ROOM = 293.0


# ============================================================================
# GALVANOMETER CALCULATIONS
# ============================================================================

def galvanometer_current_sensitivity(
    N: float,      # Number of turns
    A: float,      # Coil area (cm²)
    B: float,      # Magnetic field (gauss)
    kappa: float   # Spring constant (dyne·cm/rad)
) -> float:
    """
    Calculate galvanometer current sensitivity.
    
    S_I = N·A·B / κ  (cm/statampere)
    
    Args:
        N: Number of turns
        A: Coil area (cm²)
        B: Magnetic field (gauss)
        kappa: Spring constant (dyne·cm/rad)
    
    Returns:
        Current sensitivity (cm/statampere)
    
    Maxwell Reference: Art. 730-750
    """
    return (N * A * B) / kappa


def galvanometer_voltage_sensitivity(
    S_I: float,    # Current sensitivity (cm/statampere)
    R_total: float # Total resistance (statohm)
) -> float:
    """
    Calculate galvanometer voltage sensitivity.
    
    S_V = S_I / R_total
    
    Args:
        S_I: Current sensitivity (cm/statampere)
        R_total: Total circuit resistance (statohm)
    
    Returns:
        Voltage sensitivity (cm/statvolt)
    """
    return S_I / R_total


def galvanometer_natural_frequency(
    kappa: float,  # Spring constant (dyne·cm/rad)
    J: float       # Moment of inertia (g·cm²)
) -> float:
    """
    Calculate galvanometer natural frequency.
    
    ω_n = √(κ/J)
    
    Args:
        kappa: Spring constant (dyne·cm/rad)
        J: Moment of inertia (g·cm²)
    
    Returns:
        Natural frequency (rad/s)
    """
    return np.sqrt(kappa / J)


def galvanometer_damping_ratio(
    D: float,      # Damping coefficient (dyne·cm·s)
    kappa: float,  # Spring constant (dyne·cm/rad)
    J: float       # Moment of inertia (g·cm²)
) -> float:
    """
    Calculate galvanometer damping ratio.
    
    ζ = D / (2√(J·κ))
    
    Args:
        D: Damping coefficient (dyne·cm·s)
        kappa: Spring constant (dyne·cm/rad)
        J: Moment of inertia (g·cm²)
    
    Returns:
        Damping ratio (dimensionless)
    """
    return D / (2 * np.sqrt(J * kappa))


def galvanometer_electromagnetic_damping(
    N: float,      # Number of turns
    A: float,      # Coil area (cm²)
    B: float,      # Magnetic field (gauss)
    R_total: float # Total resistance (statohm)
) -> float:
    """
    Calculate electromagnetic damping coefficient.
    
    D_em = (N·A·B)² / R_total
    
    Args:
        N: Number of turns
        A: Coil area (cm²)
        B: Magnetic field (gauss)
        R_total: Total circuit resistance (statohm)
    
    Returns:
        Damping coefficient (dyne·cm·s)
    """
    return ((N * A * B) ** 2) / R_total


def tangent_galvanometer_current(
    R: float,      # Coil radius (cm)
    N: float,      # Number of turns
    H: float,      # Earth's field (oersted)
    theta: float   # Deflection angle (radians)
) -> float:
    """
    Calculate current from tangent galvanometer deflection.
    
    I = (2·R·H / N) · tan(θ)
    
    Args:
        R: Coil radius (cm)
        N: Number of turns
        H: Earth's horizontal field (oersted)
        theta: Deflection angle (radians)
    
    Returns:
        Current (statampere)
    
    Maxwell Reference: Art. 730-750
    """
    return (2 * R * H / N) * np.tan(theta)


def tangent_galvanometer_reduction_factor(
    R: float,      # Coil radius (cm)
    N: float,      # Number of turns
    H: float       # Earth's field (oersted)
) -> float:
    """
    Calculate reduction factor for tangent galvanometer.
    
    K = 2·R·H / N
    
    Args:
        R: Coil radius (cm)
        N: Number of turns
        H: Earth's field (oersted)
    
    Returns:
        Reduction factor (statampere)
    """
    return (2 * R * H) / N


# ============================================================================
# MAGNETOMETER CALCULATIONS
# ============================================================================

def deflection_magnetometer_field(
    kappa: float,  # Torsion constant (dyne·cm/rad)
    m: float,      # Magnetic moment (emu)
    theta: float   # Deflection angle (radians)
) -> float:
    """
    Calculate magnetic field from deflection magnetometer.
    
    H = (κ/m) · θ
    
    Args:
        kappa: Torsion constant (dyne·cm/rad)
        m: Magnetic moment (emu)
        theta: Deflection angle (radians)
    
    Returns:
        Magnetic field (oersted)
    
    Maxwell Reference: Art. 424-440
    """
    return (kappa / m) * theta


def vibration_magnetometer_field(
    J: float,      # Moment of inertia (g·cm²)
    m: float,      # Magnetic moment (emu)
    T: float       # Period (s)
) -> float:
    """
    Calculate magnetic field from vibration magnetometer.
    
    H = (4π²·J) / (m·T²)
    
    Args:
        J: Moment of inertia (g·cm²)
        m: Magnetic moment (emu)
        T: Period (s)
    
    Returns:
        Magnetic field (oersted)
    
    Maxwell Reference: Art. 449-474
    """
    return (4 * np.pi**2 * J) / (m * T**2)


def vibration_magnetometer_period(
    J: float,      # Moment of inertia (g·cm²)
    m: float,      # Magnetic moment (emu)
    H: float       # Magnetic field (oersted)
) -> float:
    """
    Calculate vibration period.
    
    T = 2π · √(J/(m·H))
    
    Args:
        J: Moment of inertia (g·cm²)
        m: Magnetic moment (emu)
        H: Magnetic field (oersted)
    
    Returns:
        Period (s)
    """
    return 2 * np.pi * np.sqrt(J / (m * H))


def magnetic_moment_from_dimensions(
    length: float,  # Magnet length (cm)
    cross_section: float,  # Cross-sectional area (cm²)
    M_sat: float    # Saturation magnetization (emu/cm³)
) -> float:
    """
    Calculate magnetic moment from magnet dimensions.
    
    m = M × V = M_sat × A × L
    
    Args:
        length: Magnet length (cm)
        cross_section: Cross-sectional area (cm²)
        M_sat: Saturation magnetization (emu/cm³)
    
    Returns:
        Magnetic moment (emu)
    """
    volume = length * cross_section
    return M_sat * volume


# ============================================================================
# ELECTROMETER CALCULATIONS
# ============================================================================

def quadrant_electrometer_torque(
    V_A: float,    # Quadrant A potential (statvolt)
    V_B: float,    # Quadrant B potential (statvolt)
    V_n: float,    # Needle potential (statvolt)
    dC_dtheta: float  # Capacitance gradient (statfarad/rad)
) -> float:
    """
    Calculate torque on quadrant electrometer needle.
    
    τ = (1/2) · (V_A - V_B) · V_n · (dC/dθ)
    
    Args:
        V_A: Quadrant A potential (statvolt)
        V_B: Quadrant B potential (statvolt)
        V_n: Needle potential (statvolt)
        dC_dtheta: Capacitance gradient (statfarad/rad)
    
    Returns:
        Torque (dyne·cm)
    
    Maxwell Reference: Art. 230-235
    """
    return 0.5 * (V_A - V_B) * V_n * dC_dtheta


def quadrant_electrometer_deflection(
    V_A: float,    # Quadrant A potential (statvolt)
    V_B: float,    # Quadrant B potential (statvolt)
    V_n: float,    # Needle potential (statvolt)
    dC_dtheta: float,  # Capacitance gradient (statfarad/rad)
    kappa: float   # Torsion constant (dyne·cm/rad)
) -> float:
    """
    Calculate needle deflection angle.
    
    θ = τ / κ = [(1/2) · (V_A - V_B) · V_n · (dC/dθ)] / κ
    
    Args:
        V_A: Quadrant A potential (statvolt)
        V_B: Quadrant B potential (statvolt)
        V_n: Needle potential (statvolt)
        dC_dtheta: Capacitance gradient (statfarad/rad)
        kappa: Torsion constant (dyne·cm/rad)
    
    Returns:
        Deflection angle (radians)
    """
    torque = quadrant_electrometer_torque(V_A, V_B, V_n, dC_dtheta)
    return torque / kappa


def quadrant_electrometer_sensitivity(
    V_n: float,    # Needle potential (statvolt)
    dC_dtheta: float,  # Capacitance gradient (statfarad/rad)
    kappa: float   # Torsion constant (dyne·cm/rad)
) -> float:
    """
    Calculate voltage sensitivity.
    
    S_V = θ / (V_A - V_B) = (V_n / 2κ) · (dC/dθ)
    
    Args:
        V_n: Needle potential (statvolt)
        dC_dtheta: Capacitance gradient (statfarad/rad)
        kappa: Torsion constant (dyne·cm/rad)
    
    Returns:
        Sensitivity (rad/statvolt)
    """
    return (V_n * dC_dtheta) / (2 * kappa)


def electrometer_charge_sensitivity(
    C_f: float     # Feedback capacitance (statfarad)
) -> float:
    """
    Calculate charge sensitivity.
    
    S_Q = dV_out/dQ = 1/C_f
    
    Args:
        C_f: Feedback capacitance (statfarad)
    
    Returns:
        Charge sensitivity (statvolt/statcoulomb)
    """
    return 1 / C_f


# ============================================================================
# NOISE CALCULATIONS
# ============================================================================

def thermal_noise_voltage(
    R: float,      # Resistance (statohm)
    T: float,      # Temperature (K)
    BW: float      # Bandwidth (Hz)
) -> float:
    """
    Calculate thermal noise voltage.
    
    e_n = √(4·k_B·T·R·Δf)
    
    Args:
        R: Resistance (statohm)
        T: Temperature (K)
        BW: Bandwidth (Hz)
    
    Returns:
        RMS noise voltage (statvolt)
    """
    return np.sqrt(4 * K_B * T * R * BW)


def thermal_noise_current(
    R: float,      # Resistance (statohm)
    T: float,      # Temperature (K)
    BW: float      # Bandwidth (Hz)
) -> float:
    """
    Calculate thermal noise current.
    
    i_n = √(4·k_B·T·Δf / R)
    
    Args:
        R: Resistance (statohm)
        T: Temperature (K)
        BW: Bandwidth (Hz)
    
    Returns:
        RMS noise current (statampere)
    """
    return np.sqrt(4 * K_B * T * BW / R)


def shot_noise_current(
    I: float,      # DC current (statampere)
    BW: float      # Bandwidth (Hz)
) -> float:
    """
    Calculate shot noise current.
    
    i_n = √(2·q·I·Δf)
    
    Args:
        I: DC current (statampere)
        BW: Bandwidth (Hz)
    
    Returns:
        RMS noise current (statampere)
    """
    return np.sqrt(2 * E_CHARGE * I * BW)


def minimum_detectable_signal(
    noise_rms: float,  # RMS noise
    sensitivity: float,  # Instrument sensitivity
    SNR_min: float = 1.0  # Minimum SNR
) -> float:
    """
    Calculate minimum detectable signal.
    
    MDS = SNR_min × noise_rms / sensitivity
    
    Args:
        noise_rms: RMS noise level
        sensitivity: Instrument sensitivity
        SNR_min: Minimum SNR for detection
    
    Returns:
        Minimum detectable input
    """
    return SNR_min * noise_rms / sensitivity


def integration_improvement(
    MDS_1s: float,  # MDS for 1 second integration
    t: float        # Integration time (s)
) -> float:
    """
    Calculate MDS with integration.
    
    MDS(t) = MDS(1s) / √t
    
    Args:
        MDS_1s: MDS for 1 second
        t: Integration time (s)
    
    Returns:
        MDS at integration time t
    """
    return MDS_1s / np.sqrt(t)


# ============================================================================
# MAXWELL ARTICLE REFERENCES
# ============================================================================

def get_maxwell_articles(instrument_type: str) -> List[str]:
    """
    Get Maxwell article references for instrument type.
    
    Args:
        instrument_type: Type of instrument
    
    Returns:
        List of article references
    """
    article_map = {
        'galvanometer': ['Art. 730-750', 'Art. 475-500'],
        'magnetometer': ['Art. 449-474', 'Art. 424-440'],
        'electrometer': ['Art. 230-235', 'Art. 44-49'],
        'bridge': ['Art. 343-348', 'Art. 287-300'],
    }
    
    return article_map.get(instrument_type, ['Art. 730-750'])


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Moving coil galvanometer
    N, A, B, kappa = 100, 4.0, 2000, 0.1
    S_I = galvanometer_current_sensitivity(N, A, B, kappa)
    print(f"Galvanometer current sensitivity: {S_I:.2e} cm/statampere")
    
    # Example: Vibration magnetometer
    J, m, H = 1.0, 100, 0.5
    T = vibration_magnetometer_period(J, m, H)
    print(f"Vibration period: {T:.3f} s")
    
    # Example: Quadrant electrometer
    V_A, V_B, V_n, dC_dtheta, kappa = 10, 0, 100, 0.01, 0.001
    theta = quadrant_electrometer_deflection(V_A, V_B, V_n, dC_dtheta, kappa)
    print(f"Electrometer deflection: {theta:.4f} rad")
    
    # Example: Thermal noise
    R, T, BW = 1000, 293, 1000
    e_n = thermal_noise_voltage(R, T, BW)
    print(f"Thermal noise: {e_n:.4e} statvolt")
```

---

## Usage Examples

```python
from instrumentum_computation_utils import *

# Example 1: Galvanometer sensitivity
S_I = galvanometer_current_sensitivity(100, 4.0, 2000, 0.1)
print(f"Current sensitivity: {S_I:.2e} cm/statampere")

# Example 2: Magnetometer field
H = deflection_magnetometer_field(0.001, 100, 0.1)
print(f"Magnetic field: {H:.4f} oersted")

# Example 3: Electrometer deflection
theta = quadrant_electrometer_deflection(10, 0, 100, 0.01, 0.001)
print(f"Deflection: {theta:.4f} rad")

# Example 4: Thermal noise
e_n = thermal_noise_voltage(1000, 293, 1000)
print(f"Thermal noise: {e_n:.4e} statvolt")
```

---

## Quality Criteria

- [ ] All computations in CGS units
- [ ] Maxwell article references included
- [ ] Instrument physics correctly modeled
- [ ] Noise calculations implemented
- [ ] Documentation complete
