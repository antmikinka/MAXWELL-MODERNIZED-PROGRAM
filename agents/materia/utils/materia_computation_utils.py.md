# Utility: materia_computation_utils

## Purpose

Python utility module for materials science computations in CGS units.

## Location

`agents/materia/utils/materia_computation_utils.py`

---

## Module Contents

```python
"""
MATERIA Computation Utilities

CGS unit computations for materials science in the Maxwell Treatise Modernization Project.

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class MaterialClassification(Enum):
    """Material classification types."""
    DIELECTRIC = "dielectric"
    MAGNETIC = "magnetic"
    CONDUCTIVE = "conductive"
    ELECTROLYTIC = "electrolytic"
    COMPOSITE = "composite"
    SEMICONDUCTOR = "semiconductor"


class TheoryClassification(Enum):
    """Theory classification for Maxwell treatise."""
    MAXWELL_ORIGINAL = "maxwell_original"
    USER_ORIGINAL = "user_original"  # DO NOT CHANGE
    STANDARD_MATH = "standard_math"


@dataclass
class DielectricProperties:
    """Dielectric material properties (CGS)."""
    K: float  # Dielectric constant (dimensionless)
    tan_delta: float  # Loss tangent
    breakdown_strength: float  # statvolt/cm
    resistivity: float  # statohm·cm
    temperature: float  # K
    maxwell_articles: List[str]
    theory_class: TheoryClassification = TheoryClassification.STANDARD_MATH


@dataclass
class MagneticProperties:
    """Magnetic material properties (CGS)."""
    mu: float  # Permeability (dimensionless)
    H_c: float  # Coercivity (oersted)
    B_r: float  # Remanence (gauss)
    B_sat: float  # Saturation (gauss)
    hysteresis_loss: float  # erg/cm³·cycle
    maxwell_articles: List[str]
    theory_class: TheoryClassification = TheoryClassification.STANDARD_MATH


@dataclass
class ElectrolyticProperties:
    """Electrolytic material properties (CGS)."""
    ion_name: str
    charge_number: int  # z
    mobility: float  # cm²/statvolt·s
    diffusion_coefficient: float  # cm²/s
    concentration: float  # mol/cm³
    maxwell_articles: List[str]
    theory_class: TheoryClassification = TheoryClassification.STANDARD_MATH


def cgs_to_si_potential(statvolt: float) -> float:
    """
    Convert CGS statvolt to SI volt.
    
    1 statvolt = 299.79 V
    """
    return statvolt * 299.79


def si_to_cgs_potential(volt: float) -> float:
    """
    Convert SI volt to CGS statvolt.
    
    1 V = 1/299.79 statvolt
    """
    return volt / 299.79


def cgs_to_si_field(statvolt_per_cm: float) -> float:
    """
    Convert CGS statvolt/cm to SI V/m.
    
    1 statvolt/cm = 29979 V/m
    """
    return statvolt_per_cm * 29979


def si_to_cgs_field(V_per_m: float) -> float:
    """
    Convert SI V/m to CGS statvolt/cm.
    """
    return V_per_m / 29979


def cgs_to_si_magnetic_field(oersted: float) -> float:
    """
    Convert CGS oersted to SI A/m.
    
    1 oersted = 79.577 A/m
    """
    return oersted * 79.577


def si_to_cgs_magnetic_field(A_per_m: float) -> float:
    """
    Convert SI A/m to CGS oersted.
    """
    return A_per_m / 79.577


def cgs_to_si_magnetic_induction(gauss: float) -> float:
    """
    Convert CGS gauss to SI tesla.
    
    1 gauss = 10⁻⁴ T
    """
    return gauss * 1e-4


def si_to_cgs_magnetic_induction(tesla: float) -> float:
    """
    Convert SI tesla to CGS gauss.
    """
    return tesla * 1e4


def maxwell_garnett_permittivity(
    K_m: float,
    K_i: float,
    f: float
) -> float:
    """
    Maxwell-Garnett formula for effective permittivity.
    
    K_eff = K_m × [(K_i + 2K_m + 2f(K_i - K_m)) / (K_i + 2K_m - f(K_i - K_m))]
    
    Reference: Maxwell, Treatise, Art. 314
    
    Args:
        K_m: Matrix permittivity (dimensionless)
        K_i: Inclusion permittivity (dimensionless)
        f: Inclusion volume fraction (0-1)
    
    Returns:
        K_eff: Effective permittivity (dimensionless)
    
    Validity: Dilute suspensions (f < 0.2)
    """
    if f < 0 or f > 1:
        raise ValueError("Volume fraction must be between 0 and 1")
    if f > 0.2:
        import warnings
        warnings.warn("Maxwell-Garnett formula may be inaccurate for f > 0.2")
    
    numerator = K_i + 2*K_m + 2*f*(K_i - K_m)
    denominator = K_i + 2*K_m - f*(K_i - K_m)
    
    return K_m * (numerator / denominator)


def bruggeman_permittivity(
    K_1: float,
    K_2: float,
    f_1: float,
    tolerance: float = 1e-10,
    max_iter: int = 1000
) -> float:
    """
    Bruggeman symmetric formula for effective permittivity.
    
    f₁ × (K₁ - K_eff) / (K₁ + 2K_eff) + f₂ × (K₂ - K_eff) / (K₂ + 2K_eff) = 0
    
    Solved numerically using Newton-Raphson method.
    
    Args:
        K_1: Phase 1 permittivity
        K_2: Phase 2 permittivity
        f_1: Phase 1 volume fraction
        tolerance: Convergence tolerance
        max_iter: Maximum iterations
    
    Returns:
        K_eff: Effective permittivity
    """
    f_2 = 1 - f_1
    
    def bruggeman_eq(K_eff):
        return (f_1 * (K_1 - K_eff) / (K_1 + 2*K_eff) + 
                f_2 * (K_2 - K_eff) / (K_2 + 2*K_eff))
    
    def d_bruggeman_dK(K_eff):
        term1 = -f_1 * (K_1 + 2*K_eff) - 2*f_1 * (K_1 - K_eff)
        term1 /= (K_1 + 2*K_eff)**2
        term2 = -f_2 * (K_2 + 2*K_eff) - 2*f_2 * (K_2 - K_eff)
        term2 /= (K_2 + 2*K_eff)**2
        return term1 + term2
    
    # Initial guess: arithmetic mean
    K_eff = f_1 * K_1 + f_2 * K_2
    
    for i in range(max_iter):
        f_val = bruggeman_eq(K_eff)
        if abs(f_val) < tolerance:
            break
        
        df_dK = d_bruggeman_dK(K_eff)
        if abs(df_dK) < 1e-15:
            break
            
        K_eff -= f_val / df_dK
    
    return K_eff


def wiener_bounds(
    K_1: float,
    K_2: float,
    f_1: float
) -> Tuple[float, float]:
    """
    Calculate Wiener bounds for effective permittivity.
    
    Upper bound (parallel/Voigt): K_upper = f₁K₁ + f₂K₂
    Lower bound (series/Reuss): 1/K_lower = f₁/K₁ + f₂/K₂
    
    Args:
        K_1, K_2: Phase permittivities
        f_1: Phase 1 volume fraction
    
    Returns:
        (K_lower, K_upper): Rigorous bounds
    """
    f_2 = 1 - f_1
    
    K_upper = f_1 * K_1 + f_2 * K_2
    K_lower = 1 / (f_1/K_1 + f_2/K_2)
    
    return K_lower, K_upper


def dielectric_energy_density(K: float, E: float) -> float:
    """
    Calculate energy density in dielectric (CGS).
    
    u = (K / 8π) × E²
    
    Reference: Maxwell, Treatise, Art. 56-57
    
    Args:
        K: Dielectric constant (dimensionless)
        E: Electric field (statvolt/cm)
    
    Returns:
        u: Energy density (erg/cm³)
    """
    return (K / (8 * np.pi)) * E**2


def magnetic_energy_density(mu: float, H: float) -> float:
    """
    Calculate energy density in magnetic field (CGS).
    
    u = (μ / 8π) × H²
    
    Reference: Maxwell, Treatise, Art. 424-426
    
    Args:
        mu: Permeability (dimensionless)
        H: Magnetic field (oersted)
    
    Returns:
        u: Energy density (erg/cm³)
    """
    return (mu / (8 * np.pi)) * H**2


def susceptibility_from_permeability(mu: float) -> float:
    """
    Calculate magnetic susceptibility from permeability (CGS).
    
    κ = (μ - 1) / 4π
    
    Reference: Maxwell, Treatise, Art. 424-440
    
    Args:
        mu: Permeability (dimensionless)
    
    Returns:
        kappa: Susceptibility (dimensionless)
    """
    return (mu - 1) / (4 * np.pi)


def permeability_from_susceptibility(kappa: float) -> float:
    """
    Calculate permeability from susceptibility (CGS).
    
    μ = 1 + 4πκ
    
    Args:
        kappa: Susceptibility (dimensionless)
    
    Returns:
        mu: Permeability (dimensionless)
    """
    return 1 + 4 * np.pi * kappa


def steinmetz_hysteresis_loss(
    eta: float,
    B_max: float,
    n: float = 1.6,
    f: float = 1.0
) -> float:
    """
    Calculate hysteresis loss using Steinmetz equation.
    
    W_h = η × B_max^n × f
    
    Reference: Maxwell, Treatise, Art. 424-430
    
    Args:
        eta: Loss coefficient (erg/cm³·cycle)
        B_max: Maximum flux density (gauss)
        n: Steinmetz exponent (typically 1.6-2.0)
        f: Frequency (Hz)
    
    Returns:
        W_h: Hysteresis loss (erg/cm³·s)
    """
    return eta * (B_max ** n) * f


def nernst_equation(
    E0: float,
    z: int,
    T: float,
    Q: float,
    R: float = 8.314e7,
    F: float = 96485
) -> float:
    """
    Nernst equation for electrode potential.
    
    E = E° - (RT/zF) × ln(Q)
    
    Reference: Maxwell, Treatise, Art. 280-286
    
    Args:
        E0: Standard potential (statvolt)
        z: Charge number
        T: Temperature (K)
        Q: Reaction quotient
        R: Gas constant (erg/mol·K)
        F: Faraday constant (C/mol)
    
    Returns:
        E: Electrode potential (statvolt)
    """
    # Convert F to CGS (statcoulomb/equiv)
    F_cgs = F * 2.873e14 / 96485  # statcoulomb/equiv
    
    return E0 - (R * T / (z * F_cgs)) * np.log(Q)


def diffusion_coefficient_from_mobility(
    u: float,
    T: float,
    z: int = 1
) -> float:
    """
    Calculate diffusion coefficient from mobility (Einstein relation).
    
    D = (kT/q) × u
    
    Args:
        u: Mobility (cm²/statvolt·s)
        T: Temperature (K)
        z: Charge number
    
    Returns:
        D: Diffusion coefficient (cm²/s)
    """
    k_B = 1.381e-16  # erg/K
    e = 4.803e-10  # statcoulomb
    
    return (k_B * T / (z * e)) * u


def limiting_current_density(
    z: int,
    D: float,
    c_b: float,
    delta: float,
    F_cgs: float = 2.873e14
) -> float:
    """
    Calculate limiting current density for electrolysis.
    
    j_L = zFDc_b / δ
    
    Reference: Maxwell, Treatise, Art. 230-235
    
    Args:
        z: Charge number
        D: Diffusion coefficient (cm²/s)
        c_b: Bulk concentration (mol/cm³)
        delta: Diffusion layer thickness (cm)
        F_cgs: Faraday constant (statcoulomb/equiv)
    
    Returns:
        j_L: Limiting current density (statampere/cm²)
    """
    return z * F_cgs * D * c_b / delta


def validate_cgs_units(properties: Dict) -> bool:
    """
    Validate that properties are within reasonable CGS ranges.
    
    Args:
        properties: Dictionary of material properties
    
    Returns:
        valid: True if all properties are reasonable
    """
    # Add validation logic for each property type
    if 'K' in properties:
        if properties['K'] < 1:
            return False
    if 'mu' in properties:
        if properties['mu'] < 0:
            return False
    if 'tan_delta' in properties:
        if properties['tan_delta'] < 0 or properties['tan_delta'] > 1:
            return False
    
    return True


def get_maxwell_articles(material_type: str) -> List[str]:
    """
    Get relevant Maxwell article references for material type.
    
    Args:
        material_type: Type of material
    
    Returns:
        List of article references
    """
    article_map = {
        'dielectric': ['Art. 50-62', 'Art. 79-83', 'Art. 103-111', 'Art. 60-62'],
        'magnetic': ['Art. 424-448', 'Art. 444-447', 'Art. 371-400'],
        'electrolytic': ['Art. 236-238', 'Art. 269-286', 'Art. 230-235'],
        'conductive': ['Art. 287-300', 'Art. 301-320', 'Art. 230-235'],
        'composite': ['Art. 314', 'Art. 103-111']
    }
    
    return article_map.get(material_type, [])
```

---

## Usage Examples

```python
from materia_computation_utils import *

# Example 1: Maxwell-Garnett effective permittivity
K_eff = maxwell_garnett_permittivity(K_m=3.5, K_i=7.0, f=0.15)
print(f"Effective permittivity: {K_eff:.3f}")

# Example 2: Unit conversion
E_si = cgs_to_si_field(100)  # 100 statvolt/cm to V/m
print(f"Electric field: {E_si:.1f} V/m")

# Example 3: Magnetic susceptibility
kappa = susceptibility_from_permeability(5000)
print(f"Susceptibility: {kappa:.1f}")

# Example 4: Hysteresis loss
W_h = steinmetz_hysteresis_loss(eta=200, B_max=10000, n=1.6, f=60)
print(f"Hysteresis loss: {W_h:.1f} erg/cm³·s")

# Example 5: Get Maxwell articles
articles = get_maxwell_articles('dielectric')
print(f"Relevant articles: {articles}")
```

---

## Quality Criteria

- [ ] All computations in CGS units
- [ ] Maxwell article references included
- [ ] Theory classification enforced
- [ ] Input validation implemented
- [ ] Documentation complete
