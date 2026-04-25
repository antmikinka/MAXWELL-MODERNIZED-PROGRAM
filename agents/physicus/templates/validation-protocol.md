# Template: validation-protocol

## Description

Template for physics validation protocols that verify implementations against analytical solutions, known physics, and Maxwell's original derivations.

## Structure

```markdown
# Validation Protocol: {component_name}

## Component Information
- **Component:** {component_path}
- **Physics Domain:** {domain}
- **Maxwell Articles:** {citations}
- **Validator:** {validator_name}
- **Date:** {date}

## Validation Overview
{summary_of_what_is_being_validated}

## Test Categories

### 1. Analytical Solutions
Tests against known closed-form solutions.

| Test ID | Description | Expected | Tolerance |
|---------|-------------|----------|-----------|
| {test_id} | {test_description} | {expected_result} | {tolerance} |

### 2. Conservation Laws
Verification of fundamental conservation principles.

| Test ID | Conservation Law | Expected | Tolerance |
|---------|------------------|----------|-----------|
| {test_id} | {law} | {expected} | {tolerance} |

### 3. Limiting Cases
Behavior in physical limits.

| Test ID | Limit | Expected Behavior | Verified |
|---------|-------|---------------------|----------|
| {test_id} | {limit} | {behavior} | [ ] |

### 4. Dimensional Analysis
CGS unit consistency checks.

| Test ID | Quantity | Expected Dimensions | Verified |
|---------|----------|----------------------|----------|
| {test_id} | {quantity} | {dimensions} | [ ] |

### 5. Numerical Convergence
For numerical implementations.

| Test ID | Resolution | Expected Error | Measured |
|---------|------------|----------------|----------|
| {test_id} | {resolution} | {expected} | {measured} |

### 6. Maxwell Article Traceability
Verification against Maxwell's original statements.

| Article | Content | Implementation | Verified |
|---------|---------|----------------|----------|
| {article} | {content} | {implementation} | [ ] |

## Detailed Test Results

### Test {test_id}: {test_name}

**Setup:**
{test_configuration}

**Input:**
{test_input}

**Expected Output:**
{expected}

**Actual Output:**
{actual}

**Comparison:**
{error_analysis}

**Status:** {PASS|FAIL|PARTIAL}

**Notes:**
{additional_observations}

## Summary

| Category | Tests | Passed | Failed | Score |
|----------|-------|--------|--------|-------|
| Analytical | {n} | {p} | {f} | {score}% |
| Conservation | {n} | {p} | {f} | {score}% |
| Limiting Cases | {n} | {p} | {f} | {score}% |
| Dimensional | {n} | {p} | {f} | {score}% |
| Convergence | {n} | {p} | {f} | {score}% |
| Traceability | {n} | {p} | {f} | {score}% |

**Overall Score:** {overall_score}%

**Status:** {VALIDATED|NEEDS_WORK|FAILED}

## Issues Found

| Issue ID | Severity | Description | Status |
|----------|----------|-------------|--------|
| {id} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Implementation | | | |
| QA | | | |

## Appendix: Test Code

```python
{test_code}
```
```

## LLM Instructions

When using this template:

1. **Comprehensive Coverage**: Test all aspects of the implementation
2. **Analytical Benchmarks**: Use known solutions where available
3. **CGS Units**: Verify unit consistency throughout
4. **Maxwell Traceability**: Link each test to specific articles
5. **Quantitative Results**: Report actual error values, not just pass/fail

## Variables

- `{component_name}`: What is being validated
- `{domain}`: Electrostatics, etc.
- `{citations}`: Maxwell article references
- `{test_configuration}`: How test is set up
- `{expected}`: Theoretical prediction
- `{actual}`: Computed result
- `{error_analysis}`: Discrepancy discussion

## Validation Checklist

