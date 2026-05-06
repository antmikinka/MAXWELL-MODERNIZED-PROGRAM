# Cycle 7 Implementation Plan

> **Theme:** Visualization Blitz + Build Validation + Lagrangian Kernel Start
> **Date:** 2026-05-06
> **Branch:** `feat/pypi-package`
> **Prepared by:** software-program-manager

---

## Execution Summary

| # | Work Item | Complexity | Dependencies | Est. Effort |
|---|-----------|------------|-------------|-------------|
| 1 | Build Validation | Trivial | None | 5 min |
| 2 | Dielectric Soakage Visualization (Art. 329) | Medium | `maxwell.electrokinematics.dielectric_conduction` | 45 min |
| 3 | Hysteresis Loops Visualization (Art. 442) | Medium | `maxwell.materials.hysteresis` | 45 min |
| 4 | EM Wave Propagation Visualization (Art. 791) | High | `maxwell.optics.plane_waves` | 60 min |
| 5 | Lagrangian Kernel Scaffolding (Layer 52) | High | `maxwell.jax.core.charge` (pattern reference) | 60 min |

**Total estimated effort:** ~3.5 hours
**Execution order:** Items 1-5 can run in any order. Items 2-4 are independent of each other. Item 5 (Lagrangian) is fully independent.

---

## Work Item 1: Build Validation

### Objective
Verify the package builds cleanly and passes distribution checks.

### Commands
```bash
# Install tools if needed
pip install build twine

# Build the package
python -m build

# Check distribution for warnings
twine check dist/*
```

### Acceptance Criteria
- `python -m build` completes without errors
- `dist/` contains both `.tar.gz` and `.whl` files
- `twine check dist/*` reports no warnings
- Document results (note any warnings for future fixes)

### Files Modified
- None (validation only)

---

## Work Item 2: Dielectric Soakage Visualization (Art. 329)

### Physics Dependency
`maxwell/electrokinematics/dielectric_conduction.py` provides:
- `DielectricConductor.step_response(voltage, times)` -- returns dict with `times`, `total_current`, `leakage_current`, `absorption_current`, `stored_charge`
- `absorption_current(voltage, capacitance, time, absorption_constants)` -- returns dict with current decay data
- `dielectric_absorption(voltage, capacitance, absorption_time, absorption_constants)` -- absorbed charge over time

The absorption current model: `I(t) = sum(V * C * a_i / tau_i * exp(-t/tau_i))`

### New File: `maxwell/vis/dielectric_soakage.py`

#### Function 1: `calc_dielectric_absorption`
```python
def calc_dielectric_absorption(
    t: np.ndarray,
    tau: list[float] | None = None,
    A: list[float] | None = None,
) -> np.ndarray:
    """Calculate dielectric absorption current: I(t) = sum(Ai * exp(-t/tau_i)).

    Art. 329: Maxwell's "electric soakage" -- current decays as a sum of
    exponentials with distinct time constants representing slow polarization
    mechanisms within the dielectric.

    Args:
        t: Time array (seconds).
        tau: List of time constants tau_i (seconds). Default: [1.0, 10.0, 100.0].
        A: List of amplitude coefficients A_i (abamperes). Default: [1.0, 0.3, 0.1].

    Returns:
        Absorption current I(t) at each time point, shape same as t.
    """
```

#### Function 2: `plot_dielectric_soakage`
```python
def plot_dielectric_soakage(
    tau: list[float] | None = None,
    A: list[float] | None = None,
    t_range: tuple[float, float] = (0.01, 1000.0),
    resolution: int = 500,
    ax: Axes | None = None,
    log_scale: bool = True,
) -> tuple[Figure, Axes]:
    """Plot time-domain absorption current decay with multiple time constants.

    Art. 329: Visualizes dielectric soakage showing the characteristic
    multi-exponential decay. The log-scale view reveals individual
    time constant contributions.

    Args:
        tau: Time constants (seconds). Default: [1.0, 10.0, 100.0].
        A: Amplitude coefficients (abamperes). Default: [1.0, 0.3, 0.1].
        t_range: (t_min, t_max) in seconds.
        resolution: Number of time points.
        ax: Existing axes to plot on (optional).
        log_scale: Use log-log scale (default True, reveals time constants).

    Returns:
        Tuple of (Figure, Axes).
    """
```

