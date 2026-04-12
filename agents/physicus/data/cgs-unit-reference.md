# CGS Unit Reference

## Purpose

Authoritative reference for CGS (centimeter-gram-second) units used throughout Maxwell's Treatise and this implementation. All physics functions use CGS units by default.

## Base Units

| Quantity | Unit | Symbol | Definition |
|----------|------|--------|------------|
| Length | centimeter | cm | 1/100 of meter |
| Mass | gram | g | 1/1000 of kilogram |
| Time | second | s | SI second |

## Derived Mechanical Units

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Velocity | cm/s | dx/dt | L·T⁻¹ | 0.01 m/s |
| Acceleration | cm/s² | dv/dt | L·T⁻² | 0.01 m/s² |
| Force | dyne | g·cm/s² | M·L·T⁻² | 10⁻⁵ N |
| Energy | erg | dyne·cm | M·L²·T⁻² | 10⁻⁷ J |
| Power | erg/s | dyne·cm/s | M·L²·T⁻³ | 10⁻⁷ W |
| Pressure | dyne/cm² | force/area | M·L⁻¹·T⁻² | 0.1 Pa |

## Electrostatic Units (ESU)

### Charge and Current

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Charge | statcoulomb (esu) | √(dyne)·cm | M¹/²·L³/²·T⁻¹ | 3.336×10⁻¹⁰ C |
| Current | statampere | statcoulomb/s | M¹/²·L³/²·T⁻² | 1.112×10⁻¹² A |
| Charge density | statcoulomb/cm³ | charge/volume | M¹/²·L⁻³/²·T⁻¹ | 3.336×10⁻⁴ C/m³ |
| Current density | statampere/cm² | current/area | M¹/²·L⁻¹/²·T⁻² | 1.112×10⁻⁸ A/m² |

### Field Quantities

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Electric field | statvolt/cm | dyne/statcoulomb | M¹/²·L⁻¹/²·T⁻¹ | 29979 V/m |
| Potential | statvolt | erg/statcoulomb | M¹/²·L¹/²·T⁻¹ | 299.79 V |
| Displacement D | statvolt/cm | same as E | M¹/²·L⁻¹/²·T⁻¹ | 29979 V/m |
| Polarization P | statvolt/cm | dipole/volume | M¹/²·L⁻¹/²·T⁻¹ | 29979 V/m |

### Circuit Quantities

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Resistance | statohm | statvolt/statampere | L⁻¹·T | 8.988×10¹¹ Ω |
| Capacitance | statfarad | statcoulomb/statvolt | L | 1.113×10⁻¹² F |
| Conductance | statmho | 1/statohm | L·T⁻¹ | 1.113×10⁻¹² S |

## Electromagnetic Units (EMU)

### Magnetic Quantities

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Magnetic field H | oersted | dyne/pole | M¹/²·L⁻¹/²·T⁻¹ | 79.577 A/m |
| Magnetic induction B | gauss | dyne/(pole·cm/s) | M¹/²·L⁻¹/²·T⁻¹ | 10⁻⁴ T |
| Magnetization M | erg/(gauss·cm³) | dipole/volume | M¹/²·L⁻¹/²·T⁻¹ | 1000 A/m |
| Magnetic moment | erg/gauss | pole·cm | M¹/²·L⁵/²·T⁻¹ | 10⁻³ A·m² |
| Flux | maxwell | gauss·cm² | M¹/²·L⁵/²·T⁻¹ | 10⁻⁸ Wb |

### Circuit Quantities

| Quantity | Unit | Formula | CGS Dimensions | SI Equivalent |
|----------|------|---------|----------------|---------------|
| Current | abampere (emu) | √(dyne) | M¹/²·L¹/²·T⁻¹ | 10 A |
| Resistance | abohm | abvolt/abampere | L·T⁻¹ | 10⁻⁹ Ω |
| Inductance | cm (emu) | length | L | 10⁻⁹ H |
| Conductance | abmho | 1/abohm | L⁻¹·T | 10⁹ S |

## CGS Gaussian (Mixed) Units

Maxwell's Treatise uses Gaussian units, which combine ESU for electric quantities and EMU for magnetic quantities.

