# Task: curl-circulation-computation

## Description

Compute the curl of vector fields and analyze circulation. This implements Maxwell's theory of rotational field properties and electromagnetic induction (Articles 23-27, 591-600).

## Workflow Steps

### 1. Vector Field Input
- Vector field definition (E, B, A, etc.)
- Coordinate system specification
- Region of interest

### 2. Curl Computation
- Apply curl operator
- Identify rotational components
- Physical interpretation

### 3. Circulation Analysis
- Define closed path for circulation
- Compute line integral
- Verify Stokes' theorem

### 4. Electromagnetic Applications
- ∇×E = -(1/c)∂B/∂t (Faraday's law)
- ∇×B = (4π/c)J + (1/c)∂E/∂t (Ampère-Maxwell law)
- Vector potential: B = ∇×A

## Requirements

**Input:**
- `vector_field`: VectorField object
- `closed_path`: Path for circulation calculation
- `surface`: Surface bounded by path (for Stokes)
- `coordinate_system`: Coordinate system

**Output:**
- `curl_field`: VectorField of ∇×F
- `circulation`: Line integral around closed path
- `stokes_verification`: Stokes' theorem check
- `physical_interpretation`: Meaning of curl in context

## Implementation

```python
from maxwell.core.vector import VectorField
from maxwell.core.path import ClosedPath
from maxwell.mathematics import vector_calculus, line_integration

def compute_curl_and_circulation(
    vector_field,
    closed_path=None,
    surface=None,
    coordinate_system='cartesian'
):
    """
    Compute curl and analyze circulation.
    
    Maxwell Articles: 23-27, 591-600
    ∇×E = -(1/c)∂B/∂t (Faraday's law)
    ∇×B = (4π/c)J (Ampère's law)
    """
    # Compute curl
    curl = vector_calculus.curl(
        vector_field,
        coords=coordinate_system
    )
    
    # Compute circulation if path provided
    circulation = None
    if closed_path is not None:
        circulation = line_integration.integrate(
            vector_field.dot(closed_path.tangent),
            path=closed_path
        )
    
    # Verify Stokes' theorem if surface provided
    stokes_verified = False
    stokes_error = None
    if surface is not None and closed_path is not None:
        surface_integral = integration.surface_integral(
            curl.dot(surface.normal),
            surface=surface
        )
        stokes_error = abs(circulation - surface_integral)
        stokes_verified = stokes_error < tolerance
    
    return {
        'curl': curl,
        'circulation': circulation,
        'stokes_verified': stokes_verified,
        'stokes_error': stokes_error
    }
```

## Validation

- Curl of gradient is zero: ∇×(∇φ) = 0
- Stokes' theorem verification
- Faraday's law for time-varying fields

## Maxwell Article References

| Article | Content |
|---------|---------|
| 23-27 | Curl and rotation |
| 591-600 | Electromagnetic induction |
| 601-610 | Vector potential and curl |
