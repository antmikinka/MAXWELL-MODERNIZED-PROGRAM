# Phase 2: PyPI Readiness -- Detailed Execution Plan

**Created:** 2026-04-26
**Baseline:** 629 tests passing, 100% article coverage (866 articles), 241 modules, 77 `__init__.py` files
**Estimated Duration:** 3-4 days

---

## 1. Audit Summary

### Current State

| Metric | Value |
|--------|-------|
| Total `__init__.py` files | 77 |
| Files with `__all__` | 50 |
| Files without `__all__` | 27 |
| Files with correct `__all__` | 46 |
| Files with stale `__all__` | 3 |
| Stub packages with "Reserved namespace" doc | 22 |
| Stub packages without proper doc | 3 |

### Issues Discovered in Existing `__all__`

| File | Issue | Severity |
|------|-------|----------|
| `maxwell/verification/__init__.py` | `__all__` contains `"test_spherical_harmonic_convergence"` and `"test_grid_convergence"` but actual imports are `measure_spherical_harmonic_convergence` and `measure_grid_convergence` | HIGH -- runtime `ImportError` on `from maxwell.verification import test_grid_convergence` |
| `maxwell/electromagnetism/sources/__init__.py` | `__all__ = ["oersted"]` but nothing is imported; exports a module name instead of symbols | MEDIUM -- no actual re-exports, dead `__all__` |
| `maxwell/__init__.py` | `__version__` in `__all__` is defined (not imported) | LOW -- valid pattern, false positive in AST audit |

### Files Missing `__all__` (27 files -- categorized)

**Category A: Populated package needing real exports**
1. `maxwell/electromagnetism/waves/__init__.py` -- 3 modules: plane_wave, polarization, wave_equation (22 public symbols)

**Category B: Package with only subpackage (needs re-export)**
2. `maxwell/experiments/__init__.py` -- 1 subpackage: ratio_v

**Category C: Stub packages needing reserved namespace doc + `__all__ = []`**
3-5. `maxwell/instruments/absolute/__init__.py` -- doc says "Absolute measurement submodule." (too brief)
6-8. `maxwell/instruments/calibration/__init__.py` -- doc says "Calibration submodule." (too brief)
9-11. `maxwell/instruments/optimization/__init__.py` -- doc says "Optimization submodule." (too brief)

**Category D: Stub packages with reserved namespace doc but missing `__all__ = []`**
12-27. 16 files (see details below)

---

## 2. Execution Steps (Ordered by Dependency)

### STEP 1: Fix Stale `__all__` Entries (0.5 days)

Fix 2 real bugs in existing `__all__` before adding new ones.

#### 1a. Fix `maxwell/verification/__init__.py`

**File:** `maxwell/verification/__init__.py`
**Change:** Lines 93-94, replace stale test_* names with actual measure_* names.

```python
# BEFORE (line 93-94):
    "test_spherical_harmonic_convergence",
    "test_grid_convergence",

# AFTER:
    "measure_spherical_harmonic_convergence",
    "measure_grid_convergence",
```

**Verification:**
```bash
python -c "from maxwell.verification import measure_spherical_harmonic_convergence, measure_grid_convergence; print('OK')"
```

#### 1b. Fix `maxwell/electromagnetism/sources/__init__.py`

**File:** `maxwell/electromagnetism/sources/__init__.py`
**Change:** Replace dead `__all__ = ["oersted"]` with proper re-exports from the oersted module.

Read `maxwell/electromagnetism/sources/oersted.py` to get its `__all__`, then update `sources/__init__.py` to import and re-export them. Expected imports based on the oersted module's own `__all__`:

```python
"""maxwell.electromagnetism.sources -- Electromagnetic source fields (Arts. 475-479).

This module contains implementations of fundamental electromagnetic
source configurations as described in Part IV of Maxwell's Treatise.
"""

from __future__ import annotations

from maxwell.electromagnetism.sources.oersted import (
    OerstedField,
    calc_oersted_field,
    calc_field_from_element,
    calc_force_on_pole,
    calc_circular_field_direction,
    verify_inverse_distance_law,
)

__all__ = [
    "OerstedField",
    "calc_oersted_field",
    "calc_field_from_element",
    "calc_force_on_pole",
    "calc_circular_field_direction",
    "verify_inverse_distance_law",
]
```

