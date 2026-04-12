# CGS Unit Dimensional Reference

## Purpose

Dimensional analysis reference for CGS unit validation.

## Base Dimensions

| Quantity | Dimension | Unit |
|----------|-----------|------|
| Length | L | cm |
| Mass | M | g |
| Time | T | s |
| Charge | Q = M¹/²L³/²T⁻¹ | statcoulomb |

## Derived Dimensions

| Quantity | Dimension | CGS Unit |
|----------|-----------|----------|
| Force | MLT⁻² | dyne |
| Energy | ML²T⁻² | erg |
| Electric field | M¹/²L⁻¹/²T⁻¹ | statvolt/cm |
| Magnetic field | M¹/²L⁻¹/²T⁻¹ | gauss |
| Potential | M¹/²L¹/²T⁻¹ | statvolt |

## Dimensional Checks

### Energy Density
```
[E²/8π] = (M¹/²L⁻¹/²T⁻¹)² = ML⁻¹T⁻² = erg/cm³ ✓
```

### Force from Field
```
[qE] = (M¹/²L³/²T⁻¹)(M¹/²L⁻¹/²T⁻¹) = MLT⁻² = dyne ✓
```

## Usage

Use for validating dimensional consistency of equations.
