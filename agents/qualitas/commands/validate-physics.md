# Command: validate-physics

## Description

Runs comprehensive physics validation tests against implementations. This command executes the full validation suite including analytical solutions, conservation laws, and limiting cases.

## Functionality

### Validation Categories

1. **Analytical Solutions**
   - Point sources (charge, dipole, monopole)
   - Standard geometries (sphere, cylinder, plane)
   - Wave solutions (plane wave, waveguide, cavity)
   - Circuit benchmarks (RC, RL, RLC)

2. **Conservation Laws**
   - Energy: Input = stored + dissipated + radiated
   - Charge: ∂ρ/∂t + ∇·J = 0
   - Momentum: Maxwell stress tensor
   - Flux: Divergence theorem

3. **Maxwell's Equations**
   - Gauss's law: ∇·D = 4πρ
   - No monopoles: ∇·B = 0
   - Faraday's law: ∇×E = -(1/c)∂B/∂t
   - Ampère-Maxwell: ∇×H = (4π/c)J + (1/c)∂D/∂t

4. **Limiting Cases**
   - Static, quasi-static, wave limits
   - Material property limits
   - Geometry limits

### Validation Levels

| Level | Description | Tolerance |
|-------|-------------|-----------|
| Unit | Individual functions | 1e-10 |
| Component | Module integration | 1e-6 |
| Physics | Fundamental laws | 1e-4 |
| System | Full application | 1e-3 |

## Usage

```python
from maxwell.quality.validation import PhysicsValidator

# Create validator
validator = PhysicsValidator()

# Run full validation suite
results = validator.validate_physics(
    component='electrostatic_field',
    level='physics',  # unit, component, physics, system
    verbose=True
)

# Run specific test
result = validator.validate_point_charge(
    E_func=electric_field_point_charge,
    q=1.0,  # statcoulomb
    test_radius=1.0,  # cm
    tolerance=1e-6
)

# Get summary
summary = validator.get_summary()
print(summary)

# Generate report
report = validator.generate_report(
    format='markdown',  # or 'html', 'json', 'pdf'
    output_path='validation_report.md'
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `component` | str | Component to validate |
| `level` | str | Validation level |
| `tolerance` | float | Override default tolerance |
| `verbose` | bool | Print detailed results |
| `stop_on_fail` | bool | Stop at first failure |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `results` | list | List of ValidationResult objects |
| `summary` | dict | Summary statistics |
| `passed` | bool | Overall pass/fail |
| `report` | str | Formatted report |

## Validation Tests

### Electrostatics (Part I)
- [ ] Point charge field (Art. 44-49)
- [ ] Dipole field (Art. 69-71)
- [ ] Gauss's law (Art. 75-76)
- [ ] Conducting sphere (Art. 144-146)
- [ ] Parallel plate capacitor (Art. 124)

### Electrokinematics (Part II)
- [ ] Ohm's law (Art. 241)
- [ ] Joule heating (Art. 242)
- [ ] Kirchhoff's laws (Art. 269-286)
- [ ] Telegraph equation (Art. 297-300)

### Magnetism (Part III)
- [ ] Magnetic dipole (Art. 385-392)
- [ ] No monopoles (Art. 403-404)
- [ ] Solenoid field (Art. 675-677)
- [ ] Constitutive relation (Art. 400)

### Electromagnetism (Part IV)
- [ ] Faraday's law (Art. 528-535)
- [ ] Ampère-Maxwell (Art. 604-611)
- [ ] Wave equation (Art. 781-785)
- [ ] Plane wave (Art. 790-793)

## Maxwell Article References

| Article | Content | Validation |
|---------|---------|------------|
| 44-49 | Electric field | Point charge |
| 75-76 | Gauss's law | Flux integral |
| 241 | Ohm's law | J = σE |
| 528-535 | Induction | EMF = -dΦ/dt |
| 604-611 | Field equations | Full Maxwell |
| 781-785 | Wave equation | c = 1/√(εμ) |

## Output Format

```
============================================================
PHYSICS VALIDATION REPORT
============================================================
Component: electrostatic_field
Level: physics
Date: 2026-04-11
============================================================

Point charge field (Art. 44-49): PASS
  Expected: E = 1.000000 statvolt/cm
  Actual:   E = 1.000001 statvolt/cm
  Error:    1.0e-6 (tolerance: 1.0e-6)

Dipole field (Art. 69-71): PASS
  Expected: E = 2.000000 statvolt/cm (on-axis)
  Actual:   E = 1.999998 statvolt/cm
  Error:    1.0e-6 (tolerance: 1.0e-6)

Gauss's law (Art. 75-76): PASS
  Expected: Flux = 12.566371
  Actual:   Flux = 12.566370
  Error:    8.0e-8 (tolerance: 1.0e-6)

============================================================
SUMMARY: 15/15 tests passed (100.0%)
============================================================
```

## Related Commands

- `check-units` - Unit consistency validation
- `verify-conservation` - Conservation law checks
- `test-analytical` - Analytical solution tests
