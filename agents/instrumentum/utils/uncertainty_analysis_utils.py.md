# Utility: uncertainty_analysis_utils

## Purpose

Python utility module for measurement uncertainty analysis following GUM (Guide to the Expression of Uncertainty in Measurement).

## Location

`agents/instrumentum/utils/uncertainty_analysis_utils.py`

---

## Module Contents

```python
"""
INSTRUMENTUM Uncertainty Analysis Utilities

Uncertainty evaluation following GUM methodology for measurements
in the Maxwell Treatise Modernization Project.

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations (GUM)

Maxwell References: Art. 287-300, Art. 343-348
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np
from scipy import stats


class DistributionType(Enum):
    """Probability distribution types."""
    NORMAL = "normal"
    RECTANGULAR = "rectangular"
    TRIANGULAR = "triangular"
    U_SHAPED = "u_shaped"
    STUDENT_T = "student_t"


@dataclass
class UncertaintyComponent:
    """Individual uncertainty component."""
    name: str
    value: float
    unit: str
    distribution: DistributionType
    divisor: float
    dof: float  # Degrees of freedom (inf for Type B)
    uncertainty_type: str  # 'A' or 'B'
    
    @property
    def standard_uncertainty(self) -> float:
        """Calculate standard uncertainty."""
        return self.value / self.divisor
    
    @property
    def variance(self) -> float:
        """Calculate variance."""
        return self.standard_uncertainty ** 2


@dataclass
class UncertaintyBudget:
    """Complete uncertainty budget."""
    measurand: str
    result: float
    unit: str
    components: List[UncertaintyComponent]
    combined_uncertainty: float
    effective_dof: float
    coverage_factor: float
    expanded_uncertainty: float
    confidence_level: float


# ============================================================================
# DISTRIBUTION DIVISORS
# ============================================================================

def get_distribution_divisor(
    distribution: DistributionType,
    coverage: Optional[float] = None,
    dof: Optional[float] = None
) -> float:
    """
    Get divisor for converting to standard uncertainty.
    
    Args:
        distribution: Distribution type
        coverage: Coverage factor (for normal)
        dof: Degrees of freedom (for t-distribution)
    
    Returns:
        Divisor for standard uncertainty calculation
    """
    if distribution == DistributionType.NORMAL:
        return coverage if coverage else 2.0
    
    elif distribution == DistributionType.RECTANGULAR:
        return np.sqrt(3)
    
    elif distribution == DistributionType.TRIANGULAR:
        return np.sqrt(6)
    
    elif distribution == DistributionType.U_SHAPED:
        return np.sqrt(2)
    
    elif distribution == DistributionType.STUDENT_T:
        if dof is None:
            dof = float('inf')
        return stats.t.ppf(0.975, dof)
    
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


# ============================================================================
# TYPE A EVALUATION
# ============================================================================

def type_a_uncertainty(
    observations: List[float]
) -> Tuple[float, float, float]:
    """
    Evaluate Type A uncertainty from repeated observations.
    
    Args:
        observations: List of observed values
    
    Returns:
        (mean, standard_uncertainty, degrees_of_freedom)
    """
    n = len(observations)
    if n < 2:
        raise ValueError("Need at least 2 observations")
    
    mean = np.mean(observations)
    std_dev = np.std(observations, ddof=1)  # Sample standard deviation
    std_uncertainty = std_dev / np.sqrt(n)  # Standard uncertainty of mean
    dof = n - 1
    
    return mean, std_uncertainty, dof


def type_a_uncertainty_from_stats(
    mean: float,
    std_dev: float,
    n: int
) -> Tuple[float, float, float]:
    """
    Evaluate Type A uncertainty from summary statistics.
    
    Args:
        mean: Sample mean
        std_dev: Sample standard deviation
        n: Number of observations
    
    Returns:
        (mean, standard_uncertainty, degrees_of_freedom)
    """
    std_uncertainty = std_dev / np.sqrt(n)
    dof = n - 1
    
    return mean, std_uncertainty, dof


def pooled_standard_deviation(
    data_sets: List[List[float]]
) -> float:
    """
    Calculate pooled standard deviation from multiple data sets.
    
    Args:
        data_sets: List of data sets (each a list of observations)
    
    Returns:
        Pooled standard deviation
    """
    total_ss = 0
    total_df = 0
    
    for data in data_sets:
        n = len(data)
        if n < 2:
            continue
        variance = np.var(data, ddof=1)
        total_ss += variance * (n - 1)
        total_df += n - 1
    
    if total_df == 0:
        raise ValueError("No valid data sets")
    
    return np.sqrt(total_ss / total_df)


# ============================================================================
# TYPE B EVALUATION
# ============================================================================

def type_b_from_tolerance(
    tolerance: float,
    distribution: DistributionType = DistributionType.RECTANGULAR,
    confidence: Optional[float] = None
) -> float:
    """
    Evaluate Type B uncertainty from tolerance specification.
    
    Args:
        tolerance: Half-width of tolerance interval
        distribution: Assumed distribution
        confidence: Confidence level (for normal distribution)
    
    Returns:
        Standard uncertainty
    """
    divisor = get_distribution_divisor(distribution, confidence)
    return tolerance / divisor


def type_b_from_calibration(
    stated_uncertainty: float,
    coverage_factor: float
) -> float:
    """
    Evaluate Type B uncertainty from calibration certificate.
    
    Args:
        stated_uncertainty: Expanded uncertainty from certificate
        coverage_factor: Coverage factor (k) from certificate
    
    Returns:
        Standard uncertainty
    """
    return stated_uncertainty / coverage_factor


def type_b_from_resolution(
    resolution: float,
    distribution: DistributionType = DistributionType.RECTANGULAR
) -> float:
    """
    Evaluate Type B uncertainty from instrument resolution.
    
    Args:
        resolution: Instrument resolution
        distribution: Assumed distribution (typically rectangular)
    
    Returns:
        Standard uncertainty
    """
    # For resolution, use half-width
    half_width = resolution / 2
    divisor = get_distribution_divisor(distribution)
    return half_width / divisor


def type_b_from_drift(
    drift_rate: float,
    time_since_calibration: float,
    distribution: DistributionType = DistributionType.RECTANGULAR
) -> float:
    """
    Evaluate Type B uncertainty from drift.
    
    Args:
        drift_rate: Drift per unit time
        time_since_calibration: Time since last calibration
        distribution: Assumed distribution
    
    Returns:
        Standard uncertainty
    """
    max_drift = drift_rate * time_since_calibration
    divisor = get_distribution_divisor(distribution)
    return max_drift / divisor


def type_b_from_temperature(
    temperature_coefficient: float,
    temperature_variation: float,
    distribution: DistributionType = DistributionType.RECTANGULAR
) -> float:
    """
    Evaluate Type B uncertainty from temperature effects.
    
    Args:
        temperature_coefficient: Effect per degree
        temperature_variation: Temperature variation
        distribution: Assumed distribution
    
    Returns:
        Standard uncertainty
    """
    max_effect = temperature_coefficient * temperature_variation
    divisor = get_distribution_divisor(distribution)
    return max_effect / divisor


# ============================================================================
# UNCERTAINTY COMBINATION
# ============================================================================

def combine_uncertainties(
    components: List[UncertaintyComponent],
    sensitivity_coefficients: Optional[List[float]] = None
) -> Tuple[float, float]:
    """
    Combine uncertainty components.
    
    Args:
        components: List of uncertainty components
        sensitivity_coefficients: Optional sensitivity coefficients
    
    Returns:
        (combined_uncertainty, effective_degrees_of_freedom)
    """
    if sensitivity_coefficients is None:
        sensitivity_coefficients = [1.0] * len(components)
    
    if len(components) != len(sensitivity_coefficients):
        raise ValueError("Mismatch between components and coefficients")
    
    # Calculate combined uncertainty
    u_c_squared = 0
    for comp, c_i in zip(components, sensitivity_coefficients):
        u_i = comp.standard_uncertainty
        u_c_squared += (c_i * u_i) ** 2
    
    u_c = np.sqrt(u_c_squared)
    
    # Calculate effective degrees of freedom (Welch-Satterthwaite)
    numerator = u_c ** 4
    denominator = 0
    
    for comp, c_i in zip(components, sensitivity_coefficients):
        if comp.dof > 0 and comp.dof != float('inf'):
            u_i = comp.standard_uncertainty
            term = (c_i * u_i) ** 4 / comp.dof
            denominator += term
    
    if denominator == 0:
        nu_eff = float('inf')
    else:
        nu_eff = numerator / denominator
    
    return u_c, nu_eff


def welch_satterthwaite(
    u_c: float,
    components: List[UncertaintyComponent],
    sensitivity_coefficients: Optional[List[float]] = None
) -> float:
    """
    Calculate effective degrees of freedom using Welch-Satterthwaite formula.
    
    Args:
        u_c: Combined uncertainty
        components: Uncertainty components
        sensitivity_coefficients: Optional sensitivity coefficients
    
    Returns:
        Effective degrees of freedom
    """
    if sensitivity_coefficients is None:
        sensitivity_coefficients = [1.0] * len(components)
    
    numerator = u_c ** 4
    denominator = 0
    
    for comp, c_i in zip(components, sensitivity_coefficients):
        if comp.dof > 0 and comp.dof != float('inf'):
            u_i = comp.standard_uncertainty
            term = (c_i * u_i) ** 4 / comp.dof
            denominator += term
    
    if denominator == 0:
        return float('inf')
    
    return numerator / denominator


# ============================================================================
# EXPANDED UNCERTAINTY
# ============================================================================

def coverage_factor(
    confidence_level: float = 0.95,
    dof: Optional[float] = None
) -> float:
    """
    Calculate coverage factor for given confidence level.
    
    Args:
        confidence_level: Desired confidence level (0 to 1)
        dof: Effective degrees of freedom
    
    Returns:
        Coverage factor k
    """
    if dof is None or dof == float('inf'):
        # Use normal distribution
        return stats.norm.ppf((1 + confidence_level) / 2)
    else:
        # Use t-distribution
        return stats.t.ppf((1 + confidence_level) / 2, dof)


def expanded_uncertainty(
    u_c: float,
    confidence_level: float = 0.95,
    dof: Optional[float] = None
) -> Tuple[float, float]:
    """
    Calculate expanded uncertainty.
    
    Args:
        u_c: Combined standard uncertainty
        confidence_level: Desired confidence level
        dof: Effective degrees of freedom
    
    Returns:
        (expanded_uncertainty, coverage_factor)
    """
    k = coverage_factor(confidence_level, dof)
    U = k * u_c
    return U, k


# ============================================================================
# UNCERTAINTY BUDGET CREATION
# ============================================================================

def create_uncertainty_budget(
    measurand: str,
    result: float,
    unit: str,
    components_data: List[Dict],
    sensitivity_coefficients: Optional[List[float]] = None,
    confidence_level: float = 0.95
) -> UncertaintyBudget:
    """
    Create complete uncertainty budget.
    
    Args:
        measurand: Name of measurand
        result: Measured value
        unit: Unit of measurement
        components_data: List of component dictionaries
        sensitivity_coefficients: Optional sensitivity coefficients
        confidence_level: Desired confidence level
    
    Returns:
        Complete uncertainty budget
    """
    # Create components
    components = []
    for data in components_data:
        dist = DistributionType(data.get('distribution', 'rectangular'))
        dof = data.get('dof', float('inf'))
        
        # Get divisor
        if dist == DistributionType.NORMAL:
            divisor = data.get('coverage', 2.0)
        else:
            divisor = get_distribution_divisor(dist, dof=dof)
        
        comp = UncertaintyComponent(
            name=data['name'],
            value=data['value'],
            unit=data.get('unit', unit),
            distribution=dist,
            divisor=divisor,
            dof=dof,
            uncertainty_type=data.get('type', 'B')
        )
        components.append(comp)
    
    # Combine uncertainties
    u_c, nu_eff = combine_uncertainties(components, sensitivity_coefficients)
    
    # Calculate expanded uncertainty
    U, k = expanded_uncertainty(u_c, confidence_level, nu_eff)
    
    return UncertaintyBudget(
        measurand=measurand,
        result=result,
        unit=unit,
        components=components,
        combined_uncertainty=u_c,
        effective_dof=nu_eff,
        coverage_factor=k,
        expanded_uncertainty=U,
        confidence_level=confidence_level
    )


# ============================================================================
# UNCERTAINTY REPORTING
# ============================================================================

def format_uncertainty_statement(
    result: float,
    u_c: float,
    U: float,
    k: float,
    unit: str,
    confidence_level: float = 0.95
) -> str:
    """
    Format uncertainty statement for reporting.
    
    Args:
        result: Measured value
        u_c: Combined uncertainty
        U: Expanded uncertainty
        k: Coverage factor
        unit: Unit of measurement
        confidence_level: Confidence level
    
    Returns:
        Formatted statement
    """
    conf_pct = confidence_level * 100
    
    statement = (
        f"Result: {result:.6g} ± {U:.6g} {unit}\n"
        f"The reported uncertainty is the expanded uncertainty with "
        f"coverage factor k = {k:.2f}, providing approximately "
        f"{conf_pct:.0f}% level of confidence."
    )
    
    return statement


def print_uncertainty_budget(budget: UncertaintyBudget) -> str:
    """
    Print formatted uncertainty budget table.
    
    Args:
        budget: Uncertainty budget
    
    Returns:
        Formatted table string
    """
    lines = []
    lines.append(f"Uncertainty Budget: {budget.measurand}")
    lines.append(f"Result: {budget.result} {budget.unit}")
    lines.append("")
    lines.append("Uncertainty Components:")
    lines.append("-" * 80)
    lines.append(f"{'Source':<20} {'Type':<6} {'Distribution':<12} {'u_i':<12} {'c_i':<6} {'c_i·u_i':<12}")
    lines.append("-" * 80)
    
    for comp in budget.components:
        u_i = comp.standard_uncertainty
        c_i = 1.0  # Default sensitivity coefficient
        contrib = c_i * u_i
        lines.append(
            f"{comp.name:<20} {comp.uncertainty_type:<6} "
            f"{comp.distribution.value:<12} {u_i:<12.4g} {c_i:<6.2f} {contrib:<12.4g}"
        )
    
    lines.append("-" * 80)
    lines.append(f"{'Combined (u_c)':<50} {budget.combined_uncertainty:.4g} {budget.unit}")
    lines.append(f"{'Effective DOF:':<50} {budget.effective_dof:.1f}")
    lines.append(f"{'Coverage factor (k=' + str(budget.confidence_level*100) + '%):':<50} {budget.coverage_factor:.3f}")
    lines.append(f"{'Expanded uncertainty (U):':<50} {budget.expanded_uncertainty:.4g} {budget.unit}")
    
    return "\n".join(lines)


# ============================================================================
# MAXWELL ARTICLE REFERENCES
# ============================================================================

def get_maxwell_measurement_articles() -> List[str]:
    """
    Get Maxwell article references for measurement uncertainty.
    
    Returns:
        List of article references
    """
    return ['Art. 287-300', 'Art. 343-348']


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Create uncertainty budget
    components_data = [
        {'name': 'Repeatability', 'value': 0.001, 'type': 'A', 'dof': 9},
        {'name': 'Calibration', 'value': 0.002, 'coverage': 2, 'distribution': 'normal'},
        {'name': 'Resolution', 'value': 0.001, 'distribution': 'rectangular'},
        {'name': 'Temperature', 'value': 0.0005, 'distribution': 'rectangular'},
    ]
    
    budget = create_uncertainty_budget(
        measurand="Resistance",
        result=1000.0,
        unit="statohm",
        components_data=components_data
    )
    
    print(print_uncertainty_budget(budget))
    print("")
    print(format_uncertainty_statement(
        budget.result,
        budget.combined_uncertainty,
        budget.expanded_uncertainty,
        budget.coverage_factor,
        budget.unit,
        budget.confidence_level
    ))
```

---

## Usage Examples

```python
from uncertainty_analysis_utils import *

# Example 1: Type A evaluation
observations = [100.1, 100.2, 100.1, 100.3, 100.2]
mean, u_A, dof = type_a_uncertainty(observations)
print(f"Mean: {mean}, u_A: {u_A}, DOF: {dof}")

# Example 2: Type B from calibration
u_cal = type_b_from_calibration(0.01, 2.0)
print(f"Standard uncertainty from calibration: {u_cal}")

# Example 3: Complete budget
components = [
    {'name': 'Repeatability', 'value': 0.001, 'type': 'A', 'dof': 9},
    {'name': 'Calibration', 'value': 0.002, 'coverage': 2},
]
budget = create_uncertainty_budget("Voltage", 100.0, "statvolt", components)
print(print_uncertainty_budget(budget))
```

---

## Quality Criteria

- [ ] GUM methodology followed
- [ ] All distribution types supported
- [ ] Welch-Satterthwaite formula implemented
- [ ] Coverage factors from t-distribution
- [ ] Complete budget creation supported
