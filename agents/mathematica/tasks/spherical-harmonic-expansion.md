# Task: spherical-harmonic-expansion

## Description

Expand functions and potentials in spherical harmonics for solving boundary value problems with spherical symmetry. This implements Maxwell's spherical harmonic analysis (Articles 125-133).

## Workflow Steps

### 1. Function Definition
- Define function on sphere surface
- Specify angular domain
- Identify symmetry properties

### 2. Harmonic Computation
- Compute Legendre polynomials
- Generate associated Legendre functions
- Build spherical harmonics Y_l^m

### 3. Expansion Coefficients
- Compute expansion coefficients via integration
- Apply orthogonality relations
- Truncate at appropriate order

### 4. Series Reconstruction
- Reconstruct function from harmonics
- Assess convergence
- Error analysis

## Requirements

**Input:**
- `function`: Callable f(θ, φ) defined on sphere
- `max_order`: Maximum l value for expansion
- `quadrature_order`: Integration precision
- `symmetry`: Symmetry properties (optional)

**Output:**
- `coefficients`: Expansion coefficients a_lm
- `reconstruction`: Reconstructed function
- `convergence_analysis`: Error vs. order
- `multipole_moments`: Physical interpretation

## Implementation

```python
from maxwell.mathematics.harmonics import SphericalHarmonics
from maxwell.mathematics import integration
import numpy as np

def expand_in_spherical_harmonics(
    function,
    max_order=10,
    quadrature_order=64
):
    """
    Expand function in spherical harmonics.
    
    Maxwell Articles: 125-133
    f(θ,φ) = Σ(l=0 to ∞) Σ(m=-l to l) a_lm Y_l^m(θ,φ)
    """
    sh = SphericalHarmonics()
    coefficients = {}
    
    # Compute expansion coefficients
    for l in range(max_order + 1):
        for m in range(-l, l + 1):
            # a_lm = ∫ f(θ,φ) Y_l^m*(θ,φ) dΩ
            def integrand(theta, phi):
                Y_lm = sh.spherical_harmonic(l, m, theta, phi)
                return function(theta, phi) * np.conj(Y_lm) * np.sin(theta)
            
            a_lm = integration.spherical_integral(
                integrand,
                quadrature_order=quadrature_order
            )
            coefficients[(l, m)] = a_lm
    
    # Create reconstruction function
    def reconstruct(theta, phi, use_orders=None):
        max_l = use_orders if use_orders else max_order
        result = 0
        for l in range(max_l + 1):
            for m in range(-l, l + 1):
                Y_lm = sh.spherical_harmonic(l, m, theta, phi)
                result += coefficients[(l, m)] * Y_lm
        return result
    
    # Convergence analysis
    convergence = analyze_convergence(function, reconstruct, max_order)
    
    return {
        'coefficients': coefficients,
        'reconstruct': reconstruct,
        'convergence': convergence,
        'multipole_moments': interpret_multipoles(coefficients)
    }
```

## Validation

- Orthogonality verification
- Known expansion comparison (e.g., point charge potential)
- Convergence rate analysis

## Maxwell Article References

| Article | Content |
|---------|---------|
| 125-133 | Spherical harmonic theory |
| 140-145 | Electrostatic applications |
| 543-555 | Magnetic applications |
