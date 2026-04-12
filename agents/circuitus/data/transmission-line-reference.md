# Data: transmission-line-reference

## Purpose

Comprehensive reference data for transmission line analysis in CGS units.

---

## Transmission Line Types

### Coaxial Line

```
Geometry:
  a = inner conductor radius (cm)
  b = outer conductor radius (cm)
  l = length (cm)
  dielectric = material between conductors
```

**Distributed Parameters (CGS):**
```
Resistance (skin effect):
  R = 1/(2πσδ) × (1/a + 1/b)  statohm/cm
  
Inductance:
  L = (μ/2π) × ln(b/a)  cm/cm (dimensionless)
  
Capacitance:
  C = K/(2 × ln(b/a))  statfarad/cm
  
Conductance:
  G = 4πσ_d/K  s⁻¹/cm
```

where:
- σ = conductor conductivity (s⁻¹)
- δ = skin depth (cm)
- μ = permeability (dimensionless)
- K = dielectric constant (dimensionless)
- σ_d = dielectric conductivity (s⁻¹)

**Characteristic Impedance:**
```
Z0 = (1/2π) × √(μ/K) × ln(b/a)  statohm
```

---

### Two-Wire Line

```
Geometry:
  a = wire radius (cm)
  d = wire separation (cm)
  h = height above ground (cm)
```

**Distributed Parameters (CGS):**
```
Resistance:
  R = 1/(πσδa)  statohm/cm

Inductance:
  L = (μ/π) × arccosh(d/2a)  cm/cm

Capacitance:
  C = K/(2 × arccosh(d/2a))  statfarad/cm

Conductance:
  G = 4πσ_d/K  s⁻¹/cm
```

**Characteristic Impedance:**
```
Z0 = (1/π) × √(μ/K) × arccosh(d/2a)  statohm
```

**For d >> a:**
```
arccosh(d/2a) ≈ ln(d/a)

Z0 ≈ (1/π) × √(μ/K) × ln(d/a)
```

---

### Stripline (Embedded Microstrip)

```
Geometry:
  w = trace width (cm)
  h = substrate height (cm)
  t = trace thickness (cm)
  K = dielectric constant
```

**Effective Dielectric Constant:**
```
K_eff ≈ (K + 1)/2  (approximate)
```

**Characteristic Impedance:**
```
For w/h > 0.35:

Z0 ≈ (60/√K_eff) × ln(4h/(0.67πw×(0.8 + t/w)))  statohm
```

---

### Microstrip (Surface Mount)

```
Geometry:
  w = trace width (cm)
  h = substrate height (cm)
  t = trace thickness (cm)
  K = substrate dielectric constant
```

**Effective Dielectric Constant:**
```
K_eff = (K + 1)/2 + (K - 1)/2 × (1 + 10h/w)^(-0.5)
```

**Characteristic Impedance:**
```
For w/h ≤ 1:
Z0 ≈ (60/√K_eff) × ln(8h/w + w/4h)

For w/h > 1:
Z0 ≈ (120π/√K_eff) / (w/h + 1.393 + 0.667×ln(w/h + 1.444))
```

---

## Propagation Parameters

### Propagation Constant

```
γ = α + jβ = √((R + jωL)(G + jωC))

where:
  α = attenuation constant (Np/cm)
  β = phase constant (rad/cm)
  ω = angular frequency (rad/s)
```

### Attenuation Constant

```
α = Re{γ}  Np/cm

To convert to dB/cm:
  α_dB = 8.686 × α  dB/cm
```

**Low-Loss Approximation:**
```
α ≈ R/(2Z0) + G×Z0/2  Np/cm
```

**Conductor Loss:**
```
α_c = R/(2Z0)  Np/cm
```

**Dielectric Loss:**
```
α_d = G×Z0/2  Np/cm
```

### Phase Constant

```
β = Im{γ}  rad/cm

Lossless case:
  β = ω × √(LC)  rad/cm
```

### Phase Velocity

```
v_p = ω/β  cm/s

Lossless case:
  v_p = 1/√(LC)  cm/s
  
For air dielectric:
  v_p ≈ c = 3×10¹⁰ cm/s
```

### Wavelength

```
λ = 2π/β = v_p/f  cm
```

### Guided Wavelength

```
λ_g = λ_0 / √K_eff

where:
  λ_0 = free-space wavelength
  K_eff = effective dielectric constant
```

---

## Characteristic Impedance

### General Formula

```
Z0 = √((R + jωL)/(G + jωC))  statohm
```

### Special Cases

#### Lossless Line (R = 0, G = 0)
```
Z0 = √(L/C)  statohm
```

#### Low-Loss Line (R << ωL, G << ωC)
```
Z0 ≈ √(L/C) × [1 + j(R/ωL - G/ωC)/2]

≈ √(L/C)  (primarily real)
```