**Verification:**
```bash
python -c "from maxwell.electromagnetism.sources import OerstedField; print('OK')"
```

---

### STEP 2: Add `__all__` to Populated Packages (1 day)

#### 2a. `maxwell/electromagnetism/waves/__init__.py`

**File:** `maxwell/electromagnetism/waves/__init__.py`
**Current state:** Docstring only, no imports, no `__all__`. 3 submodules exist.
**Change:** Import and re-export all public symbols from submodules.

```python
"""Electromagnetic wave propagation (Part IV, electromagnetic theory of light).

Contains:
    plane_wave      -- Plane wave solutions to Maxwell equations
    polarization    -- Polarization states and analysis
    wave_equation   -- Wave equation derivation and solutions
"""

from __future__ import annotations

# Plane waves (plane_wave.py)
from maxwell.electromagnetism.waves.plane_wave import (
    PlaneWave,
    verify_transversality,
    calc_EB_relationship,
    calc_poynting_vector,
    PlaneWaveAnalyzer,
)

# Polarization (polarization.py)
from maxwell.electromagnetism.waves.polarization import (
    PolarizationState,
    calc_Stokes_parameters,
    decompose_polarization,
    transform_polarization,
    analyze_polarization,
    PolarizationAnalyzer,
    Jones_linear_polarizer,
    Jones_wave_plate,
)

# Wave equation (wave_equation.py)
from maxwell.electromagnetism.waves.wave_equation import (
    ElectromagneticWave,
    derive_wave_equation,
    calc_wave_equation_3d,
    calc_wave_speed,
    calc_wave_impedance,
    verify_wave_equation,
    WaveEquationSolver,
)

__all__ = [
    # Plane waves
    "PlaneWave",
    "verify_transversality",
    "calc_EB_relationship",
    "calc_poynting_vector",
    "PlaneWaveAnalyzer",
    # Polarization
    "PolarizationState",
    "calc_Stokes_parameters",
    "decompose_polarization",
    "transform_polarization",
    "analyze_polarization",
    "PolarizationAnalyzer",
    "Jones_linear_polarizer",
    "Jones_wave_plate",
    # Wave equation
    "ElectromagneticWave",
    "derive_wave_equation",
    "calc_wave_equation_3d",
    "calc_wave_speed",
    "calc_wave_impedance",
    "verify_wave_equation",
    "WaveEquationSolver",
]
```

**Verification:**
```bash
python -c "from maxwell.electromagnetism.waves import PlaneWave, PolarizationState, ElectromagneticWave; print('waves OK')"
```

#### 2b. `maxwell/experiments/__init__.py`

**File:** `maxwell/experiments/__init__.py`
**Current state:** Docstring + `from __future__ import annotations`. Has subpackage `ratio_v`.
**Change:** Re-export subpackage and add `__all__`.

```python
"""maxwell.experiments -- Experimental physics (Arts. 768-780).

Experimental determination of the ratio between electrostatic
and electromagnetic units, proving it equals the speed of light.
"""

from __future__ import annotations

from maxwell.experiments import ratio_v

__all__ = [
    "ratio_v",
]
```

**Verification:**
```bash
python -c "from maxwell.experiments import ratio_v; print('experiments OK')"
```

---

### STEP 3: Add `__all__ = []` to Stub Packages with Reserved Namespace Docs (0.5 days)

These 16 files already have proper reserved namespace docstrings but lack `__all__`.
Add `__all__ = []` as the last line of each file (after the docstring).

| # | File |
|---|------|
| 1 | `maxwell/chemistry/__init__.py` |
| 2 | `maxwell/core/math/__init__.py` |
| 3 | `maxwell/core/space/__init__.py` |
| 4 | `maxwell/electromagnetism/field_theory/__init__.py` |
| 5 | `maxwell/electromagnetism/units/__init__.py` |
| 6 | `maxwell/kinematics/__init__.py` |
| 7 | `maxwell/magnetics/__init__.py` |
| 8 | `maxwell/magnetism/calculus/__init__.py` |
| 9 | `maxwell/magnetism/components/__init__.py` |
| 10 | `maxwell/magnetism/core/__init__.py` |
| 11 | `maxwell/magnetism/fields/__init__.py` |
| 12 | `maxwell/magnetism/geometry/__init__.py` |
| 13 | `maxwell/magnetism/geophysics/__init__.py` |
| 14 | `maxwell/magnetism/instruments/__init__.py` |
| 15 | `maxwell/magnetism/materials/__init__.py` |
| 16 | `maxwell/magnetism/mechanics/__init__.py` |
| 17 | `maxwell/magnetism/physics/__init__.py` |
| 18 | `maxwell/magnetism/solvers/__init__.py` |
| 19 | `maxwell/materials/database/__init__.py` |
| 20 | `maxwell/sim/__init__.py` |
| 21 | `maxwell/telecom/__init__.py` |
| 22 | `maxwell/thermodynamics/__init__.py` |

