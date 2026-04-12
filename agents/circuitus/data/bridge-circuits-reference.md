# Data: bridge-circuits-reference

## Purpose

Comprehensive reference data for bridge circuits in CGS units.

---

## DC Bridges

### Wheatstone Bridge

```
        V_s
         +
         |
    +----+----+
    |    |    |
   R1    R3   G (galvanometer)
    |    |    |
    A----+----B
    |    |    |
   R2    R4   (unknown)
    |    |    |
    +----+----+
         |
         -
```

**Balance Condition:**
```
R1 / R2 = R3 / R4

or: R1 × R4 = R2 × R3
```

**Unknown Resistance:**
```
R4 = R3 × (R2 / R1)
```

**Sensitivity:**
```
S = dθ / (ΔR/R)  (galvanometer deflection per unit fractional change)

Maximum sensitivity when: R1 = R2 = R3 = R4
```

**Maxwell Reference:** Art. 343-348

---

### Kelvin Double Bridge

For low resistance measurement (< 1 statohm).

```
Configuration:
- Main ratio arms: M, N
- Auxiliary ratio arms: m, n  
- Standard resistor: Rs
- Unknown resistor: Rx
- Link resistance: r
```

**Balance Condition:**
```
Rx / Rs = M / N = m / n

Unknown: Rx = Rs × (M / N)
```

**Error from Link Resistance:**
```
Error is negligible when M/N = m/n exactly
```

**Range:** 0.001 to 1 statohm
**Accuracy:** 0.02% to 0.1%

---

### Callendar-Griffiths Bridge

For platinum resistance thermometer measurements.

**Configuration:**
- Equal ratio arms
- Slide wire for fine adjustment
- Compensating leads

**Application:** Temperature measurement

---

## AC Bridges

### Maxwell Bridge

For inductance measurement.

```
        V_s (AC)
         +
         |
    +----+----+
    |    |    |
   R1    R3   D (detector)
    |    |    |
   C1    R2   Lx (unknown)
    |    |    | (with Rx)
    +----+----+
         |
         -
```

**Balance Conditions:**
```
Real: R1 × R4 = R2 × R3

Imaginary: Lx = R2 × R3 × C1
```

**Unknown Inductance:**
```
Lx = R2 × R3 × C1

Rx = (R2 × R3) / R1
```

**Maxwell Reference:** Art. 541-570

**Advantages:**
- Simple calculation
- Independent of frequency
- Suitable for medium-Q coils (Q = 1-10)

---

### Hay Bridge

For high-Q inductance measurement.

```
Configuration:
- Arm 1: R1 in series with C1
- Arm 2: R2 (standard)
- Arm 3: R3 (standard)  
- Arm 4: Lx with Rx (unknown)
```

**Balance Conditions:**
```
Lx = (R2 × R3 × C1) / (1 + ω² × R1² × C1²)

Rx = (ω² × R1 × R2 × R3 × C1²) / (1 + ω² × R1² × C1²)
```

**Q Factor:**
```
Q = 1 / (ω × R1 × C1)
```

**Application:** High-Q coils (Q > 10)

---

### Schering Bridge

For capacitance and loss angle measurement.

```
Configuration:
- Arm 1: C1 (standard)
- Arm 2: R2 in parallel with C2
- Arm 3: R3 (standard)
- Arm 4: Cx with Rx (unknown)
```

**Balance Conditions:**
```
Cx = C1 × (R4 / R3)

tan(δ) = ω × C4 × R4
```

**Loss Angle:**
```
tan(δ) = 1 / (ω × Cx × Rx)
```

**Application:** Capacitor testing, dielectric loss measurement

---

### Wien Bridge

For frequency measurement and oscillator applications.

```
Configuration:
- Arm 1: R1 in series with C1
- Arm 2: R2 in parallel with C2
- Arm 3: R3 (standard)
- Arm 4: R4 (standard)
```

**Balance Conditions:**
```
Frequency: ω² = 1 / (R1 × R2 × C1 × C2)

Amplitude: R3 / R4 = (C1/C2) + (R2/R1)
```

**For equal components (R1=R2=R, C1=C2=C):**
```
ω = 1 / (R × C)
f = 1 / (2π × R × C)

R3 / R4 = 2
```

**Application:** Frequency measurement, audio oscillators

---

