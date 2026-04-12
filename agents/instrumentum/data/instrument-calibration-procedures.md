# Data: instrument-calibration-procedures

## Purpose

Comprehensive reference for instrument calibration procedures following GUM methodology and traceability chains.

---

## Calibration Hierarchy

### Primary Standards

| Standard | Institution | Uncertainty | CGS Equivalent |
|----------|-------------|-------------|----------------|
| Josephson Voltage | NIST/PTB | 10^-10 (relative) | 1 V = 0.00334 statV |
| Quantum Hall Resistance | NIST/PTB | 10^-10 (relative) | 1 Ω = 1.113×10^-12 statΩ |
| Single Electron Current | NIST | 10^-7 (relative) | 1 A = 2.998×10^9 statA |

### Secondary Standards

| Standard | Uncertainty | Recalibration Interval |
|----------|-------------|----------------------|
| Weston Cell | 10 ppm | 1 year |
| Zener Reference | 10 ppm | 1 year |
| Resistance Standard | 0.1 ppm | 1 year |
| Capacitance Standard | 10 ppm | 2 years |

### Working Standards

| Standard | Uncertainty | Recalibration Interval |
|----------|-------------|----------------------|
| Laboratory Voltmeter | 100 ppm | 1 year |
| Laboratory Ohmmeter | 100 ppm | 1 year |
| Laboratory Ammeter | 100 ppm | 1 year |

### Field Instruments

| Instrument | Uncertainty | Recalibration Interval |
|------------|-------------|----------------------|
| Galvanometer | 1000 ppm | 2 years |
| Magnetometer | 1000 ppm | 2 years |
| Electrometer | 1000 ppm | 2 years |

---

## Calibration Procedures by Instrument

### Galvanometer Calibration

#### Current Sensitivity Calibration

**Procedure:**
1. Apply known currents (statA) using calibrated source
2. Measure deflection (cm) at each current
3. Plot deflection vs. current
4. Calculate sensitivity: S_I = deflection / current (cm/statA)
5. Verify linearity (R² > 0.99)

**Maxwell Reference:** Art. 730-750

**Uncertainty Budget:**
| Component | Type | Distribution | Uncertainty |
|-----------|------|--------------|-------------|
| Current source | B | Normal | 0.1% |
| Deflection measurement | B | Rectangular | 0.5 mm |
| Linearity | A | Normal | 0.2% |
| Temperature | B | Rectangular | 0.1%/K |

#### Damping Calibration

**Procedure:**
1. Displace galvanometer from equilibrium
2. Record oscillation decay
3. Calculate logarithmic decrement: δ = ln(A_n/A_{n+1})
4. Calculate damping ratio: ζ = δ / sqrt(4π² + δ²)

**Maxwell Reference:** Art. 730-750

---

### Magnetometer Calibration

#### Field Sensitivity Calibration

**Procedure:**
1. Apply known magnetic field (Oe) using Helmholtz coils
2. Measure deflection (rad) at each field
3. Plot deflection vs. field
4. Calculate sensitivity: S_H = deflection / field (rad/Oe)

**Maxwell Reference:** Art. 449-474

**Uncertainty Budget:**
| Component | Type | Distribution | Uncertainty |
|-----------|------|--------------|-------------|
| Helmholtz coil field | B | Normal | 0.1% |
| Deflection measurement | B | Rectangular | 0.01 rad |
| Alignment | B | Rectangular | 0.5% |
| Earth's field variation | B | Rectangular | 0.01 Oe |

#### Vibration Period Calibration

**Procedure:**
1. Displace magnet from equilibrium
2. Measure oscillation period (s)
3. Calculate field: H = (4π²J) / (m·T²)
4. Compare with known field

**Maxwell Reference:** Art. 449-474

---

### Electrometer Calibration

#### Voltage Sensitivity Calibration

**Procedure:**
1. Apply known voltages (statV) using calibrated source
2. Measure deflection (rad) at each voltage
3. Plot deflection vs. voltage
4. Calculate sensitivity: S_V = deflection / voltage (rad/statV)