**Edit pattern for each file** (append after the existing docstring):
```python

__all__ = []
```

**Verification script (run after all edits):**
```bash
# Verify all stub __init__.py files have __all__ = []
python -c "
import importlib, sys
stubs = [
    'maxwell.chemistry', 'maxwell.core.math', 'maxwell.core.space',
    'maxwell.electromagnetism.field_theory', 'maxwell.electromagnetism.units',
    'maxwell.kinematics', 'maxwell.magnetics',
    'maxwell.magnetism.calculus', 'maxwell.magnetism.components',
    'maxwell.magnetism.core', 'maxwell.magnetism.fields',
    'maxwell.magnetism.geometry', 'maxwell.magnetism.geophysics',
    'maxwell.magnetism.instruments', 'maxwell.magnetism.materials',
    'maxwell.magnetism.mechanics', 'maxwell.magnetism.physics',
    'maxwell.magnetism.solvers',
    'maxwell.materials.database', 'maxwell.sim',
    'maxwell.telecom', 'maxwell.thermodynamics',
]
for name in stubs:
    mod = importlib.import_module(name)
    assert hasattr(mod, '__all__'), f'{name} missing __all__'
    assert mod.__all__ == [], f'{name} __all__ should be [] but is {mod.__all__}'
    print(f'  OK: {name}')
print('All 22 stubs verified.')
"
```

---

### STEP 4: Fix 3 Instrument Submodule Stubs (0.5 days)

These 3 files have inadequate docstrings AND missing `__all__`.

#### 4a. `maxwell/instruments/absolute/__init__.py`

**File:** `maxwell/instruments/absolute/__init__.py`
**Current content:**
```python
"""Absolute measurement submodule."""
```

**Replace with:**
```python
"""Reserved namespace: maxwell.instruments.absolute.

This namespace is reserved for Maxwell's treatment of absolute electrical
measurements (Arts. 758-767), including absolute determination of resistance
and current standards. See docs/STRATEGIC_ROADMAP.md for planned content.
"""

__all__ = []
```

#### 4b. `maxwell/instruments/calibration/__init__.py`

**File:** `maxwell/instruments/calibration/__init__.py`
**Current content:**
```python
"""Calibration submodule."""
```

**Replace with:**
```python
"""Reserved namespace: maxwell.instruments.calibration.

This namespace is reserved for instrument calibration methods and procedures
from Maxwell's Treatise, including calibration of galvanometers, dynamometers,
and other measurement apparatus. See docs/STRATEGIC_ROADMAP.md for planned content.
"""

__all__ = []
```

#### 4c. `maxwell/instruments/optimization/__init__.py`

**File:** `maxwell/instruments/optimization/__init__.py`
**Current content:**
```python
"""Optimization submodule."""
```

**Replace with:**
```python
"""Reserved namespace: maxwell.instruments.optimization.

This namespace is reserved for instrument optimization techniques from
Maxwell's Treatise, including sensitivity optimization of suspended coils,
Helmholtz configurations, and measurement apparatus design.
See docs/STRATEGIC_ROADMAP.md for planned content.
"""

__all__ = []
```

---

### STEP 5: Zenodo DOI Badge (0.5 days)

#### 5a. Create `.zenodo.json`