**Plot elements:**
- Main decay curve (total current) on log-log or linear axes
- Individual exponential components shown as dashed lines
- Annotations marking dominant time constants
- Title references Art. 329 ("Dielectric Soakage")

### New File: `tests/test_vis_dielectric_soakage.py` (10 tests)

| # | Test Name | Verification |
|---|-----------|-------------|
| 1 | `test_decay_monotonic` | Total current decreases with time |
| 2 | `test_single_tau_exponential` | Single tau gives pure exponential decay |
| 3 | `test_multi_tau_sum` | Multi-tau equals sum of individual exponentials |
| 4 | `test_plot_returns_fig_ax` | plot_dielectric_soakage returns (Figure, Axes) |
| 5 | `test_plot_with_existing_ax` | Accepts and uses provided ax |
| 6 | `test_default_args` | Works with no arguments |
| 7 | `test_no_nan_inf` | Output contains no NaN or Inf |
| 8 | `test_log_scale_has_labels` | Log scale plot has appropriate axis labels |
| 9 | `test_current_at_zero` | I(0) = sum(A_i) |
| 10 | `test_long_time_decay` | Current approaches 0 as t >> max(tau) |

### Files to Create
- `maxwell/vis/dielectric_soakage.py`
- `tests/test_vis_dielectric_soakage.py`

### Files to Modify
- `maxwell/vis/__init__.py` -- Add exports for new functions
- `tests/test_vis.py` -- Add integration test for new exports

---

## Work Item 3: Hysteresis Loops Visualization (Art. 442)

### Physics Dependency
`maxwell/materials/hysteresis.py` provides:
- `generate_theoretical_hysteresis_loop(I_s, H_c, kappa_initial, n_points)` -- returns dict with `H_branch1`, `I_branch1`, `H_branch2`, `I_branch2`, `H_full`, `I_full`, `H_max`
- `HysteresisLoop` dataclass with `.retentivity()`, `.coercive_force()`, `.energy_loss_per_cycle()`, `.loop_area`
- `WeberModelWithHysteresis.simulate_cycle(H_max, n_points)` -- returns `(H_values, I_values)`
- `typical_hysteresis_parameters()` -- returns dict mapping material names to parameters
- `analyze_hysteresis_loop(H_values, I_values)` -- returns analysis dict

### New File: `maxwell/vis/hysteresis_loops.py`

#### Function 1: `calc_hysteresis_loop`
```python
def calc_hysteresis_loop(
    H_max: float,
    mu_r: float,
    alpha: float,
    n_points: int = 500,
) -> dict[str, np.ndarray]:
    """Generate B-H loop using a Jiles-Atherton inspired model.

    Art. 442-446: Maxwell's theory of magnetic hysteresis describes
    the lag of magnetization behind the applied field, creating a
    closed loop with retentivity and coercivity.

    This wraps generate_theoretical_hysteresis_loop with physically
    intuitive parameters.

    Args:
        H_max: Maximum applied field (gauss).
        mu_r: Relative permeability (dimensionless).
        alpha: Hysteresis coupling parameter (dimensionless, ~0.001).
        n_points: Number of points per branch.

    Returns:
        Dictionary with H_values, B_values for ascending and descending branches.
    """
```

#### Function 2: `plot_hysteresis_loops`
```python
def plot_hysteresis_loops(
    H_max: float = 1000.0,
    mu_r: float = 1000.0,
    alpha: float = 0.001,
    ax: Axes | None = None,
    show_coercivity: bool = True,
    show_retentivity: bool = True,
) -> tuple[Figure, Axes]:
    """Plot B-H hysteresis loop with labeled retentivity/coercivity.

    Art. 442-446: Visualizes the complete hysteresis loop with:
    - B-H curve with ascending/descending branches
    - Labeled coercive field H_c (x-intercept)
    - Labeled retentivity B_r (y-intercept)
    - Shaded loop area representing energy loss per cycle

    Args:
        H_max: Maximum applied field (gauss).
        mu_r: Relative permeability.
        alpha: Hysteresis coupling parameter.
        ax: Existing axes to plot on (optional).
        show_coercivity: Annotate coercive force point.
        show_retentivity: Annotate retentivity point.

    Returns:
        Tuple of (Figure, Axes).
    """
```

