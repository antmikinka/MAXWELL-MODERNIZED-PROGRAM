# Template: Field Implementation

## Purpose

Standardized template for implementing electromagnetic field modules. This template ensures consistency across all field implementations and maintains traceability to Maxwell's original articles.

## Source Category

**CRITICAL: Theory Preservation**

This template is for:
- **Maxwell's 1873 Historical Text**: Field implementations from Articles across Parts I-IV
- **Standard Mathematical Implementation**: Vector field computations
- **User Original Theory**: Mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Template Structure

### 1. Module Header

```python
"""
{FIELD_NAME} Field Implementation

Maxwell Treatise Reference:
- Primary Articles: {ARTICLE_NUMBERS}
- Part: {PART_NUMBER}

Source Category:
- Maxwell 1873: Articles {X-Y}
- Standard Math: {operations}
- User Theory: {NONE or specify}

CGS Units: {UNIT_SPECIFICATIONS}
"""

import numpy as np
from typing import Union, Optional, Tuple
from maxwell.core.vector import VectorField, ScalarField
from maxwell.core.units import CGS_UNITS
from maxwell.utils.citation import maxwell_citation
```

### 2. Field Class Definition

```python
class {FieldName}:
    """
    {FIELD_DESCRIPTION}
    
    Maxwell Articles: {ARTICLE_NUMBERS}
    
    Attributes:
        source: Source of the field (charge, current, etc.)
        coordinate_system: 'cartesian', 'cylindrical', 'spherical'
        citations: List of Maxwell article references
    
    CGS Units:
        Field: {UNIT}
        Potential: {UNIT}
    """
    
    def __init__(
        self,
        source: {SOURCE_TYPE},
        coordinate_system: str = 'cartesian',
        citations: Optional[list] = None
    ):
        self.source = source
        self.coordinate_system = coordinate_system
        self.citations = citations or self._default_citations()
    
    @staticmethod
    def _default_citations() -> list:
        """Return default Maxwell article citations."""
        return [
            maxwell_citation(article={N}, part={I}),
            # Add more as needed
        ]
```

### 3. Field Computation Methods

```python
    def field_at(self, observation_point: np.ndarray) -> VectorField:
        """
        Compute field at observation point.
        
        Args:
            observation_point: Position vector (cm)
        
        Returns:
            VectorField: Field value ({UNIT})
        
        Maxwell Reference: Art. {N}
        
        Formula:
            {FORMULA}
        
        Example:
            >>> field = {FieldName}.from_source(source)
            >>> E = field.field_at([1, 0, 0])
            >>> print(E.magnitude)  # {UNIT}
        """
        r = np.asarray(observation_point)
        # Implementation here
        pass
    
    def potential_at(self, observation_point: np.ndarray) -> ScalarField:
        """
        Compute potential at observation point.
        
        Args:
            observation_point: Position vector (cm)
        
        Returns:
            ScalarField: Potential value ({UNIT})
        
        Maxwell Reference: Art. {N}
        """
        pass
```

### 4. Derived Quantities

```python
    def energy_density(self) -> ScalarField:
        """
        Compute energy density of field.
        
        Returns:
            ScalarField: Energy density (erg/cm³)
        
        Maxwell Reference: Arts. {630-638}
        
        Formula:
            u = {FORMULA}
        """
        pass
    
    def stress_tensor(self) -> np.ndarray:
        """
        Compute Maxwell stress tensor.
        
        Returns:
            ndarray: 3x3 stress tensor (dyne/cm²)
        
        Maxwell Reference: Arts. {103-110}
        """
        pass
```

### 5. Validation Methods

