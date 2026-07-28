# Maxwell Modernized -- Strategic Roadmap & Multi-Phase Execution Plan

**Author:** Dr. Sarah Kim, Technical Product Strategist & Engineering Lead
**Date:** 2026-04-26
**Branch:** feat/treatise-100-coverage
**Version Target:** 0.1.0 (PyPI Release) -> 1.0.0 (Production)

---

## Executive Summary

The Maxwell Modernized project has achieved a historic milestone: 100% computational coverage of all 866 articles in Maxwell's 1873 Treatise. With 241 Python modules, 548 passing tests, and a robust `@maxwell_cite` traceability system, the project is positioned for a production-quality PyPI release.

This roadmap defines **8 sequential phases** beyond the just-completed Phase 1 (electrostatic visualization), covering: production readiness, visualization expansion, numerical verification, cross-framework integration, academic publication, and architectural consolidation. The total estimated scope spans approximately **280-320 new/modified modules** across all phases.

---

## Current State Baseline

| Metric | Current Value | Status |
|--------|--------------|--------|
| Articles covered | 866 / 866 | 100% |
| Python modules | 241 (170 .py + 71 __init__.py) | Complete |
| Non-init modules | 93 | Complete |
| Subpackages | 81 directories | Complete |
| Tests | 548 (522 original + 23 visualization + 3 version sync) | 100% passing |
| Math validation | 50 / 50 | 100% passing |
| Test matrix | 3 OS x 3 Python versions | CI active |
| Version | 0.1.0 | Pre-release |
| PyPI readiness | ~65% | Needs work |

### Critical Gaps Identified

| Gap | Severity | Count |
|-----|----------|-------|
| Empty `__init__.py` stub packages | High | 24 packages |
| Missing `__all__` declarations | Medium | ~50 packages |
| No `CITATION.cff` | High | 1 file |
| Minimal `CHANGELOG.md` | Medium | Incomplete |
| No README badges | Low | Cosmetic |
| No visualization beyond 2D | Medium | Phase 2+ |
| No numerical verification suite | High | Phase 3+ |
| No JOSS paper | High | Phase 4+ |
| No cross-framework adapters | Medium | Phase 5+ |

---

## Phase Roadmap Overview

```
Phase 0 (Done):  Deprecation fix + viz scaffold
Phase 1 (Done):  Electrostatic visualization engine
Phase 2:         PyPI Production Readiness (v0.1.0)
Phase 3:         Visualization Expansion (v0.2.0)
Phase 4:         Numerical Verification Suite (v0.3.0)
Phase 5:         Architecture Map Gap Resolution (v0.4.0)
Phase 6:         Cross-Framework Integration (v0.5.0)
Phase 7:         JOSS Paper & Academic Positioning (v0.6.0)
Phase 8:         Performance & Production Hardening (v1.0.0)
```

---

## PHASE 2: PyPI Production Readiness

**Objective:** Transform the current development artifact into a professional, PyPI-ready Python package.
**Target Version:** 0.1.0
**Estimated Duration:** 1-2 sprints (10-14 days)
**Estimated Module/Files Changed:** 25-30 files
**Risk Level:** Low (documentation and packaging only)

### 2.1 CITATION.cff File

**File:** `./CITATION.cff`

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "Maxwell Modernized"
version: 0.1.0
date-released: 2026-04-25
url: "https://github.com/maxwell-treatise/modernized-program"
repository-code: "https://github.com/maxwell-treatise/modernized-program"
license: MIT
type: software
authors:
  - family-names: Mikinka
    given-names: Anthony
    orcid: "https://orcid.org/0000-0000-0000-0000"
  - orcid: "https://orcid.org/0000-0000-0000-0000"
    family-names: Maxwell
    given-names: James Clerk
    role: Original author (Treatise on Electricity and Magnetism, 1873)
keywords:
  - electromagnetism
  - computational-physics
  - maxwell-equations
  - classical-physics
  - cgcs-units
  - spherical-harmonics
  - maxwell-treatise
abstract: >
  A complete computational implementation of James Clerk Maxwell's 1873
  A Treatise on Electricity and Magnetism. All 866 articles are implemented
  in Python with CGS-EMU units and citation-based traceability.
references:
  - type: article
    value: "Maxwell, J. C. (1873). A Treatise on Electricity and Magnetism. Oxford: Clarendon Press."
```

**Action:** Create the file. This is a zero-risk, high-impact addition. Required for academic credibility.

### 2.2 CHANGELOG.md Enhancement

**File:** `./CHANGELOG.md`

The current CHANGELOG has a single entry for v0.1.0. It needs to be expanded to follow Keep a Changelog conventions with clear separation of Added/Changed/Fixed/Removed categories across the project history. The CHANGELOG must also link to the CHANGELOG URL in `pyproject.toml` (line 71).

**Required additions:**
- Historical entries for all pre-v0.1.0 milestones
- Separate sections for Phase 0.1 (spherical harmonic fix), Phase 0.2 (viz scaffold), Phase 1 (vis engine)
- Add `[Unreleased]` section for future work

### 2.3 README Badge Integration

**File:** `./README.md`

Add the following badge block immediately after the `# Maxwell Modernized` header:

```markdown
[![Tests](https://github.com/maxwell-treatise/modernized-program/actions/workflows/test.yml/badge.svg)](https://github.com/maxwell-treatise/modernized-program/actions/workflows/test.yml)
[![Math Verification](https://github.com/maxwell-treatise/modernized-program/actions/workflows/math-verification.yml/badge.svg)](https://github.com/maxwell-treatise/modernized-program/actions/workflows/math-verification.yml)
[![Coverage](https://img.shields.io/badge/coverage-866%2F866%20articles-brightgreen)](docs/COVERAGE_SUMMARY.md)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

**Actions:**
1. Insert badge block after title
2. Add a brief "Metrics at a Glance" table with module count, test count, article coverage
3. Add installation section that mentions `[viz]` optional dependency
4. Add "Citing This Work" section referencing CITATION.cff

### 2.4 __all__ Declaration Audit

**Scope:** All 77 `__init__.py` files across the codebase.

**Current Status:** 47 packages have `__all__` declarations. 30 packages do not.

**Strategy:** For packages that are purely internal (no public API intended), leave without `__all__`. For packages that expose public API, add `__all__` with explicit exports.

**Packages requiring `__all__` audit and addition:**

| Package | Has __all__ | Action |
|---------|-----------|--------|
| `maxwell/chemistry/` | No (empty init) | SKIP (stub package) |
| `maxwell/kinematics/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetics/` | No (empty init) | SKIP (stub package) |
| `maxwell/telecom/` | No (empty init) | SKIP (stub package) |
| `maxwell/thermodynamics/` | No (empty init) | SKIP (stub package) |
| `maxwell/sim/` | No (empty init) | SKIP (stub package) |
| `maxwell/electromagnetism/field_theory/` | No (empty init) | SKIP (stub package) |
| `maxwell/electromagnetism/units/` | No (empty init) | SKIP (stub package) |
| `maxwell/electromagnetism/waves/` | No (empty init) | Add __all__ if has exports |
| `maxwell/materials/database/` | No (empty init) | SKIP (stub package) |
| `maxwell/meta/` | No (empty init) | Add __all__ with `maxwell_cite`, `get_citation`, `get_all_citations` |
| `maxwell/magnetism/calculus/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/components/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/core/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/fields/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/geometry/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/geophysics/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/instruments/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/materials/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/mechanics/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/physics/` | No (empty init) | SKIP (stub package) |
| `maxwell/magnetism/solvers/` | No (empty init) | SKIP (stub package) |
| `maxwell/core/math/` | No (empty init) | SKIP (stub package) |
| `maxwell/core/space/` | No (empty init) | SKIP (stub package) |
| `maxwell/core/units/` | Yes | VERIFY completeness |
| `maxwell/math/algebra/` | Need check | Add if has exports |
| `maxwell/math/geometry/` | Need check | Add if has exports |
| `maxwell/visualization/` | N/A | New in Phase 3 |

**Decision Framework:** 24 stub packages with empty `__init__.py` files are design artifacts from the architecture mapping exercise. They should NOT receive `__all__` declarations because they have no exports. Instead, they should be documented as "reserved namespaces" with docstrings indicating the intended future content.

### 2.5 Reserved Namespace Documentation

**Files to create:** All 24 empty `__init__.py` files

Replace each empty `__init__.py` stub with a proper docstring:

```python
"""Reserved namespace: maxwell.<package>.

This namespace is reserved for future implementation.
See the architecture map in docs/STRATEGIC_ROADMAP.md for planned content.
"""
```

**Packages to document:**
1. `maxwell/chemistry/`
2. `maxwell/kinematics/`
3. `maxwell/magnetics/`
4. `maxwell/telecom/`
5. `maxwell/thermodynamics/`
6. `maxwell/sim/`
7. `maxwell/electromagnetism/field_theory/`
8. `maxwell/electromagnetism/units/`
9. `maxwell/materials/database/`
10. `maxwell/magnetism/calculus/`
11. `maxwell/magnetism/components/`
12. `maxwell/magnetism/core/`
13. `maxwell/magnetism/fields/`
14. `maxwell/magnetism/geometry/`
15. `maxwell/magnetism/geophysics/`
16. `maxwell/magnetism/instruments/`
17. `maxwell/magnetism/materials/`
18. `maxwell/magnetism/mechanics/`
19. `maxwell/magnetism/physics/`
20. `maxwell/magnetism/solvers/`
21. `maxwell/core/math/`
22. `maxwell/core/space/`
23. `maxwell/electromagnetism/waves/`
24. `maxwell/meta/`

### 2.6 Version and Metadata Consistency

**Files to audit:**
- `maxwell/__init__.py` -- `__version__ = "0.1.0"`
- `pyproject.toml` -- `version = "0.1.0"`
- `CHANGELOG.md` -- `[0.1.0] - 2026-04-25`
- `CITATION.cff` -- `version: 1.2.0` / `version: 0.1.0`

**Action:** Create a version sync check in CI that verifies all four sources agree. Add a test:

```python
def test_version_consistency():
    import maxwell
    from importlib.metadata import metadata
    meta = metadata("maxwell")
    assert maxwell.__version__ == meta["Version"]