**File:** `.zenodo.json` (new file at repo root)
```json
{
    "title": "Maxwell Modernized: A Computational Implementation of Maxwell's Treatise on Electricity and Magnetism",
    "upload_type": "software",
    "description": "A complete computational implementation of James Clerk Maxwell's 1873 A Treatise on Electricity and Magnetism. All 866 articles are implemented in Python with CGS-EMU units and citation-based traceability to the original text.",
    "creators": [
        {
            "name": "Maxwell Modernization Project",
            "affiliation": "Independent"
        }
    ],
    "license": "MIT",
    "keywords": [
        "electromagnetism",
        "computational-physics",
        "maxwell-equations",
        "classical-physics",
        "cgs-units",
        "spherical-harmonics",
        "maxwell-treatise"
    ],
    "access_right": "open"
}
```

#### 5b. Create GitHub Release

Prerequisite for Zenodo DOI. Requires the `gh` CLI:
```bash
# Tag and push the release
git tag -a v0.1.0 -m "PyPI Release 0.1.0: 100% article coverage, 629 tests passing"
git push origin v0.1.0

# Create GitHub release (triggers Zenodo DOI assignment)
gh release create v0.1.0 \
    --title "v0.1.0 -- PyPI Release" \
    --notes "Initial PyPI release. 866/866 articles implemented, 629 tests passing."
```

**Verification:**
- Check Zenodo record appears at `https://zenodo.org/records/<ID>`
- DOI badge format: `![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)`

#### 5c. Add DOI Badge to README.md

Add DOI badge line to the top of `README.md` (after the title, before any other badges):
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

---

### STEP 6: CITATION.cff Validation (0.5 days)

#### 6a. Validate with `cffconvert`

```bash
pip install cffconvert
cffconvert --validate
```

#### 6b. Fix Issues if Found

Current `CITATION.cff` has these potential issues to check:
- Line 14: Second author has no `given-names` or `family-names` populated (only orcid)
- Author ORCID is `0009-0005-2955-4140` (`https://orcid.org/0009-0005-2955-4140`). The all-zero placeholder must not return.
- `date-released` should match the 1.0.0 release date (`2026-05-07`)
- Version should match `pyproject.toml` version (`1.0.0`)

**Recommended fix** (remove the incomplete second author or fill in real data):
```yaml
authors:
  - family-names: Mikinka
    given-names: Anthony
    orcid: "https://orcid.org/XXXX-XXXX-XXXX-XXXX"  # Replace with real ORCID
```

#### 6c. Generate CITATION.cff from pyproject.toml (optional but recommended)

```bash
cffconvert --output-format rfc6983 --output citation.cff
```

---

### STEP 7: MANIFEST.in Completeness Check (0.5 days)

#### 7a. Current MANIFEST.in Audit

**File:** `MANIFEST.in` (already present, well-structured)

Current contents cover:
- `README.md` -- exists, included
- `LICENSE` -- exists, included
- `CHANGELOG.md` -- exists, included
- `CITATION.cff` -- exists, included
- `pyproject.toml` -- included
- `docs/*.md` -- check if docs/ directory exists
- `maxwell/*.py *.json *.md` -- included
- `tests/*.py` -- included
- Exclusions: `__pycache__`, `*.pyc`, `*.egg-info`, `.pytest_cache`, `.benchmarks`, `chroma_data`, `agents`, `archive`, `.claude`, `audit_logs`, `build`, `dist`, `*.egg`

#### 7b. Verify sdist Contents

```bash
pip install build
python -m build --sdist
tar -tzf dist/maxwell-0.1.0.tar.gz | head -50
```

Check for:
1. Are `.zenodo.json` and `CITATION.cff` included? (add `include .zenodo.json` if not)
2. Is `LICENSE` included? (yes, via `include LICENSE`)
3. Are JSON data files included? (yes, via `recursive-include maxwell *.json`)
4. Are docstrings/README inside maxwell/ subpackages included? (yes, via `recursive-include maxwell *.md`)

#### 7c. Add Missing Entries

If `.zenodo.json` is not included:
```
# Add to MANIFEST.in:
include .zenodo.json
```

#### 7d. Test Package Build

```bash
python -m build --sdist --wheel
twine check dist/*
```

---

### STEP 8: Full Test Suite Run (0.5 days)

Run the complete test suite after all changes to verify nothing is broken.

```bash
# Full test run
python -m pytest tests/ -v --tb=short

# Verify all imports work
python -c "import maxwell; print(maxwell.__version__)"
python -c "from maxwell.electromagnetism.waves import PlaneWave, PolarizationState, ElectromagneticWave; print('waves OK')"
python -c "from maxwell.verification import measure_grid_convergence; print('verification OK')"
python -c "from maxwell.electromagnetism.sources import OerstedField; print('sources OK')"
python -c "from maxwell import *; print('star import OK')"
```

