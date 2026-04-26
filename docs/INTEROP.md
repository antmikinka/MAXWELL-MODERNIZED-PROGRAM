# Maxwell Modernized — Cross-Framework Interoperability Analysis

**Date:** 2026-04-25
**Branch:** feat/pypi-package

This document analyzes how the Maxwell Modernized library's mathematics and computational logic could integrate with other Python frameworks.

---

## Current Dependencies

- `numpy>=1.24.0` — Core numerical computing
- `scipy>=1.10.0` — Special functions (spherical harmonics, elliptic integrals), integration, optimization

---

## 1. PyTorch — GPU Acceleration

**Integration Potential: High**
**Effort: Medium**

### Modules That Benefit Most

| Module | Current Bottleneck | GPU Gain |
|---|---|---|
| `maxwell.math.spherical_harmonics` | Triple-nested coefficient loop O(L*M*Theta*Phi) | 10-50x |
| `maxwell.electromagnetism.energy.magnetic` | O(n^3) 3D grid integration | 20-100x |
| `maxwell.calculus.cyclic` | O(N^2) double line integral | 5-20x |
| `maxwell.electromagnetism.forces.stress_tensor` | Batch stress tensor computation | 10-50x |
| `maxwell.electromagnetism.forces.lorentz` | Grid-point force evaluation | 5-20x |

### Adapter Pattern

```python
"""Adapter: maxwell numpy -> PyTorch tensors for GPU computation."""
import torch
import numpy as np

def np_to_torch(arr, device="cuda"):
    return torch.tensor(np.asarray(arr, dtype=torch.float64), device=device)

def torch_to_np(tensor):
    return tensor.cpu().numpy()

# GPU spherical harmonic coefficient computation
def compute_coefficients_gpu(E_field, B_field, max_l, theta_vals, phi_vals, device="cuda"):
    E = np_to_torch(E_field, device)
    theta = np_to_torch(theta_vals, device)
    phi = np_to_torch(phi_vals, device)

    # Batched spherical harmonics evaluation
    Theta, Phi = torch.meshgrid(theta, phi, indexing="ij")
    # Precompute all Y_lm on grid, contract via einsum
    coefficients = {}
    for l in range(max_l + 1):
        for m in range(-l, l + 1):
            Y_lm = torch.special.spherical_harmonic_y(m, l, Phi, Theta)
            # Numerical integration over sphere
            dtheta = theta[1] - theta[0]
            dphi = phi[1] - phi[0]
            integral = torch.sum(field_values * Y_lm.conj()) * dtheta * dphi
            coefficients[(l, m)] = integral.item()
    return coefficients
```

### Friction Points

- `scipy.special.lpmv` and `scipy.special.sph_harm` have no direct PyTorch equivalent
- Must use `torch.special.spherical_harmonic_y` (available in PyTorch 2.0+) or pre-compute on CPU
- All functions use `np.asarray(arr, dtype=np.float64)` — directly compatible with `torch.tensor()`

---

## 2. JAX — Autodiff and JIT Compilation

**Integration Potential: High**
**Effort: Medium**

### Modules That Benefit Most

| Module | Current Approach | JAX Improvement |
|---|---|---|
| `maxwell.calculus.vector_potential` | Manual finite-difference gradients | `jax.grad` exact derivatives |
| `maxwell.electromagnetism.theory.general_equations` | `np.gradient` finite-difference stencils | Autodiff, no stencil errors |
| `maxwell.calculus.cyclic` | Manual solid angle gradient | Single `jax.grad()` call |
| `maxwell.electromagnetism.energy.magnetic` | O(n^3) Python loop | `jax.jit` + `vmap` |
| `maxwell.electromagnetism.optimization.coil_design` | `scipy.optimize.minimize_scalar` | `jax.value_and_grad` + gradient optimizers |

### Adapter Pattern

