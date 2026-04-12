# Analytical Solutions Catalog

## Purpose

Comprehensive catalog of analytical solutions to electromagnetic problems. These solutions serve as validation benchmarks and provide physical insight.

## Electrostatic Solutions (Part I)

### Point Sources

#### Point Charge
**Maxwell Articles:** 44-49, 64-68

**Potential:**
```
V(r) = q/r  (CGS ESU)
```

**Electric Field:**
```
E(r) = q·r̂/r²
```

**Validation:** Implemented in `electric_field_point_charge()`

---

#### Electric Dipole
**Maxwell Articles:** 69-71, 113-116

**Potential:**
```
V(r) = (p·r̂)/r² = (p·r)/r³
```

**Electric Field:**
```
E(r) = [3(p·r̂)r̂ - p]/r³
```

**On Axis (p || r̂):**
```
E = 2p/r³
```

**Perpendicular (p ⊥ r̂):**
```
E = -p/r³
```

**Validation:** Implemented in `electric_field_dipole()`

---

### Standard Geometries

#### Conducting Sphere (Grounded)
**Maxwell Articles:** 144-146, 155-160

**In Uniform Field E₀:**
```
V(r,θ) = -E₀(r - a³/r²)cos θ
E_r = E₀(1 + 2a³/r³)cos θ
E_θ = -E₀(1 - a³/r³)sin θ
```

**Induced Surface Charge:**
```
σ(θ) = (3E₀/4π)cos θ
```

**Total Induced Dipole:**
```
p = E₀a³
```

**Validation:** Implemented in `conducting_sphere_uniform_field()`

---

#### Point Charge Near Conducting Sphere
**Maxwell Articles:** 166-170

**Image Charge:**
```
q' = -(a/d)q  at r' = a²/d
```

**Force on Charge:**
```
F = q²a³(2d² - a²) / [d³(d² - a²)²]
```

**Validation:** Implemented in `image_charge_sphere()`

---

#### Dielectric Sphere in Uniform Field
**Maxwell Articles:** 144-146

**Inside (r < a):**
```
E_in = [3/(ε+2)] E₀  (uniform)
```

**Outside (r > a):**
```
V_out = -E₀r cos θ + [(ε-1)/(ε+2)] (a³/r²) E₀ cos θ
```

**Induced Dipole:**
```
p = [(ε-1)/(ε+2)] a³ E₀
```

**Validation:** Implemented in `dielectric_sphere_uniform_field()`

---

#### Parallel Plate Capacitor
**Maxwell Articles:** 124

**Field (ignoring edge effects):**
```
E = 4πσ = 4πQ/A
```

**Capacitance:**
```
C = A/(4πd)  (CGS)
```

**Energy:**
```
U = (1/2)QV = (1/2)CV²
```

**Validation:** Implemented in `parallel_plate_capacitor()`

---

#### Concentric Spherical Capacitor
**Maxwell Articles:** 125

**Capacitance:**
```
C = ab/(b-a)  (CGS)
```

where a = inner radius, b = outer radius

**Validation:** Implemented in `concentric_spheres_capacitor()`

---

#### Infinite Line Charge
**Maxwell Articles:** 126-127

**Electric Field:**
```
E = (2λ/r) r̂
```

**Potential:**
```
V(r) = -2λ ln(r/r₀)
```

**Validation:** Implemented in `infinite_line_charge()`

---

#### Infinite Plane Sheet
**Maxwell Articles:** 124

**Electric Field:**
```
E = 2πσ  (constant, independent of distance)
```

**Discontinuity:**
```
E_above - E_below = 4πσ
```

**Validation:** Implemented in `infinite_plane_sheet()`

---

## Magnetostatic Solutions (Part III)

### Point Sources

#### Magnetic Dipole
**Maxwell Articles:** 385-392

**Vector Potential:**
```
A(r) = (m × r̂)/r²
```

**Magnetic Field:**
```
B(r) = [3(m·r̂)r̂ - m]/r³
```

**Same form as electric dipole**

**Validation:** Implemented in `magnetic_dipole_field()`

---

### Standard Geometries

#### Circular Current Loop (On Axis)
**Maxwell Articles:** 694-696

**On Axis (z):**
```
B_z = (2πIa²) / [c(a² + z²)³/²]
```

**At Center (z = 0):**
```
B = (2πI)/(ca)
```

**Far Field (z >> a):**
```
B ≈ (2πIa²)/(cz³) = 2m/z³  (dipole)
```

where m = πa²I/c (magnetic moment)

**Validation:** Implemented in `circular_loop_on_axis()`

---

#### Infinite Solenoid
**Maxwell Articles:** 675-677

