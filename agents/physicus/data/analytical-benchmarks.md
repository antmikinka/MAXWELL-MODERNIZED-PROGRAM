# Analytical Benchmarks Reference

## Overview

This document catalogues known analytical solutions for validating electromagnetic implementations. Each benchmark includes the expected CGS result and Maxwell article references.

## Benchmark Categories

### Category 1: Electrostatic Benchmarks (Part I)

#### B-ES-01: Point Charge

**Maxwell Articles**: 44-49, 66-68

**Configuration**:
- Charge: q = 1 statC at origin
- Observation: r = 1 cm on x-axis

**Expected Results**:
```
E = q/r² = 1 statV/cm (radially outward)
V = q/r = 1 statV
```

**Validation Tolerance**: 10⁻¹⁰ (machine precision for direct evaluation)

---

#### B-ES-02: Electric Dipole

**Maxwell Articles**: 69-71

**Configuration**:
- Dipole moment: p = 1 statC·cm along z-axis
- Observation: r = 10 cm

**Expected Results**:
```
On axis (θ = 0):
  E_r = 2p/r³ = 0.002 statV/cm
  E_θ = 0

Equatorial (θ = 90°):
  E_r = 0
  E_θ = p/r³ = 0.001 statV/cm
```

**Validation Tolerance**: 10⁻⁶

---

#### B-ES-03: Uniformly Charged Sphere

**Maxwell Articles**: 96-98

**Configuration**:
- Total charge: Q = 1 statC
- Radius: R = 1 cm
- Uniform volume charge density

**Expected Results**:
```
Outside (r > R):
  E = Q/r²
  V = Q/r

Inside (r < R):
  E = Qr/R³ = Qr (since R=1)
  V = Q(3R² - r²)/(2R³) = (3 - r²)/2
```

**Validation Tolerance**: 10⁻⁶

---

#### B-ES-04: Conducting Sphere in Uniform Field

**Maxwell Articles**: 155-160

**Configuration**:
- Sphere radius: R = 1 cm, grounded
- Applied field: E₀ = 1 statV/cm along z

**Expected Results**:
```
Potential:
  V = -E₀r cosθ + E₀R³ cosθ/r²

Field on axis (z > R):
  E_z = E₀(1 + 2R³/z³)

Surface charge density:
  σ = (3E₀/4π) cosθ
```

**Validation Tolerance**: 10⁻⁶

---

#### B-ES-05: Point Charge Near Conducting Plane

**Maxwell Articles**: 161

**Configuration**:
- Charge: q = 1 statC at (0, 0, d), d = 2 cm
- Conducting plane at z = 0

**Expected Results**:
```
Image charge: q' = -q at (0, 0, -d)

Force on charge:
  F = q²/(4d²) = 1/16 = 0.0625 dyne (attractive)

Potential at (x, y, z > 0):
  V = q/√(x² + y² + (z-d)²) - q/√(x² + y² + (z+d)²)
```

**Validation Tolerance**: 10⁻⁶

---

### Category 2: Magnetostatic Benchmarks (Part III)

#### B-MS-01: Magnetic Dipole

**Maxwell Articles**: 387-388

**Configuration**:
- Dipole moment: m = 1 emu along z-axis
- Observation: r = 10 cm

**Expected Results**:
```
On axis (θ = 0):
  H_r = 2m/r³ = 0.002 Oe
  H_θ = 0

Equatorial (θ = 90°):
  H_r = 0
  H_θ = m/r³ = 0.001 Oe
```

**Validation Tolerance**: 10⁻⁶

---

#### B-MS-02: Uniformly Magnetized Sphere

**Maxwell Articles**: 431-433

**Configuration**:
- Radius: R = 1 cm
- Magnetization: M = 100 emu/cm³ along z

**Expected Results**:
```
Inside:
  H = -(4π/3)M = -418.88 Oe (demagnetizing field)
  B = H + 4πM = (8π/3)M = 837.76 G

Outside:
  Dipole field with m = (4π/3)R³M = 418.88 emu
```

**Validation Tolerance**: 10⁻⁶

---

#### B-MS-03: Infinite Straight Wire

**Maxwell Articles**: 475-479

**Configuration**:
- Current: I = 1 abA along z-axis

**Expected Results**:
```
Magnetic field (CGS Gaussian):
  H = 2I/(cr) = 2/(3×10¹⁰ × r) Oe

At r = 1 cm:
  H = 6.67×10⁻¹¹ Oe
```

**Validation Tolerance**: 10⁻⁶

---

#### B-MS-04: Circular Current Loop

