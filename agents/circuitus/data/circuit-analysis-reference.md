# Data: circuit-analysis-reference

## Purpose

Comprehensive reference data for circuit analysis in CGS units.

---

## CGS Electrical Units

### Base Units (Electrostatic CGS - ESU)

| Quantity | CGS Unit | Symbol | SI Equivalent |
|----------|----------|--------|---------------|
| Charge | statcoulomb | statC | 1 statC = 3.336×10⁻¹⁰ C |
| Current | statampere | statA | 1 statA = 3.336×10⁻¹⁰ A |
| Potential | statvolt | statV | 1 statV = 299.79 V |
| Electric Field | statvolt/cm | statV/cm | 1 statV/cm = 29979 V/m |
| Resistance | statohm | statΩ | 1 statΩ = 8.988×10¹¹ Ω |
| Capacitance | statfarad | statF | 1 statF = 1.113×10⁻¹² F |
| Conductance | s⁻¹ | - | 1 s⁻¹ (CGS) = 8.988×10¹¹ S |

### Derived Units

| Quantity | Formula | CGS Unit |
|----------|---------|----------|
| Power | P = V×I | erg/s |
| Energy | W = ∫P dt | erg |
| Admittance | Y = 1/Z | s⁻¹ |
| Impedance | Z = V/I | statohm |

### CGS Electromagnetic Units (for Inductance)

| Quantity | CGS Unit | SI Equivalent |
|----------|----------|---------------|
| Inductance | cm (or stathenry) | 1 cm = 1.113×10⁻¹² H |
| Magnetic Flux | maxwell | 1 Mx = 10⁻⁸ Wb |
| Mutual Inductance | cm | same as self-inductance |

---

## Fundamental Circuit Relations (CGS)

### Ohm's Law

```
V = I × R

where:
  V = voltage (statvolt)
  I = current (statampere)
  R = resistance (statohm)
```

### Power Relations

```
P = V × I = I² × R = V² / R

where:
  P = power (erg/s)
```

### Capacitor Relations

```
I = C × dV/dt
Q = C × V
W = (1/2) × C × V²

where:
  C = capacitance (statfarad)
  Q = charge (statcoulomb)
  W = stored energy (erg)
```

### Inductor Relations

```
V = L × dI/dt
Φ = L × I
W = (1/2) × L × I²

where:
  L = inductance (cm in CGS)
  Φ = flux linkage (maxwell)
  W = stored energy (erg)
```

---

## Time Constants

### RC Circuit

```
τ = R × C  (seconds)

where:
  R = resistance (statohm)
  C = capacitance (statfarad)
  
Dimensional check: statohm × statfarad = seconds ✓
```

### RL Circuit

```
τ = L / R  (seconds)

where:
  L = inductance (cm)
  R = resistance (statohm)
  
Dimensional check: cm / statohm = seconds ✓
```

---

## AC Circuit Analysis

### Impedance

```
Z = R + jX

where:
  R = resistance (statohm)
  X = reactance (statohm)
  
Inductive reactance: XL = ω × L
Capacitive reactance: XC = 1 / (ω × C)
```

### Admittance

```
Y = G + jB = 1 / Z

where:
  G = conductance (s⁻¹ in CGS)
  B = susceptance (s⁻¹ in CGS)
```

### Complex Power

```
S = V × I* = P + jQ

where:
  S = apparent power (erg/s)
  P = real power (erg/s)
  Q = reactive power (erg/s)
  I* = complex conjugate of current
```

### Power Factor

```
pf = cos(θ) = P / |S|

where:
  θ = phase angle between V and I
```

---

## Resonant Circuits

### Series RLC Resonance

```
Resonant frequency: ω₀ = 1 / √(L × C)

Quality factor: Q = ω₀ × L / R = 1 / (ω₀ × R × C)

Bandwidth: Δω = ω₀ / Q

where:
  ω₀ = resonant angular frequency (rad/s)
  Q = quality factor (dimensionless)
  Δω = bandwidth (rad/s)
```

### Parallel RLC Resonance

```
Resonant frequency: ω₀ = 1 / √(L × C)

Quality factor: Q = R / (ω₀ × L) = ω₀ × R × C

Bandwidth: Δω = ω₀ / Q
```

---

## Network Theorems

### Thevenin Equivalent

```
V_th = open-circuit voltage at terminals
R_th = equivalent resistance with sources zeroed

Load current: I_L = V_th / (R_th + R_L)
```

### Norton Equivalent