**Plot elements:**
- Complete B-H loop (closed curve)
- Red dot/annotation at coercivity point (H_c, 0)
- Green dot/annotation at retentivity point (0, B_r)
- Shaded interior showing energy loss area
- Grid with equal aspect ratio
- Title references Arts. 442-446

#### Function 3: `plot_material_comparison`
```python
def plot_material_comparison(
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Compare hysteresis loops for soft iron, steel, and permanent magnet materials.

    Art. 444-446: Maxwell cataloged magnetic properties of various substances.
    This plot overlays loops for representative materials to show the range
    from soft magnetic (narrow loop) to hard magnetic (wide loop).

    Materials compared:
    - Mu-metal (soft: H_c ~ 0.002 gauss)
    - Electrical steel (medium: H_c ~ 0.5 gauss)
    - Alnico 5 (hard: H_c ~ 600 gauss)

    Args:
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes).
    """
```

### New File: `tests/test_vis_hysteresis_loops.py` (10 tests)

| # | Test Name | Verification |
|---|-----------|-------------|
| 1 | `test_loop_closure` | Loop starts and ends at same B value |
| 2 | `test_coercivity_positive` | Extracted H_c > 0 |
| 3 | `test_retentivity_positive` | Extracted B_r > 0 |
| 4 | `test_loop_area_positive` | Enclosed area > 0 (energy dissipation) |
| 5 | `test_plot_returns_fig_ax` | plot_hysteresis_loops returns (Figure, Axes) |
| 6 | `test_plot_with_existing_ax` | Accepts and uses provided ax |
| 7 | `test_default_args` | Works with no arguments |
| 8 | `test_material_comparison_returns_fig` | plot_material_comparison returns figure |
| 9 | `test_soft_vs_hard_coercivity` | Hard material has larger H_c than soft |
| 10 | `test_calc_hysteresis_loop_keys` | Returns dict with expected keys |

### Files to Create
- `maxwell/vis/hysteresis_loops.py`
- `tests/test_vis_hysteresis_loops.py`

### Files to Modify
- `maxwell/vis/__init__.py` -- Add exports
- `tests/test_vis.py` -- Add integration test

---

## Work Item 4: EM Wave Propagation Visualization (Art. 791)

### Physics Dependency
`maxwell/optics/plane_waves.py` provides:
- `PlaneWave` dataclass with `.E_field(position, time)` and `.B_field(position, time)`
- `PolarizationState` with `.electric_field()`, `.magnetic_field()`, `.polarization_type()`, `.stokes_parameters()`
- Factory methods: `PolarizationState.linear_polarization()`, `.circular_polarization()`, `.elliptical_polarization()`
- `calc_B_from_E(E, k, omega)` -- computes B field from E
- `verify_transverse_condition(E, k)` -- verifies E dot k = 0
- `CONST.C` -- speed of light

### New File: `maxwell/vis/em_wave_propagation.py`

#### Function 1: `calc_em_wave`
```python
def calc_em_wave(
    x: np.ndarray,
    t: float,
    omega: float,
    k: float,
    E0: float,
    polarization: str = "linear",
) -> dict[str, np.ndarray]:
    """Calculate E and B fields for plane wave propagation.

    Art. 791: For a plane electromagnetic wave propagating in +z direction:

        E_x(z,t) = E0 * cos(k*z - omega*t)          (linear)
        E_y(z,t) = E0 * cos(k*z - omega*t + delta)   (polarization-dependent)
        B = (1/c) * k_hat x E

    Polarization states:
    - linear: E oscillates along x-axis only
    - circular: E_x = E_y with 90-degree phase difference
    - elliptical: General case with arbitrary amplitude ratio and phase

    Args:
        x: Spatial positions along propagation axis (cm).
        t: Time instant (s).
        omega: Angular frequency (rad/s).
        k: Wave number (cm^-1).
        E0: Electric field amplitude (statvolts/cm).
        polarization: 'linear', 'circular_right', 'circular_left', or 'elliptical'.

    Returns:
        Dictionary with:
        - E_x, E_y, E_z: Electric field components
        - B_x, B_y, B_z: Magnetic field components
        - E_magnitude, B_magnitude: Field magnitudes
    """
```