**Maxwell Articles**: 694-696

**Configuration**:
- Current: I = 1 abA
- Radius: a = 1 cm

**Expected Results**:
```
On axis (z):
  B_z = (2πI/c) a²/(z² + a²)^(3/2)
  
At center (z = 0):
  B_z = 2πI/(ca) = 2.09×10⁻¹⁰ G
```

**Off-axis**: Requires elliptic integrals

**Validation Tolerance**: 10⁻⁶ (on-axis), 10⁻⁴ (off-axis)

---

#### B-MS-05: Infinite Solenoid

**Maxwell Articles**: 675-677

**Configuration**:
- Turns per length: n = 100 turns/cm
- Current: I = 1 abA

**Expected Results**:
```
Inside:
  B = (4π/c)nI = (4π/3×10¹⁰) × 100 × 1 = 4.19×10⁻⁸ G

Outside:
  B = 0
```

**Validation Tolerance**: 10⁻⁶ (inside), 10⁻¹⁰ (outside)

---

### Category 3: Electromagnetic Benchmarks (Part IV)

#### B-EM-01: Plane Wave in Vacuum

**Maxwell Articles**: 790-791

**Configuration**:
- Frequency: ω = 2π×10¹⁰ rad/s
- E amplitude: E₀ = 1 statV/cm
- Propagation: +z direction

**Expected Results**:
```
Wavelength:
  λ = 2πc/ω = 3 cm

Field relation:
  |E| = |B| (in CGS Gaussian)

Phase velocity:
  v = c = 2.998×10¹⁰ cm/s

Poynting vector (time-averaged):
  <S> = (c/8π)E₀² = 1.19×10⁹ erg/cm²/s
```

**Validation Tolerance**: 10⁻⁶

---

#### B-EM-02: Wave in Dielectric

**Maxwell Articles**: 794-797

**Configuration**:
- Frequency: ω = 2π×10¹⁰ rad/s
- Permittivity: ε = 4
- E amplitude: E₀ = 1 statV/cm

**Expected Results**:
```
Refractive index:
  n = √ε = 2

Wavelength in medium:
  λ = λ₀/n = 1.5 cm

Phase velocity:
  v = c/n = 1.499×10¹⁰ cm/s
```

**Validation Tolerance**: 10⁻⁶

---

#### B-EM-03: Skin Depth in Conductor

**Maxwell Articles**: 798-800

**Configuration**:
- Frequency: f = 60 Hz (ω = 377 rad/s)
- Conductivity: σ = 5.96×10¹⁷ s⁻¹ (copper)

**Expected Results**:
```
Skin depth:
  δ = c/√(2πσω) = 0.85 cm

Attenuation:
  E(z) = E₀ exp(-z/δ)
```

**Validation Tolerance**: 10⁻⁴

---

### Category 4: Energy Benchmarks

#### B-Energy-01: Capacitor Energy

**Maxwell Articles**: 85a-b, 630-638

**Configuration**:
- Parallel plate capacitor
- Area: A = 100 cm²
- Separation: d = 0.1 cm
- Voltage: V = 1 statV

**Expected Results**:
```
Capacitance:
  C = A/(4πd) = 79.58 cm

Energy:
  U = (1/2)CV² = 39.79 erg

Energy density:
  u = E²/(8π) where E = V/d = 10 statV/cm
  u = 3.98 erg/cm³
```

**Validation Tolerance**: 10⁻⁶

---

#### B-Energy-02: Inductor Energy

**Maxwell Articles**: 551-552, 630-638

**Configuration**:
- Solenoid with L = 10 cm (inductance in CGS)
- Current: I = 1 abA

**Expected Results**:
```
Energy:
  U = (1/2)LI²/c² = (1/2)×10×1²/(3×10¹⁰)² = 5.56×10⁻²¹ erg
```

**Validation Tolerance**: 10⁻⁶

---

## Validation Protocol

For each benchmark:

1. **Setup**: Configure problem exactly as specified
2. **Compute**: Run implementation
3. **Compare**: Check against expected result
4. **Tolerance**: Verify within specified tolerance
5. **Document**: Record pass/fail with actual values

## Tolerance Standards

| Benchmark Type | Standard Tolerance |
|---------------|-------------------|
| Analytical (direct) | 10⁻¹⁰ |
| Analytical (series) | 10⁻⁶ |
| Semi-analytical | 10⁻⁴ |
| Numerical reference | 10⁻³ |

## Related Documents

- `cgs-electromagnetic-units.md` - Unit reference
- `tolerance-standards.md` - Error tolerances
- `test-case-database.md` - Test organization