```
I_N = short-circuit current at terminals
R_N = equivalent resistance (same as R_th)

Load current: I_L = I_N × R_N / (R_N + R_L)
```

### Maximum Power Transfer

```
For resistive load: R_L = R_th

Maximum power: P_max = V_th² / (4 × R_th)

Efficiency at max power: 50%
```

### Superposition

```
For linear circuits with multiple sources:
Response = Σ (response due to each source acting alone)

Note: Not applicable to power calculations
```

---

## Transformer Relations

### Ideal Transformer

```
V₂ / V₁ = N₂ / N₁ = n  (turns ratio)
I₂ / I₁ = -N₁ / N₂ = -1/n

Impedance transformation: Z_in = Z_L / n²
```

### Mutual Inductance

```
M = k × √(L₁ × L₂)

where:
  M = mutual inductance (cm)
  k = coupling coefficient (0 ≤ k ≤ 1)
  L₁, L₂ = self-inductances (cm)

Coupled circuit equations:
V₁ = L₁ × dI₁/dt + M × dI₂/dt
V₂ = M × dI₁/dt + L₂ × dI₂/dt
```

---

## Three-Phase Circuits

### Wye (Y) Connection

```
Line voltage: V_L = √3 × V_φ
Line current: I_L = I_φ

Total power: P = √3 × V_L × I_L × pf
```

### Delta (Δ) Connection

```
Line voltage: V_L = V_φ
Line current: I_L = √3 × I_φ

Total power: P = √3 × V_L × I_L × pf
```

### Y-Δ Transformation

```
For balanced networks:
Z_Δ = 3 × Z_Y

Or equivalently:
Z_Y = Z_Δ / 3
```

---

## Transmission Line Parameters

### Telegrapher's Equations

```
∂V/∂z = -L × ∂I/∂t - R × I
∂I/∂z = -C × ∂V/∂t - G × V

where:
  R = resistance per unit length (statohm/cm)
  L = inductance per unit length (cm/cm)
  G = conductance per unit length (s⁻¹/cm)
  C = capacitance per unit length (statfarad/cm)
```

### Characteristic Impedance

```
Z₀ = √((R + jωL) / (G + jωC))

Lossless case: Z₀ = √(L/C)
```

### Propagation Constant

```
γ = α + jβ = √((R + jωL)(G + jωC))

where:
  α = attenuation constant (Np/cm)
  β = phase constant (rad/cm)
```

---

## Noise in Circuits

### Thermal Noise (Nyquist)

```
<v_n²> = 4 × k_B × T × R × Δf

where:
  k_B = Boltzmann constant = 1.381×10⁻¹⁶ erg/K
  T = temperature (K)
  R = resistance (statohm)
  Δf = bandwidth (Hz)
  
In CGS: v_n in statvolt
```

### Shot Noise

```
<i_n²> = 2 × q × I × Δf

where:
  q = elementary charge = 4.803×10⁻¹⁰ statcoulomb
  I = DC current (statampere)
  
In CGS: i_n in statampere
```

---

## Reference Tables

### Common Resistance Values (CGS)

| Component | SI Value | CGS Value (statohm) |
|-----------|----------|---------------------|
| 1 Ω | 1 Ω | 1.11×10⁻¹² |
| 1 kΩ | 1000 Ω | 1.11×10⁻⁹ |
| 1 MΩ | 10⁶ Ω | 1.11×10⁻⁶ |
| 1 GΩ | 10⁹ Ω | 1.11×10⁻³ |

### Common Capacitance Values (CGS)

| Component | SI Value | CGS Value (statfarad) |
|-----------|----------|----------------------|
| 1 pF | 10⁻¹² F | 0.899 |
| 1 nF | 10⁻⁹ F | 899 |
| 1 μF | 10⁻⁶ F | 8.99×10⁵ |

### Common Inductance Values (CGS)

| Component | SI Value | CGS Value (cm) |
|-----------|----------|----------------|
| 1 nH | 10⁻⁹ H | 898 |
| 1 μH | 10⁻⁶ H | 8.98×10⁵ |
| 1 mH | 10⁻³ H | 8.98×10⁸ |

---

## Maxwell Article References

| Topic | Maxwell Articles |
|-------|------------------|
| Current flow | Art. 230-235 |
| Networks, conduction | Art. 287-300 |
| Conduction theory | Art. 301-320 |
| Resistance measurement | Art. 321-342 |
| Wheatstone bridge | Art. 343-348 |
| Self-inductance | Art. 541-570 |
| Mutual inductance | Art. 541-570 |
| Field equations | Art. 604-619 |
