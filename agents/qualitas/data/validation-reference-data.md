# Validation Reference Data

## Purpose

Reference data for validation tests including analytical solutions, physical constants, and benchmark values.

## Analytical Solution Reference Values

### Point Charge (Art. 44-49)
```
q = 1 statcoulomb
r = 1 cm
Expected: E = 1.0 statvolt/cm (radial)
```

### Electric Dipole (Art. 69-71)
```
p = 1 statcoulomb·cm (z-direction)
r = 1 cm (on axis)
Expected: E = 2.0 statvolt/cm (z-direction)

r = 1 cm (perpendicular)
Expected: E = 1.0 statvolt/cm (-z-direction)
```

### Conducting Sphere (Art. 144-146)
```
a = 1 cm (radius)
E_0 = 1 statvolt/cm (applied field)
At surface (θ=0): E = 3.0 statvolt/cm
```

### Infinite Solenoid (Art. 675-677)
```
n = 100 turns/cm
I = 1 statampere
Expected: B = 4πnI/c = 4.19 gauss
```

### Plane Wave Speed (Art. 786-787)
```
ε_r = 1, μ_r = 1 (vacuum)
Expected: v = c = 29979245800 cm/s
```

## Physical Constants (CGS)

| Constant | Symbol | Value |
|----------|--------|-------|
| Speed of light | c | 29979245800 cm/s |
| Electron charge | e | 4.80320471e-10 statcoulomb |
| Electron mass | m_e | 9.10938370e-28 g |

## Material Property Reference

| Material | Property | Value | Units |
|----------|----------|-------|-------|
| Copper | σ | 5.96e17 | s⁻¹ |
| Water | ε_r | 80.4 | dimensionless |
| Iron | μ_r (max) | 200000 | dimensionless |

## Usage

Use these reference values for validation test assertions.
