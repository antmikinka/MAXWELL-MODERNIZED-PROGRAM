# Data: instrument-reference

## Purpose

Comprehensive reference data for instrument parameters and specifications in CGS units.

---

## Galvanometer Reference

### Moving Coil Galvanometer Parameters

| Parameter | Typical Range | CGS Unit | Notes |
|-----------|---------------|----------|-------|
| Coil turns (N) | 10-1000 | - | More turns = higher sensitivity |
| Coil area (A) | 0.1-10 | cm² | Limited by magnet gap |
| Field strength (B) | 1000-5000 | gauss | Permanent magnet |
| Spring constant (κ) | 0.01-10 | dyne·cm/rad | Determines restoring torque |
| Moment of inertia (J) | 0.01-10 | g·cm² | Affects response time |
| Coil resistance (R) | 1-1000 | statohm | Wire gauge dependent |

### Sensitivity Formulas

```
Current sensitivity: S_I = N·A·B / κ  (cm/statampere)
Voltage sensitivity: S_V = S_I / R  (cm/statvolt)
```

### Typical Values

| Type | S_I (div/statampere) | R (statohm) | Response Time |
|------|---------------------|-------------|---------------|
| General purpose | 10⁶ | 100 | 1-2 s |
| Sensitive | 10⁸ | 500 | 5-10 s |
| Mirror | 10¹⁰ | 1000 | 10-20 s |

**Maxwell Reference:** Art. 730-750

---

## Magnetometer Reference

### Deflection Magnetometer

```
Measurement equation: H = (κ/m) · θ

where:
  κ = torsion constant (dyne·cm/rad)
  m = magnetic moment (emu)
  θ = deflection angle (rad)
  H = field strength (oersted)
```

### Vibration Magnetometer

```
Period equation: T = 2π · √(J/(m·H))

Field calculation: H = (4π²·J) / (m·T²)

where:
  J = moment of inertia (g·cm²)
  T = period (s)
```

### Typical Magnetometer Sensitivities

| Type | Range | Resolution | Best For |
|------|-------|------------|----------|
| Deflection | 0.01-100 Oe | 0.001 Oe | General purpose |
| Vibration | 0.1-1000 Oe | 0.0001 Oe | Precise measurement |
| Fluxgate | 0.0001-1 Oe | 0.00001 Oe | Low field |
| Hall effect | 1-10000 Oe | 0.1 Oe | High field |

**Maxwell Reference:** Art. 424-440, Art. 449-474

---

## Electrometer Reference

### Quadrant Electrometer

```
Torque equation: τ = (1/2) · (V_A - V_B) · V_n · (dC/dθ)

Deflection: θ = τ / κ = (1/2κ) · (V_A - V_B) · V_n · (dC/dθ)

Voltage sensitivity: S_V = θ / (V_A - V_B) = (V_n / 2κ) · (dC/dθ)
```

**Maxwell Reference:** Art. 230-235

### Vibrating Reed Electrometer

```
Output voltage: V_out = V_in · (ΔC/C) · G

where:
  ΔC = capacitance modulation amplitude
  G = amplifier gain
```

### Typical Electrometer Specifications

| Parameter | Quadrant | Vibrating Reed | Faraday Cup |
|-----------|----------|----------------|-------------|
| Voltage range | ±500 statV | ±50 statV | N/A |
| Input R | >10²⁰ statΩ | >10¹⁸ statΩ | >10²⁰ statΩ |
| Input C | <1 statF | <10 statF | <1 statF |
| Resolution | 0.001 statV | 0.00001 statV | 0.000001 statV |

---

## Physical Constants (CGS)

### Fundamental Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Speed of light | c | 2.998×10¹⁰ | cm/s |
| Boltzmann constant | k_B | 1.381×10⁻¹⁶ | erg/K |
| Elementary charge | e | 4.803×10⁻¹⁰ | statC |
| Planck constant | h | 6.626×10⁻²⁷ | erg·s |
| Avogadro's number | N_A | 6.022×10²³ | mol⁻¹ |
| Gas constant | R | 8.314×10⁷ | erg/mol·K |

