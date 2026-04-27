# JAX Adapter — Maxwell Modernized

> GPU/TPU-accelerated, auto-differentiable implementations of Maxwell's 1873 Treatise computations.

## Overview

The `maxwell.jax` package provides JAX-compatible versions of core Maxwell Treatise calculations, enabling:

- **JIT compilation** via `jax.jit` — compiled XLA kernels for repeated evaluations
- **Automatic differentiation** via `jax.grad` — compute field gradients, sensitivities, optimization
- **Vectorized evaluation** via `jax.vmap` — batch over thousands of field points simultaneously
- **GPU/TPU execution** — deploy on accelerators without code changes

All computations preserve **CGS-EMU units** and are **citation-traceable** to Maxwell's original articles.

## Package Structure

```
maxwell/jax/
├── __init__.py                  # x64 config, package exports
├── _compat.py                   # Pytree registration, safe arithmetic
├── _scipy_special.py            # Pure JAX wrappers: lpmv, legendre, sph_harm_y
├── _elliptic.py                 # AGM-based elliptic integrals (no scipy)
├── core/
│   ├── __init__.py
│   └── charge.py                # PointChargeJAX, multi-charge systems
├── electromagnetism/
│   ├── __init__.py
│   ├── induction.py             # FaradayInductionJAX (Lenz's law, EMF)
│   ├── equations.py             # MaxwellEquationsJAX (all 9 equations)
│   ├── forces.py                # LorentzForceJAX, MaxwellStressTensorJAX
│   └── ampere_maxwell.py        # DisplacementCurrentJAX, AmpereMaxwellLawJAX
└── math/
    ├── __init__.py
    └── spherical_harmonics.py   # SphericalHarmonicExpansionJAX
```

## Quick Start

```python
import jax
from maxwell.jax.core.charge import PointChargeJAX

# Enable float64 for CGS precision
jax.config.update("jax_enable_x64", True)

# Single charge
charge = PointChargeJAX(q=1.0, position=jax.numpy.array([0.0, 0.0, 0.0]))
E = charge.field_at(jax.numpy.array([5.0, 0.0, 0.0]))
# E = [0.04, 0.0, 0.0] statvolt/cm

# Batched evaluation over 1000 points
points = jax.numpy.linspace(-10, 10, 1000).reshape(-1, 3)
E_batched = charge.field_at_batched(points)

# JIT-compiled
from jax import jit, vmap, grad

@jit
def field_on_grid(q, pos, point):
    c = PointChargeJAX(q=q, position=pos)
    return c.field_at(point)
```

## Pytree Registration

All JAX dataclasses use the `@jax_tree` decorator for pytree registration:

```python
from maxwell.jax._compat import jax_tree
from dataclasses import dataclass

@jax_tree
@dataclass
class MyClass:
    field: jax.Array
    value: float

# Now works with jax.jit, jax.grad, jax.vmap
```

## Safe Arithmetic

The `_compat` module provides JAX-safe alternatives to division, sqrt, and norm:

```python
from maxwell.jax._compat import safe_div, safe_sqrt, safe_norm

# Safe division: returns 0 when denominator is zero
result = safe_div(numerator, denominator, safe_default=0.0)

# Safe sqrt: returns 0 for negative inputs
result = safe_sqrt(x, safe_default=0.0)

# Safe norm: returns floor value for zero vectors
result = safe_norm(x, axis=-1, safe_default=1e-30)
```

## Elliptic Integrals

Pure JAX AGM-based implementation — no scipy dependency:

```python
from maxwell.jax._elliptic import ellipk_jax, ellipe_jax

# Complete elliptic integrals
K = ellipk_jax(0.5)  # ~1.854
E = ellipe_jax(0.5)  # ~1.351

# JIT and vmap compatible
@jit
def compute_k(m):
    return ellipk_jax(m)
```

## Faraday Induction

```python
from maxwell.jax.electromagnetism.induction import FaradayInductionJAX

coil = FaradayInductionJAX(num_turns=100, resistance=50.0)

# Magnetic flux
flux = coil.magnetic_flux(B_field, area=10.0)

# Induced EMF (Lenz's law)
emf = coil.induced_emf(flux_change_rate=10000.0)

# Full analysis
from maxwell.jax.electromagnetism.induction import analyze_faraday_induction_jax
result = analyze_faraday_induction_jax(
    B_initial=jnp.zeros(3),
    B_final=jnp.array([0, 0, 1000]),
    loop_area=10.0,
    time_interval=0.5,
    num_turns=100,
)
```

