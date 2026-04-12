# Material Properties Reference

## Purpose

Reference data for electromagnetic material properties in CGS units. This document provides standard values for permittivity, permeability, conductivity, and other material parameters.

## Dielectric Materials (Part I)

### Vacuum
| Property | Symbol | Value | Units |
|----------|--------|-------|-------|
| Permittivity | ε | 1 | dimensionless |
| Permeability | μ | 1 | dimensionless |
| Breakdown field | - | ∞ | - |

---

### Gases (at STP)

| Material | ε_r | μ_r | Breakdown (statvolt/cm) | Notes |
|----------|-----|-----|------------------------|-------|
| Air | 1.00059 | 1.00000037 | 30 | Dry air at 1 atm |
| Nitrogen | 1.00055 | ~1 | 30 | |
| Oxygen | 1.00050 | 1.000002 | 30 | Paramagnetic |
| CO₂ | 1.00098 | ~1 | 30 | |
| Hydrogen | 1.00027 | ~1 | 30 | |

---

### Liquids

| Material | ε_r | μ_r | σ (s⁻¹) | Notes |
|----------|-----|-----|---------|-------|
| Distilled water | 80.4 | ~1 | 10⁻⁶ - 10⁻⁴ | 20°C |
| Sea water | ~80 | ~1 | 5×10¹⁰ | High conductivity |
| Ethanol | 24.3 | ~1 | 10⁻⁸ | |
| Methanol | 32.7 | ~1 | 10⁻⁷ | |
| Benzene | 2.28 | ~1 | 10⁻¹⁵ | Nonpolar |
| Transformer oil | 2.2 | ~1 | 10⁻¹⁴ | Insulating |
| Mercury | ~1 | ~1 | 10¹⁷ | Conductor |

---

### Solids: Insulators

| Material | ε_r | μ_r | Breakdown (statvolt/cm) | Notes |
|----------|-----|-----|------------------------|-------|
| Fused silica | 3.78 | ~1 | 800 | |
| Pyrex glass | 4.7 | ~1 | 400 | |
| Flint glass | 10 | ~1 | 300 | High index |
| Mica | 5.4-8.7 | ~1 | 1000 | Layered |
| Paraffin wax | 2.2 | ~1 | 300 | |
| Polystyrene | 2.5 | ~1 | 500 | |
| Teflon (PTFE) | 2.1 | ~1 | 500 | Low loss |
| Polyethylene | 2.25 | ~1 | 500 | |
| PVC | 3.0-3.5 | ~1 | 400 | |
| Rubber | 2.5-3.0 | ~1 | 300 | |
| Paper (dry) | 3.0 | ~1 | 200 | |
| Porcelain | 5.5-6.5 | ~1 | 150 | |
| Alumina (Al₂O₃) | 9.0 | ~1 | 300 | Ceramic |

---

### Solids: Semiconductors

| Material | ε_r | μ_r | σ (s⁻¹) | Notes |
|----------|-----|-----|---------|-------|
| Silicon (intrinsic) | 11.7 | ~1 | 10⁻⁴ | 300K |
| Germanium (intrinsic) | 16.0 | ~1 | 10² | 300K |
| GaAs | 12.9 | ~1 | 10⁻⁶ | |
| Silicon (n-type) | 11.7 | ~1 | 10⁸ - 10¹⁴ | Doped |

---

## Conductors (Part II)

### Metals (Conductivity at 20°C)

| Material | σ (s⁻¹, CGS) | σ (S/m, SI) | ρ (Ω·cm) | α (1/K) | Notes |
|----------|--------------|-------------|----------|---------|-------|
| Silver | 6.80×10¹⁷ | 6.30×10⁷ | 1.59×10⁻⁶ | 0.0038 | Best conductor |
| Copper (annealed) | 5.96×10¹⁷ | 5.96×10⁷ | 1.68×10⁻⁶ | 0.0039 | Standard |
| Copper (hard) | 5.80×10¹⁷ | 5.80×10⁷ | 1.72×10⁻⁶ | 0.0039 | |
| Gold | 4.50×10¹⁷ | 4.50×10⁷ | 2.21×10⁻⁶ | 0.0034 | Corrosion resistant |
| Aluminum | 3.77×10¹⁷ | 3.77×10⁷ | 2.65×10⁻⁶ | 0.0043 | Lightweight |
| Calcium | 2.98×10¹⁷ | 2.98×10⁷ | 3.36×10⁻⁶ | 0.0049 | |
| Tungsten | 1.89×10¹⁷ | 1.89×10⁷ | 5.28×10⁻⁶ | 0.0045 | High melting |
| Zinc | 1.69×10¹⁷ | 1.69×10⁷ | 5.90×10⁻⁶ | 0.0037 | |
| Nickel | 1.43×10¹⁷ | 1.43×10⁷ | 6.99×10⁻⁶ | 0.0060 | Ferromagnetic |
| Iron (pure) | 1.03×10¹⁷ | 1.03×10⁷ | 9.71×10⁻⁶ | 0.0050 | Ferromagnetic |
| Platinum | 9.43×10¹⁶ | 9.43×10⁶ | 1.06×10⁻⁵ | 0.0039 | |
| Tin | 9.17×10¹⁶ | 9.17×10⁶ | 1.09×10⁻⁵ | 0.0045 | |
| Steel (carbon) | 6.0×10¹⁶ | 6.0×10⁶ | 1.7×10⁻⁵ | 0.003 | Alloy |
| Lead | 4.80×10¹⁶ | 4.80×10⁶ | 2.08×10⁻⁵ | 0.0039 | |
| Stainless steel | 1.4×10¹⁶ | 1.4×10⁶ | 7.2×10⁻⁵ | 0.001 | Alloy |
| Mercury | 1.04×10¹⁶ | 1.04×10⁶ | 9.6×10⁻⁵ | 0.0009 | Liquid |
| Nichrome | 1.0×10¹⁶ | 1.0×10⁶ | 1.0×10⁻⁴ | 0.0004 | Heating element |
| Graphite | 2-3×10¹⁴ | 2-3×10⁴ | 3-5×10⁻³ | -0.0005 | Anisotropic |

