# Command: integration-test

## Description

Runs cross-part integration tests to verify that electromagnetic components work together correctly. Part IV implementations depend on validated Parts I-III.

## Functionality

### Integration Test Categories

1. **Cross-Part Dependencies**
   - Part IV uses Part I electrostatics
   - Part IV uses Part II current flow
   - Part IV uses Part III magnetostatics
   - All parts share unit system (CGS)

2. **Multi-Physics Tests**
   - Electromagnetic waves (E and B coupled)
   - Induction (changing B creates E)
   - Radiation (accelerating charge)
   - Waveguides (boundary + propagation)

3. **System-Level Tests**
   - Complete antenna simulation
   - Full circuit with fields
   - Multi-scale problems
   - Long-time stability

### Test Execution

- Verify interfaces between modules
- Check data flow across boundaries
- Validate end-to-end functionality
- Measure integration errors

## Usage

```python
from maxwell.quality.integration import IntegrationTester

# Create tester
tester = IntegrationTester()

# Run cross-part test
result = tester.test_cross_part(
    parts=['I', 'IV'],  # Electrostatics + EM
    scenario='radiating_dipole',
    tolerance=1e-4
)

# Run multi-physics test
result = tester.test_multi_physics(
    physics=['electrostatics', 'magnetostatics', 'conduction'],
    scenario='eddy_currents',
    tolerance=1e-3
)

# Run system test
result = tester.test_system(
    system='dipole_antenna',
    metrics=['gain', 'impedance', 'pattern'],
    tolerance=1e-2
)

# Get dependency graph
deps = tester.get_dependency_graph()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `parts` | list | Parts to integrate |
| `scenario` | str | Test scenario name |
| `tolerance` | float | Integration tolerance |
| `metrics` | list | Metrics to verify |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `result` | IntegrationResult | Pass/fail with details |
| `dependencies` | dict | Dependency graph |
| `issues` | list | Integration issues found |

## Cross-Part Dependency Matrix

| From Part | To Part | Dependency | Validation |
|-----------|---------|------------|------------|
| I (Electrostatics) | II (Electrokinematics) | E-field drives current | Required |
| I | III (Magnetism) | Analogous mathematics | Optional |
| I | IV (EM) | Static limit | Required |
| II | IV | Source currents | Required |
| III | IV | Static limit | Required |
| IV | IV | Self-consistent | Required |

## Integration Test Scenarios

### Scenario 1: Radiating Dipole
- **Parts involved**: I (dipole field) + IV (radiation)
- **Validation**: Near-field matches static dipole, far-field shows radiation
- **Maxwell Articles**: 113-116 (static) + 781-785 (waves)

### Scenario 2: Eddy Currents
- **Parts involved**: II (conduction) + III (magnetism) + IV (induction)
- **Validation**: Induced currents match Faraday's law
- **Maxwell Articles**: 528-535

### Scenario 3: Transmission Line
- **Parts involved**: I (capacitance) + II (telegraph) + III (inductance)
- **Validation**: Wave speed matches 1/√(LC)
- **Maxwell Articles**: 297-300

### Scenario 4: Waveguide
- **Parts involved**: I (boundary) + IV (propagation)
- **Validation**: Cutoff frequency matches analytical
- **Maxwell Articles**: 675-677

## Output Format

```
============================================================
INTEGRATION TEST REPORT
============================================================

Test: Radiating Dipole
Parts: I (Electrostatics) + IV (Electromagnetism)

Near-field check (r << λ):
  Expected: Static dipole field
  Actual:   Matches to 99.99%
  Status:   PASS

Far-field check (r >> λ):
  Expected: Radiation field (1/r)
  Actual:   Matches to 99.95%
  Status:   PASS

Transition region (r ~ λ):
  Expected: Smooth transition
  Actual:   Continuous to 99.9%
  Status:   PASS

============================================================
Test: Eddy Currents
Parts: II + III + IV

Induced current magnitude:
  Expected: From Faraday's law
  Actual:   Within 0.5%
  Status:   PASS

Phase relationship:
  Expected: Lenz's law (opposes change)
  Actual:   Correct direction
  Status:   PASS

============================================================
SUMMARY: 8/8 integration tests passed
============================================================
```

## Maxwell Article References

| Article | Content | Integration |
|---------|---------|-------------|
| 528-535 | Induction | II + IV |
| 604-611 | Field equations | All parts |
| 781-785 | Waves | I + IV |

## Related Commands

- `validate-physics` - Component validation
- `benchmark-performance` - System benchmarks
- `audit-citations` - Citation tracking