## Maxwell's Equations

```python
from maxwell.jax.electromagnetism.equations import MaxwellEquationsJAX

eq = MaxwellEquationsJAX(permittivity=1.0, permeability=1.0, conductivity=0.0)

# Gauss's law
div_D = eq.gauss_law_electric(D_field, dx=0.1, rho=0.0)

# Faraday's law
curl_E = eq.equation_A_faraday(dB_dt)

# Verify all equations
report = verify_maxwell_equations_jax()
```

## Spherical Harmonics

```python
from maxwell.jax.math.spherical_harmonics import (
    SphericalHarmonicExpansionJAX,
    legendre_batched,
    addition_theorem_jax,
)

# Legendre polynomials (batched)
x = jnp.linspace(-1, 1, 100)
P3 = legendre_batched(3, x)

# Expansion
expansion = SphericalHarmonicExpansionJAX(max_l=8)
expansion.compute_coefficients(f_theta, theta_grid)
reconstructed = expansion.reconstruct(theta, phi)
```

## Lorentz Force & Stress Tensor

```python
from maxwell.jax.electromagnetism.forces import (
    LorentzForceJAX,
    MaxwellStressTensorJAX,
    force_on_wire_jax,
    force_on_charge_jax,
    stress_tensor_jax,
)

# Lorentz force on wire
force = LorentzForceJAX(
    current=1.0,
    length=jnp.array([10.0, 0.0, 0.0]),
    B_field=jnp.array([0.0, 0.0, 1000.0]),
)
F = force.force_vector  # [0, -10000, 0] dynes

# Force on moving charge
F = force_on_charge_jax(
    charge=1.0,
    velocity=jnp.array([1e8, 0.0, 0.0]),
    B_field=jnp.array([0.0, 0.0, 100.0]),
)

# Maxwell stress tensor
tensor = MaxwellStressTensorJAX(
    E_field=jnp.array([100.0, 0.0, 0.0]),
    H_field=jnp.array([0.0, 50.0, 0.0]),
)
T = tensor.stress_tensor()  # 3x3 tensor
P = tensor.electromagnetic_pressure  # scalar pressure
```

## Automatic Differentiation

```python
from jax import grad
from maxwell.jax.core.charge import PointChargeJAX

def potential_at_q(q):
    c = PointChargeJAX(q=q, position=jnp.zeros(3))
    return c.potential_at(jnp.array([1.0, 0.0, 0.0]))

# dV/dq at q=1
dVdq = grad(potential_at_q)(1.0)
```

## Compatibility Notes

- **Float64 required**: CGS unit ratios need ~15 digits. Always `jax.config.update("jax_enable_x64", True)`.
- **scipy.special gaps**: `jax.scipy.special.sph_harm_y` works for array inputs. The `_scipy_special` module provides pure JAX `lpmv_jax` and `legendre_jax` implementations.
- **Control flow**: All loops use `jax.lax.fori_loop` or `jax.lax.while_loop` for JIT traceability.
- **Dataclass fields**: All pytree-registered dataclass fields are JAX-traced by default.

## Test Suite

123 tests cover:
- Pytree registration (3 tests)
- PointChargeJAX correctness (9 tests)
- Multi-charge systems (3 tests)
- Auto-differentiation (2 tests)
- Elliptic integrals (8 tests)
- JAX special functions (7 tests)
- Faraday induction (16 tests)
- Maxwell equations (11 tests)
- Spherical harmonics (14 tests)
- Lorentz force (13 tests)
- Maxwell stress tensor (13 tests)
- Ampere-Maxwell law (20 tests)
- Safe arithmetic (5 tests)

```bash
pytest tests/test_jax_adapter.py -v
```

## Citation Traceability

All JAX implementations maintain the `@maxwell_cite` decorator from the NumPy versions. Each function can be traced back to its source article via `get_citation(func)`.

| JAX Class | Articles |
|-----------|----------|
| PointChargeJAX | Arts. 29-30 |
| FaradayInductionJAX | Arts. 528-531, 542 |
| MaxwellEquationsJAX | Arts. 594-603 |
| SphericalHarmonicExpansionJAX | Arts. 128-146 |
| LorentzForceJAX | Arts. 490-492 |
| MaxwellStressTensorJAX | Arts. 641-646 |
| DisplacementCurrentJAX | Arts. 606-607 |
| AmpereMaxwellLawJAX | Arts. 606-607 |
| ellipk_jax, ellipe_jax | Arts. 149-152 |