```

### 2.7 MANIFEST.in Audit

**File:** `./MANIFEST.in`

The current MANIFEST.in exists (471 bytes). Verify it includes:
- `LICENSE`
- `README.md`
- `CHANGELOG.md`
- `CITATION.cff`
- `docs/` directory
- Exclude `.claude/`, `agents/`, `archive/`, `audit_logs/`, `build/`, `dist/`

### 2.8 PyPI Classifier Updates

**File:** `./pyproject.toml`

Current classifiers say `Development Status :: 3 - Alpha`. For v0.1.0 PyPI release, this is appropriate. For v1.0.0, update to `Development Status :: 4 - Beta`.

Add to classifiers:
```
"License :: OSI Approved :: MIT License",
"Natural Language :: English",
```

### 2.9 Phase 2 Deliverables Summary

| # | Deliverable | File(s) | Type |
|---|-----------|---------|------|
| 2.1 | CITATION.cff | `CITATION.cff` | NEW |
| 2.2 | Enhanced CHANGELOG | `CHANGELOG.md` | EDIT |
| 2.3 | README badges | `README.md` | EDIT |
| 2.4 | __all__ audit | 47 `__init__.py` files | REVIEW |
| 2.5 | Reserved namespace docs | 24 `__init__.py` files | EDIT |
| 2.6 | Version sync check | `tests/test_version_sync.py` | NEW |
| 2.7 | MANIFEST.in update | `MANIFEST.in` | EDIT |
| 2.8 | Classifier updates | `pyproject.toml` | EDIT |
| 2.9 | Zenodo DOI badge | `README.md` | EDIT |

---

## PHASE 3: Visualization Expansion

**Objective:** Expand the visualization engine from 2D electrostatic plots to a full-featured scientific visualization subsystem covering 3D fields, animations, hysteresis, and spherical harmonics.
**Target Version:** 0.2.0
**Estimated Duration:** 3-4 sprints (21-28 days)
**Estimated New Modules:** 25-35
**Risk Level:** Medium (new functionality, depends on matplotlib quality)

### 3.1 3D Field Visualization

**New package:** `maxwell/vis/field3d.py`

```python
def plot_3d_field_lines(
    E_func: Callable[[np.ndarray], np.ndarray],
    origins: Sequence[tuple[float, float, float]],
    max_length: float = 10.0,
    step_size: float = 0.05,
    n_lines: int = 24,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot 3D electric field lines from point sources.
    
    Integrates field line trajectories using RK4 from seed points
    arranged on a sphere around each charge origin.
    
    Args:
        E_func: Electric field function E(x, y, z) -> (Ex, Ey, Ez).
        origins: Sequence of (x, y, z) charge positions.
        max_length: Maximum field line integration length.
        step_size: RK4 integration step size.
        n_lines: Number of seed points per charge.
        ax: Optional matplotlib 3D axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_3d_coil_field(
    coil_radius: float,
    coil_center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    n_turns: int = 1,
    current: float = 1.0,
    grid_size: int = 20,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot 3D magnetic field from a circular coil.
    
    Uses the Biot-Savart law via maxwell.electromagnetism.components.circular_coils.
    
    Args:
        coil_radius: Radius of the coil in cm.
        coil_center: Center position (x, y, z) in cm.
        n_turns: Number of turns.
        current: Current in abamperes (CGS).
        grid_size: Resolution of the field grid.
        ax: Optional matplotlib 3D axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...
```

**Tests:** `tests/test_vis_field3d.py` -- 15 tests

**Dependencies:** matplotlib (already in [viz])

### 3.2 Hysteresis Loop Visualization

**New package:** `maxwell/vis/hysteresis.py`

```python
def plot_hysteresis_loop(
    model: HysteresisLoop,
    H_max: float = 10.0,
    n_points: int = 200,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot a B-H hysteresis loop from a HysteresisLoop model instance.
    
    Integrates the hysteresis model over a complete cycle and plots
    the resulting B(H) curve with annotations for coercivity,
    retentivity, and saturation.
    
    Args:
        model: HysteresisLoop instance (from maxwell.materials.hysteresis).
        H_max: Maximum applied field magnitude in Oe.
        n_points: Number of points per half-cycle.
        ax: Optional matplotlib axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_hysteresis_family(
    models: Sequence[HysteresisLoop],
    labels: Sequence[str] | None = None,
    H_max: float = 10.0,
    n_points: int = 200,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot multiple hysteresis loops on the same axes for comparison.
    
    Useful for comparing different materials (mu-metal, permalloy, iron, etc.).
    
    Args:
        models: Sequence of HysteresisLoop instances.
        labels: Optional material name labels for legend.
        H_max: Maximum applied field.
        n_points: Points per half-cycle.
        ax: Optional matplotlib axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_hysteresis_parameters(
    model: HysteresisLoop,
    H_max: float = 10.0,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot annotated hysteresis loop with parameter callouts.
    
    Labels coercive force, retentivity, saturation induction,
    and energy product (BH_max).
    
    Args:
        model: HysteresisLoop instance.
        H_max: Maximum applied field.
        ax: Optional matplotlib axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...
```

**Tests:** `tests/test_vis_hysteresis.py` -- 12 tests

### 3.3 Spherical Harmonic 3D Surface Plots

**New package:** `maxwell/vis/spherical_viz.py`

```python
def plot_spherical_harmonic_surface(
    l: int,
    m: int,
    n_points: int = 80,
    cmap: str = "RdBu_r",
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot |Y_lm(theta, phi)|^2 as a 3D radial surface.
    
    The surface radius at each (theta, phi) is proportional to
    the squared magnitude of the spherical harmonic, creating
    the characteristic orbital shapes familiar from quantum mechanics.
    
    Args:
        l: Angular momentum quantum number (l >= 0).
        m: Magnetic quantum number (-l <= m <= l).
        n_points: Resolution of the theta/phi grid.
        cmap: Colormap name.
        ax: Optional matplotlib 3D axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_spherical_harmonic_grid(
    l_max: int,
    n_points: int = 40,
    figsize: tuple[float, float] = (14, 14),
    cmap: str = "RdBu_r",
    **kwargs,
) -> Figure:
    """Plot a grid of spherical harmonic surfaces for l=0..l_max.
    
    Arranges all (l+1)^2 harmonics in a grid layout for visual comparison.
    
    Args:
        l_max: Maximum l value to plot.
        n_points: Resolution per subplot.
        figsize: Overall figure size.
        cmap: Colormap.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_spherical_harmonic_convergence(
    f_func: Callable[[float, float], float],
    l_max_sequence: Sequence[int] = (1, 2, 4, 8, 16),
    n_points: int = 40,
    figsize: tuple[float, float] = (16, 4),
    **kwargs,
) -> Figure:
    """Plot convergence of spherical harmonic expansion.
    
    Shows the approximation error as l_max increases for a given
    target function on the sphere.
    
    Args:
        f_func: Target function f(theta, phi).
        l_max_sequence: Sequence of l_max values to compare.
        n_points: Grid resolution.
        figsize: Figure size.
        
    Returns:
        Matplotlib Figure.
    """
    ...
```

**Tests:** `tests/test_vis_spherical.py` -- 10 tests

### 3.4 Time-Varying Field Animations

**New package:** `maxwell/vis/animations.py`

```python
def animate_plane_wave(
    frequency: float = 1e9,
    amplitude: float = 1.0,
    n_frames: int = 30,
    interval_ms: int = 100,
    grid_size: int = 40,
    ax: Axes | None = None,
    **kwargs,
) -> FuncAnimation:
    """Animate a plane electromagnetic wave propagating in z-direction.
    
    Shows E and B field vectors oscillating perpendicular to propagation.
    
    Args:
        frequency: Wave frequency in Hz.
        amplitude: Field amplitude (E-field magnitude).
        n_frames: Number of animation frames.
        interval_ms: Frame interval in milliseconds.
        grid_size: Spatial grid resolution.
        ax: Optional matplotlib axes.
        
    Returns:
        matplotlib.animation.FuncAnimation instance.
    """
    ...


def animate_dipole Radiation(
    frequency: float = 1e6,
    n_frames: int = 30,
    interval_ms: int = 100,
    grid_size: int = 30,
    ax: Axes | None = None,
    **kwargs,
) -> FuncAnimation:
    """Animate oscillating electric dipole radiation pattern.
    
    Shows the characteristic toroidal radiation pattern expanding
    outward from the dipole axis.
    
    Args:
        frequency: Oscillation frequency.
        n_frames: Animation frames.
        interval_ms: Frame interval.
        grid_size: Spatial resolution.
        ax: Optional axes.
        
    Returns:
        FuncAnimation instance.
    """
    ...


def animate_induction(
    B_func: Callable[[float, float, float, float], np.ndarray],
    loop_radius: float = 5.0,
    n_frames: int = 30,
    interval_ms: int = 100,
    ax: Axes | None = None,
    **kwargs,
) -> FuncAnimation:
    """Animate electromagnetic induction (Faraday's Law).
    
    Shows a conductive loop in a time-varying magnetic field
    with induced EMF displayed.
    
    Args:
        B_func: Time-varying B-field function B(x, y, z, t).
        loop_radius: Radius of the conductive loop.
        n_frames: Animation frames.
        interval_ms: Frame interval.
        ax: Optional axes.
        
    Returns:
        FuncAnimation instance.
    """
    ...
```

**Tests:** `tests/test_vis_animations.py` -- 8 tests

### 3.5 Polarization Visualization

**New package:** `maxwell/vis/polarization.py`

```python
def plot_polarization_state(
    Ex: float, Ey: float, delta: float,
    n_points: int = 100,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot the polarization ellipse of an electromagnetic wave.
    
    Visualizes the electric field vector tip trajectory over one period,
    showing linear, circular, or elliptical polarization.
    
    Args:
        Ex: E-field amplitude in x-direction.
        Ey: E-field amplitude in y-direction.
        delta: Phase difference between Ex and Ey (radians).
        n_points: Number of points on the ellipse.
        ax: Optional axes.
        
    Returns:
        Matplotlib Figure.
    """
    ...


def plot_jones_vector(
    Ex: float, Ey: float, delta: float,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot the Jones vector representation of polarization.
    
    Shows the complex Jones vector components as arrows in the
    complex plane.
    
    Args:
        Ex, Ey: Field amplitudes.
        delta: Phase difference.
        ax: Optional axes.
        
    Returns:
        Figure.
    """
    ...


def plot_poincare_sphere(
    states: Sequence[tuple[float, float, float]],
    labels: Sequence[str] | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot polarization states on the Poincare sphere.
    
    Each state is a point on the unit sphere representing
    (S1/S0, S2/S0, S3/S0) Stokes parameters.
    
    Args:
        states: Sequence of (S1, S2, S3) tuples.
        labels: Optional state labels.
        ax: Optional 3D axes.
        
    Returns:
        Figure.
    """
    ...
```

**Tests:** `tests/test_vis_polarization.py` -- 8 tests

### 3.6 Streamline Field Mapping (General Purpose)

**New package:** `maxwell/vis/streamlines.py`

```python
def plot_streamlines_2d(
    field_func: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    density: float = 1.0,
    color: str = "blue",
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot 2D streamlines for any vector field.
    
    General-purpose streamline plotting using matplotlib's streamplot.
    The field function should return (U, V) components on the grid.
    
    Args:
        field_func: Function returning (U, V) components.
        x_range: (x_min, x_max).
        y_range: (y_min, y_max).
        density: Streamline density (float, higher = more lines).
        color: Line color.
        ax: Optional axes.
        
    Returns:
        Figure.
    """
    ...


def plot_quiver_2d(
    field_func: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    nx: int = 20,
    ny: int = 20,
    ax: Axes | None = None,
    **kwargs,
) -> Figure:
    """Plot 2D vector field as arrows (quiver plot).
    
    Args:
        field_func: Vector field function.
        x_range, y_range: Domain bounds.
        nx, ny: Grid resolution.
        ax: Optional axes.
        
    Returns:
        Figure.
    """
    ...
```

**Tests:** `tests/test_vis_streamlines.py` -- 6 tests

### 3.7 vis Package Public API Expansion

**Update file:** `maxwell/vis/__init__.py`

```python
__all__ = [
    # Compatibility
    "HAS_MATPLOTLIB",
    "require_matplotlib",
    "create_figure",
    "save_figure",
    # Base utilities
    "create_meshgrid",
    "evaluate_on_grid",
    # 2D plotting (existing)
    "plot_field_lines_2d",
    "plot_dipole_field_lines",
    "plot_equipotentials_2d",
    "plot_dipole_equipotentials",
    "plot_stress_tensor_2d",
    "verify_stress_tensor_plot",
    # 3D plotting (Phase 3)
    "plot_3d_field_lines",
    "plot_3d_coil_field",
    # Hysteresis
    "plot_hysteresis_loop",
    "plot_hysteresis_family",
    "plot_hysteresis_parameters",
    # Spherical harmonics
    "plot_spherical_harmonic_surface",
    "plot_spherical_harmonic_grid",
    "plot_spherical_harmonic_convergence",
    # Animations
    "animate_plane_wave",
    "animate_dipole_radiation",
    "animate_induction",
    # Polarization
    "plot_polarization_state",
    "plot_jones_vector",
    "plot_poincare_sphere",
    # General streamlines
    "plot_streamlines_2d",
    "plot_quiver_2d",
]
```

### 3.8 Phase 3 Deliverables Summary

| # | Deliverable | Files | New Tests |
|---|-----------|-------|-----------|
| 3.1 | 3D field visualization | `vis/field3d.py` | 15 |
| 3.2 | Hysteresis plotting | `vis/hysteresis.py` | 12 |
| 3.3 | Spherical harmonic viz | `vis/spherical_viz.py` | 10 |
| 3.4 | Time-varying animations | `vis/animations.py` | 8 |
| 3.5 | Polarization viz | `vis/polarization.py` | 8 |
| 3.6 | Streamlines general | `vis/streamlines.py` | 6 |
| 3.7 | vis __init__ expansion | `vis/__init__.py` | (included above) |
| **Total** | | **6 new files** | **~59 new tests** |

---

## PHASE 4: Numerical Verification Suite

**Objective:** Build a systematic verification framework that validates every numerical module against known analytical solutions, convergence criteria, and cross-module consistency checks.
**Target Version:** 0.3.0
**Estimated Duration:** 3-4 sprints (21-28 days)
**Estimated New Modules:** 15-25
**Risk Level:** Medium-High (mathematical rigor required)

### 4.1 Verification Infrastructure

**New package:** `maxwell/verification/`

The existing `maxwell/verification/` package has 3 files with 6 classes but 0 functions (per COVERAGE_SUMMARY.md). It needs to be expanded significantly.

**New file:** `maxwell/verification/framework.py`

```python
class VerificationResult:
    """Container for a single verification test result."""
    module_name: str
    article_refs: tuple[int, ...]
    test_name: str
    expected: float
    actual: float
    relative_error: float
    tolerance: float
    passed: bool
    details: str | None


class VerificationSuite:
    """Orchestrates running all verification tests and collecting results."""
    
    def __init__(self, relative_tolerance: float = 1e-8):
        self.relative_tolerance = relative_tolerance
        self.results: list[VerificationResult] = []
    
    def run_all(self) -> dict[str, VerificationResult]:
        """Execute all registered verification tests.
        
        Returns:
            Dictionary mapping (module, test_name) to VerificationResult.
        """
        ...
    
    def run_by_module(self, module_name: str) -> dict[str, VerificationResult]:
        """Execute verification tests for a specific module."""
        ...
    
    def run_by_article(self, article: int) -> dict[str, VerificationResult]:
        """Execute all tests that reference a specific Maxwell article."""
        ...
    
    def summary(self) -> dict:
        """Generate summary statistics.
        
        Returns:
            {
                "total": int,
                "passed": int,
                "failed": int,
                "max_error": float,
                "mean_error": float,
                "by_module": {module: {passed, total}},
            }
        """
        ...
    
    def report_html(self, output_path: str | None = None) -> str:
        """Generate an HTML verification report.
        
        Includes per-test details, error distributions, and
        article-level coverage.
        """
        ...
```

**Tests:** `tests/test_verification_framework.py` -- 10 tests

### 4.2 Analytical Reference Solutions

**New file:** `maxwell/verification/analytical_solutions.py`

Reference solutions for each module category:

```python
# Electrostatics reference solutions
def reference_point_charge_field(
    q: float, r: np.ndarray, position: np.ndarray
) -> np.ndarray:
    """E = q * (r - r0) / |r - r0|^3 (CGS)."""
    ...


def reference_dipole_field(
    p: np.ndarray, r: np.ndarray
) -> np.ndarray:
    """E = [3(p.r_hat)r_hat - p] / r^3 (CGS)."""
    ...


def reference_sphere_capacitance(
    radius: float
) -> float:
    """C = R in CGS (electrostatic units)."""
    ...


def reference_parallel_plate_capacitance(
    area: float, separation: float, epsilon_r: float = 1.0
) -> float:
    """C = epsilon_r * A / (4*pi*d) in CGS."""
    ...


# Magnetism reference solutions
def reference_soloid_field(
    n_turns_per_cm: float, current: float, mu_r: float = 1.0
) -> float:
    """B = (4*pi/c) * n * I * mu_r (CGS)."""
    ...


def reference_circular_coil_center(
    radius: float, current: float, n_turns: int = 1
) -> float:
    """B = (2*pi*n*I) / (c*R) on axis at center (CGS)."""
    ...


def reference_earth_magnetic_field(
    latitude: float
) -> tuple[float, float, float]:
    """Dipole model of Earth's magnetic field at given latitude."""
    ...


# Wave propagation reference solutions
def reference_plane_wave_velocity(
    epsilon_r: float, mu_r: float
) -> float:
    """v = c / sqrt(epsilon_r * mu_r)."""
    ...


def reference_wave_impedance(
    epsilon_r: float, mu_r: float
) -> float:
    """Z = sqrt(mu_r / epsilon_r) * Z0 (in CGS, Z0 = 4*pi/c)."""
    ...


# Mathematical reference solutions
def reference_legendre_values(
    n: int, x: float
) -> float:
    """P_n(x) via Rodrigues formula."""
    ...


def reference_elliptic_K(
    m: float
) -> float:
    """Complete elliptic integral K(m) via arithmetic-geometric mean."""
    ...


def reference_elliptic_E(
    m: float
) -> float:
    """Complete elliptic integral E(m) via AGM."""
    ...
```

**Tests:** `tests/test_analytical_solutions.py` -- 20 tests

### 4.3 Module-Specific Verification Tests

**New file:** `maxwell/verification/module_checks.py`

One verification function per module group:

```python
def verify_spherical_harmonics() -> dict[str, VerificationResult]:
    """Verify spherical harmonic computations:
    - P_n(x) recurrence relations
    - Orthonormality of Y_lm
    - Addition theorem
    - Symmetry properties Y_{l,-m} = (-1)^m Y_{l,m}*
    - Convergence for known functions
    """
    ...


def verify_electrostatics() -> dict[str, VerificationResult]:
    """Verify electrostatic modules:
    - Point charge field at known distances
    - Dipole field comparison
    - Gauss law for various geometries
    - Image charge method for grounded plane
    - Capacitance formulas (sphere, parallel plate, coaxial)
    """
    ...


def verify_magnetism() -> dict[str, VerificationResult]:
    """Verify magnetic modules:
    - Solenoid field (analytical vs computed)
    - Circular coil on-axis field
    - Helmholtz coil uniformity
    - Earth field dipole model
    - Magnetic moment torque
    """
    ...


def verify_electromagnetism() -> dict[str, VerificationResult]:
    """Verify electromagnetism modules:
    - Lorentz force magnitude
    - Maxwell stress tensor symmetry and trace
    - Faraday induction EMF
    - Ampere-Maxwell consistency
    - Poynting vector conservation
    """
    ...


def verify_wave_propagation() -> dict[str, VerificationResult]:
    """Verify wave optics modules:
    - Wave equation solutions
    - Polarization states
    - Reflection/transmission at boundary
    - Faraday rotation angle
    - Radiation pressure
    """
    ...


def verify_units_and_dimensions() -> dict[str, VerificationResult]:
    """Verify unit system consistency:
    - ESU/EMU ratio = c
    - Dimensional analysis of all formulas
    - CGS to SI conversion accuracy
    - Permittivity/permeability consistency
    """
    ...
```

**Tests:** `tests/test_module_checks.py` -- 30 tests

### 4.4 Convergence Testing Framework

**New file:** `maxwell/verification/convergence.py`

```python
def test_spherical_harmonic_convergence(
    func_on_sphere: Callable[[float, float], float],
    l_max_sequence: Sequence[int] = (1, 2, 4, 8, 16, 32),
    n_grid_points: int = 100,
) -> dict:
    """Measure convergence rate of spherical harmonic expansion.
    
    Returns:
        {
            "l_values": [...],
            "errors": [...],
            "convergence_rate": float,  # slope of log-log plot
            "asymptotic": bool,
        }
    """
    ...


def test_grid_convergence(
    field_func: Callable,
    reference_func: Callable,
    grid_sequence: Sequence[int] = (10, 20, 40, 80, 160),
) -> dict:
    """Measure how error decreases with grid resolution.
    
    Used to verify that numerical integration converges at the
    expected rate (e.g., O(h^2) for trapezoidal rule).
    
    Returns:
        {
            "grid_sizes": [...],
            "errors": [...],
            "order": float,  # convergence order
        }
    """
    ...
```

**Tests:** `tests/test_convergence.py` -- 8 tests

### 4.5 Cross-Validation Between Modules

**New file:** `maxwell/verification/cross_validation.py`

```python
def validate_stress_energy_consistency() -> VerificationResult:
    """Verify that trace of stress tensor = -energy density.
    
    Cross-validates:
    - maxwell.electromagnetism.forces.stress_tensor
    - maxwell.electromagnetism.energy.magnetic
    - maxwell.electromagnetism.energy.electrostatic
    
    Expected: trace(T) = -(u_e + u_m) = -(E^2 + B^2) / (8*pi)
    """
    ...


def validate_faraday_lenz_consistency() -> VerificationResult:
    """Verify Faraday's law and Lenz's law are consistent.
    
    Cross-validates:
    - maxwell.electromagnetism.induction.faraday
    - maxwell.electromagnetism.induction.lenz
    
    Expected: EMF sign opposes flux change.
    """
    ...


def validate_maxwell_equations_self_consistency() -> VerificationResult:
    """Verify all 7 Maxwell equations are mutually consistent.
    
    Cross-validates:
    - maxwell.electromagnetism.theory.general_equations
    
    Checks:
    - div(B) = 0
    - Faraday's law: curl(E) = -d(B)/dt
    - Ampere-Maxwell: curl(B) = (1/c)(d(E)/dt + 4*pi*J)
    - Continuity: d(rho)/dt + div(J) = 0
    """
    ...


def validate_wave_equation_from_maxwell() -> VerificationResult:
    """Verify wave equation derived from Maxwell's equations.
    
    Cross-validates:
    - maxwell.electromagnetism.theory.general_equations
    - maxwell.electromagnetism.waves.wave_equation
    
    Expected: nabla^2 E = (1/c^2) d^2(E)/dt^2 in vacuum
    """
    ...
```

**Tests:** `tests/test_cross_validation.py` -- 10 tests

### 4.6 Unit Consistency Verification

**New file:** `maxwell/verification/unit_checker.py`

```python
def verify_all_module_units() -> dict[str, VerificationResult]:
    """Check that every module's output has the expected dimensions.
    
    Uses the MagneticDimensions class from maxwell.core.units to
    verify that computed quantities have the correct CGS dimensions.
    """
    ...


def verify_conversion_chain() -> VerificationResult:
    """Verify CGS <-> SI roundtrip conversion accuracy.
    
    CGS -> SI -> CGS should give back original value within tolerance.
    """
    ...
```

**Tests:** `tests/test_unit_checker.py` -- 6 tests

### 4.7 Phase 4 Deliverables Summary

| # | Deliverable | Files | New Tests |
|---|-----------|-------|-----------|
| 4.1 | Verification framework | `verification/framework.py` | 10 |
| 4.2 | Analytical solutions | `verification/analytical_solutions.py` | 20 |
| 4.3 | Module checks | `verification/module_checks.py` | 30 |
| 4.4 | Convergence testing | `verification/convergence.py` | 8 |
| 4.5 | Cross-validation | `verification/cross_validation.py` | 10 |
| 4.6 | Unit consistency | `verification/unit_checker.py` | 6 |
| **Total** | | **6 new files** | **~84 new tests** |

---

## PHASE 5: Architecture Map Gap Resolution

**Objective:** Resolve the architecture map audit finding (0/33 fully accurate, 10 partial, 23 missing) by either filling gaps with implementations or formally accepting them as design artifacts.
**Target Version:** 0.4.0
**Estimated Duration:** 4-5 sprints (28-35 days)
**Estimated New Modules:** 40-60
**Risk Level:** High (significant new content, requires deep physics knowledge)

### 5.1 Gap Assessment and Prioritization

The architecture audit found that many planned modules from the architecture maps do not have corresponding implementations. These fall into three categories:

**Category A -- Fill Immediately (Core Physics):**

These gaps represent missing physics that should be in the library for completeness.

| Gap Package | Planned Content | Priority | New Modules |
|-----------|----------------|----------|-------------|
| `maxwell/chemistry/` | Electrochemistry, Nernst equation | Low | 3-5 |
| `maxwell/thermodynamics/` | Thermodynamic relations in EM | Low | 3-5 |
| `maxwell/sim/` | Simulation framework | Medium | 5-8 |
| `maxwell/kinematics/` | Relativistic kinematics | Medium | 3-5 |
| `maxwell/magnetics/` | Static magnetic field solvers | High | 5-8 |
| `maxwell/telecom/` | Telegraphy equations (Arts. 340-350) | Medium | 3-5 |

**Category B -- Fill Later (Advanced/Specialized):**

| Gap Package | Planned Content | Priority | New Modules |
|-----------|----------------|----------|-------------|
| `maxwell/magnetism/*/` (9 subpackages) | All empty | Deferred | 0 (accept as reserved) |
| `maxwell/materials/database/` | Material property database | Medium | 5-10 |
| `maxwell/electromagnetism/field_theory/` | Advanced field theory | High | 8-12 |
| `maxwell/electromagnetism/units/` | Unit conversion framework | High | 3-5 |

**Category C -- Accept as Design Artifacts:**

The 24 empty `__init__.py` files should be accepted as reserved namespaces with proper documentation (see Phase 2.5). No implementations are required for v0.4.0.

### 5.2 Priority Fill: maxwell/magnetics/

**New package:** `maxwell/magnetics/`

```
maxwell/magnetics/
    __init__.py          # Already exists (empty) -> add docstring
    scalar_potential.py  # Magnetic scalar potential for current-free regions
    vector_potential.py  # Magnetic vector potential A = int(J/|r-r'|) dV'
    dipole_fields.py     # Dipole and multipole field calculations
    method_images.py     # Method of images for magnetic boundaries
    reluctance.py        # Magnetic circuit reluctance calculations
```

**Key functions:**

```python
# maxwell/magnetics/scalar_potential.py
@maxwell_cite(392, part=3, chapter="Magnetic Force")
def magnetic_scalar_potential(
    M: np.ndarray,
    observation_point: np.ndarray,
    source_geometry: dict,
) -> float:
    """Compute magnetic scalar potential from magnetized body.
    
    phi_m = int(M . grad(1/R)) dV  (CGS)
    
    Args:
        M: Magnetization vector (Mx, My, Mz).
        observation_point: (x, y, z) where potential is evaluated.
        source_geometry: Description of magnetized volume.
        
    Returns:
        Magnetic scalar potential in Oe*cm.
    """
    ...


# maxwell/magnetics/vector_potential.py
@maxwell_cite(540, part=4, chapter="Electromagnetic Induction")
def magnetic_vector_potential(
    current_density: Callable[[np.ndarray], np.ndarray],
    observation_point: np.ndarray,
    integration_volume: dict,
) -> np.ndarray:
    """Compute magnetic vector potential A = (1/c) int(J/R) dV.
    
    Args:
        current_density: J(x, y, z) current density function.
        observation_point: (x, y, z) where A is evaluated.
        integration_volume: Integration bounds.
        
    Returns:
        Vector potential (Ax, Ay, Az) in CGS units.
    """
    ...
```

### 5.3 Priority Fill: maxwell/materials/database/

**New package:** `maxwell/materials/database/`

```
maxwell/materials/database/
    __init__.py          # Already exists (empty) -> add docstring
    magnetic_materials.py # Curated magnetic property database
    dielectric_materials.py # Curated dielectric property database
    conductor_materials.py # Curated conductivity database
    query.py             # Material property lookup API
```

```python
# maxwell/materials/database/magnetic_materials.py
MAGNETIC_MATERIALS: dict[str, dict] = {
    "iron_annealed": {
        "mu_r_max": 200000,
        "mu_r_initial": 5000,
        "saturation_T": 2.15,
        "coercivity_Oe": 0.04,
        "retentivity_G": 21000,
        "density_gcm3": 7.87,
        "curie_temp_K": 1043,
        "article_refs": (371, 424),
    },
    "mu_metal": {
        "mu_r_max": 800000,
        "mu_r_initial": 20000,
        "saturation_T": 0.8,
        "coercivity_Oe": 0.005,
        "retentivity_G": 4000,
        "density_gcm3": 8.5,
        "curie_temp_K": 573,
        "article_refs": (424,),
    },
    # ... 15-20 more materials
}


def get_magnetic_material(name: str) -> dict:
    """Look up magnetic material properties by name."""
    ...


def find_materials_by_property(
    property_name: str,
    min_value: float | None = None,
    max_value: float | None = None,
) -> list[str]:
    """Find materials matching property constraints."""
    ...
```

### 5.4 Priority Fill: maxwell/electromagnetism/field_theory/

**New package:** `maxwell/electromagnetism/field_theory/`

```
maxwell/electromagnetism/field_theory/
    __init__.py          # Already exists (empty) -> add docstring
    green_functions.py   # Green's functions for EM boundary value problems
    mode_expansion.py    # Modal expansion of EM fields in cavities
    scattering.py        # Scattering theory for EM waves
    energy_momentum.py   # Energy-momentum tensor formalism
    lagrangian.py        # Lagrangian formulation of classical EM
```

### 5.5 Phase 5 Deliverables Summary

| # | Deliverable | Files | New Modules | New Tests |
|---|-----------|-------|-------------|-----------|
| 5.2 | magnetics package | 6 files | 6 | 25 |
| 5.3 | materials database | 5 files | 5 | 15 |
| 5.4 | field theory | 6 files | 6 | 20 |
| 5.6 | reserved namespace docs | 24 files | 0 | 0 |
| **Total** | | **41 files** | **17 new** | **~60 new tests** |

---

## PHASE 6: Cross-Framework Integration

**Objective:** Implement the highest-ROI interoperability adapters identified in INTEROP.md.
**Target Version:** 0.5.0
**Estimated Duration:** 4-6 sprints (28-42 days)
**Estimated New Modules:** 20-30
**Risk Level:** Medium-High (external dependencies, API stability)

### 6.1 JAX Adapter (Highest ROI per INTEROP.md)

**New package:** `maxwell/adapters/jax/`

```
maxwell/adapters/
    __init__.py
    jax/
        __init__.py
        core.py           # JAX-accelerated core primitives
        stress_tensor.py  # JIT-compiled stress tensor
        spherical_harmonics.py  # JAX spherical harmonics
        optimization.py   # Gradient-based coil optimization
```

```python
# maxwell/adapters/jax/core.py
import jax
import jax.numpy as jnp
from jax import jit, grad, vmap

def to_jax(arr: np.ndarray) -> jnp.ndarray:
    """Convert numpy array to JAX array, preserving device placement."""
    ...


def from_jax(arr: jnp.ndarray) -> np.ndarray:
    """Convert JAX array to numpy array."""
    ...


def get_default_device() -> str:
    """Return 'cuda', 'tpu', or 'cpu' based on available hardware."""
    ...


# maxwell/adapters/jax/stress_tensor.py
@jit
def stress_tensor_jax(
    E_field: jnp.ndarray,
    B_field: jnp.ndarray,
) -> jnp.ndarray:
    """JIT-compiled Maxwell stress tensor.
    
    Replaces the Python double-loop in stress_tensor.py with
    a JAX-compiled version that runs on GPU/TPU.
    
    Args:
        E_field: Electric field vector (3,).
        B_field: Magnetic field vector (3,).
        
    Returns:
        3x3 stress tensor as JAX array.
    """
    E2 = jnp.dot(E_field, E_field)
    B2 = jnp.dot(B_field, B_field)
    T = (jnp.outer(E_field, E_field) + jnp.outer(B_field, B_field)
         - 0.5 * jnp.eye(3) * (E2 + B2))
    return T / (4.0 * jnp.pi)


batch_stress = vmap(stress_tensor_jax, in_axes=(0, 0))
# batch_stress(E_grid, B_grid) processes 1000s of (E, B) pairs


# maxwell/adapters/jax/optimization.py
def optimize_coil_geometry(
    target_field: np.ndarray,
    target_position: np.ndarray,
    initial_radius: float = 5.0,
    initial_turns: int = 100,
    max_iterations: int = 200,
) -> dict:
    """Use JAX autodiff to optimize coil geometry for target field.
    
    Minimizes |B_computed - B_target|^2 with respect to
    (radius, turns, current) using gradient-based optimization.
    
    Returns:
        {
            "optimal_radius": float,
            "optimal_turns": int,
            "optimal_current": float,
            "final_error": float,
            "converged": bool,
            "iterations": int,
        }
    """
    ...
```

**Tests:** `tests/test_adapters_jax.py` -- 20 tests
**Dependencies:** `jax>=0.4.0` (optional, [jax] extra)

### 6.2 SymPy Verification Submodule

**New package:** `maxwell/symbolic/`

```
maxwell/symbolic/
    __init__.py
    stress_tensor.py   # Symbolic stress tensor proofs
    maxwell_eqs.py     # Symbolic Maxwell equation derivations
    spherical_harmonics.py  # Symbolic Legendre polynomial identities
    wave_equation.py   # Symbolic wave equation derivation
```

```python
# maxwell/symbolic/stress_tensor.py
import sympy as sp

def verify_stress_tensor_symmetry() -> sp.Matrix:
    """Symbolically prove T_ij = T_ji (stress tensor is symmetric)."""
    Ex, Ey, Ez = sp.symbols('Ex Ey Ez')
    Bx, By, Bz = sp.symbols('Bx By Bz')
    E = sp.Matrix([Ex, Ey, Ez])
    B = sp.Matrix([Bx, By, Bz])
    E2, B2 = E.dot(E), B.dot(B)
    T = (E * E.T + B * B.T - sp.eye(3) * (E2 + B2) / 2) / (4 * sp.pi)
    assert sp.simplify(T - T.T) == sp.zeros(3, 3)
    return T


def verify_stress_trace() -> sp.Symbol:
    """Symbolically prove trace(T) = -(E^2 + B^2) / (8*pi)."""
    ...
```

**Tests:** `tests/test_symbolic.py` -- 15 tests
**Dependencies:** `sympy>=1.12` (optional, [symbolic] extra)

### 6.3 Dask Parallelization

**New package:** `maxwell/parallel/`

```
maxwell/parallel/
    __init__.py
    energy.py          # Dask-parallel energy integration
    field_grid.py      # Dask-parallel field evaluation
    optimization.py    # Dask-parallel parameter sweeps
```

```python
# maxwell/parallel/energy.py
from dask import delayed, compute

@delayed
def compute_energy_density_at_point(
    position: tuple,
    H_func: callable,
    permeability: float,
) -> float:
    """Compute magnetic energy density at a single point (Dask delayed)."""
    H = np.asarray(H_func(position), dtype=np.float64)
    return (permeability / (8.0 * np.pi)) * np.dot(H, H)


def integrate_magnetic_energy_parallel(
    H_func: callable,
    x_range: tuple,
    y_range: tuple,
    z_range: tuple,
    n_points: int = 20,
    permeability: float = 1.0,
    n_workers: int | None = None,
) -> float:
    """Parallel magnetic energy integration using Dask.
    
    Replaces O(n^3) Python nested loop with embarrassingly
    parallel Dask task graph.
    
    Args:
        H_func: Magnetic field function H(x, y, z).
        x_range, y_range, z_range: Integration bounds.
        n_points: Points per dimension.
        permeability: Magnetic permeability.
        n_workers: Number of parallel workers (None = auto).
        
    Returns:
        Total magnetic energy in ergs (CGS).
    """
    ...
```

**Tests:** `tests/test_parallel.py` -- 10 tests
**Dependencies:** `dask>=2023.0` (optional, [parallel] extra)

### 6.4 Data Storage (h5py/Zarr)

**New package:** `maxwell/io/storage.py`

Extend the existing `maxwell/io/` package with HDF5/Zarr storage:

```python
def save_spherical_harmonic_expansion(
    filename: str,
    expansion: SphericalHarmonicExpansion,
    metadata: dict | None = None,
) -> str:
    """Save spherical harmonic coefficients to HDF5 file.
    
    Preserves metadata (max_l, article_refs, normalization).
    """
    ...


def load_spherical_harmonic_expansion(
    filename: str,
) -> SphericalHarmonicExpansion:
    """Load spherical harmonic expansion from HDF5 file."""
    ...


def save_hysteresis_loop(
    filename: str,
    loop: HysteresisLoop,
    material_name: str,
) -> str:
    """Save measured/computed hysteresis loop to HDF5."""
    ...
```

**Tests:** `tests/test_io_storage.py` -- 8 tests
**Dependencies:** `h5py>=3.0` (optional, [io] extra)

### 6.5 Adapter Package Structure

```
maxwell/adapters/
    __init__.py              # Detect available backends
    base.py                  # Abstract adapter interface
    numpy_backend.py         # Default (always available)
    jax_backend.py           # Optional [jax]
    sympy_backend.py         # Optional [symbolic]
```

**Tests:** `tests/test_adapters.py` -- 15 tests

### 6.6 Phase 6 Deliverables Summary

| # | Deliverable | Files | New Tests | Dependencies |
|---|-----------|-------|-----------|-------------|
| 6.1 | JAX adapter | 5 files | 20 | jax (optional) |
| 6.2 | SymPy verification | 5 files | 15 | sympy (optional) |
| 6.3 | Dask parallelization | 4 files | 10 | dask (optional) |
| 6.4 | HDF5/Zarr storage | 1 file (extend io/) | 8 | h5py (optional) |
| 6.5 | Adapter framework | 5 files | 15 | (none) |
| **Total** | | **20 new files** | **~68 new tests** | **4 optional deps** |

---

## PHASE 7: JOSS Paper & Academic Positioning

**Objective:** Publish in the Journal of Open Source Software and establish the project as a citable academic resource.
**Target Version:** 0.6.0
**Estimated Duration:** 2-3 sprints (14-21 days)
**Estimated New Files:** 8-12
**Risk Level:** Low (documentation and submission)

### 7.1 JOSS Paper

**New files:** `paper/paper.md`, `paper/paper.bib`

```markdown
# paper/paper.md

---
title: 'Maxwell Modernized: A Complete Computational Implementation of Maxwell''s 1873 Treatise on Electricity and Magnetism'
tags:
  - Python
  - electromagnetism
  - computational-physics
  - classical-physics
  - maxwell-equations
  - spherical-harmonics
  - CGS-units
  - history-of-physics
authors:
  - name: Anthony Mikinka
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Maxwell Modernization Project
    index: 1
date: 2026-04-26
bibliography: paper.bib
---

# Summary

James Clerk Maxwell's _A Treatise on Electricity and Magnetism_ (1873) is
one of the most influential works in the history of physics, unifying
electricity, magnetism, and light into a single theoretical framework
[@maxwell1873]. The Treatise comprises 866 articles organized into four parts,
spanning electrostatics, electrokinematics, magnetism, and electromagnetism.

Maxwell Modernized provides a complete computational re-implementation of
this Treatise in Python. Every one of the 866 articles is represented by
executable code, with full traceability via a `@maxwell_cite` decorator
that links each function to its source article(s).

The library implements classical electromagnetic theory in the CGS-EMU
unit system (the system Maxwell himself employed), with secondary SI
support. It includes spherical harmonics, elliptic integrals, vector
calculus operators, electromagnetic force calculations, field visualization,
and material property models.

# Statement of Need

[... discussion of gap in computational classical EM resources ...]
[... educational value for teaching Maxwell's original formulation ...]
[... research applications in inverse problems and FEM benchmarking ...]

# Statement of Range

[... key features, module structure, test coverage ...]

# Prior Art

[... comparison with other EM libraries: Meep, FEniCS, EMpy, etc. ...]

# Acknowledgments

[... funding, contributors, community ...]

# References
```

```bibtex
# paper/paper.bib
@book{maxwell1873,
  author = {Maxwell, James Clerk},
  title = {A Treatise on Electricity and Magnetism},
  publisher = {Clarendon Press},
  address = {Oxford},
  year = {1873},
  volume = {1},
  url = {https://archive.org/details/treatiseonelectric01maxw}
}

@book{maxwell1873vol2,
  author = {Maxwell, James Clerk},
  title = {A Treatise on Electricity and Magnetism},
  publisher = {Clarendon Press},
  address = {Oxford},
  year = {1873},
  volume = {2},
  url = {https://archive.org/details/treatiseonelectric02maxw}
}

@article{joss,
  author = {Arfon Smith and Andrea Zuzanella Rafter and others},
  title = {The Journal of Open Source Software},
  journal = {JOSS},
  year = {2026},
  url = {https://joss.theoj.org/}
}
```

### 7.2 Zenodo Integration

**File:** `.zenodo.json` (or configure via GitHub settings)

```json
{
  "title": "Maxwell Modernized",
  "description": "A complete computational implementation of Maxwell's 1873 Treatise on Electricity and Magnetism",
  "creators": [
    {
      "name": "Anthony Mikinka",
      "affiliation": "Maxwell Modernization Project"
    }
  ],
  "license": "MIT-License",
  "keywords": ["electromagnetism", "computational-physics", "maxwell", "classical-physics"],
  "upload_type": "software"
}
```

### 7.3 Additional Academic Infrastructure

| # | Deliverable | File | Description |
|---|-----------|------|-------------|
| 7.1 | JOSS paper | `paper/paper.md` | Full paper manuscript |
| 7.2 | JOSS bibliography | `paper/paper.bib` | BibTeX references |
| 7.3 | Zenodo config | `.zenodo.json` | DOI minting config |
| 7.4 | Contributing guide | `CONTRIBUTING.md` | Contributor guidelines |
| 7.5 | Code of conduct | `CODE_OF_CONDUCT.md` | Community standards |
| 7.6 | Security policy | `SECURITY.md` | Vulnerability reporting |
| 7.7 | Feature request template | `.github/ISSUE_TEMPLATE/feature.md` | Issue template |
| 7.8 | Bug report template | `.github/ISSUE_TEMPLATE/bug.md` | Issue template |

### 7.4 Phase 7 Deliverables Summary

| # | Deliverable | Files | Type |
|---|-----------|-------|------|
| 7.1 | JOSS paper | `paper/paper.md`, `paper/paper.bib` | NEW |
| 7.2 | Zenodo config | `.zenodo.json` | NEW |
| 7.3 | Contributing guide | `CONTRIBUTING.md` | NEW |
| 7.4 | Code of conduct | `CODE_OF_CONDUCT.md` | NEW |
| 7.5 | Security policy | `SECURITY.md` | NEW |
| 7.6 | Issue templates | 2 files in `.github/ISSUE_TEMPLATE/` | NEW |

---

## PHASE 8: Performance & Production Hardening

**Objective:** Achieve v1.0.0 production status with comprehensive testing, benchmarks, type safety, and performance guarantees.
**Target Version:** 1.0.0
**Estimated Duration:** 3-4 sprints (21-28 days)
**Estimated New Files:** 10-15
**Risk Level:** Medium

### 8.1 Comprehensive Type Annotations

**Scope:** All 241 Python modules.

**Current Status:** pyproject.toml has mypy configuration with `disallow_untyped_defs = true`, but this has not been enforced across the codebase.

**Actions:**
1. Run `mypy --strict maxwell/` and document all errors
2. Add type annotations to all public functions
3. Use `typing.Protocol` for array-like interfaces
4. Create `.pyi` stub files for critical modules
5. Add `--warn-unused-ignores` to CI

```python
# Example: Proper type annotations
from __future__ import annotations
from typing import Protocol, Sequence
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
Vec3 = tuple[float, float, float]

class FieldFunction(Protocol):
    def __call__(self, x: float, y: float, z: float) -> Vec3: ...

@maxwell_cite(528, 529, 530, part=4)
def faraday_induction(
    circuit: Circuit,
    magnetic_flux: FloatArray,
    dt: float = 1.0e-9,
) -> FloatArray:
    """..."""
    ...
```

### 8.2 Benchmark Suite

**New package:** `benchmarks/`

```
benchmarks/
    __init__.py
    benchmark_spherical_harmonics.py
    benchmark_stress_tensor.py
    benchmark_field_computation.py
    benchmark_energy_integration.py
    benchmark_network_solver.py
    conftest.py
```

```python
# benchmarks/benchmark_spherical_harmonics.py
import pytest
import numpy as np
from maxwell.math.spherical_harmonics import SphericalHarmonicExpansion


class BenchmarkSphericalHarmonics:
    def test_coefficient_computation_l10(self, benchmark):
        expansion = SphericalHarmonicExpansion(max_l=10)
        theta = np.linspace(0, np.pi, 50)
        phi = np.linspace(0, 2 * np.pi, 100)
        field = np.random.randn(50, 100)
        
        result = benchmark(expansion.compute_coefficients, field, theta, phi)
        assert len(result) == (10 + 1) ** 2

    def test_coefficient_computation_l20(self, benchmark):
        expansion = SphericalHarmonicExpansion(max_l=20)
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2 * np.pi, 200)
        field = np.random.randn(100, 200)
        
        result = benchmark(expansion.compute_coefficients, field, theta, phi)
        assert len(result) == (20 + 1) ** 2
```

### 8.3 CI Enhancement

**New workflow:** `.github/workflows/benchmarks.yml`

```yaml
name: Benchmarks

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - name: Run benchmarks
        run: pytest benchmarks/ --benchmark-only --benchmark-json=benchmark.json
      - name: Check performance regression
        run: |
          python scripts/check_benchmark_regression.py benchmark.json
```

**Update:** `.github/workflows/mypy.yml` -- add type checking workflow

### 8.4 API Stability Guarantees

**New file:** `maxwell/api_compat.py`

```python
"""API compatibility layer for stable public interface.

This module defines the stable public API surface. Breaking changes
to functions/classes listed here require a major version bump.

All other modules are considered internal and may change between
minor versions.
"""

STABLE_API = {
    "core": ["PointCharge", "ElectricField", "ElectricPotential",
             "Magnet", "MagneticMoment"],
    "constants": ["CONST", "C"],
    "forces": ["LorentzForce", "MaxwellStressTensor"],
    "induction": ["FaradayInduction"],
    "theory": ["MaxwellEquations", "ElectromagneticField"],
    "energy": ["calc_magnetic_energy_density",
               "calc_total_magnetic_energy",
               "calc_electrostatic_energy_density"],
    "math": ["SphericalHarmonicExpansion", "LegendrePolynomial",
             "EllipticIntegral"],
    # ... etc
}


def is_stable_api(module_path: str, name: str) -> bool:
    """Check if a given module.name is part of the stable API."""
    ...
```

### 8.5 Documentation Site

**New package:** `docs/api/`

Generate API documentation from docstrings:

```
docs/
    api/
        index.md
        core.md
        electrostatics.md
        electrokinematics.md
        electromagnetism.md
        magnetism.md
        math.md
        materials.md
        optics.md
        vis.md
        adapters.md
    tutorials/
        getting_started.ipynb
        electrostatics_tutorial.ipynb
        visualization_tutorial.ipynb
        spherical_harmonics_tutorial.ipynb
        cross_framework.ipynb
```

### 8.6 Phase 8 Deliverables Summary

| # | Deliverable | Files | Type |
|---|-----------|-------|------|
| 8.1 | Type annotations | All 241 modules | EDIT |
| 8.2 | Benchmark suite | 7 files in `benchmarks/` | NEW |
| 8.3 | CI enhancement | 2 new workflows + updates | NEW |
| 8.4 | API stability | `maxwell/api_compat.py` | NEW |
| 8.5 | Documentation site | ~15 files | NEW |
| 8.6 | Version bump to 1.0.0 | `pyproject.toml`, `__init__.py` | EDIT |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-----------|--------|------------|
| matplotlib API changes break vis | Medium | Medium | Pin matplotlib version, use [viz] optional |
| JAX API instability | Medium | Medium | Version pin jax, wrap in adapter pattern |
| Math verification fails for edge cases | Medium | High | Conservative tolerances, mark as known issues |
| JOSS paper rejection | Medium | High | Follow JOSS guidelines strictly, pre-submit inquiry |
| Architecture gaps take longer than expected | High | Medium | Accept gaps as design artifacts, prioritize by user impact |
| Type annotation effort exceeds estimate | High | Low | Phased approach, prioritize public API first |

---

## Resource Requirements

| Phase | Estimated Effort | Key Contributors | Dependencies |
|-------|-----------------|-----------------|-------------|
| Phase 2 (PyPI Readiness) | 10-14 days | 1 developer | None |
| Phase 3 (Visualization) | 21-28 days | 1-2 developers | matplotlib |
| Phase 4 (Verification) | 21-28 days | 1-2 developers (physics expertise) | None |
| Phase 5 (Architecture) | 28-35 days | 2-3 developers (physics expertise) | None |
| Phase 6 (Integration) | 28-42 days | 2 developers (framework expertise) | jax, sympy, dask, h5py |
| Phase 7 (JOSS) | 14-21 days | 1-2 authors | None |
| Phase 8 (Production) | 21-28 days | 2 developers | None |
| **TOTAL** | **~143-196 days** | **2-3 FTE** | **4 optional deps** |

---

## Recommended Execution Order

```
Week 1-2:    Phase 2 -- PyPI Readiness
Week 3-6:    Phase 3 -- Visualization Expansion (parallel with 4)
Week 3-6:    Phase 4 -- Verification Suite (parallel with 3)
Week 7-10:   Phase 5 -- Architecture Gap Resolution
Week 11-16:  Phase 6 -- Cross-Framework Integration
Week 17-19:  Phase 7 -- JOSS Paper
Week 20-24:  Phase 8 -- Production Hardening
```

**Critical Path:** Phase 2 -> Phase 4 -> Phase 8 (publication-ready quality)
**Parallelizable:** Phases 3, 5, 6 (independent feature work)
**Dependent:** Phase 7 depends on Phases 2-6 being substantially complete

---

## Success Criteria by Phase

### Phase 2 (PyPI Readiness)
- [ ] `pip install maxwell[viz]` works without errors
- [ ] All 241 modules import cleanly
- [ ] 548 tests pass on CI (3 OS x 3 Python versions)
- [ ] CITATION.cff validates with `cffconvert`
- [ ] README badges render correctly
- [ ] CHANGELOG follows Keep a Changelog format
- [ ] PyPI package page shows correct metadata

### Phase 3 (Visualization)
- [ ] All 6 new vis modules functional
- [ ] ~59 new vis tests passing
- [ ] 3D plots render correctly with matplotlib
- [ ] Animations play correctly
- [ ] Graceful degradation when matplotlib absent
- [ ] Visual output matches expected physics (qualitative review)

### Phase 4 (Verification)
- [ ] All module-specific verification tests pass
- [ ] Cross-validation checks pass
- [ ] Convergence rates match theoretical expectations
- [ ] HTML report generates correctly
- [ ] All 84 verification tests passing
- [ ] Maximum relative error < 1e-8 for all checks

### Phase 5 (Architecture)
- [ ] 17 new physics modules implemented
- [ ] All 24 stub packages documented
- [ ] Architecture map audit shows improvement
- [ ] 60 new tests passing
- [ ] No import errors across all packages

### Phase 6 (Integration)
- [ ] JAX adapter runs on GPU (if available)
- [ ] SymPy proofs verified
- [ ] Dask parallelization shows speedup
- [ ] HDF5 storage roundtrip preserves data
- [ ] 68 new adapter tests passing
- [ ] Optional dependencies gracefully degrade

### Phase 7 (JOSS)
- [ ] JOSS paper submitted
- [ ] Paper.md and paper.bib format correctly
- [ ] Zenodo DOI minted
- [ ] CONTRIBUTING.md published
- [ ] Issue templates functional

### Phase 8 (Production)
- [ ] mypy --strict passes on all public API
- [ ] Benchmark suite integrated in CI
- [ ] No performance regression in CI
- [ ] API stability layer documented
- [ ] Version bumped to 1.0.0
- [ ] All 548 + new tests passing
- [ ] Test coverage >= 90%

---

## Appendix A: Current Module Inventory by Package

| Package | Modules | Tests | Coverage | Notes |
|---------|---------|-------|----------|-------|
| maxwell/core/ | 12 | Good | Complete | Foundation -- solid |
| maxwell/config/ | 3 | Covered | Complete | Constants, conventions |
| maxwell/electrostatics/ | 10 | Good | Complete | Part I |
| maxwell/electrokinematics/ | 11 | Good | Complete | Part II |
| maxwell/magnetism/ | 3 | Good | Complete | Part III |
| maxwell/electromagnetism/ | 45 | Good | Complete | Part IV -- largest |
| maxwell/math/ | 9 | Good | Complete | Spherical harmonics, elliptic |
| maxwell/materials/ | 6 | Good | Complete | Hysteresis, constitutive |
| maxwell/optics/ | 9 | Moderate | Complete | Wave equation, polarization |
| maxwell/vis/ | 6 | Good (23) | NEW | Visualization (Phase 1) |
| maxwell/molecular/ | 5 | Moderate | Complete | Competing theories |
| maxwell/instruments/ | 7 | Moderate | Complete | Galvanometers, coils |
| maxwell/verification/ | 3 | None (0 funcs) | STUB | Needs Phase 4 work |
| maxwell/solvers/ | 3 | Moderate | Complete | Induction, shape |
| maxwell/vortex_engine/ | 6 | Moderate | Complete | Historical theory |
| maxwell/philosophy/ | 2 | Moderate | Complete | Medium check |
| maxwell/geometry/ | 3 | Moderate | Complete | Shells, solenoids |
| 24 stub packages | 24 | 0 | STUB | Need docs (Phase 2/5) |
| **TOTAL** | **241** | **548** | **100%** | **24 stubs** |

---

## Appendix B: Decision Matrix -- Architecture Map Gaps

| Gap | Fill vs. Accept | Rationale | Priority |
|-----|----------------|-----------|----------|
| `maxwell/magnetics/` | FILL | Static magnetic solvers complement existing modules | High |
| `maxwell/sim/` | FILL | Simulation framework enables Phase 3+ viz | High |
| `maxwell/electromagnetism/field_theory/` | FILL | Green's functions, scattering needed for FEM benchmark | High |
| `maxwell/materials/database/` | FILL | Material properties are frequently requested | Medium |
| `maxwell/kinematics/` | ACCEPT | Relativistic kinematics is out of scope for v1.0 | Low |
| `maxwell/chemistry/` | ACCEPT | Electrochemistry is a different domain | Low |
| `maxwell/thermodynamics/` | ACCEPT | Thermodynamics of EM is niche | Low |
| `maxwell/telecom/` | ACCEPT | Telegraphy is historical interest only | Low |
| `maxwell/magnetism/*/` (9 packages) | ACCEPT | All empty, subsumed by top-level magnetism | Low |
| `maxwell/core/math/`, `core/space/` | ACCEPT | Reserved, subsumed by maxwell/math/ | Low |
| `maxwell/electromagnetism/units/` | ACCEPT | Units handled by maxwell/core/units/ | Low |
| `maxwell/electromagnetism/waves/` | ACCEPT | Waves handled by maxwell/optics/ | Low |
| `maxwell/meta/` | ACCEPT (doc) | Single citation.py file, no expansion needed | Low |

---

## Appendix C: Inter-Phase Dependencies

```
Phase 2 (PyPI)
    |
    +---> Phase 3 (Visualization) ---+
    |                                 |
    +---> Phase 4 (Verification) -----+-----> Phase 7 (JOSS)
    |                                  |           |
    +---> Phase 5 (Architecture) ------+           |
    |                                  |           |
    +---> Phase 6 (Integration) -------+-----> Phase 8 (Production)
```

Phase 2 is the critical first step -- without PyPI readiness, all downstream
work is blocked from publication. Phase 4 (verification) provides the mathematical
credibility needed for Phase 7 (JOSS). Phase 6 (integration) can run in parallel
with most other phases but must complete before Phase 8 (production).

---

*Document prepared by Dr. Sarah Kim, Technical Product Strategist & Engineering Lead*
*Date: 2026-04-26*
*Review: Pending quality-reviewer and software-program-manager agent review*
