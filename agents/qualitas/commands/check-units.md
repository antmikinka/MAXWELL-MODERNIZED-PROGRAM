# Command: check-units

## Description

Verifies CGS unit consistency across all implementations. This command performs dimensional analysis and ensures all equations use CGS units correctly.

## Functionality

### Dimensional Analysis

1. **Base Dimension Verification**
   - Length [L]: centimeter
   - Mass [M]: gram
   - Time [T]: second
   - Charge [Q]: statcoulomb (ESU) or abcoulomb (EMU)

2. **Derived Dimension Checks**
   - Force: [M L T⁻²] = dyne
   - Energy: [M L² T⁻²] = erg
   - Electric field: [M¹/² L⁻¹/² T⁻¹] = statvolt/cm
   - Magnetic field: [M¹/² L⁻¹/² T⁻¹] = gauss

3. **Equation Consistency**
   - Both sides have same dimensions
   - Arguments to transcendental functions dimensionless
   - Exponents dimensionless

### CGS Variant Checking

4. **ESU vs EMU vs Gaussian**
   - ESU: Electric quantities from Coulomb's law
   - EMU: Magnetic quantities from Ampère's law
   - Gaussian: Mixed (electric in ESU, magnetic in EMU)

5. **Factor Verification**
   - 4π factors in source terms
   - c factors in time-varying equations
   - No ε₀ or μ₀ (SI concepts)

## Usage

```python
from maxwell.quality.unit_checker import UnitChecker

# Create checker
checker = UnitChecker()

# Check a function's dimensional consistency
result = checker.check_function(
    func=electric_field_point_charge,
    expected_dimensions={'E': 'statvolt/cm'},
    input_dimensions={'q': 'statcoulomb', 'r': 'cm'}
)

# Check module-wide consistency
report = checker.check_module('maxwell.physics.electrostatics')

# Verify constant values
constants_ok = checker.verify_constants({
    'c': 29979245800,  # cm/s
    'e': 4.80320471e-10,  # statcoulomb
    'epsilon_0': None  # Should not exist in CGS
})

# Check for SI contamination
si_contamination = checker.find_si_concepts()
# Returns: list of ε₀, μ₀, etc. usage
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `func` | callable | Function to check |
| `expected_dimensions` | dict | Expected output dimensions |
| `input_dimensions` | dict | Input parameter dimensions |
| `module_path` | str | Module to check |
| `strict` | bool | Fail on any inconsistency |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `result` | UnitCheckResult | Pass/fail with details |
| `report` | str | Detailed report |
| `issues` | list | List of dimension errors |

## Common Dimension Errors

### Missing c Factor
```python
# Wrong (SI-like):
E = -∂A/∂t

# Correct (CGS Gaussian):
E = -(1/c) ∂A/∂t
```

### Missing 4π Factor
```python
# Wrong (SI-like):
∇·D = ρ

# Correct (CGS):
∇·D = 4πρ
```

### Using ε₀ or μ₀
```python
# Wrong (SI concepts):
D = ε₀ E + P
B = μ₀ (H + M)

# Correct (CGS Gaussian):
D = E + 4πP
B = H + 4πM
```

## Dimensional Analysis Examples

### Electrostatic Energy
```
U = (1/8π) ∫ E² dV

[U] = [E]² [L]³
    = (statvolt/cm)² cm³
    = (dyne/statcoulomb)² cm³
    = (g·cm/s² / (g¹/²·cm³/²/s))² cm³
    = (g¹/²·cm⁻¹/²/s)² cm³
    = g·cm⁻¹·s⁻² · cm³
    = g·cm²/s²
    = erg ✓
```

### Wave Speed
```
v = 1/√(εμ)

[v] = 1/√([ε][μ])
    = 1/√(1 × 1)  (both dimensionless in CGS)
    = dimensionless... but should be L/T

Actually in CGS Gaussian:
v = c/√(ε_r μ_r)
[v] = [c] = cm/s ✓
```

## Output Format

```
============================================================
UNIT CONSISTENCY CHECK
============================================================
Module: maxwell.physics.electrostatics
============================================================

Function: electric_field_point_charge
  Input dimensions:
    q: [M¹/² L³/² T⁻¹] statcoulomb ✓
    r: [L] cm ✓
  Output dimensions:
    E: [M¹/² L⁻¹/² T⁻¹] statvolt/cm ✓
  Status: PASS

Function: potential_point_charge
  Input dimensions:
    q: [M¹/² L³/² T⁻¹] statcoulomb ✓
    r: [L] cm ✓
  Output dimensions:
    V: [M¹/² L¹/² T⁻¹] statvolt ✓
  Status: PASS

============================================================
SI CONTAMINATION CHECK
============================================================
No ε₀ or μ₀ usage found ✓
All constants use CGS values ✓

============================================================
SUMMARY: 12/12 functions pass unit check
============================================================
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 41-42 | Dimensions and units |
| 604-611 | Field equations (CGS form) |
| 786-787 | Speed of light derivation |

## Related Commands

- `validate-physics` - Full physics validation
- `verify-conservation` - Conservation laws
- `audit-citations` - Citation verification
