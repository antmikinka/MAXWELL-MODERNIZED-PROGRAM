# Quality Review Plan - Maxwell Part IV (58 New Modules)

**Document Version:** 1.0
**Date:** 2026-04-12
**Author:** Quality Management System
**Scope:** 58 new Part IV Electromagnetism modules

---

## Executive Summary

This document defines the comprehensive quality assurance framework for validating 58 new modules being implemented for Maxwell's Treatise Part IV (Electromagnetism). Every module must meet strict standards for:

- **@maxwell_cite decorator** presence and accuracy
- **CGS unit consistency** in all computations
- **Physics correctness** per Maxwell's equations
- **Citation coverage** linking code to Treatise articles
- **Documentation quality** including docstrings and examples

---

## 1. Quality Check Categories

### 1.1 Module Import Verification

**Check:** Every module must be importable without errors.

**Pass Criteria:**
- `import maxwell.<category>.<module>` succeeds
- No `ImportError`, `SyntaxError`, or `ModuleNotFoundError`
- All public functions/classes are accessible

**Tool:** `python -c "import maxwell.module"`

---

### 1.2 Citation Decorator Compliance

**Check:** Every public function must have `@maxwell_cite` decorator.

**Pass Criteria:**
| Criterion | Requirement |
|-----------|-------------|
| Coverage | 100% of public functions decorated |
| Part Number | Must be in range 1-6 (Part IV = 4) |
| Article Numbers | Must be positive integers matching Treatise |
| Theory Class | Must be "maxwell_original", "user_original", or "standard_math" |

**Validation Tests:**
```python
from maxwell.meta.citation import get_citation, verify_traceability

# Check individual function
citation = get_citation(my_function)
assert citation is not None
assert 1 <= citation.part <= 6
assert all(a > 0 for a in citation.articles)
assert citation.theory_class in {"maxwell_original", "user_original", "standard_math"}

# Check module coverage
result = verify_traceability([module])
assert result["coverage_pct"] == 100.0
```

---

### 1.3 CGS Unit Consistency

**Check:** All numerical computations use CGS units correctly.

**Required CGS Units by Category:**

| Physical Quantity | CGS Unit | SI Equivalent |
|-------------------|----------|---------------|
| Length | cm | 0.01 m |
| Mass | g | 0.001 kg |
| Time | s | 1 s |
| Force | dyne | 10^-5 N |
| Energy | erg | 10^-7 J |
| Current (EMU) | abampere | 10 A |
| Current (ESU) | statampere | 3.3356e-10 A |
| Charge (EMU) | abcoulomb | 10 C |
| Charge (ESU) | statcoulomb | 3.3356e-10 C |
| Potential (EMU) | abvolt | 10^-8 V |
| Potential (ESU) | statvolt | 299.792458 V |
| Magnetic Field | gauss | 10^-4 T |
| Magnetic Flux | maxwell | 10^-8 Wb |
| Resistance (EMU) | abohm | 10^-9 ohm |
| Resistance (ESU) | statohm | 8.98755e11 ohm |

**Constants Validation:**
```python
from maxwell.config.constants import CONST, C

assert CONST.C == 2.99792458e10  # cm/s
assert CONST.MU0_EMU == 1.0
assert CONST.EPS0_EMU == 1.0 / C ** 2
```

**Inverse-Distance Law Checks:**
- Oersted field: H = 2I/r (H*r = constant)
- Coulomb force: F = q1*q2/r^2 (F*r^2 = constant)
- Biot-Savart: dB ~ I*dl/r^2

---

### 1.4 Physics Correctness Criteria

**By Module Category:**

#### 4.1 Electromagnetic Sources (Oersted, Current Elements)

| Function | Formula | Validation Test |
|----------|---------|-----------------|
| `calc_oersted_field` | H = 2I/r | H*r = 2I (constant) |
| `calc_field_from_element` | dB = I*dl*sin(theta)/r^2 | Zero at theta=0, max at theta=90 |
| `calc_force_on_pole` | F = m*H = 2mI/r | Proportional to m, I; inverse to r |
| `calc_circular_field_direction` | Right-hand rule | Direction tangential, normalized |

#### 4.2 Electromagnetic Induction (Faraday)