```python
"""Adapter: JAX-accelerated Maxwell computations."""
import jax
import jax.numpy as jnp
from jax import jit, grad, vmap

# JIT-compiled stress tensor (replaces Python double loop)
@jit
def stress_tensor_jax(E_field, B_field):
    E2 = jnp.dot(E_field, E_field)
    B2 = jnp.dot(B_field, B_field)
    T = (jnp.outer(E_field, E_field) + jnp.outer(B_field, B_field)
         - 0.5 * jnp.eye(3) * (E2 + B2))
    return T / (4.0 * jnp.pi)

# Autodiff replaces manual finite-difference
def vector_potential_autodiff(current_func, observation_point):
    def solid_angle_wrapper(p):
        return solid_angle_closed_curve(current_func, p)
    grad_Omega = jax.grad(solid_angle_wrapper)(observation_point)
    return (1.0 / CONST.C) * grad_Omega  # CGS

# Vmap for batch evaluation over field grids
batch_stress = vmap(stress_tensor_jax, in_axes=(0, 0))
# Processes 1000s of (E, B) pairs simultaneously
```

### Friction Points

- No in-place mutation (codebase is mostly pure functions — good alignment)
- `np.random` must use JAX PRNG system for JIT
- `@maxwell_cite` decorator is compatible with JAX transformations

---

## 3. SymPy — Symbolic Mathematics

**Integration Potential: Medium**
**Effort: Low**

### Modules That Benefit

| Module | Use Case |
|---|---|
| `maxwell.math.spherical_harmonics` | Symbolic Legendre polynomials, verify recurrence relations |
| `maxwell.electromagnetism.forces.stress_tensor` | Prove T_ij = T_ji, trace = -energy_density |
| `maxwell.electromagnetism.theory.general_equations` | Symbolic wave equation derivation from Eq A-G |
| `maxwell.electromagnetism.components.circular_coils` | Symbolic elliptic integral series expansions |

### Example

```python
import sympy as sp

def verify_stress_tensor_symbolically():
    Ex, Ey, Ez = sp.symbols('Ex Ey Ez')
    Bx, By, Bz = sp.symbols('Bx By Bz')
    E = sp.Matrix([Ex, Ey, Ez])
    B = sp.Matrix([Bx, By, Bz])
    E2, B2 = E.dot(E), B.dot(B)

    T = (E * E.T + B * B.T - sp.eye(3) * (E2 + B2) / 2) / (4 * sp.pi)

    # Prove symmetry
    assert sp.simplify(T - T.T) == sp.zeros(3, 3)
    # Prove trace relation
    trace_T = sp.simplify(T.trace())
    expected = -(E2 + B2) / (8 * sp.pi)
    assert sp.simplify(trace_T - expected) == 0
    return T
```

This is lowest-effort: adds a `maxwell.symbolic/` verification submodule without touching numerical code.

---

## 4. TensorFlow — ML Pipelines

**Integration Potential: Medium**
**Effort: High**

### Modules That Benefit

| Module | Use Case |
|---|---|
| `maxwell.electromagnetism.optimization.coil_design` | Surrogate models for coil geometry optimization |
| `maxwell.math.spherical_harmonics` | Neural networks learning harmonic expansions from sparse measurements |
| `maxwell.materials.hysteresis` | LSTM/Transformer for hysteresis loop prediction |
| `maxwell.electromagnetism.forces.stress_tensor` | Physics-informed neural networks (PINNs) |

### Example

```python
import tensorflow as tf

def create_field_dataset(n_samples=100000):
    """Generate training data from Maxwell field computations."""
    E_fields = np.random.randn(n_samples, 3).astype(np.float32) * 100
    B_fields = np.random.randn(n_samples, 3).astype(np.float32) * 10
    from maxwell.electromagnetism.forces.stress_tensor import MaxwellStressTensor
    tensors = np.array([MaxwellStressTensor(E=e, B=b).tensor()
                        for e, b in zip(E_fields, B_fields)])
    dataset = tf.data.Dataset.from_tensor_slices(
        ({"E": E_fields, "B": B_fields}, {"stress_tensor": tensors})
    )
    return dataset.batch(256).prefetch(tf.data.AUTOTUNE)
```

### Friction Points

- Requires full ML training infrastructure
- CGS units need preprocessing normalization layer
- Best for inverse problems (inferring sources from measurements)

---

## 5. Matplotlib / Plotly — Visualization

**Integration Potential: High**
**Effort: Low**

### Modules Ready for Plotting

| Module | Plot Type |
|---|---|
| `maxwell.materials.hysteresis` | B-H hysteresis loops |
| `maxwell.math.spherical_harmonics` | 3D surface plots of |Y_lm|^2 |
| `maxwell.electromagnetism.components.circular_coils` | 3D vector field plots |
| `maxwell.electromagnetism.forces.stress_tensor` | Principal stress eigenvalue visualization |
| `maxwell.electromagnetism.theory.general_equations` | Time-evolution E/B field animations |