Notes:
- σ_CGS = σ_SI × (1/1.112×10⁻¹¹)
- Temperature coefficient: σ(T) = σ₀[1 + α(T - T₀)]⁻¹

---

### Electrolytes

| Electrolyte | Concentration | Conductivity (s⁻¹, CGS) | Notes |
|-------------|---------------|------------------------|-------|
| NaCl (aq) | 1 M | ~10¹¹ | Strong electrolyte |
| KCl (aq) | 1 M | ~1.3×10¹¹ | Standard |
| H₂SO₄ (aq) | 1 M | ~4×10¹¹ | Battery acid |
| CuSO₄ (aq) | 1 M | ~10¹¹ | Plating |
| NaOH (aq) | 1 M | ~2×10¹¹ | Caustic |

---

## Magnetic Materials (Part III)

### Diamagnetic Materials (κ < 0)

| Material | χ (dimensionless) | μ_r | Notes |
|----------|------------------|-----|-------|
| Bismuth | -1.66×10⁻⁴ | 0.999834 | Strongest diamagnet |
| Pyrolytic carbon | -4.4×10⁻⁴ | 0.99956 | Levitates |
| Water | -9.0×10⁻⁶ | 0.999991 | |
| Copper | -9.8×10⁻⁶ | 0.999990 | |
| Silver | -2.6×10⁻⁵ | 0.999974 | |
| Gold | -3.4×10⁻⁵ | 0.999966 | |
| Silicon | -4.2×10⁻⁶ | 0.999996 | |

---

### Paramagnetic Materials (κ > 0, small)

| Material | χ (dimensionless) | μ_r | Notes |
|----------|------------------|-----|-------|
| Aluminum | 2.2×10⁻⁵ | 1.000022 | |
| Platinum | 2.9×10⁻⁴ | 1.00029 | |
| Oxygen (liquid) | 3.5×10⁻³ | 1.0035 | |
| Manganese | 1.0×10⁻⁴ | 1.00010 | |
| Tungsten | 6.8×10⁻⁵ | 1.000068 | |

---

### Ferromagnetic Materials (κ >> 1)

| Material | χ_initial | χ_max | μ_r_max | B_sat (gauss) | H_c (oersted) | Notes |
|----------|-----------|-------|---------|---------------|---------------|-------|
| Iron (pure) | 200 | 5000 | 200000 | 21800 | 0.05 | Soft |
| Iron (99.95%) | - | - | 250000 | 21500 | 0.02 | Annealed |
| Steel (0.2% C) | - | - | 2000 | 20000 | 50 | Hard |
| Permalloy (78% Ni) | 8000 | 100000 | 100000 | 10500 | 0.01 | Very soft |
| Mu-metal | 20000 | 300000 | 300000 | 8000 | 0.002 | Shielding |
| Silicon steel | 1500 | 7000 | 7000 | 20000 | 0.3 | Transformer |
| Alnico 5 | - | - | 4 | 12800 | 640 | Permanent |
| Ferrite (Mn-Zn) | 1000 | 5000 | 5000 | 5000 | 0.1 | High freq |
| Ferrite (Ni-Zn) | 100 | 500 | 500 | 3000 | 0.5 | High freq |

Notes:
- B_sat = saturation flux density
- H_c = coercivity
- χ_initial = initial susceptibility
- χ_max = maximum susceptibility
- μ_r = 1 + 4πχ (CGS)

---

## Temperature Dependence

### Conductivity Temperature Coefficient

```
σ(T) = σ₀ / [1 + α(T - T₀)]
```

| Material | α (1/K) | T₀ (°C) |
|----------|---------|---------|
| Copper | 0.0039 | 20 |
| Aluminum | 0.0043 | 20 |
| Iron | 0.0050 | 20 |
| Tungsten | 0.0045 | 20 |
| Platinum | 0.0039 | 20 |
| Carbon | -0.0005 | 20 |

### Permittivity Temperature Coefficient

| Material | dε/dT (1/K) | Notes |
|----------|-------------|-------|
| Water | -0.004 | 20°C |
| Barium titanate | 0.02 | Near Curie point |
| Fused silica | 0.0001 | Stable |

### Magnetic Properties Temperature Dependence

| Material | Curie Temperature (K) | Notes |
|----------|----------------------|-------|
| Iron | 1043 | Above: paramagnetic |
| Nickel | 631 | |
| Cobalt | 1388 | |
| Gadolinium | 293 | Near room temp |

---

## Frequency Dependence

### Complex Permittivity

```
ε(ω) = ε' - iε''
```

| Material | Frequency | ε' | ε'' | Loss Tangent |
|----------|-----------|-----|-----|--------------|
| Water | 1 GHz | 80 | 10 | 0.12 |
| Water | 10 GHz | 65 | 25 | 0.38 |
| FR4 PCB | 1 GHz | 4.5 | 0.15 | 0.03 |
| Teflon | 10 GHz | 2.1 | 0.001 | 0.0005 |

---

## Usage Notes

1. All conductivity values in CGS (s⁻¹)
2. For SI: σ_SI = σ_CGS × 1.112×10⁻¹¹
3. Temperature coefficients are approximate
4. Values vary with purity, processing, and measurement method
5. For validation: compare with handbook values at specified conditions