| Function | Formula | Validation Test |
|----------|---------|-----------------|
| `calc_magnetic_flux` | Phi = B*A*cos(theta) | Max at theta=0, zero at theta=90 |
| `calc_induced_emf` | EMF = -dPhi/dt | Negative sign (Lenz's law) |
| `calc_motional_emf` | EMF = v*B*L | Proportional to v, B, L |
| `calc_self_induction` | EMF = -L*dI/dt | Opposes current change |

#### 4.3 Electromagnetic Forces (Lorentz)

| Function | Formula | Validation Test |
|----------|---------|-----------------|
| `calc_force_on_wire` | F = I*L x B | Cross product direction |
| `calc_force_on_moving_charge` | F = q*v x B | Cross product, zero if parallel |
| `calc_force_between_parallel_currents` | F = 2*I1*I2*L/r | Attract if same direction |
| `calc_torque_on_current_loop` | tau = m x B | Zero when aligned |

#### 4.4 Field Theory (Ampere-Maxwell)

| Function | Formula | Validation Test |
|----------|---------|-----------------|
| `calc_ampere_law` | H.dl = 4*pi*I | Proportional to I |
| `calc_displacement_current` | Jd = (eps/4pi)*dE/dt | Proportional to dE/dt |
| `calc_total_current_density` | J_total = J + Jd | Sum of conduction + displacement |
| `verify_displacement_current_necessity` | Capacitor paradox | Resolved when Jd included |

#### 4.5 General Equations (Maxwell's Equations)

| Equation | Formula | Validation |
|----------|---------|------------|
| Faraday (A) | curl E = -(1/c)*dB/dt | Negative sign, 1/c factor |
| General EMF (B) | E = (1/c)(v x B) - (1/c)dA/dt - grad phi | Three terms combine |
| Ponderomotive (C) | F = rho*E + (1/c)(J x B) | Electric + magnetic |
| Magnetic Induction (D) | B = H + 4*pi*M | 4*pi factor |
| Ampere-Maxwell (E) | curl H = (4pi/c)J + (1/c)dD/dt | Conduction + displacement |
| Electric Displacement (F) | D = eps*E | Proportionality |
| Conduction Current (G) | J = sigma*E | Ohm's law form |
| Gauss Electric | div D = 4*pi*rho | Charge source |
| Gauss Magnetic | div B = 0 | No monopoles |

---

### 1.5 Documentation Quality

**Check:** Every module and function has proper documentation.

**Pass Criteria:**

| Element | Requirement |
|---------|-------------|
| Module docstring | Present, describes purpose |
| Function docstring | Present, describes parameters, return value |
| Formula reference | Cites Maxwell article number |
| Example usage | At least one numeric example |
| Unit specification | Documents CGS units used |

**Docstring Template:**
```python
"""
Brief description of function purpose.

Formula: H = 2I/r (Oersted's law for infinite wire)

Args:
    current: Current in abamperes (EMU)
    distance: Radial distance in cm

Returns:
    Magnetic field strength H in oersted

Reference:
    Maxwell, Treatise, Part IV, Chapter X, Art. 475-476
"""
```

---

### 1.6 Citation Coverage Requirements

**By Module Type:**

| Module Category | Required Articles | Part | Theory Class |
|-----------------|-------------------|------|--------------|
| Oersted (sources) | 475-479 | IV | maxwell_original |
| Faraday (induction) | 528-531 | IV | maxwell_original |
| Lorentz (forces) | 490-492 | IV | maxwell_original |
| Ampere-Maxwell | 606-607 | IV | maxwell_original |
| General Equations | 594-603 | IV | maxwell_original |
| Dimensional Analysis | 620-628, 771-781 | IV | standard_math |

**Minimum Citation Requirements:**
- Each function: At least 1 article citation
- Module total: All articles in range covered
- Cross-references: Related functions cite overlapping articles

---

## 2. Checklist by Module Category

### 2.1 Sources Modules (Current-Created Fields)

| Module | Articles | Import | Citation | CGS Units | Physics | Docstring |
|--------|----------|--------|----------|-----------|---------|-----------|
| oersted.py | 475-479 | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Additional source modules...] | ... | [ ] | [ ] | [ ] | [ ] | [ ] |

**Physics Checks:**
- [ ] Inverse distance law: H ~ 1/r
- [ ] Right-hand rule direction
- [ ] Force on pole: F = m*H
- [ ] Biot-Savart integration

---

### 2.2 Induction Modules (Time-Varying Fields)

| Module | Articles | Import | Citation | CGS Units | Physics | Docstring |
|--------|----------|--------|----------|-----------|---------|-----------|
| faraday.py | 528-531 | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Additional induction modules...] | ... | [ ] | [ ] | [ ] | [ ] | [ ] |

**Physics Checks:**
- [ ] Flux formula: Phi = B*A*cos(theta)
- [ ] Lenz's law: Negative sign in EMF
- [ ] Motional EMF: v x B
- [ ] Self-induction: L*dI/dt

---

### 2.3 Forces Modules (Lorentz Force)

| Module | Articles | Import | Citation | CGS Units | Physics | Docstring |
|--------|----------|--------|----------|-----------|---------|-----------|
| lorentz.py | 490-492 | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Additional force modules...] | ... | [ ] | [ ] | [ ] | [ ] | [ ] |