### Physics Laws
- [ ] Gauss's law: ∇ · D = 4πρ
- [ ] No monopoles: ∇ · B = 0
- [ ] Faraday's law: ∇ × E = -(1/c)∂B/∂t
- [ ] Ampère-Maxwell: ∇ × H = (4π/c)J + (1/c)∂D/∂t
- [ ] Energy conservation
- [ ] Charge conservation: ∂ρ/∂t + ∇ · J = 0

### Boundary Conditions
- [ ] D_n discontinuity = 4πσ
- [ ] B_n continuous
- [ ] E_t continuous
- [ ] H_t discontinuity = (4π/c)K

### Limiting Behavior
- [ ] Static limit (ω → 0)
- [ ] Vacuum limit (ε → 1, μ → 1)
- [ ] Perfect conductor limit (σ → ∞)
- [ ] Small/large parameter limits

## Example Usage

```markdown
# Validation Protocol: electrostatic-field Command

## Component Information
- **Component:** `maxwell/physics/electrostatics/field.py`
- **Physics Domain:** Electrostatics
- **Maxwell Articles:** 44-49, 64-68, 75-78
- **Validator:** PHYSICUS Agent
- **Date:** 2026-04-11

## Validation Overview
This protocol validates the electrostatic field computation functions
against analytical solutions for point charges, dipoles, and standard
geometries. All tests use CGS ESU units.

## Test Categories

### 1. Analytical Solutions

| Test ID | Description | Expected | Tolerance |
|---------|-------------|----------|-----------|
| ES-001 | Point charge field | E = q/r² | 1e-10 |
| ES-002 | Dipole field on axis | E = 2p/r³ | 1e-8 |
| ES-003 | Uniformly charged sphere (inside) | E = Qr/R³ | 1e-6 |
| ES-004 | Uniformly charged sphere (outside) | E = Q/r² | 1e-10 |
| ES-005 | Infinite line charge | E = 2λ/r | 1e-4 |

### 2. Conservation Laws

| Test ID | Conservation Law | Expected | Tolerance |
|---------|------------------|----------|-----------|
| ES-CL-001 | Gauss's law (sphere) | Flux = 4πQ | 1e-6 |
| ES-CL-002 | ∇ × E = 0 | curl = 0 | 1e-8 |
| ES-CL-003 | Energy from ∫ρV | U = (1/8π)∫E² | 1e-4 |

### 3. Limiting Cases

| Test ID | Limit | Expected Behavior | Verified |
|---------|-------|---------------------|----------|
| ES-LC-001 | r → ∞ | E → 0 as 1/r² | [x] |
| ES-LC-002 | r → 0 (point charge) | Singular | [x] |
| ES-LC-003 | q → 0 | E → 0 | [x] |

## Detailed Test Results

### Test ES-001: Point Charge Field

**Setup:**
Point charge q = 1 statcoulomb at origin.
Evaluate E at r = [1, 0, 0] cm.

**Input:**
```python
q = 1.0  # statcoulomb
position = np.array([0, 0, 0])
obs_point = np.array([1, 0, 0])
```

**Expected Output:**
E = [1.0, 0, 0] statvolt/cm (exact)

**Actual Output:**
E = [1.0000000001, -2.3e-15, 1.1e-16] statvolt/cm

**Comparison:**
Relative error: |E_actual - E_expected| / |E_expected| = 1e-10

**Status:** PASS

**Notes:**
Small perpendicular components are numerical noise (machine precision).

## Summary

| Category | Tests | Passed | Failed | Score |
|----------|-------|--------|--------|-------|
| Analytical | 5 | 5 | 0 | 100% |
| Conservation | 3 | 3 | 0 | 100% |
| Limiting Cases | 3 | 3 | 0 | 100% |
| Dimensional | 4 | 4 | 0 | 100% |
| Traceability | 6 | 6 | 0 | 100% |

**Overall Score:** 100%

**Status:** VALIDATED

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | PHYSICUS | 2026-04-11 | [signed] |
```