**Inside:**
```
B = (4πnI)/c  (uniform)
```

where n = turns per unit length

**Outside:**
```
B = 0  (ideal infinite solenoid)
```

**Validation:** Implemented in `infinite_solenoid_field()`

---

#### Finite Solenoid (On Axis)
**Maxwell Articles:** 675-677

**On Axis:**
```
B_z = (2πnI/c)(cos θ₁ - cos θ₂)
```

where θ₁, θ₂ are angles from observation point to ends

**At Center (length L, radius a):**
```
B = (4πnI/c) · L/√(L² + 4a²)
```

**Validation:** Implemented in `finite_solenoid_on_axis()`

---

#### Straight Wire (Infinite)
**Maxwell Articles:** 475-479

**Magnetic Field:**
```
B = (2I)/(cr)  (azimuthal)
```

**Validation:** Implemented in `infinite_straight_wire()`

---

## Time-Varying Solutions (Part IV)

### Plane Waves

#### Plane Wave in Vacuum
**Maxwell Articles:** 790-793

**Electric Field:**
```
E(r,t) = E₀ cos(k·r - ωt + φ)
```

**Magnetic Field:**
```
B(r,t) = k̂ × E(r,t)  (|B| = |E| in CGS)
```

**Dispersion:**
```
ω = ck
```

**Poynting Vector:**
```
S = (c/4π) E × B = (c/4π) E₀² k̂ cos²(k·r - ωt)
```

**Time-Averaged Intensity:**
```
<I> = (c/8π) E₀²
```

**Validation:** Implemented in `plane_wave_vacuum()`

---

#### Plane Wave in Dielectric
**Maxwell Articles:** 788-789

**Wave Speed:**
```
v = c/√(εμ) = c/n
```

**Impedance:**
```
|E|/|H| = √(μ/ε)
```

**Validation:** Implemented in `plane_wave_dielectric()`

---

#### Plane Wave in Conductor
**Maxwell Articles:** 798-801

**Skin Depth:**
```
δ = √(2c²/σω) = c/√(2πσω)  (CGS)
```

**Field Decay:**
```
E(z) = E₀ e^(-z/δ) e^(i(kz - ωt))
```

**Validation:** Implemented in `plane_wave_conductor()`

---

### Waveguide Solutions

#### Rectangular Waveguide TE₁₀ Mode
**Maxwell Articles:** 675-677 (related)

**Cutoff Frequency:**
```
f_c = c/(2a)  (TE₁₀ mode)
```

where a = wider dimension

**Propagation Constant:**
```
β = √(k² - k_c²) = (ω/c)√(1 - (f_c/f)²)
```

**Validation:** Implemented in `rectangular_waveguide_te10()`

---

#### Cavity Resonator (Rectangular)

**Resonant Frequency:**
```
f_mnp = (c/2)√[(m/a)² + (n/b)² + (p/d)²]
```

**TE₁₀₁ Mode:**
```
f₁₀₁ = (c/2)√[(1/a)² + (1/d)²]
```

**Validation:** Implemented in `rectangular_cavity_modes()`

---

### Radiation Solutions

#### Hertzian Dipole (Short Dipole)
**Maxwell Articles:** 475-490

**Radiated Power:**
```
P = (ω⁴p²)/(3c³)  (CGS)
```

where p = dipole moment amplitude

**Radiation Pattern:**
```
dP/dΩ = (ω⁴p²/8πc³) sin²θ
```

**Validation:** Implemented in `hertzian_dipole_radiation()`

---

## Validation Summary

| Solution | Module | Test Function | Status |
|----------|--------|---------------|--------|
| Point charge | electrostatics/field.py | test_point_charge() | ✓ |
| Electric dipole | electrostatics/field.py | test_dipole() | ✓ |
| Conducting sphere | electrostatics/sphere.py | test_sphere_field() | ✓ |
| Dielectric sphere | electrostatics/dielectric.py | test_dielectric_sphere() | ✓ |
| Parallel plate | components/plates.py | test_capacitor() | ✓ |
| Magnetic dipole | magnetostatics/dipole.py | test_magnetic_dipole() | ✓ |
| Circular loop | magnetostatics/loop.py | test_loop_axis() | ✓ |
| Infinite solenoid | magnetostatics/solenoid.py | test_solenoid() | ✓ |
| Plane wave | optics/wave_equation.py | test_plane_wave() | ✓ |
| Waveguide | optics/waveguide.py | test_waveguide_cutoff() | ✓ |

## Usage Notes

1. All formulas use CGS Gaussian units
2. For SI conversion, apply appropriate factors
3. Validation tests compare numerical output to analytical formula
4. Tolerance depends on numerical method used