**Physics Checks:**
- [ ] Cross product direction
- [ ] Force on wire: I*L x B
- [ ] Force on charge: q*v x B
- [ ] Parallel currents: 2*I1*I2*L/r

---

### 2.4 Field Theory Modules (Maxwell's Completion)

| Module | Articles | Import | Citation | CGS Units | Physics | Docstring |
|--------|----------|--------|----------|-----------|---------|-----------|
| ampere_maxwell.py | 606-607 | [ ] | [ ] | [ ] | [ ] | [ ] |
| general_equations.py | 594-603 | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Additional field modules...] | ... | [ ] | [ ] | [ ] | [ ] | [ ] |

**Physics Checks:**
- [ ] Displacement current necessity
- [ ] Capacitor paradox resolution
- [ ] Full Maxwell equations verified
- [ ] Wave equation derivation support

---

### 2.5 Theory and Analysis Modules

| Module | Articles | Import | Citation | CGS Units | Physics | Docstring |
|--------|----------|--------|----------|-----------|---------|-----------|
| dimensional_analysis.py | 620-628, 771-781 | [ ] | [ ] | [ ] | [ ] | [ ] |
| [Additional theory modules...] | ... | [ ] | [ ] | [ ] | [ ] | [ ] |

**Physics Checks:**
- [ ] ESU/EMU dimensional ratios
- [ ] Speed of light relationship: c = ESU/EMU
- [ ] Unit conversions correct
- [ ] Dimensional consistency verified

---

## 3. Automated Quality Checks

### 3.1 Import Test Suite

```bash
# Test all 58 modules import successfully
python -c "
import sys
from pathlib import Path

modules_to_test = [
    'maxwell.electromagnetism.sources.oersted',
    'maxwell.electromagnetism.induction.faraday',
    # ... all 58 modules
]

failed = []
for mod in modules_to_test:
    try:
        __import__(mod)
        print(f'OK: {mod}')
    except Exception as e:
        failed.append((mod, str(e)))
        print(f'FAIL: {mod} - {e}')

if failed:
    print(f'\n{len(failed)} modules failed to import')
    sys.exit(1)
print(f'\nAll {len(modules_to_test)} modules imported successfully')
"
```

### 3.2 Citation Coverage Test

```python
from maxwell.meta.citation import get_citation, get_all_citations, verify_traceability
import inspect

def check_citation_coverage(module_list):
    """Verify all public functions have citations."""
    results = {
        'total_functions': 0,
        'cited_functions': 0,
        'uncited': [],
        'invalid_citations': []
    }

    for mod in module_list:
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith('_'):
                continue
            results['total_functions'] += 1

            citation = get_citation(obj)
            if citation is None:
                results['uncited'].append(f'{mod.__name__}.{name}')
            else:
                results['cited_functions'] += 1

                # Validate citation
                if not (1 <= citation.part <= 6):
                    results['invalid_citations'].append(
                        f'{mod.__name__}.{name}: Invalid part {citation.part}'
                    )
                if not all(a > 0 for a in citation.articles):
                    results['invalid_citations'].append(
                        f'{mod.__name__}.{name}: Invalid articles {citation.articles}'
                    )

    coverage = results['cited_functions'] / results['total_functions'] * 100 if results['total_functions'] else 0
    results['coverage_pct'] = coverage

    return results
```

### 3.3 CGS Unit Validation Test

```python
from maxwell.config.constants import CONST, C

def validate_cgs_constants():
    """Validate CGS constants are correctly defined."""
    errors = []

    # Speed of light
    if not (2.99e10 <= CONST.C <= 3.00e10):
        errors.append(f"C = {CONST.C}, expected ~3e10 cm/s")

    # EMU constants
    if CONST.MU0_EMU != 1.0:
        errors.append(f"MU0_EMU = {CONST.MU0_EMU}, expected 1.0")

    expected_eps0 = 1.0 / C ** 2
    if abs(CONST.EPS0_EMU - expected_eps0) > 1e-20:
        errors.append(f"EPS0_EMU incorrect")

    return {
        'passed': len(errors) == 0,
        'errors': errors
    }
```

### 3.4 Physics Formula Verification

```python
def verify_inverse_distance_law(func, current=1.0):
    """Verify H ~ 1/r inverse distance relationship."""
    import numpy as np

    distances = [0.5, 1.0, 2.0, 4.0, 8.0]
    H_values = [func(current, r) for r in distances]

    # H*r should be constant (= 2I for Oersted)
    products = [H * r for H, r in zip(H_values, distances)]

    mean_product = np.mean(products)
    max_deviation = max(abs(p - mean_product) / mean_product for p in products)

    return {
        'verified': max_deviation < 1e-10,
        'max_relative_deviation': max_deviation,
        'H_r_products': products
    }
```