#### Function 2: `plot_em_wave_propagation`
```python
def plot_em_wave_propagation(
    omega: float = 2 * np.pi,
    E0: float = 1.0,
    polarization: str = "linear",
    x_range: tuple[float, float] = (0.0, 4 * np.pi),
    resolution: int = 200,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot E and B field propagation showing orthogonal wave nature.

    Art. 791: Visualizes the propagating electromagnetic wave with:
    - E field (red) and B field (blue) on separate subplots or overlaid
    - Orthogonal relationship: E perpendicular to B, both perpendicular to propagation
    - Wave speed c = omega/k verification
    - Polarization state visualization

    Args:
        omega: Angular frequency (rad/s). Default: 2*pi (1 Hz).
        E0: Electric field amplitude (statvolts/cm).
        polarization: 'linear', 'circular_right', 'circular_left', 'elliptical'.
        x_range: (x_min, x_max) propagation distance (cm).
        resolution: Number of spatial points.
        ax: Existing axes to plot on (optional).

    Returns:
        Tuple of (Figure, Axes) or (Figure, list[Axes]) for multi-panel.
    """
```

**Plot elements:**
- Two-panel layout (or overlaid): E field vs position, B field vs position
- Color coding: E field in red, B field in blue
- Wavelength annotation
- Propagation direction arrow
- For circular polarization: polarization ellipse inset

#### Function 3: `plot_wave_snapshot_3d`
```python
def plot_wave_snapshot_3d(
    E0: float = 1.0,
    wavelength: float = 1.0,
    resolution: int = 200,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """3D visualization of E and B vectors along propagation axis.

    Art. 791: Three-dimensional view showing E vectors (red arrows)
    and B vectors (blue arrows) perpendicular to the propagation
    direction (z-axis), illustrating the transverse nature of
    electromagnetic waves.

    Args:
        E0: Electric field amplitude (statvolts/cm).
        wavelength: Wavelength lambda (cm).
        resolution: Number of sample points.
        ax: Existing 3D axes (optional).

    Returns:
        Tuple of (Figure, Axes) with 3D projection.
    """
```

**Plot elements:**
- 3D axes with propagation along z
- Red arrows for E vectors (along x)
- Blue arrows for B vectors (along y)
- Envelope curves showing sinusoidal variation
- Orthogonal axis labels

### New File: `tests/test_vis_em_wave_propagation.py` (10 tests)

| # | Test Name | Verification |
|---|-----------|-------------|
| 1 | `test_E_perpendicular_B` | E dot B = 0 at all points |
| 2 | `test_E_B_ratio_equals_c` | |E|/|B| = c (within tolerance) |
| 3 | `test_wave_speed_omega_over_k` | Propagation speed = omega/k |
| 4 | `test_linear_polarization_Ey_zero` | Linear pol: E_y = 0 |
| 5 | `test_circular_polarization_equal_amplitudes` | Circular: |E_x| = |E_y| |
| 6 | `test_elliptical_polarization` | Elliptical produces valid Stokes parameters |
| 7 | `test_plot_returns_fig_ax` | plot_em_wave_propagation returns (Figure, Axes) |
| 8 | `test_plot_3d_returns_fig_ax` | plot_wave_snapshot_3d returns (Figure, Axes) |
| 9 | `test_default_args` | Works with no arguments |
| 10 | `test_no_nan_inf` | Output contains no NaN or Inf |

### Files to Create
- `maxwell/vis/em_wave_propagation.py`
- `tests/test_vis_em_wave_propagation.py`