### Key Relations

| Relation | CGS Gaussian | SI Equivalent |
|----------|--------------|---------------|
| Lorentz force | F = q(E + v/c × B) | F = q(E + v × B) |
| Faraday's law | ∇×E = -(1/c)∂B/∂t | ∇×E = -∂B/∂t |
| Ampère-Maxwell | ∇×H = (4π/c)J + (1/c)∂D/∂t | ∇×H = J + ∂D/∂t |
| B in vacuum | B = H | B = μ₀H |

### Constitutive Relations

| Relation | CGS Gaussian | SI |
|----------|--------------|-----|
| Electric | D = E + 4πP = εE | D = ε₀E + P = ε₀ε_rE |
| Magnetic | B = H + 4πM = μH | B = μ₀(H + M) = μ₀μ_rH |
| Ohm's law | J = σE | J = σE |

### Permittivity and Permeability

| Quantity | CGS | SI | Conversion |
|----------|-----|-----|------------|
| ε₀ (vacuum permittivity) | 1/(4π) | 8.854×10⁻¹² F/m | ε₀_CGS = 1 |
| μ₀ (vacuum permeability) | 4π/c² | 4π×10⁻⁷ H/m | μ₀_CGS = 1 |
| ε_r (relative permittivity) | dimensionless | dimensionless | Same |
| μ_r (relative permeability) | dimensionless | dimensionless | Same |

## Speed of Light

| Quantity | Value | Units |
|----------|-------|-------|
| c (exact) | 2.99792458×10¹⁰ | cm/s |
| c² | 8.987551787×10²⁰ | cm²/s² |
| 1/c | 3.335640952×10⁻¹¹ | s/cm |

## Fundamental Constants (CGS)

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Speed of light | c | 2.99792458×10¹⁰ | cm/s |
| Electron charge | e | 4.8032047×10⁻¹⁰ | statcoulomb |
| Electron mass | m_e | 9.1093837×10⁻²⁸ | g |
| Proton mass | m_p | 1.6726219×10⁻²⁴ | g |
| Planck constant | ℏ | 1.0545718×10⁻²⁷ | erg·s |
| Gravitational constant | G | 6.67430×10⁻⁸ | dyne·cm²/g² |
| Boltzmann constant | k_B | 1.380649×10⁻¹⁶ | erg/K |
| Avogadro number | N_A | 6.02214076×10²³ | mol⁻¹ |
| Gas constant | R | 8.314462618×10⁷ | erg/(mol·K) |
| Stefan-Boltzmann | σ | 5.670374419×10⁻⁵ | erg/(cm²·s·K⁴) |

## Common Conversions

### Length
| CGS | SI |
|-----|-----|
| 1 cm | 0.01 m |
| 1 Å | 10⁻⁸ cm |

### Force and Energy
| CGS | SI |
|-----|-----|
| 1 dyne | 10⁻⁵ N |
| 1 erg | 10⁻⁷ J |
| 1 erg/s | 10⁻⁷ W |

### Electromagnetic
| CGS | SI |
|-----|-----|
| 1 statcoulomb | 3.336×10⁻¹⁰ C |
| 1 statvolt | 299.79 V |
| 1 gauss | 10⁻⁴ T |
| 1 oersted | 79.577 A/m |

### Practical Units
| CGS | Practical |
|-----|-----------|
| 1 statvolt/cm | 29979 V/m |
| 1 gauss | 1 maxwell/cm² |
| 1 cm (inductance) | 1 nanohenry |

## Dimensional Analysis Examples

### Electrostatic Energy Density
```
[u] = [E²/8π] = (statvolt/cm)²
    = (dyne/statcoulomb)²
    = (g·cm/s² / (g¹/²·cm³/²/s))²
    = (g¹/²·cm⁻¹/²/s)²
    = g·cm⁻¹·s⁻²
    = erg/cm³ ✓
```

### Magnetic Field from Current
```
[B] from Biot-Savart: (I/c)·(dl/r²)
    = (statampere / (cm/s)) · (cm/cm²)
    = (statcoulomb/s · s/cm) · (1/cm)
    = statcoulomb/cm²
    = gauss (after unit conversion) ✓
```
