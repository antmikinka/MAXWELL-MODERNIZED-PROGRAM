# Task: em-induction-computation

## Description

Computes electromagnetic induction effects in coupled circuits and moving conductors from Maxwell's Part IV (Arts. 528-580). This task analyzes self-induction, mutual induction, motional EMF, and transformer action.

## Workflow Steps

### 1. System Definition
- Define circuit geometries and positions
- Specify material properties
- Identify motion parameters (if moving)
- Set initial conditions

### 2. Inductance Calculation
- **Self-inductance**: L = Φ/I for single circuit
- **Mutual inductance**: M = Φ₂₁/I₁ = Φ₁₂/I₂
- **Neumann formula**: M = (1/c²) ∮∮ (dl₁·dl₂)/r
- **Energy method**: L = 2W/I²

### 3. Induction Analysis
- **Transformer EMF**: EMF = -L dI/dt (stationary)
- **Motional EMF**: EMF = (1/c) ∫(v × B) · dl (moving)
- **General form**: EMF = -(1/c) dΦ/dt

### 4. Time-Domain Solution
- Coupled differential equations
- State-space representation
- Transient and steady-state response

## Requirements

**Input:**
- `circuits`: list - Circuit geometries and properties
- `motion`: dict - Velocity, trajectory (optional)
- `excitation`: dict - Voltage/current sources
- `time_span`: array - Time points for solution

**Output:**
- `inductance_matrix`: ndarray - L and M values
- `currents`: ndarray - I(t) for each circuit
- `emf`: ndarray - Induced EMF vs. time
- `forces`: ndarray - Magnetic forces
- `energy`: ndarray - Electrokinetic energy vs. time

## Implementation

```python
from maxwell.tasks.induction import EMInductionAnalyzer
from maxwell.circuits import CurrentLoop, Solenoid

# Problem 1: Mutual inductance of coaxial coils
coil1 = CurrentLoop(radius=5, center=[0,0,0], turns=100)
coil2 = CurrentLoop(radius=5, center=[0,0,10], turns=100)

analyzer = EMInductionAnalyzer([coil1, coil2])
L_matrix = analyzer.compute_inductance_matrix(method='elliptic_integrals')
# L11 = L22 (self), L12 = L21 (mutual)

# Problem 2: Transformer with step input
transformer = {
    'primary': {'L': 100, 'R': 1},  # cm, statohm
    'secondary': {'L': 100, 'R': 1},
    'M': 95,  # mutual inductance
    'excitation': {'type': 'voltage_step', 'value': 1.0, 'time': 0}
}

analyzer_xfmr = EMInductionAnalyzer.from_circuit(transformer)
result = analyzer_xfmr.transient_response(
    time_span=[0, 0.1],
    initial_conditions={'I1': 0, 'I2': 0}
)
# Returns: I1(t), I2(t), EMF1(t), EMF2(t)

# Problem 3: Moving conductor (railgun)
railgun = {
    'rails': {'separation': 2, 'length': 100},
    'armature': {'mass': 10, 'initial_position': 0},
    'circuit': {'L': 10, 'C': 1000, 'V0': 1000},  # Capacitor bank
    'B_external': [0, 0, 10000]  # Applied field
}

analyzer_railgun = EMInductionAnalyzer(railgun)
result = analyzer_railgun.moving_conductor_simulation(
    include_velocity=True,
    include_back_emf=True,
    include_lorentz_force=True
)
# Returns: position(t), velocity(t), current(t), force(t)

# Problem 4: Eddy currents in conducting plate
plate = {
    'geometry': 'disk',
    'radius': 10,
    'thickness': 0.5,
    'conductivity': 5.96e17,  # copper
    'excitation': {
        'type': 'time_varying_B',
        'B_amplitude': 1000,
        'frequency': 60  # Hz
    }
}

eddy_result = EMInductionAnalyzer(plate).eddy_current_analysis(
    method='analytical'  # or 'numerical'
)
# Returns: J_eddy(r), power_loss, equivalent resistance
```

## Example Problems

### 1. LR Circuit Transient
```python
# RL circuit with step voltage
# I(t) = (V/R)(1 - e^(-Rt/L))
```

### 2. Coupled Oscillators
```python
# Two LC circuits with mutual inductance
# Normal modes and beat frequency
```

### 3. Falling Loop in Magnetic Field
```python
# Conducting loop falls through B-field
# Terminal velocity from magnetic braking
```

## Validation Criteria

- [ ] L and M positive definite
- [ ] Reciprocity: M₁₂ = M₂₁
- [ ] Energy conservation: dW/dt = P_in - P_loss
- [ ] Lenz's law: EMF opposes flux change
- [ ] Low-frequency limit matches DC resistance

## Maxwell Article References

| Article | Content |
|---------|---------|
| 528-535 | Faraday's induction experiments |
| 540-545 | Vector potential and induction |
| 546-570 | Self and mutual inductance |
| 578-580 | Coupled circuit dynamics |
| 594-597 | Motional EMF |

## Related Tasks

- `magnetic-circuit-design` - Static magnetic analysis
- `wave-equation-solution` - High-frequency limit
- `circuit-analysis` - Lumped element modeling