### Material Properties

| Material | Property | Value | Unit |
|----------|----------|-------|------|
| Copper | Conductivity (σ) | 5.8×10¹⁷ | s⁻¹ |
| Silver | Conductivity (σ) | 6.3×10¹⁷ | s⁻¹ |
| Iron (soft) | Permeability (μ) | 5000 | dimensionless |
| Permalloy | Permeability (μ) | 100000 | dimensionless |
| Quartz | Dielectric constant (K) | 3.78 | dimensionless |
| Mica | Dielectric constant (K) | 7.0 | dimensionless |

---

## Noise Reference

### Thermal Noise

```
Voltage noise: e_n² = 4·k_B·T·R·Δf

Current noise: i_n² = 4·k_B·T·Δf / R

where:
  k_B = 1.381×10⁻¹⁶ erg/K
  T = temperature (K)
  R = resistance (statohm)
  Δf = bandwidth (Hz)
```

### Shot Noise

```
Current noise: i_n² = 2·q·I·Δf

where:
  q = 4.803×10⁻¹⁰ statC
  I = DC current (statA)
  Δf = bandwidth (Hz)
```

### Flicker Noise

```
Noise PSD: S(f) = K_f / f^α

where:
  K_f = noise coefficient
  α ≈ 1 (typically 0.8-1.2)
  f = frequency (Hz)
```

### Room Temperature Reference (T = 293 K)

```
k_B·T = 4.05×10⁻¹⁴ erg
Thermal voltage noise (R=1 statohm, Δf=1 Hz): e_n = 1.28×10⁻⁸ statvolt/√Hz
```

---

## Unit Conversions

### Electrical Units

| SI | CGS (ESU) | Conversion |
|----|-----------|------------|
| 1 V | 1/299.79 statV | 3.336×10⁻³ statV |
| 1 A | 1/(3.336×10⁻¹⁰) statA | 2.998×10⁹ statA |
| 1 Ω | 1/(8.988×10¹¹) statΩ | 1.113×10⁻¹² statΩ |
| 1 F | 1/(1.113×10⁻¹²) statF | 8.988×10¹¹ statF |
| 1 C | 1/(3.336×10⁻¹⁰) statC | 2.998×10⁹ statC |

### Magnetic Units

| SI | CGS (EMU) | Conversion |
|----|-----------|------------|
| 1 T | 10⁴ G | 10000 gauss |
| 1 A/m | 4π×10⁻³ Oe | 0.01257 oersted |
| 1 Wb | 10⁸ Mx | 10⁸ maxwell |
| 1 H | 1/(1.113×10⁻¹²) cm | 8.988×10¹¹ cm |

### Mechanical Units

| SI | CGS | Conversion |
|----|-----|------------|
| 1 N | 10⁵ dyne | 100000 dyne |
| 1 J | 10⁷ erg | 10000000 erg |
| 1 W | 10⁷ erg/s | 10000000 erg/s |
| 1 kg·m² | 10⁷ g·cm² | 10000000 g·cm² |

---

## Maxwell Article Quick Reference

| Topic | Articles |
|-------|----------|
| Electric potential | Art. 44-49 |
| Dielectrics | Art. 50-62 |
| Capacitance | Art. 75-76 |
| Current flow | Art. 230-235 |
| Resistance | Art. 287-300 |
| Magnetic fields | Art. 424-440 |
| Magnetic measurements | Art. 449-474 |
| Electromagnetic force | Art. 475-500 |
| Galvanometers | Art. 730-750 |
| Electromagnetic measurements | Art. 751-770 |

---

## Quality Criteria

- [ ] All values in CGS units
- [ ] Maxwell article references included
- [ ] Typical ranges documented
- [ ] Formulas verified
- [ ] Conversions accurate