#### Distortionless Line (R/L = G/C)
```
Z0 = √(L/C)  (real, frequency independent)
α = √(RG)  (constant)
β = ω√(LC)  (linear with frequency)
```

---

## Input Impedance

### General Formula

```
Zin = Z0 × (ZL + Z0×tanh(γl)) / (Z0 + ZL×tanh(γl))

where:
  ZL = load impedance (statohm)
  l = line length (cm)
```

### Lossless Line

```
Zin = Z0 × (ZL + j×Z0×tan(βl)) / (Z0 + j×ZL×tan(βl))
```

### Special Cases

#### Matched Load (ZL = Z0)
```
Zin = Z0  (independent of length)
```

#### Short Circuit (ZL = 0)
```
Zin = j×Z0×tan(βl)

Pure reactance, varies from -∞ to +∞
```

#### Open Circuit (ZL = ∞)
```
Zin = -j×Z0×cot(βl)

Pure reactance, varies from +∞ to -∞
```

#### Quarter-Wave Line (l = λ/4)
```
Zin = Z0² / ZL

Impedance inverter
```

#### Half-Wave Line (l = λ/2)
```
Zin = ZL

Impedance repeater
```

---

## Reflection and VSWR

### Reflection Coefficient

```
Γ = (ZL - Z0) / (ZL + Z0)

Magnitude: |Γ| ≤ 1
Phase: ∠Γ = angle of complex Γ
```

### Special Cases

| Load | Γ |
|------|---|
| Matched (ZL = Z0) | 0 |
| Short (ZL = 0) | -1 |
| Open (ZL = ∞) | +1 |
| Pure reactance | |Γ| = 1 |

### Voltage Standing Wave Ratio (VSWR)

```
VSWR = (1 + |Γ|) / (1 - |Γ|)

Range: 1 ≤ VSWR < ∞

Inverse:
|Γ| = (VSWR - 1) / (VSWR + 1)
```

### Return Loss

```
RL = -20 × log₁₀(|Γ|)  dB

Higher RL = better match
```

---

## Power Analysis

### Incident and Reflected Power

```
P_incident = |V⁺|² / (2×Z0)  erg/s

P_reflected = |Γ|² × P_incident  erg/s

P_delivered = (1 - |Γ|²) × P_incident  erg/s
```

### Transmission Efficiency

```
η = P_delivered / P_incident × 100%
  = (1 - |Γ|²) × 100%
```

### Attenuation Loss

```
P_out = P_in × 10^(-α_dB×l/10)

where:
  α_dB = attenuation in dB/cm
  l = length in cm
```

---

## Smith Chart Relations

### Normalized Impedance

```
z = Z / Z0 = r + jx

where:
  r = normalized resistance
  x = normalized reactance
```

### Reflection Coefficient Plane

```
Γ = Γ_r + jΓ_i

|Γ| ≤ 1 (unit circle)
```

### Impedance to Reflection

```
Γ = (z - 1) / (z + 1)
```

### Reflection to Impedance

```
z = (1 + Γ) / (1 - Γ)
```

---

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| R (resistance/length) | statohm/cm | - |
| L (inductance/length) | cm/cm | dimensionless |
| G (conductance/length) | s⁻¹/cm | - |
| C (capacitance/length) | statfarad/cm | - |
| Z0 (impedance) | statohm | - |
| γ (propagation) | cm⁻¹ | - |
| α (attenuation) | Np/cm | 1 Np/cm = 8.686 dB/cm |
| β (phase) | rad/cm | - |
| v_p (velocity) | cm/s | - |
| λ (wavelength) | cm | - |

---

## Maxwell Article References

| Topic | Maxwell Articles |
|-------|------------------|
| Field equations | Art. 604-619 |
| Electromagnetic waves | Art. 781-797 |
| Conduction (loss) | Art. 287-300 |
| Energy transport | Art. 56-57, 424-430 |
| Speed of light | Art. 781-797 |

---

## Typical Values

### Coaxial Cables

| Type | Z0 (statohm) | Velocity Factor |
|------|--------------|-----------------|
| RG-58 | ~18 statohm (50 Ω) | 0.66 |
| RG-59 | ~28 statohm (75 Ω) | 0.66 |

### Microstrip

| Substrate | K | Z0 range (statohm) |
|-----------|---|---------------------|
| FR-4 | 4.5 | 17-170 |
| Alumina | 9.8 | 12-120 |
| Teflon | 2.1 | 25-250 |

---

## Quality Criteria

- [ ] Line geometry fully specified
- [ ] Distributed parameters calculated
- [ ] Z0 computed correctly
- [ ] Attenuation accounted for
- [ ] Termination effects analyzed
- [ ] Maxwell article citations included
- [ ] CGS units used throughout
