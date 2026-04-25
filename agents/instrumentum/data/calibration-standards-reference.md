# Data: calibration-standards-reference

## Purpose

Comprehensive reference data for calibration standards and traceability chains.

---

## Primary Standards

### National Metrology Institutes

| Institution | Country | Established | Specialty |
|-------------|---------|-------------|-----------|
| NIST | USA | 1901 | All physical quantities |
| PTB | Germany | 1871 | Electrical, time |
| NPL | UK | 1900 | Electrical, mass |
| NRC | Canada | 1932 | Electrical, optical |
| METAS | Switzerland | 1862 | Electrical, pressure |

### Electrical Primary Standards

#### Voltage Standard (Josephson)

```
Voltage definition: V = (n·f) / K_J

where:
  K_J = 2e/h = 483597.9 GHz/V (Josephson constant)
  f = microwave frequency
  n = integer (step number)
  
Realization uncertainty: ~10⁻¹⁰ (relative)
```

#### Resistance Standard (Quantum Hall)

```
Resistance definition: R_H = h/(e²·i) = R_K / i

where:
  R_K = h/e² = 25812.807 Ω (von Klitzing constant)
  i = integer (Landau level index)
  
Realization uncertainty: ~10⁻¹⁰ (relative)
```

#### Current Standard (Single Electron Transport)

```
Current definition: I = n·e·f

where:
  n = number of electrons per cycle
  e = elementary charge
  f = clock frequency
  
Realization uncertainty: ~10⁻⁷ (relative)
```

---

## Secondary Standards

### Working Reference Standards

| Standard Type | Typical Uncertainty | Recalibration Interval |
|---------------|--------------------|----------------------|
| Standard cell (Weston) | 1 ppm | 1 year |
| Zener reference | 10 ppm | 1 year |
| Resistance standard | 0.1 ppm | 1 year |
| Capacitance standard | 10 ppm | 2 years |
| Inductance standard | 10 ppm | 2 years |

### Weston Standard Cell

```
EMF at 20°C: E = 1.0183 V (saturated)
Temperature coefficient: -40 μV/K
Uncertainty: ±10 μV (10 ppm)

CGS equivalent: 1.0183 V = 0.00340 statvolt
```

### Zener Reference

```
Reference voltage: 6.95 V (typical)
Temperature coefficient: ±1 ppm/K
Long-term drift: ±10 ppm/year

CGS equivalent: 6.95 V = 0.0232 statvolt
```

### Resistance Standard

```
Nominal values: 1 Ω, 10 Ω, 100 Ω, 1 kΩ, 10 kΩ
Tolerance: ±0.01%
Temperature coefficient: ±1 ppm/K

CGS equivalent: 1 Ω = 1.113×10⁻¹² statohm
```

---

## Calibration Hierarchy

### Traceability Chain Example

```
Level 1: NIST Primary Standard (Quantum Hall)
         Uncertainty: 0.001 ppm
         ↓ (transfer uncertainty: 0.01 ppm)
         
Level 2: Accredited Lab Secondary Standard
         Uncertainty: 0.01 ppm
         ↓ (process uncertainty: 0.1 ppm)
         
Level 3: Working Standard
         Uncertainty: 0.1 ppm
         ↓ (process uncertainty: 1 ppm)
         
Level 4: Field Instrument
         Uncertainty: 1 ppm
```

### Test Uncertainty Ratio (TUR)

```
TUR = Tolerance / Uncertainty

Acceptance criteria:
  TUR ≥ 4:1  - Acceptable
  TUR ≥ 2:1  - Marginal (use with caution)
  TUR < 2:1  - Unacceptable
```

---

## Calibration Procedures Reference

### General Calibration Steps

1. **Preparation**
   - Verify environmental conditions
   - Allow warm-up time
   - Clean connections

2. **Zero Adjustment**
   - Apply zero input
   - Adjust zero reading
   - Verify stability

3. **Span Calibration**
   - Apply known standard values
   - Compare readings
   - Adjust if necessary

4. **Linearity Check**
   - Apply multiple points
   - Record deviations
   - Document non-linearity

5. **Verification**
   - Apply check standards
   - Verify accuracy
   - Document results

---

## Environmental Conditions

### Standard Laboratory Conditions

| Parameter | Reference | Operating | Storage |
|-----------|-----------|-----------|---------|
| Temperature | 20°C (293 K) | 15-30°C | -10-50°C |
| Humidity | 50% RH | 30-70% RH | 10-80% RH |
| Pressure | 1 atm | 0.8-1.2 atm | - |

### Temperature Effects

```
Drift = TC × ΔT

where:
  TC = temperature coefficient (ppm/K)
  ΔT = deviation from reference (K)
```

### Humidity Effects

```
Leakage current increase at high humidity
Dielectric absorption changes
Mechanical property changes
```

---

## Uncertainty Components

### Type A Evaluation (Statistical)

| Source | Evaluation Method |
|--------|------------------|
| Repeatability | Standard deviation of mean |
| Resolution | Standard deviation of readings |
| Random effects | Statistical analysis |

### Type B Evaluation (Non-Statistical)

| Source | Distribution | Divisor |
|--------|-------------|---------|
| Calibration certificate | Normal | k (from cert) |
| Resolution | Rectangular | √3 |
| Temperature effect | Rectangular | √3 |
| Non-linearity | Rectangular | √3 |
| Drift | Rectangular | √3 |

---

## Maxwell's Measurement Principles

### Accuracy Discussion

Maxwell emphasized the importance of:
- Proper instrument design (Art. 730-750)
- Accurate standards (Art. 287-300)
- Careful measurement technique
- Error analysis and correction

### Calibration Methods

From Maxwell's Treatise:
- Wheatstone bridge (Art. 343-348)
- Potentiometric methods (Art. 230-235)
- Null methods for precision

---

## CGS Unit Reference

### Electrical Standards in CGS

| Standard | SI Value | CGS Value |
|----------|----------|-----------|
| Weston cell | 1.0183 V | 0.00340 statV |
| 1 Ω resistor | 1 Ω | 1.113×10⁻¹² statΩ |
| 1 V reference | 1 V | 0.00334 statV |
| 1 A source | 1 A | 2.998×10⁹ statA |

### Calibration Uncertainties in CGS

```
For a 1 statV reference with 10 ppm uncertainty:
u = 1 statV × 10×10⁻⁶ = 1×10⁻⁵ statV
```

---

## Quality Criteria

- [ ] Standards traceable to national standards
- [ ] Calibration certificates current
- [ ] Uncertainties documented
- [ ] Environmental conditions controlled
- [ ] Maxwell article citations included
