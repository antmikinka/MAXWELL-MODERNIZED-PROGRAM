# Task: divergence-flux-analysis

## Description

Compute the divergence of vector fields and analyze flux through surfaces. This implements Maxwell's conception of flux as fundamental to understanding electric and magnetic fields (Articles 20-22, 77-78).

## Workflow Steps

### 1. Vector Field Input
- Vector field definition
- Coordinate system
- Source/sink identification

### 2. Divergence Computation
- Apply divergence operator
- Identify regions with non-zero divergence
- Relate to charge/current density

### 3. Flux Calculation
- Define surface for flux integration
- Compute surface integral of normal component
- Verify divergence theorem

### 4. Physical Interpretation
- Relate divergence to sources (Gauss's law)
- Identify solenoidal regions (∇·B = 0)
- Generate physical insights

## Requirements

**Input:**
- `vector_field`: VectorField object (E, B, J, etc.)
- `surface`: Surface definition for flux
- `volume`: Volume for divergence theorem verification
- `coordinate_system`: Coordinate system specification

**Output:**
- `divergence_field`: ScalarField of ∇·F
- `flux_result`: Flux through specified surface
- `theorem_verification`: Divergence theorem check
- `source_analysis`: Location and strength of sources

## Implementation

```python
from maxwell.core.vector import VectorField
from maxwell.core.surface import Surface
from maxwell.mathematics import vector_calculus, integration

def analyze_divergence_and_flux(
    vector_field,
    surface=None,
    volume=None,
    coordinate_system='cartesian'
):
    """
    Compute divergence and analyze flux.
    
    Maxwell Articles: 20-22, 77-78
    ∇·E = 4πρ (Gauss's law in CGS)
    ∇·B = 0 (no magnetic monopoles)
    """
    # Compute divergence
    divergence = vector_calculus.divergence(
        vector_field,
        coords=coordinate_system
    )
    
    # Compute flux through surface if provided
    flux = None
    if surface is not None:
        flux = integration.surface_integral(
            integrand=vector_field.dot(surface.normal),
            surface=surface
        )
    
    # Verify divergence theorem
    theorem verified
    if volume is not None:
        volume_integral = integration.volume_integral(
            divergence,
            volume=volume
        )
        surface_integral = integration.surface_integral(
            vector_field.dot(volume.boundary.normal),
            surface=volume.boundary
        )
        theorem_error = abs(volume_integral - surface_integral)
    
    return {
        'divergence': divergence,
        'flux': flux,
        'theorem_verified': theorem_error < tolerance,
        'theorem_error': theorem_error
    }
```

## Validation

- Divergence theorem verification
- Gauss's law for known charge distributions
- Solenoidal field verification (∇·B = 0)

## Maxwell Article References

| Article | Content |
|---------|---------|
| 20-22 | Flux and divergence |
| 77-78 | Divergence theorem |
| 79-81 | Gauss's law for electricity |
