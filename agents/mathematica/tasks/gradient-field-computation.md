# Task: gradient-field-computation

## Description

Compute the gradient of scalar potential fields to derive vector field quantities. This is fundamental for obtaining electric fields from electric potentials (E = -∇φ) and is used throughout Maxwell's electrostatics.

## Workflow Steps

### 1. Input Specification
- Scalar field definition (analytical or numerical grid)
- Coordinate system specification
- Evaluation points or grid
- Citation metadata (Maxwell article references)

### 2. Gradient Computation
- Select appropriate coordinate system formula
- Apply gradient operator
- Handle boundary conditions if numerical

### 3. Output Generation
- Vector field object
- Citation decorator with article references
- Validation status

## Requirements

**Input:**
- `scalar_field`: ScalarField object or callable
- `coordinate_system`: 'cartesian', 'cylindrical', or 'spherical'
- `evaluation_grid`: NumPy array or grid specification
- `citations`: List of relevant Maxwell article numbers

**Output:**
- `vector_field`: VectorField object representing ∇φ
- `metadata`: Computation details and citations
- `validation`: Verification results

## Implementation

```python
from maxwell.core.scalar import ScalarField
from maxwell.core.vector import VectorField
from maxwell.mathematics import vector_calculus

def compute_gradient_field(
    scalar_field,
    coordinate_system='cartesian',
    evaluation_grid=None,
    citations=None
):
    """
    Compute gradient of scalar field.
    
    Maxwell Articles: 15-18, 23-27
    E = -∇φ (electric field from potential)
    """
    # Compute gradient
    gradient = vector_calculus.gradient(
        scalar_field,
        coords=coordinate_system
    )
    
    # Create vector field with citations
    vector_field = VectorField(
        components=gradient,
        citations=citations or [],
        derived_from='gradient',
        source_field=scalar_field
    )
    
    return vector_field
```

## Validation

- Verify curl of gradient is zero: ∇×(∇φ) = 0
- Compare with analytical gradient for test functions
- Check numerical accuracy on grid

## Related Templates

- `field-derivation-template` - Document the derivation
- `citation-template` - Link to Maxwell articles

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector quantities |
| 23-27 | Gradient and potential |
| 59-61 | Electric field from potential |