---

## 3. Dependency Order

```
STEP 1 (fix stale __all__) ──┐
                             ├──> STEP 2 (add __all__ to populated packages)
                             │       │
STEP 3 (stub __all__) ───────┤       │
                             │       v
STEP 4 (instrument stubs) ───┘   STEP 5 (Zenodo DOI)
                                         │
                                         v
STEP 6 (CITATION.cff) ──> STEP 7 (MANIFEST.in) ──> STEP 8 (test run)
```

Steps 1-4 can be done in any order as they touch different files.
Steps 5-6 must follow Step 4 (DOI needs release, CITATION needs to be consistent).
Step 7 depends on Step 5 (Zenodo file must exist to include in MANIFEST).
Step 8 runs last as the gate.

---

## 4. Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| `from maxwell.electromagnetism.waves` import fails due to missing symbols | Build broken | Import test each wave submodule individually before modifying `__init__.py` |
| `measure_spherical_harmonic_convergence` not actually in convergence.py | Import fails at verification step | Verify symbol exists: `grep "def measure_spherical_harmonic_convergence" maxwell/verification/convergence.py` |
| Zenodo DOI not assigned after GitHub release | Badge broken | Manual trigger: push tag, wait 5 min, check zenodo.org for record |
| `cffconvert` validation fails on CITATION.cff | Cannot mark Phase 2 complete | Fix invalid fields, validate iteratively |
| MANIFEST.in excludes required files | PyPI upload incomplete | Test build with `python -m build --sdist` and inspect tarball |

---

## 5. Quality Checkpoints

| Checkpoint | Files Affected | Verification Command |
|------------|---------------|---------------------|
| C1: Stale `__all__` fixed | 2 files | `python -c "from maxwell.verification import measure_grid_convergence"` |
| C2: Waves package exports work | 1 file | `python -c "from maxwell.electromagnetism.waves import PlaneWave"` |
| C3: All stub packages have `__all__` | 25 files | Run verification script from Step 3 |
| C4: Instrument submodules have proper docs | 3 files | `grep -c "Reserved namespace" maxwell/instruments/*/\_\_init\_\_.py` (expect 3) |
| C5: All 77 `__init__.py` have `__all__` | 77 files | `grep -c "^__all__" $(find maxwell -name "__init__.py") \| grep -c ":0$" ` (expect 0) |
| C6: Full test suite passes | entire codebase | `python -m pytest tests/ -q` (expect 629 passing) |
| C7: Package builds cleanly | build artifacts | `python -m build --sdist --wheel && twine check dist/*` |
| C8: CITATION.cff validates | CITATION.cff | `cffconvert --validate` |
| C9: Zenodo DOI assigned | release + zenodo | Check `https://zenodo.org/record/<ID>` |

---

## 6. File Modification Summary

| Step | File | Action | Category |
|------|------|--------|----------|
| 1a | `maxwell/verification/__init__.py` | Fix 2 stale `__all__` entries | Bug fix |
| 1b | `maxwell/electromagnetism/sources/__init__.py` | Replace dead `__all__` with real imports | Bug fix |
| 2a | `maxwell/electromagnetism/waves/__init__.py` | Add imports + `__all__` (22 symbols) | New content |
| 2b | `maxwell/experiments/__init__.py` | Add `__all__ = ["ratio_v"]` | New content |
| 3 | 22 stub files | Append `__all__ = []` | Batch edit |
| 4a | `maxwell/instruments/absolute/__init__.py` | Replace docstring + add `__all__` | Rewrite |
| 4b | `maxwell/instruments/calibration/__init__.py` | Replace docstring + add `__all__` | Rewrite |
| 4c | `maxwell/instruments/optimization/__init__.py` | Replace docstring + add `__all__` | Rewrite |
| 5 | `.zenodo.json` | Create new file | New file |
| 5 | `README.md` | Add DOI badge | Edit |
| 6 | `CITATION.cff` | Validate + fix placeholder ORCID | Edit |
| 7 | `MANIFEST.in` | Verify + optionally add `.zenodo.json` | Edit |

**Total: 30+ files to create/modify**