### Example

```python
import matplotlib.pyplot as plt

def plot_hysteresis_loop(model, H_max=10.0, n_points=200):
    """Plot B-H hysteresis loop."""
    cycle = model.simulate_cycle(H_max=H_max, n_points=n_points)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(cycle['H_values'], cycle['B_values'], 'b-', linewidth=2)
    ax.axhline(y=model.retentivity(), color='r', ls='--',
               label=f'Retentivity = {model.retentivity():.3f}')
    ax.axvline(x=-model.coercive_force(), color='g', ls='--',
               label=f'Coercivity = {model.coercive_force():.3f}')
    ax.set_xlabel('H (Oe)')
    ax.set_ylabel('B (G)')
    ax.set_title('Magnetic Hysteresis Loop')
    ax.legend()
    return fig
```

Dataclass return types are already plotting-ready — no data transformation needed.

---

## 6. NumPyro / PyMC — Bayesian Inference

**Integration Potential: Medium**
**Effort: Medium**

### Modules That Benefit

| Module | Use Case |
|---|---|
| `maxwell.materials.hysteresis` | Infer Weber model parameters from B-H measurements |
| `maxwell.electromagnetism.components.circular_coils` | Infer current from measured field values |
| `maxwell.electromagnetism.optimization.coil_design` | Bayesian coil geometry optimization |

### Example

```python
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

def hysteresis_inference(B_measurements, H_values):
    """Bayesian Weber model: infer material parameters."""
    # Priors from typical_hysteresis_parameters() catalog
    kappa = numpyro.sample('kappa', dist.LogNormal(5.0, 1.0))
    k_hyst = numpyro.sample('k_hyst', dist.LogNormal(0.0, 2.0))
    alpha = numpyro.sample('alpha', dist.LogNormal(-1.0, 1.0))
    sigma = numpyro.sample('sigma', dist.HalfCauchy(1.0))

    B_predicted = webster_forward_model(H_values, kappa, k_hyst, alpha)
    numpyro.sample('obs', dist.Normal(B_predicted, sigma), obs=B_measurements)
```

The `typical_hysteresis_parameters()` catalog provides informed priors for 8 material types (mu-metal, permalloy, electrical steel, iron, alnico, ferrite, neodymium, samarium-cobalt).

---

## 7. Dask — Parallel Computation

**Integration Potential: High**
**Effort: Medium**

### Modules That Benefit

| Module | Bottleneck | Parallelization |
|---|---|---|
| `maxwell.electromagnetism.energy.magnetic` | O(n^3) triple loop | Embarrassingly parallel |
| `maxwell.electromagnetism.forces.lorentz` | Grid-point evaluation | Per-point parallel |
| `maxwell.electromagnetism.optimization.coil_design` | Multi-point uniformity | Per-point parallel |
| `maxwell.calculus.cyclic` | O(N^2) segment pairs | Per-pair parallel |

### Example

```python
from dask import delayed, compute

@delayed
def compute_energy_at_point(position, H_func, permeability):
    H = np.asarray(H_func(position), dtype=np.float64)
    return (permeability / (8.0 * np.pi)) * np.dot(H, H)

def integrate_magnetic_energy_dask(H_func, x_range, y_range, z_range,
                                    n_points=20, permeability=1.0):
    """Replace triple-nested Python loop with Dask parallel."""
    x = np.linspace(*x_range, n_points)
    y = np.linspace(*y_range, n_points)
    z = np.linspace(*z_range, n_points)
    dV = (x[1]-x[0]) * (y[1]-y[0]) * (z[1]-z[0])

    energies = [compute_energy_at_point((xi, yi, zi), H_func, permeability)
                for xi in x for yi in y for zi in z]
    energy_values = compute(*energies)
    return sum(energy_values) * dV
```

---

## 8. h5py / Zarr — Data Storage

**Integration Potential: Medium**
**Effort: Low**

### Modules That Benefit

