# Command: spherical-harmonics

## Description

Implements spherical harmonic functions essential for solving boundary value problems with spherical symmetry. Maxwell extensively used spherical harmonics in his treatment of electrostatics and magnetism (Articles 125-133, 543-555).

## Functionality

### Spherical Harmonic Types

1. **Zonal Harmonics** (m = 0)
   - Legendre polynomials P_n(cos θ)
   - Axial symmetry
   - Used for: Potential of ring charges, magnetic shells

2. **Tesseral Harmonics** (0 < m < n)
   - Associated Legendre functions P_n^m(cos θ)
   - Partial azimuthal dependence
   - Used for: Perturbed spherical problems

3. **Sectorial Harmonics** (m = n)
   - Maximum azimuthal variation
   - Used for: Rotating systems

4. **Full Spherical Harmonics** Y_l^m(θ, φ)
   - Complete angular basis
   - Orthogonality properties
   - Used for: General expansion of angular functions

### Operations

- `legendre(n, x)` - Legendre polynomial P_n(x)
- `legendre_associated(n, m, x)` - P_n^m(x)
- `spherical_harmonic(l, m, theta, phi)` - Y_l^m(θ, φ)
- `expand_function(f, max_order)` - Spherical harmonic expansion
- `addition_theorem(l, gamma)` - Legendre addition theorem

### Integral Properties

- Orthogonality relations
- Gaunt coefficients
- Clebsch-Gordan coefficients (optional)

## Usage

```python
from maxwell.mathematics.harmonics import SphericalHarmonics
import numpy as np

sh = SphericalHarmonics()

# Compute Legendre polynomial P_3(x)
P3 = sh.legendre(3, x=np.linspace(-1, 1, 100))

# Compute associated Legendre P_4^2(x)
P42 = sh.legendre_associated(4, 2, x=0.5)

# Compute spherical harmonic Y_2^1(θ, φ)
Y21 = sh.spherical_harmonic(l=2, m=1, theta=np.pi/4, phi=np.pi/3)

# Generate complete harmonic table for l=0 to 4
harmonic_table = sh.generate_table(max_l=4)

# Expand a function in spherical harmonics
# Example: potential on sphere surface
def surface_potential(theta, phi):
    return np.cos(theta) * np.sin(2*phi)

expansion = sh.expand_function(surface_potential, max_order=6)
print(f"Expansion coefficients: {expansion.coefficients}")

# Addition theorem: P_l(cos γ) in terms of angles
gamma = np.pi/3
P2_addition = sh.addition_theorem(l=2, gamma=gamma)
```

## Implementation Notes

- Uses scipy.special.lpmn for associated Legendre functions
- Normalization follows physics convention (Condon-Shortley phase)
- CGS units for any physical quantities
- Caching of computed harmonics for efficiency

## Validation

- Orthogonality verified numerically
- Recurrence relations checked
- Comparison with tabulated values (Abramowitz & Stegun)
- Addition theorem verification

## Maxwell Article References

| Article | Content |
|---------|---------|
| 125-133 | Spherical harmonic analysis |
| 140-145 | Applications to electrostatics |
| 543-555 | Spherical harmonics in magnetism |
| 692-700 | Harmonic analysis for electromagnetic fields |

## Related Commands

- `vector-calculus-ops` - Laplacian in spherical coordinates
- `potential-theory` - Solutions using harmonic expansion
- `solid-angle-calc` - Related angular computations