### Files to Modify
- `maxwell/vis/__init__.py` -- Add exports
- `tests/test_vis.py` -- Add integration test

---

## Work Item 5: Lagrangian Kernel Scaffolding (Layer 52)

### Physics Dependency
Pattern reference from `maxwell/jax/core/charge.py`:
- Uses `jax.numpy` exclusively
- `@jax_tree` decorator for pytree registration
- `jax.grad()` for automatic differentiation
- `jax.jit` for compilation
- `vmap` for batched evaluation
- Safe division via `safe_div` from `_compat`

### New Package: `maxwell/dynamics/`

#### File 1: `maxwell/dynamics/__init__.py`
```python
"""maxwell.dynamics -- Lagrangian and Hamiltonian dynamics kernel.

Provides energy-based force derivation using JAX auto-differentiation,
implementing Maxwell's variational approach to mechanics (Layer 52).

Submodules:
    lagrangian -- Lagrangian formulation with JAX auto-diff
"""

from __future__ import annotations

__all__ = [
    "GeneralizedSystem",
]

from maxwell.dynamics.lagrangian import GeneralizedSystem
```

#### File 2: `maxwell/dynamics/lagrangian.py`
```python
"""maxwell.dynamics.lagrangian -- Lagrangian formulation for force derivation.

Implements Maxwell's variational approach: forces derived from energy
gradients via JAX automatic differentiation, eliminating manual
derivative computation.

Layer 52: The Lagrangian kernel provides the foundation for:
- Electrostatic forces from potential energy gradients
- Magnetic forces from field energy derivatives
- Generalized forces in arbitrary coordinate systems

Key principle: F = d/dt(dL/dq_dot) - dL/dq where L = T - U

References:
    Maxwell's Treatise: variational methods in mechanics.
    Lagrangian mechanics: energy-based force derivation.
"""

from __future__ import annotations

from typing import Callable, Optional
import jax
import jax.numpy as jnp
from jax import grad, jit, vmap

from maxwell.jax._compat import jax_tree


@jax_tree
class GeneralizedSystem:
    """Lagrangian formulation for deriving forces from energy via JAX auto-diff.

    The generalized system takes potential and kinetic energy functions
    and derives equations of motion through automatic differentiation.

    This implements the Euler-Lagrange equation:
        d/dt(dL/dq_dot) - dL/dq = 0

    where L = T(q, q_dot) - U(q).

    Attributes:
        potential_fn: Callable U(q) -> float (potential energy).
        kinetic_fn: Callable T(q, q_dot) -> float (kinetic energy).
    """

    def __init__(
        self,
        potential_fn: Optional[Callable] = None,
        kinetic_fn: Optional[Callable] = None,
    ):
        """Initialize with potential and kinetic energy functions.

        Args:
            potential_fn: U(q) -- potential energy as function of generalized
                         coordinates. If None, uses zero potential.
            kinetic_fn: T(q, q_dot) -- kinetic energy as function of coordinates
                       and velocities. If None, uses T = 0.5 * m * q_dot^2
                       with m=1.
        """
        self._potential_fn = potential_fn or (lambda q: 0.0)
        self._kinetic_fn = kinetic_fn or (lambda q, q_dot: 0.5 * jnp.sum(q_dot ** 2))

    def potential_energy(self, q: jax.Array) -> jax.Array:
        """U(q) -- potential energy at generalized coordinates.

        Args:
            q: Generalized coordinates, shape (n,).

        Returns:
            Potential energy scalar.
        """
        return self._potential_fn(q)

    def kinetic_energy(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """T(q, q_dot) -- kinetic energy.

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Kinetic energy scalar.
        """
        return self._kinetic_fn(q, q_dot)

    def lagrangian(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """L = T - U -- the Lagrangian.

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Lagrangian value (scalar).
        """
        return self.kinetic_energy(q, q_dot) - self.potential_energy(q)

    def derive_forces(self, q: jax.Array, q_dot: jax.Array) -> jax.Array:
        """F = d/dt(dL/dq_dot) - dL/dq using JAX grad.

        Computes generalized forces via the Euler-Lagrange equation:
            F_i = d/dt(dL/dq_dot_i) - dL/dq_i

        For static (time-independent) systems, this simplifies to:
            F = -dU/dq  (force = negative gradient of potential)

        Args:
            q: Generalized coordinates, shape (n,).
            q_dot: Generalized velocities, shape (n,).

        Returns:
            Generalized force vector, shape (n,).
        """
        # Partial derivative of L w.r.t. q: dL/dq
        dL_dq = grad(lambda q_: self.lagrangian(q_, q_dot))(q)

        # Partial derivative of L w.r.t. q_dot: dL/dq_dot
        dL_dqdot = grad(lambda qd_: self.lagrangian(q, qd_))(q_dot)

        # For static systems: F = -dL/dq (since d/dt(dL/dq_dot) = 0)
        # For dynamic systems, the caller computes d/dt(dL/dq_dot) separately
        return -dL_dq

    def derive_electrostatic_force(
        self,
        q1: float,
        q2: float,
        r: jax.Array,
    ) -> jax.Array:
        """Derive Coulomb force from U = q1*q2/|r| via auto-diff.

        Proof-of-concept: starting from electrostatic potential energy,
        derive the force vector and verify it matches Coulomb's law:

            F = q1*q2 * r_hat / r^2

        Args:
            q1: Charge 1 (esu).
            q2: Charge 2 (esu).
            r: Separation vector from q1 to q2, shape (3,).

        Returns:
            Force on q2 due to q1, shape (3,).
        """
        def potential(r_vec):
            r_mag = jnp.linalg.norm(r_vec)
            return q1 * q2 / jnp.maximum(r_mag, 1e-30)

        # F = -dU/dr (force = negative gradient of potential)
        force = -grad(potential)(r)
        return force

    @staticmethod
    @jit
    def coulomb_force_direct(q1: float, q2: float, r: jax.Array) -> jax.Array:
        """Direct Coulomb force calculation for verification.

        F = q1 * q2 * r / |r|^3

        Args:
            q1: Charge 1 (esu).
            q2: Charge 2 (esu).
            r: Separation vector, shape (3,).

        Returns:
            Force vector, shape (3,).
        """
        r_mag = jnp.linalg.norm(r)
        r_mag_cubed = jnp.maximum(r_mag ** 3, 1e-30)
        return q1 * q2 * r / r_mag_cubed
```