```python
    def verify_field_equations(self, test_points: np.ndarray) -> dict:
        """
        Verify field satisfies Maxwell equations.
        
        Args:
            test_points: Array of test positions
        
        Returns:
            dict: Validation results with residuals
        
        Checks:
            - ∇ · E = 4πρ (Gauss)
            - ∇ × E = 0 (electrostatics)
            - Unit consistency
        """
        results = {
            'divergence_residual': self._check_divergence(test_points),
            'curl_residual': self._check_curl(test_points),
            'unit_consistency': self._check_units()
        }
        return results
    
    def verify_analytical_limit(self) -> bool:
        """
        Verify field matches known analytical solutions.
        
        Returns:
            bool: True if validation passes
        """
        pass
```

### 6. Factory Methods

```python
    @classmethod
    def from_point_source(cls, charge: float, position: np.ndarray):
        """
        Create field from point source.
        
        Args:
            charge: Source strength ({UNIT})
            position: Source position (cm)
        
        Returns:
            {FieldName}: Field object
        
        Maxwell Reference: Art. {N}
        """
        source = PointSource(charge=charge, position=position)
        return cls(source)
    
    @classmethod
    def from_distribution(cls, distribution: {DIST_TYPE}):
        """
        Create field from continuous distribution.
        
        Args:
            distribution: Charge/current distribution
        
        Returns:
            {FieldName}: Field object
        
        Maxwell Reference: Arts. {64-68}
        """
        return cls(source=distribution)
```

### 7. Visualization Methods

```python
    def plot_field_lines(
        self,
        seed_points: np.ndarray,
        max_length: float = 10.0,
        **kwargs
    ):
        """
        Plot field lines.
        
        Args:
            seed_points: Starting points for field lines
            max_length: Maximum field line length
            **kwargs: Passed to plotting routine
        """
        pass
    
    def plot_magnitude_slice(
        self,
        plane: str = 'xz',
        bounds: Tuple = (-5, 5),
        **kwargs
    ):
        """
        Plot field magnitude on slice plane.
        
        Args:
            plane: Slice plane ('xy', 'yz', 'xz')
            bounds: Plot bounds
            **kwargs: Passed to plotting routine
        """
        pass
```

### 8. Theory Preservation Decorator

```python
def preserve_theory(theory_type: str):
    """
    Decorator to mark theory source and prevent alteration.
    
    Args:
        theory_type: 'maxwell', 'user_authoritative', 'standard_math'
    
    Usage:
        @preserve_theory('user_authoritative')
        def user_theory_extension(self, ...):
            # DO NOT ALTER - authoritative user theory
            pass
    """
    def decorator(func):
        func._theory_source = theory_type
        func._protected = theory_type == 'user_authoritative'
        return func
    return decorator
```

## Template Usage Example

```python
"""
Electric Field Implementation

Maxwell Treatise Reference:
- Primary Articles: 44-49, 66-68
- Part: Part I (Electrostatics)

Source Category:
- Maxwell 1873: Articles 44-49 (field definition), 66-68 (Coulomb's law)
- Standard Math: Vector operations, gradient
- User Theory: NONE
"""

class ElectricField({FieldName}):
    """
    Electrostatic field implementation.
    
    Maxwell Articles: 44-49, 66-68, 75-76
    
    CGS Units:
        Field: statvolt/cm
        Charge: statcoulomb
    """
    
    @preserve_theory('maxwell')
    def field_from_point_charge(self, q, r):
        """
        Coulomb's law field.
        
        Maxwell Reference: Arts. 66-68
        
        E = q/r² r̂
        """
        # Implementation - DO NOT ALTER Maxwell's formula
        pass
```

## Checklist for Implementation

- [ ] Module header with article citations
- [ ] CGS units specified
- [ ] Source category documented
- [ ] Field computation methods implemented
- [ ] Validation methods included
- [ ] Theory preservation decorators applied
- [ ] Maxwell article citations in docstrings
- [ ] Examples with CGS units
- [ ] Visualization methods provided

## Related Templates

- `potential-solver.md` - Scalar potential implementation
- `constitutive-relation.md` - Material response
- `wave-propagation.md` - Time-dependent fields
- `analytical-solution.md` - Benchmark solutions