**Maxwell Reference:** Art. 44-49, Art. 230-235

**Uncertainty Budget:**
| Component | Type | Distribution | Uncertainty |
|-----------|------|--------------|-------------|
| Voltage source | B | Normal | 0.1% |
| Deflection measurement | B | Rectangular | 0.01 rad |
| Leakage current | B | Rectangular | 0.1% |
| Temperature | B | Rectangular | 0.1%/K |

#### Charge Sensitivity Calibration

**Procedure:**
1. Apply known charge (statC) using standard capacitor
2. Measure output voltage (statV)
3. Calculate sensitivity: S_Q = V_out / Q (statV/statC)

**Maxwell Reference:** Art. 75-76

---

## Bridge Calibration Procedures

### Wheatstone Bridge Calibration

**Procedure:**
1. Use calibrated resistance standards
2. Verify bridge balance condition: R1/R2 = R3/R4
3. Measure bridge sensitivity
4. Calculate measurement uncertainty

**Maxwell Reference:** Art. 343-348

**Uncertainty Budget:**
| Component | Type | Distribution | Uncertainty |
|-----------|------|--------------|-------------|
| Standard resistors | B | Normal | 0.01% |
| Galvanometer sensitivity | B | Normal | 0.5% |
| Contact resistance | B | Rectangular | 0.01 Ω |
| Temperature coefficient | B | Rectangular | 0.01%/K |

---

## Traceability Documentation

### Calibration Certificate Requirements

**Required Information:**
- Certificate number
- Instrument identification
- Calibration date
- Next due date
- Environmental conditions
- Reference standards used (with traceability)
- Measurement results
- Uncertainty statement
- Technician signature

### Traceability Chain Documentation

**Required Elements:**
1. Primary standard identification
2. Secondary standard identification
3. Working standard identification
4. Transfer uncertainties at each level
5. Combined uncertainty calculation

### Test Uncertainty Ratio (TUR)

**Calculation:**
```
TUR = Tolerance / Uncertainty

Acceptance Criteria:
  TUR ≥ 4:1  - Acceptable
  TUR ≥ 2:1  - Marginal (use with caution)
  TUR < 2:1  - Unacceptable
```

---

## Environmental Conditions

### Standard Laboratory Conditions

| Parameter | Reference | Operating | Storage |
|-----------|-----------|-----------|---------|
| Temperature | 293 K (20°C) | 288-303 K | 263-323 K |
| Humidity | 50% RH | 30-70% RH | 10-80% RH |
| Pressure | 1 atm | 0.8-1.2 atm | - |

### Temperature Corrections

**Formula:**
```
Corrected Value = Measured Value × [1 + TC × (T - T_ref)]

where:
  TC = Temperature coefficient (ppm/K)
  T = Actual temperature (K)
  T_ref = Reference temperature (293 K)
```

---

## CGS Unit Calibration

### Voltage Calibration (statV)

| Range | Standard | Uncertainty |
|-------|----------|-------------|
| 0.01-1 statV | Zener reference | 10 ppm |
| 1-10 statV | Voltage divider | 100 ppm |
| 10-100 statV | Electrostatic voltmeter | 1000 ppm |

### Current Calibration (statA)

| Range | Standard | Uncertainty |
|-------|----------|-------------|
| 0.001-0.1 statA | Electrometer | 100 ppm |
| 0.1-1 statA | Galvanometer | 1000 ppm |
| 1-10 statA | Shunt + voltmeter | 1000 ppm |

### Resistance Calibration (statΩ)

| Range | Standard | Uncertainty |
|-------|----------|-------------|
| 0.001-0.1 statΩ | Kelvin bridge | 10 ppm |
| 0.1-10 statΩ | Wheatstone bridge | 100 ppm |
| 10-1000 statΩ | Megohmmeter | 1000 ppm |

---

## Quality Criteria

- [ ] Calibration procedures documented for all instruments
- [ ] Traceability chain established
- [ ] Uncertainty budgets complete
- [ ] Environmental conditions specified
- [ ] CGS unit calibration procedures included
- [ ] Maxwell article references provided