### New File: `tests/test_lagrangian.py` (15 tests)

| # | Test Name | Verification |
|---|-----------|-------------|
| 1 | `test_lagrangian_equals_T_minus_U` | L = T - U |
| 2 | `test_potential_energy` | U(q) returns correct value |
| 3 | `test_kinetic_energy_default` | Default T = 0.5 * sum(q_dot^2) |
| 4 | `test_force_derivation_coulomb` | Derived force matches Coulomb's law |
| 5 | `test_coulomb_force_magnitude` | |F| = q1*q2/r^2 |
| 6 | `test_coulomb_force_direction` | Force direction = r_hat |
| 7 | `test_gradient_computation` | jax.grad works on lagrangian |
| 8 | `test_jit_compatibility` | JIT-compiled coulomb_force_direct works |
| 9 | `test_custom_potential_fn` | Custom potential function works |
| 10 | `test_custom_kinetic_fn` | Custom kinetic function works |
| 11 | `test_derive_forces_static` | Static force = -dU/dq |
| 12 | `test_electrostatic_force_sign` | Like charges repel, opposite attract |
| 13 | `test_zero_separation_safety` | No division by zero at r=0 |
| 14 | `test_pytree_registration` | GeneralizedSystem works with jax.tree_util |
| 15 | `test_batched_force_derivation` | vmap works over multiple positions |

### Files to Create
- `maxwell/dynamics/__init__.py`
- `maxwell/dynamics/lagrangian.py`
- `tests/test_lagrangian.py`

### Files to Modify
- `pyproject.toml` -- Ensure `maxwell.dynamics` is included (should be auto-discovered)
- `maxwell/__init__.py` -- Optionally add dynamics to top-level exports

