# Task: conservation-law-verification

## Description

Verifies that implementations satisfy fundamental conservation laws (energy, charge, momentum, flux).

## Workflow Steps

### 1. Define System Boundaries
- Identify control volume
- Specify boundary conditions
- Define initial conditions
- Set simulation parameters

### 2. Track Conserved Quantities
- Monitor energy flows
- Track charge accumulation
- Compute momentum balance
- Verify flux conservation

### 3. Compute Balance
- Input - Output = Storage + Dissipation
- Verify balance closes within tolerance
- Identify any imbalance sources

### 4. Document Results
- Record balance errors
- Note any violations
- Assess physical correctness

## Requirements

**Input:**
- `system`: dict - System definition
- `conservation_law`: str - Law to verify
- `tolerance`: float - Acceptable error

**Output:**
- `balance`: dict - Input/output/storage
- `error`: float - Conservation error
- `status`: str - PASS/FAIL

## Implementation

```python
from maxwell.quality.tasks import ConservationLawVerification

# Configure verification
verifier = ConservationLawVerification(
    system=simulation,
    conservation_law='energy',
    tolerance=1e-4
)

# Run verification
result = verifier.verify()

print(f"Energy balance error: {result['error']}")
print(f"Status: {result['status']}")
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 85-86 | Electrostatic energy |
| 242 | Joule heating |
| 551 | Electrokinetic energy |
| 630-640 | Field energy |
