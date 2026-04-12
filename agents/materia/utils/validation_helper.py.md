# Utility: validation_helper

## Purpose

Validation helper utilities for materials science computations including physics validation, unit consistency checks, and Maxwell article traceability.

## Location

`agents/materia/utils/validation_helper.py`

---

## Module Contents

```python
"""
MATERIA Validation Helper

Validation utilities for materials science computations in the Maxwell Treatise Modernization Project.

Provides:
- Physics validation (bounds, consistency)
- CGS unit consistency checks
- Maxwell article traceability validation
- Data quality assessment

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np


class ValidationLevel(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    level: ValidationLevel
    message: str
    category: str
    details: Optional[Dict] = None
    
    def __str__(self) -> str:
        status = "✓" if self.passed else "✗"
        return f"[{status}] {self.category}: {self.message}"


@dataclass
class ValidationReport:
    """Complete validation report."""
    material_name: str
    total_checks: int
    passed_checks: int
    warnings: int
    errors: int
    critical: int
    results: List[ValidationResult]
    overall_status: str  # "PASS", "CONDITIONAL", "FAIL"
    maxwell_articles: List[str]
    
    @property
    def pass_rate(self) -> float:
        return self.passed_checks / self.total_checks if self.total_checks > 0 else 0
    
    def summary(self) -> str:
        return (
            f"Validation Report: {self.material_name}\n"
            f"  Status: {self.overall_status}\n"
            f"  Passed: {self.passed_checks}/{self.total_checks} ({self.pass_rate*100:.1f}%)\n"
            f"  Warnings: {self.warnings}\n"
            f"  Errors: {self.errors}\n"
            f"  Critical: {self.critical}"
        )


# ============================================================================
# DIELECTRIC VALIDATION
# ============================================================================

def validate_dielectric_properties(
    K: float,
    tan_delta: float,
    breakdown_strength: float,
    resistivity: float,
    temperature: float
) -> List[ValidationResult]:
    """
    Validate dielectric material properties.
    
    Args:
        K: Dielectric constant (dimensionless, CGS)
        tan_delta: Loss tangent
        breakdown_strength: statvolt/cm
        resistivity: statohm·cm
        temperature: K
    
    Returns:
        List of validation results
    """
    results = []
    
    # K validation
    if K < 1:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Dielectric constant K={K} < 1 is unphysical for passive materials",
            category="dielectric_constant"
        ))
    elif K > 1e6:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Dielectric constant K={K} is unusually high",
            category="dielectric_constant"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"K={K} is within normal range",
            category="dielectric_constant"
        ))
    
    # Loss tangent validation
    if tan_delta < 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Loss tangent tanδ={tan_delta} < 0 is unphysical",
            category="loss_tangent"
        ))
    elif tan_delta > 1:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Loss tangent tanδ={tan_delta} > 1 indicates very lossy material",
            category="loss_tangent"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"tanδ={tan_delta} is within normal range",
            category="loss_tangent"
        ))
    
    # Breakdown strength validation
    if breakdown_strength <= 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.CRITICAL,
            message=f"Breakdown strength={breakdown_strength} must be positive",
            category="breakdown_strength"
        ))
    elif breakdown_strength > 1e6:  # statvolt/cm
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Breakdown strength={breakdown_strength} statvolt/cm is unusually high",
            category="breakdown_strength"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Breakdown strength={breakdown_strength} statvolt/cm is reasonable",
            category="breakdown_strength"
        ))
    
    # Resistivity validation
    if resistivity <= 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Resistivity={resistivity} must be positive",
            category="resistivity"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Resistivity={resistivity} statohm·cm is valid",
            category="resistivity"
        ))
    
    # Temperature validation
    if temperature <= 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.CRITICAL,
            message=f"Temperature={temperature} K is unphysical",
            category="temperature"
        ))
    elif temperature > 5000:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Temperature={temperature} K is extremely high",
            category="temperature"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Temperature={temperature} K is valid",
            category="temperature"
        ))
    
    return results


# ============================================================================
# MAGNETIC VALIDATION
# ============================================================================

def validate_magnetic_properties(
    mu: float,
    H_c: float,
    B_r: float,
    B_sat: float,
    hysteresis_loss: float
) -> List[ValidationResult]:
    """
    Validate magnetic material properties.
    
    Args:
        mu: Permeability (dimensionless, CGS)
        H_c: Coercivity (oersted)
        B_r: Remanence (gauss)
        B_sat: Saturation flux density (gauss)
        hysteresis_loss: erg/cm³·cycle
    
    Returns:
        List of validation results
    """
    results = []
    
    # Permeability validation
    if mu < 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.CRITICAL,
            message=f"Permeability μ={mu} < 0 is unphysical",
            category="permeability"
        ))
    elif mu < 1:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.INFO,
            message=f"Permeability μ={mu} < 1 indicates diamagnetic material",
            category="permeability"
        ))
    elif mu > 1e7:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Permeability μ={mu} is extremely high",
            category="permeability"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"μ={mu} is valid",
            category="permeability"
        ))
    
    # Coercivity validation
    if H_c < 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Coercivity H_c={H_c} < 0 is unphysical",
            category="coercivity"
        ))
    elif H_c > 1e6:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Coercivity H_c={H_c} oersted is extremely high",
            category="coercivity"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"H_c={H_c} oersted is valid",
            category="coercivity"
        ))
    
    # Remanence validation
    if B_r < 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Remanence B_r={B_r} < 0 is unphysical",
            category="remanence"
        ))
    elif B_r > B_sat:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Remanence B_r={B_r} > B_sat={B_sat} is unphysical",
            category="remanence"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"B_r={B_r} gauss is valid",
            category="remanence"
        ))
    
    # Saturation validation
    if B_sat <= 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.CRITICAL,
            message=f"Saturation B_sat={B_sat} must be positive",
            category="saturation"
        ))
    elif B_sat > 1e6:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Saturation B_sat={B_sat} gauss is extremely high",
            category="saturation"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"B_sat={B_sat} gauss is valid",
            category="saturation"
        ))
    
    # Hysteresis loss validation
    if hysteresis_loss < 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message=f"Hysteresis loss={hysteresis_loss} < 0 is unphysical",
            category="hysteresis_loss"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Hysteresis loss={hysteresis_loss} erg/cm³·cycle is valid",
            category="hysteresis_loss"
        ))
    
    return results


# ============================================================================
# CGS UNIT CONSISTENCY
# ============================================================================

def validate_cgs_units(properties: Dict[str, Any]) -> List[ValidationResult]:
    """
    Validate CGS unit consistency in property dictionary.
    
    Args:
        properties: Dictionary of material properties
    
    Returns:
        List of validation results
    """
    results = []
    
    # Expected CGS units for each property
    expected_units = {
        'K': ('dimensionless', None),
        'mu': ('dimensionless', None),
        'H_c': ('oersted', (0, 1e7)),
        'B_r': ('gauss', (0, 1e7)),
        'B_sat': ('gauss', (0, 1e7)),
        'breakdown_strength': ('statvolt/cm', (0, 1e7)),
        'resistivity': ('statohm·cm', (0, None)),
        'conductivity': ('s⁻¹', (0, None)),
        'E_field': ('statvolt/cm', (-1e7, 1e7)),
        'current_density': ('statampere/cm²', (-1e15, 1e15)),
        'energy_density': ('erg/cm³', (0, 1e15)),
        'concentration': ('mol/cm³', (0, 1)),
        'mobility': ('cm²/statvolt·s', (0, 1)),
        'diffusion': ('cm²/s', (1e-12, 1e-2)),
    }
    
    for prop_name, (unit, bounds) in expected_units.items():
        if prop_name not in properties:
            continue
        
        value = properties[prop_name]
        
        # Check if value is numeric
        if not isinstance(value, (int, float, np.number)):
            results.append(ValidationResult(
                passed=False,
                level=ValidationLevel.ERROR,
                message=f"{prop_name} is not numeric: {type(value)}",
                category="unit_validation"
            ))
            continue
        
        # Check bounds
        if bounds:
            min_val, max_val = bounds
            if min_val is not None and value < min_val:
                results.append(ValidationResult(
                    passed=False,
                    level=ValidationLevel.ERROR,
                    message=f"{prop_name}={value} below minimum {min_val} {unit}",
                    category="unit_validation"
                ))
            elif max_val is not None and value > max_val:
                results.append(ValidationResult(
                    passed=False,
                    level=ValidationLevel.WARNING,
                    message=f"{prop_name}={value} exceeds typical maximum {max_val} {unit}",
                    category="unit_validation"
                ))
            else:
                results.append(ValidationResult(
                    passed=True,
                    level=ValidationLevel.INFO,
                    message=f"{prop_name}={value} {unit} is within bounds",
                    category="unit_validation"
                ))
    
    return results


# ============================================================================
# MAXWELL ARTICLE TRACEABILITY
# ============================================================================

MAXWELL_ARTICLE_RANGES = {
    'electrostatics': (1, 229),
    'electrokinematics': (230, 370),
    'magnetism': (371, 474),
    'electromagnetism': (475, 866),
}

MATERIAL_ARTICLE_MAPPING = {
    'dielectric': ['50-62', '79-83', '103-111', '60-62'],
    'magnetic': ['424-448', '444-447', '371-400'],
    'electrolytic': ['236-238', '269-286', '230-235'],
    'conductive': ['287-300', '301-320'],
    'composite': ['314', '103-111'],
}


def validate_maxwell_articles(
    material_type: str,
    cited_articles: List[str]
) -> List[ValidationResult]:
    """
    Validate Maxwell article citations for material type.
    
    Args:
        material_type: Type of material
        cited_articles: List of cited article ranges
    
    Returns:
        List of validation results
    """
    results = []
    
    # Get expected articles for this material type
    expected = MATERIAL_ARTICLE_MAPPING.get(material_type, [])
    
    if not expected:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.WARNING,
            message=f"Unknown material type: {material_type}",
            category="maxwell_traceability"
        ))
        return results
    
    # Check for missing primary articles
    for article in expected:
        if not any(article in cited for cited in cited_articles):
            results.append(ValidationResult(
                passed=False,
                level=ValidationLevel.WARNING,
                message=f"Missing expected article: Art. {article}",
                category="maxwell_traceability",
                details={'expected': article}
            ))
    
    # Validate cited article format
    for article in cited_articles:
        if not validate_article_format(article):
            results.append(ValidationResult(
                passed=False,
                level=ValidationLevel.WARNING,
                message=f"Invalid article format: {article}",
                category="maxwell_traceability"
            ))
        else:
            results.append(ValidationResult(
                passed=True,
                level=ValidationLevel.INFO,
                message=f"Article {article} format valid",
                category="maxwell_traceability"
            ))
    
    # Check coverage
    if len(cited_articles) == 0:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.ERROR,
            message="No Maxwell articles cited",
            category="maxwell_traceability"
        ))
    
    return results


def validate_article_format(article: str) -> bool:
    """
    Validate Maxwell article citation format.
    
    Args:
        article: Article citation string
    
    Returns:
        True if format is valid
    """
    import re
    
    # Valid formats: "Art. 123", "Art. 123-456", "123", "123-456"
    patterns = [
        r'^Art\.\s*\d+$',
        r'^Art\.\s*\d+\s*-\s*\d+$',
        r'^\d+$',
        r'^\d+\s*-\s*\d+$',
    ]
    
    for pattern in patterns:
        if re.match(pattern, article.strip()):
            return True
    
    return False


# ============================================================================
# COMPOSITE VALIDATION
# ============================================================================

def validate_composite_properties(
    matrix_properties: Dict,
    inclusion_properties: Dict,
    volume_fraction: float
) -> List[ValidationResult]:
    """
    Validate composite material properties.
    
    Args:
        matrix_properties: Matrix phase properties
        inclusion_properties: Inclusion phase properties
        volume_fraction: Inclusion volume fraction
    
    Returns:
        List of validation results
    """
    results = []
    
    # Volume fraction validation
    if volume_fraction < 0 or volume_fraction > 1:
        results.append(ValidationResult(
            passed=False,
            level=ValidationLevel.CRITICAL,
            message=f"Volume fraction={volume_fraction} must be in [0, 1]",
            category="composite"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            level=ValidationLevel.INFO,
            message=f"Volume fraction={volume_fraction} is valid",
            category="composite"
        ))
    
    # Check that both phases have required properties
    required = ['K', 'mu'] if 'K' in matrix_properties else []
    
    for phase_name, props in [('matrix', matrix_properties), 
                               ('inclusion', inclusion_properties)]:
        for prop in required:
            if prop not in props:
                results.append(ValidationResult(
                    passed=False,
                    level=ValidationLevel.ERROR,
                    message=f"{phase_name} missing required property: {prop}",
                    category="composite"
                ))
    
    return results


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_validation_report(
    material_name: str,
    material_type: str,
    properties: Dict,
    cited_articles: List[str]
) -> ValidationReport:
    """
    Generate comprehensive validation report.
    
    Args:
        material_name: Name of material
        material_type: Type classification
        properties: Property dictionary
        cited_articles: Maxwell article citations
    
    Returns:
        Complete validation report
    """
    all_results = []
    
    # Dielectric validation
    if material_type == 'dielectric':
        all_results.extend(validate_dielectric_properties(
            K=properties.get('K', 1),
            tan_delta=properties.get('tan_delta', 0),
            breakdown_strength=properties.get('breakdown_strength', 0),
            resistivity=properties.get('resistivity', 0),
            temperature=properties.get('temperature', 293)
        ))
    
    # Magnetic validation
    if material_type == 'magnetic':
        all_results.extend(validate_magnetic_properties(
            mu=properties.get('mu', 1),
            H_c=properties.get('H_c', 0),
            B_r=properties.get('B_r', 0),
            B_sat=properties.get('B_sat', 0),
            hysteresis_loss=properties.get('hysteresis_loss', 0)
        ))
    
    # CGS unit validation
    all_results.extend(validate_cgs_units(properties))
    
    # Maxwell article validation
    all_results.extend(validate_maxwell_articles(material_type, cited_articles))
    
    # Count results
    passed = sum(1 for r in all_results if r.passed)
    warnings = sum(1 for r in all_results if r.level == ValidationLevel.WARNING)
    errors = sum(1 for r in all_results if r.level == ValidationLevel.ERROR)
    critical = sum(1 for r in all_results if r.level == ValidationLevel.CRITICAL)
    
    # Determine overall status
    if critical > 0:
        status = "FAIL"
    elif errors > 0:
        status = "FAIL"
    elif warnings > 3:
        status = "CONDITIONAL"
    elif passed >= len(all_results) * 0.8:
        status = "PASS"
    else:
        status = "CONDITIONAL"
    
    return ValidationReport(
        material_name=material_name,
        total_checks=len(all_results),
        passed_checks=passed,
        warnings=warnings,
        errors=errors,
        critical=critical,
        results=all_results,
        overall_status=status,
        maxwell_articles=cited_articles
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example validation
    properties = {
        'K': 7.0,
        'tan_delta': 0.0002,
        'breakdown_strength': 2000,
        'resistivity': 1e15,
        'temperature': 293,
    }
    
    report = generate_validation_report(
        material_name="Muscovite Mica",
        material_type="dielectric",
        properties=properties,
        cited_articles=['Art. 50-62', 'Art. 79-83', 'Art. 103-111']
    )
    
    print(report.summary())
    print("\nDetailed Results:")
    for result in report.results:
        print(f"  {result}")
```

---

## Usage Examples

```python
from validation_helper import *

# Example 1: Validate dielectric properties
results = validate_dielectric_properties(
    K=7.0,
    tan_delta=0.0002,
    breakdown_strength=2000,
    resistivity=1e15,
    temperature=293
)

for r in results:
    print(r)

# Example 2: Generate full validation report
report = generate_validation_report(
    material_name="Muscovite Mica",
    material_type="dielectric",
    properties={'K': 7.0, 'tan_delta': 0.0002},
    cited_articles=['Art. 50-62', 'Art. 79-83']
)

print(report.summary())

# Example 3: Validate Maxwell article citations
article_results = validate_maxwell_articles(
    material_type="magnetic",
    cited_articles=['Art. 424-448', 'Art. 444-447']
)
```

---

## Quality Criteria

- [ ] All validations in CGS units
- [ ] Maxwell article traceability enforced
- [ ] Physics bounds checking
- [ ] Comprehensive error reporting
- [ ] Documentation complete