### Anderson Bridge

For precise inductance measurement.

```
Modified Maxwell bridge with additional impedance
```

**Balance Conditions:**
```
Lx = C × R2 × R3 × (1 + R4/R2)

Rx = (R2 × R3) / R1
```

**Advantages:**
- More accurate than Maxwell bridge
- Less sensitive to component tolerances

---

## Bridge Comparison

| Bridge Type | Measures | Range | Frequency | Accuracy |
|-------------|----------|-------|-----------|----------|
| Wheatstone | Resistance | 1-10⁶ statohm | DC | 0.01% |
| Kelvin | Low R | 0.001-1 statohm | DC | 0.02% |
| Maxwell | Inductance | Medium L | Any | 0.1% |
| Hay | High-Q L | High L | Fixed | 0.1% |
| Schering | Capacitance | All C | Fixed | 0.1% |
| Wien | Frequency | Audio | Variable | 0.1% |
| Anderson | Inductance | Precision | Any | 0.05% |

---

## Error Sources in Bridge Measurements

### Systematic Errors

| Source | Effect | Mitigation |
|--------|--------|------------|
| Lead resistance | Adds to measured R | Use Kelvin connection |
| Contact resistance | Adds uncertainty | Clean contacts |
| Thermal EMF | DC offset | Use AC or reverse polarity |
| Stray capacitance | AC measurement error | Shield properly |
| Stray inductance | High frequency error | Minimize lead length |
| Component tolerance | Balance point error | Use precision standards |

### Random Errors

| Source | Effect | Mitigation |
|--------|--------|------------|
| Detector noise | Balance uncertainty | Use sensitive detector |
| Temperature drift | Value drift | Temperature control |
| Vibration | Contact variation | Stable mounting |

---

## Detector Types

### Galvanometer (DC Bridges)

- Sensitivity: 10⁻⁹ to 10⁻¹¹ statampere/division
- Internal resistance: 10-1000 statohm
- Period: 1-10 seconds

### Electronic Null Detector (AC Bridges)

- Sensitivity: microvolt level
- Frequency range: DC to MHz
- Input impedance: high (> 10⁹ statohm)

### Lock-in Amplifier

- Ultimate sensitivity
- Frequency selective
- Phase-sensitive detection

---

## CGS Unit Reference for Bridges

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Resistance | statohm | 1 statohm = 8.988×10¹¹ Ω |
| Capacitance | statfarad | 1 statfarad = 1.113×10⁻¹² F |
| Inductance | cm | 1 cm = 1.113×10⁻¹² H |
| Voltage (DC) | statvolt | 1 statvolt = 299.79 V |
| Voltage (AC) | statvolt (rms) | same |
| Current | statampere | 1 statampere = 3.336×10⁻¹⁰ A |
| Frequency | Hz (same) | - |
| Angular freq | rad/s | ω = 2πf |

---

## Maxwell's Contributions

### Wheatstone Bridge Analysis

Maxwell provided detailed analysis of the Wheatstone bridge in Art. 343-348, including:

- Balance condition derivation
- Sensitivity analysis
- Error analysis
- Practical measurement procedures

### Resistance Measurement

In Art. 287-300, Maxwell discussed:

- Ohm's law verification
- Resistance standards
- Current distribution in networks
- Measurement techniques

### Inductance Measurement

In Art. 541-570, Maxwell covered:

- Self-inductance definition
- Mutual inductance
- Bridge methods for L measurement
- The Maxwell bridge configuration

---

## Practical Measurement Procedures

### General Bridge Measurement Steps

1. **Setup**
   - Connect bridge according to schematic
   - Verify all connections
   - Select appropriate range

2. **Initial Balance**
   - Apply source
   - Adjust coarse controls
   - Observe detector

3. **Fine Balance**
   - Adjust fine controls
   - Minimize detector reading
   - Verify true null

4. **Reading**
   - Record standard values
   - Calculate unknown
   - Apply corrections

5. **Verification**
   - Check with alternate method
   - Verify reasonableness
   - Document results

---

## Quality Criteria

- [ ] Bridge type appropriate for measurand
- [ ] Balance condition correctly derived
- [ ] Standard values traceable
- [ ] Detector sensitivity adequate
- [ ] Error sources identified
- [ ] Uncertainty budget complete
- [ ] Maxwell article citations included