| Module | Data to Store |
|---|---|
| `maxwell.math.spherical_harmonics` | Spherical harmonic coefficients ((L+1)^2 complex values) |
| `maxwell.electromagnetism.theory.general_equations` | 3D field grids (E, B, H, D arrays) |
| `maxwell.materials.hysteresis` | Measured hysteresis loops with material metadata |
| `maxwell.electromagnetism.optimization.coil_design` | Optimization results across parameter grids |

### Example

```python
import h5py

def save_spherical_harmonic_expansion(filename, expansion, metadata=None):
    with h5py.File(filename, 'w') as f:
        grp = f.create_group('spherical_harmonics')
        grp.attrs['max_l'] = expansion.max_l
        if metadata:
            for k, v in metadata.items():
                grp.attrs[k] = v
        # Store coefficients
        for i, ((l, m), coeff) in enumerate(expansion.coefficients.items()):
            grp.create_dataset(f'coeff_l{l}_m{m}', data=coeff)
```

---

## Integration with Physics Engines

**Potential: Medium | Effort: Medium**

### As a Backend

- `@maxwell_cite` provides automatic provenance tracking for scientific engines
- Pure functions (no global state) enable safe concurrent execution
- `network_solver.py` implements a complete conductance matrix solver
- All APIs are dataclass-based, providing clean interfaces

### Challenges

- **CGS units** — Most physics engines use SI. Adapter layer needed (conversion factors already in `config/constants.py`)
- **Static field focus** — Analytical/quasi-static solutions, not full time-domain FDTD
- **No mesh input** — Canonical geometries only (solenoids, coils, planes)

### Concrete Paths

1. **Blender/Unity plugin** — Field visualization via `circular_coils.py`, `stress_tensor.py`
2. **COMSOL/Ansys add-on** — Analytical verification via `general_equations.py`
3. **Standalone solver** — `network_solver.py` packaged via pybind11 for C++/MATLAB

---

## As a FEM Solver Benchmark

**Potential: High | Effort: Low**

Analytical solutions available as benchmarks:

| Module | Benchmark |
|---|---|
| `circular_coils.py` | Exact coil field via elliptic integrals |
| `stress_tensor.py` | Tensor symmetry/trace identities |
| `general_equations.py` | All 7 Maxwell equation consistency checks |
| `spherical_harmonics.py` | Known convergence properties |
| `network_solver.py` | Exact Kirchhoff/Wheatstone bridge solutions |
| `faraday.py` | Motional EMF time-varying benchmarks |

Verification functions already implemented: `verify_stress_tensor()`, `verify_coil_design()`, `verify_kirchhoff_laws()`.

---

## As an Educational Platform

**Potential: High | Effort: Very Low**

- `@maxwell_cite` provides academic provenance (article numbers, parts, chapters)
- CGS units match historical textbook conventions
- Dataclass API is discoverable via `help()`
- `verify_*` functions serve as built-in self-tests
- Pure Python + numpy/scipy is Pyodide-compatible (no C extensions)

### Course Mapping

| Course Topic | Module |
|---|---|
| Electromagnetic fields | `general_equations.py` |
| Magnetic materials | `hysteresis.py` |
| Forces and stresses | `stress_tensor.py`, `lorentz.py` |
| Spherical harmonics | `spherical_harmonics.py` |
| Circuit analysis | `network_solver.py` |
| Induction | `faraday.py` |
| Coil design | `coil_design.py` |
| Vector calculus | `cyclic.py`, `integrals.py`, `vector_potential.py` |

---

## Priority Recommendation

**JAX integration** provides the highest ROI — replaces error-prone finite-difference code with exact autodiff, JIT-compiles expensive loops, maintains numpy-compatible APIs.

**Matplotlib/Plotly visualization** and **SymPy verification** are lowest-effort additions providing immediate value.

| Framework | Potential | Effort | Primary Benefit |
|---|---|---|---|
| JAX | High | Medium | Autodiff + JIT for loops and gradients |
| Matplotlib/Plotly | High | Low | Direct plotting of dataclass outputs |
| SymPy | Medium | Low | Symbolic identity verification |
| PyTorch | High | Medium | GPU acceleration of O(n^3) loops |
| Dask | High | Medium | Parallel parameter sweeps |
| NumPyro/PyMC | Medium | Medium | Bayesian parameter inference |
| h5py/Zarr | Medium | Low | Provenance-preserving storage |
| TensorFlow | Medium | High | ML surrogates and PINNs |
