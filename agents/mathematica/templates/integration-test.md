# Template: integration-test

## Description

Template for cross-component integration testing. This template ensures mathematical components work correctly together and with other agent implementations.

## Structure

```markdown
# Integration Test: {integration_test_name}

## Test ID
{test_identifier}

## Components Involved
| Component | Version | Agent |
|-----------|---------|-------|
| {component_1} | {version} | {agent} |
| {component_2} | {version} | {agent} |

## Integration Purpose
{what_integration_is_being_tested}

## Test Scenario
{description_of_test_scenario}

## Prerequisites
- [ ] All component unit tests pass
- [ ] Required data available
- [ ] Environment configured

## Test Setup

### Initial State
{required_initial_conditions}

### Test Data
{input_data_description}

### Dependencies
{required_dependencies}

## Test Execution

### Step 1: {step_name}
{action}
Expected: {expected_result}

### Step 2: {step_name}
...

## Data Flow
```
{component_1} --> {component_2} --> {component_3}
     |                |
     v                v
{output_1}      {output_2}
```

## Verification Points

| Point | Expected | Actual | Status |
|-------|----------|--------|--------|
| {point_1} | {expected} | {actual} | {PASS|FAIL} |

## Cross-Agent Dependencies

| Agent | Dependency | Status |
|-------|------------|--------|
| PHYSICUS | {dependency} | {available|pending} |
| QUALITAS | {dependency} | {available|pending} |

## Results Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Steps | {num} | - |
| Passed | {num} | - |
| Failed | {num} | - |
| Overall | - | {PASS|FAIL} |

## Issues Found
{any_integration_issues}

## Maxwell Article Traceability
{how_this_relates_to_treatise}
```

## LLM Instructions

When using this template:

1. **Identify All Components**: List every component involved
2. **Data Flow**: Show how data moves between components
3. **Verification Points**: Check integration at multiple points
4. **Cross-Agent**: Note dependencies on other agents
5. **End-to-End**: Test complete workflows

## Variables

- `{integration_test_name}`: Test name
- `{test_identifier}`: Unique ID
- All component information
- `{what_integration_is_being_tested}`: Purpose
- `{description_of_test_scenario}`: Scenario
- `{required_initial_conditions}`: Initial state
- `{input_data_description}`: Test data
- `{required_dependencies}`: Dependencies
- All step descriptions
- `{any_integration_issues}`: Issues found
- `{how_this_relates_to_treatise}`: Maxwell traceability

## Conditional Logic

IF integration involves multiple agents:
  DOCUMENT inter-agent communication protocol
  INCLUDE error handling for agent failures

IF integration is performance-critical:
  INCLUDE timing measurements
  ADD performance benchmarks

## Example Usage

```markdown
# Integration Test: Electrostatic Field Calculation

## Components Involved
| Component | Agent |
|-----------|-------|
| gradient() | MATHEMATICA |
| ScalarField | maxwell/core |
| VectorField | maxwell/core |

## Test Scenario
Compute E = -∇φ for point charge potential

## Data Flow
ScalarField (φ) --> gradient() --> VectorField (E)
```
