# Implementation Plan — Cycle 12 Audit Findings

> **Date:** 2026-05-06
> **Branch:** `feat/pypi-package`
> **Source:** Cycle 12 multi-agent audit
> **Scope:** `maxwell/vis/` — field_lines.py, equipotential.py, stress.py, `__init__.py`, `tests/test_vis.py`

---

## Table of Contents

1. [Tier 1 — Critical Consistency Fixes](#tier-1--critical-consistency-fixes)
2. [Tier 2 — Examples Directory](#tier-2--examples-directory)
3. [Tier 3 — Quality Infrastructure](#tier-3--quality-infrastructure)
4. [Type Annotation Unification](#type-annotation-unification)
5. [Implementation Order & Dependencies](#implementation-order--dependencies)
6. [Acceptance Criteria](#acceptance-criteria)

---

## Tier 1 — Critical Consistency Fixes

### Finding 1: Missing `@maxwell_cite` decorators

**Pattern established by:** `method_of_images.py` and `edge_singularities.py` — every public function carries a `@maxwell_cite` decorator with article number, part, chapter, and description.

**Affected files and functions:**

| File | Function | Maxwell Article | Part | Chapter |
|------|----------|----------------|------|---------|
| `field_lines.py` | `plot_field_lines_2d` | 52-61 | 1 | Lines of Force |
| `field_lines.py` | `plot_dipole_field_lines` | 52-61 | 1 | Lines of Force |
| `equipotential.py` | `plot_equipotentials_2d` | 16-19 | 1 | Equipotential Surfaces |
| `equipotential.py` | `plot_dipole_equipotentials` | 16-19 | 1 | Equipotential Surfaces |
| `stress.py` | `plot_stress_tensor_2d` | 616-620 | 4 | Stress in the Dielectric |
| `stress.py` | `verify_stress_tensor_plot` | 616-620 | 4 | Stress in the Dielectric |

#### Modification 1A: `maxwell/vis/field_lines.py`

**Line 18 (after existing imports), add:**
```python
from maxwell.meta.citation import maxwell_cite
```

**Line 20 — add decorator before `plot_field_lines_2d`:**
```python
@maxwell_cite(
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
    part=1,
    chapter="On the Lines of Electric Force",
    description="Plot 2D electric field lines using streamplot for arbitrary charge configurations.",
)
def plot_field_lines_2d(
```

**Line 108 — add decorator before `plot_dipole_field_lines`:**
```python
@maxwell_cite(
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
    part=1,
    chapter="On the Lines of Electric Force",
    description="Plot field lines for an electric dipole (convenience wrapper).",
)
def plot_dipole_field_lines(
```

#### Modification 1B: `maxwell/vis/equipotential.py`

**Line 17 (after existing imports), add:**
```python
from maxwell.meta.citation import maxwell_cite
```

**Line 20 — add decorator before `plot_equipotentials_2d`:**
```python
@maxwell_cite(
    16, 17, 18, 19,
    part=1,
    chapter="On Equipotential Surfaces and Lines of Force",
    description="Plot 2D equipotential contours for arbitrary potential functions.",
)
def plot_equipotentials_2d(
```

**Line 100 — add decorator before `plot_dipole_equipotentials`:**
```python
@maxwell_cite(
    16, 17, 18, 19,
    part=1,
    chapter="On Equipotential Surfaces and Lines of Force",
    description="Plot equipotential lines for an electric dipole (convenience wrapper).",
)
def plot_dipole_equipotentials(
```

#### Modification 1C: `maxwell/vis/stress.py`

**Line 17 (after existing imports), add:**
```python
from maxwell.meta.citation import maxwell_cite
```

**Line 20 — add decorator before `plot_stress_tensor_2d`:**
```python
@maxwell_cite(
    616, 617, 618, 619, 620,
    part=4,
    chapter="Electromagnetic Stress in the Dielectric",
    description="Plot Maxwell stress tensor as principal stress ellipses on a 2D field.",
)
def plot_stress_tensor_2d(
```

**Line 111 — add decorator before `verify_stress_tensor_plot`:**
```python
@maxwell_cite(
    616, 617, 618, 619, 620,
    part=4,
    chapter="Electromagnetic Stress in the Dielectric",
    description="Verify stress tensor properties: symmetry, trace, and eigenvalue reality.",
)
def verify_stress_tensor_plot(
```

---

### Finding 2: Unexported functions in `__init__.py`

Three functions exist in the vis modules but are not exported from the package:
- `plot_dipole_field_lines` (field_lines.py)
- `plot_dipole_equipotentials` (equipotential.py)
- `verify_stress_tensor_plot` (stress.py)

#### Modification 2: `maxwell/vis/__init__.py`

**After line 41**, add import for `plot_dipole_field_lines`:
```python
    from maxwell.vis.field_lines import (
        plot_field_lines_2d,
        plot_dipole_field_lines,
    )
```

**After line 42**, add import for `plot_dipole_equipotentials`:
```python
    from maxwell.vis.equipotential import (
        plot_equipotentials_2d,
        plot_dipole_equipotentials,
    )
```

**After line 43**, update stress import to include `verify_stress_tensor_plot`:
```python
    from maxwell.vis.stress import (
        plot_stress_tensor_2d,
        verify_stress_tensor_plot,
    )
```

**In the `__all__` list (line 116+), add after the existing vis entries:**
```python
        "plot_dipole_field_lines",
        "plot_dipole_equipotentials",
        "verify_stress_tensor_plot",
```

Exact insertion: Add `"plot_dipole_field_lines",` after `"plot_field_lines_2d",` on line 119. Add `"plot_dipole_equipotentials",` after `"plot_equipotentials_2d",` on line 120. Add `"verify_stress_tensor_plot",` after `"plot_stress_tensor_2d",` on line 121.

---

## Tier 2 — Examples Directory

Create `examples/` at the project root with 5 runnable scripts. Each script:
- Imports from `maxwell.vis` (public API)
- Generates a plot
- Saves a PNG to `examples/output/`
- Runs standalone: `python examples/<script_name>.py`

### Directory Structure
```
examples/
    __init__.py
    output/                     (git-ignored)
    01_dipole_field_lines.py
    02_equipotential_surfaces.py
    03_stress_tensor_visualization.py
    04_method_of_images_demo.py
    05_edge_singularity_study.py
```

### Script 1: `examples/01_dipole_field_lines.py`

**Purpose:** Demonstrate electric dipole field line plotting.
**Saves:** `examples/output/dipole_field_lines.png`

```python
"""Electric dipole field lines — Maxwell Part I, Arts. 52-61.

Generates a publication-quality plot of electric field lines for a dipole
configuration and saves it as a PNG.

Usage:
    python examples/01_dipole_field_lines.py
"""
from maxwell.vis import plot_dipole_field_lines

def main():
    fig = plot_dipole_field_lines(
        charge_magnitude=1.0,
        separation=2.0,
        x_min=-5.0, x_max=5.0,
        y_min=-5.0, y_max=5.0,
        nx=50, ny=50,
        density=1.5,
        cmap="autumn",
    )
    fig.savefig("examples/output/dipole_field_lines.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/dipole_field_lines.png")


if __name__ == "__main__":
    import os
    os.makedirs("examples/output", exist_ok=True)
    main()
```

### Script 2: `examples/02_equipotential_surfaces.py`

**Purpose:** Demonstrate equipotential contour plotting for a dipole.
**Saves:** `examples/output/dipole_equipotentials.png`

```python
"""Dipole equipotential surfaces — Maxwell Part I, Arts. 16-19.

Generates a publication-quality plot of equipotential lines for a dipole
and saves it as a PNG.

Usage:
    python examples/02_equipotential_surfaces.py
"""
from maxwell.vis import plot_dipole_equipotentials

def main():
    fig = plot_dipole_equipotentials(
        charge_magnitude=1.0,
        separation=2.0,
        x_min=-5.0, x_max=5.0,
        y_min=-5.0, y_max=5.0,
        nx=200, ny=200,
        n_levels=30,
        filled=True,
        cmap="RdBu_r",
    )
    fig.savefig("examples/output/dipole_equipotentials.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/dipole_equipotentials.png")


if __name__ == "__main__":
    import os
    os.makedirs("examples/output", exist_ok=True)
    main()
```

### Script 3: `examples/03_stress_tensor_visualization.py`

**Purpose:** Demonstrate Maxwell stress tensor visualization with verification.
**Saves:** `examples/output/stress_tensor.png`

```python
"""Maxwell stress tensor visualization — Maxwell Part IV, Arts. 616-620.

Generates a plot of the stress tensor for a uniform electric field, verifies
tensor properties, and saves the visualization as a PNG.

Usage:
    python examples/03_stress_tensor_visualization.py
"""
import numpy as np
from maxwell.vis import plot_stress_tensor_2d, verify_stress_tensor_plot

def main():
    # Define a uniform field for clean visualization
    def uniform_field(x, y):
        return np.ones_like(x) * 1.0, np.ones_like(y) * 0.5

    fig = plot_stress_tensor_2d(
        uniform_field,
        x_min=-5.0, x_max=5.0,
        y_min=-5.0, y_max=5.0,
        nx=30, ny=30,
        skip=2,
        quiver_scale=1.0,
        cmap="seismic",
    )
    fig.savefig("examples/output/stress_tensor.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/stress_tensor.png")

    # Verify tensor properties
    result = verify_stress_tensor_plot(
        E_field=(1.0, 2.0, 0.0),
        B_field=(0.0, 1.0, 3.0),
    )
    print(f"\nStress Tensor Verification:")
    print(f"  Symmetric: {result['symmetric']}")
    print(f"  Trace: {result['trace']:.6f}")
    print(f"  Expected trace: {result['expected_trace']:.6f}")
    print(f"  Trace error: {result['trace_error']:.2e}")
    print(f"  Energy density: {result['energy_density']:.6f}")


if __name__ == "__main__":
    import os
    os.makedirs("examples/output", exist_ok=True)
    main()
```

### Script 4: `examples/04_method_of_images_demo.py`

**Purpose:** Demonstrate Method of Images visualization (already decorated and exported).
**Saves:** `examples/output/method_of_images.png`

```python
"""Method of Images — Maxwell Part II, Art. 155.

Visualizes a point charge above an infinite conducting plane using the
image charge technique. Saves the plot as a PNG.

Usage:
    python examples/04_method_of_images_demo.py
"""
from maxwell.vis import plot_method_of_images

def main():
    fig, ax = plot_method_of_images(
        q=1.0,
        d=1.0,
        x_range=(-3.0, 3.0),
        y_range=(-3.0, 3.0),
        resolution=100,
    )
    fig.savefig("examples/output/method_of_images.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/method_of_images.png")


if __name__ == "__main__":
    import os
    os.makedirs("examples/output", exist_ok=True)
    main()
```

### Script 5: `examples/05_edge_singularity_study.py`

**Purpose:** Demonstrate edge singularity visualization and comparison (already decorated and exported).
**Saves:** `examples/output/edge_singularity.png` and `examples/output/singularity_comparison.png`

```python
"""Edge singularity study — Maxwell Part II, Art. 191.

Visualizes field enhancement near sharp conducting edges and compares
singularity strength for different wedge angles. Saves plots as PNGs.

Usage:
    python examples/05_edge_singularity_study.py
"""
import numpy as np
from maxwell.vis import plot_edge_singularity, plot_singularity_comparison

def main():
    # Single wedge visualization (90-degree edge)
    fig1, ax1 = plot_edge_singularity(
        alpha=np.pi / 2,
        resolution=100,
        log_scale=True,
    )
    fig1.savefig("examples/output/edge_singularity.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/edge_singularity.png")

    # Comparison of different wedge angles
    fig2, ax2 = plot_singularity_comparison(
        x_range=(0.01, 3.0),
        resolution=100,
    )
    fig2.savefig("examples/output/singularity_comparison.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/singularity_comparison.png")


if __name__ == "__main__":
    import os
    os.makedirs("examples/output", exist_ok=True)
    main()
```

### Supporting files:

**`examples/__init__.py`:**
```python
"""Runnable example scripts for maxwell visualization package."""
```

**Add to `.gitignore`:**
```
examples/output/
```

---

## Tier 3 — Quality Infrastructure

### Finding 4: Rendering validation tests

Add a new test class `TestRenderingValidation` to `tests/test_vis.py` that:
- Calls each plot function
- Saves the figure to a temporary file
- Verifies the file exists and has a minimum pixel count
- Cleans up after itself

#### Modification 4A: Add imports at top of `test_vis.py`

After line 8 (existing imports), add:
```python
import os
import tempfile
```

#### Modification 4B: Add new test class at end of `test_vis.py`

```python
class TestRenderingValidation:
    """Validate that visualization functions produce renderable PNG output."""

    def _save_and_validate(self, fig, min_pixels=1000):
        """Save figure to temp file and validate pixel count."""
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            tmp_path = f.name

        try:
            fig.savefig(tmp_path, dpi=80, bbox_inches="tight")
            assert os.path.exists(tmp_path), "PNG file was not created"
            assert os.path.getsize(tmp_path) > 0, "PNG file is empty"

            img = Image.open(tmp_path)
            width, height = img.size
            assert width * height >= min_pixels, (
                f"Image too small: {width}x{height} = {width*height} pixels "
                f"(minimum {min_pixels})"
            )
        finally:
            import matplotlib.pyplot as mplt
            mplt.close(fig)
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_field_lines_rendering(self):
        """plot_field_lines_2d produces a valid PNG."""
        from maxwell.vis.field_lines import plot_field_lines_2d

        def field(x, y):
            return x, y

        fig = plot_field_lines_2d(field, nx=20, ny=20)
        self._save_and_validate(fig)

    def test_dipole_field_lines_rendering(self):
        """plot_dipole_field_lines produces a valid PNG."""
        from maxwell.vis.field_lines import plot_dipole_field_lines

        fig = plot_dipole_field_lines(nx=20, ny=20)
        self._save_and_validate(fig)

    def test_equipotentials_rendering(self):
        """plot_equipotentials_2d produces a valid PNG."""
        from maxwell.vis.equipotential import plot_equipotentials_2d

        def potential(x, y):
            return 1.0 / np.sqrt(x**2 + y**2 + 0.01)

        fig = plot_equipotentials_2d(potential, nx=50, ny=50)
        self._save_and_validate(fig)

    def test_dipole_equipotentials_rendering(self):
        """plot_dipole_equipotentials produces a valid PNG."""
        from maxwell.vis.equipotential import plot_dipole_equipotentials

        fig = plot_dipole_equipotentials(nx=50, ny=50)
        self._save_and_validate(fig)

    def test_stress_tensor_rendering(self):
        """plot_stress_tensor_2d produces a valid PNG."""
        from maxwell.vis.stress import plot_stress_tensor_2d

        def field(x, y):
            return np.ones_like(x) * 1.0, np.zeros_like(x)

        fig = plot_stress_tensor_2d(field, nx=15, ny=15)
        self._save_and_validate(fig)

    def test_method_of_images_rendering(self):
        """plot_method_of_images produces a valid PNG."""
        from maxwell.vis import plot_method_of_images

        fig, ax = plot_method_of_images(resolution=50)
        self._save_and_validate(fig)

    def test_edge_singularity_rendering(self):
        """plot_edge_singularity produces a valid PNG."""
        from maxwell.vis import plot_edge_singularity

        fig, ax = plot_edge_singularity(alpha=np.pi / 2, resolution=50)
        self._save_and_validate(fig)

    def test_singularity_comparison_rendering(self):
        """plot_singularity_comparison produces a valid PNG."""
        from maxwell.vis import plot_singularity_comparison

        fig, ax = plot_singularity_comparison(resolution=50)
        self._save_and_validate(fig)
```

**Note:** This class requires the `Pillow` library for image validation. Add to test dependencies:
- In `pyproject.toml` under `[project.optional-dependencies]`:
  ```toml
  test = ["pytest", "numpy", "Pillow>=10.0"]
  ```
- Or as a conditional skip if Pillow is not available:
  ```python
  HAS_PILLOW = True
  try:
      from PIL import Image
  except ImportError:
      HAS_PILLOW = False

  render_skip = pytest.mark.skipif(not HAS_PILLOW, reason="Pillow not installed")
  ```
  Then decorate each test method with `@render_skip`.

---

### Finding 5: Unify type annotations

All vis modules should use consistent type annotations. The established pattern in newer modules (`dielectric_soakage.py`, `hysteresis_loops.py`) uses the modern `list[float] | None` syntax (PEP 604) instead of `Optional[list]`.

#### Type Annotation Changes Required

**File: `maxwell/vis/field_lines.py`**

| Line | Current | Should Be |
|------|---------|-----------|
| 12 | `from typing import Callable, Optional, Tuple` | Remove entire line (not needed after changes) |
| 29 | `linewidth: Optional[np.ndarray] = None` | `linewidth: np.ndarray \| None = None` |
| 31 | `charge_positions: Optional[list[Tuple[float, float]]] = None` | `charge_positions: list[tuple[float, float]] \| None = None` |
| 32 | `charge_signs: Optional[list[int]] = None` | `charge_signs: list[int] \| None = None` |
| 34 | `ax: Optional[Axes] = None` | `ax: Axes \| None = None` |

Also: The `Tuple` import from typing is unused since `Tuple[float, float]` can become `tuple[float, float]` (builtin, Python 3.9+).

**File: `maxwell/vis/equipotential.py`**

| Line | Current | Should Be |
|------|---------|-----------|
| 12 | `from typing import Callable, Optional, Tuple` | Remove entire line |
| 29 | `levels: Optional[np.ndarray] = None` | `levels: np.ndarray \| None = None` |
| 32 | `charge_positions: Optional[list[Tuple[float, float]]] = None` | `charge_positions: list[tuple[float, float]] \| None = None` |
| 33 | `charge_signs: Optional[list[int]] = None` | `charge_signs: list[int] \| None = None` |
| 35 | `ax: Optional[Axes] = None` | `ax: Axes \| None = None` |

**File: `maxwell/vis/stress.py`**

| Line | Current | Should Be |
|------|---------|-----------|
| 12 | `from typing import Callable, Optional, Tuple` | Change to `from typing import Callable` (Tuple still used on line 21) |
| 21 | `field_func: Callable[..., Tuple[np.ndarray, np.ndarray]]` | `field_func: Callable[..., tuple[np.ndarray, np.ndarray]]` |
| 32 | `ax: Optional[Axes] = None` | `ax: Axes \| None = None` |
| 113 | `E_field: Tuple[float, float, float] = (1.0, 0.0, 0.0)` | `E_field: tuple[float, float, float] = (1.0, 0.0, 0.0)` |
| 114 | `B_field: Tuple[float, float, float] = (0.0, 1.0, 0.0)` | `B_field: tuple[float, float, float] = (0.0, 1.0, 0.0)` |

After these changes, `stress.py` line 12 should become:
```python
from typing import Callable
```
(The `Tuple` is replaced by builtin `tuple`, and `Optional` is replaced by PEP 604 `| None`.)

**File: `maxwell/vis/_base.py`**

This file is already mostly consistent. The `ax` parameter on `format_axis_labels` (line 69) is untyped — it receives an `Axes` object but has no annotation:

| Line | Current | Should Be |
|------|---------|-----------|
| 69 | `ax,` | `ax: Axes,` |

And `Axes` needs to be imported from `_compat`:
```python
from maxwell.vis._compat import require_matplotlib, Axes
```

**File: `maxwell/vis/field_lines.py` — return type for inner function**

The nested `dipole_field` function on line 128 has no type annotation. Add:
```python
def dipole_field(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
```

**File: `maxwell/vis/equipotential.py` — return type for inner function**

The nested `dipole_potential` function on line 119 has no type annotation. Add:
```python
def dipole_potential(x: np.ndarray, y: np.ndarray) -> np.ndarray:
```

---

## Implementation Order & Dependencies

```
Step 1: Type annotation unification (field_lines.py, equipotential.py, stress.py, _base.py)
        - No dependencies, pure code cleanup
        - Lowest risk changes

Step 2: @maxwell_cite decorators (field_lines.py, equipotential.py, stress.py)
        - Depends on Step 1 (add import lines alongside type changes)
        - No behavioral change, just metadata

Step 3: __init__.py exports
        - Depends on Steps 1-2 being in place
        - Simple import additions

Step 4: Examples directory (5 scripts + __init__.py + .gitignore)
        - Depends on Step 3 (scripts use the public API)
        - Independent of Steps 1-2

Step 5: Rendering validation tests
        - Depends on Step 3 (tests import from public API)
        - May require Pillow dependency addition to pyproject.toml

Step 6: Test the test_vis.py exports test
        - Update TestVisIntegration.test_vis_all_exports to include new exports:
          plot_dipole_field_lines, plot_dipole_equipotentials, verify_stress_tensor_plot
```

---

## Acceptance Criteria

### Tier 1 Acceptance
- [ ] All 6 public functions in field_lines.py, equipotential.py, stress.py have `@maxwell_cite` decorators
- [ ] `maxwell.vis.__all__` includes `plot_dipole_field_lines`, `plot_dipole_equipotentials`, `verify_stress_tensor_plot`
- [ ] `from maxwell.vis import plot_dipole_field_lines` works without error
- [ ] `from maxwell.vis import plot_dipole_equipotentials` works without error
- [ ] `from maxwell.vis import verify_stress_tensor_plot` works without error
- [ ] `verify_traceability([maxwell.vis.field_lines, maxwell.vis.equipotential, maxwell.vis.stress])` returns 100% coverage

### Tier 2 Acceptance
- [ ] `examples/` directory exists with 5 `.py` files and `__init__.py`
- [ ] Each script runs without error: `python examples/01_*.py` through `python examples/05_*.py`
- [ ] Each script produces a PNG file in `examples/output/`
- [ ] `examples/output/` is listed in `.gitignore`
- [ ] Scripts only use public API (`from maxwell.vis import ...`)

### Tier 3 Acceptance
- [ ] `TestRenderingValidation` class exists in `tests/test_vis.py`
- [ ] All 8 rendering tests pass with PNG file creation + pixel validation
- [ ] Tests clean up temporary files after execution
- [ ] Tests gracefully skip if Pillow is not installed

### Type Annotation Acceptance
- [ ] Zero uses of `Optional[...]` in field_lines.py, equipotential.py, stress.py (replaced by `\| None`)
- [ ] Zero uses of `typing.Tuple` in those files (replaced by builtin `tuple`)
- [ ] `format_axis_labels` in `_base.py` has typed `ax` parameter
- [ ] `python -c "from maxwell.vis import *"` succeeds without errors
- [ ] All existing tests in `test_vis.py` continue to pass

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `@maxwell_cite` decorator import fails | Low | Low | Verify `maxwell.meta.citation` module exists (confirmed) |
| Type annotation change breaks runtime | Very Low | Low | PEP 604 types are Python 3.10+; if project targets 3.9, keep `from __future__ import annotations` (already present) |
| Pillow not available in test env | Medium | Low | Add conditional skip with `pytest.mark.skipif` |
| Examples fail due to missing vis deps | Low | Medium | Scripts should document `pip install maxwell[viz]` prerequisite |

---

## Estimated Effort

| Task | Complexity | Time Estimate |
|------|-----------|---------------|
| Type annotation unification | Low | 15 min |
| @maxwell_cite decorators | Low | 10 min |
| __init__.py exports | Low | 5 min |
| Examples directory (5 scripts) | Medium | 30 min |
| Rendering validation tests | Medium | 25 min |
| Test execution & verification | Low | 15 min |
| **Total** | | **~100 min** |