---

## File Modification Checklist

### New Files (5)
1. `maxwell/vis/dielectric_soakage.py`
2. `maxwell/vis/hysteresis_loops.py`
3. `maxwell/vis/em_wave_propagation.py`
4. `maxwell/dynamics/__init__.py`
5. `maxwell/dynamics/lagrangian.py`

### New Test Files (4)
1. `tests/test_vis_dielectric_soakage.py`
2. `tests/test_vis_hysteresis_loops.py`
3. `tests/test_vis_em_wave_propagation.py`
4. `tests/test_lagrangian.py`

### Modified Files (3)
1. `maxwell/vis/__init__.py` -- Add exports for 3 new visualization modules
2. `tests/test_vis.py` -- Add integration tests for new exports
3. `maxwell/__init__.py` -- Optionally add `dynamics` export

---

## Quality Gates

### Code Standards
- All files: `from __future__ import annotations`
- All functions: type hints on parameters and return values
- All functions: docstrings with Args/Returns/References sections
- All visualizations: use `maxwell.vis._compat` for matplotlib imports
- All visualizations: `require_matplotlib()` before creating figures
- All JAX code: use `jax.numpy` exclusively, no `numpy` in compute paths
- Follow Black formatting (line-length 88)
- Follow isort import ordering

### Test Standards
- pytest markers: `@pytest.mark.visualization` for vis tests, `@pytest.mark.jax` for Lagrangian tests
- All plot tests: close figures with `mplt.close(fig)` after assertions
- All calc tests: verify no NaN/Inf in outputs
- Numerical tests: use `np.isclose()` with appropriate tolerances
- Each test class: grouped by module/functionality

### Documentation Standards
- Art. references in docstrings (Maxwell article numbers)
- Physical units specified in docstrings (CGS-EMU)
- Cross-references to physics dependency modules

---

## Post-Implementation Verification

```bash
# 1. Build validation
python -m build
twine check dist/*

# 2. Run all new tests
pytest tests/test_vis_dielectric_soakage.py -v
pytest tests/test_vis_hysteresis_loops.py -v
pytest tests/test_vis_em_wave_propagation.py -v
pytest tests/test_lagrangian.py -v

# 3. Run full test suite (regression check)
pytest tests/ -v --tb=short

# 4. Run existing vis tests (ensure no breakage)
pytest tests/test_vis.py -v

# 5. Type check (optional)
mypy maxwell/vis/dielectric_soakage.py maxwell/vis/hysteresis_loops.py maxwell/vis/em_wave_propagation.py maxwell/dynamics/

# 6. Format check
black --check maxwell/vis/ maxwell/dynamics/
isort --check maxwell/vis/ maxwell/dynamics/
```

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| matplotlib not available in CI | Test skip | Already handled via `pytestmark` pattern in test_vis.py |
| JAX not available in CI | Test skip | Use `@pytest.mark.jax` marker |
| 3D plot backend issues | Visual artifacts | Use `Agg` backend (already set in _compat) |
| Lagrangian grad accuracy | Numerical errors | Verify against analytical Coulomb force |
| Test count targets missed | Quality gap | Ensure minimum test counts per item |

---

## Acceptance Criteria (Cycle 7 Complete)

- [ ] Work Item 1: `python -m build` and `twine check` pass cleanly
- [ ] Work Item 2: `maxwell/vis/dielectric_soakage.py` created with 2 functions, 10 tests passing
- [ ] Work Item 3: `maxwell/vis/hysteresis_loops.py` created with 3 functions, 10 tests passing
- [ ] Work Item 4: `maxwell/vis/em_wave_propagation.py` created with 3 functions, 10 tests passing
- [ ] Work Item 5: `maxwell/dynamics/` package created with `GeneralizedSystem`, 15 tests passing
- [ ] All existing tests continue to pass (no regressions)
- [ ] `maxwell.vis` package exports all new functions
- [ ] Total new tests: ~45 (10 + 10 + 10 + 15)
- [ ] Code formatted with Black and isort