---

## 4. Equation Verification Pipeline

### 4.1 Pipeline Overview

The verification pipeline performs 4 phases:

1. **Extraction:** Parse Mathpix JSON sources for equations
2. **Registry:** Build equation database with metadata
3. **Verification:** Compare Python implementations against extracted equations
4. **Report:** Generate verification report with pass/fail status

### 4.2 Running the Pipeline

```bash
python run_verification.py \
    --json-dirs MAXWELL_VOLUME_1_MASTER_OUTPUT MAXWELL_VOLUME_2_MASTER_OUTPUT \
    --maxwell-dir maxwell/ \
    --output verification_report.md
```

### 4.3 Expected Results

Based on current project status:
- **Total verifications:** 2,598+ equations
- **Mismatch rate:** 0%
- **Coverage:** All Part IV modules included

---

## 5. Pass/Fail Criteria Summary

### 5.1 Module-Level Criteria

A module **PASSES** if ALL of the following are true:

| Criterion | Threshold |
|-----------|-----------|
| Import success | 100% |
| Citation coverage | 100% |
| Valid citations | 100% |
| CGS unit usage | 100% |
| Physics formula accuracy | Within tolerance (1e-10) |
| Documentation completeness | All functions documented |

A module **FAILS** if ANY of:
- Import fails with error
- Any public function lacks @maxwell_cite
- Any citation has invalid part/articles
- Physics formula deviates > tolerance
- Required docstring missing

### 5.2 Tolerance Levels

| Check Type | Strict Tolerance | Coarse Tolerance |
|------------|------------------|------------------|
| Numerical formula | 1e-10 | 1e-6 |
| Vector direction | 1e-10 | 1e-6 |
| Unit conversion | 1e-12 | 1e-9 |
| CGS constant | Exact | 1e-15 |

---

## 6. Defect Classification

### 6.1 Severity Levels

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| Critical | Import failure, missing citation | Block release |
| Major | Wrong formula, incorrect units | Fix before merge |
| Minor | Docstring missing, formatting | Fix in next sprint |
| Cosmetic | Style issues, comments | Optional fix |

### 6.2 Defect Tracking Template

```markdown
## Defect Report

**Module:** maxwell.electromagnetism.sources.oersted
**Function:** calc_oersted_field
**Severity:** Major
**Category:** Physics Formula

**Description:**
Formula produces H = I/r instead of H = 2I/r

**Expected:**
H = 2 * current / distance

**Actual:**
H = current / distance

**Fix:**
Add factor of 2 to return statement
```

---

## 7. Quality Metrics Dashboard

### 7.1 Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Module import rate | 100% | TBD | Pending |
| Citation coverage | 100% | TBD | Pending |
| Equation verification pass | 100% | TBD | Pending |
| Physics formula accuracy | 1e-10 | TBD | Pending |
| Documentation coverage | 100% | TBD | Pending |

### 7.2 Trend Analysis

Track metrics over time:
- Weekly citation coverage %
- Equation verification pass rate
- Defect density per module

---

## 8. Approval Workflow

### 8.1 Quality Gate Checklist

Before a module can be merged:

- [ ] All import tests pass
- [ ] Citation coverage = 100%
- [ ] All physics formulas verified
- [ ] CGS unit tests pass
- [ ] Documentation complete
- [ ] Code review approved
- [ ] Equation verification passed

### 8.2 Sign-off Requirements

| Role | Responsibility | Sign-off |
|------|----------------|----------|
| Developer | Implementation, unit tests | [ ] |
| QA Engineer | Quality checks, validation | [ ] |
| Physics Reviewer | Formula accuracy | [ ] |
| Tech Lead | Final approval | [ ] |

---

## Appendix A: Module List (58 Modules)

*To be populated as modules are identified by the implementation agent.*

Expected categories:
- Sources (current-created fields): ~12 modules
- Induction (time-varying fields): ~10 modules
- Forces (Lorentz): ~8 modules
- Field theory (Ampere-Maxwell): ~10 modules
- General equations: ~8 modules
- Dimensional analysis: ~6 modules
- Wave propagation: ~4 modules

---

## Appendix B: Reference Documents

- `maxwell/meta/citation.py` - Citation decorator implementation
- `maxwell/config/constants.py` - CGS constants
- `tests/conftest.py` - Test fixtures
- `tests/test_cgs_units.py` - CGS unit tests
- `tests/test_citation_decorator.py` - Citation tests
- `run_verification.py` - Equation verification pipeline

---

*Document generated by Quality Management System*
*Last updated: 2026-04-12*
