# Command: test-analytical

## Description

Compares numerical implementations against known analytical solutions. This command provides benchmark tests for validation.

## Functionality

### Analytical Solution Categories

1. **Electrostatic Solutions**
   - Point charge: E = q/r²
   - Dipole: E = [3(p·r̂)r̂ - p]/r³
   - Conducting sphere in uniform field
   - Dielectric sphere in uniform field
   - Parallel plate capacitor
   - Infinite line charge
   - Infinite plane sheet

2. **Magnetostatic Solutions**
   - Magnetic dipole: B = [3(m·r̂)r̂ - m]/r³
   - Circular loop (on axis)
   - Infinite solenoid: B = 4πnI/c
   - Finite solenoid (on axis)
   - Infinite straight wire: B = 2I/(cr)

3. **Wave Solutions**
   - Plane wave in vacuum: |E| = |B|
   - Plane wave in dielectric: v = c/n
   - Plane wave in conductor: skin depth
   - Waveguide modes
   - Cavity resonances

4. **Circuit Solutions**
   - RC charging: V(t) = V₀(1 - e^(-t/RC))
   - RL transient: I(t) = (V/R)(1 - e^(-Rt/L))
   - RLC response
   - Transformer equations

### Test Execution

- Compare numerical output to analytical formula
- Compute relative error
- Verify error within tolerance
- Report pass/fail status

## Usage

```python
from maxwell.quality.analytical_tests import AnalyticalTestSuite

# Create test suite
suite = AnalyticalTestSuite()

# Run specific test
result = suite.run_test(
    test_name='point_charge_field',
    implementation=electric_field_point_charge,
    tolerance=1e-6
)

# Run all electrostatics tests
results = suite.run_category('electrostatics')

# Run full benchmark suite
full_results = suite.run_all()

# Get summary
summary = suite.get_summary()
print(summary)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `test_name` | str | Name of test to run |
| `implementation` | callable | Function to test |
| `tolerance` | float | Error tolerance |
| `category` | str | Test category |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `result` | TestResult | Pass/fail with error |
| `results` | list | List of test results |
| `summary` | dict | Summary statistics |

## Test Catalog

### Electrostatics Tests

| Test ID | Description | Maxwell Article | Tolerance |
|---------|-------------|-----------------|-----------|
| ES-001 | Point charge field | 44-49 | 1e-10 |
| ES-002 | Electric dipole | 69-71, 113-116 | 1e-8 |
| ES-003 | Conducting sphere | 144-146 | 1e-6 |
| ES-004 | Dielectric sphere | 144-146 | 1e-6 |
| ES-005 | Parallel plate | 124 | 1e-4 |
| ES-006 | Line charge | 126-127 | 1e-4 |
| ES-007 | Gauss's law | 75-76 | 1e-6 |

### Magnetostatics Tests

| Test ID | Description | Maxwell Article | Tolerance |
|---------|-------------|-----------------|-----------|
| MS-001 | Magnetic dipole | 385-392 | 1e-8 |
| MS-002 | Circular loop (axis) | 694-696 | 1e-6 |
| MS-003 | Infinite solenoid | 675-677 | 1e-6 |
| MS-004 | Straight wire | 475-479 | 1e-4 |
| MS-005 | No monopoles (∇·B=0) | 403-404 | 1e-8 |

### Wave Tests

| Test ID | Description | Maxwell Article | Tolerance |
|---------|-------------|-----------------|-----------|
| EM-001 | Plane wave speed | 786-787 | 1e-10 |
| EM-002 | |E| = |B| | 790-791 | 1e-8 |
| EM-003 | Skin depth | 798-801 | 1e-4 |
| EM-004 | Waveguide cutoff | 675-677 | 1e-4 |
| EM-005 | Cavity resonance | - | 1e-4 |

## Output Format

```
============================================================
ANALYTICAL SOLUTION TESTS
============================================================

ES-001: Point charge field
  Implementation: electric_field_point_charge
  Expected: E = 1.000000 statvolt/cm
  Actual:   E = 1.000000 statvolt/cm
  Error:    2.3e-13
  Status:   PASS (tolerance: 1.0e-10)

ES-002: Electric dipole
  Implementation: electric_field_dipole
  Expected: E = 2.000000 statvolt/cm (on-axis)
  Actual:   E = 1.999998 statvolt/cm
  Error:    1.1e-06
  Status:   PASS (tolerance: 1.0e-08)

ES-003: Conducting sphere in uniform field
  Implementation: conducting_sphere_field
  Expected: E_surface = 3.000000 E_0
  Actual:   E_surface = 2.999985 E_0
  Error:    5.0e-06
  Status:   PASS (tolerance: 1.0e-06)

============================================================
SUMMARY: 15/15 tests passed (100.0%)
Average error: 3.2e-07
============================================================
```

## Maxwell Article References

See test catalog above for article mappings.

## Related Commands

- `validate-physics` - Full validation suite
- `verify-conservation` - Conservation laws
- `convergence-study` - Numerical accuracy
